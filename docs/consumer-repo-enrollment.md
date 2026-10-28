# Personal Resource Distribution — Pi-First

**Last Updated:** 2026-10-28

**Status:** Current

**Source Of Truth:** Defines global personal resource publication, ownership safety, and legacy project-copy retirement.

**Update When:** The `agent-core sync` contract, personal manifest, ownership model, or migration behavior changes.

### Read First

- The normal workflow is machine-level `agent-core sync`, runnable from any directory.
- The fixed canonical checkout is `~/.agent-core`; sync attempts a fast-forward refresh, with a warned clean-local-commit fallback on failure. `--no-pull` skips the attempt.
- `personal-skills.toml`, `personal-pi.toml`, and `personal-devin.toml` are explicit allowlists; repository contents are never automatically enrolled.
- Default sync publishes only under `~/.pi/agent/`. `--harness devin` explicitly targets `%APPDATA%\devin\` on Windows; `--harness opencode` publishes shared skills under `~/.config/opencode/skills/`.
- Pi and Devin discover their native resources without additional discovery settings; OpenCode discovers skills at its native global path. OpenCode sync supports shared skills only; it does not publish OpenCode agents or commands.
- Global `AGENTS.md`, `CLAUDE.md`, Pi settings, and extension installations are user-managed and untouched.
- Declared resources in the selected harness are authoritative and replace differing installed content, even locally edited or previously unowned copies; unsafe file types are refused. Verified selected Pi legacy copies/aliases migrate with rollback; unselected resources remain untouched.
- Removing a manifest entry is additive and non-destructive by default; named one-time migrations may retire only unchanged fingerprint-owned predecessors.
- Human commands live in `docs/agent-core-operating-manual.md`.

## Scope

This document covers shared personal-skill publication to Pi, Devin, and OpenCode; harness-specific Pi and Devin agents; Pi prompt templates; the unmanaged global-guidance boundary; and explicit retirement of old project-local copies. OpenCode-specific agents and commands are not managed.

It does not cover production skill authoring, project-owned skills, user-authored global prompts, harness credentials, MCP configuration, security policy, the memory ledger, or active task state.

## Publication Layout

Canonical sources are selected only by the three committed manifests:

```text
personal-skills.toml            skills/<name>/SKILL.md
personal-pi.toml               pi/agents/<name>.md, pi/prompts/<name>.md
personal-devin.toml            devin/agents/<name>.md
```

The default target is Pi's native resource layout:

```text
~/.pi/agent/
├── skills/<name>/SKILL.md
├── agents/<name>.md
└── prompts/<name>.md
```

The explicit Windows Devin target is:

```text
%APPDATA%\devin\
├── skills\<name>\SKILL.md
└── agents\<name>.md
```

The explicit OpenCode target is shared skills only:

```text
~/.config/opencode/skills/<name>/SKILL.md
```

On Windows, the OpenCode path is under `%USERPROFILE%/.config/opencode/skills/`.

There is no leading dot in Devin's global Windows directory; `.devin/` is project-scoped. Native discovery requires no settings changes. OpenCode's shared skill directory is `~/.config/opencode/skills/`; OpenCode agents and commands are outside this publication contract. Pi extensions, Devin's experimental custom-subagent feature, model availability, credentials, and cloud Playbooks/plugins are outside sync's responsibility. Pi prompts are not translated because Devin has no file-based prompt-template equivalent; reusable cross-harness commands belong in explicitly invoked skills.

Migration reads existing version-2 through version-5 ownership state. For currently selected resources, sync compares the existing `~/.agents/` copy with its recorded fingerprint, publishes the canonical copy to Pi and retires the old copy. If a recorded Claude alias points to the selected old skill, that exact verified alias is also retired. Unselected, unowned, or ambiguous legacy paths remain untouched. Pre-existing native Pi files are adopted if identical; if their content differs, the declared canonical version replaces them. This is intentional: declaration grants sync authority over those exact destinations.

### Global Guidance

Sync no longer manages `~/.pi/agent/AGENTS.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`, or `~/.claude/CLAUDE.md`. Existing files remain unchanged, including local edits; absent files stay absent. Their contents and availability are now the user's responsibility.

The sync validates historical guidance ownership metadata and clears former records without ever inspecting the guidance files. It does not inspect the current prompt contents. `global/AGENTS.md` remains in the checkout but is not required or published by sync.

### Machine-Local Ownership

```text
~/.agent-core-state/ownership.json
```

This versioned JSON file is outside the tracked checkout. It records:

- each managed shared skill destination, source commit, and deterministic directory fingerprint;
- prior Claude alias metadata, used only to verify and safely retire selected legacy-owned links;
- an empty `guidance` collection plus selected Pi agent/template, Devin skill/agent, and OpenCode skill fingerprints in state version 6 (versions 2 through 5 migrate automatically).

The state retains records for names removed from the current manifest. Version 6 adds per-skill OpenCode destination records; versions 2 through 5 migrate automatically. It is published atomically only after all changed outputs succeed.

## Launcher Contract

The installed command shim invokes `~/.agent-core/agent_core/bootstrap.py` with the selected Python interpreter. For `agent-core sync`, the launcher:

1. confirms `~/.agent-core` is the canonical Git worktree root and contains required sources;
2. refuses staged, unstaged, or untracked checkout changes;
3. runs `git -C ~/.agent-core pull --ff-only` with ordinary Git authentication;
4. validates the refreshed checkout again;
5. starts `agent_core.sync` in a fresh Python process from the checkout.

For `sync`, a failed pull warns and continues from the existing local commit only after checking the checkout is still valid, clean, at the same HEAD, and free of unfinished Git operations/locks. The warning includes the Git failure and full local commit and explicitly says remote freshness is unverified. Dirty, changed-HEAD, or incomplete-operation failures remain fatal. Deprecated `apply` and `retire-local` retain fatal pull failures. The optional `agent-core sync --no-pull` skips step 3 only; both modes validate committed sources and cross the fresh-process boundary. The launcher and sync implementation use only Python 3.10+ standard-library APIs.

The Windows CMD installer locates `py -3` or `python`, creates `%LOCALAPPDATA%\AgentCore\bin\agent-core.cmd`, and updates the user PATH through `HKCU\Environment`. It does not invoke PowerShell, `setx`, `uv`, `pip`, elevation, or a package download.

## Source Contract

The manifests use narrow, dependency-free TOML string arrays: `skills = [...]` in `personal-skills.toml`, `agents = [...]` plus `prompts = [...]` in `personal-pi.toml`, and `agents = [...]` in `personal-devin.toml`. All names must be safe, distinct under case-folding within their resource category, and manually selected.

Before publication, Agent Core requires:

- the manifest to be tracked and match `HEAD`;
- every configured skill to be a real directory with `SKILL.md`, and every harness-specific source to be a regular Markdown file;
- every regular source file to be tracked;
- no missing tracked file, untracked file, symlink, reparse point, or unsupported entry in the source;
- source content and permissions to match committed content;
- a full canonical commit ID.

The launcher's clean-checkout check and the sync engine's committed-source checks are separate defenses.

Pi and Devin agent definitions intentionally remain separate. Pi uses `tools`, `advertise`, provider-qualified model IDs, and optional `thinking`; Devin custom agents use `allowed-tools`, Devin model aliases/IDs, and optional `max-nesting`. The current Devin `commit-agent` sets `model: codex`, so it does not inherit the parent model. Its associated skill does not override the model and therefore uses the custom-agent profile's selection.

## Destination And Transaction Contract

Before any mutation, sync validates the committed allowlists, canonical source files, ownership records, managed parents, and selected harness destinations. For every exact declared destination, the committed canonical resource wins: an identical target is reused, while differing content (owned or unowned) is replaced. Unsafe file types, symlinks, reparse points and unsafe parents are refused rather than traversed.

For selected resources with historical ownership under `~/.agents/`, the old copy must match the recorded fingerprint. Recorded Claude aliases are removed only when they can be verified as links to the selected old managed skill; altered aliases block the migration. Previous ownership versions are accepted and normalized before any file changes.

Resources are staged and fingerprinted, preflight is repeated, changed destinations are published using temporary transaction backups, and all installed outputs are fingerprint-verified. Pi additionally retires selected verified legacy paths. Only then is version-6 ownership atomically written. A failure restores the earlier files and any retired legacy resources. Removal from any manifest is non-destructive by default, and no unowned or unrelated directories are scanned. The `commit-with-subagent` prompt-to-skill migration retires only the exact old Pi prompt when its installed fingerprint still matches ownership state; a local edit blocks removal.

Selecting `manage-python-env` triggers the named Python consolidation: retire only fingerprint-matching owned `manage-python-agent-envs` and `manage-python-uv` directories in the selected harness, clearing their ownership only in the same rollback transaction. Pi also handles their verified `.agents` predecessors and registered Claude aliases; Devin and OpenCode never touch Pi/legacy resources. Missing owned predecessors can have stale records cleared. Unowned, modified, unsupported, or unsafe-parent predecessors block before publication with exact paths and remain untouched. Do not silently leave duplicate obsolete workflows or infer ownership from content alone. Both old and replacement names in the manifest are an error. Other removed names remain non-destructive.

Default sync publishes no resource files outside `~/.pi/agent/` except for removal of explicitly verified selected legacy-owned resources and aliases during these named migrations. Explicit Devin sync publishes only to `%APPDATA%\devin\skills\` and `%APPDATA%\devin\agents\`. Explicit OpenCode sync publishes only shared skills under `~/.config/opencode/skills/`. Ownership and transaction state remain in `~/.agent-core-state/`. Global guidance, harness settings, credentials, cloud Playbooks, and plugins remain untouched.

## Additive Manifest Changes

Adding a name publishes it at the next successful sync. Updating a committed source updates its unchanged owned copy. Manually deleting an owned copy recreates it.

Removing a name does not normally inspect, update, or delete its installed copy or ownership record. Re-adding a retained name makes its current native destination authoritative again, replacing local edits when necessary. A named one-time migration is allowed to retire only an exact fingerprint-owned predecessor, as with the old `commit-with-subagent` Pi prompt after its replacement skill became canonical.

Automatic pruning is intentionally absent. A future explicit prune operation would need its own human-visible contract.

## Observability

Successful sync prints the source commit, selected harness, exact selected resource names and counts, the verified native destination, and a brief migration/retirement count when applicable. It does not print transaction internals, aliases or ownership JSON locations during normal runs. Failures identify exact conflicts and do not claim partial success.

Verification means filesystem content matches the committed source, not that Pi, Devin, or OpenCode has loaded the files or that an agent obeyed them.

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
- The 76-test standard-library suite passed directly on Python 3.13.14 on 2026-10-13, including a Python 3.10 parser-compatibility check. The earlier suite also passed directly on Python 3.10.18 on 2026-10-08.
- Python 3.9 was rejected as the minimum because the existing implementation uses maintainable Python 3.10 typing syntax; supporting 3.9 would add conversion work without improving the target Windows setup. Python 3.11's `tomllib` dependency was removed through the narrow manifest parser, so 3.10 requires no package.
- Pi 1.0.4, Codex CLI 0.145.0, and Claude Code 2.1.285 paths were checked against installed documentation or discovery tools on 2026-10-08; Devin's Windows global skill/agent paths and custom-agent frontmatter were checked against current official documentation on 2026-10-13. OpenCode's native global skill path was rechecked against its official documentation on 2026-10-28. Runtime discovery and model compliance remain harness-level manual checks.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Personal skill list | `personal-skills.toml` | Authoritative shared skill publication set. |
| Pi resource list | `personal-pi.toml` | Authoritative Pi agent and prompt set. |
| Devin resource list | `personal-devin.toml` | Authoritative Devin custom-agent set. |
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
| 2026-10-11 | Default to Pi native resource locations. | Avoid extra discovery configuration, preserve opt-in manifests and safely migrate verified previous installations. |
| 2026-10-13 | Add an explicit Devin harness target while retaining Pi as default. | Devin Desktop/CLI can load global skills and model-pinned custom agents from `%APPDATA%\devin\`; its different frontmatter requires separate agent definitions. |
| 2026-10-28 | Add an explicit OpenCode target for shared skills only. | OpenCode's native skills path supports the existing shared-skill source; its agent and command formats are not included without dedicated canonical sources. |
| 2026-10-08 | Keep removal additive and provide exact legacy retirement separately. | Destructive cleanup must be explicit and fingerprint-proven. |
| 2026-10-08 | Set the minimum runtime to Python 3.10. | Removing `tomllib` is small and dependency-free; lowering further is unnecessary. |
