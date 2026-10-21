---
name: learning-markdown
description: Creates concise, practical Markdown lessons optimized for human reading and learning from transcripts, conversations, articles, documentation, research, notes, or other source material. Uses 80/20 distillation, clear terminology, adaptive structure, and Markdown features only when they materially improve understanding. May produce one or multiple lessons when separate files create better units of human understanding.
disable-model-invocation: false
---

# Learning Markdown

## Purpose

Turn source material or a discussion into one or more Markdown lessons that are easy to understand, useful to reread, and compact enough that a human will actually read them.

Optimize for:

- comprehension;
- retention through clear explanation;
- practical judgment;
- concise rereading;
- accurate terminology.

Do **not** try to turn the Markdown file itself into a complete learning system.

The lesson is the durable explanation. Quizzes, spaced repetition, mind maps, flashcards, interactive tutoring, and other learning methods are separate activities unless the user explicitly asks for them.

> Keep the small amount of information that delivers most of the learning value.

---

# Core Writing Principles

## Use the 80/20 rule

Distill aggressively.

Prefer the few ideas that most improve the reader's understanding or judgment:

- the core mental model;
- the main conclusion and why it is true;
- important terminology;
- causal relationships;
- useful distinctions;
- conditions and boundaries;
- trade-offs;
- failure modes or diagnostic clues;
- decision rules;
- practical implications.

Do not preserve information merely because it appeared in the source.

A long source may legitimately produce a short lesson.

Conciseness should come from removing low-value material, repetition, tangents, and unnecessary examples—not from deleting necessary nuance.

## Start with takeaways

Substantial lessons should normally begin with:

```markdown
# [Clear title]

## Takeaways

- ...
- ...
- ...
```

The reader should be able to understand the most important conclusions before reading the full explanation.

Usually prefer a small number of high-signal takeaways rather than a long summary.

Do not add a second summary at the end unless it contributes something new.

## Teach one coherent unit

One lesson should teach one coherent mental model, concept cluster, or decision problem.

Do not force an entire transcript, article, or conversation into one file.

Produce multiple lessons when separate files would each become a better unit of human understanding.

Split when topics can be understood and revisited independently.

Keep material together when splitting would:

- break one coherent mental model;
- require substantial repeated context;
- separate a conclusion from the reasoning needed to understand it.

Do not split merely because the source is long.

## Preserve useful reasoning

Do not reduce an important conclusion to a bare fact.

When reasoning matters, preserve enough of it for the reader to understand:

- why something happens;
- why a technique works;
- what assumptions it depends on;
- when it applies;
- what it costs;
- when another choice is better.

Prefer explanations such as:

> X helps under condition A because B, but introduces trade-off C.

over:

> X is better.

## Use accurate terminology

Explain concepts simply without deleting their real names.

Introduce the canonical term when the concept becomes relevant.

Include common aliases or synonymous terms when the reader is realistically likely to encounter or search for them.

Example:

> The replica can temporarily be behind the primary. This is called **replication lag**, also commonly called **replica lag**.

Do not create a glossary unless the number or density of terms makes one genuinely useful.

## Prefer causal and decision-oriented knowledge

When relevant, emphasize:

- symptom → likely cause;
- problem → mechanism;
- intervention → effect;
- choice → trade-off;
- condition → decision;
- failure → diagnosis;
- concept A → how it differs from concept B.

These relationships are usually more valuable than isolated definitions.

## Keep important caveats

Do not compress:

> X usually improves Y under conditions A and B.

into:

> X improves Y.

Keep caveats that materially affect correct understanding or practical use.

Do not preserve every edge case.

---

# Choosing What Survives

The skill should not use a heavy scoring or classification workflow.

Ask one practical question:

> **What are the few things the reader most needs to understand and remember?**

Strong candidates usually include:

- ideas required for a correct mental model;
- important causes and mechanisms;
- practical decision rules;
- major trade-offs;
- likely points of confusion;
- important boundaries;
- useful failure modes;
- diagnostic signals;
- terminology needed to recognize the concept elsewhere.

User questions, follow-ups, corrections, and moments of confusion are useful signals of importance.

They are not the boundary of the lesson.

Include critical information the user did not think to ask about when omitting it would leave a materially incomplete or misleading understanding.

When working from attached or supplied sources, preserve what those sources actually support. Do not silently replace their claims with outside knowledge. If the user asks for research, verification, correction, comparison, or expansion, distinguish added information from source-derived material.

---

# Examples and Analogies

Use examples only when they materially improve understanding.

Prefer:

- one strong example;
- a small worked example;
- a concrete scenario that makes an abstract mechanism obvious.

Avoid:

- examples for every concept;
- multiple examples that teach the same thing;
- decorative analogies;
- metaphors that are less precise than the direct explanation;
- examples that add more text than understanding.

If the concept is already clear in direct language, do not add an analogy.

---

# Structure

Use a small mandatory shell and an adaptive body.

The default substantial lesson starts with:

```markdown
# [Title]

## Takeaways

- ...
```

Everything after that should be chosen according to the subject.

Possible sections include:

```markdown
## Mental Model
## How It Works
## Why It Happens
## Key Terms
## Example
## Trade-offs
## When to Use It
## When Not to Use It
## Failure Modes
## Symptoms and Likely Causes
## Decision Guide
## Common Mistakes
## Comparison
## Practical Workflow
## Related Concepts
```

These are options, not a template.

Do not create empty or low-value sections merely for structural consistency.

Do not mechanically reproduce the source's chapter structure.

A lesson should be understandable without the original conversation or source open beside it.

---

# Progressive Reading

Write so the lesson works at multiple depths.

A reader should be able to:

1. read the title and takeaways for the conclusion;
2. scan headings and emphasized terminology to reconstruct the main structure;
3. read the full lesson for reasoning, nuance, and practical understanding.

Do not make the reader reach the final paragraph before discovering the point.

Keep the first screen high-signal.

---

# Markdown Toolkit

Use Markdown features because they communicate something better, not because Markdown supports them.

## Headings

Use headings to represent meaningful conceptual structure.

Prefer a few substantial sections.

Avoid:

- a heading for every short paragraph;
- deep heading nesting without a real hierarchy;
- generic headings that add little information.

## Paragraphs

Use short prose when an explanation requires relationships, causality, or nuance.

Prefer direct language.

Do not turn every idea into a bullet.

## Bullet lists

Use bullets for parallel items such as:

- criteria;
- properties;
- independent takeaways;
- failure modes;
- considerations;
- concise examples.

Do not use bullets when the reader needs a continuous explanation.

## Numbered lists

Use numbered lists only when order matters:

- procedures;
- sequences;
- prioritized actions;
- staged reasoning.

Do not number an arbitrary collection of facts.

## Bold

Use **bold** selectively for:

- canonical terminology;
- important conclusions;
- critical conditions;
- key contrasts.

If too much text is bold, emphasis stops working.

## Italics

Use *italics* rarely for secondary emphasis.

Do not use italics decoratively.

## Inline code

Use `inline code` for exact technical tokens such as:

- commands;
- API names;
- configuration keys;
- paths;
- identifiers;
- literal values.

Do not format ordinary concepts as code merely because they are technical.

## Code blocks

Use fenced code blocks when exact syntax, commands, configuration, pseudocode, queries, or structured examples are part of the lesson.

Do not place ordinary prose inside code blocks.

## Tables

Use tables when the reader needs to compare multiple things across the same dimensions.

Good uses:

- X vs Y;
- symptom vs likely cause;
- technique vs problem solved;
- option vs trade-off;
- terminology vs meaning;
- scenario vs preferred decision.

Prefer prose or bullets when there is no meaningful comparison structure.

Avoid large tables filled with paragraph-length cells.

## Blockquotes

Use blockquotes sparingly for a rule, principle, or conclusion that deserves to stand apart.

Example:

```markdown
> A cache is useful only when the cost of stale data is acceptable for that use case.
```

Do not use blockquotes as decorative callouts.

## Mermaid diagrams

Use Mermaid when the relationship is easier to understand visually than through prose alone.

Strong uses include:

- architecture or component relationships;
- request/data flow;
- ordered interactions;
- state transitions;
- causal or process flows;
- simple quantitative comparisons when a chart is clearer than a table.

Use the simplest diagram that communicates the idea.

One diagram should answer one main question.

Do not add a diagram when:

- one sentence explains the relationship clearly;
- the diagram simply repeats the prose;
- the source does not establish the relationships confidently;
- the diagram becomes more complex than the concept.

Choose the diagram type by intent:

- `flowchart` → structure, relationships, process or data flow;
- `sequenceDiagram` → who interacts with whom and in what order;
- `stateDiagram-v2` → lifecycle or state transitions;
- `xychart` / `xychart-beta` → lightweight numeric comparisons or trends.

Keep labels concise and human-readable.

Do not use elaborate styling merely to make the file look polished.

---

# Comparisons and Distinctions

When concepts are easy to confuse, explicitly distinguish them.

A compact table is often useful:

```markdown
| Concept | Main purpose | Main trade-off |
|---|---|---|
| A | ... | ... |
| B | ... | ... |
```

Do not create comparison tables for concepts that are not meaningfully comparable.

Sometimes one sentence is enough:

> A connection pool limits concurrent database connections; a read replica increases read capacity. They solve different bottlenecks.

Prefer the smallest form that makes the distinction clear.

---

# Practicality

Lessons should usually emphasize what helps the reader reason or act.

When relevant, prioritize:

- what problem this solves;
- what symptom suggests it;
- why it works;
- what it costs;
- when to use it;
- when not to use it;
- what commonly goes wrong;
- what alternatives differ in an important way.

Do not force these dimensions into topics where they are not useful.

Avoid exhaustive implementation trivia unless implementation itself is the lesson.

Prefer durable understanding over version-specific detail when both teach the same thing.

---

# Tone and Style

Write in plain, direct language.

Prefer:

> A read replica can serve stale data because replication takes time.

over:

> The system introduces a subtle temporal gap that may occasionally surface as stale state.

Use technical precision without unnecessary formality.

Avoid:

- mannered prose;
- decorative metaphors;
- rhetorical filler;
- excessive transitions;
- repeated conclusions;
- fake quotations;
- unnecessary adjectives;
- vague claims such as "very powerful" without explaining why.

Use examples or analogies only when they improve clarity.

---

# Source Distillation

Do not preserve the source's presentation mechanics.

Remove or heavily compress:

- repeated explanations;
- introductions that exist mainly to build suspense;
- sponsor or promotional material;
- calls to action;
- jokes that do not teach;
- conversational filler;
- tangents;
- redundant examples;
- trivia;
- implementation detail outside the lesson's scope.

Preserve source-specific details when they materially improve understanding.

Do not aim for coverage.

Aim for the highest-value understanding.

---

# Simple Workflow

Keep the process lightweight.

1. **Understand the material and identify the highest-value learning.**
2. **Choose one or more coherent lesson boundaries.**
3. **Write takeaways first, then an adaptive explanation using only useful Markdown features.**
4. **Tighten the result: remove low-value material while preserving important reasoning and nuance.**

Do not create elaborate scoring systems, editorial matrices, or multi-stage analysis unless the user explicitly asks for them.

---

# Quality Check

Before finishing, check:

- Can the reader understand the main point from the takeaways?
- Does each lesson teach one coherent unit?
- Are the most important terms named accurately?
- Is the reasoning sufficient to understand why the conclusions are true?
- Are important conditions and trade-offs preserved?
- Did low-value material get removed?
- Are examples, tables, diagrams, and formatting earning their space?
- Could anything be deleted without materially reducing understanding?

If yes, delete it.

The result should feel concise because unnecessary material is gone, not because the useful explanation was compressed beyond clarity.

---

# Non-Goals

This skill is not responsible for automatically creating:

- quizzes;
- flashcards;
- spaced-repetition cards;
- mind maps;
- recall exercises;
- study schedules;
- exhaustive source summaries;
- full transcripts;
- rigid lesson templates;
- decorative diagrams;
- knowledge-base curation or storage workflows;
- provenance systems;
- citations unless requested or needed by the task.

It may support those activities later, but the Markdown lesson itself should remain a clear, compact explanation for human reading.

---

# Final Standard

A strong lesson should let the reader quickly answer:

- What are the important takeaways?
- What is the correct mental model?
- What are the important terms?
- Why does this work or happen?
- What conditions, trade-offs, distinctions, or failure modes matter?
- What should I remember after I close the file?

The skill succeeds when the lesson delivers most of the useful learning value with substantially less reading than the original material, while remaining accurate, practical, and easy to understand.
