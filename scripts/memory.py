# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from uuid import UUID, uuid4

VALID_SCOPES = ("global", "personal", "repo", "experiment")
TOPIC_KEY_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class UserError(Exception):
    pass


@dataclass(frozen=True)
class MemoryRecord:
    id: str
    created_at: str
    scope: str
    scope_id: str | None
    topic_key: str
    content: str
    keywords: tuple[str, ...]
    line_number: int


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ledger_path() -> Path:
    return repo_root() / "memory" / "memories.jsonl"


def sqlite_path() -> Path:
    return repo_root() / "memory" / "memory.sqlite"


def memory_index_path() -> Path:
    return repo_root() / "MEMORY_INDEX.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_memory_store() -> None:
    ledger = ledger_path()
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        ledger.write_text("", encoding="utf-8")


def scope_label(scope: str, scope_id: str | None) -> str:
    return f"{scope}:{scope_id}" if scope_id else scope


def preview_text(content: str, limit: int = 96) -> str:
    first_line = next((line.strip() for line in content.splitlines() if line.strip()), "")
    if not first_line:
        return "(blank)"
    if len(first_line) <= limit:
        return first_line
    return first_line[: limit - 3].rstrip() + "..."


def normalize_scope(scope: str, scope_id: str | None) -> tuple[str, str | None]:
    normalized_scope = scope.strip().lower()
    if normalized_scope not in VALID_SCOPES:
        choices = ", ".join(VALID_SCOPES)
        raise UserError(f"Invalid scope '{scope}'. Action: retry with one of: {choices}.")

    normalized_scope_id = scope_id.strip() if scope_id is not None and scope_id.strip() else None
    if normalized_scope in {"repo", "experiment"} and not normalized_scope_id:
        raise UserError(f"Scope '{normalized_scope}' requires --scope-id.")
    return normalized_scope, normalized_scope_id


def normalize_topic_key(topic_key: str) -> str:
    normalized = topic_key.strip().lower()
    if not normalized:
        raise UserError("Topic keys cannot be blank.")
    if not TOPIC_KEY_PATTERN.fullmatch(normalized):
        raise UserError(
            "Invalid topic_key. Action: use lowercase letters, numbers, underscores, or hyphens only."
        )
    return normalized


def normalize_keywords(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        for part in value.split(","):
            keyword = part.strip().lower()
            if not keyword or keyword in seen:
                continue
            seen.add(keyword)
            normalized.append(keyword)
    return tuple(normalized)


def read_content(args: argparse.Namespace) -> str:
    if bool(args.content) == bool(args.content_file):
        raise UserError("Provide exactly one of --content or --content-file.")
    if args.content_file:
        try:
            content = Path(args.content_file).read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise UserError(
                f"Content file not found: {args.content_file}. Action: verify the file path exists, or retry with --content."
            ) from exc
    else:
        content = args.content
    if not isinstance(content, str) or not content.strip():
        raise UserError("Memory content cannot be blank.")
    return content.rstrip()


def validate_uuid(value: str, line_number: int) -> str:
    try:
        parsed = UUID(value)
    except ValueError as exc:
        raise UserError(
            f"Ledger line {line_number} has an invalid memory id '{value}'. Action: repair that JSONL row before retrying."
        ) from exc
    return str(parsed)


def record_from_payload(payload: object, line_number: int) -> MemoryRecord:
    if not isinstance(payload, dict):
        raise UserError(
            f"Ledger line {line_number} is not a JSON object. Action: repair that JSONL row before retrying."
        )

    required_fields = ("id", "created_at", "scope", "scope_id", "topic_key", "content", "keywords")
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise UserError(
            f"Ledger line {line_number} is missing required fields: {', '.join(missing)}. "
            "Action: repair that JSONL row before retrying."
        )

    record_id = validate_uuid(str(payload["id"]), line_number)
    created_at = payload["created_at"]
    if not isinstance(created_at, str):
        raise UserError(
            f"Ledger line {line_number} has a non-string created_at value. Action: repair that JSONL row before retrying."
        )
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise UserError(
            f"Ledger line {line_number} has an invalid created_at value '{created_at}'. "
            "Action: repair that JSONL row before retrying."
        ) from exc

    scope, scope_id = normalize_scope(str(payload["scope"]), None if payload["scope_id"] is None else str(payload["scope_id"]))
    topic_key = normalize_topic_key(str(payload["topic_key"]))

    content = payload["content"]
    if not isinstance(content, str) or not content.strip():
        raise UserError(
            f"Ledger line {line_number} has blank content. Action: repair that JSONL row before retrying."
        )

    keywords_payload = payload["keywords"]
    if not isinstance(keywords_payload, list) or any(not isinstance(item, str) for item in keywords_payload):
        raise UserError(
            f"Ledger line {line_number} has invalid keywords. Action: repair that JSONL row before retrying."
        )

    return MemoryRecord(
        id=record_id,
        created_at=created_at,
        scope=scope,
        scope_id=scope_id,
        topic_key=topic_key,
        content=content.rstrip(),
        keywords=normalize_keywords(keywords_payload),
        line_number=line_number,
    )


def load_records() -> list[MemoryRecord]:
    ensure_memory_store()
    records: list[MemoryRecord] = []
    ledger = ledger_path()
    with ledger.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue
            try:
                payload = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise UserError(
                    f"Ledger line {line_number} is not valid JSON. Action: repair that JSONL row before retrying."
                ) from exc
            records.append(record_from_payload(payload, line_number))
    return records


def latest_by_topic(records: Iterable[MemoryRecord]) -> dict[tuple[str, str | None, str], MemoryRecord]:
    latest: dict[tuple[str, str | None, str], MemoryRecord] = {}
    for record in records:
        latest[(record.scope, record.scope_id, record.topic_key)] = record
    return latest


def rebuild_sqlite(records: list[MemoryRecord]) -> None:
    target = sqlite_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_target = target.with_suffix(".sqlite.tmp")
    if temp_target.exists():
        temp_target.unlink()

    latest = latest_by_topic(records)
    connection = sqlite3.connect(temp_target)
    try:
        connection.executescript(
            """
            CREATE TABLE memories (
                line_number INTEGER PRIMARY KEY,
                id TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                scope TEXT NOT NULL,
                scope_id TEXT,
                topic_key TEXT NOT NULL,
                keywords_json TEXT NOT NULL,
                keywords_text TEXT NOT NULL,
                content TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                superseded_by_id TEXT
            );

            CREATE INDEX idx_memories_scope ON memories(scope, scope_id);
            CREATE INDEX idx_memories_topic ON memories(scope, scope_id, topic_key);
            CREATE INDEX idx_memories_active ON memories(is_active, scope, scope_id);
            """
        )
        for record in records:
            active_record = latest[(record.scope, record.scope_id, record.topic_key)]
            is_active = int(active_record.id == record.id)
            superseded_by_id = None if is_active else active_record.id
            connection.execute(
                """
                INSERT INTO memories (
                    line_number,
                    id,
                    created_at,
                    scope,
                    scope_id,
                    topic_key,
                    keywords_json,
                    keywords_text,
                    content,
                    is_active,
                    superseded_by_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.line_number,
                    record.id,
                    record.created_at,
                    record.scope,
                    record.scope_id,
                    record.topic_key,
                    json.dumps(list(record.keywords)),
                    " ".join(record.keywords),
                    record.content,
                    is_active,
                    superseded_by_id,
                ),
            )
        connection.commit()
    finally:
        connection.close()

    temp_target.replace(target)


def write_memory_index(records: list[MemoryRecord]) -> None:
    latest = latest_by_topic(records)
    active_records = sorted(
        latest.values(),
        key=lambda item: (item.scope, item.scope_id or "", item.topic_key),
    )

    lines = [
        "# Memory Index",
        "",
        f"Generated: {now_iso()}",
        "",
        "Active topics derived from `memory/memories.jsonl`.",
        "",
    ]

    if not active_records:
        lines.append("No active memories yet.")
        lines.append("")
        memory_index_path().write_text("\n".join(lines), encoding="utf-8")
        return

    current_scope_label: str | None = None
    for record in active_records:
        record_scope_label = scope_label(record.scope, record.scope_id)
        if record_scope_label != current_scope_label:
            if current_scope_label is not None:
                lines.append("")
            lines.append(f"## {record_scope_label}")
            lines.append("")
            current_scope_label = record_scope_label
        keywords = ", ".join(record.keywords) if record.keywords else "none"
        lines.append(
            f"- `{record.topic_key}` | keywords: {keywords} | updated: {record.created_at} | {preview_text(record.content)}"
        )

    lines.append("")
    memory_index_path().write_text("\n".join(lines), encoding="utf-8")


def rebuild_derived_artifacts(records: list[MemoryRecord]) -> None:
    rebuild_sqlite(records)
    write_memory_index(records)


def append_record(record: MemoryRecord) -> None:
    ensure_memory_store()
    payload = {
        "id": record.id,
        "created_at": record.created_at,
        "scope": record.scope,
        "scope_id": record.scope_id,
        "topic_key": record.topic_key,
        "content": record.content,
        "keywords": list(record.keywords),
    }
    with ledger_path().open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def filter_records(
    records: Iterable[MemoryRecord],
    *,
    scope: str | None,
    scope_id: str | None,
    topic_key: str | None,
    include_superseded: bool,
) -> list[tuple[MemoryRecord, bool]]:
    latest = latest_by_topic(records)
    filtered: list[tuple[MemoryRecord, bool]] = []
    for record in records:
        if scope is not None and record.scope != scope:
            continue
        if scope is not None and record.scope_id != scope_id:
            continue
        if topic_key is not None and record.topic_key != topic_key:
            continue
        is_active = latest[(record.scope, record.scope_id, record.topic_key)].id == record.id
        if is_active or include_superseded:
            filtered.append((record, is_active))
    return filtered


def matches_query(record: MemoryRecord, query: str) -> bool:
    query_lower = query.lower()
    searchable_parts = [record.topic_key, " ".join(record.keywords), record.content]
    return any(query_lower in part.lower() for part in searchable_parts)


def print_list(records: list[tuple[MemoryRecord, bool]], include_superseded: bool, scope: str | None, scope_id: str | None) -> None:
    if not records:
        if scope is None:
            print("No memories found.")
        else:
            print(f"No memories found for {scope_label(scope, scope_id)}.")
        return

    grouped: dict[str, list[tuple[MemoryRecord, bool]]] = {}
    for record, is_active in records:
        grouped.setdefault(scope_label(record.scope, record.scope_id), []).append((record, is_active))

    for group_name in sorted(grouped):
        print(group_name)
        for record, is_active in sorted(grouped[group_name], key=lambda item: item[0].line_number, reverse=True):
            status = "active" if is_active else "superseded"
            keywords = ", ".join(record.keywords) if record.keywords else "none"
            if include_superseded:
                print(
                    f"  - [{status}] {record.topic_key} | {record.created_at} | keywords: {keywords} | {preview_text(record.content)}"
                )
            else:
                print(f"  - {record.topic_key} | {record.created_at} | keywords: {keywords} | {preview_text(record.content)}")


def search_records(
    *,
    records: Iterable[MemoryRecord],
    query: str,
    scope: str,
    scope_id: str | None,
    include_superseded: bool,
    limit: int,
) -> list[tuple[str, str, str, str, int, str | None]]:
    candidates = filter_records(
        records,
        scope=scope,
        scope_id=scope_id,
        topic_key=None,
        include_superseded=include_superseded,
    )
    ranked = sorted(candidates, key=lambda item: (item[1], item[0].line_number), reverse=True)
    matches = [
        (
            record.scope,
            "" if record.scope_id is None else record.scope_id,
            record.topic_key,
            record.created_at,
            int(is_active),
            record.content,
        )
        for record, is_active in ranked
        if matches_query(record, query)
    ]
    return matches[:limit]


def perform_reindex(_: argparse.Namespace) -> int:
    records = load_records()
    rebuild_derived_artifacts(records)
    latest = latest_by_topic(records)
    print(
        f"Rebuilt memory index from {len(records)} ledger entr{'y' if len(records) == 1 else 'ies'} "
        f"across {len(latest)} active topic{'s' if len(latest) != 1 else ''}."
    )
    return 0


def perform_list(args: argparse.Namespace) -> int:
    scope: str | None = None
    scope_id: str | None = None
    if not args.all_scopes:
        if not args.scope:
            raise UserError("Provide --scope and any required --scope-id, or use --all-scopes.")
        scope, scope_id = normalize_scope(args.scope, args.scope_id)

    topic_key = normalize_topic_key(args.topic_key) if args.topic_key else None
    records = load_records()
    filtered = filter_records(
        records,
        scope=scope,
        scope_id=scope_id,
        topic_key=topic_key,
        include_superseded=args.include_superseded,
    )
    print_list(filtered, args.include_superseded, scope, scope_id)
    return 0


def perform_search(args: argparse.Namespace) -> int:
    scope, scope_id = normalize_scope(args.scope, args.scope_id)
    query = args.query.strip()
    if not query:
        raise UserError("Search query cannot be blank.")

    records = load_records()
    results = search_records(
        records=records,
        query=query,
        scope=scope,
        scope_id=scope_id,
        include_superseded=args.include_superseded,
        limit=args.limit,
    )
    if not results:
        print(f"No matches found for '{query}' in {scope_label(scope, scope_id)}.")
        return 0

    for result_scope, result_scope_id, topic_key, created_at, is_active, content in results:
        status = "active" if is_active else "superseded"
        print(
            f"- [{status}] {scope_label(result_scope, result_scope_id or None)} | {topic_key} | {created_at} | {preview_text(content)}"
        )
    return 0


def perform_write(args: argparse.Namespace) -> int:
    scope, scope_id = normalize_scope(args.scope, args.scope_id)
    topic_key = normalize_topic_key(args.topic_key)
    keywords = normalize_keywords(args.keyword)

    records = load_records()
    existing_topics = latest_by_topic(records)
    active_topic_keys = sorted(
        record.topic_key
        for record in existing_topics.values()
        if record.scope == scope and record.scope_id == scope_id
    )
    topic_exists = topic_key in active_topic_keys

    if not topic_exists and not args.allow_new_topic_key:
        existing_display = ", ".join(active_topic_keys) if active_topic_keys else "none"
        raise UserError(
            f"HUMAN APPROVAL REQUIRED: topic_key '{topic_key}' does not exist in {scope_label(scope, scope_id)}.\n"
            f"Existing topic_keys in this scope: {existing_display}.\n"
            "Action: ask the human to approve the new topic_key, then retry with --allow-new-topic-key."
        )

    content = read_content(args)
    record = MemoryRecord(
        id=str(uuid4()),
        created_at=now_iso(),
        scope=scope,
        scope_id=scope_id,
        topic_key=topic_key,
        content=content,
        keywords=keywords,
        line_number=len(records) + 1,
    )
    append_record(record)
    records = load_records()
    rebuild_derived_artifacts(records)

    if topic_exists:
        print(
            f"Wrote memory for existing topic_key '{topic_key}' in {scope_label(scope, scope_id)}. "
            f"Earlier entries for this topic are now superseded in derived views. New id: {record.id}"
        )
    else:
        print(
            f"Wrote the first memory for topic_key '{topic_key}' in {scope_label(scope, scope_id)}. New id: {record.id}"
        )
    return 0


def perform_delete(args: argparse.Namespace) -> int:
    scope, scope_id = normalize_scope(args.scope, args.scope_id)
    topic_key = normalize_topic_key(args.topic_key)
    raise UserError(
        f"Delete is intentionally unsupported for the append-only memory pilot. "
        f"Target: {scope_label(scope, scope_id)} / {topic_key}.\n"
        "Action: preserve history, or write a new entry for the same topic_key to supersede older content."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List, search, write, and reindex Agent OS memory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List memory topics or history.")
    list_parser.add_argument("--scope", help="Scope to inspect.")
    list_parser.add_argument("--scope-id", help="Scope identifier when required by the scope.")
    list_parser.add_argument("--all-scopes", action="store_true", help="List memories across every scope.")
    list_parser.add_argument("--topic-key", help="Limit the list to one topic_key.")
    list_parser.add_argument(
        "--include-superseded",
        action="store_true",
        help="Also show superseded entries instead of only active topics.",
    )
    list_parser.set_defaults(func=perform_list)

    search_parser = subparsers.add_parser("search", help="Search memory content within one scope.")
    search_parser.add_argument("query", help="Text to search for.")
    search_parser.add_argument("--scope", required=True, help="Scope to search.")
    search_parser.add_argument("--scope-id", help="Scope identifier when required by the scope.")
    search_parser.add_argument(
        "--include-superseded",
        action="store_true",
        help="Also search superseded entries.",
    )
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum number of matches to print.")
    search_parser.set_defaults(func=perform_search)

    write_parser = subparsers.add_parser("write", help="Append a new memory entry.")
    write_parser.add_argument("--scope", required=True, help="Scope for the memory entry.")
    write_parser.add_argument("--scope-id", help="Scope identifier when required by the scope.")
    write_parser.add_argument("--topic-key", required=True, help="Existing topic_key to update or approved new topic_key.")
    write_parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Keyword to associate with the memory. Repeat or pass a comma-separated list.",
    )
    write_parser.add_argument("--content", help="Memory content as inline text.")
    write_parser.add_argument("--content-file", help="Path to a UTF-8 file containing the memory content.")
    write_parser.add_argument(
        "--allow-new-topic-key",
        action="store_true",
        help="Required only after the human explicitly approves a new topic_key.",
    )
    write_parser.set_defaults(func=perform_write)

    delete_parser = subparsers.add_parser("delete", help="Refuse destructive deletion for the append-only pilot.")
    delete_parser.add_argument("--scope", required=True, help="Scope for the memory entry.")
    delete_parser.add_argument("--scope-id", help="Scope identifier when required by the scope.")
    delete_parser.add_argument("--topic-key", required=True, help="Topic key that would otherwise be deleted.")
    delete_parser.set_defaults(func=perform_delete)

    reindex_parser = subparsers.add_parser("reindex", help="Rebuild derived sqlite and markdown memory outputs.")
    reindex_parser.set_defaults(func=perform_reindex)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except UserError as exc:
        print(exc)
        return 2
    except FileNotFoundError as exc:
        print(f"SYSTEM ERROR: {exc}. Action: verify the referenced path exists and retry.")
        return 2
    except Exception as exc:
        print(f"SYSTEM ERROR: {exc}. Action: inspect the failing command inputs and retry.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
