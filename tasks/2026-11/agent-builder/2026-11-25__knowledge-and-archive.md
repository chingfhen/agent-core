# Task: Agent Builder — Knowledge and archive migration

**File:** `tasks/2026-11/agent-builder/2026-11-25__knowledge-and-archive.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Now
**Status:** Closed

**Goal:** Preserve shared agent-scoped knowledge and simplify raw artifact capture.
**Deliverables:** Agreed scoped design followed by implementation of knowledge-base.md and necessary scoped root changes on explicit human cue; verify saved source and preserve source contracts.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Human-approved editable agent-facing records with optional synthesis, explicit human-facing managed artifacts, selected originals in place, bounded maintenance and backend-specific persistence. Human explicitly authorized scoped implementation on 2026-11-25.
**Current State:** Scoped source delivery complete in [afa1d71](https://github.com/chingfhen/agent-core/commit/afa1d716483ac2604f8ae5be9dae7d211f1c27df): root, knowledge-base.md, kb-filesystem.md and kb-github.md. No runtime adoption.
**Next Action:** None for this closed task. Continue Task 04 (behaviors and lessons) only on a human cue; Task 08 owns integration and behavioral validation.
**Blockers:** None for scoped completion.
**Closure:** Completed (scoped source delivery, not runtime adoption).

## Permission and scope

Intentionally replace inbox processing in future design; preserve originals in place, require a selected source, provenance, scoped backend access, explicit managed artifact requests and legacy compatibility. No employer-to-personal transfer. Scoped source authoring was explicitly authorized and completed. No installation, migration, retirement, worker launch, or other module implementation authorized.

New design excludes a separate knowledge/ synthesis layer and inbox staging. Legacy pages and selected inbox inputs remain readable; no deletion/migration implicit. Preserve records and managed artifacts, selected archive originals and indexes.

## Decisions and verification

- Records are primarily consumed by agents; concise, reusable evidence and explanation, not human editorial quality. Managed artifacts serve explicit human purposes and may be retired/discarded on explicit request under safe disposition and navigation rules.
- Editable records with selective synthesis; reuse existing findings, check likely matches only, no mandatory parallel synthesis or broad reconciliation. Root efficiency rule applies to all maintenance modules.
- Preserve authoring, source basis, grouping, stable dated paths, root/month indexes, managed updates, selective retrieval, routing, privacy, safe retries and proportionate verification. Centralize shared setup/ownership in root; retain separate local/remote backend procedures. Intentionally replace routine inbox copy/verify/remove with selected-source read-in-place, and separate living pages with optional synthesis. Preserve legacy locators/read compatibility. Default KB AGENTS.md retrieval fragment authored; full template and setup integration Task 06, loading/recovery Task 07.
- Source commit exact four-file scope verified against parent; all four files read back exactly at commit before guarded non-forced main update. No harness invocation, capture latency benchmark, end-to-end filesystem/remote KB behavioral tests or exhaustive dependency audit. Task 08 owns these checks and separately authorized transition.
- External design references checked: Anthropic context engineering, W3C PROV overview, GitHub Git trees; encoded selective retrieval/provenance/batching rather than recurring research requirements. No measured Agent Builder efficiency claim.

## Resume Context

- [Design direction](../../../docs/agent-builder-design.md) — shared accepted direction and scope; read first.
- [Skill design guide](../../../docs/skill-design-guide.md) — research as reusable expertise and concise decision/verification observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — current contract, not yet replaced.
- [Foundation task](./2026-11-25__foundation-and-shared-contracts.md) — completed design approval, initial inventory and acceptance conditions; read before module design.
- [Agent Builder root](../../../skills/agent-builder/SKILL.md) — shared contract and efficiency.
- [KB module](../../../skills/agent-builder/references/knowledge-base.md) — approved scoped implementation.
- [Filesystem adapter](../../../skills/agent-builder/references/kb-filesystem.md) and [GitHub adapter](../../../skills/agent-builder/references/kb-github.md) — persistence and verification.
- [Completed Task 02](./2026-11-25__tasks-and-docs.md) — scoped authoring precedent and verification limits.
- [Next module: Behaviors and lessons](./2026-11-25__behaviors-and-lessons.md) — human-started design only.
- [Integration and migration](./2026-11-25__integration-and-migration.md) — full source coverage and representative validation, no automatic adoption.

## Delegation decision

Main-agent execution — scoped source authoring and integration of related references are tightly coupled; no workers launched. Later modules require their own planning and authorization.
