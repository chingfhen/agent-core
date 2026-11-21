---
name: web-interface-review
description: Inspect a specified implemented web UI for usability, accessibility, responsive behavior, and interaction-state issues; use for UI/UX/accessibility review or when a substantial changed interaction needs review. Not a visual redesign or general code audit.
disable-model-invocation: false
---

# Web Interface Review

## Job and boundary
Find observable interface problems that could confuse, exclude, or mislead real users. Review the named screens or changed flows, not the entire application by default. This is distinct from `frontend-design` (creating visual direction), `react-nextjs-practices` (framework implementation), and `code-review-quality` (general diff review).

## Review
1. Ground the review in the target users, approved behavior, actual code, and available running interface. Confirm which states and viewports can be inspected. If runtime access is missing, mark findings code-based rather than claiming tested behavior.
2. Check the relevant fundamentals: clear labels and purpose, hierarchy, keyboard/focus support, screen-reader semantics where inspectable, sufficient contrast, accessible feedback, touch targets, responsive layout, navigation, reduced motion, and meaningful loading/empty/error/success states.
3. For changed mutations, ask whether the UI honestly represents pending, saved, rejected, and stale/conflicting states. Client confirmation must not imply that a backend or external booking succeeded when it did not.
4. When current, authoritative [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) are accessible, consult applicable rules; do not let external fetch failure prevent a bounded local review. Avoid treating a checklist as automated proof of accessibility.
5. Report only actionable, evidenced issues with affected route/component, impact, severity, and a minimal corrective direction. Distinguish definite problems, likely problems needing runtime inspection, and subjective preferences. Do not silently edit when the request is review-only.

## Stop condition
The review covers the affected user flows with honest evidence levels and a prioritized, nonduplicated set of findings (or a grounded no-issue conclusion). No mandatory report for unaffected pages.

## Decision visibility

When this skill makes a consequential choice—selecting, declining, or deferring a path, or applying a material scope, permission, cost, safety, or verification gate—make the chosen outcome and its evidence-based reason visible in the normal conversation (a compact `Decision: ... — ...` is sufficient). State it before acting when permission or cost depends on the choice, otherwise at the relevant handoff. An explanation already clearly given counts; do not add a duplicate status line, routine no-op receipts, a separate log, or private reasoning. Merely loading a skill is not evidence that its decision was applied.
