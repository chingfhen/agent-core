# Task: Make selected skill names clear to humans

**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Now
**Status:** Closed — Completed with accepted validation limitation

**Goal:** Apply the human-approved names consistently to canonical skills and direct consumers, while preserving cross-harness sync and ownership behavior.
**Why:** Names should help a person understand when to use a skill without first learning agent-specific terminology.
**Current State:** Approved source names and documentation were merged into `main` via [PR #6](https://github.com/chingfhen/agent-core/pull/6). The newer Git-workflow changes were preserved. The human accepted the broken historical-task link and requested merge. The existing in-repository `.agent-envs/verification` environment's Python 3.10.18 interpreter was verified; its recipe is excluded locally and not backed up in Git. The reconciled suite had one accepted failure and one skip; focused Python retirement tests passed. Harness installation and old-copy retirement were not performed.
**Next Action:** None for this task. Harness publication and installed-copy retirement remain separately authorized operations.
**Blockers:** None for the human-accepted source delivery. The old link in an unrelated historical task remains broken; do not change that task without explicit authorization.

**Outcome:** PR #6 was merged into `main` as `c0c368b623cb120fcc94423ee06f166b5a6dc9cd` after preserving the newer Git/worktree lifecycle behavior. The human accepted the unchanged historical-link failure for this source delivery. On the reconciled head the suite ran 132 tests with one failure (that historical link) and one skip. Source names are not proof of harness installation, and removed manifest names do not uninstall old copies.

## Approved scope

The human explicitly requested the `git-workflow` managed branch, approved production skill renames, direct references, docs sync, and task closeout. Normal branch push/PR review is authorized; merge remains separately gated. Standard guarded post-merge branch cleanup applies unless the human opts out. Do not publish to a harness or remove installed copies without separate scope.

| Existing name | Approved replacement |
| --- | --- |
| design-options | tech-design-options |
| agent-lessons | improve-agent-workflows |
| human-unblock | resolve-human-blockers |
| mermaid-markdown | create-markdown-diagrams |
| project-tasks | manage-project-tasks |
| project-docs | maintain-project-docs |
| knowledge-base | maintain-knowledge-base |
| git-workflow | git-branch-to-review |
| readability | improve-readability |
| approval-gate | review-before-approval |
| manage-python-env | run-and-manage-python |
| commit-with-subagent | commit-changes |

For the last mapping the human clarified: retain a general commit skill, without making subagent delegation its defining behavior. Keep `yagni`; do not rename other suggestions that were not approved.

## Required migration and checks

- Inspect current skill files, manifests, direct references, routing templates, project guidance, tests, and executable sync behavior. Update skill identities, paths and relevant invocation cues without changing domain paths, stable marker names, historical records, or unrelated wording blindly.
- `agent_core/sync.py` has a Python-skill replacement constant and legacy retirement rules keyed to the current name; preserve safe, selected-harness migration behavior. Removal of manifest entries is normally non-destructive, so old installed skills can remain and duplicate discovery; do not claim installation or cleanup. Review any proposed installed-resource retirement against `AGENTS.md` and obtain distinct scope if needed.
- Preserve skill ownership boundaries and user content in managed guidance; changing a skill name must not inadvertently rename user directories or marker protocols. Update behavioral scenarios and executable tests where their contract actually changes. Use `manage-python-env` before any Python execution.
- Verify manifest entries and matching frontmatter, relevant links and cross-skill references, sync compatibility and focused tests. Report live behavior and adoption separately from static checks. Commit scoped changes and publish a linked PR only after checking effects and host permissions.
- User requested docs sync and task closeout. Before closure apply the coordinated closeout review, respecting project-local write gates; leave the task active if meaningful implementation, verification or review delivery remains.
