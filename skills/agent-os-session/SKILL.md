---
name: agent-os-session
description: MUST be loaded at the start of every new chat/session
disable-model-invocation: false
---

### Repository Operating Rules

* **Stay scoped; expand deliberately.**  Read and search within the current repository by default. Do not read, search, create, edit, move, rename, or delete files outside it unless the user explicitly names or authorizes the external repository or path in the current request. Do not broaden that authorization to unrelated paths. Treat destructive or difficult-to-reverse operations with additional caution. 

* **Route planning questions to the right skill.**

  * When the user asks to be grilled or wants a plan deeply stress-tested before building, load `grilling`.
  * Before substantial end-to-end execution or preparing a fresh-agent execution handoff, load `execution-readiness`.

* **`docs/` and `tasks/` are skill-gated.** Reading is unrestricted. Before editing anything under `docs/`, README files, or agent-guidance surfaces such as `AGENTS.md`, load `project-docs`. Before creating or editing anything under `tasks/`, load `project-tasks`. Those skills define the maintenance rules.

* **Repository routing.**

  * `docs/` — canonical project knowledge: architecture, decisions, invariants, contracts, workflows, and confirmed fixes.
  * `tasks/backlog/` — deferred work items, one file per task (`YYYY-MM-DD__slug.md`), indexed by `tasks/backlog.md`.
  * `tasks/archive/` — completed, cancelled, or superseded tasks kept for historical reference.
  * `source-material/` — external references, research, specifications, and seed material; not the source of truth.

* **Read relevant docs first.** Before repository-specific implementation, investigation, guidance, or decisions, read the smallest relevant set under `docs/`. Use docs when the work may depend on architecture, conventions, contracts, invariants, workflows, prior fixes, or design decisions. Skip them for isolated syntax questions, mechanical edits, formatting, typo fixes, straightforward renames, or fully specified work that does not require repository context. Prefer canonical docs/ over tasks, source material, comments, or historical artifacts. Follow references only to resolve concrete uncertainty, and stop once the relevant constraints are understood. Use docs for intended behavior and rationale; inspect code and tests to verify the current implementation. If no relevant docs exist, proceed from the repository and user request, state material assumptions, and ask only about human-owned gaps that would materially affect the outcome.
