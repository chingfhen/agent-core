# Task: Agent OS memory retrieval surface v1.1

**File:** `tasks/2026-06-20__agent-os-memory-retrieval-surface-v1_1-bookmark.md`
**Created:** 2026-06-20
**Last Updated:** 2026-06-20
**Priority:** Next
**Status:** Planned
**Docs Sync:** Not Started

**Goal:** Improve the memory retrieval interface for agent consumers without making default discovery output noisy or expensive.
**Success Bar:** Agents can keep using concise discovery commands for `list` and `search`, can deliberately retrieve full memory bodies when needed, and can request stable machine-readable output for cross-harness execution.
**Current State:** `scripts/memory.py` currently prints human-oriented summaries and preview text for `list` and `search`. There is no agent-friendly structured output mode and no dedicated command for full-body retrieval of the active entry for a topic. The memory system is primarily for coding agents, not humans, so this interface gap matters more than the current storage shape.
**Next Action:** After the real enrolled-repo validation pass, design the smallest command set that separates discovery from detail retrieval. Likely candidates are `get` or `show` plus a shared `--json` output mode.
**Blockers:** Prefer to confirm the pain points during real-repo validation first, but this task can start earlier if a human wants to front-load the interface work.

**Target Docs:** `docs/memory-pilot.md`, `README.md`, `skills/agent-os-memory/SKILL.md`
**Relevant Code:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`

## Human Intent

- Preserve concise discovery.
- Add a deliberate path for detailed recall.
- Make the interface useful for cross-harness agents rather than only ad hoc human terminal use.

## Expected Outcomes

- `list` remains a concise topic discovery surface.
- `search` remains a concise candidate discovery surface.
- A new `get` or `show` command can return the active full-body memory for a topic, with an option to include history when useful.
- `--json` exists for at least `list`, `search`, and the new detail command.
- `agent-os-memory` skill guidance explains when to use discovery output versus detail retrieval.

## Decisions Locked

- Do not make full-body output the default for `list` or `search`.
- Structured output should be a stable contract, not an ad hoc debug dump.
- Keep append-only ledger behavior unchanged.
- Agent-facing usability matters more than preserving a purely human terminal interface.

## Current Understanding

- The current preview-only behavior is good for scanning many topics quickly.
- Preview-only behavior becomes a blocker when an agent actually needs the memory body to apply it reliably.
- `--json` is more important, not less, because the main consumers are agents across different harnesses.
- A separate detailed retrieval command is likely a better tradeoff than making `search` verbose by default.

## Remaining Uncertainty

- Whether the new detail command should key off `topic_key` only or also support an exact memory `id`.
- Whether `search --json` should include full content or only previews plus enough identifiers for a follow-up `get`.
- Whether history access belongs behind a flag such as `--include-superseded` on the detail command.

## Executor Guidance

- Treat discovery and detail retrieval as separate steps.
- Prefer stable field names in JSON from day one.
- Do not dump raw ledger internals when a smaller structured view will do.
- Preserve the current bias toward active memories by default.

## Likely Blind Spots

- Optimizing for human-readable shell output while forgetting the main consumer is another agent.
- Making `list` or `search` noisy enough that discovery becomes unpleasant.
- Returning unversioned or inconsistent JSON that later tools cannot rely on.

## Verification Contract

- An agent should be able to discover candidate memories without reading full bodies by default.
- An agent should be able to fetch the current full body for a selected topic without scraping preview text.
- A machine consumer should be able to parse results without text scraping when `--json` is present.
- All read paths should remain read-only.

## Context Pointers

- `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
- `docs/memory-pilot.md`
- `scripts/memory.py`
- `skills/agent-os-memory/SKILL.md`
