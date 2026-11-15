---
name: define-success
description: >
  Collaboratively discover, challenge, and agree on what meaningful success
  requires, especially when the human cannot fully specify the goal or its
  necessary conditions. Use when the human explicitly asks to define the goal,
  define success, figure out what good looks like, challenge an intended outcome,
  or work out what they are really trying to achieve; no slash command required.
  Also use when the human accepts another workflow's offer to define success.
  Not routine task writing, solution design, implementation, or verification.
disable-model-invocation: false
---

# Define Success

## Job and boundary

**Help the human and agent agree on the right outcome before judging how to achieve it.**
The human may know the frustration or desired change without knowing the domain,
important requirements, or what could go wrong. Lead the discovery rather than
asking the human to invent a complete specification. The goal is a useful shared
understanding, not a longer requirements document.

This is a **standalone, request-led conversation**. Natural cues include
"let's define the goal", "help me define success", "what would good look like?",
"what are we really trying to accomplish?", "challenge my success criteria",
and "help me work out what done means". A slash command or exact skill name
is not required. A passing reference to goals, task creation, acceptance
criteria, or a plan does not itself invoke a discovery session. If another
workflow merely offers it, begin only when the human accepts.

**Decision ownership:** The agent owns investigating, identifying plausible
omissions, explaining implications, and recommending interpretations. The human
owns consequential choices about the desired outcome and scope. An agent's
proposal is not an approved requirement; silence is not approval. Honor
existing approved decisions and applicable constraints.

Invocation alone authorizes neither task/document/KB writes nor code,
architecture changes, tests, experiments, deployment, or other execution.
Discussion may end with no artifact. Saving the agreed result uses the
separately authorized owning workflow (such as manage-project-tasks).

## Discover and converge

Adapt these moves to the uncertainty and consequences. They are not a
compulsory questionnaire or a fixed number of turns.

1. **Reconstruct the intent.** State a provisional interpretation of whose
   problem matters, what is failing or missing, the meaningful change sought,
   and why it matters. Distinguish an intended outcome from a suggested feature,
   deliverable, implementation, or metric. If the user's framing might be a
   premature solution, present the underlying need as a hypothesis rather
   than contradicting it by fiat. Consult relevant existing context and
   authoritative sources when they could change the answer; investigate what
   is discoverable instead of making the human repeat or guess it.

2. **Find consequential gaps.** Ask how the intended result could appear
   complete yet fail in reality. Select the few lenses that matter: a
   representative user journey and aftermath, important failure or misuse,
   affected stakeholders and trust boundaries, existing commitments, hidden
   assumptions, dependencies, and the consequences of doing nothing.
   Use concrete examples and counterexamples to reveal business rules. Prioritize
   by plausible impact and uncertainty; do not generate an exhaustive edge-case
   catalogue or automatically expand the objective.

3. **Lead the dialogue.** Offer an initial interpretation and material
   candidate conditions before questioning. Explain why each missing condition
   might matter; show a realistic scenario where the current definition would
   misclassify success. When a human-owned decision would change the result,
   ask **one focused question at a time**, with a recommended answer and its
   tradeoff where grounded. Questioning is an inherent part of this skill,
   but do not ask to confirm the obvious or interrogate a settled, low-risk goal.
   Answer ordinary clarification questions as part of the conversation.

4. **Separate necessity from opportunity.** Distinguish:
   - **Established:** explicitly agreed requirements or implications firmly
     grounded in approved intent, existing contracts, or constraints.
   - **Candidate / unresolved:** plausible conditions that need human judgment,
     domain evidence, or specialist validation before becoming binding.
   - **Optional / out of scope:** potential improvements that go beyond what is
     required for the present goal.
   Never quietly promote a useful idea into an obligation. When the human is
   unfamiliar with a domain, offer an evidence-based recommendation, identify
   assumptions and knowledge limits, and retain consequential uncertainties.

5. **Agree on an observable success definition.** Once the consequential
   questions are resolved or deliberately deferred, provide a concise statement
   of the intended outcome and the smallest useful set of observable success
   conditions. Include important exclusions, unresolved choices, and what
   kind of observation would distinguish success from failure when helpful.
   Do not substitute implementation steps, a test suite, or arbitrary numerical
   targets for the outcome. Mark provisional definitions as provisional;
   revise when the human changes the goal. A clear existing success definition
   is a valid no-change conclusion.

## Example of the distinction

Human: "Let travelers edit their itineraries through ChatGPT."

Provisional underlying outcome: Travelers can make a change through their
preferred assistant and trust that the accepted trip state reflects it.

A high-value counterexample: ChatGPT says "saved", but reopening the trip
shows the old activity. That exposes persistence and honest failure reporting
as candidate necessary conditions, not merely an extra feature request.

A different idea, such as offline editing or automatic conflict merging,
may be valuable, but is not silently included. If concurrent travelers are
in scope, clarify their conflict semantics with the human using an example.
The verification workflow later decides how to gather evidence; this skill
first establishes what must be true.

## Handoff and stopping

Keep the result conversational and proportional. For substantial work, a
useful handoff usually contains the **outcome**, **agreed success conditions**,
**important exclusions**, and **unresolved questions/assumptions**. Provide
more detail only when it materially improves later judgment. Do not impose
a formal document, score, rigid headings, or compulsory approval ceremony.

Stop once the human has a usable agreement, a clearly marked provisional
definition, or a specific unresolved decision needing further evidence.
Do not keep inventing questions to appear thorough. On explicit request,
hand the agreed definition to manage-project-tasks or another owning
workflow for persistence. A task can also be saved as an early idea without
invoking this skill.

**Boundary with nearby work:** manage-project-tasks preserves execution state;
tech-design-options compares technical approaches; approval review evaluates
a consequential authorization; verification discovers and exercises evidence
against the agreed claims. They can consume this result without this skill
owning their files, decisions, or checks.
