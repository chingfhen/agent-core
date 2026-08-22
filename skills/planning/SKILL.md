---
name: planning
description: >
  Plans substantial work into a clear, approval-ready direction before execution.
  Use when the user wants to understand, shape, evaluate, or approve a non-trivial
  change before building, especially when consequential decisions, assumptions,
  risks, architecture, or sequencing need to be resolved. Starts from maintained
  project context, investigates only what materially affects the plan, asks one
  high-value human question at a time when needed, challenges premature commitment,
  and produces a scannable plan that can be approved and persisted for a fresh
  execution session.
disable-model-invocation: false
---

# Planning

## Purpose

Turn a request into a sufficiently resolved, human-ownable plan before substantial
execution begins.

The goal is not to produce the most detailed plan possible. The goal is to reach
enough clarity that the human can:

- understand what will be achieved and why;
- understand the proposed solution shape;
- inspect or challenge the consequential decisions;
- see important assumptions, risks, and trade-offs;
- understand how success will be verified;
- confidently say **"approved, go."**

Planning should reduce uncertainty, not manufacture ceremony.

A typical workflow is:

```text
maintained project context
        ↓
focused investigation
        ↓
human questions only when consequential
        ↓
approval-ready plan
        ↓
human approval
        ↓
persist to task file
        ↓
fresh execution session
        ↓
engineering executes
```

## Core Principles

### Start From Maintained Project Context

Begin with the project's maintained documentation and current task context when
available.

Use them to establish:

- architecture and ownership;
- conventions and important boundaries;
- prior decisions;
- current constraints and non-goals;
- intended behavior;
- relevant operational context.

Project documentation is the fastest map of the system, not unquestionable truth.

Use code, tests, configuration, logs, schemas, outputs, and other artifacts when
the plan depends on implementation reality, when documentation may be incomplete
or stale, or when a consequential assumption needs verification.

Do not re-discover the whole repository when maintained context already answers the
planning question.

### Evidence Before Questions

Inspect the smallest relevant set of evidence before asking the human for
information that may already be available.

Use, as relevant:

- canonical project docs;
- current task files;
- relevant code and tests;
- configuration and manifests;
- logs, generated artifacts, schemas, or outputs;
- available external evidence when the request requires it.

Use docs for intended behavior and rationale. Use implementation evidence to verify
current truth when that distinction matters.

Do not ask the human to reconstruct information the agent can discover directly.

### Investigate Directly by Default

Routine planning discovery belongs to the main agent.

Read the relevant docs, task context, code, tests, configuration, and artifacts
directly rather than casually delegating discovery to subagents.

Do not dispatch a discovery subagent merely to:

- summarize a few files;
- parallelize ordinary repository reading;
- obtain a second description of information the main agent can inspect directly;
- create the appearance of thoroughness.

Use a discovery subagent only when the investigation is genuinely large,
separable, and likely to improve the planning result materially, such as a clearly
bounded investigation of a large unfamiliar subsystem or an independent research
question.

Subagent use is an exception, not the default planning reflex.

### Investigation Must Serve a Decision

Every investigation should answer a planning question.

Do not explore the repository merely to become broadly familiar with it.

Read additional evidence only when it could:

- change the proposed direction;
- resolve a material uncertainty;
- verify an important assumption;
- expose a consequential architectural constraint;
- reduce a meaningful risk;
- improve the human's ability to approve the plan.

Stop when more discovery is unlikely to change the decision.

Planning is not pre-execution. Do not inspect implementation detail merely to
remove uncertainty that a strong executor can safely resolve later.

### Avoid Premature Commitment

The first plausible approach is not automatically the right one.

Before committing to a material direction:

1. identify the important assumptions behind the leading approach;
2. consider credible alternatives only where they could materially improve the result;
3. challenge weak assumptions, hidden coupling, unnecessary complexity, or unsupported confidence;
4. surface non-obvious trade-offs or risks when they matter;
5. then converge on the most practical direction.

Do not create alternatives merely to demonstrate breadth. Exploration is useful
only when it can change the decision.

Prefer truth and evidence over agreement. Disagree clearly when the proposed
direction is weak, risky, unnecessarily complex, or contradicted by available
evidence.

### Ask One Question at a Time

When a material human-owned decision remains unresolved, ask exactly one question
at a time.

Each question should:

- target the highest-value unresolved decision;
- depend on the current evidence and previous answers;
- explain the recommended answer briefly when a useful recommendation can be made;
- materially affect scope, architecture, behavior, risk, verification, or approval.

After each answer, reassess the entire planning state before deciding whether
another question is still necessary.

Do not batch speculative questionnaires.

Do not continue asking questions after the plan is sufficiently determined.

### Distinguish Ownership

Classify uncertainty before acting on it.

```text
Can repository or available evidence answer it?
        |-- Yes -> investigate.
        `-- No
             |
             v
Does it materially affect human control, product behavior,
architecture, security, privacy, cost, migration, risk,
failure behavior, or acceptance?
        |-- Yes -> human-owned; ask when unresolved.
        `-- No
             |
             v
Can a strong executor safely decide it during implementation?
        |-- Yes -> executor-owned; do not over-plan it.
        `-- No  -> surface the uncertainty or blocker.
```

Routine code placement, ordinary sequencing, test mechanics, naming, local
refactoring, and other reconstructible implementation choices usually belong to
the executor unless they carry meaningful consequences.

### Existing Architecture Is Evidence, Not Authority

Understand the current architecture and repository patterns before proposing
change, but do not preserve them automatically.

Treat them as evidence:

- some patterns encode deliberate constraints and should be respected;
- some are historical accidents;
- some are inconsistent or weak;
- some may no longer fit the requested change.

If the current request exposes a consequential weak boundary, harmful coupling,
poor ownership, or an established pattern that no longer fits, consider whether
improving the architecture belongs in the proposed direction.

Do not leave a material architectural problem for the executor to silently redesign
during implementation.

Equally, do not redesign unrelated areas merely because a cleaner architecture can
be imagined.

### Prefer the Simplest Adequate Direction

Planning should naturally avoid speculative scope, unnecessary abstractions,
premature infrastructure, and complexity without demonstrated value.

This is ordinary planning discipline, not the stronger `/yagni` mode.

When the user explicitly invokes `yagni`, allow that skill to apply its stronger
simplicity rules.

### Prefer Reversible Decisions Under Uncertainty

When meaningful uncertainty remains and multiple approaches are otherwise
credible, consider reversibility and migration cost.

Prefer decisions that preserve options and are inexpensive to change unless the
less-reversible choice has a demonstrated advantage.

When useful, state what evidence or future condition would justify revisiting the
decision.

Do not use reversibility as an excuse to avoid making a necessary decision.

### Scale Planning by Consequence, Not Size

Planning depth should follow consequence and uncertainty, not estimated line count.

A small schema, migration, security, contract, or externally visible change may
deserve more planning than a large but isolated implementation.

Use only enough planning depth to resolve the decisions that matter.

## Planning Process

### 1. Establish the Destination

Understand:

- the desired outcome;
- why it matters;
- important constraints and non-goals;
- what "done" means;
- any prior decisions already made.

Do not restate everything the user said. Extract what actually controls the plan.

### 2. Read Maintained Context

Start from the project's maintained documentation, current task context, and other
canonical sources when available.

Use them to establish the system map before dropping into implementation detail.

Do not perform broad repository exploration when the maintained context already
provides enough orientation to ask the next meaningful planning question.

### 3. Investigate Current Reality

Read only enough additional evidence to understand the relevant system and avoid
planning against stale or imagined architecture.

Separate:

- **observed facts** — directly supported by code, docs, tests, outputs, or other evidence;
- **inferences** — conclusions drawn from evidence;
- **assumptions** — provisional beliefs not yet verified.

Do not imply stronger certainty than the evidence supports.

Stop expanding investigation once additional evidence is unlikely to change the
plan, remove a material assumption, or improve approval confidence.

### 4. Resolve Material Uncertainty

For every important unresolved point, decide whether to:

- investigate further;
- ask the human one question;
- treat it as executor-owned implementation detail;
- record it as a genuine assumption;
- expose it as a blocker.

Continue only while another unresolved point could materially change the plan or
the human's ability to approve it.

### 5. Select the Direction

Converge on one recommended approach.

Explain the solution shape in plain language before implementation detail.

Surface:

- the consequential decisions;
- the most important trade-offs;
- meaningful alternatives rejected and why, when that helps approval;
- boundaries or explicit exclusions that prevent scope drift;
- important risks or failure modes;
- reversibility or migration implications when they materially affect the choice.

Do not leave material alternatives hidden inside phrases such as `either`,
`optionally`, `depending on preference`, or `choose during implementation`.

Either resolve them, classify them as executor-owned, or surface them as unresolved.

### 6. Build the Plan

Plans should describe meaningful outcomes and phases, not narrate routine mechanics.

Prefer phases such as:

```markdown
### Phase 1: Establish the contract
Define the behavior and ownership boundary the rest of the implementation relies on.

### Phase 2: Integrate it into the execution path
Apply the contract to the relevant runtime path while preserving existing behavior outside the intended scope.

### Phase 3: Prove success and failure behavior
Verify the intended path, important edge cases, and any migration or rollback expectations.
```

Avoid plans like:

```text
1. Edit foo.py
2. Update bar.py
3. Add tests
```

unless those exact files or commands are materially useful to human understanding
or approval.

Do not pre-specify routine executor-owned mechanics just to make the plan look
complete.

### 7. Make the Plan Human-Ownable

Surface the minimum sufficient information the human needs to understand, verify,
and approve the work.

Depending on the task, useful information may include:

- intended outcome and success criteria;
- proposed architecture or work shape;
- consequential decisions and assumptions;
- important boundaries or exclusions;
- a few relevant files, modules, commands, manifests, jobs, schemas, or artifacts;
- exact output locations;
- expected counts or observable results;
- cost, quota, or destructive-operation implications;
- failure, rollback, retry, recovery, or migration behavior;
- verification steps;
- unresolved risks or required human actions.

Do not force all of these into every plan.

Use the structure that best exposes the decisions and evidence relevant to the
current work.

### 8. Define Verification

State how success will be demonstrated.

Prefer concrete verification such as:

- specific tests or checks;
- expected runtime behavior;
- output artifacts and locations;
- expected counts or status;
- logs or metadata;
- before/after observations;
- controlled manual review;
- rollback or recovery validation where relevant.

When practical, provide the shortest useful independent verification path.

Do not claim verification that has not happened yet. During planning, describe
intended proof, not completed proof.

### 9. Surface Remaining Attention

Before asking for approval, make unresolved material concerns obvious.

Examples:

- human approval still required;
- missing credential or provider access;
- unknown external behavior;
- production-only validation gap;
- cost or quota uncertainty;
- migration or rollback decision;
- assumption that could materially invalidate the approach.

Do not bury these inside implementation detail.

### 10. Present for Approval

When the user asked to vet the plan, stop before substantial execution.

Present a scannable plan containing only the sections useful for this work.

Typical sections may include:

- Outcome
- Proposed Approach
- Key Decisions
- Work Shape
- Verification
- Human Attention / Remaining Uncertainty

These are not a mandatory template.

For simple work, use fewer sections. For consequential work, expose more detail.

The approval test is:

> Can the human understand the proposed work, challenge the important decisions, and confidently say "approved, go"?

If not, the plan is not ready for approval.

### 11. Persist for a Fresh Executor When Requested

When the user asks to create or update a project task after planning:

1. finish the planning conversation first;
2. incorporate the human's feedback;
3. wait for approval when approval was requested;
4. load `project-tasks`;
5. persist the approved direction, current truth, implementation plan, verification, blockers, and next action.

Persist enough decision context that a fresh executor can implement the task
without reconstructing the planning conversation.

The task should preserve:

- what is being achieved and why;
- the approved solution shape;
- consequential decisions and constraints;
- explicit non-goals or boundaries;
- important assumptions and risks;
- intended verification;
- blockers or human actions that remain.

Do not over-specify routine implementation details that `engineering` can safely
resolve during execution.

Do not write an exploratory or superseded plan into the task as if it were approved.

## Output Style

Optimize for:

- clarity;
- scannability;
- decision relevance;
- plain language before code symbols;
- enough detail for ownership and approval;
- proportional structure.

Avoid:

- chronological narration of investigation;
- exhaustive file inventories;
- duplicated conclusions;
- large speculative option lists;
- low-level implementation detail that a strong executor can reconstruct;
- boilerplate sections that add no decision value;
- vague claims such as `should work`, `looks good`, or `handle edge cases`.

A plan is a decision tool, not a transcript.

## Stop Conditions

Stop planning and ask for approval when:

- the destination is clear;
- one recommended direction is selected;
- material human-owned decisions are resolved;
- remaining implementation choices are safely executor-owned;
- meaningful blockers and assumptions are visible;
- the work shape is coherent;
- success can be verified.

Do not keep planning merely because:

- more repository detail could be read;
- another subagent could be dispatched;
- another alternative could be invented;
- more implementation mechanics could be specified.

Planning is complete when further detail is unlikely to improve the decision.

## Non-Negotiables

- Start from maintained project context when available.
- Investigate before asking when evidence can answer.
- Investigate directly by default; do not casually delegate routine discovery.
- Every investigation must serve a material planning question.
- Ask one human question at a time.
- Let each answer determine the next move.
- Do not batch speculative questions.
- Do not commit to the first plausible frame without testing important assumptions.
- Do not fabricate alternatives for appearance.
- Treat existing architecture as evidence, not automatic authority.
- Do not hide material decisions inside executor discretion.
- Do not pre-execute the task during planning.
- Do not over-plan routine mechanics.
- Do not confuse future verification with completed verification.
- Do not execute substantial work before approval when the user explicitly requested plan review first.
- Persist enough approved decision state for a fresh executor when requested.
- Prefer the most practical sufficiently supported direction over maximum theoretical completeness.
