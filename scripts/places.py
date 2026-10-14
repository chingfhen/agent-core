#!/usr/bin/env python3
"""Install and run the dependency-free Places directory navigator."""

from __future__ import annotations

import argparse
import ctypes
import os
import re
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence, TextIO, Tuple

MINIMUM_PYTHON = (3, 8)
MANUAL_FILENAME = "places.txt"
GENERATED_FILENAME = "places.generated.txt"
ALIAS_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
SKIPPED_DIRECTORY_NAMES = {
    ".cache",
    ".git",
    ".nox",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}
BASH_BLOCK_BEGIN = "# >>> places shell integration >>>"
BASH_BLOCK_END = "# <<< places shell integration <<<"


class PlacesError(RuntimeError):
    pass


def state_directory(home: Optional[Path] = None) -> Path:
    return Path(home or Path.home()).expanduser().resolve() / ".agent-core"


def state_paths(home: Optional[Path] = None) -> Tuple[Path, Path]:
    directory = state_directory(home)
    return directory / MANUAL_FILENAME, directory / GENERATED_FILENAME


def _create_if_missing(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="") as stream:
            stream.write(content)
    except FileExistsError:
        if not path.is_file():
            raise PlacesError("Expected a regular file but found another object: {}".format(path))


def ensure_state_files(home: Optional[Path] = None) -> Tuple[Path, Path]:
    manual, generated = state_paths(home)
    _create_if_missing(
        manual,
        "# Add one favorite per line as: alias = path\n"
        "# Aliases start with a letter and may contain letters, numbers, _ or -.\n"
        "# Example: core = ~/.agent-core\n",
    )
    _create_if_missing(generated)
    return manual, generated


def _expand_manual_path(raw: str, source: Path, line_number: int) -> Path:
    expanded = Path(raw).expanduser()
    if not expanded.is_absolute():
        raise PlacesError(
            "{}:{}: path must be absolute or start with '~'. "
            "Example: core = ~/.agent-core".format(source, line_number)
        )
    resolved = expanded.resolve()
    if not resolved.is_dir():
        raise PlacesError(
            "{}:{}: path is not an existing directory: {}. "
            "Use: alias = /absolute/path (or alias = ~/path)".format(
                source, line_number, raw
            )
        )
    return resolved


def load_favorites(path: Path) -> List[Tuple[str, Path]]:
    favorites: List[Tuple[str, Path]] = []
    aliases = {}
    destinations = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise PlacesError("{} must be UTF-8 text: {}".format(path, exc))

    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        alias, separator, raw_path = line.partition("=")
        alias = alias.strip()
        raw_path = raw_path.strip()
        if not separator or not alias or not raw_path:
            raise PlacesError(
                "{}:{}: expected 'alias = path'. Example: core = ~/.agent-core".format(
                    path, line_number
                )
            )
        if not ALIAS_PATTERN.fullmatch(alias):
            raise PlacesError(
                "{}:{}: invalid alias {!r}; aliases must start with a letter and contain "
                "only letters, numbers, '_' or '-'. Example: work = ~/work".format(
                    path, line_number, alias
                )
            )
        normalized_alias = alias.casefold()
        if normalized_alias == "q":
            raise PlacesError(
                "{}:{}: alias 'q' is reserved for cancelling the menu; choose another alias".format(
                    path, line_number
                )
            )
        if normalized_alias in aliases:
            raise PlacesError(
                "{}:{}: duplicate alias {!r}; aliases are case-insensitive and {!r} was "
                "already defined on line {}".format(
                    path,
                    line_number,
                    alias,
                    aliases[normalized_alias][0],
                    aliases[normalized_alias][1],
                )
            )
        destination = _expand_manual_path(raw_path, path, line_number)
        destination_key = _path_key(destination)
        if destination_key in destinations:
            prior_alias, prior_line = destinations[destination_key]
            raise PlacesError(
                "{}:{}: directory is already assigned to alias {!r} on line {}".format(
                    path, line_number, prior_alias, prior_line
                )
            )
        aliases[normalized_alias] = (alias, line_number)
        destinations[destination_key] = (alias, line_number)
        favorites.append((alias, destination))
    return favorites


def load_generated(path: Path) -> List[Path]:
    repositories: List[Path] = []
    seen = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise PlacesError("{} must be UTF-8 text: {}".format(path, exc))
    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue
        candidate = Path(line).expanduser()
        if not candidate.is_absolute():
            raise PlacesError(
                "{}:{}: generated path is not absolute; run 'places refresh' to rebuild the file".format(
                    path, line_number
                )
            )
        resolved = candidate.resolve()
        if not resolved.is_dir():
            continue
        key = _path_key(resolved)
        if key not in seen:
            seen.add(key)
            repositories.append(resolved)
    return sorted(repositories, key=_sort_key)


def _path_key(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))


def _sort_key(path: Path) -> Tuple[str, str]:
    rendered = str(path)
    return rendered.casefold(), rendered


def load_places(home: Optional[Path] = None) -> Tuple[List[Tuple[str, Path]], List[Path]]:
    manual_path, generated_path = ensure_state_files(home)
    favorites = load_favorites(manual_path)
    favorite_paths = {_path_key(path) for _, path in favorites}
    repositories = [
        path for path in load_generated(generated_path) if _path_key(path) not in favorite_paths
    ]
    return favorites, repositories


def _contains(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _scan_roots(home: Path, extra_roots: Sequence[str]) -> List[Path]:
    candidates = [home]
    for raw in extra_roots:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        candidates.append(candidate)

    resolved: List[Path] = []
    for candidate in candidates:
        root = candidate.resolve()
        if not root.is_dir():
            raise PlacesError("Scan root is not an existing directory: {}".format(candidate))
        if root not in resolved:
            resolved.append(root)

    minimal: List[Path] = []
    for candidate in sorted(resolved, key=lambda path: (len(path.parts), _sort_key(path))):
        if not any(_contains(parent, candidate) for parent in minimal):
            minimal.append(candidate)
    return sorted(minimal, key=_sort_key)


def discover_repositories(roots: Sequence[Path]) -> Tuple[List[Path], List[str], int]:
    repositories = {}
    errors: List[str] = []
    visited = 0

    def record_error(error: OSError) -> None:
        errors.append("{}: {}".format(error.filename or "unknown path", error.strerror or error))

    for root in roots:
        for current, directory_names, file_names in os.walk(
            str(root), topdown=True, onerror=record_error, followlinks=False
        ):
            visited += 1
            directory_names[:] = sorted(
                [name for name in directory_names if name not in SKIPPED_DIRECTORY_NAMES],
                key=lambda value: (value.casefold(), value),
            )
            if ".git" in file_names or (Path(current) / ".git").is_dir():
                repository = Path(current).resolve()
                if "\n" not in str(repository) and "\r" not in str(repository):
                    repositories[_path_key(repository)] = repository

    return sorted(repositories.values(), key=_sort_key), errors, visited


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = path.stat().st_mode & 0o7777 if path.exists() else None
    descriptor, temporary_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if existing_mode is not None:
            os.chmod(str(temporary), existing_mode)
        os.replace(str(temporary), str(path))
    except Exception:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def refresh(extra_roots: Sequence[str], home: Optional[Path] = None) -> Tuple[List[Path], List[str]]:
    resolved_home = Path(home or Path.home()).expanduser().resolve()
    _, generated_path = ensure_state_files(resolved_home)
    roots = _scan_roots(resolved_home, extra_roots)
    repositories, errors, visited = discover_repositories(roots)
    if visited == 0:
        raise PlacesError("No directories could be read; the existing generated file was preserved")
    content = "".join("{}\n".format(path) for path in repositories)
    _atomic_write(generated_path, content)
    return repositories, errors


def display_path(path: Path, home: Path) -> str:
    path_text = str(path)
    home_text = str(home)
    try:
        common = os.path.commonpath([path_text, home_text])
    except ValueError:
        return path_text
    if os.path.normcase(common) != os.path.normcase(home_text):
        return path_text
    relative = os.path.relpath(path_text, home_text)
    if relative == ".":
        return "~"
    return "~{}{}".format(os.sep, relative)


def render_menu(
    favorites: Sequence[Tuple[str, Path]], repositories: Sequence[Path], home: Path
) -> str:
    lines = ["Places", ""]
    if favorites:
        alias_width = max(len(alias) for alias, _ in favorites)
        lines.append("Favorites ({})".format(len(favorites)))
        for alias, path in favorites:
            lines.append("  [{:<{}}]  {}".format(alias, alias_width, display_path(path, home)))
    else:
        lines.extend(
            ["Favorites (0)", "  Add entries to ~/.agent-core/places.txt as: alias = path"]
        )

    lines.append("")
    if repositories:
        number_width = len(str(len(repositories)))
        name_width = max(len(path.name or str(path)) for path in repositories)
        lines.append("Git repositories ({})".format(len(repositories)))
        for number, path in enumerate(repositories, 1):
            name = path.name or str(path)
            lines.append(
                "  [{:>{}}]  {:<{}}  {}".format(
                    number,
                    number_width,
                    name,
                    name_width,
                    display_path(path, home),
                )
            )
    else:
        lines.extend(["Git repositories (0)", "  Run 'places refresh' to discover repositories."])
    return "\n".join(lines)


def list_paths(home: Optional[Path] = None) -> List[Path]:
    resolved_home = Path(home or Path.home()).expanduser().resolve()
    favorites, repositories = load_places(resolved_home)
    return [path for _, path in favorites] + repositories


def choose(
    home: Optional[Path] = None,
    input_stream: TextIO = sys.stdin,
    menu_stream: TextIO = sys.stderr,
    selection_file: Optional[Path] = None,
) -> Optional[Path]:
    resolved_home = Path(home or Path.home()).expanduser().resolve()
    favorites, repositories = load_places(resolved_home)
    if not favorites and not repositories:
        raise PlacesError(
            "No places are available. Run 'places refresh' or add "
            "'alias = path' entries to ~/.agent-core/places.txt"
        )

    print(render_menu(favorites, repositories, resolved_home), file=menu_stream)
    aliases = {alias.casefold(): path for alias, path in favorites}
    while True:
        print("", file=menu_stream)
        print("Select an alias or number (q to cancel): ", end="", file=menu_stream, flush=True)
        response = input_stream.readline()
        if not response:
            return None
        selection = response.strip()
        if not selection or selection.casefold() == "q":
            return None
        destination = aliases.get(selection.casefold())
        if destination is None and selection.isdigit():
            number = int(selection)
            if 1 <= number <= len(repositories):
                destination = repositories[number - 1]
        if destination is None:
            print(
                "Invalid selection {!r}. Enter a shown alias, a repository number, or q.".format(
                    selection
                ),
                file=menu_stream,
            )
            continue
        if selection_file is None:
            print(destination)
        else:
            _atomic_write(selection_file, str(destination) + "\n")
        return destination


def _shell_quote(value: Path) -> str:
    return shlex.quote(str(value))


def _render_bash_function(python_executable: Path, installed_script: Path) -> str:
    command = "{} {}".format(_shell_quote(python_executable), _shell_quote(installed_script))
    return """# Generated by places.py; reinstall instead of editing this file.
places() {{
    if [ "$#" -eq 0 ]; then
        local _places_destination
        _places_destination="$({command} choose)" || return $?
        if [ -n "$_places_destination" ]; then
            builtin cd -- "$_places_destination"
        fi
    else
        {command} "$@"
    fi
}}
""".format(command=command)


def _install_bash_source(bashrc: Path, function_file: Path) -> bool:
    source_line = "[ -f {0} ] && . {0}".format(_shell_quote(function_file))
    block = "{}\n{}\n{}\n".format(BASH_BLOCK_BEGIN, source_line, BASH_BLOCK_END)
    if bashrc.exists():
        if not bashrc.is_file():
            raise PlacesError("Expected a regular Bash configuration file: {}".format(bashrc))
        content = bashrc.read_text(encoding="utf-8")
    else:
        content = ""
    begin_count = content.count(BASH_BLOCK_BEGIN)
    end_count = content.count(BASH_BLOCK_END)
    if begin_count != end_count or begin_count > 1:
        raise PlacesError(
            "Cannot safely update {}; remove the malformed Places marker block and reinstall".format(
                bashrc
            )
        )
    if begin_count == 1:
        start = content.index(BASH_BLOCK_BEGIN)
        end = content.index(BASH_BLOCK_END, start) + len(BASH_BLOCK_END)
        if content[start:end].strip() == block.strip():
            return False
        raise PlacesError(
            "Cannot safely replace the existing Places block in {}; remove it and reinstall".format(
                bashrc
            )
        )

    separator = "" if not content or content.endswith("\n") else "\n"
    with bashrc.open("a", encoding="utf-8", newline="") as stream:
        stream.write(separator + ("\n" if content else "") + block)
    return True


def _batch_escape(value: Path) -> str:
    return str(value).replace("%", "%%")


def _render_cmd_launcher(python_executable: Path, installed_script: Path, runtime: Path) -> str:
    python = _batch_escape(python_executable)
    script = _batch_escape(installed_script)
    selection = _batch_escape(runtime / "selection-%RANDOM%-%RANDOM%.txt")
    return """@echo off
if not "%~1"=="" goto run_command
setlocal
set "PLACES_SELECTION={selection}"
if exist "%PLACES_SELECTION%" del /q "%PLACES_SELECTION%" >nul 2>nul
"{python}" "{script}" choose --selection-file "%PLACES_SELECTION%"
if errorlevel 1 goto choose_failed
if not exist "%PLACES_SELECTION%" endlocal & exit /b 0
set /p "PLACES_DESTINATION="<"%PLACES_SELECTION%"
del /q "%PLACES_SELECTION%" >nul 2>nul
endlocal & cd /d "%PLACES_DESTINATION%"
exit /b %errorlevel%

:choose_failed
set "PLACES_STATUS=%errorlevel%"
if exist "%PLACES_SELECTION%" del /q "%PLACES_SELECTION%" >nul 2>nul
endlocal & exit /b %PLACES_STATUS%

:run_command
"{python}" "{script}" %*
exit /b %errorlevel%
""".format(selection=selection, python=python, script=script)


def _normalized_path_entry(value: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.expandvars(value.strip().strip('"'))))


def add_to_windows_user_path(bin_directory: Path) -> bool:
    import winreg

    key_path = r"Environment"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        try:
            current, value_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current, value_type = "", winreg.REG_EXPAND_SZ
        entries = [entry for entry in current.split(";") if entry]
        wanted = _normalized_path_entry(str(bin_directory))
        if any(_normalized_path_entry(entry) == wanted for entry in entries):
            return False
        updated = ";".join([str(bin_directory)] + entries)
        winreg.SetValueEx(key, "Path", 0, value_type, updated)

    try:
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, ctypes.byref(result)
        )
    except (AttributeError, OSError):
        pass
    return True


def _copy_runtime(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination.resolve():
        temporary = destination.with_name(destination.name + ".new")
        shutil.copy2(str(source), str(temporary))
        os.replace(str(temporary), str(destination))


def install(
    source: Optional[Path] = None,
    home: Optional[Path] = None,
    platform: Optional[str] = None,
    python_executable: Optional[Path] = None,
    local_app_data: Optional[Path] = None,
) -> dict:
    if sys.version_info < MINIMUM_PYTHON:
        raise PlacesError(
            "Places requires Python {}.{} or newer; found {}.{}".format(
                MINIMUM_PYTHON[0],
                MINIMUM_PYTHON[1],
                sys.version_info.major,
                sys.version_info.minor,
            )
        )
    resolved_home = Path(home or Path.home()).expanduser().resolve()
    source = Path(source or __file__).resolve()
    if not source.is_file():
        raise PlacesError("Places source file does not exist: {}".format(source))
    python_executable = Path(python_executable or sys.executable).resolve()
    platform = platform or ("windows" if os.name == "nt" else "linux")
    if platform not in {"linux", "windows"}:
        raise PlacesError(
            "Unsupported platform {!r}; Places currently supports Linux and Windows".format(
                platform
            )
        )
    manual, generated = ensure_state_files(resolved_home)

    if platform == "windows":
        local = Path(
            local_app_data
            or os.environ.get("LOCALAPPDATA", resolved_home / "AppData" / "Local")
        )
        runtime = local / "Places"
        installed_script = runtime / "places.py"
        bin_directory = runtime / "bin"
        launcher = bin_directory / "places.cmd"
        _copy_runtime(source, installed_script)
        bin_directory.mkdir(parents=True, exist_ok=True)
        _atomic_write(
            launcher,
            _render_cmd_launcher(python_executable, installed_script, runtime),
        )
        path_changed = add_to_windows_user_path(bin_directory)
        return {
            "platform": platform,
            "runtime": runtime,
            "launcher": launcher,
            "path_changed": path_changed,
            "manual": manual,
            "generated": generated,
        }

    runtime = resolved_home / ".local" / "share" / "places"
    installed_script = runtime / "places.py"
    function_file = runtime / "places.bash"
    _copy_runtime(source, installed_script)
    _atomic_write(function_file, _render_bash_function(python_executable, installed_script))
    bashrc = resolved_home / ".bashrc"
    bashrc_changed = _install_bash_source(bashrc, function_file)
    return {
        "platform": platform,
        "runtime": runtime,
        "function": function_file,
        "bashrc": bashrc,
        "bashrc_changed": bashrc_changed,
        "manual": manual,
        "generated": generated,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="places",
        description="Navigate to favorite directories and cached Git repositories.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("install", help="Install the Bash or CMD shell integration.")
    subparsers.add_parser("list", help="Print all available paths without prompting.")
    refresh_parser = subparsers.add_parser(
        "refresh", help="Rescan home plus optional extra roots for Git repositories."
    )
    refresh_parser.add_argument("roots", nargs="*", help="Additional directory trees to scan.")
    choose_parser = subparsers.add_parser(
        "choose", help="Internal command used by the installed shell integration."
    )
    choose_parser.add_argument("--selection-file", type=Path, help=argparse.SUPPRESS)
    return parser


def _print_install_result(result: dict) -> None:
    print("Installed Places runtime: {}".format(result["runtime"]))
    print("Manual favorites: {}".format(result["manual"]))
    print("Generated repositories: {}".format(result["generated"]))
    if result["platform"] == "windows":
        print("Installed CMD launcher: {}".format(result["launcher"]))
        if result["path_changed"]:
            print("Added the launcher directory to your user PATH.")
        print("Open a new CMD terminal, then run: places refresh")
    else:
        print("Installed Bash integration: {}".format(result["function"]))
        print("Open a new Bash terminal or run: source {}".format(result["bashrc"]))
        print("Then run: places refresh")


def main(argv: Optional[Sequence[str]] = None) -> int:
    if sys.version_info < MINIMUM_PYTHON:
        print(
            "places: error: Python {}.{} or newer is required".format(*MINIMUM_PYTHON),
            file=sys.stderr,
        )
        return 1
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "choose"
    try:
        if command == "install":
            _print_install_result(install())
        elif command == "refresh":
            repositories, errors = refresh(args.roots)
            print(
                "places refresh: saved {} Git repositories to {}".format(
                    len(repositories), state_paths()[1]
                )
            )
            if errors:
                print(
                    "places refresh: warning: skipped {} unreadable locations".format(len(errors)),
                    file=sys.stderr,
                )
                for detail in errors[:5]:
                    print("  {}".format(detail), file=sys.stderr)
                if len(errors) > 5:
                    print("  ... and {} more".format(len(errors) - 5), file=sys.stderr)
        elif command == "list":
            for path in list_paths():
                print(path)
        elif command == "choose":
            choose(selection_file=getattr(args, "selection_file", None))
        else:
            parser.error("unsupported command")
    except (PlacesError, OSError) as exc:
        print("places: error: {}".format(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
