# Task: Make selected skill names clear to humans

**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Now
**Status:** Active

**Goal:** Apply the human-approved names consistently to canonical skills and direct consumers, while preserving cross-harness sync and ownership behavior.
**Why:** Names should help a person understand when to use a skill without first learning agent-specific terminology.
**Current State:** Managed branch `20261111-clarify-skill-names` from `main` at `e8f776d7b1034a6c5994a4148f0f338062c72163`. Initial renames and further source/directory changes are underway; cross-references, sync checks and behavioral validation remain incomplete. GitHub CLI is installed and authenticated. An initial push was rejected without a clear reason; remote readback found no branch. The user selected the existing in-repository `.agent-envs/verification` environment; its Python 3.10.18 interpreter was verified. Its recipe is excluded locally and not backed up in Git. `main` advanced to `e34939f` with overlapping Git-workflow changes; the human approved merging it into this branch, not merging this branch into `main`.
**Next Action:** Implement and validate the approved mappings below, including migration-specific contracts; then push and open a linked review request if host access is available. Do not merge without separate approval. Close only after the requested work and verification are complete.
**Blockers:** Publishing the branch needs diagnosis of the rejected push. Local implementation and checks can continue.

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
