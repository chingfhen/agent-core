---
name: project-tasks
description: Maintains shared human-agent execution briefs in tasks/ (including tasks/backlog/ for deferred work) so the human owner can understand and steer the work while a future fresh-session executor can resume without the prior conversation. Load before creating, editing, or managing anything under tasks/; not needed merely to read task files. Rewrites tasks into high-signal control surfaces that preserve execution-critical context and human-control nuances while compressing routine implementation detail and stale history.
disable-model-invocation: false
---

# Project Tasks

## Purpose and Ownership

Maintain task-specific execution briefs, typically in `tasks/`, for work that needs continuity across sessions.

A task file is a **shared control surface** serving two purposes:

1. **Execution continuity**: a fresh-session executor can continue and verify the work without the old conversation.
2. **Human control**: the human owner can understand the direction, inspect important nuance, challenge decisions, assess risk, and decide whether execution should proceed.

A task file is not durable documentation, a transcript, a session diary, an exhaustive implementation manual, or a dumping ground for technical detail. It is a **continuously rewritten execution brief**.

For execution-bound work, the brief and its explicitly linked shared context must be sufficient without the old chat. The human should not need to inspect the code merely to understand the plan.

```text
Human owns                         Agent owns
-----------                        ----------
Intent                             Code navigation
Priorities                         Routine implementation mechanics
Product expectations               Low-level sequencing
Important constraints              Commands and file edits
Architecture boundaries            Detailed test construction
Acceptable trade-offs              Debugging tactics
Risk tolerance                     Ordinary code-placement choices
Approvals and access               Reconstructible technical detail

                 Task file
       -------------------------
       Shared understanding of:
       what, why, chosen direction,
       current state, important nuance,
       blockers, next move, approved plan,
       and proof of success
```

The human should see anything that could materially change direction, responsibility boundaries, user-visible or failure behavior, security, privacy, data integrity, cost, maintainability, recovery semantics, or confidence in the plan. The agent should own routine mechanics that do not affect those concerns.

## Core Model

- **`project-tasks` owns active execution state**, the approved or currently authoritative plan, blockers, verification state, and fresh-session handoffs.
- **`planning` owns how substantial work is shaped and resolved before approval.**
- **`engineering` owns implementation and runtime verification.** This skill records execution state and evidence; maintaining a task does not perform the work described by it.
- **`project-docs` owns durable project knowledge** and absorbs stable truths.
- **`tasks/backlog/` owns deferred future-work briefs** that should survive without becoming active execution state.
- **`source-material/` holds supporting artifacts** that may inform work without becoming canonical truth.
- **`archive/` holds retired historical material** that should not drive current work by default.
- **Code and tests own exact implementation truth.**
- **Conversation owns exploration in progress.**
- Task files preserve current alignment, not archaeological history.
- Preserve uncertainty honestly.
- Assume future executors are technically strong.
- Keep the first screen highly scannable.
- Prefer one authoritative statement of each important fact.

## Information Selection

Ask both:

> What does the next executor need to execute effectively without the old chat?

> What does the human owner need to understand, supervise, challenge, or approve confidently?

Then apply:

```text
Does it affect human steering, approval, risk, or direction?
        |-- Yes -> surface clearly
        `-- No
             |
             v
Is it execution-critical and hard to reconstruct?
        |-- Yes -> preserve in executor detail
        `-- No  -> compress or omit
```

### Surface Clearly

Use the first screen or `Human Attention` for details affecting:

- human steering or approval;
- product behavior or architecture direction;
- responsibility boundaries;
- security, privacy, safety, cost, or data integrity;
- rollback, retry, replay, recovery, or idempotency;
- long-term maintainability;
- confidence that the selected plan is sound.

### Preserve Below the First Screen

Keep detail that is execution-critical, difficult to reconstruct, needed to prevent a repeated mistake, or necessary to understand a non-obvious constraint.

### Compress or Omit

Usually omit routine code navigation, obvious sequencing, ordinary commands, reconstructible test mechanics, duplicated facts, stale investigation history, and trivia that changes neither execution nor human control.

The goal is not to preserve history. The goal is to preserve **execution effectiveness and human control**.

## First-Screen Contract

New standalone tasks use:

```text
tasks/YYYY-MM-DD__kebab-case-name-bookmark.md
```

The date is an **immutable creation date**. Keep standalone tasks flat; use the optional grouping below for related tasks. Follow established repository naming conventions and do not mass-rename historical tasks.

### Related Task Groups

For several separately executable tasks sharing an outcome, use a dated folder:

```text
tasks/
    YYYY-MM-DD__standalone-task-bookmark.md
    YYYY-MM-DD__related-effort/
        overview.md
        01-first-outcome.md
        02-next-outcome.md
```

Use the effort's immutable creation date for the folder. Child task dates remain in their metadata; numeric prefixes indicate intended reading/execution order, not readiness or dependency enforcement.

- **Overview:** shared outcome, constraints, links to tasks, dependency/handoff map, and recommended starting point. No task dashboard or duplicate progress tracking.
- **Individual task:** its normal dashboard, outcome, inputs/outputs, specific decisions, state, blockers, next action, and verification. Set `File` to its actual path and link required shared context and predecessor tasks explicitly.
- Make the first actionable task concrete. Later tasks retain meaningful direction and completion criteria, with decisions dependent on earlier results assigned to those results rather than guessed.
- Keep shared facts authoritative in the overview and task-specific facts in the task. Update affected downstream assumptions after upstream results; do not reopen the whole plan.

One task with several steps remains one file without an overview. If it later needs independent tasks, group it while preserving creation metadata and updating references. Do not migrate unrelated historical tasks. Dependent stages in a current effort stay with that effort; intentionally deferred future work still belongs in the backlog.

### Lifecycle Fields

| Field | Values | Meaning |
| --- | --- | --- |
| **Priority** | `Now` | Active priority. |
|  | `Next` | Intended next-up work. |
|  | `Later` | Preserved but not near-term. |
| **Status** | `Active` | Open and currently intended to progress. |
|  | `Blocked` | Meaningful execution cannot proceed until a blocker clears. |
|  | `On Hold` | Intentionally paused. |
|  | `Closed` | Active execution has ended. |
| **Execution Gate** | `Needs Human Unblock` | A human must act, approve, decide, provide access, or coordinate an external unblock. |
|  | `Waiting for Dependency` | An upstream task or external event must complete; no human intervention is currently required. |
|  | `Ready for Main-Agent Execution` | No known blockers to the next meaningful action; execute mainly through the main agent. |
|  | `Ready for Delegated Execution` | No known blockers to the next meaningful action; bounded parts may be delegated safely. |
|  | `Not Applicable (Closed)` | The task is closed. |
| **Docs Sync** | `Not Synced` | Durable knowledge has not been checked or promoted. |
|  | `Partial` | Some durable knowledge was handled; more may remain. |
|  | `Synced` | Durable knowledge has been checked and any required promotion is complete. |

`Status` describes lifecycle state. `Execution Gate` describes whether execution may begin and what execution shape is allowed. `Docs Sync` describes durable-knowledge handling only.

`Ready for Delegated Execution` indicates only that bounded delegation is permissible. A delegation or execution-topology skill decides what to delegate and how.

When `Execution Gate: Needs Human Unblock`, set `Status: Blocked`, make `Next Action` the exact human action required, and state why meaningful execution should stop.

When `Execution Gate: Waiting for Dependency`, set `Status: Blocked`, name the dependency and completion evidence in `Blockers`, and make `Next Action` identify the producing task or event and the step to take once it completes. If a human must intervene, use `Needs Human Unblock` instead.

When `Status: Closed`, set `Execution Gate: Not Applicable (Closed)` and leave no pending execution disguised as completed work.

### Normal Shape

```markdown
# Task: [Clear short name]

**File:** `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** [Now | Next | Later]
**Status:** [Active | Blocked | On Hold | Closed]
**Execution Gate:** [Needs Human Unblock | Waiting for Dependency | Ready for Main-Agent Execution | Ready for Delegated Execution | Not Applicable (Closed)]
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

For a genuinely small task, `Why`, `Chosen Approach`, or `Human Attention` may be omitted when they add no value. For consequential or execution-bound work, omission should be deliberate.

### Human Skim Test

After reading the first screen, the human should be able to explain:

1. What outcome is being pursued, and why?
2. What solution shape was selected?
3. What is currently true?
4. What happens next?
5. How will success be recognized?
6. What important nuance deserves supervision?
7. Can anything stop execution?

### Writing Rules

- Use plain language before code symbols or shorthand.
- Explain system behavior and consequences, not merely file edits.
- Keep each field focused on one purpose.
- Use compact bullets for independently verifiable conditions.
- Name code locations only after explaining why they matter.
- Avoid unexplained shorthand such as `wire up`, `plumb through`, or `harden semantics`.
- Do not compress several unresolved decisions into one sentence.
- Do not make the human reconstruct the plan from implementation detail.

Weak:

> Load `threshold_config.json`.

Better:

> Load the threshold from the same validated artifact bundle as the model weights so production cannot silently combine a threshold from one training run with weights from another.

### Human Attention

Use `Human Attention` for the smallest set of non-obvious details that materially affect confidence, direction, risk, or long-term quality. Usually include one to five bullets.

A nuance belongs here when it:

- changes component ownership or responsibility boundaries;
- creates silent, repeated, or cumulative degradation;
- creates a non-obvious security, privacy, financial, data-integrity, or operational risk;
- determines important fallback, retry, replay, recovery, or idempotency behavior;
- exposes hidden coupling or a brittle assumption;
- explains why an apparently simple implementation is dangerous;
- captures a lesson future agents are likely to miss;
- materially affects approval or architecture direction.

Explain why the nuance matters. Do not fill this field with routine implementation detail.

## Adaptive Structure

The dashboard is the only default shape. Additional sections are tools, not mandatory output.

- Use only sections that improve future execution or human control.
- Omit empty, obvious, redundant, or low-value sections.
- Prefer a short bookmark with strong signal over a fully populated template.
- Do not repeat the same nuance across several sections unless each placement serves a distinct purpose.

Optional sections:

- Human Intent
- Expected Outcomes
- Decisions Locked
- Chosen Approach Detail
- Important Trade-offs
- Boundaries / Stop Conditions
- Problem Origin
- Current Understanding
- Remaining Uncertainty
- Superseded Understanding
- Implementation Plan
- Executor Guidance
- Likely Blind Spots
- Verification Contract
- Context Pointers
- Visual Handle
- Dangerous Evolution to Avoid
- Execution Topology

Typical emphasis:

- **Feature work:** outcomes, locked decisions, and implementation plan.
- **Debugging:** problem origin, current understanding, useful ruled-out conclusions, and verification.
- **Investigation:** current understanding, uncertainty, and next evidence.
- **Architecture change:** approach detail, trade-offs, Human Attention, and a visual.
- **Small task:** dashboard, next action, and verification.
- **Risky operational work:** Human Attention, stop conditions, rollback or recovery, and verification.

### Implementation Plan

When an approved or authoritative plan exists, preserve it here as a compact sequence of meaningful outcomes.

The task file owns the persisted plan, but it does not need to reproduce the full reasoning process used to create it.

Prefer:

```markdown
### Phase 1: Establish the artifact contract

Define how the threshold belongs to one trained model so it cannot drift independently from the deployed weights.

### Phase 2: Apply and validate the threshold

Load the threshold during model initialization, define behavior for missing or incompatible files, and expose the active value through logs or metadata.

### Phase 3: Prove deployed behavior

Verify valid, missing, malformed, and incompatible artifact paths.
```

Avoid reducing a human-approved plan into a low-level file-edit checklist unless those exact mechanics are important to execution or supervision.

### Dangerous Evolution to Avoid

Use this sparingly when a tempting shortcut could grow into a brittle, misowned, unsafe, or costly subsystem. State the shortcut, why it is harmful, and the boundary that prevents it.

### Visual Handle

Use a tiny ASCII sketch when the mental model is a pipeline, graph, state machine, ownership boundary, or before/after change and prose would hide the structure.

Skip it for linear, small, or obvious changes, and when it would go stale faster than it helps.

```text
queued -> running -> completed
          |
          v
        failed -> retry
```

A visual is a compression tool, not decoration.

## Decision Finality in the Task

The task must reflect one authoritative current direction.

For every material unresolved choice, do exactly one:

1. **Lock it** as an approved or authoritative decision.
2. **Classify it** as executor-owned implementation detail.
3. **Surface it** as unresolved uncertainty or a human blocker.

Do not hide material product, architecture, security, fallback, cost, migration, or user-behavior choices inside phrases such as `either`, `optionally`, `depending on preference`, or `choose during implementation`.

Those phrases are acceptable only for genuine executor-owned details that do not affect human control.

When substantial planning is still required and the user has not approved a direction, use `planning` rather than turning the task file into the planning conversation.

## Blocker Preflight

Before declaring work ready to begin or resume, inspect blockers relevant to its next meaningful action. When merely persisting a plan, classify known prerequisites and unchecked facts from available evidence; do not test credentials, environments, or future operational conditions just to write the brief.

1. **Human access:** missing credentials, permissions, private data, provider access, OAuth, billing, or external configuration.
2. **Human decision:** unresolved acceptance criteria or product, architecture, security, privacy, migration, fallback, cost, or deployment choices.
3. **External system:** unavailable provider capability, pending approval, insufficient quota, missing test environment, hardware, or live validation.
4. **Technical contract:** a required schema, interface, identifier mapping, dependency capability, production state, or safe validation path is unknown and cannot be inferred safely.
5. **Operational safety:** no rollback, backup, controlled validation, observability, clear ownership, or protection against destructive or paid-provider replay.

### Blocker Versus Executor-Owned Uncertainty

```text
Can a fresh executor resolve this through a bounded investigation?
        |-- Yes -> preserve the investigation in the plan or next action.
        `-- No, or meaningful work cannot continue
                -> hard blocker.
```

A bounded investigation should state the exact question, evidence to inspect, and the decision or implementation step that follows. `Investigate further` is not a useful next action.

For every hard blocker, record:

- the blocker;
- why it prevents meaningful execution;
- the exact human action, upstream task result, or external event required;
- whether all execution or only a later phase is blocked.

Human-only blockers should normally be cleared before handoff where practical. Never encourage an executor to brute-force around a blocker only a human can resolve.

Readiness is relative to the next meaningful action, not a claim that every future prerequisite has been verified. A bounded investigation may itself be ready to execute. Record later-phase prerequisites and their gates explicitly; never proceed into a phase before its required inputs, approvals, or safety conditions are satisfied.

## Execution Readiness Gate

Use this gate when the user asks to prepare a task for immediate execution or a fresh-agent execution handoff, or when substantial execution is about to begin. Persisting an approved task set requires an honest brief and a consistency review, not completing this operational preflight for every future stage.

```text
1. Synchronize current truth.
2. Ensure the selected direction is authoritative.
3. Ensure the human skim layer is readable.
4. Ensure the implementation plan is preserved when needed.
5. Run Blocker Preflight.
6. Check dashboard/body consistency.
7. Declare READY or BLOCKED.
```

A task passes only when:

- the goal, why, success bar, and chosen approach are clear;
- the human can understand the direction and important nuance;
- the persisted plan is coherent and verifiable when one is needed;
- decisions are separated from uncertainty;
- every material unresolved issue is classified;
- no undisclosed hard blocker remains;
- the next action is concrete;
- the task does not depend on the old conversation;
- dashboard, plan, blockers, and lifecycle fields agree.

### Consistency Checks

Reject or correct:

- `Status: Closed` with pending execution, validation, approval, or human action;
- a ready gate with a prerequisite preventing the next meaningful action;
- `Blockers: None` while another section describes a blocker to that action; identify later-phase prerequisites separately;
- a ready task containing unresolved material alternatives without an explicit investigation or approval gate before the affected work;
- `Next Action` assigned to the human while the gate says ready for agent execution;
- `Needs Human Unblock` without `Status: Blocked`;
- `Waiting for Dependency` without `Status: Blocked`, an identified dependency, and a completion condition;
- `Status: Closed` without `Not Applicable (Closed)`;
- a success bar unsupported by the verification contract;
- a chosen approach that conflicts with the implementation plan;
- current state that preserves superseded understanding;
- duplicate or contradictory authoritative statements;
- a missing Execution Gate on execution-bound work.

The dashboard is not decorative metadata. It must agree with the body.

### Ready Outcome

When no hard blockers prevent the next meaningful action:

- set the appropriate ready gate;
- set `Blockers: None` when none prevent that action, recording any later-phase prerequisites explicitly;
- put the first executable action in `Next Action`;
- ensure no missing intent or plan must be recovered from the old chat.

```text
Execution readiness: READY
Execution gate: Ready for Main-Agent Execution
Blockers: None
First executable action: [...]
```

### Blocked Outcome

When a hard blocker requires human intervention:

- set `Execution Gate: Needs Human Unblock`;
- set `Status: Blocked`;
- make `Next Action` the exact human action required to resolve or coordinate the blocker;
- explain why meaningful execution must stop;
- do not describe the task as ready.

```text
Execution readiness: BLOCKED
Blocking issue: [...]
Required action: [...]
Execution impact: [...]
Execution gate: Needs Human Unblock
```

For a dependency requiring no human intervention, report `Execution readiness: BLOCKED` with `Execution Gate: Waiting for Dependency`, `Status: Blocked`, the producing task or event, its required completion evidence, and the action that follows. Do not mark a consumer ready while its required input is unavailable, or manufacture a human action for an ordinary task dependency.

Never silently update the file while leaving the human to assume it is executable.

### Security and Privacy

- Never include secrets, credentials, API keys, tokens, passwords, or private keys.
- Minimize personally identifiable or confidential information.
- Reference protected source material rather than copying sensitive content.

## Compression and Current Truth

Rewrite tasks for both a technically strong fresh executor and a human owner with limited attention.

### Preserve

- current truth, goal, and why;
- decisions constraining future choices;
- the approved or authoritative implementation plan when needed;
- responsibility boundaries and material trade-offs;
- control-critical nuance;
- uncertainty that still changes execution;
- evidence that materially changed understanding;
- next action, blockers, and required human actions;
- dangerous directions to avoid;
- verification requirements.

### Compress or Remove

- stale hypotheses and superseded root causes;
- duplicate observations or evidence;
- obsolete plans and abandoned approaches;
- transcripts and session diaries;
- failed attempts whose lesson is already captured;
- routine navigation, commands, and reconstructible test mechanics;
- copied documentation and irrelevant technical trivia.

Do not preserve history merely because it happened. Do not add detail merely because it might be useful.

When understanding changes, update `Current State` and the selected plan, remove invalidated beliefs from active sections, and retain a ruled-out conclusion only when it prevents repeated mistakes.

The task should reflect current understanding, not archaeological layers.

## Lifecycle

All lifecycle operations must preserve dashboard/body consistency, rewrite stale understanding, and update the Execution Gate truthfully.

### Create / Persist Plan

- Create the dated standalone task or related-task group, with dashboards on individual tasks.
- Capture established alignment and explain outcome, why, selected direction, and approved plan when one exists.
- Include optional sections only when useful.
- Classify known blockers and future prerequisites from available evidence and set each gate truthfully; do not execute the planned investigations to finish writing.
- Route intentionally deferred work with no active next action to `tasks/backlog/`.

Done when the work is preserved clearly, even if it is not yet execution-ready.

When the user explicitly wants to vet substantial planning before persistence, use `planning` first and write the approved result here afterward.

### Update

- Update `Last Updated` and rewrite rather than append.
- Refresh dashboard, current truth, decisions, plan, uncertainty, blockers, Docs Sync, Human Attention, and gate.
- Compress obsolete material.

An update may legitimately leave the task exploratory, incomplete, or blocked.

### Prepare for Fresh-Session Execution

- Run the full Execution Readiness Gate.
- Preserve one authoritative selected direction.
- Remove or clearly mark stale alternatives.
- Issue an explicit `READY` or `BLOCKED` verdict.

Done when the fresh executor has the context to take the next permitted action, or a precise blocker and unblock condition, and the human can confidently supervise the plan. For a task set, distinguish the actionable tasks from dependent stages; do not imply all tasks are ready.

### Resume

- Start with the dashboard and check the gate before acting.
- If `Execution Gate: Needs Human Unblock`, stop and surface the required human action.
- If `Execution Gate: Waiting for Dependency`, check the stated completion evidence before starting the dependent work. If unavailable, surface the dependency; do not poll indefinitely or start unrelated work. When it clears, refresh the gate.
- Understand current truth before editing.
- Review deeper sections only as needed.
- Preserve newly discovered human-control nuance.
- If execution discovers a material plan-changing decision that requires human ownership, stop and surface it rather than silently redesigning the task.

### Trim / Consolidate

- Preserve alignment, current truth, selected plan, blockers, and critical lessons.
- Compress duplicates, obsolete attempts, and routine mechanics.
- Mark unresolved claims as `Needs validation`.
- Consolidate overlapping work and keep one authoritative home for each important point.

### Close

- Set `Status: Closed` and `Execution Gate: Not Applicable (Closed)`.
- Update `Last Updated`, `Docs Sync`, current state, and final verification.
- State residual follow-up explicitly.
- Create a separate active or backlog task when meaningful work remains.
- Do not leave deployment, validation, approval, or cleanup inside a closed task.

## Non-Negotiables

- Do not place live task dashboards in agent guidance files.
- `tasks/INDEX.md`, if present, is optional convenience only.
- Closed tasks are not automatically deleted.
- `Target Docs` are routing hints, not contracts.
- Preserve uncertainty honestly.
- Move durable truth to `docs/`, deferred work to `tasks/backlog/`, supporting artifacts to `source-material/`, and retired history to `archive/`.
- Blockers must state both the obstacle and required action.
- Do not declare readiness when the next meaningful action is vague, contradictory, blocked, dependent on the old chat, or requires an unresolved material choice without a prior investigation or approval gate.
- Do not hide product or architecture decisions inside implementation discretion.
- Do not bury human-control nuance in code-level detail.
- Do not bloat the task with reconstructible mechanics.
- Do not use the task file as a transcript of the planning conversation.
- Preserve the approved plan without preserving every thought that led to it.

## Final Test

A good task bookmark lets a fresh executor continue quickly, lets the human understand and supervise the work, preserves alignment code cannot reveal, preserves the authoritative plan, separates decisions from uncertainty, makes blockers actionable, defines verification, prevents repeated mistakes, and remains readable rather than becoming an implementation transcript.

```text
Agent can execute it
        +
Human can understand and supervise it
        +
Approved direction survives the session
        +
No hidden blockers
        =
Ready for fresh-session execution
```
