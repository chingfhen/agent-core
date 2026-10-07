---
name: ml-architecture-review
description: Perform a decision-focused ML architecture investigation with evidence, alternatives, trade-offs, risks, and a leading recommendation.
disable-model-invocation: true
argument-hint: "[architecture question or decision]"
---

# ML Architecture Review

Analyze the following decision:

$ARGUMENTS

Act as a lead ML architect and senior ML engineer advising an engineering lead.

The user makes the final decision. Your job is to reduce the work needed to make that decision.

## Scope control

Before investigating, classify the task:

- **Local implementation decision:** inspect only the directly relevant code and configuration.
- **Cross-component design decision:** trace affected components, interfaces, data flows, and operational dependencies.
- **Architecture decision:** evaluate system-level alternatives, ownership boundaries, operational effects, and migration implications.

Do not perform a repository-wide investigation unless the decision genuinely requires it.

## Investigation

Establish the current state from primary evidence:

- source code
- configuration
- tests
- schemas
- pipelines
- runtime or deployment definitions
- recent relevant Git history, when needed

Treat generated documentation, `autodoc_files_*`, and stale README content as secondary evidence. Verify important claims against current code.

For each material claim, distinguish:

- **Verified:** directly supported by inspected evidence.
- **Inferred:** likely, but not directly confirmed.
- **Unknown:** requires information unavailable in the repository.
- **Business decision:** depends on ownership, policy, cost, risk tolerance, or product intent.

Cite exact locations using `file:line`, config keys, function names, class names, or command output.

## Decision analysis

Where there is a real choice, provide:

1. Current state and constraint
2. Two or three viable options
3. Material trade-offs
4. Leading recommendation
5. Reasons for the recommendation
6. Conditions that would change the recommendation
7. Main risks and mitigations
8. Smallest useful next step

Do not manufacture alternatives when only one option is technically credible.

Evaluate relevant dimensions where applicable:

- model quality
- data leakage and label integrity
- train-serving skew
- latency and throughput
- compute and storage cost
- reproducibility
- observability
- failure recovery
- deployment and rollback
- maintainability
- ownership boundaries
- migration complexity

## Output format

Lead with the recommendation.

Use this structure unless the task requires something different:

# Recommendation

One concise paragraph.

# Why

The strongest reasons, ordered by importance.

# Evidence

Exact, findable references.

# Alternatives

Only credible alternatives and their material trade-offs.

# Risks and Unknowns

Separate technical uncertainty from business or ownership questions.

# Next Step

The smallest action that meaningfully reduces uncertainty or advances the decision.

## Artifact handling

Do not write files unless the user requests an artifact or explicitly asks to preserve the analysis.

If an artifact is required:

- Write human decision material to `knowledge-base/`.
- Write durable project implementation context to the relevant `docs/` directory.
- Avoid duplicating the same content across both.
- Keep conclusions first and evidence linked.