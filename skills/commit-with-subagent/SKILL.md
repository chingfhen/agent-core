---
name: commit-with-subagent
description: Create clean local Git commits, preferably using the dedicated commit-agent when available. Use only when the user explicitly asks to commit changes.
disable-model-invocation: false
triggers:
  - user
  - model
---

Create appropriate local Git commits for the current repository without pushing.

When `commit-agent` is available and delegation is permitted, delegate the complete
commit task to that custom subagent. When already running under that profile,
execute directly. Do not infer that a different agent is the same specialist.

If the specialist is unavailable in this harness or delegation is not permitted,
the main agent may perform the authorized scoped commit directly rather than
stranding its own changes. Say that the fallback was used. If the human explicitly
required that specialist or delegation, report the blocker instead of silently
substituting. This fallback does not authorize a push, another agent, or a commit
the human did not request.

Inspect all current changes and the index, preserve unrelated work, stage only
authorized paths/hunks, review the staged diff and whitespace, and report the
resulting commit hash and message. When delegating, follow the specialist's
applicable safety instructions too.
