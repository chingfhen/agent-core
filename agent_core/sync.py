from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from agent_core import apply
from agent_core.devin_manifest import (
    DEVIN_MANIFEST_FILENAME,
    DevinManifestError,
    load_devin_names,
)
from agent_core.manifest import MANIFEST_FILENAME
from agent_core.pi_manifest import PI_MANIFEST_FILENAME, PiManifestError, load_pi_names

STATE_VERSION = 6
STATE_DIRECTORY = ".agent-core-state"
STATE_FILENAME = "ownership.json"
SHARED_SKILL_BASE = Path(".pi/agent/skills")
OPENCODE_SKILL_BASE = Path(".config/opencode/skills")
DEVIN_DIRECTORY = "devin"
LEGACY_SKILL_BASE = Path(".agents/skills")
CLAUDE_SKILL_BASE = Path(".claude/skills")
PI_BASES = {"agents": Path(".pi/agent/agents"), "prompts": Path(".pi/agent/prompts")}
LEGACY_PI_BASES = {"agents": Path(".agents/agents"), "prompts": Path(".agents/prompts")}
RETIRED_PI_RESOURCES = {"prompts": {"commit-with-subagent"}}
PYTHON_SKILL_REPLACEMENT = "manage-python-env"
RETIRED_PYTHON_SKILLS = ("manage-python-agent-envs", "manage-python-uv")
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
class DevinSource:
    name: str
    path: Path
    fingerprint: str


@dataclass(frozen=True)
class DevinPlan:
    source: DevinSource
    target: Path
    classification: str


@dataclass(frozen=True)
class LegacyPlan:
    path: Path
    category: str
    name: str
    kind: str


@dataclass(frozen=True)
class SyncResult:
    harness: str
    checkout: Path
    commit: str
    manifest: Path
    state_path: Path
    shared_base: Path
    skills: list[SkillPlan]
    pi_resources: list[PiPlan]
    devin_resources: list[DevinPlan]
    legacy: list[LegacyPlan]


def global_state_path(home: Path) -> Path:
    return home / STATE_DIRECTORY / STATE_FILENAME


def _path_text(path: Path) -> str:
    return str(path.resolve(strict=False))


def _empty_state() -> dict[str, object]:
    return {
        "version": STATE_VERSION,
        "skills": {},
        "aliases": {},
        "guidance": {},
        "pi_agents": {},
        "pi_prompts": {},
        "devin_skills": {},
        "devin_agents": {},
        "opencode_skills": {},
    }


def _expect_record(record: object, fields: set[str], context: str) -> dict[str, str]:
    if not isinstance(record, dict) or set(record) != fields:
        raise SyncError(f"Ownership state has an invalid {context} record")
    if any(not isinstance(value, str) for value in record.values()):
        raise SyncError(f"Ownership state has a non-string value in {context}")
    return record


def load_global_state(
    path: Path, home: Path, devin_base: Path | None = None
) -> dict[str, object]:
    if not apply._lexists(path):
        return _empty_state()
    if apply._entry_kind(path) != "file":
        raise SyncError(f"Global ownership state is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Global ownership state is malformed: {path}: {exc}") from exc
    legacy_fields = {"version", "skills", "aliases", "guidance"}
    pi_fields = legacy_fields | {"pi_agents", "pi_prompts"}
    current_fields = pi_fields | {"devin_skills", "devin_agents", "opencode_skills"}
    if not isinstance(payload, dict):
        raise SyncError(f"Global ownership state has an invalid shape: {path}")
    if payload.get("version") == 2 and set(payload) == legacy_fields:
        payload = {
            **payload,
            "version": STATE_VERSION,
            "pi_agents": {},
            "pi_prompts": {},
            "devin_skills": {},
            "devin_agents": {},
            "opencode_skills": {},
        }
    elif payload.get("version") in {3, 4} and set(payload) == pi_fields:
        payload = {
            **payload,
            "version": STATE_VERSION,
            "devin_skills": {},
            "devin_agents": {},
            "opencode_skills": {},
        }
    elif payload.get("version") == 5 and set(payload) == pi_fields | {"devin_skills", "devin_agents"}:
        payload = {**payload, "version": STATE_VERSION, "opencode_skills": {}}
    elif payload.get("version") == STATE_VERSION and set(payload) == current_fields:
        pass
    else:
        raise SyncError(f"Global ownership state has an unsupported version or shape: {path}")
    if not all(isinstance(payload[key], dict) for key in current_fields - {"version"}):
        raise SyncError(f"Global ownership state has invalid record collections: {path}")

    for name, raw in payload["skills"].items():
        if not apply._safe_skill_name(name):
            raise SyncError(f"Global ownership state has an invalid skill name: {name!r}")
        record = _expect_record(
            raw, {"destination", "source_commit", "fingerprint"}, f"skill {name!r}"
        )
        expected = {home / SHARED_SKILL_BASE / name, home / LEGACY_SKILL_BASE / name}
        if (
            Path(record["destination"]).resolve(strict=False)
            not in {entry.resolve(strict=False) for entry in expected}
            or not apply.HEX_SHA.fullmatch(record["source_commit"])
            or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
        ):
            raise SyncError(f"Global ownership state has an invalid skill record for {name!r}")

    for name, raw in payload["aliases"].items():
        if not apply._safe_skill_name(name):
            raise SyncError(f"Global ownership state has an invalid alias name: {name!r}")
        record = _expect_record(raw, {"destination", "target"}, f"alias {name!r}")
        expected_alias = home / CLAUDE_SKILL_BASE / name
        expected_target = home / LEGACY_SKILL_BASE / name
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
            expected = {
                home / base / f"{name}.md",
                home / LEGACY_PI_BASES[category] / f"{name}.md",
            }
            if (
                Path(record["destination"]).resolve(strict=False)
                not in {entry.resolve(strict=False) for entry in expected}
                or not apply.HEX_SHA.fullmatch(record["source_commit"])
                or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
            ):
                raise SyncError(f"Invalid Pi {category} ownership record for {name!r}")

    for name, raw in payload["opencode_skills"].items():
        if not apply._safe_skill_name(name):
            raise SyncError(f"Invalid managed OpenCode skill name: {name!r}")
        record = _expect_record(
            raw, {"destination", "source_commit", "fingerprint"}, f"OpenCode skill {name!r}"
        )
        expected = home / OPENCODE_SKILL_BASE / name
        if (
            Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
            or not apply.HEX_SHA.fullmatch(record["source_commit"])
            or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
        ):
            raise SyncError(f"Invalid OpenCode skill ownership record for {name!r}")

    devin_records = [payload["devin_skills"], payload["devin_agents"]]
    if any(devin_records) and devin_base is None:
        raise SyncError("APPDATA is required to validate managed Devin ownership")
    if devin_base is not None:
        for name, raw in payload["devin_skills"].items():
            if not apply._safe_skill_name(name):
                raise SyncError(f"Invalid managed Devin skill name: {name!r}")
            record = _expect_record(
                raw, {"destination", "source_commit", "fingerprint"}, f"Devin skill {name!r}"
            )
            expected = devin_base / "skills" / name
            if (
                Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
                or not apply.HEX_SHA.fullmatch(record["source_commit"])
                or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
            ):
                raise SyncError(f"Invalid Devin skill ownership record for {name!r}")
        for name, raw in payload["devin_agents"].items():
            if not apply._safe_skill_name(name):
                raise SyncError(f"Invalid managed Devin agent name: {name!r}")
            record = _expect_record(
                raw, {"destination", "source_commit", "fingerprint"}, f"Devin agent {name!r}"
            )
            expected = devin_base / "agents" / f"{name}.md"
            if (
                Path(record["destination"]).resolve(strict=False) != expected.resolve(strict=False)
                or not apply.HEX_SHA.fullmatch(record["source_commit"])
                or not HEX_FINGERPRINT.fullmatch(record["fingerprint"])
            ):
                raise SyncError(f"Invalid Devin agent ownership record for {name!r}")
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


def _is_legacy_record(record: dict[str, str] | None, path: Path) -> bool:
    return record is not None and Path(record["destination"]).resolve(strict=False) == path.resolve(strict=False)


def _alias_matches(alias: Path, old_skill: Path) -> bool:
    try:
        metadata = alias.stat(follow_symlinks=False)
        is_link = stat.S_ISLNK(metadata.st_mode) or apply._is_reparse(metadata)
        return is_link and alias.is_dir() and old_skill.is_dir() and os.path.samefile(alias, old_skill)
    except OSError:
        return False


def _build_skill_plans(
    home: Path, sources: list[apply.SourceSkill], state: dict[str, object]
) -> tuple[list[SkillPlan], list[LegacyPlan]]:
    records = state["skills"]
    aliases = state["aliases"]
    assert isinstance(records, dict) and isinstance(aliases, dict)
    plans: list[SkillPlan] = []
    retired: list[LegacyPlan] = []
    errors: list[str] = []

    for source in sources:
        target = home / SHARED_SKILL_BASE / source.name
        old_target = home / LEGACY_SKILL_BASE / source.name
        record = records.get(source.name)
        legacy = _is_legacy_record(record, old_target)

        if legacy and apply._lexists(old_target):
            try:
                installed = apply.fingerprint_directory(old_target)
            except apply.ApplyError as exc:
                errors.append(f"Legacy skill {old_target} is unsafe: {exc}")
                continue
            if installed != record["fingerprint"]:
                errors.append(f"Legacy skill {old_target} was locally modified; refusing migration")
                continue
            retired.append(LegacyPlan(old_target, "skills", source.name, "directory"))

        if legacy and source.name in aliases:
            alias = home / CLAUDE_SKILL_BASE / source.name
            if apply._lexists(alias) and not _alias_matches(alias, old_target):
                errors.append(f"Legacy Claude alias {alias} differs or cannot be verified; resolve manually")
                continue
            # Include missing historical aliases so their ownership is cleared.
            retired.append(LegacyPlan(alias, "aliases", source.name, "link"))

        if not apply._lexists(target):
            classification = "migrated" if legacy else ("added" if record is None else "recreated")
        else:
            try:
                installed = apply.fingerprint_directory(target)
            except apply.ApplyError as exc:
                errors.append(f"Pi skill {target} is not a regular directory: {exc}")
                continue
            if installed == source.fingerprint:
                classification = "unchanged" if record is not None and not legacy else "adopted"
            else:
                # The declared canonical resource is authoritative, even if
                # the installed directory was manually created or edited.
                classification = "updated" if record is not None and not legacy else "replaced"
        plans.append(SkillPlan(source, target, classification))

    if errors:
        raise SyncError("Preflight refused skill changes:\n- " + "\n- ".join(errors))
    return plans, retired


def _file_fingerprint(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise SyncError(f"Cannot read managed resource {path}: {exc}") from exc


def _resolve_devin_base(app_data: Path | None = None) -> Path:
    if app_data is None:
        raw = os.environ.get("APPDATA", "").strip()
        if not raw:
            raise SyncError("APPDATA is required for --harness devin")
        app_data = Path(raw)
    return app_data.resolve(strict=False) / DEVIN_DIRECTORY


def _ambient_devin_base() -> Path | None:
    raw = os.environ.get("APPDATA", "").strip()
    return _resolve_devin_base(Path(raw)) if raw else None


def _load_devin_sources(checkout: Path) -> list[DevinSource]:
    manifest = checkout / DEVIN_MANIFEST_FILENAME
    if not apply._lexists(manifest):
        raise SyncError(f"Required Devin manifest is missing: {manifest}")
    if apply._entry_kind(manifest) != "file":
        raise SyncError(f"Devin manifest is not a regular file: {manifest}")
    try:
        names = load_devin_names(manifest)
    except DevinManifestError as exc:
        raise SyncError(str(exc)) from exc

    if len(set(name.casefold() for name in names)) != len(names):
        raise SyncError(f"Duplicate Devin agent names in {DEVIN_MANIFEST_FILENAME}")
    for name in names:
        if not apply._safe_skill_name(name):
            raise SyncError(f"Unsafe Devin agent name: {name!r}")

    paths = [manifest] + [checkout / "devin" / "agents" / f"{name}.md" for name in names]
    for path in paths:
        if not apply._lexists(path) or apply._entry_kind(path) != "file":
            raise SyncError(f"Configured Devin source is not a regular file: {path}")
        relative = path.relative_to(checkout).as_posix()
        if relative not in apply._tracked_paths(checkout, relative):
            raise SyncError(f"Configured Devin source is not Git-tracked: {relative}")
        diff = apply._run_git(checkout, "diff", "--quiet", "HEAD", "--", relative)
        if diff.returncode != 0:
            raise SyncError(f"Configured Devin source must match the canonical commit: {relative}")

    return [
        DevinSource(
            name,
            checkout / "devin" / "agents" / f"{name}.md",
            _file_fingerprint(checkout / "devin" / "agents" / f"{name}.md"),
        )
        for name in names
    ]


def _load_pi_sources(checkout: Path) -> list[PiSource]:
    manifest = checkout / PI_MANIFEST_FILENAME
    if not apply._lexists(manifest):
        raise SyncError(f"Required Pi manifest is missing: {manifest}")
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
) -> tuple[list[PiPlan], list[LegacyPlan]]:
    errors: list[str] = []
    plans: list[PiPlan] = []
    retired: list[LegacyPlan] = []

    for source in sources:
        target = home / PI_BASES[source.category] / f"{source.name}.md"
        old_target = home / LEGACY_PI_BASES[source.category] / f"{source.name}.md"
        records = state[f"pi_{source.category}"]
        assert isinstance(records, dict)
        record = records.get(source.name)
        legacy = _is_legacy_record(record, old_target)

        if legacy and apply._lexists(old_target):
            if apply._entry_kind(old_target) != "file":
                errors.append(f"Legacy Pi resource {old_target} is not a regular file")
                continue
            if _file_fingerprint(old_target) != record["fingerprint"]:
                errors.append(f"Legacy Pi resource {old_target} was locally modified; refusing migration")
                continue
            retired.append(LegacyPlan(old_target, source.category, source.name, "file"))

        if not apply._lexists(target):
            classification = "migrated" if legacy else ("added" if record is None else "recreated")
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
            if installed == source.fingerprint:
                classification = "unchanged" if record is not None and not legacy else "adopted"
            else:
                classification = "updated" if record is not None and not legacy else "replaced"
        plans.append(PiPlan(source, target, classification))

    if errors:
        raise SyncError("Preflight refused Pi changes:\n- " + "\n- ".join(errors))
    return plans, retired


def _build_retired_pi_plans(
    home: Path, selected: list[PiSource], state: dict[str, object]
) -> list[LegacyPlan]:
    selected_keys = {(source.category, source.name) for source in selected}
    plans: list[LegacyPlan] = []
    errors: list[str] = []

    for category, names in RETIRED_PI_RESOURCES.items():
        records = state[f"pi_{category}"]
        assert isinstance(records, dict)
        for name in names:
            if (category, name) in selected_keys:
                continue
            record = records.get(name)
            if record is None:
                continue
            target = Path(record["destination"])
            if apply._lexists(target):
                if apply._entry_kind(target) != "file":
                    errors.append(f"Retired Pi resource {target} is not a regular file")
                    continue
                if _file_fingerprint(target) != record["fingerprint"]:
                    errors.append(f"Retired Pi resource {target} was locally modified; refusing removal")
                    continue
            plans.append(LegacyPlan(target, f"pi_{category}", name, "file"))

    if errors:
        raise SyncError("Preflight refused retired Pi resource changes:\n- " + "\n- ".join(errors))
    return plans


def _build_retired_python_plans(
    home: Path,
    sources: list[apply.SourceSkill],
    state: dict[str, object],
    devin_base: Path | None = None,
    *,
    harness: str | None = None,
) -> list[LegacyPlan]:
    """Named migration only; never general pruning of removed manifest entries."""
    selected = {source.name for source in sources}
    if PYTHON_SKILL_REPLACEMENT not in selected:
        return []
    if harness is None:
        harness = "devin" if devin_base is not None else "pi"
    if harness == "pi":
        record_key = "skills"
        candidate_bases = (home / SHARED_SKILL_BASE, home / LEGACY_SKILL_BASE)
        parent_root = home
    elif harness == "devin" and devin_base is not None:
        record_key = "devin_skills"
        candidate_bases = (devin_base / "skills",)
        parent_root = devin_base
    elif harness == "opencode":
        record_key = "opencode_skills"
        candidate_bases = (home / OPENCODE_SKILL_BASE,)
        parent_root = home
    else:
        raise SyncError(f"Unsupported harness for Python skill retirement: {harness}")
    records = state[record_key]
    plans: list[LegacyPlan] = []
    errors: list[str] = []
    for name in RETIRED_PYTHON_SKILLS:
        if name in selected:
            raise SyncError(f"Conflicting Python skills selected: {PYTHON_SKILL_REPLACEMENT}, {name}")
        candidates = [base / name for base in candidate_bases]
        _ensure_real_parents(parent_root, candidates)
        record = records.get(name)
        for target in candidates:
            owned = _is_legacy_record(record, target)
            if apply._lexists(target):
                if not owned:
                    errors.append(f"Obsolete Python skill is unowned; preserve and resolve manually: {target}")
                    continue
                try:
                    fingerprint = apply.fingerprint_directory(target)
                except apply.ApplyError as exc:
                    errors.append(f"Unsafe obsolete Python skill {target}: {exc}")
                    continue
                if fingerprint != record["fingerprint"]:
                    errors.append(f"Obsolete Python skill was locally modified; refusing removal: {target}")
                    continue
            if owned:
                category = "retired_skills" if harness == "pi" else record_key
                plans.append(LegacyPlan(target, category, name, "directory"))
        if harness == "pi":
            alias = home / CLAUDE_SKILL_BASE / name
            _ensure_real_parents(home, [alias])
            registered = name in state["aliases"]
            if apply._lexists(alias) and (
                not registered or not _alias_matches(alias, home / LEGACY_SKILL_BASE / name)
            ):
                errors.append(f"Obsolete Python alias is unowned or changed; preserve and resolve manually: {alias}")
            elif registered:
                plans.append(LegacyPlan(alias, "aliases", name, "link"))
    if errors:
        raise SyncError("Preflight refused Python skill retirement:\n- " + "\n- ".join(errors))
    return plans


def _build_native_skill_plans(
    skill_base: Path,
    sources: list[apply.SourceSkill],
    state: dict[str, object],
    records_key: str,
    harness_name: str,
) -> list[SkillPlan]:
    records = state[records_key]
    assert isinstance(records, dict)
    plans: list[SkillPlan] = []
    errors: list[str] = []

    for source in sources:
        target = skill_base / source.name
        record = records.get(source.name)
        if not apply._lexists(target):
            classification = "added" if record is None else "recreated"
        else:
            try:
                installed = apply.fingerprint_directory(target)
            except apply.ApplyError as exc:
                errors.append(f"{harness_name} skill {target} is not a regular directory: {exc}")
                continue
            if installed == source.fingerprint:
                classification = "unchanged" if record is not None else "adopted"
            else:
                classification = "updated" if record is not None else "replaced"
        plans.append(SkillPlan(source, target, classification))

    if errors:
        raise SyncError(f"Preflight refused {harness_name} skill changes:\n- " + "\n- ".join(errors))
    return plans


def _build_devin_skill_plans(
    devin_base: Path, sources: list[apply.SourceSkill], state: dict[str, object]
) -> list[SkillPlan]:
    return _build_native_skill_plans(
        devin_base / "skills", sources, state, "devin_skills", "Devin"
    )


def _build_opencode_skill_plans(
    home: Path, sources: list[apply.SourceSkill], state: dict[str, object]
) -> list[SkillPlan]:
    return _build_native_skill_plans(
        home / OPENCODE_SKILL_BASE, sources, state, "opencode_skills", "OpenCode"
    )


def _build_devin_agent_plans(
    devin_base: Path, sources: list[DevinSource], state: dict[str, object]
) -> list[DevinPlan]:
    records = state["devin_agents"]
    assert isinstance(records, dict)
    plans: list[DevinPlan] = []
    errors: list[str] = []

    for source in sources:
        target = devin_base / "agents" / f"{source.name}.md"
        record = records.get(source.name)
        if not apply._lexists(target):
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
            if installed == source.fingerprint:
                classification = "unchanged" if record is not None else "adopted"
            else:
                classification = "updated" if record is not None else "replaced"
        plans.append(DevinPlan(source, target, classification))

    if errors:
        raise SyncError("Preflight refused Devin agent changes:\n- " + "\n- ".join(errors))
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
        "devin_skills": dict(sorted(state["devin_skills"].items())),
        "devin_agents": dict(sorted(state["devin_agents"].items())),
        "opencode_skills": dict(sorted(state["opencode_skills"].items())),
    }
    return json.dumps(ordered, indent=2) + "\n"


def _sync_pi_checkout(checkout: Path, home: Path) -> SyncResult:
    checkout = checkout.resolve()
    home = home.resolve()
    sources, commit = apply.load_sources(checkout)
    pi_sources = _load_pi_sources(checkout)

    ownership_path = global_state_path(home)
    state = load_global_state(ownership_path, home, _ambient_devin_base())
    destinations = [home / SHARED_SKILL_BASE / source.name for source in sources]
    destinations.extend(home / PI_BASES[src.category] / f"{src.name}.md" for src in pi_sources)
    destinations.append(ownership_path)
    skill_plans, old_skills = _build_skill_plans(home, sources, state)
    pi_plans, old_pi = _build_pi_plans(home, pi_sources, state)
    retired_pi = _build_retired_pi_plans(home, pi_sources, state)
    retired_python = _build_retired_python_plans(home, sources, state)
    legacy_plans = old_skills + old_pi + retired_pi + retired_python
    destinations.extend(plan.path for plan in legacy_plans)
    _ensure_real_parents(home, destinations)

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
    for plan in legacy_plans:
        if plan.category == "aliases":
            prospective["aliases"].pop(plan.name, None)
        elif plan.category in {"pi_agents", "pi_prompts"}:
            prospective[plan.category].pop(plan.name, None)
        elif plan.category == "retired_skills":
            prospective["skills"].pop(plan.name, None)
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
        current_state = load_global_state(ownership_path, home, _ambient_devin_base())
        if current_state != state:
            raise SyncError(f"Global ownership state changed after preflight: {ownership_path}")
        if _build_skill_plans(home, sources, state) != (skill_plans, old_skills):
            raise SyncError("Skill targets changed during preflight")
        if _build_pi_plans(home, pi_sources, state) != (pi_plans, old_pi):
            raise SyncError("Pi targets changed during preflight")
        if _build_retired_pi_plans(home, pi_sources, state) != retired_pi:
            raise SyncError("Retired Pi targets changed during preflight")
        if _build_retired_python_plans(home, sources, state) != retired_python:
            raise SyncError("Retired Python targets changed during preflight")

        for plan in skill_plans:
            if plan.classification in {"unchanged", "adopted"}:
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

        # Retire only verified legacy managed resources; the backup holds
        # originals until ownership is published, enabling rollback.
        for plan in sorted(legacy_plans, key=lambda p: p.kind != "link"):
            if not apply._lexists(plan.path):
                continue
            saved = backup / "legacy" / plan.category / (
                f"{plan.name}.md" if plan.kind == "file" else plan.name
            )
            saved.parent.mkdir(parents=True, exist_ok=True)
            os.replace(plan.path, saved)
            completed.append((plan.path, saved))

        for plan in skill_plans:
            if apply.fingerprint_directory(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published skill fingerprint mismatch: {plan.target}")
        for plan in pi_plans:
            if _file_fingerprint(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published Pi resource fingerprint mismatch: {plan.target}")

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
        "pi",
        checkout,
        commit,
        checkout / MANIFEST_FILENAME,
        ownership_path,
        home / SHARED_SKILL_BASE,
        skill_plans,
        pi_plans,
        [],
        legacy_plans,
    )


def _sync_devin_checkout(
    checkout: Path, home: Path, app_data: Path | None = None
) -> SyncResult:
    checkout = checkout.resolve()
    home = home.resolve()
    devin_base = _resolve_devin_base(app_data)
    sources, commit = apply.load_sources(checkout)
    agent_sources = _load_devin_sources(checkout)

    ownership_path = global_state_path(home)
    state = load_global_state(ownership_path, home, devin_base)
    skill_plans = _build_devin_skill_plans(devin_base, sources, state)
    agent_plans = _build_devin_agent_plans(devin_base, agent_sources, state)
    retired_python = _build_retired_python_plans(home, sources, state, devin_base)
    managed_destinations = [plan.target for plan in skill_plans]
    managed_destinations.extend(plan.path for plan in retired_python)
    managed_destinations.extend(plan.target for plan in agent_plans)
    _ensure_real_parents(devin_base, managed_destinations)
    _ensure_real_parents(home, [ownership_path])

    prospective = json.loads(json.dumps(state))
    for plan in skill_plans:
        prospective["devin_skills"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }
    for plan in retired_python:
        prospective["devin_skills"].pop(plan.name, None)
    for plan in agent_plans:
        prospective["devin_agents"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }

    state_directory = ownership_path.parent
    state_directory.mkdir(parents=True, exist_ok=True)
    transaction = state_directory / f"transaction-{uuid.uuid4().hex}"
    stage = transaction / "stage"
    backup = transaction / "backup"
    completed: list[tuple[Path, Path | None]] = []
    try:
        (stage / "skills").mkdir(parents=True)
        (stage / "agents").mkdir(parents=True)
        backup.mkdir(parents=True)
        for plan in skill_plans:
            staged = stage / "skills" / plan.source.name
            shutil.copytree(plan.source.path, staged, symlinks=True)
            if apply.fingerprint_directory(staged) != plan.source.fingerprint:
                raise SyncError(f"Staged Devin skill fingerprint mismatch: {plan.source.name}")
        for plan in agent_plans:
            staged = stage / "agents" / f"{plan.source.name}.md"
            shutil.copy2(plan.source.path, staged)
            if _file_fingerprint(staged) != plan.source.fingerprint:
                raise SyncError(f"Staged Devin agent fingerprint mismatch: {plan.source.name}")

        current_state = load_global_state(ownership_path, home, devin_base)
        if current_state != state:
            raise SyncError(f"Global ownership state changed after preflight: {ownership_path}")
        if _build_devin_skill_plans(devin_base, sources, state) != skill_plans:
            raise SyncError("Devin skill targets changed during preflight")
        if _build_devin_agent_plans(devin_base, agent_sources, state) != agent_plans:
            raise SyncError("Devin agent targets changed during preflight")
        if _build_retired_python_plans(home, sources, state, devin_base) != retired_python:
            raise SyncError("Retired Devin Python targets changed during preflight")

        for plan in skill_plans:
            if plan.classification in {"unchanged", "adopted"}:
                continue
            plan.target.parent.mkdir(parents=True, exist_ok=True)
            saved: Path | None = None
            if apply._lexists(plan.target):
                saved = backup / "skills" / plan.source.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.target, saved)
            completed.append((plan.target, saved))
            os.replace(stage / "skills" / plan.source.name, plan.target)

        for plan in agent_plans:
            if plan.classification in {"unchanged", "adopted"}:
                continue
            plan.target.parent.mkdir(parents=True, exist_ok=True)
            saved = None
            if apply._lexists(plan.target):
                saved = backup / "agents" / f"{plan.source.name}.md"
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.target, saved)
            completed.append((plan.target, saved))
            os.replace(stage / "agents" / f"{plan.source.name}.md", plan.target)

        for plan in retired_python:
            if apply._lexists(plan.path):
                saved = backup / "retired-skills" / plan.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.path, saved)
                completed.append((plan.path, saved))

        for plan in skill_plans:
            if apply.fingerprint_directory(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published Devin skill fingerprint mismatch: {plan.target}")
        for plan in agent_plans:
            if _file_fingerprint(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published Devin agent fingerprint mismatch: {plan.target}")

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
        "devin",
        checkout,
        commit,
        checkout / MANIFEST_FILENAME,
        ownership_path,
        devin_base / "skills",
        skill_plans,
        [],
        agent_plans,
        retired_python,
    )


def _sync_opencode_checkout(checkout: Path, home: Path) -> SyncResult:
    checkout = checkout.resolve()
    home = home.resolve()
    sources, commit = apply.load_sources(checkout)

    ownership_path = global_state_path(home)
    state = load_global_state(ownership_path, home, _ambient_devin_base())
    skill_plans = _build_opencode_skill_plans(home, sources, state)
    retired_python = _build_retired_python_plans(
        home, sources, state, harness="opencode"
    )
    destinations = [plan.target for plan in skill_plans]
    destinations.extend(plan.path for plan in retired_python)
    destinations.append(ownership_path)
    _ensure_real_parents(home, destinations)

    prospective = json.loads(json.dumps(state))
    for plan in skill_plans:
        prospective["opencode_skills"][plan.source.name] = {
            "destination": _path_text(plan.target),
            "source_commit": commit,
            "fingerprint": plan.source.fingerprint,
        }
    for plan in retired_python:
        prospective["opencode_skills"].pop(plan.name, None)
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
                raise SyncError(f"Staged OpenCode skill fingerprint mismatch: {plan.source.name}")

        current_state = load_global_state(ownership_path, home, _ambient_devin_base())
        if current_state != state:
            raise SyncError(f"Global ownership state changed after preflight: {ownership_path}")
        if _build_opencode_skill_plans(home, sources, state) != skill_plans:
            raise SyncError("OpenCode skill targets changed during preflight")
        if _build_retired_python_plans(
            home, sources, state, harness="opencode"
        ) != retired_python:
            raise SyncError("Retired OpenCode Python targets changed during preflight")

        for plan in skill_plans:
            if plan.classification in {"unchanged", "adopted"}:
                continue
            plan.target.parent.mkdir(parents=True, exist_ok=True)
            saved: Path | None = None
            if apply._lexists(plan.target):
                saved = backup / "skills" / plan.source.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.target, saved)
            completed.append((plan.target, saved))
            os.replace(stage / "skills" / plan.source.name, plan.target)

        for plan in retired_python:
            if apply._lexists(plan.path):
                saved = backup / "retired-skills" / plan.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(plan.path, saved)
                completed.append((plan.path, saved))

        for plan in skill_plans:
            if apply.fingerprint_directory(plan.target) != plan.source.fingerprint:
                raise SyncError(f"Published OpenCode skill fingerprint mismatch: {plan.target}")

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
        "opencode",
        checkout,
        commit,
        checkout / MANIFEST_FILENAME,
        ownership_path,
        home / OPENCODE_SKILL_BASE,
        skill_plans,
        [],
        [],
        retired_python,
    )


def sync_checkout(
    checkout: Path,
    home: Path,
    harness: str = "pi",
    *,
    app_data: Path | None = None,
) -> SyncResult:
    if harness == "pi":
        return _sync_pi_checkout(checkout, home)
    if harness == "devin":
        return _sync_devin_checkout(checkout, home, app_data)
    if harness == "opencode":
        return _sync_opencode_checkout(checkout, home)
    raise SyncError(f"Unsupported harness: {harness}")


def print_result(result: SyncResult) -> None:
    print(f"agent-core sync: OK ({result.commit[:12]})")
    print(f"Harness: {result.harness}")
    print(f"Skills ({len(result.skills)}): " + (", ".join(p.source.name for p in result.skills) or "none"))
    if result.harness == "pi":
        for category in ("agents", "prompts"):
            plans = [p for p in result.pi_resources if p.source.category == category]
            print(f"{category.capitalize()} ({len(plans)}): " + (", ".join(p.source.name for p in plans) or "none"))
        if result.legacy:
            print(f"Migrated legacy entries: {len(result.legacy)}")
        print("Verified: ~/.pi/agent/{skills,agents,prompts} (global guidance untouched)")
    elif result.harness == "devin":
        print(
            f"Agents ({len(result.devin_resources)}): "
            + (", ".join(p.source.name for p in result.devin_resources) or "none")
        )
        if result.legacy:
            print(f"Retired Python skill entries: {len(result.legacy)}")
        print("Verified: %APPDATA%\\devin\\{skills,agents} (global guidance untouched)")
    else:
        if result.legacy:
            print(f"Retired Python skill entries: {len(result.legacy)}")
        print("Verified: ~/.config/opencode/skills (global guidance untouched)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal post-refresh Agent Core global sync implementation.")
    parser.add_argument("--checkout", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--harness", choices=("pi", "devin", "opencode"), default="pi")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = sync_checkout(Path(args.checkout), Path(args.home), args.harness)
    except (SyncError, apply.ApplyError) as exc:
        print(f"agent-core: error: {exc}", file=sys.stderr)
        return 1
    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
