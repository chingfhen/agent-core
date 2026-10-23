# Task: Durable Learning Mechanism for Operational Constraints

**File:** `tasks/2026-10-23__durable-agent-constraint-learning-bookmark.md`
**Created:** 2026-10-23
**Last Updated:** 2026-10-23
**Priority:** Next
**Status:** Active

**Goal:** Find a durable mechanism that propagates operational hard constraints (e.g. OCBC Nexus-only package rules) to every new agent session, without repeating a manual workaround per constraint.

**Why:** Each hard constraint currently requires an ad-hoc patch — a new Behavior bullet, a new KB pointer, a new rule file. The next constraint means doing it all again. Devin Desktop has no memory; the KB is only consulted when an agent chooses to read it; skills only load when the task matches their description. The human wants a structural long-term solution, not accumulating one-off patches. Human accepted the ad-hoc approach as an interim measure on 2026-10-23.

**Success Bar:** Adding one operational constraint in one place makes it reliably visible to future agent sessions across harnesses/workspaces — without re-editing each consumer surface and without relying on the agent electing to look.

**Chosen Direction:** Not selected — human is taking the question outside this repo to evaluate options (harness memory/preload features, hook mechanisms, agent-core extensions, or a different skill distribution model).

**Current State:**
- Interim measure in place (2026-10-23): six OCBC environment constraint bullets added to the Behavior section of the `repos\AGENTS.md` managed block, routing to the `dev-environment` KB page and `scripts/setup_env.py` for detail.
- Mechanisms inventoried and their limits: always-loaded AGENTS.md (works, but small and manual), skills (fire only on description match — not guaranteed), KB (read-on-choice), published skills (only exposed at session start — `workspace-setup`, `commit-with-subagent`, `mermaid-markdown`, `ml-architecture-review` were on disk but unexposed this session).
- `manage-ocbc-python-envs` at `.work-context/skills/` is stale, intentionally superseded by `manage-python-env`; OCBC-specific knowledge lives in the KB (`dev-environment` page + `infra` records) and in `setup_env.py` as executable logic.

**Next Action:** Human explores long-term options outside this repo. No implementation approved.

**Blockers:** None — exploratory; the next step is human-owned evaluation.

**Human Attention:** Task is human-owned; agent created it for continuity only.

**Context Pointers:**
- `repos\AGENTS.md` — managed block, Behavior section (interim constraints)
- `repos\.work-context\knowledge-base\records\2026-10\infra\2026-10-23--repos-workspace-managed-block-setup.md` — session record
- `repos\.work-context\knowledge-base\knowledge\dev-environment.md` — the constraint source of truth
- `repos\bitbucket-smart-search\smart-search-chatbot\scripts\setup_env.py` — constraints encoded as executable bootstrap
- `~/.agent-core/skills/workspace-setup/SKILL.md` — managed-block contract (relevant if the mechanism becomes block-shaped)
