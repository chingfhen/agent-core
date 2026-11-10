# Task: Replace broad engineering with code-design

**File:** `tasks/2026-11/targeted-design-skills/2026-11-11__replace-engineering-with-code-design.md`
**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Next
**Status:** Active

**Goal:** Replace the general `engineering` skill with **`code-design`**, a request-led specialist for shaping a bounded code area so humans and agents can understand and safely change it without carrying unnecessary knowledge across the system.

**Why:** The human's original motivation was good code and good codebases. The old skill grew into a default implement/debug/test/review/commit workflow and activated on work such as Markdown skill editing. The replacement should add substantive code-design judgment at high-leverage moments, not supervise every code change or repeat baseline coding-agent instructions.

**Deliverables on later execution:** A standalone `skills/code-design/SKILL.md`; focused design/activation scenarios; recoverable retirement of the old engineering source; direct-reference/catalogue/manifest reconciliation; and an honest source/adoption receipt. No new general engineering, debugging, verification, or repository-management framework.

**Success Bar:** On a requested code-design intervention, the agent identifies a concrete comprehension/change burden, selects a proportionate improvement or justified no-change result, and explains its effect using actual responsibilities, interfaces, and a grounded change scenario. Where implementation is authorized, observable contracts remain intact except for explicitly requested changes. Routine code work and non-code editing do not activate the skill. Fewer lines, more layers, or passing tests alone are not proof of better design.

**Chosen Direction:** **Selected by the author under the human's explicit delegation to make the final design/name call.** Name: `code-design`. Focus: local reasoning, coherent ownership, useful interfaces, and changeability in a bounded module/subsystem/diff. This replaces the old engineering skill completely; it is not its Deep mode under a new label.

**Current State:** Task/design only; no replacement implemented. On 2026-11-11 Agent Core was clean on `main` at `25522dfa4462640ed0f59d0aaa534a4d19d70039`. Both old skills are absent from `personal-skills.toml` and unavailable to this session; canonical directories remain, and the catalogue/other sources retain references. Presence on disk does not mean availability, installation, or permission to invoke an old skill.

**Next Action:** Wait for a human request to implement this task. Then inspect live state and the relevant neighboring workflows, create the focused skill and scenarios, and reconcile the old owner/direct references within the later approved scope. Do not rebuild general engineering around it.

**Blockers:** None for understanding this handoff. Current authorization is task writing, not production skill implementation or publication.

## Permission and chosen boundaries

- The human authorized the author to choose this vision and new name, research it, and save two tasks plus affected index entries. **No implementation now.**
- A later explicit implementation request can cover the source and direct-reference changes described below. Commits, pushes, harness sync/removal, consumer code changes, external services, and spending require their separately established scope.
- Locked: software-code-only purpose, request-led activation, bounded design intervention, grounded changeability/reader burden, proportional behavior preservation, and no default Git or persistence effects.
- Executor-owned later: concise wording, conditional reference use, appropriate representative code fixtures, and specific check mechanics. Do not turn this detailed design brief into a long mandatory procedure in the skill.
- This skill is standalone. Ordinary authorized coding still happens without it. Users do not have to invoke a specialist to receive correct, maintainable code.

## Why this direction, rather than the earlier suggestion

An earlier conversation suggested specializing engineering in high-risk correctness and difficult debugging. That could be useful, but it would move the user's codebase-quality motivation toward failure investigation and overlap the separate undecided verification proposal.

The selected direction is **design for understandable, localized change**. Correctness, authorization, and state integrity are constraints that the design must preserve, not a mandate for this skill to become a complete testing/security/debugging workflow.

Other considered framings:
- **General clean-code checklist:** rejected; easy to activate everywhere and encourages style or metric compliance.
- **Whole-codebase health audit:** rejected; broad scope and overlap with retained `repo-audit`.
- **Refactoring-only:** too late/narrow; the best time to choose a good interface can be when a significant domain module is first written.
- **Always choose the shortest implementation:** rejected; fewest lines/files can concentrate hidden coupling, while useful abstractions sometimes reduce the knowledge needed to make a safe change.
- **A universal architecture/layering framework:** rejected; a sound boundary depends on actual behavior, language, framework, and likely changes.

## Highest-value situations

1. **A significant module or domain API is taking shape.** Several callers or side effects meet at a boundary, and ownership/interface choices will shape subsequent work. Example: a trip-edit operation shared by HTTP and assistant adapters. A routine CRUD route or scaffold does not automatically qualify.
2. **A concrete feature exposes costly coupling.** One rule is scattered across callers, a small change requires coordinated edits in unrelated places, or callers must know hidden ordering/state conventions. Improve the relevant structure before or alongside the requested feature; no unrelated cleanup programme.
3. **An important diff needs a structural review.** The requested lens is whether the change makes the code harder to understand/evolve: competing sources of truth, leaky interfaces, unnecessary indirection, confused responsibilities, or incorrect reuse. It is not a general bug/security review disguised as design review.

The key question is: **"What must a future reader know and change to perform this concrete operation safely, and can the design reduce that burden?"**

For new code, use approved requirements and representative usage/change cases. For existing code, anchor the concern in actual paths, callers, state, and constraints. Do not manufacture requirements to justify an abstraction.

## Activation and action contract

Activate only for a named invocation or a clear human request for the distinctive job: "Design this module's responsibilities and API", "Review this diff for maintainability and coupling", or "Restructure this subsystem so this rule has one owner." A request to refactor for a named structural problem can qualify. Generic "implement", "fix", "review", "refactor this variable", "write good code", or "proceed" does not qualify by itself.

No activation for editing skills/prompts/docs, writing tasks, changing styles, ordinary bug fixes, simple renaming, generic scaffolding, or incidental mentions of good architecture. Documentation in a codebase is still documentation; the presence of Git does not make every edit a code-design problem.

The agent may briefly point out a relevant structural concern during ordinary work, but must not silently load this workflow, expand the assignment, or turn every change into a design approval gate. The invocation ends with the bounded design work; it does not persist as a global session persona.

**Action follows the request:** a design/review request is read-only analysis; "implement/refactor using code-design" authorizes scoped code changes subject to normal project constraints. Explicit approved implementation proceeds without a second ceremonial approval. A behavior change, public-contract change, or broader architecture departure outside the request still needs its actual owner's decision. This is action-scope interpretation, not two new depth modes.

## Distinctive design judgment to encode

### 1. Identify the comprehension/change burden

Read the target code and only the callers/contracts needed to understand it. Trace one representative operation. State the concrete problem and consequence: duplicated business rule, hidden mutation, ordering dependency, coupled edits, leaked representation, or opaque errors. "Violates SOLID", "too many lines", and "not clean" are not sufficient findings.

If the target is already straightforward, keep it. A long but coherent algorithm may be easier to reason about than a chain of shallow helpers. Findings and refactorings are not quotas.

### 2. Put each important responsibility where it can be understood

- **Ownership:** who owns each domain rule, state transition, and authoritative value? Centralize the same rule when it otherwise drifts; do not combine unrelated rules just because their current code looks similar.
- **Useful interfaces:** a caller should need less information than the implementation contains. Keep essential preconditions, side effects, failure behavior, and units visible in names/types/contracts or concise comments. An interface that conceals critical caller obligations is not a good abstraction.
- **Cohesion and locality:** keep tightly related information together. Separate genuinely independent concerns; do not distribute one invariant across a forest of tiny functions or files just to satisfy a size preference.
- **Dependencies:** respect the established architecture and reduce unnecessary knowledge across boundaries. Prefer explicit state and dependency flow over hidden globals, temporal coupling, or bidirectional dependencies. Dependency inversion, functional cores, and adapters are tools for an evidenced need, not mandatory patterns.
- **Data and errors:** use representations that clarify valid states and boundary conditions where practical. Make meaningful failures explicit instead of replacing them with silent fallbacks. Preserve transaction, authorization, and recovery semantics while reorganizing code.
- **Navigability:** use domain-relevant names and predictable locations. Explain non-obvious contracts/rationale near their owner. More documentation or smaller functions are not automatic improvements.

Use only the lenses relevant to the concrete target; do not produce a checkbox audit of every dimension.

### 3. Evaluate a small structural improvement against a real change

Sketch the simplest adequate arrangement: what moves or becomes explicit, which responsibilities remain together, and what coupling/knowledge it removes. Compare with leaving the code as-is. One local alternative is often enough; do not automatically invoke design-options or generate several architectures.

Walk through a concrete required or credibly upcoming change using the candidate structure. Explain which owner/callers would change and why unrelated areas would stay unaffected. This is a design thought experiment unless actually executed. A speculative future feature is not permission to build its extension points.

Optimize **total reasoning/change burden**, including interfaces, indirection, duplication, and test complexity. More files can improve locality or fragment it; fewer files can simplify or entangle it. No universal function-length limits, arbitrary layer counts, mandatory class patterns, or cosmetic renaming campaigns.

Keep intentional duplication when the concepts can evolve independently. Extract a shared abstraction when shared semantics or demonstrated variation justify its ongoing cost, not simply because two blocks currently look alike.

### 4. Preserve behavior when implementation is requested

Make the smallest coherent structural change that delivers the approved outcome. Keep behavior-changing work distinguishable from structural movement. Preserve unrelated work and existing public contracts, side effects, and failure semantics unless a change is explicitly in scope.

Use existing relevant checks first. Add a focused characterization or regression check only when it protects uncertain/material behavior being changed. A successful build does not prove preserved behavior; a green suite does not prove maintainability. Conversely, a prose-only design review does not need tests merely because the skill is loaded. Expand checks for concrete affected contracts or observed failures, not to satisfy a universal ceremony. No mandatory test count, new framework, broad suite, temporary linter, or source-string assertions for every change.

A review can identify correctness concerns revealed by the design trace, but it should not silently become a full security audit, performance study, observability project, or debugging campaign. Report the specific scope/verification limit when relevant.

### 5. Show the design consequence and stop

For review: provide the material concern, evidence, the practical consequence, and a proportionate recommendation; no-change is valid. For implementation: explain the important before/after ownership or interface change, the concrete work it makes easier, and what behavior was actually checked. Do not claim quantified maintainability gains from intuition.

Stop once the selected structural issue is resolved or an explicit finding/recommendation answers the request. Do not keep searching for more "quality" work. No automatic commits, branches, PRs, task updates, docs/KB capture, or lesson reviews. No formal depth modes initially; respect the requested scope/time and provide depth where the design actually warrants it.

## Boundaries with neighboring skills

- [Design-options replacement](2026-11-11__replace-planning-with-design-options.md): choose among consequential solution mechanisms before commitment. This skill shapes a bounded code design within the selected direction. Neither is a prerequisite for the other.
- `yagni`: a requested minimalism lens. This skill asks whether structure reduces actual comprehension/change burden, not whether the diff is shortest. Never weaken correctness or build speculative features in the name of design.
- `repo-audit`: broad source-preserving repository risk/bloat investigation. This skill has a selected code target and may implement a requested local design change; no automatic repository sweep.
- Ordinary execution/debugging remains with the main agent and applicable project guidance. Do not replace every old `engineering` reference with an instruction to load `code-design`.
- [Verification proposal](../verification-design/2026-11-11__evaluate-agent-led-verification.md): still undecided. Code-design can require proportionate evidence for its own changes without taking over proactive verification/observability management or depending on a new skill.
- Learning may teach the resulting mechanism when requested/invited; Git and persistence keep their own authorization. No mandatory companion skill or special agent team.

## Research basis and limits — consulted 2026-11-11

| Source | Relevant evidence or reasoning | Consequence for this design |
| --- | --- | --- |
| [Ousterhout and Martin: APOSD vs Clean Code discussion](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md) (discussions 2024–2025; introductions, method-length and available comments sections read) | Both value readable/modular software and acknowledge possible over-decomposition; they disagree about decomposition and comments. Ousterhout frames complexity as knowledge required to understand/modify a system and its accessibility. | Ground the skill in reader/change burden and concrete tradeoffs, not tiny-function or no-comment dogma. This is expert debate, not empirical proof that one style always wins. |
| [Google: What to look for in code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Overall design, integration, excessive complexity, speculative generality, useful tests, and context matter; style preferences should not block changes. | Inspect the selected change's design in context. Borrow judgment criteria, not a mandatory Google-scale review workflow or universal test policy. |
| [Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) (2015) | Speculative capabilities incur carry/delay/repair costs; YAGNI does not prohibit making code easier to modify. | Distinguish maintainability work from speculative feature frameworks. Walk through later changes without building them now. |
| [Matklad: ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) (2021) | An explicit map of coarse modules, boundaries, and invariants can help new contributors locate responsibilities. | Favor discoverable ownership. Do not create a new architecture document for every small edit; numerical productivity anecdotes are not measurements for this user. |
| [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) (2026-02-11) | An internal agent-built product used legible boundaries and mechanically enforced invariants; the article explicitly limits generalization to other environments. | Code should expose and protect relevant boundaries for agents and humans. Do not copy its exact layering, pervasive lint rules, autonomous reviews, merge policy, or background cleanup into a solo-builder skill. |
| [Evaluating AGENTS.md, v3](https://arxiv.org/html/2602.11988v3) (2026-09-29) | Added instructions increased exploration/testing/cost in Python issue-resolution benchmarks without significant success improvement over no context. Security and long-term design quality were not evaluated. | Test the specialist's incremental value and non-activation; do not equate a longer quality checklist with improved code. Not proof about this proposed skill. |

These are primary professional guidance, expert debate, one vendor case study, and a bounded empirical instruction study—not a controlled evaluation of this design. Search returned no results for several queries, so discovery relied on directly retrieved sources; two attempted Fowler refactoring URLs returned 404 and were not used. No current-market completeness, tested productivity gain, or universal clean-code doctrine is claimed.

## Future implementation and complete replacement

1. **Reconcile evidence and scope:** Inspect current Agent Core source, neighboring skills, manifest/catalogue, and direct references. Do not invoke the unavailable old engineering skill. Historical content is migration evidence, not an instruction to commit or run a suite.
2. **Author the narrow behavior:** Keep the activation boundary and substantive design lenses prominent. Use small examples only when they distinguish good judgment from a common failure. Do not transplant the old implementation loop or this whole task into the skill.
3. **Retire the old canonical owner:** If `skills/engineering/` remains when implementation is requested, archive it under a dated historical path and remove the active owner with recoverable history. If the human already removed it, do not resurrect it. Do not keep a broad-trigger alias.
4. **Reconcile direct references and discovery:** Update the catalogue/design guide and add the new manifest entry within the later authorized source scope. Inspect `skills/git-workflow/SKILL.md` and `skills/project-tasks/SKILL.md` for actual dependencies on the old skill; replace general execution references with ordinary authorized execution, not universal code-design activation. Preserve unrelated generic uses of "engineering". Update the verification task's obsolete ownership hypothesis/source pointer when migration is authorized; its proposed capability remains independently undecided. Coordinate shared-file edits with the sibling task and preserve current changes.
5. **Validate focused behavior:** Use the cases below, including normal-code and prose negative controls. When authorized, compare a baseline response and skill-assisted response on the same supplied code and request; examine concrete design consequences and unnecessary work, not verbosity or a self-awarded score. No automatic subagents. If only static/author review is feasible, report that limit rather than claiming demonstrated runtime benefit.
6. **Separate source from adoption:** Normal publication requires the confirmed committed clean-source workflow and explicit selected harness. Removed manifest entries do not uninstall managed copies. Any installed old-skill retirement is a separate supported operation with scope/fingerprint checks; no ad hoc global deletion or manual managed-copy editing. Tripverge guidance/code changes require separate consumer authorization.

## Acceptance scenarios for later validation

| Situation | Expected behavior |
| --- | --- |
| "Design the shared trip-edit module used by HTTP and assistant clients" | Activate; assign domain-rule/state ownership and a useful interface within approved architecture. Avoid framework abstractions unrelated to the two actual callers. |
| "Refactor this subsystem so approval rules have one owner" with code-edit authorization | Trace actual duplication, consolidate the same rule coherently, preserve behavior, and run relevant checks. No unrelated cleanup or default commit. |
| "Review this diff's maintainability" where a predicate hides a mutation | Identify the hidden caller obligation with code evidence; recommend an honest interface/structure rather than just a longer name. |
| Long but cohesive function with local state and a clear contract | No automatic split by line count; retain it if extra interfaces would increase reader burden. |
| Two similar snippets represent different domain policies | Do not force a shared abstraction without shared semantics/change pressure. |
| "Implement this ordinary endpoint" / "fix this typo" / "rename this variable" | No activation based on generic code-edit wording. |
| "Rewrite the learning skill" / "save two tasks" | No code-design activation, code-style checklist, or runtime tests for Markdown prose. |
| Requested structural review finds no material concern | Return a grounded no-change conclusion; do not manufacture findings or demand tests. |
| Read-only review reveals an authorization defect | Report the material finding and scope; do not silently edit code or launch a security audit. |
| A refactor changes transaction or error behavior unexpectedly | Treat it as a real regression/contract change, not a permissible aesthetic improvement. Restore or resolve within the user's scope before claiming completion. |

For a representative code case, useful evidence includes a before/after responsibility trace, a concrete change scenario with fewer unrelated obligations, and behavior checks appropriate to actual edits. These are demonstrations of a specific result, not proof of universal maintainability or future throughput.

## Resume context and completion boundary

- Working repository: `C:\Users\tanch\.agent-core`.
- Read first: [AGENTS.md](../../../AGENTS.md), [Skill Design Guide](../../../docs/skill-design-guide.md), [Skills Catalogue](../../../docs/skills-catalog.md), and current `personal-skills.toml`. Catalogue availability claims about old skills are currently stale relative to the manifest/session.
- Read selectively for overlap: `skills/yagni/SKILL.md`, `skills/repo-audit/SKILL.md`, and the linked verification task. These are comparison sources; inspecting them does not activate their workflows.
- Before authorized publication: [Operating Manual](../../../docs/agent-core-operating-manual.md).
- Related selected vision: [design-options](2026-11-11__replace-planning-with-design-options.md). Independent implementation is possible; coordinate shared reference/manifest edits.
- Tripverge examples are illustrative. Before real consumer work read `C:\Users\tanch\Documents\Github\tripverge\AGENTS.md` and current product/architecture/MVP docs and implementation. No consumer changes are approved here.

This pass saves the selected vision/research only. No skill, retirement, behavioural trial, code refactor, installation, or production change occurred. The task remains Active for future requested implementation. Resume with: **"Implement the code-design replacement task in Agent Core."**
