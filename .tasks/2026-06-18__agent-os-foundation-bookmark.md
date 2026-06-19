# Task: Agent OS foundation

**File:** `.tasks/2026-06-18__agent-os-foundation-bookmark.md`
**Created:** 2026-06-18
**Last Updated:** 2026-06-18
**Priority:** Now
**Status:** Active
**Docs Sync:** Synced

**Goal:** Build the first working Agent OS foundation in this repo: centralized skill delivery plus a minimal memory pilot, following the decisions now documented in `README.md` and `AGENTS.md`.
**Success Bar:** `skills/` remains canonical, steward docs are stable, `agent-os-bootstrap` is defined in the canonical skill store, the first implementation scaffolding exists, OpenCode and Claude skill integration is implemented or demonstrably wired, and the initial memory ledger/search flow exists with human-gated new topic keys.
**Current State:** Architecture is aligned and documented. The repo currently contains the two canonical skills under `skills/`, the historical seed spec in `.raw/initialize.md`, and no implementation scaffolding yet.
**Next Action:** Start with the smallest foundation: scaffold the repo structure, define `skills/agent-os-bootstrap/SKILL.md`, then implement `sync_skills.py` for OpenCode and Claude before attempting memory scripts.
**Blockers:** None. Validate Windows symlink behavior and the exact OpenCode global skill-path configuration during implementation.

**Target Docs:** `README.md`, `AGENTS.md`
**Relevant Code:** `.raw/initialize.md`, `skills/project-docs/SKILL.md`, `skills/project-tasks/SKILL.md`

## Human Intent

- Centralize core skills once and reuse them across devices, repos, and harnesses.
- Make `skills/` the production source of truth.
- Keep harness-specific copies generated or configured, never primary.
- Pilot cross-project memory, but do not over-commit to it before proving value.

## Expected Outcomes

- `~/agent-os` becomes the canonical repo cloned across devices.
- OpenCode and Claude can both access the latest production skills from the canonical source.
- Executor agents can be explicitly pointed to `agent-os-bootstrap` to interpret `.agent-os.json` and use Agent OS correctly inside consumer repos.
- Consumer repos can declare repo-scoped behavior with a repo-local `.agent-os.json`.
- Memory starts as a lean append-only JSONL plus generated SQLite index.
- The system stays simple enough that the human can manually bridge bootstrap gaps when needed.

## Decisions Locked

- `AGENTS.md` is the authoritative steward-agent contract.
- `README.md` is the durable repo architecture and orientation surface.
- `skills/` is the production source for executor agents.
- Consumer repos each get their own `.agent-os.json`.
- This system does not depend on modifying consumer repo `AGENTS.md`.
- `skills/agent-os-bootstrap/SKILL.md` is the canonical executor bootstrap skill.
- The human may explicitly direct executor agents to use `agent-os-bootstrap` in consumer repos.
- OpenCode should prefer direct canonical skill-path configuration.
- Claude should use a generated install surface derived from canonical skills.
- Python steward scripts should use `uv`; each device installs `uv` and Python 3.11+ once, while script dependencies stay inline via PEP 723.
- MCP is not the primary skill-delivery path in v1.
- Memory is a pilot and should remain minimal until it proves useful.

## Non-Goals / Stop Conditions

- Do not introduce tracked `.opencode`, `.claude`, or `.codex` skill copies in this repo.
- Do not build MCP-first infrastructure for skills.
- Do not over-design the memory system beyond the agreed pilot.
- Do not treat `.raw/initialize.md` as the active source of truth after the new docs are in place.

## Current Understanding

- There are two distinct roles: the steward agent maintains `~/agent-os`, and the executor agent consumes Agent OS while working in a different repo.
- `AGENTS.md` solves steward alignment, not executor bootstrap.
- Executor bootstrap will initially rely on globally available canonical skills, `agent-os-bootstrap`, repo-local `.agent-os.json`, and explicit human direction when needed.
- `.agent-os.json` is repo-specific, low-churn, and manually placed in each consumer repo.
- Memory truth should stay immutable in JSONL; derived state belongs in SQLite and search output.

## Remaining Uncertainty

- The exact OpenCode configuration shape to point at `~/agent-os/skills` during rollout.
- Whether Claude syncing should use symlinks only or need a Windows fallback in some environments.
- The smallest useful schema for `.agent-os.json` beyond `agent_os_path`, `scope`, `scope_id`, and optional `repo_profile`.
- Whether the first memory pass should include a separate topic registry file or encode approval flow another way.
- Whether any shared test tooling later justifies a `pyproject.toml`, or whether `uv` script execution remains sufficient.

## Executor Guidance

- Keep the first implementation narrow: skills foundation first, memory second.
- Define `agent-os-bootstrap` early because it closes the shared executor bootstrap gap without requiring consumer-repo `AGENTS.md` edits.
- Prefer scripts over manual harness duplication.
- Preserve the canonical/generated boundary in every file and automation choice.
- If a choice is between a direct canonical path and a copied surface, prefer the direct path unless harness constraints block it.
- If implementing memory, preserve append-only JSONL and derive active/superseded state outside the ledger.

## Execution Sequence

1. Add minimal repo scaffolding for future `memory/`, `repo-profiles/`, and `scripts/` surfaces plus ignore rules for generated artifacts.
2. Add the canonical `skills/agent-os-bootstrap/SKILL.md` with executor-facing bootstrap instructions centered on `.agent-os.json`.
3. Implement the first skills integration path:
   - OpenCode reads canonical skills from `~/agent-os/skills` via configuration.
   - Claude receives generated installs derived from canonical skills.
4. Define the initial `.agent-os.json` schema and example manifest for consumer repos.
5. Add the first steward scripts with `uv` plus PEP 723 metadata rather than a repo-local virtualenv workflow.
6. Implement the minimal memory pilot only after the skill foundation is working:
   - append-only `memory/memories.jsonl`
   - generated `memory.sqlite`
   - search/write scripts
   - human-gated new `topic_key` flow

## Verification Contract

- Confirm the repo docs and task remain aligned after any scaffolding.
- Verify OpenCode can be pointed at canonical skills without duplicating tracked content.
- Verify Claude install output is generated from canonical skills, not hand-maintained.
- Dry-run memory write/search flows before adding extra features.
- Treat bootstrap behavior as successful if the human can reliably direct an executor agent to the canonical skills and repo manifest.

## Context Pointers

- `README.md`
- `AGENTS.md`
- `.raw/initialize.md`
- `skills/project-docs/SKILL.md`
- `skills/project-tasks/SKILL.md`
