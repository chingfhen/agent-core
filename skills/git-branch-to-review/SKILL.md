---
name: git-branch-to-review
description: >
  Manage explicitly requested Git branch-to-review delivery end to end. Start a new
  managed branch only when the human invokes or asks to use git-branch-to-review. Use for
  continuation, maintenance, status, or merge of a known managed branch, its PR/MR,
  or linked project task. Branch/date references cue discovery, not ownership or write
  permission. Generic engineering does not start this workflow; merge requires a
  separate explicit human instruction.
disable-model-invocation: false
---

# Git Workflow

Manage the approved branch, task and review request as one coherent delivery. The
PR/MR is the human's review surface; the project task is continuation memory. Use
ordinary authorized execution or the relevant domain workflow for implementation and checks. One
branch normally serves one coherent change; no branch registry or per-commit tags.

## Entry and authority

- **New work:** Only explicit human invocation or a request to use `git-branch-to-review`
  starts a new managed branch. A clear request for identified work and repository,
  with applicable defaults and permissions established, authorizes the normal
  package below—including narrowly scoped post-merge task bookkeeping and safe
  cleanup of this managed branch—without a second ceremonial approval, unless
  the human narrows it or applicable rules require otherwise. If scope, target, access,
  cost or material effects are unclear, ask before the affected action. Ordinary
  engineering does not start this workflow or create a managed branch.
- **Continue:** A request to continue, revise, inspect, pause, close or merge a known
  managed branch, its PR/MR, or a task pointing to it activates this workflow. A
  date or legacy `-cf` is a discovery cue, not approval or ownership evidence.
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
  No implicit merge, force-push, history rewrite, deployment, release, unsafe or
  unapproved branch deletion, paid checks, security changes, tool installation, or
  subagent launch. Post-merge cleanup is allowed only within the explicitly
  authorized package and the guarded conditions below.
  These instructions guide agent behavior; they do not enforce host permissions.
- **Provider setup:** Reuse working authorized host access first. If necessary,
  propose the appropriate provider tool and request yes/no installation approval;
  after approval handle setup and initiate authentication when possible. The human
  completes any required interactive authorization. Follow the provider reference;
  never request secrets in chat or bypass policy.

## 1. Find the work and inspect reality

Follow the user's entry point:

| Reference | First action |
| --- | --- |
| Task or workstream | Read configured task/index and matching task first; use manage-project-tasks for execution/authorized maintenance. Follow its managed branch/PR reference here. |
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

## 2. Agree scope once

Resolve the following as one compact agreement, without a rigid form. A direct,
clear `use git-branch-to-review for [work]` request accepts the normal package when its
repository, objective, target, permissions and material effects are established;
do not demand a redundant approval. When they are not established, propose the
missing terms and wait. External-branch adoption still needs explicit approval.
Surface the standard post-merge local/remote branch cleanup in the scope receipt
and make its opt-out clear; do not hide deletion in a generic delivery label.

- Repository; starting ref/SHA and observed freshness; proposed branch and target.
- Objective/scope, consequential acceptance criteria, and intended checks.
- Maximum delivery: local edits/commits, push destination, draft PR/MR creation
  and maintenance, and marking ready when required pre-review checks pass.
- Continuity: create or maintain the matching project task and index through
  manage-project-tasks, including post-merge bookkeeping, within applicable write gates.
- Cleanup: after an approved and verified merge, safely delete the exact managed
  remote and local branches under the conditions below; the explicit, clear skill
  invocation accepts this standard term unless the human or policy narrows it.
- Material known publication effects, such as CI, previews, visibility or cost;
  merge remains a separate explicit decision.

The human may narrow the package. Material scope, target, or side-effect changes
need a new decision. Unknown consequential publication effects block publication,
not otherwise safe authorized local work. Human approval of a merge is separate.

Prefer `YYYYMMDD-short-descriptive-slug` using the local project date; use a small
collision suffix if needed. Adapt required prefixes/tickets to repository rules.
Do not add `-cf` to new names or rename existing branches merely to conform. Dates
and legacy suffixes help discovery, never establish authority.

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
A local commit counts as a checkpoint here, not a second required
commit; the approved Git boundary governs managed work. Use commit delegation
only when requested/permitted and available, never as a dependency of this skill.
Routine commits authorized by a managed-work request do not by themselves invoke
`commit-changes`; when the human explicitly asks to commit, honor that
skill's trigger without inferring permission to spawn another agent.
Before handing over for review or pause, account for all agent-created changes:
publish the scoped, verified work and task state when authorized, or report exactly
what remains local, why and how to resume. Never label a dirty or unpushed state
clean. Preserve pre-existing or ambiguous work; do not reset, stash, discard or
include it merely to make the checkout clean. A missing optional commit helper must
not by itself strand authorized work: follow the commit skill's scoped instructions,
without inventing an agent or exceeding delegation permissions.

## 4. Task, checkpoint and publish

For substantial/multi-session work, prefer an authorized push and **draft PR/MR
after the first meaningful committed checkpoint**. Small work can open a normal
PR/MR once review-ready. Confirm destination, outgoing commits/diff, and publication
effects before pushing; use [provider operations](references/providers.md) for
host capabilities. Draft means unfinished, not private or free of CI effects.

Every managed PR/MR, including a draft, must link an existing or new project task,
unless the human explicitly says no task is needed. If the agent thinks a
task unnecessary, ask before opting out. Reuse a matching task; otherwise load
manage-project-tasks and create one in the confirmed project task surface. The approved
package includes its task/index maintenance when local rules permit; stricter opt-in
rules prevail. If the destination, permission, or accessible reference is missing,
ask or report the blocker before creating the PR/MR; do not invent a task root or
link. Preflight this before editing where possible. No new task schema or registry.

The task preserves the actual human approval, scope, branch/target, progress,
checks/gaps, and next permitted action. The PR/MR links it and is the human's
primary review surface. Use the concise format in [review presentation](references/review-presentation.md):
purpose, before/after, changed areas, consequential effects/risks, verification and
gaps, task link, state, and next action. Surface consequential changes in the PR,
not only in the task. On revisions summarize what changed since the prior review.
Preserve others' PR text; do not expose secrets or restricted task contents. Verify
host writes by reading back.

Before declaring a checkpoint resumable elsewhere, verify that its task and index
are accessible there too. If they live on the review branch, publish them with the
approved work and link to that accessible branch version; after merge, verify the
durable target and repair the link before deleting any branch needed for access.
A pushed code commit does not publish uncommitted task progress. Report partial or
local-only state accurately; avoid an endless commit loop to put a task's containing
SHA inside itself.

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
the race. A head guard does not bind the target: revalidate the target and host
protections, re-review material movement, and disclose any residual target race.
If exact-target consistency is required but the host cannot guarantee it, stop
automated integration and explain the permitted human-controlled path. Respect
the repository merge strategy. No protection bypass or implicit
auto-merge/queue enrollment; clarify deferred integration semantics when needed.
Update a branch from its target only under approved strategy, never by silent
rebase or merge. Failed checks/conflicts are not permission to rewrite history.

Read back the actual merged state and resulting revision. A queued/accepted
request is not a completed merge. Update the task/index after verified merge:
close only if the outcome is complete; otherwise record the remaining work. When
explicitly included in the approved package and permitted by project/host policy,
publish a narrowly scoped task/index-only post-merge update to the configured
task store, including a direct target-branch commit if authorized. Recheck the
target, index and concurrent changes; no code, unrelated docs, force push or
protection bypass. If this is blocked, preserve the result, report the stale task
and the exact unblock; never claim completion or create an unsolicited branch.

After a verified merge, delete the exact local and remote managed branches only if
that cleanup was explicitly authorized, current host and local refs still match the
merged reviewed head, no further work is present, and no other checkout or writer
would be disturbed. If a task or branch-hosted continuation record exists, first
verify the durable record and repaired PR link before deleting a branch needed for
access; if this cannot be established, retain that branch. For a human-approved
task opt-out, record the exception and verify no needed continuation depends on the
branch. Verify the provider's actual merge strategy, including squash or rebase,
rather than assuming ancestry proves equivalence. A checked-out branch
may be switched away from only when safe and authorized; never force or discard.
Guard both local and remote ref deletion against concurrent movement as described
in [Git operations](references/git-operations.md); retain the affected ref if
safe atomic deletion or concurrent-writer exclusion cannot be established.
Protect unmerged/closed work, unexpected commits, dirty or occupied checkouts, and
external branches. On uncertainty or unavailable permission, retain and report
the branch; never infer deletion of unmerged work from permission to close a PR.
Do not deploy incidentally.

## Completion and repository setup

At material checkpoints or a blocker, give a short delivery receipt: a clickable
actual host PR/MR link, source branch → target, current SHA and state, concise
before/after, checks/gaps, task reference, and explicit local/unpushed status. Give
the human the next branch-based cue: `continue [branch]`, `status of [branch]`,
`pause [branch]`, `merge [branch] into [target]`, or `close [branch] without
merging`. These are examples, not magic words. A PR is the one surface the human
needs to inspect; suggest its Files changed / Changes page, not a required desktop
app. Report a missing link or partial state instead of inventing one. After an
uncertain remote mutation, inspect remote state before retrying.

Repository defaults are optional. Only an authorized setup/refresh may maintain
the small owned AGENTS.md section; follow [routing](references/routing.md).
Using or publishing this skill does not configure repositories. Never put an
active branch list into standing guidance or overwrite another owner's section.
