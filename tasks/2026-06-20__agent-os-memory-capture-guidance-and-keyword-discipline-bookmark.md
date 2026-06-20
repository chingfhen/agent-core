# Task: Agent OS memory capture guidance and keyword discipline

**File:** `tasks/2026-06-20__agent-os-memory-capture-guidance-and-keyword-discipline-bookmark.md`
**Created:** 2026-06-20
**Last Updated:** 2026-06-20
**Priority:** Later
**Status:** Planned
**Docs Sync:** Not Started

**Goal:** Improve capture discipline and retrieval quality through better guidance before reaching for heavier retrieval or ranking systems.
**Success Bar:** Future sessions know how to write high-signal topics, concise durable content, and useful keywords, while the project avoids pretending that better keywords alone solve retrieval quality.
**Current State:** The current capture gate is conservative, which is good, but the keyword guidance is still light. Search already checks `topic_key`, `keywords`, and `content`, so retrieval is not actually keywords-only. Better keyword habits will help, but topic naming, concise durable content, and memory selectivity are at least as important.
**Next Action:** After real-repo validation, review the first real captures and write concrete guidance plus examples for topic-key choice, content shape, and keyword composition.
**Blockers:** This task should wait for real memory examples so the guidance reflects actual repo usage rather than hypothetical advice.

**Target Docs:** `skills/agent-os-memory/SKILL.md`, `docs/memory-pilot.md`, `README.md`
**Relevant Code:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`

## Human Intent

- Keep memory high-signal.
- Improve retrieval quality through better capture discipline first.
- Avoid premature ranking complexity unless practical failures remain after guidance improves.

## Expected Outcomes

- Clear topic-key naming guidance.
- Clear keyword guidance with examples of high-ROI keywords.
- Clear examples of concise durable content versus noisy session residue.
- A short rubric for deciding whether a retrieval miss is a capture problem, a command-surface problem, or a search-algorithm problem.

## Decisions Locked

- Better keywords help, but they are not a complete retrieval strategy.
- Do not optimize for keyword stuffing.
- Topic-key naming, concise content, and selective capture matter as much as keyword choice.
- Advanced ranking and scoring remain deferred until simpler guidance has been tested.

## Current Understanding

- Retrieval quality problems often start with poor captures, not only weak search code.
- Overly broad or repetitive keywords can pollute search instead of helping it.
- Durable content written in a compact factual style will usually search better than long narrative notes with many keywords.
- The existing conservative write gate is a strength and should be preserved.

## Remaining Uncertainty

- Which keyword patterns actually help most in real repos: tool names, repo terms, error signatures, decision categories, or user preference labels.
- Whether topic-key conventions should remain freeform or adopt a small recommended taxonomy.
- Whether retrieval misses after better guidance point toward a later ranking task.

## Executor Guidance

- Prefer precise nouns and stable repo terms over generic engineering words.
- Use keywords to improve discovery, not to compensate for noisy content.
- Keep memory bodies short, durable, and directly actionable.
- Reuse an existing topic when the truth evolved instead of creating loosely overlapping topics.

## Likely Blind Spots

- Over-crediting keywords when the real problem is vague content or poor topic keys.
- Writing guidance without enough real examples.
- Turning a lightweight guidance pass into a large taxonomy project.

## Verification Contract

- Future agents should be able to find stored memories using realistic task queries without relying on perfect wording.
- The guidance should reduce duplicate or overlapping topics.
- The project should be able to tell whether remaining failures justify algorithmic retrieval changes.

## Context Pointers

- `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
- `source-material/2026-06-20__cross-harness-agent-memory.md`
- `skills/agent-os-memory/SKILL.md`
- `docs/memory-pilot.md`
