---
name: document-text-extraction
description: Extracts text from a PDF or image only when the human explicitly asks to extract that specific document or image. Uses local tools to produce a temporary machine-extraction draft and quality report; never captures, curates, or rewrites knowledge-base evidence.
---

# Document Text Extraction

## Purpose

Convert an explicitly requested PDF or image into local, temporary text suitable for review or handoff to `evidence-authoring`.

The source document remains authoritative. Extraction is not evidence authoring, curation, or verification.

## Invocation Boundary

Do not inspect or extract an inbox document merely because it exists.

Proceed only when the human explicitly asks to extract text from a named document or image. If the request does not identify the source, ask for its path.

## Workflow

1. Inspect the source locally: file type, native-text availability, image dimensions, and page count.
2. Select the smallest suitable local method:
   - native-text PDF: PyMuPDF text extraction;
   - ordinary scanned PDF or image: Docling with local OCR/layout processing;
   - unusually tall raster page or screenshot: extract its native image, split it into temporary sections, then run Docling on each section;
   - failed or partial Docling result: optionally run PyMuPDF4LLM as a separate fallback for comparison.
3. Write collision-safe outputs under `tmp/`:
   - `<source-name>--extracted.md`
   - `<source-name>--extraction-report.md`
4. Report the output paths, method, and status: `complete-looking`, `partial`, or `failed`.

Use `uv run` and the project-locked dependencies. Keep processing local: do not upload documents, enable remote Docling services, or use a remote OCR/LLM service without explicit permission.

## Fidelity and Quality

- Do not silently correct OCR text, infer missing values, merge conflicting engine results, or claim verification.
- Preserve segment boundaries in output produced from a tall raster source.
- The report records the source path and hash, engine/version/configuration, page or segment count, and known coverage gaps. Keep it metadata-focused; do not repeat sensitive document content unnecessarily.
- Non-empty OCR output is not proof of completeness or accuracy.

Use statuses consistently:

- `complete-looking` — every expected page or segment produced meaningful output with no obvious coverage gap;
- `partial` — useful output exists, but a page, region, table, or segment is missing or unclear;
- `failed` — no useful extraction was produced.

None of these statuses means human-verified.

## Temporary Artifacts

- All generated text, reports, and synthetic image sections belong in `tmp/` and are disposable.
- Do not retain synthetic sections outside `tmp/`; they can be regenerated from the original source.
- Leave temporary outputs available for review or handoff; do not delete them unless explicitly asked.
- Do not write to `knowledge-base/inbox/`, `knowledge-base/evidence/`, or `knowledge-base/knowledge/`.
- Do not stage or commit extraction artifacts.

## Handoff

An extraction request authorizes extraction only. Do not invoke `evidence-authoring` unless the human separately asks to preserve, capture, or author evidence.

For that handoff, provide the original source, machine output, and extraction report. `evidence-authoring` owns creating a retrieval-ready Markdown artifact in the inbox and must retain the distinction between the authoritative source, machine extraction, and any human verification.
