# Filesystem Backend Adapter

## Purpose

Implement the canonical Knowledge Base workflow on an ordinary filesystem.

Read and follow the canonical `SKILL.md` first. This adapter defines storage mechanics only. It does not redefine KB semantics.

Use this backend when the active root is a local or mounted filesystem path and no storage-specific backend such as Google Drive is selected.

No Git repository is required or assumed.

---

# Runtime Configuration

Recommended project configuration:

```text
Knowledge Base Backend: filesystem
Knowledge Base Root: <exact filesystem path>
Knowledge Base Name: <optional name>
```

The exact configured root is authoritative.

When no exact root is configured, a uniquely identifiable nearby directory matching `*-knowledge-base` may be used only when current context makes the intended KB unambiguous. Otherwise ask rather than guessing.

The `*-knowledge-base` suffix is a discovery convention, not a validity requirement.

---

# Filesystem Boundary

Treat the configured root and its descendants as the complete writable KB namespace.

Before mutation, resolve the root to a stable normalized path when the runtime supports it.

Do not:

- write outside the root;
- follow a symlink, junction, mount indirection, or path traversal outside the root for KB mutation;
- delete or overwrite unrelated files;
- infer that a sibling directory belongs to the KB merely because its name looks related.

External source/context files may be read only when explicitly supplied or authorized by project configuration or the human. They remain outside KB ownership.

---

# Required Capabilities

The backend needs ordinary filesystem operations:

```text
list directories
read files
create directories
create files
replace files
move / rename
copy when explicitly needed
search filenames and text
remove files only when authorized by the canonical workflow
```

If the environment cannot safely perform a required operation, stop rather than simulating persistence.

---

# Markdown Integrity

KB Markdown must be stored as raw UTF-8 Markdown text.

Do not route Markdown through rich-document conversion merely to save it.

Preserve:

- headings;
- lists;
- code fences;
- links;
- emphasis;
- frontmatter;
- literal paths and identifiers.

Use the filesystem's normal text-file write mechanism.

---

# Mutation Mechanics

## Create

Create required parent directories first, then write the intended file.

Never silently overwrite an existing unrelated artifact. When filename identity is uncertain, use a collision-safe name or resolve the ambiguity first.

## Replace

When rewriting an existing knowledge page or index, preserve unrelated content and write only the intended new complete contents.

Prefer a temporary-file-then-rename pattern when the runtime supports it cheaply and it materially reduces partial-write risk. Do not add elaborate transactional machinery for ordinary low-risk edits.

## Move / Rename

Use a filesystem move/rename operation when possible so content remains unchanged.

After moving evidence or workflow-state artifacts, repair only directly affected links or provenance paths required by the canonical workflow.

## Delete

Delete only when the canonical workflow explicitly calls for removal or when the human explicitly authorizes it.

Routine curation normally moves items between workflow states; it should not delete the only copy of substantive material.

---

# Search and Retrieval

Prefer cheap filesystem narrowing:

```text
known path
→ direct read

known topic
→ index / filename search

remembered phrase
→ text search within the active root

approximate date
→ date-prefixed filename filtering
```

Use tools such as filename search, recursive grep, ripgrep, or equivalent capabilities when available.

Do not scan unrelated directories outside the configured root.

---

# Version History

This backend does not guarantee historical revisions of mutable knowledge pages.

Do not create synthetic change logs, snapshots, or a home-grown version-control system merely to imitate Git or Drive history.

Traceability still comes from:

```text
current knowledge
→ ## Evidence
→ permanent evidence
→ source-archive when exact original fidelity matters
```

If the host filesystem independently provides version history, it may be used when helpful, but the KB workflow does not depend on it.

---

# Verification

Follow the canonical risk-proportionate verification rules.

For normal filesystem operations, cheap checks are usually enough:

```text
create → target exists
move   → target exists and source no longer occupies the pending state
edit   → write returned successfully; inspect only the affected portion when needed
index  → expected entry is present when not otherwise established
```

Do not reread entire files after every successful local write.

Use stronger verification for destructive or large structural changes.

---

# Failure Rules

Stop or narrow when:

- the root path is missing or ambiguous;
- the root cannot be accessed safely;
- a path resolves outside the root;
- an existing target would be overwritten ambiguously;
- required read/write/move capability is unavailable;
- the operation would leave a partial workflow state that cannot be completed safely.

Never claim a filesystem mutation succeeded without an observed successful operation or minimal targeted confirmation.

---

# Filesystem Backend Standard

A healthy filesystem deployment should require only:

```text
SKILL.md
backends/filesystem.md
```

plus project or agent configuration identifying the active root.

No Git repository, database, external registry, or additional infrastructure is required.
