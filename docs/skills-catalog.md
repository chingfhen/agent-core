---
title: Skills Catalogue
description: Human- and agent-readable map of Agent Core skills, invocation cues, and personal installation status.
updated: 2026-11-24
---

# Skills Catalogue

**Find by job, not by similar-sounding names.** For skill-writing and cleanup decisions, see [Skill Design Guide](skill-design-guide.md).

`personal-skills.toml` is the authoritative list of skills published by `agent-core sync`. This catalogue is informational: being listed here **does not** install a skill. A removed manifest entry also does not automatically uninstall old copies.

All canonical skills permit model invocation. Natural-language intent can activate
request-only workflows; availability/loading does not authorize unrelated effects.

## Selected — in `personal-skills.toml`

| Skill | Reach for it when… | Boundary |
| --- | --- | --- |
| [manage-project-tasks](../skills/manage-project-tasks/SKILL.md) | Save, resume, checkpoint, hand off, or close out work. | Deliverables and execution continuity; explicit handoff/closeout coordinates KB/docs/lessons and verified context pointers. |
| [ease-into-work](../skills/ease-into-work/SKILL.md) | "Help me get into TripVerge", "I have ten minutes to reconnect", or "what could I explore tonight?" | Read-only, choice-preserving re-entry using saved project tasks; execution and stopping remain with their owning workflows. |
| [define-success](../skills/define-success/SKILL.md) | "Let's define the goal/success", "what would good look like?", or challenge incomplete success criteria together. | Request-led collaborative outcome discovery and selective questioning; no automatic task writes, implementation, or tests. |
| [maintain-project-docs](../skills/maintain-project-docs/SKILL.md) | Maintain durable project decisions, contracts, or owned guidance. | Standalone settled understanding; owns lean docs routing and independent first use. |
| [improve-agent-workflows](../skills/improve-agent-workflows/SKILL.md) | Request lessons review directly or through task handoff/closeout. | Essential rules/conditional pointers in its marked section; supporting detail through docs/KB, no new companion. |
| [project-scripts](../skills/project-scripts/SKILL.md) | Explicitly review recent work for worthwhile personal scripts; create, repair, consolidate, or retire them. | Request-only personal script stewardship in one configured Project Scripts Root; not automatically part of engineering or handoffs. |
| [maintain-knowledge-base](../skills/maintain-knowledge-base/SKILL.md) | "Sync to KB", process the KB inbox, or create/update a managed artifact. | Selective recall is independent of maintenance invocation; requested persistence includes bounded page maintenance and verified archival. |
| [tech-design-options](../skills/tech-design-options/SKILL.md) | Request a comparison of materially different technical approaches to a consequential design choice. | Request-led; recommends a leader or a bounded discriminator, without reopening approved work or authorizing execution. |
| [code-design](../skills/code-design/SKILL.md) | Design or review a bounded code area's ownership, API/interface contracts, and changeability. | Request-led structure and contract judgment; actual FastAPI/MCP implementation uses its specialist guidance. Source/manifest inclusion does not establish installation. |
| [fastapi-practices](../skills/fastapi-practices/SKILL.md) | Implement or review actual FastAPI routes, Pydantic models, dependencies, and endpoint contracts. | Version-matched framework patterns; no framework upgrade, automatic dependency changes, or blanket refactor. |
| [mcp-tool-development](../skills/mcp-tool-development/SKILL.md) | Build or review agent-facing MCP tools and host integration. | Tool usability, typed contracts, consent, failure behavior and actual host evidence; no implied deployment or registration. |
| [react-nextjs-practices](../skills/react-nextjs-practices/SKILL.md) | Write or review React/Next.js code with relevant data, state, rendering and bundle considerations. | Focused rules, not the full performance checklist; preserves project cache/security decisions. |
| [frontend-design](../skills/frontend-design/SKILL.md) | Design a concrete screen or flow with deliberate visual hierarchy and product-specific aesthetics. | Create design direction; not a required redesign for ordinary code maintenance. |
| [web-interface-review](../skills/web-interface-review/SKILL.md) | Audit a named interface or substantial interaction for accessibility, responsive behavior and honest states. | Evidence-based UI review; distinct from visual design, React implementation and general code review. |
| [security-hardening](../skills/security-hardening/SKILL.md) | Implement or review sensitive trust boundaries, authorization, private data, uploads or agent mutations. | Scoped threat model and testable controls; no unauthorized security/configuration changes or blanket audit. |
| [code-review-quality](../skills/code-review-quality/SKILL.md) | Review a code diff or PR for material bugs and change quality, especially before review or merge. | Risk-focused findings; no automatic edits, independent-review claims, or merge authority. |
| [delegate-implementation](../skills/delegate-implementation/SKILL.md) | While planning a substantial implementation-ready Project Task (or on explicit request), choose delegation or no delegation and persist an observable worker strategy. | Planner owns harness, workers, model/effort choices (cheaper preferred, not required), coordination and fallback; execution follows the approved task contract without re-invoking planning. |
| [git-branch-to-review](../skills/git-branch-to-review/SKILL.md) | Explicitly request new managed branch delivery, or continue a known managed branch, its PR/MR, or linked task. | Date-prefixed branches; linked task by default; direct review link; explicit merge and guarded approved cleanup. Source/manifest inclusion does not establish installation. |
| [learning](../skills/learning/SKILL.md) | "Help me understand/learn", explain a system or error, debrief an agent change, or create a learning lesson. | Quick default; Standard / Deep; concrete mechanisms and independent judgment; no automatic persistence. |
| [learning-notebook](../skills/learning-notebook/SKILL.md) | Create, find, open, or extend a guided learning notebook. | Owns notebook routing and discovery; uses learning and run-and-manage-python for teaching and the shared personal environment. |
| [resolve-human-blockers](../skills/resolve-human-blockers/SKILL.md) | The agent cannot progress without access, authentication, approval, or a human decision. | Give the human a precise action and resume; not general preflight. |
| [improve-readability](../skills/improve-readability/SKILL.md) | Explicitly make an answer or artifact easier to read, or review its readability. | Independent editing guidance; preserves task requirements and meaning. Chat invocation does not authorize file edits. |
| [reasoned-advocacy](../skills/reasoned-advocacy/SKILL.md) | Build or challenge a defensible position, evaluate counterarguments, or prepare for stakeholder questions. | Quick or Deep; reasoning and spoken defense, not implementation planning or automatic persistence. |
| [blind-comparison](../skills/blind-comparison/SKILL.md) | Request an independent, anonymized comparison or ranking of alternatives. | Delegates to a reviewer; reports its ratings and limitations and may propose changes without silently implementing them. |
| [grilling](../skills/grilling/SKILL.md) | "Grill my plan" with one consequential question at a time. | Explicit design interrogation, not ordinary planning. |
| [review-before-approval](../skills/review-before-approval/SKILL.md) | "Final approval check" before consequential unapproved action. | Approval brief, not execution or unblock. |
| [commit-changes](../skills/commit-changes/SKILL.md) | Explicitly create a scoped local Git commit. | Preserves unrelated work and reviews the staged diff; never pushes automatically. |
| [run-and-manage-python](../skills/run-and-manage-python/SKILL.md) | Before Python execution, including interpreter/import probes, tests, evaluations, or dependency changes. | Own root/activation section and first use; manage AND execute through compatible independent uv purpose projects. |
| [create-markdown-diagrams](../skills/create-markdown-diagrams/SKILL.md) | Add or improve a Mermaid diagram or chart in Markdown. | Visualization of understood material, not architecture decisions. |
| [yagni](../skills/yagni/SKILL.md) | "Simplify", "do less", "avoid overengineering", "YAGNI". | Deliberate minimalism; still meet correctness and safety. |
| [humanize-spoken-output](../skills/humanize-spoken-output/SKILL.md) | Rewrite spoken scripts, narration, and interview answers naturally. | Content editing, not technical teaching. |

## Retained — not selected in `personal-skills.toml`

| Skill | Reach for it when… | Note |
| --- | --- | --- |
| [workspace-setup](../skills/workspace-setup/SKILL.md) | Request coordinated setup/refresh or an approved legacy-block migration. | Optional; follows skill-owned sections and preserves position/custom text. |
| [document-text-extraction](../skills/document-text-extraction/SKILL.md) | Explicitly extract a named PDF/image locally. | Temporary extraction only; independent of KB and `evidence-authoring`. |
| [repo-audit](../skills/repo-audit/SKILL.md) | Request a dedicated whole-repository risk/bloat audit. | Specialized full-repo report, not routine code review. |
| [ml-architecture-review](../skills/ml-architecture-review/SKILL.md) | Explicitly request focused ML architecture decision analysis. | Specialized investigation; separate from general technical options comparison. |

## Archived — not active

Historical sources live in `archive/skills/`, named by retirement date:

- Superseded by KB: `evidence-authoring`.
- Covered by manage-project-tasks and ordinary decision work: `execution-readiness`, `execution-topology`.
- Replaced by `tech-design-options` on 2026-11-11: [planning](../archive/skills/2026-11-11__planning-SKILL.md) (the replacement has a narrower job).
- Replaced by `code-design` on 2026-11-11: [engineering](../archive/skills/2026-11-11__engineering-SKILL.md) (ordinary execution remains with the main agent; the replacement has a narrower job).
- Covered by `yagni`: `yagni-review`.
- Earlier technical teaching line, now consolidated into `learning`: `quick-orientation`, `human-technical-orientation`, `technical-coach`, `debrief` (via `explain-tech`).
- Replaced by `learning` on 2026-10-21: `explain-tech`, `learning-markdown` ([archived explain-tech](../archive/skills/2026-10-21__explain-tech-SKILL.md), [archived learning-markdown](../archive/skills/2026-10-21__learning-markdown-SKILL.md)).
- Converted into [Skill Design Guide](skill-design-guide.md): `skill-refinement-reference`.

## Replaced writing prompt

[improve-readability](../skills/improve-readability/SKILL.md) replaces `prompts/anti-mannered-prose.md`.
It includes the prompt's useful plain-language guidance and adds reader-focused
ordering, explanation, presentation, and meaning-preservation checks. The original
prompt is retained in [archive](../archive/prompts/2026-10-19__anti-mannered-prose.md),
not maintained as a second active instruction. `learning` and `create-markdown-diagrams` remain independent specialist skills, not dependencies.

## Specialist engineering skills — why these seven were selected

On 2026-11-18, the user reviewed 15 recommended Claude/developer skills and research on both skill effectiveness and skill-induced regressions. The aim was to fill Agent Core's **engineering-execution blind spots** for TripVerge (FastAPI, Next.js/React, MCP, private data and cross-client approval), not grow the catalogue for its own sake. The user approved seven focused specialists in this selected section; API/interface design was incorporated into `code-design` instead of adding an overlapping skill.

The seven have distinct jobs: framework-specific backend patterns, MCP tool construction, React/Next.js practices, visual frontend design, UI/accessibility review, security boundaries, and diff/PR code quality. They are deliberately bounded: no fixed MCP evaluation quota, automatic redesign, all-70-React-rules checklist, exhaustive security audit, generic review ceremony, or new permission to deploy/commit. The upstream reference for each is in its skill file.

**Not adopted in this pass:** browser-testing specialization, systematic debugging, test-driven development, verification-before-completion, Vercel deployment, standalone code simplification, CI/CD automation, and performance optimization. These remain usable upstream references or later candidates; a separate [Agent-Led Verification design task](../tasks/2026-11/verification-design/2026-11-11__evaluate-agent-led-verification.md) is still unresolved. The user explicitly deferred auto-invocation tuning and skill A/B experiments.

**Evidence limit:** [SkillsBench](https://arxiv.org/abs/2602.12670), [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) (including its October 2026 revision), and [Agent Skills Can Be Harmful](https://arxiv.org/abs/2608.11888) show benefits vary and overly prescriptive skills may worsen results. The `fastapi-patterns` benchmark result motivated scrutiny of version-matched FastAPI guidance, **not a measured improvement by our adapted `fastapi-practices` skill**. No TripVerge runtime, fresh-session routing, local harness installation, or skill-effectiveness tests were performed. For future admissions and refinements, use the [Skill Design Guide's evidence criteria](skill-design-guide.md#evidence-led-selection-of-specialist-engineering-skills). Manifest selection alone is not local installation.

## Before making another skill

Check this catalogue, identify the nearest active skill, and decide whether the missing behavior is a **mode or edit** rather than a new job. See [Skill Design Guide](skill-design-guide.md). Never infer installation from directory presence.
