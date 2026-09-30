# Google Drive Backend Adapter

## Purpose

Implement the canonical Knowledge Base workflow inside one explicitly configured Google Drive root.

Read and follow the canonical `SKILL.md` first. This adapter defines Drive identity, navigation, raw-file handling, search, version-history use, and Drive-specific verification only. It does not redefine KB semantics.

---

# Runtime Configuration

Recommended project configuration:

```text
Knowledge Base Backend: google-drive
Knowledge Base Root: <exact Drive folder URL or ID>
Knowledge Base Name: <optional human-readable name>
Knowledge Base Registry: <optional exact Drive file URL or ID>
```

The active root is mandatory for mutation and ordinary KB retrieval unless it is already unambiguously established in current context.

Use exact Drive identity when available; do not identify a KB only by visible folder name.

A human-supplied exact root in the current conversation overrides the project default for that task.

---

# Optional Knowledge Base Registry

A configured registry may be used as a discovery surface for agent-managed Drive knowledge bases.

Recommended entry fields:

```text
Name
Root
Purpose
Status (optional)
```

Registry membership is discovery, not authorization.

Operate only on the KB explicitly selected by the human, configured by the calling project, or otherwise unambiguously active from current context.

Do not use the registry as a global search scope.

When explicitly initializing/registering/repointing/deactivating/removing a Drive KB and the human has requested the registry operation, update it after verifying Drive identity.

The registry and workflow files are infrastructure, never evidence or knowledge.

---

# Hard Drive Boundary

The active Drive root and its descendants are the complete normal Drive namespace for KB content operations.

Do not:

- create, edit, move, rename, delete, reorganize, or index KB content outside the active root;
- move a KB artifact out of the active root;
- search another registered KB merely because it looks relevant;
- search unrelated Drive content for context;
- read unrelated Drive files merely because they look useful.

External Drive material may be used only when the human explicitly supplies it, identifies it as source material, or explicitly authorizes its use.

---

# Drive Navigation

Prefer deterministic traversal from the configured root when paths are known.

Normal pattern:

```text
configured root
    ↓
verified child folder or index
    ↓
verified descendant
```

Use conceptual paths as the human interface:

```text
inbox/raw/
inbox/review/
inbox/approved/
source-archive/
evidence/
knowledge/
```

Drive item IDs are the stable storage identity when available.

Use Drive search when structured navigation is insufficient or the remembered location is uncertain.

Keep search scoped to the active KB root whenever the tooling permits. If a provider search cannot enforce root scoping directly, constrain candidates using verified parent/descendant identity before reading or mutating them.

---

# Raw Markdown Storage Integrity

KB `.md` artifacts must be stored as raw Markdown text/bytes, not as native Google Docs or another rich-document representation.

Do not use a conversion round-trip such as:

```text
Markdown text → Google Doc → export as Markdown
```

as the normal way to create or update KB Markdown.

Rich-document conversion can escape or transform syntax such as headings, emphasis, list markers, or links.

Use raw-file upload or raw-file replacement capabilities that preserve Markdown bytes faithfully.

If the available runtime cannot safely create or update raw Markdown without transformation, stop rather than substituting a Google Docs conversion workaround.

When a write path has meaningful serialization/conversion risk, perform one targeted structural check after the write to confirm Markdown syntax remains intact. Do not reread the entire file merely for ceremony.

---

# Drive Mutation Mechanics

## Create Raw Markdown or Raw Sources

Use Drive raw-file upload into the verified destination folder.

Preserve the intended filename and MIME type where the API permits.

Use the returned file ID/URL/parent information as the primary confirmation of success.

## Replace Raw Markdown

Use raw-file replacement on the existing Drive file when the operation is an edit to the same logical artifact. Preserve the same Drive identity when practical.

Do not convert the Markdown file into a native Google Doc for editing.

## Move / Rename

Before moving a Drive artifact:

1. verify its current parent;
2. verify the destination folder;
3. add the destination parent and remove only the verified source parent(s) that should no longer contain the item;
4. preserve unrelated parents when they legitimately exist;
5. use returned parent metadata as verification when sufficient.

## Delete

Delete only when the canonical workflow explicitly calls for removal or the human explicitly authorizes it.

Routine curation should move workflow items rather than delete the only substantive copy.

---

# Reading Raw and Difficult Sources

For stored non-native files such as PDFs, images, Office files, archives, audio, or video, use Drive raw-file download/fetch capabilities when full fidelity is required.

For ordinary readable text retrieval, use the cheapest bounded Drive fetch that answers the question.

For native Google Docs/Sheets/Slides that are explicitly supplied as source material, use the appropriate native read capability. They remain raw sources until authored evidence is approved.

Do not export or download large files unnecessarily when a bounded content read is sufficient.

---

# Search and Retrieval

Use the canonical progressive retrieval model first:

```text
knowledge/index.md
evidence/index.md
domain index
likely artifact
```

Use Drive search when:

- the conceptual path is uncertain;
- a remembered filename or phrase is needed;
- structure alone does not narrow enough.

Use concise distinctive terms, approximate dates, domain terminology, and synonyms.

Treat search results as leads and verify substantive claims from the actual KB artifact.

Do not use Drive search as a substitute for known direct paths.

---

# Drive Version History

Drive revision history may be used when the human asks when, how, or by whom a stored file changed and the provider exposes useful revisions.

For historical comparison:

1. ground the exact Drive file;
2. inspect current content;
3. list revisions;
4. fetch the relevant prior revision;
5. compare only as deeply as the question requires.

Revision metadata can support file-level attribution, but do not overstate it as exact per-character authorship.

Do not create a synthetic curation log merely because Drive revisions exist.

---

# Verification

Follow the canonical risk-proportionate verification rules.

Drive round trips can be expensive, so use mutation responses as evidence of success when they already establish the intended state.

Routine examples:

```text
create file
→ returned Drive ID + intended parent is enough when supplied

move file
→ returned final parent/location is enough when supplied

raw Markdown replace
→ successful replacement; add one small structural read only when transformation risk exists

index update
→ confirm expected entry only when the write response does not establish it
```

Avoid repeated `write → fetch → write → fetch` cycles unless a later operation depends on read-back.

Use stronger verification for large replacements, many-file moves, major restructures, or destructive operations.

---

# Failure Rules

Stop or narrow when:

- the configured Drive root cannot be identified reliably;
- a target cannot be verified as inside the active root;
- a mutation would overwrite unrelated material;
- raw Markdown cannot be stored without unsafe transformation;
- Drive permissions do not allow the required mutation;
- a source cannot be read faithfully enough to author evidence;
- the operation would create a partial workflow transition that cannot be completed safely.

Never claim persistence, movement, deletion, or modification succeeded unless the Drive mutation result or targeted verification establishes it.

---

# Google Drive Backend Standard

A healthy Drive deployment uses:

```text
SKILL.md
backends/google-drive.md
```

plus project or agent configuration identifying the active Drive root.

An optional registry may aid discovery across multiple Drive KBs, but it is not part of the KB's substantive content and does not authorize cross-KB access.
