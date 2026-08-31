---
name: project-docs
description: Maintains durable project knowledge in docs/ and README, plus durable agent behavior in repository guidance such as AGENTS.md. Load before creating or editing those surfaces; not needed merely to read them. Distills settled, high-leverage knowledge, routes each claim to its canonical authority, rewrites stale material toward simpler current understanding, and avoids documentation bloat.
disable-model-invocation: false
---

# Project Docs

Maintain durable project knowledge and agent behavior for future sessions.

Documentation is not task state, source material, transcripts, status history, or a record of everything that happened. Preserve only settled, high-leverage knowledge and behavior that future agents should not have to rediscover or relearn.

Follow the repository's existing structure and conventions. Paths in this skill describe common roles, not folders that must exist.

## Core Model

* **`project-docs` governs the maintenance and routing of durable project knowledge and behavioral guidance.**
* **Docs answer:** What should future agents understand about the project?
* **README answers:** How should someone orient themselves to the repository?
* **Agent guidance answers:** How should future agents operate?
* **Executable surfaces may be the canonical authority** for machine-defined facts or reliably enforced behavior.
* **Active tasks own execution state** and fresh-session handoff.
* **Backlog/task systems own deferred work** that is not current project truth.
* **Source-material areas hold evidence and external inputs**; their presence in the repository does not make them canonical project authority.
* **Archive material holds history**, not current truth.
* A document should have **one coherent durable scope** and answer that scope well.
* Each durable claim should have **one canonical authority**.
* Prefer replacing stale material over appending updates.
* Preserve current understanding over historical narrative.
* Ask only when a durable choice is materially ambiguous, conflicts with authority, or changes architecture, product direction, or stable operating behavior.

### Guiding Question

> If this task disappeared tomorrow, what knowledge would future agents repeatedly pay to rediscover, or what behavior should they consistently preserve before acting?

Preserve that. Use version control for history.

## Admission And Routing

Before persisting anything, decide whether it is durable **knowledge**, durable **behavior**, or neither.

### Knowledge

Ask:

> Would future agents pay meaningful cost to rediscover or reconstruct this?

Strong candidates are:

* **Durable:** likely to remain true beyond the current task.
* **Expensive to rediscover:** forgetting it would cause repeated investigation, uncertainty, or reconstruction cost.
* **Consequential:** it materially affects implementation, decisions, operations, product understanding, or future consistency.

### Behavior

Ask:

> Would future agents materially benefit from inheriting this before they act?

Promote behavior when it is stable across tasks and omission would likely cause recurring mistakes, inconsistency, risk, or meaningful wasted work.

Do not turn one-off mistakes, temporary workarounds, or tentative lessons into permanent guidance.

### Common Destinations

| Surface | Purpose |
| --- | --- |
| `docs/` or repository equivalent | Architecture, interfaces, workflows, product/runtime behavior, durable decisions, invariants, non-obvious constraints |
| README | Overview, entry points, setup, usage, navigation, onboarding |
| `AGENTS.md`, `CLAUDE.md`, or repo-defined equivalent | Stable operating rules, validation steps, coding philosophy, recurring mistakes worth preventing |
| Active task system | Current progress, open investigation, work remaining, session handoff |
| Backlog system | Deferred future work that should survive without becoming current truth |
| Source-material area | Supporting evidence, logs, imported notes, experiments, external references, one-off artifacts |
| Archive area | Superseded or historical material retained for reference |

If another skill or repository workflow owns a destination such as `tasks/`, follow that workflow rather than bypassing it.

Do not create `docs/`, `tasks/`, `source-material/`, `archive/`, or new agent-guidance files merely to satisfy this skill. Create new surfaces only when justified by repository convention and the knowledge being preserved.

### Routing Example

During a task, the agent learns that:

* queue retries must remain idempotent;
* direct queue publishing bypasses required safeguards;
* the architectural reason is expensive to rediscover;
* several failed approaches are still part of the active investigation.

Route the result as:

```text
docs/queue.md
→ Explain the queue boundary, idempotency invariant, and durable rationale.

AGENTS.md
→ "When modifying queue publishing, use QueueService and preserve retry idempotency."

active task
→ Keep failed approaches, open questions, and current investigation state.

code/tests/schema
→ Remain authoritative for mechanically defined behavior where applicable.
```

The agent guidance contains only the behavioral consequence future agents need before acting; detailed truth stays in the canonical project documentation.

## Canonical Authority And Conflicts

Documentation is not automatically the strongest source of truth.

Use the claim type to identify the strongest authority:

| Claim | Usually strongest authority |
| --- | --- |
| Current implementation | Code; direct runtime verification when relevant |
| Expected or tested behavior | Tests and explicit contracts |
| Accepted structure or values | Schemas, types, parsers |
| Deployed/environment state | Deployment/configuration plus runtime evidence |
| Intended architecture or design constraint | Canonical design docs / ADRs |
| Product semantics or deliberate project decision | Canonical project docs |
| Stable agent operating behavior | Canonical agent guidance |

This is a reasoning aid, not a rigid precedence hierarchy.

When sources conflict:

* Determine whether the conflict is stale prose, an implementation bug, environment drift, or unresolved intent.
* Verify before changing canonical surfaces.
* Do not rewrite intended architecture merely to match an obvious bug.
* Do not preserve stale prose when machine-defined reality clearly controls the claim.
* Preserve unresolved uncertainty in the active task or appropriate investigation surface. Mark `Needs validation` in canonical documentation only when the uncertainty itself is durable and readers would otherwise be misled.

A source stored locally may still represent an authoritative external source for the external claim it defines, such as an upstream protocol, vendor contract, or regulatory requirement. Its local presence alone does not make it canonical project authority.

Other surfaces may summarize or point to a canonical claim. Agent guidance may state a concise behavioral consequence **only when the agent needs that instruction before it would normally open the canonical doc, and omission creates material risk, recurring error, or meaningful wasted work**. Otherwise prefer a pointer.

When durable behavior is already reliably enforced by tests, CI, schemas, hooks, or tooling, treat that mechanism as the stronger enforcement surface. Use agent guidance when behavior must shape action before enforcement or cannot be adequately enforced. Do not expand a documentation update into implementation work merely to add enforcement.

## Evidence Distillation

Use this flow:

`Evidence -> Understanding -> Durable conclusion -> Canonical authority / destination`

Persist conclusions, not raw investigation history.

Treat tasks, discussions, logs, experiments, and source material as inputs rather than automatic authority. Preserve evidence separately only when future decisions may need to re-evaluate it.

## Writing And Maintenance

* Prefer rewriting over appending.
* Replace obsolete explanations and instructions.
* Collapse duplication and remove historical residue after its lessons are absorbed.
* Improve existing surfaces before creating new ones.
* Keep agent guidance concise and behavior-focused.
* Keep README concise and orientation-focused.
* Keep the first screen of canonical docs short and scannable.
* Use links or stable implementation references where they reduce rediscovery.
* Do not copy task summaries into docs.
* Do not write uncertain claims as established fact.
* Do not let source material, archive material, or backlog notes silently become current truth.
* Do not expand a normal update into an audit of unrelated areas.

When a canonical document is renamed, moved, split, merged, or materially rescoped, update directly affected indexes and links in the same change.

### Markdown Conventions

Follow an established repository documentation convention when one exists.

Otherwise, canonical Markdown docs created or materially maintained by this skill use:

```markdown
---
title: [Doc Title]
description: [One sentence defining the document's canonical knowledge boundary.]
updated: YYYY-MM-DD
---
```

Change `updated` only when durable meaning changes.

Use this default shape where relevant:

```markdown
# [Doc Title]

## Read First

- Current fact or invariant.
- Current fact or invariant.

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

Small docs may omit sections that do not help their coherent scope. Tiny ASCII diagrams are useful only when they compress structure.

## Update / Sync

Use when durable project knowledge or behavior changes, or when the user asks to update/sync docs or project knowledge.

An explicit request such as `update docs` means: **evaluate the current work for durable knowledge and behavior now**. It does not mean copy everything discussed.

1. **Inspect** the relevant docs, guidance, task context, and authority surfaces.
2. **Distill** only settled, durable knowledge or behavior; investigate material authority conflicts rather than silently choosing.
3. **Route** explanatory project knowledge to docs/README, durable behavior to agent guidance, and machine-defined facts to their executable authority; respect other skills and repository workflows.
4. **Rewrite** all directly affected canonical surfaces and repair affected indexes/links, without expanding into an audit of unrelated areas.
5. **Report** only material changes, rerouting, or unresolved uncertainty.

Self-initiate persistence only when the update is **settled, material, directly related to the current work, and not contrary to repository guidance or another owning workflow**.

Do not autonomously promote open-ended ideation, unresolved alternatives, speculative conclusions, temporary workarounds, or one-off lessons.

Done when current durable knowledge and behavior are clear, transient state was left out, conflicting authority is resolved or preserved as explicit uncertainty, and no stale guidance competes with current understanding.

## Verify / Trim

Use for an explicitly requested documentation/guidance audit, migration, or scoped cleanup.

* Compare relevant docs, README, agent guidance, implementation authority, tasks, and supporting context.
* Identify stale claims, broken assumptions, duplicate authority, and obsolete guidance.
* Choose one canonical authority per durable claim.
* Replace unnecessary duplication with pointers or concise behavioral guidance where justified.
* Remove stale implementation chatter and historical residue from current surfaces.
* Check repository conventions, frontmatter, indexes, links, and orphan docs within the requested scope.
* Preserve useful current understanding while reducing maintenance burden.
* Mark durable unresolved uncertainty as `Needs validation`.
