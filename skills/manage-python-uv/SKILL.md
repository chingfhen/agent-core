---
name: manage-python-uv
description: Autonomously manage Python project environments, dependencies, tooling, and execution using uv's modern project workflow.
---

# Python Environment Management (Windows, uv)

You are responsible for maintaining this project's Python environment on Windows using `uv` as the single source of truth.

**Platform:** Windows. Use PowerShell syntax. Use `python` (not `python3`). Never reference Unix-style paths or shell activation.

---

# Invocation Flow

When this skill is invoked:

1. **Discover** — inspect `pyproject.toml`, `uv.lock`, `.python-version`, existing source/test layout
2. **Classify** — determine project state (see Project Discovery)
3. **Act** — take the action for that state
4. **Report** — tell the user what was found and what was done

---

# Core Principles

Use `uv` exclusively:

| Do | Don't |
|---|---|
| `uv add` | `pip install` |
| `uv remove` | `pip uninstall` |
| `uv sync` | `pip install -r requirements.txt` |
| `uv run <cmd>` | `python main.py` or `pytest` directly |
| `uv lock` | manual lockfile edits |
| `uv python` | system Python directly |

Never activate the virtualenv manually. These are all wrong:

- `.venv\Scripts\Activate.ps1` — unnecessary when using `uv run`
- `source .venv/bin/activate` — Unix only, wrong platform
- `uv pip install` — bypasses project management

All execution goes through `uv run`.

---

# Project Discovery

Inspect in order:

1. `pyproject.toml` — exists? has `[project]` section? has `[tool.uv]`?
2. `uv.lock` — exists and committed?
3. `.python-version` — pinned version?
4. `.gitignore` — contains `.venv/`?

**Classify and act:**

| State | Signals | Action |
|---|---|---|
| Existing uv project | `pyproject.toml` + `uv.lock` present | Run `uv sync`, verify with `uv tree` |
| Needs migration | `requirements.txt` / `setup.py` / `poetry.lock` present | See Migration section — ask user first |
| New Python project | Source files, no config | Run `uv init` |
| Non-Python project | No Python files | Do nothing, report to user |

Do not rewrite project structure unless requested.

---

# Bootstrapping New Projects

```powershell
uv init
```

After init, ensure:

- `pyproject.toml` has a `[project]` section
- `.venv\` is created by uv on first sync
- `uv.lock` exists after first `uv sync`

---

# Python Version Management

```powershell
uv python install <version>    # install a Python version
uv python pin <version>        # write .python-version, update pyproject.toml
uv python list                 # see available and installed versions
```

Respect existing `.python-version` and `requires-python` in `pyproject.toml`.

Do not change Python versions automatically if the project already has a pinned version. Ask before upgrading major versions (e.g., 3.10 → 3.11+).

---

# Dependency Management

## Adding

```powershell
uv add <package>                          # production dependency
uv add --dev <package>                    # development dependency
uv add --dev pytest ruff mypy             # multiple dev deps at once
```

Custom index (e.g., PyTorch with CUDA):

```powershell
uv add torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

`uv add` automatically resolves, installs, and updates both `pyproject.toml` and `uv.lock`. No manual `uv sync` needed after `uv add`.

## Upgrading

```powershell
uv lock --upgrade-package <package>       # upgrade one package in lockfile
uv lock --upgrade                         # upgrade all packages in lockfile
uv sync                                   # apply updated lockfile to environment
```

Do not use `uv add --upgrade` — that flag does not exist.

## Removing

```powershell
uv remove <package>
```

Do not manually remove packages from lockfiles.

## Verifying

```powershell
uv tree                                   # hierarchical dependency tree
```

---

# Running Code

All execution through `uv run`. On Windows, use `python` not `python3`.

```powershell
uv run python main.py
uv run pytest
uv run ruff check .
uv run mypy .
```

One-off execution with an ad-hoc dependency (without adding it to the project):

```powershell
uv run --with <package> python -c "import <package>"
```

Never run directly:

```powershell
python main.py        # may use wrong interpreter
pytest                # may use system pytest outside the venv
```

---

# Synchronization

```powershell
uv sync               # sync env to current lockfile (development)
uv sync --locked      # strict sync — fails if lockfile is out of date (CI/CD)
```

Run `uv sync` when:

- `pyproject.toml` was modified manually (not via `uv add`/`uv remove`)
- Pulling upstream changes that may have updated dependencies
- `.venv\` directory is absent

`uv add` and `uv remove` auto-sync — no manual `uv sync` needed after those commands.

CI must never update lockfiles — always use `uv sync --locked` in CI.

---

# Lockfile Rules

`uv.lock` is source-controlled. Always commit it.

| Do | Don't |
|---|---|
| Commit `uv.lock` | Delete `uv.lock` to fix problems |
| Fix root dependency conflicts | Blindly regenerate lockfile |
| Inspect `uv tree` first | Manually edit `uv.lock` |

If lock resolution fails:

1. Inspect `uv tree` to identify the conflict
2. Fix the root constraint in `pyproject.toml`
3. Re-run `uv lock`

---

# Tooling

For project-pinned tools (reproducible, version-controlled with the project):

```powershell
uv add --dev ruff mypy pre-commit         # preferred for CI and project scripts
```

For standalone global CLI tools (not project-specific):

```powershell
uv tool install ruff                      # installs globally, outside the project
```

Default to `uv add --dev` for any tool used in CI or project scripts. Use `uv tool install` only when you want the tool available system-wide regardless of project context.

---

# Git Hygiene

`.gitignore` must contain:

```
.venv/
__pycache__/
*.pyc
```

Track in version control:

```
pyproject.toml
uv.lock
.python-version
```

---

# Migration from Other Tools

Do not migrate aggressively. Confirm migration is requested before acting.

**If migration is requested:**

| Source | Action |
|---|---|
| `requirements.txt` | Inspect file first, then `uv add` each dep — watch for conflicts |
| `poetry` | Run `poetry export`, then `uv add` each dep |
| `pip-tools` | Inspect `.in` files, migrate constraints to `pyproject.toml` |
| `conda` | Identify pip-installable deps, migrate manually |

After migration:

1. Verify with `uv tree`
2. Run tests to confirm parity
3. Remove old config files only after user confirms

---

# Decision Rules

**Act autonomously:**

- Syncing the environment
- Adding missing dev tools (ruff, pytest) when obviously needed
- Creating missing `uv.lock`
- Adding `.gitignore` entries for `.venv/`

**Ask the user first:**

- Changing Python major versions
- Replacing dependency managers
- Removing existing dependencies
- Changing versions with compatibility risk
- Modifying build configuration (`[build-system]`)

---

# Debugging Checklist

When environment issues occur:

1. `uv tree` — check for dependency conflicts
2. `uv sync` — re-sync the environment
3. Inspect `pyproject.toml` and `uv.lock` for constraint problems

Do not:

- Recreate environments manually
- Use pip to patch issues
- Delete `uv.lock` as a first step

