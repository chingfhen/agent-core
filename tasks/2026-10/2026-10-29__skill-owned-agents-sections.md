# Task: Lean Skill-Owned Routing and Reliable Task Handoffs

**File:** `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`
**Created:** 2026-10-29
**Last Updated:** 2026-10-30
**Priority:** Next
**Status:** Closed
**Closure:** Completed canonical implementation and documentation, with structural
verification. Fresh-session harness acceptance remains unverified and separate
from this source delivery, as recorded below.

**Goal:** Make workflow skills easy to activate and independently usable, with
reliable task handoffs that preserve the context needed by a fresh session.
**Deliverables:** Canonical skill/routing changes, coordinated handoff/closeout
workflow, revised docs and acceptance scenarios, structural checks, and task closure.
**Success Bar:** Lean owned guidance, selective verified context pointers, clear
deliverables/next actions, preserved ownership and permissions, and honest checks.
**Current State:** Approved canonical skills, docs, and scenarios delivered;
four structural tests passed and the scoped changes were reviewed. Closed at the
human's request; removed from the live index. No publication or workspace adoption.
**Next Action:** None within this task. Separately authorize publication/adoption
and run fresh-session scenarios before claiming target-harness compliance.
**Blockers:** None for this source delivery; adoption checks have not been performed.

## Approved Direction

The 2026-10-30 fresh-session review supersedes earlier choices where noted:

- Keep lean, independently owned AGENTS.md sections and optional workspace-setup.
  Preserve custom wording/positions, legacy path bases, local write gates, and
  compatible first-use adoption; absent resources need initialization approval.
- Keep INDEX.md outside AGENTS.md. New task paths add one semantic workstream
  beneath the creation month. Existing task paths, including this one, stay stable.
- Enable model invocation for all canonical skills, including dormant sources;
  natural-language requests still control request-only effects.
- Project docs and KB remain standalone. Tasks coordinate their use and lessons
  review on explicit fresh-session handoff or closeout, without recursive calls.
- Tasks carry supervisable goals/deliverables/acceptance and a context map with
  exact locators, source role, and when-to-read cues. Routine task updates stay lean.
- Lessons keep essential pre-action guards and conditional pointers. Detail uses
  docs/KB through their owning workflows. **The new agent-lessons.md companion
  proposal is withdrawn**; existing useful material needs approved migration.
- Preserve substantive KB archival and Python execution contracts. Load Python
  skill before interpreter/import probes; verify the actual selected interpreter.

Durable contract and rationale live in the workspace doc below, rather than a
second full design in this execution record.

## Resume Context

- Before changing workflow behavior:
  [Workspace contract](../../docs/workspace-configuration.md)
  — canonical ownership, first use, task handoff, and lessons rules.
- For coordination implementation:
  [Handoff workflow](../../skills/project-tasks/references/handoff.md)
  — persistence order, owner evaluations, partial failure, and closeout.
- Before skill design changes:
  [Skill design guide](../../docs/skill-design-guide.md)
  — core purpose, callable/request-only distinction, and dependency direction.
- For verification:
  [Workspace scenarios](../../tests/workspace-workflow-scenarios.md) and
  [KB scenarios](../../tests/knowledge-base-scenarios.md)
  — behavioral acceptance criteria; these are not completed harness trials.
- Repository: this canonical Agent Core checkout. Production sources are `skills/`;
  installed copies and external/employer workspaces are separate surfaces.

## Permission and Delivery Boundary

The human approved all reviewed changes and explicitly requested implementation,
docs/task sync, and closure. Canonical skills, directly affected tests/docs/guidance,
this task and its index entry are authorized. The human separately selected reuse
of `.agent-envs/verification` for this operation only; no saved Python-root change.

No commits, pushes, publication/sync, subagent deployment, installed-copy edits,
or external workspace migration are included. A handoff cue does not independently
authorize any of those operations. Agent Core task writes remain explicitly opt-in.

## Delivery Record

- Four resource skills have local routing references with independent first use,
  lean section shapes, path-base compatibility, ownership and readback safeguards.
- project-tasks adds workstream folders, deliverables, required/conditional context,
  natural-language continuation, and a separately loaded closeout/handoff procedure.
- agent-lessons routes detail through docs/KB and preserves existing material when
  supporting storage is unavailable; no new companion is proposed or created.
- workspace-setup coordinates owner sections, preserves custom legacy guidance,
  supports approved migration, and proposes one optional external startup cue.
- Model-invocation suppression is removed; commit-with-subagent's explicit Devin
  triggers include model as well as user. Publication allowlists are unchanged.
- Docs, README, steward guidance, catalogue, and skill-design criteria describe
  delivered source behavior. Acceptance scenarios cover invocation, handoff/resume,
  preservation, partial failures, first use, probes, and lessons routing.

## Verification and Closeout

- Verification environment recipe inspected: independent uv project, no external
  dependencies, Python 3.10.18 pin. Human approved operation-only reuse.
- Path attributes show no reparse redirection; no running Python/uv process
  references this purpose project. Generated environment files are untracked and
  excluded by existing Git-local rules. uv 0.7.13 is available.
- Interpreter verified before checks:
  `C:/Users/tanch/.agent-core/.agent-envs/verification/.venv/Scripts/python.exe`,
  prefix `C:/Users/tanch/.agent-core/.agent-envs/verification/.venv`, Python 3.10.18.
  Recipe/lock path: `.agent-envs/verification/{pyproject.toml,uv.lock}`; no dependency
  or saved-root changes were needed. Code cwd remained this checkout.
- `uv run --project <absolute verification path> --locked python -m unittest
  discover -s tests -p test_workspace_contracts.py -v`: **4 passed**. Checks cover
  model-callable metadata (including Devin triggers), manifest/name consistency,
  balanced owner template markers, and real Markdown references/heading anchors.
- Scoped diff and scenario expectations reviewed against the written contracts;
  `git diff --check` passed. No automated preservation/behavior trial is implied.
- Fresh-session Pi/Devin/OpenCode trials have not run. Canonical-source checks
  cannot prove installed skill exposure, before-action compliance, or preservation
  by an independently executing model. Publication/adoption remain separate.
- This session's exposed Python skill differs from canonical source; no installed
  copy was changed. The stricter canonical purpose-project procedure governs these
  checks. Other workflow sources were read directly in this authorized steward
  checkout; that does not establish their harness registration.
- Docs receive the settled contract. KB evaluation selected no distinct additional
  capture beyond that canonical project understanding; no KB destination was selected
  or written, and no KB capture is claimed. Lessons review uses the owning workflow
  fixes already made; no additional standing lesson or companion is warranted.

## Related Work

[Durable Learning Mechanism for Operational Constraints](../2026-10-23__durable-agent-constraint-learning-bookmark.md)
remains separate. This task adds no shared propagation/enforcement system and
does not close that investigation.
