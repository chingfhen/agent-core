# Tasks — portable execution memory

Read after the Agent Builder root for requested task maintenance or execution of saved work. Read-only discovery, status questions and use of task context do not require this reference. Apply root permissions, project resolution, coordination, guidance and reporting rules; this module owns task content, task/index consistency and execution continuity, not the implementation method.

## Decide whether a task belongs

Create a task when future continuation would materially benefit from a durable brief. It can be an idea, investigation, design discussion, implementation, validation or approval, including non-coding work. Do not create tasks for short-lived ordinary work or a new session alone.

Consult the confirmed task index and targeted existing tasks before creating; reuse the same task for the same outcome. One file per coherent independently continuable outcome, not per step. Split when deliverables can be continued or verified independently; link prerequisites and related efforts. A shared effort overview is optional only when common intent, decisions, dependencies or entry point would otherwise be repeated. Children own their own state and acceptance; numeric prefixes convey order, not readiness.

Use the configured task surface and the root's stable creation-month/workstream naming convention. Reuse meaningful workstream labels across months. Never move a task because its priority or status changes, and never archive/delete a closed task just to tidy the index. Maintain legacy files and indexes in place.

## Index and lifecycle

The single task index (index.md for new roots, existing INDEX.md for legacy) is a navigation view of **all known unfinished work only**, derived from authoritative task files. Group by Now / Next / Later. Include a concise linked name, workstream, status and next meaningful action or re-entry/blocking condition. Keep recognizable aliases/ticket identifiers when useful and appropriate. No duplicate entry for the same outcome; list independently continuable children where needed. Closed files leave the index, remain at stable paths and are restored to the index when reopened. No separate historical/monthly index, backlog folder or dashboard.

Update affected index entries as part of authorized creation, material state/priority/next-action changes, closure and reopening. Preserve unrelated entries. If missing on an authorized write, initialize from a bounded inventory of that confirmed task surface, including legacy folders; disclose incomplete coverage rather than presenting it as complete. On index failure preserve the safe authoritative task write and report it out of sync. A broader hygiene sweep needs an explicit request.

Keep three concepts independent:

- **Priority:** Now = current focus; Next = intended next-up; Later = deferred but worth retaining.
- **Status:** Active = progress intended; Blocked = next meaningful action prevented by a dependency or decision; On Hold = deliberately paused; Closed = work ended. A normal break between sessions does not imply On Hold. Blocked/On Hold need a clearing or re-entry condition.
- **Permission:** what action is actually authorized. Priority/status are not permission or proof of readiness.

Select routine priorities autonomously during authorized maintenance using established human intent, meaningful dependencies, value and actual progress; favor valuable unblocked permitted next actions over starting more work. Do not redefine strategy or silently displace explicit human priorities. Closed has a reason: Completed (required outcomes and verification established), Cancelled or Superseded (clear human intent). Record real outcomes and residual work; never imply cancelled work was implemented. Reopen when continuation is authorized and the outcome is genuinely unfinished again.

## Author a useful brief

Choose depth autonomously from the work's uncertainty, consequences, continuity needs and intended executor. Honor an explicit human mode. Standard is the fallback when no other depth fits better, not a mandatory default that overrides judgment. Keep the named modes available without a compulsory mode announcement; explain a depth choice only if material to supervision.

- **Brief:** goal/why, known or unresolved state, authority boundary and next meaningful action; useful for early ideas or lightweight work.
- **Standard:** fresh-session working brief including success bar, current direction or uncertainty, constraints, deliverables, blockers, verification requirements and next action.
- **Detailed:** high-fidelity planner-to-executor handoff when work warrants it; include consequential decisions and rationale, grounded interfaces/files/dependencies, phases/checkpoints, acceptance tests/outcomes, edge cases, recovery, stop conditions and executor discretion. Do not require the executor to rediscover resolved choices. Do not micromanage routine details or invent implementation facts.

A normal new task begins with a human-scannable summary:

    # Task: [Clear outcome]

    **File:** tasks/YYYY-MM/<workstream>/YYYY-MM-DD--description.md
    **Created:** YYYY-MM-DD
    **Last Updated:** YYYY-MM-DD
    **Priority:** Now | Next | Later
    **Status:** Active | Blocked | On Hold | Closed

    **Goal:** [...]
    **Deliverables:** [...]
    **Success Bar:** [...]
    **Chosen Direction:** [selected | not yet selected]
    **Current State:** [...]
    **Next Action:** [action and whether it is permitted]
    **Blockers:** [none | blocker, impact and clearing condition]

    ## Permission Boundary
    ## Resume Context

Adapt this outline to the work; combine goal/why, deliverables and acceptance for small tasks when clear. Add only useful sections (verification, human attention, dependencies, decisions, implementation phases, discretion, recovery). Essential state, constraints and permission remain visible even in Brief. A goal is the intended outcome, deliverables are reviewable outputs, acceptance establishes satisfaction; none requires code.

Record each material choice as accepted/locked, executor-owned routine detail, or unresolved with its owner and permitted investigation/decision. Keep one current direction, distinguishing actual evidence from proposed changes and assumptions. A substantial plan needing human approval must be presented and approved before implementation; saving it does not count. Preserve already accepted success conditions; if consequential goal uncertainty blocks a substantial implementation plan, offer define-success only with human acceptance. Use tech-design-options for requested consequential technical choices, not ordinary planning.

### Resume context

On creation, substantial handoff or resumption, consult relevant canonical docs and selectively recall KB findings when material. Link rather than copy project truth. Retain exact usable paths/headings or remote locators, what they provide, and when to read them. Identify accepted design, observed evidence, procedure or unresolved investigation; include confirmed working system/repository and prerequisite tasks' specific outputs when relevant. Distinguish required-before-next-action from conditional later references. Verify links; an inaccessible required source is a readiness gap, not permission to guess. Preserve essential consequences in the task itself so it remains supervisable.

## Implementation delegation contract

During planning, use delegate-implementation if the human explicitly requests it or when preparing/substantially revising a substantial implementation-ready task with plausibly separable work. It owns strategy, harness/model/effort, coordination and fallback. A small indivisible task needs no specialist pass; early unsettled design should defer. Record the decision in the same task when authorized, not a registry:

- Main agent: concise decisive reason.
- Defer: missing prerequisite or human-owned decision, and next decision owner.
- Delegate: rationale and expected benefit/resource tradeoff; intended harness, workers and bounded deliverables, model/effort verified vs proposed/unknown, interfaces/sources, parent-owned architecture/integration, read/write boundaries and isolation, coordination order, verification, receipt requirements, limits and fallback/stop conditions; actual human approval state.

A surfaced specific worker plan accepted by the human (including within task plan approval) counts once; merely writing it, silence or broad agent permission does not. No extra ceremonial approval if already specific. Other costs, credentials, Git actions and external effects retain independent gates.

At execution do NOT invoke delegate-implementation to reconsider strategy. Verify the actual approved plan, harness, model/effort controls, permissions, tools, quotas, source state/interfaces and safe isolation before launch. Follow only approved assignments and fallback; if unavailable or unsafe, stop for replanning unless an expressly approved fallback applies. No recorded worker plan means normal main-agent execution, not opportunistic worker invention. Inspect actual artifacts and integrated behavior, not worker assertions. Preserve a compact planned-versus-actual receipt: actual worker/model/effort/harness if known, child-session/artifact links, checks, usage or unknown, deviations/fallback and next action. Report it without writing if task edits are barred.

## Maintenance, resume and execution

For a general tasks maintenance cue, review directly related work and saved tasks; autonomously choose relevant creations, updates, checkpoints, reprioritization and verified Completed closures, or no change. The root selects additional justified modules under the authorized pass unless restricted. Do not ask the human to name each file; ask only about material ambiguity, consequential decisions or permission. Do not run unrelated hygiene sweeps. A routine checkpoint is not a new handoff. Observe local opt-in gates.

For saved-task execution, load root and this reference, actual task and required sources, applicable guidance and evidence. Resolve working location/system independently of task-folder location. Read status, chosen direction, next action, blockers, permissions, dependencies, deliverables and success bar. Reconcile old plans or imperative checklists against current evidence; do not repeat completed work or privilege the latest timestamp alone. Explicit status questions remain read-only. An instruction to execute a task authorizes only work actually permitted by the human and gates, not all future phases.

Honor legacy Execution Gate fields conservatively: Waiting for Dependency needs evidence; Ready for Main-Agent Execution permits only stated action; Ready for Delegated Execution describes suitability, not worker approval; Not Applicable (Closed) permits none. Missing metadata is not authority. Preserve meaningful legacy gates.

Apply operational preflight relative to the **next action**, not all future steps. Check relevant approvals, access, private-data boundaries, cost/quotas, current dependencies and interfaces, production state, destructive effects, recovery, retries and a safe verification path. Do not demand deployment checks to save an idea. For blockers state what is blocked, why, who/what clears it and evidence if non-obvious. A permitted safe investigation may proceed while implementation is blocked. Never bypass human gates, poll indefinitely or assert readiness without prerequisites.

Perform only permitted work through the appropriate execution skills. If actual evidence contradicts the plan, resolve routine details within discretion or stop at material human-owned choices. Execution ordinarily includes that task's state/index bookkeeping unless a stricter gate requires separate permission. No implicit unrelated edits, cross-resource review, deployment, spending or workers.

## Checkpoint, handoff and close

At meaningful checkpoints, blocked transitions, fresh-session handoffs and completion, when authorized:
- Update current state, decisions, blockers, actual results/verification, deviations, remaining uncertainty and next permitted action in the same task.
- Reconcile the whole affected task (header, body, checklists, commands, context and index). Replace obsolete actions or label useful historical instructions non-actionable. An appended newer outcome does not invalidate a stale imperative. Preserve important rationale, failed approaches and outstanding acceptance criteria rather than appending a session diary.
- Update affected index entries and verify directly relevant consistency. If task writes are barred, provide the actionable update in conversation instead.

Treat an explicit pause/fresh-session handoff of unfinished project work as a context maintenance cue, not an intentional On Hold state or execution authorization. Use root coordination to preserve relevant settled understanding, evidence and justified lessons first, then task pointers and state. Choose only justified modules; respect task-only limits. Do not execute later investigations to prepare the handoff, and do not create tasks from casual conversational endings. Give a short resume cue using exact saved task location or recognizable workstream.

Close as Completed only when required deliverables and verification are established. Explicit closeout uses root coordinated review before closure; routine verified completion bookkeeping need not. If required work or persistence remains pending, keep it open with clearing condition or create a distinct follow-up when authorized; human may explicitly waive/cancel remaining scope. Record closure reason, tested versus untested, residual work and actual outcome; remove only the closed index entry, retain task file. Partial writes remain recoverable; do not claim complete closure on failed required work.

## Verification and reporting

For routine updates read back changed state and index entry. For substantial plans/handoffs/closure, verify required locators, deliverables/acceptance evidence, and consistency of priority/status/direction/permissions/blockers/next action throughout the affected file and index. Can a fresh agent identify what to produce, what to read, what is uncertain and what it may do next without the chat? This content check is not a fresh-agent trial. Match verification to the type of work (policy, approval, artifact, observed behavior, code or runtime as appropriate). No mandatory engineering tests for non-coding tasks.

Report meaningful changes and reasons, exact resolved task/index paths, actual checks, any approval/access gaps or deviations, and next action/closure. Do not report a proposed edit as performed. Preserve useful no-change outcomes without ceremony. Never store secrets, credentials or restricted data in task files; link approved protected sources.

## Research-informed techniques

The rules above operationalize selected practices rather than requiring a literature review on each invocation:
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents): durable progress and explicit completion evidence across context windows. Use the existing task as the continuation artifact, not an extra progress ledger; do not confuse a saved plan with passing checks.
- [The Kanban Guide](https://kanbanguides.org/the-kanban-guide/2025.5/): visible unfinished work, explicit transition policies and finishing/clearing work before indiscriminately starting more. Adopt lightweight priority and blocker semantics, not compulsory WIP limits, metrics or forecasting.

These inform design, not proof of behavior on our harnesses. Reassess material changing facts or observed failures; test representative fresh-session scenarios before replacement.
