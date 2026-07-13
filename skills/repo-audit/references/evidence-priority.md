# Evidence, Classes, and Priority

## Proof standards

### Defect and risk findings

`confirmed` and `probable` require:

```text
trigger → reachable path → consequence → safeguards checked
```

Missing trigger, path, consequence, or materiality: drop it. One bounded
external assumption may remain when explicitly stated — the finding is
then `probable`. Broader uncertainty belongs in Investigate.

### Design concerns

A `design-concern` requires:

```text
construct → demonstrated change/operation path → material engineering cost
→ existing justification or safeguards checked
```

The cost must be evidenced through current divergence, repeated change
amplification, operational weakness, unclear ownership, or another
observable maintenance burden. A merely unusual design or preferred
alternative is not reportable.

### Safeguards to check

Before reporting anything: validation at other boundaries, caller
guarantees, database constraints, transactions, framework behaviour,
feature flags, existing tests, monitoring/alerts, deployment
configuration.

## Classes

- **confirmed:** repository evidence establishes the trigger, reachable
  path, missing or ineffective safeguard, and consequence.
- **probable:** the path and consequence are strongly supported, but one
  explicit runtime, configuration, or deployment assumption remains.
  State the assumption inside the finding.
- **design-concern:** evidence establishes systemic change cost,
  divergence, or operational weakness, but not a concrete current
  failure.
- **investigate:** evidence is insufficient to classify; state the exact
  question and what would resolve it. Lives only in the Investigate
  section, never in Findings.

## Priority

```text
P0  Active or imminent catastrophic security, data, or availability failure.
P1  Reachable severe production, security, or data-integrity risk.
P2  Material defect or systemic weakness under plausible conditions.
P3  Bounded maintainability, operability, or simplification concern.
```

Constraints:

- P0 requires `confirmed · high` evidence of active or imminent
  catastrophic impact.
- A `design-concern` cannot be P0 or P1.

Rank by impact × reachability × frequency × breadth, discounted by
safeguards, reversibility, and uncertainty. Judgment, not arithmetic —
no false-precision scores.

## Confidence

```text
high    Evidence directly establishes nearly all relevant facts.
medium  Evidence is strong but one bounded assumption remains.
low     Do not place in Findings; move to Investigate.
```

`probable` normally carries medium confidence because its bounded
assumption remains unresolved. Priority and confidence never collapse
into one label: a catastrophic but speculative concern and a modest
confirmed bug need different handling.

## Conflicting intent evidence

Do not assume documentation, tests, configuration, or current code is
automatically authoritative. Default weight, strongest first:

```text
External contract / schema / accepted requirement
        ↓
Production or deployment configuration
        ↓
Integration and behavioural tests
        ↓
Implementation and call sites
        ↓
Unit tests
        ↓
Comments and general documentation
```

The hierarchy is a default, not absolute. When sources conflict:

1. identify the externally observable contract or production boundary;
2. inspect deployed configuration, schemas, callers, migrations, and
   behavioural tests;
3. use git history only when it helps explain the contradiction;
4. record unresolved contradictions explicitly — in Investigate or
   Coverage.

Do not silently choose the source that best supports a candidate
finding.

Git history: use only to resolve intent, removed safeguards, ownership,
duplicate implementations, or a specific candidate finding. Never an
unfocused history review.

## Stopping rules

Stop investigating a candidate when:

- a required link in the failure path is disproved;
- an existing safeguard fully blocks the scenario;
- the consequence is immaterial;
- the issue is owned completely by a deterministic tool;
- resolving it requires unavailable runtime evidence and it has been
  moved to Investigate;
- additional repository search no longer changes confidence or priority.
