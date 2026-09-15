---
name: knowledge-base
description: Maintains a portable Git knowledge base rooted at knowledge-base/. Use to initialize it, capture material into the inbox, review or curate inbox material, organize preserved evidence, synthesize or maintain canonical knowledge, maintain the knowledge index, or trace why knowledge changed. Owns only knowledge-base/**. Curation and maintenance are proposal-gated by explicit human approval, and every mutating operation ends with one isolated knowledge-base Git commit; never push as part of this skill.
disable-model-invocation: false
---

# Knowledge Base

## Purpose and Ownership

Maintain a portable, repository-local knowledge system rooted at:

```text
knowledge-base/
├── inbox/
├── evidence/
└── knowledge/
    └── index.md
```

This skill owns **only `knowledge-base/**`**.

Never create, edit, move, delete, stage, or commit files outside that boundary. Reading outside it is not part of normal KB work; do so only when the user explicitly asks to use other repository material as source/context. Any persisted output still belongs under `knowledge-base/`.

The skill defines the behavior. `knowledge-base/` holds the state. The same contract should work in a dedicated knowledge repository or inside a larger project repository.

## Core Model

Use only three primary concepts.

### Inbox

`knowledge-base/inbox/` is the single **unprocessed entry point**.

Humans or agents may place material here without deciding its final name, category, evidence location, or knowledge impact.

Anything still in `inbox/` is **not yet curated**.

### Evidence

`knowledge-base/evidence/` contains **processed supporting material preserved for future inspection**.

Evidence may be a PDF, Markdown file, report, transcript, research note, conversation-derived artifact, image, personal write-up, or another useful source format.

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

## Authority and History

Use the repository surfaces for different questions:

```text
What do we currently believe?      -> knowledge/*.md
What currently supports it?        -> that page's ## Evidence section
Why/when did it change?            -> Git curation commit
What exactly changed?              -> Git diff/history
What did the source actually say?  -> evidence/*
```

Do not create a manually maintained global curation log, registry, SQLite database, or other competing source of truth by default.

If a generated query/index layer becomes useful later, it must be rebuildable from canonical files and Git history.

---

# Operating Modes

This skill supports five modes:

1. **Initialize** — create the minimal KB when explicitly requested.
2. **Capture** — place explicitly requested material in `inbox/` without curating it.
3. **Review / Propose** — inspect inbox material and existing KB state, then propose curation without changing files.
4. **Curate / Maintain** — after explicit approval, organize evidence, revise knowledge, update the index, verify, and commit.
5. **Trace** — explain current provenance or historical change using evidence links and Git.

Read-only review and tracing do not create commits.

**Every mutating operation must end with one isolated Git commit containing only changes from that KB operation, and the skill must not push.**

Before any mutation, confirm the host is a Git work tree and that an isolated KB-only commit can be made safely. If not, stop before writing.

---

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

Because Git does not track empty directories, minimal placeholders under `inbox/` and `evidence/` are acceptable when needed to preserve the initialized structure.

`knowledge/index.md` starts as a concise navigation page, not a process manual.

Do not create extra schemas, registries, databases, scripts, logs, archives, or workflow files without demonstrated need and human approval.

End with one isolated commit:

```text
kb(init): initialize knowledge base
```

---

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

1. Read enough of the item to understand its durable contribution.
2. Inspect `knowledge-base/knowledge/index.md`.
3. Search relevant existing knowledge before proposing a new canonical page.
4. Inspect directly relevant evidence when needed to understand provenance, overlap, or contradiction.
5. Choose a proposed final evidence path and filename.
6. Determine whether the material:
   - creates genuinely new canonical knowledge;
   - updates/refines existing knowledge;
   - both creates and updates knowledge;
   - or causes **no material knowledge change**.
7. Determine how affected knowledge provenance should change.
8. Determine required index changes.
9. Surface material ambiguity, contradiction, overlap, or structural choices.
10. Present one authoritative Curation Proposal.

Do not move, rename, edit, delete, create, stage, or commit repository files during review.

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

---

# Mandatory Curation Proposal

Before any curation or maintenance write, present a proposal that lets the human judge **what will move, what knowledge will change, what provenance will be asserted, and why**.

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
`knowledge-base/evidence/<proposed-path>`

Reason:
- [why this category fits]
- [why this filename/date is appropriate]
- [whether an existing folder is reused or a new one is justified]

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

## Index Impact

- [entries to add/change/remove]

or

- No change.

## Planned Result

- Evidence artifacts preserved: N
- Knowledge documents created: N
- Knowledge documents updated: N
- Knowledge documents merged/removed: N
- Index entries changed: N

## Human Attention

[Only genuinely consequential, debatable, uncertain, or structural points.]

## Approval

No repository changes will be made until explicitly approved.
```

The exact proposed evidence destination must always be shown. Evidence organization is agent-managed, but the human should know roughly where material will live before approving it.

A good proposal makes clear:

1. what is being processed;
2. where preserved evidence will live;
3. what current knowledge will change;
4. whether a new canonical page is justified;
5. what evidence-to-knowledge relationships will be asserted;
6. whether the index changes;
7. what deserves human judgment;
8. what the final operation will contain.

Resolve routine choices yourself. Do not hide material alternatives behind `maybe`, `possibly`, or `either`.

---

# Human Approval Boundary

Curation and maintenance are human-approved operations.

Before approval, the agent may read, search, compare, reason, trace Git history, and revise the proposal.

Before approval, it must not as part of curation or maintenance:

- move/rename inbox material;
- create/edit/delete/merge/reorganize evidence;
- create/edit/delete/merge/reorganize knowledge;
- update the knowledge index;
- stage or commit curation changes.

Explicit approval means the human unambiguously authorizes the current proposal, for example `proceed`, `approved`, or equivalent language.

If the human changes the proposal, the changed direction becomes authoritative. If the same message both specifies the change and says to proceed, do not require a redundant approval round.

After approval, execute the approved proposal. Routine mechanics are agent-owned.

If execution reveals a **materially different** knowledge change, evidence destination, merge/split, deletion, contradiction, or structural consequence that was not approved, do not silently expand the operation. Stop the unapproved part and return with a revised proposal.

---

# Evidence Organization

Evidence organization is autonomous after the proposal is approved.

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
- avoid generic names such as `notes.md`, `research.md`, `document.pdf`;
- use the artifact/source date when confidently known and representative;
- otherwise use the date it entered the KB;
- do not mass-rename historical evidence merely to enforce newer conventions without an approved maintenance proposal.

## Structure

Organize `evidence/` for intuitive human browsing.

Prefer:

- existing sensible categories over new folders;
- shallow hierarchies;
- broad stable domains over one-folder-per-concept;
- names a human would naturally browse/search;
- local reorganization only when it improves the directly affected area.

Normally avoid more than two semantic directory levels below `evidence/` unless the existing KB clearly benefits from deeper structure.

Do not reorganize unrelated evidence during ordinary curation.

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

---

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

It is the maintained human-and-agent map of canonical knowledge, not a raw filename dump.

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

Update the index in the same approved operation whenever a knowledge document is created, renamed, moved, merged, deleted, or materially rescoped.

Do not index individual evidence artifacts.

The index should support progressive discovery: broad topic -> canonical page -> underlying evidence when needed.

---

# Apply an Approved Curation

After explicit approval:

1. Re-check repository status before writing.
2. Confirm approved targets have not materially changed since review.
3. Move/rename inbox material into the approved evidence location while preserving source content.
4. Create or rewrite approved knowledge pages.
5. Update affected `## Evidence` sections to express approved provenance relationships.
6. Repair directly affected knowledge links.
7. Update `knowledge/index.md` when required.
8. Ensure successfully curated items no longer remain in `inbox/` as pending copies.
9. Review the diff for scope, correctness, and accidental bloat.
10. Run the verification contract below.
11. Stage only approved `knowledge-base/**` changes from this operation.
12. Create one isolated commit using the required commit contract.
13. Verify the commit matches the approved proposal and unrelated work remains untouched.
14. Report the commit identifier and concise result. Do not push.

If final inspection shows that an approved semantic change is no longer justified, do not silently substitute another. Return to proposal/discussion when the difference is material.

---

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
- moved to knowledge-base/evidence/<final-path>

Knowledge:
- updated knowledge-base/knowledge/<page>.md
  - <durable conclusion added, changed, limited, or removed>
  - <provenance relationship added/changed>

- created knowledge-base/knowledge/<page>.md
  - <canonical scope introduced>

Index:
- <entries changed>

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

Always include the original inbox path and final evidence path so the artifact remains searchable after it moves.

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

Knowledge:
- <merged/split/rewritten/moved pages and semantic reason>

Index:
- <changes>

Outcome:
- knowledge-restructured

Rationale:
- <why this reduces duplication, drift, or navigation cost>

Approval:
- explicit human approval obtained before maintenance
```

The Git diff is stronger authority than commit prose if they ever disagree.

---

# Traceability

When asked why knowledge says something, move from current provenance toward deeper history only as needed.

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
                                  ├── evidence placement
                                  ├── other knowledge affected
                                  └── exact diff
```

Do not invent missing provenance. If repository evidence cannot establish why a claim exists, say so.

## Cross-KB Questions

To find which knowledge pages use an evidence artifact, search knowledge Markdown for links to its path.

To find which curation introduced an artifact or changed a page, search Git commit bodies and path history.

Do not add a database merely because a relational question is possible. Add a derived query layer only after recurring evidence shows that file search plus Git is insufficient.

---

# Maintenance and Autonomous Organization

The agent is responsible for keeping the KB navigable and compact, but all mutating maintenance remains proposal-gated.

Maintenance may identify:

- duplicate/overlapping knowledge pages;
- incoherent page scope;
- stale current conclusions;
- broken evidence links;
- canonical pages missing from the index;
- stale index descriptions;
- inconsistent evidence naming;
- poor evidence placement;
- unnecessary directory proliferation;
- orphaned knowledge pages;
- Evidence sections that no longer reflect current support;
- multiple canonical homes for the same durable concept.

Prefer the smallest coherent correction:

```text
duplicate knowledge   -> merge into one canonical page
oversized mixed scope -> split only when scopes are genuinely distinct
stale conclusion      -> rewrite current knowledge
bad evidence location -> move/rename and repair links
broken index          -> repair in the same change
```

Do not preserve obsolete structure merely because it existed historically; Git preserves history.

Do not reorganize the whole KB during ordinary curation. Broader reorganization requires its own maintenance proposal with affected paths, moves, knowledge consequences, provenance effects, and index impact.

---

# Verification Contract

Before every mutating commit, verify:

## Boundary

- every changed/staged path is under `knowledge-base/`;
- no unrelated repository work is included;
- no unrelated pre-existing KB work is included.

## Inbox

- every processed item in scope has left `inbox/`;
- no unapproved inbox item was altered;
- no partially curated state remains.

## Evidence

- final paths match the approved proposal;
- new filenames follow the convention;
- source format is preserved unless conversion was explicitly approved;
- substantive source content was not silently rewritten;
- moves/renames have not broken directly affected links.

## Knowledge

- created/updated canonical files are Markdown;
- required frontmatter is present and accurate;
- each page has one coherent scope;
- existing knowledge was improved rather than duplicated where appropriate;
- stale superseded wording was removed rather than layered underneath;
- material uncertainty remains honest;
- `## Evidence` links resolve and explain why each artifact matters;
- limiting/contradictory evidence remains visible when relevant.

## Index

- every canonical knowledge page is reachable from `knowledge/index.md`;
- created/moved/merged/rescoped pages are represented correctly;
- descriptions match current scope;
- removed pages leave no stale index links.

## Git Record

- staged diff matches the approved operation;
- commit body names original inbox and final evidence paths for curation;
- semantic knowledge changes are described, not just filenames;
- rationale explains material decisions and evidence-only outcomes;
- approval is recorded when required;
- one isolated KB-only commit succeeds;
- the final commit contains no path outside `knowledge-base/`.

After commit, report the commit identifier and concise summary. Do not push.

---

# Non-Negotiables

- This skill owns only `knowledge-base/**`.
- `inbox/` is the single unprocessed entry point.
- Capture does not imply curation.
- Curation and maintenance require explicit human approval before writes.
- Evidence organization and knowledge synthesis happen in one approved curation operation.
- An inbox item leaves `inbox/` only when its curation is complete.
- Evidence is preserved; knowledge is revised.
- Preserve original evidence formats by default.
- Canonical knowledge is Markdown only.
- Search existing knowledge before creating new knowledge.
- Prefer one canonical home for each durable concept.
- Maintain `knowledge/index.md` as the map of canonical knowledge.
- Knowledge pages expose meaningful current evidence provenance.
- Do not create a manual global curation log, registry, or database by default.
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
What has not been processed?
    -> knowledge-base/inbox/

What source material was preserved?
    -> knowledge-base/evidence/

What do we currently believe?
    -> knowledge-base/knowledge/

Where do I start browsing?
    -> knowledge-base/knowledge/index.md

What evidence supports this knowledge?
    -> the page's ## Evidence section

Why did this knowledge change?
    -> Git curation commit

What exactly changed?
    -> Git diff/history
```

The system succeeds when evidence can grow without causing knowledge to bloat, current understanding remains compact and navigable, humans approve canonical changes before they happen, and future agents can trace important conclusions back to preserved evidence and the commits that introduced them.
