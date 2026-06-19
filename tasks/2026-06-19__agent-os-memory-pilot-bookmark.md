# Task: Agent OS memory pilot

**File:** `tasks/2026-06-19__agent-os-memory-pilot-bookmark.md`
**Created:** 2026-06-19
**Last Updated:** 2026-06-19
**Priority:** Now
**Status:** Closed
**Docs Sync:** Synced

**Goal:** Build the minimal v1 Agent OS memory pilot on top of the completed skills foundation.
**Success Bar:** The repo has an append-only canonical ledger, generated derived memory outputs, a steward-owned list/search/write/reindex tool, a separate executor-facing memory skill, and a hard stop for unapproved new `topic_key` creation.
**Current State:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`, `docs/memory-pilot.md`, and `memory/memories.jsonl` are in place and smoke-tested. An enrolled temporary consumer repo confirmed the executor path through the live local alias, and follow-up fixes made `list` and `search` read-only, moved the new-topic approval gate ahead of content-file reads, quoted skill command paths for Windows safety, and added an explicit `delete` refusal command for the append-only boundary. The canonical ledger now contains experiment-scope smoke-test entries under `experiment:memory-workflow-smoke` for `workflow_smoke`, including one superseded revision and one active revision.
**Next Action:** Continue with `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md` for the first real enrolled-repo validation pass.
**Blockers:** None.

**Target Docs:** `README.md`, `AGENTS.md`, `docs/consumer-repo-enrollment.md`, `docs/memory-pilot.md`
**Relevant Code:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`, `skills/agent-os-bootstrap/SKILL.md`, `memory/memories.jsonl`

## Human Intent

- Keep the skills foundation canonical and reusable across more enrolled repos.
- Add memory as a separate layer rather than expanding bootstrap behavior.
- Preserve a strict human-in-the-loop boundary around new topic creation.
- Stop once the next step genuinely requires human judgement.

## Expected Outcomes

- `memory/memories.jsonl` is the tracked canonical ledger.
- `memory/memory.sqlite` and `MEMORY_INDEX.md` are generated from the ledger and remain disposable.
- Executors can use a dedicated `agent-os-memory` skill when `memory_enabled` is true.
- The first attempt to create a new `topic_key` stops and asks for human approval.

## Decisions Locked

- Memory remains a separate skill and workflow, not bootstrap scope.
- The pilot uses one steward script with subcommands instead of several parallel entrypoints.
- Ledger rows are immutable revisions; active and superseded state is derived.
- Topic creation approval is enforced by the write command itself.

## Current Understanding

- The skills-enrollment foundation is complete and does not need architectural rework to support memory.
- Repo-local executors already have enough manifest context to call canonical memory tooling through `agent_os_path`.
- The right first pilot is small: ledger, derived artifacts, topic discovery, write gate, and no destructive CRUD.
- The pilot now has verified create/read/update coverage plus an explicit delete refusal boundary.

## Remaining Uncertainty

- Which topic conventions will prove durable enough for wider real-repo adoption.
- Whether future agent ergonomics need structured output such as JSON once real executor usage increases.

## Executor Guidance

- Prefer reusing an existing `topic_key` after `list` or `search` before proposing a new one.
- Treat `memory/memories.jsonl` as canonical and avoid editing it directly.
- Rebuild derived outputs through `uv run scripts/memory.py reindex` rather than manual sqlite or markdown edits.

## Likely Blind Spots

- Accidentally teaching executors storage internals instead of routing them through the dedicated skill and steward script.
- Treating the empty ledger as missing work rather than an intentional pause at the approval boundary.
- Forgetting that new `topic_key` creation still requires explicit human approval outside clearly authorized testing.

## Verification Contract

- `uv run scripts/memory.py list --all-scopes` should work on an empty ledger.
- `uv run scripts/memory.py search <query> --scope ...` should work even when no topics exist.
- `uv run scripts/memory.py write ...` must refuse an unseen `topic_key` unless `--allow-new-topic-key` is present.
- `uv run scripts/memory.py delete ...` must refuse destructive deletion with an explicit append-only message.
- `uv run scripts/memory.py reindex` must rebuild derived artifacts from only the ledger.

## Context Pointers

- `README.md`
- `AGENTS.md`
- `docs/consumer-repo-enrollment.md`
- `docs/memory-pilot.md`
- `scripts/memory.py`
- `skills/agent-os-memory/SKILL.md`
- `tasks/2026-06-18__agent-os-foundation-bookmark.md`
- `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
