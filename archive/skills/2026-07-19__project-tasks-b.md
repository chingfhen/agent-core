---
name: project-tasks
description: Maintains shared human-agent execution briefs in tasks/ (including tasks/backlog/ for deferred work) so the human owner can understand and steer the work while a future fresh-session executor can resume without the prior conversation. Load before creating, editing, or managing anything under tasks/; not needed merely to read task files. Rewrites tasks into high-signal control surfaces that preserve execution-critical context and human-control nuances while compressing routine implementation detail and stale history.
disable-model-invocation: false
---

# Project Tasks

## Purpose

Maintain task-specific execution briefs, typically in `tasks/`, for work that needs continuity across sessions.

A task file is a **shared control surface** between the human owner and the executing agent.

It serves two purposes:

1. **Execution continuity**
   A fresh-session executor can understand the work, make progress, and verify completion without relying on the previous conversation.

2. **Human control**
   The human owner can understand what is happening, challenge the direction, inspect important nuances, identify risks, and decide whether execution should proceed.

A task file is not:

* durable project documentation;
* a raw transcript;
* a session diary;
* an exhaustive implementation manual;
* a dumping ground for every technical detail.

A task file is a **continuously rewritten execution brief**.

For execution-bound work, it must stand on its own. A fresh executor should not need the prior conversation, and the human owner should not need to inspect the code merely to understand the plan.

---

## Shared Ownership Boundary

The human and agent own different levels of the work.

```text
Human owns                         Agent owns
──────────                         ──────────
Intent                             Code navigation
Priorities                         Routine implementation mechanics
Product expectations               Low-level sequencing
Important constraints              Commands and file edits
Architecture boundaries            Detailed test construction
Acceptable trade-offs              Debugging tactics
Risk tolerance                     Ordinary code-placement choices
Approvals and access               Reconstructible technical detail

                 Task file
       ─────────────────────────
       Shared understanding of:
       what, why, chosen direction,
       current state, important nuance,
       blockers, next move, and proof
       of success
```

The human does not need every implementation detail.

The human **should see every detail that could materially change**:

* the system’s direction;
* component or responsibility boundaries;
* user-visible or failure behaviour;
* safety, security, privacy, or data integrity;
* cost or paid-provider exposure;
* maintainability and long-term quality;
* fallback, retry, replay, or recovery semantics;
* confidence that the selected plan is sound.

The agent should own routine mechanics that do not affect those concerns.

---

## Guiding Questions

Whenever creating, rewriting, or preparing a task, ask both:

> What does the next executor need to execute effectively without the old chat?

> What does the human owner need to understand, supervise, challenge, or approve the work confidently?

Preserve the answers.

Everything else is negotiable.

The goal is not to preserve history. The goal is to preserve **execution effectiveness and human control**.

---

## Core Model

* **`project-tasks` owns active execution state**, orchestration context, planning decisions, blockers, and fresh-session handoff briefs.
* **`project-docs` owns durable project knowledge** and continuously absorbs stable truths.
* **`tasks/backlog/` owns deferred future-work briefs** that should survive without becoming active execution state.
* **`source-material/` holds supporting artifacts** that may inform work without becoming canonical truth.
* **`archive/` holds historical material** that should not drive current execution by default.
* **Code and tests own exact implementation truth.**
* **Conversation owns exploration in progress.**
* Task files preserve current alignment, not archaeological history.
* Preserve uncertainty honestly. Never write uncertain claims as established fact.
* Assume future executors are technically strong.
* Do not handhold obvious implementation steps.
* Keep the first screen highly scannable.
* Prefer one authoritative statement of each important fact. Do not repeat the same point across several sections.

---

## Dashboard Contract

New tasks use:

```text
tasks/YYYY-MM-DD__kebab-case-name-bookmark.md
```

The date is an **immutable creation date**.

Keep `tasks/` flat unless the repository already uses another convention. Do not mass-rename historical tasks.

### Explicit Fields

| Field              | Values                           | Meaning                                                                                     |
| ------------------ | -------------------------------- | ------------------------------------------------------------------------------------------- |
| **Priority**       | `Now`                            | Active priority.                                                                            |
| **Priority**       | `Next`                           | Intended next-up work.                                                                      |
| **Priority**       | `Later`                          | Preserved but not near-term.                                                                |
| **Status**         | `Active`                         | Execution is live or ready to begin.                                                        |
| **Status**         | `Blocked`                        | Execution cannot proceed until a blocker clears.                                            |
| **Status**         | `On Hold`                        | Intentionally paused.                                                                       |
| **Status**         | `Closed`                         | Execution has ended.                                                                        |
| **Execution Gate** | `Needs Human Unblock`            | A human must act, approve, decide, or provide access before meaningful execution can begin. |
| **Execution Gate** | `Ready for Main-Agent Execution` | No known hard blockers; execute mainly phase-by-phase via the main agent.                   |
| **Execution Gate** | `Ready for Delegated Execution`  | No known hard blockers; bounded parts are safe to hand to subagents.                        |
| **Execution Gate** | `Not Applicable (Closed)`        | The task is closed and no execution gate remains.                                           |
| **Docs Sync**      | `Not Synced`                     | Durable knowledge has not been checked or promoted.                                         |
| **Docs Sync**      | `Partial`                        | Some durable knowledge was promoted or checked; more may remain.                            |
| **Docs Sync**      | `Synced`                         | Durable knowledge has been handled.                                                         |

`Status` reflects lifecycle state.

`Execution Gate` reflects whether execution may begin and what execution shape is allowed.

`Docs Sync` reflects durable-knowledge synchronization only.

When `Execution Gate: Needs Human Unblock`:

* set `Status: Blocked`;
* make `Next Action` the exact human action required;
* explain why execution should stop.

When `Status: Closed`:

* set `Execution Gate: Not Applicable (Closed)`;
* do not leave pending execution disguised as a closed task.

### First-Screen Shape

Use this as the normal first-screen structure for execution-bound tasks:

```markdown
# Task: [Clear short name]

**File:** `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** [Now | Next | Later]
**Status:** [Active | Blocked | On Hold | Closed]
**Execution Gate:** [Needs Human Unblock | Ready for Main-Agent Execution | Ready for Delegated Execution | Not Applicable (Closed)]
**Docs Sync:** [Not Synced | Partial | Synced]

**Goal:** [...]
**Why:** [...]
**Success Bar:** [...]
**Chosen Approach:** [...]
**Current State:** [...]
**Next Action:** [...]
**Blockers:** [...]
**Human Attention:** [...]

**Target Docs:** [...]
**Relevant Code:** [...]
```

For a genuinely small or obvious task, `Why`, `Chosen Approach`, or `Human Attention` may be omitted when they add no value.

For consequential or execution-bound work, omitting them should be deliberate rather than automatic.

---

## First-Screen Readability Contract

The first screen is the human skim layer.

After reading it, the human owner should be able to explain:

1. What outcome is being pursued?
2. Why does it matter?
3. What solution shape was selected?
4. What is currently true?
5. What happens next?
6. How will success be recognized?
7. What important nuance deserves supervision?
8. Is anything capable of stopping execution?

### Writing Rules

* Use plain language before code symbols or implementation shorthand.
* Explain system behaviour and consequences, not merely file edits.
* Keep each field focused on one purpose.
* Prefer short paragraphs or compact bullets over dense multi-clause sentences.
* If a field contains several independently verifiable conditions, use bullets.
* Translate important technical implications into human-understandable consequences.
* Name code locations only after explaining why they matter.
* Avoid unexplained agent shorthand such as `wire up`, `plumb through`, `harden semantics`, `validate affinity`, or `inspect callsites`.
* Technical terms are allowed when they are the clearest wording, but explain the important meaning.
* Do not compress several unresolved decisions into one sentence.
* Do not make the human reconstruct the selected plan from the implementation section.

### Examples

Weak:

> Add manifest validation.

Better:

> Validate that the model, preprocessing configuration, adapter, and threshold belong to one compatible artifact bundle so production cannot silently combine mismatched components.

Weak:

> Wire the credit query into create.

Better:

> Read the live account balance before image preparation so an insufficient-credit user is blocked immediately rather than after an expensive browser upload.

---

## Human Attention

`Human Attention` surfaces the smallest set of non-obvious details that materially affect human confidence, direction, risk assessment, or long-term system quality.

Usually include **one to five bullets**.

A nuance belongs here when it:

* changes what a component should or should not own;
* could cause silent, repeated, or cumulative degradation;
* creates a non-obvious security, privacy, financial, data-integrity, or operational risk;
* determines important fallback, retry, replay, recovery, or idempotency behaviour;
* exposes hidden coupling or a brittle assumption;
* explains why an apparently simple implementation is dangerous;
* captures a lesson future agents are likely to miss repeatedly;
* would materially affect human approval or architectural direction.

Do not merely name the nuance. Explain why it matters.

Example:

```markdown
**Human Attention:**

- CTA semantic quality belongs mainly to strategy and repair logic. The validator
  should reject malformed structures and genuine impossibilities, not grow an
  exhaustive vocabulary of acceptable phrases.

- Expanding CTA allowlists appears safe locally but rejects valid creative variants
  and has already contributed to repeated job failures.
```

Do not fill `Human Attention` with routine implementation detail.

---

## Detail Selection Test

Before adding a detail, classify it.

### Include Prominently

Include it in the first screen or `Human Attention` when it affects:

* human steering;
* approval;
* confidence;
* risk;
* responsibility boundaries;
* long-term system direction.

### Include in Executor Detail

Include it below the first screen when it is:

* execution-critical;
* not reliably reconstructible from code or docs;
* necessary to prevent repeated mistakes;
* necessary to understand a non-obvious implementation constraint.

### Compress or Omit

Usually omit it when it is:

* routine code navigation;
* obvious implementation sequencing;
* ordinary test setup;
* a command the next executor can derive;
* easily reconstructible from current code;
* duplicated elsewhere;
* stale investigation history;
* merely interesting but not decision-relevant.

Use this decision rule:

```text
Does it affect human control?
        ├── Yes → surface clearly
        └── No
             ↓
Is it execution-critical and hard to reconstruct?
        ├── Yes → preserve in executor detail
        └── No  → compress or omit
```

---

## Adaptive Structure

The dashboard is the only default shape.

Additional sections are tools, not mandatory output.

Use only sections that materially improve future execution or human control.

* Do not populate sections simply because they exist.
* Omit sections that are obvious, empty, redundant, or low-value.
* Prefer a shorter bookmark with stronger signal over a fully populated template.
* Different tasks require different structures.
* Do not repeat a nuance in `Human Attention`, `Likely Blind Spots`, and the plan unless each placement serves a distinct purpose.

Optional sections:

* Human Intent
* Expected Outcomes
* Decisions Locked
* Chosen Approach Detail
* Important Trade-offs
* Non-Goals / Stop Conditions
* Problem Origin
* Current Understanding
* Remaining Uncertainty
* Superseded Understanding
* Implementation Plan
* Executor Guidance
* Likely Blind Spots
* Verification Contract
* Context Pointers
* Rejected Direction
* Do Not Let This Evolve Into
* Visual Handle
* Execution Topology

Typical emphasis:

* **Feature work:** Human Intent, Expected Outcomes, Decisions Locked, Implementation Plan.
* **Debugging:** Problem Origin, Current State, Superseded Understanding, Verification Contract.
* **Investigation:** Current Understanding, Remaining Uncertainty, Next Evidence.
* **Architecture change:** Chosen Approach Detail, Important Trade-offs, Human Attention, Visual Handle.
* **Small task:** Dashboard, Next Action, Verification Contract.
* **Risky operational work:** Human Attention, Stop Conditions, Verification Contract, rollback or recovery guidance.

Choose structure intentionally.

---

## Do Not Let This Evolve Into

Use this optional section when a locally convenient implementation is likely to expand into a brittle, misowned, unsafe, or costly subsystem.

Describe:

1. the tempting shortcut;
2. why it is harmful;
3. the responsibility boundary or design rule that prevents it.

Example:

```markdown
## Do Not Let This Evolve Into

Do not turn CTA validation into an expanding phrase-approval vocabulary.
That makes the validator responsible for creative semantics, rejects valid
language variants, and creates ongoing maintenance and job-failure risk.
```

Use this section sparingly. It is for dangerous evolutionary directions, not generic non-goals.

---

## Visual Handle

A tiny visual or ASCII sketch is recommended when structure is the thing the human or executor must grasp.

Use it when:

* the mental model is a pipeline, graph, state machine, ownership boundary, or before/after change;
* prose would hide a relationship or responsibility boundary;
* a few lines materially improve confidence.

Skip it when:

* the task is linear or small;
* the change is pure configuration or copy;
* the structure is already obvious from code;
* the visual would go stale faster than it helps.

Keep it cheap.

Examples:

```text
request → route → auth → handler → DB → response
```

```text
queued → running → completed
          ↓
        failed → retry
```

```text
Current:
model → predictor → fixed threshold 0.5

Target:
model bundle → compatibility validation → predictor
      └──────── selected threshold ─────────┘
```

A visual is a compression tool, not decoration.

---

## Alignment Gate

Use grilling before creating or materially reshaping consequential work, especially when planning future execution.

Establish:

1. the real goal;
2. success criteria;
3. important constraints;
4. non-goals;
5. expected outcomes;
6. critical mistakes future executors must avoid;
7. important responsibility boundaries;
8. any trade-off that requires human ownership.

Draft `Expected Outcomes` for confirmation unless the user’s instructions already define them clearly or the update is routine.

Do not over-question straightforward updates.

---

## Blocker Preflight

Before writing a substantial execution plan, resuming work, or preparing a fresh-session handoff, inspect for blockers.

Do not ask only, “Are there blockers?”

Actively check the categories below.

### 1. Human Access Blockers

* credentials, secrets, API keys, tokens, or environment variables;
* repository, cloud, database, provider, dashboard, or production access;
* account permissions or role changes;
* OAuth consent;
* billing activation;
* DNS, webhook, certificate, or external configuration;
* access to private logs, datasets, tenants, or registries.

### 2. Human Decision Blockers

* unclear acceptance criteria;
* competing user-visible behaviours;
* architecture choices with material long-term consequences;
* fallback or failure behaviour;
* security, privacy, or data-retention decisions;
* cost-versus-quality decisions;
* destructive migration approval;
* backward-compatibility requirements;
* deployment timing or downtime approval;
* metric-selection or threshold decisions.

### 3. External-System Blockers

* unavailable provider capability;
* pending vendor approval or response;
* insufficient quota;
* test tenant or sandbox not provisioned;
* webhook or app registration not completed;
* missing external test data;
* required hardware or environment unavailable;
* undocumented third-party identifier mapping that needs live validation.

### 4. Technical Hard Blockers

* a required contract is unknown and cannot be inferred safely;
* a critical schema, interface, or identifier mapping is missing;
* the assumed component does not exist;
* a dependency cannot support the planned behaviour;
* there is no meaningful test or reproduction environment;
* production state is required to design a safe migration;
* incompatible architecture decisions remain unresolved.

### 5. Operational and Safety Blockers

* no rollback or recovery path for a risky change;
* no backup before destructive work;
* no staging or controlled validation path;
* unclear production ownership;
* required security review not completed;
* privacy-sensitive handling unresolved;
* paid-provider replay risk;
* no observability to determine whether the change worked.

### Blocker Versus Executor-Owned Uncertainty

Ask:

```text
Can a fresh executor resolve this independently through a bounded investigation?
        ├── Yes → put it in the execution plan
        └── No, or meaningful work cannot continue
               → hard blocker
```

A bounded investigation must state:

* the exact question;
* the evidence to inspect;
* the decision or implementation step that follows.

“Investigate further” is not a plan.

### Blocker Recording Contract

For every hard blocker, record:

* the blocker;
* why it prevents meaningful execution;
* the exact human or external action required;
* whether all execution should stop or only a later phase is blocked.

Human-only blockers should normally be cleared before handoff where practical.

Do not encourage the next executor to brute-force around a blocker only a human can resolve.

---

## Plan Finality Gate

A task is not ready merely because an executor could make a reasonable choice.

Before setting a ready Execution Gate, inspect the entire task for material unresolved choices.

For each choice, do exactly one:

1. lock the decision;
2. classify it explicitly as an executor-owned implementation detail;
3. surface it as a human blocker.

Do not leave material product, architecture, security, fallback, cost, migration, or user-behaviour choices embedded in phrases such as:

* either;
* unless the human prefers;
* could;
* optionally;
* depending on preference;
* choose during implementation.

Those phrases are acceptable only for genuine executor-owned details that do not affect human control.

### Outcome-Oriented Plan Writing

Plans should describe meaningful phases, not merely file operations.

A strong phase communicates:

* what outcome the phase creates;
* why the phase exists;
* an important boundary or risk, when relevant;
* how completion is verified.

This does not require a rigid sub-template.

Weak:

```text
1. Update config.
2. Change loader.
3. Add tests.
```

Better:

```markdown
### Phase 1 — Establish the artifact contract

Define how the threshold belongs to one trained model so it cannot drift
independently from the deployed weights.

### Phase 2 — Apply the selected threshold during inference

Load the validated threshold during model initialization and remove the hidden
assumption that production always uses 0.5.

### Phase 3 — Prevent unsafe mismatches

Define explicit behaviour for missing, malformed, or incompatible threshold files.

### Phase 4 — Prove deployed behaviour

Verify valid, missing, and incompatible artifact paths and expose the active
threshold through logs or model metadata.
```

---

## Fresh-Session Execution Readiness

Use this lifecycle operation when the user says phrases such as:

* “Get ready for execution in a fresh agent chat.”
* “Finalize the plans into the task.”
* “Check for any human or hard blockers.”
* “Make this ready for the next agent.”
* “Prepare this for execution.”

This is stricter than `Update`.

Interpret the phrase as a mandatory pass:

```text
1. Synchronize current truth
2. Finalize all material decisions
3. Build a readable human skim layer
4. Surface control-critical nuances
5. Produce an outcome-oriented execution plan
6. Run Blocker Preflight
7. Run task consistency checks
8. Declare READY or BLOCKED
```

### Readiness Requirements

A task passes only when:

* the goal and why are understandable;
* the success bar is observable;
* the chosen approach is explicit;
* the human owner can understand the important direction and nuance;
* the execution plan is coherent and outcome-oriented;
* decisions are separated from uncertainty;
* every material unresolved issue is classified;
* no undisclosed hard blocker remains;
* the next action is concrete;
* the verification path is clear;
* the task does not depend on the prior conversation;
* the dashboard, plan, blockers, and lifecycle fields agree.

### Ready Outcome

When no hard blockers remain:

* set the appropriate ready Execution Gate;
* set `Blockers: None`;
* state the first executable action in `Next Action`;
* ensure the task can be executed without recovering missing intent or plans from the old chat.

### Blocked Outcome

When a hard blocker remains:

* set `Execution Gate: Needs Human Unblock`;
* set `Status: Blocked`;
* make `Next Action` the exact human action required;
* explain why execution must stop;
* do not describe the task as ready.

### Response Contract

After performing the pass, report a concise verdict:

```text
Execution readiness: READY

Plan finalized: Yes
Human-readable first screen: Yes
Control-critical nuances surfaced: Yes
Material decisions unresolved: None
Human/hard blockers: None
First executable action: [...]
Execution gate: Ready for Main-Agent Execution
```

Or:

```text
Execution readiness: BLOCKED

Blocking issue: [...]
Why it is human-owned or externally blocked: [...]
Required action: [...]
Execution impact: [...]
Execution gate: Needs Human Unblock
```

Never silently update the file while leaving the human to assume it is executable.

---

## Compression Principle

Whenever updating a task, rewrite it from the perspective of:

* the next technically strong fresh-session executor;
* the human owner with limited attention who wants to understand and supervise the work.

### Preserve

* current truth;
* the real goal and why;
* decisions that constrain future choices;
* important responsibility boundaries;
* material trade-offs;
* control-critical nuances;
* uncertainty that still changes execution;
* evidence that materially changed understanding;
* what must happen next;
* hard blockers and required actions;
* dangerous directions future executors must avoid;
* verification requirements.

### Compress or Remove

* stale hypotheses;
* superseded root causes;
* duplicate observations;
* repeated evidence;
* obsolete plans;
* abandoned approaches;
* session diaries;
* raw transcripts;
* failed attempts whose lesson is already captured;
* routine code navigation;
* ordinary command sequences;
* detailed test mechanics a strong executor can reconstruct;
* copied project documentation;
* technical trivia that affects neither human control nor execution.

Do not preserve history merely because it happened.

Do not add detail merely because it might be useful.

Preserve only what materially improves human control or future execution.

---

## Superseded Understanding

When understanding changes substantially:

* do not leave previous beliefs scattered throughout the task;
* update `Current State` to reflect the newest understanding;
* update the selected plan;
* capture invalidated conclusions only when knowing they were ruled out prevents repeated mistakes.

Examples:

* Telemetry initialization investigated and ruled out.
* Earlier deployment hypothesis disproven.
* Prior workaround superseded by a cleaner responsibility boundary.
* Vocabulary-based CTA validation rejected because it caused brittle false failures.

Avoid preserving full reasoning trails unless execution genuinely depends on them.

The task should reflect current understanding, not archaeological layers.

---

## Lifecycle

### Create / Plan

Use when preserving goals, creating work, or preparing future execution.

* Create the dated task file.
* Build the dashboard first.
* Capture alignment decisions from the conversation.
* Explain the outcome, why, and selected direction in human-readable language.
* Record only context that materially improves execution or human control.
* Include optional sections only when they add signal.
* Run Blocker Preflight.
* Set the Execution Gate truthfully.
* If work is intentionally deferred with no active next action, route it to `tasks/backlog/`.

Done when the task preserves the work clearly, even if it is not yet execution-ready.

### Update

Use after meaningful progress, handoff, investigation, or when asked to “update the task.”

* Update `Last Updated`.
* Rewrite rather than append.
* Refresh the dashboard first.
* Replace stale context with current understanding.
* Compress obsolete material.
* Refresh decisions, uncertainty, blockers, and Docs Sync.
* Preserve newly discovered control-critical nuances.
* Refresh the Execution Gate if blockers were discovered or cleared.

An update may legitimately leave the task exploratory, incomplete, or blocked.

Done when `Current State`, `Next Action`, `Blockers`, uncertainty, and Docs Sync are accurate enough for smooth continuation.

### Prepare for Fresh-Session Execution

Use when the user invokes the fresh-session readiness code phrase or asks for plans and blockers to be finalized.

* Perform the full Fresh-Session Execution Readiness pass.
* Finalize one selected plan.
* Remove stale or competing plans.
* Make the first screen readable to the human owner.
* Surface control-critical nuances.
* Run Plan Finality Gate.
* Run Blocker Preflight.
* Run Task Consistency Checks.
* Issue an explicit READY or BLOCKED verdict.

Done when a fresh executor can execute end-to-end without reconstructing missing context, and the human owner can confidently understand and supervise the plan.

### Resume

Use when continuing work.

* Start with the dashboard.
* Check the Execution Gate before acting.
* If `Needs Human Unblock`, stop and surface the required human action.
* Understand current truth before editing.
* Review deeper sections only as needed.
* Recommend trimming if stale, contradictory, bloated, or misleading.
* Preserve new human-control nuances discovered during execution.

Done when the agent knows what to do next, what matters, and what not to repeat.

### Trim / Consolidate

Use when tasks become noisy, overlapping, or difficult to resume.

* Preserve core alignment, current truth, selected plan, blockers, and critical lessons.
* Preserve the small set of human-control nuances.
* Compress duplicate evidence, obsolete attempts, and routine mechanics.
* Mark unresolved claims as `Needs validation`.
* Consolidate overlapping work into the clearest surviving task.
* Ensure one authoritative home for each important point.

Done when the task is easier to read without losing execution effectiveness or human control.

### Close

Use when active execution has genuinely ended.

* Set `Status: Closed`.
* Set `Execution Gate: Not Applicable (Closed)`.
* Update `Last Updated` and `Docs Sync`.
* Rewrite `Current State` to describe what is now true.
* Record final verification.
* State any residual follow-up explicitly.
* Create a separate active or backlog task when meaningful work remains.
* Do not leave a human deploy, validation, or approval action inside a task marked closed.

Done when the task no longer reads like active execution state and durable learnings have been synced or clearly marked.

---

## Task Consistency Checks

Before saving any materially updated task, inspect for contradictions.

Reject or correct:

* `Status: Closed` with pending execution, deployment, validation, or human action;
* a ready Execution Gate with an unresolved human-only prerequisite;
* `Blockers: None` while another section describes required access, approval, credentials, deployment, or manual validation;
* a ready task containing unresolved material alternatives;
* `Next Action` assigned to the human while the gate says ready for agent execution;
* `Execution Gate: Needs Human Unblock` without `Status: Blocked`;
* `Status: Closed` without `Execution Gate: Not Applicable (Closed)`;
* a success bar that cannot be verified by the Verification Contract;
* a chosen approach that conflicts with the implementation plan;
* `Current State` that describes superseded understanding;
* the same important fact stated differently in multiple places;
* a missing Execution Gate on execution-bound work.

The dashboard is not decorative metadata. It must agree with the body.

---

## Non-Negotiables

* Do not place live task dashboards in agent guidance files.
* `tasks/INDEX.md`, if present, is optional convenience only.
* Closed tasks are not automatically deleted.
* `Target Docs` are routing hints, not contracts.
* Preserve uncertainty honestly.
* Do not turn `tasks/` into a general archive or generic backlog.
* Move durable truth to `docs/`.
* Move deferred future-work briefs to `tasks/backlog/`.
* Move supporting artifacts to `source-material/`.
* Move retired historical material to `archive/`.
* For execution-bound tasks, blockers must state both the obstacle and the required action.
* Do not declare readiness merely because the current state is accurate.
* Do not declare readiness when the plan is vague, missing, contradictory, or dependent on the old chat.
* Do not hide product or architecture decisions inside implementation discretion.
* Do not bury important human-control nuances in code-level detail.
* Do not bloat the task with reconstructible mechanics.

---

## Quality Bar

A good task bookmark:

* lets a fresh executor understand and continue the work quickly;
* lets the human owner understand what is happening and whether to proceed;
* explains the outcome, why, and selected direction;
* preserves alignment that code cannot reveal;
* surfaces responsibility boundaries and important trade-offs;
* captures brittle assumptions, recurring failure risks, and silent degradation risks when relevant;
* preserves current truth instead of historical buildup;
* keeps decisions separate from uncertainty;
* identifies concrete next actions;
* makes blockers actionable instead of merely listing them;
* defines how success will be verified;
* prevents repeated mistakes;
* is detailed where human control or execution requires detail;
* is compressed where the detail is routine or reconstructible;
* remains readable rather than becoming an implementation transcript.

The final test is:

```text
Agent can execute it
        +
Human can understand and supervise it
        +
No hidden blockers
        =
Ready for fresh-session execution
```
