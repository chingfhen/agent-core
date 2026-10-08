# Agent Core

**Last Updated:** 2026-10-08

**Status:** Current

**Source Of Truth:** Defines the purpose and current architecture of the private Agent Core repository.

**Update When:** Canonical layout, personal-skill distribution, global guidance, or memory architecture changes.

### Read First

- `~/.agent-core` is the fixed canonical private checkout.
- `personal-skills.toml` is the manual authoritative list of personal skills published by `agent-core sync`.
- Sync installs real skill copies under `~/.agents/skills/`, creates Claude aliases under `~/.claude/skills/`, and publishes `global/AGENTS.md` to each harness's native global guidance path.
- Pi discovers the shared skills in `~/.agents/skills/`; Pi's own directory receives global guidance at `~/.pi/agent/AGENTS.md`, not another skill copy.
- `skills/` is hand-edited production source. Do not edit production skills without explicit human approval.
- `docs/agent-core-operating-manual.md` is the human command reference. `docs/consumer-repo-enrollment.md` owns the detailed distribution and migration contract.
- `tasks/` holds active execution state; docs and agent guidance hold durable truth.

## Current Contract

### Canonical Surfaces

- `skills/**/SKILL.md`
- `personal-skills.toml`
- `global/AGENTS.md`
- `agent_core/*.py`
- `pyproject.toml`
- `scripts/install-agent-core.cmd` and `scripts/install_agent_core.py`
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`
- `memory/memories.jsonl` and steward scripts

### Installed And Generated Surfaces

A successful global sync manages only exact declared destinations:

- `~/.agents/skills/<personal-skill>/` — real copied skill directories;
- `~/.claude/skills/<personal-skill>` — links or Windows directory junctions to the shared copies;
- `~/.pi/agent/AGENTS.md`;
- `~/.codex/AGENTS.md`;
- `~/.config/opencode/AGENTS.md`;
- `~/.claude/CLAUDE.md`;
- `~/.agent-core-state/ownership.json` — machine-local fingerprints and ownership.

Unrelated files under those parent directories are not managed. Derived memory artifacts such as `memory/memory.sqlite` and `MEMORY_INDEX.md` are generated and disposable.

## Personal Skill And Guidance Sync

One-time Windows setup uses CMD and an installed Python 3.10 or newer:

```cmd
git clone <private-repo-url> "%USERPROFILE%\.agent-core"
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
agent-core sync
```

The installer uses `py` or `python`, creates a small user-owned command shim, and safely updates the user PATH through the Windows user environment registry. It does not require PowerShell, `uv`, `pip`, elevation, or downloaded Python packages. A new terminal is required when the PATH changed.

After setup, the normal update command is:

```text
agent-core sync
```

When another trusted Git client has already updated the clean canonical checkout and command-line Git cannot reach the remote, `agent-core sync --no-pull` explicitly skips only the fast-forward pull. The launcher otherwise refuses a dirty canonical checkout, fast-forwards with `git pull --ff-only`, and starts the selected committed implementation in a fresh Python process. Sync validates committed sources and every destination before mutation, stages and fingerprints copies, replaces all changed skills, aliases, and guidance as one rollback-capable operation, and publishes ownership state last.

Removing a name from `personal-skills.toml` is non-destructive. Existing installed copies, aliases, and ownership records remain until an explicit future prune or manual resolution. The manifest is never inferred from every directory under `skills/`.

Legacy `agent-core apply [--here]` remains temporarily available and deprecated; it still targets project-local `.agents/skills/` and is not retargeted globally. Use `agent-core retire-local --here` in each old target to remove only unchanged managed copies and exact legacy metadata.

See `docs/consumer-repo-enrollment.md` for collision, rollback, alias, ownership, and migration details.

## Repository Working Surfaces

- `skills/` holds production executor skills and is human-approval-gated.
- `global/` holds canonical cross-harness global guidance.
- `prompts/` holds reusable prompt and policy source material.
- `docs/`, `README.md`, and `AGENTS.md` hold durable repository truth and behavior.
- `tasks/` holds active execution handoff and fresh-session continuity.
- `source-material/` holds non-canonical seed inputs and supporting artifacts.
- `archive/` holds retired historical reference material.

## Memory Pilot

- `memory/memories.jsonl` is the append-only canonical ledger.
- Search and index outputs are disposable and untracked.
- Memory tooling remains steward-only and is run through `uv run scripts/memory.py`.
- Global sync does not configure project memory or replace the canonical Google Drive knowledge-base workflow.

## Dependency Strategy

- Runtime and installation require Python 3.10+ and use only the standard library.
- The Windows installer and generated shim do not install the package or dependencies.
- `uv` remains an optional maintainer convenience, not an installation or runtime requirement.
- Standalone steward scripts may continue using `uv run` and PEP 723 metadata where appropriate.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Steward contract | `AGENTS.md` | Governs maintainers and safety boundaries. |
| Human operating manual | `docs/agent-core-operating-manual.md` | Setup, sync, publication, verification, migration, and recovery commands. |
| Distribution contract | `docs/consumer-repo-enrollment.md` | Canonical global publication and legacy retirement behavior. |
| Personal skill list | `personal-skills.toml` | Authoritative copied skill set. |
| Global guidance | `global/AGENTS.md` | Canonical guidance published to all four harnesses. |
| CLI launcher | `agent_core/bootstrap.py` | Fixed-checkout refresh and fresh-process handoff. |
| Sync engine | `agent_core/sync.py` | Global publication, ownership, aliases, and rollback. |
| Legacy engine | `agent_core/apply.py` | Deprecated project-local compatibility. |
| Retirement engine | `agent_core/retire.py` | Safe removal of old managed project copies. |
| Memory pilot | `docs/memory-pilot.md` | Canonical ledger and approval contract. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-10-08 | Make `agent-core sync` the sole normal personal update command. | Personal workflows should be globally available without stale copies in every project. |
| 2026-10-08 | Use `~/.agents/skills/` as the shared skill authority and Claude links as compatibility aliases. | Pi, Codex, and OpenCode share one portable location while Claude sees the same content without a second copy. |
| 2026-10-08 | Publish one canonical `global/AGENTS.md` to native harness guidance files. | Mandatory routing should load automatically without a startup skill. |
| 2026-10-08 | Require Python 3.10+ with no runtime dependencies. | Python 3.10 is practical with a small manifest parser and avoids introducing a TOML package. |
| 2026-09-15 | Retain the prior project-local apply design only as explicit migration compatibility. | Existing managed copies need a safe retirement path and must not be silently retargeted. |
