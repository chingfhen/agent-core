"""Static consistency checks, not proof of model/harness compliance."""
from pathlib import Path
import re
import unittest

from agent_core.manifest import load_skill_names


ROOT = Path(__file__).resolve().parents[1]


class WorkspaceContractTests(unittest.TestCase):
    def test_declared_skills_have_matching_names(self):
        for name in load_skill_names(ROOT / "personal-skills.toml"):
            with self.subTest(skill=name):
                text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")
        for old in ("manage-python-agent-envs", "manage-python-uv"):
            self.assertFalse((ROOT / "skills" / old).exists())

    def test_all_canonical_skills_allow_model_invocation(self):
        for source in (ROOT / "skills").glob("*/SKILL.md"):
            frontmatter = source.read_text(encoding="utf-8").split("---", 2)[1]
            with self.subTest(skill=source.parent.name):
                self.assertNotRegex(frontmatter, r"(?m)^disable-model-invocation:\s*true\s*$")
                self.assertNotRegex(frontmatter, r"opencode/autoinvoke:\s*false\b")
                triggers = re.search(r"(?m)^triggers:[^\n]*(?:\n[ \t]+[^\n]*)*", frontmatter)
                if triggers:
                    self.assertRegex(triggers.group(), r"\bmodel\b")

    def test_workflow_references_resolve(self):
        files = [
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "docs/workspace-configuration.md",
            ROOT / "docs/skills-catalog.md",
            ROOT / "docs/skill-design-guide.md",
            ROOT / "docs/agent-core-operating-manual.md",
            ROOT / "tests/workspace-workflow-scenarios.md",
            ROOT / "tests/knowledge-base-scenarios.md",
            ROOT / "tasks/INDEX.md",
            ROOT / "tasks/2026-10/2026-10-29__skill-owned-agents-sections.md",
        ]
        for skill in ("project-tasks", "project-docs", "knowledge-base",
                      "manage-python-env", "agent-lessons", "workspace-setup"):
            files.extend((ROOT / "skills" / skill).rglob("*.md"))
        for source in files:
            # Fenced examples contain deliberately fictional workspace paths.
            text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", "",
                          source.read_text(encoding="utf-8"))
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(source=str(source.relative_to(ROOT)), link=link):
                    target, _, anchor = link.partition("#")
                    destination = source.parent / target
                    self.assertTrue(destination.exists())
                    if anchor and destination.suffix == ".md":
                        headings = re.findall(r"(?m)^#{1,6} (.+)$",
                                              destination.read_text(encoding="utf-8"))
                        slugs = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
                                 for h in headings]
                        self.assertIn(anchor, slugs)

    def test_owner_templates_have_one_balanced_section(self):
        owners = {
            "project-tasks/references/routing.md": "PROJECT TASKS",
            "project-docs/references/routing.md": "PROJECT DOCS",
            "knowledge-base/references/routing.md": "KNOWLEDGE BASE",
            "manage-python-env/references/routing.md": "PYTHON ENVIRONMENTS",
            "agent-lessons/SKILL.md": "AGENT LESSONS",
        }
        for relative, marker in owners.items():
            text = (ROOT / "skills" / relative).read_text(encoding="utf-8")
            markers = re.findall(r"(?m)^<!-- (BEGIN|END) ([A-Z ]+) -->$", text)
            with self.subTest(owner=relative):
                self.assertEqual(markers, [("BEGIN", marker), ("END", marker)])
