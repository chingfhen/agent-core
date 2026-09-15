# Agent OS

**Last Updated:** 2026-09-15

**Status:** Current

**Source Of Truth:** Defines the purpose and current architecture of the private Agent Core repository.

**Update When:** Canonical layout, skill distribution, or memory architecture changes.

### Read First

- `~/.agent-core` is the fixed canonical private checkout for cross-device use.
- `skills/` is the hand-edited production source. Do not edit production skills without explicit human approval.
- Use `agent-core apply --here` to copy `core-skills.toml` entries into the current directory's `.agents/skills/`, whether or not the directory is a Git worktree. Plain `agent-core apply` retains Git-root targeting.
- Copied skills update only when apply runs. Project-local ownership fingerprints prevent unrelated or locally modified content from being overwritten.
- `scripts/enroll_repo.py` is deprecated compatibility tooling. Do not use it for new targets; retain it only for safe maintenance or retirement of existing alias enrollments.
- `docs/agent-core-operating-manual.md` is the human command reference. `AGENTS.md` is the steward operating contract, and `docs/consumer-repo-enrollment.md` owns the technical distribution contract.
- `tasks/` holds active execution state, while `docs/`, this README, and `AGENTS.md` hold durable truth.

### Scope

This document orients maintainers to repository purpose, canonical/generated boundaries, skill distribution, and the memory pilot.

### Not Here

Detailed implementation tasks, generated consumer output, or session history.

## Current Contract

### Terms

- **Steward agent:** An agent maintaining this canonical repository.
- **Executor agent:** An agent working in another repo that consumes Agent Core capabilities.
- **Consumer target:** A directory receiving copied core skills; deprecated alias installations retain a compatibility contract only.

### Canonical Surfaces

- `skills/**/SKILL.md`
- `core-skills.toml`
- `agent_core/*.py`
- `pyproject.toml`
- `docs/**/*.md`
- `README.md`
- `AGENTS.md`
- `prompts/**/*.md`
- `memory/memories.jsonl`
- `scripts/*`
- `schemas/*`

### Generated Or Installed Surfaces

Simple apply workflow:

- target `.agents/skills/<configured-skill>` copies;
- target-local `.agents/.agent-core/ownership.json` for `--here`, or `<actual-git-dir>/agent-core/ownership.json` for plain apply;
- a managed exact-path block in `<git-common-dir>/info/exclude` when Git is available.

Deprecated alias compatibility surfaces:

- existing consumer `.agent-os.json`;
- existing consumer `.claude/skills/*` and `.opencode/skills/*` aliases;
- device-local `.agent-os-state/enrollments.json`.

Derived memory artifacts such as `memory/memory.sqlite` and `MEMORY_INDEX.md` are generated and disposable.

## Skill Distribution

### Simple Personal Workflow

One-time setup on each machine:

```powershell
git clone <private-gitlab-url> "$HOME\.agent-core"
uv tool install --editable "$HOME\.agent-core"
```

To target the current directory exactly, whether or not it is a Git worktree:

```text
agent-core apply --here
```

Plain `agent-core apply` remains available inside a Git worktree and targets that worktree's root.

The stable console launcher refuses a dirty canonical checkout, runs `git pull --ff-only`, and starts the newly pulled apply implementation in a fresh process. The implementation requires configured source files to match committed Git content and validates all project targets before replacement. It stages verified copies, uses backup-and-rollback replacement, atomically records ownership, and locally excludes exact copied paths without changing project `.gitignore`.

Only `core-skills.toml` controls the copied set. Removing a configured name is non-destructive: the prior copy, ownership record, and exclusion remain. Apply has no deletion or force behavior.

`--here` keeps ownership state under `<current-directory>/.agents/.agent-core/`. When the directory is inside Git, tracked-target refusal and local Git exclusions still apply. Outside Git, those Git-only checks are skipped.

See `docs/consumer-repo-enrollment.md` for source validation, tracked-target refusal, linked-worktree metadata, fingerprint, and failure semantics.

### Deprecated Alias Compatibility

Do not use `scripts/enroll_repo.py enroll` or `sync` for new targets. The registry-backed symlink/junction workflow is deprecated and retained only to avoid breaking existing installations.

When an existing alias enrollment must be inspected or retired, use its `verify` and preview-first `unenroll` commands rather than recursively deleting managed alias paths. Real local directories and unexpected aliases remain conflicts.

The normal `agent-core apply --here` workflow ignores all deprecated surfaces outside its exact `.agents/skills/<configured-skill>` targets.

## Repository Working Surfaces

- `skills/` holds production executor skills and is human-approval-gated.
- `prompts/` holds canonical reusable prompt snippets and policy blocks.
- `docs/`, `README.md`, and `AGENTS.md` hold durable repository truth and behavior.
- `tasks/` holds active execution handoff and fresh-session continuity.
- `source-material/` holds non-canonical seed inputs and supporting artifacts.
- `archive/` holds retired historical reference material.

## Memory Pilot

- The canonical ledger is append-only `memory/memories.jsonl`.
- `memory/memories.jsonl` is the only tracked memory artifact.
- Search and index outputs in `memory/memory.sqlite` and `MEMORY_INDEX.md` are disposable and untracked.
- Steward agents own canonical memory tooling and publication.
- Executor memory behavior remains available only to existing deprecated manifest enrollments where `memory_enabled` is true; the normal apply workflow does not enable memory.
- `agent-os-memory` reads manifest context directly and exposes `uv run scripts/memory.py` list, search, write, and reindex flows.
- Creating a new `topic_key` requires explicit human approval; updates within an existing active topic can be autonomous.

## Dependency Strategy

- The packaged CLI requires Python 3.11+ and has no runtime dependencies outside the standard library.
- Use `uv tool install --editable "$HOME\.agent-core"` for the console command.
- Continue running standalone steward scripts with `uv run`; retain PEP 723 metadata where those scripts need it.
- Do not rely on checked-in virtual environments or manual `pip install` state.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Steward contract | `AGENTS.md` | Governs maintainers and safety boundaries. |
| Human operating manual | `docs/agent-core-operating-manual.md` | Commands for setup, normal use, skill publication, verification, and recovery. |
| Distribution contract | `docs/consumer-repo-enrollment.md` | Canonical simple apply and deprecated alias behavior. |
| Core skill list | `core-skills.toml` | Authoritative copied skill set. |
| CLI launcher | `agent_core/bootstrap.py` | Owns fixed-checkout refresh and fresh-process handoff. |
| Apply engine | `agent_core/apply.py` | Owns safe copy, state, exclusions, and rollback. |
| Deprecated alias tooling | `scripts/enroll_repo.py` | Compatibility maintenance and verified retirement for existing enrollments only. |
| Memory pilot | `docs/memory-pilot.md` | Canonical ledger and approval contract. |
| Memory tooling | `scripts/memory.py` | Implements ledger list, search, write, and reindex. |
| Active handoff | `tasks/` | Fresh-session continuity for unfinished work. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-09-15 | Use `agent-core apply --here` and fixed `~/.agent-core` as the normal private skill workflow. | One exact-directory command works consistently in Git and non-Git targets. |
| 2026-09-15 | Copy only the manually configured core list to `.agents/skills/` with local ownership fingerprints. | A single destination and fail-closed ownership allow safe explicit updates without overwriting project content. |
| 2026-09-15 | Deprecate alias enrollment for new targets while retaining compatibility maintenance. | The copy workflow replaces routine symlink/junction enrollment without forcing unsafe cleanup of existing installations. |
| 2026-06-18 | `skills/` remains the canonical production source. | Cross-project reuse needs one hand-edited authority. |
| 2026-06-18 | Memory truth remains append-only JSONL. | Immutable truth is easy to synchronize, audit, and regenerate. |
