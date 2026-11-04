# Task: Approval-gated original-source archival for Knowledge Base

**File:** `tasks/2026-11/knowledge-base/2026-11-04__approval-gated-original-archiving.md`
**Created:** 2026-11-04
**Last Updated:** 2026-11-04
**Priority:** Now
**Status:** Active

**Goal:** Keep ordinary KB capture unchanged, add explicit approval-gated archival of original source files, and deprecate the inbox-processing queue without disturbing existing files.

**Why:** The user manually preserves many work documents in an established archive and references exact files during discussion, then asks for ordinary `capture to KB`. A different case (a personal ring receipt, diamond certificate and pictures supplied in chat) needed the original bytes retained as well as the extracted knowledge. Ordinary capture correctly extracted knowledge but did not preserve binaries. There should be no unrequested file archival, automatic archive scans, or new processing-tracker system.

**Deliverables:** On branch `feat/kb-approval-gated-original-archive-20261104`, revise the canonical `skills/knowledge-base/SKILL.md` and its directly affected routing, authoring and backend references; reconcile directly contradictory Agent Core guidance; preserve this task and its `tasks/INDEX.md` entry.

**Success Bar:**
- `capture to KB` still performs record/index maintenance and bounded living-knowledge maintenance with **no original-file copy/move/delete**.
- In KB context, `archive originals`, `capture original too`, or equivalent explicitly requested original archival means capture plus archival, unless user explicitly requests archive-only. No automatic archival from the word `capture`.
- Before *any* new original archival, agent proposes **specific candidate source filenames and individual destination paths** using the configured archive root and **`YYYY-MM` based on archival date**. It **waits for approval** and respects selected/excluded files; even “archive everything” requires the proposed inventory.
- Copies original bytes only, never overwrites; preserve original filenames with collision-safe suffixes; verify hashes/bytes and store exact destination/provenance in corresponding KB records. Never delete sources by default. No new topic directories or processing ledger.
- Archive root belongs to the verified applicable AGENTS.md KB-owned routing section; when unconfigured/inaccessible, report and ask instead of inventing destination. Different workspaces can have different roots. Never leak employer data to personal/private external storage by assumption.
- Manually archived originals are handled through exact user-specified file references in ordinary capture. Agent reads the named files if accessible, notes exact locations, never scans the archive as a processing batch; missing files must be reported.
- `inbox/` and `process inbox` are deprecated as *active workflows*: do not migrate/delete pre-existing contents automatically; no copy-verify-remove queue lifecycle remains.
- KB-owned AGENTS.md section should be autonomously established/maintained on authorized KB maintenance, including safe adoption of unambiguous existing unmarked routing; retain customized constraints and avoid duplicates. Skill edits do not automatically change unrelated workspaces.
- No changes to `main`, no deployment, no automatic merge, no archival of any real user files during this implementation.

**Chosen Direction:** Approved by the human in the Nov 4, 2026 discussion. Use the existing canonical KB skill, no new separate skill, manifests, source-tracker, archive scan, or database.

**Current State:** Revised canonical skill, routing, source-provenance guidance, filesystem and GitHub adapters, and directly affected Agent Core guidance are implemented on the feature branch. Static reads/checks and GitHub comparison verify the changed files exist only on this branch; live harness execution and approved binary-archive copying have **not** been tested.

**Next Action:** Human reviews the branch diff/approved contract. If desired, run a controlled dry-run in a workspace with a configured archive and throwaway test originals; seek separate permission before merge or rollout to installed harnesses. **Do not merge to `main` without a separate request.**

**Blockers:** None for instruction changes. End-to-end runtime/archive tests require an accessible configured archive and approved test files; do not write real originals merely to validate skill prose.

## Decisions and constraints

- **Archive layout:** `<Knowledge Base Archive>/YYYY-MM/<original-name>` where `YYYY-MM` is archival date, identical in all workspaces. The root itself is environment-specific and established by applicable AGENTS.md.
- Existing personal KB configuration: `Knowledge Base Archive: C:\Users\tanch\.kb-archive`; do not copy this path to OCBC or other workspaces. Existing OCBC archive root must be read from its own guidance; don't guess.
- **Source identity:** Preserve a stable original locator (prefer workspace-relative) and distinguish a verified accessible file from a user-reported/inaccessible path. No global processed-file inventory.
- **Permission:** Explicit archive request triggers a *proposal*, not immediate copying. Written human approval of exact file selection is required before execution. KB capture may finish independently of an unfulfilled archive request; report partial result.
- Existing legacy inbox files and archives must not be modified or purged by this change.
- Git publication/commit boundaries in the existing KB skill and the Agent Core repo remain intact.

## Resume context

- `skills/knowledge-base/SKILL.md` — canonical operating behavior.
- `skills/knowledge-base/references/routing.md` — KB-owned AGENTS.md section.
- `skills/knowledge-base/references/authoring.md` — source provenance in records.
- `skills/knowledge-base/backends/{filesystem,github}.md` — actual storage constraints.
- `docs/workspace-configuration.md` — concise canonical project understanding.
- `skills/project-tasks/SKILL.md` and `tasks/INDEX.md` — task format, maintenance and navigation.
- This task's user-approved design is from the current ring-document archival conversation; personal ring files are **not** an authorized test/archive batch.

## Verification performed (2026-11-04)

- Read back all nine affected paths at the feature branch; verified skill and
  routing references, archive contract cues, task/index navigation and AGENTS
  markers are present.
- GitHub compared `main` to this branch: branch is ahead, not behind, with
  only the task, index, canonical skill, its references, Agent Core guidance
  and workspace-configuration doc changed. No source binaries were written.
- Static scenario checks cover unchanged capture, affirmative original-file
  selection, `YYYY-MM` naming, non-destructive retention, exact manual
  archive references, missing-file reporting, deprecation of inbox processing,
  safe routing adoption and GitHub backend limitations.
- **Not validated:** actual cross-harness activation, runtime approval
  prompting, binary fidelity against an archive or legacy AGENTS migration.
  No claims of those outcomes until independently exercised.
