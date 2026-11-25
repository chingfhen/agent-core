# Personal Scripts

## Purpose and invocation

**Turn repeatable agent work into small, dependable software that both humans and agents can use.** Optimize for avoided future reasoning, tool calls, mistakes, and waiting **plus** human usefulness, not number of scripts written.

Read after Agent Builder root for "project scripts", "review scripts from this session", "automate what we did", "make this repeatable as a personal CLI", or a concrete script opportunity during human-triggered context maintenance. A general scripts cue reviews substantive available work; a named script or review-only request narrows scope. The human owns maintenance timing; the agent chooses useful interventions, including no change. Do not start persistent script stewardship during ordinary work. Temporary scripts and reuse of existing utilities remain ordinary authorized execution; preserve useful temporary work at the next authorized maintenance pass rather than reconstructing it.

Creating or fixture-testing a script does not authorize live effects, team edits, installing tools, unrelated guidance changes, publication or transfer. Respect local gates, privacy and ownership. This module owns the personal script lifecycle, not the work a script automates. Python maintenance needed for safe authorized tests follows python.md; ordinary compatible Python execution needs neither module. No recursive handoff.

## One personal location

Use the root skill's confirmed resource resolution, existing-location reuse and initialization approval rules. Default new agent-scoped collection: `.work-context/scripts/`; preserve established Project Scripts Root locations, including legacy project-scripts/ and INDEX.md. No implicit migration or competing index. The human selects any one-operation override; do not silently persist it. Group by job/domain, not repository ownership: a utility accepting a team project path does not belong to that project. Do not copy/share it with a team or transfer employer material without permission.

### Collection layout

```text
<root>/
  index.md
  <project-or-domain>/
    <verb-noun>.py                    # or an appropriate .sh/.js/.ps1
    tests/                            # only when tests justify separate files
      test_<verb_noun>.py
```

- Any suitable language or shell is permitted, including Python, Bash, PowerShell, CMD, JavaScript/TypeScript or SQL where appropriate. Choose native tooling or the simplest reliable implementation; avoid introducing a runtime merely for uniformity. Optimize for the actual operating environment; portability is useful but not required. State real platform/runtime constraints and avoid needless hard-coded paths.
- Use shallow, stable, descriptive lowercase names. Group by the **job the script serves**, not by date, session, agent, or programming language; use one script per coherent capability.
- Reuse existing groupings; create only needed directories. Keep small helpers with their owning script. Split scripts/modules only when independent reuse or actual complexity warrants it.
- `index.md` is the single human-and-agent discovery point. For each maintained script provide a short purpose, exact invocation example, arguments/inputs, effects or safety caveat, and required runtime/dependencies. Link directly to its source. Avoid a duplicated metadata catalogue or verbose histories.
- A script's own `--help` is the detailed usage authority. Add a focused README/reference beside a complex script only when `--help` and the root index are genuinely insufficient.
- Never populate the collection with placeholder utilities or copy team code/dependencies into personal storage by default.

## Review and choose

1. **Review the visible work** for repeated tool calls, command chains, tedious transformations, validation steps, predictable recovery, and recurring human tasks. Identify actual inputs, outputs, prerequisites, failure conditions, and the source of truth. Use the current conversation or selected material; consult older sources only when necessary and accessible.
2. **Inspect the relevant existing collection**, starting with `index.md`, then the nearest scripts. Prefer reuse, repair, or a small extension to another near-duplicate. Do not scan every script or rewrite the whole index for an unrelated request.
3. **Decide whether code earns its cost.** Strong candidates have stable, describable inputs; rules that can be expressed deterministically; observable success/failure; likely reuse; and worthwhile reduction in agent effort **or** clear human utility. One costly/error-prone repeatable process can qualify. Do not require a numeric score, number of repetitions, or artificial quota.
4. **Reject** one-off glue, procedures that still hinge on substantial LLM judgment, fragile environment-specific shortcuts, existing adequate tooling, and scripts whose ongoing maintenance will cost more than the work saved. If only a subset is mechanical, script that subset and leave the decision to the human/agent.
5. **Choose the smallest useful action**: no-op; point to an existing command; improve/repair an existing script; create one script; or consolidate clearly redundant scripts without breaking known callers. Do not delete or silently change a used interface merely to tidy the collection.

Do not package a previously chosen sequence in a script when a straightforward shell command or existing task-runner target is already sufficient. Avoid scripts that merely add an extra invocation layer.

## Script craftsmanship

When authoring or materially changing a script, read [CLI craftsmanship](cli-craft.md) and apply its guidance proportionately. The core standards are:

- **Human and agent interface:** explicit meaningful arguments; sensible safe defaults; useful `--help` with a runnable example; non-interactive execution unless interaction is the job. No silent dependence on a particular cwd, hard-coded machine path, or private repository layout.
- **Predictable outcome:** validate inputs early; make the main result discoverable; use exit code 0 for success and nonzero for failures; preserve errors rather than reporting a partial result as complete.
- **Observability:** concise normal summary, actionable failure diagnostics, optional extra detail (`--verbose`) where it helps. Prefer primary/machine-readable output on stdout and progress/errors on stderr so pipelines remain usable. Do not require JSON logs, dashboards, telemetry, or always-on log files.
- **Safety:** explicit targets and side effects; prefer read-only defaults; preview/dry-run for consequential mutations where useful; avoid overwriting, deleting, secret exposure, and uncontrolled retries. Never assume creating a script grants permission to run it on real resources.
- **Maintainability:** use the simplest suitable language and standard library where practical; keep dependencies explicit, isolate I/O from testable logic when valuable, and avoid frameworks/plugin systems/configuration layers without demonstrated need.
- **Proportionate verification:** test help, representative success, invalid input, and important failure behavior. Verify safe reruns and effects when applicable. Use temporary data, mocks, or a sandbox rather than risking actual project/user data. Follow the standing Python utilization contract and load python.md only for necessary environment maintenance; respect other applicable runtime contracts.

Scripts should be pleasant for a person to run directly and easy for a coding agent to call without reconstructing procedural detail.

## Ordinary discovery and utilization

When a repeatable mechanical operation is relevant, use the exact known script or index, then bounded filename/content search if needed. Read actual source/interface and safety/dependency details; don't assume a listed script is applicable or safe. Review code before invoking unknown utilities (including help if imports may have effects); use explicit inputs and authorized targets. Reuse sufficient current evidence for familiar runs. Respect platform and runtime requirements; for Python use the selected verified purpose interpreter. Inspect the result/exit status; don't recreate a sufficient utility or load the maintenance skill merely to run one. If a script is broken during ordinary work, report/use an authorized temporary alternative or request maintenance; do not silently edit durable scripts. A relevant script discovered during maintenance may be repaired/consolidated without an exhaustive sweep. Keep existing callers working; no automatic cleanup or usage tracking.

## Default AGENTS.md guidance fragment

Use the confirmed index locator in the root-owned managed block; preserve legacy names and stricter constraints. Omit absent resources; no unresolved placeholders in live guidance.

    Personal scripts: [confirmed scripts/index.md locator]
    For repeatable mechanical work, check the relevant existing utility using
    a known path or index and bounded search on misses. Read the actual interface,
    runtime requirements and effects; use explicit authorized targets and check
    results. Reuse does not need Agent Builder or authorize edits/live effects.
    Load Agent Builder and scripts.md for human-triggered script maintenance;
    temporary task-local scripts remain ordinary work.

## Implement, verify, and maintain

1. Confirm the personal root, relevant existing interfaces and current source facts. Select the script's minimal contract: who invokes it, required arguments, produced output, side effects, failure behavior, and runtime.
2. Implement only the justified capability. Keep reusable logic inside the single designated collection. A script may read or operate on other repositories through explicit arguments; creating a script does not authorize edits to those repositories.
3. Run the smallest meaningful safe tests available. Inspect outputs and exit codes, including an expected error. Do not claim the script was tested merely because it was written, statically inspected, or successfully uploaded through an API.
4. Maintain the exact script entry in `index.md`, or add/remove it only for actual collection changes. Preserve the existing index casing; never create a competing index. Ensure documented commands match implemented arguments. Preserve unrelated entries and concurrent edits.
5. For an existing script, maintain compatibility when reasonable; otherwise identify known consumers and the migration needed. Retire stale navigation or interfaces only when obsolescence is established and known consumers are protected; physical deletion or relocation requires explicit authority. Do not delete on a speculative obsolescence claim.
6. Report briefly: candidate and why it qualified (or why none did), exact script path(s), a ready-to-run example, important effects/dependencies, tests actually performed, and any access/permission blockers. Distinguish a local draft from committed/published persistence.

**Success criterion:** A future agent or human can locate the right script quickly, run it with explicit inputs, understand its result or failure, and avoid repeating the original mechanical work. If not, the script has not yet delivered its value.
