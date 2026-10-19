---
name: manage-python-agent-envs
description: >
  Create, reuse, and manage purpose-specific Python environments with uv.
  Defaults to independent projects under .agent-envs/, excluded from Git
  locally, without using or changing the repository's root environment.
  Use for Python execution, testing, evaluation, and tooling dependencies.
  Use the standard root environment only when explicitly requested.
---

# Manage Agent Python Environments

Use one independent uv project per purpose. Default to agent-owned environments,
not the team's Python setup. Even a one-off Python task uses this layout:

```text
<repo>/.agent-envs/
  offline-eval/
    pyproject.toml
    uv.lock
    .python-version
    .venv/
  data-analysis/
    pyproject.toml
    uv.lock
    .python-version
    .venv/
```

Use native uv commands, not a custom manager, registry, or activation script.
Examples below use `<env>` for the absolute purpose-project path and `<repo>` for
the absolute repository root. Use the current shell's syntax and quote paths.
Check `uv --version`; if uv or a required option is unavailable, stop and report it
rather than switching tools or silently upgrading the installation.

## Boundaries

- Never create, use, sync, or modify root `.venv/` unless explicitly requested.
  Its existence or the presence of a root `uv.lock` is not permission.
- Read shared Python configuration for requirements, but leave root manifests,
  lockfiles, Python pins, requirements files, Conda/deployment configuration, and
  tracked `.gitignore` unchanged unless their modification is explicitly in scope.
- Do not create task environments elsewhere. Do not use `uv run --with`,
  `--isolated`, `uvx`, `uv tool install`, or bare `uv venv` as shortcuts.
- Do not use activation, direct pip, `uv pip` patches, or system Python as an
  execution fallback. Run workloads through the selected uv project.
- Follow organizational package-index, certificate, proxy, and interpreter
  acquisition policy. Never bypass it or change machine-wide settings.
- uv caches, managed Python installations, and temporary package-build
  environments may live outside `.agent-envs/`; task environments must not.
  A virtualenv isolates dependencies, not the code's filesystem/network access.

## 1. Discover and select

1. Find the Git root with `git rev-parse --show-toplevel`. Read applicable project
   instructions and the workload's Python/dependency constraints. Without a Git
   repository, stop and ask rather than invent another location or initialize Git.
2. Inspect `.agent-envs/` and select a short, lowercase purpose name, such as
   `offline-eval`, `integration-tests`, or `data-analysis`. Avoid generic `dev`,
   agent names, dates, and random identifiers.
3. Reuse the matching project when its Python and dependencies are compatible.
   Add missing purpose-related dependencies there; do not create a new environment
   for every command or session. Only split for a different purpose or genuinely
   incompatible requirements, using a meaningful suffix such as `offline-eval-py311`.
4. Treat existing environments as shared between agent sessions. Do not change,
   sync, rebuild, or remove one while another run uses it. Coordinate or stop if
   uncertain; do not invent a locking service or duplicate it merely to avoid waiting.
   `uv run --locked` can still sync the environment, so it also needs this check.
5. Resolve the chosen path and confirm it stays under this repo's `.agent-envs/`.
   Refuse symlink/junction redirection or an unexplained existing directory; do not
   overwrite files or adopt an unknown bare virtualenv.

## 2. Establish local Git exclusion

Before creating environment files:

- Check `git ls-files -- .agent-envs` from the root. If it returns tracked files,
  stop: ignoring does not untrack them. Never automatically remove them from Git.
- Check whether the intended path is already ignored. If not, resolve the local
  exclusion file using `git rev-parse --git-path info/exclude` from the root and
  append `/.agent-envs/` on its own line, preserving existing contents. Do not
  assume `.git` is a directory; worktrees can use a file instead.
- Verify with `git check-ignore -v -- .agent-envs/<purpose>/pyproject.toml`.
  Confirm an effective exclusion, not a negating `!` rule. Check the created files
  again after setup. If exclusion cannot be established, stop rather than editing
  tracked `.gitignore` or choosing another location.

This is local to the checkout; no team-wide ignore change or commit is needed.
Never stage or force-add anything under `.agent-envs/`.

## 3. Create or restore the selected project

Before **every uv operation**, explicitly select `<env>`. Scope
`UV_PROJECT_ENVIRONMENT` to the absolute `<env>/.venv` for those commands only;
restore any prior value afterward. Clear inherited `VIRTUAL_ENV`, `PYTHONHOME`,
and `PYTHONPATH` for these commands, and inspect uv overrides that could change
project, interpreter, or sync selection (including `UV_PROJECT`, `UV_PYTHON`, and
`UV_NO_SYNC`). Remove conflicting overrides only in the command scope. Preserve
approved index/proxy/certificate settings. Never use `--active`.

### New project

Choose Python from the workload's explicit requirement, otherwise a compatible
repository pin, otherwise an installed supported stable Python. Resolve an exact
version and record it locally; do not silently upgrade Python on reuse. Obtain a
missing interpreter through `uv python install` only when organizational policy
permits; otherwise ask.

```text
uv init --bare --no-package --no-workspace --vcs none --python <version> "<env>"
```

Before any add, lock, sync, or run command, append this boundary to the **new
local** `pyproject.toml`:

```toml
[tool.uv.workspace]
```

This empty table makes the purpose project its own workspace boundary with no
additional members. `--no-workspace` prevents enrollment during initialization;
the table also prevents later commands from using a parent workspace's lockfile.
Do not add members or edit the parent workspace.

```text
uv python pin --project "<env>" <version>
uv lock --project "<env>"
uv sync --project "<env>" --locked
```

Set `requires-python` to the workload's actual compatibility range in the local
manifest when needed; a Python pin chooses the interpreter but does not narrow
that range. Add only the dependencies the purpose needs, using the next section.

### Existing project

Inspect its manifest, pin, and lockfile before mutation. Confirm the local empty
workspace boundary; add it only to a known agent-owned standalone project if
missing. Do not overwrite an existing workspace configuration. Reuse the recorded
Python version and run `uv sync --project "<env>" --locked` to restore its `.venv`.
If the local pin is missing, recover the environment's Python version and record
it before syncing; ask if it cannot be established safely.
If the lock is missing or stale, inspect why before intentionally running `uv lock`
inside this purpose project. Do not silently regenerate it to bypass a failure.

## 4. Manage dependencies and execute

Keep dependencies and their resolved versions in this purpose project's manifest
and lockfile. Do not hand-edit lockfiles. `uv add` and `uv remove` update both files
and sync automatically; no extra sync is normally needed afterward.

| Need | Command |
| --- | --- |
| Add a required package | `uv add --project "<env>" <package>` |
| Inspect dependencies | `uv tree --project "<env>" --locked` |
| Restore from the lock | `uv sync --project "<env>" --locked` |
| Intentionally upgrade one package | `uv lock --project "<env>" --upgrade-package <package>`, then locked sync |
| Remove an explicitly unwanted dependency | `uv remove --project "<env>" <package>` |
| Run a script | `uv run --project "<env>" --locked python "<repo>/scripts/evaluate.py"` |
| Run tests | `uv run --project "<env>" --locked python -m pytest` |

Autonomously add dependencies needed for the declared purpose. Preserve existing
constraints; ask before incompatible changes, removing dependencies other work may
need, or changing Python. Do not run blanket upgrades or install a standard suite
of tools without a task need.

`--project` selects the environment, **not the process working directory**. Run
from the repository root unless the workload requires another directory; use
absolute script/input/output paths when needed. Do not change into `<env>` merely
to run repository code.

For a packaged repository, install its local package into this environment with
`uv add --project "<env>" --editable "<repo>"` when the task needs it. This changes
only the local environment's dependency declaration, though package builds can
produce source-tree artifacts. Respect the project's build instructions. Do not
convert an unpackaged repo into a package or migrate its dependency manager.
For existing requirements files, use `uv add --project "<env>" -r "<requirements>"`
only after inspecting their dependencies, sources, and options.

Invoke scripts through `python` as above, not `uv run script.py`: inline PEP 723
metadata can select a separate script environment. If such metadata exists, carry
its required dependencies/Python constraints into the purpose project instead of
editing the shared script. Do not use `--with` to supply missing packages.
Add `--env-file "<file>"` to the explicitly targeted run command when task-required
variables are needed; never copy secrets into the manifest, lockfile, or report.

## 5. Verify, recover, and report

Before the workload, verify the interpreter:

```text
uv run --project "<env>" --locked python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.version)"
```

Confirm the executable and prefix belong to `<env>/.venv` (Windows interpreter:
`.venv/Scripts/python.exe`; POSIX: `.venv/bin/python`). Stop on a mismatch. Run a
relevant import or actual entry-point check, and inspect Git status/diffs to ensure
environment management did not change shared configuration.

On failure, inspect the error, local dependency tree, Python pin, and lockfile;
fix the cause and retry the selected project. Never fall back to root/system
Python, delete a lockfile, relax constraints blindly, or bypass package policy.
Rebuild a broken `.venv` only when known to be agent-owned and idle, preserving its
manifest, lockfile, and pin. Do not automatically prune environments; removal
requires an explicit request.

Report concisely: purpose, created/reused, absolute project and interpreter paths,
Python version, lockfile path, dependencies changed, and verification result.
When asked for an inventory, list purpose directories, Python pins, direct
dependencies, and whether their lockfiles and interpreters exist. Do not invent
verification history or maintain a separate registry.

## Explicit root mode

Only an explicit request to use/manage the repository's standard environment
selects root mode, for that task only. Explain the mode switch, inspect the existing
setup, then use the same explicit targeting with `<env> = <repo>` and environment
path `<repo>/.venv`. Do not add the agent workspace-boundary table to the root.
For an existing uv project, prefer locked sync/run. Do not initialize, migrate,
change shared dependencies, update lockfiles, or alter Python pins unless those
changes are also authorized. If the request cannot be satisfied without them, ask.
For an explicitly requested standalone root virtualenv, `uv venv "<repo>/.venv"`
is allowed; do not invent a root uv project. Default back to `.agent-envs/` for
subsequent unrelated work.
