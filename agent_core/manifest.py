from __future__ import annotations

import json
import re
from pathlib import Path


MANIFEST_FILENAME = "personal-skills.toml"
_ARRAY_START = re.compile(r"^skills\s*=\s*\[$")
_STRING_ITEM = re.compile(r'^("(?:[^"\\]|\\.)*")\s*,?$')


class ManifestError(ValueError):
    pass


def load_skill_names(path: Path) -> list[str]:
    """Parse Agent Core's deliberately small, dependency-free TOML subset."""
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ManifestError(f"Personal skill manifest is missing: {path}") from exc
    except OSError as exc:
        raise ManifestError(f"Could not read personal skill manifest {path}: {exc}") from exc

    lines = [line.strip() for line in raw_lines if line.strip() and not line.lstrip().startswith("#")]
    if len(lines) < 2 or not _ARRAY_START.fullmatch(lines[0]) or lines[-1] != "]":
        raise ManifestError(
            f"{MANIFEST_FILENAME} must contain only a top-level 'skills = [...]' string array"
        )

    names: list[str] = []
    for line in lines[1:-1]:
        match = _STRING_ITEM.fullmatch(line)
        if match is None:
            raise ManifestError(f"Invalid skill entry in {MANIFEST_FILENAME}: {line}")
        try:
            value = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise ManifestError(f"Invalid quoted skill name in {MANIFEST_FILENAME}: {line}") from exc
        if not isinstance(value, str):
            raise ManifestError(f"Skill names in {MANIFEST_FILENAME} must be strings")
        names.append(value)
    return names
