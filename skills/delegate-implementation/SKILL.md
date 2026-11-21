---
name: delegate-implementation
description: >
  Decide whether bounded coding implementation would benefit from cheaper-model
  subagents, then propose one approval-gated worker plan and coordinate its
  execution when approved. Use for substantial, plausibly separable engineering
  work or when the user asks to consider implementation subagents. Choosing no
  delegation is a valid result. Not a default for small edits, read-only research,
  long-session continuity, or ordinary Project Tasks maintenance.
disable-model-invocation: false
---

# Delegate Implementation

## Purpose and non-negotiables

**Move useful, clearly bounded implementation work to lower-cost workers while the main agent remains accountable for the result.** This is not an instruction to spawn subagents. Main-agent execution is the default until delegation has a credible advantage.

- **One human approval per bounded delegation plan**, not one conversational approval per subagent. The approved plan may contain several named workers; launch only those workers, within their authorized model, task, scope, permissions, and limits. Respect any unavoidable harness permission prompts. Silence, previous task approval, or a user's general enthusiasm for delegation is not plan approval.
- **A genuinely cheaper worker model is a hard prerequisite.** Determine the main agent's model where possible; confirm the proposed worker is actually available in this harness, will run under an explicitly selected lower-cost model, and can execute the needed tools. Do **not** rely on subagents inheriting the parent model. If this cannot be established, **do not delegate, even when requested**. Do not invent model identifiers, pricing, subscriptions, or quota access.
- Suggest a model the human is likely to recognize: **DeepSeek or Luna when available and appropriate**. These are preferences, not assumed provider/model IDs or guaranteed prices. State the exact configured model identity if known; otherwise explain the missing information. The user may change the proposed model before approving.
- **Resource economy is part of the decision.** Cheaper per token does not ensure lower total cost. Factor in extra context, coordination, verification and retries. Use a conservative initial worker count (often one), limited attempts, and no speculative swarms. If a credible saving or work-quality benefit cannot be articulated, keep the main agent.
- **No hidden authority expansion.** An approval to delegate does not authorize an unapproved feature, extra files, branch creation, credential exposure, security changes, cloud costs, publication, deployment, force push, merge, or destructive action. Respect narrower repo, harness and human gates.


## Required early delegation decision

For substantial implementation when this skill is invoked, decide **before substantive coding**, and state once in the conversation: `Delegation decision: propose workers / execute previously approved workers / main-agent execution / blocked — [decisive evidence-based reason]`. Evaluate separability, expected net benefit, actual cheaper model/tool availability, isolation, and authorization; mark unknowns explicitly. Even when no worker is appropriate, explain the decisive reason rather than silently proceeding. Do not ask permission merely to decline delegation. The statement does not authorize launching workers or bypass any approval or repository gate below. Avoid ceremonial receipts if this skill was invoked for a small or irrelevant task.

## 1. Decide whether any delegation is worthwhile

Use the existing user request, accepted design/contracts, repository state, and (when present) relevant Project Task. A large or long-running task by itself does **not** warrant subagents. The goal is *implementation delegation*, not handing all early exploration to scouts: the user typically investigates goals and design with the main agent first.

Prefer a bounded **implementation worker** when:
- desired behavior and success criteria are already sufficiently clear;
- one meaningful slice can be described with a stable interface, concrete outputs, and a coherent test boundary;
- its write scope can be separated from current parent/other-worker edits or executed sequentially without collision;
- the chosen cheaper worker is capable of the slice and the main agent can independently inspect and integrate it;
- expected saved main-model effort plausibly exceeds coordination, integration and retry overhead.

**Choose no subagents** for straightforward edits, tightly coupled changes that demand continuous shared context, ambiguous product decisions, unsettled API contracts, active Git conflicts, insecure or unapproved access, critical security/transaction invariants best retained by the main agent, weak verification paths, or insufficient cost/model/isolation evidence. Do not ask permission merely to decline; continue ordinary authorized execution.

Read-only exploration, alternative attempts and independent review are optional *supporting* delegation patterns, not the default or a compulsory prelude. Use only when they make the approved implementation materially more reliable or tractable. Avoid redundant research that the human/main agent already completed.

## 2. Propose a single approval package

If delegation passes the gates, present a concise proposal **before any child is launched**:

- **Why:** what the main agent would otherwise do, why this particular bounded implementation is better delegated, and the no-delegation fallback.
- **Workers:** number and purpose (default to one); proposed **explicit provider/model ID** when actually discoverable, why it is cheaper than the main model, and any pricing/quota uncertainty. Do not silently choose a different model.
- **Work contract for each:** deliverable, agreed behavior/constraints, exact or bounded files/modules, interfaces, permitted edits/tools, required checks, and stop/escalation conditions.
- **Coordination:** isolated workspace/worktree or sequential/nonoverlapping write protocol, parent-owned integration, maximum initial attempts and any available budget limits. Distinguish cost estimates from observed usage.
- **Approval boundary:** specify that one approval covers **all listed workers and their bounded actions**. Ask once: “Approve this delegation plan?” Do not ask the same question again for each child.

If essential runtime/model facts are missing, **report the blocker instead of seeking approval for a plan the harness cannot execute**. Do not create or modify harness agent configuration, obtain paid access, or install a provider unless separately authorized. A materially different worker model, expanded scope, additional unplanned workers, extra spending, or changed permissions **is not covered** by the old approval: stop and obtain approval for a revised plan rather than quietly escalating.

## 3. Execute the approved worker plan

1. **Recheck reality:** approved request, model routing, tool permissions, worktree/branch/dirty state, file ownership and isolation. A separate chat/session does **not** imply a separate filesystem. In OpenCode, inspect actual agents/tools/config; model inheritance is not evidence of a cheaper worker. In another harness use its actual supported equivalents.
2. **Isolate writers:** prefer a single worker on a bounded change with the main agent avoiding its files until handoff. For multiple concurrent *mutating* workers, require actual independent workspaces/worktrees or an equivalent verified isolation strategy, distinct write sets and a safe integration path. Where Git/worktree operations are governed by `git-branch-to-review`, follow that workflow and its separate gates; do not manufacture branches here. Without safe isolation, run one writer sequentially or decline delegation.
3. **Give self-contained briefs:** state required objective, relevant existing decisions, exact inputs/outputs/contracts, allowed paths, test commands if known, forbidden actions, and when to stop. Do not transmit the entire conversation or secrets. Workers should report actual changed paths, checks/output, errors, blockers and anything left incomplete. No recursive delegation by default.
4. **Observe without micromanaging:** allow the approved workers to complete their bounded work without repeated human approval or noisy progress requests. Avoid duplicate main-agent implementation of the same slice. Check meaningful results before additional planned waves; keep retries bounded and based on new evidence.
5. **Integrate with main-agent ownership:** inspect the real diff/files against baseline and the accepted contract, reconcile interactions and tests, check combined behavior and significant failure cases, and report what is verified versus merely claimed. A worker saying “done” is not evidence. Reject/repair in-scope defects through the approved process; do not silently launch replacement workers or upgrade to expensive models.
6. **Checkpoint using existing owners:** when executing a saved Project Task, use `manage-project-tasks` for authorized progress, current revision, verification state and next permitted action. When delivering managed branch/PR work, use `git-branch-to-review`. These are *conditional integrations*, not prerequisites for a standalone request. Do not create a second task ledger, worker registry, or mandatory report.

## 4. Stop, account, and learn

Stop delegation on worker-model mismatch, unavailable low-cost execution, exceeded agreed limits, unsafe concurrent writes, ambiguous side effects, repeated failure without a fresh hypothesis, or permission/scope drift. Preserve authorized work, state what remains local versus committed/published, and return control to the main-agent path when permitted.

A short receipt should identify **delegated vs retained work, actual worker model(s), observed usage if available (otherwise unknown), integrated changes, checks and gaps, and remaining human decisions**. Do not claim token savings from a hypothetical price or independence from a reviewer who saw the same context.

**Completion means the approved user outcome is supported by integration evidence, not that child sessions finished.** The skill earns its place when a suitable worker meaningfully reduces main-agent effort or improves outcomes with acceptable resource use; choosing no delegation should remain cheap and routine.

## Boundaries and sources

This is a cross-harness behavioral workflow with OpenCode as its first likely consumer. It requires actual accessible subagent/model tooling to execute and creates none. It is **not** a long-lived queue, background job service, autonomous multi-agent team, or substitute for human approval. For OpenCode-specific current model/permission details consult [OpenCode agents](https://opencode.ai/docs/agents) when needed; do not hardcode version-specific tool names.

Related Agent Core owners: `manage-project-tasks` (continuity), `git-branch-to-review` (Git delivery), `code-review-quality` and applicable checks (review), `define-success` (explicit outcome exploration). This skill does not automatically invoke those workflows for unrelated work.

Research motivation: [When Sub-Agents Work in Parallel (2026)](https://arxiv.org/abs/2610.10263) describes both selective long-horizon benefit and regressions/overhead, supporting a strong **no-delegation** option and explicit resource gates; these are not measured results for this Agent Core implementation.

## Decision visibility

When this skill makes a consequential choice—selecting, declining, or deferring a path, or applying a material scope, permission, cost, safety, or verification gate—make the chosen outcome and its evidence-based reason visible in the normal conversation (a compact `Decision: ... — ...` is sufficient). State it before acting when permission or cost depends on the choice, otherwise at the relevant handoff. An explanation already clearly given counts; do not add a duplicate status line, routine no-op receipts, a separate log, or private reasoning. Merely loading a skill is not evidence that its decision was applied.
