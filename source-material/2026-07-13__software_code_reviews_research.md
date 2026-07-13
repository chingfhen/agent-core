---
title: Practical Software Review and Repository Auditing
scope: What should be reviewed or audited, how reviews should be conducted, and where OpenCodeReview fits
research_type: Understanding, Practical Guide, and Tool Evaluation
audience: Human software engineer
generated_on: 2026-07-13
sources:

* https://github.com/alibaba/open-code-review

---

# Practical Software Review and Repository Auditing

> **Claim tags** — `[OFFICIAL]`: standards, specifications, research papers, official documentation, vendor documentation, or source code. `[COMMUNITY]`: practitioner reports or engineering commentary. `[INFERENCE]`: a synthesis or recommendation not directly demonstrated by one source. “Official” does **not** mean independently verified; vendor claims remain vendor claims.

## Executive Summary

| Question | Practical conclusion |
|---|---|
| **What is code review for?** | To decide whether a proposed change should enter the system: does it implement the intended behaviour without introducing reachable correctness, security, data-integrity, reliability, integration, or maintainability regressions? Defect detection is central, but knowledge transfer, shared ownership, and design improvement are also established outcomes. `[OFFICIAL]`[^bacchelli][^google-standard] |
| **What is a repository audit for?** | To identify **systemic** risks that a diff cannot expose reliably: unclear runtime topology, conflicting responsibilities, inconsistent trust or transaction boundaries, unreliable background workflows, weak operability, obsolete paths, duplicated domain logic, dependency exposure, and gaps in the test strategy. `[INFERENCE]` |
| **Highest-value diff concerns** | (1) intended behaviour and regression risk; (2) authorization, ownership, and data integrity; (3) failure semantics and state transitions; (4) interfaces/contracts and downstream effects; (5) tests that would fail for the discovered defect. `[INFERENCE]` |
| **Highest-value audit concerns** | (1) critical workflows and invariants; (2) trust boundaries; (3) durable state and recovery; (4) reliability/operability; (5) architectural responsibility and duplicated paths; (6) test-strategy blind spots. `[INFERENCE]` |
| **How should review and audit differ?** | A review is **change-centred, bounded, and merge-oriented**. An audit is **system-centred, exploratory, and risk-oriented**. A review asks “what did this change break?” An audit asks “where can this system fail, be abused, become inconsistent, or become unmaintainable?” |
| **Where does OpenCodeReview fit?** | Use `ocr review` as a structured LLM **second pass over a diff/branch**, after deterministic checks and before or alongside human review. Use `ocr scan` as a broad **candidate-finding sweep** over selected files/directories, not as proof that a repository has received an architecture, security, reliability, or production-readiness audit. `[OFFICIAL][INFERENCE]`[^ocr-readme][^ocr-source-scan] |
| **What remains outside OpenCodeReview?** | Compilation, formatting, linting, types, tests, SAST, secret/dependency/IaC scanning, runtime verification, threat modelling, production-readiness assessment, product intent, risk acceptance, and specialist judgment. Its own benchmark reports high precision relative to general-purpose agents but low absolute recall; the best listed configuration found only 20.0% of 1,505 benchmark issues. `[OFFICIAL]` — vendor-reported, not independently replicated.[^ocr-readme][^aacr] |

### Default operating model

```text
Deterministic gates       Contextual review               Human decision
──────────────────        ─────────────────────           ──────────────
format / lint / type  ─┐  OpenCodeReview diff pass ─┐    intent & trade-offs
unit / integration    ├─> targeted LLM investigation ├─> ownership / approval
SAST / secrets / SCA  ┘  selective repo scan         ┘    specialist escalation
```

**Core rule:** do not ask an LLM to rediscover deterministic failures. Ask it to interpret interactions, trace plausible execution paths, connect dispersed evidence, and challenge assumptions. `[INFERENCE]`

---

## Review and Audit Terminology

| Activity | Primary question | Scope | Typical trigger | Expected output |
|---|---|---|---|---|
| **Line-level review** | Is this statement or local block wrong or misleading? | One hunk/function | Inline PR review, IDE review | Precise comment tied to a line and consequence |
| **Pull-request / diff review** | Does this proposed change preserve or improve system behaviour and code health? | Changed lines plus necessary surrounding/caller/dependency context | Before merge | Blocking findings, non-blocking concerns, approval |
| **Feature / branch review** | Does the complete feature work across all touched components? | Multiple commits, end-to-end workflow, deployment/config/tests | Feature completion, release candidate | Workflow-level defects and missing integration evidence |
| **Repository-wide audit** | What systemic risks exist regardless of a recent change? | Whole repo or deliberately selected subsystems | Periodic review, takeover, migration, incident, pre-release | Ranked systemic findings, evidence paths, audit coverage and gaps |
| **Architecture review** | Are responsibilities, dependencies, boundaries, and evolution costs acceptable? | System/subsystem design and implementation | Major feature, scaling change, decomposition, recurring friction | Decisions, risks, alternatives, follow-up actions |
| **Security review** | Can an attacker or unauthorized actor violate confidentiality, integrity, availability, or accountability? | Threat model, trust boundaries, code, config, dependencies, runtime controls | Sensitive feature, periodic assessment, compliance need | Exploitable scenarios, affected assets, severity, verification plan |
| **Performance review** | Does the implementation meet latency, throughput, memory, cost, and scaling needs? | Hot paths, data volume, concurrency, external calls | Performance-sensitive change or observed problem | Complexity analysis, measurement plan, benchmark/profile evidence |
| **Production-readiness review** | Can the service be deployed, operated, diagnosed, recovered, and changed safely? | Architecture, dependencies, capacity, observability, rollout, incident response | Launch, ownership transfer, major expansion | Readiness gaps and explicit launch blockers; Google SRE treats this as a service-specific reliability assessment. `[OFFICIAL]`[^sre-prr] |
| **Compliance audit** | Is there objective evidence that specified controls and obligations are met? | Defined control set and evidence period | Regulatory/contractual schedule | Control-by-control evidence, exceptions, remediation; not interchangeable with general code review |
| **Automated static analysis** | Does code match a known syntactic, semantic, data-flow, or policy pattern? | Files/whole codebase/build artifacts | Every change and scheduled scans | Deterministic findings with rule identifiers and traces |

### Overlap without conflation

- A diff review may contain security, architecture, performance, and operability observations, but it is not automatically a dedicated assessment of any of them.
- A repository scan may read every file yet still miss runtime topology, product requirements, cloud policies, data stores, deployment behaviour, or cross-repository contracts.
- “Automated review” often means static analysis in tool documentation; LLM review is probabilistic contextual analysis and should be named separately.
- Compliance asks whether specified controls are evidenced. Engineering review asks whether the system is actually safe, correct, and operable; one can pass while the other fails. `[INFERENCE]`

---

## Objectives of Code Review

Modern code review is intended to improve the codebase over time, not to achieve local perfection. Google’s published standard favours approval once a change definitely improves overall code health and states that technical facts should override preferences. `[OFFICIAL]`[^google-standard] Empirical work at Microsoft found that defect detection is a primary motivation, while actual review also yields knowledge transfer, team awareness, and alternative solutions. `[OFFICIAL]`[^bacchelli]

### Ranked objectives

| Rank | Objective | Why it creates value | Common low-value substitute |
|---:|---|---|---|
| 1 | **Verify intended behaviour and prevent regressions** | A correct-looking implementation can violate requirements, callers, state invariants, or user expectations. | Restating code or checking syntax already covered by tooling |
| 2 | **Protect authorization, ownership, and data integrity** | These failures can silently cross tenant/user boundaries or corrupt durable state. | Generic “validate input” comments without an attack/failure path |
| 3 | **Examine failure and concurrency semantics** | Production systems fail under retry, timeout, duplication, cancellation, partial completion, and races—not only the happy path. | “Add try/except” without defining desired semantics |
| 4 | **Check integration and contracts** | API, schema, event, configuration, and deployment mismatches often sit outside the changed hunk. | Reviewing each file independently without tracing consumers |
| 5 | **Assess tests as behavioural protection** | A test is valuable if it fails for a material regression and exercises the right boundary. | Requiring arbitrary coverage or tests that duplicate implementation |
| 6 | **Control material complexity and change amplification** | Complexity matters when it raises defect likelihood or makes future changes touch many places. | Subjective refactoring and naming preferences |
| 7 | **Share context and preserve ownership** | Review spreads system knowledge and records decisions. | Turning every review into a tutorial or architecture debate |

### High-value versus noise

A finding is high-value when it identifies a **reachable condition**, an **observable consequence**, and sufficient evidence that existing safeguards do not prevent it. A comment is usually noise when it merely expresses preference, duplicates a deterministic tool, assumes an impossible input, or recommends abstraction without an actual variation point. `[INFERENCE]`

---

## Objectives of Repository Auditing

A repository audit should not be one giant equal-weight checklist. Use a broad **baseline audit** to map the system and locate risks, followed by **specialist passes** where exposure warrants it.

| Audit concern | Baseline audit? | Specialist pass when… | Typical evidence |
|---|---:|---|---|
| Systemic correctness and data invariants | Always | Financial, identity, safety, or irreversible workflows | Entry point → state transitions → persistence → downstream consumers |
| Architecture and responsibility boundaries | Always | Major rewrite, split/merge, repeated change amplification | Dependency graph, duplicated domain logic, cyclic ownership |
| Security and trust boundaries | Always at triage depth | Internet exposure, auth, multi-tenancy, payments, secrets, sensitive data | Threat model, authorization path, tenant keys, cloud policies, SAST traces |
| Reliability and recovery | Always for services/workers | Queues, external services, scheduled jobs, distributed transactions | Retry/ack order, idempotency keys, transactions, DLQ, crash recovery |
| Test strategy | Always | High-risk or poorly understood subsystem | Critical workflow-to-test map, mutation/regression evidence |
| Operability and production readiness | Always for production systems | Launch, handover, scale increase, incident history | Logs/metrics/traces, alerts, health checks, runbooks, rollback/recovery |
| Performance and capacity | Risk-triggered | Hot path, high volume, cost issue, SLO risk | Profiles, query plans, load tests, complexity and data-volume estimates |
| Dependency and supply-chain health | Always via tools | Critical packages, abandoned components, build-chain exposure | Lockfiles, SBOM/SCA, provenance, update policy |
| Dead code/configuration and bloat | Secondary | Migration, long-lived repo, confusing active paths | Reachability, deployments, feature-flag state, config consumers |
| Documentation drift | Secondary | Operational procedures/contracts are externalized | Code-to-doc comparison, generated docs, runbooks |
| Compliance | Separate | A named standard/control obligation applies | Required control evidence; assessor-defined scope |

**Conclusion:** use one audit to establish the runtime map and risk register; use separate security, reliability, data, performance, or compliance audits when a credible failure has specialist depth. `[INFERENCE]`

---

## Review Dimensions: Ranked Taxonomy

**Importance is the default for small-to-medium production systems; elevate dimensions based on risk.**

| Dimension | What is examined | Example high-value finding | Review or audit | Importance | Best reviewer |
|---|---|---|---|---:|---|
| Correctness | Requirements, invariants, branches, boundary values, caller assumptions | Empty batch returns success but leaves the job permanently `RUNNING` | Both | 5 | Human + LLM + tests |
| Data integrity | Atomicity, uniqueness, ownership keys, schema semantics, irreversible writes | Worker commits debit before recording idempotency key; retry double-charges | Both | 5 | Human + DB/tooling + LLM |
| Security | Authn/authz, trust boundaries, injection, secrets, tenant isolation | Object lookup is by resource ID only; caller ownership is never checked | Both / specialist | 5 | Security-aware human + SAST + LLM |
| Reliability | Timeout, retry, idempotency, acknowledgement, recovery | Queue message acknowledged before external upload and DB commit | Both | 5 | Human/SRE + LLM + failure tests |
| Testing | Critical behavioural and failure-path protection | Retry test mocks the retry helper and never verifies duplicate side effects | Both | 4 | Human + test tools + LLM |
| API/contracts | Input/output/schema/version/error compatibility | Producer emits `userId`; consumer validates `user_id`, silently dropping event | Both | 4 | Human + contract tools + LLM |
| Operability | Visibility, health, rollout, rollback, recovery | All job failures log generic text without job/correlation ID or metric | Audit + risky reviews | 4 | SRE/platform + human |
| Architecture | Responsibility, coupling, dependency direction, boundaries | Authorization duplicated in three adapters with divergent tenant rules | Mostly audit | 4 | Senior human; LLM assists discovery |
| Concurrency | Races, ordering, locking, cancellation, shared state | `exists()` then `insert()` admits duplicates under concurrent workers | Both | 4 | Human + race/property tools + LLM |
| Maintainability | Comprehension, change amplification, coherent concepts | Adding one event type requires synchronized edits in six registries | Both | 3 | Human + LLM |
| Dependencies | Vulnerability, license, provenance, necessity, lifecycle | Internet-facing service pins a known-vulnerable transitive package | Tools + audit | 4 | SCA/tool owner + security human |
| Performance | Algorithm/data access, batching, memory, network, cost | New endpoint performs one DB query per item with unbounded list size | Risk-triggered | 3 | Profiler/load test + human + LLM |
| YAGNI/complexity | Speculation, unnecessary layers/config/deps | Four adapter/factory layers wrap one implementation and obscure transactions | Both, usually audit | 2 | Human + LLM |
| Documentation | Contracts, operations, setup, decisions | Migration changes rollback procedure but runbook still restores old schema | Audit + relevant reviews | 2 | Human; docs tooling |

### Default core

```text
ALWAYS: correctness + data integrity + authorization + failure semantics + contracts
USUALLY: meaningful tests + concurrency + operability impact + material complexity
RISK-TRIGGERED: deep security + performance + architecture + compliance
DELEGATE: formatting + style + straightforward lint/type/dependency/secret patterns
```

---

## Correctness Review

### Behavioural model

Treat each changed workflow as a small state machine:

```text
Input + prior state
      │
      ▼
preconditions ──false──> explicit rejection / no-op / retry?
      │ true
      ▼
state transition(s) ──partial failure──> rollback / compensate / resume?
      │
      ▼
postconditions + externally visible effects
```

### What to establish

| Element | Reviewer question | Evidence to inspect |
|---|---|---|
| Intended behaviour | What user/system outcome is promised? What is explicitly out of scope? | PR description, issue, acceptance tests, API docs, commit message; ask for missing intent rather than inventing it |
| Preconditions | What must be true before execution? Who enforces it? | Validation, auth, schema constraints, caller guarantees |
| Postconditions | What must be true on success? | Returned result, persisted state, emitted event, external side effect |
| Invariants | What must remain true across every path? | Uniqueness, balance, ownership, monotonic status, referential integrity |
| Boundaries | What happens at zero, one, max, empty, missing, malformed, duplicate, stale, or reordered input? | Branches, validators, type/schema limits, tests |
| State transitions | Are all legal transitions represented and illegal ones rejected? | Enum/state machine, DB updates, event handlers |
| Partial completion | Which effects can happen before failure? | Transaction boundaries, external calls, file writes, queue ack |
| Error propagation | Is failure classified, preserved, retried, hidden, or converted correctly? | Exception mapping, status codes, retry policy, logs |
| Cross-module assumptions | Does the caller/consumer make a different assumption? | Call sites, interfaces, schemas, generated clients, other implementations |
| Temporal assumptions | Can data become stale or reordered? | Cache TTL, timestamps, eventual consistency, message ordering |
| Concurrency | Can two valid executions interleave badly? | Read-modify-write, locks, unique constraints, idempotency, shared state |
| Regression surface | What existing behaviour changes unintentionally? | Unchanged callers, tests, configuration defaults, serialization |

### Trace before reporting

Use a **failure-path proof**:

```text
1. Trigger: concrete input/state/timing
2. Entry: reachable public/job/event entry point
3. Branches: exact decisions that lead to the suspect code
4. Side effects: writes/calls/events already performed
5. Missing safeguard: constraint/test/auth/transaction that does not stop it
6. Consequence: observable wrong result, corruption, leak, outage, or stuck state
7. Evidence: file:line references for the full path
```

Report a bug only after steps 1–6 are coherent. Stop investigating when the path is blocked by a verified invariant, framework guarantee, database constraint, caller validation, or impossible deployment configuration. `[INFERENCE]`

### Common reviewer errors

- Inferring requirements solely from function names.
- Treating any uncaught exception as a bug when fail-fast is intended.
- Flagging theoretically malformed data that schema/database boundaries reject.
- Ignoring old callers because they are outside the diff.
- Reporting a race without specifying two interleaving operations.
- Recommending “more validation” without deciding which boundary owns it.

---

## Security Review

NIST’s SSDF recommends reviewing/analyzing human-readable code and using automated tools; it explicitly treats self-review as a complement, not a replacement, for review by other people or tools. `[OFFICIAL]`[^nist-ssdf] OWASP ASVS provides a verification-oriented control catalogue; use it to scope sensitive systems, not as a substitute for threat modelling. `[OFFICIAL]`[^owasp-asvs]

### Normal review versus specialist assessment

**Normal review core:** changed trust boundary, authentication flow, authorization/ownership check, tenant key, input-to-sink path, secret/sensitive-data handling, cloud permission, or dependency exposure.

**Dedicated security review:** new public attack surface; cryptography; identity/session design; multi-tenant isolation; payments; sensitive data; privileged infrastructure; deserialization/plugin execution; complex business abuse; or a history of security incidents. `[INFERENCE]`

### Division by concern

| Concern | Deterministic tooling | Contextual LLM review | Human security review | Recommended handling |
|---|---:|---:|---:|---|
| Known injection patterns | Strong where rules/data flow exist | Useful for custom sinks and validation interpretation | Needed for exploitability and unusual frameworks | SAST first; LLM/human validate reachability |
| Authentication | Limited | Can trace missing/incorrect middleware use | Essential for protocol/session assumptions | Human-led; LLM maps flows |
| Authorization | Weak-to-moderate | High value for caller/resource/tenant reasoning | Essential for policy and abuse cases | Human-owned; require concrete principal-resource path |
| Resource ownership | Weak | High value across lookup/update path | Essential | LLM candidate + human confirmation |
| Tenant isolation | Moderate with explicit tenant patterns | Useful for missing tenant propagation | Essential for architecture and data model | Specialist for material multi-tenant changes |
| Input validation | Strong for known unsafe sinks; weak for business semantics | Useful for schema-to-use mismatches | Needed for domain constraints | Tools + LLM + owner |
| SQL/shell/template/file/URL injection | Strong pattern/data-flow support | Useful for wrappers, custom sanitizers, indirect sinks | Needed where exploitability is ambiguous | SAST blocks obvious; human verifies complex |
| Unsafe deserialization | Strong known APIs | Useful for custom formats/call chains | Needed for threat model | Combination |
| Secret exposure | Strong secret scanners | Useful for derived leakage or unsafe logging | Human validates sensitivity/rotation need | Scanner is primary |
| Sensitive-data logging | Moderate | High contextual value | Needed for classification/policy | LLM candidate + privacy/security owner |
| Cloud permissions | Strong IaC/cloud-policy scanners | Useful for app-to-policy mismatch | Platform/security judgment | Scanner + platform owner |
| External-service trust | Weak | Useful for TLS, webhook signature, replay, response assumptions | Essential for threat model | Human-led |
| Dependency/supply chain | Strong SCA/SBOM/provenance tools | Useful for necessity and reachable use | Needed for exception/risk acceptance | SCA primary; do not ask LLM to enumerate CVEs |
| Business-logic abuse | Weak | Useful for generating abuse paths | Essential | Human specialist; tests/simulations |

### Evidence standard for a security finding

```text
Actor / capability
    → reachable entry point
    → missing or bypassed control
    → sensitive operation or asset
    → impact and scope
    → existing mitigations checked
```

Avoid “possible SQL injection” when the code uses verified parameter binding; avoid “missing auth” until middleware, route groups, gateway policy, and deployment configuration are checked. Security reviewers report the **attack path**, not only the suspicious line. `[INFERENCE]`

---

## Reliability and Failure Semantics

Retries are safe only when the operation’s semantics make repetition safe; AWS’s guidance emphasizes caller-provided idempotency intent for mutating APIs. `[OFFICIAL]`[^aws-idempotency] Timeouts, retries, exponential backoff, and jitter are system-level choices; indiscriminate retries can multiply load and duplicate effects. `[OFFICIAL]`[^aws-retries]

### Concrete tracing questions

| Concern | Trace this path | High-value failure to detect |
|---|---|---|
| Timeout | Caller deadline → client timeout → server cancellation → ongoing side effect | Caller retries after timeout while first request still commits |
| Retry/backoff | Error classification → retry count → delay/jitter → nested retry layers | SDK, service, and worker each retry, producing retry amplification |
| Idempotency | Idempotency key creation → storage/uniqueness → response replay → expiry | Key recorded after side effect, so crash allows duplicate execution |
| Duplicate delivery | Broker delivery → handler dedupe → side effects → acknowledgement | At-least-once message creates duplicate payment/email/object |
| Queue acknowledgement | Ack/nack timing → transaction/external calls → crash points | Ack occurs before durable state, causing permanent loss |
| Dead-letter handling | Retry exhaustion → DLQ → alert → replay tooling → poison-message policy | DLQ grows silently; replay repeats non-idempotent operation |
| Partial failure | Enumerate side effects in order and fail after each | DB commits but event publish fails, leaving downstream stale |
| Transaction boundary | Which writes share a transaction? What lies outside it? | Read/update spans separate transactions and loses concurrent update |
| Rollback/compensation | Can completed external effects be reversed or reconciled? | Compensation assumes external ID was persisted, but crash occurred before save |
| Resource exhaustion | Pool/queue/thread/memory/file descriptor limits → backpressure | Unbounded task creation collapses worker under slow dependency |
| Cancellation | Client/process cancellation → child tasks → resource cleanup | Request ends but expensive subprocess continues and holds lock |
| Graceful degradation | Dependency unavailable → fallback/cache/default → correctness | Silent empty result is treated as authoritative and deletes data |
| Crash recovery | Restart → in-progress state discovery → lease expiry/reconciliation | Jobs remain `RUNNING` forever after worker death |
| Startup/shutdown | Config validation, migrations, readiness, draining, signal handling | Pod receives traffic before model/cache/schema is ready |

### Failure matrix

For every stateful workflow, write this before reviewing implementation:

| Failure point | Durable state before | External effects before | Retry behaviour | Required recovery |
|---|---|---|---|---|
| Before first write | … | … | … | … |
| Between writes | … | … | … | … |
| After write, before publish | … | … | … | … |
| After publish, before ack | … | … | … | … |
| During shutdown | … | … | … | … |

Stop once every material failure point leads to one of: atomic rollback, safe retry, explicit compensation, reconciliation, or a visible terminal failure. “Log and continue” is not a recovery strategy unless loss is an accepted requirement. `[INFERENCE]`

---

## Architecture, Maintainability, and YAGNI

### Material architecture findings

Architecture is not “I would structure it differently.” A finding is material when evidence shows one of these effects:

- **Responsibility conflict:** the same domain decision is owned in multiple places and already diverges or can diverge.
- **Dependency inversion violation:** high-level policy depends directly on replaceable infrastructure, making testing or replacement materially difficult.
- **Change amplification:** one business change requires synchronized edits across unrelated files/services/registries.
- **Hidden coupling:** behaviour depends on global state, import order, side-effectful initialization, implicit environment, or shared mutable objects.
- **Boundary leak:** transport/storage/framework details shape domain rules and make alternate execution paths inconsistent.
- **Incoherent data ownership:** multiple components can mutate the same state without a single invariant owner.
- **Operational consequence:** topology or abstraction prevents isolation, scaling, recovery, or diagnosis.

### Evidence-oriented architecture table

| Pattern | Evidence required | Usually worth reporting? |
|---|---|---:|
| Mixed business logic and infrastructure | Same policy duplicated in API, worker, CLI; tests require network/DB for pure rules | Yes, when it causes inconsistency or test friction |
| Shared mutable state | Multiple concurrent callers; no ownership/locking/lifecycle boundary | Yes |
| Circular dependencies | Build/import cycle, initialization ordering, or inability to isolate modules | Yes |
| Interface with one implementation | No second implementation, test double, boundary, or expected variation | Only if it obscures flow or increases change cost |
| Wrapper delegating every method | No policy, adaptation, instrumentation, or lifecycle value | Low priority unless repeated/systemic |
| Factory for one product | No construction complexity or selection requirement | Usually audit/YAGNI, not merge blocker |
| Duplicate domain concept | Different validation/status/schema for same entity | Yes |
| Repository organization preference | No ownership, discoverability, build, or dependency consequence | No |

### YAGNI and complexity

Google’s review guidance explicitly asks whether a change is more complex than necessary and warns against speculative generality. `[OFFICIAL]`[^google-looking]

| Candidate | Report when… | Suppress when… |
|---|---|---|
| Dead code | It is reachable only through obsolete config, confuses active paths, or retains risky dependencies | Deletion is already staged separately or framework reflection makes reachability uncertain |
| Speculative feature | It adds state, branches, permissions, or maintenance with no present caller/requirement | Small extension point is conventional and nearly cost-free |
| Single-implementation interface/factory | It adds navigation, testing indirection, or construction complexity without a boundary | It is a genuine port across domain/infrastructure or required by framework |
| Delegating wrapper | It hides transactions/errors or multiplies layers | It enforces policy, metrics, retries, adaptation, or lifecycle |
| Unused config/flag | It creates ambiguous behaviour, dormant insecure paths, or operator burden | Planned rollout is documented and time-bounded |
| Trivial dependency | It enlarges attack/build footprint for a few stable lines | Library handles subtle standard/protocol semantics correctly |
| Re-export-only file | It obscures ownership or creates circular imports | It is the deliberate public API boundary |
| Duplicate implementation | The copies represent one domain rule and can diverge | Similar-looking code has different invariants or release ownership |

**Placement:** report newly introduced material complexity in normal review; find accumulated patterns in repository audits; use a dedicated simplification pass only when bloat itself is a stated objective. `[INFERENCE]`

---

## Testing Review

A test gap is meaningful when a material behaviour can regress **without an existing test failing**. Raw coverage cannot establish this.

### Test quality criteria

| Inspect | Good evidence | Warning sign |
|---|---|---|
| Behaviour protected | Assertion names the externally meaningful outcome/invariant | Test checks internal method calls or snapshots irrelevant structure |
| Failure path | Dependency timeout/error/partial completion produces defined state | Only happy path; broad exception assertion |
| Boundary | Empty, max, duplicate, malformed, stale, reordered input | Fixtures never vary from typical case |
| State transition | Legal and illegal transitions, persistence, emitted events | Status is mocked rather than persisted/reloaded |
| Integration/contract | Real serialization/schema/client boundary at least somewhere | Every collaborator mocked; interface mismatch cannot surface |
| Regression | Test fails on the old defective behaviour | Test passes both before and after the fix |
| Concurrency/retry | Interleaving, uniqueness, idempotency, duplicate delivery | Retry helper mocked; side effects counted only locally |
| Determinism | Controlled clock/randomness/network; stable assertions | Sleeps, real time, unordered expectations, shared mutable fixture |
| Fixture realism | Includes required defaults/constraints and production-like shape | Factory creates impossible objects or bypasses validation |

### Review method

1. Name the top 1–3 externally meaningful behaviours changed.
2. For each, identify the test that would fail if the behaviour were broken.
3. Introduce the most credible failure/boundary condition mentally or with mutation.
4. Check whether the test crosses the boundary where the bug would occur.
5. Request a test only when it materially reduces regression risk.

**Mock-heavy tests are not automatically bad.** They are insufficient when the risk is precisely in wiring, schema, transactions, serialization, framework behaviour, or collaborator semantics. `[INFERENCE]`

---

## Operability and Production Readiness

Google SRE’s Production Readiness Review considers architecture/dependencies, instrumentation, emergency response, capacity, change management, availability, latency, and efficiency. `[OFFICIAL]`[^sre-prr] Kubernetes distinguishes liveness (restart), readiness (accept traffic), and startup probes, and warns that incorrect liveness probes can cause cascading failures. `[OFFICIAL]`[^k8s-probes]

### Continuous review versus periodic audit

| Concern | Review continuously when changed | Periodic/readiness audit |
|---|---:|---:|
| Structured logs and correlation/job IDs | Yes | Verify end-to-end traceability and retention |
| Metrics for success/failure/latency/queue age | Yes for new workflow | Verify SLO/alert coverage and cardinality |
| Trace propagation | Yes across new boundaries | Verify sampled end-to-end paths |
| Health/readiness/startup | When dependencies/startup change | Exercise failure and overload behaviour |
| Configuration validation | Yes | Inventory config, defaults, ownership, secret source |
| Background job status | Yes for jobs | Verify stuck-job detection, DLQ/replay, reconciliation |
| Deployment/migration safety | Every deployment-affecting change | Rehearse rollback/restore and backward compatibility |
| Feature rollout | New risky behaviour | Verify kill switch, staged rollout, telemetry |
| Alerts | When failure mode added | Check actionability, paging thresholds, ownership |
| Runbooks/data recovery | When procedure changes | Exercise tabletop or restore test |
| External dependency visibility | New/changed integration | Dependency SLOs, dashboards, quotas, failure isolation |

### Production-readiness evidence

```text
Can detect?  logs + metrics + traces + IDs + terminal job states
Can decide?  alerts + dashboards + ownership + runbook
Can mitigate? rollback + feature flag + load shedding + disable/replay controls
Can recover?  backups + restore test + reconciliation + idempotent replay
Can learn?    incident record + durable remediation + regression test
```

---

## How Reviews Should Be Conducted

### Step-by-step diff/feature methodology

| Stage | What to learn | Evidence to inspect | Common mistake | Stop condition |
|---:|---|---|---|---|
| 1. Establish intent/scope | What outcome and constraints define success? | PR/issue, acceptance criteria, commit history, demos | Inventing requirements from code | Intent is sufficient to judge changed behaviour; otherwise raise a question, not a bug |
| 2. Identify entry points | How can changed code execute? | Routes, handlers, CLI, jobs, events, scheduled tasks, exports | Starting at modified helper instead of runtime entry | All changed behaviour mapped to one or more reachable entries |
| 3. Map callers/dependencies | Who calls it and what does it call? | References, interface implementations, schemas, config, generated clients | Reading only diff context | Material upstream/downstream contracts located |
| 4. Trace success path | What effects and postconditions occur? | Branches, writes, calls, events, return values | Reviewing syntax line by line without workflow | Success state and observable result are coherent |
| 5. Trace invalid/failure paths | What happens on malformed input and dependency/process failure? | Error branches, timeouts, retries, transactions, cleanup | Generic “handle errors” comments | Each material failure has explicit semantics |
| 6. Identify state/trust boundaries | Where does authority or durable state change? | Auth, tenant keys, DB, queue, file/object store, external API | Missing middleware/policy/config outside file | Principal, asset, state owner, and boundary are known |
| 7. Inspect tests | What regression would fail? | Unit/integration/contract/e2e tests; fixtures/mocks | Counting tests or coverage | Critical changed behaviour has credible protection or a precise gap is found |
| 8. Inspect config/deployment | Does runtime wiring match code assumptions? | Env/schema, IaC, manifests, migrations, feature flags | Assuming local defaults equal production | Relevant settings and rollout compatibility checked |
| 9. Search parallel paths | Is responsibility duplicated or an old path still active? | Symbol/search, sibling implementations, consumers | Recommending duplicate code because an implementation was missed | No conflicting active implementation found |
| 10. Validate candidates | Can each issue be reproduced or logically traced? | Full path, framework docs, constraints, tests | Reporting first suspicion | Trigger, path, consequence, and missing safeguard established |
| 11. Rank/report | Which findings affect merge/release? | Impact, likelihood, reachability, confidence, safeguards | Flooding report with style/nits | Material findings reported; weak ones suppressed or posed as questions |

### Practical navigation order

```text
PR description / requirement
  → diff overview and file topology
  → public entry points
  → changed core logic
  → callers and consumers
  → state/trust boundaries
  → tests
  → config, migrations, deployment
  → final re-read of diff for local defects
```

This combines top-down intent with bottom-up line inspection. Google’s guidance asks reviewers to consider design, functionality, edge cases, concurrency, complexity, tests, documentation, every assigned line, and broader context. `[OFFICIAL]`[^google-looking]

---

## Repository Audit Methodology

### Audit pipeline

```text
Inventory → Runtime map → Critical workflows → State/trust map
         → Targeted deep dives → Tool results → Cross-cutting search
         → Validate findings → Prioritized risk register → Coverage statement
```

| Stage | Actions | Deliverable |
|---:|---|---|
| 1. Map repository | Classify source, tests, generated/vendor, IaC, migrations, schemas, docs; identify languages/build systems | Repository inventory and explicit exclusions |
| 2. Identify runtime entry points | APIs, workers, schedulers, event consumers, CLI, serverless handlers, startup code | Runtime component map |
| 3. Identify major workflows | Choose 3–10 business/operational flows by impact, frequency, irreversibility, exposure | Critical workflow list with owners |
| 4. Map data stores/state | Tables, object stores, caches, queues, files, model/artifact stores; who reads/writes | State ownership and transition diagram |
| 5. Map trust boundaries | Users/services/tenants, auth, public endpoints, webhook/provider trust, cloud roles | Threat-boundary map |
| 6. Examine background processes | Ack/retry/idempotency/DLQ/leases/scheduling/cancellation/recovery | Reliability matrix |
| 7. Examine deployment/infra | Build, secrets, permissions, network, migrations, rollout/rollback, health | Deployment and production-readiness gaps |
| 8. Examine critical tests | Map workflow risks to unit/integration/contract/e2e/failure tests | Test-strategy gap map |
| 9. Search duplicate/obsolete paths | Duplicate concepts, flags, config, endpoints, clients, migrations, dead code | Consolidated candidates with reachability evidence |
| 10. Review operational visibility | Logs/metrics/traces/alerts/job status/runbooks/recovery | Detection-and-recovery coverage |
| 11. Validate/rank | Trace systemic findings across components and check safeguards | Findings grouped by root cause, not symptom |

### Scaling the audit

| Constraint | Adaptation |
|---|---|
| Large repository | Start from runtime/deployment manifests and ownership boundaries; sample low-risk libraries; deep-review critical workflows |
| Monorepo | Partition by deployable unit and shared libraries; then audit cross-unit contracts and ownership |
| Multiple services/repos | Build a service/event/API/schema map first; no single-repo scanner can establish all contracts |
| Generated code | Exclude generation output; audit generator, schema, versioning, and reproducibility |
| Vendored code | Exclude source review; scan provenance/licenses/vulnerabilities and local patches |
| Missing docs | Derive map from entry points, manifests, routing, dependency injection, migrations, and tests; label assumptions |
| Partial access | State inaccessible repos/config/cloud/runtime evidence as coverage limitations; do not infer safety |
| Token/context limit | Retrieve by workflow: entry point → dependencies → state → tests; summarize stable facts outside the model context; avoid full-repo dumps |

**Audit sampling rule:** completeness means every high-risk runtime workflow and trust/state boundary was considered—not that every line received equal attention. `[INFERENCE]`

---

## Evidence Standards for Findings

A review comment is not a finding merely because a suspicious pattern exists. The reviewer must connect code to a reachable consequence.

### Minimum evidence package

| Evidence element | Required? | Standard |
|---|---:|---|
| Exact location | Yes | File, symbol, and line/range for the defect or design decision |
| Execution path | Yes for correctness/security/reliability | Entry point or caller → relevant branch/state operation → consequence |
| Concrete scenario | Yes | Inputs, system state, dependency behaviour, or actor capabilities needed to trigger it |
| Observable consequence | Yes | Wrong output, data loss, unauthorized action, outage, leak, cost, or material change burden |
| Reachability checked | Yes | Explain why the path can execute; do not report dead or test-only code as production risk |
| Existing safeguards checked | Yes | Validation, caller guarantees, transaction, retry policy, feature flag, test, monitoring, framework behaviour |
| Configuration checked | When relevant | Default and deployed values, environment overrides, permissions, route/middleware registration |
| Tests inspected | For behavioural findings | State whether a test covers, contradicts, or fails to cover the scenario |
| Parallel implementation searched | For systemic/design findings | Check other clients, handlers, migrations, workers, schemas, and utilities before calling it systemic |
| Framework/library semantics verified | When relied upon | Prefer official documentation, source, or a minimal executable reproduction over memory |
| Confidence | Yes | High, medium, or low, independent of severity |
| Remediation direction | Usually | State the invariant or control to restore; avoid prescribing a large rewrite without evidence |

### Finding classes

| Class | Definition | Final report treatment |
|---|---|---|
| **Confirmed issue** | Reachable path and consequence are established from repository/runtime evidence, a failing test, reproduction, or authoritative semantics | Include and prioritize |
| **Probable issue** | Strong path and consequence, but one external assumption cannot be verified from available evidence | Include with explicit assumption and confidence |
| **Design concern** | No current failure is proved, but the structure creates measurable change amplification, ownership ambiguity, or operational risk | Include only when consequence is material and evidenced |
| **Investigation question** | Missing information prevents a conclusion | Separate questions/coverage section; do not phrase as a defect |
| **Subjective preference** | Alternative naming, formatting, pattern, or abstraction with no material consequence | Suppress unless the team explicitly requested style review |

### Failure-path proof template

```text
Trigger:
  POST /jobs receives request R with idempotency key K
Path:
  handler creates DB row → publishes queue message → returns 201
Failure:
  publish times out after broker accepted the message
Retry:
  handler creates another row because K is not persisted/checked
Consequence:
  two billable jobs process the same request
Safeguards checked:
  no unique constraint, dedup store, transactional outbox, or consumer deduplication
Evidence:
  api/jobs.ts:Lx-Ly; workers/process.ts:La-Lb; migration ...
Confidence:
  High
```

A theoretical possibility without this bridge should be omitted or converted into a question. `[INFERENCE]`

---

## Prioritization and Noise Control

### Recommended model: priority × confidence × evidence state

Do **not** collapse certainty and impact into one severity label. A catastrophic but speculative concern and a modest confirmed bug need different handling.

| Priority | Meaning | Typical examples | Default action |
|---|---|---|---|
| **P0 — emergency** | Active or immediately exploitable catastrophic risk; release/operation unsafe | Public credential exposure, active cross-tenant write, irreversible migration destroying production data | Stop release/operation; incident process |
| **P1 — must fix** | Reachable material correctness, security, data-integrity, or availability defect | Authorization bypass, duplicate financial action, crash on normal input, unbounded retry storm | Block merge/release |
| **P2 — should fix** | Material but bounded risk, or structural gap likely to cause costly future failures | Missing failure-path test on critical workflow, weak diagnostics, high change amplification | Fix before merge when local; otherwise owner/date follow-up |
| **P3 — optional** | Low-impact cleanup, readability improvement, or unlikely edge case | Local simplification, noncritical naming, small duplication | Non-blocking; usually suppress from automated reports |

| Confidence | Evidence standard |
|---|---|
| **High** | Path and semantics verified; no material unknowns |
| **Medium** | Path is credible; one deployment, caller, or external-system assumption remains |
| **Low** | Pattern or suspicion only; requires investigation |

### Ranking factors

Use judgment, not a false-precision arithmetic score:

```text
Priority rises with:
  impact × reachability × likelihood/frequency × blast radius

Priority falls with:
  effective safeguards × easy reversibility/containment

Reportability rises with:
  evidence strength × confidence
```

| Factor | Question |
|---|---|
| Impact | What is lost, exposed, corrupted, delayed, or made unavailable? |
| Reachability | Can a real caller/user/event execute the path under deployed configuration? |
| Likelihood/frequency | How often do prerequisites occur, including retries and partial failures? |
| Breadth | One request, one tenant, all workers, all deployments, or persistent data? |
| Safeguards | Do constraints, middleware, transactions, tests, alerts, or operators prevent/limit it? |
| Reversibility | Can it be rolled back or repaired without data loss or prolonged outage? |
| Evidence/confidence | Is this a demonstrated defect or an unverified interpretation? |
| Remediation effort | Used to plan—not to down-rank a severe issue merely because it is hard |

### Noise controls

- Return the **root cause once**; list affected sites beneath it instead of emitting repeated comments.
- Suppress formatter, linter, compiler, type-checker, secret-scanner, or SAST findings that the deterministic tool already reports—unless interpreting reachability, impact, or a false positive.
- Prefer zero findings to weak findings. A healthy report should say what was examined and what could not be established.
- Place style, naming, and optional simplification after material defects, or omit them entirely.
- Keep low-confidence concerns in an “investigate” section rather than presenting them as bugs.
- A normal diff review often needs **0–8 material findings**; an audit is more useful as **5–15 grouped systemic themes** than hundreds of file comments. These are noise-control heuristics, not quality targets. `[INFERENCE]`

### Healthy-result format

```text
No material findings.
Reviewed: request validation, authorization path, state update, queue publication,
consumer idempotency, failure tests, and deployment configuration.
Limitations: production IAM and broker retention policy were not available.
Non-blocking deterministic output: see linter/SAST jobs.
```

---

## Division of Labour Between Tools, LLMs, and Humans

The governing principle is **deterministic detection first, contextual interpretation second, accountable judgment last**.

| Concern | Deterministic tool | LLM value | Human value | Recommended owner |
|---|---|---|---|---|
| Syntax/build failure | Compiler/build system | Explain unfamiliar error; trace likely fix | Resolve ambiguous build architecture | Compiler/build CI |
| Formatting/style | Formatter/linter | Little; may explain project-specific convention | Set convention, arbitrate exceptions | Formatter/linter |
| Type/interface mismatch | Type checker, schema compiler | Trace cross-file consequences; find unchecked boundaries | Decide interface contract | Type checker + engineer |
| Known insecure pattern | SAST/CodeQL/Semgrep | Validate reachability, data flow, and business context | Security triage/risk acceptance | Security tooling + specialist |
| Secrets | Secret scanner, provider-side revocation checks | Identify likely propagation sites | Revoke, rotate, investigate exposure | Secret scanner + incident owner |
| Vulnerable dependencies | SCA/SBOM/license tools | Explain call-site exposure or upgrade implications | Choose mitigation/acceptance | SCA + owner/security |
| IaC/cloud misconfiguration | IaC scanner, policy-as-code, cloud analyzer | Connect resource configuration to application trust path | Validate deployed topology and risk | Platform/security |
| Dead code/unused exports | Compiler/linter/dead-code detector | Check dynamic/reflection/configured usage | Confirm operational or migration usage | Deterministic tool + owner |
| Complexity metrics | Complexity/dependency graph tools | Explain why a hotspot amplifies change | Decide whether restructuring pays off | Engineer/architect |
| Unit behaviour | Unit/property tests | Generate adversarial cases; inspect missing assertions | Define intended behaviour/oracle | Engineer + tests |
| Cross-component contract | Contract/integration tests, schema diff | Trace callers and mismatched assumptions | Confirm ownership/versioning/tradeoff | Human engineer |
| Authorization/business abuse | Some SAST/DAST/property checks | Enumerate actor/resource scenarios and suspicious paths | Establish policy and exploitability | Engineer + security specialist |
| Reliability semantics | Fault injection, integration tests, model checking where feasible | Trace retries, duplicate delivery, partial commit, cancellation | Decide semantics and operational tolerance | Engineer/SRE |
| Architecture | Dependency/layer rules can enforce known constraints | Map responsibilities, duplicated concepts, change paths | Judge domain boundaries and future direction | Senior engineer/architect |
| Operability | Config validation, smoke tests, telemetry checks | Identify missing identifiers/signals along workflows | Define SLOs, alerts, runbooks, recovery | SRE/platform + owner |
| Performance | Profilers, benchmarks, load tests, query plans | Find candidate hot paths and explain complexity | Set workload, latency/cost goals; validate tradeoffs | Performance owner/engineer |
| Product intent | Requirements/tests partially encode it | Compare implementation with supplied intent | Resolve ambiguity and approve tradeoffs | Human owner |
| Review synthesis | Tool outputs and test evidence | Correlate findings, deduplicate, draft evidence | Verify, prioritize, accept responsibility | Human reviewer assisted by LLM |

### Checks an LLM should not duplicate by default

```text
formatter output
compiler/type-checker diagnostics
known linter violations
raw dependency CVEs
raw secret matches
raw SAST/IaC findings
coverage percentage
```

An LLM adds value only by answering: **Is it reachable? What fails? What safeguard exists? Is the tool result a false positive? What is the smallest material remediation?** `[INFERENCE]`

---

## Human Code Review Practices

### Evidence-backed core

| Practice | Practical conclusion | Evidence status |
|---|---|---|
| Small, self-contained changes | Easier to understand, review promptly, test, and revert; split refactors from behavioural changes where possible | Google guidance `[OFFICIAL]`; organization-specific size numbers should not be universalized[^google-small] |
| Prompt first response | Review latency blocks authors and increases context switching; respond within one working day at most, faster for small changes | Google guidance and internal case study `[OFFICIAL]`[^google-speed] |
| Author context | State intent, user-visible behaviour, risk, test evidence, rollout/migration, and known limitations; do not make reviewers infer requirements from code | Google review guidance `[OFFICIAL]`[^google-looking] |
| Review all relevant lines and context | Inspect the change, surrounding code, tests, callers, and system implications—not only highlighted lines | Google guidance `[OFFICIAL]`[^google-looking] |
| Improve code health, not perfection | Block material defects; distinguish facts from preferences; avoid forcing unrelated cleanup | Google guidance `[OFFICIAL]`[^google-standard] |
| Qualified reviewers | Add specialists for security, privacy, concurrency, data, infrastructure, or domain semantics when the risk exceeds general expertise | Google guidance `[OFFICIAL]`[^google-looking] |
| Knowledge transfer | Review also distributes ownership and reveals alternative solutions, not merely defects | Microsoft field study `[OFFICIAL]`[^bacchelli] |
| Review participation/coverage | Observational studies associate review coverage and reviewer expertise/participation with software quality; they do not prove a universal causal threshold | Empirical studies `[OFFICIAL]`[^review-quality] |

### Team policy choices—not universal truths

- Exact reviewer count, mandatory ownership rules, approval labels, and SLA targets depend on repository criticality and team topology.
- Two generalists are not a substitute for one relevant specialist.
- “LGTM with comments” is useful only when comments are genuinely non-blocking; mark **blocking**, **follow-up**, **question**, and **nit** explicitly.
- Approval means the reviewer believes the change is safe enough under stated evidence and process—not that every possible defect was excluded.

### Review-fatigue controls

```text
Author: self-review deterministic output → explain intent/risk → keep diff focused
Automation: suppress duplicate/style noise → group root causes → cap low-confidence output
Reviewer: inspect high-risk paths first → take breaks on large reviews → request decomposition
Team: route specialist concerns → measure ignored/incorrect comments → tune rules and gates
```

Security deserves deliberate routing: empirical work finds developers often do not spontaneously frame ordinary code review as a security activity, while industrial studies show security defects are still missed. `[OFFICIAL]`[^security-mcr][^security-missed]

---

## LLM-Based Code Review

### What current evidence establishes

| Claim | Assessment |
|---|---|
| LLMs can find real defects missed or not yet found by humans | Demonstrated across curated and real-PR benchmarks, but absolute recall remains low and varies strongly by model, task, language, and context `[OFFICIAL]` |
| More repository context always helps | **False.** AACR-Bench reports heterogeneous effects; SWE-PRBench reports monotonic degradation as additional context was added. Selective, relevant context is safer than indiscriminate full-repo injection `[OFFICIAL]`[^aacr][^swe-prbench] |
| PR/issue intent helps | Supported: textual task context often improves review more reliably than bulk code context `[OFFICIAL]`[^contextcrbench] |
| LLM review replaces static analysis | Unsupported. Static tools are repeatable for formalized patterns; LLMs are probabilistic and useful for contextual interpretation or defects without a fixed rule `[INFERENCE]` |
| LLM review replaces human approval | Unsupported. Product intent, architecture tradeoffs, business authorization policy, and risk acceptance remain accountable human work `[INFERENCE]` |
| LLM comments are reliable by default | Unsupported. False positives, hallucinated premises, duplicate comments, and unstable outputs are documented concerns `[OFFICIAL]`[^llm-hallucination][^llm-field] |

### Capability profile

| Relatively stronger | Relatively weaker |
|---|---|
| Local logic inconsistencies and overlooked branches | Exhaustive recall |
| Edge-case and malformed-input hypotheses | Long, indirect call chains without retrieval support |
| Comparing code with explicit requirement text | Undocumented business intent |
| Explaining suspicious data/control flow | Whole-system architecture and runtime topology |
| Finding missing validation/error handling near a change | Proving absence of alternate safeguards |
| Drafting tests and reproductions for candidate defects | Concurrency/interleaving proofs and distributed failure semantics |
| Applying natural-language project rules | Stable adherence to every rule on every run |
| Summarizing diffs and deterministic results | Precise severity calibration without concrete evidence |

### Main failure modes and mitigations

| Failure mode | Mitigation |
|---|---|
| Hallucinated API/framework behaviour | Require source/docs/reproduction; lower confidence otherwise |
| Pattern-only theoretical warning | Require reachable scenario and consequence |
| Missing repository context | Give targeted search/read tools and require caller/test/config checks |
| Context dilution | Start from diff/workflow; retrieve related code on demand; summarize stable facts |
| Duplicate comments | Structural deduplication by root cause plus semantic deduplication |
| Wrong comment line | Relocate against current diff and fall back to summary when uncertain |
| Prompt/model sensitivity | Version prompts/rules/models; benchmark on representative internal examples |
| False confidence | Separate severity, confidence, and evidence class |
| Review fatigue | Emit only material findings; learn from dismissed comments |
| Cost/token blow-up | Filter generated/vendor/test artifacts deliberately; budget per stage; stop after risk coverage |

### Interpreting benchmark results

LLM review benchmarks differ in ground-truth construction, context availability, comment matching, languages, issue severity, and whether models can use tools. Scores are therefore useful **within a benchmark**, not interchangeable product truth. AACR-Bench’s 1,505 annotated issues include diff-, file-, and repository-context defects; SWE-PRBench uses a separate 350-PR human-annotated corpus and reports frontier-model recall of only roughly 15–31% in its diff-only condition. `[OFFICIAL]`[^aacr][^swe-prbench]

**Operational conclusion:** use LLM review as a high-value *candidate generator and evidence assistant*. Gate only well-evidenced P0/P1 findings or organization-tested high-precision rules; never interpret silence as proof of safety. `[INFERENCE]`

---

## AI-Generated Code as a Review Target

AI-generated code should receive the **same evidence standard** as human code but stronger provenance, integration, and assumption checks. Available evidence supports some risks more directly than others.

| Pattern | Evidence status | Adapted review action |
|---|---|---|
| Insecure generated code | Controlled studies and large empirical analyses show material rates of security weaknesses in generated snippets; exact rates are model/task-dependent `[OFFICIAL]` | Run SAST/tests; trace auth, injection, secrets, and resource ownership rather than trusting plausible syntax[^ai-security] |
| User overconfidence | Controlled evidence found AI-assisted participants could be more confident despite writing less-secure code `[OFFICIAL]` | Require executable evidence and independent review for security-sensitive changes[^ai-confidence] |
| Hallucinated/nonexistent packages | Large-scale research demonstrates package hallucination, especially among open-source models `[OFFICIAL]` | Lock dependencies; verify package identity/provenance; use allowlists/SCA; reject unexplained new packages[^package-hallucination] |
| Happy-path-only behaviour | Plausible and frequently observed, but not established as a universal AI-specific rate `[COMMUNITY]` | Force invalid input, failure, retry, cancellation, and partial-state traces |
| Incorrect framework assumptions | Plausible consequence of generated code and model staleness `[INFERENCE]` | Verify route/middleware/lifecycle/transaction semantics against current docs or executable tests |
| Duplicate implementations/convention drift | Likely when agents lack repository retrieval or work in parallel `[INFERENCE]` | Search existing symbols, clients, schemas, utilities, and patterns before accepting new abstractions |
| Excess dependencies/abstractions/config | Practitioner-reported and plausible, not uniquely attributable to AI `[COMMUNITY]` | Ask what requirement each layer/config/dependency serves; simplify only when material |
| Tests mirror implementation | General testing anti-pattern; AI can generate superficially convincing paired code/tests `[INFERENCE]` | Check independent behavioural oracle, mutation/failure cases, and contract tests |
| Missing authorization/idempotency | Serious system-level omissions but not proven uniquely AI-generated `[INFERENCE]` | Apply dedicated resource-ownership and repeated-delivery scenarios |
| Comments overstate completeness | Plausible language-generation failure `[INFERENCE]` | Treat comments as claims; verify against reachable code, tests, and deployment |

### AI-change review delta

```text
Normal review core
+ identify generated regions and prompt/task intent
+ verify every new API/package/framework assumption
+ search for pre-existing equivalent code
+ inspect tests for independent behavioural oracles
+ trace system integration beyond locally generated files
+ challenge silent fallbacks, generic exceptions, placeholders, and TODO paths
+ run deterministic tools and execute the change; plausible prose is not evidence
```

The distinctive risk is less “AI writes one special class of bug” than **high-volume, locally plausible code produced without durable system understanding**. Review effort should therefore shift from syntax toward repository fit, hidden assumptions, and end-to-end semantics. `[INFERENCE]`

---

## OpenCodeReview Overview

### Project objective and operating model

OpenCodeReview is an Apache-2.0 Alibaba project that turns a configured LLM into a repeatable CLI/CI reviewer. The project states that it originated from Alibaba’s internal code-review practice and combines deterministic orchestration with agentic repository tools rather than relying on a single unconstrained coding-agent prompt. `[OFFICIAL]`[^ocr-readme]

As inspected on **2026-07-13**, the latest GitHub release was **v1.7.7 (2026-07-10)**. `[OFFICIAL]`[^ocr-releases]

```text
                         OpenCodeReview
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
     ocr review                               ocr scan
   Git diff / PR                           Full selected files
          │                                       │
  parse and filter files                  walk paths + .gitignore
          │                                       │
  per-file review unit                    optional per-file plan
          │                                       │
  LLM plan + tool loop                    full-file LLM review
          │                                       │
  async comment validation                concurrent within batches
          │                                       │
  relocate to diff lines                  batch-level LLM dedup
          │                                       │
  per-file summaries                      repository summary
          └───────────────────┬───────────────────┘
                              │
                 CLI / JSON / HTML / GitHub CI
```

### Commands and intended modes

| Command | Input | Core purpose | Important controls |
|---|---|---|---|
| `ocr review` | Git working tree, staged changes, branch/commit range, or PR-oriented diff | Review proposed changes before merge | base/head/commit selection, rules, exclusions/includes, output/audience, concurrency, requirement background |
| `ocr scan` | Selected repository paths/files, even outside a Git diff | Sweep current full-file contents for candidate issues | path/exclude/include, preview, token budget, batching, concurrency, `--no-plan`, `--no-dedup`, `--no-summary` |
| `ocr setup` | Interactive configuration | Configure model/provider and defaults | provider/model/base URL/API key/config |
| `ocr view` | Local session data | Inspect report, prompts, and model responses | local viewer/host controls |

`ocr review` and `ocr scan` are complementary: the first answers “what risk does this change introduce?”; the second answers “what candidate defects exist in the selected current files?” Neither command, by itself, establishes requirements, runtime configuration, production behaviour, or comprehensive audit coverage. `[OFFICIAL]` for mechanics; conclusion `[INFERENCE]`.[^ocr-readme][^ocr-source-review][^ocr-source-scan]

### Diff-review pipeline (`ocr review`)

The implementation follows approximately this sequence: `[OFFICIAL]`[^ocr-source-review]

```pseudo
resolve git range and parse file diffs
apply binary/path/language/rule filters
make full diff map available for related-change inspection
for each selected file, up to configured concurrency:
    construct review unit from file diff + rule + optional requirement
    ask model to plan investigation
    run bounded agent loop with repository tools
    collect structured comments
    asynchronously:
        verify/reflect on candidate comments
        validate suggestions
        track/retrack changed line positions
    emit comments and file summary
render terminal/json/html/GitHub-compatible output
checkpoint session and isolate per-file failures
```

#### Review-unit and context behaviour

- The principal decomposition is **one changed file per review unit**. `[OFFICIAL]`
- The agent can inspect the full file, search code, find/read other files, and read related diffs through tools. `[OFFICIAL]`
- A complete map of changed-file diffs is injected so the model can inspect related changes, including changed files not independently dispatched for review. `[OFFICIAL]`
- Files are dispatched concurrently; default concurrency documented by the project is 8. `[OFFICIAL]`
- Very large units are filtered against a fraction of the model context budget rather than blindly submitted. `[OFFICIAL]`
- Comment post-processing attempts line tracking/relocation, reflection, and suggestion validation before presentation. `[OFFICIAL]`

This is **cross-file-capable but file-centred**. Whether cross-file defects are found depends on the plan, retrieval choices, rule, model, and available context; access to a search tool is not evidence of exhaustive data-flow analysis. `[INFERENCE]`

### Repository-scan pipeline (`ocr scan`)

The implementation follows approximately this sequence: `[OFFICIAL]`[^ocr-source-scan][^ocr-source-batch]

```pseudo
walk requested paths
honor .gitignore and OpenCodeReview include/exclude/language rules
optionally preview selected files
partition files by language, top-level directory, or no grouping
for each batch sequentially:
    for each file concurrently:
        optionally ask model for a review plan
        if planning fails, fall back to direct review
        submit full file plus applicable rule
        allow repository search/read tools
        collect structured comments
    optionally ask model to deduplicate batch comments
    preserve originals if deduplication fails/malformed
optionally generate one project summary from retained comments
stop/skip according to context and total token budget
```

Important implications:

1. “Repository-wide” describes **file selection**, not a single global architectural reasoning pass. Files remain independently reviewed; batches organize execution and deduplication. `[OFFICIAL]` for implementation; interpretation `[INFERENCE]`.
2. Directory/language batching does not prove joint reasoning over every file in the batch. `[INFERENCE]`
3. The final project summary summarizes discovered comments; it cannot recover defects the per-file passes never found. `[INFERENCE]`
4. Scan cost/noise grows with selected files, model, rules, and context retrieval; token budget and focused paths are therefore material controls. `[OFFICIAL]`

### File selection and rules

OpenCodeReview applies deterministic selection before model review. `[OFFICIAL]`[^ocr-readme]

```text
binary / unsupported file
        ↓ remove
explicit user excludes
        ↓ remove
explicit includes
        ↓ can force otherwise-excluded paths into scope
built-in default exclusions
        ↓ remove
rule matching by path/language
        ↓
selected review units
```

Rule precedence is documented as:

```text
CLI --rule
  > repository .opencodereview/rule.json
  > global configuration
  > embedded system_rules.json
```

Path rules use first-match behaviour; custom instructions can be merged with a system rule. `[OFFICIAL]`

**Material default:** the documented built-in exclusions omit many conventional test paths and filenames across Go, Java/Kotlin, Rust, JavaScript/TypeScript, Python, and Ruby. Tests can be forced into scope using include/rule configuration, but a default run should not be described as a complete test review. `[OFFICIAL]`[^ocr-readme]

### Structured findings

The project’s structured schema includes categories:

```text
bug | security | performance | maintainability
test | style | documentation | other
```

and severities:

```text
critical | high | medium | low
```

These labels are an output schema, not proof that each category receives equal depth or that severity is calibrated to an organization’s risk model. `[OFFICIAL]` for schema; limitation `[INFERENCE]`.

### Providers, configuration, and extensibility

- Supports documented commercial and open-model providers plus OpenAI-compatible and Anthropic-compatible custom endpoints. `[OFFICIAL]`
- Custom base URLs make private gateways or self-hosted model routes possible, subject to the configured provider’s actual deployment. `[OFFICIAL]`
- Supports repository/global rules and path-specific instructions. `[OFFICIAL]`
- Supports external MCP servers with configured commands and tool allowlists. `[OFFICIAL]`
- Supports terminal, JSON, HTML/session viewing, CI/GitHub workflows, and local invocation from coding-agent workflows. `[OFFICIAL]`
- Claude Code, Codex, Cursor, or another agent can call `ocr review --audience agent`; OpenCodeReview still uses its independently configured review model/backend. `[OFFICIAL]`

### Privacy and trust boundaries

OpenCodeReview’s assurance case explicitly models the local repository and configured LLM provider as trust boundaries: repository diffs/source are sent over HTTPS to the chosen model provider, model responses return as comments, and optional local session/viewer functionality stores/exposes prompts and responses. `[OFFICIAL]`—project self-assessment, not an independent security audit.[^ocr-assurance]

Practical controls:

| Risk | Control |
|---|---|
| Source sent to third party | Use an approved provider/private endpoint; verify provider retention/training/residency terms |
| Secrets in code/context | Run secret scanning first; exclude sensitive generated/config material; do not assume prompts are secret-safe |
| Local session disclosure | Protect `~/.opencodereview/sessions/`, viewer bind/host settings, CI artifacts, and logs |
| MCP tool expansion | Allowlist minimum tools; treat MCP servers and their outputs as additional trusted components |
| Prompt injection in repository text | Treat repository content as adversarial instructions; constrain tools and validate outputs—especially in untrusted PRs `[INFERENCE]` |
| Optional telemetry/content logging | Keep content logging disabled unless explicitly required and protected; verify actual configuration |

OpenCodeReview cannot guarantee that a provider does not retain or train on code; that is a property of the selected service contract/deployment, not the CLI. `[INFERENCE]`

---

## OpenCodeReview Review Model

### Coverage mapped to the broader taxonomy

| Review concern | Covered by OpenCodeReview? | Review mode | Evidence | Limitations |
|---|---:|---|---|---|
| Changed-line/local correctness | **Yes, primary** | `review` | Diff units, full-file/read/search tools, `bug` category `[OFFICIAL]` | Low recall remains; behaviour intent may be missing |
| Cross-file correctness | **Partial** | Both | Related diffs and repository tools `[OFFICIAL]` | Retrieval is model-directed; no exhaustive call/data-flow proof `[INFERENCE]` |
| Whole-file latent defects | **Yes, candidate sweep** | `scan` | Full selected file reviewed `[OFFICIAL]` | File-centred decomposition; selection/context limits |
| Repository systemic correctness | **Limited** | `scan` | Multiple files selected and summarized `[OFFICIAL]` | No explicit workflow/state architecture model; summary only reflects found comments `[INFERENCE]` |
| Security patterns/business logic | **Partial** | Both | Security category and configurable rules `[OFFICIAL]` | Not SAST/DAST/threat modelling; authorization and exploitability need verification |
| Reliability/failure semantics | **Partial** | Both | Natural-language rules and contextual reasoning | Requires explicit rules/context; no fault injection or runtime evidence `[INFERENCE]` |
| Maintainability/local complexity | **Yes** | Both | Maintainability category, full-file context `[OFFICIAL]` | Subjective/noise risk; architecture consequence may be unproved |
| Architecture/module boundaries | **Weak to partial** | Mostly focused `scan` | Search/read tools can inspect related code `[OFFICIAL]` | Per-file review units and no repository graph/architecture pass `[INFERENCE]` |
| Tests/test gaps | **Partial and configuration-dependent** | Both | `test` category and tools `[OFFICIAL]` | Many test files are excluded by default; cannot execute tests itself as review evidence unless externally integrated |
| Performance | **Partial** | Both | Performance category/rules `[OFFICIAL]` | Static suspicion only; workload/profile/query-plan evidence absent |
| Documentation drift | **Partial** | Both | Documentation category, docs can be selected `[OFFICIAL]` | Requires authoritative behaviour/requirements to compare against |
| API design/contracts | **Partial** | Both | Diff/file/search context | Cross-repo consumers and deployed versions may be unavailable |
| Data integrity/migrations | **Partial** | Both | Can inspect migrations/schema/callers when selected | No live schema, transaction trace, or data validation by default |
| Concurrency | **Limited** | Both | LLM can reason from code | Interleavings are difficult; no model checking/stress execution |
| Dependencies/supply chain | **Weak** | `scan` | Can comment on manifests | Should defer CVE/provenance/license detection to SCA/SBOM tools |
| Dead code/unused config | **Partial** | `scan` | Repository search and full files | Dynamic use/reflection/deployment config can produce false positives |
| Operability | **Partial** | Focused `scan` | Can inspect logs/metrics/health/config/IaC | No telemetry, SLO, alert, or runtime-state access by default |
| Production readiness | **Not comprehensive** | Focused `scan` may assist | Can inspect selected deployment/operational files | PRR requires architecture, ownership, capacity, runtime, rollback, and operational evidence outside source |
| Compliance audit | **No, not by itself** | Neither | Custom rules may check code evidence | Compliance requires scoped controls, evidence chain, process/runtime records, and accountable auditors |

### Default concern core for OpenCodeReview

```text
Best fit
├── diff-local correctness and edge cases
├── contextual security/reliability candidates near changed code
├── cross-file integration issues when retrieval succeeds
├── missing or weak tests for changed behaviour
└── material local maintainability problems

Supporting/focused fit
├── full-file bug sweeps
├── targeted security or reliability rules
├── selected migration/API/worker/IaC paths
└── duplicate or obsolete implementations with search evidence

Poor fit as sole reviewer
├── deterministic syntax/style/CVE/secret/IaC rule detection
├── exhaustive whole-program data flow
├── architecture governance
├── runtime performance/capacity
├── production readiness
├── threat modelling/penetration testing
└── compliance attestation
```

---

## OpenCodeReview Evaluation Evidence

### Project-published benchmark

OpenCodeReview reports results on **AACR-Bench**, a benchmark created by an overlapping Alibaba-led author group. AACR-Bench contains 200 real pull requests from 50 active open-source repositories, 10 languages, and 1,505 expert-verified issue annotations; issues are labelled by the context needed to identify them: 754 diff-level, 518 file-level, and 233 repository-level. `[OFFICIAL]`[^aacr]

The OpenCodeReview README publishes the following comparison. These are **vendor/project-reported results**, not independent product validation. `[OFFICIAL]`[^ocr-readme]

| System / model | F1 | Precision | Recall | Correct / comments | Avg time | Avg tokens |
|---|---:|---:|---:|---:|---:|---:|
| OpenCodeReview / Claude-4.6-Opus | **25.10%** | 33.90% | 20.00% | 301 / 889 | 1m23s | 385K |
| OpenCodeReview / GLM-5.2 | 21.30% | 32.30% | 15.90% | 239 / 741 | 7m58s | 682K |
| OpenCodeReview / Qwen3.7-Max | 21.20% | 25.20% | 18.30% | 276 / 1,095 | 4m41s | 625K |
| OpenCodeReview / GPT-5.5 | 21.00% | 32.10% | 15.50% | 233 / 726 | 2m51s | 422K |
| OpenCodeReview / GLM-5.1 | 20.40% | 28.90% | 15.70% | 236 / 816 | 4m11s | 743K |
| OpenCodeReview / Claude-4.8-Opus | 17.90% | 37.80% | 11.70% | 176 / 466 | 1m06s | 352K |
| OpenCodeReview / Deepseek-V4-Pro | 17.90% | 30.60% | 12.70% | 191 / 624 | 6m28s | 394K |
| Claude Code / Claude-4.8-Opus | 14.13% | 15.93% | 12.70% | 191 / 1,199 | 5m38s | 2,062K |
| Claude Code / Qwen3.7-Max | 12.17% | 8.23% | 23.37% | 352 / 4,276 | 8m06s | 5,153K |
| Claude Code / GLM-5.1 | 11.93% | 8.37% | 20.80% | 313 / 3,739 | 14m10s | 4,038K |
| Claude Code / Claude-4.6-Opus | 11.57% | 7.23% | **28.90%** | 435 / 6,016 | 13m06s | 5,664K |
| Claude Code / Deepseek-V4-Pro | 10.93% | 8.27% | 16.13% | 243 / 2,939 | 14m24s | 5,450K |
| Codex / GPT-5.5 | 8.36% | 27.82% | 4.92% | 74 / 266 | 2m58s | 525K |

### What the benchmark supports

- On this benchmark/configuration, OpenCodeReview’s orchestration produced a better precision–recall balance than the listed general-purpose-agent baselines, while several baselines emitted far more comments/tokens for higher recall but low precision. `[OFFICIAL]`
- The best listed OpenCodeReview result still found only **20%** of the 1,505 annotated issues; silence cannot be treated as safety. `[OFFICIAL]`
- Model choice materially changes precision, recall, cost, and latency even within the same orchestration. `[OFFICIAL]`
- The project’s “roughly one-ninth the tokens” claim depends on which rows are compared; the table does support substantially lower token consumption than many Claude Code baselines, not a universal ratio for every model/workload. `[OFFICIAL]` plus qualification `[INFERENCE]`.

### Evidence limitations

| Question | Assessment |
|---|---|
| Benchmark design | Real OSS PRs with reconstructed/expanded annotations; substantially stronger than synthetic bug snippets `[OFFICIAL]` |
| Ground truth | AI-assisted candidate generation plus professional-engineer verification; AACR-Bench authors acknowledge complete issue ground truth remains difficult `[OFFICIAL]` |
| Repository/language breadth | 50 repositories and 10 languages; useful but not representative of every framework, private monorepo, cloud/IaC, data/AI workload, or safety-critical domain `[OFFICIAL]` + `[INFERENCE]` |
| Selection bias | Active public OSS and selected PRs may differ from enterprise/private repositories and AI-generated changes `[INFERENCE]` |
| Baseline parity | Results depend on prompts, model versions, tool permissions, token budgets, and agent configuration; table alone cannot establish universally optimal baseline tuning `[INFERENCE]` |
| Reproducibility | Benchmark code/data are published; exact provider model versions and hosted behaviour can still change `[OFFICIAL]` |
| Independent validation | No independent published replication of the OpenCodeReview product results was found in this research `[INFERENCE]` |
| `ocr scan` evaluation | The highlighted benchmark is PR/code-review oriented; it does not validate a comprehensive repository-audit methodology or architecture-review recall `[INFERENCE]` |
| Cost | Token counts are published, but monetary cost is provider/model/date dependent and should be measured locally `[INFERENCE]` |
| Comment utility | Precision/recall matching does not fully measure remediation quality, severity calibration, reviewer trust, or workflow disruption `[INFERENCE]` |

AACR-Bench itself reports that context effects vary by model and programming paradigm. A separate 2026 preprint, SWE-PRBench, found that eight frontier models detected only 15–31% of human issues in a diff-only setting and all degraded as progressively larger context was added, with a compact structured summary outperforming longer full context. The studies conflict on the exact context curve but agree that context must be selected, not maximized. `[OFFICIAL]`[^aacr][^swe-prbench]

---

## OpenCodeReview Strengths and Limitations

### Strengths

| Strength | Why it matters | Evidence class |
|---|---|---|
| Deterministic front-end selection | Reproducible scope, exclusions, language/rule routing before probabilistic review | `[OFFICIAL]` |
| Purpose-built review orchestration | Diff parsing, per-file units, requirement context, repository tools, structured comments | `[OFFICIAL]` |
| Related-code retrieval | Better chance of validating callers/other diffs than a line-only prompt | `[OFFICIAL]`; effectiveness remains model-dependent |
| Parallelism and failure isolation | Practical CI latency and resilience across files | `[OFFICIAL]` |
| Comment relocation/reflection | Reduces stale-line and unsupported-comment noise compared with raw model output | `[OFFICIAL]`; effectiveness not independently quantified |
| Semantic deduplication in scan | Can group repeated batch findings; failure preserves originals | `[OFFICIAL]` |
| Path-specific/custom rules | Aligns checks to language/component risk rather than one universal checklist | `[OFFICIAL]` |
| Repeatable CLI/CI/agent integration | Same reviewer can run locally, in GitHub workflows, or from coding-agent sessions | `[OFFICIAL]` |
| Provider flexibility | Supports approved private gateways/self-hosted endpoints where configured | `[OFFICIAL]` |
| Published benchmark and source | More inspectable than opaque review products | `[OFFICIAL]` |

### Limitations

| Limitation | Consequence | Evidence class |
|---|---|---|
| Model-quality dependence | Recall/precision/cost vary materially by model and version | `[OFFICIAL]` benchmark |
| Low absolute recall | Best published row finds 20% of annotated issues | `[OFFICIAL]` |
| File-oriented decomposition | Systemic workflow/architecture defects may not become salient in any one unit | `[INFERENCE]` from source design |
| Selective/model-directed retrieval | Alternate safeguards or distant callers can be missed | `[INFERENCE]` |
| Context/token constraints | Large/generated files and broad scans require filtering/budgeting; excess context can hurt | `[OFFICIAL]` + external papers |
| Tests excluded by default | Test quality and gaps may be incompletely reviewed unless explicitly included | `[OFFICIAL]` |
| No runtime execution by itself | Cannot prove tests pass, reproduce failures, profile performance, inject faults, or inspect telemetry | `[INFERENCE]` from documented tool scope |
| Weak global architecture evidence | Scan summary aggregates comments; it is not an explicit architecture/state/trust model | `[INFERENCE]` |
| Language/rule maturity can vary | Generic categories do not guarantee equal framework/language expertise | `[INFERENCE]` |
| Privacy delegated to provider | Source leaves the machine unless routed to an approved endpoint; provider policy governs retention | `[OFFICIAL]` + `[INFERENCE]` |
| Configuration complexity | Rules, exclusions, providers, context, MCP, and token budgets require ownership/tuning | `[INFERENCE]` |
| Benchmark generalisability | Public OSS PR benchmark does not establish performance on private cloud/data/AI repositories or repository audits | `[INFERENCE]` |
| Missing product/operational context | Business intent, production topology, SLOs, incident history, and cross-repo contracts may be absent | `[INFERENCE]` |
| Probabilistic rule adherence | Natural-language rules cannot guarantee every check is followed on every run | `[OFFICIAL]` maintainer statement[^ocr-rules] |

---

## OpenCodeReview `review` vs `scan`

| Dimension | `ocr review` | `ocr scan` |
|---|---|---|
| Scope | Git diff/change range plus retrieved related context | Full contents of selected current files/paths |
| Primary use | Pre-merge change-risk review | Periodic or targeted latent-defect sweep |
| Review unit | One changed file/diff | One full file |
| Context | Requirement/commit background, full file, code search/read, related diffs | Full file, optional plan, repository search/read |
| Expected findings | Regressions, changed-line defects, integration/test gaps introduced by change | Existing local defects, repeated patterns, obsolete/weak implementations in selected scope |
| Cost | Usually lower and proportional to change | Potentially high and proportional to selected repository scope |
| Noise risk | Lower because change supplies relevance | Higher because unchanged code lacks trigger/intent and repeats systemic symptoms |
| Cross-file reasoning | Supported through related-diff map and tools, but not exhaustive | Supported through tools, but files remain independently reviewed |
| Architectural value | Low–moderate for architecture consequences of a change | Moderate only when narrowly scoped/rule-guided; weak as a complete architecture audit |
| Summary | Per-file/change-oriented output | Optional project summary after batch deduplication |
| Recommended frequency | Every material PR/branch before human approval, after deterministic checks | Periodically, before major release, after agent-heavy development, or on one high-risk subsystem—not necessarily every commit |
| Best configuration | Include intent, affected tests/config, high-signal rules; review modest diff | Focus paths/workflows, include tests explicitly, choose specialist rules, set token budget, validate themes manually |

### Recommended use

```text
Use review when:
  a change has a clear intent and merge decision
  you need evidence tied to changed code
  cost/noise must stay bounded

Use scan when:
  inherited or agent-generated code lacks recent review
  a subsystem is about to ship or change ownership
  searching for repeated/systemic candidates
  running a focused security/reliability/cleanup pass

Do not call scan a complete audit unless humans also establish:
  repository/runtime map, critical workflows, state/trust boundaries,
  deployment/runtime evidence, specialist tool results, and coverage limitations.
```

---

## Comparison With Alternatives

This comparison locates responsibilities; it is not a product ranking. Hosted products change frequently, and vendor capability statements are not independent quality evidence.

| Approach | Main scope | Determinism | Repository context | Security capability | Repository-audit support | Best role relative to OpenCodeReview |
|---|---|---:|---|---|---|---|
| General-purpose coding agent | User-directed inspection, editing, tests, shell/tools | Low | Potentially broad and interactive | Contextual, user-prompted | Flexible but unstructured | Deep investigation/reproduction after OCR raises a candidate; less repeatable as a standing gate |
| GitHub Copilot code review | GitHub/IDE change review with repository/custom-instruction context `[OFFICIAL]`[^copilot-review] | Low–moderate orchestration | Platform-native | Contextual review, not dedicated SAST | Primarily PR/change review | Managed GitHub-native alternative; compare on internal precision, governance, and integration rather than feature labels |
| Claude Code review workflows | Agentic codebase exploration; Anthropic also documents multi-agent web code review `[OFFICIAL]`[^claude-review] | Low unless scripted | Broad/tool-driven | Contextual | Can perform ad hoc audits | Strong interactive investigator; OCR adds an inspectable, repeatable review-specific pipeline |
| Codex review workflows | Local `/review`, GitHub review, repository guidance, serious issue focus `[OFFICIAL]`[^codex-review] | Low–moderate orchestration | Repository/tool context | Contextual | Mostly change review/ad hoc investigation | Similar role for agent users; OCR offers provider-neutral rules and explicit scan mode |
| CodeRabbit | Managed PR review, configurable path instructions/knowledge and some cross-repository context `[OFFICIAL vendor]`[^coderabbit] | Product-managed | Platform and configured knowledge | Contextual | PR-centric, vendor features may extend beyond | Managed collaboration/product experience versus self-hostable/open orchestration |
| Qodo | Managed multi-agent/context-aware PR review and organizational context claims `[OFFICIAL vendor]`[^qodo] | Product-managed | Vendor-described broad context | Contextual | Primarily PR/process oriented | Enterprise-managed alternative; claims require local validation |
| SonarQube | Rule-based static analysis across branches/PRs/codebase | High for a fixed analyzer/rule/version | Semantic analyzers, not product intent | Known vulnerability/quality rules | Good for deterministic codebase-wide issue inventory | Run before OCR; OCR should interpret relevant findings, not recreate them[^sonarqube] |
| Semgrep | Pattern/data-flow SAST, secrets, SCA depending product/config | High for fixed rules/engine | Rule-defined code/data flow | Strong for codified classes | Codebase scan, not architecture/PR intent | Primary known-pattern detector; OCR for contextual business logic and triage[^semgrep] |
| CodeQL | Query-based semantic/data-flow analysis and code scanning | High for fixed DB/query/version | Whole code database | Strong for supported vulnerability queries | Strong codebase analysis, not complete operational audit | Primary deep SAST; OCR can explain reachability/remediation and find non-query contextual issues[^codeql] |
| Snyk | Dependency, code, container, IaC and supply-chain scanning by product | High–moderate for fixed engines/databases | Artifact/config focused | Strong for known vulnerabilities/misconfigurations | Security inventory, not general architecture | Run as dedicated security tooling; OCR should not substitute for it[^snyk] |
| Conventional human PR review | Intent, system fit, tradeoffs, ownership, risk acceptance | Variable but accountable | Tacit/domain/cross-system knowledge | Strong with relevant expertise, still fallible | Human-led audit can integrate runtime/process evidence | Required final decision-maker; OCR increases coverage and prepares evidence |

### Practical selection rule

```text
Need a formalized, repeatable pattern?        → deterministic analyzer
Need to execute or reproduce behaviour?       → tests, sandbox, profiler, fault injection
Need to explore an uncertain candidate?       → coding agent or engineer
Need repeatable contextual PR screening?      → OpenCodeReview or managed AI reviewer
Need architecture/product/risk judgment?      → accountable human
Need security assurance?                      → security tools + threat model + specialist/testing
Need a repository audit?                      → human-led methodology using all of the above
```

### OpenCodeReview’s distinctive position

OpenCodeReview is most differentiated by the combination of **open source, provider flexibility, deterministic file/rule orchestration, agentic context retrieval, comment post-processing, and both diff and full-file modes**. It is not differentiated by replacing static analysis or by proving global architectural understanding. `[OFFICIAL]` for features; conclusion `[INFERENCE]`.

---

## Recommended Review Workflow

### End-to-end operating model

```text
During development
├── formatter, compiler/build, linter, type checker
├── focused unit/property/integration tests
├── secret, dependency, SAST, and IaC scans
├── coding agent executes/reproduces suspicious paths
└── author self-review against intent and failure semantics

Before merge
├── concise change description, risk, evidence, rollout/migration
├── OpenCodeReview `review` after deterministic jobs
├── author resolves/invalidates comments with evidence
├── human review of intent, system fit, tradeoffs, and residual risk
└── specialist review when security/data/reliability/platform risk warrants

Periodically or before release/ownership transfer
├── repository/runtime map
├── focused OpenCodeReview `scan` by subsystem/rule
├── deterministic codebase/security/dependency/IaC scans
├── production-readiness and recovery review
└── human consolidation into systemic findings and coverage statement

When risk warrants
├── threat model and security testing
├── load/profile/capacity investigation
├── fault injection and recovery exercise
├── migration rehearsal/data validation
└── architecture or compliance assessment
```

### Stage controls

| Stage | Trigger | Scope | Reviewer/tool | Expected findings | Minimum evidence | Blocking criteria |
|---|---|---|---|---|---|---|
| Local deterministic checks | Every meaningful edit/commit | Changed/build-relevant code | Build, format, lint, types, tests, secrets, SAST/SCA/IaC | Formalized failures/patterns | Tool output and reproduction | Build/test failure; confirmed secret; policy-defined high security issue |
| Author self-review | Before requesting review | Entire diff plus intent/tests/config | Author, optionally coding agent | Accidental files, weak naming/docs, missing cases, unnecessary complexity | Diff walkthrough and executed evidence | Author-defined readiness |
| OpenCodeReview diff review | Before human approval; after code stabilizes | PR/branch diff with targeted related context | `ocr review` | Candidate correctness, security, reliability, test, integration, material maintainability issues | Location + path + consequence; model comment must be verified | Only confirmed/probable P0/P1; project-tested high-confidence gates |
| Human PR review | Every material production change | Intent, diff, relevant surrounding system and tool evidence | Domain owner/general reviewer | Requirement mismatch, tradeoff, architecture fit, risk acceptance, ownership | Requirements, code path, tests/tool results, rollout | Material unresolved risk or insufficient evidence |
| Specialist review | Sensitive/high-blast-radius change | Relevant trust/state/runtime boundary | Security/SRE/data/platform specialist | Domain-specific failures and controls | Specialist evidence standard | Specialist-defined P0/P1/control failure |
| Focused repository scan | Scheduled, pre-release, inherited/agent-heavy subsystem | Selected paths including tests/config/docs | `ocr scan` + deterministic tools | Latent candidate defects and repeated patterns | Validate across callers/config/tests; group root cause | Usually creates work items; blocks release only for validated P0/P1 |
| Production-readiness review | New service/critical launch/material architecture change | Code + infra + operations + ownership/runtime evidence | Service owner, SRE/platform/security | Missing capacity, observability, recovery, rollout, dependency readiness | Runbooks, dashboards, alerts, load/failure/migration evidence | Inability to detect, contain, roll back, or recover material failure |
| Periodic audit | Risk-based cadence | Critical workflows and repository/system evidence | Human lead using tools/LLMs/specialists | Systemic correctness/security/reliability/maintainability gaps | Traceable systemic findings plus coverage limitations | Based on risk owner and release/compliance policy |

### Suggested configuration for an AI-agent-heavy repository

```text
On every PR:
  1. deterministic CI passes
  2. include task/acceptance criteria in review background
  3. run `ocr review` with component-specific rules
  4. explicitly include affected tests and migration/config files
  5. require author to classify each finding: fixed / invalid with evidence / accepted follow-up
  6. human approves intent and residual risk

Weekly or before release:
  1. choose one workflow or subsystem—not the whole repository by default
  2. run `ocr scan` with correctness/reliability/security rule
  3. run SAST/SCA/secrets/IaC/dead-code tools independently
  4. consolidate repeated symptoms into root causes
  5. manually trace the highest-impact candidates

Quarterly or after major topology change:
  human-led repository/production-readiness audit with runtime and operational evidence
```

### Feedback loop

Track the outcomes of AI comments:

| Metric | Purpose |
|---|---|
| Confirmed material findings / all emitted findings | Practical precision/trust |
| Confirmed findings by category, rule, model, component | Where the reviewer adds value |
| Dismissal reason: false premise / unreachable / safeguard / duplicate / preference | Tuning targets |
| Escaped defects that were in review scope | Recall proxy; silence is otherwise unmeasurable |
| Median author validation time | Workflow burden |
| Token/cost/latency per PR and per confirmed finding | Economic value |
| Human override/accepted-risk decisions | Governance and calibration |

Do not optimize comment count. Optimize **confirmed material risk found per unit of reviewer attention**. `[INFERENCE]`

---

## Practical Review Checklists

These are evidence prompts, not boxes to mark mechanically. Select the applicable subset.

### Diff review

- [ ] Read task/acceptance criteria; state the changed observable behaviour in one sentence.
- [ ] Identify entry points, changed state, external calls, schemas, config, and deployment effects.
- [ ] Trace one normal path and each newly introduced branch to a concrete outcome.
- [ ] Trace empty, missing, malformed, boundary, duplicate, timeout, and partial-failure cases that are reachable for this change.
- [ ] Inspect callers and downstream consumers for signature, schema, ordering, error, and lifecycle assumptions.
- [ ] Check authorization/resource ownership at the state-changing boundary, not only authentication middleware.
- [ ] Inspect tests for independent behavioural assertions and a regression case for each material bug fixed.
- [ ] Verify migration/config/feature-flag defaults and old/new-version compatibility where rollout is non-atomic.
- [ ] Search for an existing equivalent implementation before accepting a new helper/client/abstraction/config key.
- [ ] Report only findings with a path, consequence, safeguards checked, and confidence.

### Feature or branch review

- [ ] Map all commits/diffs to the feature’s acceptance criteria; identify temporary compatibility or scaffolding left behind.
- [ ] Trace the feature across API/UI/event entry → domain logic → state → async/external effects → user-visible result.
- [ ] Verify old and new paths during rollout, retry, rollback, and mixed-version deployment.
- [ ] Check cross-service/schema consumers and contract/version compatibility.
- [ ] Validate feature-flag ownership, default, cleanup condition, and observability by cohort/version.
- [ ] Inspect end-to-end, contract, failure, and migration tests—not only per-file unit tests.
- [ ] Confirm logs/metrics/job status expose success, failure, latency, retries, and stuck states.
- [ ] Remove or record owner/date for temporary code and unresolved risk.

### Repository audit

- [ ] Inventory deployable units, entry points, background processes, data stores, external systems, IaC, migrations, tests, generated/vendor exclusions.
- [ ] Select critical workflows by exposure, data value, irreversibility, frequency, and blast radius.
- [ ] Draw state transitions and trust boundaries for each selected workflow.
- [ ] Trace failure/recovery semantics across process and service boundaries.
- [ ] Run deterministic analyzers; deduplicate by root cause and validate reachability.
- [ ] Search duplicate domain concepts, clients, schemas, configuration, flags, and obsolete execution paths.
- [ ] Map critical risks to meaningful tests and identify untested boundaries/failures.
- [ ] Inspect deployment, permissions, secret flow, migrations, rollout/rollback, health, alerts, runbooks, and recovery.
- [ ] Produce a coverage statement: examined workflows/components, sampled areas, exclusions, unavailable evidence.
- [ ] Rank systemic findings; avoid converting every local smell into audit debt.

### Security-sensitive changes

- [ ] Enumerate actors, identities, resources, operations, and tenant boundaries.
- [ ] At every resource access, verify **who may act on which object under what state**, including indirect identifiers and batch endpoints.
- [ ] Trace untrusted data into SQL, shell, file paths, URLs, templates, deserializers, headers, logs, model prompts/tools, and cloud APIs.
- [ ] Verify validation occurs before side effects and that canonicalization/encoding matches the sink.
- [ ] Inspect secret acquisition, scope, storage, logging, rotation, and failure behaviour.
- [ ] Check cloud/service permissions against required actions/resources/conditions; reject wildcard expansion without evidence.
- [ ] Evaluate replay, brute force, enumeration, race, quota/cost, and business-logic abuse.
- [ ] Run SAST/SCA/secrets/IaC tooling and validate high findings; do not ask the LLM to replace them.
- [ ] Add a security specialist/threat model for new trust boundaries, auth protocols, sensitive data, public upload/webhook, or high-value actions.

### Background workers and queues

- [ ] Identify delivery semantics and exact acknowledgement point.
- [ ] Trace duplicate delivery before, during, and after each side effect; locate idempotency key/storage/constraint.
- [ ] Trace process crash after state commit but before ack, and after external effect but before local commit.
- [ ] Verify retry classification, timeout, bounded attempts, backoff/jitter, poison-message handling, and DLQ replay.
- [ ] Check leases/visibility timeouts against processing duration and renewal/cancellation behaviour.
- [ ] Verify transaction/outbox/compensation boundaries across DB and broker/external service.
- [ ] Inspect concurrency limits, ordering requirements, race controls, resource exhaustion, and shutdown draining.
- [ ] Ensure job status, attempt count, correlation ID, terminal reason, age, and DLQ depth are observable.
- [ ] Test duplicates, redelivery, timeout, partial external success, crash recovery, cancellation, and malformed messages.

### APIs

- [ ] Compare route, method, auth middleware, handler, domain policy, and data-store query; do not assume middleware establishes object ownership.
- [ ] Validate required/optional/null/empty distinctions, bounds, canonicalization, unknown fields, and content type.
- [ ] Check response/error contract, status codes, pagination, ordering, idempotency, rate/size limits, and version compatibility.
- [ ] Trace timeout/cancellation from client through downstream calls; avoid continuing expensive work after disconnect where inappropriate.
- [ ] Inspect sensitive data in response, error, logs, caches, and traces.
- [ ] Verify retry-safe semantics for POST/side-effecting operations or make non-retryability explicit.
- [ ] Test unauthorized actor, wrong tenant/object, malformed payload, boundary sizes, downstream failure, duplicate request, and mixed versions.

### Database and migration changes

- [ ] Identify old/new application versions and schema states that can coexist during rollout/rollback.
- [ ] Verify migration ordering: expand → backfill → switch reads/writes → enforce/contract where required.
- [ ] Check locks, table rewrites, index build mode, transaction duration, statement timeout, and production data volume.
- [ ] Validate defaults, nullability, constraints, foreign keys, uniqueness, precision/timezone/encoding, and existing dirty data.
- [ ] Trace dual-write/backfill idempotency, resume behaviour, progress/verification, and rollback feasibility.
- [ ] Check transaction boundaries and lost-update/race/isolation assumptions.
- [ ] Require data validation counts/checksums and recovery/backup plan for irreversible changes.
- [ ] Test migration against production-like schema/data scale and old/new binaries where risk warrants.

### Cloud and infrastructure changes

- [ ] Diff effective resources/permissions/network exposure, not only template syntax.
- [ ] Trace identity → role/policy → resource/action/condition; inspect cross-account and wildcard access.
- [ ] Check public ingress/egress, security groups/firewalls, private endpoints, DNS/TLS, and metadata/service-token exposure.
- [ ] Verify secret references, encryption keys, log destinations, retention, backups, deletion protection, and data residency.
- [ ] Inspect health/readiness/startup probes, autoscaling signals/limits, disruption behaviour, quotas, and regional/AZ assumptions.
- [ ] Validate rollout strategy, immutable artifact/version pinning, drift, rollback, and stateful-resource replacement.
- [ ] Run IaC policy/security scanners and compare with the deployed plan/state where available.
- [ ] Confirm metrics/alerts/runbooks identify resource saturation, dependency failure, permission denial, and failed deployment.

### AI and data-pipeline components

- [ ] Define input/output schema, provenance, ownership, quality constraints, and version compatibility for every stage.
- [ ] Trace missing/late/duplicate/out-of-order data, partial partitions, schema drift, reprocessing, and backfill.
- [ ] Verify idempotent writes, checkpointing, atomic publish, lineage, and recovery after stage failure.
- [ ] Separate training/evaluation/inference data and prevent leakage; document split and temporal assumptions.
- [ ] Check model/artifact/data version pinning, reproducibility, rollback, and cache invalidation.
- [ ] For LLM/agent systems, trace untrusted content into prompts/tools; constrain tool authority, validate structured output, and handle refusal/timeout/malformed output.
- [ ] Validate evaluation metrics against the actual task, slices, baselines, thresholds, and failure costs—not aggregate score alone.
- [ ] Inspect fallback behaviour, human escalation, content/safety/privacy controls, token/cost/rate limits, and provider retention.
- [ ] Ensure per-stage counts, lag, latency, error/drop/retry rates, data-quality metrics, model/version, and correlation IDs are observable.
- [ ] Test malformed data, provider failure, model drift, prompt injection/tool abuse, replay, duplicate processing, and recovery.

---

## Example Review and Audit Reports

The examples use invented files and systems; they demonstrate evidence quality, not claims about a real repository.

### 1. High-quality diff review

```text
P1 · Reliability / Data integrity

Problem
The API can create two billable render jobs when the queue publish succeeds but
its acknowledgement is lost and the client retries.

Evidence
- `api/routes/render.ts:84-111` inserts a new job before publishing.
- `api/routes/render.ts:116-122` returns 503 on every publish exception.
- The request's `Idempotency-Key` is logged but is not persisted or constrained.
- `workers/render.ts:41-70` accepts every message and performs the external render.
- Search found no unique request key, transactional outbox, producer deduplication,
  or consumer-side duplicate guard.
- Existing test `render_route.test.ts:130-178` covers broker rejection before
  acceptance, not an ambiguous timeout after acceptance.

Failure or maintenance consequence
A broker may accept the message and the producer may time out. The client receives
503 and retries, creating another DB row/message. Both workers can incur provider
cost and publish duplicate customer output.

Confidence
High. This follows the documented at-least-once/ambiguous-failure path and no
repository safeguard was found.

Recommended direction
Persist and enforce a client/request idempotency key, or atomically publish through
an outbox and make the consumer idempotent. Add a test that simulates accepted
publish + lost acknowledgement + retry.
```

Why it is high quality: exact path, concrete failure timing, caller behaviour, safeguards searched, test gap, consequence, and remediation invariant.

### 2. High-quality repository audit finding

```text
P1 · Security / Tenant isolation

Problem
Tenant ownership is enforced inconsistently across three document download paths;
the legacy worker-generated URL path can expose another tenant's document to any
authenticated user who obtains the object UUID.

Evidence
- REST download `documents/api.py:210-248` filters `Document.tenant_id` correctly.
- GraphQL resolver `documents/graphql.py:91-118` calls the same scoped repository.
- Legacy endpoint `exports/routes.py:55-82` loads `Document` by UUID only, then
  signs `blob_key` with the service account.
- Route registration applies authentication but no tenant policy middleware.
- UUIDs appear in export-completion emails and structured logs.
- Tests cover unauthenticated access but no cross-tenant authenticated actor.
- Deployment IAM permits the service to sign every object under the shared bucket.

Failure or maintenance consequence
A UUID disclosed through logs, email forwarding, support tooling, or another bug
can be used by a different authenticated tenant to obtain a valid signed URL.
The shared signer broadens exposure to all tenant objects.

Confidence
High for the code path; medium for practical UUID acquisition frequency.

Recommended direction
Route every download through one tenant-scoped repository/policy function, add a
cross-tenant regression test, reduce signer scope where feasible, and review UUID
exposure in logs/emails.
```

Why it is an audit finding: it compares parallel implementations and a system-wide trust boundary rather than commenting on one line in isolation.

### 3. Noisy or low-value review

```text
LOW · Maintainability
- Consider renaming `data` to something more descriptive.
- Consider adding a helper for this 8-line block.
- Consider documenting every parameter.
- Consider replacing the if/else with a strategy pattern.
- This function may be slow for very large inputs.
- Add more error handling.
```

Problems: no requirement, scale, reachable failure, duplicate implementation search, caller evidence, or material consequence; speculative abstraction adds complexity; deterministic style checks are being repeated.

### 4. Finding that should be suppressed

```text
Candidate: “The list access at `handlers.py:73` may raise IndexError when empty.”

Suppress after validation:
- The only caller passes the result of `parse_required_segments()`.
- That function either returns at least one segment or raises `InvalidRequest`.
- Property tests cover arbitrary empty/whitespace input.
- No dynamic or alternate caller was found.
```

The suspicious local pattern is protected by a verified precondition. Reporting it would transfer investigation cost without risk reduction.

### 5. Finding that should be escalated for human verification

```text
P1 candidate · Authorization / Business policy

Problem
`approve_refund()` allows the order creator to approve a refund below $500.

Evidence
- Code path is reachable and intentionally encoded in `refund_policy.ts:44-61`.
- Existing tests assert creator approval at $499 and second-party approval at $500.
- Product requirements available in the repository only say “large refunds require
  dual approval” and do not define the threshold or whether self-approval is allowed.

Consequence
If policy forbids self-approval, this is a financial-control bypass. If the $500
rule is approved policy, the code is correct.

Confidence
High in implementation behaviour; low in whether it violates policy.

Recommended direction
Escalate to the finance/control owner. Do not label the implementation a defect
until the authoritative approval policy is confirmed. Add the policy reference to
code/tests once resolved.
```

---

## Final Practical Framework

### What belongs where

| Question | Default answer |
|---|---|
| What should **always** be reviewed? | Intended behaviour; reachable correctness/regression paths; state changes; trust/authorization boundaries touched; failure propagation; meaningful tests; caller/consumer compatibility |
| What should **usually** be reviewed? | Reliability semantics, data integrity, API/schema/config/deployment effects, operability for new failure modes, material maintainability/change amplification |
| What is risk-triggered? | Dedicated security, performance/load, concurrency, migration/data, architecture, privacy, production-readiness, or compliance assessment |
| What goes to deterministic tools? | Build/syntax, formatting, types, known lint/SAST/IaC/secret/dependency patterns, executable tests, coverage collection, dead-code/complexity metrics |
| What requires human judgment? | Requirements, product/business policy, architecture tradeoffs, risk acceptance, ownership, operational tolerance, specialist assurance, final approval |
| What belongs in diff review? | Risks introduced or exposed by the change, affected callers/contracts/tests/config/rollout, changed architecture consequences |
| What belongs in repository audit? | Runtime/workflow/state/trust map, systemic duplicated responsibilities, accumulated gaps, operations/deployment/recovery, test strategy, cross-cutting architecture/security/reliability |
| How should findings be evidenced? | Exact location + execution path + trigger + consequence + safeguards/config/tests checked + confidence + coverage limitation |
| How should findings be prioritized? | Impact, reachability, likelihood, blast radius, safeguards, reversibility; then independently state confidence/evidence class |
| Where does OpenCodeReview fit? | Contextual LLM screening after deterministic checks: `review` for every material change; focused `scan` for latent candidates before human audit/release |
| What remains after adopting it? | Tests/execution, deterministic analyzers, runtime evidence, requirements, threat modelling, architecture/PRR, cross-repo context, specialist review, accountable human decision |

### Compact decision table

| Situation | First action | OpenCodeReview role | Human completion criterion |
|---|---|---|---|
| Small ordinary PR | Deterministic CI + author self-review | `ocr review` for high-signal candidate findings | Intent and material paths understood; no unresolved P0/P1 |
| Large feature branch | Decompose and map end-to-end workflow | Review constituent diffs; final branch review with requirement context | Cross-component contracts, rollout, failure, tests, and ownership verified |
| Security-sensitive change | Threat/actor/resource map + security tools | Contextual auth/business-logic candidate review | Security specialist validates policy, exploitability, controls, and residual risk |
| Queue/worker change | Duplicate/partial-failure/crash trace + failure tests | Reliability-specific diff rules | Idempotency, ack/transaction/retry/recovery semantics are executable and observable |
| Database migration | Migration rehearsal and compatibility plan | Review migration/app diffs for candidate gaps | Old/new coexistence, data validation, lock/rollback/recovery evidence accepted |
| Inherited or agent-heavy subsystem | Repository/runtime map + deterministic scans | Focused `ocr scan`, explicitly include tests/config | Highest-risk workflows and systemic findings manually traced |
| New service/release | Production-readiness review | Supplement source/config inspection | Capacity, dependencies, telemetry, alerts, rollout, rollback, runbooks, recovery proven |
| “Clean” AI review | Inspect coverage and tool/test evidence | Treat as no candidates found, not proof | Human verifies material risk areas and acknowledges unavailable evidence |

### Minimal reusable finding schema

```yaml
priority: P0 | P1 | P2 | P3
category: correctness | security | reliability | data | testing |
          architecture | maintainability | operability | performance | other
status: confirmed | probable | design-concern | question
confidence: high | medium | low
location:
  - file: path/to/file
    lines: 10-25
trigger: concrete input/state/failure/actor
path: entry -> branch -> state/external effect
consequence: observable impact
safeguards_checked:
  - validation / transaction / policy / test / config / monitoring
coverage_limitations:
  - unavailable runtime/config/repository evidence
recommended_direction: invariant or control to restore
```

### Core doctrine

```text
1. Review behaviour, not syntax already checked by machines.
2. Start from intent and risk; retrieve only relevant context.
3. Trace concrete success, invalid-input, state, trust, and failure paths.
4. Treat tests and tool output as evidence, not substitutes for judgment.
5. Report fewer findings, each with reachability and consequence.
6. Separate priority from confidence and from design preference.
7. Use diff review continuously; use audits selectively and systemically.
8. Use OpenCodeReview as a repeatable second set of eyes—not an assurance boundary.
9. Escalate specialized risk to specialized humans and executable analysis.
10. State what was not examined; absence of findings is not proof of absence.
```

---

## Unresolved

1. **Independent OpenCodeReview replication:** no independent publication was found reproducing the project’s AACR-Bench results with the same models/configuration.
2. **`ocr scan` audit validity:** no published evaluation was found measuring architecture, operability, systemic reliability, or production-readiness recall for scan mode.
3. **Rule adherence:** the project acknowledges probabilistic adherence, but no per-rule compliance benchmark quantifies which rules/models fail and under what context load.
4. **Post-processing effectiveness:** no independent ablation was found for planning, reflection, line relocation, suggestion validation, or semantic deduplication.
5. **Internal repositories:** public OSS benchmarks do not establish performance on private monorepos, infrastructure-heavy repositories, data/ML pipelines, or agent-generated code at scale.
6. **Severity calibration:** available benchmark metrics focus on issue matching; they do not establish reliable P0–P3 calibration or business impact estimation.
7. **Human workflow outcomes:** local precision, author validation time, trust, ignored comments, escaped defects, and cost per confirmed issue must be measured in the adopting team.
8. **Context contradiction:** AACR-Bench finds heterogeneous context effects, while SWE-PRBench reports consistent degradation with added context. The optimal retrieval strategy likely depends on model, representation, and issue type, but is not settled.
9. **Provider privacy:** OpenCodeReview can route to custom endpoints, but actual retention, training use, residency, and compliance depend on provider/deployment terms outside the project.
10. **Prompt-injection resistance:** repository text and untrusted pull requests can contain adversarial instructions; no project-specific security evaluation of agent-tool prompt injection was found.
11. **Default test exclusion impact:** the practical effect of default test-file exclusions on test-gap findings and benchmark performance is not published.
12. **Cross-repository contracts:** no built-in evidence was found for exhaustive reasoning across separately hosted services, schemas, deployed versions, or cloud state.

---

## References

Primary and official sources are preferred. Product documentation is authoritative for described features, not independent evidence of effectiveness.

[^ocr-readme]: Alibaba, **OpenCodeReview README and documentation**. https://github.com/alibaba/open-code-review
[^ocr-releases]: Alibaba, **OpenCodeReview releases**. https://github.com/alibaba/open-code-review/releases
[^ocr-source-review]: Alibaba, OpenCodeReview source, **diff review agent** (`internal/agent/agent.go`) and tools. https://github.com/alibaba/open-code-review/blob/main/internal/agent/agent.go and https://github.com/alibaba/open-code-review/tree/main/internal/tool
[^ocr-source-scan]: Alibaba, OpenCodeReview source, **repository scan agent** (`internal/scan/agent.go`). https://github.com/alibaba/open-code-review/blob/main/internal/scan/agent.go
[^ocr-source-batch]: Alibaba, OpenCodeReview source, **scan batching** (`internal/scan/batch.go`). https://github.com/alibaba/open-code-review/blob/main/internal/scan/batch.go
[^ocr-assurance]: Alibaba, **OpenCodeReview Assurance Case**. https://github.com/alibaba/open-code-review/blob/main/ASSURANCE_CASE.md
[^ocr-rules]: OpenCodeReview maintainer discussion on rule adherence and system rules. https://github.com/alibaba/open-code-review/discussions/243
[^aacr]: Zhang et al., **AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context** (2026), paper and data. https://arxiv.org/abs/2601.19494 and https://github.com/alibaba/aacr-bench
[^swe-prbench]: Kumar, **SWE-PRBench: Benchmarking AI Code Review Quality Against Pull Request Feedback** (2026 preprint). https://arxiv.org/abs/2603.26130
[^contextcrbench]: Hu et al., **Benchmarking LLMs for Fine-Grained Code Review with ContextCRBench** (2025 preprint). https://arxiv.org/abs/2511.07017
[^llm-hallucination]: Liu, Lin, and Thongtanunam, **Hallucinations in Code Change to Natural Language Generation: Prevalence and Evaluation of Detection Metrics** (2025 preprint). https://arxiv.org/abs/2508.08661
[^llm-field]: Aðalsteinsson et al., **Rethinking Code Review Workflows with LLM Assistance: An Empirical Study** (ESEM 2025 industrial track). https://arxiv.org/abs/2505.16339
[^bacchelli]: Bacchelli and Bird, **Expectations, Outcomes, and Challenges of Modern Code Review** (ICSE 2013). https://www.microsoft.com/en-us/research/publication/expectations-outcomes-challenges-modern-code-review/
[^review-quality]: McIntosh et al., **The Impact of Code Review Coverage and Code Review Participation on Software Quality** (Empirical Software Engineering). https://doi.org/10.1007/s10664-015-9366-8
[^google-standard]: Google, **The Standard of Code Review**. https://google.github.io/eng-practices/review/reviewer/standard.html
[^google-looking]: Google, **What to Look For in a Code Review**. https://google.github.io/eng-practices/review/reviewer/looking-for.html
[^google-speed]: Google, **Speed of Code Reviews**. https://google.github.io/eng-practices/review/reviewer/speed.html
[^google-small]: Google, **Small CLs**. https://google.github.io/eng-practices/review/developer/small-cls.html
[^security-mcr]: Braz and Bacchelli, **Software Security during Modern Code Review: The Developer’s Perspective** (ESEC/FSE 2022). https://arxiv.org/abs/2208.04261
[^security-missed]: Paul, Turzo, and Bosu, **Why Security Defects Go Unnoticed during Code Reviews? A Case-Control Study of the Chromium OS Project** (2021). https://arxiv.org/abs/2102.06909
[^nist-ssdf]: NIST, **Secure Software Development Framework (SSDF), SP 800-218**. https://csrc.nist.gov/pubs/sp/800/218/final
[^owasp-asvs]: OWASP, **Application Security Verification Standard** and **Code Review Guide**. https://owasp.org/www-project-application-security-verification-standard/ and https://owasp.org/www-project-code-review-guide/
[^aws-idempotency]: AWS Builders’ Library, **Making retries safe with idempotent APIs**. https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
[^aws-retries]: AWS Builders’ Library, **Timeouts, retries, and backoff with jitter**. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
[^k8s-probes]: Kubernetes documentation, **Configure Liveness, Readiness and Startup Probes**. https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
[^sre-prr]: Google SRE, **Launch Coordination / Production Readiness Review guidance and launch checklist**. https://sre.google/workbook/launch-checklist/
[^ai-security]: Pearce et al., **Asleep at the Keyboard? Assessing the Security of GitHub Copilot’s Code Contributions**. https://arxiv.org/abs/2108.09293
[^ai-confidence]: Perry et al., **Do Users Write More Insecure Code with AI Assistants?** https://arxiv.org/abs/2211.03622
[^package-hallucination]: Spracklen et al., **We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs**. https://arxiv.org/abs/2406.10279
[^copilot-review]: GitHub, **Using GitHub Copilot code review**. https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review
[^claude-review]: Anthropic, **Claude Code Review documentation**. https://docs.anthropic.com/en/docs/claude-code/code-review
[^codex-review]: OpenAI, **Codex code review in GitHub** and CLI review documentation. https://developers.openai.com/codex/third-party/github and https://developers.openai.com/codex/cli
[^coderabbit]: CodeRabbit, **Code Review and path-based review instructions**. https://docs.coderabbit.ai/guide/code-review and https://docs.coderabbit.ai/configuration/path-instructions
[^qodo]: Qodo, **PR review documentation**. https://docs.qodo.ai/qodo-documentation/code-review
[^sonarqube]: Sonar, **SonarQube Server documentation**. https://docs.sonarsource.com/sonarqube-server/
[^semgrep]: Semgrep, **Semgrep documentation**. https://semgrep.dev/docs/
[^codeql]: GitHub/CodeQL, **About code scanning with CodeQL** and **data-flow analysis**. https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql and https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/
[^snyk]: Snyk, **Scan with Snyk documentation**. https://docs.snyk.io/scan-with-snyk
