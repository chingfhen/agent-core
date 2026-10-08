---
name: debrief
description: Post-session teaching mode. Explains what changed, why it works, the mental model, and the important tradeoffs so the user can reason about it themselves.
disable-model-invocation: true
license: MIT
---

# Debrief

Goal: leave the user with a usable mental model of what just happened.

The user invoked this skill because they want to learn. Do not make them earn the explanation through an interview.

## Persistence

Stay in debrief mode for the current thread. Treat follow-up questions as part of the lesson. Exit when the user changes task or asks to stop.

## Default stance

- Minimal interaction.
- Dense, technical explanation.
- Prefer the actual code, diff, and behavior over generic theory.
- One coherent lesson, not a narrated changelog.

## Process

1. Reconstruct the work from the code, diff, docs, and session context.
2. Start with the mental model, not line-by-line edits.
3. Explain why the change works, not just what changed.
4. Surface the key nuance: the subtle thing most likely to be misunderstood.
5. Surface the tradeoff: what was chosen over what, and why.
6. End with what the user should now be able to explain on their own.

## Output shape

Use this shape unless the user asks otherwise:

- **What happened:** one short paragraph on the problem and the shape of the fix.
- **Mental model:** the simplest correct model of how this part works.
- **Key code paths:** 2-5 bullets with file or symbol references.
- **Why it works:** cause -> effect.
- **Common wrong model:** what a smart person might think at first, and why it's incomplete.
- **Nuance:** edge case, invariant, or tradeoff that matters.
- **You should now be able to explain:** 2-4 bullets.

## Rules

- Do not ask questions unless the artifact to explain is genuinely unclear.
- Do not pad with beginner filler.
- Define jargon on first use.
- If a claim depends on a condition, name the condition.
- Compress aggressively; skip unimportant edits.
- If the explanation needs structure, timing, or state to be legible, recommend using `diagram-generation` and wait for approval.
- Do not generate a diagram automatically.
- If there was no concrete coding session, teach the topic in the same format from first principles.