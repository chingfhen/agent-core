# Task: Replace broad engineering with code-design

**File:** `tasks/2026-11/targeted-design-skills/2026-11-11__replace-engineering-with-code-design.md`
**Created:** 2026-11-11
**Last Updated:** 2026-11-11
**Priority:** Next
**Status:** Closed — Completed

**Goal:** Replace the general `engineering` skill with a request-led specialist for understandable, safely changeable bounded code design.

**Outcome:** Created [`code-design`](../../../skills/code-design/SKILL.md) and [focused review scenarios](../../../skills/code-design/SCENARIOS.md), selected it in the personal manifest, retired the old source to the [archive](../../../archive/skills/2026-11-11__engineering-SKILL.md), and reconciled directly affected documentation and workflow references. Ordinary execution and verification remain the main agent's responsibility. The separate verification proposal remains unresolved; its historical ownership assumption and source link were corrected.

**Independent comparison:** A blind reviewer preferred the new skill for the stated design job, rating it higher on request-led scope, structural judgment, and workflow economy while identifying lost general debugging and delivery guidance. This was a subjective static comparison, not a behavioral trial; the old candidate was condensed and skill identities could be inferred from their content. After review, the new skill was refined to scale the change scenario to the decision; the verdict applies to the pre-refinement text.

**Verification and limits:** Focused activation and design scenarios were reviewed statically, not run as baseline-versus-skill behavioral trials. The archived old source matches the original Git blob. Manifest selection and source changes do not establish installation, and removing a manifest entry does not uninstall old copies. No harness sync, consumer changes, or installed-copy retirement is implied. No measured maintainability or runtime improvement is claimed.

**Closeout:** Documentation updated in the skill catalogue and skill design guide. KB and operational-lessons reviews found no separate reusable evidence or behavior needing persistence beyond these directly owned project sources. Applicable agent guidance: `C:\Users\tanch\.agent-core\AGENTS.md`, unchanged.

## Design rationale and boundaries

The earlier skill activated for broad execution and included a default commit; the new skill focuses on who owns rules, what interfaces expose, and what a future reader must know or coordinate to make a concrete change. It is not a universal design checklist, a general verification workflow, or a replacement for competent routine coding. A read-only review does not authorize edits; an approved refactor may change scoped code while preserving contracts. No-change can be the right result. The related [design-options task](2026-11-11__replace-planning-with-design-options.md) addresses selection among consequential approaches independently.

The research behind the selected direction included [Ousterhout and Martin's discussion](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md), [Google code-review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html), [Fowler on YAGNI](https://martinfowler.com/bliki/Yagni.html), [Matklad on architecture maps](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html), [OpenAI's harness engineering case study](https://openai.com/index/harness-engineering/), and [the AGENTS.md evaluation](https://arxiv.org/html/2602.11988v3). They informed judgment, not a proven productivity claim for this skill.
