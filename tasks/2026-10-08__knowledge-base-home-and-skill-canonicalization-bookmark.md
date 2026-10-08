# Task: Decide where the Knowledge Base and canonical KB skill should live

**File:** `tasks/2026-10-08__knowledge-base-home-and-skill-canonicalization-bookmark.md`  
**Created:** 2026-10-08  
**Last Updated:** 2026-10-08  
**Priority:** Later  
**Status:** On Hold

**Goal:** Choose the best long-term home for Markdown knowledge-base content, its review/approval workflow, and the canonical `knowledge-base` skill.

**Why:** GitHub provides excellent clickable, rendered Markdown and agent-accessible files. The existing Drive choice was driven by filename search and moving review files to approved, but both requirements may be met by a Git-backed KB with agent search and VS Code.

**Success Bar:** Evaluate reading, search, approval, multi-device synchronization, authorized agent operations, privacy, and recovery; select a storage architecture and canonical skill source; retain the existing capture → review → approve → curate semantics; document a safe pilot/migration plan if warranted.

**Chosen Direction:** **Not selected. No migration is approved.** Revised recommendation: **a separate private Git-backed Markdown KB is now a serious contender, potentially preferable for a Markdown-first workflow**. Do not presume Drive remains the better content backend merely because it supports searching and folder moves. A hybrid may still win.

**Current State:** Comparative analysis updated following the owner's actual Drive and VS Code experience. **An existing private GitHub KB repository has now been located**: `chingfhen/knowledge-base` (default branch `main`, not archived). This is a stale earlier KB implementation, not a hypothetical new repo. Its last visible commit was on 2026-09-22. Current canonical KB workflow and Google Drive adapter remain on Drive; Agent Core contains a noncanonical copy. No KB files or global routing were migrated.

**Next Action:** When resuming, **first investigate the existing private `chingfhen/knowledge-base` repository and reconstruct why it was replaced by Google Drive**; compare old and current workflows before proposing a migration. Then use a few *synthetic, nonsensitive* Markdown files to compare: (1) actual reading on phone and desktop, (2) filename and content retrieval by agent, VS Code and GitHub, (3) review → approved via VS Code or agent, including commit/push, (4) evidence curation and link maintenance, (5) backup and conflict recovery. Choose the backend only after a small end-to-end trial.

**Blockers / Constraints:** The decision is deferred. GitHub currently reports `chingfhen/agent-core` as **public** (checked 2026-10-08); it must not contain personal KB evidence or company-confidential content. A **private, separate repository** is required for an ordinary personal Git KB. A private repository is not automatically an authorized storage destination for workplace data; employer policy remains controlling.

**Human Attention:** No action now. When revisiting, check the GitHub file view and the exact Drive behavior observed on your devices rather than relying on feature claims from vendor documentation. Confirm whether access works in the actual personal agent environments before selecting a new backend.

## Important Newly Located Predecessor: Existing GitHub KB

**Confirmed repository:** [`chingfhen/knowledge-base`](https://github.com/chingfhen/knowledge-base) — **private**, default branch `main`, not archived; latest visible commit on **2026-09-22** (`remove skills`). Its content is an **older/stale implementation**, not the canonical current KB. Do not overwrite or treat it as current.

[Open its `AGENTS.md`](https://github.com/chingfhen/knowledge-base/blob/main/AGENTS.md) and [old KB root](https://github.com/chingfhen/knowledge-base/tree/main/knowledge-base).

Observed older layout:

```text
knowledge-base/
  inbox/       (unprocessed material)
  evidence/    (processed records, including original formats)
  knowledge/   (current synthesis)
  index.md
```

The older `AGENTS.md` describes a Git-backed approval/capture workflow, confidentiality, no pushing without explicit permission, and one isolated commit per approved KB mutation. Its old `inbox/` and source handling differ from the current Drive workflow's explicit `inbox/raw/`, `inbox/review/`, `inbox/approved/`, and `source-archive/`; **do not naively restore the old repo and assume semantic compatibility**.

**Owner recollection:** This GitHub KB was abandoned in favor of Google Drive, but the **specific reason for the migration is not remembered**. This missing decision rationale is a key investigation objective. Avoid rewriting history with an assumed explanation such as “Drive search and file moves were definitely the sole reason.”

**Before a new Git migration or private repo is created:**
1. Inspect old repo's relevant commits, docs, past KB skill decisions, and any retained task/evidence describing the move to Drive. Look for concrete pain points (agent access, GitHub read/write tools, approval UX, search, files/binary handling, sync conflicts, device access).
2. Compare the old repository **against the *current* Drive KB**. Determine what material is unique or stale and whether any historical records need preservation. Never treat the old snapshot as the source of truth merely because it is in Git.
3. Test an end-to-end workflow in a **separate test branch or synthetic test files**, preserving historical content. The existing private repository may be a suitable pilot rather than creating yet another repository, but **no cleanup/reuse is approved** until its state and history are understood.
4. Capture the actual reasons for the prior migration as confirmed or unresolved. The decision to return to Git should specifically address the original failure modes.

**Revised recommendation:** Prefer evaluating and potentially **reusing the already-existing private `chingfhen/knowledge-base`** over creating another KB repo. This reduces proliferation while retaining clean separation from the public `agent-core`. Whether to reuse it remains undecided.

## Revised Finding: Reading Markdown Is Not Equivalent on Drive

**Owner's observed behavior on 2026-10-08:** On both Google Drive mobile and web, opening `.md` files still requires handing them to **OpenNote**. The earlier claim that Drive provides an equally convenient native formatted Markdown preview was **not true in the owner's actual setup**. Do not repeat it or instruct the owner to switch to a Preview mode as though that resolves the issue.

This materially strengthens GitHub for **reading**: an ordinary GitHub file URL opens the rendered Markdown, and VS Code can also preview Markdown in a locally cloned repository (`Ctrl+Shift+V` on Windows).

Reading is a daily task; moving files for approval may be comparatively rare. Optimize for the **real frequency and effort of each operation**, not abstract feature availability.

## Finding: Git Search Has Several Good Paths

| Who is searching? | Practical method | Notes |
| --- | --- | --- |
| **Human in VS Code (local clone)** | `Ctrl+P` to open a filename; `Ctrl+Shift+F` for text across files. | Fast, local and works offline after cloning. VS Code search respects exclusions; check search settings if a file is missing. |
| **Human on GitHub web** | Repository file finder and GitHub Code Search. | GitHub search supports `repo:OWNER/KB-REPO`, `path:`, and `content:` filters. Requires appropriate repository access; search indexing/coverage may differ from local search. |
| **Human in terminal** | `rg -n "phrase" .` for full text; `rg --files | rg "part-of-name"` for filenames. | Optional power-user route; ripgrep ignores hidden/ignored files by default. `git grep -n "phrase"` is another option for tracked content. |
| **Agent with GitHub connector** | Ask the agent to find files, search contents, inspect a result, and return the exact clickable GitHub file link. | This already works for the connected `agent-core` repo. For a new **private** KB repo, verify the specific connector/agent has search and read permission. |
| **Agent with local checkout** | Agent searches filenames/content with filesystem tools or `rg`, then opens the relevant Markdown. | Needs an accessible checkout and current sync. No dependency on GitHub code-search indexing. |

**New principle:** The owner does **not** need to be their KB's primary search engine. Asking a connected agent *"find my note about X and link the relevant file"* can be the default discovery path, supplemented by VS Code for direct self-service.

However, **agent-mediated retrieval must not be the only search path**. A straightforward manual fallback (VS Code or GitHub) matters when the connector is unavailable or the agent is wrong. Prefer linkable canonical files, descriptive filenames, and concise `knowledge/index.md` / `evidence/index.md`; don't build a separate vector database or search application before evidence of need.

### Example GitHub searches

Inside GitHub's code search, substitute the actual **private KB** repository name:

```text
repo:OWNER/KB-REPO path:credit-card
repo:OWNER/KB-REPO content:"investment strategy"
repo:OWNER/KB-REPO path:knowledge/ "decision rule"
```

The examples show repository-scoped filename/path and content search; verify coverage against real notes instead of assuming indexing is instant or exhaustive.

## Finding: VS Code Can Preserve the Approval Mechanism

Existing semantic workflow:

```text
inbox/review/ --human approves--> inbox/approved/ --agent curates--> evidence/ + knowledge/
```

A Git-backed folder structure can keep **the same paths and approval rules**:

1. Human reads `inbox/review/example.md` in rendered GitHub or VS Code Markdown preview.
2. **Approval signal:** Human explicitly moves the file to `inbox/approved/` in VS Code Explorer, **or** explicitly instructs an authorized agent to approve that particular item. The agent must not infer approval from merely seeing a review file.
3. For an agent using **remote GitHub**, the approved move is visible after it is **committed and pushed**. VS Code has built-in staging, committing and pushing; just dragging a file locally is not enough to publish a durable cross-device approval.
4. The curation workflow detects approved material, moves it into permanent `evidence/`, updates `knowledge/` when justified, maintains indexes/links, and commits/pushes the result. It must not skip or forge human approval.

**Potential UX:** In VS Code this can be an ordinary drag-and-drop move followed by a short Git commit and push. It is more work than a Drive move, but may be worth it if the reading/search experience is consistently superior. On mobile, the GitHub web file editor can change a Markdown file's path and commit it; test whether that workflow feels acceptable.

**Important engineering distinction:** The current KB skill has a **filesystem adapter**. With a local Git checkout, that may already handle the file/folder operations, leaving commit/push as a distinct layer. But a cloud-only agent with only a GitHub connector needs an explicitly supported remote Git workflow (new backend adapter or carefully specified integration) to safely create, move, curate and verify files. Do not assume a read-only connector can write or a local move has synchronized.

**Multi-agent caveat:** Concurrent writers can conflict. Plan for latest-head checks, narrowly scoped commits and honest conflict handling. Don't let two agents silently overwrite the same `knowledge/` page or double-curate an approval. Git history enables recovery, but secrets remain in history after deletion unless explicitly remediated.

## Architectural Options, Updated

| Option | Assessment |
| --- | --- |
| **A. Drive KB content + Drive canonical skill** | No change or migration risk; useful for raw documents and general Drive organization. Owner's actual Markdown reading experience is weak. |
| **B. Drive KB content + Agent Core canonical skill** | Good intermediate housekeeping: one distributable skill source while preserving Drive storage. Does **not** fix the Drive Markdown-reading friction. |
| **C. Separate private Git repo(s) for Markdown-first KB + Agent Core canonical skill** | **Now the leading option to test**, not an approved decision. Strong rendered links, VS Code/terminal/web/agent search, Git history, and possible approval moves via VS Code. Requires proper privacy, connector writes, synchronization, and an end-to-end curation trial. |
| **D. Hybrid: Git for Markdown evidence/knowledge, Drive for raw documents/images** | Potential best of both if binary handling is important; creates cross-storage references and more operational complexity. Avoid unless a pilot shows clear benefit. |

**Recommendation after the correction:** Stop assuming Google Drive wins on search/approval. For **Markdown-heavy personal knowledge**, seriously pilot Option C. Keep Google Drive available for raw documents, where its strengths remain material. Compare Option C with B only after experiencing a full approval/curation cycle, not just the rendered GitHub page.

### Where should the canonical skill live?

**Preferred long-term direction (separate decision):** Agent Core should be the canonical *distribution/source* for the portable `knowledge-base` skill and its backend adapters. That aligns with `agent-core sync` and reduces a confusing second source of truth.

**But Agent Core itself should NOT be the KB content repository.** Separate executable workflows from personal evidence and records:
- `agent-core/skills/knowledge-base/`: workflow + adapter definitions, **only after a separately authorized canonical-source change**;
- `personal-knowledge-base` (example name): **private Git repository** containing `inbox/`, `evidence/`, `knowledge/`, and appropriately governed source records;
- further per-project/private roots when confidentiality or ownership demands isolation.

Moving the canonical skill from Drive is **not** approved in this task and would require validating the complete backend guidance, updating canonical pointers in `global/AGENTS.md`, registering the new active root(s), and testing the intended agents' read/write and approval support. The existing Drive KB and its adapter remain canonical until explicitly changed.

## Future Pilot (Small, Reversible)

1. **Investigate the existing KB first:** Inspect the already-existing private `chingfhen/knowledge-base` repository and investigate why Google Drive replaced it. Use nonsensitive test files in an isolated test branch or other scratch space; do not import real personal or OCBC material.
2. **Read/search:** Test GitHub rendered Markdown on Android and desktop; `Ctrl+P` filename search, `Ctrl+Shift+F` content search, `Ctrl+Shift+V` preview in VS Code; agent connector search returning direct links.
3. **Human approval:** Move one Markdown file `review/ → approved/` in VS Code, then commit/push it. Repeat approval by an explicit human chat instruction to an agent that has verified GitHub write tools.
4. **Curate:** Use a compatible workflow to move approved material into `evidence/`, consolidate `knowledge/`, update indexes and links, and verify the remote commit.
5. **Check failure cases:** Missing connector permissions, unsynced local move, concurrent updates, rejected push, and restoration from Git history.
6. **Choose the architecture:** Decide whether Git's day-to-day reading advantage outweighs added commit/push steps. Only then consider migration and canonical skill-source changes.

## Sources and Links

- [Existing private GitHub KB (historical)](https://github.com/chingfhen/knowledge-base), [old guidance](https://github.com/chingfhen/knowledge-base/blob/main/AGENTS.md), and [prior KB tree](https://github.com/chingfhen/knowledge-base/tree/main/knowledge-base).
- [Current canonical KB workflow on Google Drive](https://drive.google.com/file/d/1S6Y_RIRZUkxcY59v_XuRrVIi6LHYCubX/view) and [Drive adapter](https://drive.google.com/file/d/1fyZMXQq7YTm_X8fphdprjIl6BmXwZu1f/view).
- [Agent Core's noncanonical KB skill copy](https://github.com/chingfhen/agent-core/blob/main/skills/knowledge-base/SKILL.md) and [global routing](https://github.com/chingfhen/agent-core/blob/main/global/AGENTS.md).
- [VS Code: Find files and search across files](https://code.visualstudio.com/docs/editing/codebasics); [VS Code: Source control](https://code.visualstudio.com/docs/sourcecontrol/overview); [VS Code: Commit and push](https://code.visualstudio.com/docs/sourcecontrol/staging-commits).
- [GitHub: Code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax); [GitHub: Moving files](https://docs.github.com/en/repositories/working-with-files/managing-files/moving-a-file-to-a-new-location).
- [ripgrep](https://github.com/BurntSushi/ripgrep).
- **Observed user evidence:** On 2026-10-08, opening Drive Markdown files on the owner's mobile and web required OpenNote. This firsthand behavior overrides assumptions about how Drive documentation describes preview support.

## Permission and Closure

This is a **deferred architecture task only**. No implementation or migration is authorized by saving these findings. Do not edit Drive KB content, change canonical skill pointers, create a real KB repo, move private material, or grant new app access without separate authorization.

Close only after selecting and validating the intended content backend and skill source, and ensuring durable Agent Core documentation matches the decision.
