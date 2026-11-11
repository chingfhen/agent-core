---
title: Git Workflow — Design and Operating Contract
description: Human-controlled Git branch, review, integration, and continuation contract for the personal Git Workflow skill.
updated: 2026-11-11
---

# Git Workflow — Design and Operating Contract

## Read First

- **Source:** [git-workflow](../skills/git-workflow/SKILL.md) is the behavior contract and is declared in `personal-skills.toml`. Source, harness publication, consumer-repository setup, and observed behavior are separate. The [original delivery task](../tasks/2026-11/git-workflow/2026-11-08__design-implement-and-validate-git-workflow.md) records historical validation, not validation of later revisions.
- **Audience:** Agent Core is personally owned and used by one human. The skill also respects repositories shared with colleagues, including projects using GitHub, GitLab, or Bitbucket. Repository and organizational policies take precedence.
- **Core boundary:** New managed branches start only on explicit `git-workflow` invocation. Clear authorized work and established defaults permit the normal package without a second ceremonial approval; ambiguous scope or effects require a decision. External branch adoption and new worktrees require explicit approval. **Integration into the target requires separate explicit human instruction; necessary target-to-managed-branch maintenance is agent-owned.**
- **No universal branch requirement:** Ordinary engineering, discussions, and read-only reviews do not automatically enter this workflow. Starting a new managed branch is explicitly requested/approved; later references to a verified managed branch or linked PR/MR activate it when Git work is relevant.

## Distinct Responsibilities

| Owner/source | Authority |
| --- | --- |
| `git-workflow` | Manage explicitly requested branch/task/PR delivery, verification, human review, integration and guarded cleanup within permissions |
| Repository `AGENTS.md` Git Workflow section (opt-in) | Stable repo-specific branch naming/targets, activation and permission rules, and pointers to existing repository policy. **Not** an active-branch registry |
| Git host + Git objects | Actual branch/commit, pull/merge request, reviews, pipeline/check results, merge history |
| `project-tasks` | Work objective, decisions, approved scope, acceptance, progress, unresolved questions, next action, and context for fresh sessions |
| Existing project docs / domain checks | Detailed release/CI policy, implementation contracts and applicable verification methodology |

A project task is the default for **every managed PR/MR, including drafts**. Reuse or create it through project-tasks; only the human may opt out. It preserves continuation, while the PR is the human's review surface. Link an accessible task version before merge and its durable destination afterward. No mandatory `Delivery` section or parallel branch registry. Respect narrower project task-write gates.

## Invocation and Managed Ownership

1. **New work:** “Implement this feature” remains ordinary engineering. A new managed branch starts only on a direct request to use `git-workflow`; a clear, sufficiently scoped request can authorize its normal delivery package without a second ceremonial approval.
2. **Established work:** “Continue/status/pause/merge [branch]” for known managed work activates discovery. A PR/MR or saved task remains a valid alternate entry. Read-only requests stay read-only.
3. **Branch naming:** Prefer `YYYYMMDD-descriptive-slug` using the project's local date, with a small collision suffix. Adapt to required prefixes/tickets and retain existing branch names.
4. **Ownership evidence:** A date or legacy `-cf` is only a discovery hint, **not** proof. Verify the human-approved managed association, exact repository/branch, objective, allowed actions, and current state using conversation and durable task/PR/MR records. Ask if approval/scope cannot be recovered.
5. **Managed versus external:** Work autonomously **only within the verified approved scope** on an established managed branch. Unmanaged branches may be inspected read-only. Editing an external branch requires an explicit scoped instruction/approval; it does not silently become managed. Explicit adoption of an existing branch is permitted only after a human-approved proposal and state inspection.
6. **No per-commit tags/codewords:** Branch identity, commit SHAs, host history, and any existing ticket conventions suffice. Git tags are not used as routine provenance labels.

## Starting Agreement and Permissions

Resolve repository, starting ref and freshness, objective, target, checks, delivery, task continuity and post-merge cleanup. When an explicit `git-workflow` request supplies sufficient scope and established defaults, it authorizes the normal package once. Ask before an affected action when permissions or material effects remain unclear; adoption still needs explicit approval.

The package includes related project-task/index maintenance where local policy permits. Record actual approval and scope. A managed PR/MR requires a linked task unless the human explicitly opts out; if the agent thinks one unnecessary, ask. If the destination, permission or accessible link is unavailable, report the blocker before request creation; do not invent a task root. Before a PR exists, the task or current conversation carries authority.

Within that boundary, ordinary implementation, tests, scoped commits, publication and PR maintenance proceed without repeated approvals. Necessary target-to-branch updates use history-preserving merge where policy permits. Agents reconcile established intentions and verify combined behavior, asking only about unresolved meaning, scope or authority rather than conflict markers alone. A missing optional commit specialist must not strand authorized work; use the commit skill's fallback when delegation was not explicitly required. No implicit target integration, deployment, force-push, history rewrite, scope expansion, paid check, or security change. Project and workplace restrictions prevail.

## Branch Lifecycle and Durable Output

1. Inspect current checkout, remotes, expected base, working tree, unpublished commits and project policy. Check for matching existing managed work and duplicate branches. On ambiguity, conflicts or concurrent writers, preserve work and stop before unsafe mutation.
2. After explicit invocation and a sufficiently clear approved package, create or select the branch in a safe existing checkout. A new worktree is an explicitly approved exception, recorded in the linked task before creation. Inspect actual branch/HEAD before edits and commits. The human is **not** expected to switch manually or manage the extra checkout.
3. Implement and verify using existing engineering/domain practices. Stage only task-scoped changes; preserve unrelated work; inspect outgoing commits/diff before an approved push.
4. Publish an authorized draft checkpoint after meaningful committed work when side effects are safe; link the accessible task unless the human opted out. A short finished change can proceed to review-ready state after required checks. Draft means work in progress, **not private**.
5. Make the host PR/MR the human review surface using the [review format](../skills/git-workflow/references/review-presentation.md): purpose, before/after, changes, material effects/risks, checks/gaps, task link and next action. Provide the actual clickable host URL and branch → target; do not hide consequences in the task.
6. Before marking ready for review, the agreed implementation and required pre-review checks must be complete, with important remaining limitations stated. Mark-ready is a host review state where supported; **not** a merge authorization or proof of acceptance.
7. Review against agreed success criteria using the latest exact head commit and current target. Present passed/failed/missing checks, relevant before/after comparisons, regressions, meaningful risks, optional advisory ratings and a merge/revise/reject recommendation. Critical required gates cannot be overridden by a favorable rating.
8. On explicit human merge approval, revalidate branch/head, mergeability, required checks and scope; stop if a material revision invalidates the decision. Merge only the authorized target/change and report the resulting integrated revision. Production deployment/release remains a separate boundary.
9. After a verified merge, reconcile the task/index with the real outcome and safely remove the exact managed remote/local branches if that cleanup was explicitly authorized and guarded checks pass. Task-only post-merge publication to the configured store may be included in the approved package when allowed; never bypass protection or include unrelated changes. Report any stale state or retained branch.

## Deterministic Fresh-Session Discovery

**Use the user's reference first, not a blanket MR search:**

- Task identified: Project Tasks finds the configured task/index first. Read approved intent/next action and any branch/PR reference; Git Workflow then checks the live change.
- Exact PR/MR referenced: Git Workflow retrieves it first, then consults any associated task when needed.
- Exact branch referenced: Resolve the repository, check branch and its matching PR/MR, and verify managed approval and scope.
- Ambiguous natural-language change: Search relevant task/index and open PRs/MRs using the known project and terms; reconcile candidates before writing. On MR miss, check remote branches then the current local checkout (if available).
- No task and no PR/MR: A remote branch offers Git history but may not preserve authorization, pending acceptance or next action. A local-only branch is not portable to another machine. If continuity evidence is insufficient, request direction rather than infer write permission. A human may explicitly opt out of the draft-task rule.

At a resumable checkpoint, the linked project task preserves approved decisions and next action unless the human opted out. Verify the task and PR are accessible in a fresh session; branch-local tasks need a link that survives or is reconciled after merge. A PR summary is not a substitute for an inaccessible task. Report absent publication permissions, not bypasses.

**Before writing, committing, pushing and integrating**, verify actual repository/remotes, branch/worktree, target, HEAD/outgoing changes, clean-or-understood uncommitted work and authorized scope. Report the verified working context before first edits in a resumed session. Do not silently stash/reset/rebase/force-push or trample another writer's checkout.

Worktree approval includes agent-owned reconciliation and safe retirement. Its task records exact path, repository, branch/base, human approval, owner, preservation destination and cleanup plan, even if the human previously opted out of a PR task. If task permission or tracking is unavailable, do not create the worktree. At pause, record remaining work and the next permitted action; a new agent checks the record against live state. At completion, preserve commits and continuation outside the checkout, inspect tracked/untracked/ignored material and active use, remove only the clean owned checkout without force, and verify removal before task closure. Worktree cleanup does not grant branch deletion or permission to discard unmerged work. Retain a blocked checkout with its exact reason and next action; do not transfer unexplained cleanup to the human.

## Verification and Portability

- No general-purpose verification skill is required for v1. Use relevant existing engineering, documentation, ML/evaluation, UI, infrastructure and project CI checks. Early acceptance criteria are human-approved at the consequential level; the agent chooses proportionate concrete checks, surfacing material changes or missing gates.
- Commands such as `git status --short --branch`, `git remote -v`, `git fetch` (when permitted), `git branch --show-current`, `git diff`, `git log`, `git switch`, `git add <scoped-path>`, `git commit` and `git push` can form a *short verified-operation reference*, not a rigid script. Verify actual remote/local status and unknown push side effects before using commands. Separate provider adapters for GitHub PR, GitLab MR, and Bitbucket PR creation, readback and review states; do not assume any particular CLI/provider API, version, credential, or draft capability is present.
- Reuse working authorized host access. When unavailable, the agent proposes a suitable provider tool for yes/no installation approval, performs permitted setup, and initiates interactive sign-in when possible; the human handles required browser authorization. Prefer `gh` for GitHub if a tool is needed. Policy and security boundaries apply; detailed setup and fallback rules live in the [provider reference](../skills/git-workflow/references/providers.md).
- Skill instructions are an **agent-behavior boundary**, not permission enforcement. Actual authorization must also be consistent with host credentials, branch protections, repository policy, and (for employer repositories) approved use of tools and data.
- No automatic subagent dependency, per-commit tag scheme, centralized branch registry, background bot, general release authority or new task-file metadata schema.

## Use and Installation

- Start: “Use git-workflow for this change.” A clear request with established defaults authorizes routine managed delivery; ask only about missing material terms.
- Resume: “Continue `20261110-login-fix`.” Status, pause, revise, merge and close cues may likewise identify the branch. Legacy branches and task/PR references remain usable.
- Before edits: expect the verified repository, checkout path, branch/target, HEAD, and allowed actions.
- Review: expect a direct host link, exact revision, before/after, checks/gaps and a separate “merge [branch] into [target]” decision.
- Configure defaults only on request using the skill's [routing contract](../skills/git-workflow/references/routing.md). Source publication does not install a repository guidance block.

After separately approved integration into the clean canonical checkout, explicitly
authorize publication to the chosen harness: `agent-core sync` for Pi,
`agent-core sync --harness opencode`, or `agent-core sync --harness devin`.
These publish the selected harness's declared resource set, not just this skill.
Verify the installed copy and actual harness discovery in a fresh session. Do not
hand-copy the candidate or infer installation from manifest membership. See the
[operating manual](agent-core-operating-manual.md) for source validation and recovery.

[Acceptance scenarios](../tests/git-workflow-scenarios.md) distinguish static checks,
isolated Git trials, fresh-agent source-loading trials, and live host/harness tests.
Documentation-backed provider procedures are not proof of live provider operation.

## Related Material

- [Skill design principles](skill-design-guide.md) — determine independent invocation, scope and future publication.
- [Workspace configuration](workspace-configuration.md) — task/doc ownership and managed `AGENTS.md` routing patterns.
- [Agent Core task index](../tasks/INDEX.md) — unfinished work; the delivery task records actual results and next permitted action.
- [AdReadyClips agent delivery policy](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/ai_video_saas/docs/agent-workflow.md) — existing project-specific design to reuse, not duplicate or overwrite.
- [AdReadyClips MR adoption task](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/tasks/2026-10-10__enable-agent-mr-delivery-workflow-bookmark.md) — on-hold provider-side rollout; distinct from building the portable skill.
