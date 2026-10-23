---
name: workspace-setup
description: >
  Establish or refresh the workspace resource map and personal workflow in a
  managed section in root AGENTS.md. Use when the human asks to set up
  a workspace, refresh its configuration, or map a newly added repository or skill.
  Human-triggered maintenance, not an automatic every-session preflight.
disable-model-invocation: true
---

# Workspace Setup

Connect the human's existing skills to confirmed workspace resources. Maintain
one visible agreement, not another registry, dashboard, or master workflow.
Agent Core owns this skill and its creation-time defaults; the human owns each
workspace's choices and customized instructions.

## Contract

- The workspace is the root the human opens in the coding agent, not necessarily
  a Git root or the shell's current directory. Ask if that root is unclear.
- Own only the block between `<!-- BEGIN MANAGED WORKSPACE -->` and
  `<!-- END MANAGED WORKSPACE -->` in `<workspace>/AGENTS.md`. Keep exactly one
  block; preserve its existing position on refresh. Create the file if absent,
  after approval. Preserve all text outside the block.
- `AGENTS.md` is the location authority. Do not create or consume `projects.toml`,
  another registry, or a generated inventory file. Relative resource paths are
  relative to this workspace root, never the process working directory.
- Set up or refresh only on request. Show the proposed changes and obtain approval
  before writing; a request already approving the exact changes satisfies this.
- Never move existing content, initialize Git, stage, commit, push, install skills,
  change harness settings, or create Python environments as incidental setup.
  A content migration needs its own explicit scope and approval.
- Do not run docs/task/KB capture workflows merely to configure their locations.
  The owning skills still control their operations and permission boundaries.

## Standard home

Propose this arrangement on first setup; confirmed existing choices survive refresh:

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

Code repositories may be anywhere; a project can span several repositories.
Do not infer that each Git root is a separate project or that `others/` is one
project. Keep unrelated or unresolved repositories explicitly unassigned.
One shared KB serves this workspace. Python purpose projects are flat, reusable
across projects when compatible, and named by workload; no project nesting is
required. A prefix is useful only to disambiguate purposes.

The home can be a Git repository or an ordinary directory. Approved setup may
create the selected empty surface roots, but create no sample records, tasks,
Python environments, or archive month folders. The archive is outside the KB
and may share its Git worktree. Record both KB and archive roots explicitly.
Flag backup gaps during the proposal without configuring backup automatically.
Git alone is not backup; root AGENTS.md also needs the human's backup coverage.

## Discover only what is needed

1. Read existing root guidance, the managed block, and relevant scoped guidance.
   Preserve confirmed paths and human edits. Duplicate, incomplete, or conflicting
   markers are an ambiguity: ask rather than replacing an uncertain region.
2. Inspect the current session's exposed skill metadata. Availability means exposed
   to this session, not found on disk or merely named in a manifest. Use the initial
   personal baseline in [Defaults](references/defaults.md) plus existing rows and
   any newly exposed skills. Include extra exposed skills with purposes based on
   their descriptions; do not hide them or mislabel them as personal defaults.
   Mark expected but unexposed names `!`. Never search disk for substitute skill
   copies, load an unavailable skill by guessing its path, or claim it is installed
   or loaded. If the harness cannot expose availability, report `unknown` honestly.
   Reading a skill at its exposed path for a matching action remains normal use.
3. Inspect bounded directory metadata under the workspace or the exact new path
   supplied by the human. Recognize both `.git` files and directories; skip `.git`
   contents, `.venv`, node_modules, caches, build output, and symlink/junction
   traversal. Do not read every repository or KB. Report inaccessible branches.
   Places installation/cache is not required and must not be modified.
4. Confirm candidate project groupings and docs/tasks destinations from existing
   guidance and targeted inspection. Folder names alone do not establish ownership.
   For ambiguous KBs, repositories, or mappings, ask one focused question at a time.
   Never silently select a different KB because a new candidate appeared.
5. Inspect only purpose folders and their manifests/pins/lockfile/interpreter
   presence under the configured Python root. Do not execute or sync environments.
   Record names as an observed inventory, not compatibility or runtime verification.

For a targeted refresh, reuse previous mappings and check only the changed scope
plus current skill exposure. State the check scope beside the date; do not imply
that untouched resources were freshly verified. Do not remove missing repositories
or skill rows without confirmation. Missing/inaccessible resources are visible gaps,
not permission to invent replacement locations.

## Update without erasing customization

Read [Defaults](references/defaults.md) before creating the block or adding rows.
Use defaults only for newly created Behavior text and new skill rows. Preserve
existing `Use for` wording, repository `Description` annotations, and the entire
Behavior section on ordinary refresh, even when this skill's defaults have changed. Do not reconstruct custom wording
from remembered meaning. Update established behavior only on explicit request or
approval of that exact change. Preserve custom additions inside the block unless
they conflict with the requested change; ask about a material conflict.

Agent-maintained facts are confirmed paths, project/repository associations,
observed environment names, availability status, check date, and check scope.
Keep uncertainties in a short `Gaps:` line inside the block. Avoid long checklists,
logs, per-environment dependency inventories, or duplicate skills lists.

Use this compact shape, filling real values rather than leaving template tokens:

```markdown
<!-- BEGIN MANAGED WORKSPACE -->
## My Workspace
Checked: <date> · Scope: <initial setup / targeted change>
Workspace root: <absolute path>
Context home: .work-context/
Knowledge Base Root: .work-context/knowledge-base/
Knowledge Base Archive: .work-context/archive/knowledge-base/
Python Environment Root: .work-context/python/
Python purposes observed: <names, none, or not checked>

### Projects and repositories
All paths below are workspace-relative. Add new repositories as a row in the
repositories table under the correct project. Descriptions are human-editable
annotations; the agent maintains structure and paths.

| Project | Docs | Tasks |
| --- | --- | --- |
| <name> | <path> | <path> |

| Repository | Project | Description |
| --- | --- | --- |
| <path> | <project> | <short human-editable annotation> |

### Skills
✓ = exposed to the checking session; ! = expected but unavailable; ? = unknown.

| Skill | Status | Use for |
| --- | --- | --- |
| <name> | <status> | <default or preserved human wording> |

### Behavior
<initial defaults or preserved human text>
<!-- END MANAGED WORKSPACE -->
```

Missing destinations should be marked unresolved, not represented by fabricated
paths. Keep the Behavior heading last so all adjustable instructions stay together.

## Approve, persist, and return the evidence

1. Present the compact proposed block or a targeted diff and any consequential
   gaps. Ask for approval before writing if the exact change is not approved.
2. Re-read AGENTS.md before mutation. If it changed, merge against current content;
   seek renewed approval for material differences. Refuse unsafe file types or
   path redirection. Do not clobber concurrent human edits.
3. Write only the approved managed block, preserving its existing position and
   all outside text. Append a new block by default, without requiring it to
   remain last. Create only the explicitly approved directory roots.
4. Read back the file. Verify a single complete block, preserved outside
   text/custom instructions, and the actual approved paths and statuses.
5. Return exactly the saved managed block, including its markers, without an extra
   preamble, status report, or summary. Do not wrap it in another code fence.
   Verification and unresolved gaps belong in the block, not a second report.

A write or verification failure is an exception: report the failure and actual
partial state, never display proposed text as though it was saved. This block is
configuration and last-check evidence, not proof of future compliance. Owning
skills must verify their real execution, especially the Python interpreter.
