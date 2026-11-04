# KB routing and first use

Read when configuration is missing, routing must change, or a discovery-cue
refresh is authorized. The Knowledge Base skill owns
`<!-- BEGIN KNOWLEDGE BASE -->` through `<!-- END KNOWLEDGE BASE -->`
in the verified applicable `AGENTS.md`. Do not assume that the current Git
checkout, user home or another workspace provides the target. A shared KB needs
no invented project identity.

## Resolve and register

1. Use the operation's explicitly selected KB location, then the applicable
   existing configuration. Preserve known root, backend, repository/ref/directory,
   optional external knowledge-page root, and archive-root identities.
2. During an **authorized KB-maintenance operation**, autonomously create or
   minimally refresh the marked KB section when it is missing, incomplete, or
   outdated. A separate "set up AGENTS.md" request is **not** required. Routine
   read-only recall and merely changing/publishing the skill do not authorize
   workspace guidance writes.
3. Where the same `AGENTS.md` has unambiguous **legacy unmarked KB routing**,
   adopt those *exact established values* into the managed section in a single
   narrow edit. Retire only the now-duplicated KB routing lines; retain
   surrounding confidentiality, publication restrictions, custom guidance,
   positions and unrelated sections. Do not create competing path tables.
   If ownership, legacy path base, or conflicting directions are unclear, stop
   and ask rather than silently moving or duplicating guidance. Existing
   customized stricter write gates still apply.
4. If a compatible KB resource is unambiguously present but its routing is
   missing, reuse and register that confirmed resource within authorized scope
   rather than inventing an additional one. If neither resource nor
   configuration exists, propose `.work-context/knowledge-base/` beneath the
   confirmed workspace and ask for initialization approval.
5. **Original archive routing is optional for ordinary capture and retrieval.**
   Configure/reuse `Knowledge Base Archive` when the human wants original
   archival. If absent, propose `.work-context/archive/knowledge-base/` or
   another specifically authorized separate root and obtain approval before
   archival. Do not create archive folders or copy originals during ordinary
   capture. There is no local-home fallback.
6. Report inaccessible configured locations or incompatible ownership.
   Preserve explicit cross-repository and remote identities; do not substitute
   a personally configured archive for a different workspace.

## Section

Creation-time example only. Replace with **confirmed** locators and retain
human-customized instructions; omit unavailable optional fields. Keep detailed
copy/hash procedures in the skill/backends, not in AGENTS.md.

```markdown
<!-- BEGIN KNOWLEDGE BASE -->
## Knowledge Base
Knowledge Base Root: .work-context/knowledge-base/
Knowledge Base Archive: .work-context/archive/knowledge-base/

For explicit KB retrieval or relevant prior context, consult the confirmed root's
index, targeted records, relevant living knowledge pages and managed artifacts.
Read-only lookup does not require the maintenance skill or grant write permission.
Do not browse original archives by default. A precisely referenced original
may be read if needed and accessible; report missing/unreadable sources.

Load knowledge-base for human-requested capture, managed-artifact maintenance,
original archival or routing changes. Normal "capture to KB" extracts knowledge
and references identified sources **without copying or moving originals**.
Archiving originals is a separate explicit, approval-gated addition: present
specific source files and proposed <Knowledge Base Archive>/YYYY-MM/ destinations,
then await the human's file selection before writing. Never assume an archive
root is accessible merely because it is configured. Legacy inbox processing is
retired; leave pre-existing inbox data untouched.
<!-- END KNOWLEDGE BASE -->
```

New section-relative paths resolve from the declaring `AGENTS.md` directory,
never cwd; preserve recorded bases for legacy workspace-relative paths.
`YYYY-MM` is the standard original-archival month folder, based on archival
date, regardless of the root's environment-specific spelling. The section
stores confirmed routing and essential activation cues, not a file registry,
historical archive catalogue, or copy of the skill.

## Targeted maintenance

Markers/headings/labels and concise example cues are defaults. During each
authorized maintenance pass, reread the applicable guidance and preserve valid
customized behavior, ownership boundaries, other sections, and ordering. Skip
equivalent existing cues. Refresh only relevant routing/discovery guidance;
routine content records or archive locators do not become new AGENTS.md entries.

Refuse duplicate, incomplete, nested or ambiguous markers and unsafe paths.
For safe legacy unmarked adoption, check that all migrated path lines clearly
belong to the same KB and retain the rest verbatim. Recheck before writing,
reconcile concurrent edits, read back, and verify the owned diff and actual
locators. Report partial routing failures without losing valid KB writes.
Do not migrate old content or invent a destination solely to normalize guidance.
