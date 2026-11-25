# Task: Agent Builder — Scripts and Python

**File:** `tasks/2026-11/agent-builder/2026-11-25__scripts-and-python.md`
**Created:** 2026-11-25
**Last Updated:** 2026-11-25
**Priority:** Now
**Status:** Closed
**Closure:** Completed (scoped source delivery, not runtime adoption).

**Goal:** Preserve reusable agent-owned scripts and independent purpose-specific uv environments, including actual Python execution.
**Deliverables:** Approved module design, scripts.md, python.md, selective CLI craftsmanship reference, root/foundation integration, verification and continuation handoff.
**Success Bar:** Cohesive source contract preserves or explicitly changes prior behavior, with actionable permissions, verification and acceptance conditions.
**Chosen Direction:** Human approved retrospective script stewardship, language-agnostic utility selection, actual-platform optimization, lightweight maintenance and autonomous compatible Python maintenance without autonomous purpose deletion; direct interpreter execution for known compatible environments. Explicit implementation cue received 2026-11-25.
**Current State:** Scoped source delivered on main through [cfb27a3](https://github.com/chingfhen/agent-core/commit/cfb27a3419a812bd3febb7ebeaffcf34ebf434ce). Five intended source/design files changed; legacy workflows remain live.
**Next Action:** None for this closed task. On human cue resume Task 06 for routing/setup/continuity design only. Task 08 owns full integration, behavioral validation and separately authorized adoption.
**Blockers:** None for scoped source completion; target-harness execution and regression validation remain downstream.

## Decisions and source-contract coverage

- Scripts: preserve project-scripts' deterministic admission, smallest useful intervention, explicit CLI contract, safe fixture tests, existing callers, single index, effect/runtime visibility and no-op. Centralize routing/initialization, permissions, marker maintenance and verification in root. New default scripts/index.md and domain folders; keep established legacy paths/index casing. Language/shell unrestricted (Python, Bash, PowerShell, CMD, SQL, etc.); portability is useful but not required; document actual platform requirements. Existing CLI craftsmanship retained as selective companion, not a mandatory utilization read.
- Script stewardship remains human-triggered; autonomous retrospective creation/repair/consolidation when justified within established scope, no periodic audit or speculative cleanup. Ordinary temporary scripts and existing-script reuse do not invoke maintenance; inspect actual source/interface/effects and verify output; no implied live effects/team changes or durable edits. Physical removal/relocation needs authority; known consumers protected.
- Python: preserve independent uv purpose projects, recipe/pin/lock, exact target and workload cwd, scoped overrides, independent workspace boundary, team/root explicit mode, concurrency, generated-state/secret exclusions, approved tool/package policy, runtime verification, failure recovery and real workload execution. Centralize resource routing in root; no separate registry. New purpose creation, compatible dependency changes, repair/restore/sync autonomously within established personal root when necessary for authorized work; choose a separate compatible purpose instead of breaking shared consumers. First root initialization, disruptive shared changes, team changes and deletion retain explicit gates; no automatic pruning.
- Intentional utilization change: ordinary compatible execution uses the absolute selected .venv interpreter (not activation, implicit uv run sync or transient PEP 723 environment). Verify recipe, pin, lock, installed compatibility, actual executable/prefix/version; scoped PATH/variables and appropriate cwd; reuse sufficient evidence within a workload. Potentially mutating commands, stale/missing/broken environment or uncertain compatibility require root + python.md before maintenance; no system/transient/team fallback. Read-only uv check commands only when installed-version behavior and valid target establish non-mutation. No custom launcher.
- Default AGENTS.md fragments carry actionable discovery/use and before-action gates; root points to them. Setup/template integration Task 06, loading/recovery Task 07, actual harness and caller validation Task 08.
- Design basis preserved in modules: original CLI craft sources (CLI Guidelines, argparse, shell guide), Python venv, uv sync/CLI/workspace/configuration/inspection and PEP 723. No repeated routine research.

## Verification and limits

- Created [scripts.md](../../../skills/agent-builder/references/scripts.md), [python.md](../../../skills/agent-builder/references/python.md), [cli-craft.md](../../../skills/agent-builder/references/cli-craft.md); updated [root](../../../skills/agent-builder/SKILL.md) and [approved foundation](../../../docs/agent-builder-design.md). Exact readback of every saved source/design write; compare 52ea870..cfb27a3 showed only these five files, no legacy, manifest or AGENTS.md changes. Static source review and targeted checks of module links, activation, script timing/admission/craft, Python targeting, independence, pins/locks/exclusions, concurrency, team mode, actual execution and no-fallback contract. Scope of verification is Markdown source and guidance, not behavior.
- Task 08 must exercise ordinary reuse without loading maintenance, stale/missing environment and dependency mutation routing, valid/invalid target, installed uv version non-mutating checks, no team mutations, concurrent usage, exact execution, script discovery/reuse vs human-triggered maintenance, dependency callers (notably learning-notebook, workspace-setup and existing manifests/sync retirement), fresh-session activation, recovery and integration. No runtime tests, actual environment or personal script creation, publication/install, migration, retirement or workers in Task 05.
- Canonical docs own approved project decisions; no separate KB entry, lesson or script needed for this scoped implementation. No additional persistence overhead.

## Resume context

- [Approved foundation](../../../docs/agent-builder-design.md) — intended architecture and acceptance.
- [Skill design guide](../../../docs/skill-design-guide.md) — research, selective loading and observability.
- [Workspace configuration](../../../docs/workspace-configuration.md) — live contract pending adoption.
- [Task 06 — Routing, setup and continuity](./2026-11-25__routing-and-continuity.md) — next human-started design discussion, no implementation until explicitly approved.
- [Task 08 — Integration and migration](./2026-11-25__integration-and-migration.md) — validation and separately authorized transition.

## Delegation decision

Main-agent execution — tightly coupled scope, root and source changes; no workers authorized or launched.
