---
name: project-docs
description: Maintain durable project truth and agent behavior when asked to update or sync docs, absorb stable learnings, trim stale documentation, route knowledge across docs, README, agent guidance, source-material, archive, or tasks, or resume a repo contract.
---

# Project Docs

Maintain durable behavior and truth for long-term repo consistency.

Docs are not just documentation. They are long-term control surfaces for future agent behavior: current repo truth, operating rules, workflows, invariants, decisions, and guidance that should keep future sessions correct, smooth, and consistent after the current task disappears.

`project-docs` is general repo maintenance. It is not coding-specific.

## Core Model

- **`project-docs` owns durable behavior and truth.**
- **`project-tasks` owns active execution state** for smooth delivery of short-lived work.
- **`source-material/` holds evidence and supporting artifacts**, not authority.
- **`archive/` holds superseded historical material**, not current truth.
- Docs should reduce rediscovery, prevent drift, and keep future agents acting from the same durable contract.
- Each durable fact should have one canonical home.
- Prefer rewriting current truth over appending historical layers.
- Ask only when a durable choice is materially ambiguous, conflicts with current truth, or changes architecture, product direction, or stable operating behavior.

## Guiding Question

Ask:

> After the current task disappears, what should future agents consistently know or do?

Preserve that. Everything else is negotiable. Use version control for history; use docs for current understanding and durable behavior.

## Lifecycle

### Route

Use when deciding where knowledge belongs.

1. Inspect repository-local surfaces before writing: `docs/`, README, agent guidance files, existing documentation indexes, relevant code, `tasks/`, `source-material/`, and `archive/` when historical context matters.
2. Decide whether the material is durable truth, active execution state, supporting evidence, onboarding orientation, agent behavior guidance, or historical reference.
3. Choose the narrowest existing canonical home that fits.
4. Improve an existing surface before creating a new one.

Done when each piece of knowledge has one appropriate home, duplication is avoided, and unresolved uncertainty is marked `Needs validation` instead of written as fact.

### Update / Sync

Use when durable truth or durable agent behavior should be added, changed, extracted, refreshed, or synchronized from tasks, conversations, code changes, debugging, investigations, design discussions, completed work, or existing docs.

1. Treat tasks, discussions, code changes, and evidence as inputs, not authority.
2. Read the target document and nearby related docs.
3. Check likely overlap or conflict before editing.
4. Apply the Documentation Admission Test.
5. Distill evidence into conclusions and decisions.
6. Promote only durable truth or durable behavior.
7. Rewrite the canonical surface around current truth instead of appending a new layer.
8. Leave transient execution state in `tasks/`.
9. Route supporting evidence to `source-material/` or superseded historical reference to `archive/` only when useful.
10. Update metadata, timestamps, decisions, or related pointers only when they improve future use.

Done when the canonical surface reflects current durable truth, transient state was left out, stale guidance no longer competes with it, and every promoted fact has one appropriate home.

### Verify / Trim

Use when docs may be stale, duplicated, bloated, contradictory, or misleading.

1. Compare docs, README, agent guidance, code, tasks, and relevant source or archive material.
2. Identify stale paths, commands, workflows, assumptions, and duplicated claims.
3. Keep durable decisions, constraints, current behavior, and useful orientation.
4. Remove obsolete implementation chatter, historical residue, and stale agent guidance.
5. Replace duplication with one canonical home plus pointers only where useful.

Done when stale or duplicated guidance no longer misleads future agents and the remaining docs are simpler, current, and easier to act from.

### Resume

Use when the user asks where a topic stands or what the current durable contract is.

1. Read the most relevant docs and context.
2. State the current source of truth.
3. Summarize the durable contract.
4. Highlight important constraints and known uncertainty.
5. Identify related active work only when useful.

Done when the user has a concise answer about current truth, not a history dump.

## Documentation Admission Test

Before persisting knowledge, ask:

1. Would future agents likely need this after the current task disappears?
2. If forgotten, would future sessions repeatedly rediscover it at meaningful cost?
3. Does it change how the system works, how agents should behave, or how future decisions should be made?
4. Is it stable enough to be durable truth rather than active execution state?
5. Is version control already the better memory?

If the answer does not justify durable preservation, do not document it. Interesting is not enough. Useful during the current task is not enough.

## Routing Contract

| Surface | Owns | Use For |
| ------- | ---- | ------- |
| `docs/` | Durable project truth | Architecture, workflows, runtime behavior, product behavior, technical decisions, operational invariants, troubleshooting worth inheriting. |
| README | Repository orientation | Overview, entry points, setup, usage, high-level architecture, navigation, onboarding essentials. |
| Agent guidance files | Durable agent behavior | Repo-wide operating rules, workflow rules, coding philosophy, high-frequency conventions, recurring mistakes worth preventing. |
| `tasks/` | Active execution state | Current progress, short-lived delivery state, handoff, blockers, investigations still in flight. |
| `source-material/` | Supporting artifacts | External references, seed specs, imported notes, logs, captured evidence, experiment output. |
| `archive/` | Historical reference | Superseded specs, retired designs, frozen snapshots, old material that should not guide current truth by default. |

Do not let `source-material/` or `archive/` silently become canonical documentation. Reuse them as context, validate them, then promote only current conclusions when appropriate.

## Evidence Distillation

Use this path:

```text
Evidence -> Understanding -> Decision -> Documentation
```

Persist the conclusion future agents should act on, not everything that happened. Preserve evidence only when future decisions depend on re-evaluating it.

## Preferred Doc Shape

Use this shape when it helps. Small docs may omit optional sections.

```markdown
# [Doc Title]

**Last Updated:** YYYY-MM-DD

**Status:** Current | Draft | Stale | Deprecated

**Source Of Truth:** [One durable question this doc answers.]

**Update When:** [Concrete triggers.]

### Read First

- Current fact or invariant.
- Current fact or invariant.

### Scope

What belongs here.

### Not Here

What belongs elsewhere.

### Current Contract

Stable behavior, interfaces, workflows, schemas, commands, or rules.

### Related Surfaces

| Surface | Path / System | Why It Matters |
| ------- | ------------- | -------------- |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
```

## Non-Negotiables

- Do not copy task summaries into docs.
- Do not write uncertain claims as established fact.
- Do not duplicate facts across docs.
- Do not create new docs when an existing canonical home works.
- Prefer moving, merging, and restructuring over duplication.
- Preserve current truth over historical narrative.
- Keep README concise and orientation-focused.
- Keep agent guidance focused on behavior, not duplicated project docs.
- Mark unresolved uncertainty as `Needs validation`.
