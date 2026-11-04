# Filesystem Backend

Use this adapter for a durable local or mounted filesystem, including a local Git
checkout. Git is not required. Read the main [skill](../SKILL.md) for maintenance;
ordinary read-only access requires neither it nor this adapter.

## Roots and capabilities

Resolve KB, archive, and any explicitly configured separate knowledge-page roots
by the skill's precedence rules. Expand `~` using the actual user's home
(`%USERPROFILE%` on Windows); do not guess names, directories, or temporary
sandbox paths. KB/archive roots must be explicitly selected or configured in
applicable AGENTS.md; new section-relative paths use its declaring directory,
while legacy workspace-relative paths retain their recorded workspace root.
There are no home-directory fallbacks. Living knowledge stays at `<kb>/knowledge/`
unless explicitly configured otherwise. Report actual paths after writes.

Before mutation, normalize paths and inspect the relevant existing parents. Refuse
path traversal or symlink/junction/reparse-point indirection that escapes the selected
roots. Do not silently adopt a file where a directory is expected or initialize over
an unrelated existing layout. Preserve unrelated files and user changes.

The archive must be outside the KB directory and must not contain the KB; it may
share the KB's Git worktree. The standard configured workspace destination is
`.work-context/archive/knowledge-base/`. Check normalized selected paths, not
arbitrary repositories. If the archive overlaps the KB, request a separate
destination instead of moving sources there. Ordinary KB writes stay inside
the KB, except an explicitly configured external knowledge-page root may hold
living pages only. This does not authorize writes to unrelated documentation or
tasks. Approved original archival owns only the specifically selected destinations
of verified processed inputs.

Use ordinary directory listing, UTF-8 reads/writes, filename/text search, copying,
rename, and targeted removal. If a needed capability is missing, report the limitation;
a temporary downloaded draft does not establish durable persistence.

## Write and update

- Write raw Markdown, not a rich-document conversion. Create parents lazily.
- Read current contents before editing an existing record, artifact, or index.
  Prefer targeted edits; preserve unrelated sections and intervening user changes.
- For a substantial replacement, use a temporary file followed by atomic replacement
  when readily available. This prevents torn writes, not concurrent-edit conflicts;
  recheck the source when concurrent changes are possible.
- Never overwrite an unrelated collision. Reuse an existing identity only when its
  content/provenance establishes the match; otherwise choose a descriptive suffix.
- Do not rename an artifact merely because it was updated. Repair directly affected
  links if a requested move or rename changes its location.
- Apply the main skill's bounded knowledge-page maintenance after record/index
  persistence. An inaccessible page root or failed page write leaves that
  maintenance incomplete, not the records unsaved. Do not substitute another root.

## Explicit original-byte archival

Use this adapter **only after** the main skill has shown the proposed filenames
and `<archive>/YYYY-MM/` destinations and obtained affirmative selection.
Do not scan the archive or any legacy inbox to select additional sources.

1. Resolve and normalize each **approved** source path and destination. The
   archive root must be separately configured/authorized, outside the KB.
   Month folder is the **archival date** in `YYYY-MM` format, even when the
   original file was created earlier.
2. Preserve original filenames and exact bytes by copying (not moving). If a
   destination path exists, confirm the identity before reusing an identical
   copy; otherwise choose a collision-safe suffixed name, never overwrite.
   Do not add a mandatory topic subdirectory.
3. Verify the retained content against the source read for this operation with
   byte comparison or a strong content hash (e.g. SHA-256). Detect source changes
   during the operation. Never infer success from same filename or size.
4. After verification, write the actual archived locator into the associated
   KB record **if knowledge capture was requested**. Preserve the pre-archive
   original path when useful and do not claim archival before it exists.
5. Do not delete or move source files, empty `inbox/` directories, or delete
   old archive data. If a copy/check fails, keep all original data in place and
   report the specific incomplete action.

A manually archived original explicitly referenced by the human is read from
that exact path for ordinary capture and is **not** copied or relocated.
Report missing/inaccessible exact files instead of searching for substitutions.
An archive does not guarantee backup, portability, or permission to put
workplace source data into private storage.

## Search

Search `records/`, relevant `knowledge/`, and `managed/` (or a configured external
knowledge-page root) with available filename/grep tools. Use literal error matching when
appropriate and bound results before full reads. Do not search the archive by default.
[Selective retrieval](../references/retrieval.md) provides detail for difficult lookups.

## Git and verification

A local capture modifies files only. Do not initialize a repository, stage, commit,
push, change remotes, or edit Git exclusions as an incidental KB action. A separate
publication/migration request determines those operations and their privacy boundary.
A raw input is not recoverable from Git merely because its parent directory is a
checkout; untracked/uncommitted files may have no history.

Use successful write results and targeted checks for ordinary records/indexes. Check
that links resolve and substantial edits preserve unrelated material. For explicitly approved archival, verify retained byte fidelity, exact destinations,
and unchanged original sources.
Do not perform a whole-KB audit. Report local paths and outstanding steps; do not
claim changes are on GitHub until an authorized publication actually succeeds.
