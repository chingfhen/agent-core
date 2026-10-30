---
title: Workspace Configuration
description: Canonical resource-routing and managed-guidance contract for personal workspaces.
updated: 2026-10-30
---

# Workspace Configuration

## Read First

- **Implementation status:** the canonical production skills still use the current
  centralized workspace contract documented below. The lean skill-owned design is
  approved, but has not yet been implemented or published. Approval does not
  migrate existing workspaces or activate new write permissions.
- This document owns the durable workspace contract. The
  [implementation task](../tasks/2026-10/2026-10-29__skill-owned-agents-sections.md)
  owns execution state, the fresh-session review gate, and verification results.

## Approved Target — Lean Skill-Owned Guidance

Approved on 2026-10-29/30; implementation pending. This section describes intended
behavior, not an instruction to bypass the currently installed skills.

### Always-loaded admission

`AGENTS.md` primarily contains routing and a few essential before-action rules.
Keep information always loaded only when it helps select the right context or
prevents a consequential mistake before deeper instructions are read. Useful
information does not necessarily belong in every session.

Each pointer includes a short when-to-read cue. Procedures and maintenance rules
stay in their owning skills; operational detail belongs in selectively read
references. No universal line limit or required quota replaces this admission
judgment. Short guidance can still fail to activate a skill: clarity is not
mechanical enforcement, and agent self-report is not execution evidence.

### Section ownership and content

| Owner | In its marked AGENTS.md section | Outside always-loaded guidance |
| --- | --- | --- |
| project-tasks | Task roots and one descriptive task-index link per project; activation cue | All unfinished task navigation in INDEX.md; state and recorded gates in task files |
| project-docs | Docs roots and a few canonical entry points with consultation cues; maintenance activation cue | Detailed project truth and deeper navigation in docs |
| knowledge-base | KB/archive roots and established optional backend/knowledge location; routing cue | KB content indexes and records; capture/archival procedures in skill |
| manage-python-env | Python root beside the execution/environment-change activation cue | Purpose inventory and compatibility in recipes/runtime; procedures in skill |
| agent-lessons | Essential before-action constraints and conditional reference pointers | Existing canonical runbooks first; explicitly designated companion only when needed |

Task INDEX.md files remain in their task surfaces; moving every unfinished task
into AGENTS.md is rejected. Routine task state changes do not churn standing
instructions. KB indexes also stay local; Python environment snapshots do not
become a second runtime authority. Python execution includes interpreter checks
and import probes, but not merely inspecting a file's existence. A repository
bootstrap script does not implicitly authorize its repository-local environment.

The skill supplies markers, headings, field labels and minimal creation-time
activation wording. Normal maintenance changes confirmed paths and affected
navigation entries, not human-customized behavioral wording or unrelated blocks.
Preserve position and outside text, refuse ambiguous markers, and verify targeted
writes. General docs/guidance ownership does not override another skill's section
ownership. Initial defaults do not authorize later whole-block regeneration.

### Independent configuration and compatibility

Each skill can establish its own resources without workspace-setup, a central
project table, or another mandatory registration workflow. Optional repository
navigation remains useful; tasks or project entry points must identify relevant
code repositories before execution. Finding a shared task folder does not establish
code cwd. KB/Python need not invent a project identity.

Use established configuration first. During authorized operational use, a skill
may inspect/reuse an unambiguous existing conventional resource and register its
missing configuration in its owned section; read-only inspection alone does not
authorize writes. A folder name is not proof of ownership or compatibility. If
neither configuration nor suitable resources exist, obtain one approval for the
specific initialization and registration. Ask about ambiguity; report inaccessible
configured resources instead of inventing alternatives. Narrower local write gates
remain binding.

New relative paths resolve against the declaring AGENTS.md directory, not cwd.
Legacy workspace-relative mappings retain their recorded base until an explicitly
approved migration. Preserve operation-specific destinations, cross-project task
surfaces, KB remote locators/optional knowledge roots, and existing storage layouts.
The conventional `.work-context/` layout remains a proposal, not an automatic
fallback. Agent Core retains its own canonical `docs/` and `tasks/`.

Retain workspace-setup as an optional, human-triggered convenience. Migrating a
central block requires identified scope and approval, preserves custom instructions,
and leaves no competing destination authority. No background synchronization,
new registry, or publication change is required. A single separately approved
startup instruction may request the factual `AGENTS.md: <applicable path(s)>` cue;
each skill must not insert its own copy. The cue is recognition, not compliance
proof or a promise of live cross-session reload.

### Two-layer operational lessons

The marked Durable Agent Lessons section keeps concise conditional pointers plus
constraints that must be visible before reference retrieval. It is not strictly
pointer-only if that would hide a critical permission or safety boundary. Do not
require reading every lesson or reference at startup.

Prefer existing canonical docs/KB runbooks. Where useful operational learning has
no suitable existing home, agent-lessons may maintain one explicitly designated
companion for that guidance scope. The approved first-use proposal is
`agent-lessons.md` beside the declaring AGENTS.md, or an explicitly selected
alternative. Initial location/ownership approval is required; neither a mandatory
file nor a silent fallback is introduced. Its link in the marked section records
the location without another registry.

Organize the companion by operational topic with useful applicability/version
qualifications. Keep API payloads, command sequences and troubleshooting detail
behind topic-specific pointers. Consolidate rather than append incident histories;
do not duplicate another skill's generic procedures or an existing canonical
runbook. Create no empty companion or fabricated lessons. Existing duplicate
instructions are a reason to consolidate, not add another reminder.

Explicit agent-lessons invocation permits proportionate maintenance of its marked
section and the designated companion, subject to local permission rules. It does
not acquire ownership of arbitrary linked docs, KB records, other guidance sections,
or executable tools; use their owning workflows. A companion inside an established
docs/KB surface also follows that surface's workflow. Verify supporting content
and pointers before shortening existing lessons; preserve essential guards and
report blocked routing rather than delete the only useful source.

The cost is another file and selective reads; pointers can be missed. Verify
behavior through fresh-session tool traces separately from static contract checks.
Harness enforcement would be separately scoped work, not another prose reminder.

## Current Skill Contract — Until Implementation

### Setup and routing

- Sync installs skills; explicitly invoked `workspace-setup` connects them to a workspace.
- Root `AGENTS.md` is the authoritative resource map. The former machine-local
  `~/.agent-core/projects.toml` workflow is retired; do not read, update, or recreate
  it. Existing files are left untouched, not used as a competing authority.
- Setup owns one marked block in AGENTS.md and preserves its existing position. It asks about ambiguity,
  obtains approval, preserves human wording, and returns exactly the saved block.
- Location-dependent skills ask when configuration is missing. They never create
  silent workspace/home-directory fallbacks.

### Standard Layout

```text
<workspace>/
  AGENTS.md
  .work-context/
    knowledge-base/
    archive/knowledge-base/YYYY-MM/
    projects/<project>/docs/
    projects/<project>/tasks/
    python/<purpose>/
```

The workspace is the folder the human opens in the coding agent, not necessarily
a repository. Code repositories may have any arrangement, and one project may
include several repositories. Unassigned repositories remain visible rather than
being falsely grouped. Python purpose projects are flat, named by workload, and
reusable across projects when compatible. The context home need not use Git.

These paths are setup conventions, not implicit runtime destinations. A previously
confirmed layout is preserved until an explicit approved change. Moving an old
`cf-workspace` or KB requires separate migration scope; never create a competing
empty KB merely to match the convention.

### Managed Agreement

`skills/workspace-setup/SKILL.md` owns the procedure and block shape; its
`references/defaults.md` owns creation-time skill-purpose and Behavior wording.

The block contains only:

- workspace/context/KB/archive/Python roots, check date and check scope;
- a project/docs/tasks table and a repository/project/description table
  (descriptions are human-editable annotations preserved on refresh);
- one `Skill / Status / Use for` table;
- a compact observed Python purpose inventory and any important gaps;
- one centralized Behavior section.

Paths are absolute or explicitly workspace-relative. Relative paths resolve against
the recorded workspace root, never the shell's current directory. The map's project
is selected from the requested work, not solely by current-directory containment.
Ask if project identity or scoped guidance conflicts. An explicitly selected
operation-specific destination does not silently rewrite the saved map.

Skill availability comes from exposed session metadata, not disk discovery or a
manifest. A last-check status is not proof of future availability, loading, or
compliance. Missing skills remain visible. Newly exposed skills can be added;
existing human-edited `Use for` and Behavior text must survive unchanged unless
that text's update is explicitly approved. Changing Agent Core defaults affects
new sections/rows, not existing custom instructions.

On refresh, keep a single `<!-- BEGIN MANAGED WORKSPACE -->` / `<!-- END MANAGED WORKSPACE -->`
block in its existing position, preserve outside text, and never relocate it
just to make it last.
Refuse ambiguous markers. Targeted changes require targeted discovery, not a fresh
whole-workspace scan. Read back and verify the saved file before returning exactly
its block, without a parallel summary. Report persistence failures honestly instead.

### Owning Workflows

| Workflow | Location and responsibility |
| --- | --- |
| project-docs | The project's mapped Docs surface; settled documentation and explicitly owned guidance |
| agent-lessons | Dedicated marked lessons section in the verified applicable AGENTS.md; only on explicit invocation |
| project-tasks | The project's mapped Tasks surface; continuation state and permission boundaries |
| knowledge-base | Explicit Knowledge Base Root; shared records, syntheses, and requested managed artifacts |
| knowledge-base inbox processing | Explicit Knowledge Base Archive; verify originals before removing inbox copies |
| manage-python-env | Explicit Python Environment Root; manage AND execute through compatible independent uv purpose projects |

Normal work does not rerun setup. The owning skill still controls authorization,
content, safety, and actual execution verification. Setup does not capture KB
records, write tasks, build environments, or change installed harness settings.

### Python and Recovery

`manage-python-env` supersedes `manage-python-agent-envs` and `manage-python-uv`.
Keep purpose manifests, locks, and Python pins as the reproducible recipe; exclude
`.venv`, caches, and secrets from Git. Run actual workloads through the selected uv
project and verify its interpreter. Separate environment selection from code cwd;
never modify team Python configuration just to run personal tooling.

The KB archive is outside the KB directory, may share its Git worktree, and is
excluded from ordinary recall. Configure `.work-context/archive/knowledge-base/`
during setup so inbox processing has a known destination. Capture, copy/verify,
record provenance, then remove only the unchanged retained inbox source. Archival
does not itself authorize Git publication of originals or restricted data.

Predictability is not backup. A Git checkout needs an approved commit/push or other
backup arrangement, and root AGENTS.md sits outside a context-only repository.
Setup may flag these gaps; it does not configure remote storage or migrate data.

## Publication Boundary

`agent-core sync` publishes the new skill through `personal-skills.toml`; it never
runs setup or edits workspace AGENTS.md. The named Python retirement runs only
when the replacement is selected, only for the selected harness's verified owned
predecessors. Modified, unowned, or unsafe obsolete copies block with exact paths;
they are not deleted. Pi alone also handles verified legacy `.agents` copies and
registered aliases. See [distribution](consumer-repo-enrollment.md).

## Related

- [Operating manual](agent-core-operating-manual.md)
- [Workspace setup](../skills/workspace-setup/SKILL.md)
- [Agent lessons](../skills/agent-lessons/SKILL.md)
- [Python environments](../skills/manage-python-env/SKILL.md)
- [Knowledge base](../skills/knowledge-base/SKILL.md)
