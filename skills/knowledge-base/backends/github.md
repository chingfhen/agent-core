# GitHub Backend

Use this adapter for repository access through a connector or API. A local Git
checkout uses the filesystem adapter instead. Read the main [skill](../SKILL.md)
for maintenance; ordinary read-only access requires neither it nor this adapter.
These are capability-based requirements, not claims that a particular ChatGPT app
or plugin exposes all of them.

## Identity and workflow availability

An explicit target must establish **owner/repository, branch or ref, and KB directory**.
A repository-root KB can use `/`. If a URL establishes these, reuse it; otherwise
resolve them from explicit configuration or ask. Never guess a repository, search
the whole account for a default, or equate skill and content repositories.
A separately configured remote knowledge-page location needs its own complete
destination identity; it does not authorize unrelated writes.

The web app cannot assume access to the human's configured local KB or that a
maintenance skill is exposed merely because it can search GitHub. Read-only recall
can use available read tools and the independently configured content root without
loading the skill. For maintenance, load the canonical skill and required references;
if unavailable, report the gap. Do not create a competing workflow copy inside the KB.

## Capability check

Determine only what this operation requires, using exposed tool contracts and scoped
reads—not test writes in the real KB:

| Operation | Required capability |
| --- | --- |
| Recall | Read actual files and narrow paths/search/tree listings within the selected root/ref, including relevant living knowledge |
| Capture/update | Create/update raw Markdown at exact paths, read current contents, confirm persistence |
| Knowledge-page maintenance | Search/read the authorized page location and write affected pages; missing access leaves maintenance incomplete, not record capture blocked |
| Original archival proposal | Identify exact accessible originals and propose destinations without writing |
| Approved original archival | Copy selected **original bytes** to an authorized archive, verify fidelity and report actual locators; a Markdown-only connector is insufficient |

A read-only connector supports retrieval, not saved capture. It may supply a clearly
labeled draft when useful, but must not claim a record or managed artifact was saved.
Do not assume access to local files, binary bytes, Git writes, branch operations, or
external storage based on the ability to search a repository.

## Reads and retrieval

Use exact paths, relevant living-knowledge pages, root/month indexes, filename/tree
narrowing, and scoped text search when supported. Include selected `records/`, `knowledge/`, and
`managed/` or an explicitly configured page location, not other repositories by
inference. Honor the selected ref; default-branch search cannot establish absence
on a feature branch. Use scoped direct reads and disclose limitations.
[Selective retrieval](../references/retrieval.md) provides detail for difficult lookups.

GitHub browser code search supports `repo:` and `path:` qualifiers, but connectors
and APIs can differ. Use the actual tool's syntax rather than copying browser queries
blindly. Verify search hits by reading the file at the selected identity/ref.

Do not search original archives, legacy inbox files or another repository during
ordinary recall. An exact original specified by the human or a KB source pointer
may be read if authorized and accessible. Search can
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
  any source archival uncompleted until original bytes are verified at the approved destination.

Local capture does not imply remote publication; this adapter is used only for
a selected remote target. A separate knowledge-page destination requires separately
resolved authorization and capabilities. Apply the main skill's bounded page
maintenance after record/index persistence. Report unavailable page access or
failed updates separately; do not substitute a destination or roll back saved
records. Never expose private workplace content for runtime convenience.

## Explicit archival of original sources

A GitHub connector's ability to save Markdown does **not** establish permission
or capability to preserve binary originals. The main skill must first present
exact source names and approved proposed destinations and obtain affirmative
human file selection. Determine backend byte-copy/verification capability from
exposed operations; do not perform a test write to real user archives.

The separate archive must be explicitly configured, reachable, authorized for
these exact files, and **outside** the KB. A repository/ref/path is not an
authorized archival destination merely because the agent can push commits.
Never silently choose another GitHub repository, the KB repository itself,
Google Drive, a temporary sandbox, or an arbitrary local home. For remote
archives, publication of source bytes is a separate privacy boundary requiring
explicit destination approval. Preserve existing storage and work restrictions.

If approved and technically possible: store the **original bytes** at the
approved `<archive>/YYYY-MM/<original-name>` locator, use collision-safe names,
verify bytes/hashes, and record actual locators in KB records when capture was
requested. Never delete the source by default. If not possible, preserve any
completed Markdown capture separately and report original archival as
**unfulfilled**, with the specific access/capability blocker.

Manually archived originals identified by exact user reference are not copied,
moved, swept or rearchived. If the source is inaccessible from a remote session,
record only its user-reported locator where appropriate and explicitly state the
file could not be examined. Legacy `inbox/` cleanup is deprecated; do not
interpret a cleanup cue as permission to remove pending files.

## Completion

Report repository, branch/ref, KB-relative paths, useful URLs/revisions, and whether
changes are saved, proposed, or incomplete. Verify affected links and the final state
of compound operations without auditing the entire repository. Never claim connector
compatibility or end-to-end cleanup was tested unless that actual operation and
runtime were exercised.
