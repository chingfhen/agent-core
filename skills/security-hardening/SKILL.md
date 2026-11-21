---
name: security-hardening
description: Apply scoped threat modeling, boundary checks, and security verification when implementing or reviewing authentication, authorization, private data, uploads, untrusted input, external services, or agent-initiated mutations. Not for every ordinary style or documentation edit.
disable-model-invocation: false
---

# Security Hardening

## Job and authority
Protect the specific trust boundaries touched by the task. Security review does not authorize probing real user accounts, external systems, production, paid services, changing access controls, adding monitoring that records sensitive data, or deploying. Ask before high-impact security changes outside the approved implementation scope.

## Risk-focused procedure
1. Name the asset, actor, action, and trust boundary. Trace one normal path and one plausible misuse path (e.g., a member of Trip A accesses Trip B's proof, or an AI tool performs an unapproved mutation). Prefer concrete abuse cases over a generic exhaustive checklist.
2. Inspect existing identity, session, tenant ownership, authorization, validation, data access, file storage, logs, and tool boundaries as applicable. Treat browser checks, UI visibility, and an LLM's instruction as insufficient authorization for backend actions.
3. Apply the smallest effective controls at the authoritative boundary: reject unauthorized reads and writes; constrain accepted inputs; keep secrets out of responses, logs and client bundles; use limited-lifetime access for private files when appropriate; guard server-side fetches against unintended destinations; define approval and revision checks for agent changes.
4. Check dependency advisories, supply-chain hazards, and security headers only when relevant to affected packages or surfaces. Avoid blind updates and broad configuration changes.
5. Exercise representative denial/failure paths using synthetic identities/data and authorized test environments. A happy-path test, screenshot, or static scan alone cannot certify security. Record observed results and remaining risks; recommend specialist review for consequential unresolved exposure.

## Stop condition
The identified boundary has explicit expected behavior, relevant controls and executable checks where possible, and clear residual risk. Do not claim security certification or implement an all-OWASP audit by default.

## Source
Risk-focused adaptation of [Addy Osmani's Security and Hardening](https://github.com/addyosmani/agent-skills/tree/main/skills/security-and-hardening) and established web trust-boundary practices.

## Decision visibility

When this skill makes a consequential choice—selecting, declining, or deferring a path, or applying a material scope, permission, cost, safety, or verification gate—make the chosen outcome and its evidence-based reason visible in the normal conversation (a compact `Decision: ... — ...` is sufficient). State it before acting when permission or cost depends on the choice, otherwise at the relevant handoff. An explanation already clearly given counts; do not add a duplicate status line, routine no-op receipts, a separate log, or private reasoning. Merely loading a skill is not evidence that its decision was applied.
