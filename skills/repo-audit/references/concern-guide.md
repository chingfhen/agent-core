# Concern Guide

What to examine per dimension. Each item is a trace prompt, not a box to
tick. Skip prompts with no corresponding construct in the repo.

## Always-considered core

### Correctness and state integrity

- Intended behaviour vs implementation — judge against recorded intent,
  never the function name alone.
- Preconditions: what must hold before execution, and who enforces it.
- State transitions: all legal transitions represented, illegal ones
  rejected, terminal states reachable, nothing stuck (e.g. a job left
  `RUNNING` forever).
- Partial completion: which effects can occur before failure — rollback,
  compensate, resume, or visible terminal failure?
- Boundaries: zero, one, max, empty, missing, malformed, duplicate,
  stale, reordered input.
- Cross-module assumptions: do callers and consumers assume different
  contracts (field names, error semantics, ordering, nullability)?
- Temporal assumptions: cache staleness, eventual consistency, message
  reordering.

### Trust boundaries and authorization (triage depth)

- At every state-changing access: who may act on which object in what
  state — including indirect identifiers and batch endpoints. Middleware
  authentication does not establish object ownership.
- Divergent authorization across parallel paths (REST vs GraphQL vs
  legacy endpoint vs worker-generated URL).
- Tenant/ownership keys propagated end to end.
- Secret acquisition, scope, and logging; sensitive data in responses,
  errors, logs.
- Escalate rather than deep-dive: cryptography, session design, payments,
  new public attack surface belong to specialist review — name them in
  the report's Direction, do not attempt them.

### Reliability and failure semantics

- Acknowledgement relative to durable state change.
- Duplicate delivery and idempotency: how reservation, in-progress, and
  completed states relate atomically to the side effect; what happens if
  the process crashes before or after each transition; replay response
  and key expiry.
- Retry: error classification, bounded attempts, backoff, nested retry
  amplification across layers.
- Partial failure: enumerate side effects in order; assume failure after
  each one.
- Crash recovery: restart discovery of in-progress work, lease expiry,
  reconciliation.
- Resource exhaustion and backpressure under a slow dependency.
- "Log and continue" is not recovery unless loss is an accepted
  requirement.

### Meaningful test gaps

- For each critical behaviour, identify the test oracle or deterministic
  check that would detect a regression — a broader integration, contract,
  or property-based test may protect behaviour without directly naming
  it. Absence is a candidate gap, not automatically a finding.
- Report the gap only when a material regression could plausibly reach
  production undetected.
- Failure-path and boundary tests, not only happy path.
- Mocked-away risk: retry helper mocked, status mocked instead of
  persisted and reloaded, every collaborator mocked so a contract
  mismatch cannot surface.
- Coverage percentage is never evidence.

### Operational visibility

- Failures observable: correlation/job IDs, terminal states, error
  classification, queue age, DLQ depth.
- Stuck-work detection; configuration validated at startup.
- Missing telemetry is reportable only when a traced failure would become
  materially invisible, significantly delay detection or recovery, or
  make the affected work impossible to reconcile. Do not report the
  absence of a metric merely because one could be added.
- Applies to deployed services and workers only.

### Conflicting or duplicated domain behaviour

- Same domain decision owned in multiple places, already diverging or
  able to diverge: validation rules, status enums, authorization policy.
- Change amplification: one business change requiring synchronized edits
  across unrelated files or services.
- Pure bloat (unused flexibility, dead code) routes to the bloat pass,
  not here.

## Activate when applicable

- **Concurrency:** read-modify-write, exists-then-insert, shared mutable
  state, missing locks or unique constraints. A race finding must name
  the two interleaving operations.
- **Database and migration safety:** old/new app versions coexisting
  with old/new schema; expand → backfill → switch → contract ordering;
  locks and rewrites at production volume; existing dirty data;
  irreversible steps.
- **API compatibility:** contract, version, and error compatibility with
  deployed consumers; pagination, ordering, idempotency semantics.
- **Cloud/IAM and infrastructure:** effective permissions vs required
  actions, wildcards, public exposure, secret references, probe
  correctness.
- **Performance and resource exhaustion:** report only when a traced
  workflow establishes a plausible workload, bottleneck, or
  resource-exhaustion consequence (query-per-item on an unbounded list,
  unbounded task creation). Do not report speculative
  micro-optimizations.
- **Sensitive-data handling:** classification and propagation into logs,
  caches, traces, third parties.
- **AI/data-pipeline integrity:** see stack checklist.
- **Startup, shutdown, deployment safety:** traffic before readiness,
  draining, migration ordering, rollback behaviour.
