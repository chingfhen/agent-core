---
name: mermaid-markdown
description: Creates clear Mermaid diagrams for already-understood systems, processes, and relationships, and inserts them directly into the user's chosen Markdown file. Clarifies the intended diagram when necessary; does not perform architecture or planning work.
disable-model-invocation: true
license: MIT
---

# Mermaid Markdown

## Purpose

Draw the diagram the human actually wants to understand, then implant it directly into the Markdown file where it belongs.

The goal is communication, not completeness.

This is a supporting skill. It visualizes understanding and decisions that already exist. It does not perform architecture design, planning, or alternative evaluation.

> Draw the diagram the human actually wants to understand.

> The simplest diagram that communicates that clearly is the correct diagram.

---

# When To Use

Use this skill when the user explicitly wants a Mermaid diagram added to or updated in a Markdown file.

Examples:

- "Add an architecture diagram to this task."
- "Put the worker flow into `docs/architecture.md`."
- "Add a Mermaid diagram showing how this request works."
- "Diagram the job lifecycle in this plan."
- "Update the diagram in this Markdown."
- "Add a diagram here."

The normal output is a Mermaid fenced block directly inside the target `.md` file:

````markdown
```mermaid
flowchart LR
    User --> API
    API --> Worker
    Worker --> Database
`````

`````

Do not create a separate `.mmd`, `.svg`, image, or `diagrams/` artifact unless the user explicitly asks for one.

---

# Boundary: Visualize, Do Not Design

This skill runs after the relevant system, workflow, or plan is understood well enough to visualize.

It may inspect relevant tasks, docs, plans, repository files, or implementation evidence to understand what should be drawn.

It must not use diagram generation as an excuse to redesign the underlying system.

Do not:

- choose a new architecture;
- reopen settled architecture decisions;
- evaluate competing implementation approaches;
- invent missing system behavior;
- change responsibilities or boundaries merely to improve the diagram;
- expand into general planning.

If the source material reveals a material contradiction or missing relationship, surface it instead of silently resolving it in the diagram.

A diagram must not look more certain than the evidence behind it.

---

# Clarify The Diagram When Needed

A request for "a diagram" may have many valid interpretations.

The same system could reasonably have:

- a system/component overview;
- an end-to-end process flow;
- a request or job sequence;
- a state lifecycle;
- a deployment view;
- a data flow;
- a specific subsystem diagram.

The skill's first responsibility is therefore to understand:

> **What does the human want this diagram to make clear?**

Infer this from the request and surrounding Markdown when it is obvious.

If materially unclear, ask a concise question before drawing.

Examples:

> "What would you like this diagram to make clear: the overall architecture, the end-to-end job flow, or a specific subsystem?"

> "Do you want the component relationships or the runtime sequence?"

Also clarify the target Markdown file when the destination is genuinely unknown.

## Clarification rules

- Ask only when the unresolved ambiguity could materially change the diagram.
- Ask one useful question at a time.
- Do not turn diagram clarification into a planning session.
- Do not ask the user to choose Mermaid syntax when the skill can choose it.
- Stop asking once there is enough information to draw the intended diagram.

The human decides what they want to understand.

The skill decides how Mermaid should express it.

---

# Ground The Diagram

Before drawing, inspect enough relevant source material to represent the subject accurately.

Prefer existing truth such as:

- the target Markdown file;
- approved plans;
- current task files;
- architecture or design docs;
- relevant implementation files;
- existing diagrams that the new diagram must remain consistent with.

Use only as much investigation as is needed for the requested diagram.

This is a lightweight supporting task, not an exhaustive repository audit.

Do not represent an uncertain edge, component, state, or interaction as established fact.

---

# Choose The Diagram Type By Intent

Prefer Mermaid's simplest suitable diagram type.

## `flowchart`

Use for:

- system/component relationships;
- architecture overviews;
- data flow;
- process/workflow progression;
- deployment shape;
- dependency relationships.

Use `subgraph` when meaningful boundaries or groups improve understanding.

For structural diagrams, arrows represent relationships, dependencies, calls, or data movement as labelled.

For process flowcharts, arrows may represent progression through the process.

## `sequenceDiagram`

Use when the important question is:

> Who interacts with whom, in what order?

Good for:

- request handling;
- async job execution;
- authentication flows;
- callbacks/webhooks;
- retries;
- multi-service interactions.

Use Mermaid constructs such as `alt`, `opt`, `loop`, and responses when they genuinely improve the explanation.

## `stateDiagram-v2`

Use when the important information is lifecycle or allowed state transitions.

Good for:

- jobs;
- sessions;
- subscriptions;
- workflows;
- processing states.

## Other Mermaid types

Use more specialized types when they clearly communicate the requested information better, for example:

- `erDiagram` for entity/data relationships;
- `classDiagram` for class or type structure.

Prefer broadly supported Mermaid syntax.

Do not reach for experimental or unusually renderer-dependent syntax unless it offers a material benefit.

---

# Diagram Design

## One Diagram, One Main Question

Every diagram should have an obvious reason to exist.

Avoid combining several independent questions into one canvas.

If a reader has to understand architecture, execution order, deployment, and state transitions simultaneously, separate them.

Split a diagram when:

- it has multiple competing reading paths;
- relationships become hard to trace;
- unrelated abstraction levels are mixed;
- edge crossings or density materially hurt comprehension;
- it is answering more than one important question.

Do not split merely because a fixed node count has been exceeded.

---

## Use The Right Abstraction

Show what matters for the question being answered.

Usually include:

- major components;
- major relationships;
- meaningful boundaries;
- important data or control movement;
- relevant decisions or states.

Usually exclude:

- every source file;
- every class;
- every helper function;
- every API endpoint;
- configuration trivia;
- implementation detail that does not improve the reader's mental model.

Do not mix abstraction levels without a good reason.

---

## Make The Reading Path Obvious

Choose diagram direction intentionally.

Typical defaults:

- `LR` for pipelines, dependencies, and horizontal flows;
- `TD`/`TB` when hierarchy or vertical progression reads more naturally.

Prefer layouts where the main path is visually easy to follow.

Avoid unnecessary edge crossings.

Use subgraphs and ordering to reflect real conceptual grouping rather than merely making the diagram symmetrical.

---

## Labels

Use human-readable names.

Prefer:

- `Video Worker`
- `Job Queue`
- `Supabase`
- `Blob Storage`

over implementation identifiers such as:

- `VideoGenerationOrchestratorServiceV2`
- `supabase_prod_db_01`

Use implementation names only when those names are themselves important to the reader.

Keep node labels concise.

Edge labels should explain the relationship or payload when that information matters.

Prefer:

```text
API -->|enqueue job| Queue
Worker -->|store result| Blob
```

over long sentences on the canvas.

---

## Visual Language

Prefer Mermaid's normal visual language and minimal styling.

Do not invent elaborate house conventions for:

- colors;
- line thickness;
- arrow styles;
- custom shapes.

If a visual distinction carries meaning, make that meaning obvious and use it consistently.

Prefer explicit labels and the semantics of the chosen Mermaid diagram type over relying on subtle styling.

The diagram should remain understandable in different themes and renderers.

---

# Markdown Integration

The Markdown document is the normal source of truth for the diagram.

Insert the Mermaid block where it provides the most useful context rather than simply appending it to the end of the file.

Preserve the document's:

- heading structure;
- writing style;
- terminology;
- existing organization.

A diagram may be preceded or followed by a short sentence when that materially helps the reader understand its purpose.

Do not add verbose explanation merely because a diagram was inserted.

Example:

````markdown
## Job Processing

Generation jobs are processed asynchronously through the worker queue.

```mermaid
flowchart LR
    API["API"] -->|enqueue job| Queue["Job Queue"]
    Queue -->|dispatch| Worker["Video Worker"]
    Worker -->|generate| Provider["Video Provider"]
    Worker -->|store result| Storage["Blob Storage"]
```
`````

---

# Accessibility

For non-trivial diagrams, add a concise accessible title and description when supported by the Mermaid syntax being used.

Example:

```mermaid
flowchart LR
    accTitle: Video generation job flow
    accDescr: The API places a job on the queue, a worker processes it using the video provider, and the result is stored.

    API --> Queue
    Queue --> Worker
    Worker --> Provider
    Worker --> Storage
```

The description should summarize the information conveyed by the diagram, not reproduce every node and edge.

---

# Validation

Before finishing:

1. Check that the Mermaid syntax is internally consistent.
2. Check that the diagram matches the underlying source material.
3. Check that the chosen diagram type matches the question being answered.
4. Check that the main reading path is obvious.
5. Remove information that does not improve understanding.
6. Confirm the diagram was inserted into the intended Markdown file and location.

If the repository already has a Mermaid validation or rendering command, it may be used.

Do not install Mermaid CLI or create a rendering pipeline solely for this skill.

Native Markdown Mermaid rendering is the normal workflow.

---

# Quality Bar

A successful diagram lets the reader quickly answer the question it was created for.

The reader should be able to tell:

* what they are looking at;
* where to start;
* what the important elements are;
* how those elements relate;
* what the main flow or structure is.

The diagram should not require chat history to decode it.

If the result looks impressive but the reader still cannot quickly form the intended mental model, simplify it.

---

# Non-Goals

This skill is not responsible for:

* architecture design;
* project planning;
* requirements discovery beyond diagram intent;
* alternative evaluation;
* implementation decisions;
* exhaustive repository analysis;
* opportunistically diagramming unrelated work;
* maintaining a standalone diagram library;
* generating SVG or image derivatives;
* installing Mermaid tooling;
* elaborate visual design systems.

It is a small supporting skill:

> understand which diagram the human wants → ground it in existing truth → draw the clearest useful Mermaid diagram → insert it into the desired Markdown.

