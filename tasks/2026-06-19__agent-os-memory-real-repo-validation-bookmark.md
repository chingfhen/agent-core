# Task: Agent OS memory real-repo validation

**File:** `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md`
**Created:** 2026-06-19
**Last Updated:** 2026-06-19
**Priority:** Next
**Status:** Blocked
**Docs Sync:** Partial

**Goal:** Validate `agent-os-memory` in one real enrolled consumer repo using a human-approved repo-scoped topic.
**Success Bar:** A real consumer repo uses the local `agent-os-memory` alias successfully for list/search/write/update flows, any usability gaps are fixed, and durable behavior changes are synced back into canonical docs.
**Current State:** The memory pilot itself is complete and smoke-tested in a temporary enrolled repo plus an experiment-scoped canonical ledger entry. The remaining validation step is a real executor path in one actual enrolled consumer repo, with one approved repo-scoped `topic_key`, so the system is exercised under real repo identity and real human-approved topic semantics.
**Next Action:** Choose one real enrolled consumer repo, approve the first repo-scoped `topic_key`, then run the local executor path and capture any gaps.
**Blockers:** Needs a specific real enrolled repo choice and explicit human approval for the first new repo-scoped `topic_key`.

**Target Docs:** `docs/memory-pilot.md`, `docs/consumer-repo-enrollment.md`, `README.md`
**Relevant Code:** `scripts/memory.py`, `skills/agent-os-memory/SKILL.md`, `skills/agent-os-bootstrap/SKILL.md`, `scripts/enroll_repo.py`

## Human Intent

- Validate memory where it actually matters: in a real enrolled consumer repo, not just a temporary smoke repo.
- Preserve the human approval boundary for first-time topic creation.
- Use this validation pass to find the next practical ergonomics gaps, if any.

## Expected Outcomes

- One real enrolled consumer repo uses `agent-os-memory` through its local alias surface.
- One repo-scoped `topic_key` is human-approved and exercised end to end.
- Any newly discovered friction is either fixed immediately or recorded with clear follow-up.

## Decisions Locked

- The minimal pilot remains append-only.
- New topic creation remains human-gated.
- Validation should happen through the real local skill alias path, not by bypassing enrollment.

## Current Understanding

- The steward memory tooling is now functionally complete enough for real-repo validation.
- Temporary-repo executor smoke tests already proved the local alias path, read-only reads, approval gate ordering, and explicit delete refusal.
- The next meaningful unknown is not whether the pilot works in isolation, but whether real repo usage reveals topic-naming or workflow friction.

## Remaining Uncertainty

- Which real enrolled repo is the best first validation target.
- Which first repo-scoped topic will be durable rather than test-only churn.
- Whether real repo usage will justify structured output or additional helper commands.

## Executor Guidance

- Start from the target repo's `.agent-os.json` and local `.claude/skills/agent-os-memory` alias.
- Prefer a genuinely durable repo-scoped topic rather than a throwaway smoke-test topic if possible.
- Preserve the approval boundary: do not create the first repo topic without explicit human signoff.

## Likely Blind Spots

- Accidentally validating with a repo that is not actually enrolled or not memory-enabled.
- Choosing a topic key that is too test-specific to be durable.
- Mistaking temporary smoke coverage for real deployment confidence.

## Verification Contract

- Confirm the chosen consumer repo is enrolled and `memory_enabled` is true.
- Confirm the local `agent-os-memory` alias is present and readable through the consumer repo.
- Verify `list`, `search`, `write`, and update flows against the real repo scope.
- Capture any ergonomics gap that would make an executor fail or ask avoidable questions.

## Context Pointers

- `docs/memory-pilot.md`
- `docs/consumer-repo-enrollment.md`
- `scripts/memory.py`
- `skills/agent-os-memory/SKILL.md`
- `tasks/2026-06-19__agent-os-memory-pilot-bookmark.md`
