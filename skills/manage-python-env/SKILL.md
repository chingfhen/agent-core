---
name: manage-python-env
description: >
  Manage and execute Python through reusable, independent uv purpose projects
  under a confirmed Python Environment Root. Load before all Python execution,
  including interpreter checks and import probes, testing, evaluation, tooling,
  and dependency management;
  reuse compatible environments automatically instead of ad hoc isolated commands.
  Keep personal environments separate from team Python configuration.
disable-model-invocation: false
---

# Manage Python Environments

Own both environment management AND utilization. Before the first Python command,
including interpreter checks and import probes, load this skill and select
or create the right purpose project, then actually execute through it. Do not just
inventory environments or recommend one while running elsewhere.

## Resolve and select

1. Read `Python Environment Root` in applicable `AGENTS.md`. New section-relative
   paths resolve from its declaring directory; legacy workspace-relative paths
   retain their recorded base, never the shell's current directory. For missing
   routing or an authorized routing change, read [Python routing](references/routing.md).
   This skill can establish its own resources without workspace-setup. An explicit
   destination selected by the human for this operation is allowed without changing
   the saved routing. Report inaccessible configured resources and ask about
   conflicting ownership/destinations. No `projects.toml` or separate environment registry.
2. Identify the workload's code root and Python/dependency constraints. It may be
   a repository nested below the workspace; environment storage need not be in Git.
   Read project instructions and team dependency files without changing them.
3. Inspect immediate purpose folders under the configured root. Use one independent
   uv project per purpose, directly under that root, e.g. `offline-eval` or
   `data-analysis`. Reuse one when its Python and dependencies are compatible,
   including across repositories. Add missing purpose-related dependencies there.
   Split only for a distinct purpose or incompatible requirements; use meaningful
   names such as `retrieval-eval-py311`, not dates, agent names, or random IDs.
4. Treat environments as shared across sessions. Before any command that can sync,
   modify, or rebuild one, establish that no conflicting run is using it. Even
   `uv run --locked` may sync. Coordinate or stop if uncertain; do not invent a
   locking service or clone an environment merely to avoid waiting.
5. Resolve paths and require the selected purpose project to stay inside the
   configured root. Refuse symlink/junction/reparse redirection, unexplained existing
   directories, and unknown bare virtualenvs. Do not adopt or overwrite them.

Reading a path or source file is not Python execution. Selecting a repository's
bootstrap script does not select or authorize its repository-local environment.

Use `<env>` below for the absolute purpose-project path and `<code>` for the
workload's code root. Paths are separate on purpose. The context home can be a
Git repository, part of one, or not versioned at all.

## Boundaries

- Never create, use, sync, or change a team/root `.venv` unless explicitly requested
  for this task. Its existence or a root `uv.lock` does not grant permission.
- Leave team manifests, locks, pins, requirements, deployment settings and tracked
  `.gitignore` unchanged unless modification is explicitly in scope.
- No `uv run --with`, `--isolated`, `uvx`, `uv tool install`, bare `uv venv`,
  activation, pip, `uv pip` patches, or system-Python workload fallback.
- Follow approved package-index, certificate, proxy, and interpreter-download
  policy. Never bypass policy or change machine-wide settings.
- uv caches, managed interpreter installations, and temporary build environments
  may live outside the root; the purpose project and its `.venv` must not.
- A virtualenv isolates dependencies, not code's filesystem or network permissions.
- Do not auto-prune environments. Removal needs an explicit request.

## Preserve the recipe; exclude generated state

A purpose folder contains:

```text
<env>/
  pyproject.toml
  uv.lock
  .python-version
  .venv/
```

The first three files are reproducible configuration and may be versioned; do not
ignore the whole purpose project. `.venv`, Python caches, and secret files must not
be committed. Never copy credentials into a manifest, lockfile, or report.

Before creating generated files, determine the actual Git worktree containing
`<env>` if any. In an explicitly personal context repository, inspect existing
ignore rules and add narrowly scoped exclusions for `.venv/`, `__pycache__/`,
`*.pyc`, `.env`, and identified secret files inside the configured Python area.
Use its tracked `.gitignore` so exclusions survive recovery. Preserve existing
rules, check `git ls-files` for already tracked generated/secret paths, and verify
with `git check-ignore -v` (not a negating rule). If generated files are already
tracked, stop rather than untracking them automatically. Never stage or commit
as incidental environment management.

If the context is inside a team worktree instead, do not change its tracked ignore
file: use exact context-relative exclusions in its Git-local `info/exclude`,
resolved with `git rev-parse --git-path info/exclude`. If ownership is unclear, ask.
Without Git, no Git setup is required; report that backup is not established rather
than initializing a repository. Inspect output/status to ensure team configuration
remains unchanged. Secret exclusion patterns are not a substitute for data review.

## Target every uv operation

Check `uv --version`; if uv or a required option is unavailable, stop rather than
silently upgrading or switching tools. Use native uv commands, no custom manager.
Use the current shell's syntax and quoted absolute paths.

For each project operation, explicitly select `<env>`. Scope
`UV_PROJECT_ENVIRONMENT` to `<env>/.venv` for those commands only. Clear inherited
`VIRTUAL_ENV`, `PYTHONHOME`, and `PYTHONPATH` in that command scope; inspect conflicting
uv overrides such as `UV_PROJECT`, `UV_PYTHON`, and `UV_NO_SYNC` and remove them
only in that scope. Restore prior values afterward. Preserve approved proxy/index/
certificate settings. Never use `--active`.

### New purpose project

Choose Python from the workload requirement, then a compatible code pin, then an
installed supported stable Python. Resolve an exact version and pin it. Acquire
an unavailable interpreter with `uv python install` only if organizational policy
permits; otherwise ask. No silent Python upgrades on reuse.

```text
uv init --bare --no-package --no-workspace --vcs none --python <version> "<env>"
```

Before add/lock/sync/run, put this boundary in the new local `pyproject.toml`:

```toml
[tool.uv.workspace]
```

It makes the purpose project independent from parent uv workspaces. Do not enroll
members or edit a parent's workspace. Set `requires-python` to the workload's
actual supported range when needed; a pin alone does not narrow that range.

```text
uv python pin --project "<env>" <version>
uv lock --project "<env>"
uv sync --project "<env>" --locked
```

### Existing purpose project

Inspect the manifest, pin, lockfile, and independent workspace boundary before
mutation. Add a missing empty boundary only to a known agent-owned standalone
project; do not overwrite an existing workspace configuration. Reuse its recorded
Python version. If a pin is absent, recover the exact version from the environment
before syncing; ask if it cannot be established safely. Restore an absent `.venv`
with locked sync. Inspect missing/stale locks before deliberately relocking; do
not regenerate a lock merely to bypass an error.

## Manage dependencies AND execute

| Need | Command |
| --- | --- |
| Add a required dependency | `uv add --project "<env>" <package>` |
| Inspect dependencies | `uv tree --project "<env>" --locked` |
| Restore from the lock | `uv sync --project "<env>" --locked` |
| Intentionally upgrade one package | `uv lock --project "<env>" --upgrade-package <package>`, then locked sync |
| Remove an explicitly unwanted dependency | `uv remove --project "<env>" <package>` |
| Execute a script | `uv run --project "<env>" --locked python "<code>/scripts/evaluate.py"` |
| Execute tests | `uv run --project "<env>" --locked python -m pytest` |

Autonomously add dependencies necessary for the authorized purpose; `uv add` and
`uv remove` already update manifest/lock and sync. Ask before incompatible changes,
Python changes, or removing dependencies other work may need. No blanket upgrades
or preinstalled generic tool suites. Never hand-edit lockfiles.

`--project` selects the environment, NOT the process working directory. Run from
the workload's code root unless its instructions require otherwise, using absolute
script/input/output paths as needed. Do not change into `<env>` to run repository
code. An explicitly needed local package can be installed with
`uv add --project "<env>" --editable "<code>"`; inspect build instructions and
possible source-tree build artifacts. Do not convert an unpackaged repo or migrate
its package manager. Inspect requirements before importing them with
`uv add --project "<env>" -r "<requirements>"`.

Invoke scripts through `python`, not `uv run script.py`: PEP 723 inline metadata
can select a separate script environment. Carry those requirements into the
purpose project instead of editing the shared script. Use a scoped `--env-file`
only when required; do not copy its secret values into configuration or reports.

## Verify, recover, report

Before the workload, with the same scoped targeting, run:

```text
uv run --project "<env>" --locked python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.version)"
```

Confirm executable and prefix belong to `<env>/.venv` (Windows:
`.venv/Scripts/python.exe`; POSIX: `.venv/bin/python`). Stop on mismatch. Then
run the real workload or relevant entry-point/import check through that project.
Inspect Git status/diffs where applicable for unintended shared configuration edits.

Diagnose errors using the selected project's pin, dependencies, lock and command.
Never fall back to root/system Python, delete the lock, relax constraints blindly,
or bypass package policy. Rebuild a broken `.venv` only when known owned and idle,
preserving the recipe. Report purpose, created/reused, absolute project/interpreter
paths, Python version, lock path, dependency changes, and actual workload result.
Inventory-only requests list purpose folders, pins, direct dependencies, and
lock/interpreter presence, without claiming runtime verification or writing a
second registry. Runtime use does not require rewriting AGENTS.md routing.

## Explicit team/root mode

Only an explicit human request selects the code repository's standard environment
for that task. Explain the switch and inspect the setup. Explicit targeting and
verification still apply, but do not insert the agent workspace boundary into team
configuration. Prefer locked operations for existing uv projects. Initializing,
migrating, modifying dependencies/locks/pins still needs its own authorization.
For an explicitly requested standalone root virtualenv, `uv venv` is permitted;
do not invent a root uv project. Return to configured purpose projects for unrelated
work. This exception is not permission to bypass missing workspace configuration.
