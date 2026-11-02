# Task: Analyze and implement autonomous task lifecycle for project-tasks

**File:** `tasks/2026-11/project-tasks-autonomy/2026-11-02__autonomous-task-lifecycle.md`
**Created:** 2026-11-02
**Last Updated:** 2026-11-02
**Priority:** Now
**Status:** Active — original scope needs clarification

**Goal:** Make `project-tasks` operate as the human↔agent bridge: the agent manages the full task lifecycle (create, update, checkpoint, prioritize, close, index) autonomously and smoothly, while the human supervises without needing content-level judgment.
**Why:** The human is a new joiner who cannot judge which tasks to open/close/prioritize — the agent holds the context (dumped into KB records). Gating lifecycle decisions on the human produces stale or absent tasks; the pilot on 2026-11-02 showed state living in the conversation until a wrap-up request, instead of in task files.
**Deliverables:** (a) analysis of the current skill against the feedback below; (b) a proportionate design for autonomous lifecycle + reporting contract; (c) implementation where permitted — skill text changes need explicit human approval under the steward contract, so expect a proposal artifact plus any ungated config edits.
**Success Bar:** A fresh session can resume any workstream by natural reference ("that eaip thing on the infinity ticket"), the agent maintains tasks from work-start (not wrap-up), closes/reprioritizes autonomously with visible reporting, and the human never has to answer "should we open/close this?" to keep the system working.

**Current State:** The merged `project-tasks` skill now supports autonomous task
creation, updates, reprioritization, and verified-Completed closure during a
human-triggered maintenance pass, subject to local gates. See commits `9edb41c`,
`e1ed3be`, and `5d8aa38`, merged in `22a5f01`. This is narrower than the original
standing-autonomy ideas below; it does not authorize task maintenance throughout
ordinary conversation. The original success bar has not been verified in a fresh
session. Treat the original ideas as historical, not as an approved implementation plan.

**Next Action:** Clarify whether any of the original broader outcome remains wanted
or whether this task should be closed as superseded. Do not delegate the original
proposal or infer approval for standing autonomous task writes. Publication and
workspace adoption of the merged skill require separate verification.

## Human feedback (verbatim intent)

- "We have the semantic folders... multiple and full loads of things that I personally don't quite understand. Asking me to open and close is also difficult — I'm not familiar. You have the context and knowledge."
- "My judgement to open and close tasks will not be as strong as yours."
- Desired interaction: "hey we have this new task please create a task" or "hey about that eaip migration we doing on the infinity ticket" — natural-language task resolution, agent does the rest.
- Wants tasks used "smoothly, autonomously, independently, as if it's literally the bridge between you and me."

## Agent pilot feedback (from the 2026-11-02 deployment session)

What worked: task contract first-screen (Goal/Status/Next Action/Blockers made resume trivial); stable paths; permission-boundary section; INDEX as scan target.

What didn't:

1. **Timing, not autonomy, was the real friction.** Tasks were created at wrap-up, so the day's state lived in conversation. If tasks exist from work-start, "maintain progress automatically" keeps them continuously accurate. Earlier creation = more value → argues for autonomy.
2. **The approval gate forces a per-session trigger.** Work happened for hours before "update/create tasks, sync docs, capture kb" authorized any writes.
3. **Closure/priority gates fail differently than designed.** My initial recommendation kept Cancelled/Superseded closures and Now/Next/Later changes human-gated — but the human's feedback shows gating on them doesn't work when they lack context to judge. Design must resolve this: the likely answer is *autonomous but loudly reported and reversible* (files stay at stable paths, reopening restores index entry — reversal is already cheap) rather than *ask first*.
4. Autonomy matrix that mostly held: progress updates/INDEX/status flips/new-task creation = safe autonomous; deploy and approval actions must never be task-authorized (circular permission — "priority/status is not execution permission" stays).

## Ideas to evaluate

- **Standing authorization line** in workspace `AGENTS.md` Behavior: pre-authorize task writes within active work scope, agent reports each write; removes the per-session trigger.
- **Supervision model shift:** approval-before → review-after. Human supervises via a per-write report line + periodic digest, not by judging each operation. Reversibility of closes/moves is the safety property.
- **Write-report contract:** every task mutation surfaces a one-line changelog (created/updated/closed X — reason), so awareness doesn't require judgment.
- **Closure policy:** Completed-against-verified-success-bar autonomous; Cancelled/Superseded also autonomous *but* prominently reported (human can veto/reopen). Priority (Now/Next/Later) agent-managed with visible reporting — human redirects by saying so, not by gate.
- **Early creation norm:** create the task when work begins (or on first meaningful checkpoint), not at handoff. Possibly: agent proposes "track this as a task?" only for ambiguous small asks.
- **Natural-language resolution:** strengthen the index → targeted-search → task path so vague references resolve reliably; ask only when materially different candidates remain.
- **Human-attention field or equivalent:** surface genuinely human-owned items (approvals to chase, decisions only the human can make) in a way the human can scan without understanding internals.

## Boundaries for the delegated agent

- `skills/` is hand-edited production source — propose skill changes; do not rewrite autonomously. Present a diff/proposal for human approval per the steward contract.
- Ungated surfaces (e.g. a workspace AGENTS.md behavior line, prompts/, docs/) may be implemented directly if the human approves the design.
- Do not weaken the core invariants: tasks are execution memory, not proof of state; status/priority ≠ execution permission; no secrets in task files; stable paths; INDEX as derived navigation.
- Scope is the task lifecycle and its human interface — not KB, docs, or subagent spawning policy (link where relevant).

## Resume Context

- Skill under analysis: `skills/project-tasks/SKILL.md` (+ `references/handoff.md`, `references/routing.md`); published copy at `%APPDATA%\devin\skills\project-tasks\`.
- Steward contract: `AGENTS.md` — roles, skill-edit gate, sync rules.
- Workspace-side gate being redesigned: `ching/repos/AGENTS.md` Behavior — "CRUD on project docs, project tasks and knowledge base is approval gated."
- Pilot evidence: `repos/.work-context/projects/propensity/tasks/` — 3 tasks created at wrap-up (2026-11-02, edsp-prod workstream), INDEX maintained; `.work-context/knowledge-base/records/2026-11/propensity/2026-11-02--onprem-edsp-deployment-status.md` shows mid-session staleness the tasks would have prevented.
