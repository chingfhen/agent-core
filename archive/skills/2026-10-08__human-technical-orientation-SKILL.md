---
name: human-technical-orientation
description: Use when the user needs to understand a technical topic, system, repository change, configuration, error, architecture, or agent output well enough to reason about it and supervise further work. Build the minimum sufficient technical map using concrete evidence, real system anchors, and whatever explanatory structure best fits the topic.
---

# Human Technical Orientation

## Purpose

Help the human develop a usable understanding of what is happening.

Do not merely translate technical language into simpler language.

Expose enough of the real system that the human can:

```text
understand the behaviour
        ↓
locate the important parts
        ↓
reason about changes and consequences
        ↓
supervise an agent working on it
```

The goal is the **minimum sufficient technical map**.

Not a full tutorial.

Not a shallow summary.

Not a fixed response format.

## Core Principle

Optimize for:

```text
compression without hiding the mechanism
```

A simplified explanation is useful only when it preserves the parts that matter.

Do not replace concrete details such as routes, tables, paths, permissions, environment variables, services, or state transitions with vague labels such as:

```text
the backend
the database
the cloud
the model
the system
```

Use the real names when they are known and relevant.

## What the Human Should Understand

For every topic, determine which pieces of understanding would give the human genuine leverage.

The human does not need every detail. They normally need enough to answer some combination of these questions:

```text
What is this?

Why does it exist?

How does it actually work?

What enters it and what comes out?

Which services, files, tables, paths, or settings are involved?

Where does state live?

What controls the behaviour?

Where can I inspect or change it?

What depends on it?

What assumptions must remain true?

How can it fail?

What remains unverified?
```

Do not answer every question mechanically.

Select the questions that matter for the topic.

## Orient Around Leverage

Prefer details that help the human:

* predict behaviour;
* locate implementation;
* trace data or control flow;
* understand ownership and boundaries;
* identify configuration and permissions;
* recognize important dependencies;
* know where to inspect, modify, test, or debug;
* evaluate whether an agent's proposed change makes sense.

Deprioritize details that merely demonstrate technical sophistication.

## Choose the Right Explanatory Lens

Different topics require different mental models.

Select one or more lenses based on what best exposes the mechanism.

### Topology

Use when the important question is what exists and how resources are arranged.

```text
Singapore Region
└── VPC: 10.0.0.0/16
    ├── Public subnet:  10.0.1.0/24
    │   └── ALB
    └── Private subnet: 10.0.2.0/24
        └── EC2 worker
```

Topology is useful for:

* infrastructure;
* repository layout;
* service architecture;
* storage hierarchy;
* model artifact structure.

### Flow

Use when the important question is how work or data moves.

```text
Browser → API → jobs table → queue → worker → S3 result
```

Flow is useful for:

* request handling;
* data pipelines;
* authentication;
* payments;
* model inference;
* event-driven systems.

### State Machine

Use when behaviour depends on status and transitions.

```text
queued → running → completed
          ↓
        failed → retry
```

State machines are useful for:

* jobs;
* subscriptions;
* deployments;
* approval workflows;
* retries;
* model lifecycle.

### Control Surface

Use when the important question is what changes or restricts behaviour.

```text
Environment variables ─┐
Config file ────────────┼─→ runtime behaviour
IAM policy ─────────────┤
Database settings ──────┘
```

Control surfaces include:

* environment variables;
* configuration fields;
* permissions;
* IAM policies;
* feature flags;
* model URIs;
* CLI arguments;
* request parameters;
* table values.

### Trace

Use when the human needs to know where to follow execution.

```text
POST /jobs
    ↓
create_job()
    ↓
jobs table
    ↓
queue message
    ↓
worker.process_job()
```

A trace should connect runtime behaviour to concrete implementation locations.

### Data Map

Use when the important question is what data exists and where it lives.

```text
Uploaded image
    ↓
S3: users/{user_id}/uploads/{asset_id}.png

Metadata
    ↓
user_image_assets table

Processing status
    ↓
jobs table
```

Use exact tables, prefixes, schemas, or artifact paths when known.

### Boundary Map

Use when the important question is responsibility, trust, or isolation.

```text
User-controlled input
        │
        ▼
API validation
        │ trusted internal object
        ▼
worker
```

Boundary maps are useful for:

* authentication;
* authorization;
* network boundaries;
* external integrations;
* package interfaces;
* model compatibility;
* ownership checks.

### Before and After

Use when explaining a change.

```text
Before:
API performs inference and waits

After:
API creates job → worker performs inference → client polls status
```

Show only the change that alters the mental model.

### Concrete Example

Use when an abstract explanation would remain difficult to apply.

```text
s3://einstein-artifacts/
└── vision_deepfake/
    ├── embedding_models/
    └── classifier_head/
        └── run=20260319_035513_bq38k/
            └── best_model.pt
```

The example should expose the real naming, hierarchy, or behaviour.

## Structure Must Follow the Topic

Do not impose a standard response template.

Choose the structure that produces the clearest mental map.

Possible forms include:

* a short explanation followed by one code excerpt;
* an annotated configuration block;
* an ASCII architecture map;
* a before-and-after comparison;
* a runtime trace;
* a table of resources and responsibilities;
* a walkthrough of one request;
* a state transition diagram;
* a repository navigation guide;
* a layered explanation from concept to concrete implementation;
* a direct interpretation of an agent's output.

Headings are optional.

Use them only when they improve navigation.

Do not add sections merely because the skill contains a corresponding concept.

## Start From the Most Revealing Thing

Plain English is often useful, but it is not always the best starting point.

Start with whichever element gives the human the fastest accurate orientation.

Examples:

For an unfamiliar concept:

```text
plain-English mechanism → visual → concrete example
```

For configuration:

```text
actual config → line-by-line meaning → runtime consequence
```

For architecture:

```text
system map → responsibilities → important boundaries
```

For an error:

```text
failure evidence → location in flow → likely cause → next inspection point
```

For a repository change:

```text
changed behaviour → changed files → affected resources → verification path
```

For an API route:

```text
route signature → authentication → side effects → persisted state
```

## Use Concrete Technical Anchors

Small pieces of actual technical material often teach more than another paragraph of abstraction.

Useful anchors include:

* code excerpts;
* configuration;
* environment variables;
* API routes;
* table and column names;
* S3 paths;
* filenames;
* commands;
* logs;
* schemas;
* function signatures;
* queue names;
* IAM actions;
* deployment resources;
* model artifact URIs.

Use anchors when they show:

```text
where the behaviour begins
what controls it
what resource it touches
what assumption it relies on
what evidence supports the explanation
```

### Example: Configuration

```jsonc
"mcp": {
  "supabase-dev": {
    "type": "remote",
    "url": "https://mcp.supabase.com/mcp?project_ref=...&read_only=true",
    "enabled": true
  }
},
"permission": {
  "supabase-dev_*": "ask"
}
```

The important understanding is not merely:

```text
The agent connects to Supabase.
```

It is:

```text
supabase-dev
    = the local name OpenCode gives this MCP server

type: remote
    = OpenCode connects to a server over a URL rather than launching it locally

project_ref=...
    = selects the Supabase project

read_only=true
    = asks the server to expose read-only behaviour

supabase-dev_*
    = every tool exposed through this named MCP connection

ask
    = require human approval before each matching tool call
```

This gives the human a concrete control map.

### Example: API Route

```python
@app.post(
    "/assets/images",
    response_model=UserImageAssetUploadResponse,
    status_code=201,
)
```

Useful interpretation:

```text
POST /assets/images
    = client entry point for creating an image asset

UserImageAssetUploadResponse
    = the response contract

201
    = successful creation of a new resource
```

The function body may then reveal where metadata and files are stored.

### Example: Dependency Injection

```python
user_id: str = Depends(require_authenticated_user)
```

Useful interpretation:

```text
The route does not trust a user_id supplied directly by the caller.

FastAPI resolves the authenticated identity through
require_authenticated_user.
```

### Example: Environment Variable

```env
CLASSIFIER_MODEL_S3_URI=s3://einstein-artifacts/vision_deepfake/classifier_head/run=20260319_035513_bq38k/best_model.pt
```

Useful interpretation:

```text
Application starts
    ↓
reads CLASSIFIER_MODEL_S3_URI
    ↓
loads this classifier artifact
    ↓
uses it instead of the library default
```

The path also reveals:

```text
bucket:
einstein-artifacts

system:
vision_deepfake

artifact type:
classifier_head

training run:
run=20260319_035513_bq38k

selected file:
best_model.pt
```

## Explain Snippets, Do Not Merely Display Them

A snippet is useful only when the explanation connects syntax to behaviour.

For each included excerpt, explain the symbols that materially affect understanding.

Do not explain obvious punctuation or boilerplate.

Do not dump large files and expect the human to infer the important lines.

Prefer excerpts that are small enough to hold in working memory.

Usually:

```text
2–15 lines
```

Use more only when the surrounding structure is necessary.

## Reveal Human Entry Points

In AI-managed codebases, the human needs to know where to regain control.

When relevant, identify:

```text
Where do I inspect this?

Where do I change it?

Where do I run it?

Where do I observe its output?

Where do I debug failure?

Where is the persisted state?

Which setting changes behaviour?

Which file is the source of truth?
```

Examples:

```text
Inspect API entry point:
app/api/routes/jobs.py

Inspect job state:
jobs table

Change selected model:
CLASSIFIER_MODEL_S3_URI

Inspect generated artifact:
s3://einstein-artifacts/.../best_model.pt

Observe worker failure:
CloudWatch log group /ecs/deepfake-worker

Test the route:
POST /jobs/{job_id}/download-url
```

Do not invent locations.

Use exact paths only when supported by evidence.

## Preserve Important Technical Detail

Do not classify all implementation detail as unnecessary.

A detail is important when it changes the human's ability to reason about:

* system behaviour;
* cost;
* security;
* compatibility;
* ownership;
* failure;
* deployment;
* data location;
* model selection;
* change impact.

Examples of details that are often worth preserving:

```text
The exact S3 prefix used

Which table owns the status

Whether the API writes directly or publishes a queue message

Whether identity comes from authentication or request input

Whether a permission is read-only, approval-gated, or both

Which environment variable overrides a default

Whether a classifier head must match a specific embedding space

Whether a subnet is public because of its route table, not its name
```

## Make Relationships Explicit

Do not present isolated facts when the relationship is the important part.

Weak:

```text
There is an API, a queue, and a worker.
```

Better:

```text
API creates the job
        ↓
queue carries the job ID
        ↓
worker reads the job and performs inference
        ↓
jobs table stores the final status
```

Weak:

```text
There is an adapter and a classifier.
```

Better:

```text
DINOv3 + LoRA adapter → adapted embedding space → matching classifier head
```

The human should understand why the pieces belong together.

## Use Visuals Opportunistically

Use a visual when it compresses relationships more effectively than prose.

Do not add a visual merely because the skill encourages visuals.

Possible visual forms include:

```text
hierarchies
flows
state transitions
before/after views
boundaries
data locations
control relationships
dependency chains
failure paths
```

Keep visuals small enough to interpret immediately.

Prefer meaningful labels over decorative boxes.

Use technical names where they matter.

### Hierarchy

```text
AWS Account
└── Singapore Region
    └── VPC: 10.0.0.0/16
        ├── Public subnet: 10.0.1.0/24
        └── Private subnet: 10.0.2.0/24
```

### State

```text
created → queued → running → completed
                      │
                      └→ failed → retrying
```

### Control

```text
Library default URI
        │
        ├── no environment override → use default
        │
        └── override present → use configured S3 URI
```

### Failure Location

```text
Client → ALB → API → Queue → Worker → S3
                    ✕
             message not published
```

No visual is required when a direct explanation or code excerpt is clearer.

## Progressive Disclosure

Begin with the smallest explanation that preserves the mechanism.

Then add detail only where it improves the user's ability to reason.

A useful progression is often:

```text
basic shape
    ↓
real components
    ↓
concrete anchor
    ↓
important boundary or control
```

Do not front-load every caveat.

Do not hide important caveats that would materially change the interpretation.

## Distinguish Knowledge Levels

Make it clear what is known and what is inferred.

Use natural wording such as:

```text
Confirmed from the configuration:

Likely based on the route signature:

The function body would need to be inspected to confirm:

This is the general mechanism; the repository-specific behaviour is not yet verified:
```

Evidence priority:

```text
actual code, config, logs, or schema
        ↓
named resource or documented behaviour
        ↓
strong inference from surrounding evidence
        ↓
generic technical explanation
```

Never present a generic explanation as confirmed repository behaviour.

## Identify the Main Misunderstanding

When useful, explicitly contrast the correct model with the likely mistaken one.

Examples:

```text
This is approval gating, not the source of read-only enforcement.

The subnet is not public because it has “public” in its name.
It is public because its route table reaches an Internet Gateway.

The S3 URI does not contain the model itself in configuration.
It tells the application where to retrieve the model.

The API route signature proves the endpoint exists.
It does not yet prove what database or storage operations happen inside it.
```

Use this only when a misunderstanding is genuinely likely.

## Decide What to Omit

Omit details that do not improve the current mental map.

Commonly safe to omit:

* boilerplate imports;
* complete response schemas;
* internal library implementation;
* every database column;
* every deployment setting;
* all possible failure modes;
* historical context;
* alternatives that are not under consideration.

But do not omit a detail merely because it is technical.

The test is:

```text
Would knowing this materially improve the human's ability to understand,
locate, supervise, change, or debug the system?
```

If yes, include it.

## Adapt Depth to the Request

### Fast orientation

Give the basic mechanism, concrete components, and one or two important anchors.

### Learning explanation

Build the mental model progressively and explain why the pieces relate.

### Agent-output interpretation

Translate the agent's claims into:

```text
what changed
where it changed
what behaviour results
what remains unverified
```

### Repository orientation

Prioritize:

```text
entry points
source-of-truth files
runtime flow
tables and storage
configuration
deployment
debugging locations
```

### Error orientation

Prioritize:

```text
where the failure occurs
what evidence says
which boundary was crossed
what to inspect next
```

### Architecture orientation

Prioritize:

```text
components
responsibilities
flows
state locations
trust boundaries
operational control points
```

### Configuration orientation

Prioritize:

```text
actual fields
how matching works
who enforces the setting
runtime consequences
override behaviour
```

## Avoid These Failure Modes

### Oversimplified summary

```text
This gives the agent safe database access.
```

This hides how the connection, scope, permission, and approval actually work.

### Code dump

Showing an entire file without identifying the few lines that explain the behaviour.

### Forced format

Producing the same headings regardless of whether the topic is networking, model loading, API design, or an error log.

### Analogy without mechanism

An analogy may introduce the idea, but it must not replace the real technical explanation.

### Vocabulary substitution

Replacing technical nouns with vague words rather than teaching the relevant nouns.

### Exhaustive tutorial

Explaining everything associated with a topic instead of the subset needed to orient the human.

### False certainty

Describing uninspected repository behaviour as though it were confirmed.

### Visual clutter

Using several diagrams when one relationship is the only thing the human needs to see.

## Completion Test

Before finishing, check whether the explanation gives the human enough leverage.

They should understand the relevant parts of:

```text
shape
mechanism
real components
important data or state
control points
human entry points
boundaries
uncertainty
```

Not every category must appear.

The explanation is complete when the human can reasonably say:

```text
I understand what this does.

I can see how the important pieces connect.

I know where the behaviour comes from.

I know where I would inspect or change it.

I know which details matter and which can wait.
```
