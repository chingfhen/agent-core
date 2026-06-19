---
name: agent-os-bootstrap
description: Hydrates repo-local Agent OS context from .agent-os.json so executor agents can use local skills with the right repo identity and memory boundary.
disable-model-invocation: false
---

# Agent OS Bootstrap

Read this repo's `.agent-os.json` before relying on Agent OS-specific assumptions.

## What To Do

1. Read `.agent-os.json` from the repo root.
2. If it exists and parses, capture:
   - `repo_id`
   - `scope`
   - `scope_id`
   - `agent_os_path`
   - `memory_enabled`
3. Treat any additional top-level keys as repo-local Agent OS settings if they are present.
4. If the file is missing or invalid, tell the user the repo is not fully enrolled or the manifest needs repair, then continue without assuming Agent OS features are available.

## Behavior Contract

- Use the manifest only to hydrate runtime context.
- Treat local skills such as `project-docs`, `project-tasks`, `manage-python-uv`, and `agent-os-memory` as ordinary repo-local skills.
- Only reach for memory behavior when `memory_enabled` is `true` and the corresponding local skill exists.
- Do not explain or depend on canonical skill provenance, symlink mechanics, or steward internals unless the user explicitly asks.
- Do not rewrite `.agent-os.json` yourself unless the user explicitly asks for enrollment or repair work.

## Manifest Contract

Version 1 manifests must include:

- `version`
- `repo_id`
- `scope`
- `scope_id`
- `agent_os_path`
- `memory_enabled`
