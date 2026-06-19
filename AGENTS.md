# Agent OS Steward Contract

**Last Updated:** 2026-06-19

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain `~/agent-os`.

**Update When:** Steward/executor roles, canonical surfaces, or integration rules change.

### Read First

- You are the steward agent when working in this repo.
- `skills/` is the hand-edited production source for executor agents.
- Consumer repos are enrolled per device; do not hand-maintain consumer-repo skill copies.
- `agent-os-bootstrap` is a thin manifest-hydration skill; executor agents should use local aliases without being taught canonical provenance.
- The first shared project-local alias surface is `.claude/skills/*`; Claude uses it natively and OpenCode also discovers it.
- On Windows, prefer directory symlinks but fall back to directory junctions when symlink privileges are unavailable.
- Symlinks and directory junctions both satisfy the live-update guarantee; copied local skill directories do not.
- `docs/consumer-repo-enrollment.md` is the canonical contract for steward-managed repo enrollment details.
- `README.md` holds the durable repo architecture; keep this file focused on operating rules.
- `.raw/initialize.md` is historical input, not the ongoing source of truth.
- Use `.tasks/` for active execution handoff, not durable architecture.

### Scope

This file governs agents maintaining `~/agent-os`.

### Not Here

Consumer-repo-local instructions, runtime task state, or generated harness output.

### Current Contract

- **Steward agent:** Agent working inside `~/agent-os` to maintain the system itself.
- **Executor agent:** Agent working inside another repo that consumes Agent OS capabilities.
- **Consumer repo:** Any non-`agent-os` repo that participates in this system.
- Canonical surfaces are `skills/`, steward docs such as `README.md`, `AGENTS.md`, and `docs/**/*.md`, and future canonical stores such as `memory/memories.jsonl`.
- Generated surfaces include consumer-repo-local `.agent-os.json`, consumer-repo-local `.claude/skills/*` aliases consumed by Claude and OpenCode, future harness-native aliases only where they add distinct value, device-local steward enrollment state in `.agent-os-state/enrollments.json`, and future derived memory artifacts such as `memory.sqlite` and `MEMORY_INDEX.md`.
- Do not add tracked `.opencode`, `.claude`, or `.codex` production copies to this repo.
- Consumer repos are enrolled per device by steward workflows; this repo does not depend on editing consumer-repo `AGENTS.md`.
- `skills/agent-os-bootstrap/SKILL.md` is the executor bootstrap skill in the canonical production store.
- `agent-os-bootstrap` should only teach executors to read `.agent-os.json` and hydrate repo identity, scope, memory availability, and repo-local Agent OS settings.
- Executor agents should consume repo-local skill aliases as ordinary repo skills; they do not need canonical/source-provenance explanation.
- OpenCode discovers `.claude/skills/*`, so do not duplicate the same skill names under `.opencode/skills/*` unless the contract changes.
- The trusted steady state is live aliasing to canonical skills; copied local skill directories are only transitional and should be replaced during enroll or sync.
- Default ignore behavior in consumer repos is `.agent-os.json` plus exact managed alias paths, unless a broader existing ignore already covers them.
- Memory remains a pilot: append-only JSONL is canonical truth, generated search/index artifacts are disposable, and active/superseded state is derived rather than rewritten into prior rows.
- `memory/memories.jsonl` is the only tracked memory ledger; `memory.sqlite` and `MEMORY_INDEX.md` are generated/local artifacts and should not be committed.
- Executors may eventually use memory via repo-local skills when `memory_enabled` is enabled, but steward agents own the memory subsystem and canonical repo publication in `~/agent-os`.
- Future executor-facing memory tooling should expose list/search/write flows so executors can discover topics without storage-internal knowledge.
- MCP is backlog for memory/tooling, not the primary skill-delivery path in v1.

### Steward Rules

- Keep `skills/` production-ready and hand-edited.
- Keep shared bootstrap behavior in canonical skills rather than consumer-repo-local guidance.
- Sync durable architecture into `README.md`; keep this file concise and operational.
- Put active execution context in `.tasks/`.
- Prefer single-file Python scripts with PEP 723 metadata and run them with `uv`.
- Start with `uv run` plus PEP 723 scripts; do not introduce a repo-wide `pyproject.toml` unless shared tooling or packaging needs justify it.
- Do not depend on checked-in virtual environments or manual `pip install` state.
- Prefer minimal reversible foundations before adding automation.
- Prefer steward-managed enrollment over manual consumer-repo setup.
- When syncing/installing consumer-repo skills, preflight each target path as `missing`, `managed`, or `conflict`.
- Replace only clearly steward-managed aliases automatically; stop and ask before overwriting unrelated existing files or directories.
- Replace matching local skill directories with live aliases automatically and surface a human-visible notice.
- Remember the working device link mode locally so future enrollments can skip known-failing symlink probes.
- Gitignore `.agent-os.json` and exact managed alias paths by default unless a broader existing ignore already covers them.
- Keep `agent-os-bootstrap` thin and move memory behavior into separate future skills.
- Keep memory operations append-only; prefer write/supersede plus generated reindexing over delete or edit-in-place flows.
- Use `uv run scripts/enroll_repo.py verify --repo <path>` when you need to confirm the live update guarantee quickly.
- When implementing cross-harness access, preserve the canonical/generated boundary.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Durable explanation of what this repo is and how it is structured. |
| Consumer repo integration | `docs/consumer-repo-enrollment.md` | Canonical contract for enrollment, alias installs, ignore rules, and bootstrap scope. |
| Enrollment script | `scripts/enroll_repo.py` | Implements enrollment, repair, local registry updates, and Windows link fallback behavior. |
| Manifest schema | `schemas/agent-os-manifest.schema.json` | Defines the v1 consumer-repo manifest shape. |
| Historical seed spec | `.raw/initialize.md` | Starting point that informed the current contract. |
| Active handoff | `.tasks/` | Fresh-session execution continuity for unfinished work. |
