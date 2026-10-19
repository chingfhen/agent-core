---
name: manage-python-agent-envs
description: Autonomously create and manage local, purpose-specific uv environments under .agent-envs without modifying the repository's existing Python environment. Use when an agent needs isolated testing, evaluation, integration, or tooling dependencies that are not part of the product.
---

# Manage Local Agent Python Environments

Manage agent-owned Python environments under:

`<repo>/.agent-envs/<purpose>/`

These environments are local implementation details. They must not modify or
replace the repository's existing Python environment.

## Ownership boundary

The repository's existing environment belongs to the product:

- `<repo>/pyproject.toml`
- `<repo>/uv.lock`
- `<repo>/.venv/`
- Existing requirements files
- Existing Conda configuration
- Existing deployment environment

Do not modify those files unless the task explicitly concerns the product
environment.

Agent-owned environments belong under:

`<repo>/.agent-envs/`

## Standard layout

Each durable agent environment uses:

`<repo>/.agent-envs/<purpose>/pyproject.toml`
`<repo>/.agent-envs/<purpose>/uv.lock`
`<repo>/.agent-envs/<purpose>/.venv/`

Use short, purpose-based names:

- `evaluation`
- `integration`
- `tools`
- `data-analysis`
- `notebooks`

Do not use:

- `prod`
- `dev`
- Agent names
- Random identifiers
- Dates or timestamps

Do not create multiple environments for the same purpose unless incompatible
Python or package requirements require it.

## Git isolation

Ensure the repository's `.gitignore` contains:

`.agent-envs/`

If `.gitignore` is unavailable or must not be changed, use the repository-local
Git exclusion file:

`.git/info/exclude`

Add:

`.agent-envs/`

Prefer `.git/info/exclude` when this workflow is personal and should not alter
the repository's tracked `.gitignore`.

Never commit anything under `.agent-envs/`.

## Environment selection

Before creating an environment:

1. Inspect `.agent-envs/` for an existing matching purpose.
2. Reuse it when its Python and dependency requirements are compatible.
3. Create a new environment only when no suitable environment exists.
4. Never modify the root project merely to support agent tooling.

Use an isolated temporary run instead of a durable environment when:

- The task is a one-off probe
- Only one or two temporary packages are required
- No persistent dependency definition is needed

Use a durable `.agent-envs/<purpose>/` project when:

- The environment will be used repeatedly
- Several packages must be resolved together
- A lockfile is useful
- More than one agent session may use it
- The task needs a stable Python version

## Creation procedure

For a new durable environment:

1. Create `.agent-envs/<purpose>/`.
2. Initialize a minimal uv project in that directory.
3. Pin or select the required Python version.
4. Add only dependencies required for that purpose.
5. Generate `uv.lock`.
6. Run `uv sync`.
7. Verify using the actual entry point or import.
8. Report the exact project, interpreter and lockfile paths.

Do not initialize a uv workspace.

Each purpose environment is an independent uv project with its own lockfile.

## Execution

Run commands against the selected environment from its project directory, or
use uv's project-selection option where supported.

Do not manually activate `.venv`.

Do not use:

- Direct `pip install`
- The system Python as an implicit fallback
- The repository's root environment for unrelated agent tooling
- Public package indexes when an organizational package policy applies

## Dependency changes

The agent may autonomously:

- Create a new purpose environment
- Add dependencies needed for its declared purpose
- Update that environment's lockfile
- Recreate its `.venv`
- Reuse a compatible existing purpose environment

The agent must not autonomously:

- Modify repository-level dependency files
- Modify deployment requirements
- Change an existing environment to an incompatible Python version
- Remove an environment that may be in use
- Substitute an unapproved package source

## Reporting

After creating or modifying an environment, report:

Environment: <purpose>
Mode: durable agent environment
Project: <absolute path>
Interpreter: <absolute path to Python>
Python: <version>
Lockfile: <absolute path>
Packages changed: <summary>
Verification: <command and result>

For temporary execution, report:

Environment: temporary isolated uv environment
Purpose: <purpose>
Packages: <packages>
Verification: <command and result>

## Discovery command

When the human asks where environments are stored, list:

- Each directory under `.agent-envs/`
- Its Python requirement
- Its interpreter path
- Whether `.venv` exists
- Whether `uv.lock` exists
- Its direct dependencies
- The most recent verification performed, if recorded

## Organizational policy overlay

If an organization-specific environment skill applies, its rules override this
skill for:

- Package indexes
- Proxy configuration
- Certificates
- Interpreter acquisition
- Package quarantine
- Approved download sources