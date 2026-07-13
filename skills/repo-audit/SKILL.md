---
name: repo-audit
description: >
  Whole-repo risk audit producing one standalone markdown report. Maps the
  system, traces critical workflows for correctness, trust-boundary,
  reliability, and test gaps, then hunts bloat (supersedes yagni-audit).
  Use when the user says "audit this repo", "repo audit", "audit this
  codebase", "audit for over-engineering", "find bloat", "what can I delete
  from this repo", "repo-audit", or "/repo-audit". Source-preserving:
  writes only the audit report to artifacts/audit/; remediates nothing.
---

# Repo Audit

One-shot, repo-wide. Answers "where can this system fail, be abused,
diverge, or rot?" — not "what did this change break?" (that is diff
review). Output: one markdown report. Remediate nothing.

## Scope argument

- `/repo-audit` — repository-wide baseline: comprehensive mapping with
  risk-based depth, not exhaustive inspection of every file.
- `/repo-audit <focus>` — a dimension (`reliability`, `security`,
  `bloat`) or a path (`src/workers/`).
- `--static-only` — no command execution.

A dimension focus runs that dimension plus the baseline concerns needed
to reason about it. A path focus includes the path plus the callers,
dependencies, schemas, configuration, and tests needed to evaluate it.
`security` focus means repository-level security triage, not a
specialist security assessment. Natural-language requests such as "find
bloat" imply `bloat` focus. Record narrowing in Coverage.

## References

Load from this skill's `references/` as needed; never inline all of them
into every run.

| File | Load when |
|---|---|
| `evidence-priority.md` | Always — intent conflicts and candidate validation |
| `report-template.md` | Always, before writing the report |
| `concern-guide.md` | Before depth tracing |
| `stack-checklists.md` | Repo has APIs, workers, DB migrations, cloud/IaC, or AI/data pipelines — matching sections only |
| `bloat-guide.md` | Before the bloat pass |

## Method

0. **Establish intent.** Read the README, API/schema definitions, tests,
   migrations, deployment manifests, configuration examples, design docs,
   and targeted git history. Record: externally observable behaviour,
   authoritative contracts and schemas, important invariants, deployment
   assumptions, and uncertain or undocumented expectations. Never infer a
   defect solely from disagreement with the implementation. When sources
   conflict, apply the conflicting-evidence rules in
   `evidence-priority.md`. Use git history only to resolve intent,
   removed safeguards, ownership, duplicate implementations, or a
   specific candidate finding — never an unfocused history review.
1. **Breadth map.** Deployables and runtime entry points, public
   interfaces, stores and schemas, workers and scheduled processes,
   external systems, deployment and infrastructure, configuration, shared
   domain modules. Skip absent concerns — no operability pass for a pure
   library.
2. **Select 3–7 critical workflows.** Weigh business/data impact,
   external exposure, statefulness/irreversibility, execution frequency,
   and recovery difficulty. When present in the repo, include at least
   one each: externally triggered, state-changing, asynchronous or
   background, privileged or trust-boundary, deployment or recovery path.
3. **Depth trace** each workflow end to end against the selected concerns
   (below), using the matching stack-checklist sections.
4. **Bloat pass** per `bloat-guide.md`: light during a full baseline,
   deep for a `bloat` focus, skipped for other narrow focuses unless
   directly relevant.
5. **Validate** every candidate per `evidence-priority.md`, applying its
   stopping rules. Unresolved candidates move to Investigate.
6. **Report** per `report-template.md` to
   `artifacts/audit/YYYY-MM-DD__repo-audit.md` in the audited repo
   (create the directory). Standalone — no cross-report bookkeeping.

## Concern selection

Always consider: correctness and state integrity; trust boundaries and
authorization; reliability and failure semantics; meaningful test gaps;
operational visibility; conflicting or duplicated domain behaviour.

Activate when applicable: concurrency; database and migration safety;
API compatibility; cloud/IAM and infrastructure; performance and resource
exhaustion; sensitive-data handling; AI/data-pipeline integrity; startup,
shutdown, and deployment safety.

Do not force absent dimensions. Record activated dimensions in Coverage.

## Executable evidence

Static inspection is the default. You may run documented local commands
that do not intentionally change source, configuration, persistent data,
dependencies, or external systems — tests, type checks, dependency
inspection, repository search — when they can confirm or falsify a
material candidate finding. Prefer existing repository commands over
constructing new ones. Incidental caches and temporary test artifacts
are acceptable when understood; never commit them. Under
`--static-only`, run nothing.

Unless explicitly authorized, do not: install or update dependencies;
access the network; start persistent services; build or push images;
invoke infrastructure tooling; execute migrations; call production or
external services; run scripts with unclear side effects. Never modify
source or generated files. Never reproduce raw lint, formatting, CVE,
secret, or coverage reports. Deterministic output is evidence, not the
report — report only the contextual conclusion derived from it.

## Findings discipline

- Return the five most material root-cause findings by default. Never
  suppress an additional P0 or P1 solely to satisfy the limit. Combine
  manifestations sharing a root cause. Omit low-value overflow rather
  than appending noise.
- Priority, confidence, and class are separate labels, defined in
  `evidence-priority.md`. Low confidence never appears in Findings.
- Do not report what deterministic tools own: lint, types, formatting,
  CVE lists, secret-pattern matches, coverage %.
- Zero findings is a valid result — state it with coverage limits, never
  as "clean" or "safe".

## Scale strategy

For repositories too large for complete inspection: inventory all
deployables and major packages; exclude generated, vendored, and build
output; rank components by exposure, statefulness, and impact; select
representative cross-component workflows; search globally for each
material pattern found locally; record precisely what was examined versus
sampled; never present sampled coverage as a full-repository conclusion.

## Boundaries

- Source-preserving and non-remediating: applies no code, configuration,
  dependency, schema, or infrastructure changes. The only intended
  repository change is the audit report. One-shot.
- Change-scoped review → `/code-review` or `/security-review`. Bloat-only
  sweep of a diff → `yagni-review`.
- Style and naming preferences: out of scope entirely.
- Not an assurance boundary: absence of findings is not proof of absence.
