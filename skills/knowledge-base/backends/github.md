# GitHub Backend

Read the main [skill](../SKILL.md) first. Use this adapter for repository access
through a connector or API. A local Git checkout uses the filesystem adapter instead.
These are capability-based requirements, not claims that a particular ChatGPT app
or plugin exposes all of them.

## Identity and skill loading

An explicit target must establish **owner/repository, branch or ref, and KB directory**.
A repository-root KB can use `/`. If a URL establishes these, reuse it; otherwise
resolve them from explicit configuration or ask. Never guess a repository, search
the whole account for a default, or equate skill and content repositories.
A separately configured remote knowledge-page location needs its own complete
destination identity; it does not authorize unrelated writes.

The web app cannot assume access to the human's configured local KB. It also does not necessarily discover
or execute `SKILL.md` merely because it can search GitHub. The calling environment
must load the canonical skill and required relative references from Agent Core, then
resolve the independently selected content root. Do not create a competing workflow
copy inside the KB to simulate skill installation.

## Capability check

Determine only what this operation requires, using exposed tool contracts and scoped
reads—not test writes in the real KB:

| Operation | Required capability |
| --- | --- |
| Recall | Read actual files and narrow paths/search/tree listings within the selected root/ref, including relevant living knowledge |
| Capture/update | Create/update raw Markdown at exact paths, read current contents, confirm persistence |
| Knowledge-page maintenance | Search/read the authorized page location and write affected pages; missing access leaves maintenance incomplete, not record capture blocked |
| Inbox processing | Read source content faithfully and perform the required record/index writes |
| Inbox clearing | Additionally preserve original bytes in an authorized separate archive, verify identity, and remove exact inbox entries safely |

A read-only connector supports retrieval, not saved capture. It may supply a clearly
labeled draft when useful, but must not claim a record or managed artifact was saved.
Do not assume access to local files, binary bytes, Git writes, branch operations, or
external storage based on the ability to search a repository.

## Reads and retrieval

Apply [selective retrieval](../references/retrieval.md). Use exact paths, relevant
living-knowledge pages, root/month indexes, filename/tree narrowing, and scoped
text search when supported. Include selected `records/`, `knowledge/`, and
`managed/` or an explicitly configured page location, not other repositories by
inference. Honor the selected ref; default-branch search cannot establish absence
on a feature branch. Use scoped direct reads and disclose limitations.

GitHub browser code search supports `repo:` and `path:` qualifiers, but connectors
and APIs can differ. Use the actual tool's syntax rather than copying browser queries
blindly. Verify search hits by reading the file at the selected identity/ref.

Do not include raw inbox files or another repository in ordinary recall. Search can
lag writes; use mutation-returned paths/revisions and direct reads for recent content.

## Mutations and publication boundary

A request to save to an explicitly selected remote KB authorizes the necessary scoped
remote write only when the repository, branch, and write mechanism are clear. Explain
if that mechanism creates a commit or a pull request. If the write target/publication
mode is unresolved, establish it before mutation. Reading a connected repository does
not authorize writing to its default branch.

- Read current files and use expected file SHA/revision or branch-head guards where
  available. Do not overwrite a concurrent edit; reread and reconcile or stop.
- Write raw UTF-8 Markdown. Preserve unrelated bytes/sections in existing targets.
  Never create a Google Doc or another conversion intermediate.
- Prefer one coherent multi-file write for records and indexes when supported. If
  only individual writes are available, track affected paths and finish missing steps
  on retry without creating duplicate records. Do not clear inputs before completion.
- Respect established branch/PR policy. Do not force-push, create repositories, change
  permissions, bypass protections, merge a PR, or modify unrelated files.
- A proposed PR is not merged canonical content. Report its status and link; keep
  inbox sources pending until required outputs are durable in the selected KB ref.

Local capture does not imply remote publication; this adapter is used only for
a selected remote target. A separate knowledge-page destination requires separately
resolved authorization and capabilities. Apply the main skill's bounded page
maintenance after record/index persistence. Report unavailable page access or
failed updates separately; do not substitute a destination or roll back saved
records. Never expose private workplace content for runtime convenience.

## Archive and cleanup

This backend has no automatic archive service. Use an explicitly identified,
authorized archive reachable from the current runtime, outside the KB directory
and not containing it. It may be a separate directory in the same repository/ref
when publication of those original bytes is explicitly authorized. Establish its
complete repository/ref/path identity before writing.
Do not choose Google Drive, another repository, a temporary sandbox, or a fictitious
local home as a fallback. Do not treat Git history as the source archive.

Before removing an inbox entry, establish original-byte preservation, actual archive
identity, completed records/indexes, recorded provenance, and an unchanged source
revision/content. Use guarded removal when available. If exact bytes or safe removal
cannot be verified, retain the source and report cleanup as pending. Missing archive
access need not prevent safe capture, but it prevents claiming the inbox is cleared.

An archive path written by a local agent may be inaccessible here. Preserve the
locator and state that limitation when original-source access is needed. Do not
fabricate a remote copy or assume GitHub contains those bytes.

## Completion

Report repository, branch/ref, KB-relative paths, useful URLs/revisions, and whether
changes are saved, proposed, or incomplete. Verify affected links and the final state
of compound operations without auditing the entire repository. Never claim connector
compatibility or end-to-end cleanup was tested unless that actual operation and
runtime were exercised.
