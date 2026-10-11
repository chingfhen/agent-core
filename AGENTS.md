# Agent OS Steward Contract

**Last Updated:** 2026-10-11

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain the private Agent Core repository.

**Update When:** Steward roles, canonical surfaces, skill distribution, or integration rules change.

### Read First

- You are the steward agent when working in this repository.
- `skills/` is the hand-edited production source. Do not change production workflow skills unless the human explicitly approves the skill edit.
- `agent-core sync` publishes declared skills, Pi agents and Pi prompt templates under Pi-native `~/.pi/agent/`. No other harness is targeted by default; global guidance and harness settings stay unmanaged.
- Do not hand-maintain managed copies. Sync owns exact declared Pi resources recorded in `~/.agent-core-state/ownership.json`; verified previously managed `.agents/` copies and registered Claude aliases are safely retired during migration.
- `docs/agent-core-operating-manual.md` is the canonical human command reference.
- Before editing `tasks/`, load `project-tasks`. Before editing docs, README, or agent guidance, load `project-docs`.
- Prefer durable guidance updates in `AGENTS.md`, `docs/`, and `prompts/` over production skill edits. `global/AGENTS.md` is retained but no longer published by sync.

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

- `skills/`, `pi/`, `personal-skills.toml`, and `personal-pi.toml`;
- `agent_core/`, `pyproject.toml`, and installer scripts;
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`;
- schemas, steward scripts, and the append-only `memory/memories.jsonl` ledger.

Installed or generated surfaces include:

- real skill copies under `~/.pi/agent/skills/<personal-skill>/`;
- declared Pi agents and templates under `~/.pi/agent/agents/*.md` and `~/.pi/agent/prompts/*.md`;
- `~/.agent-core-state/ownership.json`;
- derived `memory/memory.sqlite` and `MEMORY_INDEX.md`.

### Global Sync Rules

- `~/.agent-core` is the fixed canonical checkout. Do not add configurable checkout paths, credential handling, or another bootstrap package.
- Both personal manifests are manual allowlists. Never infer publication by scanning `skills/` or `pi/`.
- Keep the console launcher and CMD installer small and stable. The normal Windows path must not require PowerShell, `uv`, `pip`, elevation, or downloaded packages.
- Require Python 3.10+ and keep runtime code standard-library-only.
- The launcher must reject a dirty checkout and cross a fresh-process boundary before sync code runs. Ordinary sync fast-forwards with authenticated Git; explicit `sync --no-pull` skips only that refresh and publishes the current clean committed checkout without silent fallback.
- Require every configured skill source to match tracked committed content. Do not require `global/AGENTS.md` for sync.
- Preflight each configured skill, Pi agent/template, and ownership record. Do not inspect or modify global system guidance or harness settings.
- The committed manifest is authoritative for exactly declared Pi-native skills, agents and prompts: overwrite different installed files/directories, even if unmanaged or locally edited. Refuse unsupported file types and unsafe parents. Legacy `.agents/` migration still requires verified fingerprints.
- Preserve unrelated files under every parent directory. Removing manifest entries remains non-destructive by default.
- Stage, fingerprint and verify selected resources; migrate verified legacy-owned copies and registered aliases through the same rollback transaction; atomically publish ownership last. Preserve unrelated, unowned and unselected resources.
- Publish selected files only under `~/.pi/agent/{skills,agents,prompts}/`. Never create copies or aliases for Codex, Claude or other harnesses by default.
- Never modify project `.gitignore`, project source, credentials, MCP settings, or harness security configuration during global sync.
- Successful sync prints the commit, exact declared names/counts, verified Pi root, and migration count when relevant. Conflicts report exact paths.

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
| CLI launcher | `agent_core/bootstrap.py` | Canonical refresh and fresh-process boundary. |
| Sync engine | `agent_core/sync.py` | Pi-native publication, verification, safe migration and rollback. |
| Legacy retirement | `agent_core/retire.py` | Safe cleanup of prior project-local installations. |
| Memory contract | `docs/memory-pilot.md` | Ledger schema, approval boundary, and tooling behavior. |
| Active handoff | `tasks/` | Fresh-session continuity for unfinished work. |
