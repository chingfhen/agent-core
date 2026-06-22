# Memory Pilot

**Last Updated:** 2026-06-21

**Status:** Current

**Source Of Truth:** Defines the current v1 Agent OS memory pilot, including ledger shape, approval boundaries, and steward tooling.

**Update When:** Memory schema, approval gates, derived artifacts, or executor-facing memory flows change.

### Read First

- `memory/memories.jsonl` is the only tracked memory ledger and remains append-only.
- `memory/memory.sqlite` and `MEMORY_INDEX.md` are derived artifacts rebuilt from the ledger and should not be committed.
- `uv run scripts/memory.py` is the steward-owned entry point for `list`, `search`, `write`, and `reindex` flows.
- Updating an existing `topic_key` within the active scope can be autonomous.
- Creating a new `topic_key` requires explicit human approval.
- Executor memory behavior is an active recall and conservative capture layer, not transcript storage or task logging.
- Source code, tests, docs, and active task files remain the better surfaces when they already own the information.
- Executor-facing memory behavior lives in `skills/agent-os-memory/SKILL.md`, which reads `.agent-os.json` directly when memory is enabled.

### Scope

This document covers the canonical memory ledger, derived search/index outputs, human-approval boundaries, and the current steward and executor tooling contract.

### Not Here

- Consumer-repo enrollment mechanics beyond the memory opt-in boundary
- Task-level decisions about which new topics should actually be created

### Current Contract

#### Canonical And Derived Surfaces

- Canonical ledger: `memory/memories.jsonl`
- Derived sqlite view: `memory/memory.sqlite`
- Derived markdown topic map: `MEMORY_INDEX.md`

#### Ledger Schema

Each JSONL row stores one immutable memory revision with these fields:

- `id`: UUID4 string
- `created_at`: ISO 8601 timestamp
- `scope`: `global` | `personal` | `repo` | `experiment`
- `scope_id`: string or `null`; required for `repo` and `experiment`
- `topic_key`: lowercase key using letters, numbers, underscores, or hyphens
- `content`: markdown/text body
- `keywords`: string array

- The ledger does not rewrite prior rows.
- Active versus superseded state is derived from append order inside each `(scope, scope_id, topic_key)` group.
- The latest row for a topic is active; earlier rows for the same topic become superseded in derived views.

#### Steward Script

- Command entry point: `uv run scripts/memory.py`
- Supported subcommands:
  - `list`
  - `search`
  - `write`
  - `delete` (explicitly refused for the append-only pilot)
  - `reindex`
- `list` shows active topics by default and can include superseded history.
- `search` matches on `topic_key`, `keywords`, and `content` within one scope.
- `list` and `search` read directly from the ledger and do not mutate derived artifacts.
- `write` appends a new ledger row, then rebuilds the derived sqlite and markdown outputs.
- `delete` exists only to return a clear refusal message for destructive deletion requests.
- `reindex` rebuilds derived outputs without changing the ledger.

#### Human Approval Boundary

- Reusing an existing `topic_key` in the active scope is autonomous.
- If the requested `topic_key` does not already exist in that scope, `write` must stop and return a human-approval message.
- After the human approves the new key, the steward or executor may retry with `--allow-new-topic-key`.

#### Executor Flow

- Consumer repos opt into memory by setting `memory_enabled` in `.agent-os.json`.
- Executors should use the separate local `agent-os-memory` skill only when memory is enabled.
- Executors should proactively recall memory before consequential work when durable user or repo context could affect the task.
- Executors should discover existing topics through `list` and `search`, not by reading `jsonl` or `sqlite` internals.
- Executors should pass `scope` and `scope_id` from `.agent-os.json` into `scripts/memory.py`.
- Executors should treat retrieved memory as advisory context. Current user instructions, system/developer instructions, and current repo files have higher priority.
- Executors should capture only high-signal durable knowledge: recurring user preferences, stable repo or environment constraints, durable decisions and rationale, validated repeatable procedures, and unusual resolved failures likely to recur.
- Executors should not capture raw transcripts, scratch notes, routine command output, ordinary task progress, guesses, secrets, or facts already better represented in code, tests, docs, or `tasks/`.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | Top-level orientation and durable system boundaries. |
| Steward contract | `AGENTS.md` | Governs append-only behavior and human approval rules. |
| Consumer repo integration | `docs/consumer-repo-enrollment.md` | Defines how consumer repos opt into memory-enabled executor behavior. |
| Executor memory skill | `skills/agent-os-memory/SKILL.md` | Tells executors how to use memory without direct storage internals. |
| Steward memory script | `scripts/memory.py` | Implements list/search/write/reindex flows and the topic approval gate. |
| Active memory task | `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md` | Tracks the next real enrolled-repo validation pass for the memory pilot. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-06-19 | The first memory pilot ships as `scripts/memory.py` subcommands rather than multiple entry scripts. | One single-file steward tool is the smallest correct implementation while still exposing list/search/write/reindex flows. |
| 2026-06-19 | The ledger stores immutable revisions without a mutable `status` field. | Active versus superseded state is already a derived concept and should not require rewriting prior rows. |
| 2026-06-19 | The first new topic in a scope hard-stops unless the human approves it. | The human-in-the-loop boundary is more important than completing a write autonomously. |
