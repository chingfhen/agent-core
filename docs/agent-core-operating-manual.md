# Agent Core Human Operating Manual

**Last Updated:** 2026-09-15

**Status:** Current

**Source Of Truth:** Defines the commands the owner follows to install, apply, update, and troubleshoot private Agent Core skills.

**Update When:** Machine setup, the normal apply command, core-skill publication, or common recovery steps change.

## Use This Command Normally

Move to the exact directory that should receive `.agents/skills/`, then run:

```powershell
Set-Location "<target-directory>"
agent-core apply --here
```

Always use `--here` for normal personal use. It targets the current directory exactly and works whether or not that directory is a Git repository.

Do not manually copy core skills into targets. `agent-core apply --here` pulls the latest canonical checkout and safely creates or updates the configured copies.

## New Computer Setup

### Prerequisites

Confirm that Git and `uv` are installed and that normal private GitLab authentication works:

```powershell
git --version
uv --version
```

### Install Agent Core

Run once on the new computer:

```powershell
git clone https://gitlab.com/chingfhen/agent-core.git "$HOME\.agent-core"
uv tool install --editable "$HOME\.agent-core"
```

Confirm the command is available:

```powershell
agent-core apply --help
```

The help output should include `--here`.

If PowerShell cannot find `agent-core`, run:

```powershell
uv tool update-shell
```

Then close and reopen PowerShell.

## Apply Skills To A Directory

Example:

```powershell
Set-Location "C:\Users\TanChingFhen\Documents\ching\aws-codecommit-einstein-deepfake-detection-dev\gitlab-deepfake-detection-development"
agent-core apply --here
```

The result is:

```text
<current-directory>/.agents/skills/<core-skill>/
```

The command automatically:

1. checks that `~/.agent-core` is clean;
2. runs a fast-forward-only Git pull;
3. reads `core-skills.toml`;
4. validates all sources and destinations;
5. safely copies or updates each configured skill.

For `--here`, ownership metadata is stored at:

```text
<current-directory>/.agents/.agent-core/ownership.json
```

When the target is inside Git, Agent Core also refuses tracked skill targets and locally excludes managed private copies. Non-Git targets skip only those Git-specific checks.

### Verify The Result

```powershell
Get-ChildItem ".agents\skills"
Test-Path ".agents\skills\approval-gate\SKILL.md"
```

In a Git target, managed files should not appear in ordinary status output:

```powershell
git status --short
```

## Publish A New Core Skill

A skill must be committed to the private Agent Core repository and listed in `core-skills.toml` before other computers can receive it.

### 1. Create The Skill

Under the canonical checkout, create:

```text
$HOME/.agent-core/skills/<skill-name>/SKILL.md
```

The file needs valid skill frontmatter, including `name` and `description`.

### 2. Add It To The Core List

Edit:

```text
$HOME/.agent-core/core-skills.toml
```

Example:

```toml
skills = [
    "project-tasks",
    "project-docs",
    "planning",
    "engineering",
    "grilling",
    "approval-gate",
    "<new-skill-name>",
]
```

Adding a skill here means every later `agent-core apply --here` installs it in that command's target directory.

### 3. Commit And Push

```powershell
Set-Location "$HOME\.agent-core"
git status --short
git add "skills\<skill-name>\SKILL.md" core-skills.toml
git commit -m "Add <skill-name> to core skills"
git push origin main
```

Include any tracked helper files belonging to the skill in `git add`. Agent Core refuses ignored or otherwise uncommitted files inside configured source skills.

### 4. Apply It Where Needed

```powershell
Set-Location "<target-directory>"
agent-core apply --here
```

Repeat only in directories that should receive the update.

## Update An Existing Core Skill

Edit the canonical source, not a copied target:

```text
$HOME/.agent-core/skills/<skill-name>/
```

Then commit and push:

```powershell
Set-Location "$HOME\.agent-core"
git status --short
git add "skills\<skill-name>"
git commit -m "Update <skill-name>"
git push origin main
```

Apply the update in each desired target:

```powershell
Set-Location "<target-directory>"
agent-core apply --here
```

## Stop Distributing A Skill

Remove its name from `core-skills.toml`, then commit and push that configuration change.

This does **not** remove copies already present in target directories. It only stops future updates from treating that skill as currently configured.

If a retained copy is no longer wanted, delete that exact target directory manually:

```powershell
Remove-Item -Recurse -Force ".agents\skills\<skill-name>"
```

Do not delete the whole `.agents` directory when it may contain other skills or ownership state.

## Troubleshooting

### `unrecognized arguments: --here`

The installed launcher predates `--here` and rejects the option before it can update itself. Perform this one-time update:

```powershell
git -C "$HOME\.agent-core" pull --ff-only
agent-core apply --help
```

If `--here` still does not appear:

```powershell
uv tool install --editable "$HOME\.agent-core" --reinstall
```

Ordinary future applies update automatically; reinstalls are not normally needed.

### Canonical checkout is dirty

Inspect it:

```powershell
git -C "$HOME\.agent-core" status --short
```

Commit and push intentional canonical changes before applying. Resolve unwanted changes manually. Agent Core intentionally does not stash, reset, or clean them.

### A managed target was locally modified

Do not force an overwrite. If the target edits matter, copy them somewhere safe first. To discard the target edits and restore the canonical skill, delete only that skill directory and apply again:

```powershell
Remove-Item -Recurse -Force ".agents\skills\<skill-name>"
agent-core apply --here
```

### A target exists but is not owned by Agent Core

Inspect it before doing anything. If it is safe to replace, move or delete that exact skill directory manually, then rerun apply. Agent Core will not decide this destructively.

### A target is tracked by Git

Agent Core will not manage or overwrite it. Decide whether the repository-owned version or the private Agent Core copy should be authoritative before changing Git tracking.

### Pull or authentication failure

Confirm normal GitLab access:

```powershell
git -C "$HOME\.agent-core" pull --ff-only
```

Fix Git credentials, connectivity, or branch divergence outside Agent Core, then rerun apply.

## Deprecated Alias Workflow

Do not use `scripts/enroll_repo.py enroll` or `sync` for new targets. The symlink/junction workflow is deprecated and retained only to avoid breaking existing enrolled repositories.

`agent-core apply --here` does not inspect, migrate, or remove old `.claude/skills/`, `.opencode/skills/`, `.agent-os.json`, or enrollment registry state. Ask a steward to retire an existing enrollment safely if cleanup is needed.

## Quick Reference

```powershell
# Normal use
Set-Location "<target-directory>"
agent-core apply --here

# Verify
Get-ChildItem ".agents\skills"

# Inspect canonical checkout problems
git -C "$HOME\.agent-core" status --short

# Publish canonical changes
Set-Location "$HOME\.agent-core"
git status --short
git add <exact-paths>
git commit -m "Describe the Agent Core change"
git push origin main
```
