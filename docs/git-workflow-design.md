---
title: Git Workflow — Approved Design Direction
description: Intended human-controlled Git branch, review, integration, and continuation contract for a future personal Agent Core skill; not yet implemented.
updated: 2026-11-08
---

# Git Workflow — Approved Design Direction

## Read First

- **Status:** Approved design direction for a **future** `git-workflow` skill. This document is not evidence that the skill, its managed guidance, provider integrations, checks, or branch conventions have been implemented or installed.
- **Audience:** Agent Core is personally owned and used by one human. The proposed skill should nonetheless work safely in repositories shared with colleagues, including projects using GitHub, GitLab, or Bitbucket. Repository and organizational policies take precedence.
- **Core boundary:** Creating or adopting a managed branch requires explicit human approval. Once managed ownership and scope are verified, the agent may continue approved implementation and local commits autonomously. **Unmanaged branches are read-only by default for writes. Merging always requires fresh, explicit human approval.**
- **No universal branch requirement:** Ordinary engineering, discussions, and read-only reviews do not automatically enter this workflow. Starting a new managed branch is explicitly requested/approved; later references to a verified managed branch or linked PR/MR activate it when Git work is relevant.

## Distinct Responsibilities

| Owner/source | Authority |
| --- | --- |
| `git-workflow` (future skill) | Propose/select approved Git strategy, verify working state, create/resume branches, commit, publish/review/integrate within permissions, provide concise delivery receipt |
| Repository `AGENTS.md` Git Workflow section (future, opt-in) | Stable repo-specific branch naming/targets, activation and permission rules, and pointers to existing repository policy. **Not** an active-branch registry |
| Git host + Git objects | Actual branch/commit, pull/merge request, reviews, pipeline/check results, merge history |
| `project-tasks` when applicable | Work objective, decisions, approved scope, acceptance, progress, unresolved questions, next action, and context for fresh sessions |
| Existing project docs / domain checks | Detailed release/CI policy, implementation contracts and applicable verification methodology |

A Project Task is **preferred for substantial or multi-session work** and leads when the user references a saved task. An existing Task can link to a branch or PR/MR in ordinary status/context prose; the PR/MR can link back. No new mandatory `Delivery` section or parallel branch database. A small self-contained change may use its PR/MR as its only durable change record. An MR does not automatically preserve the rationale and pending work that Project Tasks is designed to retain.

## Invocation and Managed Ownership

1. **New work:** “Implement this feature” remains normal engineering; do not automatically create or switch to a managed branch. “Use git-workflow,” “create a managed branch,” or an equivalent clear request initiates the branch proposal and approval flow.
2. **Established work:** An explicit managed branch reference (for example `feature/evaluation-pipeline-cf`), its associated PR/MR, or a saved task leading to it activates Git Workflow as needed. Discovering the candidate does not confer permission.
3. **Branch naming:** Prefer unobtrusive `feature/<descriptive-slug>-cf` where allowed. Preserve the repository's required prefix/ticket scheme; do not force `agent/`, rename existing branches, or imply AI-generated authorship. Other prefixes are possible under local policy.
4. **Ownership evidence:** Suffix matching is only a discovery hint, **not** proof. Verify the human-approved managed association, exact repository/branch, objective, allowed actions, and current state using available conversation and durable task/PR/MR records. If approval/scope cannot be established for a fresh session, stop before writing and ask.
5. **Managed versus external:** Work autonomously **only within the verified approved scope** on an established managed branch. Unmanaged branches may be inspected read-only. Editing an external branch requires an explicit scoped instruction/approval; it does not silently become managed. Explicit adoption of an existing branch is permitted only after a human-approved proposal and state inspection.
6. **No per-commit tags/codewords:** Branch identity, commit SHAs, host history, and any existing ticket conventions suffice. Git tags are not used as routine provenance labels.

## Starting Agreement and Permissions

Before creating a managed branch, propose a small human-reviewable agreement including: repository, starting ref and its observed freshness, proposed branch, integration target, why this branch is appropriate, work objective, consequential acceptance criteria, proposed verification approach, and **maximum delivery boundary**. The latter distinguishes local branch/commits, remote push, draft PR/MR creation, and subsequent integration. Human may approve these proposed steps together once. Branch creation remains human-approved, never automatic.

Within that boundary, ordinary implementation, tests, scoped local commits, authorized publication and PR/MR maintenance can proceed without repetitive approvals. No implicit permission to merge, deploy, force-push, rewrite history, expand scope, access privileged systems, run paid checks, or alter project security settings. Existing review/deploy rules and workplace restrictions are stronger where applicable.

## Branch Lifecycle and Durable Output

1. Inspect current checkout, remotes, expected base, working tree, unpublished commits and project policy. Check for matching existing managed work and duplicate branches. On ambiguity, conflicts or concurrent writers, preserve work and stop before unsafe mutation.
2. After approval, create or select the exact approved branch (or safe separate worktree); inspect actual branch/HEAD before edits and commits. The human is **not** expected to switch branches manually.
3. Implement and verify using existing engineering/domain practices. Stage only task-scoped changes; preserve unrelated work; inspect outgoing commits/diff before an approved push.
4. For short changes, publish/open a review-ready PR/MR when implementation and pre-review checks are done, as authorized.
5. For substantial/multi-session changes, **prefer** an authorized remote checkpoint and early draft PR/MR after the first meaningful committed work, provided push/MR CI, secrets, deployment, cost and preview side effects are safe. Draft means work in progress, **not private**. An MR is not required at the instant a branch is created.
6. Before marking ready for review, the agreed implementation and required pre-review checks must be complete, with important remaining limitations stated. Mark-ready is a host review state where supported; **not** a merge authorization or proof of acceptance.
7. Review against agreed success criteria using the latest exact head commit and current target. Present passed/failed/missing checks, relevant before/after comparisons, regressions, meaningful risks, optional advisory ratings and a merge/revise/reject recommendation. Critical required gates cannot be overridden by a favorable rating.
8. On explicit human merge approval, revalidate branch/head, mergeability, required checks and scope; stop if a material revision invalidates the decision. Merge only the authorized target/change and report the resulting integrated revision. Production deployment/release remains a separate boundary.
9. After material checkpoints report a **delivery receipt**: repository, branch, target, actual commit SHA, PR/MR link/status (or absent), verified checks and gaps, authorized next action, and where continuation context lives. Reconcile an existing task when its owner authorizes maintenance; do not silently change unrelated task files or delete branches.

## Deterministic Fresh-Session Discovery

**Use the user's reference first, not a blanket MR search:**

- Task identified: Project Tasks finds the configured task/index first. Read approved intent/next action and any branch/PR reference; Git Workflow then checks the live change.
- Exact PR/MR referenced: Git Workflow retrieves it first, then consults any associated task when needed.
- Exact branch referenced: Resolve the repository, check branch and its matching PR/MR, and verify managed approval and scope.
- Ambiguous natural-language change: Search relevant task/index and open PRs/MRs using the known project and terms; reconcile candidates before writing. On MR miss, check remote branches then the current local checkout (if available).
- No task and no PR/MR: A remote branch offers Git history but may not preserve authorization, pending acceptance or next action. A local-only branch is not portable to another machine. If continuity evidence is insufficient, request direction rather than infer write permission.

At a resumable checkpoint, substantial work should normally retain its approved decisions and next action in Project Tasks, with the corresponding PR/MR referencing it. Small work may use a sufficiently informative PR/MR description. An approved remote publication is needed for cross-machine branch recovery; absent permissions must be reported, not bypassed.

**Before writing, committing, pushing and integrating**, verify actual repository/remotes, branch/worktree, target, HEAD/outgoing changes, clean-or-understood uncommitted work and authorized scope. Report the verified working context before first edits in a resumed session. Do not silently stash/reset/rebase/force-push or trample another writer's checkout. Worktrees are a useful optional isolation technique, not a universal requirement.

## Verification and Portability

- No general-purpose verification skill is required for v1. Use relevant existing engineering, documentation, ML/evaluation, UI, infrastructure and project CI checks. Early acceptance criteria are human-approved at the consequential level; the agent chooses proportionate concrete checks, surfacing material changes or missing gates.
- Commands such as `git status --short --branch`, `git remote -v`, `git fetch` (when permitted), `git branch --show-current`, `git diff`, `git log`, `git switch`, `git add <scoped-path>`, `git commit` and `git push` can form a *short verified-operation reference*, not a rigid script. Verify actual remote/local status and unknown push side effects before using commands. Separate provider adapters for GitHub PR, GitLab MR, and Bitbucket PR creation, readback and review states; do not assume any particular CLI/provider API, version, credential, or draft capability is present.
- Skill instructions are an **agent-behavior boundary**, not permission enforcement. Actual authorization must also be consistent with host credentials, branch protections, repository policy, and (for employer repositories) approved use of tools and data.
- No automatic subagent dependency, per-commit tag scheme, centralized branch registry, background bot, general release authority or new task-file metadata schema.

## Related Material

- [Skill design principles](skill-design-guide.md) — determine independent invocation, scope and future publication.
- [Workspace configuration](workspace-configuration.md) — task/doc ownership and managed `AGENTS.md` routing patterns.
- [Agent Core task index](../tasks/INDEX.md) — unfinished implementation work. The Git Workflow design/implementation task holds open decisions and the next permitted action.
- [AdReadyClips agent delivery policy](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/ai_video_saas/docs/agent-workflow.md) — existing project-specific design to reuse, not duplicate or overwrite.
- [AdReadyClips MR adoption task](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/tasks/2026-10-10__enable-agent-mr-delivery-workflow-bookmark.md) — on-hold provider-side rollout; distinct from building the portable skill.
