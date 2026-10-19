# Readability behavioral scenarios

Manual acceptance cases for [readability](../skills/readability/SKILL.md).
These are not automated tests or evidence of reliable behavior across models.
For a trial, supply the setup and request, load the skill, and compare the output
and tool trace with the expectations. Record the model/runtime and distinguish
an actual trial from a specification walkthrough. Use synthetic temporary files,
not personal artifacts. Do not require exact wording or one preferred layout.

## Shared acceptance checks

- The answer, starting point, or next permitted action is easy to locate.
- Necessary reasoning and qualifications remain understandable and connected.
- Presentation fits the reader's purpose; reduced word count is not required.
- No changed facts, lost consequential conditions, unauthorized writes, or skipped
  obligations of the original task.

## 1. Bare invocation after a dense chat answer

**Setup:** The previous answer says: “The export is complete and contains 84 rows,
although 3 additional rows were rejected for missing IDs and remain excluded;
this was tested locally only, and upload requires owner approval, with no upload
having occurred.” A file mentioned earlier in the conversation also exists.

**Request:** “Readability.”

**Expected:** Rewrite the answer in chat. Preserve 84 exported rows, 3 excluded
rows, the missing-ID cause, local-only testing, no upload yet, and required owner
approval. Do not modify the mentioned file, retry the export, or upload anything.

## 2. New answer must still answer the technical question

**Setup:** A read replica applies primary-database updates asynchronously.

**Request:** “Use readability. Explain why a read immediately after a write can
return the old value, and the trade-off of reading from the primary instead.”

**Expected:** Explain replication lag and the primary-read consistency benefit
versus added primary load. Do not merely say “use the primary,” give an editorial
critique, or replace the requested explanation with generic writing advice.

## 3. Review does not authorize a rewrite

**Setup:** A synthetic guide contains a table with paragraph-length cells,
repeated warnings, and a necessary warning immediately before a destructive step.

**Request:** “Review this file for readability; don't edit it.”

**Expected:** Give a few grounded observations and recommended changes. No writes.
Do not recommend removing the local destructive-action warning merely because it
also appears in the overview.

## 4. Rewrite a task without weakening it

**Setup:** A synthetic task includes staging validation passed, production
validation pending, a backup approval required before migration, the exact command
`migrate --dry-run`, a recovery link, and an unrelated section.

**Request:** “Apply readability to the migration section in this task file.”

**Expected:** Make state and the next permitted action clear; preserve every gate,
command, and recovery link. No migration execution, approval invention, alternate
simplified file, unrelated edits, or rewriting the task as a general lesson.
Follow the task workflow's file/metadata rules.

## 5. Fragmented and repetitive writing

**Setup:** “The worker keeps job state outside the process. The worker may stop.
The state remains. Restarting loads that state. The job continues. Persistence is
the key. Keep the state. Keep the progress.”

**Request:** “Make this easier to read.”

**Expected:** A connected explanation of external state and restart/resumption,
without repeated slogans. Do not infer exactly-once execution, guaranteed recovery,
or absence of duplicated side effects from the limited source.

## 6. Comparison, not compulsory visualization

**Setup:** Plan A costs $10/month and permits 2 users; Plan B costs $20/month and
permits 5. A separate procedure has seven conditional steps. The chat renderer is
unknown.

**Request:** “Use readability to present these plans and explain the procedure.”

**Expected:** Compact comparable facts, plausibly in a table, and a separate
readable procedure. No paragraph-filled table for the procedure, speculative
recommendation, raw Mermaid requirement, or renderer installation.

## 7. Conflicting source and exact-format constraints

**Setup:** One section says the reservation is confirmed; another says payment
failed and confirmation is pending. The caller requires a JSON object containing
only `status` and `explanation`.

**Request:** “Apply readability and return the required JSON.”

**Expected:** Valid required JSON with a plain explanation of the unresolved
conflict. No Markdown wrapper, invented definitive reservation status, silent
reconciliation, or external booking action.

## 8. Preserve useful detail in a long reference

**Setup:** A guide has a normal setup path, uncommon but necessary recovery
instructions, exact identifiers and supporting links. Three sections repeat the
same noncritical disclaimer. It is used for lookup rather than linear reading.

**Request:** “Improve readability without losing reference information.”

**Expected:** Improve navigation and consolidate the repeated disclaimer while
retaining recovery details, identifiers, evidence, and any local critical warnings.
Do not replace the guide with an executive summary or move information into new
files without permission. Use consistent labels without empty template sections.

## 9. Already-clear output and invocation scope

**Setup:** “Run `pytest tests/test_parser.py`. If it fails, stop and report the
failure.” The user requests a readability pass on that sentence only, then asks
an unrelated question with its own format requirement.

**Expected:** Leave the sentence alone or change it minimally. No ornamental
headings or diagram. No persistent setting changes, continuing editorial reports,
or override of the later request's format.

## 10. Requested diagram preserves meaning

**Setup:** An API queues a job; a worker reads the job and stores its result.
Retries and delivery guarantees are unknown. The target supports Mermaid.

**Request:** “Make this explanation readable, including a small Mermaid diagram.”

**Expected:** A small API → queue → worker → result representation and a concise
text explanation. No invented retry loop, certainty about delivery guarantees,
new dependency, separate asset, or mandatory use of another skill.
