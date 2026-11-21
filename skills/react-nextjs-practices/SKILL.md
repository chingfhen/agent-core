---
name: react-nextjs-practices
description: Apply focused React and Next.js rendering, data-fetching, state, and bundle guidance when implementing or reviewing actual React/Next.js code. Trigger on relevant web-app code, not generic frontend design or framework-independent tasks.
disable-model-invocation: false
---

# React and Next.js Practices

## Job and boundary
Improve correctness and understandable performance of an actual React/Next.js change. First match the project's React/Next.js versions, routing mode, server/client boundaries, and existing conventions. Do not treat performance advice as proof of a bottleneck or apply all rules mechanically. Avoid framework upgrades, dependency additions, cache policy changes, and broad refactors unless requested or required for the agreed change.

## Focused decision sequence
1. Identify the user-visible behavior, data sources, sensitive values, and components/routes touched. Preserve the app's canonical backend state and avoid showing optimistic success for rejected mutations.
2. Prevent *material* sequential request waterfalls where independent calls can run together. Avoid fetching unnecessary data or duplicating requests; prefer simpler existing project patterns to new abstractions.
3. Choose client and server execution intentionally. Keep private data out of shared caches, static payloads, or unauthenticated client output. Validate backend permission regardless of frontend rendering choices.
4. Keep state ownership clear: derive render state where possible; avoid effects that merely copy props or create update loops. Split components for meaningful boundaries, not to satisfy a code-size target.
5. Look for expensive dependencies or avoidable re-renders only when the change introduces credible cost or observed regressions. Prefer measuring before optimizations with complexity or caching trade-offs.
6. Exercise affected interactions and loading/error states. Use accessible, responsive behavior, then run the existing build/type/test checks relevant to the change and report observed results.

## References
Use the relevant part of [Vercel's React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices), which groups guidance by waterfalls, bundles, server and client behavior, re-renders, and rendering. Its broad rule list is a lookup resource, not a checklist to exhaust. For visual direction use `frontend-design`; for a dedicated UI audit use `web-interface-review`.

## Decision visibility

When this skill makes a consequential choice—selecting, declining, or deferring a path, or applying a material scope, permission, cost, safety, or verification gate—make the chosen outcome and its evidence-based reason visible in the normal conversation (a compact `Decision: ... — ...` is sufficient). State it before acting when permission or cost depends on the choice, otherwise at the relevant handoff. An explanation already clearly given counts; do not add a duplicate status line, routine no-op receipts, a separate log, or private reasoning. Merely loading a skill is not evidence that its decision was applied.
