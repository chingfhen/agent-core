from __future__ import annotations

import json
import re
from pathlib import Path

DEVIN_MANIFEST_FILENAME = "personal-devin.toml"
_ARRAY_START = re.compile(r"^agents\s*=\s*\[$")
_STRING_ITEM = re.compile(r'^("(?:[^"\\]|\\.)*")\s*,?$')


class DevinManifestError(ValueError):
    pass


def load_devin_names(path: Path) -> list[str]:
    """Parse Agent Core's narrow, dependency-free Devin manifest."""
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise DevinManifestError(f"Devin manifest is missing: {path}") from exc
    except OSError as exc:
        raise DevinManifestError(f"Could not read Devin manifest {path}: {exc}") from exc

    lines = [line.strip() for line in raw_lines if line.strip() and not line.lstrip().startswith("#")]
    if len(lines) < 2 or not _ARRAY_START.fullmatch(lines[0]) or lines[-1] != "]":
        raise DevinManifestError(
            f"{DEVIN_MANIFEST_FILENAME} must contain only a top-level 'agents = [...]' string array"
        )

    names: list[str] = []
    for line in lines[1:-1]:
        match = _STRING_ITEM.fullmatch(line)
        if match is None:
            raise DevinManifestError(f"Invalid agent entry in {DEVIN_MANIFEST_FILENAME}: {line}")
        try:
            value = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise DevinManifestError(
                f"Invalid quoted agent name in {DEVIN_MANIFEST_FILENAME}: {line}"
            ) from exc
        if not isinstance(value, str):
            raise DevinManifestError(f"Agent names in {DEVIN_MANIFEST_FILENAME} must be strings")
        names.append(value)
    return names
