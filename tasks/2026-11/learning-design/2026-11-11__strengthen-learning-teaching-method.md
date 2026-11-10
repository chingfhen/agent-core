# Task: Strengthen the learning skill's teaching method

**File:** `tasks/2026-11/learning-design/2026-11-11__strengthen-learning-teaching-method.md`
**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Now
**Status:** Closed

**Closure:** Completed the authorized canonical source revision and audit record on 2026-11-11. This closes source editing and author/static review, not harness publication or empirical validation of teaching effectiveness.

**Goal:** Improve how the standalone `learning` skill frames, explains, and adapts teaching while preserving Quick, Standard, and Deep.

**Why:** During a Tripverge workflow assessment, the human wanted agent-led technical understanding rather than repeatedly having to request missing explanations. The human then narrowed this implementation to teaching quality: genuinely consider different methods, select the useful ones, and encode them in the existing canonical skill. Proactive teaching is wanted; automatic assessment or proof of human understanding is not this skill's job. Time constraints make a genuinely useful Quick mode essential.

**Deliverables:** Revised canonical learning skill, updated existing behavioral scenarios, and this detailed implementation/rationale record. A separate verification-design handoff preserves the other proposed capability without implementing it.

**Success Bar:** The skill helps an agent choose an explanation strategy for the learner's actual gap; explains with concrete causal links and discriminating examples; deepens without unnecessary repetition; repairs confusion by changing representation; respects requested depth/time; and remains standalone, general-purpose, and teaching-only. Acceptance concerns observable instruction/output quality, not a claim of measured comprehension.

**Chosen Direction:** Explicitly approved: edit `skills/learning/SKILL.md` directly and autonomously choose teaching improvements. Retain all three modes. Treat verification as an undecided proposal for another session.

**Current State:** Canonical `skills/learning/SKILL.md` is revised and the existing behavioral scenarios are updated. Changes are local and uncommitted. The installed OpenCode copy was inspected as the prior 168-line version and was not modified or synced. Agent Core was clean on `main` at `3f7632f13567db91172903b3d54e825d334ebd2e` before this work. An unrelated concurrent manifest edit was observed at final status review and preserved; see verification notes.

**Next Action:** None for the completed source-edit scope. Commit/publication and installed-harness trials require a separate request. Verification-design continuation belongs to the linked task and remains undecided.

**Blockers:** None for the completed scope. Runtime publication is outside this completion claim and requires the authorized clean, committed-source delivery workflow.

## Permission and scope

- The human explicitly authorized this production skill edit and these task records in `C:\Users\tanch\.agent-core`. Repository task writes are otherwise opt-in.
- Edit the canonical skill and directly related behavioral scenarios. Keep the skill usable without Tripverge, other skills, code access, a persistent learner profile, or a particular harness.
- Do not create or implement `verification`, change engineering/Git policies, modify Tripverge, introduce scheduled teaching, or broaden into a general skill cleanup.
- No commit, push, harness sync, installed-copy edits, or subagent launch is authorized by this task. The requested delegation is a portable task for another human-started session.
- This audit record remains at its stable path when closed. Only unfinished work belongs in `tasks/INDEX.md`.

## Evidence and diagnosed weak points

Inspected `AGENTS.md`, `docs/skill-design-guide.md`, `docs/agent-core-operating-manual.md`, the canonical and installed learning skill, `tests/learning-scenarios.md`, the task index, and targeted related task matches. No nested guidance was found beneath `skills/` or `tasks/`; no ancestor `AGENTS.md` was found at the checked user/Users/drive roots.

1. **Good ingredients, weak method selection:** The existing skill lists causal chains, examples, mechanisms, judgment, and caveats. It gives fewer rules for deciding when to use a trace, contrast, explanation of purpose, or a component map. An agent can satisfy the vocabulary without resolving the learner's particular confusion.
2. **Abstraction can arrive too early:** A mental-model-first instruction can still produce several unfamiliar terms before the learner has a concrete referent. An anchor example and just-in-time terminology can make the mechanism easier to follow.
3. **The distinctive difference can stay implicit:** Definitions alone often fail to distinguish adjacent ideas. One controlled contrast can reveal the condition that changes the result.
4. **Completeness competes with limited time:** Listing predictions, decisions, failure cases, and inspection methods can encourage cramming all of them into Quick. Depth should control the explanatory scope; Quick must retain one complete causal bridge, not every facet.
5. **Confusion repair is under-specified:** The current instruction to diagnose the missing link is sound, but needs concrete representation changes rather than a longer paraphrase.
6. **Completion overreaches observable evidence:** The skill and scenarios refer to learner understanding as the completion criterion. The revision should own the explanation, not assess, grade, track, or claim the human's comprehension.

These are design judgments from instruction review, not measured failures in representative model trials or findings from a new educational study.

## Approaches considered and decision

| Approach | Useful property | Decision |
| --- | --- | --- |
| Socratic/tutor-first questioning | Can expose the learner's current model | Not the default or assessment mechanism; conflicts with time constraints and the requested teaching-only scope. Ask one clarification only when it materially changes the explanation. |
| A fixed explain-everything template | Predictable coverage | Reject as the universal output shape. It can bury the answer and inflate Quick. Use an internal method selector instead. |
| Analogy-first explanation | Can offer a familiar bridge | Conditional tool, not the backbone. Explicitly map and bound it, then explain the actual mechanism. |
| Concrete worked example, then generalization | Gives unfamiliar terms stable referents and makes causal steps inspectable | Primary method for mechanisms and unfamiliar abstractions. Keep one example through the explanation. |
| Minimal contrast / counterfactual | Isolates why outcomes differ or a step matters | Primary method for distinctions and misconceptions, paired with a mechanism rather than slogans. |
| Progressive depth and representation repair | Respects time and avoids repeating what is already clear | Primary control strategy. Quick answers completely within a narrow scope; deeper modes expand meaningful scope. Change representation when an explanation does not land. |

## Implemented changes

1. Preserved the human-understanding purpose and grounding/permission boundaries; changed the completion bar to delivered teaching rather than assessed human comprehension.
2. Retained Quick/Standard/Deep with distinct teaching scope: one complete insight, one usable model, and reasoning across conditions. Time constraints narrow scope rather than compressing a textbook; deeper follow-ups build on the same case.
3. Added a gap-to-method selector and an anchor → mechanism → reusable principle composition guide. Controlled contrasts reveal pivotal differences. Neither is a mandatory response template.
4. Made framing concrete: answer early, use stable nouns and active verbs, introduce terminology beside its role, keep causal links adjacent, bound analogies, and avoid redundant formats or repeated caveats.
5. Added specific confusion-repair moves and bounded proactive teaching: supply prerequisites inside the current lesson; honor invited ongoing teaching at meaningful moments; respect a current request to skip it.
6. Updated `tests/learning-scenarios.md`: preserved the existing 12 cases, aligned acceptance with teaching rather than comprehension assessment, and added 7 cases for the changed behavior (19 total). These are specifications, not model-trial results.
7. Created the separate verification proposal handoff and updated the active task index. The completed learning audit remains reachable from that handoff and by its stable path, rather than remaining in the unfinished-work dashboard.

## Verification and outcome

- Reviewed the complete tracked diff and read both new tasks. Checked the permission boundaries and fresh-session next action against the human's latest request.
- PowerShell checked the five changed files' 21 relative Markdown destinations, learning frontmatter shape, all three mode markers, absence of Unicode replacement characters, 19 scenario headings, and task/index lifecycle consistency. All checked conditions passed. This is structural validation, not a full YAML parser or harness activation test. A follow-up check using PowerShell's default `Get-Content` decoding falsely reported missing Unicode mode labels; rerunning with explicit UTF-8-capable `.NET ReadAllText` passed without changing the skill text.
- `git diff --check` passed; Git reported only the repository's LF/CRLF conversion notices. No runtime code changed, and no Python execution or application test suite was needed for these Markdown changes.
- During review, corrected the new race scenario to place another write **between** a separate check and write. An already-stale value alone would not demonstrate that race. Also clarified that teaching permits relevant source inspection while not authorizing implementation or test execution by itself.
- Author-reviewed the examples below against mode depth, causal accuracy, stable referents, absence of quizzes, and illustration-versus-observation boundaries. They illustrate the intended behavior; they are not independent model outputs, fresh-session trials, or measured learning gains.
- Reviewed existing nontechnical, unavailable-vendor-API, no-persistence, and ordinary-implementation cases for compatibility. Ongoing teaching remains an explicit invitation, not an automatic lecture on every edit.
- This work made no commits or pushes and did not edit installed copies, manifests, catalogues, engineering rules, Tripverge files, or harness settings. The existing catalogue description remains accurate; the revised skill frontmatter supplies its more specific activation cue.
- Final status inspection found an unrelated concurrent edit to `personal-skills.toml` removing `planning` and `engineering`. It was absent at initial clean status. Inspected its diff and left it untouched and unstaged; no ownership or intent was inferred. Any later delivery must preserve/reconcile that work rather than treating the whole working tree as this task's changes.

### Representative authored teaching examples

These synthetic examples are design walkthroughs authored during this revision, not actual Tripverge behavior. Mode markers are shown as they would appear in a teaching response.

**Learning · Quick** (also: Standard / Deep)

Checking and saving separately leaves a gap. Imagine A checks revision 7, B then saves revision 8, and A writes using its earlier check: A can overwrite B's change. Making the revision comparison and update one indivisible database operation closes that gap. That is what “atomic” means here; this example explains the required mechanism, not a verified implementation.

**Review:** One timeline exposes the pivotal race and defines the term through its role. No database survey, test claim, or learner question.

**Learning · Standard** (also: Quick / Deep)

The cached price becomes stale because changing the source price does not necessarily change the cached copy. In this illustrative case, the cache stores $20 at noon with a five-minute lifetime. The source changes to $25 at 12:01, but a request at 12:02 can still get the unexpired $20 entry. Expiry bounds how long that copy is reused; explicitly invalidating it on a price change can shorten the stale window but adds coordination. To inspect the behavior, compare the source value, cached value, and expiry time rather than checking only that the request succeeded.

**Review:** One case carries the source/cache distinction, causal sequence, tradeoff, and inspection clue. It extends the earlier hit/miss concept without reintroducing it.

**Learning · Deep** (also: Quick / Standard)

A database transaction can roll back its own writes; it does not automatically reverse a payment already accepted by another system. In an illustrative checkout, the payment provider accepts the charge, then the local database write fails. The local rollback can leave “charged externally, no completed order locally.” Reversing the order creates another failure window: the database can record an order before payment succeeds.

The design therefore needs to represent intermediate states and recover across the boundary. A pending order plus a durable work item committed together can let a worker retry delivery to the payment provider after a crash. That still does not make the external call exactly-once: if the response is lost after a successful charge, a retry needs a provider-supported idempotency mechanism or reconciliation to avoid a second charge. Compensation, such as a refund, is another operation with its own possible failure, not a database rollback. The useful design question is which partial states are allowed and how each is detected and resolved; the right answer depends on the actual provider and product contract.

**Review:** Develops the same boundary through two orderings, a recovery design, and its limits. Does not invent a provider API, promise universal exactly-once behavior, or require an answer from the reader.

### Persistence disposition

This task records the requested rationale/audit. The skill owns the actual teaching behavior; the verification task owns its unresolved proposal. Bounded handoff review found no separate KB capture, project-docs edit, or durable agent lesson needed. `C:\Users\tanch\.agent-core\AGENTS.md` was inspected and remains unchanged. No generalized preference or workflow rule was copied into unrelated guidance.

## Resume context

- Before any continuation: [Agent Core guidance](../../../AGENTS.md) — canonical edit permission, task ownership, and publication boundaries.
- For skill design: [Skill design guide](../../../docs/skill-design-guide.md) — standalone scope, trigger design, and proportionate instruction quality.
- Behavior authority: [Learning](../../../skills/learning/SKILL.md).
- Acceptance examples: [Learning scenarios](../../../tests/learning-scenarios.md) — specifications, not model-trial results.
- Before publication, only if separately authorized: [Operating manual](../../../docs/agent-core-operating-manual.md) — committed clean-source and selected-harness sync requirements.
- Related unfinished proposal: [Evaluate agent-led verification](../verification-design/2026-11-11__evaluate-agent-led-verification.md) — separate permission boundary; does not gate this teaching edit.
