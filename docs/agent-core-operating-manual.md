# Agent Core Human Operating Manual

**Last Updated:** 2026-10-23

**Status:** Current

**Source Of Truth:** Defines the commands the owner follows to install, sync, publish, verify, migrate, and troubleshoot private Agent Core skills.

**Update When:** Machine setup, the normal sync command, skill publication targets, or recovery steps change.

## Use This Command Normally

```cmd
agent-core sync
```

Run it from any directory. It refreshes the fixed `~/.agent-core` checkout and publishes configured skills, subagents and prompt templates into Pi's native home. It does not publish global system guidance or change settings. Pi remains the default harness.

To publish shared skills and Devin-specific custom agents globally for Devin Desktop/CLI on Windows, run:

```cmd
agent-core sync --harness devin
```

Do not manually copy managed skills. Maintain global prompts yourself. Do not run the deprecated project-local `apply` command for normal personal use.

## New Windows Computer Setup

### Prerequisites

Use CMD to confirm Git and Python 3.10 or newer are available:

```cmd
git --version
py -3 --version
```

If the Python launcher is unavailable, `python --version` is sufficient. Configure ordinary private-repository Git authentication separately; Agent Core does not store credentials.

### Install Agent Core

```cmd
git clone <private-repo-url> "%USERPROFILE%\.agent-core"
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
```

The installer:

1. finds a supported interpreter through `py -3` or `python`;
2. creates `%LOCALAPPDATA%\AgentCore\bin\agent-core.cmd`;
3. adds that directory to the current user's PATH through the Windows user environment registry;
4. reports whether a new terminal is required.

It does not use PowerShell, `setx`, `uv`, `pip`, elevation, or downloaded Python packages.

If the installer changed PATH, close CMD and open a new one. Then run:

```cmd
agent-core sync
```

After setup, this is the normal update command, including when command-line Git cannot access the remote. A failed pull prints a warning and publishes the existing local commit only if the checkout remains valid, clean, unchanged, and free of unfinished Git operations. It explicitly reports that remote freshness is unverified. To skip the pull attempt entirely, optionally use:

```cmd
agent-core sync --no-pull
```

`--no-pull` skips only `git pull --ff-only`. It still requires the fixed checkout to be clean, validates committed source content, and publishes from its current checked-out commit. Sync reports that commit so the owner can verify what was installed.

## What Sync Installs

Default Pi sync installs:

```text
~/.pi/agent/
├── skills/<name>/SKILL.md
├── agents/<name>.md
└── prompts/<name>.md
```

Explicit Devin sync installs:

```text
%APPDATA%\devin\
├── skills\<name>\SKILL.md
└── agents\<name>.md
```

The global Windows Devin path has no leading dot. `.devin/` is a project-level directory.

Three allowlists select what is published:

- `personal-skills.toml`: shared skill directories from `skills/<name>/`.
- `personal-pi.toml`: Pi agent definitions from `pi/agents/<name>.md` and command templates from `pi/prompts/<name>.md`.
- `personal-devin.toml`: Devin custom-agent definitions from `devin/agents/<name>.md`.

Both harnesses discover their native locations automatically. Install `pi-subagents`, enable Devin subagents where required, and configure model credentials separately; sync never installs extensions, changes settings, or manages cloud Playbooks/plugins. Devin has no file-based prompt-template destination, so cross-harness reusable commands such as `commit-with-subagent` are installed as explicit-only skills.

The first sync upgrades older ownership records (versions 2 through 4). For **selected** resources, an unchanged previously managed `~/.agents/` copy is moved to Pi by the guarded transaction. A previously managed Claude skill alias pointing exactly to that old copy can also be retired. Pi-native declared skills, agents and templates are overwritten when they differ, regardless of previous ownership or local edits; identical content is adopted without rewriting. Legacy managed `.agents/` copies must still be unchanged to qualify for automatic removal. Unselected or unowned old resources are preserved.

### Global guidance

`AGENTS.md`, `CLAUDE.md`, other harness settings and Pi's `settings.json` are not managed or inspected.

### Ownership

Machine-local tracking is retained at `~/.agent-core-state/ownership.json`, outside the repository. It records exact per-harness managed destinations and fingerprints so migration and updates can be verified and rolled back.

## Verify The Result

Successful output is intentionally brief. For example:

```text
agent-core sync: OK (abcdef012345)
Harness: pi
Skills (13): project-tasks, project-docs, ..., commit-with-subagent
Agents (1): commit-agent
Prompts (0): none
Migrated legacy entries: 14
Verified: ~/.pi/agent/{skills,agents,prompts} (global guidance untouched)
```

The migration line appears only on a run with legacy entries. For cheap manual verification on Windows:

```cmd
dir "%USERPROFILE%\.pi\agent\skills"
dir "%USERPROFILE%\.pi\agent\agents"
dir "%USERPROFILE%\.pi\agent\prompts"
```

Start a new Pi session or use `/reload` to discover changed Pi resources. Restart or reload Devin Desktop as appropriate after Devin sync. File verification is not proof that either harness loaded or obeyed the instructions.

For Devin filesystem inspection:

```cmd
dir "%APPDATA%\devin\skills"
dir "%APPDATA%\devin\agents"
```

## Publish A Personal Skill

A skill is published only when it is committed under `skills/` and listed in `personal-skills.toml`.

### Add or update the source

```text
%USERPROFILE%\.agent-core\skills\<skill-name>\SKILL.md
```

Include valid Agent Skills frontmatter and any committed supporting files. Edit only the canonical source, never an installed copy.

### Maintain the authoritative list

Edit:

```text
%USERPROFILE%\.agent-core\personal-skills.toml
```

The file intentionally contains only one string array:

```toml
skills = [
    "project-tasks",
    "project-docs",
    "planning",
    "<skill-name>",
]
```

The list is manual. Not every repository skill is necessarily personal.

### Commit and publish

```cmd
cd /d "%USERPROFILE%\.agent-core"
git status --short
git add "skills\<skill-name>" personal-skills.toml
git commit -m "Publish <skill-name> as a personal skill"
git push origin main
agent-core sync
```

Agent Core refuses ignored, untracked, missing, linked, or uncommitted files inside configured sources.

Removing a name from any personal manifest normally stops future updates without deleting the installed copy or ownership record. Selecting `manage-python-env` is a named exception: it safely retires unchanged fingerprint-owned `manage-python-agent-envs` and `manage-python-uv` copies for the selected harness. Modified, unowned, or unsafe obsolete copies are preserved and reported as exact-path conflicts; resolve them explicitly rather than expecting sync to delete them. Pi additionally handles verified legacy copies and registered aliases. The `commit-with-subagent` prompt-to-skill migration is another narrow exception: Pi sync removes that old prompt only when it is still fingerprint-identical to the managed copy. This preserves local edits while avoiding duplicate commands. There is no default global force or prune command.

## Set Up Or Refresh A Workspace

1. Run `agent-core sync` (Pi) or `agent-core sync --harness devin`.
2. Reload/restart the agent so the updated skills are exposed.
3. Open your normal workspace root and invoke `workspace-setup`.
4. Resolve any ambiguous project/KB mappings, inspect the proposed section, and approve it.

The skill creates one managed block in root `AGENTS.md` and preserves its position on refresh. It lists project repositories, docs/tasks destinations, shared KB/archive, flat Python purpose projects, exposed/missing skills, and concise behavior. Its final response is exactly the saved block. Your custom Use for and Behavior wording survives refreshes. Add a repository or skill later? Request a targeted refresh; no per-session setup is needed.

To review a session for high-value behavioral lessons, explicitly invoke `agent-lessons`. It autonomously maintains only its marked `AGENTS.md` section and reports changed paths plus a brief summary; it may correctly make no changes.

The setup convention is `.work-context/{knowledge-base,archive/knowledge-base,projects,python}/`. The confirmed AGENTS.md locations are authoritative, not the convention itself. The old `projects.toml` workflow is retired and its files are left untouched. No setup action moves old `cf-workspace` content or configures backup without explicit approval. `manage-python-env` both maintains environments and runs Python workloads through them. See [workspace configuration](workspace-configuration.md).

## Knowledge Base Workflow

The canonical workflow is [`skills/knowledge-base/SKILL.md`](../skills/knowledge-base/SKILL.md), selected in `personal-skills.toml`. Publish source changes through the normal committed-source sync above; do not hand-copy installed files. A manifest edit alone does not install or reload a skill.

Use `sync to KB` to capture/update records, `clear my inbox` to capture and archive raw inputs, and `create/update a managed artifact` for human-facing Markdown outputs. The skill owns the detailed effects and retrieval rules. KB and archive roots must be explicitly selected or configured; there are no home-directory fallbacks. Workspace setup records `.work-context/knowledge-base/` and `.work-context/archive/knowledge-base/`. The archive is separate from the KB directory but may share its Git worktree; ordinary recall excludes it. Processing verifies retention before removing originals. Archival does not authorize committing or pushing raw sources.

The former Drive workflow is no longer canonical; existing KB content remains where it is until a separate migration is requested. GitHub-connected web apps need an explicitly selected repository/ref/directory and access to the canonical skill and its references. Connector access does not guarantee skill discovery, writes, or external archival. Updating Agent Core does not configure those integrations or replace user-managed global guidance that may still point to Drive.

## Maintain Global Guidance Separately

`agent-core sync` does not copy `global/AGENTS.md` or manage global system guidance files. Existing `CLAUDE.md` and `AGENTS.md` files remain untouched, and you own their contents. Edit the prompt for the harness you use, then restart its session to load the change. Changes to one harness's global file are not distributed to the others by Agent Core.

## Retire Old Project-Local Copies

The former workflow installed copies into each project's `.agents/skills/`. Migrate one exact directory at a time:

```cmd
cd /d "<old-target-directory>"
agent-core retire-local --here
```

The command reads prior ownership state and preflights every recorded destination. It removes only unchanged managed copies, the exact obsolete ownership state, and exact Agent Core entries in Git's local exclude file. It preserves unrelated `.agents` content and unrelated exclusion rules.

It refuses the whole operation if a managed copy was modified, is tracked by Git, or cannot be safely identified. It never scans other repositories. After retiring desired old targets, use only global `agent-core sync`.

`agent-core apply [--here]` remains temporarily available only for compatibility and prints a deprecation warning. It still targets project-local `.agents/skills/`; it is not an alias for global sync.

## Safety And Recovery

### Canonical checkout is dirty

```cmd
git -C "%USERPROFILE%\.agent-core" status --short
```

Commit and push intended canonical changes or resolve unwanted changes manually. Agent Core never stashes, resets, or cleans the checkout.

### Pull, authentication, or certificate validation fails

```cmd
git -C "%USERPROFILE%\.agent-core" pull --ff-only
```

Normal `agent-core sync --harness devin` already tolerates a failed refresh when the unchanged local checkout remains safe; inspect its warning and commit ID. Fix ordinary Git credentials, connectivity, or certificate trust when convenient; never disable SSL verification. GitHub Desktop can update the checkout separately. To explicitly avoid another network attempt:

```cmd
git -C "%USERPROFILE%\.agent-core" status --short
agent-core sync --no-pull
```

The status command must print nothing. Both modes refuse dirty/invalid checkouts or unfinished Git operations. If a failed pull changed HEAD, sync stops rather than guessing which implementation to publish. The warning fallback applies only to `sync`, not deprecated `apply` or `retire-local`.

### An installed harness resource differs from the canonical source

For any declared resource in the selected harness, sync installs the committed canonical version automatically, replacing differing native content without user-created backups. The transactional rollback area is temporary and exists only to recover from a failed sync. If an installed target is a symlink, a directory where a Markdown file belongs, or another unsupported object, sync refuses it instead of following or deleting it. Unselected resources stay untouched.

### Previously installed Claude alias

The Pi-first migration retires a Claude skill alias only if it is a previously recorded and verifiable link to a selected legacy-managed skill. Unowned, unrelated and unselected aliases remain untouched. If a recorded alias has changed or cannot be verified, resolve that exact conflict manually.

### Existing installation rejects `sync`

A launcher installed before this migration cannot update itself because it rejects the new subcommand before pulling. After these repository changes are committed and pushed, run this one-time migration in CMD:

```cmd
git -C "%USERPROFILE%\.agent-core" pull --ff-only
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
```

Open a new terminal if instructed, then run `agent-core sync`. Future syncs refresh themselves normally.

### Command is not found after installation

Open a new terminal. The installer reports the shim path, normally:

```text
%LOCALAPPDATA%\AgentCore\bin\agent-core.cmd
```

Run the installer again if the shim is missing. It updates the user PATH without `setx`.

### Ownership state is malformed or lost

Sync fails closed rather than adopting existing content. Keep installed files in place, inspect `%USERPROFILE%\.agent-core-state\ownership.json`, and restore a valid backup if available. If no trustworthy state exists, move the exact managed-looking destinations aside, remove the malformed state, and rerun sync so ownership can be established without overwriting unknown content.

## Quick Reference

```cmd
:: Normal update
agent-core sync

:: Publish a clean checkout already updated through GitHub Desktop
agent-core sync --no-pull

:: Publish global Devin Desktop/CLI resources
agent-core sync --harness devin

:: Verify Pi skills and ownership
dir "%USERPROFILE%\.pi\agent\skills"
type "%USERPROFILE%\.agent-core-state\ownership.json"

:: Verify Devin resources
dir "%APPDATA%\devin\skills"
dir "%APPDATA%\devin\agents"

:: Inspect canonical checkout problems
git -C "%USERPROFILE%\.agent-core" status --short

:: Retire one old project-local installation
cd /d "<old-target-directory>"
agent-core retire-local --here
```
