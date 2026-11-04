---
title: Workspace Configuration
description: Canonical skill-owned routing, task continuity, and coordinated handoff contract.
updated: 2026-11-04
---

# Workspace Configuration

## Read First

- Canonical skills implement lean, independently owned AGENTS.md routing and
  explicit coordinated task handoff/closeout. Publication and workspace adoption
  are separate; source edits do not update installed skills or external guidance.
- `project-docs`, `knowledge-base`, and `project-scripts` are independently
  usable resource skills. `project-tasks` coordinates task continuity and
  KB/docs/operational-lessons review for explicit handoff/closeout.
  `agent-lessons` coordinates bounded improvements to future agent behavior,
  using relevant owning skills without making those skills depend on it.
  Coordinators must respect owner permissions and avoid recursive invocation.
  There is no mandatory setup skill or new lessons registry.
- The [implementation task](../tasks/2026-10/2026-10-29__skill-owned-agents-sections.md)
  records delivery and actual verification. Static checks and saved instructions
  do not establish fresh-session harness compliance.

## Skill-Owned Guidance

### Guidance admission

AGENTS.md contains confirmed routing, selective entry points with when-to-read
cues, and essential before-action constraints. Detailed procedures stay in their
owning skills or selectively read references. No line quota replaces this judgment.
When applicable guidance and resources are available, agents can discover, read,
and use relevant docs, KB material, task context, and existing lessons without
invoking their maintenance skills. Reading does not authorize maintenance. Consult
only what the work needs; missing or inaccessible resources are gaps, not permission
to guess a replacement or initialize one. Applicable guidance is not necessarily
actually loaded by every harness.

| Owner | Standing guidance | Detail elsewhere |
| --- | --- | --- |
| project-tasks | Task roots and descriptive INDEX.md links; activation cue | Workstream navigation in INDEX.md; deliverables, state, gates, context map in tasks |
| project-docs | Docs roots and a few canonical entry points with consultation cues | Project meaning, architecture, rationale, rules, and deeper navigation in docs |
| knowledge-base | KB root, optional original-archive root, backend/knowledge-page configuration and selective retrieval cue | Records, syntheses, content indexes, approval-gated original preservation |
| manage-python-env | Python root beside its before-execution activation cue | Compatibility in manifests/pins/locks/runtime; execution procedure in skill |
| agent-lessons | Essential pre-action constraints and conditional reference pointers | Settled procedures in docs; reusable findings/evidence in KB |

The four resource owners define their creation-time shapes in skill-local
`references/routing.md`; agent-lessons defines its narrow section in SKILL.md.
Task/KB indexes stay local. Environment and skill inventories do not become
standing guidance. The knowledge-base skill maintains its own marked AGENTS.md
section during authorized KB maintenance (including safe adoption of clear
legacy unmarked routing); ordinary capture leaves source bytes untouched.
Approved original archival retains exact originals under the configured archive
root's `YYYY-MM/` month, without overwriting or deleting sources. The legacy
`inbox/` processing lifecycle is deprecated, with any existing files preserved. Python execution includes interpreter/import probes; reading
a path/source file is not execution. Selecting a repository script does not
authorize its repository-local environment.

### Ownership and maintenance

Each owner uses its own BEGIN/END marker pair: PROJECT TASKS, PROJECT DOCS,
KNOWLEDGE BASE, PYTHON ENVIRONMENTS, or AGENT LESSONS. Markers, headings, labels,
and minimal initial activation cues are defaults. Routine maintenance updates
confirmed paths and affected navigation, preserving customized behavior, outside
text, other sections, and position. Managed does not mean regenerate.

During a human-authorized docs or KB maintenance pass, an owner may minimally
refresh a missing or outdated discovery cue when that guidance is within the
authorized scope; an explicit cue-only refresh is also valid. Preserve customized
wording and stricter gates, ask about conflicts, and leave equivalent cues unchanged.
Reading, source edits, and publication alone do not authorize workspace changes.
Keep useful outputs reachable through existing indexes and links; add a guidance
pointer only for a missing durable entry point or trigger, not for every output.

Reread before mutation. Refuse ambiguous, duplicate, incomplete, or nested markers
and unsafe paths; reconcile concurrent edits safely, read back, and verify scoped
changes and links. General project-docs guidance ownership does not override
another skill's section. Partial routing/index failures are reported without
discarding valid primary work or claiming everything succeeded.

### Resource resolution and first use

1. Use established configuration, including operation-specific human-selected
   destinations without silently changing saved routing.
2. During authorized operational use, inspect/reuse a clearly identifiable
   compatible conventional resource and register missing configuration without
   redundant adoption approval. Read-only inspection authorizes no writes.
3. If neither configuration nor a suitable resource exists, propose the relevant
   conventional location and obtain one approval for initialization/registration.
4. Ask about ambiguity and report inaccessible configured resources rather than
   substituting another destination. Preserve narrower local permission gates.

Folder existence alone proves neither identity nor ownership. Python adoption
requires actual recipe/independence inspection. Initialize only the invoking
skill's resources. An original archive is optional for ordinary KB recall and capture. Explicit original archival requires the destination and approval of the proposed files and their paths; existing archives are never scanned as processing queues.
KB/Python need no project identity; preserve explicit cross-project task surfaces.

New section-relative paths resolve from the directory containing the declaring
AGENTS.md, including nested scopes, never cwd. Legacy workspace-relative mappings
retain their recorded base until approved migration. Preserve explicit layouts,
remote KB locators/backends, and optional external knowledge-page destinations.
Confirm workspace scope from the human/guidance, not a Git root or cwd alone.

Conventional proposals:

```text
<workspace>/
  AGENTS.md
  .work-context/
    projects/<project>/{docs,tasks}/
    knowledge-base/
    archive/knowledge-base/
    python/<purpose>/
```

Code organization is unconstrained. Several repositories may form one project.
Agent Core retains its explicitly owned `docs/` and `tasks/`; publishing skills
does not migrate this repository or employer workspaces.

## Task Continuity and Deliverables

The goal describes the intended outcome; deliverables identify reviewable outputs
or changes; acceptance establishes whether they satisfy the goal. A task can
deliver IaC, a validation report, or a PR. Small tasks can combine these fields.

New tasks use one shallow semantic workstream level:

```text
tasks/
  INDEX.md
  YYYY-MM/
    aws-migration/
      YYYY-MM-DD__validate-cutover.md
      YYYY-MM-DD__prepare-rollback.md
    dataset-evaluation/
      YYYY-MM-DD__agree-evaluation-criteria.md
```

Dates are creation dates. Reuse literal workstream names across months. Paths stay
stable through completion or deferral; existing tasks remain usable in place.
Use one task per coherent outcome and split independently continuable deliverables,
not conversations or ordinary steps. Shared effort overviews are created only when
they reduce meaningful duplication; no monthly indexes or taxonomy framework.

INDEX.md retains all known unfinished work under Now/Next/Later, with workstream
labels, status, and a meaningful next action or re-entry condition. Closed files
stay in place and leave the live index; reopening restores them. Report incomplete
initial inventory coverage. Routine progress does not rewrite AGENTS.md.

### Resume context

Task creation/resumption consults relevant docs and selectively recalls KB context
when prior findings matter. Tasks retain their supervisable goal, constraints,
current state, deliverables, and next permitted action. Their context map gives:

- exact paths/headings or usable remote locators;
- what each source supplies and when to read it;
- its role: approved design, observed evidence, procedure, or open investigation;
- confirmed code repository and specific prerequisite task outputs where relevant.

Read required sources before dependent work; conditional references wait until
relevant. An inaccessible essential source is a readiness gap. Task prose is not
proof of current code/runtime state; resolve material conflicts against the
appropriate authority. Natural-language continuation selects the project/index,
then reads the matching task; ask when materially different candidates remain.

## Coordinated Handoff and Closeout

In project-task context, requests such as "hand this off to a fresh session",
"prepare/delegate the next tasks to another agent", and "we're done; close this
task" authorize bounded KB capture, docs integration, task maintenance, and
operational-lessons review. The human need not name four skills or say "full".
Narrower requests and local write gates prevail. The cue does not spawn agents
or authorize implementation, commits, publication, or resource migration.

The [handoff workflow](../skills/project-tasks/references/handoff.md) governs:

1. Identify what must survive: decisions/rationale, evidence, deliverables, actual
   results, uncertainty, dependencies, permission boundaries, and useful lessons.
2. Load the owning skills and evaluate KB capture, docs integration, and lessons.
   Each may correctly make no change. Route each claim to its primary authority;
   reuse sources and findings rather than writing four overlapping summaries.
3. Persist and verify supporting material before adding pointers or shortening
   existing detail; save tasks/context/dependencies and affected index entries.
4. Read back and check that the next agent can identify what to produce, read,
   decide, and do without the old chat. This review is not a fresh-agent trial.
5. Report exact resumption paths, meaningful source changes/no-ops, material gaps,
   and the next action or closure result.

Routine progress updates and execution bookkeeping do not trigger this review.
Meaningful checkpoints preserve decisions before context is lost. Missing skills,
configuration, or access are reported; preserve valid task state and incomplete
closeout steps without inventing storage or claiming success. Required incomplete
work remains pending until completed or explicitly waived/cancelled.

## Operational Lessons

Explicit natural-language lessons requests and coordinated handoff/closeout cues
activate a bounded behavioral-improvement review. `agent-lessons` diagnoses
improvement opportunities, judges likely benefit and interference, and selects
only justified interventions: guidance, docs, KB, a genuine continuation task,
a concrete deterministic personal script/check, or no change. It delegates
resource maintenance to the relevant owning skill through a bounded request.
An owner may accept authorized delegated work without knowing the caller's
identity. Delegation does not override local write gates or create permission
to modify unrelated resources. A task handoff may still invoke lessons review;
the lessons review must not recursively start another handoff.

The marked lessons section keeps essential pre-action rules and conditional
pointers to specific headings. It never requires reading every reference at
session start. Maintain affected rules by consolidating, narrowing, or retiring
them when justified; consequential changes should consider possible unintended
behavior and use proportionate verification. No change is a valid outcome.

Detailed project procedures live in project docs; reusable findings and evidence
live in KB; personal deterministic utilities belong to Project Scripts. These
remain independently usable. No new `agent-lessons.md` companion or lessons
registry is needed. Preserve existing companion material until any authorized
migration saves its replacement. Save and verify supporting detail before
shortening guidance. Generic skill procedures stay in their owning skills;
fix missed activation cues at the owner instead of adding duplicate lessons.

## Optional Setup and Invocation

workspace-setup is an optional, request-triggered initializer/refresh coordinator.
It follows owner contracts, proposes only the requested scope, obtains approval,
preserves customization/position, and reports saved paths and gaps briefly.
It creates no skill catalogue or environment snapshot and does not run content
capture just to configure locations.

Migrating a legacy central block requires exact targets and approval. Preserve
human Behavior/Use for wording and repository annotations; translate relative
paths only from their known bases and leave no competing destination tables.
No content moves or external workspace migration are implicit.

One separately approved startup instruction outside owner sections may request
`AGENTS.md: <applicable path(s)>`. Owners preserve it rather than inserting copies.
It is recognition, not compliance proof or a promise of cross-session reload.

All canonical skills permit model invocation. Natural-language requests activate
request-only operations; availability does not broaden authorization. Supported
harness discovery/trigger settings and actual installed content still matter.
Publication uses the existing manual allowlists and selected-harness sync; it
does not run setup or change global guidance/settings.

## Related

- [Operating manual](agent-core-operating-manual.md)
- [Skill design guide](skill-design-guide.md)
- [Workspace scenarios](../tests/workspace-workflow-scenarios.md)
- [Distribution and migration](consumer-repo-enrollment.md)
