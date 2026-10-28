from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import tempfile
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from agent_core import apply, bootstrap, retire, sync
from agent_core.devin_manifest import (
    DEVIN_MANIFEST_FILENAME,
    DevinManifestError,
    load_devin_names,
)
from agent_core.manifest import MANIFEST_FILENAME, ManifestError, load_skill_names
from agent_core.pi_manifest import PI_MANIFEST_FILENAME, PiManifestError, load_pi_names


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        raise AssertionError(f"Command failed: {command}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd, check=check)


def initialize_repo(path: Path) -> None:
    path.mkdir(parents=True)
    git(path, "init", "-q")
    git(path, "config", "user.name", "Agent Core Tests")
    git(path, "config", "user.email", "agent-core@example.invalid")
    git(path, "config", "gc.auto", "0")
    git(path, "config", "maintenance.auto", "false")


def commit_all(path: Path, message: str) -> None:
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", message)


def write_skill(checkout: Path, name: str, content: str) -> None:
    skill = checkout / "skills" / name
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test\n---\n\n{content}\n",
        encoding="utf-8",
    )


def write_config(checkout: Path, names: list[str]) -> None:
    rendered = "skills = [\n" + "".join(f'    "{name}",\n' for name in names) + "]\n"
    (checkout / MANIFEST_FILENAME).write_text(rendered, encoding="utf-8")
    # Both manifests are mandatory for sync. Legacy apply ignores the Pi list.
    pi_manifest = checkout / PI_MANIFEST_FILENAME
    if not pi_manifest.exists():
        write_pi_config(checkout, agents=[], prompts=[])
    devin_manifest = checkout / DEVIN_MANIFEST_FILENAME
    if not devin_manifest.exists():
        write_devin_config(checkout, agents=[])


def write_pi_config(checkout: Path, agents: list[str], prompts: list[str]) -> None:
    content = ""
    for category, names in (("agents", agents), ("prompts", prompts)):
        content += category + " = [\n"
        content += "".join(f'    "{name}",\n' for name in names)
        content += "]\n"
    (checkout / PI_MANIFEST_FILENAME).write_text(content, encoding="utf-8")


def write_pi_resource(checkout: Path, category: str, name: str, content: str) -> None:
    path = checkout / "pi" / category / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_devin_config(checkout: Path, agents: list[str]) -> None:
    content = "agents = [\n" + "".join(f'    "{name}",\n' for name in agents) + "]\n"
    (checkout / DEVIN_MANIFEST_FILENAME).write_text(content, encoding="utf-8")


def write_devin_resource(checkout: Path, name: str, content: str) -> None:
    path = checkout / "devin" / "agents" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_installer_module():
    path = REPOSITORY_ROOT / "scripts" / "install_agent_core.py"
    spec = importlib.util.spec_from_file_location("install_agent_core", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ManifestTests(unittest.TestCase):
    def test_strict_manifest_parser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / MANIFEST_FILENAME
            path.write_text('skills = [\n  "one",\n  "two",\n]\n', encoding="utf-8")
            self.assertEqual(load_skill_names(path), ["one", "two"])
            path.write_text('[other]\nskills = ["one"]\n', encoding="utf-8")
            with self.assertRaisesRegex(ManifestError, "must contain only"):
                load_skill_names(path)


class AgentCoreSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "canonical"
        initialize_repo(self.checkout)
        write_skill(self.checkout, "demo", "version one")
        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "initial canonical")
        self.home = self.root / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def skill(self, name: str = "demo") -> Path:
        return self.home / ".pi" / "agent" / "skills" / name

    def alias(self, name: str = "demo") -> Path:
        return self.home / ".claude" / "skills" / name

    def test_first_sync_and_repeat_no_op_publish_only_skills(self) -> None:
        first = sync.sync_checkout(self.checkout, self.home)
        second = sync.sync_checkout(self.checkout, self.home)

        self.assertEqual([plan.classification for plan in first.skills], ["added"])
        self.assertEqual([plan.classification for plan in second.skills], ["unchanged"])
        self.assertFalse(self.alias().exists())
        for relative in sync.LEGACY_GUIDANCE_DESTINATIONS.values():
            self.assertFalse((self.home / relative).exists())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertEqual(state["version"], sync.STATE_VERSION)
        self.assertIn("demo", state["skills"])
        self.assertEqual(state["guidance"], {})

    def test_updates_recreates_and_keeps_removed_config_additively(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        write_skill(self.checkout, "demo", "version two")
        write_skill(self.checkout, "second", "second")
        write_config(self.checkout, ["demo", "second"])
        commit_all(self.checkout, "update and add")
        shutil.rmtree(self.skill())

        result = sync.sync_checkout(self.checkout, self.home)
        classes = {plan.source.name: plan.classification for plan in result.skills}
        self.assertEqual(classes, {"demo": "recreated", "second": "added"})
        self.assertIn("version two", (self.skill() / "SKILL.md").read_text(encoding="utf-8"))

        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "remove second")
        sync.sync_checkout(self.checkout, self.home)
        self.assertTrue((self.skill("second") / "SKILL.md").is_file())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertIn("second", state["skills"])
        self.assertNotIn("second", state["aliases"])

    def test_missing_or_untracked_pi_manifest_is_refused(self) -> None:
        pi_manifest = self.checkout / PI_MANIFEST_FILENAME
        pi_manifest.unlink()
        with self.assertRaisesRegex(sync.SyncError, "Required Pi manifest is missing"):
            sync.sync_checkout(self.checkout, self.home)
        committed = git(self.checkout, "show", f"HEAD:{PI_MANIFEST_FILENAME}").stdout
        pi_manifest.write_text(committed + "# uncommitted edit\n", encoding="utf-8")
        with self.assertRaisesRegex(sync.SyncError, "must match the canonical commit"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.skill().exists())

    def test_committed_skill_updates_are_reported(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        write_skill(self.checkout, "demo", "version two")
        commit_all(self.checkout, "update published source")

        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.skills[0].classification, "updated")
        self.assertIn("version two", (self.skill() / "SKILL.md").read_text(encoding="utf-8"))

    def test_modified_owned_skill_is_replaced_by_canonical(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        (self.skill() / "SKILL.md").write_text("local edit", encoding="utf-8")
        (self.skill() / "extra.md").write_text("manual extra", encoding="utf-8")

        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.skills[0].classification, "updated")
        self.assertIn("version one", (self.skill() / "SKILL.md").read_text(encoding="utf-8"))
        self.assertFalse((self.skill() / "extra.md").exists())

    def test_unowned_differing_skill_is_replaced_by_canonical(self) -> None:
        self.skill().mkdir(parents=True)
        (self.skill() / "SKILL.md").write_text("custom skill", encoding="utf-8")
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.skills[0].classification, "replaced")
        self.assertIn("version one", (self.skill() / "SKILL.md").read_text(encoding="utf-8"))

    def test_unowned_guidance_and_other_skills_are_preserved(self) -> None:
        unrelated = self.home / ".agents/skills/third-party"
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("third party", encoding="utf-8")
        claude = self.home / ".claude/CLAUDE.md"
        claude.parent.mkdir(parents=True)
        claude.write_text("my prompt\n", encoding="utf-8")

        sync.sync_checkout(self.checkout, self.home)
        self.assertEqual((unrelated / "SKILL.md").read_text(), "third party")
        self.assertEqual(claude.read_text(encoding="utf-8"), "my prompt\n")
        claude.write_text("updated prompt\n", encoding="utf-8")
        sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(claude.read_text(encoding="utf-8"), "updated prompt\n")

    def test_sync_releases_legacy_guidance_without_changing_files(self) -> None:
        guidance = {}
        for harness, relative in sync.LEGACY_GUIDANCE_DESTINATIONS.items():
            target = self.home / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"{harness} prompt\n", encoding="utf-8")
            guidance[harness] = {
                "destination": str(target),
                "source_commit": "0" * 40,
                "fingerprint": "0" * 64,
            }
        state_path = sync.global_state_path(self.home)
        state_path.parent.mkdir(parents=True)
        state_path.write_text(
            json.dumps({"version": 2, "skills": {}, "aliases": {}, "guidance": guidance}),
            encoding="utf-8",
        )

        sync.sync_checkout(self.checkout, self.home)
        for harness, relative in sync.LEGACY_GUIDANCE_DESTINATIONS.items():
            self.assertEqual((self.home / relative).read_text(encoding="utf-8"), f"{harness} prompt\n")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["guidance"], {})
        self.assertTrue(self.skill().is_dir())

    def test_existing_claude_alias_is_unmanaged_and_preserved(self) -> None:
        alias = self.alias()
        alias.mkdir(parents=True)
        (alias / "keep.txt").write_text("user-owned", encoding="utf-8")
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual((alias / "keep.txt").read_text(encoding="utf-8"), "user-owned")
        sync.sync_checkout(self.checkout, self.home)
        self.assertEqual((alias / "keep.txt").read_text(encoding="utf-8"), "user-owned")

    def test_state_publication_failure_rolls_back(self) -> None:
        original = apply._atomic_write

        def fail_state(path: Path, content: str) -> None:
            if path.name == sync.STATE_FILENAME and path.parent.name == sync.STATE_DIRECTORY:
                raise OSError("injected state failure")
            original(path, content)

        with patch.object(apply, "_atomic_write", side_effect=fail_state):
            with self.assertRaisesRegex(sync.SyncError, "injected state failure"):
                sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.skill().exists())
        self.assertFalse(sync.global_state_path(self.home).exists())

    def test_uncommitted_sources_and_manifest_are_refused(self) -> None:
        (self.checkout / "skills/demo/local.txt").write_text("untracked", encoding="utf-8")
        with self.assertRaisesRegex(apply.ApplyError, "not tracked"):
            sync.sync_checkout(self.checkout, self.home)
        (self.checkout / "skills/demo/local.txt").unlink()
        write_config(self.checkout, [])
        with self.assertRaisesRegex(apply.ApplyError, "must match committed"):
            sync.sync_checkout(self.checkout, self.home)

    def test_result_output_is_concise_and_complete(self) -> None:
        result = sync.sync_checkout(self.checkout, self.home)
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            sync.print_result(result)
        output = stdout.getvalue()
        self.assertIn("agent-core sync: OK (", output)
        self.assertIn("Skills (1): demo", output)
        agent_names = [plan.source.name for plan in result.pi_resources if plan.source.category == "agents"]
        self.assertIn(f"Agents ({len(agent_names)}): " + (", ".join(agent_names) or "none"), output)
        self.assertIn("Verified: ~/.pi/agent/{skills,agents,prompts}", output)
        self.assertNotIn("Claude aliases:", output)
        prompt_names = [plan.source.name for plan in result.pi_resources if plan.source.category == "prompts"]
        self.assertIn(f"Prompts ({len(prompt_names)}): " + (", ".join(prompt_names) or "none"), output)



class PiManifestTests(unittest.TestCase):
    def test_strict_pi_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / PI_MANIFEST_FILENAME
            path.write_text('agents = [\n  "commit-agent",\n]\nprompts = [\n]\n', encoding="utf-8")
            self.assertEqual(load_pi_names(path), {"agents": ["commit-agent"], "prompts": []})
            path.write_text('agents = ["one"]\nprompts = []\n', encoding="utf-8")
            with self.assertRaises(PiManifestError):
                load_pi_names(path)


class DevinManifestTests(unittest.TestCase):
    def test_strict_devin_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / DEVIN_MANIFEST_FILENAME
            path.write_text('agents = [\n  "commit-agent",\n]\n', encoding="utf-8")
            self.assertEqual(load_devin_names(path), ["commit-agent"])
            path.write_text('agents = ["one"]\n', encoding="utf-8")
            with self.assertRaises(DevinManifestError):
                load_devin_names(path)


class DevinResourceSyncTests(AgentCoreSyncTests):
    def setUp(self) -> None:
        super().setUp()
        write_devin_config(self.checkout, agents=["commit-agent"])
        write_devin_resource(
            self.checkout,
            "commit-agent",
            "---\nname: commit-agent\nmodel: codex\nallowed-tools:\n  - read\n  - exec\n---\n",
        )
        commit_all(self.checkout, "configure Devin resources")
        self.app_data = self.root / "AppData" / "Roaming"

    def devin_skill(self, name: str = "demo") -> Path:
        return self.app_data / "devin" / "skills" / name

    def devin_agent(self) -> Path:
        return self.app_data / "devin" / "agents" / "commit-agent.md"

    def test_devin_publish_is_global_native_and_idempotent(self) -> None:
        first = sync.sync_checkout(
            self.checkout, self.home, "devin", app_data=self.app_data
        )
        second = sync.sync_checkout(
            self.checkout, self.home, "devin", app_data=self.app_data
        )

        self.assertEqual([plan.classification for plan in first.skills], ["added"])
        self.assertEqual([plan.classification for plan in first.devin_resources], ["added"])
        self.assertEqual([plan.classification for plan in second.skills], ["unchanged"])
        self.assertEqual([plan.classification for plan in second.devin_resources], ["unchanged"])
        self.assertTrue((self.devin_skill() / "SKILL.md").is_file())
        self.assertIn("model: codex", self.devin_agent().read_text(encoding="utf-8"))
        self.assertFalse((self.app_data / ".devin").exists())
        self.assertFalse((self.home / ".pi").exists())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertIn("demo", state["devin_skills"])
        self.assertIn("commit-agent", state["devin_agents"])
        self.assertEqual(state["skills"], {})

    def test_devin_declared_resources_replace_differing_targets(self) -> None:
        self.devin_skill().mkdir(parents=True)
        (self.devin_skill() / "SKILL.md").write_text("local skill", encoding="utf-8")
        self.devin_agent().parent.mkdir(parents=True)
        self.devin_agent().write_text("local agent", encoding="utf-8")

        result = sync.sync_checkout(
            self.checkout, self.home, "devin", app_data=self.app_data
        )

        self.assertEqual([plan.classification for plan in result.skills], ["replaced"])
        self.assertEqual([plan.classification for plan in result.devin_resources], ["replaced"])
        self.assertIn("version one", (self.devin_skill() / "SKILL.md").read_text())
        self.assertIn("model: codex", self.devin_agent().read_text())

    def test_pi_and_devin_ownership_coexist(self) -> None:
        sync.sync_checkout(self.checkout, self.home, "devin", app_data=self.app_data)
        with patch.dict(os.environ, {"APPDATA": str(self.app_data)}):
            sync.sync_checkout(self.checkout, self.home)

        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertIn("demo", state["skills"])
        self.assertIn("demo", state["devin_skills"])
        self.assertIn("commit-agent", state["devin_agents"])

    def test_uncommitted_devin_source_is_refused(self) -> None:
        write_devin_resource(self.checkout, "commit-agent", "uncommitted edit")
        with self.assertRaisesRegex(sync.SyncError, "must match the canonical commit"):
            sync.sync_checkout(self.checkout, self.home, "devin", app_data=self.app_data)
        self.assertFalse(self.devin_agent().exists())

    def test_devin_state_failure_rolls_back_all_resources(self) -> None:
        with patch.object(apply, "_atomic_write", side_effect=OSError("test state failure")):
            with self.assertRaisesRegex(sync.SyncError, "test state failure"):
                sync.sync_checkout(
                    self.checkout, self.home, "devin", app_data=self.app_data
                )
        self.assertFalse(self.devin_skill().exists())
        self.assertFalse(self.devin_agent().exists())
        self.assertFalse(sync.global_state_path(self.home).exists())

    def test_devin_requires_appdata(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(sync.SyncError, "APPDATA is required"):
                sync.sync_checkout(self.checkout, self.home, "devin")

    def test_devin_result_output_names_native_destination(self) -> None:
        result = sync.sync_checkout(
            self.checkout, self.home, "devin", app_data=self.app_data
        )
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            sync.print_result(result)
        output = stdout.getvalue()
        self.assertIn("Harness: devin", output)
        self.assertIn("Skills (1): demo", output)
        self.assertIn("Agents (1): commit-agent", output)
        self.assertIn(r"%APPDATA%\devin\{skills,agents}", output)
        self.assertNotIn("Prompts", output)


class OpenCodeResourceSyncTests(AgentCoreSyncTests):
    def opencode_skill(self, name: str = "demo") -> Path:
        return self.home / ".config/opencode/skills" / name

    def test_opencode_publishes_shared_skills_only_and_is_idempotent(self) -> None:
        guidance = self.home / ".config/opencode/AGENTS.md"
        guidance.parent.mkdir(parents=True)
        guidance.write_text("user-owned guidance\n", encoding="utf-8")

        first = sync.sync_checkout(self.checkout, self.home, "opencode")
        second = sync.sync_checkout(self.checkout, self.home, "opencode")

        self.assertEqual([plan.classification for plan in first.skills], ["added"])
        self.assertEqual([plan.classification for plan in second.skills], ["unchanged"])
        self.assertTrue((self.opencode_skill() / "SKILL.md").is_file())
        self.assertFalse((self.home / ".pi").exists())
        self.assertEqual(guidance.read_text(encoding="utf-8"), "user-owned guidance\n")
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertIn("demo", state["opencode_skills"])
        self.assertEqual(state["skills"], {})
        self.assertEqual(state["devin_skills"], {})

    def test_opencode_replaces_declared_skill_and_preserves_unrelated_content(self) -> None:
        target = self.opencode_skill()
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("local edit", encoding="utf-8")
        unrelated = self.opencode_skill("third-party")
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("leave me", encoding="utf-8")

        result = sync.sync_checkout(self.checkout, self.home, "opencode")

        self.assertEqual([plan.classification for plan in result.skills], ["replaced"])
        self.assertIn("version one", (target / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual((unrelated / "SKILL.md").read_text(encoding="utf-8"), "leave me")

    def test_opencode_state_failure_rolls_back(self) -> None:
        with patch.object(apply, "_atomic_write", side_effect=OSError("test state failure")):
            with self.assertRaisesRegex(sync.SyncError, "test state failure"):
                sync.sync_checkout(self.checkout, self.home, "opencode")
        self.assertFalse(self.opencode_skill().exists())
        self.assertFalse(sync.global_state_path(self.home).exists())

    def test_opencode_upgrades_version_five_ownership(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        state_path = sync.global_state_path(self.home)
        old_state = json.loads(state_path.read_text(encoding="utf-8"))
        old_state["version"] = 5
        old_state.pop("opencode_skills")
        state_path.write_text(json.dumps(old_state), encoding="utf-8")

        sync.sync_checkout(self.checkout, self.home, "opencode")

        migrated = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["version"], sync.STATE_VERSION)
        self.assertIn("demo", migrated["skills"])
        self.assertIn("demo", migrated["opencode_skills"])

    def test_opencode_result_output_names_native_destination(self) -> None:
        result = sync.sync_checkout(self.checkout, self.home, "opencode")
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            sync.print_result(result)
        output = stdout.getvalue()
        self.assertIn("Harness: opencode", output)
        self.assertIn("Skills (1): demo", output)
        self.assertIn("Verified: ~/.config/opencode/skills", output)
        self.assertNotIn("Agents", output)
        self.assertNotIn("Prompts", output)


class PiResourceSyncTests(AgentCoreSyncTests):
    def setUp(self) -> None:
        super().setUp()
        write_pi_config(self.checkout, agents=["commit-agent"], prompts=["commit-with-subagent"])
        write_pi_resource(self.checkout, "agents", "commit-agent", "---\nname: commit-agent\n---\n")
        write_pi_resource(self.checkout, "prompts", "commit-with-subagent", "---\ndescription: commit\n---\n")
        commit_all(self.checkout, "configure Pi resources")

    def agent(self) -> Path:
        return self.home / ".pi/agent/agents/commit-agent.md"

    def prompt(self) -> Path:
        return self.home / ".pi/agent/prompts/commit-with-subagent.md"

    def test_pi_publish_idempotent_and_guidance_untouched(self) -> None:
        pi_guidance = self.home / ".pi/agent/AGENTS.md"
        pi_guidance.parent.mkdir(parents=True, exist_ok=True)
        pi_guidance.write_text("user instructions\n", encoding="utf-8")
        first = sync.sync_checkout(self.checkout, self.home)
        second = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual([p.classification for p in first.pi_resources], ["added", "added"])
        self.assertEqual([p.classification for p in second.pi_resources], ["unchanged", "unchanged"])
        self.assertTrue(self.agent().is_file())
        self.assertTrue(self.prompt().is_file())
        self.assertEqual(pi_guidance.read_text(encoding="utf-8"), "user instructions\n")
        self.assertFalse((self.home / ".agents/agents/commit-agent.md").exists())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertIn("commit-agent", state["pi_agents"])
        self.assertIn("commit-with-subagent", state["pi_prompts"])

    def test_existing_identical_is_adopted_without_overwrite(self) -> None:
        self.agent().parent.mkdir(parents=True)
        self.agent().write_bytes((self.checkout / "pi/agents/commit-agent.md").read_bytes())
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.pi_resources[0].classification, "adopted")
        self.assertTrue(self.prompt().is_file())
        repeat = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(repeat.pi_resources[0].classification, "unchanged")

    def test_unowned_differing_agent_and_prompt_are_replaced(self) -> None:
        self.agent().parent.mkdir(parents=True)
        self.prompt().parent.mkdir(parents=True)
        self.agent().write_text("custom local agent", encoding="utf-8")
        self.prompt().write_text("custom local prompt", encoding="utf-8")
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual([p.classification for p in result.pi_resources], ["replaced", "replaced"])
        self.assertEqual(self.agent().read_bytes(), (self.checkout / "pi/agents/commit-agent.md").read_bytes())
        self.assertEqual(self.prompt().read_bytes(), (self.checkout / "pi/prompts/commit-with-subagent.md").read_bytes())

    def test_modified_owned_pi_file_is_replaced_by_canonical(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        self.agent().write_text("local changes", encoding="utf-8")
        self.prompt().write_text("local changes", encoding="utf-8")
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual([p.classification for p in result.pi_resources], ["updated", "updated"])
        self.assertEqual(self.agent().read_bytes(), (self.checkout / "pi/agents/commit-agent.md").read_bytes())
        self.assertEqual(self.prompt().read_bytes(), (self.checkout / "pi/prompts/commit-with-subagent.md").read_bytes())

    def test_unowned_non_regular_agent_refuses_unsafe_replacement(self) -> None:
        self.agent().mkdir(parents=True)
        with self.assertRaisesRegex(sync.SyncError, "not a regular file"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertTrue(self.agent().is_dir())

    def test_update_recreate_and_remove_are_non_destructive(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        write_pi_resource(self.checkout, "agents", "commit-agent", "---\nname: commit-agent\n---\nchanged\n")
        commit_all(self.checkout, "update agent")
        self.prompt().unlink()
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual([p.classification for p in result.pi_resources], ["updated", "recreated"])
        write_pi_config(self.checkout, agents=[], prompts=[])
        commit_all(self.checkout, "remove Pi selections")
        sync.sync_checkout(self.checkout, self.home)
        self.assertTrue(self.agent().exists())
        self.assertFalse(self.prompt().exists())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertNotIn("commit-with-subagent", state["pi_prompts"])

    def test_locally_modified_retired_prompt_blocks_removal(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        self.prompt().write_text("local prompt edit", encoding="utf-8")
        write_pi_config(self.checkout, agents=["commit-agent"], prompts=[])
        commit_all(self.checkout, "replace prompt with skill")

        with self.assertRaisesRegex(sync.SyncError, "locally modified"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(self.prompt().read_text(encoding="utf-8"), "local prompt edit")

    def test_uncommitted_pi_source_fails_before_installation(self) -> None:
        write_pi_resource(self.checkout, "agents", "commit-agent", "uncommitted edit")
        with self.assertRaisesRegex(sync.SyncError, "must match the canonical commit"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.prompt().exists())

    def test_state_failure_rolls_back_pi_and_skill_installs(self) -> None:
        with patch.object(apply, "_atomic_write", side_effect=OSError("test state failure")):
            with self.assertRaisesRegex(sync.SyncError, "test state failure"):
                sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.skill().exists())
        self.assertFalse(self.agent().exists())
        self.assertFalse(self.prompt().exists())
        self.assertFalse(sync.global_state_path(self.home).exists())



class PiMigrationTests(unittest.TestCase):
    """Simulate an existing version-3 machine without modifying real user files."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "canonical"
        initialize_repo(self.checkout)
        write_skill(self.checkout, "demo", "canonical skill")
        write_config(self.checkout, ["demo"])
        write_pi_config(self.checkout, agents=["commit-agent"], prompts=["commit-with-subagent"])
        write_pi_resource(self.checkout, "agents", "commit-agent", "canonical agent\n")
        write_pi_resource(self.checkout, "prompts", "commit-with-subagent", "canonical prompt\n")
        commit_all(self.checkout, "canonical resources")
        self.home = self.root / "home"
        self.home.mkdir()
        self.commit = git(self.checkout, "rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def legacy_skill(self) -> Path:
        return self.home / ".agents/skills/demo"

    def pi_skill(self) -> Path:
        return self.home / ".pi/agent/skills/demo"

    def pi_agent(self) -> Path:
        return self.home / ".pi/agent/agents/commit-agent.md"

    def pi_prompt(self) -> Path:
        return self.home / ".pi/agent/prompts/commit-with-subagent.md"

    def seed_legacy(self, *, with_alias: bool = False) -> None:
        source_skill = self.checkout / "skills/demo"
        old_skill = self.legacy_skill()
        old_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_skill, old_skill)

        state = {
            "version": 3,
            "skills": {
                "demo": {
                    "destination": str(old_skill.resolve()),
                    "source_commit": self.commit,
                    "fingerprint": apply.fingerprint_directory(old_skill),
                }
            },
            "aliases": {},
            "guidance": {},
            "pi_agents": {},
            "pi_prompts": {},
        }
        for category, name in (("agents", "commit-agent"), ("prompts", "commit-with-subagent")):
            source = self.checkout / "pi" / category / f"{name}.md"
            target = self.home / ".agents" / category / f"{name}.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            state["pi_" + category][name] = {
                "destination": str(target.resolve()),
                "source_commit": self.commit,
                "fingerprint": hashlib.sha256(target.read_bytes()).hexdigest(),
            }

        if with_alias:
            alias = self.home / ".claude/skills/demo"
            alias.parent.mkdir(parents=True)
            if os.name == "nt":
                result = subprocess.run(
                    ["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(old_skill)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            else:
                alias.symlink_to(old_skill, target_is_directory=True)
            state["aliases"]["demo"] = {
                "destination": str(alias),
                "target": str(old_skill),
            }
        state_path = sync.global_state_path(self.home)
        state_path.parent.mkdir(parents=True)
        state_path.write_text(json.dumps(state), encoding="utf-8")

    def test_migration_moves_only_owned_resources_to_pi(self) -> None:
        self.seed_legacy()
        unrelated = self.home / ".agents/skills/unrelated"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("keep", encoding="utf-8")
        guidance = self.home / ".pi/agent/AGENTS.md"
        guidance.parent.mkdir(parents=True)
        guidance.write_text("keep guidance", encoding="utf-8")
        settings = guidance.parent / "settings.json"
        settings.write_text('{"theme":"custom"}', encoding="utf-8")

        result = sync.sync_checkout(self.checkout, self.home)
        self.assertTrue(self.pi_skill().is_dir())
        self.assertEqual(self.pi_agent().read_text(), "canonical agent\n")
        self.assertEqual(self.pi_prompt().read_text(), "canonical prompt\n")
        self.assertEqual(len(result.legacy), 3)
        self.assertFalse(self.legacy_skill().exists())
        self.assertFalse((self.home / ".agents/agents/commit-agent.md").exists())
        self.assertFalse((self.home / ".agents/prompts/commit-with-subagent.md").exists())
        self.assertEqual((unrelated / "SKILL.md").read_text(), "keep")
        self.assertEqual(guidance.read_text(), "keep guidance")
        self.assertEqual(settings.read_text(), '{"theme":"custom"}')

        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertEqual(state["version"], sync.STATE_VERSION)
        self.assertEqual(Path(state["skills"]["demo"]["destination"]).resolve(), self.pi_skill().resolve())
        self.assertEqual(Path(state["pi_agents"]["commit-agent"]["destination"]).resolve(), self.pi_agent().resolve())
        self.assertEqual(sync.sync_checkout(self.checkout, self.home).legacy, [])

    def test_native_identical_copies_adopted_during_migration(self) -> None:
        self.seed_legacy()
        shutil.copytree(self.checkout / "skills/demo", self.pi_skill())
        self.pi_agent().parent.mkdir(parents=True)
        self.pi_prompt().parent.mkdir(parents=True)
        shutil.copy2(self.checkout / "pi/agents/commit-agent.md", self.pi_agent())
        shutil.copy2(self.checkout / "pi/prompts/commit-with-subagent.md", self.pi_prompt())

        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.skills[0].classification, "adopted")
        self.assertEqual([p.classification for p in result.pi_resources], ["adopted", "adopted"])
        self.assertFalse(self.legacy_skill().exists())

    def test_differing_native_file_is_overwritten_during_legacy_migration(self) -> None:
        self.seed_legacy()
        self.pi_agent().parent.mkdir(parents=True)
        self.pi_agent().write_text("my custom agent\n", encoding="utf-8")
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.pi_resources[0].classification, "replaced")
        self.assertFalse(self.legacy_skill().exists())
        self.assertTrue(self.pi_skill().exists())
        self.assertEqual(self.pi_agent().read_text(), "canonical agent\n")

    def test_modified_managed_legacy_skill_blocks_migration(self) -> None:
        self.seed_legacy()
        (self.legacy_skill() / "SKILL.md").write_text("local edit", encoding="utf-8")
        with self.assertRaisesRegex(sync.SyncError, "locally modified"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.pi_skill().exists())

    def test_rollback_restores_old_files_and_state(self) -> None:
        self.seed_legacy(with_alias=True)
        old_state = sync.global_state_path(self.home).read_bytes()
        alias = self.home / ".claude/skills/demo"
        with patch.object(apply, "_atomic_write", side_effect=OSError("injected state failure")):
            with self.assertRaisesRegex(sync.SyncError, "injected state failure"):
                sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(old_state, sync.global_state_path(self.home).read_bytes())
        self.assertTrue(self.legacy_skill().is_dir())
        self.assertTrue(alias.exists())
        self.assertTrue(sync._alias_matches(alias, self.legacy_skill()))
        self.assertTrue((self.home / ".agents/agents/commit-agent.md").is_file())
        self.assertFalse(self.pi_skill().exists())
        self.assertFalse(self.pi_agent().exists())

    def test_verified_legacy_claude_junction_retired(self) -> None:
        self.seed_legacy(with_alias=True)
        alias = self.home / ".claude/skills/demo"
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(len(result.legacy), 4)
        self.assertFalse(alias.exists())
        state = json.loads(sync.global_state_path(self.home).read_text(encoding="utf-8"))
        self.assertEqual(state["aliases"], {})
        self.assertTrue(self.pi_skill().exists())

    def test_unowned_claude_alias_is_preserved(self) -> None:
        self.seed_legacy()
        alias = self.home / ".claude/skills/demo"
        alias.mkdir(parents=True)
        (alias / "keep.txt").write_text("keep", encoding="utf-8")
        sync.sync_checkout(self.checkout, self.home)
        self.assertEqual((alias / "keep.txt").read_text(), "keep")


class LegacyApplyAndRetirementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "canonical"
        initialize_repo(self.checkout)
        write_skill(self.checkout, "demo", "version one")
        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "canonical")
        self.project = self.root / "project"
        initialize_repo(self.project)
        (self.project / "README.md").write_text("project\n", encoding="utf-8")
        commit_all(self.project, "project")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_legacy_apply_still_uses_project_destination(self) -> None:
        plans = apply.apply_checkout(self.checkout, self.project, here=True)
        self.assertEqual(plans[0].classification, "absent")
        self.assertTrue((self.project / ".agents/skills/demo/SKILL.md").is_file())
        self.assertFalse((self.root / ".agents").exists())

    def test_retire_here_removes_only_owned_content_and_exact_metadata(self) -> None:
        apply.apply_checkout(self.checkout, self.project, here=True)
        unrelated = self.project / ".agents/skills/unrelated"
        unrelated.mkdir()
        (unrelated / "keep.txt").write_text("keep", encoding="utf-8")
        paths = apply.resolve_project(self.project, here=True)
        exclude = paths.git_common_dir / "info/exclude"
        with exclude.open("a", encoding="utf-8") as stream:
            stream.write("/unrelated-rule/\n")

        result = retire.retire_local(self.project, here=True)
        self.assertEqual(result.removed, ["demo"])
        self.assertFalse((self.project / ".agents/skills/demo").exists())
        self.assertEqual((unrelated / "keep.txt").read_text(), "keep")
        self.assertFalse((self.project / ".agents/.agent-core/ownership.json").exists())
        exclusions = exclude.read_text(encoding="utf-8")
        self.assertIn("/unrelated-rule/", exclusions)
        self.assertNotIn("agent-core managed skills", exclusions)

    def test_retire_refuses_modified_or_tracked_content_before_mutation(self) -> None:
        apply.apply_checkout(self.checkout, self.project, here=True)
        target = self.project / ".agents/skills/demo/SKILL.md"
        target.write_text("local", encoding="utf-8")
        with self.assertRaisesRegex(retire.RetireError, "locally modified"):
            retire.retire_local(self.project, here=True)
        self.assertTrue(target.exists())

        target.write_text((self.checkout / "skills/demo/SKILL.md").read_text(), encoding="utf-8")
        git(self.project, "add", "-f", ".agents/skills/demo/SKILL.md")
        commit_all(self.project, "track legacy copy")
        with self.assertRaisesRegex(retire.RetireError, "tracked by Git"):
            retire.retire_local(self.project, here=True)
        self.assertTrue(target.exists())

    def test_retire_here_recognizes_prior_plain_apply_at_git_root(self) -> None:
        apply.apply_checkout(self.checkout, self.project)
        result = retire.retire_local(self.project, here=True)
        self.assertEqual(result.removed, ["demo"])
        self.assertFalse((self.project / ".agents/skills/demo").exists())


class AgentCoreBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.upstream = self.root / "upstream"
        initialize_repo(self.upstream)
        shutil.copytree(
            REPOSITORY_ROOT / "agent_core", self.upstream / "agent_core",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        shutil.copy2(REPOSITORY_ROOT / "pyproject.toml", self.upstream / "pyproject.toml")
        write_skill(self.upstream, "demo", "remote one")
        write_config(self.upstream, ["demo"])
        commit_all(self.upstream, "initial")
        self.remote = self.root / "remote.git"
        git(self.root, "init", "-q", "--bare", str(self.remote))
        git(self.upstream, "remote", "add", "origin", str(self.remote))
        branch = git(self.upstream, "branch", "--show-current").stdout.strip()
        git(self.upstream, "push", "-q", "-u", "origin", branch)
        self.home = self.root / "home"
        self.home.mkdir()
        self.checkout = self.home / ".agent-core"
        git(self.root, "clone", "-q", str(self.remote), str(self.checkout))
        self.project = self.root / "project"
        self.project.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_fast_forward_uses_fresh_sync_implementation(self) -> None:
        implementation = self.upstream / "agent_core" / "sync.py"
        text = implementation.read_text(encoding="utf-8")
        marker = '    Path(args.home, "fresh-process.txt").write_text("fresh", encoding="utf-8")\n'
        text = text.replace("    try:\n        result = sync_checkout", marker + "    try:\n        result = sync_checkout")
        implementation.write_text(text, encoding="utf-8")
        write_skill(self.upstream, "demo", "remote two")
        commit_all(self.upstream, "fresh implementation")
        git(self.upstream, "push", "-q")

        result = bootstrap.refresh_and_launch(
            self.checkout, self.project, command="sync", home=self.home
        )
        self.assertEqual(result, 0)
        self.assertEqual((self.home / "fresh-process.txt").read_text(), "fresh")
        self.assertIn("remote two", (self.home / ".pi/agent/skills/demo/SKILL.md").read_text())

    def test_explicit_devin_harness_reaches_fresh_process(self) -> None:
        app_data = self.root / "AppData" / "Roaming"
        with patch.dict(os.environ, {"APPDATA": str(app_data)}):
            result = bootstrap.refresh_and_launch(
                self.checkout,
                self.project,
                command="sync",
                home=self.home,
                harness="devin",
            )

        self.assertEqual(result, 0)
        self.assertIn(
            "remote one",
            (app_data / "devin/skills/demo/SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertFalse((self.home / ".pi").exists())

    def test_explicit_opencode_harness_reaches_fresh_process(self) -> None:
        result = bootstrap.refresh_and_launch(
            self.checkout,
            self.project,
            command="sync",
            home=self.home,
            harness="opencode",
        )

        self.assertEqual(result, 0)
        self.assertIn(
            "remote one",
            (self.home / ".config/opencode/skills/demo/SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertFalse((self.home / ".pi").exists())

    def test_dirty_checkout_is_refused(self) -> None:
        (self.checkout / "dirty.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "staged, unstaged, or untracked"):
            bootstrap.refresh_and_launch(self.checkout, self.project, command="sync", home=self.home)
        self.assertFalse((self.home / ".agents").exists())

    def test_pull_failure_warns_and_publishes_local_commit_for_all_harnesses(self) -> None:
        self.remote.rename(self.root / "unavailable.git")
        commit = git(self.checkout, "rev-parse", "HEAD").stdout.strip()
        app_data = self.root / "AppData" / "Roaming"
        # Keep bytecode generated by the fresh process out of this fixture's status.
        with (self.checkout / ".git/info/exclude").open("a") as stream:
            stream.write("\n__pycache__/\n")
        for harness in ("pi", "devin", "opencode"):
            with self.subTest(harness=harness), patch.dict(os.environ, {"APPDATA": str(app_data)}), patch("sys.stderr", new_callable=StringIO) as stderr:
                result = bootstrap.refresh_and_launch(
                    self.checkout, self.project, command="sync", home=self.home, harness=harness
                )
                self.assertEqual(result, 0)
                self.assertIn(commit, stderr.getvalue())
                self.assertIn("remote freshness is unverified", stderr.getvalue())
        self.assertIn("remote one", (self.home / ".pi/agent/skills/demo/SKILL.md").read_text())
        self.assertIn("remote one", (app_data / "devin/skills/demo/SKILL.md").read_text())
        self.assertIn("remote one", (self.home / ".config/opencode/skills/demo/SKILL.md").read_text())

    def test_failed_pull_never_falls_back_for_legacy_commands(self) -> None:
        self.remote.rename(self.root / "unavailable.git")
        for command in ("apply", "retire-local"):
            with self.subTest(command=command), self.assertRaisesRegex(bootstrap.AgentCoreError, "Could not refresh"):
                bootstrap.refresh_and_launch(self.checkout, self.project, command=command, here=True)

    def test_failed_pull_refuses_dirty_changed_head_or_unfinished_operation(self) -> None:
        original_git = bootstrap._git
        for damage in ("dirty", "head", "operation"):
            with self.subTest(damage=damage):
                original_head = git(self.checkout, "rev-parse", "HEAD").stdout.strip()
                def failed_pull(checkout, *args):
                    if args == ("pull", "--ff-only"):
                        if damage == "dirty":
                            (checkout / "dirty.txt").write_text("changed")
                        elif damage == "head":
                            git(checkout, "-c", "user.name=Tests", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "changed HEAD")
                        else:
                            (checkout / ".git/MERGE_HEAD").write_text(original_head)
                        return subprocess.CompletedProcess(args, 1, "", "injected failure")
                    return original_git(checkout, *args)
                with patch.object(bootstrap, "_git", side_effect=failed_pull), self.assertRaises(bootstrap.AgentCoreError):
                    bootstrap.refresh_and_launch(self.checkout, self.project, home=self.home)
                self.assertFalse((self.home / ".pi").exists())
                if damage == "dirty":
                    (self.checkout / "dirty.txt").unlink()
                elif damage == "operation":
                    (self.checkout / ".git/MERGE_HEAD").unlink()

    def test_unfinished_operation_refused_even_with_no_pull(self) -> None:
        (self.checkout / ".git/rebase-merge").mkdir()
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "Unfinished Git"):
            bootstrap.refresh_and_launch(self.checkout, self.project, home=self.home, no_pull=True)
        self.assertFalse((self.home / ".pi").exists())

    def test_no_pull_uses_current_clean_commit_without_remote_access(self) -> None:
        self.remote.rename(self.root / "unavailable.git")

        result = bootstrap.refresh_and_launch(
            self.checkout,
            self.project,
            command="sync",
            home=self.home,
            no_pull=True,
        )

        self.assertEqual(result, 0)
        self.assertIn("remote one", (self.home / ".pi/agent/skills/demo/SKILL.md").read_text())

    def test_no_pull_still_refuses_a_dirty_checkout(self) -> None:
        (self.checkout / "dirty.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "staged, unstaged, or untracked"):
            bootstrap.refresh_and_launch(
                self.checkout,
                self.project,
                command="sync",
                home=self.home,
                no_pull=True,
            )
        self.assertFalse((self.home / ".agents").exists())

    def test_cli_routes_sync_apply_and_retire(self) -> None:
        with patch.object(bootstrap, "canonical_checkout", return_value=self.checkout), patch.object(
            bootstrap, "refresh_and_launch", return_value=0
        ) as launch:
            self.assertEqual(bootstrap.main(["sync", "--no-pull"]), 0)
            self.assertEqual(bootstrap.main(["sync", "--harness", "devin"]), 0)
            self.assertEqual(bootstrap.main(["sync", "--harness", "opencode"]), 0)
            self.assertEqual(bootstrap.main(["apply", "--here"]), 0)
            self.assertEqual(bootstrap.main(["retire-local", "--here"]), 0)
        self.assertEqual(launch.call_count, 5)
        self.assertEqual(launch.call_args_list[0].kwargs["command"], "sync")
        self.assertTrue(launch.call_args_list[0].kwargs["no_pull"])
        self.assertEqual(launch.call_args_list[0].kwargs["harness"], "pi")
        self.assertEqual(launch.call_args_list[1].kwargs["command"], "sync")
        self.assertEqual(launch.call_args_list[1].kwargs["harness"], "devin")
        self.assertEqual(launch.call_args_list[2].kwargs["harness"], "opencode")
        self.assertEqual(launch.call_args_list[3].kwargs["command"], "apply")
        self.assertFalse(launch.call_args_list[3].kwargs["no_pull"])
        self.assertEqual(launch.call_args_list[4].kwargs["command"], "retire-local")


class InstallerAndCompatibilityTests(unittest.TestCase):
    def test_installer_writes_cmd_shim_and_requests_path_update(self) -> None:
        installer = load_installer_module()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            checkout = home / ".agent-core"
            checkout.mkdir(parents=True)
            local = Path(directory) / "local"
            with patch.object(installer, "add_to_user_path", return_value=True) as add:
                shim, bin_directory, changed = installer.install(
                    checkout=checkout,
                    home=home,
                    local_app_data=local,
                    python_executable=Path("C:/Python310/python.exe"),
                )
            self.assertTrue(changed)
            self.assertEqual(bin_directory, local / "AgentCore/bin")
            self.assertIn("bootstrap.py", shim.read_text(encoding="utf-8"))
            self.assertIn(str(Path("C:/Python310/python.exe")), shim.read_text(encoding="utf-8"))
            add.assert_called_once_with(bin_directory)

    def test_user_path_update_preserves_long_existing_value(self) -> None:
        installer = load_installer_module()
        captured: dict[str, object] = {}
        existing = ";".join(["C:/existing/" + ("x" * 4000), "C:/other"])

        class Key:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        fake_winreg = types.SimpleNamespace(
            HKEY_CURRENT_USER=object(),
            REG_EXPAND_SZ=2,
            CreateKey=lambda *_: Key(),
            QueryValueEx=lambda *_: (existing, 2),
            SetValueEx=lambda _key, name, _reserved, kind, value: captured.update(
                name=name, kind=kind, value=value
            ),
        )
        fake_ctypes = types.SimpleNamespace(
            c_ulong=lambda: object(),
            byref=lambda value: value,
            windll=types.SimpleNamespace(
                user32=types.SimpleNamespace(SendMessageTimeoutW=lambda *args: 1)
            ),
        )
        with patch.dict("sys.modules", {"winreg": fake_winreg}), patch.object(
            installer, "ctypes", fake_ctypes
        ):
            changed = installer.add_to_user_path(Path("C:/AgentCore/bin"))
        self.assertTrue(changed)
        self.assertEqual(captured["kind"], 2)
        self.assertTrue(str(captured["value"]).startswith(str(Path("C:/AgentCore/bin")) + ";"))
        self.assertIn(existing, str(captured["value"]))

    def test_cmd_installer_has_no_forbidden_dependency(self) -> None:
        content = (REPOSITORY_ROOT / "scripts/install-agent-core.cmd").read_text(encoding="utf-8").lower()
        for forbidden in ("powershell", "setx", "pip", "uv "):
            self.assertNotIn(forbidden, content)
        self.assertIn("py -3", content)
        self.assertIn("python", content)

    def test_runtime_sources_parse_as_python_310(self) -> None:
        paths = list((REPOSITORY_ROOT / "agent_core").glob("*.py"))
        paths.append(REPOSITORY_ROOT / "scripts/install_agent_core.py")
        for path in paths:
            with self.subTest(path=path):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=(3, 10))


if __name__ == "__main__":
    unittest.main()
