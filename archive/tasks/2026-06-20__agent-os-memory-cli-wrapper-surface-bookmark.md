# Task: Agent OS memory CLI wrapper surface

**File:** `tasks/2026-06-20__agent-os-memory-cli-wrapper-surface-bookmark.md`
**Created:** 2026-06-20
**Last Updated:** 2026-06-20
**Priority:** Next
**Status:** Planned
**Docs Sync:** Not Started

**Goal:** Expose a stable Agent OS memory CLI contract for executors while keeping the current Python plus `uv` implementation hidden behind that surface.
**Success Bar:** Executors no longer call `uv run "<agent_os_path>/scripts/memory.py"` directly. Instead they call one documented CLI entrypoint whose location is stable relative to `agent_os_path`, while the underlying implementation can still be the current steward-owned script.
**Current State:** The current executor guidance exposes implementation details directly in skill instructions. This is acceptable for the first pilot, but it couples every harness to Python-file invocation details and makes later implementation changes harder.
**Next Action:** Design the thinnest possible wrapper contract. Prefer a documented wrapper path derived from `agent_os_path` over adding a new manifest field immediately.
**Blockers:** None for design. Full rollout should ideally happen after the retrieval-surface task so the wrapper reflects the better command set rather than freezing the current rougher one.

**Target Docs:** `docs/memory-pilot.md`, `docs/consumer-repo-enrollment.md`, `README.md`, `skills/agent-os-memory/SKILL.md`
**Relevant Code:** `scripts/memory.py`, `scripts/enroll_repo.py`, `schemas/agent-os-manifest.schema.json`, `skills/agent-os-memory/SKILL.md`

## Human Intent

- Give executors a stable command surface.
- Decouple the public interface from the current implementation.
- Improve cross-harness portability without forcing a premature rewrite away from Python.

## Expected Outcomes

- A documented CLI contract such as a wrapper under the canonical Agent OS repo.
- `agent-os-memory` skill instructions call the wrapper, not `uv run` on the script path.
- The wrapper preserves argument behavior and exit semantics from the underlying tool.
- Manifest growth is avoided unless a real need emerges that `agent_os_path` cannot cover cleanly.

## Decisions Locked

- Keep `scripts/memory.py` as the canonical implementation until there is a concrete reason to replace it.
- Do not add a raw command string to `.agent-os.json`.
- Prefer deriving the wrapper path from `agent_os_path` before introducing a dedicated `memory_cli_path` or similar field.
- A wrapper improves interface stability; it does not by itself remove the runtime dependency on `uv` and Python.

## Current Understanding

- The repo already intentionally standardizes steward script execution on `uv` plus PEP 723 Python scripts.
- A wrapper is mainly about public contract stability, not immediate runtime independence.
- If the implementation later moves to a native executable, harness tool, or MCP integration, the wrapper contract can stay stable.
- Adding a manifest field now would duplicate information that may be derivable from `agent_os_path` and create new drift risk.

## Remaining Uncertainty

- Which wrapper shape is best across Windows-first usage and possible future Unix usage.
- Whether the wrapper should live under `scripts/`, `bin/`, or another conventional path.
- Whether future enrolled repos ever need the wrapper projected into the consumer repo itself rather than called through `agent_os_path`.

## Executor Guidance

- Keep the public command shape simple and explicit.
- Preserve current argument names where practical to minimize migration friction.
- Prefer one stable command contract over multiple harness-specific call paths.

## Likely Blind Spots

- Mistaking the wrapper task for a full packaging task.
- Expanding the manifest prematurely to hold implementation details.
- Breaking existing skill instructions without a migration plan.

## Verification Contract

- An executor should be able to call memory commands through a single stable entrypoint.
- The wrapper should preserve exit codes and refusal messages.
- The wrapper should not require future agents to know the underlying script filename.
- The design should still fit the current `agent_os_path` manifest contract unless a proven need forces expansion.

## Context Pointers

- `tasks/2026-06-20__agent-os-memory-retrieval-surface-v1_1-bookmark.md`
- `docs/memory-pilot.md`
- `docs/consumer-repo-enrollment.md`
- `scripts/memory.py`
- `scripts/enroll_repo.py`
