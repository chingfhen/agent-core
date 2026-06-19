# Agent OS Steward Contract

**Last Updated:** 2026-06-18

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain `~/agent-os`.

**Update When:** Steward/executor roles, canonical surfaces, or integration rules change.

### Read First

- You are the steward agent when working in this repo.
- `skills/` is the hand-edited production source for executor agents.
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
- Canonical surfaces are `skills/`, steward docs such as `README.md` and `AGENTS.md`, and future canonical stores such as `memory/memories.jsonl`.
- Generated surfaces include harness install targets such as `~/.claude/skills/*` and future derived memory artifacts such as `memory.sqlite` and `MEMORY_INDEX.md`.
- Do not add tracked `.opencode`, `.claude`, or `.codex` production copies to this repo.
- Consumer repos get their own `.agent-os.json`; this repo does not depend on editing consumer-repo `AGENTS.md`.
- `skills/agent-os-bootstrap/SKILL.md` is the planned executor bootstrap skill in the canonical production store.
- V1 bootstrap assumes the human may explicitly tell executor agents to use `agent-os-bootstrap` and read `.agent-os.json`.
- OpenCode should eventually consume canonical skills from `~/agent-os/skills` via configuration.
- Claude should eventually consume generated installs derived from canonical skills.
- Memory remains a pilot: append-only JSONL is canonical truth, generated search/index artifacts are disposable, and active/superseded state is derived rather than rewritten into prior rows.
- MCP is backlog for memory/tooling, not the primary skill-delivery path in v1.

### Steward Rules

- Keep `skills/` production-ready and hand-edited.
- Keep shared bootstrap behavior in canonical skills rather than consumer-repo-local guidance.
- Sync durable architecture into `README.md`; keep this file concise and operational.
- Put active execution context in `.tasks/`.
- Prefer single-file Python scripts with PEP 723 metadata and run them with `uv`.
- Do not depend on checked-in virtual environments or manual `pip install` state.
- Prefer minimal reversible foundations before adding automation.
- When implementing cross-harness access, preserve the canonical/generated boundary.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Durable explanation of what this repo is and how it is structured. |
| Historical seed spec | `.raw/initialize.md` | Starting point that informed the current contract. |
| Active handoff | `.tasks/` | Fresh-session execution continuity for unfinished work. |
