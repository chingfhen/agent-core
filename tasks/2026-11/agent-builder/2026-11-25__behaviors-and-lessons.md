# Task: Agent Builder — Behaviors and lessons

**File:** `tasks/2026-11/agent-builder/2026-11-25__behaviors-and-lessons.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Now
**Status:** Closed

**Goal:** Establish distinct human-directed behavior and evidence-driven lessons capabilities.
**Deliverables:** Agreed scoped design, authored behaviors.md and lessons.md, targeted root/foundation changes, verification and continuation handoff.
**Success Bar:** The approved module contract is cohesive with the foundation, source behavior is preserved or explicitly changed, and relevant acceptance/permission conditions are clear.
**Chosen Direction:** Human-approved single living behaviors file and indexed topic-based lessons, hybrid always-visible and conditional utilization. Explicit implementation cue received on 2026-11-25.
**Current State:** Scoped source delivery complete in [76ba3b3](https://github.com/chingfhen/agent-core/commit/76ba3b37808be84ae2cc36ec55193905ef09f542). Two module references, root and foundation updated and verified. No runtime adoption.
**Next Action:** None for this closed task. Resume Task 05 on a human cue for scripts and Python design discussion; Task 08 owns integration and behavioral validation.
**Blockers:** None for scoped completion.
**Closure:** Completed (scoped source delivery, not runtime adoption).

## Decisions and source-contract coverage

- Agent-scoped default `.work-context/behaviors.md` is one living human-reviewable document; natural headings, explicit human persistent intent and scope, not inferred preferences or request chronology. Canonical cue: "remember this behavior"; persistent natural language equivalents work; temporary instructions do not persist; review-only is read-only. Human-owned preferences cannot be silently altered or retired.
- Agent-scoped default `.work-context/lessons/index.md` and undated kebab-case topic files represent current operational guidance, not one file per incident or a chronological log. Index holds topics, recognizable triggers and links; update affected files and navigation, consolidate and retire on evidence. No fixed taxonomy, scores, registries, mandatory reflection or background work.
- Hybrid utilization approved: essential universal behaviors and before-action constraints remain inline in the single managed AGENTS.md block; relevant behavior headings and lesson topics are retrieved selectively using confirmed locators, direct links, index and bounded search. No maintenance skill load for ordinary utilization. Curated guidance is distinct from KB evidence; reconcile projections rather than create competing authorities. Preserve legacy content and independent guidance until authorized migration.
- Preserve improve-agent-workflows contracts: autonomous discovery during authorized maintenance, causal diagnosis, future-session counterfactual, interference and future-use tests, narrow scope, smallest effective intervention, no-op, evidence qualification, conditional pointers, consolidation, safe persistence and verification. Existing source ownership and local gates remain. Root centralizes timing, reference coordination, marker safety, permission and reporting; no recursive handoff. New default resources intentionally supersede prior append-to-guidance architecture only in the future adopted design.
- Agent may introduce narrow checks and safer defaults, not independently create new permanent human-approval gates or expand permissions; consequential proposed changes to human-owned boundaries are surfaced. No per-lesson approval in established scope, but new resource initialization retains root approval. No inferred human preferences. Other interventions use appropriate owner and permission boundary; no speculative implementation or live script effects.
- Design basis encoded in lessons.md: AGENTS.md context cost study (arXiv 2602.11988), Anthropic context engineering, procedural skill negative-transfer study (arXiv 2605.23899), Google SRE postmortem analysis. No routine literature review, mandatory audits or claimed demonstrated performance benefit.

## Verification and limits

- Source commit checked against its exact parent: four intended files only. All four read back exactly at commit before guarded non-forced update to main; main head subsequently confirmed. Static checks confirmed layout agreement, reference routing, behavior admission/review, hybrid retrieval, lesson admission and topic navigation, read-side permission boundary, initialization and ownership, and Task 05's discussion-only gate.
- No fresh-session invocation/compliance tests, actual resource creation, behavior-effect benchmark, worker launch, installation, migration, retirement, or manifest changes. Task 06 owns setup/template integration; Task 07 owns reliable loading/recovery; Task 08 owns full dependency and regression coverage including relevant versus unrelated retrieval, preference preservation, lesson effectiveness and maintenance efficiency. No claim that static source verification demonstrates agent behavior.
- Project-specific decisions integrated into canonical foundation; no additional KB or workspace lesson entry needed because the durable architecture and source expertise already have authoritative homes.

## Resume Context

- [Approved design](../../../docs/agent-builder-design.md) — revised shared storage, hybrid utilization, authority and scope.
- [Agent Builder root](../../../skills/agent-builder/SKILL.md) — shared procedure and reference routing.
- [Behaviors module](../../../skills/agent-builder/references/behaviors.md) — admission, human-readable living resource, default guidance fragment.
- [Lessons module](../../../skills/agent-builder/references/lessons.md) — evidence-driven intervention, living topic collection, guidance fragment and research basis.
- [Original lessons skill](../../../skills/improve-agent-workflows/SKILL.md) — remains live pending authorized integration and retirement.
- [Skill design guide](../../../docs/skill-design-guide.md) — source expertise and verification.
- [Next module: Scripts and Python](./2026-11-25__scripts-and-python.md) — design discussion only on human cue.
- [Integration and migration](./2026-11-25__integration-and-migration.md) — representative validation and separately authorized transition.

## Delegation decision

Main-agent execution — tightly coupled source and shared-contract changes; no workers launched. Later modules require their own planning and authorization.
