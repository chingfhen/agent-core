# Agent OS

**Last Updated:** 2026-07-09

**Status:** Current

**Source Of Truth:** Defines the purpose and current v1 architecture of `~/agent-os`.

**Update When:** Canonical layout, integration model, or memory model changes.

### Read First

- `~/agent-os` is the canonical repo for centralized production skills and the current cautious cross-project memory pilot.
- `skills/` is the hand-edited production source; consumer repos receive generated local skill aliases, not hand-maintained copies.
- `prompts/` holds canonical reusable prompt snippets and policy blocks steward agents can reuse across repos and workflows.
- `AGENTS.md` is the authoritative operating contract for steward agents maintaining this repo.
- `docs/consumer-repo-enrollment.md` is the canonical contract for steward-managed consumer-repo enrollment and local alias behavior.
- Consumer repos are enrolled per device by steward workflows that install local skill aliases under both `.claude/skills` and `.opencode/skills`, install `yagni`, `project-docs`, `project-tasks`, `manage-python-uv`, and `grilling` by default, write `.agent-os.json`, and keep those outputs gitignored by default.
- There is no shared executor bootstrap skill; any executor skill that needs Agent OS repo context reads `.agent-os.json` directly.
- Steward-managed local skill aliases are installed under `.claude/skills` for Claude and `.opencode/skills` for OpenCode.
- On Windows, enrollment prefers directory symlinks and falls back to directory junctions when symlink privileges are unavailable.
- After a successful enroll or sync, selected consumer-repo skills should be live aliases, not copied directories; `verify` checks that guarantee directly.
- Harness-specific skill surfaces and steward enrollment state are generated/local, not canonical content.
- `tasks/` holds active execution handoff rather than durable architecture.
- `source-material/` holds seed inputs and supporting artifacts; `archive/` is reserved for retired historical reference material.

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
- `docs/**/*.md`
- `README.md`
- `AGENTS.md`
- `prompts/**/*.md`
- `memory/memories.jsonl`
- `repo-profiles/*`
- `scripts/*`
- `schemas/*`

#### Generated Or Installed Surfaces

- Consumer-repo-local `.agent-os.json`
- Consumer-repo-local `.claude/skills/*` aliases used by Claude
- Consumer-repo-local `.opencode/skills/*` aliases used by OpenCode
- Device-local steward enrollment state in `.agent-os-state/enrollments.json`
- `memory/memory.sqlite`
- `MEMORY_INDEX.md`

#### Consumer Repo Integration

- Each consumer repo is enrolled per device by a steward workflow.
- Enrollment writes a repo-local `.agent-os.json`, installs repo-local skill aliases under both `.claude/skills` and `.opencode/skills`, installs the default consumer-repo skill set documented in `docs/consumer-repo-enrollment.md`, and keeps those outputs gitignored by default.
- Steward sync keeps the same canonical skills aligned across Claude's native `.claude/skills` path and OpenCode's native `.opencode/skills` path.
- Matching local skill directories are auto-replaced with live aliases during enroll and sync, with a human-visible notice.
- Executors consume ordinary local skill aliases rather than reasoning about canonical skill provenance.
- This system does not depend on modifying consumer repo `AGENTS.md`.
- Consumer repos do not receive a shared bootstrap skill.
- Executor skills that need Agent OS repo context read `.agent-os.json` directly.
- `agent-os-memory` is the current executor skill that consumes manifest fields such as `agent_os_path`, `scope`, `scope_id`, and `memory_enabled`.
- Executor agents use local skill aliases as ordinary repo skills; they do not need to know whether the installed surface is symlinked or a junction-backed alias.
- On Windows, link installation tries a directory symlink first and falls back to a directory junction when Win32 symlink privileges are unavailable.
- Both symlinks and directory junctions satisfy the live update guarantee: edits propagate immediately in both directions because the consumer path resolves to the canonical skill directory.
- `uv run scripts/enroll_repo.py verify --repo <path>` returns success only when the repo is in that live-alias steady state.
- `uv run scripts/enroll_repo.py sync --repo <path>` removes retired `agent-os-bootstrap` aliases and drops the stale registry entry from older enrollments.
- The local steward registry also remembers the working device link mode so future repo enrollments can skip known-failing symlink probes.
- See `docs/consumer-repo-enrollment.md` for the full enrollment, ignore, and conflict-handling contract.

#### Repo Working Surfaces

- `tasks/` holds active execution handoff and fresh-session continuity.
- `docs/`, `README.md`, and `AGENTS.md` hold durable repo truth.
- `prompts/` holds canonical reusable prompt snippets and policy blocks.
- `source-material/` holds non-canonical seed inputs and supporting artifacts that may still inform later work.
- `archive/` is the home for retired historical reference material that should not drive current truth by default.

#### Memory Pilot

- Memory is a pilot, not yet a proven core workflow.
- The canonical truth is append-only `memory/memories.jsonl`.
- `memory/memories.jsonl` is the only tracked memory ledger.
- Search and derived state live in generated artifacts such as `memory/memory.sqlite` and `MEMORY_INDEX.md`, which remain disposable and should not be committed.
- Steward agents own the memory subsystem and canonical repo publication in `~/agent-os`.
- Executors may use memory through the separate repo-local `agent-os-memory` skill when `memory_enabled` is true, but they should not need storage-internal knowledge.
- Topic discovery should come from `uv run scripts/memory.py list` and `search` flows exposed through `agent-os-memory`, not a hand-maintained registry.
- Memory tooling starts with read-only `list` and `search`, append-only `write`, an explicit delete refusal, and `reindex`; destructive delete and in-place ledger edits stay out of scope for the append-only pilot.
- Active versus superseded memory state is derived in search/index results, not by rewriting prior ledger rows.
- Creating a new `topic_key` requires explicit human approval.
- Updating an existing `topic_key` within the active scope can be autonomous.
- Memory behavior lives in the repo-local `agent-os-memory` skill rather than a shared bootstrap layer.

#### Dependency Strategy

- Python script tooling in this repo should use `uv`.
- Device setup is one-time per machine: install `uv`, then provision Python 3.11+ once.
- Prefer `uv python install 3.11` so the repo does not depend on an already-correct system Python.
- `uv` remains useful before any repo-wide `pyproject.toml` exists.
- Repo scripts should declare dependencies inline with PEP 723 metadata.
- Run steward scripts with `uv run`, not manual `pip install` plus ad hoc virtual environments.
- The default starting point is scripts-first `uv run` execution; `uv` does not require `uv init` or a checked-in `pyproject.toml` for that phase.
- Do not rely on checked-in `.venv`, `requirements.txt`, or per-device manual dependency state.
- If the repo later grows beyond a small scripts-first model or needs shared test/tooling configuration, reassess whether a checked-in `pyproject.toml` is justified.

#### Deferred For Later

- MCP as an interface for memory/tooling
- Additional harness-native alias surfaces beyond the steward-managed `.claude/skills` and `.opencode/skills` paths

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Steward contract | `AGENTS.md` | Governs how agents maintain this repo. |
| Prompt library | `prompts/` | Canonical reusable prompt snippets and policy blocks steward agents manage. |
| Consumer repo integration | `docs/consumer-repo-enrollment.md` | Canonical contract for steward-managed repo enrollment and executor-facing local aliases. |
| Memory pilot contract | `docs/memory-pilot.md` | Canonical contract for the append-only ledger, derived artifacts, and approval boundary. |
| Enrollment script | `scripts/enroll_repo.py` | Writes `.agent-os.json`, manages local aliases, updates ignore rules, and records local enrollment state. |
| Memory script | `scripts/memory.py` | Implements the list/search/write/reindex memory flows and rebuilds derived artifacts. |
| Manifest schema | `schemas/agent-os-manifest.schema.json` | Defines the v1 `.agent-os.json` contract for consumer repos. |
| Verification command | `uv run scripts/enroll_repo.py verify --repo <path>` | Confirms a consumer repo is using live aliases that receive canonical updates immediately. |
| Historical seed spec | `source-material/initialize.md` | Original input that informed the current architecture; no longer the ongoing source of truth. |
| Active handoff | `tasks/` | Fresh-session execution continuity for unfinished work. |
| Core production skill | `skills/project-docs/SKILL.md` | Defines how durable project knowledge should be routed and maintained. |
| Core production skill | `skills/project-tasks/SKILL.md` | Defines how execution handoff should be preserved across fresh sessions. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-06-18 | `AGENTS.md` is the steward-agent contract. | Steward agents need the repo contract auto-loaded in future sessions. |
| 2026-06-18 | `skills/` is the canonical production source. | Cross-device and cross-harness skill reuse needs one hand-edited source of truth. |
| 2026-06-18 | Consumer repos use repo-local `.agent-os.json`. | Repo-specific scope data needs a deterministic, machine-readable manifest. |
| 2026-06-18 | Consumer repo `AGENTS.md` files are out of scope. | The human will bridge bootstrap gaps without forcing edits into other repos. |
| 2026-06-18 | Skills are not delivered MCP-first in v1. | Filesystem and harness-native loading are simpler and more reliable for static skills. |
| 2026-06-18 | Memory truth stays append-only in JSONL. | Immutable truth is easier to reason about, sync, and regenerate from. |
| 2026-06-18 | Python runtime and script dependencies use `uv` plus PEP 723. | Cross-device script execution should avoid repo-local virtualenv drift and manual dependency setup. |
| 2026-06-19 | Consumer repos are enrolled per device by steward workflows. | Repo setup should be repeatable and steward-managed rather than relying on manual manifest placement. |
| 2026-06-19 | Executors consume repo-local skill aliases. | Executor agents should use ordinary local skill names without caring about canonical provenance. |
| 2026-06-19 | `.agent-os.json` is gitignored by default. | The manifest contains per-user and per-device integration state and should not confuse teammates. |
| 2026-06-19 | Managed ignore rules default to exact alias paths. | Narrow ignores avoid masking other repo-owned harness files. |
| 2026-06-21 | There is no shared executor bootstrap skill. | Only `agent-os-memory` currently needs manifest fields, so a separate bootstrap step only duplicated logic and created conceptual noise. |
| 2026-07-09 | Removed `yagni-review`, `agent-os-memory`, and `diagram-generation` from default enrollment. | These skills remain opt-in, while new enrollments start from a smaller default skill set. |
| 2026-06-22 | New enrollments install a curated default consumer-repo skill set. | Review, docs, task handoff, Python workflow, memory, and grilling support should be present in most enrolled consumer repos, while more specialized skills stay opt-in. |
| 2026-06-19 | Steward enrollment state is local and untracked. | Device-specific repo enrollment should not create cross-device drift or tracked repo noise. |
| 2026-06-19 | Consumer repo enrollment details live in `docs/consumer-repo-enrollment.md`. | The README should stay orienting while one dedicated doc owns the full integration contract. |
| 2026-06-19 | `uv` starts in scripts-first mode without requiring `pyproject.toml`. | Small steward utilities should stay lightweight until shared tooling justifies a project file. |
| 2026-06-19 | Steward owns canonical memory publication in `~/agent-os`. | Executors may use memory, but one owner boundary prevents canonical ledger churn and storage coupling. |
| 2026-06-21 | Shared local project skills sync to both `.claude/skills` and `.opencode/skills`. | Claude and OpenCode should each receive the same canonical skills through their native project-local discovery paths. |
| 2026-06-19 | Windows enrollment defaults to symlink with junction fallback. | The first pilot lacked symlink privileges, so a non-destructive fallback was required to complete setup. |
| 2026-06-19 | Device-local enrollment state lives in `.agent-os-state/enrollments.json`. | Repair runs need a local registry without adding tracked repo noise. |
| 2026-06-19 | Consumer-repo skill copies are transitional and auto-replaced. | The system's value depends on live canonical updates, so steady state must be alias-backed rather than copy-backed. |
| 2026-06-19 | Repo working surfaces standardize on `tasks/` and `source-material/`, with `archive/` reserved for retired historical reference. | Visible folder names work with OpenCode discovery and keep active execution, durable docs, and non-canonical artifacts clearly separated. |
| 2026-06-19 | The first memory pilot ships as `scripts/memory.py` subcommands. | One steward-owned single-file script is the smallest correct surface for list/search/write/reindex memory flows. |
