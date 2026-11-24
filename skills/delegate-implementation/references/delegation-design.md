# Delegation design playbook — consult only for complex planning

**Use when:** A material implementation plan offers multiple credible worker boundaries, uncertain coordination cost, model/effort tradeoffs, or cross-harness execution. For a simple no-delegation decision, do not load this reference. The core behavior and approval rules live in [../SKILL.md](../SKILL.md).

## Assess task shape before allocating agents

| Work shape | Preferred arrangement | Why |
| --- | --- | --- |
| Small, tightly coupled change | Main agent | Worker briefing and integration likely cost more than implementation. |
| Independent component against a stable accepted interface | One bounded worker; parent owns integration | High independence and inspectable artifact. |
| Several independent components with nonoverlapping writes and stable contracts | Multiple workers when isolation/coordination support is real | Parallel work may reduce critical path; only if interfaces are settled. |
| Shared authorization, security or consistency logic | Parent retains invariant; delegate only separable tests or supporting modules when useful | Cross-cutting decisions need single authoritative owner. |
| Expansive evidence gathering before design | Separate research work only if explicitly useful to planning | More independent search is possible, but not an obligatory scout before coding. |
| Long sequential mutation pipeline with coupled steps | Parent-led sequential work; optionally one specialist worker per stable phase | Parallelization can multiply stale-state errors. |
| Independent black-box verification of an implemented contract | Bounded reviewer/tester with separate acceptance oracle | Review has value only when not conflated with worker self-report. |

These are **heuristics**, not permission or a guarantee of returns. Never introduce a worker solely to satisfy a count.

## Estimate net value without fake precision

Consider:
- **Benefit:** saved main-agent implementation/context cost, specialized capability, real wall-clock shortening, stronger verifiable correctness.
- **Additional burden:** child setup, copied input context, child tool/model usage, parent coordination, artifact reconciliation, verification, retries, and human approval overhead.
- **Quality impact:** can a parent evaluate this output independently using tests, diffs, schemas or real behavior? If not, delegation can increase verification burden.
- **Budget:** worker cost is not just price per token; parallel child agents consume tokens concurrently. Same-model delegation can still offer valuable context isolation or work partition, but should not be called cheap.
- **Thinking effort:** choose the effort/variant whose expected incremental benefit fits that worker's task; more thinking is not automatically better. Record only the setting the target provider/harness exposes.

Use qualitative comparison for ordinary tasks. No routine benchmark, token estimates with invented rates, or repeated internet searches. When models/costs are truly decision-relevant and currently available, check authoritative provider/harness sources.

## Worker decomposition and coordination contract

The task is the *durable decision record*, not a real-time message bus. Use a **parent orchestrator and bounded workers** by default:

1. Accept stable contracts, list independently verifiable deliverables, and identify the one component that can be handed off with little ambiguity.
2. Allocate write sets/modules: no simultaneous edits to the same files or shared schema unless the plan explicitly serializes work and validates transitions.
3. Put the worker's constraints in a short brief: expected behavior, owner of inputs/outputs, authoritative references, allowed paths, tools, acceptance checks, and when to stop and ask.
4. Choose parallelism only for independent contracts. If one worker must consume another's incomplete output, prefer sequential handoff with a verifiable checkpoint instead.
5. Require a compact **receipt**: actual file/diff path, parent-readable outcome, tests run and their results, incomplete items, risks, blockers, actual model/effort and observed usage if available. A summary does not replace inspection.
6. Keep integration with one parent. The parent does not run the same implementation in parallel and independently verifies combined behavior. Escalate meaningful contract changes, not routine progress updates.

**Example work order (adapt to actual files):**

```text
Worker: itinerary-day-card
Outcome: Implement accepted day-card component against schema v2.
Authoritative context: Project Task link; schema/interface refs.
Scope: UI module only; cannot change API, auth policy, or migrations.
Model/effort: exact configured selection (or explicitly unknown).
Files: allowed edit paths; no overlap with parent/other workers.
Checks: component tests, type checks; report commands and failures.
Stop: interface ambiguity, missing permission, shared-file conflict.
Return: patch/commit reference; actual changed files; checks; blockers.
```

Do not copy the entire Project Task or a massive chat into each child unless that large context is demonstrably essential. Reference canonical sources and supply the few relevant accepted decisions.

## Harness constraints

- **OpenCode:** [Official agents guide](https://opencode.ai/docs/agents). Current documentation allows per-agent provider/model plus optional variant, and says an unconfigured subagent inherits parent model. It documents separate child context and parent/child permissions. Verify actual installed version and visible agent; do not infer a child is cheap or that its variant is active simply because it was requested.
- **Devin:** Check accessible current product documentation, session capabilities, agent launch and available model/effort controls in the *actual* target environment before claiming a named subagent model or reasoning level is selectable. An OpenCode `#variant` selector is not a cross-harness standard. If unavailable at planning, note candidates and an explicit execution-time preflight/fallback, not an invented configuration.
- **Other harnesses:** Same rule: describe capabilities observed, unknowns explicitly; no imaginary tool or silent provider/effort substitution.
- **Ownership:** New branches/worktrees, remote commits/PRs/merges, model purchases and runtime configuration remain subject to their separate approvals and owning workflows; a planning contract is not a source of new privileges.

## Evidence and limits

- [Anthropic, multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system): strong internal results on breadth-first research and large token overhead; the 15x-chat figure is **not** a coding multiplier for this user's plan. Teaches scoped objectives and compressed handoffs.
- [Anthropic, when to use multi-agent systems](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them): context isolation, parallelizable tasks, specialization are the typical cases; warns against unnecessary overhead and repeated context.
- [Anthropic, fold subagents into one loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop): redundant router/planner agents can decrease effectiveness when their scope is better held in the main agent.
- [Google Research, scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/): systematic evidence that coordination helps differently on parallel vs sequential tasks.
- [When Sub-Agents Work in Parallel](https://arxiv.org/abs/2610.10263): mixed coding task results; use as a warning against universal parallelism, not a prediction for Agent Core.
- [OpenCode, agents](https://opencode.ai/docs/agents): model/variant/permission mechanics apply to the documentation's stated version, not to every installed harness.

**Application standard:** choose the smallest credible delegation architecture, report assumptions and no-delegation decisions clearly, and let normal execution traces inform later improvements. No experiment is mandatory for ordinary work.
