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

For imperfect recollection ("that dependency issue we solved"), infer possible
systems, aliases, synonyms, error terms, and work contexts before searching. The
user need not remember the date, precise phrase, or filename.

## Search progressively

1. **Resolve intent and vocabulary:** infer the likely problem, system, team,
   alternate wording, error fragments, commands, and time clues.
2. **Known target:** open the exact path. A directly relevant `knowledge/` page
   can provide quick orientation; an index visit is not mandatory.
3. **Likely topic:** inspect matching filenames and compact relevant indexes in
   `records/`, `knowledge/`, and `managed/`, using distinctive terms and aliases.
4. **Temporal clue:** distinguish event/source date, capture date, and update
   date. Month folders and filename dates describe capture, not occurrence or
   latest change. Use those folders as a strict filter only for a capture-date
   request; for event/update dates, search relevant subjects across months and
   check body dates or `updated` metadata. Recent folders can be a first pass
   for recurring work, not a complete search.
5. **Broaden when needed:** search names and text across record months when
   wording is uncertain, matches weak, prerequisites missing, or accounts
   conflict. Try alternative terms; do not walk every month or stop just
   because a recent page exists.
6. **Read and reconcile:** open strongest candidates and directly relevant links.
   Check consequential knowledge-page claims in supporting records. Rank
   source basis, environment, verification, and applicability before recency.
   Stop when grounded; cite actual documents used.

Do not impose a fixed "current month only" cutoff. A recent hit may be a workaround
that depends on an older constraint; follow that relationship when consequential.
For a broad question such as "our Jira process", use cross-month narrowing even if
this month's notes happen to mention Jira.

For example, a September incident captured in October lives under October. A
record captured in June and corrected yesterday stays under June. Neither should
be excluded by an event-date or update-date question targeting another month.

Indexes are navigation, not factual authority. If an index is missing or stale, use
filenames and targeted content search; a lookup does not silently rebuild the index.
Mention a discovery gap only when material to the answer.

## Control tool and context cost

- Local filename listing and text search can inspect many files without putting them
  all into model context. Return bounded filenames/matching lines before full reads.
- Search the selected `records/`, relevant `knowledge/`, and `managed/`
  paths, plus any explicitly configured knowledge-page location. Do not search
  the home directory or unrelated repositories. The KB root may be hidden;
  account for hidden-file behavior rather than treating it as empty.
- Exclude inbox, source archives, Git internals, and unrelated files from normal recall.
- On GitHub, scope searches to the selected repository, ref, and KB directory
  (or explicit separate knowledge-page location). Use supported path/filename/
  content filters; browser search syntax may not work in every API or app.
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

Treat `knowledge/` pages as aids, not authority: a page's current-state claim is
only as good as the records behind it. Confirm consequential claims in the
linked records before relying on them. An unresolved/outdated notice applies to
the affected claim, not necessarily the entire page. Follow its evidence links;
do not present that claim as settled or silently repair the page during recall.

Separate remembered knowledge from newly reasoned advice. Cite the actual documents
used, not merely their index entries. Preserve material conflicts rather than making
"newest wins" the truth rule. Say when nothing relevant was found or access/search was
limited; absence from a bounded search is not proof the information never existed.

For exact quotations or original formatting, follow an authorized source locator.
If the archive is local-only and this runtime cannot access it, explain that limit;
do not imply that the GitHub copy includes the originals.
