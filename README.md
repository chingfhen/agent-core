# Agent Core

**Last Updated:** 2026-10-30

**Status:** Current

**Source Of Truth:** Defines the purpose and current architecture of the private Agent Core repository.

**Update When:** Canonical layout, personal-skill distribution, memory architecture, or the Places contract changes.

### Read First

- `~/.agent-core` is the fixed canonical private checkout.
- `personal-skills.toml` selects shared skills; `personal-pi.toml` and `personal-devin.toml` select harness-specific agents and Pi templates.
- `agent-core sync` remains Pi-first. `agent-core sync --harness devin` explicitly publishes shared skills and declared Devin agents; `agent-core sync --harness opencode` publishes shared skills to OpenCode's native global skill directory.
- Pi and Devin discover their native resources without settings edits; OpenCode discovers skills at its native global path. OpenCode sync manages shared skills only. Global guidance remains unmanaged.
- `skills/` is hand-edited production source. Do not edit production skills without explicit human approval.
- `docs/agent-core-operating-manual.md` is the human command reference. `docs/consumer-repo-enrollment.md` owns the detailed distribution and migration contract.
- `scripts/places.py` is a standalone Bash/CMD directory navigator documented in `docs/places.md`; it is independent of Agent Core sync.
- `tasks/` holds active execution state; docs and agent guidance hold durable truth.

## Current Contract

### Canonical Surfaces

- `skills/**/SKILL.md`
- `personal-skills.toml`, `personal-pi.toml`, and `personal-devin.toml`
- `agent_core/*.py`
- `pyproject.toml`
- `scripts/install-agent-core.cmd`, `scripts/install_agent_core.py`, and `scripts/places.py`
- `README.md`, `AGENTS.md`, `docs/`, and `prompts/`
- `memory/memories.jsonl` and steward scripts

### Installed And Generated Surfaces

A successful global sync manages only exact declared destinations for the selected harness:

- Pi: `~/.pi/agent/skills/<personal-skill>/`, `agents/<name>.md`, and `prompts/<name>.md`;
- Devin on Windows: `%APPDATA%\devin\skills\<personal-skill>\` and `%APPDATA%\devin\agents\<name>.md`;
- OpenCode: `~/.config/opencode/skills/<personal-skill>/` only;
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

Publish the shared skills to OpenCode explicitly:

```text
agent-core sync --harness opencode
```

The launcher refuses a dirty checkout or unfinished Git operation, attempts `git pull --ff-only`, and starts the selected committed implementation in a fresh Python process. If pull fails, ordinary sync warns and publishes the existing local commit only after verifying the checkout is still valid, clean, unchanged, and free of unfinished Git operations. Remote freshness is explicitly unverified. `agent-core sync --no-pull` optionally skips the attempt; it is not required for offline/authentication failures. Sync validates committed manifests and selected resources before mutation, stages and fingerprints the copies, publishes changed shared files through a rollback-capable transaction, and atomically writes ownership state last.

Removing a name from any manifest is normally non-destructive. Selecting `agent-builder` triggers the named Agent Builder consolidation: for the selected harness only, retire exact unchanged fingerprint-owned predecessors (the seven original workflows and the known historical names `project-tasks`, `project-docs`, `knowledge-base`, `agent-lessons`, `manage-python-env`, `manage-python-agent-envs`, `manage-python-uv`). Modified, unowned, or unsafe copies block with exact paths before publication; do not delete them automatically. Pi additionally handles its verified legacy `.agents/` copies and registered Claude aliases. Retirement and publication share the existing rollback transaction; unrelated skills and other harnesses are untouched. The prior named Python-only migration remains supported when `run-and-manage-python` alone is selected. Ordinary manifest removal still does not prune. The Pi prompt-to-skill migration also remains supported.

Each harness discovers its native installed paths directly. For every declared destination, the committed repository version replaces any differing installed copy, including previously unmanaged or locally edited content; unsupported file types are refused. OpenCode sync publishes shared skills only; this repository has no OpenCode-specific agent or command source. Devin custom agents remain harness-specific because their model and tool frontmatter differs from Pi. Sync does not edit harness settings or credentials.

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

## Places Directory Navigator

`scripts/places.py` is a standalone, dependency-free personal directory navigator for Linux Bash and Windows CMD. It keeps stable manually aliased favorites separate from a generated Git-repository cache under `~/.agent-core/`, and installs the minimal shell integration required for an interactive selection to change the current directory. It is independent of `agent-core sync` and can be copied to another machine by itself.

See `docs/places.md` for setup, commands, file formats, refresh behavior, and platform boundaries.

## Workspace Integration

Agent Builder owns persistent workspace context. Ask to set up or refresh the agent, register a project, sync tasks/docs/KB, capture lessons, maintain scripts or a Python environment, or hand off/close out work. It loads the relevant reference for maintenance; ordinary discovery and compatible Python utilization need no maintenance skill. Human controls timing and scope; narrower permissions prevail. It uses one managed AGENT BUILDER block for newly configured workspaces, with confirmed locators and selective utilization cues. Existing resource locations, legacy owner blocks and custom instructions remain valid until explicitly migrated; sync does not modify workspace guidance, Git configuration, or resources. Preserve employer confidentiality and do not transfer work material to personal storage.

New resources default to .work-context/; existing paths and indexes remain stable. New tasks use creation month/workstream and double-hyphen dated filenames; the unfinished-work index and actual task retain next permitted actions and evidence. Recovery and optional Git persistence are explicit requests, not setup side effects. See [workspace configuration](docs/workspace-configuration.md).

## Knowledge Base

[Agent Builder](skills/agent-builder/SKILL.md) with its [KB reference](skills/agent-builder/references/knowledge-base.md) is the canonical workflow. Capture high-signal reusable records and explicitly requested human-facing artifacts, retrieve selectively, preserve provenance and originals, and honor confirmed backend scope. Legacy inbox requests use selected-source capture without cleanup; existing knowledge pages remain readable. No automatic migration or new synthesis layer.

The former Drive workflow is no longer authoritative. GitHub/web-app use requires explicit repository/ref/directory and suitable connector capabilities. See the [human operating manual](docs/agent-core-operating-manual.md#knowledge-base-workflow).

## Memory Pilot

- `memory/memories.jsonl` is the append-only canonical ledger.
- Search and index outputs are disposable and untracked.
- Memory tooling remains steward-only and is run through `uv run scripts/memory.py`.
- Global sync does not configure project memory. Agent Builder's KB workflow does not use or change this ledger.

## Dependency Strategy

- Agent Core runtime and installation require Python 3.10+ and use only the standard library.
- The standalone Places navigator supports Python 3.8+ and also uses only the standard library.
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
| Workspace contract | `docs/workspace-configuration.md` | Explicit resource map, setup, custom behavior, and owning skills. |
| Pi resource list | `personal-pi.toml` | Authoritative Pi agent and prompt allowlist. |
| Devin resource list | `personal-devin.toml` | Authoritative Devin custom-agent allowlist. |
| CLI launcher | `agent_core/bootstrap.py` | Fixed-checkout refresh and fresh-process handoff. |
| Sync engine | `agent_core/sync.py` | Pi-default and explicit Devin/OpenCode publication, ownership, rollback, and Pi legacy migration. |
| Legacy engine | `agent_core/apply.py` | Deprecated project-local compatibility. |
| Retirement engine | `agent_core/retire.py` | Safe removal of old managed project copies. |
| Places navigator | `docs/places.md` | Standalone directory discovery, menu, state, setup, and portability contract. |
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
