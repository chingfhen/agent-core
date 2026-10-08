"""Install the dependency-free Agent Core command shim on Windows."""

import ctypes
import os
import sys
from pathlib import Path

MINIMUM_PYTHON = (3, 10)


def render_shim(python_executable, checkout):
    bootstrap = checkout / "agent_core" / "bootstrap.py"
    return '@echo off\r\n"{}" "{}" %*\r\n'.format(python_executable, bootstrap)


def _normalized_path_entry(value):
    return os.path.normcase(os.path.normpath(os.path.expandvars(value.strip().strip('"'))))


def add_to_user_path(bin_directory):
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
        updated = ";".join([str(bin_directory), *entries])
        winreg.SetValueEx(key, "Path", 0, value_type, updated)

    try:
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result),
        )
    except (AttributeError, OSError):
        pass
    return True


def install(checkout=None, home=None, local_app_data=None, python_executable=None):
    if sys.version_info < MINIMUM_PYTHON:
        raise RuntimeError(
            "Agent Core requires Python {}.{} or newer; found {}.{}.".format(
                *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
            )
        )
    home = Path(home or Path.home()).resolve()
    checkout = Path(checkout or Path(__file__).resolve().parents[1]).resolve()
    expected = (home / ".agent-core").resolve()
    if checkout != expected:
        raise RuntimeError(
            "This installer must run from the fixed canonical checkout: {} (found {})".format(
                expected, checkout
            )
        )
    if os.name != "nt":
        raise RuntimeError("install-agent-core.cmd is the supported installer for Windows")

    local_app_data = Path(local_app_data or os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
    bin_directory = local_app_data / "AgentCore" / "bin"
    bin_directory.mkdir(parents=True, exist_ok=True)
    shim = bin_directory / "agent-core.cmd"
    content = render_shim(python_executable or sys.executable, checkout)
    shim.write_text(content, encoding="utf-8", newline="")
    path_changed = add_to_user_path(bin_directory)
    return shim, bin_directory, path_changed


def main():
    try:
        shim, bin_directory, path_changed = install()
    except Exception as exc:
        print("agent-core installer: error: {}".format(exc), file=sys.stderr)
        return 1
    print("Installed Agent Core command shim: {}".format(shim))
    print("User command directory: {}".format(bin_directory))
    if path_changed:
        print("Added the command directory to the user PATH without setx.")
        print("Open a new terminal, then run: agent-core sync")
    else:
        print("The command directory is already on the user PATH.")
        print("Run: agent-core sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
