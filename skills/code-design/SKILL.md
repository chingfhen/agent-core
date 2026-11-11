---
name: code-design
description: Design, review, or restructure a bounded area of software code for clear ownership, useful interfaces, and safe, understandable change. Use when explicitly invoked or asked for that structural design job, such as reviewing coupling or giving a domain rule one owner; not for ordinary implementation, debugging, generic review, or editing prose.
disable-model-invocation: false
---

# Code Design

## Job and boundary

Reduce the knowledge and coordinated edits needed to understand and safely change a specific module, subsystem, or diff. Activate for a named invocation or a clear request for this structural job. Ordinary coding does not need this skill; generic implement, fix, review, or refactor requests and editing skills, docs, or other prose do not activate it. You may flag a material structural concern during ordinary work without silently expanding the assignment.

Follow the requested action: design or review is read-only; an authorized refactor or implementation permits scoped code changes. Do not make an unrequested behavior or public-contract change or broader architectural departure. Do not make a separate approval ceremony for already authorized work. This is not a general debugging, security, verification, or repository audit, and it does not create commits, branches, task updates, or other persistence by default.

## Reason about the design

1. **Trace the actual burden.** Read the target and the callers, state, and contracts necessary to follow one representative operation. For new code, use approved requirements and representative usage. Explain what a reader must know or coordinate and the consequence: for example, a duplicated rule that can drift, hidden mutation, an ordering obligation, or a leaked representation. A style violation, line count, or abstract principle alone is not evidence.
2. **Find a proportionate arrangement.** Identify who owns the relevant rules, state transitions, and authoritative values. Consider whether callers can use a clear interface without knowing implementation details, while still seeing essential preconditions, side effects, failures, and units. Keep related invariants together; reduce unnecessary dependencies and hidden state. Respect existing architecture, authorization, transaction, and recovery semantics. Use only the lenses that matter to this case.
3. **Compare with leaving it alone.** Describe the smallest coherent change, if any, and briefly walk through a real required or credible upcoming change: what would its owner and callers need to change? Scale the trace to the decision. Explain what knowledge or coordination is removed and what indirection or other cost is added. The future change is a thought experiment, not permission to build speculative extension points. Do not force shared abstractions on similar code with independent meanings, or split a cohesive function solely because it is long. Keeping the design is a valid outcome.
4. **When code changes are authorized**, preserve observable contracts and failure behavior unless the request explicitly changes them. Separate behavioral changes from structural movement where useful. Use relevant existing checks; add a focused characterization or regression check when it protects uncertain or material behavior. Expand checks for affected contracts or evidence, not ceremony. Passing checks do not by themselves establish better design; a read-only design review does not inherently require tests.
5. **Show the consequence and stop.** For review, give evidence, practical impact, and a proportionate recommendation or a grounded no-change conclusion. For implementation, explain the important before/after ownership or interface and the concrete change it makes easier; report checks actually performed and meaningful limits. Do not manufacture findings, quantify maintainability gains without evidence, or broaden into unrelated cleanup.

Local design alternatives do not require `tech-design-options`, which compares consequential solution approaches when requested. Minimal code is not necessarily the lowest reasoning burden; `yagni` is a separate requested minimalism lens. Neither skill is a prerequisite for ordinary execution or for the other.
