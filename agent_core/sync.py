from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from agent_core import apply
from agent_core.manifest import MANIFEST_FILENAME

STATE_VERSION = 2
STATE_DIRECTORY = ".agent-core-state"
STATE_FILENAME = "ownership.json"
SHARED_SKILL_BASE = Path(".agents/skills")
CLAUDE_SKILL_BASE = Path(".claude/skills")
LEGACY_GUIDANCE_DESTINATIONS = {
    "pi": Path(".pi/agent/AGENTS.md"),
    "codex": Path(".codex/AGENTS.md"),
    "opencode": Path(".config/opencode/AGENTS.md"),
    "claude": Path(".claude/CLAUDE.md"),
}
HEX_FINGERPRINT = apply.HEX_FINGERPRINT


class SyncError(RuntimeError):
    pass


@dataclass(frozen=True)
class SkillPlan:
    source: apply.SourceSkill
    target: Path
    classification: str


@dataclass(frozen=True)
class AliasPlan:
    name: str
    target: Path
    alias: Path
    classification: str
    replace_existing: bool


@dataclass(frozen=True)
class SyncResult:
    checkout: Path
    commit: str
    manifest: Path
    state_path: Path
    shared_base: Path
    claude_base: Path
    skills: list[SkillPlan]
    aliases: list[AliasPlan]


def global_state_path(home: Path) -> Path:
    return home / STATE_DIRECTORY / STATE_FILENAME


def _path_text(path: Path) -> str:
    return str(path.resolve(strict=False))


def _empty_state() -> dict[str, object]:
    return {"version": STATE_VERSION, "skills": {}, "aliases": {}, "guidance": {}}


def _expect_record(record: object, fields: set[str], context: str) -> dict[str, str]:
    if not isinstance(record, dict) or set(record) != fields:
        raise SyncError(f"Ownership state has an invalid {context} record")
    if any(not isinstance(value, str) for value in record.values()):
        raise SyncError(f"Ownership state has a non-string value in {context}")
    return record


def load_global_state(path: Path, home: Path) -> dict[str, object]:
    if not apply._lexists(path):
        return _empty_state()
    if apply._entry_kind(path) != "file":
        raise SyncError(f"Global ownership state is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Global ownership state is malformed: {path}: {exc}") from exc
    if not isinstance(payload, dict) or set(payload) != {"version", "skills", "aliases", "guidance"}:
        raise SyncError(f"Global ownership state has an invalid shape: {path}")
    if payload["version"] != STATE_VERSION:
        raise SyncError(f"Global ownership state has an unsupported version: {path}")
    if not all(isinstance(payload[key], dict) for key in ("skills", "aliases", "guidance")):
        raise SyncError(f"Global ownership state has invalid record collections: {path}")

    for name, raw in payload["skills"].items():
        if not apply._safe_skill_name(name):
            raise SyncError(f"Global ownership state has an invalid skill name: {name!r}")
        record = _expect_record(
            raw, {"destination", "source_commit", "fingerprint"}, f"skill {name!r}"
        )
        expected = home / SHARED_SKILL_BASE / name
        if (
            Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
            or not apply.HEX_SHA.fullmatch(record["source_commit"])
            or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
        ):
            raise SyncError(f"Global ownership state has an invalid skill record for {name!r}")

    for name, raw in payload["aliases"].items():
        if not apply._safe_skill_name(name):
            raise SyncError(f"Global ownership state has an invalid alias name: {name!r}")
        record = _expect_record(raw, {"destination", "target"}, f"alias {name!r}")
        expected_alias = home / CLAUDE_SKILL_BASE / name
        expected_target = home / SHARED_SKILL_BASE / name
        if (
            Path(record["destination"]).resolve(strict=False) != expected_alias.resolve(strict=False)
            or Path(record["target"]).resolve(strict=False) != expected_target.resolve(strict=False)
        ):
            raise SyncError(f"Global ownership state has an invalid alias record for {name!r}")

    for harness, raw in payload["guidance"].items():
        if harness not in LEGACY_GUIDANCE_DESTINATIONS:
            raise SyncError(f"Global ownership state has an unknown guidance target: {harness!r}")
        record = _expect_record(
            raw, {"destination", "source_commit", "fingerprint"}, f"guidance {harness!r}"
        )
        expected = home / LEGACY_GUIDANCE_DESTINATIONS[harness]
        if (
            Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
            or not apply.HEX_SHA.fullmatch(record["source_commit"])
            or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
        ):
            raise SyncError(f"Global ownership state has an invalid guidance record for {harness!r}")
    return payload


def _ensure_real_parents(home: Path, destinations: list[Path]) -> None:
    errors: list[str] = []
    home_resolved = home.resolve(strict=False)
    for destination in destinations:
        current = destination.parent
        chain: list[Path] = []
        while current != home and current != current.parent:
            chain.append(current)
            current = current.parent
        if current.resolve(strict=False) != home_resolved:
            errors.append(f"destination is outside the selected home: {destination}")
            continue
        for parent in reversed(chain):
            if not apply._lexists(parent):
                continue
            try:
                kind = apply._entry_kind(parent)
            except apply.ApplyError as exc:
                errors.append(str(exc))
                continue
            if kind != "directory":
                errors.append(f"managed destination parent is not a real directory: {parent} ({kind})")
    if errors:
        raise SyncError("Preflight refused global changes:\n- " + "\n- ".join(errors))


def _is_alias_entry(path: Path) -> bool:
    try:
        metadata = path.stat(follow_symlinks=False)
    except OSError:
        return False
    return stat.S_ISLNK(metadata.st_mode) or apply._is_reparse(metadata)


def _alias_matches(alias: Path, target: Path) -> bool:
    if not _is_alias_entry(alias):
        return False
    try:
        return alias.is_dir() and target.is_dir() and os.path.samefile(alias, target)
    except OSError:
        return False


def _build_plans(
    home: Path,
    sources: list[apply.SourceSkill],
    state: dict[str, object],
) -> tuple[list[SkillPlan], list[AliasPlan]]:
    skill_records = state["skills"]
    alias_records = state["aliases"]
    assert isinstance(skill_records, dict)
    assert isinstance(alias_records, dict)

    errors: list[str] = []
    skill_plans: list[SkillPlan] = []
    for source in sources:
        target = home / SHARED_SKILL_BASE / source.name
        record = skill_records.get(source.name)
        exists = apply._lexists(target)
        if record is None:
            if exists:
                errors.append(f"{target} exists but is not owned by Agent Core")
                continue
            classification = "added"
        elif not exists:
            classification = "recreated"
        else:
            try:
                installed = apply.fingerprint_directory(target)
            except apply.ApplyError as exc:
                errors.append(f"{target} is not an unchanged managed skill: {exc}")
                continue
            if installed != record["fingerprint"]:
                errors.append(f"{target} was locally modified")
                continue
            classification = "unchanged" if installed == source.fingerprint else "updated"
        skill_plans.append(SkillPlan(source, target, classification))

    alias_plans: list[AliasPlan] = []
    for source in sources:
        target = home / SHARED_SKILL_BASE / source.name
        alias = home / CLAUDE_SKILL_BASE / source.name
        record = alias_records.get(source.name)
        exists = apply._lexists(alias)
        if record is None:
            if exists:
                errors.append(f"{alias} exists but is not owned by Agent Core")
                continue
            classification = "added"
            replace_existing = False
        elif not exists:
            classification = "recreated"
            replace_existing = False
        elif _alias_matches(alias, target):
            classification = "unchanged"
            replace_existing = False
        elif not apply._lexists(target) and _is_alias_entry(alias):
            # A managed alias can be temporarily broken when its managed skill copy was deleted.
            classification = "recreated"
            replace_existing = True
        else:
            errors.append(f"{alias} no longer points to the managed shared skill {target}")
            continue
        alias_plans.append(AliasPlan(source.name, target, alias, classification, replace_existing))

    if errors:
        raise SyncError("Preflight refused global changes:\n- " + "\n- ".join(errors))
    return skill_plans, alias_plans


def _remove_path(path: Path) -> None:
    metadata = path.stat(follow_symlinks=False)
    if stat.S_ISLNK(metadata.st_mode):
        path.unlink()
    elif apply._is_reparse(metadata):
        if path.is_dir():
            os.rmdir(path)
        else:
            path.unlink()
    elif stat.S_ISDIR(metadata.st_mode):
        shutil.rmtree(path)
    else:
        path.unlink()


def _create_directory_alias(alias: Path, target: Path) -> None:
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
            raise SyncError(f"Could not create Claude directory junction {alias}: {detail}")
    else:
        try:
            alias.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            raise SyncError(f"Could not create Claude skill symlink {alias}: {exc}") from exc


def _render_state(state: dict[str, object]) -> str:
    ordered = {
        "version": STATE_VERSION,
        "skills": dict(sorted(state["skills"].items())),
        "aliases": dict(sorted(state["aliases"].items())),
        "guidance": dict(sorted(state["guidance"].items())),
    }
    return json.dumps(ordered, indent=2) + "\n"


def sync_checkout(checkout: Path, home: Path) -> SyncResult:
    checkout = checkout.resolve()
    home = home.resolve()
    sources, commit = apply.load_sources(checkout)

    ownership_path = global_state_path(home)
    state = load_global_state(ownership_path, home)
    destinations = [home / SHARED_SKILL_BASE / source.name for source in sources]
    destinations.extend(home / CLAUDE_SKILL_BASE / source.name for source in sources)
    destinations.append(ownership_path)
    _ensure_real_parents(home, destinations)
    skill_plans, alias_plans = _build_plans(home, sources, state)

    prospective = json.loads(json.dumps(state))
    for plan in skill_plans:
        prospective["skills"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }
    for plan in alias_plans:
        prospective["aliases"][plan.name] = {
            "destination": _path_text(plan.alias),
            "target": _path_text(plan.target),
        }
    prospective["guidance"] = {}

    state_directory = ownership_path.parent
    state_directory.mkdir(parents=True, exist_ok=True)
    transaction = state_directory / f"transaction-{uuid.uuid4().hex}"
    stage = transaction / "stage"
    backup = transaction / "backup"
    completed: list[tuple[Path, Path | None]] = []
    try:
        (stage / "skills").mkdir(parents=True)
        backup.mkdir(parents=True)
        for plan in skill_plans:
            staged = stage / "skills" / plan.source.name
            shutil.copytree(plan.source.path, staged, symlinks=True)
            if apply.fingerprint_directory(staged) != plan.source.fingerprint:
                raise SyncError(f"Staged skill fingerprint mismatch: {plan.source.name}")

        # Repeat all safety checks immediately before the first replacement.
        current_state = load_global_state(ownership_path, home)
        if current_state != state:
            raise SyncError(f"Global ownership state changed after preflight: {ownership_path}")
        _build_plans(home, sources, state)

        for plan in skill_plans:
            if plan.classification == "unchanged":
                continue
            plan.target.parent.mkdir(parents=True, exist_ok=True)
            saved: Path | None = None
            if apply._lexists(plan.target):
                saved = backup / "skills" / plan.source.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.target, saved)
            completed.append((plan.target, saved))
            os.replace(stage / "skills" / plan.source.name, plan.target)

        for plan in alias_plans:
            if plan.classification == "unchanged":
                continue
            plan.alias.parent.mkdir(parents=True, exist_ok=True)
            saved = None
            if apply._lexists(plan.alias):
                saved = backup / "aliases" / plan.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.alias, saved)
            completed.append((plan.alias, saved))
            _create_directory_alias(plan.alias, plan.target)
            if not _alias_matches(plan.alias, plan.target):
                raise SyncError(f"Created Claude alias does not resolve to its shared skill: {plan.alias}")

        try:
            apply._atomic_write(ownership_path, _render_state(prospective))
        except OSError as exc:
            raise SyncError(f"Could not publish global ownership state {ownership_path}: {exc}") from exc
    except Exception as exc:
        rollback_errors: list[str] = []
        for target, saved in reversed(completed):
            try:
                if apply._lexists(target):
                    _remove_path(target)
                if saved is not None and apply._lexists(saved):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(saved, target)
            except Exception as rollback_exc:
                rollback_errors.append(f"{target}: {rollback_exc}")
        if rollback_errors:
            raise SyncError(
                f"Sync failed ({exc}) and rollback was incomplete:\n- " + "\n- ".join(rollback_errors)
            ) from exc
        if isinstance(exc, (SyncError, apply.ApplyError)):
            raise SyncError(str(exc)) from exc
        raise SyncError(f"Sync failed before completion: {exc}") from exc
    finally:
        shutil.rmtree(transaction, ignore_errors=True)

    return SyncResult(
        checkout,
        commit,
        checkout / MANIFEST_FILENAME,
        ownership_path,
        home / SHARED_SKILL_BASE,
        home / CLAUDE_SKILL_BASE,
        skill_plans,
        alias_plans,
    )


def _counts(items: Sequence[object]) -> str:
    classifications = [getattr(item, "classification") for item in items]
    return ", ".join(
        f"{name}={classifications.count(name)}" for name in ("added", "updated", "recreated", "unchanged")
    )


def print_result(result: SyncResult) -> None:
    changed = [plan.source.name for plan in result.skills if plan.classification != "unchanged"]
    print(f"Canonical checkout: {result.checkout}")
    print(f"Canonical commit: {result.commit}")
    print(f"Manifest: {result.manifest} ({len(result.skills)} configured skills)")
    print(f"Shared skills: {result.shared_base} ({_counts(result.skills)})")
    print("Changed skills: " + (", ".join(changed) if changed else "none"))
    alias_statuses = sorted({plan.classification for plan in result.aliases})
    print(
        f"Claude aliases: {result.claude_base} ({len(result.aliases)} aliases; "
        + ", ".join(alias_statuses)
        + ")"
    )
    print("Global guidance: not managed (existing files preserved)")
    print(f"Ownership state: {result.state_path}")
    print("Reload or restart active harness sessions to use changed skills.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal post-refresh Agent Core global sync implementation.")
    parser.add_argument("--checkout", required=True)
    parser.add_argument("--home", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = sync_checkout(Path(args.checkout), Path(args.home))
    except (SyncError, apply.ApplyError) as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1
    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
