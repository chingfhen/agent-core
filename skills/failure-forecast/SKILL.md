---
name: failure-forecast
description: >
  Surface and test plausible ways an intended outcome could fail before the
  failure becomes expensive. Use to stress-test a plan, system, decision,
  experiment, launch, migration, operational change, or nearly finished
  product; identify evidence-backed failure paths, early warning signals, and
  proportionate actions before the next meaningful commitment.
license: MIT
metadata:
  version: 1.1.0
  category: reasoning
  domain: decision-support
  concepts: prospective-hindsight, failure-modes, causal-chains, early-warning-signals, risk-triage
---

# Failure Forecast

## Purpose

Surface and test the **few plausible failure paths that should change what happens next**.

This is broader than a project pre-mortem. It can stress-test an idea, decision, architecture, experiment, workflow, launch, migration, operational change, or product that is already mostly built.

Treat the result as structured hypothesis generation, not prophecy. Imagining failure improves exploration; it does not prove that an imagined risk is real.

## Core Mindset

Use prospective hindsight:

> Assume the intended outcome failed. Explain how that became true.

Then test and challenge the explanations.

```text
intended outcome
      ↓
assumptions and direct evidence
      ↓
plausible failure modes
      ↓
failure chains and propagation
      ↓
early signals or discriminating tests
      ↓
prevent / test / detect / contain / recover / transfer / accept
```

## When to Use

Use when the user wants to:

- find likely failure points or hidden weaknesses;
- decide whether something is ready to proceed or launch;
- stress-test an almost-complete build without reopening everything;
- challenge an architecture, migration, experiment, or implementation plan;
- separate must-fix issues from manageable risks;
- understand a vague concern about a decision;
- turn risks into tests, monitoring, fallbacks, or recovery plans.

Also use after a near miss, failed test, incident, material design change, or changed assumption to assess what could fail next.

## Do Not Use As

Do not use this skill as:

- a substitute for specialist security, safety, legal, medical, financial, or compliance review;
- a probability calculator without real data;
- a reason to delay until all uncertainty disappears;
- a generic brainstorm of every conceivable concern;
- a rigid workshop or mandatory response template;
- a claim that future failure can be predicted reliably from prose alone.

For a high-stakes specialist concern, name the boundary and recommend the appropriate scoped review. Do not present this forecast as clearance to proceed.

## Workflow

### 1. Gather direct evidence

Before forecasting, inspect the most direct available evidence for the target. Use only sources that fit the situation:

- plan, requirements, decision record, or success criteria;
- implementation, interfaces, data model, configuration, and deployment path;
- tests, test gaps, experiments, and observed failures;
- production metrics, logs, incidents, support requests, and user research;
- dependency behavior, service limits, operational runbooks, and recovery procedures.

State material evidence that was inspected and material information that was unavailable. Do not invent facts to complete a plausible story.

If the target is mostly hypothetical, say so and treat the result as a set of validation hypotheses.

### 2. Orient to the outcome

Determine from the available context:

- **Target** - what is being stress-tested?
- **Outcome** - what must be true for it to count as successful?
- **Stage** - idea, design, build, nearly complete, launch, or operating?
- **Commitment** - what decision or expensive step comes next?
- **Horizon** - when are we imagining the failure became clear?

Do not force clarification when useful assumptions are possible. State material assumptions briefly and proceed.

Ask at most one or two questions only when the answer would substantially change the analysis and cannot be responsibly inferred.

Choose a horizon that exposes the relevant failure class:

```text
first hour    -> deployment, access, corruption
first week    -> usability, reliability, support
three months  -> retention, economics, adoption
one year      -> maintainability, strategy, dependency
```

Define a concrete failed outcome, not generic doom.

Examples:

- "The application launched, but most users never completed a useful first job."
- "The migration completed, then caused unacceptable operational instability."
- "The model had strong offline metrics but failed in production."
- "The technical system worked, but the product was not economically sustainable."
- "Six months later, this decision was clearly regrettable."

Separate technical completion from outcome success:

```text
system works
   !=
user receives value
   !=
user returns
   !=
outcome is sustainable
```

### 3. Generate candidate failure modes

Generate broadly before ranking, defending the plan, or proposing mitigation. Then retain only candidates with a credible mechanism or a material unknown worth resolving.

Surface assumptions that the plan requires but has not established. Typical assumptions include:

- a dependency behaves as expected;
- interfaces, identifiers, or data models map correctly;
- users provide sufficiently good input;
- demo quality generalizes to real usage;
- capacity, latency, or cost remains acceptable at scale;
- someone owns operations, support, or recovery;
- an apparently reversible decision is actually reversible;
- provider, policy, market, or stakeholder behavior remains stable.

Distinguish hidden assumptions from known defects.

Use only the lenses that fit:

- user value, demand, adoption, and retention;
- correctness and output quality;
- architecture, data, interfaces, and dependencies;
- latency, capacity, queues, retries, and resource exhaustion;
- operations, ownership, observability, support, and recovery;
- cost, pricing, and unit economics;
- incentives, communication, and human behavior;
- security, privacy, safety, compliance, and reputation when material.

These are coverage prompts, not compulsory response sections.

### 4. Turn candidates into mechanisms

A useful failure mode explains how failure occurs:

```text
trigger or weak assumption
        ↓
specific failure mode
        ↓
local effect
        ↓
wider user, system, or business consequence
```

Weak:

> Scalability may be a problem.

Useful:

```text
provider latency doubles during peak demand
        ↓
worker throughput falls below arrival rate
        ↓
queue age grows continuously
        ↓
users abandon before receiving an output
```

Demote vague concerns that cannot be turned into a mechanism, unless the vague concern is itself a material unknown that needs validation or specialist review.

Trace propagation and concentration. Ask:

> If this breaks, what breaks next?

Look for:

- cascading failures and feedback loops;
- single points of failure;
- correlated dependencies disguised as redundancy;
- retries, fallbacks, health checks, or automation that amplify failure;
- failures hidden until late;
- one weak assumption supporting several decisions;
- mitigations that create another failure mode.

Use compact ASCII chains when they expose leverage better than prose.

### 5. Challenge the forecast

For each retained candidate, label the evidence honestly:

- **Known issue** - observed directly or credibly evidenced.
- **Plausible inference** - supported by facts and a mechanism, but not yet observed.
- **Speculative** - conceivable but weakly supported.
- **Unknown** - missing information materially controls the conclusion.

Ask:

- What must be true for this chain to occur?
- What evidence supports or weakens it?
- Has it appeared in production, tests, incidents, or comparable systems?
- Is it independent, correlated with another risk, or a consequence of another risk?
- Can uncertainty be resolved with a cheap, discriminating test?
- Would we detect it before severe damage?
- Can it be contained or recovered from?
- Would mitigation cost more than accepting it?

Do not invent likelihood percentages or imply that polished wording equals confidence.

### 6. Prioritize for the next decision

Judge using severity, evidence, time to impact, detectability, reversibility, recoverability, cascade potential, and cost and timing of action.

Assign one disposition:

- **Block now** - credible path to severe or irreversible failure; address before proceeding.
- **Validate soon** - important uncertainty that can be tested before the next major commitment.
- **Monitor** - plausible but not worth mitigating now; define a signal, threshold or condition, resulting decision, and an owner or explicit ownership gap.
- **Accept / defer** - understood and proportionate to tolerate at the current stage.

Do not make every important-sounding risk a blocker.

### 7. Choose the smallest useful response

A response may:

- **Prevent** the initiating condition.
- **Test** the assumption and replace speculation with evidence.
- **Detect** the failure earlier.
- **Contain** propagation.
- **Recover** through rollback, fallback, restore, retry, or manual handling.
- **Transfer / isolate** dependency risk.
- **Accept** the tradeoff and proceed.

For a `Validate soon` item, prefer the smallest discriminating test unless testing is infeasible or would create more risk than the uncertainty. A targeted failure test is often more valuable than an elaborate mitigation based only on imagination.

Prefer cheap, reversible responses before large redesigns.

### 8. Decide and revisit

When a next commitment is in scope, end with one decision. Otherwise state that no proceed/hold decision was assessed:

- **Proceed** - no retained blocker and remaining risk is proportionate.
- **Proceed with conditions** - name the required validation, guardrail, or acceptance.
- **Hold for validation** - name the exact evidence needed before the commitment.
- **Do not proceed** - name the blocker and the condition that would remove it.

Revisit retained `Block now`, `Validate soon`, and `Monitor` items after material test results, incidents, design changes, launches, or dependency changes. Retire forecasts invalidated by new evidence rather than accumulating a stale risk register.

## Stage-Aware Emphasis

### Idea or early design

Focus on fatal assumptions, demand, feasibility, irreversible commitments, and the cheapest validation path.

### Active build

Focus on interfaces, data assumptions, dependency behavior, integration gaps, ownership, tests, and recovery.

### Nearly complete or pre-launch

Do not reflexively reopen architecture decisions. Prioritize:

- whether users can reach value;
- reliability and graceful degradation;
- launch operations and support;
- monitoring and warning signals;
- cost and throughput;
- dependency failure and fallbacks;
- rollback and recovery;
- retention and repeated usage.

### Already operating

Ground the forecast in incidents, metrics, support issues, and near misses. Identify what may propagate or become the next bottleneck.

## Output Guidance

Adapt the structure to the problem. Do not force a fixed report template.

A strong response usually:

1. states the failed outcome, horizon, inspected evidence, and material unknowns;
2. gives the overall decision when a next commitment is in scope;
3. presents only the top three to seven failure modes;
4. identifies the evidence status and mechanism for each retained mode;
5. shows important causal chains;
6. identifies the earliest useful signal or discriminating test;
7. gives a disposition and smallest next action;
8. names accepted risks and, when a commitment is in scope, conditions for proceeding.

A compact table may work:

| Priority | Failure mode | Evidence | Why plausible / chain | Signal or test | Disposition and next action |
|---|---|---|---|---|---|

For a monitored risk, include:

```text
signal -> threshold or condition -> decision -> owner
```

Prefer prose or ASCII when they communicate the mechanism more clearly.

Use this reasoning record when helpful, but render evidence status and disposition for every retained risk:

```yaml
failure_mode: What specifically fails?
outcome_at_risk: What intended result does this defeat?
evidence_status: known_issue | plausible_inference | speculative | unknown
why_plausible: Evidence, mechanism, or exposed assumption
failure_chain: Trigger -> local effect -> wider consequence
early_signal_or_test: First observable indication or smallest discriminating test
response: prevent | test | detect | contain | recover | transfer | accept
priority: block_now | validate_soon | monitor | accept_defer
threshold_condition: Required for monitored risks
decision_owner_or_gap: Accountable person or team, or the ownership assignment required
next_step: Smallest concrete action
```

## Useful Prompts

Use these when the obvious risks are exhausted:

- What has to go right every time?
- Which dependency or person has no substitute?
- What works in the demo but is unproven under real conditions?
- Where can work arrive faster than it can be processed?
- What can silently damage quality without crashing?
- What would users notice before internal metrics look bad?
- What becomes expensive only after usage grows?
- Which assumption supports several independent-looking decisions?
- What would be discovered too late to reverse cheaply?
- What happens when the "noncritical" component never responds?
- Can the system fail safely, degrade gracefully, and recover?
- Could it work technically while failing to deliver value?
- Is the proposed mitigation more costly than the risk?

## Team Use

When several people are involved:

- generate failure reasons independently before group discussion;
- include people close to implementation and operations;
- separate generation from defending the plan;
- invite disconfirming evidence and unpopular concerns;
- do not automatically infer political concerns from keywords;
- assign ownership only to retained actions, not every brainstormed concern.

## Anti-Patterns

Avoid:

- giant risk inventories;
- fake numerical precision;
- vague risks without mechanisms or a material unknown;
- treating speculation as evidence;
- expensive mitigations for cheap, reversible failures;
- redesigning an almost-finished system instead of testing it;
- monitoring without a threshold, decision, and owner or explicit ownership gap;
- listing risks without a prevention, containment, recovery, test, or acceptance path;
- refusing to proceed merely because uncertainty remains.

## Stop Rule

Stop when the analysis has changed at least one decision, test, warning signal, containment, recovery plan, sequence, owner, or explicit risk acceptance.

For normal work, retain roughly three to seven decision-relevant failure modes. Include more only for a requested deep audit or a safety-critical domain.

## Quality Check

Before answering, verify:

- Is the failed outcome concrete?
- Did I inspect and disclose the most relevant available evidence?
- Are known issues, inference, speculation, and unknowns distinct?
- Are the risks mechanisms rather than topic labels?
- Did I consider propagation, dependency concentration, and recovery?
- Did I propose signals or discriminating tests for important uncertainties?
- Does every monitored item have a threshold, decision, and owner or explicit ownership gap?
- Is prioritization proportional rather than alarmist?
- Did I avoid invented numbers?
- Did I adapt to the current stage?
- When a next commitment is in scope, did I state a concrete proceed, hold, or do-not-proceed decision?
- Is the output small enough to act on?

## Core Principle

> Failure forecasting succeeds when it changes one important action before failure, not when it predicts every possible problem.
