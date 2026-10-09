# Personal Skill Distribution

**Last Updated:** 2026-10-09

**Status:** Current

**Source Of Truth:** Defines global personal-skill publication, ownership safety, and legacy project-copy retirement.

**Update When:** The `agent-core sync` contract, personal manifest, ownership model, or migration behavior changes.

### Read First

- The normal workflow is machine-level `agent-core sync`, runnable from any directory.
- The fixed canonical checkout is `~/.agent-core`; every sync fast-forwards that clean checkout before touching installed targets.
- `personal-skills.toml` is the authoritative manual list. It is never inferred from all `skills/` directories.
- Real copies live under `~/.agents/skills/`. Claude Code receives aliases under `~/.claude/skills/` that resolve to those copies.
- Pi discovers the shared `~/.agents/skills/` entries; its global prompt is not part of skill sync.
- Global prompts are user-owned: sync does not read, create, overwrite, or delete them. The first skills-only sync releases old guidance ownership records without touching existing files.
- Sync refuses unowned collisions and locally modified managed skill targets, and preserves unrelated user and project content.
- Removing a manifest entry is additive and non-destructive.
- Human commands live in `docs/agent-core-operating-manual.md`.

## Scope

This document covers private personal-skill publication, the transition away from managed global guidance, and explicit retirement of former project-local copies.

It does not cover production skill authoring, project-owned skills, user-authored global prompts, harness credentials, MCP configuration, security policy, the memory ledger, or active task state.

## Publication Layout

### Skills

Configured sources:

```text
~/.agent-core/skills/<personal-skill>/
```

Shared installed authority:

```text
~/.agents/skills/<personal-skill>/
```

Claude compatibility alias:

```text
~/.claude/skills/<personal-skill>
    -> ~/.agents/skills/<personal-skill>
```

Windows uses unprivileged directory junctions. Other platforms use directory symlinks. Agent Core never silently creates a second Claude content copy.

Pi, Codex, and OpenCode use the shared Agent Skills location directly. Pi 1.0.4 was checked through RPC `get_commands` in an isolated Windows home; it returned a synthetic `~/.agents/skills/` skill once with user scope. OpenCode 1.18.11 was checked with both the shared skill and Claude junction present; `opencode debug skill` returned the test skill once at its shared location. Pi's discovery documentation does not identify `~/.claude/skills/` as a Pi location.

### Global Guidance

Sync no longer manages `~/.pi/agent/AGENTS.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`, or `~/.claude/CLAUDE.md`. Existing files remain unchanged, including local edits; absent files stay absent. Their contents and availability are now the user's responsibility.

The first successful skills-only sync validates old guidance ownership records, then clears those records in the atomically published ownership state. It does not inspect the current prompt contents. `global/AGENTS.md` remains in the checkout but is not required or published by sync.

### Machine-Local Ownership

```text
~/.agent-core-state/ownership.json
```

This versioned JSON file is outside the tracked checkout. It records:

- each managed shared skill destination, source commit, and deterministic directory fingerprint;
- each Claude alias destination and expected shared target;
- an empty `guidance` collection retained for state-version compatibility after the first skills-only sync.

The state retains records for names removed from the current manifest. It is published atomically only after all changed outputs succeed.

## Launcher Contract

The installed command shim invokes `~/.agent-core/agent_core/bootstrap.py` with the selected Python interpreter. For `agent-core sync`, the launcher:

1. confirms `~/.agent-core` is the canonical Git worktree root and contains required sources;
2. refuses staged, unstaged, or untracked checkout changes;
3. runs `git -C ~/.agent-core pull --ff-only` with ordinary Git authentication;
4. validates the refreshed checkout again;
5. starts `agent_core.sync` in a fresh Python process from the checkout.

Pull, authentication, network, certificate, or divergence failures stop before installed files change. The explicit `agent-core sync --no-pull` variant skips step 3 only. It still requires a clean fixed checkout, validates committed sources, crosses the same fresh-process boundary, and reports the exact current commit. It is intended for a checkout already updated through another trusted Git client such as GitHub Desktop; ordinary sync never silently falls back to it. The launcher and sync implementation use only Python 3.10+ standard-library APIs.

The Windows CMD installer locates `py -3` or `python`, creates `%LOCALAPPDATA%\AgentCore\bin\agent-core.cmd`, and updates the user PATH through `HKCU\Environment`. It does not invoke PowerShell, `setx`, `uv`, `pip`, elevation, or a package download.

## Source Contract

`personal-skills.toml` accepts a deliberately narrow dependency-free TOML subset: one top-level `skills = [...]` array of quoted strings. Names must be unique under case-folding and safe as one directory component.

Before publication, Agent Core requires:

- the manifest to be tracked and match `HEAD`;
- every configured source to be a real directory with a regular `SKILL.md`;
- every regular source file to be tracked;
- no missing tracked file, untracked file, symlink, reparse point, or unsupported entry in the source;
- source content and permissions to match committed content;
- a full canonical commit ID.

The launcher's clean-checkout check and the sync engine's committed-source checks are separate defenses.

## Destination And Transaction Contract

Before any replacement, sync validates every configured skill, Claude alias, managed parent path, and ownership record. Former guidance records are validated as historical state, but the associated files are not checked.

A configured shared skill is safe only when it is:

- absent and unowned;
- owned and fingerprint-unchanged;
- owned but missing.

A Claude alias is safe only when it is:

- absent and unowned;
- owned and resolves to its exact shared skill;
- owned but missing;
- an owned broken alias whose exact managed shared target is also missing and will be recreated.

All other entries are conflicts. There is no default force option.

After preflight, sync:

1. stages and fingerprints every configured skill copy;
2. repeats state and target safety checks immediately before replacement;
3. moves changed existing skill targets to transaction backups;
4. publishes changed skills;
5. creates or recreates Claude aliases and verifies their identity;
6. atomically writes prospective ownership state with guidance ownership cleared;
7. removes transaction artifacts.

Any ordinary failure before ownership publication rolls back changed skills and aliases. If rollback itself is incomplete, the error lists exact affected paths.

Managed parent directories may be created when absent but must otherwise be real directories, not links or unsupported entries. Unrelated entries under `.agents` and `.claude` are preserved; global guidance locations are never inspected or changed.

## Additive Manifest Changes

Adding a name publishes it at the next successful sync. Updating a committed source updates its unchanged owned copy. Manually deleting an owned copy recreates it.

Removing a name does not inspect, update, or delete its prior shared copy, alias, or ownership record. Re-adding an unchanged retained name resumes normal updates; a locally modified retained copy is a conflict when re-added.

Automatic pruning is intentionally absent. A future explicit prune operation would need its own human-visible contract.

## Observability

Successful sync output reports:

- canonical checkout and commit;
- selected manifest and configured count;
- shared destination with added, updated, recreated, and unchanged counts;
- changed skill names;
- Claude alias destination, count, and statuses;
- confirmation that global guidance is not managed;
- ownership-state location;
- the need to reload or restart active harness sessions.

A refusal identifies exact conflicting destinations and why they are unsafe. Output proves completed filesystem operations, not that a model followed the installed instructions.

## Legacy Project-Local Compatibility

`agent-core apply [--here]` remains deprecated during migration. It still copies the current personal manifest into a project-local `.agents/skills/` and preserves the former version-1 ownership and Git local-exclusion behavior. It prints a deprecation warning and is never silently redirected to global targets.

Use this explicit migration command in each old target:

```text
agent-core retire-local --here
```

Retirement:

1. selects only the exact current directory, with a narrow fallback for prior plain-apply state when that directory is the Git worktree root;
2. reads version-1 Agent Core ownership records;
3. preflights every record before mutation;
4. refuses tracked, locally modified, malformed, or unsupported managed targets;
5. moves only fingerprint-matching managed copies through a rollback area;
6. removes only the exact obsolete ownership file and exact matching entries in Agent Core's Git local-exclusion block;
7. preserves unrelated `.agents` content and unrelated exclusion rules;
8. never scans other repositories.

Missing managed copies do not block exact metadata cleanup. Any unsafe remaining copy blocks the whole retirement rather than producing a partial guess.

## Compatibility Evidence

- Runtime syntax is constrained to Python 3.10 and the suite includes a Python 3.10 parser check.
- The 22-test standard-library suite passed directly on Python 3.13.14 and Python 3.10.18 on 2026-10-08.
- Python 3.9 was rejected as the minimum because the existing implementation uses maintainable Python 3.10 typing syntax; supporting 3.9 would add conversion work without improving the target Windows setup. Python 3.11's `tomllib` dependency was removed through the narrow manifest parser, so 3.10 requires no package.
- Pi 1.0.4, Codex CLI 0.145.0, OpenCode 1.18.11, and Claude Code 2.1.285 paths were checked against installed documentation or discovery tools on 2026-10-08. Runtime model compliance remains a harness-level manual check.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Personal list | `personal-skills.toml` | Authoritative publication set. |
| Stable launcher | `agent_core/bootstrap.py` | Refresh and fresh-process handoff. |
| Sync implementation | `agent_core/sync.py` | Global ownership, copying, aliases, and rollback. |
| Legacy apply | `agent_core/apply.py` | Deprecated project-local compatibility. |
| Legacy retirement | `agent_core/retire.py` | Exact safe migration cleanup. |
| Windows installer | `scripts/install-agent-core.cmd` | CMD-first setup entry point. |
| Installer helper | `scripts/install_agent_core.py` | Shim creation and safe user-PATH update. |
| Human manual | `docs/agent-core-operating-manual.md` | Owner-facing commands and recovery. |
| Repository architecture | `README.md` | Canonical and installed boundaries. |
| Steward contract | `AGENTS.md` | Stable maintenance and safety rules. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-10-08 | Replace normal per-project apply with machine-level global sync. | Personal workflows should remain current across projects without duplicate managed copies. |
| 2026-10-08 | Keep one real installed copy under `~/.agents/skills/` and alias it for Claude. | This serves the portable harnesses and Claude without independent content authorities. |
| 2026-10-08 | Store ownership under `~/.agent-core-state/`. | Runtime state must not dirty the canonical checkout. |
| 2026-10-08 | Initialize only absent or empty unowned guidance destinations (superseded). | Complete-file publication avoided overwriting personal content while guidance was managed. |
| 2026-10-09 | Stop publishing global guidance and release its ownership on the next sync. | Global prompt files remain untouched and can be maintained independently of personal skills. |
| 2026-10-08 | Keep removal additive and provide exact legacy retirement separately. | Destructive cleanup must be explicit and fingerprint-proven. |
| 2026-10-08 | Set the minimum runtime to Python 3.10. | Removing `tomllib` is small and dependency-free; lowering further is unnecessary. |
