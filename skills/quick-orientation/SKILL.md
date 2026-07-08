---
name: quick-orientation
description: Use when the user needs a fast, low-density explanation of a technical topic, repo change, tool, error, architecture, or agent output.
---

# Quick Orientation Skill

## Purpose

Help the user quickly understand **what the hell is going on**.

The goal is not depth.
The goal is a usable first mental map.

A good answer should leave the user able to say:

```text
I get the basic shape now.
I know what matters.
I know what to ask next.
```

## Default Response Shape

```markdown
## Quick orientation: <topic>

**Plain English**
<2-4 sentences>

**Mental picture**
<tiny visual, analogy, or before/after>

**What matters**
- <1-3 key points>

**Ignore for now**
- <details not worth learning yet>

**Main trap**
<common misunderstanding>

**Next question**
"<useful follow-up question>"
```

## Style

Be short, direct, and practical.

Prefer:

* simple words;
* one concrete example;
* tiny arrow visuals;
* before/after contrast;
* “this is basically X, not Y”;
* saying what can be ignored.

Avoid:

* full tutorials;
* interview-style answers;
* exhaustive lists;
* deep architecture review;
* too many caveats;
* explaining every file or line;
* formal diagrams unless asked.

## Micro-Visuals

Use tiny visuals when they compress the idea.

Examples:

```text
Frontend → API → Queue → Worker → Result
```

```text
Before: request waits for slow work
After:  request creates job; worker finishes later
```

```text
User pays → webhook arrives → backend verifies → credits added
```

```text
Docker image = packaged app
Registry = warehouse for packages
Old tags = boxes still taking space
```

## Core Rules

1. Start with the plain-English answer.
2. Explain only the main mechanism.
3. Use one mental picture, not five.
4. Separate what matters from what can be ignored.
5. Call out the most likely misunderstanding.
6. End with the next useful question.
7. Keep the default answer under 250 words.

## If Evidence Is Missing

For repo-specific, log-specific, or code-specific claims, do not pretend.

Say:

```text
Unverified: I have not inspected the actual code/logs, so this is the likely explanation rather than confirmed repo behavior.
```

## Escalation

Go deeper only when the user asks for:

* risks;
* implementation details;
* comparison;
* decision support;
* debugging steps;
* handoff to an agent;
* production-readiness review.
