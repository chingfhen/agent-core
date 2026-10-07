---
name: project-tasks
description: Maintains shared human-agent continuation briefs in the active project's configured task surface (conventionally tasks/, including tasks/backlog/ for deferred work) so unfinished discussion, planning, investigation, implementation, or validation can continue without the prior conversation. Load before creating, editing, moving, deleting, or managing task files; not needed merely to read an explicitly identified task file. Rewrites tasks toward current truth while preserving permission boundaries, consequential decisions, blockers, verification state, and the next permitted action.
disable-model-invocation: false
---

# Project Tasks

## Purpose and Admission

Use a task when unfinished work needs to remain understandable and continuable across sessions, agents, harnesses, or machines.

Ask:

> Does future continuation of this work need a durable brief?

A valid continuation may be discussion, planning, investigation, implementation, validation, a human action, or a bounded delegated activity. A task does not need to be ready for implementation to be useful.

Each task is a shared control surface for:

- a human to understand the goal, rationale, direction, current state, uncertainty, consequential decisions, risk, and required attention;
- a fresh executor to take the next permitted action without the old conversation.

A task is not durable project documentation, a transcript, a session diary, or an exhaustive implementation manual. Rewrite it toward current usefulness. Preserve history only when it prevents a repeated mistake or explains a constraint that still matters.

Saving, checkpointing, updating, handing off, or resuming a task does not by itself authorize implementation or broaden any existing permission. Maintaining a task records work; it does not perform the work described by it.

## Surface Ownership

This skill writes only to the task surface configured for the active project.

Machine-local registry:

```text
~/.agent-core/projects.toml
```

Example:

```toml
[projects.smart-search]
description = "OCBC Smart Search"
root = "/home/cdsw/smart-search-workspace"
docs = "/home/cdsw/smart-search-workspace/docs"
tasks = "/home/cdsw/smart-search-workspace/tasks"
knowledge_base = "/home/cdsw/smart-search-workspace/knowledge-base"
```

For this skill, `root` and `tasks` are the relevant fields.

Before creating, editing, moving, deleting, listing, or otherwise managing task files:

1. Read `~/.agent-core/projects.toml` when it exists.
2. Identify the project whose configured `root` contains the current working directory. If several match, use the most specific root.
3. Treat that project's exact `tasks` value as the writable task-surface root.
4. Perform task CRUD only inside that configured surface. Do not choose or create a nearby `tasks/` directory because it appears to match the repository.
5. If no active project or task surface can be resolved, report the missing configuration instead of guessing.
6. Read the registry for normal task work, but modify it only when the human explicitly asks to register, remove, or change a project.
7. After a mutation, report every exact resolved filesystem path changed.

Paths such as `tasks/foo.md` and `tasks/backlog/foo.md` are portable logical paths. If the configured surface is `/home/cdsw/smart-search-workspace/tasks`, then logical `tasks/foo.md` resolves to `/home/cdsw/smart-search-workspace/tasks/foo.md`. Record the logical path in the task when useful; report the physical path after mutation.

The task surface is the only normal writable surface owned by this skill. Reference docs, source material, code, evidence, or archives as needed, but use their owning workflows for mutations. Any task archive must be an established, authorized location inside the configured task surface; do not invent an external archive.

## What a Task Owns

- `project-tasks` owns unfinished-work state, the authoritative current direction, consequential uncertainty, blockers, verification state, and the next permitted action.
- `planning` owns shaping and resolving substantial work before approval when plan review is requested.
- Implementation and runtime verification belong to the relevant execution workflow. A task records their state and evidence.
- `project-docs` owns settled project understanding and durable operating guidance.
- `tasks/backlog/` holds deferred work that should survive but has no active near-term continuation.
- Code, tests, schemas, configuration, and observed runtime behavior remain authorities for their respective implementation claims.
- Conversation may hold exploration in progress until that work needs continuity.

One claim should have one primary authority. A task may link to that authority and state the consequence needed for continuation rather than copy a competing explanation.

## Universal Task Contract

The first screen should normally make these points clear:

- logical file path and creation/update dates;
- priority and lifecycle status;
- goal and why it matters;
- success bar;
- chosen direction, or explicitly that no direction has been selected;
- current state;
- concrete next action, including what kind of activity is permitted;
- blockers, their impact, and what clears them;
- material human attention when needed.

Preserve verification requirements and durable-knowledge handling somewhere appropriate, but do not turn every useful field into mandatory template filling.

### Default Shape

New standalone tasks normally use:

```text
tasks/YYYY-MM-DD__kebab-case-name-bookmark.md
```

The filename date is the immutable creation date. Follow an established task-surface convention when one exists, and do not mass-rename older tasks.

Use this concise shape when it fits:

```markdown
# Task: [Clear short name]

**File:** `tasks/YYYY-MM-DD__kebab-case-name-bookmark.md`
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Priority:** [Now | Next | Later]
**Status:** [Active | Blocked | On Hold | Closed]

**Goal:** [...]
**Why:** [...]
**Success Bar:** [...]
**Chosen Direction:** [Selected direction | Not selected]
**Current State:** [...]
**Next Action:** [...]
**Blockers:** [None | obstacle, impact, and clearing condition]
**Human Attention:** [...]
```

`Why` may be combined with `Goal`. `Human Attention` may be omitted when nothing requires it. Add fields such as `Permission Boundary`, `Verification`, `Docs Sync`, `Target Docs`, or `Relevant Code` only when they improve control or continuation.

Use:

- `Priority: Now` for active priority, `Next` for intended next-up work, and `Later` for preserved work that is not near-term;
- `Status: Active` for open work intended to progress, `Blocked` when the next permitted meaningful action cannot proceed, `On Hold` for an intentional pause, and `Closed` only when required work has ended.

An exploratory task may say:

```text
Chosen Direction: Not selected
Next Action: Continue comparing the two architectures. Implementation is not approved. Resolve the ownership boundary before selecting a design.
```

Do not invent a decision to make the brief appear complete.

### Human Skim Test

A reader should be able to answer:

1. What outcome is being pursued, and why?
2. What direction has been selected, if any?
3. What is currently true?
4. What activity is permitted next?
5. What blocks it, and what clears the blocker?
6. How will success be recognized?
7. What deserves human attention?

### Information Selection

Surface details that affect approval, direction, product or failure behavior, responsibility boundaries, security, privacy, data integrity, cost, recovery, maintainability, or confidence in the plan.

Preserve below the first screen only what is difficult to reconstruct, execution-critical, needed to understand a non-obvious constraint, or likely to prevent a repeated mistake.

Compress routine code navigation, obvious sequencing, ordinary commands, reconstructible test mechanics, duplicate evidence, stale hypotheses, and abandoned plans whose lessons are already captured. Assume future executors are technically strong.

Use direct language. Explain behavior and consequences before file edits or code symbols. Avoid vague instructions such as `investigate further`, `wire up`, or `harden semantics`.

## Continuation and Permission

The task must distinguish among these requests:

- save or checkpoint the task;
- update the task;
- prepare it for a fresh session;
- prepare it for immediate execution;
- resume the next permitted action;
- move it to backlog;
- close it.

A fresh-session handoff is not automatically an immediate execution handoff. Persisting a plan must not execute its investigations, test future credentials, or validate later environments merely to complete the brief.

Write `Next Action` so the allowed activity is unambiguous. When implementation, production access, spending, or another consequential action is not approved, say so directly. If permission is unclear, preserve the narrower interpretation and ask only when the next action actually requires clarification.

Keep delegation topology separate from operational readiness. Describing work as delegable does not grant permission to spawn subagents; follow the runtime's permission requirements.

### Existing Execution Gates

Read older tasks conservatively. If a task contains `Execution Gate` or equivalent permission metadata:

- honor an explicit prohibition or required human unblock;
- treat `Waiting for Dependency` as blocked until the named completion evidence exists;
- treat `Ready for Main-Agent Execution` as permission for the stated next action, not unrelated work;
- treat `Ready for Delegated Execution` as task-level suitability only; the runtime's separate permission requirements for subagents still apply;
- treat `Not Applicable (Closed)` as no execution permission;
- do not interpret missing newer metadata as authorization;
- do not remove or reinterpret a legacy gate during an unrelated update.

Do not mass-migrate historical tasks. Update a task's shape only when that task is otherwise authorized for modification.

## Decisions, Plans, and Uncertainty

The task should contain one authoritative current state, but it need not contain a selected solution before one exists.

For each material choice:

1. record it as an approved or otherwise authoritative decision;
2. classify it as executor-owned routine detail; or
3. preserve it as unresolved uncertainty with the discussion, investigation, or human decision needed next.

Do not hide product, architecture, security, privacy, migration, fallback, cost, or user-behavior choices inside phrases such as `either`, `optionally`, or `choose during implementation`.

When substantial planning still needs human review, use `planning`; do not turn the task into the planning conversation. When an approved or authoritative plan exists, preserve its meaningful outcomes, constraints, phase boundaries, and verification requirements. Omit low-level mechanics a strong executor can reconstruct.

Useful optional sections include:

- Decisions Locked
- Current Understanding
- Remaining Uncertainty
- Implementation Plan
- Boundaries / Stop Conditions
- Verification Contract
- Executor Guidance
- Human Attention
- Context Pointers
- Dangerous Evolution to Avoid
- Execution Topology

Use only sections that improve continuation or human control. A small task should remain small.

## Conditional Operational Readiness

Apply operational preflight when the user asks to prepare for immediate execution, when substantial execution is about to begin, or when the next permitted action itself can create meaningful risk. Do not require full later-phase preflight merely to checkpoint, discuss, or plan.

Judge the actual action, not its label. An investigation may require the same safeguards as implementation if it launches paid jobs, handles sensitive data, alters production, creates external resources, or has destructive effects.

Check as relevant:

- human approval, access, credentials, private data, provider configuration, billing, or quota;
- unresolved product, architecture, security, privacy, migration, fallback, cost, or deployment decisions;
- external dependencies, provider capabilities, hardware, environments, or completion evidence;
- required schemas, interfaces, identity mappings, current production state, or safe validation paths;
- destructive effects, backup, rollback, recovery, observability, ownership, retries, and paid-provider replay;
- verification sufficient for the permitted action.

Never put secrets, passwords, tokens, API keys, recovery codes, or private keys in a task. Minimize personal or confidential information and point to protected sources instead of copying them.

### Readiness Is Relative

Readiness applies to the next meaningful action, not the whole effort. A bounded investigation may be ready even though implementation is not. Record later-phase prerequisites without falsely blocking an earlier safe step or implying later work is approved.

A bounded investigation should state:

- the exact question;
- the evidence to inspect or produce;
- the decision or step that follows;
- any cost, access, production, privacy, or safety boundary.

For every blocker, record:

- the obstacle;
- its impact on the next action or later phase;
- the human action, dependency result, or external event that clears it;
- the evidence that shows it is cleared when that is not obvious.

Distinguish a human unblock from an ordinary dependency. Do not manufacture a human action for a dependency, poll indefinitely, or work around a blocker that only the human can clear.

When an explicit readiness verdict is needed, use plain language:

```text
Operational readiness: READY for [bounded next action]
Permission boundary: [...]
Later prerequisites: [...]
```

or:

```text
Operational readiness: BLOCKED
Blocking issue: [...]
Required human action or dependency result: [...]
Execution impact: [...]
```

Before declaring readiness, ensure the current state, selected direction, next action, blockers, permission boundary, plan, and verification contract agree. Correct contradictions such as:

- `Status: Closed` with required validation, approval, cleanup, or implementation pending;
- a ready verdict while a prerequisite blocks the stated next action;
- `Blockers: None` while another section identifies a blocker to that action;
- unresolved material alternatives without a permitted investigation or required decision before affected work;
- a human-owned next action described as ready for agent execution;
- a success bar unsupported by the verification contract;
- a chosen direction that conflicts with the plan;
- stale understanding presented as current truth.

Do not silently update a task in a way that leaves the human believing it is executable when it is not.

## Lifecycle Operations

All operations must preserve current truth, permission boundaries, dashboard/body consistency, task-surface ownership, and exact-path reporting.

### Save or Checkpoint

Capture the current goal, rationale, known alternatives or selected direction, uncertainty, current state, next permitted action, blockers, and success bar. Do not invent decisions or broaden permission. Done means the work can continue later, not that it is ready for implementation.

### Create or Persist a Plan

Create a dated task or related-task group. Preserve approved direction when one exists, but allow an honest exploratory state when it does not. Classify known prerequisites from available evidence without executing planned investigations or operational checks for future stages.

When the human requested plan review before persistence, use `planning` first and persist the resulting direction only after approval. An explicit instruction to persist an already approved plan does not require another ceremony.

### Update

Change `Last Updated` and rewrite affected sections toward current truth. Refresh decisions, uncertainty, blockers, permission boundaries, verification, durable-knowledge handling, and the next action. Remove superseded material rather than appending a session log.

### Prepare for a Fresh Session

Make the brief independent of the old conversation and make the next permitted activity explicit. Run operational preflight only to the degree required by that next activity. A discussion or planning handoff may remain unresolved; an execution handoff needs the stricter readiness review.

### Resume

Read the first screen, explicit gates, permission statements, blockers, and current state before acting. Take only the next permitted action. Preserve an implementation gate while conducting an approved investigation. If new evidence creates a material human-owned decision or contradicts the authorized direction, stop and surface that issue instead of silently redesigning the work.

### Move to Backlog

Use logical `tasks/backlog/` for intentionally deferred work that should survive without being active. Preserve a meaningful re-entry condition or next action. Moving to backlog does not approve future execution.

### Close

Close only when required work and required validation are complete or have been explicitly removed from scope. Record final state, honest verification, durable-doc handling, and residual follow-up. If required work remains, keep the task open or create an authorized active/backlog task for that work. Closed tasks are not automatically deleted.

## Related Task Groups

Use one file for one coherent outcome even when it has several steps. For several independently continuable tasks sharing an outcome, use:

```text
tasks/
    YYYY-MM-DD__related-effort/
        overview.md
        01-first-outcome.md
        02-next-outcome.md
```

The overview owns the shared outcome, constraints, links, dependency map, and recommended starting point. It does not duplicate each task's dashboard or progress.

Each task owns its outcome, inputs and outputs, decisions, state, blockers, next action, and verification. Make the first actionable task concrete. Later tasks may depend on earlier results; state what result will determine their unresolved choices rather than guessing or executing the investigation early.

Numeric prefixes indicate reading or execution order, not readiness or permission. Keep shared facts authoritative in the overview and task-specific facts in each task. Update only affected downstream assumptions when upstream results arrive. Do not migrate unrelated historical tasks.

## Durable Knowledge and Other Routing

- Route settled project understanding and durable operating behavior through `project-docs` when appropriate.
- Treat `Target Docs` as a routing hint, not a write contract.
- Keep current progress, unresolved choices, and remaining work in the task.
- Keep deferred work in the configured backlog.
- Reference source material, evidence, and archive content without silently mutating those surfaces.
- Do not automatically capture task work into a knowledge base.
- `tasks/INDEX.md`, if present, is optional navigation rather than an authoritative live dashboard.
- Do not place live task dashboards in agent-guidance files.

A durable-doc review can correctly conclude that no documentation change is needed. Record that conclusion only when useful; do not manufacture docs to mark a field complete.

## Final Test

A good task lets a fresh executor continue the next permitted activity without the old conversation and lets the human understand and supervise the work. It preserves current truth, rationale, consequential decisions, honest uncertainty, permission boundaries, actionable blockers, verification requirements, and a concrete next step without becoming a transcript or implementation manual.
