# Agent OS Steward Contract

**Last Updated:** 2026-09-15

**Status:** Current

**Source Of Truth:** Defines how steward agents maintain the private Agent Core repository.

**Update When:** Steward/executor roles, canonical surfaces, distribution, or integration rules change.

### Read First

- You are the steward agent when working in this repo.
- At the start of every chat, load `agent-os-session` and state `Loaded agent-os-session.`
- `skills/` is the hand-edited production source for executor agents. Do not change production workflow skills unless the human explicitly approves the skill edit.
- The simple personal distribution workflow is `agent-core apply`: it refreshes the fixed clean `~/.agent-core` checkout and copies `core-skills.toml` entries only to `.agents/skills/` in the current Git project.
- Do not hand-maintain consumer copies. Apply owns only exact configured destinations that its project-local fingerprint state proves it installed.
- `scripts/enroll_repo.py` is separate advanced tooling for manifests and live `.claude`/`.opencode` aliases; do not mix its state or behavior into apply.
- Before editing `tasks/`, load `project-tasks`. Before editing docs, README, or agent guidance, load `project-docs`.
- Prefer durable guidance updates in `AGENTS.md`, `docs/`, and `prompts/` over production skill edits.

### Scope

This file governs steward agents maintaining this repository.

### Not Here

Consumer-repo-local instructions, generated output, runtime task state, or detailed implementation contracts.

## Autonomous State And Memory Routing

You are a node in an ongoing execution chain. Improve future repository context while preserving the boundary between active execution state and durable memory.

- **Read-only execution state by default:** The human architect manages `tasks/`. Read tasks for current state, but do not create, edit, or manage them unless explicitly instructed.
- **Route stable truth to `docs/`:** Preserve decisions, invariants, contracts, workflows, and confirmed fixes that future agents would otherwise have to rediscover.
- **Route external evidence to `source-material/`:** Keep third-party references, research, and seed inputs non-canonical.
- **Route superseded material to `archive/`:** Move content only when a newer canonical source clearly replaces it.
- **Use docs first:** Check relevant docs before source when understanding architecture or contracts. Inspect implementation when docs are incomplete or current code behavior must be verified.
- **Keep quality high:** Do not promote transient notes, tentative hypotheses, or session-local debugging artifacts.

## Current Contract

### Roles

- **Steward agent:** Maintains this canonical repository, package, docs, workflows, and memory tooling.
- **Executor agent:** Works in another repo using copied or advanced-enrolled Agent Core skills.
- **Consumer repo:** A Git project receiving simple copied skills or advanced enrollment.

### Canonical And Generated Boundaries

Canonical surfaces include:

- `skills/`;
- `core-skills.toml`;
- `agent_core/` and `pyproject.toml`;
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`;
- `scripts/`, schemas, and the append-only `memory/memories.jsonl` ledger.

Generated surfaces include:

- simple consumer `.agents/skills/<configured-skill>` copies;
- simple ownership state under the actual consumer Git directory;
- simple exact-path entries in the consumer Git common metadata `info/exclude`;
- advanced `.agent-os.json`, `.claude/skills/*`, `.opencode/skills/*`, and `.agent-os-state/enrollments.json`;
- derived `memory/memory.sqlite` and `MEMORY_INDEX.md`.

### Simple Apply Rules

- `~/.agent-core` is the fixed canonical checkout. Do not add configurable checkout paths, credential handling, or another bootstrap package.
- `core-skills.toml` is manually maintained and authoritative; never infer the list from all `skills/` directories.
- Keep the console launcher small and stable. It must reject a dirty canonical checkout, fast-forward with ordinary authenticated Git, and cross a fresh-process import boundary before apply code runs.
- Keep the implementation standard-library-only so ordinary source updates do not require reinstalling dependencies.
- Apply owns only `.agents/skills/<configured-skill>` targets. It must ignore advanced manifests, registries, aliases, and all other skill surfaces.
- Require every configured source file to be tracked in the canonical commit; never copy ignored or other uncommitted source artifacts.
- Preflight every configured target before replacing any. Refuse tracked targets or descendants, unrelated existing content, malformed ownership, unsupported filesystem entries, and locally modified managed copies.
- Store ownership under the actual Git directory and exclusions under the Git common directory so linked worktrees behave correctly.
- Preserve additive removal: unconfigured prior copies, records, and exclusions remain untouched. Do not add automatic removal or force behavior.
- Stage and fingerprint all copies, replace through backups with rollback, and atomically publish ownership only after successful replacement.
- Never change the tracked consumer `.gitignore`; preserve unrelated local exclusion content.

Canonical details: `docs/consumer-repo-enrollment.md`.

### Advanced Enrollment Rules

- Keep `scripts/enroll_repo.py` operational as optional advanced tooling.
- Device-local enrolled paths live in `.agent-os-state/enrollments.json`.
- Keep `.claude/skills/*` and `.opencode/skills/*` aligned during advanced enroll and sync.
- Prefer directory symlinks and fall back to Windows junctions when symlink privileges are unavailable.
- Symlinks and junctions satisfy the advanced live-update guarantee; copied directories do not.
- Preflight targets as missing, managed aliases, or conflicts. A real local skill directory is always a conflict.
- Replace only verified managed aliases. Stop before overwriting unrelated files, directories, broken aliases, or aliases to unexpected sources.
- Never recursively delete, move, or modify a live alias or its harness parent; edits can reach canonical source.
- Remove advanced aliases only through `uv run scripts/enroll_repo.py unenroll --repo <path> --apply` after preview and verification.

### Memory Rules

- The memory pilot remains append-only; `memory/memories.jsonl` is canonical, and generated search/index artifacts are disposable.
- Route memory operations through `uv run scripts/memory.py`, not direct ledger edits.
- Keep executor memory behavior in `agent-os-memory`; do not expand `agent-os-session` into manifest or memory bootstrap behavior.
- New memory topic creation requires explicit human approval. Existing active topics may be updated autonomously within scope.
- Advanced manifest enrollment remains the mechanism for `memory_enabled`; simple apply does not create or infer memory configuration.

## Steward Rules

- Keep `skills/` production-ready and hand-edited.
- Do not edit production workflow skills autonomously.
- Keep durable architecture in `README.md` and detailed stable contracts in focused docs.
- Use `tasks/` only for active execution handoff, under the `project-tasks` workflow.
- Prefer `uv`; use the packaged project for `agent-core` and PEP 723 single-file scripts for standalone steward tools.
- Do not rely on checked-in virtual environments or manual `pip install` state.
- Preserve the canonical/generated boundary when adding cross-harness access.
- Prefer minimal reversible foundations over speculative automation.
- Use `uv run scripts/enroll_repo.py verify --repo <path>` when the advanced live-alias guarantee needs confirmation.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Durable repository orientation and boundaries. |
| Distribution contract | `docs/consumer-repo-enrollment.md` | Canonical simple apply and advanced alias behavior. |
| Core list | `core-skills.toml` | Authoritative copied skill set. |
| CLI launcher | `agent_core/bootstrap.py` | Canonical refresh and fresh-process boundary. |
| Apply engine | `agent_core/apply.py` | Copy ownership, conflict safety, rollback, and exclusions. |
| Session skill | `skills/agent-os-session/SKILL.md` | Shared session-start routing and visible confirmation. |
| Advanced enrollment | `scripts/enroll_repo.py` | Optional manifest and live-alias workflow. |
| Memory contract | `docs/memory-pilot.md` | Ledger schema, approval boundary, and tooling behavior. |
| Memory tooling | `scripts/memory.py` | List, search, append, and reindex operations. |
| Active handoff | `tasks/` | Fresh-session continuity for unfinished work. |
