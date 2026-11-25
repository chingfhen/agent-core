# Task: Agent Builder — Persistence and recovery

**File:** `tasks/2026-11/agent-builder/2026-11-25__persistence-and-recovery.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Next
**Status:** Blocked

**Goal:** Ensure the canonical instruction source and agent state can be recovered and loaded reliably.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; see canonical design direction. Details depend on approved foundation and module design.
**Current State:** Direction accepted; no production implementation or tests, worker launch, publication or workspace migration performed. Awaiting prerequisite design decisions.
**Next Action:** After foundation approval, compare root Git allowlist, tracked context source materialized at root and supported alternatives; verify actual harness behavior when authorized.
**Blockers:** Approved foundation contract; then human-started module design.

## Permission and scope

No Git boundary migration, backups, or changes to employer workspace without approval. Verify ignore exclusions, tracked files, raw-source approval, canonical ownership, restore and instruction loading. Saving this task is not approval to implement, publish/install, migrate, or run workers.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — prerequisite agreed contract; read its verified outcome before designing this module.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — shared contracts and module interfaces are not implementation-ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
