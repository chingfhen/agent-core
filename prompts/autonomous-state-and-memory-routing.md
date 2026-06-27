# Autonomous State And Memory Routing

**Status:** Current

**Purpose:** Canonical reusable `AGENTS.md` section for repos that use `tasks/`, `docs/`, `source-material/`, and `archive/`.

Use this wording as the source template when adding the policy to future repos.

## Canonical Snippet

```md
### Autonomous State & Memory Routing

You are a node in an ongoing execution chain. Optimize repository context for future agent sessions while preserving a strict boundary between active execution state, deferred future work, and durable memory.

- **Read-only execution state:** The human architect manages `tasks/` for active alignment and session handoff. You may read these files to understand current state, but do not create, edit, or manage task files unless explicitly instructed.
- **Deferred future-work routing:** Use `ai_video_saas/docs/backlog/` for non-active future-feature briefs, deferred opportunities, and preserve-for-later execution notes that should survive but are not live task state. Use dated filenames `YYYY-MM-DD__kebab-case-bookmark.md` so backlog items sort chronologically. `ai_video_saas/docs/backlog.md`, if present, should stay a thin index/summary rather than the place for full backlog writeups. Do not use `tasks/` as a backlog graveyard, and do not use `archive/` for live deferred ideas.
- **Durable memory routing:** Maintain `docs/`, `source-material/`, and `archive/` as follows:
  - **Route to `docs/`:** Store stable project truth such as decisions, invariants, contracts, and confirmed fixes. Prefer the smallest durable update that improves clarity for future sessions.
  - **Route to `source-material/`:** Store external intelligence, third-party references, web research, or seed inputs that inform the work but are not canonical project truth.
  - **Route to `archive/`:** Move content here only when it is clearly superseded by a newer canonical source and should no longer guide future work.
  - **Docs-first problem solving:** `docs/` is the higher rung. Before reading source files to understand how something works, check canonical docs first. If the topic is a deferred feature or future opportunity, also check `ai_video_saas/docs/backlog/` and `ai_video_saas/docs/backlog.md` before rediscovering intent from code or stale task files. Docs capture decisions, invariants, contracts, and architecture that code must be read to infer. Reading code to rediscover documented understanding is wasted effort — the same anti-pattern as writing custom code when the stdlib already ships it.
- **Quality bar:** Only persist information that is stable, repo-relevant, and likely to help a future agent. Do not promote transient notes, tentative hypotheses, or session-local debugging artifacts into durable memory.
- **Silent optimization:** Perform these updates opportunistically at natural workflow boundaries without asking for permission, but avoid unnecessary churn and do not archive or rewrite content unless the status is clear.
```
