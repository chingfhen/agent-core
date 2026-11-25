# Task: Agent Builder — Integration, validation and migration

**File:** `tasks/2026-11/agent-builder/2026-11-25__integration-and-migration.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Later
**Status:** Blocked

**Goal:** Integrate modules and prove consolidation without regression before retiring originals.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; foundation approved 2026-11-25. Read canonical shared contracts; module details require human agreement.
**Current State:** Foundation approved; no production implementation or tests, worker launch, publication or workspace migration performed. Module design not yet approved.
**Next Action:** After module decisions and authorized implementation, prepare integration and independent acceptance plan; obtain approval for source changes, publication and retirement separately.
**Blockers:** Module outcomes, accepted implementation plan and approval; foundation prerequisite satisfied.

## Permission and scope

Test routing/cues, read vs write, task continuation, docs/KB/lessons, selected archive capture, scripts and Python, failure paths, recovery, dependent skills, manifests and fingerprint-safe retirement; no automatic install or merge. Saving this task is not approval to implement, publish/install, migrate, or run workers.

Validate deliberate changes (new naming, no synthesis/inbox, broader maintenance autonomy, routine Python utilization without skill) alongside preserved contracts. Verify dependent callers, old-path compatibility, actual activation/utilization and safe retirement.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — completed design approval, initial inventory and acceptance conditions; read before module design.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — foundation is agreed, but this module's interfaces and implementation plan are not yet ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
