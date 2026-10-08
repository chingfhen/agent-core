# Task: Decide where the Knowledge Base and canonical KB skill should live

**File:** `tasks/2026-10-08__knowledge-base-home-and-skill-canonicalization-bookmark.md`  
**Created:** 2026-10-08  
**Last Updated:** 2026-10-08  
**Priority:** Later  
**Status:** On Hold

**Goal:** Decide whether to keep personal and project knowledge bases on Google Drive or migrate some or all content to GitHub, and whether the canonical `knowledge-base` skill should be maintained in Agent Core instead of Google Drive.

**Why:** GitHub's direct links, readable rendered Markdown, version history and connected-agent edits feel substantially better for opening a known page. Google Drive was chosen for discoverable files, folder moves as human approval signals, and convenient everyday file management.

**Success Bar:** A deliberate, evidence-backed choice for **(a) KB content storage** and **(b) canonical skill source**, with a tested capture → review → approve → curate → retrieve workflow, clear access/security boundaries, and a reversible migration plan if anything moves.

**Chosen Direction:** **No migration approved.** Current recommendation: **keep KB contents on Drive; eventually consider Agent Core as the canonical *skill-source* repository**. Do not make `agent-core` the KB data store.

**Current State:** Comparative analysis captured. The Drive KB workflow and adapter remain canonical. Agent Core contains a noncanonical copy at `skills/knowledge-base/SKILL.md` for portability. No Google Drive KB files, registry, or global routing instructions have been changed.

**Next Action:** When revisiting, run a small *read-only* comparison of the same Markdown artifact on Drive and GitHub, then decide whether to (1) keep the hybrid, (2) make GitHub canonical for skill code only, or (3) pilot a **separate private** Git repo for a nonsensitive KB subset. Require new approval before any migration or changes to canonical routing.

**Blockers:** Design decision deferred; also evaluate write capabilities and identity/permissions in the intended agent harnesses. **Safety boundary:** `chingfhen/agent-core` is currently reported by GitHub as **public** (verified 2026-10-08). Do not commit private KB evidence, personal information, workplace content, or other confidential material there.

**Human Attention:** Follow the two sample links below on mobile and desktop; compare rendered reading, search, and moving an item through review/approval. Do not grant repository access or change visibility automatically.

## Short Recommendation

Separate **skill definition**, **knowledge content**, and **storage adapter**:

| Layer | Preferred home | Why |
| --- | --- | --- |
| Agent Core skills and distribution | `agent-core` (GitHub) | One versioned source with `agent-core sync`, clear code review and direct links |
| Canonical KB skill, **eventually** | `agent-core/skills/knowledge-base/` with adapter references, **if explicitly migrated** | Makes the workflow portable to personal agents; avoid two competing SKILL.md sources |
| KB evidence, knowledge, raw files, inbox/review/approved | Existing per-KB Google Drive roots | Easy file browsing, metadata search, direct moves, and independent private access boundaries |
| Other future KBs if Git-backed storage genuinely wins | **Separate private KB repo(s)**, not `agent-core` | Separation of concerns, privacy and different retention/versioning needs |

**Important:** Moving the *skill code* to Agent Core does **not** grant an agent access to Drive. The agent still needs an authorized Drive tool with raw Markdown read/upload/move/replace capabilities; otherwise the correct response is an access limitation, not a workaround. A local filesystem adapter remains independently useful. Keep approval and curation semantics stable across backends.

## Content Storage Comparison

| Need | Google Drive | GitHub repository |
| --- | --- | --- |
| Open a specific Markdown file | Direct file link; Google now supports formatted Markdown preview and .md editing | Excellent rendered Markdown page and permanent version links |
| Find by name/content | Drive UI search and folder browsing | Repository finder/code search and paths; search/indexing and access rules differ |
| Human approval by moving a file | Natural Drive file move `inbox/review/ → inbox/approved/` | Feasible by renaming/moving a path, but creates a Git commit; less natural as a lightweight approval gesture |
| Automated approval/curation | Drive adapter supports raw file operations if the connected agent exposes writes | Possible via Git operations and commits; requires implementing and testing a Git backend adapter, permissions and concurrency handling |
| Edit history/recovery | Drive revisions | Git commit history, diff and blame |
| Mobile/nontechnical use | Strong everyday file/folder UI | Strong reading links; moving, committing and conflict resolution more technical |
| PDFs, images and binary originals | Comfortable general-purpose storage | Possible, but potentially awkward for repository size/history, mobile use and binary lifecycle |
| Privacy | Per-folder/file permissions | Per-repository access model; cloned local copies and git history need explicit consideration |

GitHub *can* support the existing approval workflow; moving a Markdown file to a subfolder via its web editor is documented by GitHub. However, easy **individual** file moves in Drive were an intentional product requirement, not incidental implementation detail. Do not infer that GitHub is better simply because direct reading links are attractive.

**Security finding:** This Agent Core repository is **public**, despite some internal docs describing it as private. Verify actual visibility before any future KB decision, and never rely on a README claim as access control. Making Agent Core private could affect distribution/access; evaluate separately, not as a side effect of KB planning. For a Git-backed personal KB, use a private, distinct repository and test permissions.

## Three Real Options

1. **Drive content + Drive canonical skill (no change)** — lowest risk and maintenance; distribution of the skill to environments without Drive access remains inconvenient.
2. **Drive content + Agent Core canonical skill (preferred potential improvement)** — resolves dual skill-source maintenance while retaining Drive approval/file browsing. Requires deliberate migration of the *complete* canonical skill, backend references and adapter contract; update `global/AGENTS.md`, `personal-skills.toml`, and other links together; test Pi/other harness read/write before retiring the Drive skill source.
3. **Separate private Git-backed KB (pilot only)** — improved code-style reviewing, links and branching. Requires a new Git backend adapter, migration plan, review-approval UX validation, binary handling, and safe treatment of secrets/private records. Keep `agent-core` out of the data storage role.

**Not recommended:** Use the public `agent-core` repository itself as a personal/work KB, or put evidence and operational skill code together merely for convenience. Agent Core should distribute the tools/workflows, not own all personal knowledge.

## When This Resumes: Small Experiment

1. Open the same real `.md` file through Drive preview (switch to **Preview**) and a GitHub rendered Markdown link; compare readability on Android and desktop.
2. Find a file by partial filename and content; measure whether both feel natural without agent help.
3. In a test area with **nonsensitive synthetic files**, perform review → approved → curated moves using each UI and agent connector. Verify Markdown text is preserved; test recovery and bulk changes. Do not use real evidence as a test.
4. Confirm the exact integration available to Pi and work environments. A connector that only reads does not make a writable workflow.
5. If the hybrid wins, request approval for **skill-source canonicalization only**. Keep the Drive KB root/format untouched, then validate installation and one safe read/write cycle before changing canonical pointers.

## Evidence and Links

- [Example real Drive Markdown review artifact — OCBC CML work notes](https://drive.google.com/file/d/1G3AKeA_PlYISARf_4TvgwGbMehbmEhav/view) (personal, may require sign-in; do not copy to public GitHub).
- [Canonical KB skill on Drive](https://drive.google.com/file/d/1S6Y_RIRZUkxcY59v_XuRrVIi6LHYCubX/view) and [Drive backend adapter](https://drive.google.com/file/d/1fyZMXQq7YTm_X8fphdprjIl6BmXwZu1f/view).
- [Agent Core's noncanonical KB skill copy](https://github.com/chingfhen/agent-core/blob/main/skills/knowledge-base/SKILL.md) and [global routing](https://github.com/chingfhen/agent-core/blob/main/global/AGENTS.md).
- [Google: Preview and edit raw .md in Drive](https://support.google.com/docs/answer/18289341?hl=en).
- [GitHub: Move a file in the browser](https://docs.github.com/en/repositories/working-with-files/managing-files/moving-a-file-to-a-new-location).
- [GitHub: Search files and code](https://docs.github.com/en/get-started/learning-to-code/finding-and-understanding-example-code).

## Permission and Closure

This document records a **deferred decision**, not permission to replatform, edit the canonical KB workflow, change visibility, migrate files, grant connectors, or modify other repositories.

Close this task only after confirming the chosen storage/canonical skill arrangement, validating the required workflow, and syncing relevant durable Agent Core docs and guidance.
