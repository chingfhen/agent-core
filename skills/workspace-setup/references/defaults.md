# Creation-time defaults

Agent Core maintains these defaults. They are seeds, not a policy to overwrite
human-edited workspace instructions. The personal baseline mirrors the manual
publication allowlist; maintain it when that allowlist changes. Runtime setup
must not depend on finding Agent Core's checkout or reading its manifest.
Availability comes only from the current session's exposed metadata.

## Initial personal skill rows

| Skill | Use for |
| --- | --- |
| workspace-setup | Establish or refresh this workspace map on request |
| manage-python-env | All Python execution, testing, evaluation, dependencies, and reusable environments |
| knowledge-base | Relevant prior context; requested KB capture and inbox processing |
| project-docs | Durable project documentation and owned guidance |
| agent-lessons | Explicitly learn from agent work and maintain durable AGENTS.md lessons |
| project-tasks | Continuation tasks |
| engineering | Code implementation, debugging, and review |
| planning | Substantial work requiring a plan |
| learning | Learning and explanations |
| human-unblock | Human-only blockers |
| readability | Readability improvements |
| reasoned-advocacy | Evaluating and defending recommendations |
| grilling | Stress-testing designs |
| approval-gate | Consequential approval checks |
| commit-with-subagent | Explicitly requested local commits through the commit agent |
| mermaid-markdown | Mermaid diagrams |
| yagni | Simplest adequate solutions |

Do not claim the old Python names are available substitutes. If exposed, list
`manage-python-agent-envs` or `manage-python-uv` as obsolete/conflicting extras
and flag the installation gap. Do not remove or modify installed copies here.

## Initial Behavior section

```markdown
### Behavior
- Load the relevant skill before acting; briefly name it and the selected resource.
- Use configured locations; ask when the project or destination is unclear.
- Consult the shared KB when prior work or organizational context matters.
- For Python, use manage-python-env to manage and execute through a compatible purpose environment under the configured Python root; reuse before creating.
- Report unavailable skills; do not search disk for substitute copies.
- Refresh this section on request, with approval; preserve existing custom instructions and all text outside it.
```

These concise reminders do not authorize capture, task edits, migration, Git
publication, or delegation beyond the owning workflow and human request.
