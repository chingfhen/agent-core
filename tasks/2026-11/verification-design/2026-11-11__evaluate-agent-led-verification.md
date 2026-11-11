# Task: Evaluate agent-led verification and failure discovery

**File:** `tasks/2026-11/verification-design/2026-11-11__evaluate-agent-led-verification.md`
**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Next
**Status:** Active

**Goal:** With the human, decide how agents should proactively own credible verification, failure discovery, and the observation paths needed to do that work; determine whether a separate `verification` skill is justified.

**Why:** The human often has to lead efforts to run the product, find failure cases, and establish whether an agent's changes actually work. They want bounded, managed initiative comparable to their other core workflows. They remain unsure of the proposed verification skill and requested only a detailed handoff for another session.

**Deliverables:** An evidence-grounded, human-reviewable recommendation: chosen ownership model, activation and stop conditions, boundaries, a concrete Tripverge pilot, and success criteria. If the human subsequently approves implementation, record its exact authorized scope before editing production skills or consumer projects.

**Success Bar:** The human can judge what the capability adds beyond ordinary execution and current guidance, who remains accountable, what causes it to run, what it may change, when it stops, and how a real feature would demonstrate its value. A polished skill file alone is not the desired outcome.

**Chosen Direction:** Unresolved. The previous agent proposed a focused `verification` skill connected to the former engineering workflow; this is not an approved design or implementation instruction.

**Current State:** No verification skill, consumer guidance, runtime instrumentation, or pilot has been implemented by this work. The former engineering skill has been retired; its archived instructions are historical evidence, not current execution ownership. The main agent and applicable guidance remain responsible for ordinary delivery and verification. Tripverge's inspected docs describe intended behavior; no working application or browser-testing setup was established in this assessment.

**Next Action:** In a human-started follow-up session, read the context below, inspect relevant current execution guidance and Tripverge evidence, and present/refine a bounded recommendation with the human. Use `design-options` only if the human requests a substantive comparison of technical approaches. Do not create the skill or begin the pilot without subsequent explicit approval.

**Blockers:** None for discussion/read-only investigation. Implementation is gated on the human selecting and approving a direction; missing runtime capability must be established rather than assumed.

## Permission and delegation

- Working repository for skill design: `C:\Users\tanch\.agent-core`. Follow its `AGENTS.md` before action. The human explicitly requested this task/index write and delegation brief.
- This is a handoff to another session, not an instruction to spawn a subagent now or a scheduled job. No agent has been launched by saving it.
- The next session may read and discuss relevant local sources and maintain this task when asked to resume/manage it. Production skill edits, Tripverge changes, tools/infrastructure installation, spending, internet exposure, deployment, Git publication, and harness sync require their own explicit scope approval.
- The human deferred acting on the broader critique of their memory/governance skills. Do not reopen a general simplification or policy cleanup under this task.
- Human teaching is a separate capability. Its approved revision is recorded in [the learning task](../learning-design/2026-11-11__strengthen-learning-teaching-method.md). Do not make verification responsible for assessing or proving human understanding.

## Problem and prior proposal

The practical gap is not another instruction to "run tests." It is agent ownership of the path from a behavior claim to evidence, including recognizing when the environment cannot reveal a relevant failure. The proposed loop is:

**Claim → realistic failure hypothesis → exercise → observation → diagnosis → in-scope correction → repeatable check.**

Observability is supporting infrastructure: logs, request traces, state inspection, browser behavior, or another useful signal. It cannot alone establish correctness. A screenshot can show UI state without proving persistence; a mocked host can exercise a contract without proving real-host compatibility; a green test can miss the defect it claims to protect against.

### Candidate responsibilities

1. Derive consequential claims from approved user outcomes and contracts, rather than reverse-engineering acceptance from the new implementation.
2. Select realistic failure paths by consequence, likelihood, and uncertainty. Do not expand into exhaustive hypothetical breakage.
3. Discover the run/check/inspection path. Within an approved implementation scope, establish the smallest missing fixture, check, or diagnostic capability needed for the feature. Surface larger work instead of silently taking it on.
4. Exercise the actual relevant behavior and inspect state/results; diagnose failures and fix in-scope causes without making the human lead every step.
5. Retain meaningful reproducible regression protection where it earns its cost. Not every exploratory experiment becomes a permanent test.
6. Report what was actually established and residual uncertainty; stop when adequate scoped evidence exists or a specific blocker prevents it.

### Ownership hypothesis to challenge

- The main agent owns delivery and final completion under applicable guidance. It cannot shed verification accountability because another skill was not loaded.
- A separate skill could own evidence planning and failure-discovery execution while using the same agent and existing tools.
- Relevant verification should shape substantial runtime work early enough to avoid an untestable design, then continue through completion. Trivial changes retain lightweight checks.
- Existing project tasks preserve real unfinished gaps; established project docs can hold settled run/inspection instructions under their own authorization. No new verification registry, mandatory report for every change, or competing task system.
- `learning` may explain the consequential mechanism using the same evidence at an invited debrief. It neither certifies software nor measures the human.

## Decisions the next session must resolve

Resolve evidence first and ask one consequential question at a time; do not begin with a large questionnaire.

1. Does the missing behavior require a distinct reusable skill, or a focused change to execution guidance and project setup? Compare outcomes and triggers, not just overlapping steps.
2. What is the smallest useful activation rule that gives initiative without running a broad audit for every edit? Does explicit invocation also support standalone investigation with no repair authority?
3. What observation-enabling work falls inside feature implementation, and what requires a separately approved infrastructure or privacy decision?
4. What counts as sufficient evidence for each relevant type of change? Distinguish static checks, unit/integration tests, browser behavior, real external hosts, and production-only claims.
5. How will a new session discover the agreed obligation and reusable checks without the human remembering a special command? Skill publication, consumer guidance, and executable checks are distinct adoption steps.

The prior Git workflow task excluded creating a general verification skill **within that Git workflow project**. Read its scope accurately; it neither authorizes this new proposal nor establishes a global prohibition against discussing it.

## Proposed Tripverge pilot — conditional on approval

Consumer repository: `C:\Users\tanch\Documents\Github\tripverge`. Read its current `AGENTS.md`, `docs/product.md`, `docs/architecture.md`, `docs/mvp.md`, and actual implementation before proposing changes. The inspected architecture names Next.js, FastAPI, Supabase, private Blob files, and assistant-facing domain operations; these are intended directions, not runtime evidence.

Use one small synthetic-data edit flow. The first slice should have a reproducible start path, deterministic sample data, a way to inspect relevant errors and saved state, and rerunnable checks. Match claims to what is actually implemented:

| Claim | Candidate evidence |
| --- | --- |
| An accepted edit persists | Save, independently reload/read, and inspect the resulting state. |
| Stale proposals cannot overwrite new revisions | Two clients read a revision; the second conflicting update cannot replace the first accepted update. Check the atomic compare/write boundary. |
| Failed saves are represented honestly | Exercise a controlled save failure; the UI must not show false saved success. |
| Trip/evidence authorization is enforced, once implemented | Use distinct synthetic identities and inspect denial without data leakage at the backend. |
| Both actual surfaces share authoritative state, once available | Demonstrate a real supported host and website using the same state. Local mocks do not establish real-host support. |

Product invariants also include approval tied to a revision, independent activity/booking states, and attached evidence not implying verified reservations. Select the relevant ones for the actual feature rather than making all of them first-slice requirements.

Use synthetic data and scoped local failure injection only when authorized. Keep private travel data, secrets, and booking identifiers out of fixtures, screenshots, and telemetry. Do not infer internet exposure, external accounts, paid observability, production fault injection, or security changes from a verification request.

### How to establish the proposal earns its place

After authorized implementation/adoption, a fresh session should handle a meaningful feature request without the human separately saying "test it": identify consequential failure risk, use an observation path, investigate failures, and provide reproducible evidence. Distinguish a real fresh-session trial from the author's self-review.

For an important new check, demonstrate that it detects its target failure when feasible—for example, failure against a known defect and success after the fix in an isolated authorized test context. Never weaken expected behavior merely to make the suite pass.

At a natural checkpoint ask whether the human still had to lead discovery, whether another session can reproduce the evidence, and whether the workflow created unnecessary work. No separate evaluation service or costly multi-agent setup is assumed.

## Stop conditions and anti-goals

- Proactive means initiative during authorized work, not an always-on monitor or background scheduling.
- Do not construct a telemetry platform, exhaustive test catalogue, new approval chain, or compulsory report before a concrete need exists.
- Reuse existing checks and tools; do not assume browser automation is available or install dependencies blindly.
- Bound retries and exploration by a changing diagnostic hypothesis. Preserve failed or missing evidence honestly.
- Distinguish implementation completion, verification coverage, and human acceptance. No self-certification or independent-review claim from a second prompt to the same agent.
- No generalized skill/memory redesign, automatic teaching assessment, cloud provisioning, or Tripverge architecture pivot under this discussion.

## Context and evidence for resumption

Read first:
- [Agent Core guidance](../../../AGENTS.md) — canonical ownership and explicit edit/publication gates.
- [Skill design guide](../../../docs/skill-design-guide.md) — burden of proof for a separate skill and standalone scope.
- [Former engineering skill](../../../archive/skills/2026-11-11__engineering-SKILL.md) — historical delivery and verification proposal evidence, not active guidance; inspect current execution guidance separately.
- [Learning](../../../skills/learning/SKILL.md) and [teaching-revision audit](../learning-design/2026-11-11__strengthen-learning-teaching-method.md) — separate teaching responsibility and its actual implementation state.
- [Git workflow task](../git-workflow/2026-11-08__design-implement-and-validate-git-workflow.md) — only if resolving the prior scoped exclusion or delivery ownership.

Use the absolute Tripverge paths above for product-specific decisions; do not treat this summary as canonical product authority. No Tripverge files were changed by this handoff.

Prior assessment consulted these public sources; refresh consequential/tool-specific claims if reused:
- [OpenAI harness engineering](https://openai.com/index/harness-engineering) — vendor experience with executable environments, browser/log visibility, and enforced invariants; not a transferable productivity guarantee.
- [Anthropic long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) — incremental progress and end-to-end checks; historical model-specific guidance.
- [Anthropic harness design](https://www.anthropic.com/research/harness-design-long-running-apps) — evaluator and harness tradeoffs; does not justify an expensive multi-agent default.

The human uses OpenCode and reported roughly S$30/month for a ChatGPT subscription, calling it Pro. The earlier assessment suggested it may be Plus; exact tier, connection, allowances, and billing route were not verified. Treat this as a soft budget constraint, not proof of access to any tool or model.

## Handoff verification

Read back this task and checked relative links and authority consistency on 2026-11-11. The task preserves an actionable discussion/investigation step, unresolved design, and the approval boundary before implementation. This was an author review, not an independent fresh-session trial. No verification-skill implementation, model trial, browser run, or new research is claimed by creating this task. No additional KB/docs/agent-lessons persistence is needed for this bounded proposal: unresolved design remains here; the teaching behavior belongs in its canonical skill.

**Resume cue:** "Resume the agent-led verification design task in Agent Core. Evaluate the proposal with me before implementing it."
