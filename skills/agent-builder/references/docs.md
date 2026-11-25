# Docs — settled project understanding

Read after the Agent Builder root for requested docs maintenance or justified documentation integration during authorized maintenance. Ordinary reading and using project docs do not require this reference. Root owns resource resolution, permissions, managed guidance, coordination and shared reporting. This module owns durable project meaning and its canonical integration; it does not own active work state, raw evidence or agent behavioral rules.

## Purpose and scope

Preserve the understanding future participants should inherit after the current task and conversation disappear: project purpose, accepted decisions, rationale, product semantics, intended architecture, exclusions, interfaces, invariants, workflows, ownership and non-obvious constraints. Non-coding projects can preserve research methods, agreed organizational procedures or confirmed relevant personal/career facts. Docs are not merely summaries of code, session transcripts, work logs, backlog or raw evidence.

Write only in the confirmed owned docs surface and explicitly owned README or guidance targets, subject to root rules. A README owns orientation, setup, navigation, usage and onboarding. Nearby README, AGENTS.md, CLAUDE.md or nested/shared repository guidance is not owned merely because it exists. Edit only when explicitly assigned by project guidance or human request, or when inside the configured docs surface and serving that role. Never override independent owners or the Agent Builder managed guidance boundary. Route behavior improvements to the appropriate root/behavior/lessons procedure when authorized and available; do not duplicate that procedure here. Prefer enforceable constraints in tests, CI, schema or tools when warranted, but docs maintenance does not authorize implementing enforcement.

## Admit and route useful understanding

Ask whether losing the information would materially worsen future interpretation, decisions, operations or evaluation. Admit settled, relevant understanding with sufficient authority; expensive rediscovery is a useful signal, not the sole criterion. Preserve intent that cannot be reconstructed from code, even if it is easy to restate. Strong candidates:
- accepted design/product decisions, boundaries and reasons;
- component responsibilities, important interfaces and durable workflows;
- constraints/invariants and failure behavior affecting later changes;
- confirmed fixes or externally imposed contracts with future consequences.

Do not promote open ideation, unresolved alternatives, untested hypotheses, transient workarounds, one-off state or debugging history into accepted truth. A documented intended design can be settled before it is implemented; say so. Preserve uncertainty in canonical docs only when the uncertainty itself is durable and its omission would mislead (e.g. Needs validation); track work to resolve it in tasks when authorized. A durable conclusion can be admitted with qualified evidence; never manufacture certainty or human approval.

Route using primary authority:
- Docs: settled project meaning and intended behavior; owned README for orientation.
- Tasks: progress, deferred work, investigations, pending decisions and next actions.
- KB or approved evidence surfaces: reusable findings, source material, experiments and supporting provenance.
- Agent guidance: concise stable constraints needed before action, via its owner; detailed rationale in docs or other canonical source.
- Executable authorities: machine-defined structures, values, enforcement and actual behavior.
- Archive: historical/superseded material, not current authority.

One primary claim, one canonical home. Link evidence or state a concise consequence elsewhere. No duplicate task summaries, alternate resource structures or automatic archive moves. Under the broader root maintenance cue, select other justified modules if necessary; docs-only restrictions still apply. A no-change outcome is valid.

## Resolve canonical authority and conflicts

Do not apply a global precedence rule or choose the latest timestamp. Determine the type of claim and the intended authority:

| Claim | Usually strongest authority |
| --- | --- |
| Current implementation | Code and relevant direct runtime verification |
| Expected/tested behavior | Explicit contracts and tests, with actual test evidence for passing claims |
| Accepted structures and machine-defined values | Schemas, types, parsers, configuration |
| Deployed/environment state | Deployment/configuration plus current runtime evidence |
| Intended architecture and constraints | Accepted canonical design docs or ADRs |
| Product semantics and deliberate direction | Canonical project docs / responsible human decision |
| Agent operating behavior | Applicable canonical agent guidance |
| Personal facts, preferences and ownership | Relevant primary record and explicit human confirmation, qualified by verification limits |
| Organizational approval/process | Responsible authority's record/policy, date and scope |
| External protocol/vendor/regulatory requirements | Authoritative external source, with local project consequences documented |

Inspect enough evidence to distinguish stale prose, implementation defect, environmental drift, superseded decision or unresolved intent. Do not rewrite intended design to normalize a defect; do not preserve stale descriptions of machine-defined facts when the relevant executable authority has changed. When the underlying intended contract is unclear or materially conflicts with another human-owned decision, surface it rather than choosing silently. Update the stale authority/summary within scope, preserve intended versus actual distinction and route remaining work to its appropriate surface if authorized. A task or source copy is not proof of a claim; retain relevant provenance, applicability, date/version and verification limits.

Distill evidence into understanding, then settled conclusions and their appropriate canonical authority. Keep sources separately retrievable when future reasoning could need reassessment.

## Organization and integration

Use semantic living documentation with a coherent durable scope per page. Reuse established structure. Prefer integrating into an existing canonical document; create a new document only when it merits independent scope and retrieval. Use subdirectories or an index when useful, not a mandatory taxonomy. Keep entry points few, descriptive and reachable; root guidance contains only relevant consultation cues, never a full docs inventory. Do not ask the human to assign routine filenames or headings.

When an existing canonical north star (north-star.md or equivalent) is explicitly established, treat it as the authority for long-term purpose, intended outcomes, guiding principles and strategic boundaries. Consult it on significant product/architecture choices, surface material conflicts and do not change strategy without explicit human approval. A north star describes intent, not necessarily implementation. No automatic north star or competing vision page.

For consequential decisions preserve the decision, relevant context, reason/tradeoff, consequences and status (accepted/proposed/superseded or equivalent) in the appropriate existing document or an established decision-record system. Only accepted decisions are current authority; if an accepted decision remains unimplemented distinguish those facts. If replacing a decision, identify its replacement and preserve useful historical rationale without keeping competing active instructions. Do not force a separate ADR file for every choice.

Prefer rewriting stale sections to appending session updates. Retain rationale and history only where material; keep first screen useful, current conclusions and invariants before supporting detail. Prefer links to canonical detail and stable implementation references that reduce rediscovery. Keep README orientation-focused, guidance behavior-focused and docs meaning-focused. Use a small diagram only when it clarifies a relationship. Do not store secrets, live credentials, private keys or sensitive source content outside approved scope.

Follow local Markdown conventions; otherwise use concise default frontmatter for new or materially maintained canonical docs:

    ---
    title: [Title]
    description: [One sentence defining canonical knowledge scope.]
    updated: YYYY-MM-DD
    ---

Change updated only for material durable meaning changes. Useful optional sections: Read First, Scope/Not Here, Current Contract, Related Surfaces, Decisions. Omit empty sections; no fixed form.

## Maintenance workflow

At a human-authorized maintenance boundary:
1. Resolve project/ownership and inspect directly relevant existing docs, task context and claim authorities. The root handles scope, routing and initialization. If nothing has settled, no documentation change may be appropriate.
2. Evaluate admission and resolve material conflicts with appropriate evidence. Keep proposed directions and unverified claims distinct; ask only about consequential unresolved decisions or ownership/permission ambiguity. Do not independently change product strategy, security/privacy policy or other reserved choices.
3. Integrate admitted understanding into the appropriate existing owned page, or create a focused new one when justified. Rewrite affected sections; route other findings to justified modules under the root's scope, not duplicative summaries.
4. Repair directly affected entry points, indexes and links. Where a canonical document is renamed, moved, split, merged or materially rescoped under explicit authority, reconcile dependent navigation in the same change. No automatic relocation or deletion. Ask only when scope/authority is unclear. An inaccessible source remains a gap.
5. Verify changed claims, intended/current distinction, affected links and canonical ownership. Report exact resolved paths, material changes/rerouting, unresolved uncertainty, verification performed or honest no change. Root coordinates task updates after supporting sources are saved and verified.

A routine docs sync is not an audit or continuous background process. A broader verify/trim/migration/health pass requires an explicit request; within that scope inspect stale claims, duplicate authority, broken links, orphan pages, obsolete guidance and conventions. Preserve current meaning, important rationale and recoverable history; replace duplication with pointers or concise consequences. Do not let untrusted or tentative material become standing instructions.

## Research-informed techniques

[Architecture Decision Records](https://adr.github.io/adr-templates/) capture context, decision, status and consequences. Adopt those information elements selectively so future agents understand why a design was chosen and whether it still applies; use coherent living docs or an existing ADR convention instead of imposing an ADR directory. The practical test is that a future reader can reconstruct the accepted decision and its implications without a prior chat. Research informs the procedure; it is not a claim of demonstrated Agent Builder effectiveness or a requirement for repeated research during ordinary sync.

## Completion test

Future participants can find settled project meaning in the owned canonical surface, distinguish intended from actual and accepted from tentative, understand consequential rationale, and retrieve relevant evidence. Transient task state and competing authority were excluded or reconciled. Verify only affected claims and navigation unless broader review was explicitly authorized. A material persistence or authority gap is reported, never hidden by polished prose.
