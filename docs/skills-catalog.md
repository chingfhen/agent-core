---
title: Skills Catalogue
description: Human- and agent-readable map of Agent Core skills, invocation cues, and personal installation status.
updated: 2026-10-09
---

# Skills Catalogue

**Find by job, not by similar-sounding names.** For skill-writing and cleanup decisions, see [Skill Design Guide](skill-design-guide.md).

`personal-skills.toml` is the authoritative list of skills published by `agent-core sync`. This catalogue is informational: being listed here **does not** install a skill. A removed manifest entry also does not automatically uninstall old copies.

## Active — in `personal-skills.toml`

| Skill | Reach for it when… | Boundary |
| --- | --- | --- |
| [project-tasks](../skills/project-tasks/SKILL.md) | You need to save, resume, checkpoint, or hand off unfinished work. | Execution continuity, not project truth. |
| [project-docs](../skills/project-docs/SKILL.md) | You want to maintain durable project decisions, contracts, or guidance. | Settled understanding, not an active backlog. |
| [planning](../skills/planning/SKILL.md) | You want to evaluate options and agree on a build direction. | Decide before implementing. |
| [engineering](../skills/engineering/SKILL.md) | You want the agent to implement, fix, refactor, or review code. | Execute the approved scope. |
| [explain-tech](../skills/explain-tech/SKILL.md) | "Explain this error/architecture/change" or "debrief what we built." | Quick by default; Deep and Debrief modes. |
| [human-unblock](../skills/human-unblock/SKILL.md) | The agent cannot progress without access, authentication, approval, or a human decision. | Give the human a precise action and resume; not general preflight. |
| [learning-markdown](../skills/learning-markdown/SKILL.md) | You want a reusable Markdown lesson from material or a conversation. | Teaching artifact; not automatic KB capture. |
| [grilling](../skills/grilling/SKILL.md) | "Grill my plan" with one consequential question at a time. | Explicit design interrogation, not ordinary planning. |
| [approval-gate](../skills/approval-gate/SKILL.md) | "Final approval check" before consequential unapproved action. | Approval brief, not execution or unblock. |
| [manage-python-uv](../skills/manage-python-uv/SKILL.md) | Set up, run, or maintain a **Windows uv** Python environment. | Do not apply to corporate CML/Mamba by default. |
| [mermaid-markdown](../skills/mermaid-markdown/SKILL.md) | Add or improve a Mermaid diagram or chart in Markdown. | Visualization of understood material, not architecture decisions. |
| [yagni](../skills/yagni/SKILL.md) | "Simplify", "do less", "avoid overengineering", "YAGNI". | Deliberate minimalism; still meet correctness and safety. |

## Dormant — retained but not installed

| Skill | Reach for it when… | Note |
| --- | --- | --- |
| [document-text-extraction](../skills/document-text-extraction/SKILL.md) | Explicitly extract a named PDF/image locally. | Temporary extraction only; independent of KB and `evidence-authoring`. |
| [knowledge-base](../skills/knowledge-base/SKILL.md) | Consult the **repo copy** of the KB workflow. | **Not installed by sync.** Agent Core's steward guidance identifies a separate Google Drive workflow; `global/AGENTS.md` is no longer published to user prompts. |
| [repo-audit](../skills/repo-audit/SKILL.md) | Request a dedicated whole-repository risk/bloat audit. | Specialized full-repo report, not routine code review. |
| [ml-architecture-review](../skills/ml-architecture-review/SKILL.md) | Explicitly request focused ML architecture decision analysis. | Specialized investigation; planning remains general-purpose. |
| [humanize-spoken-output](../skills/humanize-spoken-output/SKILL.md) | Rewrite spoken scripts, narration, and interview answers naturally. | Content editing, not technical teaching. |

## Archived — not active

Historical source lives in `archive/skills/` with a `2026-10-08__<former-name>-SKILL.md` filename:

- Superseded by KB: `evidence-authoring`.
- Covered by project-tasks / planning: `execution-readiness`, `execution-topology`.
- Covered by `yagni`: `yagni-review`.
- Consolidated into `explain-tech`: `quick-orientation`, `human-technical-orientation`, `technical-coach`, `debrief`.
- Converted into [Skill Design Guide](skill-design-guide.md): `skill-refinement-reference`.

## Before making another skill

Check this catalogue, identify the nearest active skill, and decide whether the missing behavior is a **mode or edit** rather than a new job. See [Skill Design Guide](skill-design-guide.md). Never infer installation from directory presence.
