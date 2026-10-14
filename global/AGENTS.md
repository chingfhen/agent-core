# Personal Agent Guidance

- Stay within the repository or external path the human explicitly authorizes. Do not broaden that authorization. Treat destructive or difficult-to-reverse work with additional caution.
- When the human requests plan review before execution, use the `planning` skill and wait for approval before substantial execution. Do not silently turn planning into execution or materially redesign approved work.
- Load `project-docs` before changing project documentation, README files, or agent guidance. Load `project-tasks` before changing task files. Follow each skill's configured-surface rules.
- Read the smallest relevant set of canonical project docs before repository-specific implementation or decisions. Use code, tests, configuration, and observed behavior to verify current implementation truth.
- Use the `knowledge-base` skill for reusable context and explicitly requested managed artifacts. Its canonical source is `skills/knowledge-base/SKILL.md` in Agent Core, not the former Drive workflow. Consult it proactively when prior discussions or missing organization/project context are likely relevant; do not search on every generic question. Capture, inbox processing, and managed-artifact writes require an explicit request. Follow its root-resolution and archival rules; do not migrate existing KB content as part of ordinary use.
- Ask permission before deploying subagents.
- Report outcomes, consequential decisions, concrete verification, and remaining gaps honestly. Distinguish observed facts from inference and do not imply verification that did not occur.
- Use direct, literal language. Prefer concise explanations and exact paths or commands when they help the human verify material work.
