# Task: Agent Builder — Knowledge and archive migration

**File:** `tasks/2026-11/agent-builder/2026-11-25__knowledge-and-archive.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Next
**Status:** Blocked

**Goal:** Preserve shared agent-scoped knowledge and simplify raw artifact capture.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; see canonical design direction. Details depend on approved foundation and module design.
**Current State:** Direction accepted; no production implementation or tests, worker launch, publication or workspace migration performed. Awaiting prerequisite design decisions.
**Next Action:** After foundation approval, discuss records, synthesis, managed artifacts, backends, retrieval, indexes and selected-source archive capture.
**Blockers:** Approved foundation contract; then human-started module design.

## Permission and scope

Intentionally replace inbox processing in future design; preserve originals in place, require a selected source, provenance, scoped backend access, explicit managed artifact requests and legacy compatibility. No employer-to-personal transfer. Saving this task is not approval to implement, publish/install, migrate, or run workers.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — prerequisite agreed contract; read its verified outcome before designing this module.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — shared contracts and module interfaces are not implementation-ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
