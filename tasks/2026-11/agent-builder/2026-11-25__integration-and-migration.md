# Task: Agent Builder — Integration, validation and migration

**File:** `tasks/2026-11/agent-builder/2026-11-25__integration-and-migration.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-26
**Priority:** Next
**Status:** Active

**Goal:** Integrate modules and prove consolidation without regression before retiring originals.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; foundation approved 2026-11-25. Read canonical shared contracts; module details require human agreement.
**Current State:** Tasks 01–07 completed at their agreed source scope; Agent Builder root and seven references authored, including explicit persistence/recovery. No integrated behavioral validation, worker launch, harness publication/install or workspace migration performed. Task 08 design and acceptance plan not yet approved.
**Next Action:** On human-started Task 08, inspect actual source and original contracts/dependents, reconcile coverage, discuss integration and representative independent acceptance plan; obtain scoped approval for source changes/tests, publication and retirement separately.
**Blockers:** Await human-started Task 08 design and scoped implementation/test approval; module prerequisites satisfied.

## Permission and scope

Test routing/cues, read vs write, task continuation, docs/KB/lessons, selected archive capture, scripts and Python, failure paths, recovery, dependent skills, manifests and fingerprint-safe retirement; no automatic install or merge. Saving this task is not approval to implement, publish/install, migrate, or run workers.

Validate deliberate changes (new naming, no synthesis/inbox, broader maintenance autonomy, routine Python utilization without skill) alongside preserved contracts. Verify dependent callers, old-path compatibility, actual activation/utilization and safe retirement. Include safe isolated fixtures for optional Git root allowlist (approved state eligible, new nested repositories and sensitive/generated paths excluded, already-tracked/override gaps detected), Git-free workspace, canonical loading from actual supported harnesses and intended nested/external entry points, approved alternative boundaries where relevant, fresh-session recovery and partial failure. No live workspace initialization, backup configuration, migration, publication or retirement without separate authorization.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — completed design approval, initial inventory and acceptance conditions; read before module design.
- [Task 07 — Persistence and recovery](./2026-11-25__persistence-and-recovery.md) — settled source contract, actual harness loading/recovery not yet demonstrated.
- [Agent Builder root](../../../skills/agent-builder/SKILL.md) and all applicable references — actual authored source to integrate, not a new design from scratch.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — foundation is agreed, but this module's interfaces and implementation plan are not yet ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
