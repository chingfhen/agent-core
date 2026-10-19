---
name: readability
description: >
  Improve human readability for readability-focused requests: rewrite a hard-to-read
  response or document, review its readability, or make a new answer or artifact
  easy to understand and use. Works across subjects and workflows; preserves
  meaning, task requirements, and consequential detail. Not automatic editing,
  summarization, fact-checking, or permission to change files.
disable-model-invocation: false
---

# Readability

Make the selected output easier for its intended reader to understand and use,
without weakening the work it must do. Reduce the reader's effort to find the
point, follow the reasoning, and act correctly—not simply the word count.

This is a request-scoped intervention, not a permanent writing mode.
It works independently of other writing skills and does not require Markdown.

## Resolve the request

- **Rewrite:** Improve the selected response, passage, or artifact. A bare
  invocation after an answer means rewrite the last substantive answer in chat.
- **Write:** When invoked with a new task, perform that task and apply these
  principles to the human-facing output. Do not substitute editing for execution.
- **Review:** When asked to assess readability without rewriting, give a brief
  diagnosis with concrete examples and the most useful changes. Do not edit.

Infer the reader's knowledge, purpose, and medium from context: understanding,
deciding, following a procedure, or looking up a fact. Ask only when the target
or a consequential choice is genuinely ambiguous, not to make the user choose
an editorial template.
Apply to the selected output only unless the user explicitly requests a longer
scope; do not silently change settings or unrelated future responses.

A request to improve a chat response does not authorize file changes. A request
to rewrite an identified file authorizes only that scope, subject to applicable
instructions. Follow the
owning workflow for file location, metadata, links, and lifecycle. Do not create
an alternate simplified copy, split files, archive material, or update other
artifacts without authorization.

## Protect the task before editing

Identify what the output must still accomplish. Preserve:

- facts, decisions, rationale needed to understand them, and relevant alternatives;
- uncertainty, attribution, scope, dates, units, prerequisites, and exceptions that
  affect interpretation or action;
- permission boundaries, blockers, next permitted actions, warnings, recovery
  instructions, and honest verification state;
- exact commands, code, identifiers, paths, quotations, evidence links, and required
  output formats where their fidelity matters.

Do not turn tentative into confirmed, reported into verified, suggested into
approved, or a successful test into a guarantee. Do not remove a unique relevant
fact merely to meet a length target. A request for readability is not a request
for a lossy summary or for beginner-level treatment.

Keep research, implementation, testing, and other obligations of the original
request intact. Do not change executable content or machine-readable schemas as
prose cleanup. Required formatting wins over optional presentation improvements.
If the source contradicts itself, flag the conflict; do not choose a convenient
truth. Do not launch new research or invent explanations to make a rewrite flow.

## Edit in this order

### 1. Give the reader a useful starting point

Lead with the answer, current state, recommendation, or first action appropriate
to the purpose. Place any qualification that changes its meaning beside it.
Skip ceremonial introductions and narration of the agent's process.

For a long reference, provide a short orientation and a clear route to detail.
A short answer may need only one paragraph. Do not add an executive summary,
takeaways, and a concluding summary that all repeat the same point.

### 2. Reorganize around the reader's questions

Group related information and order it by explanation, decision, or use—not by
conversation chronology or the order facts were discovered. Put prerequisites
before actions and causes near consequences. For procedures, make actions and
expected outcomes clear, with relevant checks or recovery steps nearby.
Separate optional exploration, evidence, history, and maintenance
instructions from the main reading path when present, while keeping them
accessible where the document's purpose requires them.

Consolidate repeated statements into one clear explanation. Repeat a critical
warning at its point of use when a section may be consulted independently; do not
make the reader search elsewhere for a condition needed to act safely.

Within a document, use a logical heading hierarchy and present comparable
sections or items with consistent terms, labels, order, and formatting. A
repeated pattern should help readers know where to look next, not force empty
sections, identical paragraph lengths, or redundant disclaimers.

### 3. Make the explanation easy to follow

Use direct, literal language and name the actor or action where ambiguity matters.
Keep accurate technical terms; explain unfamiliar ones briefly when needed.
Unpack sentences that combine several independent conditions or decisions.

Keep connected reasoning in connected prose. Short sentences and whitespace help
only when they clarify; avoid a string of isolated assertions or slogans. Add a
brief connecting explanation or concrete example when it prevents the reader
having to infer a missing relationship. Do not invent facts to supply that bridge.

Remove unnecessary metaphor, flourish, dramatic framing, stock transitions, and
polished wording that adds no information. Keep an analogy when it genuinely
clarifies the subject. Preserve an appropriate human voice rather than making
all outputs terse, impersonal, or bureaucratic.

### 4. Choose presentation that earns its space

Use the simplest form that makes the information easier to understand:

- **Prose:** explanations, reasoning, and relationships.
- **Bullets:** parallel choices, properties, or independent points.
- **Numbered steps:** a real sequence or an explicitly ranked list.
- **Headings:** useful previews of meaningful sections, not every sentence.
- **Tables:** compact comparisons across common dimensions. Use subsections instead
  when cells become paragraphs, contain branching procedures, or need wide screens.
- **Emphasis:** a few conclusions, critical conditions, or navigational labels.
  If everything is bold, reduce it. Do not use capitals as routine emphasis.
- **Code formatting:** exact syntax and literal tokens, not decorative framing.
- **Links:** descriptive labels near supported claims or actions; avoid repeatedly
  interrupting the main explanation with the same evidence trail.
- **Diagrams:** established relationships, sequences, or states that are genuinely
  easier to see than to explain. One visual should answer one clear question.

Where supported, provide text alternatives for informative visuals and do not
convey essential meaning through colour or position alone.

Use Markdown only where supported and useful. Mermaid is optional, not a required
skill or dependency. If rendering is unsupported or unknown, prefer prose or a
simple list unless a diagram was requested. Keep a concise textual explanation
when using a diagram; never invent relationships or imply greater certainty than
the source. Do not install rendering tools or generate extra assets as a side effect.

For quantitative comparisons, preserve values, units, and uncertainty. Prefer a
table when exact numbers matter; do not add a chart simply because numbers exist.

### 5. Check readability and fidelity

Before returning the result, silently check:

1. Can the reader quickly find the answer or starting point?
2. Can they follow the reasoning or procedure without reconstructing missing links?
3. Can they distinguish required actions, optional detail, and unresolved choices?
4. Is the hierarchy coherent, are comparable items consistent, and are repetition
   and formatting justified?
5. Compared with the source or task requirements, have any consequential facts,
   qualifications, permissions, exact tokens, or evidence relationships changed?

Fix both presentation and preservation problems. Do not optimize a readability
score, reading-grade target, percentage reduction, or arbitrary word limit unless
requested. Longer can be clearer. Already-clear text may need little or no change.

Return the improved output, not an editorial report, unless review was requested.
For file edits, report the exact changed paths and any meaningful unresolved issue
briefly. Do not claim fact-checking, rendered validation, or reliability testing
that was not performed.

## Calibration examples

These illustrate judgment, not mandatory wording or templates.

### Dense instructions → ordered actions and a local warning

**Before:** Activate each pass Friday, having first shared one with your companion,
with each traveller using their own phone and live QR rather than a screenshot,
and remember internet access is required.

**After:** Share one pass with your companion. On Friday, each traveller activates
their pass on their own phone and displays its live QR. **Internet is required;
screenshots are not accepted.**

### Fragmented rhetoric → connected explanation

**Before:** The worker keeps job state outside the process. The worker may stop.
The state remains. Restarting loads that state. The job continues. Keep the state.
Keep the progress.

**After:** The worker stores job state outside its process, so the state survives
when the worker stops. On restart, the worker loads that state to continue the job.

### Task simplification → preserve the permission boundary

**Before:** Migration staging validation has successfully concluded, with the
exception of production validation, which remains outstanding; execution is
contingent upon owner approval of a backup.

**After:** The migration passed staging validation. Production validation remains
outstanding. Do not run the migration until the owner approves the backup.

### Readable already → leave it alone

“Run `pytest tests/test_parser.py`. If it fails, stop and report the failure.”

Do not add headings, a table, a diagram, or a second summary.
