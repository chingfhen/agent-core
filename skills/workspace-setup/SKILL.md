---
name: workspace-setup
description: >
  On request, initialize or refresh lean skill-owned resource routing in applicable
  AGENTS.md. Use to set up a workspace, register changed resources, or migrate an
  existing central workspace block with approval. Optional convenience: individual
  workflow skills can establish their own resources. Not an every-session preflight.
disable-model-invocation: false
---

# Workspace Setup

Connect the human's skills to confirmed resources with lean, selective routing.
The human owns workspace choices and custom instructions; each workflow skill
owns its routing section and substantive operations. Setup coordinates an approved
initialization/refresh, without a central registry or mandatory setup dependency.

## Resolve the scope

1. Confirm the workspace the human opens, not necessarily cwd or a Git root.
   Read applicable AGENTS.md, established resource locations, and scoped guidance.
2. Inspect only the requested scope: existing guidance and bounded directory
   metadata or the exact new path. Recognize .git files/directories; skip caches,
   environment contents, build output, and symlink/junction traversal. Do not
   inventory the whole workspace for a targeted refresh.
3. Confirm project identity and ownership where docs/tasks need them. Several
   repositories may form one project; preserve shared cross-project task surfaces.
   KB and Python need no invented project. Existing repository navigation can
   remain ordinary guidance; no project/repository table is mandatory.
4. Determine skill availability from exposed session metadata, not disk presence
   or a manifest. Load only the available owning skills needed for the requested
   setup and follow their section contracts. Report unavailable owners; do not
   guess substitute copies or claim their setup was performed.

For missing resources, propose the relevant part of this convention:

```text
<workspace>/
  AGENTS.md
  .work-context/
    projects/<project>/{docs,tasks}/
    knowledge-base/
    archive/knowledge-base/
    python/<purpose>/
```

These are proposals, not fallback paths. Reuse established resources; confirm
identity/ownership from more than folder names. Missing or inaccessible configured
resources are gaps, not permission to create competing roots. Ask about material
ambiguity. An archive is needed for inbox processing, not ordinary KB retrieval.
Python compatibility comes from recipes and runtime, not a setup inventory.

## Propose only useful routing

Read [Defaults](references/defaults.md) for the admission rule and optional startup
cue. Each owner supplies its own minimal creation-time section:

- project-tasks: task roots and descriptive INDEX.md links;
- project-docs: docs roots and a few existing canonical entry points with cues;
- knowledge-base: KB/archive and any established backend/knowledge-page routing;
- manage-python-env: Python root beside its before-execution activation cue;
- agent-lessons: existing essential rules and conditional pointers; no seeded lessons.

Keep procedures, live task lists, environment inventories, skill catalogues, and
last-check dashboards out of newly created routing. Preserve customized wording
rather than resetting it to current defaults. Setup establishes locations; it does
not run capture, docs integration, task authoring, lessons review, or Python execution.

Present the targeted proposal and consequential gaps, then obtain approval before
writing. A request approving the exact changes satisfies this gate. Approved setup
may create selected resource roots and AGENTS.md, but no sample content, empty
lessons sections, purpose environments, or archive month folders. If an index or
entry point needs initialization, use its owning workflow with the required approval;
do not add a link to a nonexistent file as though setup succeeded.

## Migrate a legacy central block only with approval

Recognize `<!-- BEGIN MANAGED WORKSPACE -->` / `<!-- END MANAGED WORKSPACE -->`.
Ordinary targeted refresh preserves that block's position, human-edited `Use for`
and `Behavior` wording, repository descriptions, and outside text. Do not rebuild
it from new defaults or silently convert its workspace-relative path base.

For an explicitly requested migration, identify exact targets and propose moving
confirmed routing into owner sections. Preserve custom instructions and repository
annotations as ordinary guidance at the existing location unless another position
is approved. Translate relative paths only with their recorded bases established.
Remove superseded destination rows in the same approved change so no competing
authorities remain. Resolve conflicts before writing; approval here does not
authorize moving resource contents or migrating another workspace.

## Persist and verify

1. Reread AGENTS.md before mutation. Refuse duplicate, incomplete, nested, or
   ambiguous markers and unsafe paths. Reconcile concurrent edits; obtain renewed
   approval only for material changes to the proposal.
2. Change only approved sections, preserving their position and all other content.
   Do not override an owner's rules or narrower local write permissions. New
   section-relative paths resolve from the declaring AGENTS.md directory, not cwd.
3. Read back and verify complete marker pairs, preserved custom/outside content,
   actual paths and links, and no competing destination tables. Preserve valid
   primary work on partial failure and report exactly what remains incomplete.
4. Return a short receipt with exact guidance/resource paths, changed routing, and
   material gaps. The saved file is authoritative; do not echo a second whole map.

Never initialize Git, stage, commit, push, install skills, modify harness settings,
or configure backup incidentally. Publication and resource-content migration are
separate operations. Saved routing and a startup path cue do not prove harness
loading, compliance, interpreter health, or automatic cross-session reload.
