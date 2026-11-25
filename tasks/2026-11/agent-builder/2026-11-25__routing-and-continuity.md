# Task: Agent Builder — Routing, setup and continuity

**File:** `tasks/2026-11/agent-builder/2026-11-25__routing-and-continuity.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Next
**Status:** Blocked

**Goal:** Make a fresh workspace agent discover projects, repositories and relevant active work without unnecessary scans.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Modular Agent Builder; foundation approved 2026-11-25. Read canonical shared contracts; module details require human agreement.
**Current State:** Foundation approved; no production implementation or tests, worker launch, publication or workspace migration performed. Module design not yet approved.
**Next Action:** When the human starts this module, design setup, registration, continuity, discovery and user-visible receipts.
**Blockers:** Awaiting human-started module design; foundation prerequisite satisfied.

## Permission and scope

Human chooses workspace/project identity; agent organizes children. Repos can be external; use verified paths and concise AGENTS.md routing, no automatic write authority. Preserve remote KB access and cross-harness limitations. Saving this task is not approval to implement, publish/install, migrate, or run workers.

Root SKILL.md owns setup, project/repository registration, instruction management and continuity; no separate workspace.md/continuity.md by default. Exactly one managed block with first-class actionable utilization/discovery instructions. Human controls timing; named maintenance reference required and additional references agent-selected.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — completed design approval, initial inventory and acceptance conditions; read before module design.
- Read the relevant original skill(s) and all applicable references before porting.

## Delegation decision

Defer — foundation is agreed, but this module's interfaces and implementation plan are not yet ready. Parent owns the foundation and integration; later planning may choose bounded workers with verified harness/model/effort/isolation and single human approval. No worker is approved or launched. Revisit only during authorized implementation planning.
