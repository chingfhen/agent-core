from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tomllib
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

STATE_VERSION = 1
STATE_DIRECTORY = "agent-core"
STATE_FILENAME = "ownership.json"
DESTINATION_BASE = Path(".agents/skills")
EXCLUDE_START = "# >>> agent-core managed skills >>>"
EXCLUDE_END = "# <<< agent-core managed skills <<<"
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HEX_SHA = re.compile(r"^[0-9a-f]{40,64}$")
HEX_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")
RECORD_FIELDS = ("destination", "source_skill", "source_commit", "fingerprint")


class ApplyError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceSkill:
    name: str
    path: Path
    fingerprint: str


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    git_root: Path | None
    git_dir: Path | None
    git_common_dir: Path | None
    state_in_target: bool


@dataclass(frozen=True)
class TargetPlan:
    source: SourceSkill
    destination: str
    target: Path
    classification: str


def _run_git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _git_output(path: Path, *args: str, context: str) -> str:
    result = _run_git(path, *args)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise ApplyError(f"{context}: {detail}")
    return result.stdout.strip()


def _safe_skill_name(name: object) -> bool:
    return isinstance(name, str) and bool(SAFE_NAME.fullmatch(name)) and name not in {".", ".."}


def _lexists(path: Path) -> bool:
    try:
        path.stat(follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _is_reparse(metadata: os.stat_result) -> bool:
    attributes = getattr(metadata, "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _entry_kind(path: Path) -> str:
    try:
        metadata = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise ApplyError(f"Could not inspect filesystem entry {path}: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode) or _is_reparse(metadata):
        return "unsupported link or reparse point"
    if stat.S_ISDIR(metadata.st_mode):
        return "directory"
    if stat.S_ISREG(metadata.st_mode):
        return "file"
    return "unsupported filesystem entry"


def fingerprint_directory(root: Path) -> str:
    if not _lexists(root) or _entry_kind(root) != "directory":
        raise ApplyError(f"Expected a real directory suitable for copying: {root}")

    digest = hashlib.sha256(b"agent-core-directory-v1\0")

    def add_field(value: bytes) -> None:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    def add_permissions(path: Path) -> None:
        try:
            permissions = stat.S_IMODE(path.stat(follow_symlinks=False).st_mode)
        except OSError as exc:
            raise ApplyError(f"Could not inspect filesystem permissions for {path}: {exc}") from exc
        add_field(permissions.to_bytes(4, "big"))

    def visit(directory: Path, relative: Path) -> None:
        try:
            children = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            raise ApplyError(f"Could not read directory {directory}: {exc}") from exc
        for child in children:
            child_relative = relative / child.name
            relative_bytes = child_relative.as_posix().encode("utf-8")
            kind = _entry_kind(child)
            if kind == "directory":
                add_field(b"D")
                add_field(relative_bytes)
                add_permissions(child)
                visit(child, child_relative)
            elif kind == "file":
                add_field(b"F")
                add_field(relative_bytes)
                add_permissions(child)
                try:
                    with child.open("rb") as stream:
                        while chunk := stream.read(1024 * 1024):
                            add_field(chunk)
                except OSError as exc:
                    raise ApplyError(f"Could not read file {child}: {exc}") from exc
            else:
                raise ApplyError(f"Unsupported filesystem entry in skill source or copy: {child} ({kind})")

    add_permissions(root)
    visit(root, Path())
    return digest.hexdigest()


def _tracked_paths(checkout: Path, pathspec: str) -> set[str]:
    result = _run_git(checkout, "ls-files", "-z", "--cached", "--", pathspec)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise ApplyError(f"Could not inspect canonical tracked files for {pathspec}: {detail}")
    return {path for path in result.stdout.split("\0") if path}


def _validate_committed_source(checkout: Path, source: Path) -> None:
    relative_source = source.relative_to(checkout).as_posix()
    tracked = _tracked_paths(checkout, relative_source)
    actual = {
        path.relative_to(checkout).as_posix()
        for path in source.rglob("*")
        if _entry_kind(path) == "file"
    }
    if actual != tracked:
        untracked = sorted(actual - tracked)
        missing = sorted(tracked - actual)
        details: list[str] = []
        if untracked:
            details.append("not tracked: " + ", ".join(untracked))
        if missing:
            details.append("tracked but missing: " + ", ".join(missing))
        raise ApplyError(
            f"Configured skill source must match committed Git files ({relative_source}): "
            + "; ".join(details)
        )


def load_sources(checkout: Path) -> tuple[list[SourceSkill], str]:
    config_path = checkout / "core-skills.toml"
    try:
        with config_path.open("rb") as stream:
            config = tomllib.load(stream)
    except FileNotFoundError as exc:
        raise ApplyError(f"Core skill configuration is missing: {config_path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ApplyError(f"Core skill configuration is invalid: {exc}") from exc

    if "core-skills.toml" not in _tracked_paths(checkout, "core-skills.toml"):
        raise ApplyError("core-skills.toml must be tracked by the canonical Git checkout")

    names = config.get("skills") if isinstance(config, dict) else None
    if not isinstance(names, list):
        raise ApplyError("core-skills.toml must define a 'skills' array")
    if any(not _safe_skill_name(name) for name in names):
        raise ApplyError("core-skills.toml contains an unsafe or non-string skill name")
    normalized_names = [name.casefold() for name in names]
    if len(set(normalized_names)) != len(normalized_names):
        raise ApplyError("core-skills.toml contains duplicate skill names")

    commit = _git_output(checkout, "rev-parse", "HEAD", context="Could not identify canonical source commit")
    if not HEX_SHA.fullmatch(commit):
        raise ApplyError(f"Canonical source commit is not a full Git object ID: {commit}")

    sources: list[SourceSkill] = []
    for name in names:
        source = checkout / "skills" / name
        if not _lexists(source) or _entry_kind(source) != "directory":
            raise ApplyError(f"Configured skill source is not a real directory: {source}")
        skill_file = source / "SKILL.md"
        if not _lexists(skill_file) or _entry_kind(skill_file) != "file":
            raise ApplyError(f"Configured skill is missing a regular SKILL.md: {skill_file}")
        fingerprint = fingerprint_directory(source)
        _validate_committed_source(checkout, source)
        sources.append(SourceSkill(name=name, path=source, fingerprint=fingerprint))
    return sources, commit


def resolve_project(cwd: Path, *, here: bool = False) -> ProjectPaths:
    target = cwd.resolve()
    if not target.is_dir():
        raise ApplyError(f"Target directory does not exist: {target}")

    root_result = _run_git(target, "rev-parse", "--show-toplevel")
    if root_result.returncode != 0:
        if here:
            return ProjectPaths(target, None, None, None, True)
        detail = root_result.stderr.strip() or root_result.stdout.strip() or f"exit code {root_result.returncode}"
        raise ApplyError(f"Current directory is not in a Git worktree: {detail}")

    git_root = Path(root_result.stdout.strip()).resolve()
    git_dir_text = _git_output(target, "rev-parse", "--absolute-git-dir", context="Could not resolve Git metadata directory")
    common_text = _git_output(
        target,
        "rev-parse",
        "--path-format=absolute",
        "--git-common-dir",
        context="Could not resolve common Git metadata directory",
    )
    root = target if here else git_root
    return ProjectPaths(
        root=root,
        git_root=git_root,
        git_dir=Path(git_dir_text).resolve(),
        git_common_dir=Path(common_text).resolve(),
        state_in_target=here,
    )


def state_path(project: ProjectPaths) -> Path:
    if project.state_in_target:
        return project.root / ".agents" / ".agent-core" / STATE_FILENAME
    if project.git_dir is None:
        raise ApplyError("Git ownership state is unavailable for this target")
    return project.git_dir / STATE_DIRECTORY / STATE_FILENAME


def _validate_record(key: object, record: object) -> dict[str, str]:
    if not isinstance(key, str) or not isinstance(record, dict):
        raise ApplyError("Ownership state contains an invalid destination record")
    if set(record) != set(RECORD_FIELDS) or any(not isinstance(record[field], str) for field in RECORD_FIELDS):
        raise ApplyError(f"Ownership record for {key!r} has an invalid shape")
    source_skill = record["source_skill"]
    expected_destination = (DESTINATION_BASE / source_skill).as_posix()
    if (
        not _safe_skill_name(source_skill)
        or key != record["destination"]
        or key != expected_destination
        or not HEX_SHA.fullmatch(record["source_commit"])
        or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
    ):
        raise ApplyError(f"Ownership record for {key!r} is invalid")
    return {field: record[field] for field in RECORD_FIELDS}


def load_state(path: Path) -> dict[str, dict[str, str]]:
    if not _lexists(path):
        return {}
    if _entry_kind(path) != "file":
        raise ApplyError(f"Ownership state is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ApplyError(f"Ownership state is malformed: {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("version") != STATE_VERSION:
        raise ApplyError(f"Ownership state has an unsupported or missing version: {path}")
    destinations = payload.get("destinations")
    if set(payload) != {"version", "destinations"} or not isinstance(destinations, dict):
        raise ApplyError(f"Ownership state has an invalid shape: {path}")
    return {key: _validate_record(key, record) for key, record in destinations.items()}


def _ensure_real_target_parents(project_root: Path) -> None:
    for path in (project_root / ".agents", project_root / DESTINATION_BASE):
        if not _lexists(path):
            continue
        if _entry_kind(path) != "directory":
            raise ApplyError(f"Skill destination parent is not a real directory: {path}")


def _git_relative_destination(project: ProjectPaths, destination: str) -> str:
    if project.git_root is None:
        return destination
    prefix = project.root.relative_to(project.git_root)
    return (prefix / destination).as_posix()


def _target_is_tracked(project: ProjectPaths, destination: str) -> bool:
    if project.git_root is None:
        return False
    git_destination = _git_relative_destination(project, destination)
    result = _run_git(project.git_root, "ls-files", "-z", "--", git_destination)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise ApplyError(f"Could not inspect tracked project paths for {destination}: {detail}")
    return bool(result.stdout)


def build_plan(
    project: ProjectPaths,
    sources: list[SourceSkill],
    records: dict[str, dict[str, str]],
) -> list[TargetPlan]:
    _ensure_real_target_parents(project.root)
    plans: list[TargetPlan] = []
    errors: list[str] = []
    for source in sources:
        destination = (DESTINATION_BASE / source.name).as_posix()
        target = project.root / destination
        record = records.get(destination)

        if _target_is_tracked(project, destination):
            errors.append(f"{destination} is tracked by project Git")
            continue

        exists = _lexists(target)
        if record is None:
            if exists:
                errors.append(f"{destination} exists but is not provably owned by agent-core")
            else:
                plans.append(TargetPlan(source, destination, target, "absent"))
            continue

        if record["source_skill"] != source.name:
            errors.append(f"{destination} has an ownership record for a different source skill")
            continue
        if not exists:
            plans.append(TargetPlan(source, destination, target, "owned-missing"))
            continue
        try:
            installed_fingerprint = fingerprint_directory(target)
        except ApplyError as exc:
            errors.append(f"{destination} is not an unchanged owned directory: {exc}")
            continue
        if installed_fingerprint != record["fingerprint"]:
            errors.append(f"{destination} was locally modified")
            continue
        plans.append(TargetPlan(source, destination, target, "owned-unchanged"))

    if errors:
        raise ApplyError("Preflight refused project changes:\n- " + "\n- ".join(errors))
    return plans


def verify_plan_still_safe(
    project: ProjectPaths,
    plans: list[TargetPlan],
    records: dict[str, dict[str, str]],
) -> None:
    _ensure_real_target_parents(project.root)
    errors: list[str] = []
    for plan in plans:
        if _target_is_tracked(project, plan.destination):
            errors.append(f"{plan.destination} became tracked by project Git")
            continue
        exists = _lexists(plan.target)
        if plan.classification in {"absent", "owned-missing"}:
            if exists:
                errors.append(f"{plan.destination} appeared after preflight")
            continue
        if not exists:
            errors.append(f"{plan.destination} disappeared after preflight")
            continue
        try:
            fingerprint = fingerprint_directory(plan.target)
        except ApplyError as exc:
            errors.append(f"{plan.destination} changed after preflight: {exc}")
            continue
        if fingerprint != records[plan.destination]["fingerprint"]:
            errors.append(f"{plan.destination} changed after preflight")
    if errors:
        raise ApplyError("Final pre-replacement check refused project changes:\n- " + "\n- ".join(errors))


def _render_state(records: dict[str, dict[str, str]]) -> str:
    payload = {"version": STATE_VERSION, "destinations": dict(sorted(records.items()))}
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def _render_exclusions(existing: str, destinations: list[str]) -> str:
    lines = existing.splitlines()
    starts = [index for index, line in enumerate(lines) if line == EXCLUDE_START]
    ends = [index for index, line in enumerate(lines) if line == EXCLUDE_END]
    if len(starts) != len(ends) or len(starts) > 1 or (starts and starts[0] >= ends[0]):
        raise ApplyError("Git local exclude file contains a malformed agent-core managed block")

    managed = {f"/{destination}/" for destination in destinations}
    if starts:
        managed.update(line for line in lines[starts[0] + 1 : ends[0]] if line)
    block = [EXCLUDE_START, *sorted(managed), EXCLUDE_END]
    if starts:
        lines[starts[0] : ends[0] + 1] = block
    else:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(block)
    return "\n".join(lines) + "\n"


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.agent-core-{uuid.uuid4().hex}.tmp"
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if _lexists(temporary):
            temporary.unlink()


def _prepare_exclusions(project: ProjectPaths, records: dict[str, dict[str, str]]) -> None:
    if project.git_common_dir is None:
        return
    exclude_path = project.git_common_dir / "info" / "exclude"
    try:
        existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    except OSError as exc:
        raise ApplyError(f"Could not read Git local exclusions: {exclude_path}: {exc}") from exc
    destinations = [_git_relative_destination(project, destination) for destination in records]
    if project.state_in_target:
        destinations.append(_git_relative_destination(project, ".agents/.agent-core"))
    rendered = _render_exclusions(existing, destinations)
    if rendered != existing:
        try:
            _atomic_write(exclude_path, rendered)
        except OSError as exc:
            raise ApplyError(f"Could not update Git local exclusions: {exclude_path}: {exc}") from exc


def _remove_path(path: Path) -> None:
    kind = _entry_kind(path)
    if kind == "directory":
        shutil.rmtree(path)
    else:
        path.unlink()


def _move_path(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def _cleanup_empty_parents(project_root: Path) -> None:
    for path in (project_root / DESTINATION_BASE, project_root / ".agents"):
        try:
            path.rmdir()
        except OSError:
            pass


def apply_checkout(checkout: Path, cwd: Path, *, here: bool = False) -> list[TargetPlan]:
    checkout = checkout.resolve()
    sources, commit = load_sources(checkout)
    project = resolve_project(cwd, here=here)
    ownership_path = state_path(project)
    records = load_state(ownership_path)
    plans = build_plan(project, sources, records)

    prospective = dict(records)
    for plan in plans:
        prospective[plan.destination] = {
            "destination": plan.destination,
            "source_skill": plan.source.name,
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }

    operation_id = uuid.uuid4().hex
    staging_root = project.root / ".agents" / f".agent-core-stage-{operation_id}"
    backup_root = project.root / ".agents" / f".agent-core-backup-{operation_id}"
    completed: list[tuple[Path, Path | None]] = []
    replacements_started = False
    try:
        staging_root.mkdir(parents=True)
        for plan in plans:
            staged = staging_root / plan.source.name
            shutil.copytree(plan.source.path, staged, symlinks=True)
            staged_fingerprint = fingerprint_directory(staged)
            if staged_fingerprint != plan.source.fingerprint:
                raise ApplyError(f"Staged copy fingerprint mismatch for skill {plan.source.name}")

        verify_plan_still_safe(project, plans, records)
        _prepare_exclusions(project, prospective)
        (project.root / DESTINATION_BASE).mkdir(parents=True, exist_ok=True)
        backup_root.mkdir()
        replacements_started = True
        for plan in plans:
            backup: Path | None = None
            if _lexists(plan.target):
                backup = backup_root / plan.source.name
                _move_path(plan.target, backup)
            completed.append((plan.target, backup))
            _move_path(staging_root / plan.source.name, plan.target)

        try:
            _atomic_write(ownership_path, _render_state(prospective))
        except OSError as exc:
            raise ApplyError(f"Could not persist ownership state: {ownership_path}: {exc}") from exc
    except Exception as exc:
        rollback_errors: list[str] = []
        if replacements_started:
            for target, backup in reversed(completed):
                try:
                    if _lexists(target):
                        _remove_path(target)
                    if backup is not None and _lexists(backup):
                        target.parent.mkdir(parents=True, exist_ok=True)
                        _move_path(backup, target)
                except Exception as rollback_exc:
                    rollback_errors.append(f"{target}: {rollback_exc}")
        if rollback_errors:
            raise ApplyError(
                f"Apply failed ({exc}) and rollback was incomplete:\n- " + "\n- ".join(rollback_errors)
            ) from exc
        if isinstance(exc, ApplyError):
            raise
        raise ApplyError(f"Apply failed before completion: {exc}") from exc
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)
        shutil.rmtree(backup_root, ignore_errors=True)
        _cleanup_empty_parents(project.root)

    return plans


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal post-refresh Agent Core apply implementation.")
    parser.add_argument("--checkout", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--here", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        plans = apply_checkout(Path(args.checkout), Path(args.cwd), here=args.here)
    except ApplyError as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1
    actions = {
        "absent": "added",
        "owned-missing": "recreated",
        "owned-unchanged": "replaced",
    }
    print(f"Applied {len(plans)} configured skills:")
    for plan in plans:
        print(f"- {actions[plan.classification]}: {plan.source.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
