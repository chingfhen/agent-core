---
name: code-review-quality
description: Review an actual code diff, change set, or PR for important correctness, test, readability, architecture, security, and performance issues, especially before handoff or merge. Use for code-review requests or review-ready changes, not routine implementation or repo-wide auditing.
disable-model-invocation: false
---

# Code Review and Quality

## Job and boundary
Assess whether a specific change improves the software safely. Review-only intent never authorizes edits, commits, host review submission, merges, or deployment. This skill reviews implementation quality; `git-branch-to-review` owns managed branch/PR delivery and merge permission; `code-design` owns a requested structural design job. The author's own review is not an independent audit.

## Review the evidence
1. Read the objective, affected contracts, repository conventions, changed files, and diff against the actual target. Look first at tests and observable behavior claimed by the change; do not infer success from a green status without examining what it checks.
2. Follow important changed execution paths, including error/empty/stale/concurrent cases. Apply the relevant axes proportionately:
   - Correctness: requirements, invariants, edge cases, state, transactions, and effective tests.
   - Readability: changes another developer could follow; avoid preference-only criticism.
   - Architecture: ownership and coupling with demonstrated change burden.
   - Security: changed trust boundaries and privilege/data exposure.
   - Performance: credible workload or observed regression, not speculative micro-optimizations.
3. Confirm whether mandatory checks actually ran on the reviewed revision. If absent, report missing evidence rather than inventing failures or assuming they pass. Suggest the smallest decisive test when helpful.
4. Findings should identify exact file/line or path when available, a concrete failure scenario, severity/blocking status, and the minimal remedy. Prioritize real defects over exhaustive stylistic checklists. It is valid to find no meaningful issues.
5. Give a merge/revise recommendation tied to evidence and remaining risks. A review recommendation is not a merge or a permission to fix the issues. If review triggers discovery of a material new threat or contract design question, point to the appropriate specialist without launching a mandatory skill chain.

## Stop condition
A reviewer can see the significant findings, their evidence and severity, actual check status, and a proportionate recommendation. Do not require every axis to have a finding or spawn subagents without explicit approval.

## Source
Adapted from [Addy Osmani's Code Review and Quality](https://github.com/addyosmani/agent-skills/tree/main/skills/code-review-and-quality), focusing on concrete findings rather than an always-exhaustive ceremony.
