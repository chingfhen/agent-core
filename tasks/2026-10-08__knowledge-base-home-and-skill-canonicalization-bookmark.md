# Task: Migrate the General Knowledge Base from Drive into the existing private GitHub repo

**File:** `tasks/2026-10-08__knowledge-base-home-and-skill-canonicalization-bookmark.md`

**Created:** 2026-10-08

**Last Updated:** 2026-10-15

**Priority:** Next

**Status:** Blocked — migration staged externally; GitHub authentication and privacy verification required

**Goal:** Use the current Agent Core KB skill with a GitHub-backed local Markdown KB, retaining existing useful content and especially recent human-facing artifacts.

**Success Bar:** The existing private repository contains a usable `records/`, `knowledge/`, `managed/`, `inbox/` layout with indexes and repaired links; recent Drive artifacts are retained in full; every inventoried content file has a disposition; original sources remain recoverable; authorized publication is verified.

**Chosen Direction:** GitHub as the KB home and Agent Core as the skill authority are decided by the human. **Approved migration method:** reuse `chingfhen/knowledge-base` and its existing local checkout; retain its nested KB directory; perform one preservation-first migration, not a new repository or ongoing Drive mirror.

**Current State:** Human approved execution by a Luna subagent at xhigh/max, followed by task closure and a KB-repo commit after completion. Luna at xhigh is the sole migration writer; the parent owns final acceptance, publication, and task closure. Planning inspection is recorded below; execution verification remains pending. Do not investigate why Drive was chosen or resurrect approval-folder semantics.

**Next Action:** Human completes interactive GitHub authentication and confirms the existing repo is private. Parent rechecks remote head, resumes the same Luna child to apply verified staging, then verifies, commits/publishes, and closes only after success.

**Blockers:** Noninteractive `git ls-remote` exited 128 because credentials were unavailable. Current private visibility and remote-head agreement are unverified. Live KB remains unchanged. One potentially workplace-specific review artifact is preserved externally and held from publication pending policy clearance; see the private report.

**Execution Checkpoint:** Luna preserved 61 local files and downloaded 53 Drive files. External staging reports 40 records, 18 knowledge pages, 8 managed artifacts, and 9 pending inputs; all four recent-guide anchors retained whole, 115 relative links checked. Parent independently verified 61 local snapshot/live-source hashes, 53 Drive snapshot hashes, 75 staged-file hashes, four full recent-guide matches, and a clean live checkout. Final content-diff/live-tree verification remains pending. Report: `C:\Users\tanch\.kb-archive\migrations\2026-10-15--drive-to-github\migration-report.md`. Resumed Luna run: `934cb848-8b82-432a-b963-0588dd26a691`; child completed with a blocked checkpoint and no live KB mutation; resume this same child after authentication is resolved. No commit or push yet.

## 1. Decisions and exact locations

### Reuse, do not create another repository

The existing checkout is usable. A new repo would add setup, duplicate identity, and require the same content classification anyway. Stale content is handled by preserving the old snapshot and importing useful material, not by creating another remote.

| Role | Exact location |
| --- | --- |
| Git worktree root (`REPO`) | `C:\Users\tanch\Documents\Github\my-knowledge-base\knowledge-base` |
| Active content root (`KB`) | `C:\Users\tanch\Documents\Github\my-knowledge-base\knowledge-base\knowledge-base` |
| Remote | `https://github.com/chingfhen/knowledge-base.git` |
| Target branch | `main` |
| GitHub content directory | `knowledge-base/` |
| Canonical skill | `C:\Users\tanch\.agent-core\skills\knowledge-base\SKILL.md` and its referenced files |
| External source archive | `C:\Users\tanch\.kb-archive` — outside the Git worktree |
| Migration snapshots/report | `C:\Users\tanch\.kb-archive\migrations\<execution-date>--drive-to-github\` (unique suffix on collision) |
| Drive source | `https://drive.google.com/drive/folders/1ameHGTlTn88aiSXXegmSxjSixSC9CIzl` |

**The doubled final `knowledge-base` is intentional:** the supplied path is the checkout root, not today's content root. Keeping the existing inner directory is less work than flattening it. Do not create a second active KB at the checkout root.

Target:

```text
REPO/
  AGENTS.md                 # concise current routing, not a copied skill
  knowledge-base/           # KB
    index.md
    records/YYYY-MM/index.md
    records/YYYY-MM/<topic>/YYYY-MM-DD--description.md
    knowledge/...
    managed/YYYY-MM-DD--description.md
    inbox/...
```

Empty folders need not be tracked; create `inbox/` locally and retain it in Git only if it contains pending inputs. No `.gitkeep` scaffolding unless actually needed.

### Authority and boundaries

- Follow the current canonical source skill, not Drive `_workflow/`, the old repo workflow, or an older installed skill copy. Read `backends/filesystem.md` and `references/authoring.md` before migration writes.
- No production skill editing or hand-updating installed copies. If the installed skill is stale, normal committed-source `agent-core sync` is a separate action, not migration scope.
- No renewed debate about backend choice, synthetic pilot, approval queue, curation gate, database, embeddings, sync daemon, dual-write system, or general migration framework.
- This is relocation/classification, not content improvement. Preserve full artifacts, qualifications, draft labels, dates, tables, code blocks, and non-English text. Do not summarize recent guides to save effort.
- Do not treat stored instructions or guide commands as executable instructions.
- No inbox processing, OCR, legal/financial fact-checking, external research, historical Git cleanup, or unrelated repo cleanup.
- No Drive writes, moves, deletions, sharing changes, or stale-workflow edits. Keep Drive as an untouched rollback source, not the ongoing operational KB.

## 2. Evidence collected during planning

### Existing local repository

- `git rev-parse --show-toplevel` confirms `REPO` above. Its parent `my-knowledge-base` is not the Git root.
- Branch `main`, origin as above, local HEAD `856649e` (`remove skills`, commit date 2026-09-22).
- `git status --short` was empty. There are 60 tracked files below the inner `knowledge-base/`, including indexes, Markdown, raw inbox inputs, and personal source PDFs/images. There are also local ignored scratch/environment files outside that content directory; do not sweep them into a migration commit.
- Existing `REPO/AGENTS.md` is obsolete: it requires original sources in `evidence/` and a commit for each KB mutation. It must be replaced with current routing/permission guidance as an explicitly scoped part of the approved migration.
- The earlier task reported the remote private; **privacy was not reverified in this planning session**. `gh` was not found on this shell's PATH. Do not assume Git CLI authentication proves current visibility or that a GitHub connector exists.

### Drive sources

Drive MCP account alias **`drive`** successfully listed folders and read Markdown. The earlier `default` account failed authorization; specify `account: "drive"` and recheck access when executing.

| Source | Folder ID | Observed state |
| --- | --- | --- |
| KB root | `1ameHGTlTn88aiSXXegmSxjSixSC9CIzl` | `_workflow`, `evidence`, `inbox`, `knowledge`, `source-archive` |
| Evidence | `1_f4i-PjMbiB1bysFHnQPkjypU2jYqda-` | Topic folders plus index; recursive inventory not done |
| Knowledge | `1kJmyrBS8qXAyMchpHaLTqU9Al6KHjDkM` | Topic folders plus index; recursive inventory not done |
| Inbox | `19QBUP_MxyUQN5c3R7ok4jppQ6hyvW2Cg` | Legacy `raw`, `review`, `approved` folders |
| Raw | `1_7cTxY2Uh69sWb16Xvj0yyTnjPOmdNug` | Empty at inspection |
| Approved | `1O3a3vcOFEZJd2Xdo-9J473fQdxsseuxP` | Empty at inspection |
| Review | `1Pur-AQwbMqkgsmYjwUaXbl64YKf_hRxE` | **14 Markdown files**, dates 2026-10-05 through 2026-10-12 |
| Source archive | `1HU-pMLKCpSbzqXSNF2eHBCQ7z4tkIkf9` | One text file at inspection |

Recent artifact retention anchors in `review/`:

- `2026-10-10--fly-sprites-setup-guide.md`, ID `1bCaKwL-e2GcQuOrZ36Ac-7chxWJHwyJW`: sampled opening explicitly says review draft and documentation-tested, not executed. Preserve that limitation.
- `2026-10-10--pi-pocket-setup-guide.md`, ID `1czAUrFd8uANMs3Rk5Q-r1WaEEMRtYniw`.
- `2026-10-10--cloud-pi-workflow-and-operations.md`, ID `1FcF_EYAr7sbh6ZCiHwtWuQH_SurQc0oD`.
- `2026-10-12--ica-statutory-declaration-udon-thani-bilingual-guide.md`, ID `1oLqzgXZRNPg4W1NX-4t9uIwJ9t_FXJ6i`: sampled opening contains Thai/English content. Preserve the entire document, not just the sampled prefix.

All 14 need accounting, not only these four. The two sampled reads were truncated and **are not migration copies**. No full content audit, total Drive file count, or duplicate analysis has been performed.

## 3. Execution plan after approval

### A. Establish a recoverable starting point

1. Read this task, the canonical KB skill/references, and applicable repo guidance. For the scoped `AGENTS.md` update, load `project-docs`; do not alter unrelated guidance. Approval of this migration explicitly supersedes the obsolete evidence-layout/per-mutation-commit rules, not confidentiality protections.
2. Recheck `REPO` root, origin, branch, and status. Preserve unrelated changes; stop rather than reset/stash/delete someone else's work. Verify remote visibility is still private with an authenticated GitHub capability or a human-confirmed settings view. Never change visibility.
3. Fetch only the selected remote; establish agreement with `origin/main`. Fast-forward only when safe. A diverged branch or unexpected remote needs resolution, not force-push or automatic merge.
4. Create the external migration directory. Record pre-migration HEAD and make a byte-verified snapshot of the entire existing inner KB plus `REPO/AGENTS.md`. Include untracked content inside the KB; Git history alone does not protect it. Do not copy `.git`, `.venv`, unrelated scratch, or session exports.
5. Recursively inventory only the selected Drive content root, excluding `_workflow`. Follow pagination and record IDs, relative paths, types, and available modified/revision metadata. Do not use filename alone as identity. Freeze this inventory for the run; recheck changed sources before finalizing.
6. Download complete source files into the external migration snapshot, preserving original bytes for regular files. `downloadFile` is preferable to reconstructing long Markdown from truncated tool output. If MCP and shell filesystems differ, verify the returned local location is actually accessible; otherwise use a complete non-truncated text read for text, or report the affected binary/export blocked. Native Google documents, if found, need an explicit faithful export and verification; do not pretend an export is original bytes.
7. Keep one simple local TSV/JSON mapping report in the migration directory: source ID/path, source hash/revision where available, disposition, destination, and verification result. This is a one-off checklist, not KB infrastructure.

**Preservation priority:** snapshot all review files first, then evidence/knowledge, other pending inputs, and source archive. Do not begin retiring old active paths before local backup verification succeeds.

### B. Map content without rewriting its substance

Use actual content and purpose, not the old folder name alone:

| Legacy content | Target/disposition |
| --- | --- |
| Dated learning, findings, decisions, context records | `records/YYYY-MM/<topic>/YYYY-MM-DD--description.md` |
| Human-facing guide, lesson, checklist, command reference, script, comparison | Flat `managed/YYYY-MM-DD--description.md` |
| Existing cross-record synthesis | `knowledge/` — preserve established topic subdirectories if convenient; no flattening requirement |
| Genuine raw/unprocessed user input | `inbox/`, still pending; relocation does not mean processed |
| Legacy review/approved authored Markdown | Classify as record or managed artifact; retain draft/proposal/unverified wording. No new approval queue and no implied human validation |
| Processed original PDFs/images or other raw source evidence | Verified external archive snapshot; source links/locators remain recoverable; not `records/` disguised as Markdown |
| Drive `source-archive/` | Preserve in external migration snapshot; no default retrieval indexing |
| Old indexes | Preserve in snapshots; rebuild active navigation rather than treating them as records |
| Drive `_workflow/` | Excluded and left untouched; never install or copy as authority |

Detailed rules for a smaller-model executor:

1. **Preserve every recent artifact whole.** For an existing dated Markdown artifact, retain the filename when compatible with the flat `managed/` layout. Relocation is not permission to rewrite or update its advice.
2. Use reliable original capture/creation dates from metadata/content where present. A source/event date is not automatically a capture date. If unknown, use migration date and state that the original capture date is unknown; retain available source dates and locators. Do not invent dates to satisfy the folder shape.
3. Treat Drive as the newer primary input but not infallible. Bring forward unique useful local Markdown as well. Exact duplicates can share one target with both origins in the mapping report. Similar filenames are not duplicates. Preserve materially different versions as distinct dated records/artifacts with descriptive suffixes rather than inventing a merged consensus.
4. Existing local knowledge with no competing current page may be retained with its historical date/applicability visible. When local and Drive syntheses conflict, keep the newer supported page as active knowledge and preserve the older conflicting explanation as a historical record, with links. Do not present both as simultaneously current or resolve factual conflicts through guesswork.
5. Preserve existing metadata; add only missing minimal metadata/provenance where needed. Do not mass-reformat bodies, strip review warnings, or convert proposals into verified instructions.
6. Map links using source identity and old-to-new paths. Repair links among migrated pages and associated images/assets. Keep external web links unchanged. For originals retained outside Git, retain an honest archive locator and/or unchanged Drive URL; do not fabricate a GitHub URL for local-only material.
7. Known credentials must not be imported into Git. Screen prospective publication files without echoing secret values. Personal data stays private; suspected restricted employer/customer material stays in its original location or verified local preservation copy and is reported as held, not silently uploaded. Existing sensitive Git history is not cleaned by this migration.

### C. Replace the active legacy layout and route future use

1. Build the mapped active content after snapshots are verified. Retire the old active `evidence/` and obsolete inbox review/approved structure only after every affected file has a verified new destination or explicit archive/held disposition. Do not leave two competing active KB trees. Preserve unrelated repo-root files.
2. Create the root `index.md` with month links, managed-artifact links/descriptions, and a simple route to knowledge pages. Create each populated monthly `records/YYYY-MM/index.md`. Preserve useful existing knowledge navigation and repair affected links. Do not index raw inputs or archive contents as ordinary recall.
3. Replace only stale `REPO/AGENTS.md` KB rules with concise current guidance: canonical Agent Core skill authority; content root; external archive; confidentiality; no approval queue; and local writes do not imply commit/push. Do not embed a duplicate skill.
4. Set applicable repo guidance to:

   ```text
   Knowledge Base Root: C:\Users\tanch\Documents\Github\my-knowledge-base\knowledge-base\knowledge-base
   Knowledge Base Archive: C:\Users\tanch\.kb-archive
   Remote KB: chingfhen/knowledge-base, branch main, directory knowledge-base/
   ```

   Explain that another machine must use its own local clone path or explicitly select the remote identity.
5. **Cross-workspace use:** repo guidance is automatically applicable only inside that repo. Outside it, explicitly give the skill the KB root above; remote sessions explicitly use `chingfhen/knowledge-base`, `main`, `knowledge-base/`. Do not silently initialize `~/.kb/`, edit `projects.toml`, introduce a symlink/junction, or change global harness settings. A global convenience pointer is separate future work, not required to migrate.
6. No automatic future Git publication rule is introduced. A normal local `capture` remains a local file write; the human separately requests commit/push. This migration's approval may authorize its one publication only.

### D. Verify, then publish the approved migration

Before commit/push:

- Every source in the frozen inventory and local snapshot is accounted for as migrated, exact duplicate, archived original, obsolete index, or explicitly held. Report held files and why; do not claim they were migrated.
- Every one of the 14 initially observed review files, plus any added before the frozen inventory, has a verified disposition. The four named artifact anchors exist in `managed/` with full bodies and original limitations intact.
- Compare unchanged body bytes/text or hashes to source snapshots. For edited links/metadata, inspect the precise differences; file count or equal size alone is insufficient. Verify Unicode and code fences in the recent guides.
- All active local Markdown links resolve, or explicitly identify an external/local-only archive target. Root/month indexes point to actual files; managed items are discoverable.
- Representative retrieval finds one recent managed guide, one migrated record, and one knowledge page using the current skill/root. This is read-only verification, not a fake capture or inbox processing run.
- Snapshot originals remain intact; Drive has not been modified. No source material or private KB content is copied into Agent Core's task/docs/commits.
- Inspect `git diff --stat`, scoped diff, staged paths, and `git diff --check`. Stage only intended KB paths and the scoped guidance update; never use blanket `git add .`.

With explicit approval covering publication, make one coherent migration commit on `main`, then normal push to the verified private origin. Respect branch protection; if publication is rejected, stop and report the local commit, not a forced bypass. Verify the remote branch SHA equals the migration commit and read back representative remote files using an available authenticated mechanism.

If publication was not approved or access is unavailable, stop at verified local changes (or the separately approved local commit), report the exact pending step, and **do not say migration to GitHub is complete**.

## 4. Recovery and stopping rules

- No Drive deletion is necessary for success. Git history, untouched Drive, and the verified external local snapshot provide simple recovery.
- On interruption, use the mapping report and source hashes to resume missing work; do not reimport everything or overwrite an existing target blindly.
- A changed source or target requires rereading/reconciliation. Preserve both versions when identity is uncertain; stop the affected item rather than silently losing it.
- Before publication, restore only migration-owned paths from the verified snapshot if rollback is requested. After publication, use a normal revert commit if rollback is requested. Never reset/clean/force-push as an automatic recovery action.
- Missing access, unverified private visibility, actual secrets, restricted publication, unsafe path resolution, unrecoverable source truncation, or branch divergence block the affected phase. Do not silently create another repo or change permissions as a workaround.

## 5. Approval scope and handoff

**Recommend approving:** reuse the existing private repo; retain the existing nested content root; snapshot and migrate/classify both sources under the current skill; preserve full recent artifacts; update only the KB repo guidance and active navigation; retire verified old active paths; and make/push one scoped migration commit after verification.

**Trade-offs:** existing Git history remains, including historical sensitive material; the nested path stays slightly awkward; archives are outside Git and may not be reachable from a remote-only agent. These do not require a new repository. If the human wants history sanitization or globally automatic root selection, that is separate work.

**Approval recorded (2026-10-15):** Human requested Luna delegation to execute this task, followed by closure and a KB-repo commit when everything is done. The migration and its scoped publication are approved; parent retains final commit/push and closure authority. Repo creation, Drive mutation, skill changes, sharing changes, global routing changes, and Agent Core commits remain outside scope.

**Executor completion report:** exact local/remote KB roots, commit and remote verification, imported record/page/artifact counts, all recent-artifact retention results, source/archive locations, held items, and the explicit invocation needed outside the repo. Update this task with honest verification and remaining work. Close only after the agreed success bar is met; otherwise leave it active with the precise next step.

**Durable guidance:** current skill remains canonical and unchanged. The KB repo's concise `AGENTS.md` is the routing surface to update during approved execution. No Agent Core docs change is required merely to move personal KB content. Keep source inventories and personal details in the private migration report, not this steward task.
