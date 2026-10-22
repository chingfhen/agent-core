"""Static consistency checks, not proof of model/harness compliance."""
from pathlib import Path
import re
import unittest

from agent_core.manifest import load_skill_names


ROOT = Path(__file__).resolve().parents[1]


class WorkspaceContractTests(unittest.TestCase):
    def test_personal_baseline_matches_publication_manifest(self):
        defaults = (ROOT / "skills/workspace-setup/references/defaults.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| ([a-z][a-z0-9-]+) \|", defaults, re.MULTILINE)
        self.assertCountEqual(rows, load_skill_names(ROOT / "personal-skills.toml"))
        self.assertEqual(len(rows), len(set(rows)))

    def test_declared_skills_have_matching_names(self):
        for name in load_skill_names(ROOT / "personal-skills.toml"):
            with self.subTest(skill=name):
                text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")
        for old in ("manage-python-agent-envs", "manage-python-uv"):
            self.assertFalse((ROOT / "skills" / old).exists())

    def test_workspace_references_resolve(self):
        files = [
            ROOT / "skills/workspace-setup/SKILL.md",
            ROOT / "skills/workspace-setup/references/defaults.md",
            ROOT / "docs/workspace-configuration.md",
            ROOT / "docs/skills-catalog.md",
            ROOT / "tests/workspace-workflow-scenarios.md",
        ]
        for source in files:
            for link in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(source=source.name, link=link):
                    self.assertTrue((source.parent / link.split("#")[0]).exists())

    def test_setup_is_explicit_and_contains_persistence_boundary(self):
        text = (ROOT / "skills/workspace-setup/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("disable-model-invocation: true", text)
        self.assertIn("<!-- BEGIN MANAGED WORKSPACE -->", text)
        self.assertIn("<!-- END MANAGED WORKSPACE -->", text)
        self.assertIn("Return exactly the saved managed block", text)
        self.assertIn("Python Environment Root:", text)
        self.assertIn("Knowledge Base Archive:", text)
