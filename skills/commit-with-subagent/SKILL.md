---
name: commit-with-subagent
description: Create clean local Git commits using the dedicated commit-agent subagent. Use only when the user explicitly asks to commit changes.
disable-model-invocation: true
agent: commit-agent
triggers:
  - user
---

Create appropriate local Git commits for the current repository without pushing.

When this skill is active in a parent session, delegate the complete commit task to the `commit-agent` custom subagent. When it is already running under that profile, execute the task directly.

Inspect all current changes, preserve unrelated work, follow the commit agent's configured safety instructions, and report the resulting commit hash and message.
