# Task: Agent Builder — Foundation and shared contracts

**File:** `tasks/2026-11/agent-builder/2026-11-25__foundation-and-shared-contracts.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Now
**Status:** Closed — Completed (design approval only)

**Goal:** Agree with the human on a lean shared architecture and module interfaces before migration.
**Deliverables:** Approved foundation design, initial source-contract inventory/coverage approach, module boundaries, open decisions and acceptance conditions.
**Success Bar:** Human approves concrete shared contracts; downstream tasks can continue without rediscovering prior discussion.
**Chosen Direction:** [Approved foundation](../../../docs/agent-builder-design.md), accepted explicitly on 2026-11-25.
**Current State:** Human approved architecture, revised naming/index conventions, removal of synthesis layer, broader agent-selected maintenance, proactive utilization, Python utilization/maintenance split, autonomous scripts and evidence-driven standing lessons. Design persistence only; no production implementation, harness tests, worker launch, skill publication/install or workspace migration.
**Next Action:** Resume [Task 02 — Tasks and docs migration](./2026-11-25__tasks-and-docs.md) for human-led module design; no implementation until separately approved.
**Blockers:** None for foundation closure. Downstream design and implementation/worker approvals remain separate.

## Approved design and scope

The canonical foundation document owns shared paths, naming, ownership, timing, retrieval, instruction block, root/ref responsibilities, coordination and migration contracts. Human controls maintenance timing and consequential scope; agent owns how to maintain established context and may select additional justified references. The human explicitly approved autonomous creation/testing of useful personal scripts and evidence-driven standing lessons, subject to existing boundaries. Read-side retrieval and known compatible Python use do not need the skill; maintenance requires root and applicable reference. AGENTS.md must actively reinforce relevant utilization. No implementation authorization.

## Initial source-contract inventory

| Source | Preserve / centralize |
| --- | --- |
| [manage-project-tasks](../../../skills/manage-project-tasks/SKILL.md) and routing/handoff | Task identity, priority/status, permission, next permitted action, stable paths, context map, state/index reconciliation, authorized checkpoints, closeout, delegation receipt |
| [maintain-project-docs](../../../skills/maintain-project-docs/SKILL.md) and routing | Settled meaning, claim-specific authority, admission, conflict handling, north star, scoped docs/link maintenance |
| [maintain-knowledge-base](../../../skills/maintain-knowledge-base/SKILL.md) and authoring/retrieval/routing/filesystem/GitHub | Record grouping, provenance, scope, selective retrieval, managed artifacts, safe retries and backend verification; explicitly retire new synthesis and inbox workflow only after approved transition |
| [improve-agent-workflows](../../../skills/improve-agent-workflows/SKILL.md) | Evidence-driven lessons, future-session counterfactual, interference, conditional pointers, smallest intervention, scope and no recursion |
| [project-scripts](../../../skills/project-scripts/SKILL.md) and CLI craft | Utility admission, safe interfaces, existing callers, tests, index and execution boundary |
| [run-and-manage-python](../../../skills/run-and-manage-python/SKILL.md) and routing | Independent uv purpose projects, actual targeting and execution, recipes/lock/pin, concurrency, team separation, safety/runtime verification; change mandatory skill-read for routine utilization |
| [workspace-setup](../../../skills/workspace-setup/SKILL.md) and defaults | Confirmed resource resolution, initialization approval, legacy compatibility, guidance maintenance |

Initial dependency search found ease-into-work, define-success, git-branch-to-review, delegate-implementation, learning-notebook, reasoned-advocacy, manifests, sync engine, catalogue, operating manual and tests referencing source identities. This is preliminary, not a complete porting audit. Build a temporary coverage map before porting, recording each contract as preserved, centralized, intentionally changed or retired with rationale and verification. Inspect actual callers and supporting refs during each module; no duplicate canonical procedures.

## Acceptance conditions for downstream integration

- Actual fresh-session cues route to the right root/ref; ordinary retrieval/utilization works without the skill; unrelated requests do not trigger maintenance.
- Relevant project/KB/task/script/environment context is actually discovered and applied; no whole-workspace scan or stale instruction reliance.
- Human-triggered maintenance reads primary reference, autonomously selects useful others, respects explicit limits/ownership, preserves narrower gates and no-op behavior; lessons/scripts cannot expand authority.
- One managed block preserves custom and unrelated content; existing paths/indexes/callers remain usable; new naming applies without mass renaming.
- Fresh-session task resumption/handoff preserves goal, evidence, permission, next action and actual verification; partial failure and inaccessible resources are surfaced.
- Python routine use reuses a compatible environment safely without skill read; mutations load python.md and preserve team isolation, lock/pin, targeting, concurrency and actual execution checks.
- Selected-source capture preserves original, provenance and backend boundaries; no new synthesis layer or inbox cleanup; old resources are not silently removed.
- Actual target-harness loading/recovery, migration compatibility and fingerprint-safe retirement are tested before old skills are removed. Static links/schema checks alone are insufficient.

## Open decisions and dependencies

Task 02 owns detailed tasks/docs; Task 03 owns archive/legacy synthesis and inbox transition; Task 04 owns behavior/lesson admission; Task 05 owns Python read/run/mutation boundary and activation cues; Task 06 owns routing/setup/continuity and exact reference triggers; Task 07 owns concrete AGENTS.md persistence and recovery; Task 08 owns integration, acceptance and publication/retirement plan. Exact specialist reference splits and any compatibility entry points remain conditional on module design/tests. No speculative infrastructure.

[Prior workflow-continuity task](../workflow-continuity/2026-11-08__refine-discovery-and-handoff.md) is still pending independent human review; useful contracts are migration inputs, not evidence of accepted branch or automatic closure.

## Verification and delegation

Design review read canonical design, current workspace configuration, updated skill design guide, source skills and relevant references, prior KB rationale, downstream tasks, manifest and targeted dependency searches. Human explicitly accepted the revised foundation and requested sync to docs, tasks and KB on 2026-11-25. No behavioral tests or implementation were performed.

Decision: defer implementation delegation until module contracts and implementation plans are ready. Parent owns foundation/integration and final verification; later use delegate-implementation with verified harness/model/effort/isolation and human approval. No workers authorized or launched.
