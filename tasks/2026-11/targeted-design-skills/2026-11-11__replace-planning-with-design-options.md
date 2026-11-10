# Task: Replace broad planning with design-options

**File:** `tasks/2026-11/targeted-design-skills/2026-11-11__replace-planning-with-design-options.md`
**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Next
**Status:** Active

**Goal:** Replace the general `planning` skill with **`design-options`**, a request-led skill for generating and discriminating genuinely different approaches to consequential software/product-system design decisions.

**Why:** The old skill became a general pre-execution process and could reactivate analysis after a direction was already settled. The human wants fewer, more targeted activations. Their original inspiration was a prompt that countered premature commitment by considering genuinely different approaches before selecting the leading one(s). This replacement should make that discipline concrete without becoming a universal thinking framework.

**Deliverables on later execution:** A standalone `skills/design-options/SKILL.md`; focused behavioral cases; retirement of the old canonical planning skill with recoverable history; directly affected routing/catalogue/reference reconciliation; and an honest source-versus-installation receipt. References are optional and must earn their retrieval cost. No new planning service, task format, or mandatory decision document.

**Success Bar:** On an invited, material design choice, the agent presents feasible approaches that differ in mechanism, evaluates them on common grounded criteria, and recommends a leader or a bounded way to resolve a real tie. On routine implementation, persistence, or already-approved work, it stays inactive. Its answer should change or substantiate a decision, not merely add a plan-shaped document.

**Chosen Direction:** **Selected by the author under the human's explicit delegation to make the final design/name call.** Name: `design-options`. Job: compare technical solution designs before consequential commitment. Request-led activation; no automatic linkage to implementation. This task replaces the proposed role of the old planning skill completely, rather than adding a special mode to it.

**Current State:** Task/design only; no replacement skill implemented. On 2026-11-11 Agent Core was clean on `main` at `25522dfa4462640ed0f59d0aaa534a4d19d70039`. `personal-skills.toml` excludes both `planning` and `engineering`, while their canonical source directories still exist and some docs/skills still reference them. Both old skills are unavailable to this session and must not be invoked. Their presence on disk is not active authorization or proof of harness installation.

**Next Action:** Wait for a human request to implement this task. Then inspect current repository state and direct references, implement the selected design, and retire/reconcile the old source within the approved scope. Do not restart broad design exploration unless new evidence exposes a concrete conflict with this brief.

**Blockers:** None for understanding this handoff. Production edits and installation are not authorized by the current task-writing request.

## Permission and decision ownership

- Current authorization: research, choose the vision/name, and write this task plus its sibling and affected index entries in `C:\Users\tanch\.agent-core`. **No implementation now.**
- A later request to implement this task should authorize its explicitly described source and direct-reference changes. Commit, push, harness publication/removal, paid tools, and consumer-repository changes remain separately scoped actions. Recheck the actual request and repository guidance at that time.
- Locked for this brief: narrow design-choice purpose, request-led activation, materially different alternatives, common comparison criteria, a convergent result, and no compulsory persistence or execution pipeline.
- Executor-owned later: wording, internal section organization, whether any short supporting reference is worthwhile, and the smallest representative checks. Do not copy this detailed task wholesale into the skill.
- The human retains decisions about their product, architecture, spending, and deployment. Delegating the **skill design** is not delegating every future consequential decision to that skill.

## Vision: choose the approach, not the task list

The central question is: **"What are the credible, materially different ways to solve this design problem, and which fits our constraints best?"**

A good use has three properties: a consequential unresolved choice, plausible alternative mechanisms, and a human request to explore/compare those approaches. Consequence is concrete—state ownership, authority, failure semantics, meaningful operating cost, or an expensive commitment—not a generic assertion that all software is important.

Highest-value situations:

1. **Ownership and boundary decisions:** where state, domain rules, trust, or integration responsibilities should live. Example: how a website and assistant share approval/revision behavior without competing write authority.
2. **Execution/data strategy with real tradeoffs:** synchronous versus asynchronous processing, snapshots versus a revision history, local versus remote computation, or reconciliation strategies. Compare the mechanism and consequences, not buzzwords.
3. **Commitments with material switching cost:** infrastructure or provider arrangements where identity, operations, constraints, and migration consequences materially differ. A simple feature/price lookup does not itself require this skill.

It is not an all-purpose roadmap planner, brainstorming companion, prioritization method, skill-writing workflow, or approval gate. Product strategy and ordinary advice can be handled without it. Its scope is software/product-system design alternatives, not every life or business decision.

## Activation contract

The description must express the narrow job and human-intent boundary. Keep normal model discoverability; do not rely on a harness-specific disable flag to enforce request-only use.

**Activate:** a named invocation, or a clear request such as "Explore genuinely different architectures before recommending one", "Compare the main ways to handle approval and revisions", or "Challenge our proposed processing approach against credible alternatives."

**Do not activate merely because:** the user says plan, build, implement, proceed, review, architecture, or important; a task exists; work is large; the agent can imagine an alternative; the chat concerns editing a Markdown skill; or the previous conversation used this skill.

**Negative examples:** "Implement the approved design", "Save our decision in a task", "Break the agreed work into steps", "Fix this bug", "Write a skill from this approved brief", and "What's next?" do not start this workflow. A generic "review this plan" remains ordinary review unless the user requests substantive design alternatives or invokes this skill.

If a relevant unresolved choice appears during unrelated work, the agent may briefly identify the choice and suggest an options comparison. It must not silently start the workflow, repeatedly solicit activation, or block ordinary authorized work just to use the skill. An actual unresolved consequential decision may still require clarification under the ordinary task's rules.

Activation lasts for the selected decision, including relevant follow-up. It ends when that decision is settled, explicitly paused, or replaced. It does not turn the rest of the session into a planning mode.

## Distinctive method to encode

### 1. Frame the decision before favoring an answer

Read enough relevant evidence to identify the desired outcome, binding constraints, actual decision owner, and what has already been decided. Separate constraints from preferences and observed facts from forecasts. Establish the few criteria that can discriminate the options before ranking them; do not tailor the criteria afterward to justify a favorite. If new evidence changes the criteria, say why and apply the change to all candidates.

Do not ask the human to repeat information the agent can discover. Ask one consequential clarification at a time only when it would change the comparison. Do not run a questionnaire or demand that the human invent the alternatives.

### 2. Generate alternatives that differ in mechanism

Look along relevant axes: ownership, persistence model, timing, coupling, computation placement, trust boundary, or reliance on an external system. Usually a small set is enough; there is no quota of three options. Renaming vendors, offering small/medium/large versions of one design, or listing a deliberately impractical option does not constitute genuine exploration.

Include the current arrangement, doing less, or postponing commitment when genuinely viable. Do not manufacture a status-quo option when it violates the required outcome. If constraints leave only one credible design, explain the elimination and stop rather than inventing diversity.

Before choosing, make each serious candidate concrete enough to compare: a short flow/ownership sketch, what it requires, what it gives up, and the context where it would win. Do not implement multiple prototypes just to demonstrate diligence.

### 3. Compare with the same concrete situations

Apply the same representative workload, user flow, failure condition, and relevant change scenario to each candidate. Pick only dimensions that can change this decision. Expose costs and complexity displaced to another component, provider, operator, or user. Avoid ungrounded numeric scores and false precision; a small comparison table is useful only if it clarifies the decisive differences.

Treat the human's favorite and the agent's initial favorite as candidates, not facts. State the strongest credible case against the provisional winner and the circumstances where a rival wins. This is structured challenge, not a claim of independent review or a guarantee of eliminating model bias. No automatic subagents, debate teams, or repeated sampling.

### 4. Spend investigation on the discriminator

Research the fact whose answer could change the recommendation. If a bounded experiment is needed, identify what it would distinguish and whether it is authorized; a comparison request does not authorize provisioning, spending, or production changes. Stop researching when further information would not materially affect the choice.

Distinguish a reversible choice that can reasonably be made now from a consequential unknown that should gate commitment. Avoid using "needs more research" as an indefinite escape from judgment.

### 5. Converge and stop

Recommend the leading approach, its deciding reasons, the accepted tradeoff, and the evidence/condition that would reverse the recommendation. If two options remain genuinely tied on a consequential unknown, retain only those leaders and name the smallest useful discriminator. Do not end with an unranked menu or ask the human to do the entire synthesis.

Output a decision brief, normally compact: **decision → credible alternatives → recommendation and tradeoff → material uncertainty/next decision**. This is a useful shape, not mandatory headings. No formal depth modes are needed initially; explicit requests for depth or a time budget control the amount of evidence and exposition.

Once the human has selected the approach, stop exploring unless new evidence contradicts a material assumption. Recording a plan or executing an approved direction must not retrigger this skill.

## Relationship to other capabilities

- [Code-design replacement](2026-11-11__replace-engineering-with-code-design.md): asks how a bounded code area should be organized for understandable, safe change. `design-options` compares consequential solution approaches. They are independent; neither automatically invokes the other. Code-design may compare local module arrangements without launching this broader comparison.
- `reasoned-advocacy`: evaluates/communicates a position and its evidence. This skill's distinctive deliverable is candidate **technical designs** and a selection grounded in their mechanisms, not generic argumentation or stakeholder speaking points.
- `grilling`: human-facing sequential interrogation. Here the agent investigates and proposes alternatives; it should not shift the exploration burden onto the human.
- `blind-comparison`: explicitly independent/anonymized review. Same-agent option generation must never be described as blind or independent.
- Project tasks/docs own requested persistence. No auto-created ADR, plan file, task, or KB entry. No required companion skill to give the answer.
- The [verification proposal](../verification-design/2026-11-11__evaluate-agent-led-verification.md) remains undecided. It is not an implementation dependency or a reason to add a verification platform to this skill.

## Research basis and limits — consulted 2026-11-11

| Source | What it supports | Limit / design consequence |
| --- | --- | --- |
| [Design Council: Double Diamond](https://www.designcouncil.org.uk/our-resources/the-double-diamond/) | Understand/define the problem, develop different answers, then test/select rather than assume the first framing. | A design-process framework, not an experiment proving better LLM decisions. Borrow divergence/convergence; do not impose its full organizational process. |
| [SEI: ATAM report landing page and abstract](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/) (2000) | Architecture involves tradeoffs among performance, availability, security, and modifiability. | Only the landing page/abstract was read, not the PDF. It supports explicit quality tradeoffs, not a claim that this lightweight skill implements formal ATAM. |
| [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) (2015) | Premature capabilities have build, delay, carry, and repair costs; later change can be reasoned about rather than assumed expensive. | Practitioner reasoning, not a universal rule against up-front design. Include simpler/reversible choices while preserving known requirements. |
| [Evaluating AGENTS.md, v3](https://arxiv.org/html/2602.11988v3) (2026-09-29) | In tested Python issue-resolution settings, additional context increased exploration/testing and cost without a statistically significant success improvement over no context. | Not a study of this skill, design quality, greenfield work, or long-term maintainability. Motive to test selective activation and useful output, not proof that guidance is bad. |

The human's concern about premature model convergence is a design motivation, not a measured diagnosis of this model. This research did not establish that one agent proposing several options removes anchoring or reliably improves decisions. Web search returned no results for several targeted queries, including LLM anchoring; the usable evidence came from directly retrieved primary sources. No broad/current-market coverage or empirical debiasing result is claimed. Two attempted Fowler pages on refactoring returned 404 and were not used as evidence.

## Implementation and replacement work — future, not executed

1. **Reconcile the live scope:** Read applicable Agent Core guidance, this brief, current source/manifest/catalogue, and direct references. Treat old planning instructions as historical migration input, not an execution prerequisite. Preserve unrelated changes.
2. **Write the focused skill:** Encode the trigger boundary and the distinctive option-generation/comparison method. Keep operational boilerplate out. The description itself must make it hard to activate on ordinary planning or skill editing.
3. **Retire the old canonical owner:** When implementation is requested, archive the existing `skills/planning/` under a dated historical location if it still exists, preserve meaningful history, and remove the active old owner. Do not restore it or create a compatibility alias with the same broad triggers if the human already removed it.
4. **Reconcile direct consumers:** Update the catalogue/design-guide entries and the skill manifest as included in the later source-implementation request. Audit direct invocation instructions in `skills/project-tasks/SKILL.md`, not every generic use of the word "planning". Replace automatic planning requirements with ordinary decision work plus a conditional pointer to the new **request-led** job. Preserve the need for approval where consequential decisions require it; do not make this new skill mandatory to save a task. Reconcile the verification task's obsolete "load planning" next action when this migration is authorized. Coordinate shared-file edits with the sibling task; do not overwrite its work or mass-replace terminology.
5. **Check behavior selectively:** Use representative positive, negative, and counterexample cases below. Review actual output/action traces if a model trial is authorized and available. Otherwise identify them as unexecuted scenarios. Structural checks alone cannot establish non-activation or decision quality.
6. **Report source and adoption separately:** Normal sync is selected-harness, clean-committed-source publication. Removing a manifest entry does not uninstall old managed copies. Any installed-resource retirement needs its own explicit supported migration scope; never hand-delete or hand-copy global skills. Consumer projects such as Tripverge are not writable merely because this Agent Core task is executed.

## Acceptance scenarios for later validation

| Situation | Expected behavior |
| --- | --- |
| "Compare genuinely different ways to share revisions between a website and assistant" | Activate; compare real ownership/data-flow designs against the same constraints and converge. |
| Human favors a distributed design; a simpler approach meets the evidence | Present the simpler candidate fairly and recommend it if supported; do not rubber-stamp the user's favorite. |
| Constraints eliminate all but one candidate | Explain why the alternatives fail; no artificial three-option menu. |
| The leading option depends on unverified host support | Identify that discriminator, qualify the recommendation, and propose a bounded check rather than claim compatibility. |
| "Implement the design we approved" / "save it as a task" | No new alternatives exercise, extra approval ceremony, or skill activation solely from the wording. |
| "Write the learning skill using the approved brief" | Ordinary instruction editing; no automatic planning or codebase workflow. |
| "What should I do next?" or "review this plan for omissions" | Ordinary response/review unless a specific comparison is requested. |
| More depth requested after a selected design | Deepen relevant rationale; do not reopen settled choices without contrary evidence. |

Evaluate whether candidates differ materially, receive fair scrutiny, and lead to an actionable recommendation; evaluate false activation and unnecessary extra work as failures too. A scenario written in this task is not a performed trial.

## Resume context and completion boundary

- Working repository: `C:\Users\tanch\.agent-core`.
- Read first: [AGENTS.md](../../../AGENTS.md), [Skill Design Guide](../../../docs/skill-design-guide.md), and [Skills Catalogue](../../../docs/skills-catalog.md). The catalogue currently overstates active availability of the old skills; the manifest/session availability are separate evidence.
- Read before publication only when authorized: [Operating Manual](../../../docs/agent-core-operating-manual.md).
- Related selected vision: [code-design](2026-11-11__replace-engineering-with-code-design.md). Neither task requires the other to be implemented first.
- Product examples are illustrative, informed by Tripverge at `C:\Users\tanch\Documents\Github\tripverge`; consult that repository's current guidance/docs before making real product decisions. This task approves no Tripverge change.

This writing pass preserves the selected design and research; it does not implement, retire, install, or test the skill. The task remains Active for future requested implementation. Resume with: **"Implement the design-options replacement task in Agent Core."**
