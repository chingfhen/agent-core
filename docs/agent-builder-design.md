---
title: Agent Builder Design Direction
description: Accepted direction and invariants for consolidating persistent workspace-agent workflows; not the live runtime contract.
updated: 2026-11-25
---

# Agent Builder — Design Direction

## Read First

- **Consolidation without regression.** Build a modular canonical skill for the persistent agent and its operating environment. The human has accepted the direction, not a production implementation or migration.
- Current [workspace configuration](workspace-configuration.md), individual skills, publication manifests and installed copies remain authoritative until an approved replacement is validated.
- Preserve distinct resource semantics, narrow permissions, reusable knowledge and familiar cues. Optimize for future-session continuity, discoverability, predictable organization, low maintenance and recoverability.
- Research-informed practice and concise observability are general skill-authoring principles; see [Skill Design Guide](skill-design-guide.md).

## Agent and resource boundaries

An agent is attached to a human-selected workspace, not necessarily a code repository or a project. Multiple projects can share domain knowledge, operating constraints, skills and utilities; a project can span multiple independently owned repositories. Repositories may be inside or outside the workspace; register their verified locations, aliases, project associations and responsibilities. Routing does not grant access or mutation rights. Humans select agent/workspace boundaries and approve new project identity; agents manage ordinary child organization within authorized roots. Separate confidentiality/ownership domains rather than sharing memory indiscriminately.

Agent Builder owns the persistent lifecycle, not all methods of working. Consolidation targets workspace setup, project tasks/docs, knowledge base, agent lessons, scripts, and **the complete reusable Python environment and execution contract**. Python's purpose is to avoid transient environments and repeat discovery, keeping personal uv state independent of team configuration; maintain its mandatory before-execution routing, create/reuse cues and safety gates. The exact activation mechanism and transition are open, not a decision to weaken or drop the guard. Learning, readability, design, delegation and other work-performing skills remain independent.

## Shared conventions

Preferred baseline (foundation to finalize exact names and exceptions):

```text
<workspace>/
  AGENTS.md
  .work-context/                 # configurable root, stable once chosen
    projects/<project>/
      tasks/INDEX.md
      tasks/YYYY-MM/<workstream>/...
      docs/
    knowledge-base/
      index.md
      records/YYYY-MM/index.md
      knowledge/
      managed/
    archive/YYYY-MM/
    scripts/INDEX.md
    python/<purpose>/
  <independent repositories, if locally placed here>
```

Tasks and docs default to project scope; shared records, living knowledge, managed artifacts, scripts and Python environments to agent scope. Archive is human-supplied raw material. Use stable designated folder names and semantic grouping; agents select filenames and child folders within agreed conventions. Prefer YYYY-MM and date-based names, preserve stable legacy paths and explicit existing destinations, and do not mass-migrate merely for consistency. Foundation must settle exact casing/separators and any needed exceptions. No mandatory empty directories, redundant indexes, global dashboards or extra registries. Prefer existing task indexes, KB navigation and script indexes; concise projects/repository routing belongs in AGENTS.md unless actual scale warrants an external index. Docs indexes optional when useful.

## Instruction management and retrieval

One Agent Builder managed block in the applicable AGENTS.md, with internally scoped subsections for resource routing, project/repository registrations, continuity, behaviors and lessons; preserve human-authored/outside guidance and unrelated owners. Central ownership does not mean broad rewrite authority. Keep essential pre-action rules and concise retrieval cues readily available. Retrieve selective task/doc/knowledge evidence in ordinary work without triggering maintenance. Project orientation should reveal active tracks and next actions when relevant, not scan the whole KB each session.

Human-directed behaviors and agent-discovered lessons are separate capabilities and cues, even though both influence future instructions. Explicit preference is not an evidence-based lesson; lessons use the existing counterfactual and proportionate intervention methodology. Avoid bloating instruction files; detailed procedures belong at their canonical authority with actionable pointers.

One canonical instruction source, reliably loaded workspace entry point, and recoverable state are requirements. Concrete root Git boundary versus materialization/symlink or other mechanisms is deferred. Do not assume file presence establishes loading or local Git is a device-loss backup. Employer data stays in approved locations; no incidental publication.

## Modules and maintenance

Thin root SKILL.md owns shared architecture, conventions, cue routing, one managed block, permission rules and coordination. Specialized procedures live in linked references, read selectively. Candidate modules: setup, projects, repositories, continuity, tasks, docs, KB/records/knowledge/managed artifacts, archive, behaviors, lessons, scripts, Python, sync and recovery. Exact file split remains open: no unnecessary file per concept. Explicit "load Agent Builder" is acceptable; preserve familiar natural-language cues and test activation.

Targeted maintenance stays targeted. A coordinated sync can evaluate relevant authorized surfaces once, route each durable claim to one primary authority and verify affected writes. Reading is not permission to maintain; saving state does not authorize implementation, spending, commits/pushes or external actions. Maintain no-op outcomes, narrower local gates and verified readback. Managed artifacts still require explicit human intent.

**Intentional archive change:** new design removes inbox as a staging queue. Human places original files in a predictable month directory, identifies selected source for capture, and agent preserves original in place with a source locator/provenance in records. No default archive scan, move, rename or deletion. Current KB inbox behavior remains live until migration.

## Migration constraints

- Inventory all substantive original contracts and supporting references, including backend/routing and execution safeguards. Maintain a temporary coverage map: preserved, centralized, intentionally changed or retired with reason. Verify meaningful behavior, not merely file count.
- Keep old skills and installed workflows until approved replacement passes representative activation, fresh-session retrieval, targeted sync, permissions, consistency, failure and recovery checks. Inspect direct dependent skills and references, manifests and installation/retirement rules. Ordinary sync does not remove old copies.
- Parent retains architecture, cross-cutting contracts, integration and final verification. After foundation agreement, evaluate bounded module migration delegation using the canonical delegation skill; verify harness, model, effort, isolation and approval. No speculative swarms.
- YAGNI: existing Git/Markdown and native uv remain baseline. Avoid new services or ceremonies absent concrete need.

## Related

- [01 — Foundation and shared contracts](../tasks/2026-11/agent-builder/2026-11-25__foundation-and-shared-contracts.md)
- [02 — Tasks and docs migration](../tasks/2026-11/agent-builder/2026-11-25__tasks-and-docs.md)
- [03 — Knowledge and archive migration](../tasks/2026-11/agent-builder/2026-11-25__knowledge-and-archive.md)
- [04 — Behaviors and lessons](../tasks/2026-11/agent-builder/2026-11-25__behaviors-and-lessons.md)
- [05 — Scripts and Python](../tasks/2026-11/agent-builder/2026-11-25__scripts-and-python.md)
- [06 — Routing, setup and continuity](../tasks/2026-11/agent-builder/2026-11-25__routing-and-continuity.md)
- [07 — Persistence and recovery](../tasks/2026-11/agent-builder/2026-11-25__persistence-and-recovery.md)
- [08 — Integration, validation and migration](../tasks/2026-11/agent-builder/2026-11-25__integration-and-migration.md)

Historical rationale: [KB capture](https://github.com/chingfhen/knowledge-base/blob/main/knowledge-base/records/2026-11/agent-workflows/2026-11-25--agent-builder-consolidation.md). Project tasks hold next actions; this page is the design direction, not a live operating manual.
