---
name: approval-gate
description: >
  Provide a concise, neutral approval check before consequential work.
  Use when the user asks for an approval check/review, or before taking a
  consequential action that has not already been explicitly authorized.
---

# Approval Gate

Help the user make an informed approval decision. Do not persuade them to approve.

## When to use

Use this skill when the user says things such as:

- "Approval check."
- "Run the approval gate."
- "Ready for approval?"
- "Give me an approval brief."
- "Final check before I approve."

Also use it before an unapproved action that is materially consequential because it is
hard to reverse, destructive, externally visible, affects shared systems or other
people, commits meaningful resources, changes security/permissions, or materially
deviates from an already approved direction.

Do not gate ordinary research, discussion, drafting, testing, or local reversible work.
Do not ask again for approval that the user has already clearly given.

## Approval check

In the next response:

- State exactly what you recommend approving.
- Give only the key reasoning needed to evaluate it.
- Surface material trade-offs, risks, assumptions, and uncertainty.
- Clearly identify anything that should block approval.
- If you do not recommend proceeding, say so and explain why.
- Define the scope of what the approval would authorize.

Keep it concise. Do not reproduce the full plan or task specification.
Do not manufacture confidence or optimize for agreement.
Avoid mannered prose.

Then stop. Do not perform the gated action until the user explicitly approves it.

## After approval

Return control to the originating workflow and proceed within the approved scope.

Approval does not authorize materially different or additional consequential actions.
If the direction materially changes, run another approval check.