# Task: Agent Builder — Routing, setup and continuity

**File:** `tasks/2026-11/agent-builder/2026-11-25__routing-and-continuity.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Next
**Status:** Closed — Completed (scoped source and static verification)

**Goal:** Make a fresh workspace agent discover projects, repositories and relevant active work without unnecessary scans.
**Deliverables:** Approved setup/routing/continuity design; existing root extended; task/docs default guidance fragments; verified source and next-session handoff.
**Success Bar:** Correct identity and ownership, low-friction setup, proactive relevant utilization, reliable continuation, efficient maintenance, non-destructive guidance and honest gap reporting. Task 06 establishes these as source contracts; actual fresh-session behavior remains subject to Tasks 07–08.
**Chosen Direction:** Human approved the proposed design and hybrid natural-language continuation on 2026-11-25, and explicitly authorized scoped implementation.
**Current State:** Root and two references authored and verified at source commit `c4b3f96aa8d2faf42de0d9a5e7ea02139acda80e`; canonical design and handoff reconciled. Other five module contracts unchanged. No runtime installation, migration, worker launch or harness trials.
**Next Action:** Human may start [Task 07 — Persistence and recovery](./2026-11-25__persistence-and-recovery.md) for discussion of reliable canonical loading and recovery; no Task 07 implementation approved.
**Blockers:** None for Task 06 source closure. Actual harness behavior and replacement/adoption remain downstream.

## Approved contract and source

- [Canonical design](../../../docs/agent-builder-design.md) owns the settled Task 06 direction and continuation rule.
- [Agent Builder root](../../../skills/agent-builder/SKILL.md) owns targeted setup, registration, resource resolution, hybrid orientation, managed-block integration, coordination and verification.
- [Tasks](../../../skills/agent-builder/references/tasks.md) and [docs](../../../skills/agent-builder/references/docs.md) now supply default guidance fragments alongside the other five modules. No new routing/setup/continuity reference or registry.
- Legacy [workspace configuration](../../../docs/workspace-configuration.md) and original skills remain live until authorized transition. Preserve existing paths, remote KB locators and independent instructions; registration is not access or mutation authority.

## Verification and remaining acceptance

At the source commit, reread the root and all seven module references. Confirmed all seven fragments and root links, hybrid continuation and human-choice fallback, legacy marker/conflict protection, no write authority from discovery, selective maintenance efficiency and downstream scope. Root/task/docs source commits were saved on main; transient GitHub write failures on docs were resolved using a verified candidate commit and successful non-force ref update. This establishes saved source content, not observed invocation, runtime safety or harness compliance. Task 07 owns concrete canonical instruction loading and recovery; Task 08 owns full source-contract regression, fresh-session cases (clear continuation, ambiguous tracks, relevant/unrelated lookup, external repository/multiple checkout, legacy setup, permission/partial failure), integration and separately authorized adoption.

## Maintenance and delegation

Main agent: tightly coupled Markdown changes, no worker approval or launch. Canonical design and task continuity are the appropriate authorities; no separate KB capture or standing lesson warranted (the transient connector issue is already covered by the existing verify-before-retry/partial-failure contract). No changes to live legacy guidance, manifests, installs, employer resources or Git/backup mechanisms.
