# Agent OS Steward Contract

**Last Updated:** 2026-07-18

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain `~/agent-os`.

**Update When:** Steward/executor roles, canonical surfaces, or integration rules change.

### Read First

- You are the steward agent when working in this repo.
- At the start of every chat, load `agent-os-session` and state `Loaded agent-os-session.`
- `skills/` is the hand-edited production source for executor agents.
- Do not update production workflow skills in `skills/` unless the human explicitly approves the skill edit.
- Prefer autonomous durable guidance updates in `AGENTS.md`, `docs/`, and `prompts/` rather than changing production workflow skills.
- Consumer repos are enrolled per device; do not hand-maintain consumer-repo skill copies.
- Device-local enrolled repo paths live in `.agent-os-state/enrollments.json`; read it when a requested consumer repo is not obvious from the workspace tree.
- `agent-os-session` is the shared session-start skill; executor skills that need Agent OS repo context should read `.agent-os.json` directly.
- The shared project-local alias surfaces are `.claude/skills/*` for Claude and `.opencode/skills/*` for OpenCode.
- On Windows, prefer directory symlinks but fall back to directory junctions when symlink privileges are unavailable.
- Symlinks and directory junctions both satisfy the live-update guarantee; copied local skill directories do not.
- Consumer aliases can resolve directly into canonical `skills/`. Never recursively delete, move, or modify an alias or its `.claude/skills` or `.opencode/skills` parent; use `unenroll` for verified aliases or stop and ask.
- `docs/consumer-repo-enrollment.md` is the canonical contract for steward-managed repo enrollment details.
- `prompts/` holds canonical reusable prompt snippets and policy blocks steward agents manage.
- `prompts/autonomous-state-and-memory-routing.md` is historical source material for the routing policy now canonicalized in `agent-os-session`.
- `README.md` holds the durable repo architecture; keep this file focused on operating rules.
- `source-material/initialize.md` is seed input kept for reference, not the ongoing source of truth.
- Use `tasks/` for active execution handoff, not durable architecture.
- Use `source-material/` for supporting artifacts and `archive/` for retired historical reference material.

### Scope

This file governs agents maintaining `~/agent-os`.

### Not Here

Consumer-repo-local instructions, runtime task state, or generated harness output.

### Autonomous State & Memory Routing

You are a node in an ongoing execution chain. Optimize repository context for future agent sessions while preserving a strict boundary between active execution state and durable memory.

- **Read-only execution state:** The human architect manages `tasks/` for active alignment and session handoff. You may read these files to understand current state, but do not create, edit, or manage task files unless explicitly instructed.
- **Durable memory routing:** Maintain `docs/`, `source-material/`, and `archive/` as follows:
  - **Route to `docs/`:** Store stable project truth such as decisions, invariants, contracts, and confirmed fixes. Prefer the smallest durable update that improves clarity for future sessions.
  - **Route to `source-material/`:** Store external intelligence, third-party references, web research, or seed inputs that inform the work but are not canonical project truth.
  - **Route to `archive/`:** Move content here only when it is clearly superseded by a newer canonical source and should no longer guide future work.
  - **Docs-first problem solving:** `docs/` is the higher rung. Before reading source files to understand how something works, check `docs/` first. If a relevant doc exists, read it and stop there unless it is incomplete. Docs capture decisions, invariants, contracts, and architecture that code must be read to infer. Reading code to rediscover documented understanding is wasted effort — the same anti-pattern as writing custom code when the stdlib already ships it.
- **Quality bar:** Only persist information that is stable, repo-relevant, and likely to help a future agent. Do not promote transient notes, tentative hypotheses, or session-local debugging artifacts into durable memory.
- **Silent optimization:** Perform these updates opportunistically at natural workflow boundaries without asking for permission, but avoid unnecessary churn and do not archive or rewrite content unless the status is clear.

### Current Contract

- **Steward agent:** Agent working inside `~/agent-os` to maintain the system itself.
- **Executor agent:** Agent working inside another repo that consumes Agent OS capabilities.
- **Consumer repo:** Any non-`agent-os` repo that participates in this system.
- `agent-os-session` is the default shared session-start skill for enrolled repos; it exists to prevent copied instruction drift and to make session-start compliance visible.
- Canonical surfaces are `skills/`, steward docs such as `README.md`, `AGENTS.md`, `docs/**/*.md`, and `prompts/**/*.md`, plus the append-only memory ledger `memory/memories.jsonl`.
- Generated surfaces include consumer-repo-local `.agent-os.json`, consumer-repo-local `.claude/skills/*` and `.opencode/skills/*` aliases, future harness-native aliases only where they add distinct value, device-local steward enrollment state in `.agent-os-state/enrollments.json`, and derived memory artifacts such as `memory/memory.sqlite` and `MEMORY_INDEX.md`.
- `.agent-os-state/enrollments.json` is untracked but authoritative for this device's enrolled consumer repo paths and recorded link modes.
- Do not add tracked `.opencode`, `.claude`, or `.codex` production copies to this repo.
- Consumer repos are enrolled per device by steward workflows; this repo does not depend on editing consumer-repo `AGENTS.md`.
- Executor skills that need manifest context should read `.agent-os.json` directly rather than relying on a shared manifest bootstrap layer.
- New enrollments include the default consumer-repo skill set defined in `docs/consumer-repo-enrollment.md`; explicit `--skill` values add more repo-local aliases.
- Executor agents should consume repo-local skill aliases as ordinary repo skills; they do not need canonical/source-provenance explanation.
- Keep `.claude/skills/*` and `.opencode/skills/*` aligned during enroll and sync so Claude and OpenCode receive the same canonical skill set.
- The trusted steady state is live aliasing to canonical skills; real local skill directories are conflicts that require explicit migration.
- Default ignore behavior in consumer repos is `.agent-os.json` plus exact managed alias paths, unless a broader existing ignore already covers them.
- Memory remains a pilot: append-only JSONL is canonical truth, generated search/index artifacts are disposable, and active/superseded state is derived rather than rewritten into prior rows.
- `memory/memories.jsonl` is the only tracked memory ledger; `memory/memory.sqlite` and `MEMORY_INDEX.md` are generated/local artifacts and should not be committed.
- Executors may use memory via repo-local skills when `memory_enabled` is enabled, but steward agents own the memory subsystem and canonical repo publication in `~/agent-os`.
- Executor-facing memory tooling is exposed through `scripts/memory.py` and `skills/agent-os-memory/SKILL.md` so executors can discover topics without storage-internal knowledge.
- MCP is backlog for memory/tooling, not the primary skill-delivery path in v1.

### Steward Rules

- Keep `skills/` production-ready and hand-edited.
- Do not edit production workflow skills autonomously; wait for explicit human approval before changing `skills/`.
- Keep manifest reads local to the executor skills that actually need them; `agent-os-session` is only for session-start routing and must not become a manifest bootstrap layer.
- Sync durable architecture into `README.md`; keep this file concise and operational.
- Put active execution context in `tasks/`.
- Prefer single-file Python scripts with PEP 723 metadata and run them with `uv`.
- Start with `uv run` plus PEP 723 scripts; do not introduce a repo-wide `pyproject.toml` unless shared tooling or packaging needs justify it.
- Do not depend on checked-in virtual environments or manual `pip install` state.
- Prefer minimal reversible foundations before adding automation.
- Prefer steward-managed enrollment over manual consumer-repo setup.
- When syncing/installing consumer-repo skills, preflight each target path as `missing`, `managed`, or `conflict`.
- Replace only clearly steward-managed aliases automatically; stop and ask before overwriting unrelated existing files or directories.
- Treat every real local skill directory as a conflict; do not delete it automatically, even when it declares the expected skill name.
- Remove consumer aliases only through `uv run scripts/enroll_repo.py unenroll --repo <path> --apply`; if link verification fails or no supported command exists, stop and ask.
- Remember the working device link mode locally so future enrollments can skip known-failing symlink probes.
- Gitignore `.agent-os.json` and exact managed alias paths by default unless a broader existing ignore already covers them.
- Keep memory behavior in `agent-os-memory`; do not expand `agent-os-session` into memory or manifest bootstrap behavior unless the real executor workflows justify it.
- Keep memory operations append-only; prefer write/supersede plus generated reindexing over delete or edit-in-place flows.
- Route memory reads and writes through `uv run scripts/memory.py` rather than direct ledger edits.
- Use `uv run scripts/enroll_repo.py verify --repo <path>` when you need to confirm the live update guarantee quickly.
- When implementing cross-harness access, preserve the canonical/generated boundary.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Durable explanation of what this repo is and how it is structured. |
| Session skill | `skills/agent-os-session/SKILL.md` | Shared session-start routing policy and visible load confirmation. |
| Prompt library | `prompts/` | Canonical reusable prompt snippets and policy blocks steward agents manage. |
| Memory-routing source material | `prompts/autonomous-state-and-memory-routing.md` | Historical source material for the routing policy promoted into `agent-os-session`. |
| Consumer repo integration | `docs/consumer-repo-enrollment.md` | Canonical contract for enrollment, alias installs, ignore rules, and manifest-consumer behavior. |
| Memory pilot contract | `docs/memory-pilot.md` | Defines the ledger schema, approval boundary, and steward memory tooling. |
| Enrollment script | `scripts/enroll_repo.py` | Implements enrollment, repair, local registry updates, and Windows link fallback behavior. |
| Memory script | `scripts/memory.py` | Implements list/search/write/reindex over the append-only memory ledger. |
| Manifest schema | `schemas/agent-os-manifest.schema.json` | Defines the v1 consumer-repo manifest shape. |
| Historical seed spec | `source-material/initialize.md` | Starting point that informed the current contract. |
| Active handoff | `tasks/` | Fresh-session execution continuity for unfinished work. |
