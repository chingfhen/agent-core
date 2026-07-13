# Stack Checklists

Load only the sections matching the repository. Items are trace prompts
for the depth pass.

## APIs

Trace:

- authentication → authorization → ownership/tenant validation, per
  route — middleware alone does not establish object ownership
- request validation and schema conversion: required/optional/null/empty
  distinctions, bounds, unknown fields, content type
- the state-changing boundary and its transaction scope
- retry and idempotency semantics for side-effecting methods
- error mapping: status codes, leaked internals, retryability signals
- sensitive data in responses, errors, logs, caches
- versioning and backward compatibility with deployed consumers
- timeout and cancellation propagation to downstream calls

## Background workers and queues

Trace:

- enqueue → receive → validate → mutate → acknowledge
- acknowledgement relative to durable state change
- retry and backoff behaviour; nested retry amplification
- duplicate delivery and idempotency: how reservation, in-progress, and
  completed states relate atomically to the side effect; what happens if
  the process crashes before or after each transition?
- partial completion between side effects
- poison messages and dead-letter handling; DLQ replay safety
- leases/visibility timeouts vs actual processing duration
- stuck-job detection, crash recovery, cancellation, shutdown draining

## Databases and migrations

Trace:

- old/new application versions coexisting with old/new schema during
  rollout and rollback
- expand → backfill → switch reads/writes → contract ordering
- locks, table rewrites, index build mode, transaction duration at
  production data volume
- defaults, nullability, constraints, uniqueness vs existing dirty data
- dual-write and backfill idempotency and resumability
- rollback feasibility; irreversible steps flagged explicitly
- transaction boundaries; lost-update and isolation assumptions

## Cloud and infrastructure

Trace:

- effective resources, permissions, and network exposure — not template
  syntax
- identity → role/policy → resource/action/condition; wildcards and
  cross-account access
- public ingress/egress, private endpoints, TLS, metadata/service-token
  exposure
- secret references, encryption, log retention, backups, deletion
  protection
- health/readiness/startup probes; autoscaling signals and limits
- rollout strategy, version pinning, drift, rollback, stateful-resource
  replacement

## AI and data pipelines

Trace:

- dataset and schema assumptions, provenance, and ownership per stage
- train/inference preprocessing parity; evaluation leakage
- model and artifact versioning, reproducibility, lineage
- silent fallback behaviour treated as authoritative output
- partial batch completion; reprocessing and backfill idempotency
- malformed or refused model output handling; structured-output
  validation
- untrusted content reaching prompts or tools; tool authority bounds
- cost and rate-limit failure behaviour
