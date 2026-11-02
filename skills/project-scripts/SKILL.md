---
name: project-scripts
description: >
  On explicit request, review recent agent work or the current conversation for
  worthwhile personal deterministic scripts; create, improve, consolidate, or
  retire scripts in the configured Project Scripts Root. Use for "project scripts",
  "review scripts from this session", "automate what we did", or "make this
  repeatable as a personal CLI". This is script stewardship, not ordinary
  engineering execution, agent-lessons capture, or automatic project handoff.
disable-model-invocation: false
---

# Project Scripts

## Purpose and invocation

**Turn repeatable agent work into small, dependable software that both humans and agents can use.** Optimize for avoided future reasoning, tool calls, mistakes, and waiting **plus** human usefulness, not number of scripts written.

Invoke only when the human requests a script review, creation, improvement, or maintenance. A general request to implement a feature, run tests, capture lessons, or hand off a task does **not** invoke this skill. Do not add this skill to another workflow's automatic steps. A named script or review-only request narrows the scope; an unqualified `project-scripts` invocation reviews the substantive available conversation and relevant existing personal scripts. Do not invent inaccessible history.

An invocation permits proportionate script maintenance in the confirmed personal scripts collection, subject to applicable permissions. It does **not** authorize executing real-world effects of those scripts, modifying team/project source repositories, installing tools, changing unrelated guidance or skills, or publishing scripts elsewhere. Building or testing with safe fixtures is different from running against actual data or services. Honor narrower human or repository restrictions. A review-only request makes no edits.

This skill owns the **script lifecycle**, not the tasks it might automate. It can return **no changes** when deterministic software would not earn its maintenance cost.

## One personal location

Resolve a single authoritative **Project Scripts Root** for the current personal workspace:

1. Use an explicitly selected root for this operation, or the `Project Scripts Root` configured in applicable workspace `AGENTS.md`. Do not infer it from the shell's working directory or the source-code repository.
2. When not configured, propose `<workspace>/.work-context/project-scripts/` alongside the personal workspace (not inside a team repository), or another human-selected personal location. Obtain one approval before initializing or registering it. An inaccessible configured root is a blocker, not permission to create an alternative.
3. On approved first use, create only the needed collection and a minimal routing cue within this skill's own marked section in the applicable personal `AGENTS.md`, preserving unrelated guidance. A user-selected one-time root does not implicitly change saved configuration. Never edit another skill's owned section.
4. Keep personal scripts in this collection, even when they operate on different project repositories. A script accepting a project's path as an argument is not owned by that project's repository. The human decides later whether to copy/share a useful script with a team.

Use the following canonical marker for routing when registration is approved:

```md
<!-- BEGIN PROJECT SCRIPTS -->
## Project Scripts
Project Scripts Root: <confirmed location>
For personal script discovery, read <root>/INDEX.md; invoke `project-scripts` only on request to maintain scripts.
<!-- END PROJECT SCRIPTS -->
```

Resolve paths consistently with the declaring guidance: new relative paths are relative to that `AGENTS.md` directory, not process cwd. Preserve existing configurations; don't create competing script roots, global registries, auto-sync services, or a second package manager.

### Collection layout

```text
<root>/
  INDEX.md
  <project-or-domain>/
    <verb-noun>.py                    # or an appropriate .sh/.js/.ps1
    tests/                            # only when tests justify separate files
      test_<verb_noun>.py
```

- Use shallow, stable, descriptive lowercase names. Group by the **job the script serves**, not by date, session, agent, or programming language; use one script per coherent capability.
- Reuse existing groupings; create only needed directories. Keep small helpers with their owning script. Split scripts/modules only when independent reuse or actual complexity warrants it.
- `INDEX.md` is the single human-and-agent discovery point. For each maintained script provide a short purpose, exact invocation example, arguments/inputs, effects or safety caveat, and required runtime/dependencies. Link directly to its source. Avoid a duplicated metadata catalogue or verbose histories.
- A script's own `--help` is the detailed usage authority. Add a focused README/reference beside a complex script only when `--help` and the root index are genuinely insufficient.
- Never populate the collection with placeholder utilities or copy team code/dependencies into personal storage by default.

## Review and choose

1. **Review the visible work** for repeated tool calls, command chains, tedious transformations, validation steps, predictable recovery, and recurring human tasks. Identify actual inputs, outputs, prerequisites, failure conditions, and the source of truth. Use the current conversation or selected material; consult older sources only when necessary and accessible.
2. **Inspect the relevant existing collection**, starting with `INDEX.md`, then the nearest scripts. Prefer reuse, repair, or a small extension to another near-duplicate. Do not scan every script or rewrite the whole index for an unrelated request.
3. **Decide whether code earns its cost.** Strong candidates have stable, describable inputs; rules that can be expressed deterministically; observable success/failure; likely reuse; and worthwhile reduction in agent effort **or** clear human utility. One costly/error-prone repeatable process can qualify. Do not require a numeric score, number of repetitions, or artificial quota.
4. **Reject** one-off glue, procedures that still hinge on substantial LLM judgment, fragile environment-specific shortcuts, existing adequate tooling, and scripts whose ongoing maintenance will cost more than the work saved. If only a subset is mechanical, script that subset and leave the decision to the human/agent.
5. **Choose the smallest useful action**: no-op; point to an existing command; improve/repair an existing script; create one script; or consolidate clearly redundant scripts without breaking known callers. Do not delete or silently change a used interface merely to tidy the collection.

Do not package a previously chosen sequence in a script when a straightforward shell command or existing task-runner target is already sufficient. Avoid scripts that merely add an extra invocation layer.

## Script craftsmanship

When authoring or materially changing a script, read [CLI craftsmanship](references/cli-craft.md) and apply its guidance proportionately. The core standards are:

- **Human and agent interface:** explicit meaningful arguments; sensible safe defaults; useful `--help` with a runnable example; non-interactive execution unless interaction is the job. No silent dependence on a particular cwd, hard-coded machine path, or private repository layout.
- **Predictable outcome:** validate inputs early; make the main result discoverable; use exit code 0 for success and nonzero for failures; preserve errors rather than reporting a partial result as complete.
- **Observability:** concise normal summary, actionable failure diagnostics, optional extra detail (`--verbose`) where it helps. Prefer primary/machine-readable output on stdout and progress/errors on stderr so pipelines remain usable. Do not require JSON logs, dashboards, telemetry, or always-on log files.
- **Safety:** explicit targets and side effects; prefer read-only defaults; preview/dry-run for consequential mutations where useful; avoid overwriting, deleting, secret exposure, and uncontrolled retries. Never assume creating a script grants permission to run it on real resources.
- **Maintainability:** use the simplest suitable language and standard library where practical; keep dependencies explicit, isolate I/O from testable logic when valuable, and avoid frameworks/plugin systems/configuration layers without demonstrated need.
- **Proportionate verification:** test help, representative success, invalid input, and important failure behavior. Verify safe reruns and effects when applicable. Use temporary data, mocks, or a sandbox rather than risking actual project/user data. Follow `manage-python-env` and any other applicable runtime contract for Python execution.

Scripts should be pleasant for a person to run directly and easy for a coding agent to call without reconstructing procedural detail.

## Implement, verify, and maintain

1. Confirm the personal root, relevant existing interfaces and current source facts. Select the script's minimal contract: who invokes it, required arguments, produced output, side effects, failure behavior, and runtime.
2. Implement only the justified capability. Keep reusable logic inside the single designated collection. A script may read or operate on other repositories through explicit arguments; creating a script does not authorize edits to those repositories.
3. Run the smallest meaningful safe tests available. Inspect outputs and exit codes, including an expected error. Do not claim the script was tested merely because it was written, statically inspected, or successfully uploaded through an API.
4. Maintain the exact script entry in `INDEX.md`, or add/remove it only for actual collection changes. Ensure documented commands match implemented arguments. Preserve unrelated entries and concurrent edits.
5. For an existing script, maintain compatibility when reasonable; otherwise identify known consumers and the migration needed. Do not delete on a speculative obsolescence claim.
6. Report briefly: candidate and why it qualified (or why none did), exact script path(s), a ready-to-run example, important effects/dependencies, tests actually performed, and any access/permission blockers. Distinguish a local draft from committed/published persistence.

**Success criterion:** A future agent or human can locate the right script quickly, run it with explicit inputs, understand its result or failure, and avoid repeating the original mechanical work. If not, the script has not yet delivered its value.
