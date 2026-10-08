---
name: evidence-authoring
description: Creates faithful, retrieval-ready Markdown evidence from explicitly supplied statements, conversations, emails, messages, ideas, research, events, or document text. Use when the human asks to capture, record, preserve, or author new Markdown evidence in knowledge-base/inbox/. Does not extract binary documents or curate the result.
---

# Evidence Authoring

## Purpose

Turn supplied material into one self-contained, final-quality Markdown evidence artifact in `knowledge-base/inbox/`.

The artifact should be ready for later curation, but it remains unprocessed while in the inbox. The `knowledge-base` skill owns permanent placement, indexing, and any knowledge synthesis.

## Invocation Boundary

Run only when the human explicitly asks to capture, record, preserve, save, or author evidence. Do not persist ordinary conversation automatically.

A request to author evidence does not authorize document extraction. If only a PDF or image is supplied without extracted text, ask the human to explicitly request extraction rather than invoking `document-text-extraction` silently.

## Inputs

Accept either:

- **direct material** — owner statements, conversations, emails, messages, ideas, research, events, or other supplied text;
- **an extraction package** — original source path, source hash, machine-extraction path, and extraction report from `document-text-extraction`.

The original source remains authoritative. Machine extraction and authored Markdown are derived representations.

## Workflow

1. Identify the source, relevant dates, context, and supplied uncertainty.
2. Choose the smallest structure that makes the material understandable later.
3. Preserve all substantive content and distinguish quotation, paraphrase, interpretation, and unknowns.
4. Write one collision-safe file:

   `knowledge-base/inbox/YYYY-MM-DD--descriptive-title.md`

5. Before mutation, load the `knowledge-base` skill and follow its capture, Git-isolation, and commit rules.

If the human asks only for a draft or preview, return Markdown without writing a file.

## Writing Shape

Begin with applicable provenance fields; omit fields that add no value:

```markdown
# Descriptive Title

Recorded: YYYY-MM-DD
Source: [owner statement, conversation, email, extracted document, etc.]
Source date: [when known]
Derived from: [original source path, when applicable]
Source hash: [when supplied]
Extraction: [temporary extraction path, when applicable]
Extraction status: [complete-looking, partial, or failed]
Verification: [owner-provided, machine-extracted, human-verified, etc.]
```

Adapt the remaining headings to the material. Useful shapes include:

- fact or contact — `Record`, `Effective As Of`, `Context`;
- conversation — `Context`, `Participants`, `Discussion`, `Decisions`, `Open Questions`, `Follow-Up`;
- email or message — supplied headers, `Message` or `Summary`, `Context`, `Requested Actions`;
- idea — `Idea`, `Motivation`, `Assumptions`, `Constraints`, `Open Questions`;
- research — `Question`, `Sources`, `Findings`, `Limitations`;
- event — `Event`, `Date`, `People`, `Outcome`, `Follow-Up`;
- extracted document — preserve the document's natural headings, reading order, lists, and tables.

Use only supported sections. Never emit empty template sections. Rich means contextually complete, not verbose.

## Fidelity

- Never invent missing facts or silently resolve ambiguity or contradictions.
- Preserve quotations exactly; label generated retellings as summaries or paraphrases.
- Do not turn recollections into transcripts, proposals into decisions, or ideas into established facts.
- Do not summarize away substantive source content unless the human explicitly requests a summary.
- Ask a question only when proceeding would create a materially misleading record.
- Use `Unknown`, `Not supplied`, or `[unclear]` only when the gap materially matters.

For machine-extracted text, formatting normalization may restore paragraphs, headings, lists, tables, and reading order or remove obvious extraction-only line wrapping and repeated page furniture. Do not silently correct uncertain names, dates, identifiers, amounts, or clauses. Carry forward known extraction gaps and never claim verification without source-level review.

## Privacy

Keep unnecessary sensitive values out of filenames, titles, summaries, and commit messages. Never preserve passwords, tokens, recovery codes, private keys, or other live credentials. Do not send material to external services without explicit permission.

## Boundaries

This skill does not:

- extract text from PDFs, images, or other binary documents;
- move material from inbox to evidence;
- choose permanent domains or subdomains;
- update evidence indexes or canonical knowledge;
- determine whether source claims are currently true;
- replace, modify, or delete an original source.
