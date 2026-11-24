# Task: Make implementation delegation a planning-owned decision

**File:** `tasks/2026-11/delegation/2026-11-24__make-delegation-a-planning-decision.md`
**Created:** 2026-11-24
**Last Updated:** 2026-11-24
**Priority:** Now
**Status:** Active

**Goal:** Replace Agent Core's execution-time discretionary delegation strategy with a research-informed planning decision, carried as an observable delegation or no-delegation contract in the Project Task.
**Why:** An executor focused on implementation may skip costly strategic delegation reasoning. The human wants decisions and worker contracts deliberately prepared upfront, without repeated research or expensive evaluation.
**Deliverables:** Rewrite the existing production delegation skill (or replace it safely); integrate its planning trigger and execution handoff into `manage-project-tasks`; reconcile the skills catalogue/manifest as needed; verify and commit the scoped canonical sources.
**Success Bar:** A planner, when asked or when preparing a substantial implementation-ready task, can choose delegation or no delegation and record the rationale. A delegation plan names worker responsibilities, intended harness, model and reasoning/effort where supported, context/interface boundaries, coordination, integration, checks, stop conditions, fallback, and any unresolved runtime facts. The executor follows the approved plan without a second economic/strategic delegation decision; it checks live prerequisites, reports deviations, and preserves human permissions. No new queue, worker registry, or mandatory benchmarking.
**Chosen Direction:** Planning-owned strategy; execution-owned operational validation and integration. Prefer cheaper workers where sensible, but permit same/higher-cost models or effort when justified. One plan may contain multiple independent workers; no worker is also a valid outcome. The planner chooses method and makes the decision visible; the human can adjust.
**Current State:** Approved implementation request. Existing `delegate-implementation` skill and `manage-project-tasks` were read; the old skill currently requires a cheaper worker and an execution-time strategic decision.
**Next Action:** Implement and commit the agreed skill and task-routing changes, reconcile the catalogue, reread changed files, then close this audit record and remove it from the active index.
**Blockers:** None for canonical source edits. Actual harness deployment, model availability, and behavior remain unverified.

## Decisions and scope

- Preserve one canonical delegation skill rather than introduce a default meta-planner subagent. Reuse the existing name if it avoids stale installed copies and duplicate active instructions.
- Human may explicitly trigger delegation planning; the task-planning agent may also invoke the skill when preparing substantial implementation-ready work. Avoid triggering during small edits, routine task maintenance, or merely executing a task.
- A Project Task's recorded delegation is a **strategy**, not automatically permission to launch workers. The human may approve it along with the explicitly surfaced implementation plan. A saved task by itself grants no new execution/spending/branch or security authority.
- The planner owns model/effort proposals, distinguishing verified harness features from intended selections and unknowns; cheaper is a preference, not a gate.
- Execution honors the recorded plan subject to environment, permission, isolation and scope safety. Use the documented fallback or stop on changed facts; do not silently replan.
- Prefer one worker initially where beneficial, with multiple workers allowed for genuinely independent scopes. Use short self-contained worker briefs, nonoverlapping writes, actual diff/test evidence, and parent-owned integration.
- Preserve or create audit visibility through the task's planned decision and concise outcome, linked session/commit/test references and actual usage where available; do not duplicate full transcripts.

## Research foundation

- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) — independent work, explicit worker boundaries, expensive token overhead; internal research evidence is not a coding guarantee.
- [Anthropic: Building multi-agent systems — when and how](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them) — context separation, independent parallelizable work, specialization, coordination costs.
- [Anthropic: When to fold subagents into the main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) — avoid unnecessary planner/router agents and duplicated context.
- [Google Research: Towards a science of scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) — differences between parallelizable and sequential work.
- [OpenCode agents](https://opencode.ai/docs/agents) — configuration must be checked against the user's live harness; do not assume model/effort controls transfer to Devin.

## Authority and exclusions

**Authorized:** Scoped canonical edits/commits to the delegation skill, `manage-project-tasks` integration, skills catalogue and any required manifest change, this audit task and active index; read back and report.
**Not authorized:** Start actual subagents, deploy/sync to OpenCode or Devin installations, alter provider configuration or credentials, change consumer projects, implement a task execution service, run paid benchmark experiments, create unrelated tasks or KB artifacts.

## Verification and completion

Read back source files and check trigger, decision ownership, model/effort/harness distinction, worker contract and fallback, permissions, execution boundaries, catalogue selection, and task-index state. No claim of actual subagent performance without a harness trial. Close as Completed after all approved canonical edits are verified; the closed audit file remains at this path.
