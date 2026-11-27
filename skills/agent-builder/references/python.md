# Python Environments and Execution

Own both reusable purpose environments AND actual Python execution. Read after Agent Builder root for "create a Python environment for X", "manage my Python environments", explicit dependency/pin/lock changes, repair, sync or routing, or a concrete maintenance need during an authorized workload. Known compatible environment discovery, inspection, interpreter/import probes and execution use the standing AGENTS.md utilization contract below without loading Agent Builder. A request to run a Python script is a workload cue, not automatically maintenance. Do not stop at inventory or advice when execution is requested.

## Resolve and select

Use the root's confirmed resource resolution and initialization/registration approval. Default new agent-scoped root: `.work-context/python/`; preserve configured Python Environment Root, legacy path bases and explicit one-operation selection. Reuse/register an unambiguous compatible existing root during authorized maintenance; confirm actual ownership, recipes and independence, not folder names. Read-only discovery does not register. Never substitute an inaccessible root or invent a project identity. No registry.

Identify the workload's code root, applicable team/project instructions, Python version and required dependencies/groups/extras/platform. Inspect immediate purpose folders and their manifest, exact pin, lock, independent workspace boundary and installed state. Reuse a compatible purpose across repositories where appropriate. Split for a distinct purpose or incompatible requirements, not for a new task/session, random suffix or to avoid waiting. Use descriptive names such as offline-eval or retrieval-eval-py311. Optimize for the actual platform; cross-platform compatibility is not a requirement. Recipe recovery on the same machine still matters.

Confirm absolute project and .venv paths are within the configured root; reject unexplained directories, unknown bare virtualenvs, unsafe symlink/junction/reparse redirection of roots, purpose directories or .venv. Normal POSIX venv interpreter symlinks to a base interpreter are expected: verify the invocation path and actual sys.prefix rather than rejecting the legitimate base executable. Preserve narrower local gates. Reading source/path/recipe is not Python execution. Selecting a team bootstrap script does not authorize a team environment.

## Exact utilization boundary

Ordinary use may inspect files, recipes, installed metadata, interpreter identity and dependencies, and execute authorized scripts/modules/tests/imports through an existing compatible purpose interpreter. It does not create, sync, install, remove, relock, upgrade, rebuild or alter routing/recipes. Generated normal workload output/cache is not environment maintenance; an invocation that installs packages, self-bootstraps a venv, alters an interpreter or changes a recipe is maintenance regardless of the wrapper used. Inspect unknown scripts/bootstrap commands before running. A virtualenv is dependency isolation, not a security sandbox.

Use the direct absolute interpreter path, from the workload's code root, without activation or uv run. This avoids implicit sync/rebuild and PEP 723 script environment selection. Verify before the first dependent workload (including when launching a notebook kernel), reuse sufficiently current evidence within the same workload, and recheck after environment/recipe/requirement changes, observed drift or conflicting activity. Do not run while conflicting environment mutation is underway. Use the selected interpreter's bin/Scripts at the front of command-scoped PATH for necessary child Python/console commands, clear inherited VIRTUAL_ENV, PYTHONHOME and PYTHONPATH (and user-site injection where applicable), inspect conflicting overrides, preserve approved index/proxy/cert settings, restore previous values after the command. Use explicit interpreter for child Python where possible. No persistent activation or machine-wide changes.

Establish compatibility before use: exact pin, requires-python, relevant locked requirements/groups/extras/platform, actual sys.executable, sys.prefix, version, installed relevant distribution versions/imports and dependency consistency. Use sufficiently current verified locked-sync evidence or native non-mutating inspection; folder presence or an import alone is insufficient. Example probe using the selected absolute interpreter (with scoped variables above):

    "<python>" -c "import sys; print(sys.executable); print(sys.prefix); print(sys.version)"

Check the invocation and prefix belong to the selected .venv; compare version with pin and workload. Stop on mismatch. For dependency checks use explicit `uv pip check --python "<python>"` and `uv pip list --python "<python>"` when needed (no installation), comparing actual versions with the applicable lock/requirements; these alone do not establish lock freshness. Where the installed uv version's behavior is established to be non-mutating, with existing valid .venv and explicit scoped targeting, `uv lock --check --project "<env>" --offline --no-python-downloads` and `uv sync --check --locked --project "<env>" --offline --no-python-downloads` can check recipe freshness and synchronization; inspect flags/version, never probe an absent/broken environment this way, and route to maintenance if non-mutation or compatibility cannot be established. Do not treat --no-sync/--frozen or --locked alone as a safe substitute. No new wrapper or verification registry. Preserve sufficient prior evidence; don't repeat package inventories on every command.

If requirements are missing, incompatible, stale, inaccessible or uncertain, do not silently run elsewhere; load Agent Builder and this reference for necessary maintenance (or report an ownership/access/policy blocker). Select a compatible environment, create/repair/sync when authorized, then perform the requested workload and inspect actual result. Routine reuse may not edit routing.

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
- Do not auto-prune environments. Deleting a purpose project/recipe requires explicit human intent; safe repair/rebuild of a known-owned idle generated .venv is allowed during authorized maintenance. Do not delete working purpose environments merely to reclaim space.

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

## Autonomous maintenance and concurrency

A concrete need during authorized execution or a human maintenance request permits ordinary maintenance of established personal purpose projects: select/create a compatible purpose, add necessary compatible dependencies, choose a suitable pinned Python for a new purpose, restore/sync/repair known owned state, and actually run the workload. First initialization of a new resource root follows root approval; do not silently change workspace routing or install uv/other machine tools. Respect repository/employer/network/package policy. Prefer a separate compatible purpose rather than changing an existing environment in a way that may break other consumers. Inspect affected dependencies/consumers and lock changes; no blanket upgrades, disruptive removals or incompatible pin changes to a shared purpose without human authority. No destructive cleanup or automatic maintenance of unrelated environments.

Treat environments as shared across sessions. Before any command that can sync, modify or rebuild, establish that no conflicting run or mutation is using that environment; even uv run --locked may sync. Coordinate or stop if uncertain; do not invent a locking service or duplicate environments just to avoid waiting. Recheck ownership, target and current recipe immediately before mutation; reconcile concurrent edits. If repair fails, preserve recipe, explain the blocker and never fall back to system/transient/team Python.

## Target every uv operation

For uv operations check `uv --version`; if uv or a required option is unavailable, stop rather than
silently upgrading or switching tools. Use native uv commands, no custom manager.
Use the current shell's syntax and quoted absolute paths.

For each project operation, explicitly select `<env>`. Scope
`UV_PROJECT_ENVIRONMENT` to `<env>/.venv` for those commands only. Clear inherited
`VIRTUAL_ENV`, `PYTHONHOME`, and `PYTHONPATH` in that command scope; inspect conflicting
uv overrides such as `UV_PROJECT`, `UV_PYTHON`, `UV_NO_SYNC`, `UV_FROZEN`, dependency group/extra selectors and interpreter targeting, removing conflicting values
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
| Execute a script after verifying compatible state | `"<python>" "<code>/scripts/evaluate.py"` |
| Execute tests after verifying compatible state | `"<python>" -m pytest` |

Autonomously add dependencies necessary for the authorized purpose; `uv add` and
`uv remove` already update manifest/lock and sync. Prefer a separate purpose for incompatible requirements. Ask before disruptive changes to an existing shared purpose, including incompatible Python changes or removing dependencies other work may need. No blanket upgrades
or preinstalled generic tool suites. Never hand-edit lockfiles.

`--project` selects the environment, NOT the process working directory. Run from
the workload's code root unless its instructions require otherwise, using absolute
script/input/output paths as needed. Do not change into `<env>` to run repository
code. An explicitly needed local package can be installed with
`uv add --project "<env>" --editable "<code>"`; inspect build instructions and
possible source-tree build artifacts. Do not convert an unpackaged repo or migrate
its package manager. Inspect requirements before importing them with
`uv add --project "<env>" -r "<requirements>"`.

Invoke scripts through the selected absolute interpreter, not `uv run script.py`: PEP 723 metadata can select a separate script environment. Inspect and carry those requirements into the purpose project instead of editing the shared script. If an env file is explicitly needed, load its approved values via the workload's existing scoped mechanism (or an authorized maintenance-mode uv command); never persist secret values or expose them in logs. Do not treat direct interpreter invocation as proof a nested command uses the same environment.

## Verify, recover, report

After maintenance verify the actual recipe/pin/lock, generated-state placement and relevant exclusions, then apply the utilization checks above using the same explicit interpreter and scoped variables. Run the real workload or required representative entry-point/import check and inspect actual exit status/results. Inspect Git status/diffs where applicable for unintended shared configuration edits. Reuse sufficient verification rather than repeating probes or scanning unrelated environments. Missing workload execution is not success.

Diagnose errors using the selected project's pin, dependencies, lock and command.
Never fall back to root/system Python, delete the lock, relax constraints blindly,
or bypass package policy. Rebuild a broken `.venv` only when known owned and idle,
preserving the recipe.
For maintenance report actual created/reused purpose, project/interpreter and lock paths, Python version, dependency changes and actual workload outcome. Ordinary reuse needs no separate maintenance receipt; disclose consequential deviations or gaps. Inventory-only requests list purpose folders, pins, direct dependencies and lock/interpreter presence without claiming runtime verification or writing a second registry. Runtime use does not require rewriting AGENTS.md routing.

## Explicit team/root mode

Only an explicit human request selects the code repository's standard environment
for that task. Explain the switch and inspect the setup. Explicit targeting and
verification still apply, but do not insert the agent workspace boundary into team
configuration. Prefer locked operations for existing uv projects. Initializing,
migrating, modifying dependencies/locks/pins still needs its own authorization.
For an explicitly requested standalone root virtualenv, `uv venv` is permitted;
do not invent a root uv project. Return to configured purpose projects for unrelated
work. This exception is not permission to bypass missing workspace configuration.

## Default AGENTS.md guidance fragment

Use confirmed locators in the root-owned block or an authoritative retained legacy section during approved incremental adoption; never duplicate routing. This is actionable standing guidance for ordinary use, not a demand to read the maintenance skill on every invocation.

    Python Environment Root: [confirmed locator]
    Before Python work (including import/interpreter probes, tests, notebooks
    or tools), resolve applicable project instructions and workload code root,
    Python/dependency requirements; inspect immediate purpose projects' manifest,
    exact pin, lock, independent workspace boundary and installed state. Reuse a
    known compatible purpose; never infer compatibility from folder name.
    Confirm owned project/.venv inside the root, no unsafe directory redirection.
    Use absolute <env>/.venv/Scripts/python.exe (Windows) or
    <env>/.venv/bin/python (POSIX) from the workload's code root, not the
    environment folder. Scope PATH for child tools to that environment; clear
    inherited VIRTUAL_ENV, PYTHONHOME, PYTHONPATH and conflicting overrides;
    preserve approved policy settings and restore shell state. No activation.
    Probe sys.executable, sys.prefix and sys.version through that interpreter;
    check target/pin and required installed versions against recipe/lock.
    Reuse sufficient current locked-sync/runtime evidence; otherwise inspect
    metadata (uv pip list/check --python <absolute interpreter>) and lock.
    For project-level check commands use --project <absolute env>, scoped
    UV_PROJECT_ENVIRONMENT=<absolute env>/.venv, no interpreter downloads and
    offline checks; clear conflicting uv overrides. Only use check flags when
    installed-version non-mutation is established and target is valid; never use --locked alone or --no-sync as
    proof of compatibility. Stop on uncertainty, drift, mismatch or concurrent
    mutation; load Agent Builder and python.md for necessary maintenance.
    Execute requested workload through the verified interpreter; inspect result.
    Legacy uv run --locked recipes may sync; do not use them as the ordinary
    verified-interpreter execution route.
    Never use system Python, transient environments, ad hoc pip/uv pip patches,
    uvx, --with/--isolated, auto-installing wrappers or team/root .venv by default.
    Load Agent Builder + python.md before creation, dependency/pin/lock change,
    sync/rebuild/repair or routing, including commands that may implicitly mutate.
    Autonomous compatible maintenance is permitted for authorized personal work;
    no team modifications, disruptive shared changes or purpose deletion without
    applicable explicit permission. No fallback or silent tool/policy changes.

The root may condense wording without dropping essential checks. Version-specific maintenance details and recovery stay here. Do not duplicate inventories in guidance.

## Design basis

- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) and [CLI reference](https://docs.astral.sh/uv/reference/cli/): lock freshness, installed-state checks and execution are separate; --locked may still sync, --no-sync skips that check. Use native explicitly targeted uv maintenance.
- [Python venv](https://docs.python.org/3/library/venv.html): absolute interpreter invocation avoids activation; sys.prefix distinguishes venv use. Venvs are generated state, not portable backups.
- [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) and [project configuration](https://docs.astral.sh/uv/concepts/projects/config/): independent project boundary, explicit project selection and environment override matter.
- [uv environment inspection](https://docs.astral.sh/uv/pip/inspection/): metadata and compatibility checks are useful but do not alone prove equality to a specific lock.
- [PEP 723](https://peps.python.org/pep-0723/): inline script metadata may select script dependencies; use purpose project instead of implicit ephemeral script environments.

Do not repeat design research routinely. Task 08 must verify installed-version check flags, no-mutation behavior, scoped targeting, fresh-session activation and actual execution on representative target harnesses before transition; this source is not proof of runtime compliance.
