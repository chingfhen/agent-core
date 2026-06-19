# Agent OS

**Last Updated:** 2026-06-18

**Status:** Current

**Source Of Truth:** Defines the purpose and current v1 architecture of `~/agent-os`.

**Update When:** Canonical layout, integration model, or memory model changes.

### Read First

- `~/agent-os` is the canonical repo for centralized production skills and a cautious cross-project memory pilot.
- `skills/` is the production source consumed by executor agents.
- `AGENTS.md` is the authoritative operating contract for steward agents maintaining this repo.
- Consumer repos use their own `.agent-os.json` to declare repo-specific scope and integration values.
- `skills/agent-os-bootstrap/SKILL.md` will be the shared bootstrap skill for executor agents.
- Harness-specific skill surfaces are generated or configured install targets, not canonical content.

### Scope

This document defines the repo purpose, key terms, canonical/generated boundaries, and the current v1 integration model.

### Not Here

Detailed implementation tasks, generated output, or session-by-session execution history.

### Current Contract

#### Terms

- **Steward agent:** An agent working inside `~/agent-os` to maintain the system itself.
- **Executor agent:** An agent working inside another repo that consumes Agent OS capabilities.
- **Consumer repo:** Any non-`agent-os` repo that participates in this system.

#### Canonical Surfaces

- `skills/**/SKILL.md`
- `README.md`
- `AGENTS.md`
- Future `memory/memories.jsonl`
- Future `repo-profiles/*`
- Future `scripts/*`

#### Generated Or Installed Surfaces

- `~/.claude/skills/*`
- OpenCode harness configuration or install targets that expose `~/agent-os/skills`
- Future `memory/memory.sqlite`
- Future `MEMORY_INDEX.md`

#### Consumer Repo Integration

- Each consumer repo gets a repo-local `.agent-os.json`.
- The file uses a shared schema but repo-specific values.
- The initial rollout assumes the human manually places this file into each consumer repo.
- This system does not depend on modifying consumer repo `AGENTS.md`.
- `agent-os-bootstrap` will live in `~/agent-os/skills/agent-os-bootstrap/SKILL.md`.
- The human may explicitly tell executor agents to use `agent-os-bootstrap` when entering a consumer repo.
- `agent-os-bootstrap` teaches executor agents to read `.agent-os.json` when present and route themselves to the canonical Agent OS surfaces.

#### Memory Pilot

- Memory is a pilot, not yet a proven core workflow.
- The canonical truth will be append-only `memory/memories.jsonl`.
- Search and derived state will live in generated artifacts such as `memory.sqlite`.
- Active versus superseded memory state is derived in search/index results, not by rewriting prior ledger rows.
- Creating a new `topic_key` requires explicit human approval.
- Updating an existing `topic_key` within the active scope can be autonomous.

#### Dependency Strategy

- Python script tooling in this repo should use `uv`.
- Device setup is one-time per machine: install `uv`, then provision Python 3.11+ once.
- Prefer `uv python install 3.11` so the repo does not depend on an already-correct system Python.
- Repo scripts should declare dependencies inline with PEP 723 metadata.
- Run steward scripts with `uv run`, not manual `pip install` plus ad hoc virtual environments.
- Do not rely on checked-in `.venv`, `requirements.txt`, or per-device manual dependency state.
- If the repo later grows beyond a scripts-first model, reassess whether a `pyproject.toml` package is justified.

#### Deferred For Later

- MCP as an interface for memory/tooling
- Broader harness support beyond OpenCode and Claude

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Steward contract | `AGENTS.md` | Governs how agents maintain this repo. |
| Historical seed spec | `.raw/initialize.md` | Original input that informed the current architecture; no longer the ongoing source of truth. |
| Core production skill | `skills/project-docs/SKILL.md` | Defines how durable project knowledge should be routed and maintained. |
| Core production skill | `skills/project-tasks/SKILL.md` | Defines how execution handoff should be preserved across fresh sessions. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-06-18 | `AGENTS.md` is the steward-agent contract. | Steward agents need the repo contract auto-loaded in future sessions. |
| 2026-06-18 | `skills/` is the canonical production source. | Cross-device and cross-harness skill reuse needs one hand-edited source of truth. |
| 2026-06-18 | Consumer repos use repo-local `.agent-os.json`. | Repo-specific scope data needs a deterministic, machine-readable manifest. |
| 2026-06-18 | Consumer repo `AGENTS.md` files are out of scope. | The human will bridge bootstrap gaps without forcing edits into other repos. |
| 2026-06-18 | `agent-os-bootstrap` is the executor bootstrap skill. | Shared bootstrap instructions belong in a canonical production skill, not in per-repo duplicated guidance. |
| 2026-06-18 | Skills are not delivered MCP-first in v1. | Filesystem and harness-native loading are simpler and more reliable for static skills. |
| 2026-06-18 | Memory truth stays append-only in JSONL. | Immutable truth is easier to reason about, sync, and regenerate from. |
| 2026-06-18 | Python runtime and script dependencies use `uv` plus PEP 723. | Cross-device script execution should avoid repo-local virtualenv drift and manual dependency setup. |
