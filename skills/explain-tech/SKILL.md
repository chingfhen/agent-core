---
name: explain-tech
description: Explain technical systems, code changes, errors, tools, agent outputs, and completed engineering work so the human can understand and supervise them. Default to a quick explanation; use Deep when requested or complexity demands it, and Debrief after completed work.
---

# Explain Tech

## Purpose

Give the human the **smallest accurate mental model that makes them more capable**: what happened, how it works, where to look, what matters, and what remains uncertain.

This is explanation, not implementation, formal planning, or lesson-file authoring. Do not change code or documentation solely to explain it.

## Modes and visibility

**Default to Quick** unless the user requests more depth or the subject genuinely cannot be explained responsibly in a quick answer.

Open with a compact mode marker so the human knows other levels exist:

> **Explain-tech · Quick** (also: Deep / Debrief)

Use the matching label for the active mode. Do not add more preamble about the mode.

- **Quick (default):** Fast orientation, typically 100–250 words. Explain the mechanism in plain language, identify 1–3 important details and the main misconception. Include one small example or arrow diagram only when useful. Avoid exhaustive templates.
- **Deep:** Enough concrete structure to trace, reason about, and supervise the system. Select relevant lenses: architecture/topology, runtime flow, control surface, data/state, ownership, failure paths, trade-offs, verification. Expand progressively, not by dumping every section.
- **Debrief:** After work is completed, reconstruct actual changes from the available diff, code, tests, and context. Explain the change, why it works, important files, trade-offs, what was verified, and the key lesson. Do not narrate every edit or ask a quiz by default.

The user may simply say `explain-tech deep`, `explain-tech debrief`, or `quick explanation`. If the user requests a specific length, respect it over the defaults.

## Evidence and useful anchors

Start with relevant observed source material when the answer is about a particular repository, run, configuration, error, or agent output. Reuse existing context; inspect code, logs, diffs, docs, or settings only as needed.

Prefer **real names and relationships**: function or file, API route, environment variable, database table, storage path, permission boundary, command, or log line. A small accurate trace beats generic abstractions.

Explain causal relationships:

```text
request -> handler -> queue -> worker -> stored result
```

Use actual labels when they are known. For a change, contrast before and after. For an error, locate the first observed failure before offering a likely explanation.

Clearly separate **observed behavior** from **inference**. If the underlying system is inaccessible, say exactly which claim is unverified; don't invent paths, permissions, or runtime results.

## Human comprehension

- Lead with the answer or mental picture, then add only the supporting details that provide leverage.
- Avoid drowning a beginner in jargon. Explain unfamiliar terms once, in context.
- Show **where the human can inspect or regain control** when relevant.
- Surface the most consequential caveat or trade-off, not a catalogue of possibilities.
- Use a short example, tiny visual, or before/after when it helps understanding.
- When the human needs to perform a technical unblock, hand off to `human-unblock` rather than extending the explanation into speculative instructions.
- Do not persist explanations automatically; use `learning-markdown` only when a lesson artifact is requested and the separately authorized KB workflow only when explicit capture is requested.

## Completion

A useful explanation lets the human say, in their own words: **what it does, why it behaves that way, what they can inspect or change, and what is still unknown**. Provide the next useful question or action only if one genuinely follows.
