---
name: project-tasks
description: >
  Preserve unfinished project work as portable human-agent execution memory.
  Use to create, checkpoint, prepare, revise, resume, execute, or close a saved
  project task, including maintaining its progress and task index. Load before
  managing a configured task surface or continuing a persisted task; not for
  unrelated implementation or merely reading an explicitly named file. Resolve
  project task locations from applicable AGENTS.md, and preserve decisions,
  permission boundaries, verification state, and the next permitted action.
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

This skill owns the *memory of the work*, not the work's implementation method.
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
deployment, commits, pushes, or documentation/KB writes.

## Resolve the project and its task surface

Before creating, changing, indexing, or executing a persisted task, read the
applicable `AGENTS.md` project map and relevant repository guidance. Resolve the
**project from the requested work**, not just the current working directory.
One project can span multiple repositories and use one shared Tasks location;
different projects can share a workspace root.

- Use the mapped `Tasks` location. Resolve workspace-relative paths from the
  recorded workspace root, not the process working directory. A directly
  identified task file may be read without loading this skill merely to read it.
- When the project, mapping, root, or destination is missing, conflicting, or
  ambiguous, ask the human before managing or executing task state. When the
  destination is inaccessible, report that instead of substituting a path.
- A human can explicitly select a destination for one operation, without
  silently changing the saved map. Create a confirmed but absent directory only
  during an authorized write.
- No guessed `tasks/` fallback, `projects.toml`, directory-wide search for
  substitute task surfaces, or incidental workspace configuration updates.
  `workspace-setup` alone owns the managed workspace block and project/task
  mappings in `AGENTS.md`; this skill never edits that block.
- The configured task surface (including its `INDEX.md`) is this skill's normal
  writable scope. Other repositories, docs, code, raw evidence, archives, and
  guidance must be changed only under their own authorization/workflows.
  Report exact physical paths changed, as well as useful logical task paths.

Apply narrower repository rules even when this skill would ordinarily maintain
state automatically. In particular, a repository that makes task changes
explicitly opt-in does not gain broader write permission just because execution
started.

## Stable layout and discovery

For **new** tasks, use creation-month folders inside the configured task
surface:

```text
tasks/
  INDEX.md
  YYYY-MM/
    YYYY-MM-DD__descriptive-name.md
    YYYY-MM-DD__related-effort/
      overview.md
      01-first-outcome.md
      02-following-outcome.md
```

`tasks/` here is a *logical* location; its actual root comes from `AGENTS.md`.
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
  and meaningful next action or re-entry/blocking condition. Keep this scannable.
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

**File:** `tasks/YYYY-MM/YYYY-MM-DD__descriptive-name.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** Now | Next | Later
**Status:** Active | Blocked | On Hold | Closed

**Goal:** [...]
**Why:** [...]
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

## Resume, execute, checkpoint, and close

When asked to **resume or execute a named persisted task**, load this skill
and the task, identify its configured project/task surface, read applicable
`AGENTS.md` guidance, and inspect the relevant current code, docs, and evidence.
You need not load this skill merely to answer a question about a file's contents.
The task is execution intent and memory, **not proof that code or the environment
still matches it**.

1. **Check authority and readiness.** Read the status, current direction,
   explicit permission/gates, blockers, next action, dependencies, and success
   bar. Resolve contradictions before acting. Distinguish preparing a handoff
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
creation-month related-effort group shown above only when its children have
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
record that docs sync remains required without silently writing docs. Do not
automatically capture to a KB. A broader sweep to identify duplicate, stale,
abandoned, or inconsistent tasks requires a specific request; ordinary writes
only repair related entries and direct conflicts.

**Final test:** A human can supervise the current work, a fresh agent can
continue the next *permitted* action without the old conversation, and the
index points to the actual unfinished tasks without moving or duplicating
their authoritative files.
