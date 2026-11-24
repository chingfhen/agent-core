---
name: delegate-implementation
description: >
  During planning of substantial implementation work, decide whether and how
  subagents should execute bounded parts of the work, or explicitly choose no
  delegation. Use when the human requests delegation planning or while preparing
  an implementation-ready Project Task with plausible separable work. Select an
  intended execution harness, worker responsibilities, model and thinking effort
  where support is known, coordination, verification and fallback; persist the
  decision in an authorized Project Task and show it to the human. For execution
  of an existing approved plan, follow its contract and check live prerequisites
  without reopening the delegation strategy. Not for routine task bookkeeping,
  small edits, or compulsory subagent invocation.
disable-model-invocation: false
---

# Plan Implementation Delegation

## Ownership and trigger

**Planning decides whether/how to delegate; execution follows that decision.** The goal is reliable, useful implementation delegation, **not** maximum worker invocation or minimum per-token price.

- **Planning-time invocation:** Load when the human says to plan delegation, including "use the delegation skill", or when preparing/substantially revising a **substantial implementation-ready Project Task** where meaningful bounded work might be separable. The planning agent makes the decision itself using this skill; no mandatory meta-planner subagent. For small or obviously indivisible work, a one-sentence no-delegation result suffices. Do not invoke on ordinary maintenance, read-only task discovery, early goals without settled implementation constraints, or merely because a task exists.
- **Planning output:** Choose **delegate**, **no delegation**, or **defer** when essential design facts are unresolved. Show the decision and concise rationale to the human. When task-authoring rights exist, record it in that Project Task **before implementation**; when they do not, report it in the conversation and do not mutate the task. This skill neither creates a task store nor grants task-write permission.
- **Execution-time use:** If a saved task includes a current, approved delegation contract, the executor consults **this skill's execution sections only** to apply its operational checks, run authorized workers, integrate, and account. It does **not** redo economic/strategic delegation analysis. A stale/unsafe plan follows its documented fallback or returns for replanning; no unrecorded substitution.
- **No planned delegation:** Implement normally. An executor must not decide to create an opportunistic worker plan just because it can call subagents. A human may explicitly commission a new planning pass before affected implementation.

The planning agent owns strategic choice; the executing parent agent remains responsible for the final code and verification. The human can change a proposed worker, model, effort, harness, or scope before authorizing execution. A planning decision is **not permission** to launch workers or to edit unrelated files.

## Planning: choose useful work, not an agent count

Ground the decision in the user's outcome, approved technical approach, actual task and repository boundaries, acceptance tests, and expected implementation effort. Use the applicable research-derived practices below, not a fresh broad literature review for each task. Consult [Delegation design reference](references/delegation-design.md) when decomposition, coordination, or model choice is genuinely complex.

**Prefer bounded delegation** where at least one material slice has: stable inputs and interface; a useful independent output; separate working context or coherent file ownership; a verification oracle; a credible benefit in reduced parent work, specialist focus, parallel time, or context isolation; and an integration path that costs less than redoing it. Candidate patterns include a component against an accepted contract, a self-contained migration, independent test implementation, or a black-box verification pass. A worker can be useful **sequentially**; concurrency is not required.

**Prefer no delegation** for a small edit, ambiguous goal, unsettled contracts, strongly sequential/tightly coupled writes, frequent cross-worker conversation, shared security/transaction invariants best held by the parent, weak verification, or expected context/coordination overhead exceeding benefits. A big task alone does not justify more workers. A high-capability single agent with focused tools may be better than a routing/planning subagent.

**Optimize end-to-end rather than per-token cost:** compare expected parent effort saved and any quality/latency gains with worker setup, duplicated context, tool/inference consumption, integration, verification, and likely retries. Cheaper models are **preferred when fit**, but **not mandatory**. The same model, a stronger model, or higher thinking effort may be justified for a bounded high-value slice; make that tradeoff visible. Prefer the smallest effective worker count (often one), but allow multiple genuinely independent scopes when benefits justify them. No speculative swarms or recursive worker delegation by default.

**Limit coordination tax:**
1. Split by independently testable **deliverables and stable interfaces**, not arbitrary code-file counts or repeated "help me" roles. Retain cross-cutting architecture, security invariants, arbitration, integration and end-to-end acceptance with the parent.
2. Assign each worker a single clear output, bounded write/read permissions, relevant source-of-truth references, required tests, and escalation conditions. No overlapping concurrent writers. Share *minimal sufficient* context, never the full conversation by default; link the Project Task rather than copying it whole into every child.
3. Use **hub-and-spoke** communication: task is the durable decision record, parent supplies focused briefs, workers return actual artifacts plus short evidence receipts, parent resolves dependencies. Do not require agents to negotiate with one another or continuously message progress. Batch questions at real blockers.
4. Prefer sequential delegation when contracts or state are unstable, and parallel delegation only with independent work and actual workspace isolation. Verify combined behavior at integration.

## Planning: select harness, model and thinking effort

Choose the **intended execution harness** first (e.g. OpenCode or Devin) from where the work will actually run, not merely the planner's current chat. Investigate accessible, current documentation or config when available. Do **not** assume that two harnesses expose the same agent APIs, model picker, reasoning settings, tools, quota, or permissions.

For **each planned worker**, specify:
- intended role and exact/bounded implementation slice;
- **provider/model identifier** when verifiable and the harness can select it; otherwise a clearly marked *candidate or deferred runtime choice* with selection criteria, not a fabricated ID;
- **thinking level/variant** only if the specific harness/provider/model exposes and supports it; otherwise state *not controllable/unknown*, never claim an requested "xhigh" was applied by wishful wording;
- capability rationale and expected resource tradeoff, including whether it uses the same model as the parent, rather than asserting that same-model delegation saves tokens;
- necessary agent/tool permissions, isolated execution requirements, and any meaningful paid quota/cost uncertainty.

OpenCode's [current agents documentation](https://opencode.ai/docs/agents) describes child sessions, agent-specific model selection and optional variants, and parent/child permissions. At runtime verify the installed version/config and actual selection; model inheritance is not a cost guarantee. For Devin, inspect its **live** subagent/model/effort controls; do not project OpenCode syntax or capabilities into Devin. The planner may produce a conditional plan with explicit unresolved runtime facts; lack of preplanning harness access does not automatically force no delegation. **Actual execution must not claim an unverified configuration was honored.**

## Persist the decision and show it

For an implementation-ready Project Task, add a concise **Delegation Decision** section or equivalent. Do not require a long section for no-delegation. Choose one branch:

- **No delegation:** `Decision: main agent — [material reason]`. The executor works normally.
- **Defer:** `Decision: defer — [specific missing accepted design/contract or other prerequisite, and owner of next decision]`. Do not imply implementation or workers are ready.
- **Delegate:** Record `Decision: delegate`, why this is advantageous over direct implementation, intended **execution harness**, approved/candidate worker(s) with responsibilities and model/effort status, stable interfaces and authoritative references, parent-retained work, write boundaries and isolation, short handoff/receipt expectations, checks, coordination order, budgets/attempt limits if applicable, **fallback/stop conditions**, and **approval state**. Use compact per-worker details rather than repeating the full task. No mandatory table/template for simple work.

**Visibility:** Present a short human-readable receipt while planning: decision, workers and assignments, harness and model/effort (verified vs proposed), expected benefit/tradeoff, fallback, and what requires human authorization. Make uncertainty visible; invite adjustment without requiring the human to design the delegation. Preserve the approved configuration and changes in the task for future sessions. A task records *intent and evidence*, not a hidden tool invocation.

**Authority:** A plan in a task is not itself execution permission. Explicit human approval of the **surfaced task implementation plan including its delegation arrangement** counts as the single approval for all named workers; do **not** ask again at execution or per worker. A separately explicit approval of this delegation plan also counts. Silence, merely saving a task, or general enthusiasm for delegation do not. The recorded approval must actually be traceable; if absent or contradicted, do not launch. Tool-level authorization prompts still apply. Approval never expands implementation scope, write access, branch/PR authority, credential access, deployment, or spending gates. Material model, effort, worker-count, cost, scope, or permission changes require a new human decision unless the approved plan **explicitly** includes the bounded alternative.

## Execution: apply, verify, and report; do not replan

When an approved Project Task calls for delegated execution:

1. **Read the current authoritative task and approval.** Identify the intended harness and each worker's immutable contract, source/target revision assumptions, parent's retained work, exact fallback, limits, and permitted next action. Recheck actual requested execution authority against repository/harness rules. A stale task is not permission.
2. **Preflight operational reality only:** Confirm selected worker ID/model and effort/variant if the plan requires them, tools, access, actual cost/quota limitations, working tree/branch/dirty state, independent workspace requirements, and no overlapping writers. A child session is not necessarily a separate filesystem. If the planned configuration is unavailable, follow a **preapproved** equivalent or main-agent fallback if explicitly documented; otherwise **stop and report**. Do not quietly choose a new strategy, worker, model, or effort.
3. **Issue focused worker briefs** from the saved contract: objective and success criteria, accepted interface and authoritative context references, exact/bounded read/write paths, tools, tests, prohibited actions, expected output and evidence receipt, budget/attempt limit and stop/escalation conditions. Avoid copying huge transcripts or transmitting secrets. No recursive delegation absent explicit plan authorization.
4. **Coordinate without duplicated work:** Avoid parent implementation of a worker's assigned slice. Let bounded workers finish without routine conversational micromanagement; handle genuine blockers. Serialize conflicting writes; concurrent mutating workers require verified separate worktrees/workspaces or equivalent, and follow `git-branch-to-review` where applicable (including its independent branch/worktree gates).
5. **Own integration and acceptance:** Inspect actual changed files/diff against baseline, verify claimed checks, test combined behavior including important failure cases, and reconcile dependencies. Worker self-reports are not proof. Repair only within existing authorization and retry limits; do not silently spawn replacements, expand scope, or promote a costly model.
6. **Checkpoint with existing owners:** When task changes are authorized, use `manage-project-tasks` to record planned-versus-actual workers/models/effort, relevant child-session identifiers, commit/diff/check references, **observed** usage if available (otherwise unknown), results, deviations, verified gaps, and next permitted action. When writes are barred, return this concise receipt for authorized task maintenance. Do not invent a second registry or store transcripts in the task.

**Stop or fall back** on unapproved material deviations, missing capability, unsafe isolation, interface drift, ambiguous side effects, blocked permission, exceeded attempt/budget limit, or repeated failure. Only use a fallback the human previously authorized; otherwise stop and request replanning/approval. Do not treat a good-sounding alternative as approved. If the fallback is main-agent execution, state that before continuing and mark the deviation in the task where permitted.

## Research and boundaries

The rules above adapt published findings, not guaranteed savings for this harness:

- [Anthropic, building multi-agent systems](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them): use independent contexts, parallelizable work or specialization to offset coordination; start with a competent single agent.
- [Anthropic, folding unnecessary subagents into the main loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop): avoid redundant planner/router workers and excess context transfer.
- [Anthropic, multi-agent research engineering](https://www.anthropic.com/research/multi-agent-research-system): explicit worker scopes and condensed handoffs; research gains with significant token overhead are **not** coding guarantees.
- [Google Research, scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/): coordination favors parallelizable rather than sequential tasks.
- [When Sub-Agents Work in Parallel (2026)](https://arxiv.org/abs/2610.10263): coding throughput and quality effects depend on workload and coordination.

This is a **cross-harness planning and execution contract**, not a runtime orchestrator, authorization bypass, automatic subagent factory, model installer, budget meter, persistent queue, or request for benchmarks. `manage-project-tasks` owns task persistence and permission boundaries; `git-branch-to-review` owns managed Git delivery; independent review and engineering specialists retain their own scopes. The saved plan should replace repeated strategic delegation reasoning, not add a new compulsory layer.

## Decision visibility

During **planning**, state `Delegation decision: delegate / main-agent execution / defer — [decisive reason]` and show the worker outline if selected. During **execution**, state only `Delegation execution: following approved plan / authorized fallback / blocked — [material evidence]` at the relevant boundary. Merely loading this skill is not evidence that its decision or execution happened.
