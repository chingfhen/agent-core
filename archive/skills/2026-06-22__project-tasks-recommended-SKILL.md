---
name: project-tasks
description: Maintain active execution state in tasks/ when work needs continuity, smooth delivery, current alignment, fresh-session resume, task update, trim, consolidation, or clean closure.
---

# Project Tasks

Maintain active execution state for repo progress.

A task file is a short-lived execution surface for work that needs continuity, delivery discipline, current alignment, or fresh-session handoff. It should preserve the state needed to continue execution smoothly: goal, current understanding, constraints, next action, blockers, unresolved uncertainty, and decisions that affect delivery.

`project-tasks` is general repo maintenance. It is not coding-specific.

## Core Model

- **`project-tasks` owns active execution state** for smooth delivery of short-lived work.
- **`project-docs` owns durable behavior and truth** for long-term agent consistency.
- **`source-material/` holds supporting artifacts** that may still inform work without becoming canonical truth.
- **`archive/` holds historical material** that should not drive current execution by default.
- A task is neither a transcript nor durable documentation.
- A task is a continuously rewritten execution bookmark.
- Preserve what future executors cannot reliably infer from code, docs, or obvious context.
- Compress what no longer changes future decisions.
- Prefer current state over historical narrative.
- Assume future executors are technically strong; preserve alignment, intent, constraints, non-goals, blind spots, and decision context they would otherwise miss.

## Guiding Question

Ask:

> If a fresh agent resumed this work tomorrow, what execution state would they need that they could not quickly reconstruct?

Preserve that. Everything else is negotiable. The goal is smooth delivery, not preserving history.

## Lifecycle

### Create / Plan

Use when new work needs continuity, current alignment, or planned execution state.

1. Create `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md` unless updating an existing task fits better.
2. Build the dashboard first: goal, success bar, current state, next action, blockers, target docs, and relevant code.
3. Capture human intent, constraints, non-goals, expected outcomes, and critical mistakes future executors must avoid when they change execution quality.
4. Use `grilling` before creating or materially reshaping consequential work when the goal, constraints, or success bar are not already clear.
5. Record only context future executors cannot reliably reconstruct.

Done when a future executor can start the work without asking what the work is, why it matters, what success means, or what to do next.

### Update

Use after meaningful progress, a handoff point, a decision, a new blocker, or an explicit request to update the task.

1. Update `Last Updated`.
2. Refresh the dashboard first.
3. Rewrite around current state instead of appending a session diary.
4. Replace stale hypotheses, obsolete plans, and superseded guidance with the newest understanding.
5. Move stable truths into docs when they become durable. Keep `Target Docs` current.

Done when current state, next action, blockers, uncertainty, and docs-sync state are accurate enough for smooth continuation.

### Resume

Use when continuing work from a task.

1. Start with the dashboard.
2. Read deeper sections only as needed.
3. Identify current truth, next action, blockers, and uncertainty before acting.
4. Treat stale or contradictory material as a signal to trim before relying on it.

Done when the agent knows what to do next, what constraints matter, and what not to repeat.

### Trim / Consolidate

Use when tasks become noisy, stale, overlapping, contradictory, or hard to resume.

1. Preserve core alignment, current understanding, next action, blockers, unresolved uncertainty, and critical lessons.
2. Remove duplicate evidence, raw transcripts, stale hypotheses, obsolete plans, abandoned approaches, and failed attempts whose lessons are already captured.
3. Consolidate overlapping work into the clearest surviving task when one bookmark can carry the execution state better.
4. Mark unresolved claims as `Needs validation` instead of promoting them to fact.

Done when stale history no longer competes with current state and a future executor can resume without archaeological reading.

### Close

Use when active execution has ended or the task no longer represents live work.

1. Set `Status` to `Closed`.
2. Update `Last Updated`.
3. Set `Docs Sync` to `Synced`, `Partial`, or `Not Synced` based only on durable knowledge synchronization.
4. Rewrite `Current State` to state what is now true.
5. State remaining follow-up explicitly, or say none.
6. Route durable learnings to `project-docs` when needed.

Done when the task no longer reads like active execution state and any durable learnings have either been synced or clearly marked as not synced.

## Dashboard Contract

New tasks use `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`. The date is an immutable creation date. Keep `tasks/` flat unless the repository already uses another convention. Do not mass-rename historical tasks.

Use only these explicit fields:

| Field | Values | Meaning |
| ----- | ------ | ------- |
| Priority | `Now` | Active priority. |
| Priority | `Next` | Intended next-up work. |
| Priority | `Later` | Preserved but not near-term. |
| Status | `Active` | Execution is live. |
| Status | `Blocked` | Execution cannot proceed without a blocker clearing. |
| Status | `On Hold` | Intentionally paused. |
| Status | `Closed` | Execution has ended. |
| Docs Sync | `Not Synced` | Durable knowledge has not been checked or promoted. |
| Docs Sync | `Partial` | Some durable knowledge was promoted or checked; more may remain. |
| Docs Sync | `Synced` | Durable knowledge has been handled. |

`Status` reflects execution state only. `Docs Sync` reflects durable knowledge synchronization only. Put descriptive state in `Current State`, never in status fields.

Suggested dashboard:

```markdown
# Task: [Clear short name]

**File:** `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** [Now | Next | Later]
**Status:** [Active | Blocked | On Hold | Closed]
**Docs Sync:** [Not Synced | Partial | Synced]

**Goal:** [...]
**Success Bar:** [...]
**Current State:** [...]
**Next Action:** [...]
**Blockers:** [...]

**Target Docs:** [...]
**Relevant Code:** [...]
```

## Adaptive Sections

Use only sections that materially improve future execution. Do not populate sections simply because they exist. A shorter bookmark with stronger signal is preferred over a fully populated template.

Optional sections:

- Human Intent
- Expected Outcomes
- Decisions Locked
- Non-Goals / Stop Conditions
- Problem Origin
- Current Understanding
- Remaining Uncertainty
- Superseded Understanding
- Executor Guidance
- Likely Blind Spots
- Verification Contract
- Context Pointers

Feature work may emphasize intent, outcomes, and decisions. Debugging may emphasize problem origin, current state, ruled-out hypotheses, and verification. Investigations may emphasize current understanding, remaining uncertainty, and next evidence. Small tasks may need only the dashboard.

## Compression Rules

Preserve:

- Current truth
- Remaining uncertainty
- Evidence that materially changed understanding
- Decisions that constrain future choices
- Next action
- Blockers
- Mistakes future executors must not repeat
- Human intent that code or docs cannot reveal

Compress or remove:

- Stale hypotheses
- Superseded root causes
- Duplicate observations
- Repeated evidence
- Obsolete plans
- Abandoned approaches
- Session diaries
- Raw transcripts
- Failed attempts whose lessons have already been captured

When understanding changes substantially, update `Current State` to the newest understanding. Keep superseded understanding only when knowing it was ruled out prevents repeated mistakes.

## Non-Negotiables

- Do not place live task dashboards in agent guidance files.
- `tasks/INDEX.md`, if present, is optional convenience only.
- Closed tasks are not automatically deleted.
- `Target Docs` are routing hints, not contracts.
- Preserve uncertainty honestly; do not write uncertain claims as established fact.
- Do not turn `tasks/` into a general archive.
- Move durable truth to `docs/`, supporting artifacts to `source-material/`, and retired historical material to `archive/`.
