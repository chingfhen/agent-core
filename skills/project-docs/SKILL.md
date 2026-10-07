---
name: project-docs
description: Maintains settled project understanding in the active project's configured documentation surface, or the workspace docs/ fallback when the project is not registered, and stable agent behavior in explicitly owned project guidance. Load before creating, editing, moving, deleting, or managing those surfaces; not needed merely to read explicitly identified files. Routes each durable claim to its canonical authority, integrates useful meaning into existing docs, rewrites stale material toward current understanding, and allows a docs sync to conclude that no change is needed.
disable-model-invocation: false
---

# Project Docs

## Purpose

Maintain the project understanding and operating guidance that future participants should inherit after the current task and conversation disappear.

Docs may own intended architecture, product meaning, exclusions, rationale, ownership boundaries, invariants, and constraints that code does not express. They are not merely prose summaries of code.

A request to `sync to docs` means:

> Evaluate the current work for settled project understanding and durable operating behavior, then integrate what matters into the configured owned documentation surfaces.

A sync may correctly produce no changes. Do not create or modify a document merely to demonstrate activity.

Documentation is not active task state, a transcript, raw evidence, status history, a backlog, or a record of everything that happened. Preserve settled meaning and behavior whose absence would cause worse decisions, repeated investigation, recurring mistakes, or loss of important project intent.

## Surface Ownership

This skill writes only to the documentation surface resolved for the active project—configured when available, otherwise the workspace-root `docs/` fallback—and to project-guidance files explicitly assigned to this workflow.

Machine-local registry:

```text
~/.agent-core/projects.toml
```

Example:

```toml
[projects.smart-search]
description = "OCBC Smart Search"
root = "/home/cdsw/smart-search-workspace"
docs = "/home/cdsw/smart-search-workspace/docs"
tasks = "/home/cdsw/smart-search-workspace/tasks"
knowledge_base = "/home/cdsw/smart-search-workspace/knowledge-base"
```

For this skill, `root` and `docs` are the relevant fields.

Before creating, editing, moving, deleting, or otherwise managing project documentation:

1. Read `~/.agent-core/projects.toml` when it exists.
2. Identify the project whose configured `root` contains the current working directory. If several match, use the most specific root.
3. When a matching project has a `docs` value, treat that exact value as the default writable documentation-surface root.
4. When the registry does not exist or has no matching project with a `docs` value, use (and create as needed) `docs/` directly under the active workspace root. Do not search for another nearby docs directory or substitute a containing Git root.
5. After using the workspace fallback, tell the human that no configured documentation surface was available and report the exact fallback path.
6. Perform documentation CRUD only inside the resolved configured or fallback surface unless the human, project configuration, or established project guidance explicitly assigns another project-guidance file to this workflow.
7. If the registry exists but cannot be read or parsed, report the error instead of silently falling back.
8. Read the registry for normal documentation work, but modify it only when the human explicitly asks to register, remove, or change a project.
9. After a mutation, report every exact resolved filesystem path changed.

Paths such as `docs/architecture.md` are logical paths. If the configured surface is `/home/cdsw/smart-search-workspace/docs`, then logical `docs/architecture.md` resolves to `/home/cdsw/smart-search-workspace/docs/architecture.md`. The surface may be inside or outside a Git repository; matching registry configuration remains authoritative when available.

### README and Agent Guidance

`README`, `AGENTS.md`, `CLAUDE.md`, and similar guidance files are not owned merely because they are visible in a nearby or nested repository.

Edit one only when:

- it is inside the configured docs surface and serves that role there;
- the human explicitly identifies it as an owned target for the operation; or
- project configuration or established project guidance assigns it to this documentation workflow.

Do not silently edit guidance in a nested or shared repository. Other project surfaces may be read as context, but this skill does not silently mutate them.

## What Each Surface Owns

- **Project docs:** settled architecture, product semantics, interfaces, workflows, invariants, durable decisions, rationale, exclusions, ownership boundaries, and non-obvious constraints.
- **Explicitly owned README:** orientation, entry points, setup, usage, navigation, and onboarding.
- **Explicitly owned agent guidance:** concise stable behavior that should shape an agent before it acts.
- **Code, tests, schemas, configuration, and runtime evidence:** machine-defined or observed claims within their respective scopes.
- **Active tasks:** current progress, open investigation, remaining work, uncertainty, and fresh-session continuation.
- **Backlog:** deferred work, not current project truth.
- **Source or evidence surfaces:** supporting material that may ground a conclusion but is not automatically canonical project meaning.
- **Archive:** historical or superseded material that should not drive current work by default.
- **Knowledge base:** retained evidence and synthesized understanding under its own workflow; a docs sync does not automatically capture or curate KB content.

One durable claim should have one primary authority. Other surfaces may link to it or state a concise consequence when needed rather than maintain competing full explanations.

## Admission and Routing

Before writing, determine whether the work produced settled project understanding, stable operating behavior, or neither.

### Project Understanding

Preserve understanding when it is likely to remain useful and materially affects how the project should be interpreted, changed, operated, or evaluated. Strong candidates include:

- intended architecture and component ownership;
- product meaning and deliberate exclusions;
- durable decisions and rationale not recoverable from implementation alone;
- important interfaces, workflows, and invariants;
- constraints or failure behavior that affect future changes;
- confirmed fixes or lessons that would otherwise cause recurring mistakes;
- external contracts whose consequences the project must preserve.

Expensive rediscovery is a useful test, but it is not the only admission rule. Preserve settled project meaning even when code cannot express it.

Do not promote open-ended ideation, unresolved alternatives, temporary workarounds, one-off status, or tentative conclusions as established truth.

### Durable Behavior

Use agent guidance when a stable instruction should shape action before a future agent would normally read deeper documentation and omission would create material risk, recurring error, inconsistency, or wasted work.

Keep the guidance concise. Put explanatory truth and rationale in canonical docs and link to it when useful. Prefer executable enforcement through tests, CI, schemas, hooks, or tooling when behavior can be enforced reliably; do not expand a docs sync into implementation merely to add enforcement.

### Routing Table

| Destination | Put here |
| --- | --- |
| Configured docs surface | Project understanding, intended behavior, architecture, rationale, constraints, interfaces, workflows, durable decisions |
| Explicitly owned README | Orientation, setup, usage, navigation, onboarding |
| Explicitly owned agent guidance | Stable behavior needed before action |
| Active task workflow | Progress, open questions, pending decisions, next actions, validation still required |
| Backlog workflow | Deferred future work |
| Source/evidence workflow | Logs, imported notes, experiments, external references, supporting records |
| Archive | Superseded or historical material retained for reference |
| Executable authority | Machine-defined values, schemas, enforced behavior, current implementation |

Follow the owning workflow for any destination outside this skill. Do not create alternate docs, task, source, archive, guidance, or KB structures merely to complete a sync.

## Autonomous Integration Within Ownership

When the destination and authority are clear, choose and update the appropriate existing owned document without asking the human which file or heading to use. Prefer improving a current canonical page over creating another one.

Ask only when a material product, architecture, ownership, security, privacy, or other durable decision remains unresolved, when authorities conflict in a way evidence cannot settle, or when the operation would exceed configured ownership. Routine wording, headings, placement, and link repair are executor-owned.

Autonomy does not expand write scope. A request to sync docs authorizes evaluation and integration only within the owned surfaces and current request.

If nothing settled or durable needs preservation, report that the sync produced no documentation change. Do not manufacture a page, decision, or rule.

## Canonical Authority and Conflicts

Documentation is not automatically stronger than every other source. Identify authority by claim:

| Claim | Usually strongest authority |
| --- | --- |
| Current implementation | Code; direct runtime verification when relevant |
| Expected or tested behavior | Tests and explicit contracts |
| Accepted structures or values | Schemas, types, parsers |
| Deployed or environment state | Deployment/configuration plus runtime evidence |
| Intended architecture or design constraint | Canonical design docs or ADRs |
| Product semantics or deliberate project decision | Canonical project docs |
| Stable agent operating behavior | Canonical agent guidance |
| External protocol, vendor, or regulatory requirement | The authoritative external source, with project consequences documented locally |

This is a reasoning aid, not a rigid global precedence order.

When sources conflict:

1. determine the claim type and intended authority;
2. inspect enough evidence to distinguish stale prose, an implementation bug, environment drift, an obsolete decision, or unresolved intent;
3. update only the authority or summary that is actually stale;
4. do not rewrite intended design to normalize an implementation bug;
5. do not preserve stale prose when executable authority clearly controls the claim;
6. keep unresolved work in the task or investigation surface. Mark `Needs validation` in canonical docs only when the uncertainty itself is durable and readers would otherwise be misled.

A local copy of an external source can still be authoritative for the external claim it records; local storage alone does not make it canonical project authority.

Use this distillation path:

```text
evidence -> understanding -> settled conclusion -> canonical authority
```

Persist conclusions and useful rationale, not raw investigation history. Preserve evidence separately when future decisions may need to reassess it.

## Writing and Maintenance

- Prefer rewriting stale sections over appending updates.
- Preserve current understanding rather than session chronology.
- Improve an existing canonical surface before creating a new page.
- Give each document one coherent durable scope.
- Keep the first screen short and useful.
- Put conclusions and invariants before supporting detail.
- Keep README material orientation-focused and agent guidance behavior-focused.
- Link to canonical detail instead of duplicating it.
- Use stable implementation references when they reduce rediscovery without making prose brittle.
- Do not copy task summaries into docs.
- Do not write uncertainty as established fact.
- Do not let source material, backlog notes, or archive content silently become current truth.
- Do not include secrets, passwords, tokens, private keys, live credentials, or sensitive source content that does not belong in project documentation.
- Do not turn a routine sync into an audit of unrelated areas.

When a canonical document is renamed, moved, split, merged, or materially rescoped, update directly affected indexes and links in the same change.

### Markdown Conventions

Follow the established convention inside the resolved documentation surface when one exists.

Otherwise, canonical Markdown docs created or materially maintained by this skill use:

```markdown
---
title: [Doc Title]
description: [One sentence defining the document's canonical knowledge boundary.]
updated: YYYY-MM-DD
---
```

Change `updated` only when durable meaning changes.

Use this shape when it helps:

```markdown
# [Doc Title]

## Read First

- Current fact, decision, or invariant.

## Scope

What belongs here.

## Not Here

What belongs elsewhere.

## Current Contract

Stable behavior, interfaces, workflows, schemas, commands, or rules.

## Related Surfaces

| Surface | Path / System | Why It Matters |
| --- | --- | --- |

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
```

Small documents should omit sections that do not help. Use a compact diagram only when it clarifies structure better than prose.

## Sync Workflow

Use this workflow when durable understanding or behavior changes, or when the human asks to update or sync docs or project knowledge.

1. **Resolve ownership.** Identify the configured docs surface and any explicitly owned README or guidance target. Inspect relevant existing docs, task context, and authority surfaces.
2. **Evaluate admission.** Determine what settled project understanding or durable behavior should survive. It is valid to select nothing.
3. **Resolve authority.** Investigate material conflicts rather than silently choosing the most convenient source.
4. **Route.** Put explanatory project meaning in docs or an owned README, concise stable behavior in owned guidance, current state in tasks, evidence in its source workflow, and machine-defined claims in executable authorities.
5. **Integrate.** Choose the appropriate existing canonical document autonomously when clear. Rewrite affected sections and create a new page only when it deserves an independent durable scope.
6. **Repair.** Update directly affected indexes and links without expanding into an unrelated audit.
7. **Verify and report.** Check the changed surfaces and affected links proportionately. Report material changes, rerouting, unresolved uncertainty, or a valid no-op, plus every exact resolved path mutated.

Self-initiate a docs update only when the result is settled, material, directly related to current work, and consistent with repository guidance and owning workflows.

A sync is complete when durable meaning is clear in its canonical home, transient state was excluded, authority conflicts were resolved or honestly preserved, and no stale directly affected guidance competes with the result.

## Scoped Audit or Cleanup

Use a broader `verify`, `trim`, migration, or documentation health pass only when explicitly requested.

Within the requested scope:

- compare docs, owned README/guidance, executable authorities, tasks, and supporting evidence as relevant;
- find stale claims, broken assumptions, duplicate authority, obsolete guidance, broken links, and orphan pages;
- choose one canonical authority for each durable claim;
- replace duplication with pointers or concise behavioral consequences;
- remove historical residue after preserving any lesson that still matters;
- check conventions, frontmatter, indexes, and links;
- preserve useful current understanding while reducing maintenance burden;
- mark durable unresolved uncertainty as `Needs validation`.

Do not broaden a routine sync into this audit without authorization.

## Final Test

A good documentation update leaves future participants with the settled project meaning and stable behavior they need, in the owned canonical surfaces, without copying active task state or manufacturing documentation. The result identifies the right authority for each claim, replaces stale material, preserves intended design when implementation is wrong, and reports either the exact changed paths or an honest no-change outcome.
