from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_core import apply, sync
from test_agent_core import commit_all, initialize_repo, write_config, write_skill


class PythonSkillRetirementTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "canonical"
        initialize_repo(self.checkout)
        self.home = self.root / "home"
        self.home.mkdir()
        self.app_data = self.root / "AppData/Roaming"
        self.environment = patch.dict(os.environ, {"APPDATA": str(self.app_data)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        for name in (*sync.RETIRED_PYTHON_SKILLS, "unrelated"):
            write_skill(self.checkout, name, "old content")
        write_config(self.checkout, [*sync.RETIRED_PYTHON_SKILLS, "unrelated"])
        commit_all(self.checkout, "old skills")

    def publish(self, harness):
        return sync.sync_checkout(self.checkout, self.home, harness, app_data=self.app_data)

    def target(self, harness, name):
        if harness == "pi":
            base = self.home / ".pi/agent"
        elif harness == "devin":
            base = self.app_data / "devin"
        else:
            base = self.home / ".config/opencode"
        return base / "skills" / name

    def replace_manifest(self):
        write_skill(self.checkout, sync.PYTHON_SKILL_REPLACEMENT, "new workflow")
        write_config(self.checkout, [sync.PYTHON_SKILL_REPLACEMENT])
        commit_all(self.checkout, "consolidate Python")

    def test_selected_harness_only_owned_predecessors_retired_and_idempotent(self):
        for harness in ("pi", "devin", "opencode"):
            self.publish(harness)
        self.replace_manifest()
        for harness in ("pi", "devin", "opencode"):
            with self.subTest(harness=harness):
                result = self.publish(harness)
                self.assertEqual(len(result.legacy), 2)
                self.assertTrue(self.target(harness, sync.PYTHON_SKILL_REPLACEMENT).is_dir())
                self.assertTrue(self.target(harness, "unrelated").is_dir())
                for old in sync.RETIRED_PYTHON_SKILLS:
                    self.assertFalse(self.target(harness, old).exists())
                if harness == "pi":
                    self.assertTrue(self.target("devin", sync.RETIRED_PYTHON_SKILLS[0]).exists())
                    self.assertTrue(self.target("opencode", sync.RETIRED_PYTHON_SKILLS[0]).exists())
                self.assertEqual(self.publish(harness).legacy, [])
        state = json.loads(sync.global_state_path(self.home).read_text())
        for key in ("skills", "devin_skills", "opencode_skills"):
            self.assertIn("unrelated", state[key])
            self.assertNotIn(sync.RETIRED_PYTHON_SKILLS[0], state[key])

    def test_modified_owned_predecessor_blocks_before_publication(self):
        for harness in ("pi", "devin", "opencode"):
            self.publish(harness)
        self.replace_manifest()
        for harness in ("pi", "devin", "opencode"):
            old = self.target(harness, sync.RETIRED_PYTHON_SKILLS[0]) / "SKILL.md"
            old.write_text("human customization")
            before = sync.global_state_path(self.home).read_bytes()
            with self.subTest(harness=harness), self.assertRaisesRegex(sync.SyncError, "locally modified"):
                self.publish(harness)
            self.assertEqual(old.read_text(), "human customization")
            self.assertEqual(sync.global_state_path(self.home).read_bytes(), before)
            self.assertFalse(self.target(harness, sync.PYTHON_SKILL_REPLACEMENT).exists())

    def test_unowned_predecessor_preserved_and_reported(self):
        self.replace_manifest()
        for harness in ("pi", "devin", "opencode"):
            old = self.target(harness, sync.RETIRED_PYTHON_SKILLS[1])
            old.mkdir(parents=True)
            (old / "SKILL.md").write_text("unowned")
            with self.subTest(harness=harness), self.assertRaisesRegex(sync.SyncError, "unowned") as error:
                self.publish(harness)
            self.assertIn(str(old), str(error.exception))
            self.assertEqual((old / "SKILL.md").read_text(), "unowned")
            self.assertFalse(self.target(harness, sync.PYTHON_SKILL_REPLACEMENT).exists())

    def test_state_failure_restores_old_skills_and_preserves_other_harness(self):
        for harness in ("pi", "devin", "opencode"):
            self.publish(harness)
        self.replace_manifest()
        before = sync.global_state_path(self.home).read_bytes()
        for harness in ("pi", "devin", "opencode"):
            with self.subTest(harness=harness), patch.object(apply, "_atomic_write", side_effect=OSError("injected")), self.assertRaisesRegex(sync.SyncError, "injected"):
                self.publish(harness)
            self.assertEqual(sync.global_state_path(self.home).read_bytes(), before)
            self.assertFalse(self.target(harness, sync.PYTHON_SKILL_REPLACEMENT).exists())
            for other in ("pi", "devin", "opencode"):
                for old in sync.RETIRED_PYTHON_SKILLS:
                    self.assertTrue((self.target(other, old) / "SKILL.md").is_file())

    def test_missing_predecessor_clears_ownership_without_failure(self):
        self.publish("pi")
        for old in sync.RETIRED_PYTHON_SKILLS:
            shutil.rmtree(self.target("pi", old))
        self.replace_manifest()
        self.publish("pi")
        state = json.loads(sync.global_state_path(self.home).read_text())
        self.assertNotIn(sync.RETIRED_PYTHON_SKILLS[0], state["skills"])

    def test_removed_names_are_not_pruned_without_replacement_selected(self):
        self.publish("pi")
        write_config(self.checkout, ["unrelated"])
        commit_all(self.checkout, "deselect only")
        self.publish("pi")
        self.assertTrue(self.target("pi", sync.RETIRED_PYTHON_SKILLS[0]).is_dir())

    def test_legacy_owned_predecessors_retired_by_pi_only(self):
        self.publish("pi")
        state_path = sync.global_state_path(self.home)
        state = json.loads(state_path.read_text())
        for old in sync.RETIRED_PYTHON_SKILLS:
            legacy = self.home / ".agents/skills" / old
            legacy.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(self.target("pi", old)), legacy)
            state["skills"][old]["destination"] = str(legacy.resolve())
        state_path.write_text(json.dumps(state))
        self.replace_manifest()
        self.publish("devin")
        self.assertTrue((self.home / ".agents/skills" / sync.RETIRED_PYTHON_SKILLS[0]).is_dir())
        self.publish("pi")
        for old in sync.RETIRED_PYTHON_SKILLS:
            self.assertFalse((self.home / ".agents/skills" / old).exists())

    def test_preflight_detects_predecessor_changed_during_staging(self):
        self.publish("pi")
        self.replace_manifest()
        original_copy = shutil.copytree
        old = self.target("pi", sync.RETIRED_PYTHON_SKILLS[0]) / "SKILL.md"
        def mutate_then_copy(*args, **kwargs):
            old.write_text("concurrent edit")
            return original_copy(*args, **kwargs)
        with patch.object(shutil, "copytree", side_effect=mutate_then_copy), self.assertRaisesRegex(sync.SyncError, "locally modified"):
            self.publish("pi")
        self.assertEqual(old.read_text(), "concurrent edit")
        self.assertFalse(self.target("pi", sync.PYTHON_SKILL_REPLACEMENT).exists())

    def test_legacy_alias_rollback_and_retirement(self):
        self.publish("pi")
        old = sync.RETIRED_PYTHON_SKILLS[0]
        legacy = self.home / ".agents/skills" / old
        legacy.parent.mkdir(parents=True)
        shutil.move(str(self.target("pi", old)), legacy)
        alias = self.home / ".claude/skills" / old
        alias.parent.mkdir(parents=True)
        if os.name == "nt":
            result = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(legacy)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            alias.symlink_to(legacy, target_is_directory=True)
        state_path = sync.global_state_path(self.home)
        state = json.loads(state_path.read_text())
        state["skills"][old]["destination"] = str(legacy.resolve())
        state["aliases"][old] = {"destination": str(alias), "target": str(legacy)}
        state_path.write_text(json.dumps(state))
        self.replace_manifest()
        before = state_path.read_bytes()
        with patch.object(apply, "_atomic_write", side_effect=OSError("injected")), self.assertRaisesRegex(sync.SyncError, "injected"):
            self.publish("pi")
        self.assertEqual(before, state_path.read_bytes())
        self.assertTrue(sync._alias_matches(alias, legacy))
        self.publish("pi")
        self.assertFalse(apply._lexists(alias))
        self.assertFalse(legacy.exists())
        self.assertNotIn(old, json.loads(state_path.read_text())["aliases"])

    def test_unsupported_predecessor_type_preserved(self):
        for harness in ("pi", "devin", "opencode"):
            self.publish(harness)
        self.replace_manifest()
        for harness in ("pi", "devin", "opencode"):
            old = self.target(harness, sync.RETIRED_PYTHON_SKILLS[0])
            shutil.rmtree(old)
            old.write_text("not a directory")
            with self.subTest(harness=harness), self.assertRaisesRegex(sync.SyncError, "Unsafe obsolete"):
                self.publish(harness)
            self.assertEqual(old.read_text(), "not a directory")
            self.assertFalse(self.target(harness, sync.PYTHON_SKILL_REPLACEMENT).exists())

    def test_conflicting_manifest_names_refused(self):
        self.replace_manifest()
        write_config(self.checkout, [sync.PYTHON_SKILL_REPLACEMENT, sync.RETIRED_PYTHON_SKILLS[0]])
        commit_all(self.checkout, "invalid coexistence")
        with self.assertRaisesRegex(sync.SyncError, "Conflicting Python"):
            self.publish("pi")
