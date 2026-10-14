---
title: Places Directory Navigator
description: Canonical setup, state, discovery, menu, and portability contract for the standalone Places command.
updated: 2026-10-14
---

# Places Directory Navigator

## Read First

- `places` shows favorites and cached Git repositories, accepts an alias or number, and changes the current Bash or CMD directory.
- `places refresh [EXTRA_ROOT ...]` searches the user's home directory plus any extra roots. Ordinary navigation reads the cache and does not rescan.
- The implementation is the standalone, Python-standard-library-only `scripts/places.py`. It supports Python 3.8 or newer on Linux Bash and Windows CMD.
- Places is independent of `agent-core sync`; copying `places.py` and running its installer is sufficient.

## Setup

From the Agent Core checkout, run:

```bash
python3 "$HOME/.agent-core/scripts/places.py" install
```

Or in Windows CMD, preferring the Windows Python Launcher:

```cmd
py -3 "%USERPROFILE%\.agent-core\scripts\places.py" install
```

If `py` is unavailable but `python` resolves to Python 3.8 or newer, replace `py -3` with `python`. When using a standalone copy instead of the checkout, run the same command against its current location, for example:

```bash
python3 places.py install
```

The installer creates missing state files without replacing existing ones. On Linux it copies the runtime under `~/.local/share/places/`, writes a generated Bash function, and adds one marked source block to `~/.bashrc`. On Windows it copies the runtime under `%USERPROFILE%\.local\share\places\`, installs `%USERPROFILE%\.local\bin\places.cmd`, and updates the user PATH when needed. The user-home destination avoids Microsoft Store Python's package-specific filesystem virtualization. Reinstallation removes the obsolete `%LOCALAPPDATA%\Places\bin` PATH entry created by the original installer. Open a new terminal after installation, or source `~/.bashrc` in the current Bash session.

## Commands

```text
places
places list
places refresh [EXTRA_ROOT ...]
```

- `places` displays the interactive menu. Favorites are selected by stable alias; discovered repositories are selected by their current number. Blank input or `q` cancels without changing directory.
- `places list` emits absolute paths without menu formatting or prompting.
- `places refresh` recursively searches home for working trees identified by a `.git` directory or file. Extra roots extend that scan for the current refresh. The command validates all roots before replacing the cache, skips directory symlinks and common heavy generated directories, and reports inaccessible locations.

A refresh rewrites the complete generated cache. Repositories from an extra root disappear from the next refresh if that root is omitted.

## State Files

Places always uses:

```text
~/.agent-core/places.txt
~/.agent-core/places.generated.txt
```

`places.txt` is human-owned and is never overwritten. Define one favorite per line:

```text
# alias = path
core = ~/.agent-core
shared = /data/team/shared
A = ~/important-folder
```

Aliases are case-insensitive, must start with a letter, and may contain letters, numbers, `_`, or `-`. `q` is reserved for cancelling the menu. Paths must be existing directories and must be absolute or start with `~`. Invalid entries report the file, line number, problem, and a valid example.

Favorite order follows `places.txt`, so it is deterministic and human-controlled. Generated repositories are normalized, deduplicated, and sorted by full path. A favorite wins when the same directory also appears in the generated cache.

`places.generated.txt` is machine-generated. Installation creates it only when absent; only a successful `places refresh` replaces it, using an atomic write. Both state files are ignored by this repository's Git configuration.

## Boundaries

- Direct directory changes require shell integration because a child Python process cannot change its parent shell.
- Initial shell support is Bash on Linux and CMD on Windows. Zsh, Fish, PowerShell, and WSL-to-Windows path translation are not supported.
- Bare Git repositories are not indexed because they are not working directories.
- If Agent Core is not installed, Places still creates `~/.agent-core` for its state. A later Agent Core clone into that exact path requires temporarily moving the state files, cloning, and restoring them.
