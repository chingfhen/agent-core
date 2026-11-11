# Task: Make selected skill names clear to humans

**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Now
**Status:** Blocked — review-ready validation incomplete

**Goal:** Apply the human-approved names consistently to canonical skills and direct consumers, while preserving cross-harness sync and ownership behavior.
**Why:** Names should help a person understand when to use a skill without first learning agent-specific terminology.
**Current State:** Managed branch `20261111-clarify-skill-names` is published as [draft PR #6](https://github.com/chingfhen/agent-core/pull/6), targeting `main`. Approved source directories have been renamed, Python sync's replacement selector updated, and a source-name mapping added to the skill guide; cross-reference reconciliation and behavioral validation remain incomplete. The human approved and the agent merged newer `main` (`e34939f`) into this branch; this did not merge the branch into `main`. GitHub CLI is installed and authenticated. An initial push was rejected; a command-scoped authenticated GitHub CLI credential helper succeeded without changing global Git configuration. The existing in-repository `.agent-envs/verification` environment's Python 3.10.18 interpreter was verified; its recipe is excluded locally and not backed up in Git. The full suite ran 131 tests with one failure and one skip: a broken link in the separate historical `tasks/2026-10/2026-10-29__skill-owned-agents-sections.md`. The human requested docs mapping instead of approving that task edit. A subsequent focused run passed 12 Python retirement tests, including a new check that the immediate predecessor is preserved by default.
**Next Action:** Finish the reference and behavior audit, resolve the historical-link failure without exceeding task-write permissions, and rerun relevant validation. Update PR #6 for review; do not merge without separate approval. Close only after the requested work and verification are complete.
**Blockers:** The old link in an unrelated historical task remains broken and causes the workspace contract check to fail. Do not change that task without explicit authorization. Review delivery and full verification remain outstanding.

**Reconciliation update:** On the human's request to reconcile and merge, `origin/main` at `2cc72f3` was merged into the review branch; conflicts were resolved by preserving its newer Git/worktree lifecycle behavior under the renamed skill. The workspace contract check was rerun after resolution and still failed on the unchanged historical task link. The PR remains a draft until the failure and remaining verification are resolved; integration into `main` has not occurred.

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
