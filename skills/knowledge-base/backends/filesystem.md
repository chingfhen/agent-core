# Filesystem Backend

Read the main [skill](../SKILL.md) first. Use this adapter for a durable local or
mounted filesystem, including a local Git checkout. Git is not required.

## Roots and capabilities

Resolve KB, archive, and any explicitly configured separate knowledge-page roots
by the skill's precedence rules. Expand `~` using the actual user's home
(`%USERPROFILE%` on Windows); do not guess names, directories, or temporary
sandbox paths. Default KB/archive roots are `~/.kb/` and `~/.kb-archive/`;
living knowledge defaults to `<kb>/knowledge/`. Report actual paths after writes.

Before mutation, normalize paths and inspect the relevant existing parents. Refuse
path traversal or symlink/junction/reparse-point indirection that escapes the selected
roots. Do not silently adopt a file where a directory is expected or initialize over
an unrelated existing layout. Preserve unrelated files and user changes.

The archive must be outside the KB and its Git worktree. Check the selected paths,
not arbitrary repositories. If an explicit archive violates that boundary, request
a safe destination instead of moving sources there. Ordinary KB writes stay inside
the KB, except an explicitly configured external knowledge-page root may hold
living pages only. This does not authorize writes to unrelated documentation or
tasks. Inbox processing owns only the exact archival destinations and removal
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

## Archive and clear safely

Use the main skill's capture-first sequence. For each source whose records and
navigation are complete:

1. Select `<archive>/YYYY-MM/<original-name>` using archive date. If that path is
   occupied, use a collision-safe suffix, unless verified identity proves it is the
   same source from an interrupted operation. Never replace an existing original.
2. Copy the original bytes without normalization or extraction. For sources already
   archived on a previous attempt, verify the existing copy instead of duplicating it.
3. Compare bytes or a content hash, not just size/name, between the input read for
   capture, the current input, and the archive. A changed input remains pending.
4. Record the actual archive locator in associated records. Keep the original
   KB-relative input path for provenance. Verify these targeted updates succeeded.
5. Remove only the exact unchanged inbox file after the retained copy and record
   links are established. Recheck identity immediately before removal. If concurrent
   writing cannot be excluded safely, leave the input pending.
6. Confirm the input is absent and the archive remains present. Remove empty input
   subdirectories only when they belonged to this completed batch; preserve the inbox.

Copy-verify-remove is intentional: the archive may be on another volume and a move
alone may not provide enough fidelity/recovery evidence. If interrupted, an extra
copy is safer than lost source material. Do not use recursive deletion to empty an
inbox or archive. Do not remove directories containing unprocessed or newly added files.

Archival does not guarantee backup, portability, or suitability for personal storage.
Do not archive known secrets or restricted data into an unauthorized destination;
leave the input in place and report the issue without echoing sensitive values.

## Search

Apply [selective retrieval](../references/retrieval.md). Search `records/`,
relevant `knowledge/`, and `managed/` (or a configured external knowledge-page
root) with available filename/grep tools. Use literal error matching when
appropriate and bound results before full reads. Do not search the archive by default.

## Git and verification

A local capture modifies files only. Do not initialize a repository, stage, commit,
push, change remotes, or edit Git exclusions as an incidental KB action. A separate
publication/migration request determines those operations and their privacy boundary.
A raw input is not recoverable from Git merely because its parent directory is a
checkout; untracked/uncommitted files may have no history.

Use successful write results and targeted checks for ordinary records/indexes. Check
that links resolve and substantial edits preserve unrelated material. For clearing,
verify retained source fidelity, completed associated records, and source absence.
Do not perform a whole-KB audit. Report local paths and outstanding steps; do not
claim changes are on GitHub until an authorized publication actually succeeds.
