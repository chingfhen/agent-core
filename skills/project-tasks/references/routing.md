# Task routing and first use

Read when task configuration is missing, its routing must change, or an existing
managed section has an authorized cue refresh. This skill
owns only `<!-- BEGIN PROJECT TASKS -->` through `<!-- END PROJECT TASKS -->`
in the verified applicable AGENTS.md. A workspace is the human's working scope,
not necessarily cwd or a Git root. Ask if scope/project identity is ambiguous.

1. Use established configuration or the human's operation-specific destination;
   the latter does not silently change saved routing. Preserve explicit shared
   cross-project task surfaces without inventing a project.
2. During authorized task management, inspect/reuse an unambiguous existing
   conventional resource and register missing routing without a second adoption
   approval. Confirm identity/ownership from guidance and contents, not its name.
   Read-only inspection is not permission to register or initialize anything.
3. If no suitable resource exists, propose
   `.work-context/projects/<project>/tasks/` under the confirmed workspace and
   obtain one approval for initialization and registration. Established paths,
   including repository-owned `tasks/`, remain valid. Initialize only task resources.
4. Report inaccessible configured resources. Preserve narrower write gates and
   ask about conflicting ownership/destinations; never create a competing root.

## Section

Creation-time example only; substitute confirmed paths and a useful description:

```markdown
<!-- BEGIN PROJECT TASKS -->
## Project Tasks
When saved task context is relevant to the current work or a workstream reference,
consult the task index and matching tasks before planning or acting. Use targeted
search if needed; ask when materially different matches remain. If none match,
continue within the request and permissions. Reading or using task context does
not require loading project-tasks. Verify consequential claims against current
evidence and respect recorded permission boundaries.

Load project-tasks for task maintenance or execution of a saved task.

### Forecasting
Tasks: .work-context/projects/forecasting/tasks/
- [Task index](.work-context/projects/forecasting/tasks/INDEX.md)
  — unfinished forecast reconciliation and rollout work.
<!-- END PROJECT TASKS -->
```

New relative paths resolve from the directory containing the declaring AGENTS.md.
Legacy workspace-relative paths keep their recorded base until approved migration.
Keep unfinished-work navigation in INDEX.md and execution state in task files;
routine progress does not rewrite this section. Initialize index coverage honestly
under the main skill's rules; never advertise a nonexistent index as saved.

## Targeted maintenance

Markers/headings/labels and the initial activation cue are defaults. Maintain
confirmed locations and affected navigation; preserve customized behavioral text,
outside content, and block position. Do not copy skill procedures into guidance.
Do not edit another owner's section or regenerate the entire file.

When an existing section is explicitly authorized for a cue refresh, add or refine
its read-side guidance to make relevant index/task discovery independent of skill
invocation. Replace the old default cue requiring skill loading before "continuing"
saved tasks when it conflicts with that distinction; preserve genuinely customized
behavior and local write gates. A source or installed skill update does not by itself
rewrite existing workspace sections.

Reread immediately before writing. Refuse duplicate, incomplete, nested, or
ambiguous markers and unsafe paths; reconcile concurrent edits without clobbering
human work. Read back, check the owned diff and links, and report partial failure
without discarding valid task work. An existing central workspace block requires
identified scope and migration approval; do not leave competing location tables.
