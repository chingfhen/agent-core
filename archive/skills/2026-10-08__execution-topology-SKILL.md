---
name: execution-topology
description: Decide whether a project task is ready to execute, whether human blockers must be cleared first, and whether execution should use the main agent, phases, or limited subagents.
disable-model-invocation: false
---

# Execution Topology

Choose the safest execution shape for a project task.

This skill answers:

> Can execution begin now, and should it use subagents?

Use it for large, uncertain, high-risk, or multi-phase coding tasks.
Do not use it for small obvious edits.

## Core Rule

Check blockers before planning execution.

If the task needs something only the human can provide, approve, configure, or decide, stop and mark it blocked.

Do not let agents brute-force around missing credentials, secrets, dashboard setup, deployment approval, product decisions, or unclear acceptance criteria.

## Execution Gate

Assign one gate:

| Gate                             | Meaning                                                                    |
| -------------------------------- | -------------------------------------------------------------------------- |
| `Needs Human Unblock`            | Do not execute yet. Human action or decision required.                     |
| `Ready for Main-Agent Execution` | No known hard blockers. Main agent should execute, usually phase-by-phase. |
| `Ready for Delegated Execution`  | No known hard blockers. Some bounded subagent use is useful and safe.      |

If the task file supports a dashboard field, add:

```markdown
**Execution Gate:** [Needs Human Unblock | Ready for Main-Agent Execution | Ready for Delegated Execution]
```

Otherwise, include the gate inside an `Execution Topology` section.

## When to Use Subagents

Use subagents only when they reduce risk or context overload.

Good uses:

* Read-only codebase exploration.
* External docs/API research.
* Test or log triage.
* Independent review of a diff.
* Isolated implementation work with clear file boundaries.

Avoid subagents when:

* The task is small.
* Work is tightly coupled.
* Product behavior is unclear.
* Human judgment is needed often.
* Files are likely to conflict.
* Credentials, deployment, infra, or approval blockers remain.

The main agent remains the continuity owner.
Subagents are bounded helpers.

## Required Output

When invoked, produce a compact section like this:

```markdown
## Execution Topology

**Execution Gate:** [...]

**Recommended Shape:** [...]

**Blocker Preflight:** [...]

**Human Gates:** [...]

**Delegation Plan:** [...]

**Do Not Delegate:** [...]
```

Omit fields that add no value.

## Recommended Shapes

Use the simplest viable shape:

* `Main agent only`
* `Main agent phase-by-phase`
* `Planning scout(s) first, then main-agent execution`
* `Main agent + verifier subagent`
* `Main agent + limited execution subagents`
* `No execution until human unblock`

## Blocker Preflight

Before execution, check for:

* Missing API keys, tokens, credentials, or secrets.
* Missing env vars.
* Missing provider, cloud, dashboard, repo, or database access.
* Required OAuth, webhook, DNS, billing, or external setup.
* Required migration, deployment, payment, security, or product approval.
* Unclear success criteria or product behavior.
* Manual testing or login required before progress is meaningful.

If any are required, set:

```markdown
**Execution Gate:** Needs Human Unblock
```

Then write the exact human action needed.

## Human Gates

List where execution must stop.

Examples:

```markdown
**Human Gates:**
- Stop before applying database migrations.
- Stop before changing production env vars.
- Stop before deployment.
- Stop before billing/payment behavior changes.
```

## Delegation Guidance

If subagents are useful, define their scope narrowly.

Example:

```markdown
**Delegation Plan:**
- Codebase scout, read-only: map affected files and existing patterns.
- Main agent: implement phase-by-phase.
- Verifier subagent, read-only: review final diff against Success Bar.
```

If subagents are not useful:

```markdown
**Delegation Plan:** Do not use subagents. Main-agent execution is simpler and safer.
```

## Do Not Delegate

Usually do not delegate:

* Credential or secret handling.
* Production deployment.
* Provider dashboard setup.
* Database migration approval.
* Billing/payment decisions.
* Security-sensitive decisions.
* Ambiguous product behavior.
* Final integration across tightly coupled files.

## Quality Bar

A good topology note lets a fresh executor know:

* whether execution may begin;
* what blockers remain;
* whether to use subagents;
* where human approval is required;
* what must not be delegated.

If that is clear, the skill has done its job.
