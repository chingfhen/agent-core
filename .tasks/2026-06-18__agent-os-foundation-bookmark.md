# Task: Agent OS foundation

**File:** `.tasks/2026-06-18__agent-os-foundation-bookmark.md`
**Created:** 2026-06-18
**Last Updated:** 2026-06-19
**Priority:** Now
**Status:** Closed
**Docs Sync:** Synced
**Deletion Status:** Safe to delete

**Goal:** Build the first working Agent OS foundation in this repo: steward-managed repo enrollment, repo-local skill alias installs, thin bootstrap behavior, and only then a minimal memory pilot.
**Success Bar:** `skills/` remains canonical, steward docs are stable, `agent-os-bootstrap` is scoped to manifest hydration, consumer repos can be safely enrolled with repo-local aliases plus a gitignored `.agent-os.json`, and the skill foundation is ready for the later memory pilot.
**Current State:** The skills foundation is complete. `skills/agent-os-bootstrap/SKILL.md`, `schemas/agent-os-manifest.schema.json`, `schemas/examples/consumer-repo.agent-os.example.json`, and `scripts/enroll_repo.py` are in place; the pilot repo at `C:\Users\chingfhen\Documents\ST Eng\projects\Einstein\summarization-project` is enrolled with live `.claude/skills/*` aliases; `verify` confirms the live-update guarantee; copied skill directories are auto-replaced during enroll and sync; and the local steward registry remembers the working Windows link mode for faster future enrollments.
**Next Action:** Open a separate follow-up bookmark when starting the minimal memory pilot or any later Codex-specific alias work.
**Blockers:** None. This foundation task is complete.

**Target Docs:** `README.md`, `AGENTS.md`, `docs/consumer-repo-enrollment.md`
**Relevant Code:** `.raw/initialize.md`, `skills/project-docs/SKILL.md`, `skills/project-tasks/SKILL.md`, `skills/agent-os-bootstrap/SKILL.md`, `schemas/agent-os-manifest.schema.json`, `scripts/enroll_repo.py`

## Human Intent

- Centralize core skills once in this repo and let the steward reuse them across devices and consumer repos.
- Let the steward enroll repos by installing local harness aliases and repo-local manifests instead of relying on manual setup.
- Keep executor experience simple: local skills should look ordinary and should not expose canonical or symlink internals.
- Keep generated consumer-repo setup local and gitignored so teammates are not confused by personal Agent OS files.
- Add memory later as a separate skill and workflow, not as bootstrap behavior.

## Expected Outcomes

- `README.md`, `AGENTS.md`, and `docs/consumer-repo-enrollment.md` define steward-managed per-device repo enrollment and repo-local skill alias installs.
- The active task preserves the final v1 contract, safety rules, and remaining implementation unknowns.
- `agent-os-bootstrap` is explicitly scoped to reading `.agent-os.json` and hydrating runtime context.
- Future implementation will generate a gitignored `.agent-os.json`, exact managed alias ignore entries, and device-local steward enrollment state.
- Memory remains a later separate `agent-os-memory` layer rather than bootstrap scope.
- The durable docs define steward-owned canonical memory publication plus executor-facing list/search/write memory flows for later implementation.

## Decisions Locked

- `AGENTS.md` is the authoritative steward-agent contract.
- `README.md` is the durable repo architecture and orientation surface.
- `skills/` is the production source for executor agents.
- Consumer repos each get their own `.agent-os.json`.
- This system does not depend on modifying consumer repo `AGENTS.md`.
- `skills/agent-os-bootstrap/SKILL.md` is the canonical executor bootstrap skill.
- Consumer repos are enrolled per device by steward workflows rather than manual manifest placement.
- Executors consume repo-local skill aliases and should not reason about canonical provenance.
- `.agent-os.json` is repo-local generated state and gitignored by default.
- Ignore exact managed alias paths by default unless the repo already ignores a broader harness path.
- `agent-os-bootstrap` only reads `.agent-os.json` and hydrates runtime context.
- Future memory behavior belongs in a separate `agent-os-memory` skill.
- Python steward scripts should use `uv`; each device installs `uv` and Python 3.11+ once, while script dependencies stay inline via PEP 723.
- Start steward automation with `uv run` plus PEP 723 single-file scripts; do not add a repo-wide `pyproject.toml` unless shared tooling later justifies it.
- Shared local project skills standardize on `.claude/skills`; Claude uses that path natively and OpenCode also discovers it.
- Windows enrollment defaults to directory symlinks with a directory-junction fallback when symlink privileges are unavailable.
- Device-local enrollment state lives in `.agent-os-state/enrollments.json`.
- The consumer-repo manifest stays minimal with six required fields; selected skills, surfaces, and link mode live in the local steward registry rather than `.agent-os.json`.
- The trusted steady state is live aliasing, not copied skill directories; enroll and sync auto-replace matching local copies and `verify` confirms the guarantee.
- Executors should discover existing memory topics via future list/search tooling exposed by `agent-os-memory`, not by inspecting storage internals or relying on a hand-maintained registry.
- Steward owns canonical memory commits and publication decisions in `~/agent-os`; executors may use memory when enabled but should not publish canonical repo changes themselves.
- MCP is not the primary skill-delivery path in v1.
- Memory is a pilot and should remain minimal until it proves useful.

## Non-Goals / Stop Conditions

- Do not introduce tracked `.opencode`, `.claude`, or `.codex` skill copies in this repo.
- Do not build MCP-first infrastructure for skills.
- Do not over-design the memory system beyond the agreed pilot.
- Do not treat `.raw/initialize.md` as the active source of truth after the new docs are in place.
- Do not make executors discover canonical skill locations directly.
- Do not overwrite unrelated existing harness files or directories without explicit approval.

## Current Understanding

- There are two distinct roles: the steward agent maintains `~/agent-os`, and the executor agent consumes Agent OS while working in a different repo.
- `AGENTS.md` solves steward alignment, not executor bootstrap.
- The steward owns device enrollment and repo-local harness alias management.
- Executor agents should consume ordinary local skill aliases without being taught whether they are canonical, symlinked, or copied.
- `.agent-os.json` is repo-specific, low-churn, generated by the steward, and gitignored by default.
- `agent_os_path` should remain in `.agent-os.json` so future scripts and memory tooling can still locate the canonical repo.
- The first local skill surface is `.claude/skills`; OpenCode can share it because it discovers Claude-compatible project skills.
- Selected skills, target surfaces, and actual link mode are local steward concerns stored in `.agent-os-state/enrollments.json`, not in `.agent-os.json`.
- Directory symlinks and directory junctions both satisfy the live-update guarantee because they resolve the consumer repo path back to the canonical skill directory.
- Memory truth should stay immutable in JSONL; derived state belongs in SQLite and search output.
- Executors should learn existing memory topics through future list/search tooling rather than direct repository internals.
- The first memory tooling surface is list/search/write/supersede, not destructive delete or edit-in-place CRUD.

## Remaining Uncertainty

- Codex repo-local skill semantics and whether it can share an existing surface without duplicate-name collisions.
- Whether future repo-local Agent OS settings should stay as optional extra manifest keys or move into a separate steward-managed surface.
- Whether the minimal memory pilot should stay in this task or be split into a focused follow-up bookmark.

## Executor Guidance

- Keep the first implementation narrow: skills foundation first, memory second.
- Define `agent-os-bootstrap` early, but keep it limited to manifest hydration.
- Prefer steward scripts over manual harness duplication.
- Preserve the canonical/generated boundary in every file and automation choice.
- Treat consumer-repo outputs as generated local state, not canonical content.
- Preflight every target alias path as `missing`, `managed`, or `conflict`; only auto-replace `managed`.
- Prefer exact managed gitignore entries over blanket harness ignores unless broader ignores already exist.
- Use `.claude/skills` as the shared local surface for Claude and OpenCode until another harness proves it needs a distinct path.
- Treat matching local skill directories as replaceable transitional state and converge them automatically to live aliases.
- Use `verify` when you need an explicit yes-or-no answer about whether canonical skill updates propagate immediately.
- If implementing memory, preserve append-only JSONL and derive active/superseded state outside the ledger.
- If implementing memory, start with list/search/write/supersede scripts rather than a full destructive CRUD surface.

## Likely Blind Spots

- Reintroducing the older model where OpenCode points directly at canonical skills rather than repo-local aliases.
- Duplicating the same skill names under both `.claude/skills` and `.opencode/skills`, which would collide for OpenCode discovery.
- Treating `.agent-os.json` as team-shared tracked config instead of local generated state.
- Wiping entire harness directories instead of only the steward-managed alias paths.
- Assuming Windows symlink privileges exist everywhere instead of planning for junction fallback.
- Mistaking an exact copied skill directory for a trusted live alias when updates do not actually propagate.
- Growing `agent-os-bootstrap` into a memory or tooling instruction dump.

## Execution Sequence

1. Completed: add minimal repo scaffolding for future `memory/`, `repo-profiles/`, and `scripts/` surfaces plus ignore rules for generated artifacts.
2. Completed: add the canonical `skills/agent-os-bootstrap/SKILL.md` with executor-facing bootstrap instructions centered on reading `.agent-os.json`.
3. Completed: define the initial `.agent-os.json` schema and example manifest for consumer repos.
4. Completed: add the first steward script with `uv` plus PEP 723 metadata rather than a repo-local virtualenv workflow.
5. Completed: implement the first skills integration path as steward-managed `.claude/skills/*` alias installs, exact managed ignore entries, and device-local enrollment state.
6. Completed: validate the flow against the pilot repo at `C:\Users\chingfhen\Documents\ST Eng\projects\Einstein\summarization-project`, including Windows junction fallback and repair dry-runs.
7. Next: implement the minimal memory pilot only after the skill foundation is working:
    - append-only `memory/memories.jsonl`
    - generated `memory.sqlite`
    - list/search/write scripts
    - human-gated new `topic_key` flow

## Verification Contract

- Confirm the repo docs and task remain aligned after any scaffolding.
- Verify enrollment can write `.agent-os.json` and exact managed ignore entries without touching unrelated repo files.
- Verify local aliases are discoverable and can be repaired when already steward-managed.
- Verify conflict paths stop for approval instead of overwriting unrelated files or directories.
- Verify Windows link fallback can recover to managed state when directory symlinks are not permitted.
- Verify `verify` only returns success when every enrolled skill is a live symlink or junction rather than a copied directory.
- Dry-run memory list/search/write flows before adding extra features.
- Verify enabled memory tooling can list existing topics without requiring executors to inspect storage internals.
- Treat bootstrap behavior as successful if a fresh executor can read `.agent-os.json` and correctly hydrate repo-local Agent OS context from the installed local alias.

## Context Pointers

- `README.md`
- `AGENTS.md`
- `docs/consumer-repo-enrollment.md`
- `.raw/initialize.md`
- `scripts/enroll_repo.py`
- `schemas/agent-os-manifest.schema.json`
- `schemas/examples/consumer-repo.agent-os.example.json`
- `C:\Users\chingfhen\Documents\ST Eng\projects\Einstein\summarization-project`
- `skills/project-docs/SKILL.md`
- `skills/project-tasks/SKILL.md`
