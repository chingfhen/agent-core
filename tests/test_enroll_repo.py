from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import enroll_repo


@unittest.skipUnless(os.name == "nt", "Windows junction coverage")
class EnrollmentAliasSafetyTests(unittest.TestCase):
    def write_skill(self, source_dir: Path, name: str = "demo") -> None:
        source_dir.mkdir(parents=True)
        (source_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test skill\n---\n",
            encoding="utf-8",
        )
        (source_dir / "canonical-sentinel.txt").write_text("keep", encoding="utf-8")

    def make_enrollment(self, root: Path) -> tuple[Path, Path, Path]:
        root = root.resolve()
        agent_os_path = root / "agent-os"
        source_dir = agent_os_path / "skills" / "demo"
        self.write_skill(source_dir)

        repo_path = root / "consumer"
        repo_path.mkdir()
        for surface in (".claude", ".opencode"):
            target_dir = repo_path / surface / "skills" / "demo"
            target_dir.parent.mkdir(parents=True)
            enroll_repo.create_junction(source_dir, target_dir)

        manifest_payload = enroll_repo.build_manifest_payload(
            repo_id="consumer",
            scope="repo",
            scope_id="consumer",
            agent_os_path=agent_os_path,
            memory_enabled=False,
        )
        (repo_path / ".agent-os.json").write_text(
            enroll_repo.render_manifest(manifest_payload), encoding="utf-8"
        )
        registry_path = root / "state" / "enrollments.json"
        registry_path.parent.mkdir()
        registry_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "device_defaults": {},
                    "enrollments": {
                        str(repo_path): {
                            "repo_path": str(repo_path),
                            "manifest_path": str(repo_path / ".agent-os.json"),
                            "repo_id": "consumer",
                            "scope": "repo",
                            "scope_id": "consumer",
                            "agent_os_path": str(agent_os_path),
                            "memory_enabled": False,
                            "skills": ["demo"],
                            "surfaces": ["claude", "opencode"],
                            "manage_ignore": True,
                            "link_mode": "junction",
                            "updated_at": "2026-07-18T00:00:00+00:00",
                        }
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return agent_os_path, repo_path, registry_path

    def test_remove_verified_junction_preserves_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source_dir = root / "canonical"
            self.write_skill(source_dir)
            alias_dir = root / "alias"
            enroll_repo.create_junction(source_dir, alias_dir)

            self.assertEqual(enroll_repo.link_kind(alias_dir), "junction")
            enroll_repo.remove_verified_alias(alias_dir, source_dir)

            self.assertFalse(enroll_repo.path_lexists(alias_dir))
            self.assertEqual((source_dir / "canonical-sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_remove_verified_alias_refuses_a_real_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source_dir = root / "canonical"
            self.write_skill(source_dir)
            local_dir = root / "local-skill"
            self.write_skill(local_dir)

            with self.assertRaisesRegex(RuntimeError, "non-alias"):
                enroll_repo.remove_verified_alias(local_dir, source_dir)

            self.assertEqual((local_dir / "canonical-sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_unenroll_removes_only_recorded_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            agent_os_path, repo_path, registry_path = self.make_enrollment(Path(temporary_dir))
            unrelated_skill = repo_path / ".claude" / "skills" / "e2e-runner"
            unrelated_skill.mkdir()
            (unrelated_skill / "sentinel.txt").write_text("keep", encoding="utf-8")

            with (
                patch.object(enroll_repo, "repo_root", return_value=agent_os_path),
                patch.object(enroll_repo, "registry_path", return_value=registry_path),
                patch.object(
                    sys,
                    "argv",
                    ["enroll_repo.py", "unenroll", "--repo", str(repo_path), "--apply"],
                ),
            ):
                self.assertEqual(enroll_repo.main(), 0)

            self.assertTrue((agent_os_path / "skills" / "demo" / "canonical-sentinel.txt").is_file())
            self.assertFalse(enroll_repo.path_lexists(repo_path / ".claude" / "skills" / "demo"))
            self.assertFalse(enroll_repo.path_lexists(repo_path / ".opencode" / "skills" / "demo"))
            self.assertEqual((unrelated_skill / "sentinel.txt").read_text(encoding="utf-8"), "keep")
            self.assertFalse((repo_path / ".agent-os.json").exists())
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertNotIn(str(repo_path), registry["enrollments"])

    def test_unenroll_defaults_to_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            agent_os_path, repo_path, registry_path = self.make_enrollment(Path(temporary_dir))

            with (
                patch.object(enroll_repo, "repo_root", return_value=agent_os_path),
                patch.object(enroll_repo, "registry_path", return_value=registry_path),
                patch.object(sys, "argv", ["enroll_repo.py", "unenroll", "--repo", str(repo_path)]),
            ):
                self.assertEqual(enroll_repo.main(), 0)

            self.assertTrue(enroll_repo.path_lexists(repo_path / ".claude" / "skills" / "demo"))
            self.assertTrue(enroll_repo.path_lexists(repo_path / ".opencode" / "skills" / "demo"))
            self.assertTrue((repo_path / ".agent-os.json").is_file())
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertIn(str(repo_path), registry["enrollments"])


if __name__ == "__main__":
    unittest.main()
