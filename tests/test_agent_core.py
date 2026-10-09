from __future__ import annotations

import ast
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
from agent_core.manifest import MANIFEST_FILENAME, ManifestError, load_skill_names


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
        return self.home / ".agents" / "skills" / name

    def alias(self, name: str = "demo") -> Path:
        return self.home / ".claude" / "skills" / name

    def test_first_sync_and_repeat_no_op_publish_only_skills(self) -> None:
        first = sync.sync_checkout(self.checkout, self.home)
        second = sync.sync_checkout(self.checkout, self.home)

        self.assertEqual([plan.classification for plan in first.skills], ["added"])
        self.assertEqual([plan.classification for plan in second.skills], ["unchanged"])
        self.assertTrue(os.path.samefile(self.skill(), self.alias()))
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
        self.assertIn("second", state["aliases"])

    def test_committed_skill_updates_are_reported(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        write_skill(self.checkout, "demo", "version two")
        commit_all(self.checkout, "update published source")

        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.skills[0].classification, "updated")
        self.assertIn("version two", (self.skill() / "SKILL.md").read_text(encoding="utf-8"))

    def test_modified_target_refuses_all_changes(self) -> None:
        sync.sync_checkout(self.checkout, self.home)
        (self.skill() / "SKILL.md").write_text("local edit", encoding="utf-8")

        with self.assertRaisesRegex(sync.SyncError, "locally modified"):
            sync.sync_checkout(self.checkout, self.home)

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
            json.dumps({"version": sync.STATE_VERSION, "skills": {}, "aliases": {}, "guidance": guidance}),
            encoding="utf-8",
        )

        sync.sync_checkout(self.checkout, self.home)
        for harness, relative in sync.LEGACY_GUIDANCE_DESTINATIONS.items():
            self.assertEqual((self.home / relative).read_text(encoding="utf-8"), f"{harness} prompt\n")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["guidance"], {})
        self.assertTrue(self.skill().is_dir())

    def test_alias_collision_and_broken_alias_recovery(self) -> None:
        collision = self.alias()
        collision.mkdir(parents=True)
        (collision / "keep.txt").write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(sync.SyncError, "not owned"):
            sync.sync_checkout(self.checkout, self.home)
        self.assertEqual((collision / "keep.txt").read_text(), "keep")

        shutil.rmtree(collision)
        sync.sync_checkout(self.checkout, self.home)
        shutil.rmtree(self.skill())
        result = sync.sync_checkout(self.checkout, self.home)
        self.assertEqual(result.aliases[0].classification, "recreated")
        self.assertTrue(os.path.samefile(self.skill(), self.alias()))

    def test_rollback_spans_skills_aliases_and_state(self) -> None:
        with patch.object(sync, "_create_directory_alias", side_effect=sync.SyncError("injected alias failure")):
            with self.assertRaisesRegex(sync.SyncError, "injected alias failure"):
                sync.sync_checkout(self.checkout, self.home)
        self.assertFalse(self.skill().exists())
        self.assertFalse(sync.global_state_path(self.home).exists())

    def test_state_publication_failure_rolls_back(self) -> None:
        original = apply._atomic_write

        def fail_state(path: Path, content: str) -> None:
            if path == sync.global_state_path(self.home):
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
        self.assertIn("Canonical checkout:", output)
        self.assertIn("1 configured skills", output)
        self.assertIn("Changed skills: demo", output)
        self.assertIn("Global guidance: not managed", output)
        self.assertIn("Ownership state:", output)
        self.assertIn("Reload or restart", output)


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
        shutil.copytree(REPOSITORY_ROOT / "agent_core", self.upstream / "agent_core")
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
        self.assertIn("remote two", (self.home / ".agents/skills/demo/SKILL.md").read_text())

    def test_dirty_checkout_and_pull_failure_are_refused(self) -> None:
        (self.checkout / "dirty.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "staged, unstaged, or untracked"):
            bootstrap.refresh_and_launch(self.checkout, self.project, command="sync", home=self.home)
        self.assertFalse((self.home / ".agents").exists())
        (self.checkout / "dirty.txt").unlink()
        self.remote.rename(self.root / "unavailable.git")
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "Could not refresh"):
            bootstrap.refresh_and_launch(self.checkout, self.project, command="sync", home=self.home)
        self.assertFalse((self.home / ".agents").exists())

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
        self.assertIn("remote one", (self.home / ".agents/skills/demo/SKILL.md").read_text())

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
            self.assertEqual(bootstrap.main(["apply", "--here"]), 0)
            self.assertEqual(bootstrap.main(["retire-local", "--here"]), 0)
        self.assertEqual(launch.call_count, 3)
        self.assertEqual(launch.call_args_list[0].kwargs["command"], "sync")
        self.assertTrue(launch.call_args_list[0].kwargs["no_pull"])
        self.assertEqual(launch.call_args_list[1].kwargs["command"], "apply")
        self.assertFalse(launch.call_args_list[1].kwargs["no_pull"])
        self.assertEqual(launch.call_args_list[2].kwargs["command"], "retire-local")


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
