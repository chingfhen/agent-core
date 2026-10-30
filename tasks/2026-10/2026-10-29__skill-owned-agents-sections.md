# Task: Make Core Skills Own Lean AGENTS.md Routing and Operational Lessons

**File:** `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`
**Created:** 2026-10-29
**Last Updated:** 2026-10-30
**Priority:** Next
**Status:** Active

**Goal:** Let project-tasks, project-docs, knowledge-base, manage-python-env, and agent-lessons maintain useful, lean sections in applicable `AGENTS.md`, without requiring workspace-setup or a shared registry.
**Why:** Improve resource discovery and before-action skill activation across multi-project/multi-repository workspaces without turning always-loaded guidance into a runbook.
**Success Bar:** Guidance contains confirmed locations, selective entry points, minimal activation cues, and only essential before-action rules. Detailed procedures live in skills or selectively read references. Existing permissions, customization, and resource locations survive.
**Chosen Direction:** Approved: lean skill-owned routing, retained task indexes, first-use/ownership rules, and the two-layer operational-lessons extension. No design approval remains pending for that scope.
**Current State:** Audit and implementation reconnaissance completed; detailed handoff and docs sync saved. `docs/workspace-configuration.md` distinguishes the approved target from the current unmodified skills. `AGENTS.md` records the steward's skill-quality responsibility. No production skills, tests, installed copies, or workspace resources changed; no Python or fresh-session behavioral checks executed.
**Next Action:** Review this merged task with the human in a fresh session. Implementation is deferred until the human says to proceed after that review; do not automatically start from the earlier execution instruction. Then implement, verify, reconcile docs to delivered behavior, and close honestly.
**Blockers:** No unresolved design decision within approved scope. Execution awaits the requested fresh-session review/go-ahead; Python checks additionally need an approved environment destination (see Verification Environment).

## Permission Boundary

The human approved the core audit recommendations, then explicitly approved the two-layer lessons extension. The latest instruction is to update this task in detail, sync to docs, and review/execute in a fresh session. That changes execution timing, not the settled design.

- Authorized now: detailed task/index handoff, docs sync of settled design with accurate implementation status, and recording the steward's quality responsibility in owned guidance.
- Approved scope for later execution: canonical production skill/template changes, directly affected tests and guidance/docs integration, and honest task closure. Wait for the human's go-ahead following the requested fresh-session review before implementing.
- The companion design is approved; individual future workspaces still require initial companion location/ownership approval. This is not authorization to create a companion in this checkout or an employer workspace now.
- Not authorized: external/employer workspace migration, copying workplace-specific operational material into this personal repository, installed-copy edits, publication/sync, delegation, commits, or pushes. These remain separate from docs sync.
- Preserve stricter local rules, including opt-in task writes or approval-gated docs/tasks/KB operations. Configuration is not new execution or persistence permission.
- Do not close merely because the prose has been edited. Record actual checks and remaining limits; static tests do not prove harness compliance.

## Approved Core Decisions

### 1. Always-loaded admission rule

`AGENTS.md` primarily contains routing plus a few essential before-action rules. Keep information always loaded only when it helps select the right context or prevents a consequential mistake before deeper instructions are read.

Procedures and maintenance rules belong in their owning skills, not abbreviated mini-workflows in the managed sections. Remove reminders about index upkeep, canonical integration, environment reuse/verification mechanics, and archive-before-delete steps from the creation-time section templates; preserve the complete procedures in the skills.

A pointer needs a short consultation trigger. Reading relevant project rules is distinct from invoking the skill that maintains their documentation. No universal line limit or required quota is implied.

### 2. Independent skill-owned sections

| Owner | Always-loaded content | Detail elsewhere |
| --- | --- | --- |
| project-tasks | Per-project task root and descriptive task-index link; one activation cue | All unfinished task navigation in each task INDEX.md; state/gates in task files |
| project-docs | Per-project docs root and a few canonical entry points with when-to-read descriptions; reading/maintenance cues | Architecture, rules, rationale, deeper navigation in docs |
| knowledge-base | Confirmed KB/archive locations and optional established backend/knowledge-page configuration; one routing cue | Content indexes and records inside KB; storage/archival workflow in skill |
| manage-python-env | Confirmed Python root and one activation cue | Environment inventory/compatibility from manifests, pins, locks and runtime; execution procedure in skill |
| agent-lessons | Narrow marked section for essential before-action rules and conditional pointers | Existing canonical references first; explicitly designated companion for otherwise homeless operational learning, as approved below |

Do not require a central project registry or workspace-setup invocation. KB/Python normally need no project identity. Existing shared repository/project navigation may remain useful ordinary guidance; it is not a mandatory schema.

### 3. Predefined wording versus maintained data

- **Predefined:** markers, headings, field labels, and minimal creation-time activation cues.
- **Skill-maintained:** confirmed paths and directly affected navigation entries.
- **Human-customized:** behavioral wording, preserved unless its change is explicitly approved.
- **Skill procedures:** remain in SKILL.md; routine maintenance never copies them into guidance.

Managed does not mean regenerate. Each skill owns only its declared section; general project-docs guidance ownership does not authorize rewriting another skill's block. Preserve outside text and block positions. Refuse ambiguous/duplicate/incomplete/nested markers; reread before mutation, reconcile detected concurrent changes safely, and read back the result.

### 4. Resource resolution and first use

1. Use established configuration, including operation-specific human-selected destinations without silently changing the saved configuration.
2. During authorized operational use, inspect/reuse an unambiguous existing conventional resource and register missing configuration in the skill's owned section without redundant adoption approval. Read-only inspection does not itself authorize configuration writes.
3. If neither configuration nor suitable resource exists, propose the conventional location and obtain one approval covering initialization and registration.
4. Ask when workspace/project identity, ownership, or destination is ambiguous; report an inaccessible configured resource rather than substituting another.

Folder existence alone does not prove identity, ownership, or compatibility. Existing Python purpose projects require actual recipe inspection, not adoption by folder name. Once configured, compatible reuse/creation for authorized work follows manage-python-env. Initialize only the invoking skill's resources; preserve narrower local write gates.

New section-relative paths resolve against the directory containing the declaring AGENTS.md, not process cwd. Legacy workspace-relative mappings retain their recorded base until explicitly migrated. Do not infer the workspace from cwd or a Git root alone.

Conventional proposals remain:

```text
<workspace>/
  AGENTS.md
  .work-context/
    projects/<project>/{tasks,docs}/
    knowledge-base/
    archive/knowledge-base/
    python/<purpose>/
```

Established paths remain valid. Agent Core keeps its canonical `docs/` and `tasks/`. Preserve explicitly configured cross-project task surfaces rather than forcing them into an invented project. Preserve KB remote locators and optional Knowledge Base Knowledge destinations. An archive is needed for inbox processing, not ordinary retrieval.

### 5. Task indexes stay outside AGENTS.md

**This supersedes the original approved proposal to embed every unfinished task in AGENTS.md and remove INDEX.md.** The human explicitly approved this reversal after the audit.

Keep each task INDEX.md, with all known unfinished work, Now/Next/Later navigation, stable task paths, and closure/reopening behavior. AGENTS.md links to that index once per project with a short recognition description. Routine task lifecycle/progress changes do not rewrite AGENTS.md unless the root/index routing changes.

Natural-language continuation selects the project/index, then reads the selected task before its next permitted action. Ask when materially different candidates remain plausible. Avoid whole-workspace inventory. Navigation and task priority do not grant authority; task files record prior approvals/gates rather than independently owning permission. Confirm relevant code repositories from the task or a project entry point before acting: finding shared docs/tasks alone does not establish code cwd.

### 6. Minimal startup cue and optional setup

The approved first-response cue is factual, for example `AGENTS.md: C:/work/AGENTS.md`. Multiple applicable paths can appear compactly. It is recognition, not proof of compliance or harness loading.

Use one separately approved startup instruction outside the five skill blocks, not repeated directives inserted by every skill. Establish it during approved guidance initialization/update; ordinary section maintenance preserves it. Do not fabricate an absent file or promise cross-session live reload.

Retain workspace-setup as an optional, explicitly invoked convenience adapted to the independent sections, not their prerequisite or exclusive owner. Do not retire it or change publication manifests incidentally. Do not create a new required shared skill, registry, generator, or configuration framework.

Migration of existing central blocks requires identified targets and approval. Preserve custom Behavior/Use for text and repository annotations; do not leave competing authoritative destination tables. No task-index deletion is now needed. No external workspace migration is included in this task.

## Approved Creation-Time Section Shapes

Fictional examples only; use real confirmed values in actual guidance. Preserve established human wording instead of resetting to these templates.

### Project Tasks

```markdown
<!-- BEGIN PROJECT TASKS -->
## Project Tasks
Load project-tasks before managing or continuing saved tasks.

### Forecasting
Tasks: .work-context/projects/forecasting/tasks/
- [Task index](.work-context/projects/forecasting/tasks/INDEX.md)
  — unfinished forecast reconciliation and rollout work.
<!-- END PROJECT TASKS -->
```

### Project Docs

```markdown
<!-- BEGIN PROJECT DOCS -->
## Project Docs
Consult relevant entry points below for project decisions.
Load project-docs before maintaining documentation or owned guidance.

### Forecasting
Docs: .work-context/projects/forecasting/docs/
- [Architecture](.work-context/projects/forecasting/docs/architecture.md)
  — repository responsibilities and system boundaries.
- [Forecast rules](.work-context/projects/forecasting/docs/forecast-rules.md)
  — definitions governing forecast calculations.
<!-- END PROJECT DOCS -->
```

### Knowledge Base

```markdown
<!-- BEGIN KNOWLEDGE BASE -->
## Knowledge Base
Knowledge Base Root: .work-context/knowledge-base/
Knowledge Base Archive: .work-context/archive/knowledge-base/

Use knowledge-base for relevant prior context and requested KB writes.
<!-- END KNOWLEDGE BASE -->
```

### Python Environments

```markdown
<!-- BEGIN PYTHON ENVIRONMENTS -->
## Python Environments
Python Environment Root: .work-context/python/

Load manage-python-env before Python execution or environment changes,
including interpreter checks and import probes.
<!-- END PYTHON ENVIRONMENTS -->
```

Including probes is a bounded trigger clarification, not a rename or new environment policy. Merely inspecting a path or source file is not Python execution.

### Agent Lessons — approved two-layer shape

```markdown
<!-- BEGIN AGENT LESSONS -->
## Durable Agent Lessons

- Before creating a PR, consult the
  [PR procedure](agent-lessons.md#pull-requests).
- Before designing dataset operations, consult the
  [deployed-platform constraints](agent-lessons.md#dataset-platform).
<!-- END AGENT LESSONS -->
```

Illustrative only: create neither sample lessons nor an empty companion. Keep essential guards inline when they must shape action before retrieval. Use actual stable reference paths/headings and preserve existing marker names.

## New Evidence: Skill Activation and Lessons Growth

The human supplied an existing employer workspace AGENTS.md and an excerpt of a Devin conversation. Treat them as supplied evidence, not current local instructions or independently verified workplace state. Do not copy internal hostnames, credentials procedures, account details, package pins, or operational content into personal production guidance/test fixtures; use synthetic examples.

Observed from the supplied material:

- Python root and activation instructions were already present, but separated by a large resource/skills map and many operational details.
- The lessons section mixed useful constraints with API payloads, version-specific capability inventories, incident fixes, package pins, credential procedures, and long commands.
- A saved environment inventory listed one purpose while the agent later reported three, illustrating snapshot staleness.
- Devin reported selecting/checking a repository-local interpreter before loading manage-python-env, then discovered purpose environments after the human corrected it.
- The shown follow-up command inspected imports/manifest text; it did not yet verify interpreter selection or successful workload execution.
- The original command is not available here. Merely checking a file's existence is not Python execution; do not claim an execution violation without the tool trace. Retrospective agent explanations do not prove the exact internal cause.

Inference, not proof: competing always-loaded detail and a familiar repository-local environment may contribute to missed skill activation. The current description already explicitly covers all Python execution/testing/evaluation/tooling; renaming is not justified by this evidence. Colocate configuration and activation cue, include probes in the trigger, and test the first executable command.

The existing agent-lessons skill already says to consolidate, avoid duplicated rules, and keep command catalogues/incident histories out of guidance. A longer reminder alone does not solve noncompliance. The new design must demonstrate selective retrieval and consolidation rather than relocating an ever-growing transcript.

## Approved Lessons Extension

**Decision approved 2026-10-30:** two layers, with existing canonical sources preferred over a new duplicate. This extends the approved core work; it does not replace or reopen it.

1. The marked AGENTS.md lessons section keeps a small set of situation-specific pointers and only constraints that must be visible before the reference would be opened. Do not require literal pointer-only guidance when that would hide a critical gate. Never instruct agents to read the whole companion on every session.
2. Reuse existing discoverable project docs/KB runbooks for detail through their owning workflows. For operational learning without a suitable existing home, agent-lessons may maintain one explicitly designated companion reference for that guidance scope. Approved first-use proposal: `agent-lessons.md` beside the declaring AGENTS.md; a human-selected existing path is equally valid. Each workspace still needs initial location/ownership approval, not a silent fallback or mandatory file for every project.
3. Link directly to relevant headings with when-to-read cues. The link records the companion location; no extra registry or machine-specific absolute path is needed. Group by operational topic; preserve consequential scope/version qualifications, not chronological transcripts. Update/consolidate relevant content rather than append every incident.
4. Explicit agent-lessons invocation authorizes proportionate maintenance of its marked section and the designated companion within local permission rules. It does not acquire ownership of arbitrary linked docs, KB records, other guidance sections, or executable tooling. Use the relevant owning workflow for those surfaces. If the companion lies in an existing configured docs/KB surface, respect that workflow too.
5. Create no empty companion or fabricated lessons. Persist/verify supporting material before shortening an existing lesson; retain critical restrictions in guidance when needed before retrieval. Removing/moving existing human content requires the appropriate approval and preservation of meaning.
6. Existing duplication is a reason to consolidate, not add another Python rule to lessons. The Python activation cue belongs in its own section. Do not move generic skill procedures into the companion as a second authority.

Trade-offs accepted: an extra read and another scoped file to maintain; selective pointers can be missed. This is context management, not deterministic enforcement. The companion must not be loaded wholesale or become a second competing KB. No employer-workspace rewrite is authorized by approval of this implementation contract.

### Companion content and maintenance contract

The companion is a selectively read operational reference, not a chronological lesson ledger or a second generic skill manual. Use topic headings, short applicability/version qualifications where needed, and the minimum procedure/checks required to act correctly. Point to existing sources instead of copying their entire content. One file per designated guidance scope is sufficient; do not invent monthly folders, a database, quotas, or an additional index.

Examples of routing, using synthetic rather than workplace content:

| Learning | Always-loaded consequence | Selectively read detail |
| --- | --- | --- |
| PR creation procedure | Before creating a PR, consult the procedure; preserve a critical base-branch guard if needed | Payload shape, commands, verification, timeout caveats |
| Version-specific platform limitations | Consult deployed-version constraints before designing operations | Capability matrix, probes, workarounds and version evidence |
| Package/download failure | Consult the troubleshooting reference when the matching failure occurs | Historical diagnosis and still-valid recovery steps; not universal package pins |
| Existing skill missed | Improve the owning section's activation cue if justified | Do not create a duplicate lesson or a second copy of the skill procedure |

Apply the current skill's evidence/admission test before retaining anything. Keep hard permission/package/security boundaries discoverable before action. An invocation may correctly make no changes. Do not shorten a lesson until its useful supporting detail is safely retained and its pointer resolves. If archival/movement is blocked by permissions or inaccessible references, keep the valid existing content and report the gap instead of deleting it.

## Implementation Work

### Phase 1: Fresh-session review, then execution go-ahead

Read this task and the canonical approved-target contract in `docs/workspace-configuration.md`. Show the human the merged direction and any genuinely new conflict; do not ask them to reapprove each settled choice. Respect the requested review-before-execution sequence. After the human says to proceed, inspect current worktree/source state and execute within the approved scope. Resolve the Python destination only before Python checks; do not run later-stage preflight just to review the task.

### Phase 2: Implement skills and templates

Update canonical project-tasks, project-docs, knowledge-base, manage-python-env, and agent-lessons within approved scope. Add concise skill-local first-use/section-maintenance procedures while preserving each substantive workflow. Implement approved lean templates and ownership boundaries. Keep task/KB indexes local and Python recipes authoritative. Adapt workspace-setup/defaults as an optional convenience without a second location authority.

Resolve the current discrepancy between agent-lessons' broader supporting-resource workflow and repository guidance describing only its marked section. Express narrow direct ownership and use of other owning workflows consistently; do not treat this as blanket expansion of write permission.

#### Focused change map

| Surface | Required implementation outcome |
| --- | --- |
| `skills/project-tasks/SKILL.md` | Own task-root/index-pointer section; independent first use; keep existing INDEX.md lifecycle and gates; no inline live task dashboard |
| `skills/project-docs/SKILL.md` | Own docs-root/curated-entry-point section; independent first use; respect other marked owners and explicitly owned guidance only |
| `skills/knowledge-base/SKILL.md` | Own root/archive/optional existing configuration section; preserve backends, selective recall, requested writes, local indexes, verified archival |
| `skills/manage-python-env/SKILL.md` | Own root/activation section; compatible existing-purpose adoption; clarify probe trigger; preserve team isolation, recipes, idle checks and actual interpreter verification |
| `skills/agent-lessons/SKILL.md` | Implement approved conditional-pointer/critical-rule layer plus explicitly designated companion; reuse existing sources; consolidate rather than accumulate; verify pointers and preserve scope |
| `skills/workspace-setup/SKILL.md`, `references/defaults.md` | Optional approved initialization/refresh using owning section contracts; preserve customized legacy blocks until approved migration; no central inventory/schema dependency |
| `AGENTS.md`, `docs/workspace-configuration.md`, `docs/agent-core-operating-manual.md`, `docs/skills-catalog.md`, README | Reconcile current-vs-target language only when delivered; preserve stewardship approval boundaries and existing local resource layout |
| `tests/test_workspace_contracts.py`, `tests/workspace-workflow-scenarios.md`, affected KB scenarios | Test the new structure/ownership contracts, remove obsolete exact-block assertions, and add bounded behavioral trial cases |

Routine wording, small skill-local supporting files, and test mechanics are executor-owned. Material changes to write permission, default storage, publication, or migration scope require renewed approval. Do not solve independence by introducing a mandatory shared setup/reference dependency.

### Phase 3: Verify and sync settled truth to docs

Update affected static tests and synthetic scenarios. Check preserved custom wording/positions, legacy path semantics, no-setup first use, retained indexes, missing/inaccessible/ambiguous resources, permission fidelity, partial-write reporting, and startup-cue placement.

Update canonical `docs/workspace-configuration.md`, directly affected operating-manual/catalogue/README material, and steward AGENTS.md through project-docs. Keep the main contract in focused docs rather than duplicating it in always-loaded guidance. Preserve Agent Core's existing data layout and publication allowlists.

### Phase 4: Close honestly

Inspect the scoped diff and actual test results. Distinguish automated structural checks, manual scenario review, and fresh-session behavioral trials. Record outcomes and limitations, remove this task's index entry only when required work is complete, and leave its file at its stable path. Publication and external workspace adoption remain separate operations.

## Acceptance and Verification

- Each skill operates without a central map/setup dependency; roots resolve against declaring guidance, including nested scopes and changed cwd.
- Existing explicit locations/operation-specific selections, cross-project task surfaces, KB remote backends/optional knowledge roots, and legacy path bases remain valid.
- Unconfigured absent resources produce one initialization proposal; clear compatible existing resources can be registered during authorized use, not read-only inspection. Folder presence alone is insufficient.
- A readable task/index/configuration is not authorization. Stricter repository or human write gates survive migration.
- Task lifecycle keeps INDEX.md current without routine AGENTS.md churn; blocked/deferred tasks remain discoverable and closed files stay stable. Unknown initial coverage is reported rather than claimed complete.
- Docs navigation stays curated; KB records and Python inventories are not copied into guidance. Existing docs entry points can identify code repositories without a mandatory registry.
- Targeted changes preserve human wording, unrelated blocks and position; malformed markers/concurrent edits cause safe refusal or reconciliation. Partial navigation failure preserves valid primary work and is reported precisely.
- Python regression: provide both repository `.venv` and purpose environments, request an interpreter/import probe without naming the skill, and inspect whether the skill is read before Python execution. Confirm actual executable/prefix under the selected purpose environment. Selecting a repository bootstrap script does not implicitly select its environment.
- Lessons regression: a long synthetic operational recipe is routed to a relevant existing reference or approved companion with a conditional pointer, critical pre-action guards preserved, and no mandatory whole-file read. Existing Python routing prevents a duplicate lesson. Unavailable reference/missing approval cannot cause deletion of the only useful content.
- Startup cue is one factual path display, not a compliance claim or duplicated skill directive. Existing sessions are not promised automatic reload.
- No installed-copy changes, external-workspace migration, silent index deletion, unapproved resource relocation, or publication.

### Verification surfaces and known defect

Read during audit: `tests/test_workspace_contracts.py`, `tests/workspace-workflow-scenarios.md`, and the relevant initial part of `tests/test_python_skill_retirement.py`. `tests/knowledge-base-scenarios.md` remains to inspect as needed.

Scenario 4 in workspace-workflow-scenarios currently expects moving the block to the end, contradicting the current preserve-position contract; correct this in scope. Existing static tests assert the legacy single workspace block and exact-output response; adapt them to the approved contract rather than merely keeping obsolete strings.

Fresh-session target-harness trials have not run. Do not claim Devin/Pi compliance from static prose tests, synthetic fixture inspection, or agent self-report alone.

### Verification Environment

Current checkout has no configured Python root. `.work-context/python/` exists but is empty. `.agent-envs/verification/` contains an independent uv project with an empty dependency list, `[tool.uv.workspace]`, uv.lock, Python 3.10.18 pin, and a .venv. Its interpreter/idle state has not been verified. uv 0.7.13 is available.

A focused question proposed reusing `.agent-envs/verification` for this operation only (no saved-map change), or initializing/recording the conventional root. It received no answer before the user supplied more context. Do not treat that interruption as approval, adopt an empty directory as a compatible resource, or fall back to the repository environment. Obtain the destination decision before Python execution once implementation resumes. The latest handoff request defers production edits too; do not use this verification note to bypass the fresh-session review.

## Handoff and Docs Sync — 2026-10-30

- Settled design is documented in `docs/workspace-configuration.md` under the explicitly labeled approved target, not represented as current shipped skill behavior. This task owns execution state and detailed implementation/verification handoff; the doc owns the durable contract.
- `AGENTS.md` records the steward's responsibility to oversee skill effectiveness, reliability and robustness, investigate observed failures, propose proportionate improvements, and implement production changes after explicit human approval. This is ongoing stewardship, not autonomous permission to rewrite skills.
- This session changed only this task, `tasks/INDEX.md`, the canonical workspace doc, and the small stewardship/status clarification in `AGENTS.md`. Production skills/tests, installed copies, manifests and external resources remain unchanged.
- Handoff verification is limited to rereading changed text, checking referenced local files, permission/status consistency, and `git diff --check`. No implementation tests or fresh-session harness trials have run. A successful handoff is not task completion.
- Working tree already contained this task/index revision from the preceding approval gate. Preserve those and any other concurrent changes; no commit or publication is included.

## Related Work and Resume

[Durable Learning Mechanism for Operational Constraints](../2026-10-23__durable-agent-constraint-learning-bookmark.md) remains related but distinct; do not close or rewrite it incidentally. No shared propagation/enforcement system is added here.

**Resume:** "Review `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`. The merged core and two-layer lessons design are approved. Review the handoff with me before implementation; then proceed when I give the go-ahead. Keep task indexes, preserve local approval gates, verify honestly, and do not publish or migrate external workspaces."
