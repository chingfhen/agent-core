# Optional repository routing

Read only for requested Git Workflow setup/refresh. This skill owns the
GIT WORKFLOW marker pair in an explicitly confirmed repository's AGENTS.md.
Setup is separate from branch approval, skill publication, and ordinary use.

1. Confirm repository, exact guidance file, applicable nested guidance, naming and
   target conventions, and existing team delivery policy. Reuse policy by pointer.
2. Propose the small section and obtain setup approval. An approved exact edit
   satisfies this gate. Resolve conflicts with existing instructions before writing.
3. Reread the file. Refuse duplicate, incomplete, nested or ambiguous markers and
   unsafe symlink/junction paths. Preserve outside text, section position, custom
   wording, stricter rules, and other owners' sections; managed does not mean replace.
4. Update only confirmed defaults/pointers and missing necessary activation cues.
   New relative links resolve from this AGENTS.md directory, not cwd. Do not invent
   policy files or silently migrate legacy guidance. Equivalent wording is a no-op.
5. Read back the scoped diff, marker pair, and referenced paths. Report exact saved
   path and any partial failure. Saved guidance is not proof of harness loading.

Example only; substitute confirmed conventions and an existing policy locator,
or omit the policy line if none exists:

```markdown
<!-- BEGIN GIT WORKFLOW -->
## Git Workflow

Branch convention: YYYYMMDD-<descriptive-slug> (adapt to required prefixes/tickets).
Default review target: main.
Policy: [Delivery policy](docs/delivery.md) — consult before publishing or merging.

Start new managed work only on an explicit request to use git-branch-to-review; continue
known managed work through its branch, PR/MR or project task. A date or legacy
-cf is a discovery cue, not authority; verify the saved approval and live Git
state. Generic engineering does not start this workflow. Integration into the
target needs separate explicit human instruction; routine target-to-branch
maintenance is agent-owned. New worktrees require explicit approval and task-backed
lifecycle ownership through safe cleanup. Use manage-project-tasks for authorized continuity, and
follow repository task-write and branch-cleanup policy.
<!-- END GIT WORKFLOW -->
```

Keep live branches, SHAs, PR lists, approval records, check dashboards, and detailed
Git commands out of this section. Task routing remains owned by manage-project-tasks;
actual branch/request state belongs to Git/the host. This section grants no blanket
write permission on external branches. Managed PRs require a task unless the human
explicitly opts out; honor narrower repository task-write gates.
