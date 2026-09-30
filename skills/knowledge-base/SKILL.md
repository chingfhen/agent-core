---
name: knowledge-base
description: Maintains a portable human-readable Markdown knowledge base on a configured storage backend. Captures conversation-derived evidence into review-ready Markdown, prepares raw sources, supports explicit human approval, curates approved evidence into durable evidence and current knowledge, retrieves progressively, and maintains structure with low-friction verification. Storage mechanics are delegated to the selected backend adapter.
disable-model-invocation: false
---

# Knowledge Base

## Purpose

Maintain a durable, readable, retrieval-friendly knowledge base under one explicitly configured root.

The primary permanent product is:

```text
evidence/
knowledge/
```

Everything else exists to safely turn conversations and source material into those two useful surfaces.

The system should produce:

- faithful, readable Markdown evidence;
- practical current knowledge for human reading;
- predictable organization;
- cheap retrieval for future agents;
- clear provenance from knowledge to evidence and, when needed, to original sources;
- a structure that remains understandable when browsed directly with ordinary storage tools.

Core invariant:

> **Evidence may accumulate. Knowledge must consolidate.**

Useful distinction:

> **Evidence tells you what was recorded. Knowledge tells you what is useful to understand now.**

---

# Runtime Configuration

This skill is canonical and storage-agnostic. Do not hardcode one workspace's knowledge-base root into this file.

## Project Registry Resolution

On a local machine, use the machine-local project registry when available:

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

For this skill, `root` identifies the active project and `knowledge_base` identifies the exact KB root.

When `~/.agent-core/projects.toml` is available:

1. Identify the project whose configured `root` contains the current working directory.
2. If more than one configured root matches, use the most specific matching root.
3. If that project defines `knowledge_base`, use that exact value as the active KB root.
4. Do not substitute another nearby `knowledge-base/` directory merely because one exists.
5. If the active project is registered but does not define `knowledge_base`, treat the project as having no configured KB and do not invent one. An explicit human-selected KB for the current operation may still be used.
6. Normal KB operations read the project registry but do not modify it. Modify the registry only when the human explicitly asks to register, remove, or change a project.

The `knowledge_base` value may be any root representation supported by this skill, including a local filesystem path or a supported external backend root such as a Google Drive folder URL.

## Other Runtime Configuration

When no applicable machine-local project registry is available, resolve the active knowledge base from an explicit human instruction, the calling project instructions, `AGENTS.md`, equivalent agent configuration, or an explicitly configured backend-supported KB registry.

An explicit human instruction selecting a KB for the current operation takes precedence over ambient configuration.

Recommended explicit configuration:

```text
Knowledge Base Backend: filesystem | google-drive
Knowledge Base Root: <exact local path, Drive folder URL, or Drive folder ID>
Knowledge Base Name: <optional human-readable name>
Knowledge Base Registry: <optional backend-supported registry location>
```

`Knowledge Base Root` is mandatory for mutation and ordinary KB retrieval unless the active root has already been resolved unambiguously from the machine-local project registry or other explicit current context.

The backend may be inferred when the root representation makes it unambiguous:

- local filesystem path -> `filesystem`;
- Google Drive folder URL or ID in a Drive-configured project -> `google-drive`.

Prefer an explicitly configured backend when available.

Do not assume Git or any other version-control system. Git behavior is outside this canonical workflow unless the human explicitly introduces a separate Git-specific extension. Git repository boundaries do not determine the KB root.

## Root Naming Convention

When the environment permits it, prefer a descriptive root name ending in:

```text
<name>-knowledge-base
```

Examples:

```text
ocbc-knowledge-base
personal-finance-knowledge-base
adreadyclips-knowledge-base
```

This is a discovery convention, not an identity or validity requirement. The configured root remains authoritative.

---

# Backend Adapters

Storage semantics live in this file. Storage mechanics live in backend adapters.

Supported adapters:

```text
backends/filesystem.md
backends/google-drive.md
```

Before performing backend-specific reads or mutations, read the adapter matching the active backend unless its rules are already present in current context.

The adapter may define:

- root resolution and identity;
- safe read/write/move/delete primitives;
- search behavior;
- backend-specific version history;
- raw Markdown integrity requirements;
- backend-specific verification;
- optional discovery registries.

The adapter must not redefine the semantic meaning of `raw`, `review`, `approved`, `evidence`, or `knowledge`.

If the configured backend has no available adapter or the required storage operations cannot be performed safely, stop rather than improvising incompatible persistence semantics.

---

# Ownership and Boundary

The active KB root and its descendants are the complete normal namespace owned by this workflow.

When the root comes from `~/.agent-core/projects.toml`, the configured `knowledge_base` value is authoritative for that project. Do not infer a different KB from the current Git repository, sibling folders, parent folders, or nearby directories with similar names.

The skill may read explicitly authorized external source/context material when the human or project configuration supplies it, but this does not expand KB write ownership.

Do not create, edit, move, rename, delete, reorganize, or index KB content outside the active root.

Do not search unrelated storage locations merely because they may contain useful context.

Do not treat workflow files, adapters, registries, or agent configuration as substantive evidence or canonical knowledge.

---

# Knowledge Base Structure

Use:

```text
<root>/
├── inbox/
│   ├── raw/
│   ├── review/
│   └── approved/
├── source-archive/
├── evidence/
│   ├── index.md
│   └── <domain>/
│       ├── index.md
│       └── <subdomain>/
│           └── [<optional-deeper-path>/]
│               └── YYYY-MM-DD--description.md
└── knowledge/
    ├── index.md
    └── [concept-oriented folders and Markdown pages]
```

Workflow states:

```text
inbox/raw/       = genuine raw source material awaiting evidence preparation
inbox/review/    = authored Markdown evidence awaiting human approval
inbox/approved/  = human-approved Markdown evidence awaiting automated curation
source-archive/  = original source material whose approved evidence has been curated
evidence/        = permanent approved historical grounding
knowledge/       = practical current synthesized understanding
```

A file's location is part of the workflow contract.

---

# Core Model

## Raw Sources

`inbox/raw/` is for source material that still needs selection and authoring.

Examples:

- PDFs;
- screenshots and images;
- exported emails or messages;
- copied articles or reports;
- transcripts;
- rough notes;
- source files supplied substantially as-is.

Raw material is not approved evidence and must not become canonical knowledge directly.

## Review Evidence

`inbox/review/` contains complete, readable Markdown evidence awaiting human approval.

Presence here means:

> The evidence has been selected and authored, but the human has not yet approved its substantive contents.

## Approved Evidence

`inbox/approved/` contains Markdown whose substantive contents the human has approved as a faithful evidence record.

Presence here means:

> This evidence is approved and ready for permanent curation.

## Source Archive

`source-archive/` preserves original source material after its corresponding evidence has been approved and curated.

It is a provenance layer, not a second evidence system and not the normal retrieval starting point.

## Evidence

`evidence/` contains permanent human-approved Markdown grounding.

Evidence may include:

- factual records;
- observations;
- decisions;
- research findings;
- source claims;
- useful uncertainty;
- contradictory material;
- historical understanding.

Evidence is preserved history, not automatically current truth.

## Knowledge

`knowledge/` contains practical current understanding.

Knowledge is:

- Markdown only;
- concept-oriented rather than source-oriented;
- current rather than chronological;
- substantially more compact than evidence;
- written for fast human reading;
- rewritten as understanding improves;
- traceable to relevant evidence.

Knowledge answers:

> **What is useful to understand now?**

---

# Canonical Workflow Cues

Use distinct verbs for distinct workflow stages.

```text
conversation
    ↓ capture
review/

raw/
    ↓ prepare
review/

review/
    ↓ approve
approved/

approved/
    ↓ curate
evidence/ + knowledge/
```

## `capture this`

Use information already developed in the current conversation as the source.

Perform evidence selection and author clean Markdown directly into:

```text
inbox/review/
```

Natural equivalents include:

```text
capture this to the KB
save this as evidence
create evidence from this
record this in the KB
```

## `prepare raw inbox`

Operate on in-scope material in:

```text
inbox/raw/
```

Perform evidence selection and author clean Markdown into:

```text
inbox/review/
```

Leave raw sources in place until the resulting evidence has been approved and curated.

## `review pending evidence`

Inspect or list:

```text
inbox/review/
```

This cue does not approve, move, or curate anything.

## `approve <item>`

Move the specified artifact unchanged from:

```text
inbox/review/
```

to:

```text
inbox/approved/
```

The move is the approval signal.

## `approve all`

Move all in-scope review artifacts unchanged into:

```text
inbox/approved/
```

## `curate approved inbox`

Operate on:

```text
inbox/approved/
```

Place approved evidence permanently, maintain indexes, update knowledge when useful, reconcile raw sources, and complete routine curation automatically.

Natural equivalents include:

```text
curate the approved evidence
process approved evidence
process the approved inbox
curate approved
```

Generic phrases such as `process the inbox` or `handle the inbox` have no canonical meaning. Resolve them from clear immediate context when possible; otherwise ask which workflow stage is intended.

---

# Initialize

Initialize only when explicitly requested.

Create:

```text
<root>/
├── inbox/
│   ├── raw/
│   ├── review/
│   └── approved/
├── source-archive/
├── evidence/
│   └── index.md
└── knowledge/
    └── index.md
```

Do not invent evidence domains or subdomains during initialization.

`evidence/index.md` and `knowledge/index.md` should begin as concise navigation pages.

---

# Capture

Capture should place information into the furthest justified workflow state without skipping human approval.

Use two intake paths:

```text
genuine raw source
    → inbox/raw/
    → prepare raw inbox
    → inbox/review/

conversation or agent-authored capture
    → evidence selection + Markdown authoring
    → inbox/review/
```

## Capture from the Current Conversation

When the human asks to capture information already developed in the current conversation:

1. identify the intended scope;
2. perform evidence selection;
3. write the selected material as clean, self-contained Markdown;
4. preserve important facts, decisions, conclusions, constraints, assumptions, uncertainty, useful reasoning outcomes, and relevant provenance;
5. write the artifact directly to `inbox/review/`;
6. verify the write with the cheapest useful confirmation;
7. report concisely what was created.

The current conversation acts as the source. A separate raw transcript is not required.

Use work already completed in the conversation. If research, comparison, synthesis, or structuring has already been performed, carry those durable results forward into the evidence artifact.

Do not deliberately reduce already-processed information into an unstructured raw note.

## Raw Capture

Use `inbox/raw/` when the supplied material is itself a source that still needs preparation.

For raw capture:

1. preserve the supplied representation and substantive content;
2. place it in `inbox/raw/`;
3. use a collision-safe filename;
4. retain available source date and provenance;
5. verify the write with the cheapest useful confirmation.

Raw capture does not require evidence selection or evidence authoring at capture time.

---

# Preparing the Raw Inbox

`prepare raw inbox` operates only on in-scope items in `inbox/raw/`.

For each raw source:

1. determine whether the source can be read faithfully;
2. identify source date, context, provenance, and uncertainty when available;
3. check whether the source is already represented in `review/`, `approved/`, or curated evidence;
4. perform evidence selection: `0 / 1 / N`;
5. author each selected artifact as clean, self-contained Markdown;
6. write the artifacts to `inbox/review/`;
7. leave the raw source in `inbox/raw/` until its resulting evidence has been approved and curated;
8. report the prepared artifacts concisely.

Do not repeatedly prepare the same raw source merely because it remains in `raw/` awaiting later workflow steps.

Use provenance fields to associate review evidence with its raw source when useful.

---

# Reading Binary, Image, and Difficult Sources

Use document-reading, visual-reading, parsing, or extraction capabilities available in the current runtime when needed.

For PDFs, images, scans, spreadsheets, exported messages, or other non-clean-text sources:

- preserve the original in `raw/` until approved evidence has been curated;
- extract or inspect only what can be represented faithfully;
- preserve natural headings, lists, tables, reading order, and document structure when useful;
- remove obvious extraction-only line wrapping and repeated page furniture;
- preserve material uncertainty in names, dates, identifiers, amounts, clauses, and table values;
- distinguish machine-derived text from human verification when that distinction matters.

If the source cannot be read reliably enough to author evidence, leave it in `raw/` and report the limitation.

Do not send source material to an external service without explicit permission.

---

# Evidence Selection

Evidence selection happens before evidence authoring.

The workflow owns:

```text
source -> 0 / 1 / N evidence artifacts
```

Preserve material when it has plausible future value as:

- factual reference;
- a decision or decision context;
- a durable observation;
- useful research;
- an event or conversation record;
- a meaningful idea;
- a constraint or assumption that affects future work;
- supporting or limiting evidence for current knowledge;
- provenance for a future conclusion.

Favor durable signal over conversational completeness.

Default to one artifact when material shares one coherent source or context.

Split only when distinct subjects are genuinely likely to be retrieved independently later.

Keep this distinction explicit:

```text
selection = decide what durable material becomes an artifact
authoring = faithfully represent the selected scope
```

Selection may exclude irrelevant or non-durable source material.

Once a scope is selected, preserve the substantive information needed to represent that scope faithfully.

A raw source may legitimately produce zero evidence artifacts. In that case, leave the source in `raw/`, report the proposed `0 evidence` outcome, and do not archive or delete it without human acceptance of that disposition.

---

# Evidence Authoring

Evidence authoring turns selected material into a durable record that remains useful after the original conversation or source is forgotten.

The objective is not to reproduce the source. It is to preserve the **durable substance of the selected scope faithfully and clearly**.

A good evidence artifact should let a future reader answer:

- What was learned, observed, decided, or established?
- What details materially support that understanding?
- What conditions, exceptions, assumptions, or uncertainty matter?
- Where did the information come from?
- What would be lost if the original source were unavailable?

## Authoring from Conversation or Agent Research

When the agent has already discussed, researched, compared, reasoned about, or structured the subject with the human, use that completed work when writing the evidence.

Capture the durable outcome rather than the conversational sequence.

Preserve, when materially useful:

- key facts and findings;
- decisions and preferences;
- conclusions reached;
- comparison outcomes;
- important reasoning behind a conclusion;
- conditions and exceptions;
- assumptions that affect the result;
- uncertainty or unresolved questions;
- dates, amounts, thresholds, names, or other details needed for future use;
- source references used for researched claims.

The artifact should stand on its own without requiring the future reader to reconstruct the chat.

## Information Selection Within an Artifact

Give highest priority to information with future decision or retrieval value:

```text
conclusion / decision
        ↓
important supporting facts
        ↓
conditions and exceptions
        ↓
reasoning that explains non-obvious conclusions
        ↓
uncertainty and unresolved questions
        ↓
useful provenance
```

Compression should remove conversational overhead, not useful substance.

## Structure

Choose structure from the information rather than applying one fixed template.

Useful patterns include:

```markdown
# Descriptive Title

Recorded: YYYY-MM-DD
Source: conversation

## Decision
...

## Basis
- ...

## Conditions / Exceptions
- ...
```

or:

```markdown
# Descriptive Title

Recorded: YYYY-MM-DD
Source: research discussion

## Findings
...

## Practical Takeaways
- ...

## Caveats
- ...

## Sources
- ...
```

Use only sections that materially improve the record.

## Provenance

Useful provenance fields include:

```markdown
Recorded: YYYY-MM-DD
Source: [conversation, owner notes, email, report, extracted document, etc.]
Source date: [when materially useful]
Source file: [conceptual KB path when one exists]
Verification: [awaiting human approval / human-approved / owner-recorded / machine-extracted, as applicable]
```

Additional provenance may include `Derived from`, `Effective as of`, `Participants`, or `Extraction status` when useful.

Use metadata proportionately. The body remains the primary record.

## Rough Owner Notes

Owner-written rough notes may be normalized aggressively when meaning is clear.

Allowed cleanup includes spelling, grammar, punctuation, ordering, duplicate removal, obvious abbreviation expansion, grouping related statements, and converting fragments into clear sentences, bullets, tables, or sections.

Preserve substantive meaning, meaningful uncertainty, important distinctions, source status, and unresolved ambiguity.

## Fidelity Rules

Preserve fidelity.

Do not invent missing facts, silently resolve meaningful ambiguity, silently resolve contradictions, turn recollections into transcripts, turn proposals into decisions, turn ideas into established facts, present generated paraphrase as quotation, or claim source-level verification that did not occur.

Preserve quotations exactly when quotation matters.

If sources conflict, preserve the conflict rather than choosing one silently.

---

# Review

`inbox/review/` contains authored Markdown evidence awaiting human approval.

A review artifact should already be a complete, readable, self-contained evidence record.

When the agent creates or revises review evidence:

1. write the complete Markdown artifact to `inbox/review/`;
2. verify the write with the cheapest useful confirmation;
3. tell the human concisely what was created or changed.

Do not reproduce the full Markdown in chat by default unless the human asks to review it there.

The human may inspect, edit, revise, split, merge, expand, reduce, approve, or reject review artifacts.

---

# Approval

Approval means that the human accepts the current substantive contents of a review artifact as a faithful evidence record.

The transition is:

```text
inbox/review/
      ↓
inbox/approved/
```

Moving a file into `inbox/approved/` is itself the approval signal.

Approval does not rewrite the artifact.

## Human-Performed Approval

The human may move accepted files directly from `review/` to `approved/` using ordinary storage tools. No additional agent action is required for the evidence to become approved.

## Agent-Performed Approval

When the human asks the agent to approve an artifact:

1. identify the intended review artifact;
2. move it unchanged from `inbox/review/` to `inbox/approved/`;
3. confirm the move with the cheapest useful check;
4. report the completed transition.

If an artifact needs substantive changes, revise it while it remains in `review/` and obtain approval of the revised version afterward.

Associated raw sources remain in `raw/` until approved evidence is successfully curated.

---

# Curating the Approved Inbox

`curate approved inbox` performs the full routine curation of human-approved evidence in:

```text
inbox/approved/
```

Human approval of evidence content is the substantive quality gate.

Once an artifact is in `approved/`, the agent should determine permanent placement, maintain indexes, update canonical knowledge when appropriate, reconcile raw sources, and complete routine curation **without requiring another approval round**.

Resolve routine curation decisions autonomously and report the result afterward.

Ask only when execution reveals a genuinely material ambiguity that cannot be resolved faithfully, such as uncertain evidence identity, destructive conflict, or a major structural choice with multiple materially different outcomes.

## Curation Context

Before placing approved evidence, establish the current structure of both permanent KB surfaces.

Read first when relevant structure is not already known:

```text
evidence/index.md
knowledge/index.md
```

Use them to determine:

- which existing evidence domain is the best fit;
- whether a new evidence domain is genuinely needed;
- which existing knowledge page owns the concept;
- whether the approved evidence introduces a genuinely new knowledge scope.

Then read only relevant deeper material:

```text
evidence/<domain>/index.md
relevant knowledge page(s)
relevant existing evidence when needed
```

Read existing evidence only when necessary to resolve overlap, duplication, contradiction, historical context, provenance, or uncertainty about knowledge impact.

Do not scan the entire KB by default.

## Curation Outcomes

An approved artifact may result in:

```text
evidence only
evidence + existing knowledge update
evidence + new knowledge page
evidence + several closely related knowledge updates
```

A knowledge change is not required merely because new evidence exists.

## Curation Steps

For each approved artifact:

1. determine the most appropriate existing evidence domain and subdomain;
2. create new structure only when existing structure would materially misrepresent the subject;
3. move the artifact into its permanent evidence location;
4. preserve its approved Markdown contents unchanged except for mechanical filename/provenance adjustments required by final placement;
5. maintain the evidence indexes;
6. determine and apply useful knowledge changes;
7. archive any associated raw source after successful curation;
8. perform proportionate final-state verification;
9. report the outcome concisely.

Successfully curated artifacts should no longer remain in `inbox/approved/`.

---

# Evidence Organization

`evidence/` contains permanent human-approved records.

Evidence is organized for:

1. predictable subject-based browsing;
2. chronological reading within a subject;
3. efficient retrieval by future agents;
4. preservation of approved contents.

Use:

```text
evidence/
├── index.md
└── <domain>/
    ├── index.md
    └── <subdomain>/
        └── [<optional-deeper-path>/]
            └── YYYY-MM-DD--description.md
```

## Placement

Every curated evidence artifact has one clear primary location.

Before placing evidence:

1. read `evidence/index.md` when the likely domain is not already known;
2. identify the most likely existing domain;
3. read that domain's `index.md`;
4. reuse an existing suitable subdomain when possible;
5. create new structure only when existing structure would make the evidence difficult or misleading to find.

Placement should reflect the **main subject a future reader would look under**, not every topic mentioned in the artifact.

Do not duplicate one evidence artifact into multiple folders merely for discovery.

## Domains and Subdomains

Domains are broad, durable areas of the knowledge base. Prefer reusing established domains.

Create a new domain only when the material represents a durable area not coherently covered by an existing domain and future evidence is plausibly likely to belong there.

Subdomains provide practical subject grouping within a domain. Use literal names a human would naturally browse.

Subdomains should be broad enough to accumulate related evidence over time but specific enough that their chronological file list remains meaningful.

Avoid catch-all names such as `misc`, `other`, or `general` when a clearer subject exists.

Additional nesting below the subdomain is optional and should arise from repeated organizational need rather than advance ontology design.

## Evidence Filenames

Use:

```text
YYYY-MM-DD--lowercase-kebab-case.md
```

The date prefix is deliberate. Within a subject folder, filenames should naturally form a chronological record.

Use the source or event date when known and representative; otherwise use the date the evidence entered the KB.

Choose descriptive terms a future human is likely to remember.

Avoid unnecessary PII in filenames.

## Evidence Preservation

Permanent evidence is an approved historical record.

Routine curation and maintenance may move or rename evidence and repair mechanical links or provenance paths, but substantive Markdown contents remain preserved.

If a genuine capture error or material misrepresentation is discovered, handle it as an explicit evidence correction rather than silently rewriting history.

---

# Evidence Index

Maintain:

```text
evidence/index.md
```

as the high-level map of the evidence base.

Its purpose is to answer:

> Which evidence domain should I inspect?

List each domain once with:

- a human-readable name;
- a link to its domain index;
- a concise description of what belongs there.

Example:

```markdown
# Evidence

- [Finance](finance/index.md) — Banking, payment cards, investments, insurance, personal financial planning, and related research.
- [Career](career/index.md) — Employment, compensation, workplaces, career decisions, professional development, and work-related records.
```

Keep this index compact. Do not list individual evidence artifacts here.

Update it only when a domain is created, renamed, merged, removed, or materially rescoped.

---

# Evidence Domain Indexes

Every evidence domain maintains:

```text
evidence/<domain>/index.md
```

The domain index is the discovery surface for all evidence beneath that domain.

Every curated evidence artifact receives exactly one domain-index record.

Use one concise Markdown line:

```markdown
- YYYY-MM-DD | `<subdomain[/deeper-path]>` | [<Title>](<relative-path>) | <retrieval description>
```

Descriptions should help a human or agent decide whether opening the artifact is worthwhile.

Include central subject, distinctive names or terms, major categories covered, and useful decision or research context.

Do not reproduce the artifact summary or add unsupported conclusions.

During ordinary curation, preserve unrelated existing index content. Use the backend's cheapest safe update mechanism; do not rewrite unrelated records merely to add one entry.

---

# Knowledge Admission

`knowledge/` contains practical current understanding for human and agent use.

Its purpose is to reduce the need to repeatedly read many evidence artifacts.

Ask:

> Would preserving this understanding save meaningful future reading, reconstruction, or decision effort?

Good knowledge candidates include:

- current strategies;
- durable preferences;
- recurring rules;
- useful comparisons;
- important constraints;
- current plans;
- stable relationships between facts;
- conclusions supported across evidence;
- reusable decision frameworks;
- practical guidance derived from accumulated evidence.

Keep information only in evidence when it is primarily historical detail, source-specific wording, a one-off event, low-value chronology, supporting detail unlikely to matter independently, superseded understanding useful only as history, or material already easy to retrieve from evidence when needed.

A useful test:

```text
Would I reasonably want to open a knowledge page for this later?

Yes → consider knowledge
No  → evidence may be sufficient
```

---

# Canonical Knowledge Ownership

Each durable concept should have one primary canonical home.

Before creating a knowledge page:

1. read `knowledge/index.md` unless the relevant canonical page is already known;
2. identify the most likely existing page;
3. read that page;
4. update it when the new understanding fits its scope coherently;
5. create a new page only when the concept deserves an independently useful reading surface.

Prefer improving an existing page over creating another related page.

A new page is justified when:

- the subject is likely to be searched or browsed independently;
- it has enough durable substance to be useful on its own;
- placing it elsewhere would make another page confusing or overly broad;
- it represents a distinct practical concept rather than merely a new source or event.

Do not create pages according to conversation boundaries, evidence filenames, dates, or source documents.

---

# Knowledge Filenames

Knowledge filenames describe durable concepts.

Use stable lowercase kebab-case names without date prefixes.

Examples:

```text
credit-card-payment-strategy.md
investment-strategy.md
housing-strategy.md
career-development.md
```

Choose filenames that help a human predict:

> “This is probably the page I want to read.”

Prefer familiar, literal terms over abstract taxonomy.

Do not use dates, temporary states, source names, or suffixes such as `v2`, `new`, or `latest` for ordinary canonical knowledge.

---

# Knowledge Synthesis

Knowledge answers:

> **What is useful to understand now?**

Synthesize across relevant approved evidence rather than summarizing each evidence artifact separately.

The agent should:

1. identify the current useful conclusions;
2. combine compatible evidence;
3. remove duplication;
4. replace stale understanding;
5. preserve important conditions and exceptions;
6. preserve uncertainty when it still matters;
7. keep only reasoning necessary to understand or apply the conclusion;
8. link back to evidence when deeper detail, chronology, or source verification may be useful.

Knowledge should favor practical understanding over historical completeness.

## Updating Existing Knowledge

Prefer:

```text
old understanding
        +
new evidence
        ↓
rewritten current understanding
```

rather than stacking dated updates.

Remove or rewrite statements that are no longer current.

Keep historical context in knowledge only when that history materially helps explain the current situation.

## Level of Detail

Include details when they materially affect a decision, action, interpretation, important exception, comparison, future planning, or understanding of why a conclusion matters.

Leave deeper source detail in evidence.

Useful division:

```text
knowledge
→ conclusions
→ practical rules
→ current plans
→ important conditions
→ essential rationale

evidence
→ chronological records
→ source-specific details
→ supporting facts
→ research depth
→ historical versions
→ provenance
```

## Reasoning in Knowledge

Preserve reasoning when it materially improves future judgment, such as why one option is preferred, why an exception exists, what trade-off drives a decision, or what assumption a strategy depends on.

Compress procedural or reconstructable reasoning.

Do not preserve long exploratory chains or abandoned alternatives unless they remain useful to future decisions.

## New Evidence That Does Not Change Knowledge

New evidence may simply reinforce what is already known.

When the canonical page already expresses the useful current understanding accurately, leave the prose unchanged. Add or refresh the evidence relationship only when useful.

## Conflicting Evidence

When approved evidence conflicts:

1. determine whether one record clearly supersedes another;
2. update current knowledge when newer or stronger evidence resolves the issue;
3. preserve material unresolved conflict when it remains genuinely unresolved;
4. keep the underlying records in evidence regardless.

Do not turn disagreement into false certainty.

## Knowledge Page Scope

Each knowledge page should have one coherent practical scope.

A page is too broad when unrelated subjects accumulate, readers cannot predict what belongs there, or sections are independently useful and commonly retrieved separately.

A page is too narrow when it contains only one minor fact or one evidence artifact and naturally belongs inside another page.

Prefer one useful medium-sized canonical page over many tiny pages.

---

# Knowledge Markdown Contract

Every canonical knowledge page except `knowledge/index.md` uses minimal frontmatter:

```markdown
---
title: [Knowledge Title]
description: [One sentence defining what useful understanding belongs on this page.]
updated: YYYY-MM-DD
---
```

Required fields are exactly:

```text
title
description
updated
```

Keep metadata minimal.

Change `updated` only when durable meaning changes.

## Default Page Shape

Use this when it fits:

```markdown
---
title: [Title]
description: [Canonical scope.]
updated: YYYY-MM-DD
---

# Title

## Read First

- Highest-value current conclusion.
- Important practical rule, constraint, or exception.

## [Topic-specific sections]

Current useful understanding.

## Evidence

- [Evidence title](relative/path)
  - What this evidence materially supports or clarifies.
```

This is a default, not a mandatory template.

## Read First

`## Read First` is the fast-reading surface.

It should contain the smallest set of points that gives the reader a useful mental model of the page.

Prefer current conclusions, practical rules, important preferences or decisions, major constraints, and consequential exceptions.

Keep it short and avoid duplicating the entire page.

## Body Structure

Choose headings based on the subject.

Prefer headings such as:

```text
Current Strategy
Payment Routing
Important Exceptions
Housing Options
Decision Criteria
Current Plan
Trade-offs
What to Watch
```

Avoid generic headings such as `Background`, `Overview`, `Details`, `Miscellaneous`, or `Additional Notes` unless they genuinely describe the content well.

Organize the page around how a future reader is likely to use the information.

## Knowledge Writing Quality

Write for fast human reading first and reliable agent retrieval second.

Prefer:

- direct, literal language;
- the useful conclusion before supporting explanation;
- short paragraphs;
- bullets for rules, preferences, conditions, and parallel facts;
- tables when comparisons or structured choices are materially easier to scan;
- explicit numbers, dates, thresholds, and conditions when they affect decisions;
- concise reasoning when it explains a non-obvious conclusion;
- clear distinction between confirmed understanding and uncertainty.

Compress repeated facts, source-by-source narration, obsolete chronology, exploratory reasoning, and redundant explanations.

Preserve current conclusions, material rationale, important conditions, uncertainty, trade-offs, reusable rules, and details that change what the reader should do or understand.

## Evidence Section

Include `## Evidence` when the page contains understanding derived from KB evidence.

The purpose is traceability, not citation density.

List evidence that materially supports, qualifies, or contradicts the current page. Explain briefly why each item matters.

Do not list every evidence artifact that merely mentions the topic.

Use `### Supporting` and `### Limiting or Contradictory` only when those distinctions materially help.

## Current Understanding, Not Change Log

Canonical knowledge pages describe the current useful state.

Prefer rewriting the relevant section when understanding changes.

Avoid accumulating `Update`, `Latest Update`, `Revision`, or date-stamped appendices unless the history itself is useful to the concept.

Evidence already preserves chronology.

Knowledge should remain readable as though it had been written correctly in its current form from the beginning.

---

# Knowledge Index

Maintain:

```text
knowledge/index.md
```

as the primary navigation map for canonical knowledge.

Its purpose is to help a human or agent quickly identify which knowledge page is likely to contain the useful current understanding they need.

The index should answer:

> Which page should I open?

It should not attempt to answer the underlying subject itself.

Group knowledge pages under intuitive topical headings when that improves browsing.

Example:

```markdown
# Knowledge

## Finance

- [Credit Card Payment Strategy](finance/credit-card-payment-strategy.md) — Current routing between cards for local, overseas, recurring, excluded, and special payment categories.
- [Investment Strategy](finance/investment-strategy.md) — Portfolio structure, allocation principles, DCA approach, and current investment preferences.
```

Use the smallest hierarchy that keeps navigation clear.

Every canonical knowledge page should have exactly one primary entry in `knowledge/index.md`.

Each entry contains page title, relative link, and a short scope description.

Describe page scope, not page contents.

Update the index automatically when curation changes canonical knowledge structure: creation, rename/move, material rescope, merge, removal, or meaningful topical regrouping.

Do not change the index merely because an existing page's contents changed while its scope remained the same.

Do not list evidence, inbox artifacts, source archive files, workflow files, or backend adapters in `knowledge/index.md`.

---

# Retrieval

Retrieval should be question-driven, progressive, and economical.

Use indexes and structure to narrow before opening detailed files.

Do not scan the entire knowledge base when a small number of targeted reads can answer the question.

Main retrieval surfaces:

```text
knowledge/index.md
evidence/index.md
evidence/<domain>/index.md
knowledge/<page>.md
evidence/<domain>/<subdomain>/.../<artifact>.md
source-archive/
```

## Current Understanding

For questions about what should currently be understood, start with `knowledge/index.md` unless the relevant canonical page is already known.

Preferred path:

```text
knowledge/index.md
      ↓
likely canonical knowledge page
      ↓
relevant section
      ↓
evidence only when more detail is needed
```

Do not routinely reread supporting evidence when the canonical page already answers adequately.

## Evidence and Historical Questions

For questions about what was recorded, researched, observed, or decided at a particular point, start from evidence structure.

Preferred path:

```text
evidence/index.md
      ↓
likely domain
      ↓
evidence/<domain>/index.md
      ↓
likely dated artifact
      ↓
actual evidence Markdown
```

When the likely domain is already obvious, go directly to its domain index.

An index entry is a discovery aid, not a substitute for evidence itself.

## Mixed Questions

When a question needs both current understanding and historical grounding, start with the surface that best matches the main question.

Usually:

```text
knowledge page
      ↓
its relevant evidence references
      ↓
additional domain-index retrieval only if needed
```

Prefer explicit evidence relationships from the knowledge page before broader search.

## Original Sources

Use `source-archive/` when exact original representation matters.

Preferred path:

```text
knowledge or evidence
      ↓
evidence provenance
      ↓
source-archive/
```

Do not use source archive as the normal starting point for substantive retrieval.

## Workflow-State Retrieval

Use inbox folders when the human explicitly asks about pending KB work:

```text
inbox/raw/       → unprepared sources
inbox/review/    → authored evidence awaiting approval
inbox/approved/  → approved evidence awaiting curation
```

Do not use raw or review material as canonical knowledge for ordinary substantive answers.

## Progressive Retrieval

Increase retrieval depth only as the question requires:

```text
index
  ↓
likely page or domain index
  ↓
relevant artifact
  ↓
related evidence
  ↓
original source
```

Stop once enough authoritative information has been found to answer well.

Exploit known verified paths; indexes are navigation aids, not ritual hops.

Do not add embeddings, vector databases, generated catalogs, sidecar databases, or duplicate retrieval registries unless repeated real use demonstrates that the human-readable system is materially insufficient.

---

# Traceability

Knowledge pages should expose evidence relevant to their current claims.

The `## Evidence` section represents current supporting, limiting, or contradictory evidence, not every source that ever touched the page.

For each listed artifact, identify the evidence and explain briefly why it matters.

For especially important or disputed claims, evidence may also be referenced near the claim when useful.

Do not require inline citation on every sentence.

Historical revision traceability depends on the selected backend. The core workflow guarantees evidence provenance and current relationships; it does not invent a revision ledger when the backend does not provide one.

---

# Knowledge Base Maintenance

`maintain the knowledge base` keeps the permanent KB coherent, navigable, and consistent over time.

Maintenance is primarily an automated housekeeping operation.

When explicitly invoked, inspect the relevant KB structure, identify meaningful problems, make clear low-risk corrections, verify resulting state proportionately, and report the outcome concisely.

Do not require the human to approve routine repairs individually.

Ask only when the correct durable outcome is materially ambiguous, would discard information, substantively rewrite approved evidence, or substantially restructure the knowledge base.

## Maintenance Scope

Maintenance may inspect and repair:

### Knowledge

- duplicate or overlapping canonical pages;
- incoherent page scope;
- stale current conclusions;
- obsolete sections left after newer understanding replaced them;
- pages that clearly should be merged or split;
- orphaned knowledge pages;
- stale or broken evidence references;
- knowledge pages missing from `knowledge/index.md`;
- stale knowledge-index descriptions;
- multiple canonical homes for the same durable concept.

### Evidence

- evidence under an unsuitable domain or subdomain;
- inconsistent filenames;
- duplicate or near-duplicate folder structure;
- unnecessary directory depth;
- missing or broken provenance paths;
- evidence missing from its domain index;
- duplicate or stale evidence-index records;
- domains missing from `evidence/index.md`;
- stale domain descriptions.

### Workflow State

- approved evidence already curated but still remaining in `approved/`;
- raw sources that should already have moved to `source-archive/`;
- review artifacts duplicated across workflow states;
- incomplete mechanical workflow transitions.

Maintenance must not treat unresolved `raw/` or `review/` material as approved evidence.

## Maintenance Principles

Prefer the smallest correction that restores a clear structure.

Improve existing organization before introducing new structure.

Do not redesign unrelated parts of the KB merely because maintenance is running.

Permanent evidence remains preserved; maintenance may move, rename, or repair mechanical links and indexes without substantively rewriting approved evidence.

Knowledge is current understanding and may be rewritten, consolidated, merged, or split when that clearly improves canonical structure.

If the human asks for a general health pass, use `knowledge/index.md` and `evidence/index.md` as the main maps and inspect deeper files only where necessary.

---

# Human Readability

Optimize permanent Markdown for humans as well as agents.

Prefer:

- understandable folder names;
- shallow useful hierarchy;
- descriptive dated evidence filenames;
- stable concept-oriented knowledge filenames;
- concise headings;
- scannable lists;
- well-designed tables;
- compact practical knowledge pages;
- evidence that preserves necessary detail without source noise.

Do not introduce complex schemas merely because they are technically possible.

---

# Privacy and Information Security

PII is not categorically excluded.

## Evidence

Preserve PII when it is substantively part of the record and removing it would reduce fidelity, retrieval value, or practical usefulness.

Avoid sensitive values that have no plausible future value.

## Knowledge

Prefer minimizing or abstracting PII when identity itself is not important.

Retain it when identity materially improves correctness or usefulness.

## High-Exposure Surfaces

Minimize PII more strongly in filenames, folder names, index descriptions, and high-level summaries.

## Credentials and Secrets

Never preserve passwords, authentication tokens, recovery codes, private keys, API secrets, or live credentials.

Do not use a personal knowledge base to bypass employer information-security restrictions.

If supplied material appears likely to contain customer data, restricted internal information, security-sensitive material, live credentials, or other information that should not leave its source environment, do not encourage transfer into another environment.

---

# Verification

Verification should provide confidence without materially slowing ordinary KB operations.

Use the **cheapest verification that establishes the intended result**.

Do not perform a full KB audit after routine mutations.

## Routine Mutations

For low-risk operations such as creating a review artifact, moving review evidence to approved, moving approved evidence into permanent evidence, adding a straightforward index entry, updating one knowledge page, or archiving one raw source, verify only the directly affected result.

Examples:

```text
create file
→ trust a successful mutation result when it identifies the created target

move file
→ trust the returned final location when sufficient

edit file
→ confirm the write succeeded

index update
→ confirm the expected entry exists when the mutation result alone is insufficient
```

Avoid rereading complete files when the mutation response already establishes success.

## Compound Curation

When one operation changes several connected surfaces, prefer completing the coherent transaction and then checking resulting state once per changed surface.

Avoid repeated `write → read → write → read` cycles unless a later write depends on the read-back.

## Higher-Risk Changes

Use stronger verification when an operation replaces substantial existing content, merges or splits knowledge pages, moves many files, restructures evidence domains, rewrites a large index, deletes information, or repairs inconsistent state.

Verify enough to ensure unrelated information was not lost or changed.

## Minimum Completion Check

Before reporting a routine operation as complete, establish only that:

1. the intended artifact exists in the intended workflow or permanent location;
2. any directly required index or knowledge update succeeded;
3. no known partial workflow transition remains.

Backend adapters may add a small integrity check when the storage mechanism itself can transform content.

Verification is a safeguard, not an audit.

## Mutation Reporting

After creating, editing, moving, renaming, or deleting KB artifacts, report the exact resolved location or locations changed as a cheap human observability check.

For a filesystem backend, report the resolved absolute filesystem path.

For a non-filesystem backend, report the concrete backend location as precisely as the runtime permits, including the KB root and conceptual path when useful. Example:

```text
Google Drive → OCBC Knowledge Base → inbox/review/2026-09-30--example.md
```

Do not turn this into a broader verification pass. The purpose is to let the human immediately notice if the workflow touched the wrong KB or path.

---

# Failure Rules

Stop or narrow the operation when:

- the active KB root cannot be identified reliably;
- the selected backend cannot be resolved or its adapter is unavailable;
- an operation would leave the active root without explicit source-only authorization;
- an operation would overwrite unrelated material;
- a source cannot be read faithfully enough to author evidence;
- an approved artifact appears corrupted or materially incomplete;
- required provenance cannot be resolved without guessing when that provenance materially matters;
- the runtime cannot safely perform the required storage mutation;
- the requested operation violates the security model.

Prefer partial safe completion over speculative mutation.

Never silently expand scope.

Never claim persistence, movement, deletion, or modification succeeded unless the available mutation result or targeted verification establishes it.

---

# Non-Negotiables

- `evidence/` and `knowledge/` are the useful permanent product.
- Storage semantics are canonical; backend mechanics are delegated to adapters.
- Do not assume Git or version control by default.
- The configured root is authoritative; `*-knowledge-base` is a convention, not a requirement.
- When an active local project is resolved from `~/.agent-core/projects.toml`, its configured `knowledge_base` value is the authoritative KB root for ordinary operations.
- Do not infer a KB root from Git boundaries or nearby folders when the project registry provides one.
- Normal KB operations do not modify the project registry.
- After KB mutations, report the exact resolved location or locations changed.
- Raw source material is not approved evidence.
- Agent-authored capture from an already-developed conversation goes directly to review-ready Markdown.
- Review Markdown is not approved evidence.
- Presence in `approved/` means human-approved evidence content.
- Approval is a state transition, not a rewrite.
- `prepare raw inbox` operates on `raw/`.
- `curate approved inbox` operates on `approved/` and completes routine curation automatically.
- Original raw sources move to `source-archive/` after their approved evidence is successfully curated.
- Source archive is provenance, not canonical evidence.
- Evidence selection is deliberate: `0 / 1 / N`.
- Permanent evidence is faithful, readable, dated Markdown and historically preserved in substance.
- Knowledge is practical, current, concept-oriented, and substantially more compact than evidence.
- Search existing knowledge before creating new canonical knowledge.
- No substantive canonical knowledge claim comes from unapproved raw or review material.
- `evidence/index.md` maps evidence domains.
- Evidence domain indexes discover individual evidence artifacts.
- `knowledge/index.md` maps canonical knowledge pages.
- Retrieval should narrow cheaply before opening many files.
- Known verified paths may be accessed directly; indexes are navigation aids, not ritual hops.
- Routine curation and maintenance should be automated rather than proposal-gated.
- Verification should be proportionate to risk and should not add unnecessary round trips.
- Never let the KB become a transcript archive disguised as knowledge.

---

# Final Model

```text
conversation already developed with agent
                ↓
           "capture this"
                ↓
      select + author Markdown
                ↓
          inbox/review/
                ↓
          HUMAN APPROVAL
                ↓
         inbox/approved/
                ↓
       curate approved inbox
                ↓
 evidence/ + indexes + useful knowledge updates
```

Raw-source path:

```text
PDF / image / notes / exported source
                ↓
           inbox/raw/
                ↓
         prepare raw inbox
                ↓
      select + author Markdown
                ↓
          inbox/review/
                ↓
          HUMAN APPROVAL
                ↓
         inbox/approved/
                ↓
       curate approved inbox
          ↙             ↘
 source-archive/     evidence/
                         ↓
                  knowledge/ when useful
```

Retrieval:

```text
current practical understanding
    → knowledge/index.md
    → canonical knowledge page
    → evidence only when more detail is needed

historical/source evidence
    → evidence/index.md
    → domain index
    → dated evidence artifact
    → source archive only for exact original fidelity
```

The system succeeds when noisy inputs become a knowledge base whose evidence is faithful and chronologically useful, whose knowledge is practical and easy to browse, and whose structure is cheap for both humans and agents to navigate and maintain regardless of whether the active backend is a local filesystem or Google Drive.
