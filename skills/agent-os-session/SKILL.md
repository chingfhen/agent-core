---
name: agent-os-session
description: MUST be loaded at the start of every new chat/session
disable-model-invocation: false
---

### Autonomous State & Memory Routing

- **Stay in-repo; ask first.** Operate only within this repository. Don't read, search, or act on files outside it unless the user explicitly names an external path in the current request. If required information exists outside the repo, or is inherently human-owned (judgment calls, business intent, missing requirements, credentials, etc.), ask the user instead of searching broadly or making assumptions.

- **`docs/` and `tasks/` are skill-gated.** Reading is unrestricted. Before editing anything under `docs/`, load `project-docs`. Before creating or editing anything under `tasks/`, load `project-tasks`. Those skills define the maintenance rules.

- **Repository routing.**
  - `docs/` — canonical project knowledge: architecture, decisions, invariants, contracts, workflows, and confirmed fixes.
  - `tasks/backlog/` — deferred work items, one file per task (`YYYY-MM-DD__slug.md`), indexed by `tasks/backlog.md`.
  - `tasks/archive/` — completed, cancelled, or superseded tasks kept for historical reference.
  - `source-material/` — external references, research, specifications, and seed material; not the source of truth.
  
- **Read relevant docs first.** Before changing project behavior, making repository-specific decisions, investigating existing behavior, or giving implementation guidance, read the smallest relevant set of files under `docs/`.

  Read docs whenever the request may depend on documented architecture, conventions, contracts, invariants, workflows, prior fixes, or design decisions. Typical examples include behavior-changing code edits, API/schema/data-flow changes, cross-component work, deployments, bug investigations, task scoping, and questions about how the repository is intended to work.

  Skip docs for isolated syntax questions, mechanical edits, formatting, typo fixes, straightforward renames, or work fully specified by the user that does not depend on repository context.

  Identify the knowledge needed, locate only the docs likely to contain it, and follow references only to resolve concrete uncertainty. Prefer canonical `docs/` over tasks, source material, comments, or historical artifacts. Do not scan all documentation by default. Stop once the relevant constraints and decisions are understood.

  If no relevant documentation exists, proceed using the repository and the user's request. Clearly state any material assumptions. Ask only when missing information is human-owned or would materially change the outcome.

