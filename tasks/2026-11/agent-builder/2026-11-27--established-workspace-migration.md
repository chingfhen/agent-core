# Task: Agent Builder — Established workspace migration

**File:** `tasks/2026-11/agent-builder/2026-11-27--established-workspace-migration.md`
**Created:** 2026-11-27
**Last Updated:** 2026-11-27
**Status:** Closed — Completed (canonical source scope; workspace adoption separate)

## Outcome and authorization
An existing agent can adopt Agent Builder incrementally, return to productive work without a perfect structural conversion, and retain useful context and safety constraints. Human approves a concise, bounded migration proposal; the agent handles routine decisions within it. The human explicitly requested this audit task and direct source implementation on 2026-11-27. Scope is canonical source/docs only, not installation, employer workspace edits, external data transfer or Git persistence changes.

## Implemented plan (historical)
1. Add selectively loaded migration.md: inspect actual compatibility, propose the smallest useful scope, obtain approval, preserve independent owners and recoverability, perform approved repairs, verify affected functionality, defer optional work. Cover legacy block mapping, behaviors/lessons, stale cues, Python execution, legacy knowledge/inbox, and partial adoption.
2. Route migration in root, clarify coexistence of compatible legacy guidance with new managed guidance (no competing authority), update targeted module fragments and human-facing operating manual/workspace contract. Preserve existing module contracts and publication mechanics.
3. Source readback and targeted consistency checks completed; representative scenarios reviewed against the written contract, not executed in a harness. Close source-delivery task and remove its index entry.

## Success bar
Functional compatibility first, not structural conformity. Removed skill cues resolve; essential Python checks are available inline; existing resources, human rules and independent owners remain intact; approval and reporting are lightweight; interruption/deferred work does not force full migration. Report blockers only for affected capabilities. No registry, migration tooling, mandatory full conversion, revived synthesis/inbox queue, or speculative redesign. Source verification is sufficient for this delivery; actual harness adoption remains a separate human-controlled trial.

## Evidence
Prior integration task and current root/module contracts; independent read-only review reported successful skill retirement but stale workspace cues, missing inline Python guidance and legacy KB/inbox semantic drift. Review is reported evidence, not an independently reproduced runtime trial. No employer-specific source or identifiers retained here.

## Delivered and verified
- [Migration reference](../../../skills/agent-builder/references/migration.md): approved incremental scope, legacy mapping, optional content extraction, safe snapshots, limited stale-cue inspection, changed contracts, partial-failure handling, proportionate verification and separate rollback.
- [Root](../../../skills/agent-builder/SKILL.md): explicit migration routing, compatible retained legacy sections, one authority per rule/destination, safe pre-migration Python checks.
- [KB](../../../skills/agent-builder/references/knowledge-base.md) and [Python](../../../skills/agent-builder/references/python.md) references: legacy page staleness, inbox producer semantics, direct-interpreter guidance.
- [Manual](../../../docs/agent-core-operating-manual.md), [workspace contract](../../../docs/workspace-configuration.md) and [approved design](../../../docs/agent-builder-design.md): align human adoption with the revised contract.

Remote readback at 66265061280e5281c44342aa1645f2d8b6f7ac0b verified all seven changed source/docs paths exist, migration routing and approval gates, minimal repair, partial adoption with noncompeting authority, Python fallback checks and direct interpreter, KB staleness and inbox semantics, independent owner retention, recovery and stop conditions. Static scenario walkthrough: (1) stale Python cue with no inline contract → load root + Python reference for required safety checks, offer approved minimal repair, leave other sections untouched; (2) approved selected consolidation → replace only selected authoritative routes, preserve independent owners and verified supporting details; (3) deferred KB/lessons work or interrupted write → retain working authority, report affected gap, resume only approved scope. These are source-level judgments, not actual agent or harness trials. No Python/runtime tests, installation, workspace edits or external worker execution performed. No manifest or distribution changes required.

Next human action, when useful: sync selected harness, restart, ask Agent Builder to assess migration and recommend only useful changes; approve desired scope. No outstanding mandatory structural migration or new task. 
