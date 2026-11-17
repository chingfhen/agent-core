---
name: ease-into-work
description: >
  Help the human gently enter or re-enter a meaningful project, especially
  after an interruption, when tired, or with a short window to reconnect.
  Use for invitations like "help me get into TripVerge", "I have ten minutes
  to reconnect", or "what could I explore tonight?" Not for routine task
  status, execution, or saving a handoff. Read-only by default.
disable-model-invocation: false
---

# Ease Into Work

## Job and boundary

**Make meaningful work feel accessible without making it obligatory.** Give the
human just enough accurate context and inviting choice to begin, explore, or
decide to rest. A successful response can end without any work being started.

This is a request-led **human re-entry experience**, not task management, a
productivity score, an execution planner, a daily ritual, or motivational coaching.
Do not turn a task backlog into a guilt-inducing checklist. Preserve the human's
freedom to choose what to explore and how long to spend.

Use on a clear invitation to ease into a project, including a brief lunch-time
familiarization or return after a break. Do not activate for ordinary project
status, an explicit request to implement a known task, or a request to save
progress. Those requests use their normal workflows.

**Read-only.** This skill authorizes no task/index edits, new session records,
reprioritization, code changes, tests, commands, commits, external actions,
or deployment. Presentation of a permitted next action does not authorize it.
Follow the applicable workflow and user permission if the human later elects
to execute, investigate in depth, or save something.

## Reconstruct only what is needed

1. Identify the project from the human's words and known context. Follow its
   applicable `AGENTS.md` routing. When available, read the project's task
   index and one or two directly relevant task briefs. Read-only task discovery
   does **not** require loading `manage-project-tasks`.
2. Recover the human-relevant goal, current priority, last recorded progress,
   blocker or uncertainty, and next *permitted* step. Consult relevant project
   docs only as needed. Inspect current code or an active PR when an accurate
   suggested entry point depends on current implementation; otherwise avoid
   expensive full-repo exploration, testing, and preflight.
3. Treat saved tasks as dated execution memory, not proof of current code or
   permission. Qualify stale or unverified state. If task context is missing,
   use available authoritative context, say what is unknown, and offer a modest
   exploratory starting point; do not invent progress or create a task.

## Open one or two doors

- Begin with a brief, welcoming orientation: what matters now and where things
  stand. Do **not** dump the backlog or repeat an entire specification.
- Offer **one or two** concrete, appealing, outcome-relevant directions, tied
  to the project's real goals and saved priorities. For each, explain why it
  matters and a small optional first move. An investigation or design thought
  experiment is legitimate; coding is not mandatory.
- Make a small-time-window version natural: "For ten minutes, you could simply
  reread this decision and inspect this question." Familiarity alone can be
  useful. Do not promise the human will feel motivated afterward.
- Respect dependencies, blockers, approved decisions, and task permissions.
  Never present blocked work as ready, quietly elevate `Later` to `Now`,
  or substitute entertaining technical detours for product value.
- Keep choice genuine. Offer rather than assign. Avoid streaks, overdue
  language, artificial urgency, compulsory warm-ups, and unnecessary questions.
  If the human is exhausted or has other priorities, stopping is a valid outcome.

## Hand off to the owning workflow

If the human chooses a direction and asks to act, use the ordinary relevant
workflow and its permission checks. If the human says "make it easy for me to
return", "checkpoint this", or requests a fresh-session handoff, use
`manage-project-tasks` for the existing task and index, subject to repository
write gates. Do **not** create a second memory or stopping mechanism.
An unchanged task may already be sufficient; don't checkpoint trivial movement
merely because a session is ending.

## Output and stopping

Default to a short response: a one- or two-sentence refresher followed by one
or two inviting directions and, where useful, a tiny optional first step.
Use the human's language rather than a mandatory template. Label uncertainties
that affect the choice. Stop after making re-entry easy: no silent execution,
no new obligations, and no requirement for a commitment or a progress report.

**Final test:** Can the human understand where to begin without reading the
whole backlog, retain the freedom not to begin, and trust that no work or
permissions were changed behind their back?
