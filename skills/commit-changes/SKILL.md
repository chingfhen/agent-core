---
name: commit-changes
description: Create clean, scoped local Git commits when the user explicitly asks to commit changes. Preserve unrelated work and review the staged diff; do not push without separate authorization.
disable-model-invocation: false
triggers:
  - user
  - model
---

Create appropriate local Git commits for the current repository without pushing.

Perform the authorized commit directly. Delegation requires separate permission;
this skill does not authorize a push or a commit the human did not request.

Inspect all current changes and the index, preserve unrelated work, stage only
authorized paths/hunks, review the staged diff and whitespace, and report the
resulting commit hash and message.

## Decision visibility

When this skill makes a consequential choice—selecting, declining, or deferring a path, or applying a material scope, permission, cost, safety, or verification gate—make the chosen outcome and its evidence-based reason visible in the normal conversation (a compact `Decision: ... — ...` is sufficient). State it before acting when permission or cost depends on the choice, otherwise at the relevant handoff. An explanation already clearly given counts; do not add a duplicate status line, routine no-op receipts, a separate log, or private reasoning. Merely loading a skill is not evidence that its decision was applied.
