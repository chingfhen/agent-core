# Task: Agent OS memory provenance and supersession contract

**File:** `tasks/2026-06-20__agent-os-memory-provenance-and-supersession-contract-bookmark.md`
**Created:** 2026-06-20
**Last Updated:** 2026-06-20
**Priority:** Later
**Status:** Planned
**Docs Sync:** Not Started

**Goal:** Add the smallest useful provenance and stale-truth contract improvements so agents can trust where a memory came from and understand when newer truth replaced older truth.
**Success Bar:** The memory contract clearly distinguishes timestamp data from origin metadata, preserves append-only writes, and makes current versus historical truth easier to reason about without adopting a heavy temporal or graph model.
**Current State:** Each ledger row currently stores `id`, `created_at`, `scope`, `scope_id`, `topic_key`, `content`, and `keywords`. That records when something was written, but not who wrote it, from which artifact it was captured, or whether a newer entry was intended to supersede it for a specific reason beyond append order within the same topic.
**Next Action:** After validation and retrieval-surface improvements, design the minimal provenance fields and supersession semantics that materially improve trust without bloating the pilot.
**Blockers:** This should follow real-repo validation so the design responds to actual trust and stale-truth pain points, not only theory.

**Target Docs:** `docs/memory-pilot.md`, `README.md`, `skills/agent-os-memory/SKILL.md`
**Relevant Code:** `scripts/memory.py`, `memory/memories.jsonl`, `MEMORY_INDEX.md`

## Human Intent

- Make memory origin inspectable.
- Improve trust and conflict handling.
- Reduce the chance that stale truth quietly keeps winning because the system records only time, not origin or replacement context.

## Expected Outcomes

- A documented definition of provenance for Agent OS memory.
- A minimal set of provenance fields such as the writing agent and source artifact, if real validation confirms they are worth the cost.
- A clearer contract for how same-topic updates supersede prior entries and how future contradictions should be surfaced.
- No mutable `status` field and no in-place ledger edits.

## Decisions Locked

- Provenance is not just dates. Dates answer when; provenance answers who, from what source, and under what capture path.
- Keep the ledger append-only.
- Do not add mutable `updated_at` or row rewrites.
- Avoid a heavy temporal model unless real usage proves the simpler model insufficient.

## Current Understanding

- `created_at` is necessary but not sufficient for trust.
- If memory later comes from multiple harnesses, origin metadata will help debug conflicts and audit questionable captures.
- The current active-versus-superseded derivation by topic is a strong base and should remain the default behavior.
- The next stale-truth improvement should probably be lightweight, such as explicit provenance and optional supersession metadata, not full validity windows.

## Remaining Uncertainty

- Which provenance fields carry lasting value versus short-lived noise.
- Whether `source_session` is useful enough to justify storing it.
- Whether explicit `supersedes_id` adds enough clarity beyond current topic-based append order.
- Whether cross-topic contradiction handling is needed yet or whether same-topic discipline is enough for now.

## Executor Guidance

- Prefer provenance fields that future agents can actually use to judge trust.
- Keep the field set small and stable.
- Do not store noisy session trivia just because it is available.
- Preserve the current bias that higher-priority repo truth still beats memory.

## Likely Blind Spots

- Confusing provenance with timestamps.
- Adding too many metadata fields before proving retrieval benefit.
- Building a temporal framework that the pilot does not yet need.

## Verification Contract

- Future agents should be able to tell when a memory was written and also where it came from.
- Superseded history should remain inspectable.
- The contract should improve stale-truth reasoning without requiring mutable storage.
- The resulting schema should still be easy to regenerate into derived artifacts.

## Context Pointers

- `source-material/2026-06-20__cross-harness-agent-memory.md`
- `docs/memory-pilot.md`
- `scripts/memory.py`
- `memory/memories.jsonl`
