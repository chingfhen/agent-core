# Task: Agent Builder — Persistence and recovery

**File:** `tasks/2026-11/agent-builder/2026-11-25__persistence-and-recovery.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-26
**Priority:** Next
**Status:** Closed — Completed (source contract)

**Goal:** Ensure the canonical instruction source and agent state can be recovered and loaded reliably.
**Deliverables:** Agreed scoped design and implementation-ready handoff (after approval); preserve source contracts and verify representative outcomes.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Human approved minimal explicit persistence/recovery assistance on 2026-11-26. Direct workspace-root AGENTS.md and optional root Git allowlist preferred; local-only and approved alternative boundaries supported. See canonical design and root skill.
**Current State:** Tasks 01–07 completed at agreed source scope. Root skill now defines request-led Git allowlist setup and recovery, canonical authority, actual loading verification, tracking/confidentiality gates and partial failure handling. No live workspace modification, harness installation, worker launch, backup configuration or migration.
**Next Action:** Resume [Task 08 — Integration, validation and migration](./2026-11-25__integration-and-migration.md) on a human cue. Review source coverage, plan and obtain approval for representative tests and separately authorized adoption/retirement.
**Blockers:** None for source closure; actual target-harness loading and recovery validation remain Task 08 acceptance conditions.

## Permission and scope

No Git boundary migration, backups, or changes to employer workspace without approval. Verify ignore exclusions, tracked files, raw-source approval, canonical ownership, restore and instruction loading. Saving this task is not approval to implement, publish/install, migrate, or run workers.

Preserve one canonical instruction authority, reliable actual loading, recovery and employer boundaries. Concrete contract settled; no live Git initialization/migration, external transfer or backup authorized here.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — completed design approval, initial inventory and acceptance conditions; read before module design.
- [Task 06 — Routing, setup and continuity](./2026-11-25__routing-and-continuity.md) — completed source contract and verification limits.
- [Agent Builder root](../../../skills/agent-builder/SKILL.md) — existing setup/routing/continuity and one canonical managed block; extend, do not recreate.
- Read the relevant original skill(s) and all applicable references before porting.

## Outcome and verification

Human requested completion after agreeing that Agent Builder should be able to assist with allowlist setup when explicitly requested, without making Git mandatory or incidental. Define-success outcome: recover durable context and one authoritative instruction entry point, safely distinguish tracking and transfer, and establish real fresh-session use or report the gap. Tech-design-options compared direct root tracking, isolated context/materialization and Git-free operation; YAGNI selected native Git/Markdown/harness mechanisms with no new reference or code. Consulted the original workspace setup/defaults, repository guidance, foundation and Task 06; Git's ignore/check-ignore documentation supports the specific exclusion rules. Harness documentation was partially accessible; no version-specific loading claim or runtime test is made.

Source acceptance: existing root, shared design, task continuity and index reconciled; one managed block, human-controlled maintenance, independent repository authority, proactive utilization and hybrid continuation preserved. Verify saved source at the delivery commit and check the scoped diff. Actual allowlist setup on a human workspace, recovery and harness probes are not performed here; Task 08 owns representative validation. KB/lessons no-op: this is project architecture already owned by the design/root, not a separate reusable finding or new standing instruction for the live workspace.

Decision: parent implemented the small coupled Markdown change; no workers approved or launched.
