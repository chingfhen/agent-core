# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = 1
REGISTRY_VERSION = 1
SUPPORTED_SURFACES = {
    "claude": Path(".claude/skills"),
    "opencode": Path(".opencode/skills"),
}
DEFAULT_SURFACES = ("claude", "opencode")
DEFAULT_ENROLL_SKILLS = (
    "yagni-review",
    "yagni",
    "project-docs",
    "project-tasks",
    "manage-python-uv",
    "agent-os-memory",
    "grilling",
    "diagram-generation",
)
RETIRED_SKILLS = {
    "agent-os-bootstrap": (
        "Shared bootstrap was removed. Executor skills that need Agent OS context should read "
        ".agent-os.json directly."
    ),
}
REQUIRED_MANIFEST_KEYS = (
    "version",
    "repo_id",
    "scope",
    "scope_id",
    "agent_os_path",
    "memory_enabled",
)


@dataclass
class PlannedSkill:
    surface: str
    skill_name: str
    source_dir: Path
    target_dir: Path
    state: str
    detail: str
    live_updates: bool
    notice: str | None


@dataclass
class PlannedManifest:
    path: Path
    state: str
    detail: str


@dataclass
class PlannedRetiredSkill:
    surface: str
    skill_name: str
    target_dir: Path
    state: str
    detail: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def registry_path() -> Path:
    return repo_root() / ".agent-os-state" / "enrollments.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def path_lexists(path: Path) -> bool:
    try:
        path.stat(follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_file_manifest(path: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for child in sorted(path.rglob("*")):
        if child.is_file():
            manifest[child.relative_to(path).as_posix()] = file_hash(child)
    return manifest


def is_reparse_directory(path: Path) -> bool:
    if path.is_symlink() or not path_lexists(path):
        return False
    try:
        attributes = path.stat(follow_symlinks=False).st_file_attributes
    except (AttributeError, FileNotFoundError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT) and (path.is_dir() or not path.exists())


def read_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def parse_skill_name(skill_file: Path) -> str | None:
    in_frontmatter = False
    for line in skill_file.read_text(encoding="utf-8").splitlines():
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            break
        if in_frontmatter and line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None


def ensure_supported_surface(surface: str) -> None:
    if surface not in SUPPORTED_SURFACES:
        choices = ", ".join(sorted(SUPPORTED_SURFACES))
        raise SystemExit(f"Unsupported surface '{surface}'. Supported surfaces: {choices}")


def ensure_skill_source(agent_os_path: Path, skill_name: str) -> Path:
    skill_dir = agent_os_path / "skills" / skill_name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise SystemExit(f"Canonical skill not found: {skill_file}")
    return skill_dir


def split_retired_skills(skills: list[str]) -> tuple[list[str], list[str]]:
    active: list[str] = []
    retired: list[str] = []
    for skill_name in dedupe(skills):
        if skill_name in RETIRED_SKILLS:
            retired.append(skill_name)
        else:
            active.append(skill_name)
    return active, retired


def normalize_surfaces(surfaces: list[str]) -> list[str]:
    normalized = dedupe(surfaces)
    for surface in normalized:
        ensure_supported_surface(surface)
    for surface in DEFAULT_SURFACES:
        if surface not in normalized:
            normalized.append(surface)
    return normalized


def classify_manifest(manifest_path: Path, agent_os_path: Path) -> PlannedManifest:
    if not path_lexists(manifest_path):
        return PlannedManifest(manifest_path, "missing", "manifest does not exist yet")

    payload = read_json(manifest_path)
    if not isinstance(payload, dict):
        return PlannedManifest(manifest_path, "conflict", "existing manifest is not valid JSON")

    missing_keys = [key for key in REQUIRED_MANIFEST_KEYS if key not in payload]
    if missing_keys:
        return PlannedManifest(
            manifest_path,
            "conflict",
            "existing manifest is missing required keys: " + ", ".join(missing_keys),
        )

    recorded_agent_os_path = str(payload.get("agent_os_path", ""))
    if recorded_agent_os_path != str(agent_os_path):
        return PlannedManifest(
            manifest_path,
            "conflict",
            f"manifest points at a different Agent OS repo: {recorded_agent_os_path}",
        )

    return PlannedManifest(manifest_path, "managed", "existing manifest belongs to this Agent OS repo")


def classify_skill_target(
    *,
    target_dir: Path,
    source_dir: Path,
    skill_name: str,
) -> tuple[str, str, bool, str | None]:
    if not path_lexists(target_dir):
        return ("missing", "skill alias path does not exist yet", False, None)

    if target_dir.is_symlink():
        try:
            resolved = target_dir.resolve(strict=True)
        except FileNotFoundError:
            return ("conflict", "skill alias is a broken symlink", False, None)
        if resolved == source_dir.resolve():
            return ("managed", "symlink already points at the canonical skill", True, None)
        return ("conflict", f"symlink points at a different target: {resolved}", False, None)

    if is_reparse_directory(target_dir):
        try:
            resolved = target_dir.resolve(strict=True)
        except FileNotFoundError:
            return ("conflict", "skill alias is a broken junction", False, None)
        if resolved == source_dir.resolve():
            return ("managed", "junction already points at the canonical skill", True, None)
        return ("conflict", f"junction points at a different target: {resolved}", False, None)

    if target_dir.is_file():
        return ("conflict", "skill alias path is a file", False, None)

    if not target_dir.is_dir():
        return ("conflict", "skill alias path uses an unsupported filesystem type", False, None)

    skill_file = target_dir / "SKILL.md"
    if not skill_file.is_file():
        entries = sorted(child.name for child in target_dir.iterdir())
        return (
            "conflict",
            "skill directory does not contain SKILL.md; entries: " + ", ".join(entries[:5]),
            False,
            None,
        )

    local_skill_name = parse_skill_name(skill_file)
    if local_skill_name != skill_name:
        return (
            "conflict",
            f"skill directory declares a different skill name: {local_skill_name or 'missing'}",
            False,
            None,
        )

    source_manifest = directory_file_manifest(source_dir)
    target_manifest = directory_file_manifest(target_dir)
    if target_manifest == source_manifest:
        return (
            "managed",
            "existing local skill copy matches the canonical source and will be replaced with a live alias on apply",
            False,
            f"{target_dir} is a copied skill directory, not a live alias. Enroll/sync will replace it.",
        )

    return (
        "managed",
        "existing local skill copy differs from the canonical source and will be replaced with a live alias on apply",
        False,
        f"{target_dir} diverged from canonical and will be auto-replaced with the live alias.",
    )


def classify_retired_skill_target(target_dir: Path, skill_name: str, agent_os_path: Path) -> tuple[str, str]:
    expected_source_dir = (agent_os_path / "skills" / skill_name).resolve()
    if not path_lexists(target_dir):
        return ("missing", "retired skill alias path does not exist")

    if target_dir.is_symlink():
        try:
            resolved = target_dir.resolve(strict=True)
        except FileNotFoundError:
            return ("managed", "retired skill alias is a broken symlink and will be removed on sync")
        if resolved == expected_source_dir:
            return ("managed", "retired skill alias points at the canonical retired skill and will be removed on sync")
        return ("conflict", f"skill alias path is a symlink to a different target: {resolved}")

    if is_reparse_directory(target_dir):
        try:
            resolved = target_dir.resolve(strict=True)
        except FileNotFoundError:
            return ("managed", "retired skill alias is a broken junction and will be removed on sync")
        if resolved == expected_source_dir:
            return ("managed", "retired skill alias points at the canonical retired skill and will be removed on sync")
        return ("conflict", f"skill alias path is a junction to a different target: {resolved}")

    if target_dir.is_file():
        return ("conflict", "retired skill alias path is a file")

    if not target_dir.is_dir():
        return ("conflict", "retired skill alias path uses an unsupported filesystem type")

    skill_file = target_dir / "SKILL.md"
    if not skill_file.is_file():
        entries = sorted(child.name for child in target_dir.iterdir())
        return (
            "conflict",
            "retired skill directory does not contain SKILL.md; entries: " + ", ".join(entries[:5]),
        )

    local_skill_name = parse_skill_name(skill_file)
    if local_skill_name == skill_name:
        return ("managed", "retired local skill copy will be removed on sync")

    return (
        "conflict",
        f"retired skill directory declares a different skill name: {local_skill_name or 'missing'}",
    )


def build_manifest_payload(
    *,
    repo_id: str,
    scope: str,
    scope_id: str,
    agent_os_path: Path,
    memory_enabled: bool,
) -> dict:
    return {
        "version": MANIFEST_VERSION,
        "repo_id": repo_id,
        "scope": scope,
        "scope_id": scope_id,
        "agent_os_path": str(agent_os_path),
        "memory_enabled": memory_enabled,
    }


def render_manifest(payload: dict) -> str:
    return json.dumps(payload, indent=2) + "\n"


def managed_ignore_entries(skills: list[str], surfaces: list[str]) -> list[str]:
    entries = ["/.agent-os.json"]
    for surface in surfaces:
        base = SUPPORTED_SURFACES[surface]
        for skill_name in skills:
            entries.append("/" + (base / skill_name).as_posix())
    return entries


def normalize_ignore_line(line: str) -> str:
    return line.strip().replace("\\", "/")


def is_comment_or_blank(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def existing_ignore_covers(line: str, desired: str) -> bool:
    pattern = normalize_ignore_line(line)
    if is_comment_or_blank(pattern) or pattern.startswith("!"):
        return False

    pattern = pattern.lstrip("/")
    desired_clean = normalize_ignore_line(desired).lstrip("/").rstrip("/")
    if pattern.rstrip("/") == desired_clean:
        return True

    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return desired_clean == prefix or desired_clean.startswith(prefix + "/")

    if pattern.endswith("/*"):
        prefix = pattern[:-2].rstrip("/")
        if not desired_clean.startswith(prefix + "/"):
            return False
        remainder = desired_clean[len(prefix) + 1 :]
        return remainder != "" and "/" not in remainder

    if pattern.endswith("/"):
        prefix = pattern.rstrip("/")
        return desired_clean == prefix or desired_clean.startswith(prefix + "/")

    return False


def update_gitignore(repo_path: Path, desired_entries: list[str], dry_run: bool) -> list[str]:
    ignore_path = repo_path / ".gitignore"
    existing_text = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    existing_lines = existing_text.splitlines()
    new_entries = [entry for entry in desired_entries if not any(existing_ignore_covers(line, entry) for line in existing_lines)]

    if not new_entries or dry_run:
        return new_entries

    new_block = "\n".join(new_entries)
    if existing_text and not existing_text.endswith(("\n", "\r")):
        existing_text += "\n"
    if existing_text:
        existing_text += new_block + "\n"
    else:
        existing_text = new_block + "\n"
    ignore_path.write_text(existing_text, encoding="utf-8")
    return new_entries


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if is_reparse_directory(path):
        path.rmdir()
        return
    if path.is_dir():
        shutil.rmtree(path)
        return
    if not path_lexists(path):
        return
    raise RuntimeError(f"Cannot remove unsupported path type: {path}")


def create_junction(source_dir: Path, target_dir: Path) -> None:
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(target_dir), str(source_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or f"exit code {result.returncode}"
        raise SystemExit(f"Failed to create a directory junction for {target_dir}: {detail}")


def create_directory_link(source_dir: Path, target_dir: Path, link_mode: str) -> str:
    if link_mode in {"auto", "symlink"}:
        try:
            os.symlink(str(source_dir), str(target_dir), target_is_directory=True)
            return "symlink"
        except OSError as exc:
            if link_mode == "symlink" or os.name != "nt" or getattr(exc, "winerror", None) != 1314:
                raise SystemExit(
                    "Failed to create a directory symlink. "
                    "Windows Developer Mode or equivalent symlink permissions are required. "
                    f"Target: {target_dir} Error: {exc}"
                ) from exc

    if link_mode in {"auto", "junction"} and os.name == "nt":
        create_junction(source_dir, target_dir)
        return "junction"

    raise SystemExit(f"Unsupported link mode '{link_mode}' for target {target_dir}")


def install_skill_alias(planned_skill: PlannedSkill, dry_run: bool, link_mode: str) -> str:
    if dry_run:
        return link_mode

    planned_skill.target_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_target = planned_skill.target_dir.parent / f".{planned_skill.target_dir.name}.agent-os-tmp"
    if path_lexists(temp_target):
        remove_path(temp_target)

    actual_link_mode = create_directory_link(planned_skill.source_dir, temp_target, link_mode)
    try:
        if path_lexists(planned_skill.target_dir):
            remove_path(planned_skill.target_dir)
        temp_target.replace(planned_skill.target_dir)
    except Exception:
        if path_lexists(temp_target):
            remove_path(temp_target)
        raise
    return actual_link_mode


def load_registry() -> dict:
    path = registry_path()
    payload = read_json(path)
    if not isinstance(payload, dict):
        return {"version": REGISTRY_VERSION, "device_defaults": {}, "enrollments": {}}
    device_defaults = payload.get("device_defaults")
    if not isinstance(device_defaults, dict):
        device_defaults = {}
    enrollments = payload.get("enrollments")
    if not isinstance(enrollments, dict):
        enrollments = {}
    return {"version": REGISTRY_VERSION, "device_defaults": device_defaults, "enrollments": enrollments}


def save_registry(payload: dict, dry_run: bool) -> None:
    if dry_run:
        return
    path = registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_skill_plan(
    *,
    repo_path: Path,
    agent_os_path: Path,
    skills: list[str],
    surfaces: list[str],
) -> list[PlannedSkill]:
    planned: list[PlannedSkill] = []
    for surface in surfaces:
        ensure_supported_surface(surface)
        for skill_name in skills:
            source_dir = ensure_skill_source(agent_os_path, skill_name)
            target_dir = repo_path / SUPPORTED_SURFACES[surface] / skill_name
            state, detail, live_updates, notice = classify_skill_target(
                target_dir=target_dir,
                source_dir=source_dir,
                skill_name=skill_name,
            )
            planned.append(
                PlannedSkill(
                    surface=surface,
                    skill_name=skill_name,
                    source_dir=source_dir,
                    target_dir=target_dir,
                    state=state,
                    detail=detail,
                    live_updates=live_updates,
                    notice=notice,
                )
            )
    return planned


def build_retired_skill_plan(
    *,
    repo_path: Path,
    agent_os_path: Path,
    skills: list[str],
    surfaces: list[str],
) -> list[PlannedRetiredSkill]:
    planned: list[PlannedRetiredSkill] = []
    for surface in surfaces:
        ensure_supported_surface(surface)
        for skill_name in skills:
            target_dir = repo_path / SUPPORTED_SURFACES[surface] / skill_name
            state, detail = classify_retired_skill_target(target_dir, skill_name, agent_os_path)
            planned.append(
                PlannedRetiredSkill(
                    surface=surface,
                    skill_name=skill_name,
                    target_dir=target_dir,
                    state=state,
                    detail=detail,
                )
            )
    return planned


def write_manifest(manifest_path: Path, payload: dict, dry_run: bool) -> None:
    if dry_run:
        return
    manifest_path.write_text(render_manifest(payload), encoding="utf-8")


def apply_retired_skill_cleanup(retired_skill_plan: list[PlannedRetiredSkill], dry_run: bool) -> None:
    if dry_run:
        return
    for item in retired_skill_plan:
        if item.state == "managed" and path_lexists(item.target_dir):
            remove_path(item.target_dir)


def has_conflicts(
    manifest_plan: PlannedManifest,
    skill_plan: list[PlannedSkill],
    retired_skill_plan: list[PlannedRetiredSkill],
) -> bool:
    if manifest_plan.state == "conflict":
        return True
    return any(item.state == "conflict" for item in skill_plan) or any(
        item.state == "conflict" for item in retired_skill_plan
    )


def print_plan(
    *,
    repo_path: Path,
    manifest_plan: PlannedManifest,
    skill_plan: list[PlannedSkill],
    retired_skill_plan: list[PlannedRetiredSkill],
    new_ignore_entries: list[str],
    git_repo_detected: bool,
    dry_run: bool,
) -> None:
    mode = "DRY RUN" if dry_run else "APPLY"
    print(f"[{mode}] Repo: {repo_path}")
    print(f"Manifest: {manifest_plan.state} - {manifest_plan.detail}")
    print(f"Git repo detected: {'yes' if git_repo_detected else 'no'}")
    print("Skill aliases:")
    for item in skill_plan:
        live_flag = "yes" if item.live_updates else "no"
        print(f"  - {item.surface}:{item.skill_name}: {item.state} - {item.detail} [live updates: {live_flag}]")
    if retired_skill_plan:
        print("Retired skill aliases:")
        for item in retired_skill_plan:
            print(f"  - {item.surface}:{item.skill_name}: {item.state} - {item.detail}")
    if new_ignore_entries:
        print("Gitignore additions:")
        for entry in new_ignore_entries:
            print(f"  - {entry}")
    else:
        print("Gitignore additions: none")
    notices = [item.notice for item in skill_plan if item.notice]
    if notices:
        print("Notices:")
        for notice in notices:
            print(f"  - {notice}")


def live_update_guarantee(
    manifest_plan: PlannedManifest,
    skill_plan: list[PlannedSkill],
    retired_skill_plan: list[PlannedRetiredSkill],
) -> bool:
    if manifest_plan.state != "managed":
        return False
    if retired_skill_plan:
        return False
    return all(item.state == "managed" and item.live_updates for item in skill_plan)


def update_registry_entry(
    *,
    repo_path: Path,
    manifest_payload: dict,
    skills: list[str],
    surfaces: list[str],
    manage_ignore: bool,
    link_mode: str,
    device_link_mode_default: str | None,
    dry_run: bool,
) -> None:
    registry = load_registry()
    if device_link_mode_default is not None:
        registry["device_defaults"]["link_mode"] = device_link_mode_default
    registry["enrollments"][str(repo_path)] = {
        "repo_path": str(repo_path),
        "manifest_path": str(repo_path / ".agent-os.json"),
        "repo_id": manifest_payload["repo_id"],
        "scope": manifest_payload["scope"],
        "scope_id": manifest_payload["scope_id"],
        "agent_os_path": manifest_payload["agent_os_path"],
        "memory_enabled": manifest_payload["memory_enabled"],
        "skills": skills,
        "surfaces": surfaces,
        "manage_ignore": manage_ignore,
        "link_mode": link_mode,
        "updated_at": now_iso(),
    }
    save_registry(registry, dry_run=dry_run)


def perform_enroll(args: argparse.Namespace) -> int:
    agent_os_path = repo_root()
    repo_path = Path(args.repo).resolve()
    if not repo_path.is_dir():
        raise SystemExit(f"Repo path does not exist: {repo_path}")
    registry = load_registry()

    requested_skills = dedupe([*DEFAULT_ENROLL_SKILLS, *args.skill])
    skills, retired_skills = split_retired_skills(requested_skills)
    if not skills:
        raise SystemExit("At least one supported --skill is required")

    surfaces = normalize_surfaces(args.surface)
    requested_link_mode = args.link_mode
    if requested_link_mode == "auto":
        requested_link_mode = str(registry.get("device_defaults", {}).get("link_mode", "auto"))
    repo_id = args.repo_id or repo_path.name
    scope = args.scope
    scope_id = args.scope_id or repo_id
    manifest_payload = build_manifest_payload(
        repo_id=repo_id,
        scope=scope,
        scope_id=scope_id,
        agent_os_path=agent_os_path,
        memory_enabled=args.memory_enabled,
    )

    manifest_path = repo_path / ".agent-os.json"
    manifest_plan = classify_manifest(manifest_path, agent_os_path)
    skill_plan = build_skill_plan(
        repo_path=repo_path,
        agent_os_path=agent_os_path,
        skills=skills,
        surfaces=surfaces,
    )
    retired_skill_plan = build_retired_skill_plan(
        repo_path=repo_path,
        agent_os_path=agent_os_path,
        skills=retired_skills,
        surfaces=surfaces,
    )

    if has_conflicts(manifest_plan, skill_plan, retired_skill_plan):
        print_plan(
            repo_path=repo_path,
            manifest_plan=manifest_plan,
            skill_plan=skill_plan,
            retired_skill_plan=retired_skill_plan,
            new_ignore_entries=[],
            git_repo_detected=(repo_path / ".git").exists(),
            dry_run=True,
        )
        print("Conflicts detected. Re-run with explicit approval or repair the conflicting paths first.")
        return 2

    new_ignore_entries: list[str] = []
    if args.manage_ignore:
        ignore_entries = managed_ignore_entries(skills, surfaces)
        new_ignore_entries = update_gitignore(repo_path, ignore_entries, dry_run=args.dry_run)

    print_plan(
        repo_path=repo_path,
        manifest_plan=manifest_plan,
        skill_plan=skill_plan,
        retired_skill_plan=retired_skill_plan,
        new_ignore_entries=new_ignore_entries,
        git_repo_detected=(repo_path / ".git").exists(),
        dry_run=args.dry_run,
    )
    for skill_name in retired_skills:
        print(f"Notice: {skill_name} is retired and will not be installed. {RETIRED_SKILLS[skill_name]}")

    if args.dry_run:
        return 0

    write_manifest(manifest_path, manifest_payload, dry_run=False)
    apply_retired_skill_cleanup(retired_skill_plan, dry_run=False)
    actual_link_mode = requested_link_mode
    for planned_skill in skill_plan:
        previous_link_mode = actual_link_mode
        actual_link_mode = install_skill_alias(planned_skill, dry_run=False, link_mode=actual_link_mode)
        if previous_link_mode == "auto" and actual_link_mode in {"symlink", "junction"}:
            print(f"Notice: Remaining installs will use link mode '{actual_link_mode}'.")
    update_registry_entry(
        repo_path=repo_path,
        manifest_payload=manifest_payload,
        skills=skills,
        surfaces=surfaces,
        manage_ignore=args.manage_ignore,
        link_mode=actual_link_mode,
        device_link_mode_default=actual_link_mode if args.link_mode == "auto" and actual_link_mode in {"symlink", "junction"} else None,
        dry_run=False,
    )
    return 0


def perform_sync(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo).resolve()
    registry = load_registry()
    enrollment = registry["enrollments"].get(str(repo_path))
    if not isinstance(enrollment, dict):
        raise SystemExit(f"No enrollment record found for repo: {repo_path}")

    manifest_payload = build_manifest_payload(
        repo_id=enrollment["repo_id"],
        scope=enrollment["scope"],
        scope_id=enrollment["scope_id"],
        agent_os_path=repo_root(),
        memory_enabled=bool(enrollment["memory_enabled"]),
    )
    skills, retired_skills = split_retired_skills(list(enrollment["skills"]))
    surfaces = normalize_surfaces(list(enrollment.get("surfaces", [])))
    manage_ignore = bool(enrollment.get("manage_ignore", True))
    link_mode = args.link_mode or str(enrollment.get("link_mode", "auto"))
    manifest_path = repo_path / ".agent-os.json"
    manifest_plan = classify_manifest(manifest_path, repo_root())
    skill_plan = build_skill_plan(
        repo_path=repo_path,
        agent_os_path=repo_root(),
        skills=skills,
        surfaces=surfaces,
    )
    retired_skill_plan = build_retired_skill_plan(
        repo_path=repo_path,
        agent_os_path=repo_root(),
        skills=retired_skills,
        surfaces=surfaces,
    )

    if has_conflicts(manifest_plan, skill_plan, retired_skill_plan):
        print_plan(
            repo_path=repo_path,
            manifest_plan=manifest_plan,
            skill_plan=skill_plan,
            retired_skill_plan=retired_skill_plan,
            new_ignore_entries=[],
            git_repo_detected=(repo_path / ".git").exists(),
            dry_run=True,
        )
        print("Conflicts detected. Re-run with explicit approval or repair the conflicting paths first.")
        return 2

    new_ignore_entries: list[str] = []
    if manage_ignore:
        ignore_entries = managed_ignore_entries(skills, surfaces)
        new_ignore_entries = update_gitignore(repo_path, ignore_entries, dry_run=args.dry_run)

    print_plan(
        repo_path=repo_path,
        manifest_plan=manifest_plan,
        skill_plan=skill_plan,
        retired_skill_plan=retired_skill_plan,
        new_ignore_entries=new_ignore_entries,
        git_repo_detected=(repo_path / ".git").exists(),
        dry_run=args.dry_run,
    )
    for skill_name in retired_skills:
        print(f"Notice: Sync will remove retired skill '{skill_name}'. {RETIRED_SKILLS[skill_name]}")

    if args.dry_run:
        return 0

    write_manifest(manifest_path, manifest_payload, dry_run=False)
    apply_retired_skill_cleanup(retired_skill_plan, dry_run=False)
    actual_link_mode = link_mode
    for planned_skill in skill_plan:
        previous_link_mode = actual_link_mode
        actual_link_mode = install_skill_alias(planned_skill, dry_run=False, link_mode=actual_link_mode)
        if previous_link_mode == "auto" and actual_link_mode in {"symlink", "junction"}:
            print(f"Notice: Remaining installs will use link mode '{actual_link_mode}'.")
    update_registry_entry(
        repo_path=repo_path,
        manifest_payload=manifest_payload,
        skills=skills,
        surfaces=surfaces,
        manage_ignore=manage_ignore,
        link_mode=actual_link_mode,
        device_link_mode_default=None,
        dry_run=False,
    )
    return 0


def perform_verify(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo).resolve()
    registry = load_registry()
    enrollment = registry["enrollments"].get(str(repo_path))
    if not isinstance(enrollment, dict):
        raise SystemExit(f"No enrollment record found for repo: {repo_path}")

    skills, retired_skills = split_retired_skills(list(enrollment["skills"]))
    surfaces = normalize_surfaces(list(enrollment.get("surfaces", [])))
    manifest_plan = classify_manifest(repo_path / ".agent-os.json", repo_root())
    skill_plan = build_skill_plan(
        repo_path=repo_path,
        agent_os_path=repo_root(),
        skills=skills,
        surfaces=surfaces,
    )
    retired_skill_plan = build_retired_skill_plan(
        repo_path=repo_path,
        agent_os_path=repo_root(),
        skills=retired_skills,
        surfaces=surfaces,
    )
    print_plan(
        repo_path=repo_path,
        manifest_plan=manifest_plan,
        skill_plan=skill_plan,
        retired_skill_plan=retired_skill_plan,
        new_ignore_entries=[],
        git_repo_detected=(repo_path / ".git").exists(),
        dry_run=True,
    )
    for skill_name in retired_skills:
        print(f"Notice: Retired skill '{skill_name}' is still recorded for this repo. Run sync to remove it.")
    guarantee = live_update_guarantee(manifest_plan, skill_plan, retired_skill_plan)
    print(f"Live update guarantee: {'yes' if guarantee else 'no'}")
    if not guarantee:
        print("Run enroll or sync to replace copied skill directories, remove retired skill aliases, and repair any missing links.")
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Enroll, repair, and verify consumer repos for Agent OS local skill aliases.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    enroll = subparsers.add_parser("enroll", help="Write the manifest and install skill aliases.")
    enroll.add_argument("--repo", required=True, help="Path to the consumer repo.")
    enroll.add_argument("--repo-id", help="Repo identifier for .agent-os.json. Defaults to the folder name.")
    enroll.add_argument("--scope", default="repo", help="Manifest scope. Defaults to 'repo'.")
    enroll.add_argument("--scope-id", help="Manifest scope identifier. Defaults to repo_id.")
    enroll.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Additional canonical skill to install. Repeat for multiple skills. Default skills are enrolled automatically.",
    )
    enroll.add_argument(
        "--surface",
        action="append",
        default=[],
        help="Repo-local skill surface to manage. Steward sync converges enrollments onto both 'claude' and 'opencode'.",
    )
    enroll.add_argument(
        "--memory-enabled",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Set memory_enabled in the manifest. Disabled by default.",
    )
    enroll.add_argument(
        "--manage-ignore",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Update repo-local ignore rules for steward-managed outputs. Enabled by default.",
    )
    enroll.add_argument(
        "--link-mode",
        choices=("auto", "symlink", "junction"),
        default="auto",
        help="Link strategy for installed skill aliases. Defaults to auto.",
    )
    enroll.add_argument(
        "--force",
        action="store_true",
        help="Deprecated compatibility flag. Matching local skill directories are auto-replaced by default.",
    )
    enroll.add_argument("--dry-run", action="store_true", help="Print the plan without changing files.")
    enroll.set_defaults(func=perform_enroll)

    sync = subparsers.add_parser("sync", help="Repair a previously enrolled repo from the local registry.")
    sync.add_argument("--repo", required=True, help="Path to the enrolled consumer repo.")
    sync.add_argument(
        "--link-mode",
        choices=("auto", "symlink", "junction"),
        help="Override the recorded link strategy for this repair run.",
    )
    sync.add_argument(
        "--force",
        action="store_true",
        help="Deprecated compatibility flag. Matching local skill directories are auto-replaced by default.",
    )
    sync.add_argument("--dry-run", action="store_true", help="Print the repair plan without changing files.")
    sync.set_defaults(func=perform_sync)

    verify = subparsers.add_parser("verify", help="Check whether enrolled skills are live aliases that receive canonical updates immediately.")
    verify.add_argument("--repo", required=True, help="Path to the enrolled consumer repo.")
    verify.set_defaults(func=perform_verify)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
