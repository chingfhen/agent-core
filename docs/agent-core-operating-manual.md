# Agent Core Human Operating Manual

**Last Updated:** 2026-10-08

**Status:** Current

**Source Of Truth:** Defines the commands the owner follows to install, sync, publish, verify, migrate, and troubleshoot private Agent Core skills and guidance.

**Update When:** Machine setup, the normal sync command, publication targets, or recovery steps change.

## Use This Command Normally

```cmd
agent-core sync
```

Run it from any directory. It refreshes the fixed `~/.agent-core` checkout and safely publishes the configured personal skills and global guidance for Pi, Codex, OpenCode, and Claude Code.

Do not manually copy managed skills or guidance. Do not run the deprecated project-local `apply` command for normal personal use.

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

After setup, this is the only normal update command.

## What Sync Installs

### Personal skills

Real managed copies are installed at:

```text
%USERPROFILE%\.agents\skills\<personal-skill>\
```

Pi, Codex, and OpenCode discover this portable Agent Skills location. Claude Code receives directory junctions at:

```text
%USERPROFILE%\.claude\skills\<personal-skill>
    -> %USERPROFILE%\.agents\skills\<personal-skill>
```

There is one installed content authority. **Skills are not copied into `%USERPROFILE%\.pi\agent\skills`.** Pi loads them from `%USERPROFILE%\.agents\skills`.

### Global guidance

The complete canonical `global/AGENTS.md` is published to:

```text
%USERPROFILE%\.pi\agent\AGENTS.md
%USERPROFILE%\.codex\AGENTS.md
%USERPROFILE%\.config\opencode\AGENTS.md
%USERPROFILE%\.claude\CLAUDE.md
```

Thus Pi's `.pi` directory receives the global `AGENTS.md`; the shared skills remain under `.agents`.

### Ownership

Machine-local state is stored outside the Git checkout:

```text
%USERPROFILE%\.agent-core-state\ownership.json
```

It records exact destinations, source commits, fingerprints, and alias targets. Do not edit it manually. On successful sync, the output reports the checkout commit, manifest count, changed skills, alias status, every guidance destination, and this ownership path.

## Verify The Result

In CMD:

```cmd
dir "%USERPROFILE%\.agents\skills"
dir "%USERPROFILE%\.claude\skills"
type "%USERPROFILE%\.pi\agent\AGENTS.md"
type "%USERPROFILE%\.agent-core-state\ownership.json"
```

For Pi, run `/reload` in an active session or start a new session. The skill command menu should expose configured names, and Pi should load `%USERPROFILE%\.pi\agent\AGENTS.md` as user guidance. Restart active Codex, OpenCode, and Claude Code sessions after changed resources.

OpenCode provides a cheap discovery check:

```cmd
opencode debug skill
```

A configured personal skill should appear once with a location under `%USERPROFILE%\.agents\skills`.

File existence and successful sync output prove publication, not model compliance. For consequential guidance changes, verify behavior in the relevant harness.

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

Removing a name from `personal-skills.toml` stops future updates but does not delete its existing copy, Claude alias, or ownership record. This additive behavior avoids surprise deletion. Resolve obsolete retained entries deliberately; there is no default global force or prune command.

## Update Global Guidance

Edit only:

```text
%USERPROFILE%\.agent-core\global\AGENTS.md
```

Commit and push it, then run `agent-core sync`. Sync updates all four owned destinations together. It refuses a non-empty unowned destination and refuses any managed guidance file changed after installation. An absent or empty unowned destination may be initialized.

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

### Pull or authentication fails

```cmd
git -C "%USERPROFILE%\.agent-core" pull --ff-only
```

Fix ordinary Git credentials, connectivity, or divergence outside Agent Core, then rerun sync.

### A managed global target was modified

The error names the exact path. Preserve any desired local edit elsewhere, then restore the recorded content or delete only that managed destination and rerun sync. A missing owned destination is safely recreated. There is no default force overwrite.

### An unowned target already exists

Inspect the exact conflict. If the existing content should remain authoritative, do not enroll that name or guidance path. If Agent Core should own it, move or remove that exact entry manually and rerun sync. Never delete an entire parent directory that may contain unrelated user content.

### A Claude alias is broken

If its shared managed skill was deleted, sync recreates the skill and alias. If the alias was redirected or replaced, sync refuses it as a local modification; inspect and resolve that exact alias manually.

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

:: Verify Pi guidance and shared skills
dir "%USERPROFILE%\.agents\skills"
type "%USERPROFILE%\.pi\agent\AGENTS.md"

:: Inspect canonical checkout problems
git -C "%USERPROFILE%\.agent-core" status --short

:: Retire one old project-local installation
cd /d "<old-target-directory>"
agent-core retire-local --here
```
