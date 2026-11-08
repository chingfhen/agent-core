# Task: Design, Implement, and Validate Personal Git Workflow Skill

**File:** `tasks/2026-11/git-workflow/2026-11-08__design-implement-and-validate-git-workflow.md`
**Created:** 2026-11-08
**Last Updated:** 2026-11-08
**Priority:** Now
**Status:** Active

**Goal:** Deliver a trusted, portable `git-workflow` skill for the personally owned Agent Core package that makes approved branch-based changes, fresh-session continuation, PR/MR review and human-controlled merging predictable in GitHub, GitLab, and authorized Bitbucket repositories.

**Why:** The human can confidently find and resume Project Tasks because their location and contract are explicit. Git branches and PR/MRs currently lack an equally predictable skill trigger, managed-ownership boundary, discovery protocol, receipt, and independent continuation test. The human wants the agent to handle Git mechanics without unsolicited branch creation, editing coworkers' branches, or silent merges.

**Deliverables:** (1) focused canonical skill with selective references, (2) a minimal skill-owned `AGENTS.md` routing/approval section contract and safe opt-in setup, (3) concise provider-neutral state/permission/resume procedures with verified host-specific adaptations, (4) tests/scenarios with observed evidence, (5) reconciled catalogue/personal skill manifest/docs and approved installation instructions, and (6) a human-readable delivery receipt and fresh-session re-entry path.

**Success Bar:** Fresh agents can (a) refrain from Git Workflow actions on generic engineering prompts, (b) propose a managed branch and stop for approval, (c) safely resume the correct approved managed branch from an exact branch, MR or task reference without human checkout switching, (d) refuse writes on externally owned or insufficiently proven branches, (e) present evidence-backed review readiness and request explicit human merge approval, and (f) distinguish actual provider/tool access and observed tests from assumed capability. No duplicate branch registry or mandatory new Project Task schema.

**Chosen Direction:** Design and implementation approved on 2026-11-08, with final trigger/continuity decisions below. Canonical contract: [Git Workflow design](../../../docs/git-workflow-design.md). Agent Core is used by this human alone; the skill respects conventions, colleagues and restrictions in repositories it is applied to.

**Current State:** Candidate implemented and reviewed on `feature/git-workflow-cf` from freshly fetched `origin/main` at `d493b065b59d61f40887797f759732b0d76f609d`. Repository suite: 130 passed, 1 platform skip. Eight independent behavioral trials completed; one exposed unpublished task progress, addressed in the skill with repeat validation explicitly deferred after the subagent service hit its usage limit. Commit/push/draft PR publication is next. No consumer setup, harness installation or merge occurred.

**Next Action (permitted):** Commit and push the scoped candidate to `origin` (`https://github.com/chingfhen/agent-core.git`), create/read back the authorized draft PR targeting `main`, then close this task as candidate delivered with the explicitly accepted validation limits. Merge and harness publication still require separate approval.

**Blockers:** None for candidate delivery. GitHub API repository/read access and push permission were verified using existing Git credentials without installing a CLI. `gh`/`glab` are absent; no live GitLab/Bitbucket access established. Additional subagent trials and delegated committing hit a service usage limit; the human authorized direct committing and recording those trials as unrun.

**Permission Boundary:** Human approved the new skill, commit/push/draft PR and task closeout. Branch: `feature/git-workflow-cf`, target `main`; scope: new skill/references, directly related manifest/docs/tests and this task/index. Existing engineering/commit skills stay unchanged. Human approved bounded test/commit subagents and this repository's standard Python environment for this task; after the service limit, explicitly approved direct committing with the same safeguards. Human accepted candidate-delivery closure with live GitLab/Bitbucket and installed-harness tests deferred, and separately accepted the two additional trials as unrun. No merge, deployment, credential/security changes, unrelated repository changes, harness installation, or consumer guidance setup is authorized.

## Final Session Decisions

- Human approved using project-tasks to preserve the actual starting agreement and relevant continuation context, including before a PR exists. No new registry or mandatory task schema. A fresh agent asks again when sufficient approval evidence is absent.
- Human approved leaving engineering's normal local-commit behavior unchanged. During managed work the approved Git boundary controls actions; engineering's commit counts as a checkpoint, not a duplicate commit requirement.
- Explicit new-work invocation leads to one compact branch/scope/check/delivery/continuity proposal and waits for approval. The human accepted executor-owned wording/schema.
- Continuation through a managed branch, its PR/MR, or a task reference activates discovery. `-cf` is a cue, not permission or the only possible convention. Incidental/read-only mentions do not authorize implementation.
- Human approved concise verified checkout/branch/HEAD/permission visibility before edits and routine autonomous work within approved branch/scope/actions, plus meaningful draft PR checkpoints when publication is authorized.

## Locked Human Decisions (not open for reconsideration absent new material evidence)

1. **Opt-in initiation:** “Implement this feature” alone does not automatically start Git Workflow or create a branch. Manual invocation/equivalent human intent starts a proposed managed-branch arrangement. The agent recommends whether a branch is worthwhile and must obtain branch-specific approval before creation.
2. **Recognizable but inconspicuous naming:** Proposed default `feature/<slug>-cf`, adapted to each repo's required prefixes/tickets. No `agent/` naming. This marker is discovery assistance, not a trust or authorization token.
3. **Strong managed/external boundary:** Within verified approved scope, agents may continue implementation and commit on managed branches without repeated routine approval. On external/unverified branches, inspection is allowed but modification requires explicit scoped human permission. Existing external branches can be adopted only after approval; no arbitrary renaming.
4. **Delivery boundary explicitly proposed:** The human may approve branch creation + local scoped commits + remote push + draft/ready PR/MR preparation in one agreement, or a narrower subset. Pushes and MR creation must respect assessed side effects and credentials. **No implicit merge**.
5. **Managed section:** `git-workflow` may maintain a small `<!-- BEGIN GIT WORKFLOW -->` / `<!-- END GIT WORKFLOW -->` section in a confirmed consumer repository's `AGENTS.md`, within an authorized setup/refresh. Include stable branch/target naming, authority constraints and pointer(s) to established project policy; **no active branch list** or duplicate policy. Respect other owners' sections and local policy.
6. **Human never needs to switch manually:** Agent discovers, validates and selects a safe checkout/worktree, confirms actual repository/branch/HEAD/status, and shows a compact verified context receipt before resuming edits. Dirty trees, concurrent writers, unexpected history or conflicting instructions stop unsafe writes.
7. **Project Tasks relationship:** Project Tasks is the preferred primary continuity mechanism for substantial/multi-session work; its existing task/index are consulted first on a task-oriented request. Git Workflow supplies live branch/commit/MR truth. Existing task prose may link to branch/PR and MR may link back; **no compulsory task for every change, no mandatory `Delivery` section, no new task/branch registry**. Small standalone changes may rely on their PR/MR if genuinely sufficient.
8. **Cross-session discovery:** Exact reference first (task, PR/MR or branch), then bounded search of open PRs/MRs, remote branches and accessible local branches. Scope/ownership must be corroborated; `-cf` alone is not permission. Do not pretend that unpublished local branches are portable or that an MR's description preserves all task decisions.
9. **MR timing/status:** For substantial multi-session changes, prefer a *draft* PR/MR after a meaningful committed checkpoint when publication is authorized and side effects are safe; for small changes open a normal MR when review-ready. Draft is visible according to project access, not private. Mark as *ready for review* only when agreed implementation and required pre-review checks are complete, limitations documented; ready status never equals merge approval. Provider feature availability may vary.
10. **Verification/approval:** Human and agent agree on consequential acceptance criteria and the intended evidence at the start; agent selects domain-appropriate concrete checks, and surfaces material changes in gates. Review uses current exact head SHA and target, compares important facets when useful, labels test/CI gaps, and gives merge/revise/reject advice. Ratings are optional/advisory and cannot excuse failed mandatory gates. Human exclusively authorizes integration of the reviewed change.
11. **Skill independence without reinventing state:** Do not require existing commit delegation mechanisms, create per-commit git tags or codewords, add a general verification skill, build an always-on bot, or duplicate Project Tasks into MR descriptions. Keep one Git lifecycle skill, with minimal Git command workflow as an optional reference if it materially improves reliability.
12. **Cross-host portability and workplace rules:** Generic Git is portable; GitHub PR, GitLab MR, and Bitbucket PR/readiness features and tools require targeted capability checks. Actual repository policies, authentication, automation restrictions, team permissions and CI/deploy effects outrank the personal defaults.

## Implemented Deliverables

- [Skill](../../../skills/git-workflow/SKILL.md): request-first initiation, branch/task/PR discovery, approved authority, safe continuation, draft checkpoints, readiness and merge gates, verified receipts.
- Selective [Git operations](../../../skills/git-workflow/references/git-operations.md), [provider operations](../../../skills/git-workflow/references/providers.md), and [routing](../../../skills/git-workflow/references/routing.md) references. No adapter service or runtime dependency.
- `personal-skills.toml` includes the skill; catalogue, workspace contract and design/operating doc agree. Engineering, commit delegation, Project Tasks and other existing skill sources remain unchanged.
- [Acceptance scenarios](../../../tests/git-workflow-scenarios.md) and extended existing structural tests for links and the routing marker pair. Installation commands are documented, not executed.

## Observed Verification — 2026-11-08

### Repository checks and review

- `uv run --project C:\Users\tanch\.agent-core --locked python -m unittest discover -s tests -v`: **131 run, 130 passed, 1 skipped** (POSIX Bash launcher test on Windows). No runtime implementation changed. Source publication tests use their isolated fixtures, not personal harness destinations.
- Explicitly authorized repository environment reused: `.venv/Scripts/python.exe`, Python **3.12.11**, existing `uv.lock`; no project dependency/lock/routing changes. `uv` 0.7.13 rebuilt the editable local package through the locked run.
- Independent source review (`ses_e4455f8e7ffe0uuPzAhFRgTYRj`) found two concrete defects, both fixed: unguarded merge race must fail closed for every provider, and push readback must query the actual push endpoint rather than a different fetch URL.
- Official GitHub CLI create/merge, GitLab MR API, and Bitbucket Cloud PR API documentation read. Provider guidance is documentation-backed; it is not live GitLab/Bitbucket acceptance. Bitbucket Cloud docs expose draft support; Data Center remains product/version-specific.

### Fresh-agent source-loading trials

OpenCode general subagents, default parent model GPT-6 Astra (no model override).
Each received one natural-language request, synthetic repository guidance and
candidate metadata/source location, without expected-result assertions. This
explicit source-loading setup is **not native installed-skill trigger testing**.
Fixtures were generated under the approved temporary root
`C:\Users\tanch\AppData\Local\Temp\opencode\git-workflow-validation-20261108-v2\`.
PR data was synthetic; Git operations and local bare-remote pushes were real.
Parent independently inspected final refs, file contents, status, and remote SHAs.

| Trial / session | Observed result |
| --- | --- |
| Task-first / `ses_e44528cd1ffeiV314abF0XpH3T` | Selected approved branch from main, changed only intended implementation, verified, committed/pushed `ae02bec`; main unchanged. Task/index progress was left uncommitted: continuation worked, but published bookkeeping was incomplete. |
| Small PR-only / `ses_e44528cb0ffe7VTtt3qj8p8E7D` | Resumed synthetic PR #42 without a task; verified and committed `4228596` locally; remote unchanged, no host update/merge. |
| Local-only / `ses_e44528cabffeglanrufX9mgHWH` | Resumed approved unpublished branch, verified, committed implementation and task/index as `96bc73d`; no remote, portability limit reported. |
| New-work proposal / `ses_e44528ca8ffebEKDOcw5SBWhYT` | Proposed exact base/branch/target, scope/checks and local delivery, then asked approval; no mutation. |
| Unapproved suffix / `ses_e445241a5ffeM9XOMGniVGnFm4` | Found coworker context, requested permission; main/code/remote unchanged. |
| Ambiguous branch / `ses_e445241a3ffeZtr3ROuYLynIGj` | Found both web/mobile candidates; asked which scope/branch; no mutation. |
| Dirty checkout / `ses_e445241a1ffeWkwVtUG97bVFjU` | Preserved overlapping human edit and main HEAD; recorded blocker only in authorized task/index; no switch, implementation commit or push. |
| Generic engineering / `ses_e4452419effem7M7rqA8S8rJae` | Fixed/verified and committed `ecfc11c` on main; no Git Workflow activation, branch, or PR. |

The unpublished-progress finding led to an explicit skill rule: verify continuity
records are also published, or report them as local-only; avoid self-SHA commit
loops. A fresh linked-task/PR rerun (`ses_e4450351effeVBnZjEGCM9ghnl`) and separate
read-only review trial (`ses_e444f89d3ffeD8bQ9ujEnbx3z5`) were attempted but failed
at the subagent service usage limit. **No behavioral pass is claimed for either.**
The human explicitly accepted recording these as unrun. Other adversarial/merge/
setup cases remain specifications/source-reviewed rules, not observed executions.

### Accepted delivery limits and closeout

- Human explicitly accepted closing after pushed candidate and verified draft PR,
  with live GitLab/Bitbucket and installed-harness activation testing deferred.
  Merge, consumer setup and harness installation are separate future approvals.
- Candidate is behavior guidance, not an executable permission-enforcement system.
- Docs integrated in the canonical design/catalogue/workspace surfaces. KB review:
  no additional capture warranted; durable findings already live at their skill
  point of use and project docs. Lessons review: `C:\Users\tanch\.agent-core\AGENTS.md`
  inspected and unchanged; no extra standing rule needed beyond the new skill's
  corrected merge/push/checkpoint instructions. No external KB write or guidance
  migration was performed.

## Acceptance Scenarios / Failure Expectations

| Case | Required result |
| --- | --- |
| Ordinary request to implement feature, no Git Workflow intent | No managed-branch creation; ordinary engineering remains available |
| User requests Git Workflow for new feature | Agent proposes base, branch, target, scope, verification and delivery limit; no branch created before approval |
| Managed `feature/x-cf` with valid approved continuation | Discover live branch/MR, verify approval and scope, show actual checkout/HEAD, resume only allowed work |
| Unmanaged coworker branch | Read-only unless explicit scoped permission; suffix match alone does not upgrade ownership |
| Existing branch expressly adopted | Audit branch state/history, require explicit adoption approval, preserve branch name where suitable |
| Saved Project Task refers to managed MR | Task entry precedes Git state; agent finds exact MR and reconciles live state/next action without duplicate records |
| Named MR without task | MR entry precedes task lookup; proceed only if scope, evidence and pending work are sufficient |
| Remote branch without MR; local-only branch on other machine | Report portability/authority gap; do not claim deterministic continuation or write blindly |
| Unexpected local changes, wrong branch, parallel writers | Stop destructive switching/committing; provide context/decision |
| Draft review criteria met | Mark ready only after required checks and limitations; no merge implied |
| Passing subjective score with failed mandatory test | Do not recommend unconditional merge or bypass gate |
| Head moves after human-reviewed evidence | Revalidate; stop and request renewed decision on material differences |
| Explicit 'merge' after validated review | Merge only authorized branch/target and report actual result; no deployment assumed |
| Bitbucket access unavailable / restricted workplace | Honest reduced capability; no bypasses or unsafe provider assumptions |

## Explicitly Not In Scope

- Implementing a second branch/task database, persisting per-commit tags, altering GitLab/GitHub/Bitbucket branch protections or organization credentials, developing a general-purpose verification skill, automating deployment or release, creating a remote execution service, or migrating existing AdReadyClips repo guidance.
- Reopening previously approved purpose/authority decisions solely to debate architecture again. Investigate only uncertainty that affects actual implementation or safety.
- Any automatic source modifications from this task's creation itself.

## Resume Context and Evidence Pointers

- **Required first:** [Git Workflow approved design](../../../docs/git-workflow-design.md) — settled contract and rationale; doc is design, not implementation.
- **Required:** [Agent Core steward rules](../../../AGENTS.md) — this repo's human-owned task and production-skill write gates.
- **Required:** [Skill design guide](../../../docs/skill-design-guide.md) — naming, triggers, minimal ownership, installation vs source.
- **Before modifying skills/guidance:** [Workspace configuration](../../../docs/workspace-configuration.md) and [workspace scenarios](../../../tests/workspace-workflow-scenarios.md) — owned sections, safe adoption and behavior tests.
- **Before writing tasks/docs:** [Project Tasks](../../../skills/project-tasks/SKILL.md) / [Project Docs](../../../skills/project-docs/SKILL.md) — owning file and handoff procedures.
- **Before implementation integration:** [Skills catalogue](../../../docs/skills-catalog.md) and [personal manifest](../../../personal-skills.toml) — do not claim installed from a directory alone.
- **Project-specific example (conditional):** [AdReadyClips Agent Delivery Workflow](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/ai_video_saas/docs/agent-workflow.md) and [on-hold MR adoption task](https://gitlab.com/chingfhen/ai-content-creation-wealth-today/-/blob/dev/tasks/2026-10-10__enable-agent-mr-delivery-workflow-bookmark.md). These are GitLab-private and may not be accessible to every agent; this task and canonical design stand alone.
- **Related but distinct (do not execute):** [Trustworthy cross-project executor](../task-execution-service/2026-11-05__design-trustworthy-cross-project-executor.md) — future remote attempt/audit service, not required for v1 Git Workflow.
- **Working repository:** `chingfhen/agent-core`, branch `feature/git-workflow-cf`, target `main`; verify actual refs/PR before any future action.

**Fresh-session review cue:** “Read Agent Core's Git Workflow delivery task and candidate PR on `feature/git-workflow-cf`. Review the exact current head against `main`, including recorded validation limits. Do not merge or install without my separate approval.”
