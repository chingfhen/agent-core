# Selective KB Retrieval

Use with the [skill](../SKILL.md) when finding prior context. This is a bounded
lookup, not a KB audit or a requirement to search before every answer.

## Decide whether a lookup earns its cost

Search when a meaningful missing fact is likely personal, historical, organizational,
or project-specific: "what did we decide", an earlier incident, an unfamiliar internal
acronym, or a recurring failure. An explicit KB search always warrants a lookup within
its requested scope. A managed-artifact request warrants grounding in relevant records.

Skip lookup when the available conversation already supplies the needed context,
the question is generic, or the human asks to use only supplied material. Do not repeat
an unsuccessful search for the same unchanged question within the session. Try again
when new identifiers, a new scope, or newly saved material make it worthwhile.

## Search progressively

1. **Known target:** open the actual known path. An index visit is not mandatory.
2. **Likely topic:** inspect filenames or a compact relevant index for distinctive
   terms: project, process, error fragment, system name, command, or common alias.
3. **Temporal context:** narrow to the requested dates. For recent recurring work,
   the current/recent month can be a cheap first pass, including adjacent months at
   a month boundary. Use source dates inside records for events captured later.
4. **Broader topic:** search filenames or text across record months for an undated
   question, weak matches, missing prerequisites, or conflicting findings. Do not
   walk every month's full contents one by one.
5. **Read candidates:** open the strongest matches and follow directly relevant
   links only when they fill a gap. Stop when the question is sufficiently grounded.

Do not impose a fixed "current month only" cutoff. A recent hit may be a workaround
that depends on an older constraint; follow that relationship when consequential.
For a broad question such as "our Jira process", use cross-month narrowing even if
this month's notes happen to mention Jira.

Indexes are navigation, not factual authority. If an index is missing or stale, use
filenames and targeted content search; a lookup does not silently rebuild the index.
Mention a discovery gap only when material to the answer.

## Control tool and context cost

- Local filename listing and text search can inspect many files without putting them
  all into model context. Return bounded filenames/matching lines before full reads.
- Search the explicit `records/` or `managed/` paths, not the home directory. The KB
  root is hidden by default; account for a tool's hidden-file behavior rather than
  treating an excluded directory as empty.
- Exclude inbox, source archives, Git internals, and unrelated files from normal recall.
- On GitHub, scope every search to the selected repository and KB directory. Use the
  connector's supported filename/path/content filters; do not assume browser code
  search syntax works in every API or app.
- Use known paths, repository trees, or indexes when indexed search misses a recent
  write. A search result/snippet is a lead, not proof of complete or current content.
- Respect output truncation and pagination. Finish reading relevant portions, not
  necessarily every result. Disclose partial search when it affects confidence.

No embeddings, vector store, duplicate content catalogue, or synthetic topic summary
is required. Root/month indexes and targeted reads are the baseline.

## Interpret before answering

Rank relevance and context applicability before age. Compare environment/version,
source/event date, source authority, verification, and unresolved qualifications.
Capture date establishes when a record was saved, not when every claim became true.

A managed artifact may be the best concise answer, but it is not automatically current
or stronger evidence than a record. Read its update date and relevant supporting
material when freshness affects the question. Neither source needs automatic rewriting.

Separate remembered knowledge from newly reasoned advice. Cite the actual documents
used, not merely their index entries. Preserve material conflicts rather than making
"newest wins" the truth rule. Say when nothing relevant was found or access/search was
limited; absence from a bounded search is not proof the information never existed.

For exact quotations or original formatting, follow an authorized source locator.
If the archive is local-only and this runtime cannot access it, explain that limit;
do not imply that the GitHub copy includes the originals.
