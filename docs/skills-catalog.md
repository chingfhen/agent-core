---
title: Skills Catalogue
description: Human- and agent-readable map of Agent Core skills, invocation cues, and personal installation status.
updated: 2026-10-30
---

# Skills Catalogue

**Find by job, not by similar-sounding names.** For skill-writing and cleanup decisions, see [Skill Design Guide](skill-design-guide.md).

`personal-skills.toml` is the authoritative list of skills published by `agent-core sync`. This catalogue is informational: being listed here **does not** install a skill. A removed manifest entry also does not automatically uninstall old copies.

All canonical skills permit model invocation. Natural-language intent can activate
request-only workflows; availability/loading does not authorize unrelated effects.

## Active — in `personal-skills.toml`

| Skill | Reach for it when… | Boundary |
| --- | --- | --- |
| [workspace-setup](../skills/workspace-setup/SKILL.md) | Request coordinated setup/refresh or an approved legacy-block migration. | Optional; follows skill-owned sections and preserves position/custom text. |
| [project-tasks](../skills/project-tasks/SKILL.md) | Save, resume, checkpoint, hand off, or close out work. | Deliverables and execution continuity; explicit handoff/closeout coordinates KB/docs/lessons and verified context pointers. |
| [project-docs](../skills/project-docs/SKILL.md) | Maintain durable project decisions, contracts, or owned guidance. | Standalone settled understanding; owns lean docs routing and independent first use. |
| [agent-lessons](../skills/agent-lessons/SKILL.md) | Request lessons review directly or through task handoff/closeout. | Essential rules/conditional pointers in its marked section; supporting detail through docs/KB, no new companion. |
| [knowledge-base](../skills/knowledge-base/SKILL.md) | "Sync to KB", process the KB inbox, create/update a managed artifact, or recall prior context. | Standalone selective recall and requested persistence; own routing, bounded knowledge-page maintenance, verified archival. |
| [planning](../skills/planning/SKILL.md) | You want to evaluate options and agree on a build direction. | Decide before implementing. |
| [engineering](../skills/engineering/SKILL.md) | Implement, debug, fix, refactor, or review code; proceed with an agreed change. Direct requests work without a task file. | Quick by default; Deep for requested depth or concrete risk/uncertainty. Same quality floor and authorized scope. |
| [learning](../skills/learning/SKILL.md) | "Help me understand/learn", explain a system or error, debrief an agent change, or create a learning lesson. | Quick default; Standard / Deep; concrete mechanisms and independent judgment; no automatic persistence. |
| [human-unblock](../skills/human-unblock/SKILL.md) | The agent cannot progress without access, authentication, approval, or a human decision. | Give the human a precise action and resume; not general preflight. |
| [readability](../skills/readability/SKILL.md) | Explicitly make an answer or artifact easier to read, or review its readability. | Independent editing guidance; preserves task requirements and meaning. Chat invocation does not authorize file edits. |
| [reasoned-advocacy](../skills/reasoned-advocacy/SKILL.md) | Build or challenge a defensible position, evaluate counterarguments, or prepare for stakeholder questions. | Quick or Deep; reasoning and spoken defense, not implementation planning or automatic persistence. |
| [grilling](../skills/grilling/SKILL.md) | "Grill my plan" with one consequential question at a time. | Explicit design interrogation, not ordinary planning. |
| [approval-gate](../skills/approval-gate/SKILL.md) | "Final approval check" before consequential unapproved action. | Approval brief, not execution or unblock. |
| [commit-with-subagent](../skills/commit-with-subagent/SKILL.md) | Explicitly create local commits through the configured commit-agent specialist. | User-triggered only; never pushes. |
| [manage-python-env](../skills/manage-python-env/SKILL.md) | Before Python execution, including interpreter/import probes, tests, evaluations, or dependency changes. | Own root/activation section and first use; manage AND execute through compatible independent uv purpose projects. |
| [mermaid-markdown](../skills/mermaid-markdown/SKILL.md) | Add or improve a Mermaid diagram or chart in Markdown. | Visualization of understood material, not architecture decisions. |
| [yagni](../skills/yagni/SKILL.md) | "Simplify", "do less", "avoid overengineering", "YAGNI". | Deliberate minimalism; still meet correctness and safety. |

## Dormant — retained but not installed

| Skill | Reach for it when… | Note |
| --- | --- | --- |
| [document-text-extraction](../skills/document-text-extraction/SKILL.md) | Explicitly extract a named PDF/image locally. | Temporary extraction only; independent of KB and `evidence-authoring`. |
| [repo-audit](../skills/repo-audit/SKILL.md) | Request a dedicated whole-repository risk/bloat audit. | Specialized full-repo report, not routine code review. |
| [ml-architecture-review](../skills/ml-architecture-review/SKILL.md) | Explicitly request focused ML architecture decision analysis. | Specialized investigation; planning remains general-purpose. |
| [humanize-spoken-output](../skills/humanize-spoken-output/SKILL.md) | Rewrite spoken scripts, narration, and interview answers naturally. | Content editing, not technical teaching. |

## Archived — not active

Historical sources live in `archive/skills/`, named by retirement date:

- Superseded by KB: `evidence-authoring`.
- Covered by project-tasks / planning: `execution-readiness`, `execution-topology`.
- Covered by `yagni`: `yagni-review`.
- Earlier technical teaching line, now consolidated into `learning`: `quick-orientation`, `human-technical-orientation`, `technical-coach`, `debrief` (via `explain-tech`).
- Replaced by `learning` on 2026-10-21: `explain-tech`, `learning-markdown` ([archived explain-tech](../archive/skills/2026-10-21__explain-tech-SKILL.md), [archived learning-markdown](../archive/skills/2026-10-21__learning-markdown-SKILL.md)).
- Converted into [Skill Design Guide](skill-design-guide.md): `skill-refinement-reference`.

## Replaced writing prompt

[readability](../skills/readability/SKILL.md) replaces `prompts/anti-mannered-prose.md`.
It includes the prompt's useful plain-language guidance and adds reader-focused
ordering, explanation, presentation, and meaning-preservation checks. The original
prompt is retained in [archive](../archive/prompts/2026-10-19__anti-mannered-prose.md),
not maintained as a second active instruction. `learning` and `mermaid-markdown` remain independent specialist skills, not dependencies.

## Before making another skill

Check this catalogue, identify the nearest active skill, and decide whether the missing behavior is a **mode or edit** rather than a new job. See [Skill Design Guide](skill-design-guide.md). Never infer installation from directory presence.
