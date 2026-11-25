# Task: Agent Builder — Foundation and shared contracts

**File:** `tasks/2026-11/agent-builder/2026-11-25__foundation-and-shared-contracts.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Now
**Status:** Active

**Goal:** Agree with the human on a lean shared architecture and module interfaces before migration.
**Deliverables:** Agreed foundation design brief, source-contract inventory/coverage approach, explicit module boundaries and open decisions, reviewable acceptance conditions.
**Success Bar:** Human can approve a concrete shared contract without needing to rediscover prior discussion; downstream work has stable inputs and no unresolved cross-cutting ambiguity disguised as a decision.
**Chosen Direction:** Modular Agent Builder; see canonical design direction. Details require discussion and approval.
**Current State:** Direction accepted; no production implementation or tests, worker launch, publication or workspace migration performed. Ready for a human-started design discussion.
**Next Action:** Read the design direction, current source skills and relevant references; compare unresolved options with YAGNI. Produce a reviewable foundation decision brief; discuss and obtain human agreement, not implementation approval.
**Blockers:** None for design discussion. Human approval required before implementation or worker launch.

## Permission and scope

No implementation or worker launch. Inventory substantive contracts and external callers before porting. Settle stable paths/naming, resource scope, one managed block, authority, permission gates, module routing, index policy and migration compatibility. Leave the concrete AGENTS.md persistence mechanism to task 07. Saving this task is not approval to implement, publish/install, migrate, or run workers.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- Read canonical source SKILL.md files and applicable references for manage-project-tasks, maintain-project-docs, maintain-knowledge-base, improve-agent-workflows, project-scripts, workspace-setup and run-and-manage-python. Use tech-design-options and yagni. Read delegate-implementation for later planning, not worker launch.
- [Prior workflow-continuity task](../workflow-continuity/2026-11-08__refine-discovery-and-handoff.md) — related older candidate; reconcile overlap before supersession or integration; no automatic closure.

## Delegation decision

Defer — shared contracts and module interfaces are not implementation-ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
