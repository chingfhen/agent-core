---
name: human-unblock
description: Use during execution when progress is blocked, or likely to stall, on an action or information only the human can provide—for example access approval, interactive authentication, an inaccessible system, a permission change, or a required decision. Help the human unblock the agent quickly; do not apply to ordinary solvable errors.
---

# Human Unblock

## Purpose

Keep the agent autonomous without leaving the human guessing when their intervention is necessary.

## When to intervene

Continue working independently when the issue is reasonably solvable using available tools and evidence.

Escalate promptly when a specific human action is likely necessary or clearly the fastest legitimate way forward. Typical signals include inaccessible logs or systems, missing entitlements, interactive sign-in, approvals, or an organizational decision.

Do not repeatedly retry the same ineffective approach, invent internal procedures, or disguise a human-owned blocker as a code problem. A suspected blocker is enough to raise when further autonomous attempts are unlikely to help; state uncertainty plainly.

## How to ask

Make the intervention *easy to perform*, even for a beginner with limited attention.

Tell the human, concisely:

1. **Blocker and impact:** What is stuck, and why their action is needed.
2. **Next action:** Exactly where to go and what to click, run, copy, or ask someone else. Give a ready-to-send message or command when useful.
3. **Return signal:** What to paste back or confirm so execution can resume.

Prefer one actionable step at a time when the process is unfamiliar. If the exact internal procedure is unknown, say so and ask for the smallest screenshot, log excerpt, or clarification that would reveal it—do not fabricate steps.

Never request passwords, tokens, private keys, or other secrets in chat. Have the human perform authentication in the approved system; do not bypass access or security controls.

## Scope

This is an **execution-time escalation aid**, not a mandatory preflight, approval gate, or blanket instruction to pause. Do not interrupt for routine implementation choices, minor uncertainty, or problems the agent can resolve itself.

Once unblocked, resume the original task autonomously.
