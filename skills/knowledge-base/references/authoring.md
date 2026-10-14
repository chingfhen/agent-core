# Authoring Records and Managed Artifacts

Read when writing either content category. The main [skill](../SKILL.md) owns
invocation, locations, permissions, and lifecycle; this reference owns writing
quality. Adapt structure to the material rather than filling a universal template.

## Shared Markdown conventions

Use raw UTF-8 Markdown with descriptive filenames. Start new documents with minimal
frontmatter:

```yaml
---
title: Dependency Resolution in the Shared Environment
description: Constraints, tested commands, and unresolved compatibility issues.
created: 2026-10-14
updated: 2026-10-14
---
```

`created` is the immutable capture/creation date; `updated` changes with substantive
meaning, not a link repair or formatting change. These are illustrative dates.
Index files need no frontmatter. Preserve established metadata when updating rather
than mass-normalizing existing files. Quote YAML values containing special syntax.

Use source/event dates in the body when they differ from capture date. Include
source links or locators where they support later retrieval and verification.
Never fabricate provenance, exact quotations, command results, or human validation.
A missing original should be disclosed when exact wording or fidelity matters.

## Records: preserve what prevents rediscovery

Ask: **What would a capable future agent otherwise need the human to explain again?**

Strong candidates include:

- organization-specific vocabulary, relationships, responsibilities, and procedures;
- environment/version constraints and reasons ordinary advice does not apply;
- what was observed, attempted, ruled out, changed, or established;
- decisions/preferences and the conditions or rationale that make them useful;
- exact commands, configuration fragments, thresholds, or identifiers needed to reuse
  a finding safely, excluding secrets;
- useful mental models, contradictions, unknowns, and limitations.

Select the durable scope first, then represent it faithfully. Default to one coherent
record; split when independently retrievable topics would otherwise be buried.
Do not split merely because a transcript is long. Do not preserve every pasted error,
repetition, exploratory detour, or intermediate hypothesis.

A short opening such as **What we learned** can convey the main result and important
qualifications. Follow with context and supporting detail only as needed. It is not
a substitute for a requested managed artifact.

### Use the whole available understanding

A rough transcript or note is only one input. The discussion may explain acronyms,
correct a speaker, distinguish a proposal from a decision, or identify the actual
working procedure. Carry those clarifications into the record with their source
basis intact. Do not guess what unexplained fragments such as `A > B > C` mean.

Distinguish claims naturally where it matters:

- **Observed/tested:** the available output shows what happened in a stated context.
- **Reported:** the human or a named source supplied the claim.
- **Inferred:** an explanation fits the evidence but has not been independently proven.
- **Unresolved/untested:** a question, candidate fix, or uncertainty remains.

Do not assign artificial confidence scores or put every sentence into a schema.
Keep meaningful conflict visible. A command succeeding once is not proof of a
universal root cause or a permanently supported solution.

### Example: debugging knowledge

A useful dependency-resolution record might contain:

1. The environment, package versions, permissions, and network constraints that mattered.
2. The symptom and established cause, or the leading explanation labeled as such.
3. The working commands, execution location, prerequisites, and material side effects.
4. The observed result and verification actually performed.
5. Important failed approaches and why repeating them would waste effort.
6. Remaining limits, unresolved questions, and relevant source links.

A meeting record may instead need participants' roles, a process, decisions, and
open interpretations. Do not force technical debugging headings onto other subjects.

### Updates and corrections

Extend an existing record when it is clearly the same learning context and that
improves future use. Use a new record when a distinct event or result deserves its
own dated identity. A repeated sync can be a no-op.

Correct relevant errors encountered during an authorized write. For a material
correction, briefly identify what changed and its basis; do not silently turn a
historical failed attempt into a success. Link related records when their difference
or supersession matters. Do not search the entire KB for other things to correct.

### Raw-source provenance

For records derived from inbox files, retain enough identity to prevent duplicate
processing and recover the original:

```text
Source: Teams meeting transcript, clarified in discussion
Source date: 2026-10-12
Original input: inbox/aws-session.txt
Archived source: <actual verified archive path or remote locator>
```

Use an available stable source ID or content hash when needed to distinguish changed
files or resume partial archival. A filename match alone does not establish identity.
Only record completed archival after it exists; while processing is incomplete the
original-input locator remains sufficient. Each output from a split source retains
its source association. Archive paths are provenance, not ordinary search targets.

## Managed artifacts: write for a specific human use

Start with purpose and audience, using context already supplied. Ask only when the
missing choice materially affects the output. Prefer an appropriate existing artifact
when the request is an update; do not create competing `v2` or `latest` files.

Choose a structure that serves the requested product:

| Product | Useful emphasis |
| --- | --- |
| Lesson or explanation | Key takeaways, mental model, real terminology, causal reasoning, limits |
| Command reference | Task-based command groups, prerequisites, exact syntax, side effects, expected results |
| Checklist or procedure | Ordered actions, decision points, required inputs, completion conditions |
| Presentation script | Audience, intended duration when known, speakable sequence, transitions |
| Comparison or decision aid | Comparable criteria, meaningful trade-offs, applicability and uncertainty |

Use the highest-value material rather than summarizing every source. Explain the
reasoning necessary to understand or apply a conclusion. Preserve important exceptions
and conditions even when simplifying aggressively. Ground substantive claims in
relevant records or supplied sources; do not require artificial intermediary records.

Use short prose for causal explanations, bullets for parallel points, numbered lists
for genuine sequences, fenced blocks for exact commands, and tables for comparisons.
A simple Mermaid diagram is appropriate when it makes an established relationship
clearer; avoid decorative or speculative diagrams. Keep a prose explanation so the
artifact remains useful where Mermaid rendering is unavailable. Do not execute
commands just because they appear in a command reference.

Other writing skills may be used when explicitly requested or independently relevant,
but are not prerequisites for a competent managed output.

Before completion, check that the artifact works without the old conversation,
answers its intended human need, and keeps the caveats that affect correct use.
Remove repetitive summaries, empty sections, jargon without explanation, and detail
that does not serve the requested output. Include concise supporting links when useful.
