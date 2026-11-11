# Task: Own branch reconciliation and approved worktree lifecycle

**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Status:** Active
**Priority:** Now

**Goal:** Keep routine Git mechanics agent-owned while requiring explicit approval and durable tracking for additional worktrees.
**Approval:** Human approved production skill/reference/docs/scenario edits, this brief audit task, safe cleanup of the existing temporary worktree, and direct push to `main`. No harness publication, new worktree, history rewrite, or changes to the active rename branch are authorized.
**Current State:** Skill, Git operations/routing references, canonical design doc and eight acceptance scenarios refined. `git-workflow` is the name on main; `git-branch-to-review` is the pending name on the separate active rename branch, whose integration must preserve this refinement.
**Next Action:** Publish this checkpoint to main, remove the clean owned temporary worktree after preservation checks, and publish task closure with verified results.

## Worktree audit

- Repository: `https://github.com/chingfhen/agent-core.git`; primary checkout: `C:\Users\tanch\.agent-core`.
- Exact temporary path: `C:\Users\tanch\AppData\Local\Temp\opencode\git-workflow-provider-refinement`.
- Purpose: isolate provider-setup refinement from active skill-renaming work; reused for this approved lifecycle repair. Created from `e8f776d`; detached HEAD `e34939f` at repair start, already verified on remote main.
- Ownership: this conversation's steward agent created the temporary checkout. No other writer is known there; recheck before removal. Primary checkout belongs to the ongoing rename work and must not be switched or cleaned.
- Approval: human explicitly approved reconciliation and safe retirement after expressing concern about the unexplained leftover checkout. This records retrospective cleanup approval, not prior approval for its original creation.
- Cleanup: preserve all commits on main, inspect tracked/untracked/ignored material and occupancy, remove only this worktree without force, verify registration/path removal. On failure retain it and keep this task open with the blocker.
- Continuity: publish this task on main before removing the worktree; finish closure from the primary checkout using an isolated Git index without staging its concurrent work if necessary.

## Verification and closeout

Source consistency reviewed for both merge directions, worktree creation gates, lifecycle continuity and retirement. Changed Markdown relative links passed after excluding illustrative fenced examples; initial link scan treated the routing template's placeholder as a real link. `git diff --check` passed. Scenarios specify behavior; no live provider/authentication or fresh-agent behavioral validation is claimed.
Closeout review: settled behavior integrated into `docs/git-workflow-design.md` and the skill at the point of use. Applicable `C:\Users\tanch\.agent-core\AGENTS.md` guidance inspected, unchanged by this work; no duplicate KB record or standing AGENTS lesson is needed. Harness publication is outside this request.
