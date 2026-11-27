# Agent Core Human Operating Manual

**Last Updated:** 2026-11-02

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

To publish shared skills to OpenCode's native global skills directory:

```cmd
agent-core sync --harness opencode
```

OpenCode sync publishes shared skills only; OpenCode agents, commands, global guidance, and settings remain unmanaged.

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

The global Windows Devin path has no leading dot. `.devin/` is a project-level directory. OpenCode skills use `~/.config/opencode/skills/<name>/SKILL.md`; on Windows, the root is `%USERPROFILE%/.config/opencode/skills/`.

Three allowlists select what is published:

- `personal-skills.toml`: shared skill directories from `skills/<name>/`.
- `personal-pi.toml`: Pi agent definitions from `pi/agents/<name>.md` and command templates from `pi/prompts/<name>.md`.
- `personal-devin.toml`: Devin custom-agent definitions from `devin/agents/<name>.md`.

OpenCode uses the shared-skill allowlist only; this repository has no OpenCode-specific agent or command manifest.

Pi and Devin discover their native locations automatically, as does OpenCode for skills. Install `pi-subagents`, enable Devin subagents where required, and configure model credentials separately; sync never installs extensions, changes settings, or manages cloud Playbooks/plugins. Devin has no file-based prompt-template destination, so cross-harness reusable commands such as `commit-changes` are installed as skills. They are model-callable; committing still requires an explicit human request.

The first sync upgrades older ownership records (versions 2 through 5). For **selected** resources, an unchanged previously managed `~/.agents/` copy is moved to Pi by the guarded transaction. A previously managed Claude skill alias pointing exactly to that old copy can also be retired. Pi-native declared skills, agents and templates are overwritten when they differ, regardless of previous ownership or local edits; identical content is adopted without rewriting. Legacy managed `.agents/` copies must still be unchanged to qualify for automatic removal. Unselected or unowned old resources are preserved.

### Global guidance

`AGENTS.md`, `CLAUDE.md`, OpenCode's `~/.config/opencode/AGENTS.md`, other harness settings and Pi's `settings.json` are not managed or inspected.

### Ownership

Machine-local tracking is retained at `~/.agent-core-state/ownership.json`, outside the repository. It records exact per-harness managed destinations and fingerprints so migration and updates can be verified and rolled back.

## Verify The Result

Successful output is intentionally brief. For example:

```text
agent-core sync: OK (abcdef012345)
Harness: pi
Skills (...): agent-builder, ..., commit-changes
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

Start a new Pi session or use `/reload` to discover changed Pi resources. Restart or reload Devin Desktop as appropriate after Devin sync. OpenCode V2 supports live resource reload and `/reload`; verify its exposed skills. File verification is not proof that Pi, Devin, or OpenCode loaded the files or obeyed the instructions.

For Devin filesystem inspection:

```cmd
dir "%APPDATA%\devin\skills"
dir "%APPDATA%\devin\agents"
```

For OpenCode skill inspection:

```cmd
dir "%USERPROFILE%\.config\opencode\skills"
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
    "agent-builder",
    "tech-design-options",
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

Removing a name from any personal manifest normally stops future updates without deleting its installed copy or record. Selecting `agent-builder` triggers the named Agent Builder consolidation: for the selected harness only, retire exact unchanged fingerprint-owned predecessors (the seven original workflows and the known historical names `project-tasks`, `project-docs`, `knowledge-base`, `agent-lessons`, `manage-python-env`, `manage-python-agent-envs`, `manage-python-uv`). Modified, unowned, or unsafe copies block with exact paths before publication; do not delete them automatically. Pi additionally handles its verified legacy `.agents/` copies and registered Claude aliases. Retirement and publication share the existing rollback transaction; unrelated skills and other harnesses are untouched. The prior named Python-only migration remains supported when `run-and-manage-python` alone is selected. Ordinary manifest removal still does not prune. The existing Pi prompt-to-skill migration remains supported. No global force/prune command.

## Set Up Or Refresh A Workspace

1. Run `agent-core sync` (Pi), `agent-core sync --harness devin`, or `agent-core sync --harness opencode`, matching your actual harness. Confirm the printed commit and selected skills; restart the session.
2. Open the normal workspace root and ask Agent Builder to inspect existing routing, read applicable guidance and confirm the current resources. Existing legacy blocks and paths stay authoritative. For an established workspace, say "Assess migration to Agent Builder and recommend only useful changes." The agent reads [migration.md](../skills/agent-builder/references/migration.md), proposes a concise scope and obtains approval before migration. Prioritize broken live cues and missing Python utilization guidance; full block consolidation and extraction of behaviors/lessons are optional. Approved partial adoption is valid; retain usable legacy routes without competing authority.
3. Verify only affected capabilities and guidance after approved repairs. Try ordinary context discovery, a narrow maintenance cue or a fresh-session handoff as relevant; confirm the correct interpreter before Python execution. Distinguish static checks from actual behavior, and resume normal work without requiring a complete migration. Report real issues rather than treating skill installation as proof of compliance.

Agent Builder owns persistent workspace context. Ask to set up or refresh the agent, register a project, sync tasks/docs/KB, capture lessons, maintain scripts or a Python environment, or hand off/close out work. It loads the relevant reference for maintenance; ordinary discovery and compatible Python utilization need no maintenance skill. Human controls timing and scope; narrower permissions prevail. It uses one managed AGENT BUILDER block for newly configured workspaces, with confirmed locators and selective utilization cues. Existing resource locations, legacy owner blocks and custom instructions remain valid until explicitly migrated; sync does not modify workspace guidance, Git configuration, or resources. Preserve employer confidentiality and do not transfer work material to personal storage.

If sync reports a modified/unowned obsolete copy, stop and review the exact path; preserve custom work and decide manually how to resolve the conflict. Do not force-delete or hand-copy managed skills. For rollback, restore the previous approved canonical manifest/source revision in the canonical checkout through an authorized Git operation and sync the selected harness. Ordinary removal of agent-builder does not uninstall it: after restoring originals, explicitly resolve that exact installed copy with ownership verification, without pruning unrelated skills. Transaction rollback on publication failure is automatic; rollback of a successful adoption is separate.

### Everyday Agent Builder cues

Use the [canonical capability nouns](../skills/agent-builder/SKILL.md#activation-and-routing) to address or combine resources. Normal maintenance is the default; explicitly say "quick sync" for a faster, current-context-focused pass. Quick preserves essential checks and permissions.

| Say | Result |
| --- | --- |
| `/agent-builder sync` | Normal maintenance of relevant core resources. |
| `/agent-builder quick sync tasks, docs and KB` | Fast pass with those named capabilities primary. |
| `/agent-builder update my todo` | Refresh the optional Human / Agent / Waiting Markdown action list. |
| `/agent-builder give me the next prompt` | Copy-ready continuation prompt, without implicit persistence. |
| `/agent-builder sync and give me the next prompt` | Maintain context first, then produce the prompt. |

Todo and Next prompt are opt-in, not automatic during general sync. They can be combined with other explicit requests. No separate tool or installation is needed.

### Hand Work to the Next Session or Close It Out

Say "hand this off to a fresh session" or "close this task". Agent Builder reads tasks.md and only other justified references, saves verified supporting material before updating the task/index, preserves unfinished obligations and reports actual next permitted action. "Task only" narrows scope. No worker launch or execution permission is implied. New paths use YYYY-MM/workstream/YYYY-MM-DD--description.md and index.md; established filenames and uppercase INDEX.md stay intact.

## Knowledge Base Workflow

Use [Agent Builder](../skills/agent-builder/SKILL.md) and its [KB reference](../skills/agent-builder/references/knowledge-base.md). "Sync to KB" captures reusable records; "capture these files" selects originals without moving them; legacy inbox cues explain the changed workflow without deleting inputs. Managed artifacts require explicit intent. Ask to "retire/deprecate these artifacts" to move approved files into searchable retired/ without losing their contents, or "restore this artifact" to return it to managed/. Retired artifacts stay available for recall but out of the active human list; discard is separate. Existing KB roots, archives, records and legacy knowledge pages remain in place. Ordinary recall is read-only and can occur without loading the maintenance skill. No new synthesis layer, automatic cleanup, remote transfer or backend substitution.

The former Drive workflow is not canonical. Remote use requires confirmed repository/ref/directory and scoped access. Publication does not configure connectors or migrate existing resources.

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

Normal `agent-core sync` for Pi, Devin, and OpenCode already tolerates a failed refresh when the unchanged local checkout remains safe; inspect its warning and commit ID. Fix ordinary Git credentials, connectivity, or certificate trust when convenient; never disable SSL verification. GitHub Desktop can update the checkout separately. To explicitly avoid another network attempt:

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

:: Publish shared skills to OpenCode
agent-core sync --harness opencode

:: Verify Pi skills and ownership
dir "%USERPROFILE%\.pi\agent\skills"
type "%USERPROFILE%\.agent-core-state\ownership.json"

:: Verify Devin resources
dir "%APPDATA%\devin\skills"
dir "%APPDATA%\devin\agents"

:: Verify OpenCode skills
dir "%USERPROFILE%\.config\opencode\skills"

:: Inspect canonical checkout problems
git -C "%USERPROFILE%\.agent-core" status --short

:: Retire one old project-local installation
cd /d "<old-target-directory>"
agent-core retire-local --here
```
