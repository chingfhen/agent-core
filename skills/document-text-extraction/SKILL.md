---
name: document-text-extraction
description: Extract text from a specified PDF or image into local temporary Markdown and a quality report only when the human explicitly requests extraction. Does not capture, author, or curate knowledge-base material.
---

# Document Text Extraction

## Purpose

Convert an explicitly requested PDF or image into local, temporary text for human inspection or a later, separately authorized workflow.

The **source document remains authoritative**. Machine extraction is not human verification, evidence authoring, or knowledge-base curation.

## Invocation Boundary

Do not inspect or extract an inbox document merely because it exists. Proceed only when the human explicitly requests extraction of an identifiable source. If the source is ambiguous, ask for its location.

## Workflow

1. Inspect the source locally: file type, whether PDF text is native, image dimensions, and page count.
2. Choose the smallest suitable local method:
   - Native-text PDF: PyMuPDF extraction.
   - Scanned PDF or image: locally installed Docling OCR/layout processing.
   - Unusually tall image: divide into temporary segments, then process each segment.
   - Partial or failed output: optionally compare a separate local PyMuPDF4LLM extraction where suitable.
3. Write collision-safe outputs under `tmp/`:
   - `<source-name>--extracted.md`
   - `<source-name>--extraction-report.md`
4. Return paths, extraction method, and status: `complete-looking`, `partial`, or `failed`.

Use the project's approved local dependencies and invocation conventions; use `uv run` for the Windows uv-managed workflow where applicable. Never install unapproved dependencies or send sensitive source material to remote OCR/LLM services without explicit permission.

## Fidelity

- Do not silently correct OCR, invent missing values, combine conflicting engine outputs as facts, or imply that extraction was human-verified.
- Preserve page or segment boundaries when necessary to find coverage gaps.
- Record source path/hash, engine/version/settings, expected pages/segments, and limitations in the report without unnecessarily repeating sensitive content.
- Non-empty text is not proof of completeness.

Statuses:
- **complete-looking:** expected pages/segments yield meaningful content, with no obvious coverage gap.
- **partial:** some useful content exists, but coverage or fidelity is uncertain.
- **failed:** no useful extraction was obtained.

## Output Boundary

Temporary outputs under `tmp/` are disposable but remain available for inspection. Do not stage or commit them, and do not write into any knowledge-base evidence, inbox, or knowledge folders.

An extraction request authorizes **extraction only**. If the human later asks to capture or preserve the result, provide the original source, extraction, and quality report to the **separately selected authoritative knowledge-base workflow**. That later workflow owns any authoring or persistence. This skill has no runtime dependency on another skill.
