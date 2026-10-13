# Agent Core

**Last Updated:** 2026-10-13

**Status:** Current

**Source Of Truth:** Defines the purpose and current architecture of the private Agent Core repository.

**Update When:** Canonical layout, personal-skill distribution, or memory architecture changes.

### Read First

- `~/.agent-core` is the fixed canonical private checkout.
- `personal-skills.toml` selects shared skills; `personal-pi.toml` and `personal-devin.toml` select harness-specific subagents and Pi templates.
- `agent-core sync` remains Pi-first. `agent-core sync --harness devin` explicitly publishes the shared skills and declared Devin agents to Devin Desktop/CLI's Windows application-data directory.
- Pi and Devin discover their native resources without settings edits. Global guidance remains unmanaged.
- `skills/` is hand-edited production source. Do not edit production skills without explicit human approval.
- `docs/agent-core-operating-manual.md` is the human command reference. `docs/consumer-repo-enrollment.md` owns the detailed distribution and migration contract.
- `tasks/` holds active execution state; docs and agent guidance hold durable truth.

## Current Contract

### Canonical Surfaces

- `skills/**/SKILL.md`
- `personal-skills.toml`, `personal-pi.toml`, and `personal-devin.toml`
- `agent_core/*.py`
- `pyproject.toml`
- `scripts/install-agent-core.cmd` and `scripts/install_agent_core.py`
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`
- `memory/memories.jsonl` and steward scripts

### Installed And Generated Surfaces

A successful global sync manages only exact declared destinations for the selected harness:

- Pi: `~/.pi/agent/skills/<personal-skill>/`, `agents/<name>.md`, and `prompts/<name>.md`;
- Devin on Windows: `%APPDATA%\devin\skills\<personal-skill>\` and `%APPDATA%\devin\agents\<name>.md`;
- `~/.agent-core-state/ownership.json` — machine-local per-harness ownership, fingerprints and safe legacy-migration state.

Existing global guidance files remain in place but are no longer managed by sync. The first skills-only sync releases their old ownership records without reading or editing the files. Derived memory artifacts such as `memory/memory.sqlite` and `MEMORY_INDEX.md` are generated and disposable.

## Personal Resource Sync

One-time Windows setup uses CMD and an installed Python 3.10 or newer:

```cmd
git clone <private-repo-url> "%USERPROFILE%\.agent-core"
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
agent-core sync
```

The installer uses `py` or `python`, creates a small user-owned command shim, and safely updates the user PATH through the Windows user environment registry. It does not require PowerShell, `uv`, `pip`, elevation, or downloaded Python packages. A new terminal is required when the PATH changed.

After setup, the normal Pi update command is:

```text
agent-core sync
```

Publish the same declared skills plus Devin-specific agents to Devin Desktop/CLI explicitly:

```text
agent-core sync --harness devin
```

When another trusted Git client has already updated the clean canonical checkout and command-line Git cannot reach the remote, `agent-core sync --no-pull` explicitly skips only the fast-forward pull. The launcher otherwise refuses a dirty canonical checkout, fast-forwards with `git pull --ff-only`, and starts the selected committed implementation in a fresh Python process. Sync validates committed manifests and selected resources before mutation, stages and fingerprints the copies, publishes changed shared files through a rollback-capable transaction, and atomically writes ownership state last.

Removing a name from any manifest is normally non-destructive. The prompt-to-skill migration is a narrow exception: Pi sync retires the old managed `commit-with-subagent` prompt only when its recorded fingerprint still matches. Pi also migrates **selected** legacy `.agents/` copies and registered Claude aliases only when ownership is verified, with rollback on failure. Unselected and unowned files remain untouched.

Each harness discovers its native installed paths directly. For every declared destination, the committed repository version replaces any differing installed copy, including previously unmanaged or locally edited content; unsupported file types are refused. Devin custom agents remain harness-specific because their model and tool frontmatter differs from Pi. Sync does not edit either harness's settings or credentials.

Legacy `agent-core apply [--here]` remains temporarily available and deprecated; it still targets project-local `.agents/skills/` and is not retargeted globally. Use `agent-core retire-local --here` in each old target to remove only unchanged managed copies and exact legacy metadata.

See `docs/consumer-repo-enrollment.md` for collision, rollback, alias, ownership, and migration details.

## Repository Working Surfaces

- `skills/` holds production executor skills and is human-approval-gated.
- `global/AGENTS.md` is retained as a former guidance source; sync no longer publishes it.
- `prompts/` holds reusable non-installed source material; `pi/` and `devin/` hold explicitly selected harness-specific resources.
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
| Pi resource list | `personal-pi.toml` | Authoritative Pi agent and prompt allowlist. |
| Devin resource list | `personal-devin.toml` | Authoritative Devin custom-agent allowlist. |
| CLI launcher | `agent_core/bootstrap.py` | Fixed-checkout refresh and fresh-process handoff. |
| Sync engine | `agent_core/sync.py` | Pi-default and explicit Devin publication, ownership, rollback, and Pi legacy migration. |
| Legacy engine | `agent_core/apply.py` | Deprecated project-local compatibility. |
| Retirement engine | `agent_core/retire.py` | Safe removal of old managed project copies. |
| Memory pilot | `docs/memory-pilot.md` | Canonical ledger and approval contract. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-10-08 | Make `agent-core sync` the sole normal personal update command. | Personal workflows should be globally available without stale copies in every project. |
| 2026-10-08 | Use `~/.agents/skills/` as the shared skill authority and Claude links as compatibility aliases. | Pi, Codex, and OpenCode share one portable location while Claude sees the same content without a second copy. |
| 2026-10-08 | Publish one canonical `global/AGENTS.md` to native harness guidance files (superseded). | This coupled office and non-office global instructions. |
| 2026-10-09 | Stop managing global system guidance. | Existing `AGENTS.md` and `CLAUDE.md` remain user-owned. |
| 2026-10-11 | Publish selected resources only under `~/.agents/` (superseded). | Previous shared-root attempt. |
| 2026-10-11 | Default to Pi-native `~/.pi/agent/` paths. | Pi is the current active harness; native discovery needs no manual settings or duplicate resources. |
| 2026-10-13 | Add explicit global Devin publication without changing the Pi default. | Devin Desktop/CLI has native Windows application-data locations for skills and custom agents but no file-based prompt-template equivalent. |
| 2026-10-08 | Require Python 3.10+ with no runtime dependencies. | Python 3.10 is practical with a small manifest parser and avoids introducing a TOML package. |
| 2026-09-15 | Retain the prior project-local apply design only as explicit migration compatibility. | Existing managed copies need a safe retirement path and must not be silently retargeted. |
