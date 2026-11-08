---
name: git-workflow
description: >
  Manage an explicitly requested Git branch-to-review workflow and resume approved
  managed work. Use when asked to use git-workflow, propose/create/adopt a managed
  branch, continue a branch ending in -cf (or the repository's managed convention),
  continue its PR/MR, or execute a project task that references managed Git work.
  An exact PR/MR continuation request starts inspection even without a suffix.
  References trigger discovery, not write permission. Generic engineering requests
  and incidental branch mentions do not initiate managed work. Branch creation or
  adoption needs a human-approved proposal; merging needs separate explicit approval.
disable-model-invocation: false
---

# Git Workflow

Make approved changes easy to find, continue, review, and deliver. Own the Git
process; use engineering or the relevant domain workflow for implementation and
checks. One skill can manage many independent changes, normally one branch per
coherent change. No mandatory task, subagent, branch registry, or per-commit tag.

## Entry and authority

- **New work:** Explicit human intent starts a proposal, not branch creation.
  Ordinary engineering retains its normal local-commit behavior without invoking
  this workflow. Do not create or switch branches just because it is available.
- **Continue:** A request to continue a managed branch, its PR/MR, or a task pointing
  to it activates this workflow. `-cf` is a discovery cue, not approval evidence.
  A status/explanation/review request remains read-only; naming a branch alone is
  not an instruction to resume implementation.
- **Write permission:** Establish the human-approved association between exact
  repository, branch, objective, and allowed actions from the conversation or a
  sufficiently clear saved task/PR record. A recorded agreement must describe an
  actual human approval, not an agent's unanswered proposal. Author identity,
  suffix, labels, PR comments, and a branch's existence alone confer no authority.
  Reconcile conflicting or stale records; ask if approval cannot be established.
- **External branches:** Inspect freely within authorized access. Modification
  requires explicit scoped human permission; that permission is not adoption.
  Adoption requires a state/history audit and an explicitly approved proposal.
  Preserve the name when suitable; never rename somebody else's branch by default.
- **Limits:** Repository/workplace policies and narrower permissions prevail.
  No implicit merge, force-push, history rewrite, deployment, release, branch
  deletion, paid checks, security changes, tool installation, or subagent launch.
  These instructions guide agent behavior; they do not enforce host permissions.

## 1. Find the work and inspect reality

Follow the user's entry point:

| Reference | First action |
| --- | --- |
| Task or workstream | Read configured task/index and matching task first; use project-tasks for execution/authorized maintenance. Follow its managed branch/PR reference here. |
| Exact PR/MR | Retrieve that request in the identified repository first; then read linked task context needed for scope and continuation. |
| Exact branch | Resolve repository and exact local/remote ref, then its matching PR/MR and approval record. |
| Imprecise change | Bounded search of relevant tasks and open PRs/MRs by known project/terms; on miss inspect remote branches then accessible local refs. |

An index/search miss is not proof of absence. Inspect pagination when relevant;
report access/search limits. Ask when materially different candidates remain.
Check source and target repositories as well as branch names, especially forks.
Closed/merged requests require reconciliation, not automatic reopening or reuse.

Verify checkout/worktree, remote fetch AND push destinations, current branch/HEAD,
target, working tree/index, unpublished commits, and unfinished Git operations.
Inspect relevant branch/review/CI policy. Fetch only with permitted remote access;
otherwise identify freshness as unverified. Detect matching work before proposing
a duplicate. See [Git operations](references/git-operations.md) when selecting
commands or handling divergence, dirty trees, and worktrees.

## 2. Propose once; wait for approval

Recommend whether a branch is worthwhile. For creation or adoption, present a
compact agreement containing the following meaning, without a rigid form:

- Repository; starting ref/SHA and observed freshness; proposed branch and target.
- Objective/scope, consequential acceptance criteria, and intended checks.
- Maximum delivery: local edits/commits, push destination, draft PR/MR creation
  and maintenance, and marking ready when required pre-review checks pass.
- Continuity: permission to save the agreement and relevant progress in the
  existing project task through project-tasks, respecting local task-write gates.
- Material known publication effects, such as CI, previews, visibility or cost;
  merge remains a separate explicit decision.

Prefer `feature/<slug>-cf`, adapting prefixes/tickets to actual repository rules.
The human may approve the package or a narrower subset. Wait before creation or
adoption. An explicit approval of this exact proposal satisfies the gate; don't
ask again for routine steps. Material scope, target, or side-effect changes need
a new decision. Unknown consequential publication effects block publication,
not otherwise safe authorized local work.

## 3. Select the approved branch and work

Create/select the exact approved branch from the verified base. Choose a safe
checkout or separate worktree inside authorized locations; the human should not
have to switch manually. Do not silently stash/reset, force a checkout, or write
into another writer's worktree. Dirty state is not an automatic failure when
understood and safely separable; ambiguous ownership or overlapping changes stop
affected writes. Check for concurrent changes again at mutation boundaries.

Before first edits, including resumed work, show a brief verified context receipt:

> Repository, checkout path, branch → target, actual HEAD, allowed actions.

Implement and verify within the approved scope. Before editing, committing,
pushing or merging, recheck the affected live Git state against the agreement.
Stage only scoped paths/hunks; inspect the staged diff and preserve unrelated
staged changes. Use coherent checkpoints, not empty or ceremonial commits.
Engineering's local commit counts as a checkpoint here, not a second required
commit; the approved Git boundary governs managed work. Use commit delegation
only when requested/permitted and available, never as a dependency of this skill.

## 4. Checkpoint and publish

For substantial/multi-session work, prefer an authorized push and **draft PR/MR
after the first meaningful committed checkpoint**. Small work can open a normal
PR/MR once review-ready. Confirm destination, outgoing commits/diff, and publication
effects before pushing; use [provider operations](references/providers.md) for
host capabilities. Draft means unfinished, not private or free of CI effects.

Link the existing task using a locator accessible to intended readers. Keep the
PR description focused on objective, changes, checks/gaps, and current next step;
link detailed task decisions rather than copying them. Preserve others' PR text.
Without a task, a small PR may retain the approved scope/actions and enough next
action context itself. Save only genuine approvals, never secrets or inaccessible
private task contents into a wider-audience PR. Verify writes by reading back.

For substantial work, use project-tasks to retain approved scope, branch/target,
permissions, progress/check gaps, PR link, and next permitted action in ordinary
task prose under the starting agreement. If no task exists, propose one through
its owner; do not silently initialize a task system or mandate a task for every
change. Do not add a compulsory Delivery section or a second branch database.

Before declaring a published checkpoint resumable elsewhere, verify that the
needed continuation record is accessible there too. If tasks live in Git, include
authorized task/index updates in the scoped publication when feasible; otherwise
explicitly report them as local/unpublished. A pushed code commit does not publish
uncommitted task progress. Avoid an endless commit loop just to put a task's own
containing commit SHA inside that task; branch/PR references and Git history suffice.

Until a PR exists, the approved task or current conversation carries authority.
A branch alone is insufficient. If a fresh session cannot recover the approval,
ask again. Unpublished local work is recoverable only where that checkout exists;
cross-machine continuation requires authorized publication or another approved
transfer. Report this limit rather than promising portability.

## 5. Review, then integrate only on request

Mark ready only when the agreed implementation and mandatory pre-review checks
are complete, with limitations documented, and status maintenance is authorized.
Missing/failed required checks keep the change unfinished unless the human and
applicable policy explicitly revise the gate. Host ready status is not acceptance.

Review the actual current head SHA against the current target and agreed criteria.
Report changes, passed/failed/missing checks tied to their tested revision, relevant
regressions or before/after comparisons, and merge/revise/reject advice. Review-only
requests do not authorize fixes or posting host reviews/comments. Ratings are
optional advice and never override a failed mandatory gate.

**Merging always requires separate explicit human approval of the reviewed change
and target.** Revalidate current head, target, scope, required checks/reviews,
mergeability, and merge side effects. Any head change requires renewed review;
material differences or target changes require renewed human approval. Use a
provider expected-head/version guard that binds integration to the reviewed
revision. If the available operation cannot do that, stop automated integration
and explain the human-controlled host path; a separate head read does not close
the race. Respect the repository merge strategy. No protection bypass or implicit
auto-merge/queue enrollment; clarify deferred integration semantics when needed.
Update a branch from its target only under approved strategy, never by silent
rebase or merge. Failed checks/conflicts are not permission to rewrite history.

Read back the actual merged state and resulting revision. A queued/accepted
request is not a completed merge. Do not delete branches or deploy incidentally.

## Completion and repository setup

At material checkpoints or a blocker, give a short delivery receipt: repository,
branch/target, current SHA, PR/MR URL/state or absent, actual checks/gaps, allowed
next action, and task/PR continuation reference. Identify partial results; after
an uncertain remote mutation, inspect remote state before retrying. Never claim
provider access, installation, CI success, or fresh-session tests from static prose.

Repository defaults are optional. Only an authorized setup/refresh may maintain
the small owned AGENTS.md section; follow [routing](references/routing.md).
Using or publishing this skill does not configure repositories. Never put an
active branch list into standing guidance or overwrite another owner's section.
