# Consumer Repo Skill Distribution

**Last Updated:** 2026-09-15

**Status:** Current

**Source Of Truth:** Defines the simple copy-based skill workflow and the separate advanced alias enrollment workflow for consumer repos.

**Update When:** The `agent-core apply` contract, core skill configuration, ownership model, or advanced enrollment behavior changes.

### Read First

- The normal personal workflow is `agent-core apply --here`, which targets the current directory whether or not it is a Git worktree. Plain `agent-core apply` targets the containing Git root.
- The canonical private checkout is fixed at `~/.agent-core`; every apply fast-forwards that clean checkout before touching project skill targets.
- `core-skills.toml` is the authoritative core list. Apply copies only those skills to `.agents/skills/<skill>`.
- Copied directories update explicitly on the next apply. They are not links and do not propagate edits live.
- Apply refuses tracked targets, unrelated existing targets, and managed copies whose installed fingerprint changed.
- Removing a skill from `core-skills.toml` is additive: its copy, ownership record, and local exclusion remain untouched.
- `scripts/enroll_repo.py` remains available as separate advanced tooling for manifests and live Claude/OpenCode aliases. Apply does not inspect or migrate that workflow.

### Scope

This document covers private skill delivery into Git and non-Git target directories, including copy ownership, conflict safety, local Git exclusions when available, and the optional advanced alias workflow.

### Not Here

- Canonical skill authoring in `skills/`
- Memory ledger internals
- Active rollout or implementation task state

## Simple Personal Workflow

### One-Time Machine Setup

```powershell
git clone <private-gitlab-url> "$HOME\.agent-core"
uv tool install --editable "$HOME\.agent-core"
```

The checkout location is intentionally not configurable. Authentication comes from the user's ordinary Git and GitLab configuration; Agent Core does not store or rewrite credentials.

### Everyday Use

To target the current directory exactly:

```text
agent-core apply --here
```

This works in Git and non-Git directories. Plain `agent-core apply` remains available inside a Git worktree and targets the worktree root.

The launcher:

1. resolves the exact current directory for `--here`, or requires and resolves a Git worktree for plain apply;
2. confirms `~/.agent-core` is the canonical Git worktree root and contains the package, `skills/`, and `core-skills.toml`;
3. refuses staged, unstaged, or untracked canonical-checkout changes;
4. runs `git -C ~/.agent-core pull --ff-only`;
5. launches the newly pulled apply implementation in a fresh Python process.

Pull, authentication, network, or divergence failures stop before project files are changed. The launcher and apply implementation are standard-library-only, so ordinary source updates do not require dependency reinstalls.

### Core Skill Configuration

`core-skills.toml` is manually maintained and authoritative. The current list is:

- `project-tasks`
- `project-docs`
- `planning`
- `engineering`
- `grilling`
- `approval-gate`

Apply validates the complete list and every source before replacing any configured target. Names must be unique safe directory names, each real source directory must contain a regular `SKILL.md`, and every copied source file must be tracked in the canonical Git commit. Ignored or otherwise uncommitted source files, links, reparse points, and other unsupported entries are rejected rather than copied.

### Destination And Ownership

Each configured source is copied to:

```text
<target-root>/.agents/skills/<skill>
```

No other project skill surface participates in this workflow.

Ownership state is versioned JSON. Plain apply stores it at:

```text
<actual-git-dir>/agent-core/ownership.json
```

`--here` stores it under the exact target:

```text
<current-directory>/.agents/.agent-core/ownership.json
```

This target-local location remains stable if a non-Git directory later becomes a Git repository. Plain apply resolves the actual Git directory, so linked worktrees receive their own ownership state. Each record includes the destination, source skill, canonical source commit, and a deterministic fingerprint of installed paths, permissions, and file contents.

For every configured target, apply fails closed unless it is one of:

- absent;
- recorded as owned and unchanged;
- recorded as owned but manually deleted.

When Git metadata is available, a tracked target or tracked descendant is always a conflict. Existing unowned content and locally modified managed copies are never overwritten. There is no `--force` option. Non-Git `--here` targets skip only tracked-path and Git-exclusion behavior.

Removing a name from `core-skills.toml` does not inspect, update, or delete its prior copy or ownership record. If it is re-added unchanged, it can update normally. If it was modified while absent from configuration, re-adding it exposes the conflict.

### Transaction And Local Git Protection

After full source validation and all-target preflight, apply stages and fingerprints every copy on the project filesystem. It replaces safe targets through temporary backups, rolls replacements back on ordinary failure, and atomically writes ownership state only after successful replacement.

When Git is available, exact managed destinations and target-local `--here` ownership state are maintained in a tool-owned block in:

```text
<git-common-dir>/info/exclude
```

Unrelated exclusion content is preserved, and the tracked project `.gitignore` is not modified. Non-Git targets have no Git exclusion file to update. Retained records keep removed core skills excluded; stale exclusions after manual deletion are harmless.

### Legacy Independence

`agent-core apply` does not read, write, detect, or migrate:

- `.agent-os.json`;
- `.agent-os-state/` registries;
- `.claude/skills/`;
- `.opencode/skills/`;
- enrollment symlinks or junctions.

Those surfaces matter only if they independently occupy an exact `.agents/skills/<configured-skill>` target.

## Advanced Alias Enrollment

`scripts/enroll_repo.py` remains operational for cases that deliberately need `.agent-os.json`, device-local enrollment records, memory enablement, or live aliases under both `.claude/skills/*` and `.opencode/skills/*`.

- Run it with `uv run scripts/enroll_repo.py`.
- Enrollment and sync preflight exact targets as missing, managed aliases, or conflicts.
- On Windows, automatic link mode tries a directory symlink and falls back to a junction.
- Real local skill directories, broken aliases, and aliases to unexpected sources are conflicts.
- `verify` checks the live-alias guarantee.
- `unenroll` is preview-first and removes only registry-recorded aliases that still resolve to expected canonical sources.
- Advanced generated surfaces remain locally ignored according to that workflow's existing rules.

Never recursively delete or replace a live alias or its harness parent directory; editing through a live alias can modify canonical skill source. Use verified unenrollment or stop on uncertainty.

### Memory Boundary

The advanced `.agent-os.json` workflow remains the only workflow that carries `memory_enabled` and other manifest fields. Executor skills needing that context read the manifest directly. The simple copy workflow neither creates a manifest nor enables memory implicitly.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Core list | `core-skills.toml` | Authoritative copied skill set. |
| Stable launcher | `agent_core/bootstrap.py` | Validates and refreshes the fixed checkout before fresh-process handoff. |
| Apply implementation | `agent_core/apply.py` | Implements validation, ownership, copying, rollback, and local exclusions. |
| Package contract | `pyproject.toml` | Defines the editable `agent-core` console command. |
| Advanced enrollment | `scripts/enroll_repo.py` | Optional manifest and live-alias workflow. |
| Manifest schema | `schemas/agent-os-manifest.schema.json` | Defines advanced workflow manifest v1. |
| Repo architecture | `README.md` | High-level orientation and canonical/generated boundaries. |
| Steward contract | `AGENTS.md` | Stable maintenance and safety rules. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-09-15 | Make `agent-core apply` the simple personal workflow, using copied `.agents/skills/*` directories and local ownership fingerprints. | Explicit per-project refresh is simpler across devices than live links, multiple harness destinations, and a global enrollment registry. |
| 2026-09-15 | Keep advanced alias enrollment separate and migration-free. | Existing manifest, memory, and live-link use cases remain valid without coupling the simple workflow to legacy state. |
| 2026-07-18 | Advanced enroll and sync fail on real local skill directories; unenroll removes only verified aliases. | Live aliases can resolve into canonical source, so automatic recursive replacement or cleanup is unsafe. |
| 2026-06-19 | Advanced Windows enrollment prefers symlinks with junction fallback. | A non-destructive fallback supports devices without symlink privileges. |
