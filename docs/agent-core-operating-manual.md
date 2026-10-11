# Agent Core Human Operating Manual

**Last Updated:** 2026-10-11

**Status:** Current

**Source Of Truth:** Defines the commands the owner follows to install, sync, publish, verify, migrate, and troubleshoot private Agent Core skills.

**Update When:** Machine setup, the normal sync command, skill publication targets, or recovery steps change.

## Use This Command Normally

```cmd
agent-core sync
```

Run it from any directory. It refreshes the fixed `~/.agent-core` checkout and publishes configured skills, subagents and prompt templates into Pi's native home only. It does not publish global system guidance or change settings.

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

After setup, this is the normal update command. If command-line Git cannot access the remote but the checkout was already updated through GitHub Desktop, use the explicit offline-refresh variant:

```cmd
agent-core sync --no-pull
```

`--no-pull` skips only `git pull --ff-only`. It still requires the fixed checkout to be clean, validates committed source content, and publishes from its current checked-out commit. Sync reports that commit so the owner can verify what was installed.

## What Sync Installs

```text
~/.pi/agent/
├── skills/<name>/SKILL.md
├── agents/<name>.md
└── prompts/<name>.md
```

Two allowlists select what is published:

- `personal-skills.toml`: skill directories from `skills/<name>/`.
- `personal-pi.toml`: agent definitions from `pi/agents/<name>.md` and command templates from `pi/prompts/<name>.md`.

Pi discovers all three native locations automatically. No extra `settings.json` entries or manual copies are required. Install `pi-subagents` and set up any specialized model credentials separately; sync never installs extensions or edits settings.

The first sync upgrades older ownership records (version 2 or 3). For **selected** resources, an unchanged previously managed `~/.agents/` copy is moved to Pi by the guarded transaction. A previously managed Claude skill alias pointing exactly to that old copy can also be retired. Locally modified managed files or conflicting files already in Pi's native folders cause the entire sync to refuse instead of replacing anyone's work. Identical native files can be adopted safely. Unselected or unowned old resources are preserved.

### Global guidance

`AGENTS.md`, `CLAUDE.md`, other harness settings and Pi's `settings.json` are not managed or inspected.

### Ownership

Machine-local tracking is retained at `~/.agent-core-state/ownership.json`, outside the repository. It records exact managed destinations and fingerprints so migration and updates can be verified and rolled back.

## Verify The Result

Successful output is intentionally brief. For example:

```text
agent-core sync: OK (abcdef012345)
Skills (12): project-tasks, project-docs, ...
Agents (1): commit-agent
Prompts (1): commit-with-subagent
Migrated legacy entries: 14
Verified: ~/.pi/agent/{skills,agents,prompts} (global guidance untouched)
```

The migration line appears only on a run with legacy entries. For cheap manual verification on Windows:

```cmd
dir "%USERPROFILE%\.pi\agent\skills"
dir "%USERPROFILE%\.pi\agent\agents"
dir "%USERPROFILE%\.pi\agent\prompts"
```

Start a new Pi session or use `/reload` to discover changed resources. File verification is not proof that Pi or an underlying model obeyed the instructions.

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

Removing a name from either personal manifest stops future updates but does not delete previously installed managed copies or their ownership records. This additive behavior avoids surprise deletion. Resolve obsolete retained entries deliberately; there is no default global force or prune command.

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

Prefer fixing ordinary Git credentials, connectivity, or certificate trust. Do not disable SSL verification. If GitHub Desktop can safely update the canonical checkout while command-line Git cannot access the remote, pull that checkout in GitHub Desktop, confirm it is clean, then publish its current commit without another network operation:

```cmd
git -C "%USERPROFILE%\.agent-core" status --short
agent-core sync --no-pull
```

The status command must print nothing. `--no-pull` is explicit and never silently falls back when an ordinary sync pull fails.

### An unowned target already exists

Inspect the exact conflicting Pi-native skill, agent or prompt. If the local file must remain authoritative, keep it; otherwise compare it against the canonical source and deliberately move or rename only that file before rerunning sync. Never delete whole parent directories.

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

:: Verify Pi skills and ownership
dir "%USERPROFILE%\.pi\agent\skills"
type "%USERPROFILE%\.agent-core-state\ownership.json"

:: Inspect canonical checkout problems
git -C "%USERPROFILE%\.agent-core" status --short

:: Retire one old project-local installation
cd /d "<old-target-directory>"
agent-core retire-local --here
```
