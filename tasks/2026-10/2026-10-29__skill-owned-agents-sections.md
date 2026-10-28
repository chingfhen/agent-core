# Task: Make Core Skills Own Their AGENTS.md Configuration and Navigation

**File:** `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`
**Created:** 2026-10-29
**Last Updated:** 2026-10-29
**Priority:** Next
**Status:** Active

**Goal:** Let project-tasks, project-docs, knowledge-base, manage-python-env, and agent-lessons establish and maintain their own useful sections in applicable `AGENTS.md`, without requiring workspace-setup or a shared project registry.
**Why:** The human opens one workspace containing multiple projects, each potentially spanning several repositories. Each project has one shared task surface and docs surface. Immediate navigation and independently usable skills should reduce wrong-context work, repeated path discovery, and setup friction.
**Success Bar:** A fresh agent can recognize its guidance location, find the intended project/task/docs from concise AGENTS.md navigation, and use or establish a skill's resources without another skill's setup procedure. Maintenance follows authorized normal work; detailed procedures remain in the skills.
**Chosen Direction:** Architecture and illustrative section shapes approved; exact behavioral instructions require another human review before implementation.
**Current State:** Discussion preserved in this detailed handoff. No production skills, guidance, docs, installed resources, or workspace layouts changed. The existing task INDEX.md is maintained for this handoff under the current contract.
**Next Action:** When the human resumes, review this task and the proposed managed-section instructions for unintended behavior. Review/discussion is the next permitted action, not implementation.
**Blockers:** Implementation awaits human review of this task, the behavioral wording, and explicit approval to execute production skill changes.

## Permission Boundary — Read First

The final human instruction was to create a detailed implementation task, **not execute it**, because the instructions inside the proposed sections could cause unintended consequences and need another review on another day.

- Approval of the direction and section examples is not approval to implement now.
- Do not change production skills, AGENTS.md, docs, workspace resources, or publication manifests merely by resuming this task.
- Do not run sync, migrate/delete indexes, create environments, or alter installed skill copies during review.
- Task persistence and its current index entry are authorized. Further task updates follow the human's continuation request and repository rules.
- Delegation, commits, pushes, publication, and external-workspace migration are not authorized by this handoff.

## Human Context and Design Intent

- A recent agent session began coding from the wrong directory. The human noticed odd behavior but could not identify why. A minimal visible AGENTS.md path is the desired recognition signal; its absence is enough to alert the human.
- The human wants skills to depend on applicable AGENTS.md, not another setup skill. Workspace setup is rarely used and should not be an operational prerequisite.
- Work involves multiple projects, each with multiple repositories. Several repositories can share one project's task folder. The human wants to keep opening the same workspace root and refer naturally to a subject such as “get back to the forecast mismatch.”
- At discussion time there were reportedly fewer than 30 unfinished tasks across the work workspace, only a few truly active. This scale supports embedding the live task directory in AGENTS.md. The work workspace itself was not inspected in this session.
- The human values predictable `.work-context/` storage and autonomous maintenance, not another housekeeping command.
- Keep changes light: concise positive instructions, not growing lists of prohibitions, elaborate decision tables, or a configuration framework. Preserve the core job of each skill.

## Approved Decisions

### 1. Minimal startup cue

The approved display is:

```text
AGENTS.md: C:/work/AGENTS.md
```

It is requested by AGENTS.md itself, at the beginning of the first response before substantive action. This is a human recognition cue, not proof of compliance, a readiness badge, or a harness-enforced check. No global mechanism is required to detect an absent file. Multiple applicable guidance paths may be shown compactly; exact multi-file wording can be settled during review.

### 2. Independent skill-owned sections

Each participating skill establishes and maintains its own marked section:

- project-tasks: per-project task locations, concise activation/use instructions, live task directory.
- project-docs: per-project docs locations, concise instructions, curated canonical-document directory.
- knowledge-base: KB/archive configuration and concise usage instructions; content indexes stay in the KB.
- manage-python-env: Python root and concise environment-use instructions; manifests/pins/locks remain the runtime authority.
- agent-lessons: its existing marked durable lessons section; actual lessons, not fabricated boilerplate.

Detailed procedures remain in the owning skill. Human-customized section wording should survive ordinary navigation/configuration maintenance.

### 3. No required shared workspace/project schema

A shared workspace table is optional ordinary guidance. Skills can consult it when present but must work without it and must not require another workflow to create it.

Tasks and docs can record project names and destinations directly in their own sections. Python and KB do not normally need project identity. Do not reintroduce the rejected mandatory shared registration procedure or duplicate the old central destination table alongside the new authoritative locations.

New section-relative paths resolve against the directory containing the declaring AGENTS.md, not process cwd. No separate Workspace Root field is required. Existing legacy workspace-relative mappings must retain their meaning during compatibility/migration; do not reinterpret their path bases silently.

### 4. Conventional resource layout

Approved default proposal for unconfigured resources:

```text
<workspace>/
  AGENTS.md
  .work-context/
    projects/<project>/tasks/
    projects/<project>/docs/
    knowledge-base/
    archive/knowledge-base/
    python/<purpose>/
```

Established explicit locations remain valid. This repository's existing `docs/` and `tasks/` are explicitly owned surfaces; this direction does not authorize moving them into `.work-context/`.

### 5. Helpful first-use initialization

The agreed lightweight behavior:

1. Use an established configuration.
2. If configuration is absent but the relevant conventional resource clearly already exists, inspect/reuse it and register the missing configuration without another approval request.
3. If neither configuration nor the relevant resource exists, propose the conventional location and obtain approval to initialize and record it.
4. Ask when workspace identity or existing configuration is genuinely ambiguous; report inaccessible configured resources instead of inventing a replacement.

The human specifically approved autonomous recognition of existing Python purpose projects under `.work-context/python/`; lack of an AGENTS.md field should not make the agent helpless or require redundant adoption approval. A directory name alone is not evidence that arbitrary contents are compatible purpose projects.

One approval covers the stated initialization, not separate approvals for each directory/configuration line. After setup, compatible environment reuse/creation for authorized work and normal section maintenance are autonomous. Bootstrap only the invoking skill's resources; express this by positively scoped procedures rather than repeated boilerplate prohibitions.

Example first-use proposal, not a literal runtime requirement:

> Python storage is not configured or present. I propose `.work-context/python/` and will record it in `AGENTS.md`. Approve?

### 6. Task navigation moves into AGENTS.md

Replace the separate live task INDEX.md with a directory in the project-tasks section, grouped by project and then Now / Next / Later; omit empty priority groups. Include all known unfinished tasks at this scale, including blocked/deferred work. Closed tasks leave the directory but remain at stable file paths; reopening restores the entry.

Entries contain meaningful task names, links, and short recognition descriptions using the human's terminology. This is navigation, not a second task record. Detailed state, decisions, blockers, verification, and permission remain in task files.

Normal authorized task work maintains corresponding navigation automatically: creation, material purpose/priority changes, closure, and reopening. Ordinary progress checkpoints update the task, with directory changes only when navigation changes. Do not introduce background synchronization or a separate upkeep command.

For an unambiguous natural-language match, read the task and continue only its permitted next action. Ask when materially different candidates remain plausible. Avoid whole-workspace inventory on routine continuation.

### 7. Docs navigation is curated; KB navigation stays local

Project-docs owns a compact list of canonical entry points with descriptions explaining when to consult them. It maintains affected entries when documents are added, moved, merged, materially rescoped, or superseded. Not every Markdown file belongs in always-loaded guidance. Existing deeper docs navigation may remain useful, without duplicating the same top-level directory.

The KB retains its own root/monthly content indexes and selective retrieval. Do not embed every KB record in AGENTS.md. Python likewise does not need a detailed always-loaded environment inventory.

## Section Shapes — Approved Structure, Wording Pending Review

These examples use fictional projects. The human approved their shape and intent, but explicitly requested another review of the behavioral instructions before implementation. Do not copy sample projects, tasks, docs, or placeholder lessons into actual guidance.

### Project Tasks

```markdown
<!-- BEGIN PROJECT TASKS -->
## Project Tasks

- Load project-tasks before managing or continuing saved tasks.
- Match requests to the project and task descriptions below; ask when ambiguous.
- Read the selected task before acting; it owns current state and permission.
- Keep this directory current as tasks are created, reprioritized, closed, or reopened.

### Forecasting
Tasks: .work-context/projects/forecasting/tasks/

**Now**
- [Revenue reconciliation](.work-context/projects/forecasting/tasks/2026-10/2026-10-28__reconciliation.md)
  — investigate forecast/actual mismatch.

**Next**
- [APAC rollout](.work-context/projects/forecasting/tasks/2026-10/2026-10-28__apac-rollout.md)
  — extend forecasting to APAC.

### Reporting
Tasks: .work-context/projects/reporting/tasks/

**Now**
- [Monthly report automation](.work-context/projects/reporting/tasks/2026-10/2026-10-28__monthly-reports.md)
  — replace manual report assembly.
<!-- END PROJECT TASKS -->
```

### Project Docs

```markdown
<!-- BEGIN PROJECT DOCS -->
## Project Docs

- Load project-docs before maintaining project documentation.
- Consult the relevant documents below before decisions they govern.
- Preserve settled understanding in its canonical document.
- Keep this directory current when canonical documents are added, moved, or superseded.

### Forecasting
Docs: .work-context/projects/forecasting/docs/

- [Architecture](.work-context/projects/forecasting/docs/architecture.md)
  — system boundaries and repository responsibilities.
- [Forecast rules](.work-context/projects/forecasting/docs/forecast-rules.md)
  — business definitions and calculation rules.

### Reporting
Docs: .work-context/projects/reporting/docs/

- [Reporting workflow](.work-context/projects/reporting/docs/workflow.md)
  — data sources, processing, and report delivery.
<!-- END PROJECT DOCS -->
```

### Knowledge Base

```markdown
<!-- BEGIN KNOWLEDGE BASE -->
## Knowledge Base
Knowledge Base Root: .work-context/knowledge-base/
Knowledge Base Archive: .work-context/archive/knowledge-base/

- Load knowledge-base before KB operations.
- Retrieve relevant prior learning when it would help the current work.
- Capture or process the inbox when requested.
- For inbox processing, verify archival of originals before removing inbox copies.
<!-- END KNOWLEDGE BASE -->
```

### Python Environments

```markdown
<!-- BEGIN PYTHON ENVIRONMENTS -->
## Python Environments
Python Environment Root: .work-context/python/

- Load manage-python-env before running Python.
- Reuse a compatible purpose environment; create one when needed.
- Run from the code directory using the selected environment, and verify its interpreter.
- Change team Python configuration only when explicitly requested.
<!-- END PYTHON ENVIRONMENTS -->
```

### Agent Lessons

```markdown
<!-- BEGIN AGENT LESSONS -->
## Durable Agent Lessons

- When [specific situation], [action that improves future work].
<!-- END AGENT LESSONS -->
```

Keep the existing lessons mechanism; create a real section only when an evidenced lesson qualifies.

## Grounded Current Understanding

Sources read during planning:

- `AGENTS.md`: production skill edits need explicit human approval; tasks are opt-in; docs/guidance edits require project-docs. Current workspace contract still assigns centralized mapping to workspace-setup.
- `skills/project-tasks/SKILL.md`: currently requires its INDEX.md, preserves stable task paths and execution gates, and prohibits editing workspace-setup's managed map. Explicit operation-specific destinations are already allowed.
- `skills/project-docs/SKILL.md`: consumes configured Docs destinations and restricts guidance edits to explicitly owned targets. Does not mandate a universal docs INDEX.md.
- `skills/knowledge-base/SKILL.md`: has explicit location resolution, local KB indexes, requested writes and archival checks; workspace-setup currently confirms shared configuration.
- `skills/manage-python-env/SKILL.md`: `.work-context/python/` is currently a setup convention, not runtime fallback. It owns environment selection AND execution, independent uv purpose projects, team isolation, reuse, and interpreter verification.
- `skills/agent-lessons/SKILL.md`: already owns marked lessons; preserve its substantive operational-learning workflow rather than redesigning it incidentally.
- `skills/workspace-setup/SKILL.md` and `references/defaults.md`: own one central block and project table; defaults currently request briefly naming the selected skill/resource, not the proposed minimal startup cue.
- `docs/workspace-configuration.md`: current central map, workspace-root-relative paths, approval/customization, and publication boundaries.
- `docs/skill-design-guide.md`: supports distinctive jobs, concise contracts, one authoritative source, and avoiding speculative abstractions.

Candidate verification surfaces found but not yet examined: `tests/test_workspace_contracts.py`, `tests/workspace-workflow-scenarios.md`, `tests/knowledge-base-scenarios.md`, and `tests/test_python_skill_retirement.py`. Inspect them during approved implementation planning rather than assuming exact assertions.

## Remaining Human Review

The next session should review the proposed wording for behavioral side effects, not reopen settled choices without new evidence. In particular:

1. Ensure short reminders do not grant execution permission, authorize unrelated persistence, or make task prose stronger than the current human request and project instructions. The phrase “it owns ... permission” needs careful review.
2. Ensure maintenance rules preserve human-customized instructions and do not turn every read, Python run, or doc edit into a broad AGENTS.md rewrite.
3. Settle how the startup cue is inserted once and maintained without duplicated directives from every skill, including multiple applicable AGENTS.md files.
4. Settle the transition for existing centralized workspace blocks and task INDEX.md files: preserve existing mappings/content, avoid competing authorities, and define which exact migrations need explicit approval. Do not silently delete legacy navigation.
5. Decide whether workspace-setup remains an optional convenience adapted to the new sections or is retired. Only removing its prerequisite/exclusive ownership is settled; retirement/publication changes are not approved.
6. Confirm the lightweight treatment of partial existing layouts, scoped/nested guidance, and initial directory coverage. A fresh file or a folder's existence alone should not invent project identity or claim complete navigation.

These are review topics, not a request to build a comprehensive policy framework. Keep the final skill changes short and focused.

## Implementation Phases — After Explicit Approval

### Phase 1: Approve the behavioral contract

Review this task with the human, refine the concise section instructions, and settle the material transition/startup/workspace-setup choices above. Record the resulting decision and implementation permission. Stop here until that approval exists.

### Phase 2: Implement independent configuration and ownership

Update the canonical participating skills with short first-use/configuration maintenance procedures and approved section shapes. Remove mandatory workspace-setup/shared-map dependencies while preserving each skill's main workflow and meaningful safety/permission boundaries. Preserve existing lesson ownership.

Implement the approved startup instruction placement. Keep relative paths anchored to their declaring guidance, including explicit handling of old path semantics. Prefer direct prose and small skill-local references only if needed; do not create a required new shared skill, registry, generator, or bootstrap package.

### Phase 3: Integrate navigation and compatibility

Move task navigation responsibility to its AGENTS.md section under the approved transition policy. Preserve task metadata, stable paths, execution gates, and closure/reopening semantics. Add curated docs navigation maintenance; retain KB indexes and real Python compatibility checks.

Adapt or retire workspace-setup according to the reviewed decision. Replace contradictory canonical guidance/docs and directly affected references using project-docs. Relevant candidates include `AGENTS.md`, `docs/workspace-configuration.md`, `docs/agent-core-operating-manual.md`, `docs/skills-catalog.md`, README, workspace defaults, and publication manifests only if a selected publication change requires them.

Do not broaden this into migration of employer workspaces, installed copies, unrelated docs, or this repository's data layout. Actual workspace migration/publication needs identified targets and authorization.

### Phase 4: Verify behavior and close honestly

Inspect existing contract tests/scenarios, update affected expectations, and add focused cases below. Run applicable checks through manage-python-env if Python execution is required; any new local initialization follows the currently applicable permission contract.

Review the resulting instructions for readability, contradiction, duplicate authority, and unwanted side effects. Report automated checks separately from prompt/scenario review and actual fresh-session observations. Do not claim harness loading or compliance from static text tests alone.

## Acceptance and Verification

Demonstrate, with proportionate tests/scenarios and explicit gaps:

- **No setup dependency:** each owning skill can begin with no central workspace block or project table. KB/Python do not require an invented project identity.
- **Approved initialization:** a genuinely unconfigured, absent resource produces a concrete location proposal and waits for approval; approval records the configuration and permits the stated initialization.
- **Existing Python resources:** identifiable existing purpose projects are inspected/reused and the missing section is recorded without redundant adoption approval; compatible environments are selected through actual manifests/pins/locks.
- **Correct context:** missing/ambiguous workspace identity is not silently equated with cwd. A configured inaccessible root is reported, not replaced.
- **Path resolution:** changing process cwd does not redirect section-relative outputs; legacy mappings retain their intended base until explicitly migrated.
- **Task discovery:** a natural-language request resolves a clear entry across multiple projects/repositories and reads the selected task; materially ambiguous matches trigger a focused question.
- **Task lifecycle:** creation, navigation changes, closure and reopening update only appropriate entries; unfinished blocked/deferred tasks remain discoverable, closed files remain stable, and task progress does not become duplicated central state.
- **Docs navigation:** canonical additions/moves/supersession update affected entry points; ordinary document edits do not require enumerating every file or maintaining a competing index.
- **KB/Python scope:** KB content indexes remain local; Python execution still uses/verifies the selected environment and preserves team configuration unless explicitly authorized.
- **Customization and shared file:** unrelated sections and human wording survive targeted maintenance; malformed/ambiguous markers or detected concurrent changes do not get overwritten blindly.
- **Permission fidelity:** a directory entry, task priority, configuration registration, or readable task is not new execution authorization. Repository-specific restrictions remain effective.
- **Startup cue:** approved guidance produces the minimal factual path cue at the first response; absence of guidance has no fabricated success claim. Label any actual harness checks versus hypothetical scenarios.
- **Transition:** no duplicate authoritative destination table or competing live task index remains in a migrated scope; no silent relocation/deletion or unapproved external-workspace changes occur.
- **Partial maintenance:** if task/document persistence succeeds but its navigation update fails, preserve valid work and report the exact incomplete navigation instead of claiming completion.

Existing sessions may retain stale loaded guidance after another session edits AGENTS.md. The directory helps selection; rereading the selected task establishes current task truth. This task does not promise live cross-session reload or a locking service.

## Executor Discretion and Stop Conditions

After implementation approval, routine prose organization, targeted link repair, filenames for skill-local supporting references, and test mechanics are executor-owned. Human-owned choices remain exact behavioral approval, material migration scope, workspace-setup retirement, publication, and any altered permission boundary.

Stop and surface the specific issue if an implementation requires widening scope, changing approved storage/ownership, migrating existing user resources, overwriting customization, or bypassing an established constraint. Do not solve uncertainty by expanding the shared configuration architecture.

## Related Work and Resume Cue

- Related but distinct: [Durable Learning Mechanism for Operational Constraints](../2026-10-23__durable-agent-constraint-learning-bookmark.md). That task concerns propagation of operational constraints; this task concerns skill-owned configuration/navigation and a minimal startup cue. No supersession or closure of that task is implied.
- Worktree at handoff already contained changes to `tasks/INDEX.md`, an untracked `docs/pi-opencode-shortcuts.md`, and an existing untracked October shortcut task. Preserve those unrelated changes.
- This handoff adds only this task and its current INDEX.md entry. No implementation checks have run.

**Resume:** “Review `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`, especially the managed-section instructions and their unintended effects. Do not implement until I approve.”
