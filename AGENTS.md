# Agent OS Steward Contract

**Last Updated:** 2026-10-14

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain the private Agent Core repository.

**Update When:** Steward roles, canonical surfaces, skill distribution, or integration rules change.

### Read First

- You are the steward agent when working in this repository.
- `skills/` is the hand-edited production source. Do not change production workflow skills unless the human explicitly approves the skill edit.
- `agent-core sync` defaults to Pi-native publication. `agent-core sync --harness devin` explicitly publishes shared skills and declared Devin agents under `%APPDATA%\devin\`; global guidance and harness settings stay unmanaged.
- Do not hand-maintain managed copies. Sync owns exact declared per-harness resources recorded in `~/.agent-core-state/ownership.json`; verified previously managed `.agents/` copies and registered Claude aliases are safely retired only by Pi migration.
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

- `skills/`, `pi/`, `devin/`, `personal-skills.toml`, `personal-pi.toml`, and `personal-devin.toml`;
- `agent_core/`, `pyproject.toml`, and installer scripts;
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`;
- schemas, steward scripts, and the append-only `memory/memories.jsonl` ledger.

Installed or generated surfaces include:

- real skill copies under `~/.pi/agent/skills/<personal-skill>/`;
- declared Pi agents and templates under `~/.pi/agent/agents/*.md` and `~/.pi/agent/prompts/*.md`;
- explicit Devin copies under `%APPDATA%\devin\skills\` and `%APPDATA%\devin\agents\`;
- `~/.agent-core-state/ownership.json`;
- derived `memory/memory.sqlite` and `MEMORY_INDEX.md`.

### Global Sync Rules

- `~/.agent-core` is the fixed canonical checkout. Do not add configurable checkout paths, credential handling, or another bootstrap package.
- All three personal manifests are manual allowlists. Never infer publication by scanning `skills/`, `pi/`, or `devin/`.
- Keep the console launcher and CMD installer small and stable. The normal Windows path must not require PowerShell, `uv`, `pip`, elevation, or downloaded packages.
- Require Python 3.10+ and keep runtime code standard-library-only.
- The launcher must reject a dirty checkout and cross a fresh-process boundary before sync code runs. Ordinary sync fast-forwards with authenticated Git; explicit `sync --no-pull` skips only that refresh and publishes the current clean committed checkout without silent fallback.
- Require every configured skill source to match tracked committed content. Do not require `global/AGENTS.md` for sync.
- Preflight each configured skill, harness-specific agent/template, and ownership record. Do not inspect or modify global system guidance or harness settings.
- The committed manifests are authoritative for exactly declared destinations in the selected harness: overwrite different installed files/directories, even if unmanaged or locally edited. Refuse unsupported file types and unsafe parents. Legacy `.agents/` migration still requires verified fingerprints and remains Pi-only.
- Preserve unrelated files under every parent directory. Removing manifest entries remains non-destructive by default; a named one-time resource migration may retire only its unchanged fingerprint-owned predecessor.
- Stage, fingerprint and verify selected resources; migrate verified legacy-owned copies and registered aliases through the same rollback transaction; atomically publish ownership last. Preserve unrelated, unowned and unselected resources.
- Default sync publishes selected files only under `~/.pi/agent/{skills,agents,prompts}/`. The explicit Devin harness publishes only under `%APPDATA%\devin\{skills,agents}\`; never target another harness implicitly.
- Never modify project `.gitignore`, project source, credentials, MCP settings, or harness security configuration during global sync.
- Successful sync prints the commit, selected harness, exact declared names/counts, verified native root, and Pi migration count when relevant. Conflicts report exact paths.

Canonical details: `docs/consumer-repo-enrollment.md`.

### Legacy Migration Rules

- `agent-core apply [--here]` is deprecated compatibility and must continue targeting project-local `.agents/skills/`; never silently retarget it globally.
- `agent-core retire-local --here` may remove only fingerprint-matching managed copies and exact legacy state and exclusion entries.
- Refuse tracked or locally modified legacy copies before mutation and preserve unrelated `.agents` and Git exclusion content.
- Do not scan arbitrary repositories for old installations.

### Memory Rules

- The memory pilot remains append-only; `memory/memories.jsonl` is canonical, and generated search/index artifacts are disposable.
- Route steward-ledger operations through `uv run scripts/memory.py`, not direct ledger edits.
- New ledger topic creation requires explicit human approval. Existing active ledger topics may be updated autonomously within scope.
- Memory tooling is steward-only. Global sync does not create or infer project memory configuration.
- The canonical knowledge-base workflow is `skills/knowledge-base/SKILL.md`, selected in `personal-skills.toml`. It owns reusable Markdown records and explicitly requested managed artifacts, not this memory ledger. Retrieval may be proactive when relevant; capture, inbox processing, and artifact writes require an explicit request. The former Drive workflow is no longer authoritative; changing the skill does not migrate KB content.

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
| Sync engine | `agent_core/sync.py` | Pi-default and explicit Devin publication, verification, safe migration and rollback. |
| Legacy retirement | `agent_core/retire.py` | Safe cleanup of prior project-local installations. |
| Memory contract | `docs/memory-pilot.md` | Ledger schema, approval boundary, and tooling behavior. |
| Active handoff | `tasks/` | Fresh-session continuity for unfinished work. |
