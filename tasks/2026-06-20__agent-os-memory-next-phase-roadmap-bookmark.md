# Task: Agent OS memory next-phase roadmap

**File:** `tasks/2026-06-20__agent-os-memory-next-phase-roadmap-bookmark.md`
**Created:** 2026-06-20
**Last Updated:** 2026-06-20
**Priority:** Now
**Status:** Planned
**Docs Sync:** N/A

**Goal:** Preserve an ordered, minimal roadmap for the next phase of Agent OS memory after the initial pilot so future sessions can improve the system without restarting the architecture discussion.
**Success Bar:** Future sessions can pick the next memory task in priority order, the order reflects the actual bottlenecks for cross-harness coding agents, and the roadmap keeps the project biased toward practical validation rather than speculative redesign.
**Current State:** The append-only memory pilot is complete and smoke-tested, but real enrolled-repo validation is still blocked. Review of the current system plus new source material highlighted five areas worth improving: real usage validation, retrieval ergonomics, a stable CLI surface, provenance plus stale-truth handling, and capture discipline. The external source material was useful for prompts and vocabulary, but it is not the source of truth for this repo.
**Next Action:** Start with `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`. Do not skip priority 1 unless the human explicitly reprioritizes.
**Blockers:** Priority 1 remains blocked on choosing a real enrolled repo and approving its first durable repo-scoped `topic_key`.

**Target Docs:** `README.md`, `docs/memory-pilot.md`, `docs/consumer-repo-enrollment.md`
**Relevant Code:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`, `scripts/enroll_repo.py`, `schemas/agent-os-manifest.schema.json`

## Human Intent

- Improve Agent OS memory where it will concretely help cross-harness coding agents.
- Preserve the append-only pilot shape unless real usage proves a gap.
- Avoid over-design based on untrusted or generic external memory-system material.
- Keep future sessions focused on the highest-leverage bottlenecks first.

## Ordered Task Sequence

1. `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
2. `tasks/2026-06-20__agent-os-memory-retrieval-surface-v1_1-bookmark.md`
3. `tasks/2026-06-20__agent-os-memory-cli-wrapper-surface-bookmark.md`
4. `tasks/2026-06-20__agent-os-memory-provenance-and-supersession-contract-bookmark.md`
5. `tasks/2026-06-20__agent-os-memory-capture-guidance-and-keyword-discipline-bookmark.md`

## Decisions Locked

- Real enrolled-repo validation stays ahead of deeper memory redesign.
- Do not add vector search, graph storage, automatic extraction, or LLM ranking until the current pilot proves insufficient.
- Keep the canonical implementation small and reversible.
- Prefer a stable CLI contract over teaching executors to call `uv run` directly.
- Prefer separate discovery and detail retrieval flows instead of making every command verbose.
- Keep the manifest minimal unless a real portability problem forces a new field.

## Current Understanding

- The current biggest functional gap is not storage. It is the agent-facing interface around retrieval and trust.
- Provenance means origin metadata such as who or what created the memory and from which artifact, not only when it was written.
- The current search is not keywords-only; it matches `topic_key`, `keywords`, and `content`, so better keywords help but are not the whole retrieval story.
- Preview-only output is useful for discovery, but agents still need a deliberate path to fetch the full memory body when they need to apply it.
- A CLI wrapper improves cross-harness stability even if it still dispatches to `uv run scripts/memory.py` internally at first.

## Non-Goals / Stop Conditions

- Do not rewrite the pilot around a different storage backend.
- Do not expand `agent-os-bootstrap` into a memory or tooling dump.
- Do not add manifest churn just to encode implementation details that can be derived from `agent_os_path`.
- Do not let external research override repo-local decisions already captured in docs and code.

## Verification Contract

- Each follow-up task should keep append-only ledger behavior intact unless a human explicitly changes that contract.
- Each follow-up task should state whether it is blocked on real-repo validation findings.
- Future sessions should be able to execute any one task without redoing the whole roadmap discussion.

## Context Pointers

- `tasks/2026-06-19__agent-os-memory-pilot-bookmark.md`
- `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
- `source-material/2026-06-20__cross-harness-agent-memory.md`
- `docs/memory-pilot.md`
- `scripts/memory.py`
- `skills/agent-os-memory/SKILL.md`
