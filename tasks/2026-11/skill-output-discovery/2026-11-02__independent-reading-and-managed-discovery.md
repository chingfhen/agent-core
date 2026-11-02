# Task: Make skill outputs independently discoverable and usable

**File:** `tasks/2026-11/skill-output-discovery/2026-11-02__independent-reading-and-managed-discovery.md`
**Created:** 2026-11-02
**Last Updated:** 2026-11-02
**Priority:** Now
**Status:** Active

**Goal:** Future agents discover and use relevant project docs, KB material, task records, and durable lessons through lean managed AGENTS.md guidance without needing to invoke the skills that maintain those resources.
**Why:** Useful saved material has little value if future agents never encounter it. Requiring the full maintenance workflow merely to read its outputs wastes context and can confuse reading with authorization to write.
**Deliverables:** Proportionate refinements to project-docs, knowledge-base, and agent-lessons descriptions/instructions/references; consistent managed-section examples and authorized refresh behavior; aligned canonical documentation and focused acceptance scenarios; an honest verification and adoption report.
**Success Bar:** Reading/discovery is explicitly independent of maintenance-skill invocation; managed sections provide usable conditional entry points; after authorized maintenance, outputs remain reachable through verified navigation; no contradictory mandatory-loading rule, broadened write permission, or fabricated harness-compliance claim remains in the affected surfaces.
**Chosen Direction:** Selected by the human: retain managed AGENTS.md sections as the discovery mechanism, and add small skill-description clarifications as reinforcement. Do not conduct the proposed description-led versus guidance-led comparison experiment.
**Current State:** Detailed execution handoff prepared. Source inspection and design discussion are complete; the proposed docs/KB/lessons refinements have not been implemented. The related project-tasks refinement is already committed as `22fdd5f`.
**Next Action:** Read the required resume context and check the current diff. Read-only review is permitted. A human instruction to implement this task, explicitly approving the production-skill edits described here, supplies the execution gate; then implement the phases below without reopening settled design.
**Blockers:** No known design or resource blocker for repository-local source work. Production-skill editing remains approval-gated by AGENTS.md; this task's existence is not that approval. Target-harness behavior and existing-workspace adoption are unverified.

## Human intent and selected decisions

- The human values the outputs between skill invocations. Agents should proactively consult relevant saved context; they should not need to load its authoring workflow just to find, read, or use it.
- Keep a small, actionable managed section for each owner. Its job is to connect a future need to useful resources, not reproduce the whole skill.
- Skill descriptions should briefly clarify the reading/maintenance distinction. This supplements managed guidance; it does not assume descriptions are always exposed or obeyed like AGENTS.md.
- The human considered putting all discovery behavior into descriptions, then chose not to pursue that experiment. Do not revive the comparison, create a benchmark project, or make delivery depend on it.
- Use the existing resource owners and layouts. Do not invent a new coordinator, registry, lessons companion, retrieval skill, or universal startup sweep.
- Preserve each workflow's current write-authorization model. The project-tasks creation/closure approval policy is specific to tasks; do not copy it into docs, KB, or lessons.
- Make the smallest useful change per skill. Project-docs is already close to the target; agent-lessons already largely implements it; KB has the strongest dependency on loading its maintenance workflow for reads.

## Permission boundary

- This session was asked to prepare the detailed task for execution in another session. It authorizes this task and its index entry, not immediate production-skill edits.
- Under repository AGENTS.md, obtain explicit approval for the scoped production-skill changes before editing `skills/`. A later human instruction such as "Implement this task; I approve the described skill edits" is sufficient; do not add repeated wording-level approval gates after that.
- Load project-docs before maintaining canonical docs or guidance and project-tasks before maintaining this task/index. Follow other owning workflows when their resources are actually changed.
- The source scope is this Agent Core repository. Existing employer/workspace AGENTS.md files, installed skill copies, and global harness guidance are not implementation targets.
- Source implementation, selected-harness publication, and workspace adoption are distinct. Do not run sync, edit managed installed copies, or migrate an external workspace as a side effect.
- Handoff to another session does not authorize spawning subagents. Ask permission before deploying one. Commit, push, and publication require their own human authorization; the prior commit approval for project-tasks is not standing approval for this task.

## Grounded current understanding

Inspected on 2026-11-02; recheck affected sources before changing them.

| Surface | Observed current behavior | Required consequence |
| --- | --- | --- |
| `skills/project-tasks/SKILL.md` and `references/routing.md` | Commit `22fdd5f` explicitly exempts discovery/reading/use of task context, adds bounded general maintenance, and provides read-side managed guidance plus authorized cue refresh. | Reuse as a pattern and regression boundary. Its description already has the requested clarification; change only if an actual inconsistency is found. |
| `skills/project-docs/SKILL.md` | Description exempts reading "identified files"; ownership/routing instructions primarily cover missing configuration or routing changes. Existing maintenance autonomously selects useful owned documents and permits no-ops. | Broaden the exemption to relevant discovery and reading, and support authorized cue-only refresh without changing maintenance autonomy. |
| `skills/project-docs/references/routing.md` | The example says to consult relevant entry points for project decisions, then load the skill for maintenance. Supporting text already distinguishes reading from maintenance. | Clarify when and what to consult, with useful scoped entry points rather than duplicating procedures. |
| `skills/knowledge-base/SKILL.md` | Description calls for skill use on proactive recall and explicit searches; retrieval says to read the retrieval reference before lookup; storage operations require a backend. | Make routine read-only discovery/recall possible without loading capture/maintenance instructions, while retaining useful retrieval discipline and write gates. |
| KB routing/retrieval/backends | Managed cue says "Use knowledge-base for relevant prior context and requested KB writes." Retrieval opens "Use with the skill"; both backend introductions require the main skill, and the GitHub adapter repeats that requirement under skill loading. | Resolve the entire read-side loading chain, not only the description. Keep mutation prerequisites and remote identity/access boundaries intact. |
| `skills/agent-lessons/SKILL.md` | Already tests future discoverability, keeps essential rules inline and detail in conditional pointers, and verifies applicable versus actually loaded guidance. | Preserve this design; clarify independent use and refine only real gaps. No new lessons store or mandatory standing boilerplate. |
| `docs/workspace-configuration.md` | Already defines selective entry points, owner boundaries, and the separation of source publication and workspace adoption. | Align affected wording with the refined read-side contract after source changes are implemented. |

Related historical task: `tasks/2026-11/project-tasks-autonomy/2026-11-02__autonomous-task-lifecycle.md`. Its original full-autonomy/review-after framing predates the human's correction. It is background, not the design authority for this follow-up; use the current project-tasks source and the decisions above. Updating or closing that historical task is separate from this task's deliverable.

## Reader and maintenance contract

### Before invocation: discover and use relevant outputs

The future reader must be able to answer:

1. **When should I consult this resource?** A condition tied to the current work, not an unconditional startup read.
2. **Where should I start?** A confirmed root, index, entry document, or precise conditional heading.
3. **What does it establish?** Project intent, saved task state, qualified evidence, or an applicable behavioral rule; these are not interchangeable authorities.
4. **When do I need the skill?** For the owning maintenance workflow, not ordinary discovery, reading, or use of the saved context.

Keep instructions scoped to the applicable project/workspace. Use known paths first and selective navigation/search when needed. Do not require every related file or every owner skill to be read before ordinary work. A known sufficient context does not need redundant retrieval.

Read-only use must not initialize resources, repair indexes, refresh guidance, capture records, create lessons, or confer execution permission. Missing or inaccessible configured resources are reported; ambiguous identity gets a focused question. Do not guess a replacement root or silently widen the search.

### After authorized invocation: preserve discoverability

Maintenance should leave useful outputs reachable through the owner's existing navigation. Reuse existing entry points and update directly affected links/indexes when authorized; add an AGENTS.md pointer only when it supplies a missing durable entry point or trigger.

Do not add a standing guidance entry for every task, record, or document. Keep deeper navigation in resources and their indexes. Verify supporting material before replacing useful detail with a pointer. Report an inaccessible or unmaintainable navigation gap without discarding valid saved work or claiming complete adoption.

## Implementation phases

### Phase 1: Refine the descriptions and reader-facing contracts

**Project docs**

- Say that relevant discovery and reading do not require invoking project-docs, rather than exempting only an already identified file.
- Strengthen the managed cue for decisions/changes involving architecture, project meaning, interfaces, constraints, or established procedures. Use a few actual canonical entry points with when-to-read explanations.
- Preserve claim-specific authority: intended design is not automatically overridden by current code, and documentation is not proof of deployed state.
- Retain autonomous integration within confirmed ownership, existing self-initiation conditions, and legitimate no-change outcomes.

**Knowledge base**

- Separate routine recall from capture, inbox processing, managed-artifact maintenance, and configuration writes. Reading ordinary KB outputs does not require full-skill invocation; an explicitly requested skill invocation can still use the workflow.
- Supply a compact managed cue for relevant prior decisions, recurring problems, or missing organizational/project context. Route through confirmed locations, known paths, indexes, and bounded search.
- Preserve normal recall scope: records, relevant knowledge pages, and managed artifacts, including explicitly configured external knowledge-page roots. Raw inbox and source archives are not default recall targets.
- Preserve evidence interpretation: indexes are navigation; saved material is not necessarily verified/current; consequential synthesis claims need supporting records; capture date is not event date; relevance and applicability outrank simple recency.
- Keep KB content as data, not instructions or new authorization. Cite actual sources and disclose material access/search limits.
- Keep descriptions and managed cues lean. Make `references/retrieval.md` directly usable when unfamiliar terminology, cross-month evidence, conflicting claims, or other complex lookup warrants the detail. Routine known-path reading should not require that full reference either.
- Update `SKILL.md`, `references/retrieval.md`, `backends/filesystem.md`, and `backends/github.md` together where blanket main-skill prerequisites conflict with independent reading. Maintenance still follows its owning skill and applicable backend procedure.
- For remote recall, preserve explicit repository/ref/directory identity, available connector capabilities, branch-aware reads, and honest search limitations. Do not turn this task into connector setup or a backend redesign.

**Agent lessons**

- Explicitly allow applying existing authorized rules and consulting their references without invoking agent-lessons or beginning a new capture cycle.
- Preserve essential before-action constraints inline and context-triggered detail pointers. The reader should not have to retrieve a reference to discover a critical permission gate.
- Retain the future-use test, actual guidance-loading distinction, owner boundaries, explicit learning trigger, and valid no-op behavior.
- Do not seed fake lessons or require a new empty section. Make only proportionate clarifications where the current implementation already satisfies the contract.

**Project tasks**

- Verify that its existing description and managed cue remain consistent with the above. Preserve bounded triggered maintenance, named-task execution bookkeeping, default inferred creation/closure approvals, and local gates.
- Do not broaden this task into another task-lifecycle redesign. No source edit is needed if the current text already satisfies the shared reading principle.

### Phase 2: Make new and existing managed sections consistent

- Update creation-time templates in each owning source; use real confirmed resource locations on adoption, never literal example paths.
- Permit an explicitly authorized cue-only refresh even when paths have not changed; route callers to the relevant reference for that case.
- Replace old default cues that wrongly require invocation just to read. Preserve genuinely customized human behavior, stricter gates, other owners' sections, outside text, and block positions.
- Ask about conflicting customized instructions rather than silently overriding them. Preserve marker/concurrency/path validation and legacy migration approval boundaries.
- Source edits and sync do not refresh existing workspace guidance. State the required separate adoption step in the implementation receipt.

### Phase 3: Align durable contract and prove source consistency

- Under project-docs, update affected passages of `docs/workspace-configuration.md` to describe independent reading, lean routing, post-maintenance reachability, and authorized cue refresh.
- Check `docs/skills-catalog.md` for affected invocation wording, especially KB recall. Change only entries that would otherwise compete with the source contract.
- Extend existing scenario documents with focused cases below. Avoid new test infrastructure or exact-wording tests that only mirror prose.
- Separate independent-reader scenario setup from maintenance setup. The current KB scenario introduction tells trial agents to load the skill and references; that would invalidate a test intended to show reading without invocation.
- Review descriptions, main bodies, routing templates, retrieval/backend references, and affected docs for contradictory load-before-read rules and accidental broadening of write scope.
- Verify the task's actual state and next action after implementation; leave clear publication/adoption and live-behavior gaps in the receipt.

## Acceptance and verification

Required source checks and scenario walkthroughs:

| Case | Expected outcome |
| --- | --- |
| Docs discovery from an architectural question, no filename supplied | Relevant configured entry point/document is consulted without needing project-docs solely to read; intended constraints and current implementation are distinguished. |
| KB known-path reading and vague prior-context recall | Known path is read directly; otherwise bounded indexes/search locate relevant material without requiring the full maintenance workflow. |
| KB cross-month, conflicting, or stale synthesis | Retrieval detail is selectively consulted when needed; evidence/provenance/applicability is retained, without loading capture procedures merely to read or silently repairing records. |
| Remote KB or external knowledge-page root | Exact configured identity/scope is honored; unavailable tools or ref-specific search limits are disclosed, not bypassed. |
| Existing lesson and conditional procedure | Inline rule is followed and relevant detail read without invoking lessons maintenance; unrelated references are not all loaded. |
| No relevant saved context or inaccessible root | No irrelevant sweep, invented path, initialization, or maintenance write. Missing essential context is an explicit gap. |
| Authorized maintenance produces or updates useful content | Appropriate existing indexes/links are maintained and verified; no per-output AGENTS.md accumulation; legitimate no-op remains valid. |
| Cue-only refresh with an old default and custom wording | Conflicting default is replaced within the owned section; human text, stricter gates, positions, and neighboring sections survive. |
| Reader has managed guidance/resources but no exposed maintenance skill | It can still discover and use the resources with available read tools; maintenance unavailability is not falsely presented as a reading blocker. |
| Task regression and local gates | Independent task reading and existing execution bookkeeping remain consistent; reading never supplies new write/implementation permission. |

Use `tests/workspace-workflow-scenarios.md` and, where retrieval-specific behavior belongs there, `tests/knowledge-base-scenarios.md`. Review their existing cases before adding duplicates.

Run proportionate existing checks after implementation, through the applicable manage-python-env workflow. The repository's existing static workspace checks can be run with:

```text
uv run --no-sync python -m unittest discover -s tests -p test_workspace_contracts.py
git diff --check
```

Confirm the configured Python execution environment before using that command; it is not permission to bypass its owning workflow. Broaden tests only for affected behavior or failures. Static checks cover metadata, links, and template structure, not model behavior.

No description-versus-guidance experiment is required. Record scenario walkthroughs as walkthroughs. If a separately authorized fresh-session trial is performed, record model/harness, source or installed revision, supplied guidance, and observed reads/skill invocations/writes. Do not label static review as a live trial or promise universal compliance. Source implementation may complete with live-harness validation explicitly unverified.

## Executor discretion and stop conditions

- Exact prose, ordering, link placement, and small consolidation choices are executor-owned once source edits are approved. Do not force identical wording or equal change size across skills.
- Reuse existing resources. No separate umbrella skill, generated registry, database, automatic scheduled sweep, or employer-workspace migration.
- Stop for ambiguous ownership, conflicting human-customized guidance, a need to change authorization semantics, or an implementation that cannot preserve retrieval boundaries. Surface the specific decision rather than restarting the whole design.
- No known functional dependency on another unfinished task. The already committed task change is a reference implementation, not proof of cross-harness adoption.

## Resume Context

All paths below are repository-relative to `C:\Users\tanch\.agent-core`.

- Before any implementation: `AGENTS.md` — canonical stewardship, skill-edit approval, owned surfaces, publication boundaries, and task-write policy.
- Before designing guidance changes: `docs/workspace-configuration.md` and `docs/skill-design-guide.md` — canonical owner/routing contracts, selective admission, source/publication/adoption separation, and skill design criteria.
- Before docs changes: `skills/project-docs/SKILL.md` and `skills/project-docs/references/routing.md` — maintenance owner, claim authority, and current reader cues.
- Before KB changes: `skills/knowledge-base/SKILL.md`, `skills/knowledge-base/references/routing.md`, `skills/knowledge-base/references/retrieval.md`, `skills/knowledge-base/backends/filesystem.md`, and `skills/knowledge-base/backends/github.md` — current read dependencies and retained retrieval/backend boundaries.
- Before lessons changes: `skills/agent-lessons/SKILL.md` — existing future-use test, owned marker section, conditional pointers, and verification distinction.
- Before cross-skill consistency review: `skills/project-tasks/SKILL.md`, `skills/project-tasks/references/routing.md`, and commit `22fdd5f` — already implemented independent reading and triggered maintenance pattern.
- Before validation: `tests/workspace-workflow-scenarios.md`, `tests/knowledge-base-scenarios.md`, and `tests/test_workspace_contracts.py` — existing behavioral specifications and static coverage limits.
- Before documentation alignment: `docs/skills-catalog.md` — invocation/discovery summaries that must not contradict updated skills.

## Handoff review and reporting

- This task preserves the selected design, rationale, implementation scope, approval boundary, verification requirements, and next action without requiring the old conversation.
- Docs integration is a planned implementation deliverable; do not present the proposed behavior as already implemented canonical truth.
- No separate KB capture or standing lesson is needed for this handoff: the material is an unfinished repository design, supported by the exact canonical sources above. Do not duplicate it into a new storage surface.
- Final implementation receipt should identify exact changed paths, checks actually performed, meaningful no-ops, and remaining approval/access gaps. Separately state source completion, installed publication, workspace adoption, and any live-harness verification.
