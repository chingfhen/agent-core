# Task: Introduce a personal Project Scripts skill

**File:** `tasks/2026-11/agent-workflow/2026-11-02__personal-project-scripts-skill.md`
**Created:** 2026-11-02
**Last Updated:** 2026-11-02
**Priority:** Now
**Status:** Closed

**Goal:** Add an independent, explicitly invoked `project-scripts` skill to convert worthwhile recurring agent procedures into usable, deterministic personal scripts.

**Chosen Direction:** One configured personal Project Scripts Root, consistent domain-based organization and discoverable commands. The skill reviews the active conversation, reuses/maintains scripts before creating new ones, and may conclude no change is worthwhile. Optimize for less future agent work **and** easy human use. Favor argument-driven CLIs, sensible logs, failure visibility, and proportional tests.

**Boundaries:** Personal utilities, not shared project code; a script is shared only by an explicit later decision. Do not modify any existing skill or automatically trigger this skill from engineering, agent-lessons, or task handoff. Do not execute script side effects without applicable permission.

**Deliverable:** New `skills/project-scripts/SKILL.md` (plus focused authoring reference if useful), personal installation manifest entry and skills catalogue entry on `main`. No personal script or workspace storage root needs to be created until the first actual script request.

**Outcome:** Completed 2026-11-02. Created [`skills/project-scripts/SKILL.md`](../../../../skills/project-scripts/SKILL.md) and [`references/cli-craft.md`](../../../../skills/project-scripts/references/cli-craft.md). Registered in `personal-skills.toml` and `docs/skills-catalog.md`, directly on `main`. Verified remote file contents and cross-references; not runtime-tested in Pi/OpenCode, and no script collection was initialized because no actual script was requested.

**Next Action:** None for this task. First actual script invocation should resolve/approve one personal Project Scripts Root, then initialize it only if a script qualifies.
