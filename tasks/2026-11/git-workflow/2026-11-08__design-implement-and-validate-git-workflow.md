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

**Chosen Direction:** Approved at design level. Canonical intended contract: [Git Workflow design](../../../docs/git-workflow-design.md). Agent Core is used by this human alone; the skill should nonetheless respect conventions, colleagues and restrictions in repositories it is applied to.

**Current State:** Design discussion completed and synced into `docs/git-workflow-design.md`. **No `git-workflow` skill exists, no new `AGENTS.md` Git Workflow section was configured, no target branch for implementation was approved or created, and no implementation, harness sync, live provider acceptance, or cross-session trial occurred.** Relevant older AdReadyClips GitLab design and on-hold MR adoption task were located; neither was modified.

**Next Action (permitted):** In a **fresh session**, read this task and design doc, verify current canonical skills/repo state and inspect the portable AdReadyClips policy as necessary. Reconcile the implementation plan below with current tool/harness realities, present the **specific proposed implementation branch** (suggested `feature/git-workflow-cf`, target `main`) plus delivery boundaries and significant verification gates, and request the human's approval **before creating the branch or editing any production skill**. After approval, implement the bounded plan; do not infer it from the task's Active status.

**Blockers:** None to plan/review/read-only investigation. **Implementation branch creation and production skill modifications require human approval.** Any provider-specific live integration tests need suitable access and safe side-effect review; do not assume Bitbucket availability or organizational authorization.

**Permission Boundary:** This wrap-up authorized **only** writing this task, its index and the design documentation. Do not treat it as permission to create a branch, edit `skills/`, alter other repos, push/open PRs, merge, deploy, change remote protection/CI settings, spend money, install/update harness resources, or invoke external automation. Future approval may cover branch, scoped implementation/commit, publication and review preparation together, but merging always requires distinct explicit approval.

## Locked Human Decisions (not open for reconsideration absent new material evidence)

1. **Opt-in initiation:** “Implement this feature” alone does not automatically start Git Workflow or create a branch. Manual invocation/equivalent human intent starts a proposed managed-branch arrangement. The agent recommends whether a branch is worthwhile and must obtain branch-specific approval before creation.
2. **Recognizable but inconspicuous naming:** Proposed default `feature/<slug>-cf`, adapted to each repo's required prefixes/tickets. No `agent/` naming. This marker is discovery assistance, not a trust or authorization token.
3. **Strong managed/external boundary:** Within verified approved scope, agents may continue implementation and commit on managed branches without repeated routine approval. On external/unverified branches, inspection is allowed but modification requires explicit scoped human permission. Existing external branches can be adopted only after approval; no arbitrary renaming.
4. **Delivery boundary explicitly proposed:** The human may approve branch creation + local scoped commits + remote push + draft/ready PR/MR preparation in one agreement, or a narrower subset. Pushes and MR creation must respect assessed side effects and credentials. **No implicit merge**.
5. **Managed section:** A future `git-workflow` skill may maintain a small `<!-- BEGIN GIT WORKFLOW -->` / `<!-- END GIT WORKFLOW -->` section in a confirmed consumer repository's `AGENTS.md`, within an authorized setup/refresh. Include stable branch/target naming, authority constraints and pointer(s) to established project policy; **no active branch list** or duplicate policy. Respect other owners' sections and local policy.
6. **Human never needs to switch manually:** Agent discovers, validates and selects a safe checkout/worktree, confirms actual repository/branch/HEAD/status, and shows a compact verified context receipt before resuming edits. Dirty trees, concurrent writers, unexpected history or conflicting instructions stop unsafe writes.
7. **Project Tasks relationship:** Project Tasks is the preferred primary continuity mechanism for substantial/multi-session work; its existing task/index are consulted first on a task-oriented request. Git Workflow supplies live branch/commit/MR truth. Existing task prose may link to branch/PR and MR may link back; **no compulsory task for every change, no mandatory `Delivery` section, no new task/branch registry**. Small standalone changes may rely on their PR/MR if genuinely sufficient.
8. **Cross-session discovery:** Exact reference first (task, PR/MR or branch), then bounded search of open PRs/MRs, remote branches and accessible local branches. Scope/ownership must be corroborated; `-cf` alone is not permission. Do not pretend that unpublished local branches are portable or that an MR's description preserves all task decisions.
9. **MR timing/status:** For substantial multi-session changes, prefer a *draft* PR/MR after a meaningful committed checkpoint when publication is authorized and side effects are safe; for small changes open a normal MR when review-ready. Draft is visible according to project access, not private. Mark as *ready for review* only when agreed implementation and required pre-review checks are complete, limitations documented; ready status never equals merge approval. Provider feature availability may vary.
10. **Verification/approval:** Human and agent agree on consequential acceptance criteria and the intended evidence at the start; agent selects domain-appropriate concrete checks, and surfaces material changes in gates. Review uses current exact head SHA and target, compares important facets when useful, labels test/CI gaps, and gives merge/revise/reject advice. Ratings are optional/advisory and cannot excuse failed mandatory gates. Human exclusively authorizes integration of the reviewed change.
11. **Skill independence without reinventing state:** Do not require existing commit delegation mechanisms, create per-commit git tags or codewords, add a general verification skill, build an always-on bot, or duplicate Project Tasks into MR descriptions. Keep one Git lifecycle skill, with minimal Git command workflow as an optional reference if it materially improves reliability.
12. **Cross-host portability and workplace rules:** Generic Git is portable; GitHub PR, GitLab MR, and Bitbucket PR/readiness features and tools require targeted capability checks. Actual repository policies, authentication, automation restrictions, team permissions and CI/deploy effects outrank the personal defaults.

## Architecture and Routing to Implement

- `skills/git-workflow/SKILL.md` owns the future concise trigger, authority boundaries, lifecycle, discovery, verification receipt and request-only consequential operations. Keep lengthy provider specifics and command examples in skill-local `references/` only when justified.
- The managed consumer `AGENTS.md` section is a **stable entry point** and per-repository policy locator. Create/maintain only on separately authorized configuration, preserving existing text, stricter permissions and other managed sections. No automatic migration of AdReadyClips' existing guidance.
- In Agent Core, `docs/git-workflow-design.md` owns the durable intended design; this task owns the **current plan/status and decisions awaiting validation**. `docs/skills-catalog.md`, `personal-skills.toml`, `docs/workspace-configuration.md`, and appropriate tests are integration targets **when the skill is approved and implemented**, not evidence that it exists now.
- A Project Task is a natural starting point for saved work. The task points to managed branch/PR using ordinary status prose. The PR/MR points back when relevant and owns diff/check/review discussion. Their records are complementary; read current Git state when there is disagreement over Git facts.
- A **delivery receipt** should contain repository identity, proposed/actual branch and review target, current SHA, PR/MR URL/status or absent, approved permission boundary, real checks/gaps, and precise next action/continuation reference. It is a human-facing view of sources, **not another persistent registry**.

## Planned Execution Phases (future execution, not current authorization)

### Phase 1 — Resolve interfaces and failure modes

- Inspect the current `engineering`, `planning`, `project-tasks`, `project-docs`, `approval-gate`, `workspace-setup` and skill-design/managed-AGENTS conventions. Prefer existing owner procedures, avoid duplicate skill instructions.
- Confirm practical Git/host CLI/API operations and how identity, PR/MR status and pipeline evidence are read in the intended harness. Check GitHub/GitLab and the actual relevant Bitbucket product/version/tooling; do not simulate provider parity.
- Decide the minimal skill entry/reference split and the smallest necessary cross-skill routing cues. Human approval is required before materially changing other production skills.
- Decide how a new branch's approved scope is durably recoverable before PR/MR creation without inventing a global ledger: task for substantial work or sufficiently reliable explicitly authorized provider/checkout record. If evidence is absent, the fail-closed behavior is to ask again.

### Phase 2 — Implement the canonical skill and routing contract

- Write `skills/git-workflow/SKILL.md` with request-first opt-in, managed-branch continuation triggers, explicit branch/adoption/merge approval, no routine subagent dependency, and proportional edit/commit/publish/readiness flow.
- Provide a short git-state safety/reference section only for checks where predictable commands help (repo/remote, fetch when authorized, status, switch/worktree, HEAD, scoped diff, outgoing commits, push). Keep provider-specific PR/MR operations modular rather than hardcoded.
- Specify creation and refresh of the marked `AGENTS.md` block under user-authorized setup, protecting other skill sections and existing team policy.
- Establish PR/MR continuity descriptors if useful (objective, scope, acceptance, verification, state and next action); **do not** create a competing Project Tasks schema.

### Phase 3 — Integration and scenario-based verification

- Add or extend practical workflow acceptance scenarios, exercising non-activation, branch proposal/approval, managed resumption, external branch refusal/adoption, draft MR, read-only review, CI evidence and merge authorization.
- Test against actual isolated Git repositories/fixtures where possible. Use real hosted provider operations only after explicit authorization and side-effect review.
- Test fresh-session recovery from (a) a Project Task + linked MR, (b) a branch/MR without task, (c) approved local-only work not visible remotely, and (d) ambiguous matching branches. Include suffix spoofing, wrong checkout, dirty worktree, changed head after review, unavailable provider API and missing approval as explicit negative cases.
- Verify no unsolicited edits for a generic engineering request, no unapproved branch creation, no writes to external/unproven branches, no unauthorized push, and no merge from an advisory rating or mere 'ready' status.
- Evaluate task/project-doc ownership and link consistency without claiming an unrun fresh-session behavioral test succeeded. Record what was static reasoning versus observed execution.

### Phase 4 — Publish a reviewed candidate, not an unapproved merge

- Once specifically approved, create the agreed `feature/git-workflow-cf` branch or another human-approved name from a verified base; implement and commit the bounded scope, and publish/open a PR only to the authorized endpoint.
- Compare candidate against `main` on meaningful safety, continuation, integration, portability, complexity and verification facets. Summarize findings and unresolved tests. Human decides whether to merge; no automatic integration.
- After approved integration, reconcile installation manifest and skills catalogue as actually implemented, verify selected harness sync only if separately authorized, and close this task only on its recorded success bar.

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
- **Working repository:** `chingfhen/agent-core`, `main`; no implementation branch established. Fresh agent should inspect actual refs and worktree before proposing a branch.

**Fresh-session resume cue:** “Read Agent Core's Git Workflow implementation task and its linked design doc. Review the execution plan, propose `feature/git-workflow-cf` and the exact delivery/verification boundary for my approval. Do not create the branch or edit production skills until approved.”
