# Task: Simplify private cross-device skill distribution

**File:** `tasks/2026-09-15__simplify-private-skill-distribution-bookmark.md`
**Created:** 2026-09-15
**Last Updated:** 2026-09-15
**Priority:** Now
**Status:** Closed
**Execution Gate:** Not Applicable (Closed)
**Docs Sync:** Synced

**Goal:** Provide one private, cross-device command that refreshes the canonical Agent Core checkout and safely copies configured core skills into the current Git project.

**Why:** The owner wanted a simpler replacement for manually arranging per-project symlinks or junctions. Projects need explicit updates rather than live propagation, central tracking, or multiple harness-specific destinations.

**Success Bar:** After one-time machine setup, the owner can enter any Git project and run `agent-core apply`; the command pulls the clean canonical checkout and safely adds or updates configured skills under `.agents/skills/` without overwriting unrelated, tracked, or locally modified content.

**Chosen Approach:** Package a standard-library Python CLI in the private repository. The stable console launcher refreshes the fixed `~/.agent-core` checkout, then starts the newly pulled apply implementation in a fresh process. Apply reads `core-skills.toml` and owns copied destinations through project-local fingerprints.

**Current State:** Complete. The package, core list, safe copy engine, ownership state, rollback behavior, local exclusions, cross-platform tests, and durable documentation are implemented. Production skill contents were not changed, and the advanced alias enrollment script remains operational and independent.

**Next Action:** None.

**Blockers:** None.

**Human Attention:**

- The only simple-workflow destination is `.agents/skills/`; advanced `.claude`, `.opencode`, manifest, and registry surfaces are ignored.
- Configuration removal remains additive. Prior copies, ownership records, and exclusions stay in place and can be safely checked if a skill is re-added.
- Ownership state uses each worktree's actual Git directory, while exact private-path exclusions use the Git common metadata directory.
- There is no automatic removal or force behavior.

**Target Docs:** `README.md`, `AGENTS.md`, `docs/consumer-repo-enrollment.md`
**Relevant Code:** `agent_core/`, `core-skills.toml`, `pyproject.toml`, `tests/test_agent_core.py`

## Completion Evidence

- `uv run --python 3.11 python -m unittest discover -s tests -v` — 24 tests passed, including the existing Windows junction and unenrollment tests.
- Coverage includes first apply, fast-forward refresh, fresh-process implementation loading, additive configuration changes, deletion/recreation, ownership conflicts, tracked descendants, dirty and failed refreshes, rejected ignored source artifacts, permission-sensitive fingerprints, invalid sources and state, all-target preflight, rollback, local exclusions, linked worktrees, and legacy independence.
- `uv run --python 3.11 python -m compileall -q agent_core tests scripts` — passed.
- `uv run agent-core --help` — packaged console entry point loaded and displayed the `apply` command.
- `git diff --check` — passed before closure.
- Required docs and `AGENTS.md` were synchronized to make `agent-core apply` the simple personal workflow and preserve advanced alias enrollment as optional tooling.

## Residual Follow-Up

None. The private GitLab URL remains an intentional setup placeholder in documentation.
