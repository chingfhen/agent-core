# Task: Refine workflow discovery and handoff continuity

**Created:** 2026-11-08
**Last Updated:** 2026-11-08
**Priority:** Now
**Status:** Blocked — awaiting independent human review

**Goal:** Improve discovery without loaded maintenance skills, current-state consistency after handoffs, and support for non-coding work while preserving the existing workflow.
**Deliverables:** Focused canonical skill/routing changes, aligned workspace documentation, comparative acceptance scenarios, and a committed review branch pushed to origin.
**Success Bar:** Static checks pass; changes preserve human-controlled persistence timing and existing permission boundaries; the human can independently compare main with the candidate. Fresh-session behavioral improvement is not established by static checks.
**Current State:** Candidate implemented, structurally checked, committed, and published on `refine/workflow-continuity`, based on `main` at `bce5d5b3de107346a49c2c8b800866b7f5888899`. Implementation commit `d1338041da109bba4491c39ecb9752adb0561cfc` was verified on origin. This checkpoint records delivery; independent comparative acceptance remains pending.
**Next Action:** Human compares main with the review branch and supplies the independent rating/findings. A future agent may inspect and discuss the candidate; await direction before revisions, merge, or harness installation. Do not repeat implementation or treat publication as acceptance.
**Blockers:** Human-owned comparative review is pending; clear through the user's review result and direction.

## Approved direction and boundaries

- Keep separate tasks, docs, KB, and lessons skills, stable paths, and current semantic/date organization.
- Put reader discovery behavior in managed guidance and useful navigation, so retrieving context does not require maintenance-skill loading.
- Reconcile current task instructions throughout the affected file and index during authorized checkpoints; retain useful historical evidence without leaving obsolete executable-looking instructions.
- Make core contracts suitable for research, organizational processes, career work, and engineering; require code/repository/runtime evidence only when relevant.
- Preserve human control over docs/KB/lessons maintenance timing. Existing authorized task bookkeeping remains available; no new background maintenance.
- Edit canonical sources in Agent Core only. Do not migrate consumer workspaces, copy employer material, install the candidate into harnesses, merge main, or modify unrelated tasks.
- Branch publication means a Git push for review, not skill installation. The user will perform the independent relative comparison.

## Delivered candidate and verification

- Reader-side routing now covers imperfect references, index misses, and task-state reconciliation without loading maintenance skills. Task/KB indexes retain useful established search terms. Agent Core's own task-routing block preserves its opt-in write gate.
- Task checkpoints reconcile obsolete plans, checklists, and re-entry commands throughout the affected file. Useful evidence, rationale, and remaining obligations stay intact.
- Core tasks/docs contracts support non-coding work with claim-appropriate authorities. Docs maintenance honors the human's requested timing; coordinated handoff remains a single user-facing request.
- PowerShell structural checks passed across 27 Markdown files: 79 local links/anchors, five owner-section templates, 18 manifest-declared skill identities, and canonical invocation metadata. Python tests were not run; no Python environment was configured for this workload. These checks do not establish model behavior.
- `git diff --check` passed; the scoped diff was inspected for ownership, permission changes, and contradictions. No runtime code or publication manifest changed.
- Synthetic comparison scenarios 18e–18i were added to the existing acceptance document. Actual fresh-session trials and comparative ratings remain pending and human-owned.
- `git ls-remote` confirmed origin's review branch matched implementation commit `d1338041da109bba4491c39ecb9752adb0561cfc` after push. Main was not merged or modified; active harness skills were not installed from this branch.

## Independent review entry points

- [Compare main with the candidate](https://github.com/chingfhen/agent-core/compare/main...refine/workflow-continuity).
- [Implementation commit](https://github.com/chingfhen/agent-core/commit/d1338041da109bba4491c39ecb9752adb0561cfc) — fixed candidate implementation for repeatable comparison with the recorded base.
- Reader trials must use the candidate's routing cues; merely installing the skill does not change existing consumer AGENTS.md. Use synthetic workspaces rather than migrating real ones to conduct the comparison.

## Resume context

- [Workspace contract](../../../docs/workspace-configuration.md) — routing, claim ownership, and coordinated handoff.
- [Project Tasks](../../../skills/project-tasks/SKILL.md) and its routing/handoff references — primary continuation changes.
- [Project Docs](../../../skills/project-docs/SKILL.md), [KB](../../../skills/knowledge-base/SKILL.md), [Agent Lessons](../../../skills/agent-lessons/SKILL.md) — independent owners and maintenance boundaries.
- [Acceptance scenarios](../../../tests/workspace-workflow-scenarios.md) — synthetic checks; not evidence of live trials.
- [Earlier autonomy task](../project-tasks-autonomy/2026-11-02__autonomous-task-lifecycle.md) — related historical discussion, not authority to introduce standing autonomous writes here.
