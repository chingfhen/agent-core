---
name: knowledge-base
description: Maintains a portable Git knowledge base rooted at knowledge-base/. Use to initialize it, capture material into the inbox, review or curate inbox material, organize and index preserved evidence for retrieval, synthesize or maintain canonical knowledge, maintain knowledge navigation, retrieve prior evidence, or trace why knowledge changed. Owns only knowledge-base/**. Curation and maintenance are proposal-gated by explicit human approval, and every mutating operation ends with one isolated knowledge-base Git commit; never push as part of this skill.
disable-model-invocation: false
---

# Knowledge Base

## Purpose and Ownership

Maintain a portable, repository-local knowledge system rooted at:

```text
knowledge-base/
├── inbox/
├── evidence/
│   └── <domain>/
│       ├── index.md
│       └── <subdomain>/
│           └── [<optional-deeper-path>/]
│               └── YYYY-MM-DD--description.ext
└── knowledge/
    └── index.md
```

This skill owns **only `knowledge-base/**`**.

Never create, edit, move, delete, stage, or commit files outside that boundary. The skill may read the smallest relevant set under `docs/` when project context materially helps review, curation, maintenance, retrieval, or tracing. It may read other repository material outside `knowledge-base/**` only when the user explicitly asks to use it as source/context. These read exceptions do not expand write ownership. Any persisted output still belongs under `knowledge-base/`.

The skill defines the behavior. `knowledge-base/` holds the state. The same contract should work in a dedicated knowledge repository or inside a larger project repository.

## Core Model

Use only three primary concepts.

### Inbox

`knowledge-base/inbox/` is the single **unprocessed entry point**.

Humans or agents may place material here without deciding its final name, category, evidence location, or knowledge impact.

Anything still in `inbox/` is **not yet curated**.

### Evidence

`knowledge-base/evidence/` contains **processed supporting material preserved for future inspection and retrieval**.

Evidence may be a PDF, Markdown file, report, transcript, research note, conversation-derived artifact, image, personal write-up, or another useful source format.

All evidence follows the same ingestion contract. Do not create evidence classes such as `rich`, `raw`, `primary`, or `processed` merely because some artifacts are more structured than others.

Every newly curated evidence artifact must be discoverable through multiple cheap signals:

```text
domain
subdomain
optional deeper path
date-prefixed descriptive filename
domain evidence index entry
source content when text-searchable
```

Evidence is not automatically canonical truth. Preserve it so future humans and agents can inspect what informed the knowledge base and reconsider conclusions later.

### Knowledge

`knowledge-base/knowledge/` contains **current human-approved synthesized understanding**.

Knowledge:

- is Markdown only;
- is revisable as understanding improves;
- represents current understanding, not historical accumulation;
- should remain substantially more compact than the evidence base;
- should update existing canonical pages rather than proliferate overlapping pages;
- must remain traceable to material supporting or limiting evidence.

Core invariant:

> **Evidence may accumulate. Knowledge must consolidate.**

## Project Context from Canonical Docs

When the knowledge base lives inside a project repository, use canonical project documentation under `docs/` as the source of project context.

The purpose is not to ingest or duplicate project documentation. It is to let the KB maintainer understand the project well enough to interpret incoming material and existing knowledge in context.

Use this conservatively:

- Capture does not require reading project docs.
- During Review / Propose, Curate / Maintain, Retrieve, or Trace, read relevant docs only when project context can materially improve interpretation or judgment.
- Read the **smallest relevant set**. Start from an obvious docs index, overview, or directly relevant page when available; follow references only to resolve concrete uncertainty.
- Do not sweep all of `docs/` merely because KB work is occurring.
- Do not copy project docs into the KB merely to make them discoverable there.
- Do not create a `project-context.md` surrogate or another summary layer by default.
- `docs/` remains authoritative for documented project architecture, decisions, invariants, contracts, workflows, and implemented intent.
- `knowledge-base/knowledge/` contains synthesized durable understanding derived from curated evidence. It may inform project work but should not compete with `docs/` as the source of truth for current project state.
- If KB knowledge conflicts with current project docs or verified repository reality, preserve the evidence honestly, treat the project docs/repository as authoritative for implemented state, and surface the discrepancy when it materially affects curation.
- If no relevant project docs exist, proceed from the inbox material, existing KB state, and the user's request. Do not invent project context.

Project docs should orient judgment without prescribing what the KB must retain. The maintainer remains responsible for deciding what evidence is useful, what knowledge is durable, and how new material relates to the project.

## Authority and History

Use repository surfaces for different questions:

```text
What is the project's documented current intent/state? -> docs/ + repository
What has not been processed?                            -> inbox/
What source material do we have?                        -> evidence/<domain>/index.md + evidence tree
What did a source actually say?                         -> evidence/*
What durable understanding has the KB synthesized?     -> knowledge/*.md
What currently supports it?                             -> that page's ## Evidence section
Why/when did it change?                                 -> Git curation commit
What exactly changed?                                   -> Git diff/history
```

Evidence indexes are **discovery metadata, not a competing source of truth**. The evidence artifact remains authoritative for its own contents.

Do not create a global curation log, registry, SQLite database, vector database, sidecar metadata system, or other competing source of truth by default. Domain evidence indexes defined by this skill are the only default evidence-discovery layer.

If a richer generated query layer becomes useful later, it must be rebuildable from canonical files and Git history and requires an approved maintenance change.

# Operating Modes

This skill supports six modes:

1. **Initialize** — create the minimal KB when explicitly requested.
2. **Capture** — place explicitly requested material in `inbox/` without curating it.
3. **Review / Propose** — inspect inbox material and existing KB state, then propose curation without changing files.
4. **Curate / Maintain** — after explicit approval, organize and index evidence, revise knowledge, update navigation, verify, and commit.
5. **Retrieve** — locate preserved evidence or current knowledge using repository search and inspection without changing files.
6. **Trace** — explain current provenance or historical change using evidence links and Git.

Read-only review, retrieval, and tracing do not create commits.

**Every mutating operation must end with one isolated Git commit containing only changes from that KB operation, and the skill must not push.**

Before any mutation, confirm the host is a Git work tree and that an isolated KB-only commit can be made safely. If not, stop before writing.

# Initialize

Initialize only when explicitly requested.

Create the minimal structure:

```text
knowledge-base/
├── inbox/
├── evidence/
└── knowledge/
    └── index.md
```

Do **not** invent evidence domains or subdomains during initialization. Create `evidence/<domain>/index.md` only when the first curated artifact for that domain is approved.

Because Git does not track empty directories, minimal placeholders under `inbox/` and `evidence/` are acceptable when needed to preserve the initialized structure.

`knowledge/index.md` starts as a concise navigation page, not a process manual.

Do not create extra schemas, registries, databases, scripts, logs, archives, or workflow files without demonstrated need and human approval.

End with one isolated commit:

```text
kb(init): initialize knowledge base
```

# Capture

Capture is deliberately low-friction.

When the user explicitly asks to save, drop, or place material into the KB without curating it:

1. Put it under `knowledge-base/inbox/`.
2. Preserve supplied format and substantive content.
3. Avoid semantic classification beyond choosing a collision-safe inbox filename.
4. Do not change `evidence/`, `knowledge/`, or `knowledge/index.md`.
5. Do not infer that capture authorizes curation.
6. Commit only the captured inbox material.

Capture needs no separate curation proposal because canonical knowledge is unchanged; the user's request to capture is the authorization.

Example:

```text
kb(capture): add experience-to-capability playbook

Inbox:
- knowledge-base/inbox/Experience-to-Capability-Playbook.md

Outcome:
- captured-unprocessed
```

Never overwrite an existing inbox item silently. Use a collision-safe name or ask when identity is ambiguous.

---

# Review Before Curation

When the user asks to process, digest, curate, organize, or consider inbox material, **review first and change nothing** unless the user has already explicitly approved a concrete current proposal.

For each relevant inbox item:

1. Read enough of the item to understand its durable contribution and distinctive retrieval terms.
2. When project context can materially affect interpretation, read the smallest relevant set under `docs/`; do not read project docs merely as ceremony.
3. Inspect `knowledge-base/knowledge/index.md`.
4. Search relevant existing knowledge before proposing a new canonical page.
5. Inspect directly relevant evidence when needed to understand provenance, overlap, or contradiction.
6. Inspect existing evidence domain and subdomain directory names so sensible categories are reused rather than duplicated.
7. Choose an exact proposed evidence destination satisfying the mandatory evidence path contract.
8. Draft the exact one-line domain evidence-index record that curation will append.
9. Determine whether the material:
   - creates genuinely new canonical knowledge;
   - updates/refines existing knowledge;
   - both creates and updates knowledge;
   - or causes **no material knowledge change**.
10. Determine how affected knowledge provenance should change.
11. Determine required `knowledge/index.md` changes.
12. Surface material ambiguity, contradiction, overlap, or structural choices.
13. Present one authoritative Curation Proposal.

Do not move, rename, edit, delete, create, stage, or commit repository files during review.

Do not read an entire existing domain evidence index merely to prepare an append. Search it only when needed to check an exact path, investigate possible duplicate evidence, or answer a retrieval question.

## Curation Outcomes

A fully curated inbox item ends in one of these states:

```text
preserve evidence + create knowledge
preserve evidence + update knowledge
preserve evidence + create and update knowledge
preserve evidence only; no material knowledge change
```

There is no separate `digested but not synthesized` state.

```text
inbox/          = pending / unprocessed
outside inbox/  = processed
```

Do not remove an item from `inbox/` unless its approved curation is completed in the same operation.

# Mandatory Curation Proposal

Before any curation or maintenance write, present a proposal that lets the human judge **what will move, how the evidence will remain discoverable, what knowledge will change, what provenance will be asserted, and why**.

Use this shape, omitting only genuinely irrelevant sections:

```markdown
# Curation Proposal

## Input

- `knowledge-base/inbox/<current-file>`

## Summary

[Concise description of the material and why it may matter.]

## Evidence Placement

From:
`knowledge-base/inbox/<current-file>`

To:
`knowledge-base/evidence/<domain>/<subdomain>/[<optional-deeper-path>/]<YYYY-MM-DD--name.ext>`

Reason:
- [why this domain fits]
- [why this subdomain fits]
- [why any deeper path is justified]
- [why this filename/date is appropriate]
- [which existing directories are reused or why a new domain/subdomain is justified]

## Evidence Discovery

Index:
`knowledge-base/evidence/<domain>/index.md`

Append record:
`- YYYY-MM-DD | <subdomain[/deeper-path]> | [<Title>](<relative-path>) | <retrieval-oriented description>`

Retrieval terms:
- [the distinctive concepts/entities/techniques intentionally represented in the description]

## Knowledge Impact

### Update
`knowledge-base/knowledge/<existing-page>.md`

Content changes:
- [specific durable conclusion/change]

Provenance changes:
- Add `<evidence-file>` as supporting, limiting, or contradictory evidence for [specific conclusion].

Why:
[Why this belongs in this canonical page.]

### Create
`knowledge-base/knowledge/<new-page>.md`

Scope:
[What durable conceptual question this page will own.]

Why a new page is justified:
[Why existing knowledge cannot coherently absorb it.]

### No Knowledge Change

[Use when applicable.]

Reason:
[Why the evidence does not materially create, refine, contradict, or limit current understanding.]

## Knowledge Index Impact

- [entries to add/change/remove]

or

- No change.

## Planned Result

- Evidence artifacts preserved: N
- Evidence-index records appended: N
- Evidence domain indexes created: N
- Knowledge documents created: N
- Knowledge documents updated: N
- Knowledge documents merged/removed: N
- Knowledge-index entries changed: N

## Human Attention

[Only genuinely consequential, debatable, uncertain, or structural points.]

## Approval

No repository changes will be made until explicitly approved.
```

The exact proposed evidence destination and exact discovery record must always be shown. Evidence organization is agent-managed, but the human should know where material will live and how it will be discoverable before approving it.

A good proposal makes clear:

1. what is being processed;
2. where preserved evidence will live;
3. which domain index will receive the discovery record;
4. what retrieval description will be stored;
5. what current knowledge will change;
6. whether a new canonical page is justified;
7. what evidence-to-knowledge relationships will be asserted;
8. whether the knowledge index changes;
9. what deserves human judgment;
10. what the final operation will contain.

Resolve routine choices yourself. Do not hide material alternatives behind `maybe`, `possibly`, or `either`.

# Human Approval Boundary

Curation and maintenance are human-approved operations.

Before approval, the agent may read, search, compare, reason, trace Git history, and revise the proposal.

Before approval, it must not as part of curation or maintenance:

- move/rename inbox material;
- create/edit/delete/merge/reorganize evidence;
- create/edit/delete/merge/reorganize knowledge;
- create or update evidence domain indexes;
- update the knowledge index;
- stage or commit curation changes.

Explicit approval means the human unambiguously authorizes the current proposal, for example `proceed`, `approved`, or equivalent language.

If the human changes the proposal, the changed direction becomes authoritative. If the same message both specifies the change and says to proceed, do not require a redundant approval round.

After approval, execute the approved proposal. Routine mechanics are agent-owned.

If execution reveals a **materially different** knowledge change, evidence destination, evidence-index record, merge/split, deletion, contradiction, or structural consequence that was not approved, do not silently expand the operation. Stop the unapproved part and return with a revised proposal.

---

# Evidence Organization

Evidence ingestion is deliberately **strict and cheap**.

The storage contract should make future retrieval easy without requiring rich metadata, embeddings, a database, or repeated full-corpus analysis.

## Mandatory Path Contract

Every newly curated evidence artifact must live at least two semantic directory levels below `evidence/`:

```text
knowledge-base/evidence/
  <domain>/
    <subdomain>/
      [<optional-deeper-path>/]
        YYYY-MM-DD--lowercase-kebab-case.ext
```

Rules:

- `<domain>` is mandatory.
- `<subdomain>` is mandatory.
- Additional semantic directories are optional.
- Never place curated evidence directly in `evidence/`.
- Never place curated evidence directly in `evidence/<domain>/`.
- Reuse an existing domain whenever it reasonably fits.
- Reuse an existing subdomain whenever it reasonably fits.
- Create a new domain or subdomain only when existing categories would be materially misleading.
- Additional nesting should normally reuse an existing useful structure; do not invent deeper paths merely to describe one artifact more precisely.
- Prefer broad, stable category names that a human would naturally browse or search.
- Do not use catch-all subdomains such as `misc`, `other`, or `general` merely to satisfy the minimum depth when a meaningful category can be chosen.
- Do not reorganize unrelated evidence during ordinary curation.

This is a **minimum structure**, not an invitation to build a deep ontology.

Examples:

```text
evidence/ai/evaluation/2026-09-16--prompt-evaluation-and-optimization.md
evidence/ai/agents/2026-09-13--agent-tooling-interface-design.md
evidence/career/compensation/2026-09-10--bank-data-scientist-benchmarking.md
```

Avoid:

```text
evidence/2026-09-16--prompt-evaluation.md
evidence/ai/2026-09-16--prompt-evaluation.md
evidence/ai/llm/prompts/evaluation/pairwise/ranking/2026-09-16--prompt-evaluation.md
```

Before proposing placement, inspect existing domain and subdomain directory names. This should be a cheap structural inspection, not a full evidence audit.

## Naming

Newly curated evidence uses:

```text
YYYY-MM-DD--lowercase-kebab-case.ext
```

Examples:

```text
2026-09-07--experience-to-capability-playbook.md
2026-09-13--karpathy-llm-wiki.pdf
2026-09-13--agent-tooling-interface-design.md
```

Rules:

- ISO `YYYY-MM-DD`;
- exactly `--` between date and descriptive name;
- lowercase kebab-case descriptive portion;
- concise but recognizable in VS Code;
- preserve useful domain terminology;
- choose words a future human or agent might plausibly remember;
- avoid generic names such as `notes.md`, `research.md`, `document.pdf`, or `chatgpt.md`;
- use the artifact/source date when confidently known and representative;
- otherwise use the date it entered the KB;
- do not mass-rename historical evidence merely to enforce newer conventions without an approved maintenance proposal.

## Domain Evidence Index Contract

Each evidence domain has exactly one discovery index:

```text
knowledge-base/evidence/<domain>/index.md
```

The domain index covers **all evidence artifacts beneath that domain**, including every subdomain and any deeper approved paths.

Do not create:

```text
knowledge-base/evidence/index.md
knowledge-base/evidence/<domain>/<subdomain>/index.md
```

for ordinary evidence discovery.

Every newly curated evidence artifact receives **exactly one** record in its domain index.

### Record Shape

Each record is exactly one physical Markdown line:

```markdown
- YYYY-MM-DD | `<subdomain[/deeper-path]>` | [<Descriptive Title>](<relative-path-from-domain>) | <retrieval-oriented description>
```

Example:

```markdown
- 2026-09-16 | `evaluation` | [Prompt Evaluation and Optimization](evaluation/2026-09-16--prompt-evaluation-and-optimization.md) | Prompt evaluation, deterministic checks, semantic LLM judges, pairwise comparison, Elo, Bradley-Terry, adaptive sampling.
```

The record must be compact enough for the index to remain useful at scale.

The retrieval-oriented description must:

- be a single line;
- normally be about 8–30 words;
- state the central subject;
- include several distinctive terms, entities, techniques, or phrases a future user may remember;
- prefer terminology actually present in or faithfully describing the evidence;
- avoid generic wording such as `useful discussion`, `research notes`, or `AI information`;
- avoid conclusions, provenance narratives, detailed summaries, and information not present in the evidence.

Do not add tags, YAML metadata, aliases, sidecar files, per-artifact summaries, or duplicate catalog records merely for retrieval.

### Append-Only Curation Contract

During ordinary curation, an existing domain index is **append-only**.

To add a record:

1. Construct the complete record from the evidence already reviewed.
2. If the domain index exists, perform only a cheap exact-path duplicate check as needed; do not read or parse the whole file merely to append.
3. Append the record as a new line using an append primitive, for example:

```bash
printf '%s\n' "$record" >> knowledge-base/evidence/<domain>/index.md
```

4. Do not rewrite, sort, reformat, regroup, or regenerate existing records during ordinary curation.
5. Do not use a read-modify-write operation when a direct append will do.
6. Do not use whole-file write/replace APIs for an existing domain index during ordinary curation; use an append-capable primitive.
7. If the domain is new, create `index.md` once with a concise heading and the first record:

```markdown
# Evidence Index — <Domain>

- ...
```

The exact shell command is not normative; **append semantics are**. Use the safest append mechanism available in the environment.

A domain index may be rewritten only during an explicitly approved maintenance operation, for example to repair stale paths, remove duplicates, or reflect approved evidence moves/renames.

Git preserves index history. Do not turn the index itself into an event log with `added`, `moved`, `deleted`, or `superseded` records.

## Preserve Original Representation

Preserve source format by default:

```text
PDF      -> PDF
Markdown -> Markdown
image    -> image
```

Moving or renaming evidence must not silently alter substantive source content.

Do not automatically convert PDFs, images, or other original artifacts into Markdown. A derived note may be created only when it has independent durable value and appears in the approved proposal.

Evidence is historical material. Correct its content only when explicitly requested or when an objective capture error is identified and approved.

## Retrieval Design

Evidence is intentionally stored so future agents can recover it through several independent signals:

```text
domain index records
domain/subdomain paths
date-prefixed filenames
descriptive filenames
full-text search where supported
Git history when historical context matters
```

Retrieval is guidance, not a rigid protocol.

When asked to find remembered evidence, use any efficient combination of:

- searching one likely domain index;
- searching all `evidence/*/index.md` files;
- filtering paths or filenames by remembered date, domain, subdomain, or words;
- grepping/searching text-searchable evidence contents;
- inspecting likely candidate artifacts;
- broadening terms, synonyms, or date ranges when the first search is insufficient;
- using Git when the question is about when, why, or where something moved or changed.

Prefer cheap narrowing before opening many artifacts, but do not require one fixed search order.

The indexes are especially valuable for binary or poorly text-searchable evidence because every curated artifact still receives a compact textual discovery surface.

# Knowledge Admission and Synthesis

Before creating a knowledge document, search existing knowledge.

Ask:

> Does an existing canonical page already own this concept well enough to absorb the new understanding coherently?

Prefer updating that page when yes.

Create a new page only when the material establishes a distinct durable conceptual scope that would make an existing page incoherent, overly broad, or hard to maintain.

Do not create a knowledge page merely because:

- a new evidence file exists;
- the source has a convenient title;
- it came from a separate conversation/research session;
- creating another file is easier than synthesizing into an existing one.

Each durable concept should have one primary canonical home.

## Maintain Current Understanding

Canonical knowledge answers:

> What should a future human or agent understand now?

When understanding changes:

- rewrite affected explanations;
- remove or replace stale conclusions;
- consolidate duplicated statements;
- preserve material uncertainty honestly;
- keep limiting/contradictory evidence visible when it still affects interpretation;
- rely on Git for historical versions.

Do not append `Update`, `Latest`, `Revision`, or dated-history sections merely to preserve old beliefs that Git already retains.

## Distill Evidence

Use this flow:

```text
preserved evidence
      ↓
understanding
      ↓
durable current conclusion
      ↓
canonical knowledge page
```

Persist conclusions, not the reasoning transcript.

A new evidence item may legitimately produce **no knowledge change**. Preserve the evidence and record that outcome in the curation commit rather than manufacturing a conclusion.

## Contradiction and Uncertainty

Do not silently choose between materially conflicting evidence.

Surface important conflict in the proposal. After approval, canonical knowledge should accurately reflect the current state, such as:

- evidence is mixed;
- a conclusion applies only under stated conditions;
- one source limits another;
- the current interpretation remains uncertain.

Do not create a separate hypothesis subsystem for ordinary uncertainty.

---

# Knowledge Markdown Contract

Every canonical file under `knowledge-base/knowledge/`, except `index.md`, must be Markdown with minimal frontmatter:

```markdown
---
title: [Knowledge Title]
description: [One sentence defining the document's canonical knowledge boundary.]
updated: YYYY-MM-DD
---
```

Required fields are exactly:

- `title`
- `description`
- `updated`

Do not add mandatory metadata without demonstrated need and human approval.

Change `updated` only when durable meaning changes, not for formatting-only edits.

## File Names

Use stable lowercase kebab-case concept names without date prefixes:

```text
agent-memory.md
knowledge-evolution.md
software-maintainability.md
```

Git owns historical versions. Do not create `v2`, `latest`, or dated duplicates for ordinary evolution.

## Writing Shape

A knowledge document has one coherent durable scope and must be understandable without the old conversation.

Use only sections that help the topic. A common shape is:

```markdown
# [Title]

## Read First

- [highest-signal current conclusion]
- [important condition or boundary]

## [Topic-specific sections]

[Current synthesized understanding.]

## Evidence

### Supporting

- [Evidence title](relative/path)
  - [What this evidence materially supports.]

### Limiting or Contradictory

- [Evidence title](relative/path)
  - [What it limits, contradicts, or qualifies.]
```

`Read First` is recommended for substantial pages but optional when it adds no value.

`## Evidence` is required whenever a page contains evidence-derived knowledge; in normal curated knowledge this should almost always be present.

## Evidence Section Rules

The section represents evidence relevant to the **current** knowledge, not every source that ever touched the page.

For each listed artifact:

- use a working relative link to preserved evidence;
- explain why it matters;
- distinguish supporting from limiting/contradictory evidence when useful;
- avoid a flat bibliography with no semantic relationship;
- remove evidence that no longer materially supports or limits current understanding; Git preserves historical relationships.

For especially important or disputed claims, evidence may also be linked near the claim. Do not require inline citations for every sentence.

## Writing Rules

- Prefer rewriting over appending.
- Replace obsolete explanations instead of stacking updates underneath them.
- Collapse duplication.
- Keep the first screen scannable.
- Use plain language and explicit relationships.
- Preserve meaningful conditions and boundaries.
- Do not copy entire evidence artifacts into knowledge.
- Do not turn knowledge into a transcript, research diary, or chronology.
- Do not let stored evidence silently become canonical truth.
- Do not expand ordinary curation into an audit of unrelated knowledge.

---

# Knowledge Index Contract

`knowledge-base/knowledge/index.md` is mandatory.

It is the maintained human-and-agent map of **canonical knowledge**, not an evidence catalog.

Every canonical knowledge document must be reachable from the index.

Use intuitive topical grouping and one-line descriptions:

```markdown
# Knowledge Index

## AI

### Agents

- [Agent Memory](ai/agents/agent-memory.md)
  How agents preserve and use information across executions.

- [Knowledge Evolution](ai/agents/knowledge-evolution.md)
  How evidence is synthesized into maintained knowledge and improved capability.
```

Update the knowledge index in the same approved operation whenever a knowledge document is created, renamed, moved, merged, deleted, or materially rescoped.

Do not list individual evidence artifacts in `knowledge/index.md`. Evidence discovery belongs in `evidence/<domain>/index.md`.

The knowledge index should support progressive discovery:

```text
broad topic -> canonical knowledge page -> underlying evidence when needed
```

# Apply an Approved Curation

After explicit approval:

1. Re-check repository status before writing.
2. Confirm approved targets have not materially changed since review.
3. Confirm the approved evidence domain/subdomain path still fits the current directory structure.
4. Move/rename inbox material into the approved evidence location while preserving source content.
5. Ensure the corresponding `evidence/<domain>/index.md` exists; create it only if this is the first evidence in a new domain.
6. Append exactly the approved one-line discovery record using append semantics. Do not rewrite an existing domain index merely to add the record.
7. Create or rewrite approved knowledge pages.
8. Update affected `## Evidence` sections to express approved provenance relationships.
9. Repair directly affected knowledge links.
10. Update `knowledge/index.md` when required.
11. Ensure successfully curated items no longer remain in `inbox/` as pending copies.
12. Review the diff for scope, correctness, accidental bloat, and append-only index behavior.
13. Run the verification contract below.
14. Stage only approved `knowledge-base/**` changes from this operation.
15. Create one isolated commit using the required commit contract.
16. Verify the commit matches the approved proposal and unrelated work remains untouched.
17. Report the commit identifier and concise result. Do not push.

If final inspection shows that an approved semantic change is no longer justified, do not silently substitute another. Return to proposal/discussion when the difference is material.

If execution requires a materially different evidence domain/subdomain, a different discovery description, or a non-append rewrite of an existing domain index, treat that as a proposal change rather than silently expanding the operation.

# Git Safety and Isolation

Git history is the durable curation ledger, so commit quality is part of KB quality.

## Hard Rules

- Never include files outside `knowledge-base/**` in a KB commit.
- Never mix unrelated application/project work into a KB commit.
- Never mix unrelated pre-existing KB changes into the current operation.
- Never reset, clean, discard, rewrite, or otherwise disturb unrelated work to obtain a clean commit.
- Do not amend or rewrite previous KB commits unless explicitly requested.
- Never push as part of this skill.

Before writing or staging, inspect repository status.

If an approved target already has uncommitted changes that cannot be safely attributed to this operation, stop rather than overwrite or combine work.

If pre-staged or unrelated changes make an isolated KB-only commit unsafe, stop and ask rather than manipulating unrelated repository state.

Use path-scoped staging/committing only when it reliably preserves unrelated work untouched.

---

# Commit Contract

The **proposal is temporary**. The **commit is the permanent ledger entry** describing what was actually executed.

## Titles

Use:

```text
kb(curate): <short searchable description>
kb(maintain): <short searchable description>
kb(capture): <short searchable description>
kb(init): initialize knowledge base
```

## Curation Body

Use this structure:

```text
Input:
- knowledge-base/inbox/<original-name>

Evidence:
- moved to knowledge-base/evidence/<domain>/<subdomain>/<final-path>

Evidence Index:
- appended one record to knowledge-base/evidence/<domain>/index.md
  - <short retrieval description>
- or created knowledge-base/evidence/<domain>/index.md with first record

Knowledge:
- updated knowledge-base/knowledge/<page>.md
  - <durable conclusion added, changed, limited, or removed>
  - <provenance relationship added/changed>

- created knowledge-base/knowledge/<page>.md
  - <canonical scope introduced>

Knowledge Index:
- <entries changed, or no change>

Outcome:
- <outcome token>

Rationale:
- <why knowledge changed or intentionally did not change>
- <why a new page was or was not justified>
- <material structural rationale when useful>

Approval:
- explicit human approval obtained before curation
```

The body must be rich enough for a future agent to understand the semantic transaction without relying only on filenames.

Always include the original inbox path, final evidence path, and affected evidence domain index so the artifact remains searchable after it moves.

## Outcome Tokens

Use one or more as applicable:

```text
evidence-only
knowledge-created
knowledge-updated
knowledge-created-and-updated
knowledge-restructured
```

For evidence-only curation, make the deliberate no-change result explicit:

```text
Outcome:
- evidence-only

Rationale:
- evaluated against relevant existing knowledge
- no material new, contradictory, limiting, or refining conclusion identified
```

This distinguishes `considered and unchanged` from `forgotten or unprocessed`.

## Maintenance Body

For approved organization/consolidation not driven by a specific inbox item:

```text
Scope:
- <affected KB paths or topic>

Evidence:
- <moves/renames, or no change>

Evidence Index:
- <records repaired/rewritten, domain indexes affected, or no change>

Knowledge:
- <merged/split/rewritten/moved pages and semantic reason>

Knowledge Index:
- <changes, or no change>

Outcome:
- knowledge-restructured

Rationale:
- <why this reduces duplication, drift, or navigation cost>

Approval:
- explicit human approval obtained before maintenance
```

The Git diff is stronger authority than commit prose if they ever disagree.

# Traceability

When asked why knowledge says something, move from current provenance toward deeper history only as needed.

## Evidence Retrieval

When the user remembers a prior discussion, source, report, or artifact rather than a canonical knowledge page, search evidence directly.

Useful search surfaces include:

```text
evidence/<domain>/index.md
evidence paths and filenames
date prefixes
evidence contents
Git history
```

Examples of useful strategies:

```text
remembered topic/entity
    -> grep likely domain index or all domain indexes

remembered approximate date
    -> filter YYYY-MM or nearby date-prefixed paths

remembered exact/distinctive phrase
    -> grep text-searchable evidence contents

remembered broad area
    -> narrow to domain/subdomain before wider search

uncertain memory
    -> combine index, filename, content, and date searches
```

These are suggestions, not a mandatory sequence. A retrieval agent may use better repository tools when available.

Verify likely candidates by opening enough of the actual evidence to confirm that it matches the user's request. Do not treat an index description as a substitute for the source itself.

## Current Provenance

Start with the knowledge page's `## Evidence` section.

Answer:

> What evidence currently supports, limits, or contradicts this understanding?

Follow linked evidence artifacts when necessary.

## Historical Provenance

When asked when or why a conclusion was introduced, changed, or removed:

1. identify the knowledge file/section;
2. inspect path-limited Git history;
3. use blame/history to find the relevant changing commit when useful;
4. read its structured KB commit body;
5. inspect the exact diff;
6. follow the preserved evidence path from the commit or knowledge file.

Intended trace:

```text
current knowledge claim
      │
      ├── ## Evidence ───────> preserved evidence
      │
      └── Git history/blame ─> curation commit
                                  │
                                  ├── semantic rationale
                                  ├── evidence placement/index
                                  ├── other knowledge affected
                                  └── exact diff
```

Do not invent missing provenance. If repository evidence cannot establish why a claim exists, say so.

## Cross-KB Questions

To find which knowledge pages use an evidence artifact, search knowledge Markdown for links to its path.

To find evidence by topic, date, filename, remembered wording, or domain, use the evidence retrieval surfaces above.

To find which curation introduced an artifact or changed a page, search Git commit bodies and path history.

Do not add a database merely because a relational question is possible. Add a richer derived query layer only after recurring evidence shows that domain indexes, filesystem/content search, and Git are insufficient.

# Maintenance and Autonomous Organization

The agent is responsible for keeping the KB navigable and compact, but all mutating maintenance remains proposal-gated.

Maintenance may identify:

- duplicate/overlapping knowledge pages;
- incoherent page scope;
- stale current conclusions;
- broken evidence links;
- canonical pages missing from the knowledge index;
- stale knowledge-index descriptions;
- evidence outside the mandatory domain/subdomain path contract;
- duplicate or near-duplicate domain/subdomain categories;
- inconsistent evidence naming;
- poor evidence placement;
- unnecessary directory proliferation;
- missing, duplicate, malformed, or stale domain evidence-index records;
- evidence-domain indexes containing paths that no longer resolve;
- ordinary curation that previously rewrote/sorted an index instead of appending;
- orphaned knowledge pages;
- Evidence sections that no longer reflect current support;
- multiple canonical homes for the same durable concept.

Prefer the smallest coherent correction:

```text
duplicate knowledge        -> merge into one canonical page
oversized mixed scope      -> split only when scopes are genuinely distinct
stale conclusion           -> rewrite current knowledge
bad evidence location      -> move/rename and repair links/index record
category drift             -> consolidate only affected domain/subdomain paths
broken evidence index      -> rewrite only the affected domain index
broken knowledge index     -> repair in the same change
```

Evidence-domain indexes are append-only during ordinary curation but **may be rewritten during approved maintenance** when repair requires it.

Do not preserve obsolete structure merely because it existed historically; Git preserves history.

Do not reorganize the whole KB during ordinary curation. Broader reorganization requires its own maintenance proposal with affected paths, evidence-index consequences, knowledge consequences, provenance effects, and knowledge-index impact.

# Verification Contract

Before every mutating commit, verify:

## Boundary

- every changed/staged path is under `knowledge-base/`;
- any `docs/` consulted for project context remained read-only;
- no `project-context.md` or equivalent summary layer was created by default;
- no unrelated repository work is included;
- no unrelated pre-existing KB work is included.

## Inbox

- every processed item in scope has left `inbox/`;
- no unapproved inbox item was altered;
- no partially curated state remains.

## Evidence

- every newly curated artifact is under `evidence/<domain>/<subdomain>/...`;
- no curated artifact was placed directly in `evidence/` or directly in `evidence/<domain>/`;
- final paths match the approved proposal;
- existing sensible domains/subdomains were reused where appropriate;
- new filenames follow the convention;
- source format is preserved unless conversion was explicitly approved;
- substantive source content was not silently rewritten;
- moves/renames have not broken directly affected links.

## Evidence Index

For each newly curated evidence artifact:

- exactly one discovery record exists in `evidence/<domain>/index.md`;
- no subdomain index or global `evidence/index.md` was created for ordinary discovery;
- the record is one physical line;
- the date, subdomain/deeper path, title, and relative link are correct;
- the description is concise and retrieval-oriented rather than a full summary;
- the linked evidence path resolves;
- ordinary curation changed an existing domain index only by appending the approved record;
- existing records were not sorted, reformatted, regenerated, or rewritten merely to add the new record;
- if the domain was new, its index contains only the concise heading and valid records.

## Knowledge

- created/updated canonical files are Markdown;
- required frontmatter is present and accurate;
- each page has one coherent scope;
- existing knowledge was improved rather than duplicated where appropriate;
- stale superseded wording was removed rather than layered underneath;
- material uncertainty remains honest;
- `## Evidence` links resolve and explain why each artifact matters;
- limiting/contradictory evidence remains visible when relevant.

## Knowledge Index

- every canonical knowledge page is reachable from `knowledge/index.md`;
- created/moved/merged/rescoped pages are represented correctly;
- descriptions match current scope;
- removed pages leave no stale index links;
- individual evidence artifacts were not added to the knowledge index.

## Git Record

- staged diff matches the approved operation;
- commit body names original inbox and final evidence paths for curation;
- commit body names the affected evidence domain index;
- semantic knowledge changes are described, not just filenames;
- rationale explains material decisions and evidence-only outcomes;
- approval is recorded when required;
- one isolated KB-only commit succeeds;
- the final commit contains no path outside `knowledge-base/`.

After commit, report the commit identifier and concise summary. Do not push.

# Non-Negotiables

- This skill owns only `knowledge-base/**`.
- Use relevant `docs/` as read-only project context when it materially helps KB judgment; do not duplicate project docs into the KB by default.
- Read the smallest relevant project-doc set; do not sweep `docs/` merely because KB work is occurring.
- Do not create `knowledge-base/project-context.md` or another project-context surrogate by default.
- `docs/` and verified repository state remain authoritative for current project implementation and documented project decisions.
- `inbox/` is the single unprocessed entry point.
- Capture does not imply curation.
- Curation and maintenance require explicit human approval before writes.
- Evidence organization, evidence indexing, and knowledge synthesis happen in one approved curation operation.
- An inbox item leaves `inbox/` only when its curation is complete.
- Evidence is preserved; knowledge is revised.
- All evidence is treated under one ingestion model; do not create special evidence classes by richness or format.
- Preserve original evidence formats by default.
- Every newly curated evidence artifact must live under `evidence/<domain>/<subdomain>/...`.
- Domain and subdomain are mandatory; additional nesting is optional and should remain purposeful.
- Reuse sensible existing domain/subdomain categories before creating new ones.
- Every evidence domain has exactly one `evidence/<domain>/index.md`.
- Every newly curated evidence artifact gets exactly one compact discovery record in its domain index.
- Existing domain evidence indexes are append-only during ordinary curation.
- Do not read/rewrite an entire domain index merely to append a normal record.
- Do not create a global evidence index or subdomain indexes by default.
- Evidence index records are discovery metadata; evidence files remain authoritative.
- Do not create sidecar metadata, tag systems, per-artifact summaries, databases, or embeddings by default.
- Canonical knowledge is Markdown only.
- Search existing knowledge before creating new knowledge.
- Prefer one canonical home for each durable concept.
- Maintain `knowledge/index.md` as the map of canonical knowledge.
- Do not put individual evidence artifacts in `knowledge/index.md`.
- Knowledge pages expose meaningful current evidence provenance.
- Git commits are the durable curation ledger.
- One approved mutating operation produces one isolated KB-only commit.
- Commit bodies must be rich enough to reconstruct the semantic transaction later.
- Never silently expand an approved proposal into materially different changes.
- Never touch unrelated project files or unrelated repository work.
- Never push as part of this skill.
- Do not let the KB become a transcript archive disguised as knowledge.
- Do not preserve historical duplication that Git already preserves better.

## Final Test

A healthy KB lets a future human or agent answer without the old conversation:

```text
What is the project's documented current context?
    -> relevant docs/ + repository

What has not been processed?
    -> knowledge-base/inbox/

What source material was preserved?
    -> knowledge-base/evidence/<domain>/index.md + evidence tree

I remember an old discussion/source. Where is it?
    -> domain indexes, paths/filenames, content search, and date clues

What did the source actually say?
    -> preserved evidence artifact

What do we currently believe?
    -> knowledge-base/knowledge/

Where do I start browsing canonical knowledge?
    -> knowledge-base/knowledge/index.md

What evidence supports this knowledge?
    -> the page's ## Evidence section

Why did this knowledge change?
    -> Git curation commit

What exactly changed?
    -> Git diff/history
```

The system succeeds when:

- project context comes from canonical docs rather than a duplicated KB context file;
- evidence grows without becoming a flat dump;
- ingestion remains deterministic and cheap;
- every curated artifact has several independent retrieval signals;
- retrieval agents can use whatever search strategy is most effective;
- evidence can grow without causing knowledge to bloat;
- current understanding remains compact and navigable;
- humans approve canonical changes before they happen;
- future agents can trace important conclusions back to preserved evidence and the commits that introduced them.
