# Task: Agent Builder — Integration, validation and migration

**File:** `tasks/2026-11/agent-builder/2026-11-25__integration-and-migration.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Later
**Status:** Blocked

**Goal:** Integrate modules and prove consolidation without regression before retiring originals.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; see canonical design direction. Details depend on approved foundation and module design.
**Current State:** Direction accepted; no production implementation or tests, worker launch, publication or workspace migration performed. Awaiting prerequisite design decisions.
**Next Action:** After foundation and module decisions/implementation, prepare integration and independent acceptance plan; obtain approval for source changes, publication and retirement separately.
**Blockers:** Foundation and module outcomes, accepted implementation plan and approval.

## Permission and scope

Test routing/cues, read vs write, task continuation, docs/KB/lessons, selected archive capture, scripts and Python, failure paths, recovery, dependent skills, manifests and fingerprint-safe retirement; no automatic install or merge. Saving this task is not approval to implement, publish/install, migrate, or run workers.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — prerequisite agreed contract; read its verified outcome before designing this module.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — shared contracts and module interfaces are not implementation-ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
