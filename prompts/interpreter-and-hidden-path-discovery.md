# Interpreter And Hidden-Path Discovery

**Status:** Current

**Purpose:** Canonical reusable instruction block for interpreter selection and explicit checks of hidden dot-prefixed local paths.

Use this wording as the source template when adding the policy to future repos, prompts, or skills.

## Canonical Snippet

```md
## Interpreter And Hidden-Path Discovery

- When an explicit Python interpreter is needed, prefer the repo-local `.venv\Scripts\python.exe` if it exists.
- `.venv/`, `.opencode/`, `.claude/`, and other dot-prefixed local folders may be hidden from globbing, indexing, or search tools, especially when they are also gitignored.
- Do not conclude these paths are absent based on search results alone. Verify explicit paths with direct filesystem checks before falling back to another interpreter or workflow.
- Avoid borrowing interpreters from sibling repositories unless the task explicitly requires cross-repo execution.
```
