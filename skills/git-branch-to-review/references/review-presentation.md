# Managed PR/MR review presentation

Read when creating or updating a managed draft or presenting a review. The host's
actual PR/MR URL is the human's single review entry point; do not require a desktop
app, task-file inspection, or guessing which branches to compare. Retrieve and
read back the real link from the provider; if unavailable, report that limitation.
Host access controls still apply.

Use a concise, consistent description in GitHub, GitLab or Bitbucket. Adapt labels
to host capabilities and preserve existing third-party text. Include all material
information directly in the request; link deeper continuation to the task without
making the human follow it to assess the change:

```markdown
## Purpose
What problem is being solved and why.

## Before → After
The meaningful behavior, experience or state change.

## What changed
Key areas and the host's complete file diff. Do not hide material scope changes.

## Important effects and risks
Consequential data, security, privacy, cost, deployment, compatibility,
migration, recovery and user-visible effects; say none identified when appropriate.

## Verification
Actual checks and results, failed or missing checks, and remaining uncertainty.

## Continuation
Task: accessible task link, unless the human explicitly opted out.
State: work in progress / ready for human review; meaningful unfinished work.
Next: branch-based cue for revision, pause, or explicitly approved merge.
```

On a revised head, add a concise **Changed since your review** section and point
out changes affecting the earlier decision. The human reviews the actual current
head and target; a score, draft status, or favorable prose is not approval. Record
the revision tested when it matters. Preserve differences between preview, draft,
ready, approved and merged; never present pending/queued integration as complete.

The agent's accompanying message is a short receipt: direct clickable PR/MR URL,
source → target, head, before/after, checks/gaps, task reference, and explicit
uncommitted/unpushed state. Suggest the host's **Files changed / Changes** view and
branch-name cues such as “revise [branch]” or “merge [branch] into [target].”
Do not make the human inspect local Git state to understand the handoff. If task
and PR have different audiences, link only what their access permits and do not
copy restricted content. A branch-local task link must remain retrievable before
merge; after merge, verify and link the durable target before deleting a branch
needed for that record.
