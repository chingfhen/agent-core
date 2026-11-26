---
title: Workspace Configuration
description: Current persistent-workspace routing, continuity, maintenance and migration contract.
updated: 2026-11-26
---

# Workspace Configuration

## Read First

- [Agent Builder](../skills/agent-builder/SKILL.md) is the canonical workspace maintenance source. Its [approved design](agent-builder-design.md) preserves the rationale; individual references own detailed procedures. Source integration and manifest selection are complete; actual harness behavior and workspace adoption are not established by publication.
- Agent Builder owns persistent workspace context. Ask to set up or refresh the agent, register a project, sync tasks/docs/KB, capture lessons, maintain scripts or a Python environment, or hand off/close out work. It loads the relevant reference for maintenance; ordinary discovery and compatible Python utilization need no maintenance skill. Human controls timing and scope; narrower permissions prevail. It uses one managed AGENT BUILDER block for newly configured workspaces, with confirmed locators and selective utilization cues. Existing resource locations, legacy owner blocks and custom instructions remain valid until explicitly migrated; sync does not modify workspace guidance, Git configuration, or resources. Preserve employer confidentiality and do not transfer work material to personal storage.
- Previous independent resource skills remain unselected historical comparison/rollback source. For old guidance, use the matching Agent Builder reference and preserve established paths and gates. Existing workspaces are not automatically migrated.
- Git Workflow and Learning Notebook retain their own independent instruction ownership, caller-specific gates and procedures.

## Skill-Owned Guidance

### Guidance admission

One canonical editable workspace AGENTS.md, with one Agent Builder-managed block when adopted. Confirm workspace scope with the human; do not infer it from cwd, Git root, repository or harness. Keep essential before-action constraints, resource locators, a few when-to-read cues and concise behavior/lesson projections. Detailed procedures remain in the root and references. Read relevant docs, actual tasks/evidence, KB records and relevant active/retired artifacts, applicable behaviors/lessons and existing scripts proactively when useful; no maintenance activation is required for recall or compatible routine Python use. A found path is not proof of actual harness loading. Read-only discovery grants no write or execution authority.

### Interactive capture and deferred offline memory maintenance

Human-triggered maintenance selects relevant references and smallest useful changes. Capture reusable agent-facing records with provenance and uncertainty; retain selected originals, no automatic inbox cleanup or new synthesis layer. Legacy knowledge pages remain readable, with consequential claims checked against evidence. Managed artifact creation/update/retirement/restoration requires explicit intent. Retirement moves selected artifacts to searchable retired/; the root links its index and lists active managed artifacts only. No routine retired-artifact updates. Offline reflection/dreaming remains deferred; no background sync or worker launch is implied. The [memory pilot](memory-pilot.md) is independent.

### Ownership and maintenance

One primary authority per claim. Tasks own unfinished work; docs own settled project meaning; records own reusable findings; behaviors own explicit personal persistent instructions; lessons own evidenced operational improvement; scripts own reusable deterministic utilities; Python recipes/pins/locks own purpose environments; code/config/tests and observed evidence own actual implementation claims. Independently owned repository guidance stays independent. Docs may maintain explicitly assigned guidance, subject to other owners and local restrictions.

Preserve custom wording, position and outside text. Read before mutation; refuse ambiguous/duplicate/incomplete/nested markers or unsafe paths; reconcile concurrent changes and verify scoped diffs. Existing separate owner blocks remain authoritative until explicitly approved migration. Translate only confirmed path bases, preserve custom restrictions and remove superseded duplicate routing together, without moving contents. Supporting persistence precedes pointers. Report partial failures, don't weaken gates.

### Resource resolution and first use

Prefer an explicit operation destination, then confirmed routing. Discover a verified compatible existing resource using bounded metadata/content; reuse without changing configuration during read-only work. Register unambiguous existing resources during authorized maintenance; obtain approval for new resource initialization and new project identity. Report inaccessible configured resources rather than inventing alternatives. New relative paths resolve from the declaring AGENTS.md; preserve legacy bases, remote locators and backends.

Default proposals only:

```text
<workspace>/AGENTS.md
<workspace>/.work-context/
  projects/<project>/tasks/index.md
  projects/<project>/tasks/YYYY-MM/<workstream>/YYYY-MM-DD--description.md
  projects/<project>/docs/
  knowledge-base/index.md
  knowledge-base/records/YYYY-MM/index.md
  knowledge-base/managed/
  knowledge-base/retired/index.md
  archive/YYYY-MM/
  behaviors.md
  lessons/index.md
  scripts/index.md
  python/<purpose>/
```

No empty collections or competing indexes required. Established uppercase INDEX.md, dated names, archive/knowledge-base and learning-notebook locations remain valid. Register repositories by verified identity and checkout separately; multiple repositories or no repository per project are valid. Registration grants no mutation or transfer authority.

## Task Continuity and Deliverables

Use [tasks.md](../skills/agent-builder/references/tasks.md) for task maintenance and saved-task execution, not reading. One stable file per independently continuable outcome. The unfinished-work index preserves priority, state and next action/re-entry; closed files stay discoverable. Select Brief/Standard/Detailed as useful. Keep evidence, deliverables, approval and actual verification distinct; priority and a saved plan grant no implementation permission.

### Resume context

Use known task or index then bounded search across dates and aliases; read the actual task and required sources, verify consequential live state and reconcile stale instructions. Recommend next task when several meaningful tracks exist. Preserve goal, constraints, rationale, evidence, blockers and next permitted action. An inaccessible required source is a readiness gap; status orientation stays read-only.

## Coordinated Handoff and Closeout

Explicit pause/handoff/closeout authorizes bounded relevant maintenance, not launching workers, implementation, publication or migration. Load tasks.md and only justified additional references. Preserve supporting material before pointers, reconcile actual task and index, keep required incomplete work pending unless explicitly waived, and provide a short resume cue. Narrower "task only" and repository rules prevail. Routine checkpoints do not trigger a whole-context review.

## Operational Lessons

Use [behaviors.md](../skills/agent-builder/references/behaviors.md) for explicitly requested persistent preferences and [lessons.md](../skills/agent-builder/references/lessons.md) for evidence-based operational learning. Admit useful behavior-changing knowledge, choose the smallest intervention, check applicability/interference and preserve no-change outcomes. Do not invent human-owned permissions or strategic choices. Essential universal rules appear in guidance as concise consistent projections; conditional detail stays in its authority. Scripts have a separate human-triggered stewardship boundary.

## Optional Setup and Invocation

Setup and registration are explicit requests, not per-session preflight. Select actual harness and verify guidance loading on fresh entry points. Routine compatible Python execution follows confirmed guidance and exact selected interpreter; load [python.md](../skills/agent-builder/references/python.md) when maintenance, missing guidance or incompatibility requires it. Protect independent team environments, verify runtime, and never silently fall back.

Git persistence and recovery are optional explicit requests. Default-deny allowlist assistance must review actual candidate/index paths, nested repositories, overrides, secrets and generated state; ignore rules are not security controls. Local storage, history and remote transfer are separate decisions. Prefer the real workspace-root AGENTS.md as sole editable authority. Indirection requires proven compatibility and approval. Preserve employer boundaries; sync must not configure workspace Git, backup, global guidance or credentials. Verify actual fresh-session loading and recovery before making strong claims.

## Planned Agent Builder consolidation

Historical design is now delivered at source scope; see [Task 08](../tasks/2026-11/agent-builder/2026-11-25__integration-and-migration.md). The human elected controlled personal use instead of extensive synthetic validation. Runtime validation remains unperformed. Use the [operating manual](agent-core-operating-manual.md#set-up-or-refresh-a-workspace) for adoption and conflict handling; do not claim all harnesses verified.

## Related

- [Operating manual](agent-core-operating-manual.md)
- [Skill design guide](skill-design-guide.md)
- [Distribution and migration](consumer-repo-enrollment.md)
- [Approved design](agent-builder-design.md)
