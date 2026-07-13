# Report Template

Write to `artifacts/audit/YYYY-MM-DD__repo-audit.md` in the audited repo
(create the directory). Standalone — no cross-report bookkeeping.

```markdown
---
date: YYYY-MM-DD
repo: <name>
commit: <short hash>
scope: full baseline | <focus or path>
mode: static-only | executable-evidence
---

# Repo Audit: <repo>

## Verdict
<2–4 sentences: risk posture.>
Findings: <n> (P0 <n> · P1 <n> · P2 <n> · P3 <n>). Cuts: <n>.

## System map
<compact: entry points → workflows → state stores → external systems;
trust boundaries marked. Tiny arrow diagrams beat prose.>

## Findings
### 1. [P1 · confirmed · high] <title>
- **Where:** primary and supporting path:lines
- **Evidence:** relevant execution, change, or ownership path
- **Scenario / mechanism:** concrete failure scenario, or the mechanism
  creating the design concern
- **Consequence / engineering cost:** observable impact, or demonstrated
  operational or maintenance cost
- **Safeguards or justification checked:** controls or architectural
  reasons examined and why they do not resolve this
- **Assumption:** probable findings only — the one unverified runtime,
  configuration, or deployment assumption
- **Direction:** invariant, control, boundary, or simplification
  direction; name an executable follow-up or specialist escalation where
  useful

## Cut list
<tag> <what to cut> — <why removal is safe and materially useful>.
<replacement>. [path]

estimated reduction: approximately <N> lines and <M> direct dependencies
<or: reduction not estimated without constructing a patch>

## Investigate
- <exact question, phrased as a question, plus the evidence that would
  resolve it>

## Coverage
Examined: <workflows/components traced end to end>
Sampled: <areas skimmed, not traced>
Excluded: <generated, vendored, out-of-scope>
Activated dimensions: <conditional concerns applied this run>
Intent evidence: <contracts, schemas, tests, docs, config, and history used>
Commands run: <commands, or "none">
Unavailable: <runtime config, deployed infra, cross-repo consumers, …>
```

Empty states:

- No findings: `No material findings.` in place of the register.
  Coverage is still required — never write "clean" or "safe".
- Nothing to cut: `Lean already.` in place of the cut list.
- Omit the Investigate section only when genuinely empty.
