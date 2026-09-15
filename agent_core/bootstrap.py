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
        checkout / "agent_core" / "bootstrap.py",
        checkout / "agent_core" / "apply.py",
        checkout / "core-skills.toml",
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


def refresh_and_launch(checkout: Path, project_cwd: Path) -> int:
    _ensure_project_worktree(project_cwd)
    _validate_checkout(checkout)
    _ensure_clean(checkout)

    pull = _git(checkout, "pull", "--ff-only")
    if pull.returncode != 0:
        detail = pull.stderr.strip() or pull.stdout.strip() or f"exit code {pull.returncode}"
        raise AgentCoreError(f"Could not refresh canonical checkout: {detail}")

    _validate_checkout(checkout)
    implementation = checkout / "agent_core" / "apply.py"
    result = subprocess.run(
        [
            sys.executable,
            str(implementation),
            "--checkout",
            str(checkout),
            "--cwd",
            str(project_cwd),
        ],
        check=False,
    )
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-core",
        description="Refresh the private Agent Core checkout and apply configured skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("apply", help="Refresh and safely copy core skills into the current Git project.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "apply":
        parser.error(f"unsupported command: {args.command}")

    try:
        return refresh_and_launch(canonical_checkout(), Path.cwd())
    except AgentCoreError as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
