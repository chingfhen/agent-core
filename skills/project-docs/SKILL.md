---
name: project-docs
description: Maintains durable project knowledge in docs/ (plus README and agent-guidance surfaces like AGENTS.md) as inherited truth for future agents. Load before creating or editing anything under docs/, README or AGENTS.md; not needed to merely read docs. Routes high-leverage knowledge into canonical files, rewrites docs toward simpler current understanding, and prevents bloat through canonical routing and evidence distillation.
disable-model-invocation: false
---

# Project Docs

Maintain durable project knowledge as inherited truth for future agents.  
Durable knowledge usually belongs in `docs/`, README, agent guidance files, or a deliberate combination of those surfaces.  
Docs are not task state, source material, transcripts, status diaries, or execution history.  
Documentation exists to reduce future rediscovery cost and keep future agents correct, smooth, and consistent.  
Optimize documentation and agent guidance for future agent sessions by preserving only durable, high-leverage knowledge that future executors should not have to rediscover.

## Core Model

* **`project-docs` owns durable project knowledge and long-term agent behavior.**
* **Active tasks in `tasks/` own execution state** and fresh-session handoff.
* **`tasks/backlog/` owns deferred future-work briefs** that should survive without becoming active task state.
* **`source-material/` holds supporting artifacts and source evidence**, not authority.
* **`archive/` holds historical reference material**, not current truth.
* A document should answer **one durable question well**.
* Each durable fact should have **one canonical home**.
* **Prefer replacing stale content** over appending updates.
* **Preserve current truth** over historical narrative.
* Optimize for future agent effectiveness **without accumulating documentation bloat**.
* **Ask only when a durable choice is materially ambiguous**, conflicts with existing truth, or changes architecture, product direction, or stable operating behavior.

### Guiding Philosophy

Ask:
> If this task disappeared tomorrow, what knowledge would future executors repeatedly pay to rediscover, or what behavior should future agents consistently preserve?

* **Preserve that.**
* Everything else is negotiable.
* The purpose of documentation is **not to remember everything**.
* The purpose of documentation is to **preserve inherited truth and durable behavior**.
* Use version control for history.
* Use documentation for **current understanding**.

## Documentation Admission Test

Before persisting knowledge, make one holistic judgment:

> Is this durable, actionable project truth that future agents would pay meaningful cost to rediscover?

Consider three reinforcing lenses, not separate mandatory gates:

* **Durable:** It remains true after the current task.
* **Expensive to rediscover:** Forgetting it would create meaningful repeated investigation or uncertainty.
* **Actionable:** It affects system behavior, agent behavior, or future decisions.

Document knowledge when these lenses together show it is worth inheriting. If version control is already the better memory, do not document it.

*Interesting is not enough.* *Useful during the current task is not enough.* Only preserve knowledge that meaningfully reduces future rediscovery or stabilizes future agent behavior.

## Knowledge Destinations

### Docs
* **Answers:** What is true about the project?
* **Default home:** `docs/`
* *Examples:* Architecture, Interfaces, Workflows, Runtime behavior, Infrastructure, Product behavior, Technical decisions, Operational invariants, Troubleshooting guidance worth inheriting.

### README
* **Answers:** How should someone orient themselves to this repository?
* *Examples:* Project overview, Entry points, High-level architecture, Setup and usage, Important workflows, Navigation guidance, Onboarding essentials.
* README should optimize discoverability and orientation. It should remain concise and is **not a dumping ground for implementation detail**.

### Agent Guidance Files
* **Answers:** How should agents operate in this project?
* *Examples:* Repo-wide operating principles, Stable workflow rules, Coding philosophy, Planning heuristics, High-frequency conventions, Important agent guidance, Recurring mistakes worth preventing.
* *Supported examples include:* `AGENTS.md`, `CLAUDE.md`, and other repository-defined agent guidance files.
* Agent guidance files are **not a second documentation system**. Keep them concise and prefer behavioral guidance over project knowledge.

### Tasks
* **Owns:** Active execution state, Current progress, Session handoff, Work remaining, Investigations still in flight.
* **Default home:** `tasks/`

### Backlog Reports
* **Answers:** What deferred future work should survive without becoming active task state or canonical runtime truth?
* **Default home:** `tasks/backlog/`
* *Examples:* Deferred feature briefs, future integrations, later opportunities, and preserve-for-later execution notes.
* Use dated filenames: `YYYY-MM-DD__kebab-case-bookmark.md`.
* `tasks/backlog.md`, if present, should stay a thin index or summary.

### Source Material
* **Answers:** What supporting artifacts or inputs should remain available without becoming canonical truth?
* **Default home:** `source-material/`
* *Examples:* Seed specs, imported notes, external references, logs, captured investigations, experiment output, one-off artifacts.
* Source material is **not durable truth** and should not flow directly into docs.

### Archive
* **Answers:** What historical material is still worth keeping for reference?
* **Default home:** `archive/`
* *Examples:* Superseded specs, retired designs, frozen exports, old snapshots, historical notes that should not shape current truth by default.
* Archive is **not canonical truth**. Reuse it as context, then validate before promoting conclusions back into docs.

## Evidence Distillation

Follow this model:
$$\text{Evidence} \rightarrow \text{Understanding} \rightarrow \text{Decision} \rightarrow \text{Documentation}$$

Persist the **conclusions reached from evidence**, not the evidence itself. Preserve evidence only when future decisions depend on re-evaluating it.

If the evidence itself must be retained, keep it in `source-material/` or `archive/`, not in canonical docs.

Docs should answer **what future agents should act on**, not everything that happened.

## Non-Negotiables

* **Do not copy task summaries** into docs.
* **Do not write uncertain claims** as established fact.
* **Do not duplicate facts** across docs.
* **Do not create new docs** when an existing canonical home works.
* **Prefer moving, merging, and restructuring** over duplication.
* **Verify conflicting information** before choosing a source of truth.
* Mark unresolved uncertainty as `Needs validation`.
* **Preserve only durable, high-leverage knowledge** that benefits future sessions.
* **Improve existing docs** before creating new ones.
* **Use README and agent guidance files intentionally** rather than duplicating information elsewhere.
* **Do not let `source-material/` or `archive/` silently become canonical documentation.**
* **Do not let `tasks/backlog/` become active task state, a raw research dump, or a general archive.**

---

## Preferred Doc Shape And Canonical Routing

Use relevant sections intentionally. The first screen should remain short and scannable.

Choose the narrowest existing canonical home that fits. Improve an existing document before creating a new one. Create a new doc only when no existing document answers the durable question well.

Before writing, inspect repository-local routing surfaces:

* `docs/`
* README.md
* Agent guidance files
* Documentation indexes
* Existing docs
* Nearby code ownership
* `tasks/` when execution context matters
* `source-material/` when source evidence matters
* `archive/` only when historical context still affects the decision

For agent guidance files:

* Prefer the repository's established convention.
* Recognize AGENTS.md, CLAUDE.md, and other repo-defined equivalents.
* If multiple agent guidance files exist, identify the canonical one and avoid duplicating guidance.
* Prefer thin pointers over duplicated instructions when appropriate.
* Create a new agent guidance file only when explicitly requested or clearly required by repository convention.

Canonical Markdown docs use `title`, `description`, and `updated` frontmatter. `type`, `tags`, and `update_when` are optional and should appear only when useful. README and agent-guidance files should keep their established conventions unless the repository deliberately chooses otherwise.

Write `description` so it helps readers discover the document and identifies its canonical knowledge boundary. When an established documentation index includes a description, reuse the canonical frontmatter description instead of maintaining a separate summary.

Change `updated` only when durable meaning changes, not for formatting, spelling, metadata normalization, or mechanical link repair.

```markdown
---
title: [Doc Title]
description: [One sentence describing the document's canonical knowledge boundary.]
updated: YYYY-MM-DD
---

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

Tiny visuals / ASCII sketches are recommended when they make structure easier to scan, but only as lightweight compression, not decoration.

## Related Surfaces

| Surface | Path / System | Why It Matters |
| ------- | ------------- | -------------- |

## Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
```

Small docs may omit optional body sections. Prefer contextual links between related canonical docs and selective references to stable implementation entry points.

## Documentation Evolution

Documentation should evolve toward simpler expressions of current understanding. When updating docs:

* Prefer rewriting over appending.
* Replace obsolete explanations.
* Collapse duplicated decisions.
* Remove historical residue once its lessons have been absorbed.
* Simplify wording when understanding improves.
* Improve discoverability, orientation, and reduce future cognitive load.

Do not preserve earlier explanations merely because they existed. Version control preserves history; documentation preserves inherited truth.

## Lifecycle Operations

### Update / Sync Durable Knowledge

Use when durable knowledge changes, or when the user asks to update or sync knowledge from current conversation decisions, active tasks, completed tasks, code changes, debugging findings, investigations, design discussions, existing docs, or any other session context. This is the default documentation-maintenance operation.

* Do not assume update or sync means task harvest only or preserving everything.
* Read the target document and relevant surrounding context.
* Check likely related docs for overlap or conflict.
* Treat tasks, discussions, code changes, and evidence as inputs, not authority.
* Apply the Documentation Admission Test and extract only durable knowledge.
* Distill evidence into conclusions and decisions.
* Choose the canonical home.
* Route project truth to docs.
* Route deferred future-feature briefs and preserve-for-later execution notes to `tasks/backlog/` when they should survive but are not active work.
* Route supporting but non-canonical artifacts to `source-material/` when they should remain available.
* Route retired or historical reference material to `archive/` when it should be kept but not treated as current truth.
* Route onboarding knowledge to README when appropriate.
* Route agent behavior guidance to agent guidance files.
* Route information to multiple destinations only when each serves a distinct purpose. Avoid duplicating detailed documentation inside agent guidance files.
* Validate important claims against current docs, code, or evidence when practical.
* Rewrite existing docs or restructure documentation when a clearer canonical shape or better expression of current understanding emerges.
* Update every canonical document whose durable truth is materially affected.
* Add or normalize required frontmatter only on canonical documents materially edited; do not perform unrelated metadata churn.
* When a canonical document's title, description, path, scope, or existence changes, update its established index entry and directly affected documentation links.
* Keep the first screen concise.
* Add decisions only when they prevent future drift.
* Report: Persisted, Already documented / skipped, Rewritten / simplified, Uncertain, Rerouted / restructured.

Done when the canonical surface reflects current durable truth, transient state was left out, stale guidance no longer competes with it, and every promoted fact has one appropriate home.

### Verify / Trim

Use for an explicitly requested documentation audit, migration, or scoped cleanup. Do not turn an ordinary documentation update into a repository-wide audit. During normal updates, repair only obvious, nearby issues that are certain, cheap, and material to future understanding.

* Compare docs, README, agent guidance files, `tasks/`, code, and any relevant `source-material/` or `archive/` context.
* Flag stale paths, commands, workflows, and assumptions.
* Identify duplicated knowledge and choose one canonical home.
* Replace duplication with pointers where appropriate.
* Remove obsolete implementation chatter, historical residue, and stale agent guidance from canonical docs.
* Keep agent guidance focused on behavior.
* Preserve durable decisions, constraints, and current behavior.
* Simplify documentation where understanding has improved.
* For a requested audit or migration, also check frontmatter consistency, index drift, broken documentation links, and orphan canonical documents.
* Preserve future usefulness while minimizing maintenance burden.
* Mark risky uncertainty as Needs validation.

### Resume

Use when the user asks where a topic stands.

* Read the most relevant docs and context.
* State the current source of truth.
* Summarize the current contract.
* Highlight important constraints and known uncertainty.
* Identify related work when useful.
* Keep the response concise.
