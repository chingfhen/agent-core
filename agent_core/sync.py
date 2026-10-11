from __future__ import annotations

import argparse
import hashlib
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
from agent_core.pi_manifest import PI_MANIFEST_FILENAME, PiManifestError, load_pi_names

STATE_VERSION = 3
PREVIOUS_STATE_VERSION = 2
STATE_DIRECTORY = ".agent-core-state"
STATE_FILENAME = "ownership.json"
SHARED_SKILL_BASE = Path(".agents/skills")
CLAUDE_SKILL_BASE = Path(".claude/skills")
PI_BASES = {"agents": Path(".agents/agents"), "prompts": Path(".agents/prompts")}
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
class PiSource:
    category: str
    name: str
    path: Path
    fingerprint: str


@dataclass(frozen=True)
class PiPlan:
    source: PiSource
    target: Path
    classification: str


@dataclass(frozen=True)
class SyncResult:
    checkout: Path
    commit: str
    manifest: Path
    state_path: Path
    shared_base: Path
    skills: list[SkillPlan]
    pi_resources: list[PiPlan]


def global_state_path(home: Path) -> Path:
    return home / STATE_DIRECTORY / STATE_FILENAME


def _path_text(path: Path) -> str:
    return str(path.resolve(strict=False))


def _empty_state() -> dict[str, object]:
    return {"version": STATE_VERSION, "skills": {}, "aliases": {}, "guidance": {}, "pi_agents": {}, "pi_prompts": {}}


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
    old_fields = {"version", "skills", "aliases", "guidance"}
    new_fields = old_fields | {"pi_agents", "pi_prompts"}
    if not isinstance(payload, dict):
        raise SyncError(f"Global ownership state has an invalid shape: {path}")
    if payload.get("version") == PREVIOUS_STATE_VERSION and set(payload) == old_fields:
        # Existing skills-only machines upgrade without touching installed resources.
        payload = {**payload, "version": STATE_VERSION, "pi_agents": {}, "pi_prompts": {}}
    elif payload.get("version") != STATE_VERSION or set(payload) != new_fields:
        raise SyncError(f"Global ownership state has an unsupported version or shape: {path}")
    if not all(isinstance(payload[key], dict) for key in new_fields - {"version"}):
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
    for category, base in PI_BASES.items():
        for name, raw in payload[f"pi_{category}"].items():
            if not apply._safe_skill_name(name):
                raise SyncError(f"Invalid managed Pi {category} name: {name!r}")
            record = _expect_record(
                raw, {"destination", "source_commit", "fingerprint"}, f"Pi {category} {name!r}"
            )
            expected = home / base / f"{name}.md"
            if (
                Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
                or not apply.HEX_SHA.fullmatch(record["source_commit"])
                or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
            ):
                raise SyncError(f"Invalid Pi {category} ownership record for {name!r}")
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


def _build_skill_plans(
    home: Path,
    sources: list[apply.SourceSkill],
    state: dict[str, object],
) -> list[SkillPlan]:
    skill_records = state["skills"]
    assert isinstance(skill_records, dict)

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

    if errors:
        raise SyncError("Preflight refused global changes:\n- " + "\n- ".join(errors))
    return skill_plans


def _file_fingerprint(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise SyncError(f"Cannot read Pi resource {path}: {exc}") from exc


def _load_pi_sources(checkout: Path) -> list[PiSource]:
    manifest = checkout / PI_MANIFEST_FILENAME
    if not apply._lexists(manifest):
        # Allow historical skills-only checkouts and existing fixtures.
        return []
    if apply._entry_kind(manifest) != "file":
        raise SyncError(f"Pi manifest is not a regular file: {manifest}")
    try:
        configured = load_pi_names(manifest)
    except PiManifestError as exc:
        raise SyncError(str(exc)) from exc

    for category, names in configured.items():
        if len(set(name.casefold() for name in names)) != len(names):
            raise SyncError(f"Duplicate Pi {category} names in {PI_MANIFEST_FILENAME}")
        for name in names:
            if not apply._safe_skill_name(name):
                raise SyncError(f"Unsafe Pi {category} name: {name!r}")
    for path in [manifest] + [
        checkout / "pi" / category / f"{name}.md"
        for category, names in configured.items()
        for name in names
    ]:
        if not apply._lexists(path) or apply._entry_kind(path) != "file":
            raise SyncError(f"Configured Pi source is not a regular file: {path}")
        relative = path.relative_to(checkout).as_posix()
        if relative not in apply._tracked_paths(checkout, relative):
            raise SyncError(f"Configured Pi source is not Git-tracked: {relative}")
        diff = apply._run_git(checkout, "diff", "--quiet", "HEAD", "--", relative)
        if diff.returncode != 0:
            raise SyncError(f"Configured Pi source must match the canonical commit: {relative}")

    sources: list[PiSource] = []
    for category, names in configured.items():
        for name in names:
            path = checkout / "pi" / category / f"{name}.md"
            sources.append(PiSource(category, name, path, _file_fingerprint(path)))
    return sources


def _build_pi_plans(
    home: Path, sources: list[PiSource], state: dict[str, object]
) -> list[PiPlan]:
    errors: list[str] = []
    plans: list[PiPlan] = []
    for source in sources:
        target = home / PI_BASES[source.category] / f"{source.name}.md"
        records = state[f"pi_{source.category}"]
        assert isinstance(records, dict)
        record = records.get(source.name)
        exists = apply._lexists(target)
        if not exists:
            classification = "added" if record is None else "recreated"
        else:
            try:
                kind = apply._entry_kind(target)
                installed = _file_fingerprint(target) if kind == "file" else None
            except (apply.ApplyError, SyncError) as exc:
                errors.append(str(exc))
                continue
            if installed is None:
                errors.append(f"{target} is not a regular file")
                continue
            if record is None:
                if installed != source.fingerprint:
                    errors.append(f"{target} exists but is not owned by Agent Core and differs from source")
                    continue
                classification = "adopted"
            elif installed != record["fingerprint"]:
                errors.append(f"{target} was locally modified")
                continue
            else:
                classification = "unchanged" if installed == source.fingerprint else "updated"
        plans.append(PiPlan(source, target, classification))
    if errors:
        raise SyncError("Preflight refused Pi changes:\n- " + "\n- ".join(errors))
    return plans


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


def _render_state(state: dict[str, object]) -> str:
    ordered = {
        "version": STATE_VERSION,
        "skills": dict(sorted(state["skills"].items())),
        "aliases": dict(sorted(state["aliases"].items())),
        "guidance": dict(sorted(state["guidance"].items())),
        "pi_agents": dict(sorted(state["pi_agents"].items())),
        "pi_prompts": dict(sorted(state["pi_prompts"].items())),
    }
    return json.dumps(ordered, indent=2) + "\n"


def sync_checkout(checkout: Path, home: Path) -> SyncResult:
    checkout = checkout.resolve()
    home = home.resolve()
    sources, commit = apply.load_sources(checkout)
    pi_sources = _load_pi_sources(checkout)

    ownership_path = global_state_path(home)
    state = load_global_state(ownership_path, home)
    destinations = [home / SHARED_SKILL_BASE / source.name for source in sources]
    destinations.extend(home / PI_BASES[src.category] / f"{src.name}.md" for src in pi_sources)
    destinations.append(ownership_path)
    _ensure_real_parents(home, destinations)
    skill_plans = _build_skill_plans(home, sources, state)
    pi_plans = _build_pi_plans(home, pi_sources, state)

    prospective = json.loads(json.dumps(state))
    for plan in skill_plans:
        prospective["skills"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }
    for plan in pi_plans:
        prospective[f"pi_{plan.source.category}"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
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
        for plan in pi_plans:
            staged = stage / "pi" / plan.source.category / f"{plan.source.name}.md"
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(plan.source.path, staged)
            if _file_fingerprint(staged) != plan.source.fingerprint:
                raise SyncError(f"Staged Pi resource fingerprint mismatch: {plan.source.name}")

        # Repeat all safety checks immediately before the first replacement.
        current_state = load_global_state(ownership_path, home)
        if current_state != state:
            raise SyncError(f"Global ownership state changed after preflight: {ownership_path}")
        _build_skill_plans(home, sources, state)
        _build_pi_plans(home, pi_sources, state)

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

        for plan in pi_plans:
            if plan.classification in {"unchanged", "adopted"}:
                continue
            plan.target.parent.mkdir(parents=True, exist_ok=True)
            saved = None
            if apply._lexists(plan.target):
                saved = backup / "pi" / plan.source.category / f"{plan.source.name}.md"
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.target, saved)
            completed.append((plan.target, saved))
            os.replace(stage / "pi" / plan.source.category / f"{plan.source.name}.md", plan.target)
            if _file_fingerprint(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published Pi resource mismatch: {plan.target}")

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
        skill_plans,
        pi_plans,
    )


def print_result(result: SyncResult) -> None:
    print(f"agent-core sync: OK ({result.commit[:12]})")
    print(f"Skills ({len(result.skills)}): " + (", ".join(p.source.name for p in result.skills) or "none"))
    for category in ("agents", "prompts"):
        plans = [p for p in result.pi_resources if p.source.category == category]
        print(f"Pi {category} ({len(plans)}): " + (", ".join(p.source.name for p in plans) or "none"))
    print("Installed root: ~/.agents/ (global guidance unchanged)")


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
