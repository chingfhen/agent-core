---
name: project-tasks
description: >
  Preserve unfinished project work as portable human-agent execution memory.
  Use to create, checkpoint, pause for a fresh session, prepare, revise,
  resume, execute, or close a saved project task, including maintaining its
  progress and task index. Coordinate docs, KB, and lessons when the human asks
  to hand work to a fresh session or close it out. Load before
  managing a configured task surface or continuing a persisted task; not for
  unrelated implementation or merely reading an explicitly named file. Resolve
  project task locations through applicable AGENTS.md, and preserve decisions,
  deliverables, permission boundaries, verification state, and the next permitted action.
disable-model-invocation: false
---

# Project Tasks

## Job and boundary

**Make unfinished work portable.** A task is durable execution memory: a shared
human-agent brief that makes planning, investigation, implementation, validation,
or later discussion continuable across sessions, agents, harnesses, and machines.

Use one when the answer to **"Will future continuation of this work need a durable
brief?"** is yes. A task need not be implementation-ready. Its first screen
should help the human understand and supervise the work; a fresh agent should be
able to take the **next permitted action** without the previous conversation.

This skill owns the *memory of the work* and its handoff, not the work's implementation method.
`planning` shapes substantial work when plan review is required; engineering or
other execution workflows perform and verify the work; `project-docs` owns
settled project understanding. Code, tests, schemas, and observed behavior
remain authoritative for their respective implementation claims. Do not create
tasks for ordinary short-lived implementation with no persistence need.

Saving a task does not approve implementation. Asking to execute a saved task
authorizes only the actions already permitted by the user's request, project
guidance, and task gates. It normally also includes maintaining **that task's
progress and its index entry**, unless stricter guidance requires separate
permission. It does not authorize unrelated task edits, subagents, spending,
deployment, commits, pushes, or documentation/KB writes. Explicit handoff and
closeout requests additionally authorize the bounded persistence review below,
subject to narrower local rules and the human's stated limits.

## Resolve the project and its task surface

Before creating, changing, indexing, or executing a persisted task, read the
applicable `AGENTS.md` task routing and relevant repository guidance. Resolve the
**project from the requested work**, not just the current working directory.
One project can span multiple repositories and use one shared Tasks location;
different projects can share a workspace root.

- Use the configured `Tasks` location. New section-relative paths resolve from
  the declaring AGENTS.md directory; legacy workspace-relative paths retain their
  recorded workspace root. Neither uses the process working directory. A directly
  identified task file may be read without loading this skill merely to read it.
- For missing routing or an authorized routing change, read
  [Task routing](references/routing.md). This skill can establish its own resources
  without workspace-setup. Ask about ambiguous identity/ownership; report an
  inaccessible configured destination instead of substituting a path.
- A human can explicitly select a destination for one operation, without
  silently changing the saved map. Create a confirmed but absent directory only
  during an authorized write.
- No guessed `tasks/` fallback, `projects.toml`, or whole-workspace inventory.
  Maintain only the owned task-root/index section when routing actually changes;
  preserve legacy central blocks until an explicitly approved migration.
- The configured task surface (including its `INDEX.md`) is this skill's normal
  writable scope. Other repositories, docs, code, raw evidence, archives, and
  guidance must be changed only under their own authorization/workflows.
  Report exact physical paths changed, as well as useful logical task paths.

Apply narrower repository rules even when this skill would ordinarily maintain
state automatically. In particular, a repository that makes task changes
explicitly opt-in does not gain broader write permission just because execution
started.

## Stable layout and discovery

For **new** tasks, use a creation-month folder and one shallow, semantic
workstream folder inside the configured task surface:

```text
tasks/
  INDEX.md
  YYYY-MM/
    aws-migration/
      YYYY-MM-DD__validate-cutover.md
      YYYY-MM-DD__prepare-rollback.md
    dataset-evaluation/
      YYYY-MM-DD__agree-evaluation-criteria.md
```

`tasks/` here is a *logical* location; its actual root comes from `AGENTS.md`.
Reuse literal workstream names across months; create folders only as needed.
An overview or related-effort subfolder is useful only for independently
continuable tasks sharing meaningful coordination, not for every workstream.
Use descriptive, distinctive filenames. The folder and filename dates are the
task's **creation date**, not the last update, planned execution date, or closure
date. Once created, the path stays stable across Active, Blocked, On Hold, and
Closed. Do not move completed tasks into `archive/` or deferred tasks into
`backlog/`. Git history or the unchanged file preserves historical access.

Legacy task locations, filename suffixes, groups, and gates remain usable.
Read or modify an authorized legacy file **in place**. Do not silently rename,
move, delete, or mass-migrate existing files to the new scheme.

### INDEX.md — the current-work view

Maintain `INDEX.md` automatically as part of every authorized task creation,
material state/priority/next-action change, closure, or reopening. It is a
**navigation view**, not a competing source of truth or a second task record.

- Include links to **all known unfinished tasks**: Active, Blocked, and On Hold.
  Group by `Now`, `Next`, and `Later` priority; show a concise task name, status,
  and meaningful next action or re-entry/blocking condition. Show workstream
  labels so related work remains discoverable across months. Keep this scannable.
- Exclude Closed tasks from the live dashboard. Keep their files at their stable
  paths for filename, month, and targeted-content search. Reopening restores
  the entry. Don't create a separate historical catalogue by default.
- Derive entries from the task files. On routine changes, update only affected
  entries and preserve unrelated content. Check relevant index entries before
  creating a task; use bounded, targeted search when similar work may exist.
- When `INDEX.md` is absent on an authorized write, initialize it from a
  bounded inventory of the configured task surface, including known legacy
  folders. Do not silently present a partial inventory as complete: flag
  unknown coverage if exhaustive discovery is unavailable. Never search other
  projects or rewrite unrelated files to make the index look full.
- Keep relative links and any group overview/child links valid. Avoid redundant
  entries for the same coherent effort; list independently continuable outcomes
  when they need separate tracking. If index maintenance fails, preserve the
  authoritative task write if safe and report the index as out of sync.

No monthly indexes, external registries, background synchronizers, database,
or automatic scheduled sweeps are required. A broader task hygiene sweep is a
separate, explicitly requested operation.

For natural-language continuation such as "where are we with the AWS migration?",
select the relevant project/index, then read the matching task before its next
permitted action. Ask only when materially different candidates remain plausible.
Give a short state/next-action summary. Confirm the relevant code repository from
the task or a project entry point; a shared task folder does not establish code cwd.

## Task depth — Brief / Standard / Detailed

**Standard is the default.** Select the level by the requested handoff and its
consequences, not a word-count quota. Respect an explicit mode; use Detailed
when the human specifically wants a strong planner to prepare work for a smaller
executor. Do not silently inflate routine tasks.

When authoring or substantially revising a task, show **one compact human-facing
line** identifying the selected mode and alternatives, for example:

`Project Tasks · Standard (also: Brief / Detailed)`

This is output observability, not mandatory task metadata or a heading in the
saved file. Omit the mode line for ordinary reading, execution, or minor status
updates.

- **Brief:** preserve an idea, early investigation, or lightweight handoff.
  Capture goal/why, what's known or undecided, permission boundary, and next
  meaningful action. Compactness does not excuse ambiguity.
- **Standard:** a fresh-session working brief. Add success bar, current state,
  selected direction or explicit uncertainty, important constraints, blockers,
  verification requirements, and an actionable next step.
- **Detailed:** a high-fidelity planner-to-executor handoff. Preserve consequential
  decisions and rationale; the chosen architecture or strategy; grounded files,
  interfaces, and dependencies where known; ordered phases and checkpoints;
  acceptance tests or observable outcomes; important edge cases, recovery paths,
  stop conditions, and boundaries of executor discretion. Clearly distinguish
  observed facts, planned changes, assumptions, and unresolved human choices.
  Include the details a smaller model might otherwise have to rediscover.

**Trust the executor's ability to implement, but do not require it to
rediscover decisions that the planner has already resolved.** Detailed does
not mean micromanaging every command or prescribing speculative code edits.
Correctness, honesty, and executable clarity apply at all depths. Preserve
useful depth through handoff; compress completed or superseded mechanics as
work proceeds without discarding still-binding decisions, acceptance criteria,
or important failure lessons.

## Task contract

Keep the first screen useful before any long plan. A normal new task has:

```markdown
# Task: [Clear outcome]

**File:** `tasks/YYYY-MM/<workstream>/YYYY-MM-DD__descriptive-name.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** Now | Next | Later
**Status:** Active | Blocked | On Hold | Closed

**Goal:** [...]
**Why:** [...]
**Deliverables:** [concrete outputs or changes, when useful]
**Success Bar:** [...]
**Chosen Direction:** [selected | not yet selected]
**Current State:** [...]
**Next Action:** [action AND whether it is permitted]
**Blockers:** [none | blocker, impact, and clearing condition]
```

Combine `Why` with `Goal` or omit empty optional fields on simple tasks. Add
`Human Attention`, `Permission Boundary`, `Verification`, `Docs Sync`,
`Relevant Code`, or deeper sections only when they improve control or
continuation. Do not turn this outline into a mandatory form.

The goal describes the intended outcome; deliverables name reviewable outputs
(for example IaC, a validation report, or a PR); the success bar establishes their
acceptance. Combine these on small tasks rather than requiring three empty fields.

The human should quickly know **what/why, what is decided, what is true now,
what is allowed next, what blocks it, and how success will be verified**.

Use two independent dimensions:

- **Priority:** Now = current focus; Next = intended next-up; Later = deferred
  but worth retaining. Later replaces a separate backlog folder.
- **Status:** Active = progress intended; Blocked = next meaningful action
  prevented by a dependency or human decision; On Hold = intentionally paused;
  Closed = work ended, not necessarily successfully implemented.

Closing may mean **Completed**, **Cancelled**, or **Superseded**. Record the
reason and actual verification/outcome when consequential; never portray
cancelled work as implemented. Closure does not change the file path. A paused
or blocked task needs a useful re-entry condition. Priority and status are
*not* execution permission.

### Decisions, plans, and uncertainty

For material choices, record one of: **locked/approved decision**, **executor-owned
routine detail**, or **unresolved choice with a permitted investigation or human
decision**. Preserve consequential product, architecture, security, privacy,
migration, fallback, cost, and user-behavior choices. Don't hide them behind
"either", "optionally", or "choose during implementation".

A task should have one current direction and current state; it need not pretend
the direction is selected before it is. Keep it self-contained for a fresh
session, linking canonical sources rather than copying competing project truth.
Rework stale sections instead of appending a session diary. Preserve history only
where it prevents a recurring mistake or explains a still-binding constraint.

Useful optional Detailed sections: `Decisions Locked`, `Grounded Current
Understanding`, `Implementation Strategy`, `Execution Phases`, `Acceptance and
Verification`, `Edge Cases and Recovery`, `Stop Conditions`, `Executor
Discretion`, and `Context Pointers`. Use only those that earn their space.

When substantial planning requires review, use `planning` and wait for approval.
Persist an approved plan without re-requesting ceremonial approval; do not
execute future investigations or preflight checks merely to write the task.

### Resume context

On creation, resumption, or substantial handoff, consult relevant project docs and use KB
recall when prior findings could materially inform the work. Read-only retrieval
does not authorize source maintenance. Keep a small context map with exact paths
or remote locators, what each source supplies, and when it must be read. Identify
approved design, observed evidence, procedures, and unresolved investigation
accurately; code/runtime still controls current implementation claims.

```markdown
## Resume Context
- Before implementation: <docs path>#<heading>
  — approved constraints and rationale.
- Before validation: <KB locator>
  — observed limitation, scope/version, and remaining uncertainty.
- Repository: <confirmed code location>.
- Dependency: <task path> — consumes its verified compatibility report.
```

Use real sources only; omit inapplicable entries. Retain consequential constraints
and the next action in the task itself so the human can supervise it. Verify
pointers and consult required sources before dependent work; an inaccessible
required source is a specific readiness gap, not permission to guess. Conditional
references wait until relevant. Reconcile material conflicts with current evidence.

## Resume, execute, checkpoint, and close

### Coordinated handoff and closeout

In project-task context, "hand this off to a fresh session", "prepare/delegate
the next tasks to another agent", and "we're done; close this task" request a
coordinated persistence review. No slash commands or special word "full" are
required. Read [Handoff and closeout](references/handoff.md): evaluate KB capture,
docs integration, and operational lessons through their owning skills, verify
supporting material, then save task state/context and index navigation. Each
review may correctly produce no change. Respect a narrower "task only" request.

This does not spawn agents or approve implementation/publication. Routine status
updates and ordinary execution bookkeeping do not trigger the cross-surface review.

### Pause for a fresh session

Treat cues such as "let's pause", "continue in a fresh session", or "pick this
up next time" as a request to save a **fresh-session continuation handoff** when
the conversation concerns unfinished project work. If a task already exists,
update that task in place; otherwise create one in the configured task surface
when authorized. Preserve the goal, decisions and rationale already settled,
current progress and verification, unresolved questions, blockers, relevant
context pointers, and an unambiguous next permitted action. Make the brief
self-contained without the present chat. Update `INDEX.md` accordingly and
report the exact task path plus a short resume cue.

An explicit fresh-session handoff also uses the coordinated workflow above;
a simple progress checkpoint need not. Save consequential decisions at meaningful
checkpoints while context is available, rather than relying on a final transcript
reconstruction after context has been lost.

A conversational pause does **not** imply implementation approval, execution
preflight, or that the work is intentionally deferred. Keep `Status: Active`
when work simply continues in a later session; use `On Hold` only when the human
intentionally suspends the work pending a meaningful re-entry condition. Do not
start additional investigation or implementation merely to finish the handoff,
and do not silently create a task when the user is merely ending casual chat.
Honor configured locations and narrower write permissions.

When asked to **resume or execute a named persisted task**, load this skill
and the task, identify its configured project/task surface, read applicable
`AGENTS.md` guidance, and inspect the relevant current code, docs, and evidence.
You need not load this skill merely to answer a question about a file's contents.
The task is execution intent and memory, **not proof that code or the environment
still matches it**.

1. **Check authority and readiness.** Read the status, current direction,
   explicit permission/gates, blockers, next action, dependencies, and success
   bar and deliverables. Read the task's required resume context before dependent
   work. Resolve contradictions before acting. Distinguish preparing a handoff
   from permission to implement. Do not treat an index entry as authorization.
2. **Act within the approved scope.** Perform only the next permitted work through
   the relevant implementation workflow. If current evidence contradicts the
   plan or creates a material human-owned decision, stop and surface it rather
   than silently redesigning, spending, deploying, or escalating access.
3. **Maintain execution memory automatically when authorized.** At meaningful
   checkpoints, blocked transitions, handoffs, and completion, update the same
   task's current state, decisions affected, blockers, verification actually
   performed, material deviations, remaining uncertainty, and next action;
   refresh its index entry. Do not record every command or trivial progress.
   If a stricter rule withholds task-write permission, report what needs an
   update instead of editing.
4. **Close honestly.** Close when the required outcome and verification are
   complete, or the human explicitly cancels/supersedes the remaining work.
   For an explicit closeout request, complete the coordinated review first.
   Record the result and closure reason, distinguish tested from untested,
   and identify residual follow-up. If required work remains, leave the task
   open or, when authorized, make a distinct follow-up task. Remove only the
   closed task's index entry; do not archive, delete, or relocate its file.
5. **Report succinctly.** State what changed, verification and gaps, any
   consequential plan deviation or human action, current task status, and
   exact task/index paths updated. A failed or partial execution still needs
   an accurate checkpoint when writes are allowed.

"Execute this task" ordinarily includes the bookkeeping above; the human
should not need to separately ask to update, close, or re-index it. This
does not override narrower repository write rules or permission gates.

### Execution gates and operational preflight

Read legacy `Execution Gate` fields conservatively. Honor prohibitions and
human unblocks; `Waiting for Dependency` needs evidence before proceeding;
`Ready for Main-Agent Execution` permits only its stated action;
`Ready for Delegated Execution` indicates suitability, not permission to
spawn subagents; `Not Applicable (Closed)` permits none. Missing or old
metadata is not implicit authorization. Preserve material legacy gates when
touching older files; do not mass-migrate them.

Apply operational preflight **relative to the next action** when preparing
immediate execution or performing risky activity, including investigations
that access production, sensitive data, or paid services. Check what matters:
approval and access, private-data handling, cost/quota, external dependencies,
interfaces/schemas, production state, destructive effects, backups/rollback,
retries, observability, and a safe verification path. Do not demand later-phase
preflight just to checkpoint an idea.

For a blocker, state what is blocked, why, what will clear it, and the evidence
of clearance if non-obvious. Distinguish human unblock from ordinary dependency.
Never poll indefinitely, work around a human gate, or mark READY for a blocked
next action. A safe investigation may proceed while implementation is blocked
if its own permission and prerequisites are satisfied.

Before claiming execution readiness or closure, check consistency among
status, priority, direction, blockers, permission, next action, and success
bar/verification. A `Closed` task with required unperformed work, `Blockers:
None` alongside an actual blocker, or an "approved" decision contradicted by
the plan is not a valid handoff.

Never store secrets, keys, passwords, tokens, or recovery codes in task files.
Minimize sensitive or restricted data; link approved protected sources instead.

## Related tasks, knowledge, and maintenance

Prefer one file per coherent outcome, even with several steps. Use the
creation-month/workstream related-effort group only when its children have
independently continuable outcomes. `overview.md` owns common intent,
dependencies, decisions, and suggested entry point; children own their own
state and verification. Numeric prefixes express sequence, not readiness.
Keep the index navigable without duplicating every child dashboard.

Before creating another task, inspect the index and targeted relevant existing
tasks. Reuse or update an existing task when the outcome is the same; link
related-but-distinct work and dependencies instead of creating competing plans.
Do not combine genuinely independently continuable outcomes just to reduce
file count.

Route settled project knowledge to `project-docs` when authorized; a task may
record that docs sync remains required without silently writing docs. KB capture
requires a capture request or the explicit coordinated handoff/closeout intent
above; ordinary task maintenance does not authorize it. A broader sweep to identify
duplicate, stale, abandoned, or inconsistent tasks requires a specific request; ordinary writes
only repair related entries and direct conflicts.

**Final test:** A human can supervise the current work, a fresh agent can
continue the next *permitted* action without the old conversation, and the
index points to the actual unfinished tasks without moving or duplicating
their authoritative files.
