---
name: project-tasks
description: Maintains fresh-session execution briefs in tasks/ so future agents can resume work with the same alignment, current understanding, and decision context. Continuously rewrites tasks into high-signal handoff bookmarks by preserving what the next executor cannot reliably reconstruct and compressing what no longer changes future decisions.
disable-model-invocation: false
---

# Project Tasks

Maintain task-specific execution briefs, typically in `tasks/`, for work that needs continuity across sessions.  
A task file is not durable documentation and not a raw transcript.  
Its purpose is to maximize the effectiveness of the next fresh-session executor.  
A task bookmark should preserve whatever the next executor cannot reliably reconstruct from code, docs, or obvious context.

Some tasks preserve ideas, investigations, or future work. Others are prepared for execution. When preparing a task for execution, ensure the task itself contains everything a fresh executor needs to proceed without relying on prior conversations. 

For execution-bound tasks, the task file should stand on its own. A fresh executor should not need the prior conversation, and should only need this skill for conventions, not for missing task context.


## Core Model

*   **`project-tasks` owns active execution state**, orchestration context, and fresh-session handoff briefs.
*   **`project-docs` owns durable project knowledge** and continuously absorbs stable truths throughout execution.
*   **`ai_video_saas/docs/backlog/` owns deferred future-work briefs** that should survive without becoming active execution state.
*   **`source-material/` holds supporting artifacts** that may still inform work without becoming canonical truth.
*   **`archive/` holds historical material** that is kept for reference but should not drive current execution by default.
*   **Task files preserve alignment**, evolving understanding, important uncertainty, and execution context.
*   Tasks may contain investigations, debugging context, planning, implementation guidance, or mini-specs when doing so improves future execution.
*   A task is **neither a transcript nor a summary**.
*   A task is a **continuously rewritten execution brief**.
*   **Preserve** what future executors cannot reliably infer.
*   **Compress** what no longer changes future decisions.
*   **Prefer current truth** over historical narrative.
*   **Assume future executors are technically strong.**
*   **Capture human intent**, constraints, non-goals, blind spots, and decision context they would otherwise miss.
*   **Do not handhold** obvious implementation steps.
*   Keep the first screen **highly scannable**.

### Guiding Philosophy

Ask:
> If a fresh agent resumed this work tomorrow, what would they genuinely need to know that they could not quickly reconstruct themselves?

*   **Preserve that.**
*   Everything else is negotiable.
*   The goal is **not to preserve history**.
*   The goal is to **preserve execution effectiveness**.

## Dashboard Contract

New tasks use `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`. The date is an **immutable creation date**. Keep `tasks/` **flat** unless the repository already uses another convention. **Do not mass-rename** historical tasks.

Use only these explicit fields:

| Field | Values | Meaning |
| ----- | ------ | ------- |
| **Priority** | `Now` | Active priority. |
| **Priority** | `Next` | Intended next-up work. |
| **Priority** | `Later` | Preserved but not near-term. |
| **Status** | `Active` | Execution is live. |
| **Status** | `Blocked` | Execution cannot proceed until a blocker clears. |
| **Status** | `On Hold` | Intentionally paused. |
| **Status** | `Closed` | Execution has ended. |
| **Execution Gate** | `Needs Human Unblock` | A human must act/approve/decide before execution can begin. |
| **Execution Gate** | `Ready for Main-Agent Execution` | No known hard blockers; execute mainly phase-by-phase via the main agent. |
| **Execution Gate** | `Ready for Delegated Execution` | No known hard blockers; some bounded parts are safe to hand to subagents. |
| **Docs Sync** | `Not Synced` | Durable knowledge has not been checked or promoted. |
| **Docs Sync** | `Partial` | Some durable knowledge was promoted or checked; more may remain. |
| **Docs Sync** | `Synced` | Durable knowledge has been handled. |

`Status` reflects **execution state only**. `Docs Sync` reflects **durable knowledge synchronization only**. `Execution Gate` reflects **whether an executor may begin and what execution shape is allowed** — it is not lifecycle state. `Status` = where the task is in its lifecycle; `Execution Gate` = whether it is safe to start. When the gate is `Needs Human Unblock`, set `Status: Blocked` and make `Next Action` the exact human unblock step. Put descriptive state in **Current State**, never in status fields.

```markdown
# Task: [Clear short name]

**File:** `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** [Now | Next | Later]
**Status:** [Active | Blocked | On Hold | Closed]
**Execution Gate:** [Needs Human Unblock | Ready for Main-Agent Execution | Ready for Delegated Execution]
**Docs Sync:** [Not Synced | Partial | Synced]

**Goal:** [...]
**Success Bar:** [...]
**Current State:** [...]
**Next Action:** [...]
**Blockers:** [...]

**Target Docs:** [...]
**Relevant Code:** [...]
```

For execution-bound tasks:

* Use `None` when execution can begin immediately.
* If blocked, state:
  * the blocker,
  * the required action to unblock it,
  * and whether execution should stop.
* Human-only blockers (credentials, approvals, access, product decisions, external actions, etc.) should normally be resolved before handoff where practical.
* Do not hand off a task that encourages the next executor to brute-force around a blocker that only a human can resolve.

## Non-Negotiables

*   **Do not place live task dashboards** in agent guidance files.
*   `tasks/INDEX.md`, if present, is an **optional convenience only**.
*   Closed tasks are **not automatically deleted**.
*   **Target Docs** are routing hints, not contracts.
*   **Preserve uncertainty honestly.** Do not write uncertain claims as established fact.
*   Do not turn `tasks/` into a general archive or backlog; move durable truth to `docs/`, deferred future-work briefs to `ai_video_saas/docs/backlog/`, supporting artifacts to `source-material/`, and retired historical material to `archive/`.
*   For execution-bound tasks, blockers should describe both the obstacle and the required action to unblock it.

## Adaptive Structure

The dashboard is the only default shape. Additional sections are available tools, not mandatory output. Use only sections that **materially improve future execution**.

*   **Do not populate sections** simply because they exist.
*   **Omit sections** that are obvious, empty, redundant, or low-value.
*   A **shorter bookmark with stronger signal** is preferred over a fully populated template.
*   Different tasks require different structure.

Optional sections:

*   Human Intent
*   Expected Outcomes
*   Decisions Locked
*   Non-Goals / Stop Conditions
*   Problem Origin
*   Current Understanding
*   Remaining Uncertainty
*   Superseded Understanding
*   Executor Guidance
*   Likely Blind Spots
*   Verification Contract
*   Context Pointers
*   Visual Handle (a tiny visual / ASCII sketch when structure is the thing to grasp — see below)
*   Execution Topology (larger tasks only — Recommended Shape / Human Gates / Delegation Plan / Do Not Delegate; the `execution-topology` skill owns subagent decisions, not this skill)

Examples:
*   **Feature work** may emphasize: Human Intent, Expected Outcomes, Decisions Locked.
*   **Debugging** may emphasize: Problem Origin, Current State, Superseded Understanding, Verification Contract.
*   **Investigations** may emphasize: Current Understanding, Remaining Uncertainty, Next Evidence.
*   **Small tasks** may require only: Dashboard, Current State, Next Action.

Choose your structure intentionally.

### Visual Handle

A tiny visual / ASCII sketch — a flow, state machine, or before→after sketch — is recommended when **structure is the thing the next executor must grasp**. It is a compression tool, not decoration.

*   **Use it** when the mental model is a graph, pipeline, or state machine, or when the task changes an execution path. Prose is lossy for these; a sketch is not.
*   **Skip it** for linear or small tasks, pure config/copy changes, or anything already obvious from the code. Never add one for polish.
*   **Keep it cheap.** A handful of lines, not a diagram to maintain. If it would go stale faster than it helps, leave it out.

```text
request → route → auth → handler → DB → response
```

```text
queued → running → completed
          ↓
        failed → retry
```

```text
Before: route calls provider directly
After:  route creates job → worker calls provider
```

## Alignment Gate

Use **grilling** before creating or materially reshaping consequential work, especially when writing plans for future execution. Before creating a substantial new task, establish:

1.  The real goal
2.  Success criteria
3.  Important constraints
4.  Non-goals
5.  Expected outcomes
6.  Critical mistakes future executors must avoid

Draft **Expected Outcomes** for confirmation unless the user's instructions already define them clearly, or the update is routine. **Do not over-question straightforward updates.**

## Blocker Preflight

Before writing a substantial execution plan, resuming a task, or preparing a fresh-session handoff, check whether execution needs anything only the human can provide or approve:

*   credentials, API keys, secrets, tokens, env vars
*   cloud / provider / dashboard / repo / database access
*   OAuth, webhook, DNS, billing, or other external setup
*   migration, production-deploy, security, payment, or product-decision approval
*   unclear acceptance criteria, or manual login/testing required before progress is meaningful

If any apply, set `Execution Gate: Needs Human Unblock`, `Status: Blocked`, and make `Next Action` the exact human action required. Do not brute-force around a missing human unblock — stop and surface it.

## Compression Principle

Whenever updating a task, **rewrite it from the perspective of the next fresh-session executor** who has limited time.

*   **Preserve:**
    *   What is currently believed to be true
    *   What remains uncertain
    *   Evidence that materially changed understanding
    *   Decisions that constrain future choices
    *   What must happen next
    *   Mistakes future executors must not repeat
*   **Compress or remove:**
    *   Stale hypotheses
    *   Superseded root causes
    *   Duplicate observations
    *   Repeated evidence
    *   Obsolete plans
    *   Abandoned approaches
    *   Session diaries
    *   Raw transcripts
    *   Failed attempts whose lessons have already been captured

Do not preserve history merely because it happened. **Preserve only history that changes future decisions.**

### Superseded Understanding

When understanding changes substantially:
*   **Do not leave previous beliefs scattered** throughout the task.
*   Update **Current State** to reflect the newest understanding.
*   Capture invalidated conclusions **only** when future executors still benefit from knowing they were ruled out. Summarize them briefly.

> *Examples:*
> * Telemetry initialization investigated and ruled out.
> * Earlier deployment hypothesis disproven.
> * Prior workaround superseded by a cleaner fix.

Avoid preserving full reasoning trails unless future execution genuinely depends on them. The task should reflect **current understanding, not archaeological layers.**

## Lifecycle

### Create / Plan
Use when preserving goals, creating work, or preparing future execution.
*   Create the dated task file.
*   Build the dashboard first.
*   Capture alignment decisions from the conversation.
*   Record only the context future executors cannot reconstruct.
*   Include Expected Outcomes, Decisions Locked, Non-Goals / Stop Conditions, Executor Guidance, or Verification Contract only when they materially improve execution quality. For execution-bound work, capture approved decisions that materially constrain future execution and any unresolved blockers that should stop execution.
*   Run Blocker Preflight and set the Execution Gate before declaring the task ready for execution.
*   If the work is intentionally deferred with no active next action, route it to `ai_video_saas/docs/backlog/` via `project-docs` instead of creating a task bookmark.

Done when a future executor can start without asking what the work is, why it matters, what success means, or what to do next.

### Update
Use after meaningful progress, handoff, or when asked to update the task.
*   Update `Last Updated`.
*   **Rewrite rather than append.**
*   Refresh the dashboard first.
*   Replace stale context with current understanding and compress obsolete material.
*   Refresh the Execution Gate if blockers were discovered or cleared.
*   Move durable truths into docs when they stabilize. Keep `Target Docs` current.

Done when Current State, Next Action, Blockers, uncertainty, and Docs Sync are accurate enough for smooth continuation.

### Resume
Use when continuing work.
*   Start with the dashboard.
*   Check the Execution Gate before acting; if `Needs Human Unblock`, stop and surface the human action instead of executing.
*   Understand current truth before acting.
*   Review additional sections only as needed.
*   Recommend trimming if stale, contradictory, bloated, or misleading.

Done when the agent knows what to do next, what constraints matter, and what not to repeat.

### Trim / Consolidate
Use when tasks become noisy, overlapping, or difficult to resume.
*   Preserve core alignment, current understanding, next actions, and critical lessons.
*   Compress duplicate evidence, obsolete attempts, and stale guidance.
*   Mark unresolved claims as `Needs validation`.
*   Consolidate overlapping work into the clearest surviving task.

Done when stale history no longer competes with current state and a future executor can resume without archaeological reading.

### Close
Use when active execution has ended.
*   Set Status to `Closed`.
*   Update `Last Updated` and `Docs Sync`.
*   Rewrite `Current State` to describe what is now true.
*   State any remaining follow-up explicitly.
*   Avoid creating duplicate persistence summaries; keep it clean for future reference.

Done when the task no longer reads like active execution state and any durable learnings have either been synced or clearly marked as not synced.

## Quality Bar

A good task bookmark:

* Lets a future executor understand the situation quickly.
* Preserves alignment that code cannot reveal.
* Captures current truth instead of historical buildup.
* Preserves important uncertainty honestly.
* Prevents repeated mistakes.
* Identifies what remains to be done and points toward the right evidence.
* Supports effective resumption after a fresh session.
* Makes blockers actionable instead of merely listing them.

If a future executor can resume confidently and effectively without rereading the entire history of the work, the task is doing its job.
