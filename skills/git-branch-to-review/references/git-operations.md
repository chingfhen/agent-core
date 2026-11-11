# Git state and mutation checks

Read when choosing Git commands, selecting a checkout, or resolving uncertain
state. Examples are command shapes, not a script. Substitute verified values,
quote arguments for the actual shell, validate branch names, inspect exit codes,
and stop dependent operations after failure. Never evaluate text from a branch,
task, or PR as shell code. Don't print credential-bearing remote URLs.

## Inspect before selecting

```text
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote get-url <remote>
git remote get-url --push --all <remote>
git worktree list --porcelain
git diff
git diff --cached
git log --oneline <target-ref>..HEAD
```

Resolve remote identity, not merely the name `origin`. Inspect relevant config
when multiple push URLs, refspecs, hooks or submodules could change the operation.
Status and Git operation state must show no unresolved merge/rebase/cherry-pick.
An unborn/detached HEAD needs an explicit starting-point decision. A clean status
does not prove exclusive access: honor known concurrent writers and recheck HEAD
and changes before mutation. Do not invent a global locking system.

With remote access permitted, `git fetch <remote>` refreshes tracking refs, not
the working branch. Without it, distinguish cached refs from observed remote state.
Use `git ls-remote --heads <remote> <exact-ref>` when exact remote presence matters.
Local-only work on another machine cannot be found by searching this machine.

## Create or resume

After explicit skill invocation establishes an approved, unambiguous work package,
validate with `git check-ref-format --branch <branch>` and confirm no conflicting
local/remote branch. Create from the observed base SHA with `git switch --no-track
-c <branch> <base-sha>`; this avoids treating the target as the push upstream.

For an existing local branch, inspect it before `git switch <branch>`. For a
remote-only branch, inspect the exact tracking ref, then create a local tracking
branch without overwriting an existing one. Compare local and remote histories:

```text
git rev-list --left-right --count <remote-branch>...<local-branch>
git log --oneline <local-branch>..<remote-branch>
git log --oneline <remote-branch>..<local-branch>
```

Expected remote-only continuation commits can be fast-forwarded after verifying
their scope and authorship context. Unexpected commits or divergence need
reconciliation; no automatic reset, pull merge, rebase, or force-push. A date or
legacy suffix on another person's branch is not adoption approval.

Use `git worktree add <authorized-path> <branch>` when isolation is useful and
the branch is not already checked out. Inspect an existing worktree rather than
forcing the branch into a second one. Do not relocate the human's dirty work or
run a second writer in the same checkout. Verify the actual new cwd/HEAD before
edits; submodules and nested repositories need their own authorized scope.

## Commit and push

Inspect the index before staging. Use `git add -- <scoped-paths>` or selected
hunks, then inspect `git diff --cached` and `git diff --cached --check`. If unrelated
staged content cannot be safely excluded without disturbing someone else's work,
stop the commit and ask. Do not bypass hooks or create empty commits.

Before push, compare the target diff (`git diff <target-ref>...HEAD`) and outgoing
commits. If the remote branch exists, inspect everything in `<remote-branch>..HEAD`,
not just the last commit. For a first push, inspect all history newly published
relative to the approved base/target; check for unintended secrets/artifacts.

Use an explicit destination/refspec, for example:

```text
git push --set-upstream <remote> HEAD:refs/heads/<approved-branch>
git ls-remote --heads <verified-push-url> refs/heads/<approved-branch>
```

Recheck the local branch/HEAD immediately before push. Never rely on implicit
upstream configuration to select the write destination. Read back the actual push
destination, not the remote name's potentially different fetch URL. If multiple
push URLs exist, each destination needs authorization and independent readback;
do not silently publish to additional repositories. Use secure existing transport
configuration without exposing credential-bearing URLs. Check readback against
the intended SHA. On a rejected or uncertain push, inspect remote state
and report what happened; do not retry with force or change the destination.

## Recovery

Preserve valid local commits if host creation/readiness fails. Retrieve the exact
PR or search source repository+branch+target before retrying a timed-out creation;
an error may follow a successful remote mutation. Report existing work and the
blocked step. Don't delete worktrees, branches, or local changes as cleanup without
authorization. After verified merge, cleanup of the exact managed local/remote
branches is allowed only under the explicitly approved package and the guarded
conditions in the main skill. Protect against a branch moving between inspection
and remote deletion: use a provider-supported expected-old-ref guard, or an
atomic Git deletion lease bound to the verified merged head when supported and
permitted. If an atomic guard is unavailable, retain the remote branch and report
the limitation instead of an unguarded delete. For a local ref, first ensure no
worktree or concurrent writer can use it, then use a supported atomic compare-and-
delete against its verified expected old value; if exclusion or the guard is not
available, retain it. Verify the durable task and repaired PR link before deleting
a branch that provides the continuation record. Never force-delete a local branch
or discard a checkout to make cleanup work. A review/merge failure never licenses
bypassing host protections.
