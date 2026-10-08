# Agent OS Steward Contract

**Last Updated:** 2026-10-08

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain the private Agent Core repository.

**Update When:** Steward roles, canonical surfaces, distribution, or integration rules change.

### Read First

- You are the steward agent when working in this repository.
- `skills/` is the hand-edited production source. Do not change production workflow skills unless the human explicitly approves the skill edit.
- The normal personal command is `agent-core sync`. It refreshes the fixed clean `~/.agent-core` checkout and publishes `personal-skills.toml` entries plus canonical global guidance to user-global harness locations.
- Do not hand-maintain installed copies or aliases. Sync owns only exact destinations recorded in `~/.agent-core-state/ownership.json`.
- `docs/agent-core-operating-manual.md` is the canonical human command reference.
- Before editing `tasks/`, load `project-tasks`. Before editing docs, README, or agent guidance, load `project-docs`.
- Prefer durable guidance updates in `AGENTS.md`, `docs/`, `global/`, and `prompts/` over production skill edits.

## Autonomous State And Memory Routing

- **Read-only execution state by default:** The human architect manages `tasks/`. Read tasks for current state, but do not create, edit, or manage them unless explicitly instructed.
- **Route stable truth to `docs/`:** Preserve decisions, invariants, contracts, workflows, and confirmed fixes that future agents would otherwise rediscover.
- **Route external evidence to `source-material/`:** Keep third-party references, research, and seed inputs non-canonical.
- **Route superseded material to `archive/`:** Move content only when a newer canonical source clearly replaces it.
- **Use docs first:** Check relevant docs before source when understanding architecture or contracts; inspect implementation when current behavior must be verified.
- **Keep quality high:** Do not promote transient notes, tentative hypotheses, or session-local debugging artifacts.

## Current Contract

### Roles

- **Steward agent:** Maintains this canonical repository, package, docs, workflows, and memory tooling.
- **Executor agent:** Works in any directory using globally installed personal skills plus project-owned instructions and skills.
- **Managed global destination:** An exact user-home path published by Agent Core and fingerprinted in machine-local ownership state.

### Canonical And Installed Boundaries

Canonical surfaces include:

- `skills/` and `personal-skills.toml`;
- `global/AGENTS.md`;
- `agent_core/`, `pyproject.toml`, and installer scripts;
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`;
- schemas, steward scripts, and the append-only `memory/memories.jsonl` ledger.

Installed or generated surfaces include:

- real skill copies under `~/.agents/skills/<personal-skill>/`;
- Claude aliases under `~/.claude/skills/<personal-skill>`;
- complete guidance files at Pi, Codex, OpenCode, and Claude global instruction paths;
- `~/.agent-core-state/ownership.json`;
- derived `memory/memory.sqlite` and `MEMORY_INDEX.md`.

### Global Sync Rules

- `~/.agent-core` is the fixed canonical checkout. Do not add configurable checkout paths, credential handling, or another bootstrap package.
- `personal-skills.toml` is manually maintained and authoritative. Never infer publication from all `skills/` directories.
- Keep the console launcher and CMD installer small and stable. The normal Windows path must not require PowerShell, `uv`, `pip`, elevation, or downloaded packages.
- Require Python 3.10+ and keep runtime code standard-library-only.
- The launcher must reject a dirty checkout and cross a fresh-process boundary before sync code runs. Ordinary sync fast-forwards with authenticated Git; explicit `sync --no-pull` skips only that refresh and publishes the current clean committed checkout without silent fallback.
- Require every configured source and the global guidance source to match tracked committed content.
- Preflight every configured skill, Claude alias, guidance file, and ownership record before replacing any target.
- Refuse unowned collisions, malformed ownership, unsupported entries, and locally modified managed content. Empty unowned guidance files may be initialized.
- Preserve unrelated files under every parent directory. Removing manifest entries remains non-destructive by default.
- Stage and fingerprint copies, replace through backups with rollback, and atomically publish ownership only after all output succeeds.
- Use real copies only under `~/.agents/skills/`. Claude receives links or Windows directory junctions to those copies, never independent duplicates.
- Never modify project `.gitignore`, project source, credentials, MCP settings, or harness security configuration during global sync.
- Report the checkout commit, manifest count, changed skill names, alias status, every guidance status, ownership path, and reload requirement.

Canonical details: `docs/consumer-repo-enrollment.md`.

### Legacy Migration Rules

- `agent-core apply [--here]` is deprecated compatibility and must continue targeting project-local `.agents/skills/`; never silently retarget it globally.
- `agent-core retire-local --here` may remove only fingerprint-matching managed copies and exact legacy state and exclusion entries.
- Refuse tracked or locally modified legacy copies before mutation and preserve unrelated `.agents` and Git exclusion content.
- Do not scan arbitrary repositories for old installations.

### Memory Rules

- The memory pilot remains append-only; `memory/memories.jsonl` is canonical, and generated search/index artifacts are disposable.
- Route memory operations through `uv run scripts/memory.py`, not direct ledger edits.
- New memory topic creation requires explicit human approval. Existing active topics may be updated autonomously within scope.
- Memory tooling is steward-only. Global sync does not create or infer project memory configuration.
- Knowledge-base work uses the canonical Google Drive workflow identified in `global/AGENTS.md`; do not restore the retired repository-local workflow.

## Steward Rules

- Keep `skills/` production-ready and hand-edited.
- Do not edit production workflow skills autonomously.
- Keep durable architecture in `README.md` and detailed stable contracts in focused docs.
- Use `tasks/` only for active execution handoff under `project-tasks`.
- Prefer `uv` for maintainer workflows, while preserving the dependency-free installed runtime.
- Do not rely on checked-in virtual environments or manual `pip install` state.
- Preserve the canonical/installed boundary when adding cross-harness access.
- Prefer minimal reversible foundations over speculative automation.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Durable repository orientation and boundaries. |
| Human operating manual | `docs/agent-core-operating-manual.md` | Canonical setup, sync, publication, migration, verification, and recovery commands. |
| Distribution contract | `docs/consumer-repo-enrollment.md` | Canonical global sync and legacy retirement behavior. |
| Personal list | `personal-skills.toml` | Authoritative copied skill set. |
| Global guidance | `global/AGENTS.md` | Automatically loaded personal behavior for supported harnesses. |
| CLI launcher | `agent_core/bootstrap.py` | Canonical refresh and fresh-process boundary. |
| Sync engine | `agent_core/sync.py` | Copy ownership, conflict safety, rollback, aliases, and guidance. |
| Legacy retirement | `agent_core/retire.py` | Safe cleanup of prior project-local installations. |
| Memory contract | `docs/memory-pilot.md` | Ledger schema, approval boundary, and tooling behavior. |
| Active handoff | `tasks/` | Fresh-session continuity for unfinished work. |
