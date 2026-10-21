---
name: reasoned-advocacy
description: >
  Evaluate, strengthen, and communicate a position through sound reasoning,
  evidence, alternatives, and counterarguments. Use when the user wants to
  justify or challenge a recommendation, build a defensible case, or prepare
  to answer stakeholder objections. Quick by default; Deep for thorough work.
disable-model-invocation: false
---

# Reasoned Advocacy

## Purpose

Help the human reach a justified position, understand why it holds, and explain
or defend it intelligently in discussion. The primary job is stronger judgment
and argumentation; persuasive delivery is secondary. The position may need to
be strengthened, qualified, reversed, or replaced.

This skill is independent of implementation planning, editing, and persistence
workflows. Do not confuse making a case for a decision with planning its execution.

## Modes and visibility

**Quick is the default.** Use **Deep** when explicitly requested or the human
clearly requests comprehensive investigation or argument preparation. Do not
silently escalate routine requests to Deep merely because the topic is complex.

Open human-facing answers with one compact marker showing the active mode and
alternative, without extra mode narration:

- **Reasoned Advocacy · Quick** (also: Deep)
- **Reasoned Advocacy · Deep** (also: Quick)

Keep the marker outside any separately requested managed artifact, document,
or strict-format output when it would interfere with that output.

### Quick (default)

Deliver the smallest useful defensible case, usually within a screen:

- Current assessment or recommendation, with the essential conditions.
- Strongest reasons **and why** they support the conclusion.
- The most consequential alternative, counterargument, or weakness.
- What fact or condition would change the conclusion, when meaningful.
- Natural, memorable speaking points only when useful for the situation.

Do not use a mandatory template or expand every conceivable objection.
Brevity must not erase the reasoning needed to understand the conclusion.

### Deep

Build sufficient understanding to explain and defend the position under
substantive scrutiny. Investigate relevant evidence, mechanisms, decision
criteria, alternatives, constraints, trade-offs, assumptions, and opposing
arguments. Prepare likely questions and reasoned answers when useful.

Spend depth where it could change the judgment or make the human more capable.
Do not equate depth with length, exhaustive lists, or a fixed academic worksheet.

## Working method

### 1. Identify the real proposition

Determine what is being advocated or questioned, the decision objective,
relevant context and constraints, and realistic alternatives. Distinguish:

- whether a claim is true or adequately supported;
- whether an option is attractive under a particular objective;
- whether it is better than its alternatives under the relevant conditions.

If no position is supplied, form a provisional one only when the basis warrants
it. If an important unknown prevents a responsible conclusion, identify it.
Ask one focused question only when it materially changes the work and cannot
be resolved from available context; otherwise proceed with labeled assumptions.

### 2. Understand the substance

Establish the causal mechanisms, concepts, and conditions needed to understand
the issue. For consequential arguments, connect:

**claim → supporting evidence or reasons → why they justify the claim →
assumptions and limits.**

Avoid feature lists that do not demonstrate a comparative advantage. Explain
technical terms accurately and plainly when they matter; one concrete example
is often better than an abstract slogan.

### 3. Evaluate the support

Check whether reasons are credible, relevant, and sufficient for the conclusion.
Distinguish observations and verified facts from reported claims, inference,
forecasts, and unknowns where that difference could change a decision.

Use available sources and research when material claims require checking,
especially in Deep mode. Prefer authoritative or primary evidence and cite
consequential sources where available. Do not invent measurements, citations,
organizational restrictions, stakeholder views, or numerical confidence.

### 4. Challenge fairly

Build the strongest **credible** opposing case before defending the initial one.
Compare realistic alternatives against relevant criteria, not a cherry-picked
list of strengths. Look for hidden assumptions, failure modes, opportunity
costs, and situations where another approach wins.

Concede valid objections. Avoid both straw-man counterarguments and false
balance when one position is better supported. Disagreement can arise from
different objectives or premises, not merely errors of logic.

### 5. Reach a calibrated judgment

Recommend, qualify, reject, or defer as the available support warrants. State
the determining trade-offs and important uncertainty, including evidence or
conditions that would reverse the recommendation.

If the user explicitly needs to present a selected position, help formulate its
strongest **truthful** case without hiding decisive objections or pretending it
is unconditionally optimal.

### 6. Prepare to explain and respond

Translate the underlying reasoning into a few speakable, memorable points.
Prioritize understanding over memorizing a polished speech.

When useful, anticipate likely stakeholder questions and give concise responses
that acknowledge the concern, explain the reasoning, and identify any relevant
unknown. Consider stakeholder priorities only when grounded or clearly framed
as possibilities; do not invent people's motives.

For requested rehearsal, challenge one substantial point at a time, respond to
the human's answer, and help strengthen their reasoning. Do not automatically
turn ordinary requests into a debate or interrogation.

## Output quality

Lead with the assessment and its decisive qualification. Organize content by
the questions a learner or stakeholder would ask, not the order research was
performed. Keep connected reasoning in connected prose; use bullets for parallel
points and tables only for useful comparisons. Keep headings and labels
consistent within repeated sections.

Maintain natural spoken phrasing without sacrificing technical precision,
evidence, or important caveats. Speaking points are optional, not a compulsory
second summary. Do not produce a lengthy word-for-word script unless requested.

## Boundaries and completion

- Do not implement a decision, create task plans, edit files, or persist content
  solely because this skill was invoked.
- Readability and knowledge-base skills may be used separately but are not
  dependencies. If a managed artifact is requested, its owning workflow handles
  saving, identity, links, and lifecycle.
- Never send employer-confidential or customer information to unauthorized tools.
- Do not optimize for winning arguments at the expense of truth or relationships.

A successful result enables the human to explain what is justified, why,
which alternatives and objections matter, and what would change the conclusion.
Quick establishes this practically; Deep substantiates it more thoroughly.
