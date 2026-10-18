# Task: Migrate the General Knowledge Base into the existing private GitHub repo

**File:** `tasks/2026-10-08__knowledge-base-home-and-skill-canonicalization-bookmark.md`

**Created:** 2026-10-08

**Last Updated:** 2026-10-16

**Priority:** Completed

**Status:** Closed

**Goal:** Use the current Agent Core KB skill with the existing GitHub-backed local Markdown KB, preserving useful legacy content and recent artifacts.

**Final State:** Migration applied, independently checked, committed, and pushed to private `chingfhen/knowledge-base`, branch `main`. Remote head and representative remote file contents verified; KB worktree clean. Commit: `ab97fa8684385922cc1a3a3319a3abe2d6ba8399` — `Migrate knowledge base to current Markdown layout`.

**Next Action:** None for this migration. Use the new KB. The explicitly held policy-sensitive draft is excluded from publication and remains recoverable; publishing it requires separate clearance, not reopening completed migration mechanics.

**Permission:** Human approved Luna execution, KB commit, and task closure. Parent retained final acceptance/publication. No Agent Core commit was requested or made.

## Canonical locations and daily use

- Git worktree: `C:\Users\tanch\Documents\Github\my-knowledge-base\knowledge-base`
- **Active KB:** `C:\Users\tanch\Documents\Github\my-knowledge-base\knowledge-base\knowledge-base`
- Remote: `chingfhen/knowledge-base`, `main`, directory `knowledge-base/`.
- Browse: https://github.com/chingfhen/knowledge-base/tree/main/knowledge-base
- Canonical workflow: `C:\Users\tanch\.agent-core\skills\knowledge-base\SKILL.md` and its references; unchanged by migration.
- External archive: `C:\Users\tanch\.kb-archive`.
- Repo `AGENTS.md` now routes to these locations and the current skill. Outside this repo, explicitly supply the active KB root; remote sessions must select the owner/repo, branch, and directory. Global routing and installed skill publication were not changed.
- Ordinary local capture does not imply Git commit/push. This migration's publication permission does not establish automatic future publication.

The original nested content root was retained intentionally: the user-supplied path is the Git root, and its inner `knowledge-base/` holds the content. No new repository, symlink, synchronization service, or competing layout was created.

## Completed migration

Luna (`openai-codex/gpt-6-luna`, xhigh) was the sole migration writer. Parent inspected reports, reran preservation/live validation, audited source-to-target changes and the Git index, then committed and published.

Final active content:

- 40 records under `records/YYYY-MM/<topic>/`.
- 18 knowledge pages.
- 8 managed artifacts, including all four named recent-guide retention anchors.
- 9 pending inbox inputs, preserved without processing.
- Five rebuilt navigation indexes; 80 inner-KB files total, plus the scoped root `AGENTS.md` update.

All 14 old Drive review files were accounted for: 13 migrated, one explicitly held outside publication. Review/draft/unexecuted caveats were retained; migration did not imply human validation. Original bodies were preserved apart from necessary links/provenance. Historical local payment-card synthesis was retained as a dated record rather than presented as a competing current page.

The old active `evidence/` hierarchy was retired after verification. Sixteen original local PDF/image evidence files remain byte-preserved in external snapshots/rollback copies and in existing Git history, not ordinary KB recall. Pending raw inputs remain in `inbox/`. Drive was left untouched, including its obsolete `_workflow/`; it is not the operational skill authority or a dual-write destination.

## Verification and publication evidence

- 61 local snapshot files verified against original SHA-256 values; independent rollback copy verified.
- 53 full Drive downloads preserved; source IDs/paths/type/timestamps rechecked before apply with no observed additions, deletions, moves, or modifications. Source API exposed no revision/checksum; local hashes prove downloaded-byte preservation, not unavailable remote revision identity.
- All 81 final files match verified staging, including indexes and guidance.
- Four required recent guides remained byte-identical locally to complete downloads, including qualifications and Thai/English content.
- 115 relative Markdown links resolve. Representative root/record/knowledge/managed retrieval checked.
- Parent inspected source-to-target differences: provenance additions and scoped link/historical-status changes, not substantive compression of retained documents.
- Parent verified every final file against the Git index using existing Git line-ending normalization and confirmed all staged changes were within `AGENTS.md` and `knowledge-base/`.
- Unstaged diff check passed. After staging imported files, the ordinary cached whitespace check reported 75 source-inherited Markdown hard-break/EOF warnings; parent verified each against preserved originals and intentionally retained them instead of rewriting artifacts. Do not report the cached check as warning-free.
- GitHub API verified repository private, not archived, default branch `main`. Normal push succeeded, live remote SHA equals the commit above, and authenticated readback matched committed root index, a recent managed guide, and the October records index.
- Final KB Git worktree is clean. Git's existing LF/CRLF normalization remains unchanged.

Authentication was resolved using Git Credential Manager browser login. Global Git also uses AWS CodeCommit credentials and path-specific credential handling. Network operations used only command-scoped overrides:

```text
git -C <repo> -c credential.helper= -c credential.helper=manager -c credential.useHttpPath=false <network-command>
```

No persistent credential/Git configuration was changed and no secrets were written to reports.

## Preservation, exception, and recovery

Private migration evidence and originals:

`C:\Users\tanch\.kb-archive\migrations\2026-10-15--drive-to-github\`

Key files/directories: `snapshot/local/`, `snapshot/drive-source/`, `live-pre-apply-knowledge-base/`, `live-pre-apply-AGENTS.md`, `local-disposition-map.tsv`, `drive-disposition-map.tsv`, `staging-complete-manifest.tsv`, `post-apply-path-audit.tsv`, `post-apply-report.md`, and `post-apply-verification.txt`.

The one-off `verify_post_apply.py` checks the pre-commit handoff state and therefore expects the old HEAD and an empty index. Its prior passing result is retained; do not run it after publication and mistake its expected HEAD failure for content loss. Validate current files against manifests and the published commit instead.

**Exception:** One potentially employer/project-policy-specific draft is preserved in the Drive snapshot and original Drive location but not published. Exact identity and reason are in the private report/mapping. No additional classification or publication is authorized without clearance. This is an explicit held disposition, not lost content.

Existing sensitive Git history was not rewritten. Source archives are local-only and are not automatically available to remote agents. No OCR, inbox processing, advice fact-checking, or broad content refresh was performed.

If rollback is explicitly requested, prefer a normal revert of the migration commit and use verified snapshots for original-byte recovery. Do not force-push, delete Drive originals, or discard snapshots as a side effect of closing this task.

## Durable guidance

The KB repo's updated `AGENTS.md` owns location/routing guidance; the current Agent Core skill owns workflow. No Agent Core production skill or durable docs changes were required. This closed task records completion and recovery pointers, not a competing KB workflow.
