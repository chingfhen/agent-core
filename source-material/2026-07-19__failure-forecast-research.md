# Failure Forecasting: Research Basis and Design Arguments

## Purpose

This memo explains the reasoning behind a general-purpose **failure-forecasting** skill: a skill that stress-tests a plan, system, decision, experiment, launch, migration, or nearly finished product by predicting plausible failure points before they become expensive.

The goal is not to reproduce a traditional project-management pre-mortem. The goal is to extract its strongest mechanism, combine it with useful ideas from reliability engineering and operations, and remove the ceremony, animal labels, fake precision, and oversized risk registers.

## Executive thesis

A pre-mortem is useful, but incomplete.

Its strongest contribution is a cognitive reframing:

> Assume the intended outcome failed. Explain how that became true.

That framing can generate more concrete explanations than ordinary forward-looking brainstorming. However, generating more possibilities is not the same as identifying the correct or most important ones. A robust skill therefore needs a second half: evidence checks, causal chains, prioritization, warning signals, and proportionate responses.

The resulting capability is better described as **failure forecasting**:

```text
intended outcome
      ↓
hidden assumptions
      ↓
plausible failure modes
      ↓
causal propagation
      ↓
early observable signals
      ↓
prevent / test / contain / recover / accept
```

It should be treated as structured hypothesis generation, not prophecy.

---

## 1. What the original pre-mortem gets right

### 1.1 Prospective hindsight changes the reasoning frame

Mitchell, Russo, and Pennington defined **prospective hindsight** as explaining a future event as though it had already occurred. Their experiments found that treating an outcome as certain changed the explanations people generated: explanations tended to become longer and more episodic. This supports the basic intuition that “it failed—why?” can unlock details that “what might go wrong?” does not.

Gary Klein later operationalized this framing as the project pre-mortem: brief the team on a plan, declare that it failed, and ask people to generate plausible reasons. Klein’s practical argument was also social: the exercise legitimizes dissent and gives worried participants permission to speak.

**Design implication:** retain the imagined-failure frame. It is the most distinctive and defensible part of the original method.

### 1.2 The technique is an idea generator, not a truth machine

A later study of retrospective planning found that participants generated significantly more ideas when reasoning backward from an imagined future, but the ideas were not higher quality on average.

That is an important limitation. The framing helps people “see more,” but does not guarantee that they “see better.” An AI agent is especially vulnerable to producing many polished, plausible-sounding risks that have little connection to reality.

**Design implication:** split the workflow into two deliberately different phases:

1. **Generate broadly** without prematurely defending the plan.
2. **Filter aggressively** using evidence, mechanisms, impact, detectability, and actionability.

The skill must never equate fluent risk generation with accurate forecasting.

---

## 2. What reliability engineering adds

### 2.1 Analyze failure modes and effects, not just worries

Failure Mode and Effects Analysis (FMEA/FMECA) introduces a useful discipline:

- What function or component is expected to work?
- In what specific way can it fail?
- What causes that failure?
- What effect does it have locally and at the system level?
- How is it detected or controlled?

NASA’s current FMECA guidance describes the analysis as a **living risk assessment** developed alongside the system and updated as designs, operating conditions, and knowledge change.

This matters because a vague concern such as “the provider may be unreliable” is not yet a useful failure forecast. A useful version is:

```text
provider throttles generation requests
        ↓
queue age grows faster than completion rate
        ↓
user sees a 25-minute wait with no credible ETA
        ↓
first-session abandonment rises
        ↓
users never reach the value moment
```

**Design implication:** every important risk should be expressed as a concrete failure mode with a causal mechanism and consequence, not as a topic label.

### 2.2 A failure forecast should remain useful after development begins

Traditional pre-mortem descriptions often imply a one-time meeting before committing to a build. Reliability practice is stronger here: the analysis evolves as evidence arrives.

A nearly finished product can still fail through:

- poor onboarding or weak value realization;
- cost, latency, quality, or reliability problems;
- operational ownership gaps;
- external provider dependency;
- missing recovery paths;
- customer acquisition or retention failure;
- a mismatch between “technically working” and “commercially useful.”

**Design implication:** make the skill stage-aware. Near launch, it should focus less on speculative architectural redesign and more on validation, reliability, observability, recovery, user behavior, economics, and launch operations.

---

## 3. What site reliability engineering adds

### 3.1 Failures propagate through chains

Google’s SRE guidance defines cascading failure as a failure that grows through positive feedback: one component fails, increasing pressure on the remaining system, which makes further failure more likely.

This is a major improvement over flat risk lists. Real failures often involve several individually survivable weaknesses combining:

```text
slow dependency
   ↓
request timeout
   ↓
automatic retry storm
   ↓
worker saturation
   ↓
queue growth
   ↓
more timeouts
```

The top-level failure may appear to be “the provider went down,” while the actual preventable problem is an unsafe retry and backpressure strategy.

**Design implication:** identify propagation, feedback loops, correlated dependencies, and single points of failure. Ask not only “what breaks?” but “what breaks next?”

### 3.2 Prediction must lead to tests

Google’s SRE guidance repeatedly emphasizes testing systems at and beyond their breaking points because exact behavior under overload is difficult to predict from first principles.

This yields a critical principle:

> A cheap, targeted failure test is stronger than an elaborate written mitigation based only on imagination.

Examples:

- inject dependency timeouts;
- load-test until queue latency becomes unacceptable;
- remove a supposedly noncritical backend;
- simulate malformed inputs;
- test provider rate limits;
- run the full user journey with a first-time user;
- measure whether generated output requires too much manual correction.

**Design implication:** when a forecast is testable, recommend the smallest experiment that can replace speculation with evidence.

### 3.3 A risk without a signal is operationally weak

Monitoring guidance distinguishes meaningful indicators from alerts that merely say something looks unusual. A forecast becomes more actionable when it specifies the earliest observable evidence that the failure chain is beginning.

Examples:

| Forecasted failure | Early signal |
|---|---|
| Users do not reach value | Low first-project completion rate |
| Provider instability destroys trust | Rising provider error and fallback rate |
| Unit economics fail | Median variable cost per usable output exceeds target |
| Queue overload causes abandonment | Queue age and cancellation rate rise together |
| Output quality is inconsistent | Regeneration and manual-edit rates increase |

**Design implication:** attach an early warning signal to every high-priority failure mode whenever one can reasonably be observed.

---

## 4. What risk research warns against

### 4.1 Do not manufacture precision

Risk matrices and traditional scoring systems often create an appearance of mathematical rigor without reliable underlying data. Cox’s analysis of risk matrices found poor resolution, range compression, and potential ranking errors. Similar concerns apply when an AI invents likelihood percentages or multiplies subjective scores into a “risk priority number.”

A score such as `likelihood 4 × impact 5 = 20` is not inherently more truthful than a well-supported qualitative judgment.

**Design implication:** default to transparent qualitative prioritization:

- **Block now** — credible path to severe or irreversible failure; action is required before proceeding.
- **Validate soon** — important uncertainty that can be tested cheaply or before the next major commitment.
- **Monitor** — plausible, but mitigation is currently disproportionate; define a signal and threshold.
- **Accept / defer** — understood risk whose cost is lower than the cost of addressing it now.

Use numerical estimates only when the user has real data or explicitly requests quantitative modeling.

### 4.2 Assumptions and uncertainty must stay visible

NIST risk guidance emphasizes that risk conclusions depend on assumptions, available information, and uncertainty. This is particularly important for agent-generated analysis.

The skill should distinguish:

- **Known issue** — observed directly or supported by credible evidence.
- **Plausible inference** — a mechanism follows from known facts, but has not been observed.
- **Speculative possibility** — conceivable, but weakly supported.
- **Unknown** — information is missing and materially affects the conclusion.

**Design implication:** the agent must not hide uncertainty behind confident prose. Evidence status is part of the output, not an internal detail.

---

## 5. My arguments for the redesigned skill

### Argument 1: The unit of analysis should be an intended outcome, not a “project”

The original pre-mortem is framed around project failure. That is unnecessarily narrow.

The same reasoning applies to:

- a product launch;
- an almost-finished application;
- an architecture or migration;
- a model-training run;
- an experiment;
- an operational process;
- a business or career decision;
- a travel plan;
- a personal commitment.

A failure forecast begins by defining what success was supposed to look like and what failure would mean at a relevant horizon.

### Argument 2: The horizon must match the question

“Fourteen days after launch” is not universally useful.

Different horizons expose different failure modes:

```text
first hour       → deployment, access, data corruption
first week       → onboarding, reliability, support load
three months     → retention, economics, acquisition
one year         → maintainability, strategy, dependency risk
```

The horizon should be chosen because it changes the analysis, not because a framework mandates it.

### Argument 3: Technical success and outcome success must be separated

A system can work exactly as designed and still fail.

For an AI product:

```text
pipeline completes successfully
        ≠
output is useful enough to pay for
        ≠
customer repeats usage
        ≠
business is economically sustainable
```

The skill should scan across layers rather than concentrating only on implementation defects.

Useful lenses include:

- intended value and user behavior;
- technical correctness and reliability;
- dependencies and interfaces;
- operations, ownership, and recovery;
- economics and resource constraints;
- security, privacy, safety, and compliance where relevant;
- incentives, communication, and human behavior.

These are prompts for coverage, not mandatory headings in every response.

### Argument 4: A failure list without causal structure creates noise

Flat lists make every item look independent and equally important. Failure chains reveal leverage points.

```text
weak onboarding
      ↓
poor initial input
      ↓
low-quality output
      ↓
user blames model quality
      ↓
regeneration cost rises
      ↓
retention and margin both fall
```

The cheapest intervention may be better examples or guided input—not a new model.

### Argument 5: The response should be proportional to the risk

The original skill’s launch-blocking / fast-follow / track distinction is useful. The redesigned version should preserve this idea without animal branding.

Possible responses are broader than “fix it”:

- **Prevent** the initiating condition.
- **Detect** the condition earlier.
- **Contain** propagation.
- **Recover** cheaply and quickly.
- **Transfer** or isolate dependency risk.
- **Accept** the risk consciously.
- **Test** the assumption before committing more resources.

A good forecast reduces uncertainty or limits damage. It does not automatically demand more engineering.

### Argument 6: The skill must resist becoming a pessimism generator

Failure-oriented thinking has predictable failure modes of its own:

- endless hypothetical objections;
- treating low-probability concerns as blockers;
- discouraging experimentation;
- posturing as “rigorous” through long registers and scores;
- redesigning already-built systems instead of validating them;
- generating mitigations more expensive than the failures;
- rewarding fear rather than evidence.

Therefore the skill needs explicit stop rules:

- prioritize only the few risks that change a decision;
- cap standard output at roughly three to seven major failure modes;
- label speculative risks;
- prefer reversible and cheap actions;
- state when the current plan is reasonably safe enough to proceed;
- do not block progress merely because uncertainty exists.

### Argument 7: The artifact should help someone act tomorrow

A useful output answers:

1. What is most likely to defeat the intended outcome?
2. Why is that plausible here?
3. How would the failure propagate?
4. What would we notice first?
5. What is the smallest sensible response now?
6. Which risks are consciously accepted?

Everything else is optional.

---

## 6. Proposed operating model

### Step 1 — Orient to the outcome

Identify:

- the thing being stress-tested;
- the intended outcome;
- the current stage;
- the decision or commitment at stake;
- a useful failure horizon.

Do not force clarification when sensible assumptions are possible. State assumptions briefly and proceed.

### Step 2 — Instantiate failure

Use one or more concrete counterfactuals:

- “The launch happened, but customers did not return.”
- “The migration completed, then caused unacceptable operational instability.”
- “The model achieved good offline metrics but failed in production.”
- “The decision looked reasonable, but six months later we regretted it.”

The failure statement must be specific enough to generate mechanisms, not generic doom.

### Step 3 — Generate across the system

Search for failure modes around:

- value and demand;
- correctness and quality;
- dependencies and interfaces;
- capacity, latency, queues, and cost;
- data and assumptions;
- operations, ownership, support, and recovery;
- incentives and human behavior;
- legal, security, privacy, or safety constraints when material.

Generate independently before narrowing. In a team, silent generation can reduce anchoring and hierarchy effects.

### Step 4 — Convert concerns into mechanisms

For each serious candidate, form:

```text
trigger or weak assumption
        ↓
specific failure mode
        ↓
local effect
        ↓
system / user / business consequence
```

Discard entries that remain vague after this step unless the vagueness itself is the key unknown.

### Step 5 — Challenge the forecast

Ask:

- What evidence supports this?
- Has it happened already, elsewhere, or under test?
- What must be true for this chain to occur?
- Is the failure independent, correlated, or a consequence of another risk?
- Is it detectable before severe damage?
- Is recovery possible?
- Would the proposed mitigation cost more than accepting the risk?

### Step 6 — Prioritize without false precision

Use judgment based on:

- severity;
- plausibility and evidence;
- time to impact;
- detectability;
- reversibility and recoverability;
- ability to trigger cascades;
- cost and timing of action.

Assign one decision-oriented category:

- Block now
- Validate soon
- Monitor
- Accept / defer

### Step 7 — Convert the top risks into action

For each retained risk, choose the smallest useful response:

- a test;
- an instrumentation or warning signal;
- a containment or fallback;
- a recovery plan;
- a design change;
- an ownership decision;
- explicit acceptance.

### Step 8 — Stop

The exercise is complete when it has changed priorities, tests, monitoring, or an explicit risk decision. A longer list is not automatically better.

---

## 7. Recommended risk record

The skill should adapt its presentation, but this is the underlying information model:

```yaml
failure_mode: What specifically fails?
outcome_at_risk: What intended result does this defeat?
evidence_status: known_issue | plausible_inference | speculative | unknown
why_plausible: Evidence, mechanism, or exposed assumption
failure_chain: Trigger → local effect → wider consequence
early_signal: First observable indication
response: prevent | test | detect | contain | recover | accept
priority: block_now | validate_soon | monitor | accept_defer
owner_or_next_step: Concrete action where relevant
```

Not every field needs to be rendered every time. The model exists to improve reasoning, not to enforce a response template.

---

## 8. What the skill should not become

It should not become:

- a generic “list risks” prompt;
- an excuse to delay shipping;
- a numerical scoring engine without data;
- an automated classifier pretending to know which concerns are politically sensitive;
- a replacement for security review, safety engineering, legal advice, domain expertise, or real testing;
- a requirement to hold a 60–90 minute workshop;
- a giant risk registry that no one updates.

Its proper role is narrower and more useful:

> Generate plausible failure hypotheses, expose their mechanisms and assumptions, then decide which few deserve prevention, validation, monitoring, containment, recovery planning, or conscious acceptance.

---

## 9. Final design position

The original pre-mortem is not useless hype. Its central framing is psychologically and practically valuable. The hype begins when a compact reasoning technique is presented as a complete risk-management system, dressed in memorable labels, automation, and process ceremony.

The redesigned skill should preserve the insight while being honest about its limits:

- imagined failure improves exploration;
- exploration does not guarantee accuracy;
- causal structure is more useful than labels;
- evidence matters more than confidence of wording;
- early signals and tests turn prediction into operational value;
- proportional responses prevent risk analysis from becoming paralysis;
- the best output is a small number of decisions, not a large number of risks.

---

## References

1. Mitchell, D. J., Russo, J. E., & Pennington, N. (1989). *Back to the Future: Temporal Perspective in the Explanation of Events*. Journal of Behavioral Decision Making, 2(1), 25–38. DOI: 10.1002/bdm.3960020103.
2. Klein, G. (2007). *Performing a Project Premortem*. Harvard Business Review.
3. Rollier, B., & Turner, J. A. (1994). *Planning Forward by Looking Backward: Retrospective Thinking in Strategic Decision Making*. Decision Sciences, 25(2), 169–188. DOI: 10.1111/j.1540-5915.1994.tb00799.x.
4. NASA Goddard Space Flight Center (2024). *Guideline for Failure Modes and Effects Analysis and Risk Assessment*, GSFC-HDBK-8004.
5. Google Site Reliability Engineering. *Monitoring Distributed Systems*.
6. Google Site Reliability Engineering. *Addressing Cascading Failures*.
7. NIST SP 800-30 Rev. 1. *Guide for Conducting Risk Assessments*.
8. Cox, L. A. Jr. (2008). *What’s Wrong with Risk Matrices?* Risk Analysis, 28(2), 497–512. DOI: 10.1111/j.1539-6924.2008.01030.x.

Research reviewed on 2026-07-19.
