---
title: Workspace Configuration
description: Canonical resource-routing and managed-guidance contract for personal workspaces.
updated: 2026-10-23
---

# Workspace Configuration

## Read First

- Sync installs skills; explicitly invoked `workspace-setup` connects them to a workspace.
- Root `AGENTS.md` is the authoritative resource map. The former machine-local
  `~/.agent-core/projects.toml` workflow is retired; do not read, update, or recreate
  it. Existing files are left untouched, not used as a competing authority.
- Setup owns one marked block in AGENTS.md and preserves its existing position. It asks about ambiguity,
  obtains approval, preserves human wording, and returns exactly the saved block.
- Location-dependent skills ask when configuration is missing. They never create
  silent workspace/home-directory fallbacks.

## Standard Layout

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

## Managed Agreement

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

## Owning Workflows

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

## Python and Recovery

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
