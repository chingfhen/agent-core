---
name: agent-os-memory
description: Lists, searches, and writes Agent OS memory through the canonical steward memory script when the current repo has memory enabled.
disable-model-invocation: false
---

# Agent OS Memory

Use this skill only when the current repo's `.agent-os.json` exists and `memory_enabled` is `true`.

## What To Do

1. Read `.agent-os.json` and capture `agent_os_path`, `scope`, `scope_id`, and `memory_enabled`.
2. If `memory_enabled` is `false`, stop and tell the user memory is not enabled for this repo.
3. Before writing, inspect existing topics first:
   - `uv run "<agent_os_path>/scripts/memory.py" list --scope <scope> --scope-id <scope_id>`
   - `uv run "<agent_os_path>/scripts/memory.py" search "<query>" --scope <scope> --scope-id <scope_id>`
4. Reuse an existing `topic_key` whenever it fits.
5. For a quick update to an existing topic, prefer inline content:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content "<note>"`
6. For a longer note, use a file instead:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content-file "<path>"`
7. If no suitable `topic_key` exists, stop and ask the human to approve the new `topic_key` before writing.
8. After approval, retry with:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content "<note>" --allow-new-topic-key`
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content-file "<path>" --allow-new-topic-key`

## Behavior Contract

- Treat `memory/memories.jsonl` as canonical truth.
- Treat `memory/memory.sqlite` and `MEMORY_INDEX.md` as derived outputs.
- Do not edit memory files directly; always use `scripts/memory.py`.
- `list` and `search` are read-only; only `write` and `reindex` rebuild the derived outputs.
- Updating an existing `topic_key` within the active scope can be autonomous.
- Creating a new `topic_key` requires explicit human approval, then `--allow-new-topic-key` on the write command.
- If someone asks to delete memory, explain that the pilot is append-only and `uv run "<agent_os_path>/scripts/memory.py" delete ...` only returns a refusal message.
- Do not delete or rewrite prior ledger entries.
