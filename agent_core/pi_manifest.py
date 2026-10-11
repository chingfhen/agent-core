from __future__ import annotations

import json
import re
from pathlib import Path

PI_MANIFEST_FILENAME = "personal-pi.toml"
_ARRAY_START = re.compile(r"^(agents|prompts)\s*=\s*\[$")
_STRING_ITEM = re.compile(r'^("(?:[^"\\]|\\.)*")\s*,?$')


class PiManifestError(ValueError):
    pass


def load_pi_names(path: Path) -> dict[str, list[str]]:
    """Parse a deliberately narrow Python 3.10-compatible two-array TOML manifest."""
    try:
        raw = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise PiManifestError(f"Cannot read {PI_MANIFEST_FILENAME}: {exc}") from exc

    lines = [s.strip() for s in raw if s.strip() and not s.lstrip().startswith("#")]
    result: dict[str, list[str]] = {}
    index = 0
    while index < len(lines):
        match = _ARRAY_START.fullmatch(lines[index])
        if match is None or match.group(1) in result:
            raise PiManifestError(f"{PI_MANIFEST_FILENAME} must contain unique agents and prompts arrays")
        category = match.group(1)
        index += 1
        names: list[str] = []
        while index < len(lines) and lines[index] != "]":
            item = _STRING_ITEM.fullmatch(lines[index])
            if item is None:
                raise PiManifestError(f"Invalid entry in {PI_MANIFEST_FILENAME}: {lines[index]}")
            try:
                name = json.loads(item.group(1))
            except json.JSONDecodeError as exc:
                raise PiManifestError(f"Invalid quoted entry in {PI_MANIFEST_FILENAME}") from exc
            if not isinstance(name, str):
                raise PiManifestError(f"{PI_MANIFEST_FILENAME} entries must be strings")
            names.append(name)
            index += 1
        if index == len(lines):
            raise PiManifestError(f"Unclosed array in {PI_MANIFEST_FILENAME}")
        result[category] = names
        index += 1
    if set(result) != {"agents", "prompts"}:
        raise PiManifestError(f"{PI_MANIFEST_FILENAME} requires agents and prompts arrays")
    return result
