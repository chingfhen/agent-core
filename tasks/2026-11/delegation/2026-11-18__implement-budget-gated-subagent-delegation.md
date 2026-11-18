# Task: Implement cost-gated, approval-first subagent delegation

**File:** `tasks/2026-11/delegation/2026-11-18__implement-budget-gated-subagent-delegation.md`  
**Created:** 2026-11-18  
**Last Updated:** 2026-11-18  
**Priority:** Now  
**Status:** Closed — canonical source delivered; runtime effectiveness untested

**Goal:** Provide a small, reusable cross-harness Agent Core skill that recognizes when bounded **implementation-worker subagents** can help an otherwise capable main agent, chooses not to delegate when it cannot justify the benefit, and executes a **single human-approved delegation plan** using explicitly cheaper worker model(s), without replacing Project Tasks or Git Workflow.

**Why this matters:** The user already explores design with the main agent and personally orchestrates longer-term work by resuming durable Project Tasks in fresh sessions. Exploration-only delegation would add little to that established workflow. The desired new capability is that a main agent can identify separable coding work and have a cheaper worker implement it under clear scope, taking over part of the coordination/supervision the human would otherwise perform. The user has constrained model/quota resources; subagent enthusiasm must not create avoidable model or token spend. The user wants the option to refuse delegation even for apparently large work.

**Approved direction (user, 18 November 2026):**
- New capability is **implementation-worker first**, with read-only scouts/reviewers optional only where they materially help.
- First-class decision-making is required: assess separability, stable contracts, likely coordination cost, filesystem conflicts, testability and risk; prefer no delegation on small, tightly coupled, ambiguous or security-critical implementation.
- **One conversational approval for the bounded plan**, including all worker launches within it; do not ask for permission before every subagent. Material changes to the plan are outside the original approval, not an excuse for silent extension.
- Main agent proposes a worker model (user generally prefers **DeepSeek or Luna**, but no specific provider/model ID or price is assumed). The user will correct the choice or research a nonpreferred proposal before agreeing. The worker must actually use a cheaper model than the parent. Never accept inherited main-agent model or unavailable/unverified cheaper execution as a fallback; if the cheaper worker cannot be established, run normally without delegation, even when requested.
- Be conservative about **aggregate token usage**: bounded worker scope/count, no automatic retry swarms, no speculative parallelism, no costly alternative attempts without a separately approved plan. Cheap per-token rates do not guarantee a cheaper overall run.
- Preserve **cross-harness use** (OpenCode first, Pi/others when capable) without creating a custom OpenCode-specific implementation requirement or unmanaged agent configurations. A plain skill cannot magically provide subagent tooling or install models.
- Use existing `manage-project-tasks` when continuing a saved task, but **do not require a Project Task for a standalone scoped implementation**. Project Tasks retains durable execution memory, approvals, checkpoints and cross-session handoffs.
- Preserve the existing `git-branch-to-review` authority for managed branches, worktrees, PRs, publication/merge/cleanup; no delegation permission implies writing outside approved scope, pushing, deploying, provisioning, credential use, or circumventing host permissions.
- Do not revive or copy the retired `execution-topology` skill. It is historical inspiration only; this new job is narrowly about whether/how to delegate implementation and integrate work.

## Success bar

A capable agent loading the skill should:
1. **Decline correctly:** For a small fix, coupled multi-file change, unresolved behavior, unverified cheap worker, missing workspace isolation or a risky authorization boundary, choose single-agent execution, without needless permission ceremony.
2. **Propose useful work:** For a demonstrably separable implementation slice, explain why one (or at most a few) cheaper workers are preferable to the main agent doing it, which files/contracts the child owns, what it will deliver and what the parent retains.
3. **Propose a real model:** State the exact available worker provider/model when exposed; prefer user-mentioned DeepSeek or Luna if actually available and fit for task; distinguish an unverified candidate from a confirmed cheaper model. Never silently inherit the parent model.
4. **Obtain one approval:** Present one compact plan covering worker identity/model, number and scopes, isolation/write permissions, stop/budget guardrails, integration and verification. After explicit approval, execute all authorized workers **without a separate per-worker conversational prompt**. Honor unavoidable host tool permission dialogs. No approval means no launch.
5. **Control interference:** Never give workers conflicting write authority. For concurrently mutating workers require verified separate workspaces/worktrees or equivalent real isolation; do not assume separate chat sessions imply separate filesystems. In a shared checkout, use a single bounded writer and avoid simultaneous parent writes to the same working set. Check pre-existing work and concurrent changes.
6. **Preserve quality and accountability:** Child reports actual files, tests, issues and limitations; parent inspects real diff/output, resolves integration, runs appropriate combined tests, reports actual verification, and updates an authorized Project Task/checkpoint if in use. Worker self-report is not proof.
7. **Stop cleanly:** Bound failures/retries and spending; on cheap-model loss, ambiguous side effects, merge conflict, budget pressure or materially changed scope, stop delegation and report rather than launching more children. Continue main-agent work only if still within existing authority.
8. **Work without extra infrastructure:** No job queue, scheduler, new task registry, custom agents, cloud executor, monitoring platform or automatic recursive delegation needed for v1.

### Representative cases for future evaluation (not performed now)

- **Good candidate:** TripVerge contracts already fixed; a UI implementation slice has a stable interface and distinct write paths. Propose one cheap implementation worker; parent owns domain invariants and integration.
- **Decline:** Fix a one-file bug; both parent and worker would edit the same functions; or critical backend authorization is unresolved.
- **Hard cost rejection:** OpenCode subagent would inherit the parent's model because no explicit cheaper configured worker is available. Do not spawn.
- **Approval batching:** User approves one plan with two independent workers; both execute without two further conversational approvals, while changes to model, count or scope require re-scoping and approval.
- **Conflict/quality:** Child reports success but tests show a stale-write regression; parent does not mark task complete and must isolate/reconcile work before any further delegate attempt.
- **Compatibility:** OpenCode can use native subagent tools when configured; a harness without explicit cheaper worker execution receives a clear no-delegation outcome.
- **No Task:** Same skill can coordinate a permitted standalone implementation without creating a mandatory task file or new task tracker.

## Scope and rights for this task

**Authorized now:** create this detailed Agent Core project-task record; create a new production delegation skill using the approved decisions and any necessary concise references/scenarios; reconcile `personal-skills.toml` and the Skills Catalogue so it can be published through the normal explicit harness sync. Update the task and its index as execution state changes. Read relevant existing skills for boundaries. Make scoped GitHub source commits for these approved changes.

**Not authorized:** actual deployment or use of subagents to implement a consumer project, modifying TripVerge, changing Git Workflow / Project Tasks / global AGENTS.md, installing models or custom agents, invoking harness sync on a machine, launching paid workers, changing credentials, setting up a Task Execution Service, or running real multi-model usage experiments. Publication to the configured local OpenCode/Pi/Devin installation remains a separate user action. No KB capture was requested here.

**Expected source:** `skills/delegate-implementation/SKILL.md` (name is a practical choice, not the outcome itself), selected in `personal-skills.toml`, discoverable in `docs/skills-catalog.md`. Keep one canonical source; no duplicate skills or task execution ledger.

## Why this is not simply long-session management

The human already uses `manage-project-tasks` and Git as cross-session durability. The requested incremental capability is **situational low-cost implementation delegation**, not making one conversation run for days, spawning general research teams, or autonomous orchestration. The main agent retains overall outcome ownership and can complete most tasks itself.

## Sources and prior constraints

- [Current Project Tasks](../../../skills/manage-project-tasks/SKILL.md) — durable execution context; task execution alone does not authorize child agents.
- [Current Git Workflow](../../../skills/git-branch-to-review/SKILL.md) — source isolation, permission, branch/PR integration and protected changes.
- [Skill Design Guide](../../../docs/skill-design-guide.md) — distinct job, concise trigger, minimal cost, observable outcomes.
- [Archived execution-topology](../../../archive/skills/2026-10-08__execution-topology-SKILL.md) — historical idea only.
- [Defer Task Execution Service](../task-execution-service/2026-11-05__design-trustworthy-cross-project-executor.md) — a separate unattended queue/worker architecture, not part of this skill.
- [OpenCode agent documentation](https://opencode.ai/docs/agents) — current per-agent model and subagent tools need runtime confirmation.
- [When Sub-Agents Work in Parallel (2026)](https://arxiv.org/abs/2610.10263) — cited in discussion for gains on long-horizon tasks and regressions/costs on bounded coding tasks; do not infer benefit on this exact harness without trials.
- [Recent enterprise-style multi-agent research](https://arxiv.org/) — discussion noted high token overhead in a particular comparison; no benchmark result here should be treated as a verified budget for this task.

## Delivery result — 2026-11-18

**Completed:** Added [`delegate-implementation`](../../../skills/delegate-implementation/SKILL.md) to Agent Core `main`, selected it in [`personal-skills.toml`](../../../personal-skills.toml), and indexed it in the [Skills Catalogue](../../../docs/skills-catalog.md). The skill implements a selective *implementation-worker-first* workflow: no-delegation decision; actual cheaper-model preflight (DeepSeek/Luna preferred when available); one conversational approval covering all bounded workers in a plan; isolation/no overlapping writes; main-agent integration and check ownership; optional but compatible Project Tasks integration. Existing Git workflow approvals and publication boundaries remain unchanged.

**GitHub commits:** [Skill source](https://github.com/chingfhen/agent-core/commit/4422ca8dfe37b0a9b5c991d3e5cb615c3cedce38); [selected manifest](https://github.com/chingfhen/agent-core/commit/d9a7c812fb1a5fbcb8b3d87c649cd926e11a0d38); [catalogue](https://github.com/chingfhen/agent-core/commit/c8c892ae8793f08166450fbabef6fbf28f2db0bd). The final task status/index bookkeeping is a separate commit.

**Checks actually performed:** Remote GitHub read-back of skill/manifest/catalogue/task/index; inspected critical trigger, approval, hard cheaper-model refusal, optional Project Tasks dependency, worker isolation and Git ownership text; confirmed selected name is unique and catalogue links to the skill. These are **structural checks**, not a model/harness behavior trial.

**Not verified:** No execution in OpenCode or Pi, no lower-cost provider lookup in the user's installed harness, no live child launch, no real resource savings or token metering, no isolation/merge integration test, no fresh-session skill triggering, and no automated Python test suite or CI status claimed. No extra consumer repository, KB, model configuration or installed harness was changed.

**Next action:** None required to finish this source-delivery task. If desired later, run `agent-core sync --harness opencode` on the user's machine and inspect loaded skills; a separately authorized real feature trial can then evaluate correct refusal, one-shot approval, cheaper model routing, cost and integration evidence. Do not treat this delivery task as automatic permission to initiate that trial or create a second open evaluation task.

## Completion and evidence

During delivery record actual files, revision/commit, static checks and missing runtime evidence. Source presence does not establish agent's correct refusal, proper model selection, invocation, child isolation or net token savings. Complete this task once the approved canonical skill and manifest/catalogue are saved and read back; preserve deferred experimental verification as an explicit limitation rather than a newly mandatory task or silently claiming success. Do not automatically initiate a KB/docs/lessons capture without a separate request.
