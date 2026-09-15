from __future__ import annotations

import json
import shutil
import stat
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_core import apply, bootstrap


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
    (checkout / "core-skills.toml").write_text(rendered, encoding="utf-8")


class AgentCoreApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "canonical"
        initialize_repo(self.checkout)
        write_skill(self.checkout, "demo", "version one")
        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "initial canonical")

        self.project = self.root / "project"
        initialize_repo(self.project)
        (self.project / "README.md").write_text("project\n", encoding="utf-8")
        commit_all(self.project, "initial project")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def target(self, name: str = "demo") -> Path:
        return self.project / ".agents" / "skills" / name

    def ownership_path(self, project: Path | None = None) -> Path:
        paths = apply.resolve_project(project or self.project)
        return apply.state_path(paths)

    def test_first_apply_records_ownership_and_is_idempotent(self) -> None:
        first = apply.apply_checkout(self.checkout, self.project)
        second = apply.apply_checkout(self.checkout, self.project)

        self.assertEqual([plan.classification for plan in first], ["absent"])
        self.assertEqual([plan.classification for plan in second], ["owned-unchanged"])
        self.assertIn("version one", (self.target() / "SKILL.md").read_text(encoding="utf-8"))
        state = json.loads(self.ownership_path().read_text(encoding="utf-8"))
        record = state["destinations"][".agents/skills/demo"]
        self.assertEqual(record["source_skill"], "demo")
        self.assertEqual(record["fingerprint"], apply.fingerprint_directory(self.target()))
        self.assertRegex(record["source_commit"], r"^[0-9a-f]{40,64}$")

    def test_adding_and_cleanly_readding_a_configured_skill(self) -> None:
        apply.apply_checkout(self.checkout, self.project)
        write_skill(self.checkout, "second", "second one")
        write_config(self.checkout, ["demo", "second"])
        commit_all(self.checkout, "add second")
        apply.apply_checkout(self.checkout, self.project)

        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "remove second from config")
        before = (self.target("second") / "SKILL.md").read_text(encoding="utf-8")
        apply.apply_checkout(self.checkout, self.project)
        self.assertEqual((self.target("second") / "SKILL.md").read_text(encoding="utf-8"), before)
        self.assertIn(".agents/skills/second", json.loads(self.ownership_path().read_text())["destinations"])

        write_skill(self.checkout, "second", "second two")
        write_config(self.checkout, ["demo", "second"])
        commit_all(self.checkout, "readd second")
        apply.apply_checkout(self.checkout, self.project)
        self.assertIn("second two", (self.target("second") / "SKILL.md").read_text(encoding="utf-8"))

    def test_manual_deletion_is_safely_recreated(self) -> None:
        apply.apply_checkout(self.checkout, self.project)
        shutil.rmtree(self.target())
        plans = apply.apply_checkout(self.checkout, self.project)
        self.assertEqual(plans[0].classification, "owned-missing")
        self.assertTrue((self.target() / "SKILL.md").is_file())

    def test_locally_modified_removed_skill_is_refused_when_readded(self) -> None:
        apply.apply_checkout(self.checkout, self.project)
        write_config(self.checkout, [])
        commit_all(self.checkout, "remove demo")
        (self.target() / "SKILL.md").write_text("local while removed", encoding="utf-8")
        apply.apply_checkout(self.checkout, self.project)

        write_config(self.checkout, ["demo"])
        commit_all(self.checkout, "readd demo")
        with self.assertRaisesRegex(apply.ApplyError, "locally modified"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertEqual((self.target() / "SKILL.md").read_text(), "local while removed")

    def test_refuses_unowned_or_locally_modified_target(self) -> None:
        self.target().mkdir(parents=True)
        (self.target() / "local.txt").write_text("private", encoding="utf-8")
        with self.assertRaisesRegex(apply.ApplyError, "not provably owned"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertEqual((self.target() / "local.txt").read_text(), "private")

        shutil.rmtree(self.target())
        apply.apply_checkout(self.checkout, self.project)
        (self.target() / "SKILL.md").write_text("local edit", encoding="utf-8")
        with self.assertRaisesRegex(apply.ApplyError, "locally modified"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertEqual((self.target() / "SKILL.md").read_text(), "local edit")

    def test_refuses_tracked_target_and_tracked_descendant(self) -> None:
        for relative in (Path(".agents/skills/demo"), Path(".agents/skills/demo/child.txt")):
            with self.subTest(relative=relative):
                isolated = self.root / ("tracked-" + str(len(relative.parts)))
                initialize_repo(isolated)
                path = isolated / relative
                path.parent.mkdir(parents=True)
                path.write_text("tracked", encoding="utf-8")
                commit_all(isolated, "tracked target")
                with self.assertRaisesRegex(apply.ApplyError, "tracked by project Git"):
                    apply.apply_checkout(self.checkout, isolated)

    def test_missing_or_invalid_sources_fail_before_project_mutation(self) -> None:
        write_config(self.checkout, ["missing"])
        commit_all(self.checkout, "missing source")
        with self.assertRaisesRegex(apply.ApplyError, "not a real directory"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertFalse(self.target().exists())

        write_config(self.checkout, ["demo", "Demo"])
        commit_all(self.checkout, "duplicate source")
        with self.assertRaisesRegex(apply.ApplyError, "duplicate"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertFalse((self.project / ".agents").exists())

    def test_ignored_untracked_source_file_is_not_copied(self) -> None:
        (self.checkout / ".gitignore").write_text("*.private\n", encoding="utf-8")
        commit_all(self.checkout, "ignore private artifacts")
        (self.checkout / "skills/demo/local.private").write_text("not committed", encoding="utf-8")
        self.assertEqual(git(self.checkout, "status", "--porcelain").stdout, "")

        with self.assertRaisesRegex(apply.ApplyError, "not tracked"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertFalse(self.target().exists())

    def test_fingerprint_includes_permission_changes(self) -> None:
        skill_file = self.checkout / "skills/demo/SKILL.md"
        original_mode = stat.S_IMODE(skill_file.stat().st_mode)
        original_fingerprint = apply.fingerprint_directory(skill_file.parent)
        try:
            skill_file.chmod(original_mode ^ stat.S_IWUSR)
            changed_mode = stat.S_IMODE(skill_file.stat().st_mode)
            if changed_mode == original_mode:
                self.skipTest("filesystem does not expose chmod changes")
            self.assertNotEqual(original_fingerprint, apply.fingerprint_directory(skill_file.parent))
        finally:
            skill_file.chmod(original_mode)

    def test_malformed_ownership_state_fails_closed(self) -> None:
        path = self.ownership_path()
        path.parent.mkdir(parents=True)
        path.write_text('{"version": 1, "destinations": {"bad": {}}}', encoding="utf-8")
        with self.assertRaisesRegex(apply.ApplyError, "invalid"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertFalse(self.target().exists())

    def test_all_target_preflight_prevents_partial_update(self) -> None:
        apply.apply_checkout(self.checkout, self.project)
        original = (self.target() / "SKILL.md").read_text(encoding="utf-8")
        write_skill(self.checkout, "demo", "version two")
        write_skill(self.checkout, "second", "second")
        write_config(self.checkout, ["demo", "second"])
        commit_all(self.checkout, "two skill update")
        self.target("second").mkdir()
        (self.target("second") / "local.txt").write_text("keep", encoding="utf-8")

        with self.assertRaisesRegex(apply.ApplyError, "not provably owned"):
            apply.apply_checkout(self.checkout, self.project)
        self.assertEqual((self.target() / "SKILL.md").read_text(encoding="utf-8"), original)

    def test_replacement_failure_rolls_back_and_does_not_write_state(self) -> None:
        write_skill(self.checkout, "second", "second")
        write_config(self.checkout, ["demo", "second"])
        commit_all(self.checkout, "two skills")
        original_move = apply._move_path
        calls = 0

        def fail_second(source: Path, destination: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replacement failure")
            original_move(source, destination)

        with patch.object(apply, "_move_path", side_effect=fail_second):
            with self.assertRaisesRegex(apply.ApplyError, "injected replacement failure"):
                apply.apply_checkout(self.checkout, self.project)

        self.assertFalse(self.target().exists())
        self.assertFalse(self.target("second").exists())
        self.assertFalse(self.ownership_path().exists())
        artifacts = list((self.project / ".agents").glob(".agent-core-*") if (self.project / ".agents").exists() else [])
        self.assertEqual(artifacts, [])

    def test_exclusions_are_idempotent_and_preserve_unrelated_content(self) -> None:
        project_paths = apply.resolve_project(self.project)
        exclude = project_paths.git_common_dir / "info" / "exclude"
        exclude.write_text("# local rule\n/cache/\n", encoding="utf-8")
        apply.apply_checkout(self.checkout, self.project)
        first = exclude.read_text(encoding="utf-8")
        apply.apply_checkout(self.checkout, self.project)
        second = exclude.read_text(encoding="utf-8")

        self.assertEqual(first, second)
        self.assertIn("# local rule\n/cache/", second)
        self.assertEqual(second.count(apply.EXCLUDE_START), 1)
        self.assertIn("/.agents/skills/demo/", second)
        self.assertFalse((self.project / ".gitignore").exists())
        status = git(self.project, "status", "--short").stdout
        self.assertNotIn(".agents/skills/demo", status)

    def test_linked_worktree_uses_actual_git_dir_and_common_exclude(self) -> None:
        linked = self.root / "linked"
        git(self.project, "worktree", "add", "-q", "-b", "linked-test", str(linked))
        apply.apply_checkout(self.checkout, linked)
        paths = apply.resolve_project(linked)

        self.assertNotEqual(paths.git_dir, paths.git_common_dir)
        self.assertTrue(apply.state_path(paths).is_file())
        self.assertFalse((paths.git_common_dir / apply.STATE_DIRECTORY / apply.STATE_FILENAME).exists())
        self.assertIn("/.agents/skills/demo/", (paths.git_common_dir / "info" / "exclude").read_text())

    def test_here_applies_to_a_non_git_directory(self) -> None:
        workspace = self.root / "workspace"
        workspace.mkdir()

        plans = apply.apply_checkout(self.checkout, workspace, here=True)
        project_paths = apply.resolve_project(workspace, here=True)

        self.assertEqual([plan.classification for plan in plans], ["absent"])
        self.assertTrue((workspace / ".agents/skills/demo/SKILL.md").is_file())
        self.assertEqual(
            apply.state_path(project_paths), workspace.resolve() / ".agents/.agent-core/ownership.json"
        )
        self.assertTrue(apply.state_path(project_paths).is_file())

        git(workspace, "init", "-q")
        git(workspace, "config", "user.name", "Agent Core Tests")
        git(workspace, "config", "user.email", "agent-core@example.invalid")
        (workspace / "README.md").write_text("workspace\n", encoding="utf-8")
        git(workspace, "add", "README.md")
        git(workspace, "commit", "-q", "-m", "initialize workspace")

        repeated = apply.apply_checkout(self.checkout, workspace, here=True)
        self.assertEqual([plan.classification for plan in repeated], ["owned-unchanged"])
        self.assertTrue((workspace / ".agents/.agent-core/ownership.json").is_file())
        self.assertNotIn(".agents", git(workspace, "status", "--short").stdout)

    def test_here_targets_a_git_subdirectory_and_keeps_git_safety(self) -> None:
        workspace = self.project / "workspace"
        workspace.mkdir()
        apply.apply_checkout(self.checkout, workspace, here=True)
        project_paths = apply.resolve_project(workspace, here=True)

        self.assertTrue((workspace / ".agents/skills/demo/SKILL.md").is_file())
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(
            apply.state_path(project_paths), workspace.resolve() / ".agents/.agent-core/ownership.json"
        )
        exclude = project_paths.git_common_dir / "info/exclude"
        exclusions = exclude.read_text(encoding="utf-8")
        self.assertIn("/workspace/.agents/skills/demo/", exclusions)
        self.assertIn("/workspace/.agents/.agent-core/", exclusions)

        git(self.project, "add", "-f", "workspace/.agents/skills/demo/SKILL.md")
        commit_all(self.project, "track copied skill")
        with self.assertRaisesRegex(apply.ApplyError, "tracked by project Git"):
            apply.apply_checkout(self.checkout, workspace, here=True)

    def test_legacy_surfaces_are_ignored(self) -> None:
        (self.project / ".agent-os.json").write_text("not json", encoding="utf-8")
        (self.project / ".agent-os-state").mkdir()
        for surface in (".claude", ".opencode"):
            legacy = self.project / surface / "skills" / "demo"
            legacy.mkdir(parents=True)
            (legacy / "keep.txt").write_text("keep", encoding="utf-8")

        apply.apply_checkout(self.checkout, self.project)
        self.assertTrue((self.target() / "SKILL.md").is_file())
        self.assertEqual((self.project / ".claude/skills/demo/keep.txt").read_text(), "keep")
        self.assertEqual((self.project / ".opencode/skills/demo/keep.txt").read_text(), "keep")


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

        self.checkout = self.root / "home" / ".agent-core"
        self.checkout.parent.mkdir()
        git(self.root, "clone", "-q", str(self.remote), str(self.checkout))

        self.project = self.root / "project"
        initialize_repo(self.project)
        (self.project / "README.md").write_text("project\n", encoding="utf-8")
        commit_all(self.project, "initial")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_fast_forward_uses_freshly_pulled_apply_implementation(self) -> None:
        write_skill(self.upstream, "demo", "remote two")
        implementation = self.upstream / "agent_core" / "apply.py"
        text = implementation.read_text(encoding="utf-8")
        text = text.replace(
            "        plans = apply_checkout(Path(args.checkout), Path(args.cwd), here=args.here)",
            '        (Path(args.cwd) / "fresh-process.txt").write_text("fresh", encoding="utf-8")\n'
            "        plans = apply_checkout(Path(args.checkout), Path(args.cwd), here=args.here)",
        )
        implementation.write_text(text, encoding="utf-8")
        commit_all(self.upstream, "fresh implementation")
        git(self.upstream, "push", "-q")

        result = bootstrap.refresh_and_launch(self.checkout, self.project)

        self.assertEqual(result, 0)
        self.assertEqual((self.project / "fresh-process.txt").read_text(), "fresh")
        self.assertIn("remote two", (self.project / ".agents/skills/demo/SKILL.md").read_text())

    def test_dirty_checkout_is_refused_before_project_mutation(self) -> None:
        (self.checkout / "untracked.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "staged, unstaged, or untracked"):
            bootstrap.refresh_and_launch(self.checkout, self.project)
        self.assertFalse((self.project / ".agents").exists())

    def test_pull_failure_is_refused_before_project_mutation(self) -> None:
        unavailable = self.root / "unavailable.git"
        self.remote.rename(unavailable)
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "Could not refresh"):
            bootstrap.refresh_and_launch(self.checkout, self.project)
        self.assertFalse((self.project / ".agents").exists())

    def test_cli_and_entry_point_smoke_contract(self) -> None:
        config = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["project"]["scripts"]["agent-core"], "agent_core.bootstrap:main")
        with patch.object(bootstrap, "canonical_checkout", return_value=self.checkout), patch.object(
            bootstrap, "refresh_and_launch", return_value=0
        ) as launch:
            self.assertEqual(bootstrap.main(["apply"]), 0)
        launch.assert_called_once()

    def test_non_git_directory_fails_without_writes(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        before = git(self.checkout, "rev-parse", "HEAD").stdout
        with self.assertRaisesRegex(bootstrap.AgentCoreError, "not in a Git worktree"):
            bootstrap.refresh_and_launch(self.checkout, outside)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD").stdout, before)

    def test_here_bootstrap_allows_a_non_git_directory(self) -> None:
        outside = self.root / "outside-here"
        outside.mkdir()

        result = bootstrap.refresh_and_launch(self.checkout, outside, here=True)

        self.assertEqual(result, 0)
        self.assertTrue((outside / ".agents/skills/demo/SKILL.md").is_file())
        self.assertTrue((outside / ".agents/.agent-core/ownership.json").is_file())

    def test_cli_passes_here_mode(self) -> None:
        with patch.object(bootstrap, "canonical_checkout", return_value=self.checkout), patch.object(
            bootstrap, "refresh_and_launch", return_value=0
        ) as launch:
            self.assertEqual(bootstrap.main(["apply", "--here"]), 0)
        launch.assert_called_once_with(self.checkout, Path.cwd(), here=True)


if __name__ == "__main__":
    unittest.main()
