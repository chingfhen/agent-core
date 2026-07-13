[Research brief: Investigate how software code reviews and repository audits should be conducted in practice: what should be examined, how concerns should be investigated, how findings should be evidenced and prioritized, and which activities are best handled by deterministic tools, LLM-based reviewers, or human engineers. Use Alibaba OpenCodeReview as the primary case study to understand how a purpose-built LLM review system implements diff review and repository-wide scanning, but do not limit the research to the tool or attempt to design a new review skill. The intended audience is a software engineer working extensively with AI coding agents on small-to-medium production systems, particularly Python, TypeScript, APIs, background workers, cloud infrastructure, data pipelines, and AI applications. The research should produce a practical review and audit methodology and an informed assessment of where OpenCodeReview fits within it.]

Research this and produce a dense markdown artifact.

Begin with frontmatter:

---

title: Practical Software Review and Repository Auditing
scope: What should be reviewed or audited, how reviews should be conducted, and where OpenCodeReview fits
research_type: Understanding, Practical Guide, and Tool Evaluation
audience: Human software engineer
generated_on: 2026-07-13
sources:

* https://github.com/alibaba/open-code-review

---

Suggested sections (revise, remove, merge, or add sections based on what you actually find):

## Executive Summary

Provide a concise practical answer to:

* What is the purpose of code review?
* What is the purpose of a repository audit?
* What are the highest-value concerns in each?
* How should reviews and audits differ?
* What role should OpenCodeReview play?
* What should still be handled by other tools or humans?

Prefer clear conclusions over a long summary of the research process.

## Review and Audit Terminology

Define and distinguish:

* Line-level review
* Pull-request or diff review
* Feature or branch review
* Repository-wide audit
* Architecture review
* Security review
* Performance review
* Production-readiness review
* Compliance audit
* Automated static analysis

For each activity, state:

| Activity | Primary question | Scope | Typical trigger | Expected output |
| -------- | ---------------- | ----- | --------------- | --------------- |

Clarify where these terms overlap and where they should remain separate.

## Objectives of Code Review

Investigate the established purposes of reviewing a proposed change.

Potential objectives include:

* Preventing defects and regressions
* Verifying intended behaviour
* Identifying security risks introduced by the change
* Evaluating failure handling and edge cases
* Checking integration with existing components
* Ensuring tests protect meaningful behaviour
* Controlling unnecessary complexity
* Maintaining consistency and comprehensibility
* Sharing knowledge and preserving system ownership

Determine which objectives provide the highest engineering value and which commonly produce low-value review noise.

## Objectives of Repository Auditing

Investigate what repository-wide audits should examine that diff reviews frequently miss.

Potential objectives include:

* Systemic correctness risks
* Architectural coherence
* Responsibility and module boundaries
* Security and trust boundaries
* State management and data integrity
* Reliability and failure semantics
* Accumulated technical debt
* Duplicate or conflicting implementations
* Dead code, unused configuration, and dependency bloat
* Test-strategy gaps
* Operability and diagnosability
* Production readiness
* Documentation drift

Clarify whether these concerns belong in one general audit or in separate specialist audits.

## Review Dimensions

Develop a ranked taxonomy of possible review dimensions.

Evaluate at least:

* Correctness
* Security
* Reliability
* Maintainability
* Architecture
* Testing
* Operability
* Performance
* Dependencies
* Documentation
* API design
* Data integrity
* Concurrency
* YAGNI and unnecessary complexity

For each dimension, provide:

| Dimension | What is examined | Example high-value finding | Review or audit | Importance | Best reviewer |
| --------- | ---------------- | -------------------------- | --------------- | ---------: | ------------- |

The goal is not to recommend reviewing everything equally. Identify the small set of concerns that should form the default review and audit core.

## Correctness Review

Investigate how reviewers should reason about behaviour rather than merely inspect syntax.

Cover:

* Intended behaviour and requirements
* Preconditions and postconditions
* Invariants
* Boundary conditions
* Empty, missing, malformed, and unexpected input
* State transitions
* Partial completion
* Error propagation
* Cross-module assumptions
* Schema and interface mismatches
* Temporal assumptions
* Concurrency behaviour
* Regression risks

Explain how a reviewer can trace a concrete failure path before reporting a bug.

## Security Review

Determine which security concerns should be part of normal review and which require a dedicated security assessment.

Distinguish:

* Pattern-based vulnerabilities detectable by SAST
* Authentication
* Authorization
* Resource ownership
* Tenant isolation
* Input validation
* Injection
* Unsafe file, URL, shell, SQL, template, or deserialization handling
* Secret handling
* Sensitive-data exposure
* Logging of confidential information
* Cloud permissions
* External-service trust
* Dependency and supply-chain risks
* Business-logic abuse

For each concern, state whether it is best handled by:

* Deterministic tooling
* Contextual LLM review
* Human security review
* A combination

Do not treat an LLM review as a replacement for security testing or professional security assessment.

## Reliability and Failure Semantics

Investigate how reviewers should examine behaviour when dependencies, processes, networks, or machines fail.

Cover:

* Timeouts
* Retries and backoff
* Idempotency
* Duplicate delivery
* Partial failure
* Transaction boundaries
* Rollback and compensation
* Queue acknowledgement
* Dead-letter handling
* Resource exhaustion
* Cancellation
* Graceful degradation
* Recovery after crashes
* External-service failure
* Startup and shutdown behaviour

Provide concrete questions and tracing methods rather than generic reliability advice.

## Architecture and Maintainability

Investigate how reviewers evaluate whether code is easy to understand, change, test, and operate.

Cover:

* Responsibility placement
* Module and service boundaries
* Coupling and cohesion
* Dependency direction
* Shared mutable state
* Hidden global behaviour
* Business logic mixed with infrastructure
* Duplicate domain concepts
* Abstractions and extension points
* Wrappers, factories, adapters, and interfaces
* Configuration proliferation
* Change amplification
* Cross-cutting behaviour
* Repository organisation

Distinguish genuine architectural problems from subjective preferences.

## YAGNI and Complexity Review

Investigate when simplification is worth reporting.

Cover:

* Dead code
* Speculative features
* Single-implementation interfaces
* Single-product factories
* Delegating wrappers
* Unused configuration
* Unused feature flags
* Hand-rolled standard-library functionality
* Dependencies used for trivial behaviour
* Multiple layers with one caller
* Re-export-only files
* Duplicate implementations

Determine:

* When complexity becomes a material engineering problem
* When simplification should be omitted as low priority
* Whether YAGNI belongs in normal review, repository audit, or a dedicated pass
* How reviewers can avoid encouraging premature simplification

## Testing Review

Investigate how reviewers should assess tests without relying on raw coverage percentages.

Cover:

* Protection of important behaviour
* Failure-path tests
* Boundary tests
* State-transition tests
* Integration and contract tests
* Mock-heavy tests
* Tests coupled to implementation details
* Nondeterministic tests
* Unrealistic fixtures
* Tests that reproduce the implementation
* Missing regression tests
* Tests for retries, concurrency, and partial failures

Provide criteria for identifying a meaningful testing gap.

## Operability and Production Readiness

Investigate concerns that affect running and debugging the system in production.

Cover:

* Logs
* Metrics
* Tracing
* Correlation and job identifiers
* Health and readiness checks
* Error visibility
* Background-job status
* Configuration validation
* Startup failures
* Deployment safety
* Rollback behaviour
* Database migration safety
* Feature rollout
* Alerts
* Runbooks
* Data recovery
* Observability of external dependencies

Clarify which concerns should be reviewed continuously and which belong in periodic readiness audits.

## How Reviews Should Be Conducted

Develop a practical step-by-step methodology.

Potential stages:

1. Establish the intended behaviour and scope
2. Identify entry points and affected components
3. Map callers, dependencies, and downstream effects
4. Trace the primary success path
5. Trace invalid-input and failure paths
6. Identify stateful operations and trust boundaries
7. Inspect related tests
8. Inspect configuration and deployment assumptions
9. Search for parallel or conflicting implementations
10. Validate every candidate finding
11. Rank and report only material findings

For each stage, describe:

* What the reviewer is trying to learn
* What repository evidence to inspect
* Common mistakes
* When to stop investigating

## Repository Audit Methodology

Develop a separate practical methodology for whole-repository auditing.

Consider:

1. Map the repository
2. Identify runtime entry points
3. Identify major workflows
4. Identify data stores and state transitions
5. Identify trust boundaries and external systems
6. Identify background processes
7. Examine deployment and infrastructure
8. Examine critical tests
9. Search for duplicate responsibilities and obsolete paths
10. Review operational visibility
11. Validate and rank systemic findings

Address:

* Large repositories
* Monorepos
* Multiple services
* Generated code
* Vendored code
* Missing documentation
* Partial repository access
* Token and context constraints

## Evidence Standards for Findings

Define the minimum evidence required before reporting an issue.

Evaluate requirements such as:

* Exact file and line references
* Relevant caller or execution path
* Concrete failure scenario
* Observable consequence
* Configuration usage checked
* Tests inspected
* Alternative implementation searched
* Framework behaviour verified
* Confidence level
* Suggested remediation direction

Distinguish:

* Confirmed issue
* Probable issue
* Design concern
* Investigation question
* Subjective preference

Recommend which categories should appear in a final review report.

## Prioritization and Noise Control

Research how findings should be ranked and filtered.

Evaluate factors such as:

* Impact
* Likelihood
* Reachability
* Frequency
* Breadth
* Confidence
* Evidence strength
* Remediation effort
* Reversibility
* Existing safeguards

Determine:

* Whether P0–P3, severity labels, confidence labels, or a simple ranking is most useful
* How many findings a review should normally return
* Whether weak findings should be omitted entirely
* How duplicate findings should be combined
* How to prevent style comments from overwhelming correctness issues
* How to report a healthy change or repository

Include a recommended prioritization model.

## Division of Labour Between Tools, LLMs, and Humans

Map review concerns to the most suitable reviewer.

Include:

* Compiler
* Formatter
* Linter
* Type checker
* Unit and integration tests
* Property-based testing
* SAST
* Secret scanner
* Dependency scanner
* Infrastructure scanner
* Dead-code detector
* Complexity tools
* LLM reviewer
* Human engineer
* Security specialist
* SRE or platform engineer

Produce a table:

| Concern | Deterministic tool | LLM value | Human value | Recommended owner |
| ------- | ------------------ | --------- | ----------- | ----------------- |

Identify checks that an LLM should not duplicate unless interpreting or validating the deterministic result.

## Human Code Review Practices

Investigate established practices used by experienced engineers and engineering organisations.

Cover:

* Review size
* Review latency
* Author-provided context
* Review checklists
* Reviewer ownership
* Multiple reviewers
* Specialist reviewers
* Blocking versus non-blocking comments
* Discussion and disagreement
* Approval standards
* Follow-up verification
* Knowledge sharing
* Review fatigue

Separate evidence-backed practices from organisational preferences.

## LLM-Based Code Review

Investigate current evidence on LLM reviewers.

Cover:

* Defect categories they identify well
* Defect categories they commonly miss
* False-positive behaviour
* Hallucinated findings
* Repository-context limitations
* Call-chain and data-flow reasoning
* Comment positioning
* Duplicate comments
* Prompt sensitivity
* Model sensitivity
* Review consistency
* Token and cost constraints
* Multi-agent and tool-assisted review
* Comparison with static tools
* Comparison with human review

Prioritize research papers, benchmarks, documented experiments, and detailed engineering reports.

Clearly separate:

* Demonstrated capabilities
* Vendor claims
* Practitioner observations
* Reasonable inference

## AI-Generated Code as a Review Target

Investigate whether AI-generated code creates distinctive review risks.

Potential patterns:

* Happy-path-only implementations
* Generic exception handling
* Incorrect framework assumptions
* Duplicate implementations
* Inconsistent conventions
* Excess dependencies
* Placeholder logic
* Tests that mirror implementation
* Missing authorization
* Missing idempotency
* Local correctness with broken system behaviour
* Configuration proliferation
* Unnecessary abstractions
* Compatibility layers with no real requirement
* Silent fallback behaviour
* Comments or documentation that overstate completeness

Determine which patterns are supported by evidence and how review practices should adapt.

## OpenCodeReview Overview

Analyse Alibaba OpenCodeReview in detail.

Cover:

* Project objective
* Supported review modes
* `ocr review`
* `ocr scan`
* Diff and repository-wide workflows
* File selection
* Review-unit construction
* Context retrieval
* Related-file handling
* Rule selection
* Parallel review execution
* Comment positioning
* Deduplication
* Reflection or validation stages
* Summary generation
* Severity and category handling
* Supported languages
* Model providers
* Configuration
* Custom rules
* CLI usage
* CI integration
* Coding-agent integration
* Privacy and source-code handling

Use diagrams or pseudocode to explain the review pipeline.

## OpenCodeReview Review Model

Determine what OpenCodeReview actually reviews.

Map its built-in concerns and rules to the broader review taxonomy.

Produce:

| Review concern | Covered by OpenCodeReview? | Review mode | Evidence | Limitations |
| -------------- | -------------------------: | ----------- | -------- | ----------- |

Investigate whether it focuses primarily on:

* Line-level defects
* Cross-file defects
* Security
* Maintainability
* Tests
* Performance
* Documentation
* Architecture
* Repository-level systemic issues

Do not infer complete coverage from category names alone.

## OpenCodeReview Evaluation Evidence

Critically assess the available evidence for OpenCodeReview.

Cover:

* Published benchmark design
* Number and type of repositories
* Languages
* Pull requests
* Annotated issues
* Baselines
* Precision
* Recall
* F1
* Token consumption
* Cost
* Review latency
* Model choice
* Selection bias
* Labelling methodology
* Reproducibility
* Availability of evaluation data
* Independent validation

Clearly distinguish vendor-reported results from independently verified evidence.

## OpenCodeReview Strengths and Limitations

Assess likely strengths such as:

* Deterministic coverage
* Structured orchestration
* Parallel review
* Repository search
* File-specific rules
* Lower prompt sensitivity
* Comment positioning
* Deduplication
* Repeatable CLI and CI use

Assess likely limitations such as:

* Dependence on model quality
* False negatives
* Context-window constraints
* Repository-scale constraints
* File-oriented decomposition
* Weak global architectural reasoning
* Language-specific rule maturity
* Provider privacy concerns
* Configuration complexity
* Benchmark generalisability
* Lack of product or business context

Label inferred limitations explicitly as inference.

## OpenCodeReview `review` vs `scan`

Compare the two operating modes.

| Dimension             | `ocr review` | `ocr scan` |
| --------------------- | ------------ | ---------- |
| Scope                 |              |            |
| Primary use           |              |            |
| Context               |              |            |
| Expected findings     |              |            |
| Cost                  |              |            |
| Noise risk            |              |            |
| Cross-file reasoning  |              |            |
| Architectural value   |              |            |
| Recommended frequency |              |            |

Recommend when each mode should be used.

## Comparison With Alternatives

Compare OpenCodeReview with representative alternatives, including:

* General-purpose coding agents
* GitHub Copilot code review
* Claude Code review workflows
* Codex review workflows
* CodeRabbit
* Qodo or equivalent AI review products
* SonarQube
* Semgrep
* CodeQL
* Snyk
* Conventional human pull-request review

Compare:

* Review scope
* Determinism
* Repository context
* Customisation
* Security capabilities
* CI integration
* Privacy
* Cost
* False positives
* Evidence quality
* Intended user
* Repository audit support

Avoid turning this into a broad product-ranking exercise. Compare only where it clarifies OpenCodeReview's role.

## Recommended Review Workflow

Develop a practical workflow for an engineer using AI coding agents.

Potential structure:

```text
During development
├── formatter
├── linter
├── type checker
├── tests
├── secret scanner
└── dependency/security tooling

Before merge
├── author self-review
├── OpenCodeReview diff or branch review
└── human review for intent and tradeoffs

Periodically or before release
├── repository scan
├── production-readiness review
└── targeted security or architecture audit

When risk warrants
├── specialist security review
├── performance investigation
└── data or reliability audit
```

For each stage, specify:

* Trigger
* Scope
* Reviewer or tool
* Expected findings
* Evidence standard
* Blocking criteria

## Practical Review Checklists

Produce concise, evidence-oriented checklists for:

* Diff review
* Feature review
* Repository audit
* Security-sensitive changes
* Background workers and queues
* APIs
* Database changes
* Cloud and infrastructure changes
* AI and data-pipeline components

Avoid generic checklist items such as “ensure code quality.”

Each item should describe what to inspect or trace.

## Example Review and Audit Reports

Provide examples of:

1. A high-quality diff review
2. A high-quality repository audit
3. A noisy or low-value review
4. A finding that should be suppressed
5. A finding that should be escalated for human verification

Use a consistent structure:

```text
Priority and category
Problem
Evidence
Failure or maintenance consequence
Confidence
Recommended direction
```

## Final Practical Framework

End with a concise framework that answers:

* What should always be reviewed?
* What should usually be reviewed?
* What should only be reviewed when risk warrants?
* What should be delegated to deterministic tools?
* What requires human judgment?
* What belongs in a diff review?
* What belongs in a repository audit?
* How should findings be evidenced and prioritized?
* Where does OpenCodeReview fit?
* What important gaps remain after adopting it?

Include a compact decision table suitable for future reference.

## Unresolved

List important questions that the available evidence cannot answer confidently.

Rules:

* Dense and factual.
* Prefer tables, checklists, decision matrices, diagrams, schemas, examples, benchmarks, and pseudocode over long prose.
* Avoid filler, motivational language, and generic “best practice” statements.
* Optimize for information density and practical usefulness.
* Focus on the practice of software review and auditing, not on designing a custom agent skill.
* Use OpenCodeReview as the primary case study, but do not treat its design as the definition of good review.
* Prefer primary sources:

  * Research papers
  * Official project documentation
  * Published engineering standards
  * Security standards
  * Official tool documentation
  * Reproducible benchmarks
* Use practitioner sources for workflow experience, failure modes, and real-world limitations.
* Tag claims inline:

  * `[OFFICIAL]` for documentation, standards, specifications, papers, vendor sources, and primary references.
  * `[COMMUNITY]` for practitioner reports, engineering blogs, forums, and community consensus.
  * `[INFERENCE]` for conclusions derived from multiple sources but not directly demonstrated.
* Distinguish vendor claims from independently verified evidence.
* Explicitly call out conflicting evidence and tradeoffs.
* Do not assume every review dimension belongs in every review pass.
* Rank concerns by engineering value rather than producing an exhaustive equal-weight checklist.
* Distinguish deterministic detection from contextual reasoning.
* Do not treat LLM review as a replacement for tests, static analysis, security tooling, or human judgment.
* Avoid style-only recommendations unless they materially affect correctness or maintainability.
* Do not report theoretical risks without explaining the reachable scenario.
* Do not force sections that lack sufficient evidence.
* If important questions remain unresolved, end with an "Unresolved" section.
