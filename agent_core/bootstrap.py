from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


class AgentCoreError(RuntimeError):
    pass


def canonical_checkout() -> Path:
    return Path.home() / ".agent-core"


def _git(checkout: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(checkout), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _git_output(checkout: Path, *args: str) -> str:
    result = _git(checkout, *args)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise AgentCoreError(f"Git command failed for canonical checkout: {detail}")
    return result.stdout.strip()


def _validate_checkout(checkout: Path) -> None:
    if not checkout.is_dir():
        raise AgentCoreError(f"Canonical checkout does not exist: {checkout}")

    root = Path(_git_output(checkout, "rev-parse", "--show-toplevel")).resolve()
    if root != checkout.resolve():
        raise AgentCoreError(f"Canonical path is not the root of its Git worktree: {checkout}")

    required_files = (
        checkout / "pyproject.toml",
        checkout / "personal-skills.toml",
        checkout / "global" / "AGENTS.md",
        checkout / "agent_core" / "bootstrap.py",
        checkout / "agent_core" / "apply.py",
        checkout / "agent_core" / "sync.py",
        checkout / "agent_core" / "retire.py",
        checkout / "agent_core" / "manifest.py",
    )
    required_directories = (checkout / "agent_core", checkout / "skills")
    missing = [str(path) for path in required_files if not path.is_file()]
    missing.extend(str(path) for path in required_directories if not path.is_dir())
    if missing:
        raise AgentCoreError("Canonical checkout is incomplete; missing: " + ", ".join(missing))


def _ensure_project_worktree(project_cwd: Path) -> None:
    result = subprocess.run(
        ["git", "-C", str(project_cwd), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise AgentCoreError(f"Current directory is not in a Git worktree: {detail}")


def _ensure_clean(checkout: Path) -> None:
    status = _git_output(checkout, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise AgentCoreError("Canonical checkout has staged, unstaged, or untracked changes; refusing to pull")


def refresh_and_launch(
    checkout: Path,
    project_cwd: Path,
    *,
    command: str = "sync",
    here: bool = False,
    home: Path | None = None,
) -> int:
    if command in {"apply", "retire-local"}:
        if here:
            if not project_cwd.is_dir():
                raise AgentCoreError(f"Target directory does not exist: {project_cwd}")
        else:
            _ensure_project_worktree(project_cwd)
    _validate_checkout(checkout)
    _ensure_clean(checkout)

    pull = _git(checkout, "pull", "--ff-only")
    if pull.returncode != 0:
        detail = pull.stderr.strip() or pull.stdout.strip() or f"exit code {pull.returncode}"
        raise AgentCoreError(f"Could not refresh canonical checkout: {detail}")

    _validate_checkout(checkout)
    if command == "sync":
        module = "agent_core.sync"
        arguments = ["--checkout", str(checkout), "--home", str(home or Path.home())]
    elif command == "apply":
        module = "agent_core.apply"
        arguments = ["--checkout", str(checkout), "--cwd", str(project_cwd)]
        if here:
            arguments.append("--here")
    elif command == "retire-local":
        module = "agent_core.retire"
        arguments = ["--cwd", str(project_cwd)]
        if here:
            arguments.append("--here")
    else:
        raise AgentCoreError(f"Unsupported internal command: {command}")

    result = subprocess.run(
        [sys.executable, "-m", module, *arguments],
        cwd=checkout,
        check=False,
    )
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-core",
        description="Refresh the private Agent Core checkout and publish personal agent resources.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sync", help="Publish personal skills and global guidance for all supported harnesses.")
    apply_parser = subparsers.add_parser(
        "apply", help="Deprecated: copy configured skills into one project or directory."
    )
    apply_parser.add_argument(
        "--here",
        action="store_true",
        help="Use the current directory exactly, whether or not it is a Git worktree.",
    )
    retire_parser = subparsers.add_parser(
        "retire-local", help="Safely remove a legacy project-local Agent Core installation."
    )
    retire_parser.add_argument(
        "--here",
        action="store_true",
        help="Use the current directory exactly; also recognizes prior plain-apply state at a Git root.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "apply":
        print(
            "agent-core: warning: 'apply' is deprecated; use 'agent-core sync' for personal skills",
            file=sys.stderr,
        )
    try:
        return refresh_and_launch(
            canonical_checkout(),
            Path.cwd(),
            command=args.command,
            here=getattr(args, "here", False),
        )
    except AgentCoreError as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
