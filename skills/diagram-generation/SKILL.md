---
name: diagram-generation
description: Creates Mermaid diagrams (flowcharts, sequence diagrams, state machines) as source-controlled .mmd files under diagrams/.
disable-model-invocation: true
license: MIT
---

# Diagram Generation

Purpose:

Transform complex systems, workflows, and codebases into clear diagrams that
help humans understand the system.

The goal is communication, not completeness.

This skill is user-invoked only. Create a diagram when explicitly asked for
one. Do not produce a diagram as a side effect of unrelated work — if one
would help, say so in your response and wait for the user to ask.

---

# Core Principle

A diagram is a compression mechanism.

Do not attempt to represent every implementation detail.

Show:

* major components
* major dependencies
* major data flow
* major control flow

Avoid:

* every function
* every class
* every API endpoint
* every configuration value
* every implementation detail

If a diagram becomes difficult to read, split it.

---

# Output Location And Naming

All diagram output lives under the dedicated top-level `diagrams/` folder, the same way `tasks/` and `docs/` are dedicated folders. Never write diagram source into `docs/`.

File name: `diagrams/YYYY-MM-DD__kebab-case-name.mmd`. The date is an **immutable creation date**, matching the `tasks/` convention — it tells a human at a glance which diagrams are recent and which are stale, without opening the file.

Structure inside `diagrams/` beyond the root is the executing agent's call. Default to flat. Only introduce subfolders when the number of diagrams genuinely makes flat hard to scan, or when the user explicitly asks for a specific structure — in that case, follow exactly what was asked.

Render an `.svg` alongside the source whenever `mmdc` is on `PATH` (see Tooling). Never let a missing renderer block producing the `.mmd` source — the source is the deliverable. When an existing `.mmd` file is updated, re-render its `.svg` immediately so the two never drift.

---

# Tooling

Mermaid is the only diagram tool this skill uses.

D2 was evaluated — nicer default layout for very large architecture
diagrams — but it has no native rendering anywhere (always needs the CLI run
before anyone sees a picture) and a rougher install. It's deferred to the
backlog; don't reach for it unless the user explicitly asks for it again.

**Setup, in order:**

1. Check first: run `mmdc --version`. If it prints a version, skip straight to rendering.
2. If missing, install once:
   ```
   npm install -g @mermaid-js/mermaid-cli
   ```
   This pulls its own Chromium via Puppeteer on first install (~50s, one-time, fully automatic). Works the same on Windows, macOS, and Linux — no extra flags or fallback steps needed.
3. If `npm`/`node` themselves aren't installed, that's a prerequisite outside this skill's scope — tell the user rather than trying to install Node yourself.

**Render a diagram** (after writing the `.mmd` source):

```
mmdc -i diagrams/YYYY-MM-DD__name.mmd -o diagrams/YYYY-MM-DD__name.svg
```

---

# Diagram Types

Pick the Mermaid diagram type by intent:

* **flowchart** — components, relationships, architecture, workflows. Use `subgraph` blocks to group related components (e.g. one subgraph per service boundary) when you need the kind of grouping a container-based tool would show.
* **sequenceDiagram** — time-ordered interactions between actors or services.
* **stateDiagram-v2** — lifecycle and state transitions.

Split into multiple diagrams once a single diagram exceeds ~15 nodes. Never produce one giant diagram by default.

---

# Diagram Design Rules

## One Diagram = One Concern

Good:

* system-overview.mmd
* video-generation-workflow.mmd
* job-lifecycle.mmd

Bad:

* complete-system-everything.mmd

---

## Layering

Prefer layered diagrams.

Example:

Architecture:

1. System Overview
2. Video Generation Subsystem
3. Billing Subsystem
4. Deployment Topology

Instead of:

1. Massive Everything Diagram

---

## Naming

Use human-readable labels.

Prefer:

"Video Generation Worker"

Instead of:

"VideoGenerationOrchestratorServiceV2"

Prefer:

"Supabase"

Instead of:

"supabase_prod_db_01"

---

## Structural vs Behavioral — Don't Mix

A flowchart shows topology: which components exist and who calls whom. It does not show order.

A sequenceDiagram shows order: who calls whom, and when, including loops and branches.

Do not add ordering claims to a flowchart. A numbered edge label (`1. do X`, `2. do Y`) is an order claim. If a flowchart needs order, that's a sign the content belongs in a sequenceDiagram instead, where `loop` and `alt` blocks express it correctly.

If a flowchart's layout itself implies an order it doesn't have (`flowchart LR` reads left-to-right as "first to last"), either keep left-to-right strictly chronological, or accept that this diagram doesn't claim order and let a sequence diagram own that question.

---

# Visual Language

A diagram's visual encoding — line style, color, numbering — is itself information. Each encoding choice must carry exactly one meaning, declared once per diagram, and reused consistently. Never let one style mean two different things in the same diagram.

## Line Styles

Pick a small, fixed set of line styles before drawing, and make sure each one's meaning is recoverable from the diagram itself (a legend, or labels that make the distinction obvious). A common pattern for call-based diagrams:

* solid arrow (`-->`) — a call that happens once
* thick solid arrow (`==>`) — a call that repeats (polling, retries) until a condition resolves
* dotted arrow (`-.->`) — asynchronous / out-of-band, not on the primary path being traced

This is one example, not a mandate — the right vocabulary depends on what the diagram shows. What's not optional: three styles or fewer, one meaning each, never reused for a second meaning in the same diagram. If a diagram needs a fourth distinct call semantic, split the diagram rather than growing the line vocabulary.

## Color / Fill Legend

When using fills/colors to categorize nodes, render the legend inside the diagram itself — a small `Legend` subgraph or note with one labeled, colored swatch per category — rather than leaving the meaning only in chat history or an external doc. A reader should be able to decode the diagram without having seen the conversation that produced it.

Define categories that fit the content of that specific diagram (by layer, by ownership, by trust boundary — whatever distinction matters there) rather than reusing another diagram's palette by default. A network diagram, a data model, and a state machine each need their own category set.

Never reuse a color to mean "this part was wrong" or "this part changed" in a diagram meant as a durable reference — that meaning rots the moment the context that motivated it is forgotten. A "what changed" diagram is a different, disposable diagram type, not the reference diagram.

## Edge and Node Text

* Node text: name + one-line role, not a procedural description of what it does internally.
* Edge text: verb + key payload, five words or fewer. Full sentences belong in chat or a doc, not on the canvas.

## Numbering vs. Trigger Conditions

Don't number edges in a flowchart to show order — that's a sequence diagram's job (see Structural vs Behavioral, above). Partial numbering (some edges numbered, most not) is worse than none: it implies a complete ordering that isn't there.

If an edge's firing depends on something else happening first, say so in that edge's own label instead of numbering it — e.g. `runs once upstream check passes` rather than `2. run check`. This expresses a local precondition (real structural information) without making a global step-count claim the diagram type can't back up.

---

# Mermaid Guidelines

## Flowcharts (architecture and workflows)

Preferred for components, relationships, and process steps.

Example — architecture:

```
flowchart LR
  subgraph Frontend
    UI[Vercel Frontend]
  end
  subgraph Backend
    API[FastAPI API]
    Queue[Job Queue]
    Worker[Video Worker]
  end
  Blob[Azure Blob Storage]

  UI --> API --> Queue --> Worker --> Blob
```

Example — workflow:

```
flowchart LR
  User --> Upload
  Upload --> Plan
  Plan --> Generate
  Generate --> Package
  Package --> Deliver
```

---

## Sequence Diagrams

Preferred when explaining execution order.

```
sequenceDiagram
  User->>API: Create Job
  API->>Queue: Enqueue Job
  Queue->>Worker: Dispatch
  Worker->>Provider: Generate Video
  Provider-->>Worker: Result
  Worker-->>User: Complete
```

---

## State Machines

Preferred when describing lifecycle transitions.

```
stateDiagram-v2
  Draft --> Queued
  Queued --> Running
  Running --> Completed
  Running --> Failed
```

---

# Output Expectations

Generate `.mmd` source under `diagrams/` (see Output Location And Naming).

Do not generate screenshots.

Do not use browser automation.

Do not manually draw diagrams.

Preferred outputs:

* .mmd
* .svg (optional, see Tooling)

Diagram source should remain editable and version-controlled.

---

# Diagram Checklist

Before finalizing any diagram:

* Are all major components/relationships represented (if structural)?
* Is the start visible, and the end visible (if it's a process)?
* Are decision points visible?
* Is the sequence or relationship unambiguous?
* Is the diagram understandable in under 30 seconds, without asking questions?
* Does every line style and color carry exactly one meaning, declared in a legend?
* Are structural (topology) and temporal (order) information kept in separate diagrams, with no numbering smuggled into the structural one?

If not, simplify.

---

# Examples

User:

"Draw AdReadyClips architecture."

Expected:

diagrams/2026-06-22__adreadyclips-overview.mmd (flowchart with subgraphs)

---

User:

"Explain the video generation process."

Expected:

diagrams/2026-06-22__video-generation-workflow.mmd

---

User:

"Show the queue processing lifecycle."

Expected:

diagrams/2026-06-22__job-lifecycle-sequence.mmd

---

User:

"Show job states."

Expected:

diagrams/2026-06-22__job-state-machine.mmd

---

The simplest diagram that communicates the idea is the correct diagram.
