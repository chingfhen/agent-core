from __future__ import annotations

import argparse
import os
import shutil
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from agent_core import apply


class RetireError(RuntimeError):
    pass


@dataclass(frozen=True)
class RetireResult:
    root: Path
    state_path: Path
    removed: list[str]
    already_missing: list[str]
    exclude_path: Path | None


def _select_project(cwd: Path, here: bool) -> tuple[apply.ProjectPaths, Path]:
    project = apply.resolve_project(cwd, here=here)
    path = apply.state_path(project)
    if apply._lexists(path):
        return project, path

    # A prior plain `apply` stored state in Git metadata. Allow --here to retire it
    # only when the exact selected directory is that worktree root.
    if here and project.git_root is not None and project.root == project.git_root:
        plain = apply.resolve_project(cwd, here=False)
        plain_path = apply.state_path(plain)
        if apply._lexists(plain_path):
            return plain, plain_path
    raise RetireError(
        f"No legacy Agent Core ownership state exists for the selected directory: {project.root}"
    )


def _render_exclusions_without(existing: str, removals: set[str]) -> str:
    lines = existing.splitlines()
    starts = [index for index, line in enumerate(lines) if line == apply.EXCLUDE_START]
    ends = [index for index, line in enumerate(lines) if line == apply.EXCLUDE_END]
    if len(starts) != len(ends) or len(starts) > 1 or (starts and starts[0] >= ends[0]):
        raise RetireError("Git local exclude file contains a malformed agent-core managed block")
    if not starts:
        return existing

    start, end = starts[0], ends[0]
    retained = [line for line in lines[start + 1 : end] if line and line not in removals]
    if retained:
        lines[start : end + 1] = [apply.EXCLUDE_START, *retained, apply.EXCLUDE_END]
    else:
        del lines[start : end + 1]
        if start > 0 and start < len(lines) and lines[start - 1] == "" and lines[start] == "":
            del lines[start]
        if lines and lines[-1] == "":
            while len(lines) > 1 and lines[-1] == "" and lines[-2] == "":
                lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def retire_local(cwd: Path, *, here: bool = False) -> RetireResult:
    project, ownership_path = _select_project(cwd, here)
    records = apply.load_state(ownership_path)
    if not records:
        raise RetireError(f"Legacy ownership state has no managed skill records: {ownership_path}")

    errors: list[str] = []
    existing: list[tuple[str, Path]] = []
    missing: list[str] = []
    for destination, record in records.items():
        target = project.root / destination
        if apply._target_is_tracked(project, destination):
            errors.append(f"{target} is tracked by Git and will not be removed")
            continue
        if not apply._lexists(target):
            missing.append(record["source_skill"])
            continue
        try:
            fingerprint = apply.fingerprint_directory(target)
        except apply.ApplyError as exc:
            errors.append(f"{target} is not an unchanged managed directory: {exc}")
            continue
        if fingerprint != record["fingerprint"]:
            errors.append(f"{target} was locally modified and will not be removed")
            continue
        existing.append((record["source_skill"], target))
    if errors:
        raise RetireError("Retirement refused all changes:\n- " + "\n- ".join(errors))

    exclude_path: Path | None = None
    old_exclusions: str | None = None
    new_exclusions: str | None = None
    if project.git_common_dir is not None:
        exclude_path = project.git_common_dir / "info" / "exclude"
        try:
            old_exclusions = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
        except OSError as exc:
            raise RetireError(f"Could not read Git local exclusions {exclude_path}: {exc}") from exc
        removals = {
            f"/{apply._git_relative_destination(project, destination)}/" for destination in records
        }
        if project.state_in_target:
            removals.add(f"/{apply._git_relative_destination(project, '.agents/.agent-core')}/")
        new_exclusions = _render_exclusions_without(old_exclusions, removals)

    operation = project.root / ".agents" / f".agent-core-retire-{uuid.uuid4().hex}"
    moved: list[tuple[Path, Path]] = []
    exclusions_changed = False
    try:
        operation.mkdir(parents=True)
        for name, target in existing:
            saved = operation / name
            os.replace(target, saved)
            moved.append((target, saved))
        if exclude_path is not None and new_exclusions != old_exclusions:
            apply._atomic_write(exclude_path, new_exclusions or "")
            exclusions_changed = True
        ownership_path.unlink()
    except Exception as exc:
        rollback_errors: list[str] = []
        if exclusions_changed and exclude_path is not None and old_exclusions is not None:
            try:
                apply._atomic_write(exclude_path, old_exclusions)
            except Exception as rollback_exc:
                rollback_errors.append(f"{exclude_path}: {rollback_exc}")
        for target, saved in reversed(moved):
            try:
                if apply._lexists(saved):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(saved, target)
            except Exception as rollback_exc:
                rollback_errors.append(f"{target}: {rollback_exc}")
        if rollback_errors:
            raise RetireError(
                f"Retirement failed ({exc}) and rollback was incomplete:\n- "
                + "\n- ".join(rollback_errors)
            ) from exc
        raise RetireError(f"Retirement failed before completion: {exc}") from exc
    finally:
        shutil.rmtree(operation, ignore_errors=True)

    for parent in (ownership_path.parent, project.root / apply.DESTINATION_BASE, project.root / ".agents"):
        try:
            parent.rmdir()
        except OSError:
            pass
    return RetireResult(project.root, ownership_path, [name for name, _ in existing], missing, exclude_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Retire a legacy project-local Agent Core installation.")
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--here", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = retire_local(Path(args.cwd), here=args.here)
    except (RetireError, apply.ApplyError) as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1
    print(f"Retired legacy Agent Core copies from: {result.root}")
    print("Removed skills: " + (", ".join(result.removed) if result.removed else "none"))
    if result.already_missing:
        print("Already missing managed skills: " + ", ".join(result.already_missing))
    print(f"Removed legacy ownership state: {result.state_path}")
    if result.exclude_path is not None:
        print(f"Cleaned exact legacy exclusions: {result.exclude_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
