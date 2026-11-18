---
name: frontend-design
description: Establish or improve a distinctive, intentional visual design for a concrete frontend screen, flow, or product UI when design creation or redesign is requested. Use for aesthetic direction and visual hierarchy, not as a mandatory process for ordinary React bug fixes.
disable-model-invocation: false
---

# Frontend Design

## Job and limits
Produce a coherent visual experience that fits the actual product, users, and purpose rather than a generic generated template. Respect approved brand, accessibility, product scope, content, and design constraints. Do not invent product features, replace genuine data with misleading mock facts, or require a redesign when a focused UI adjustment is requested.

## Design and build
1. Identify the screen's primary user decision or action, the real content it must communicate, its use context (including small screens), and existing design conventions. For a new direction, propose one coherent visual treatment rather than an unsolicited moodboard of alternatives.
2. Make hierarchy carry meaning: distinguish committed versus tentative states, primary versus secondary actions, editable versus locked information, and saved versus pending/failed actions. Choose typography, spacing, color, and imagery based on this content rather than fashion or generic SaaS patterns.
3. Design for representative content lengths and real failure/empty/loading states. Preserve legibility, sufficient contrast, focus indication, touch usability, and reduced-motion preferences. Motion must communicate an interaction or state, not merely decorate.
4. Implement or describe the smallest coherent scope authorized by the request. Reuse existing components/tokens where sensible; change broader patterns only when the identified design goal needs it.
5. Inspect the actual UI in a supported renderer when available, including a phone-sized viewport. Distinguish a screenshot/design critique from actual usability or accessibility verification; report untested conditions.

## Stop condition
The requested screen/flow has an explainable visual hierarchy grounded in real content, and the result or design recommendation accounts for consequential states and constraints. Do not create an identity system or full component library without a product need.

## Source
Adapted from [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design), with an explicit preference for product constraints over prescribed aesthetics.
