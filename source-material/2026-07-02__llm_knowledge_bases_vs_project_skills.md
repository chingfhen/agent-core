---
title: LLM-Maintained Knowledge Bases vs Project Docs and Task Skills
scope: Gather intelligence on Karpathy-style LLM knowledge bases and identify concrete improvements for repo-based coding-agent documentation, task memory, and research workflows.
research_type: Decision Support + Practical Guide
audience: Both human engineer and AI coding agents
generated_on: 2026-07-02
sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://x.com/karpathy/status/2039805659525644595
  - https://obsidian.md/help/web-clipper
  - https://github.com/obsidianmd/obsidian-clipper
  - https://marp.app/
  - https://github.com/marp-team/marp
  - https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-llm-wiki
  - https://arxiv.org/abs/2604.11243
  - https://arxiv.org/abs/2604.12034
---

# Executive Summary

Karpathy's LLM Wiki pattern is a **source-to-wiki compiler**: collect raw documents, let an LLM compile them into durable interlinked Markdown, then use the wiki as a compounding reasoning layer for future Q&A, visualizations, and research outputs. [COMMUNITY]

Your current `project-docs` + `project-tasks` skills are adjacent but not identical:

| Dimension | Karpathy-style LLM Wiki | Your current project-docs / project-tasks |
|---|---|---|
| Primary purpose | Research knowledge compounding | Engineering execution continuity |
| Source layer | `raw/` articles, papers, repos, datasets, images | Repo docs, implementation notes, task bookmarks |
| Compiled layer | Concept/entity wiki pages | Authoritative project documentation |
| Ephemeral layer | Q&A outputs, generated slides/images, new article candidates | `.tasks/` in-flight execution state |
| Human role | Mostly reviews/queries, rarely edits wiki manually | Reviews docs/tasks and uses agent skills to steer coding |
| Agent role | Maintains wiki, backlinks, summaries, health checks | Updates docs/tasks, validates assumptions, preserves implementation state |
| Retrieval | Markdown indexes + summaries; light search; optional CLI | Skill-driven docs lookup, task bookmarks, validation notes |
| Output loop | Answers filed back into wiki | Tasks completed, docs updated, implementation guided |
| Biggest gap | Less strict engineering validation | Less research-ingest / concept synthesis machinery |

Best conclusion: **do not replace your current skills with an LLM Wiki. Add a research-wiki layer beside them.** Your docs/tasks system is good for “what the repo is doing and what work is in flight.” Karpathy’s pattern is better for “what we have learned across sources, decisions, experiments, papers, competitors, and architectural options.”

---

# 1. What the Karpathy Pattern Actually Is

## Core pipeline

```text
raw/
  source documents
  articles
  papers
  repos
  screenshots/images
  datasets
      ↓ LLM incremental compilation
wiki/
  concept pages
  source summaries
  entity pages
  backlinks
  indexes
  synthesis pages
  contradiction notes
      ↓ agent queries / linting / outputs
outputs/
  Q&A reports
  Marp slide decks
  matplotlib charts
  research briefs
  diagrams
      ↓ optional filing
wiki/
  updated synthesis pages
```

Karpathy's public gist describes the LLM Wiki as a copy-pasteable idea file for coding agents such as Codex, Claude Code, OpenCode, or Pi, with the agent expected to build specifics collaboratively. [OFFICIAL/COMMUNITY]

The key move is **compilation**, not storage. Raw inputs are not merely indexed; they are transformed into maintained concept pages, summaries, links, and candidate articles. [COMMUNITY]

## Why this is not just “RAG”

| RAG-style workflow | LLM Wiki workflow |
|---|---|
| Query triggers retrieval every time | Knowledge is compiled once, reused many times |
| Chunks are often contextless | Wiki pages are synthesized and human-readable |
| Vector store is opaque | Markdown is inspectable, git-diffable, and portable |
| Answers often disappear after chat | Useful answers are filed back into the wiki |
| Contradictions are rediscovered repeatedly | Contradictions can become maintained notes/pages |

A Nous Research Hermes skill describes the LLM Wiki pattern as persistent, compounding, interlinked Markdown rather than traditional RAG that rediscovers knowledge per query. [COMMUNITY]

---

# 2. Tooling Signals

## Obsidian as frontend

Obsidian is a Markdown-based personal knowledge base application. The official Obsidian Web Clipper saves web content/highlights into a vault; its GitHub repo emphasizes durable Markdown files that can be read offline and preserved long-term. [OFFICIAL]

Implication for your workflow: Obsidian is not the “database.” It is the **inspection/debugging IDE** for agent-maintained Markdown.

## Web Clipper as ingest helper

Official Obsidian Web Clipper supports browser capture into the vault. This matters because source ingestion is usually the weakest part of LLM wiki workflows: messy HTML, missing images, bad metadata, and link rot. [OFFICIAL]

Recommended source frontmatter:

```yaml
---
title:
source_url:
source_type: article | paper | repo | dataset | image | internal_doc | meeting_note
captured_on:
author:
publisher:
status: raw | summarized | compiled | superseded
tags: []
related_concepts: []
---
```

## Marp as output format

Marp is a Markdown presentation ecosystem. Its official materials describe writing slide decks in Markdown, and the GitHub ecosystem includes CLI conversion into formats such as HTML, PDF, PPTX, and images. [OFFICIAL]

Implication: Marp fits the “LLM writes artifact → human views in Obsidian/preview → optional file-back into wiki” loop.

---

# 3. Comparison Against Your Current Skills

## Current architecture, restated

Based on your existing direction:

```text
project-docs
  durable authoritative Markdown
  validated project knowledge
  canonical implementation decisions

project-tasks
  ephemeral execution memory
  in-flight task bookmarks
  usually under .tasks/
  completion tracked separately from docs

grill-me
  pre-commit / pre-task validation
  surfaces assumptions and risks
  optional validation notes
```

This is stronger than a naive LLM Wiki for engineering work because it separates:

| Layer | Function |
|---|---|
| Durable docs | Canonical truth |
| Task state | Temporary execution continuity |
| Validation | Prevents bad assumptions entering docs/tasks |

## Where Karpathy's pattern is stronger

| Capability | Current skills | LLM Wiki pattern | Gap |
|---|---|---|---|
| Research ingest | Partial/manual | First-class `raw/` ingestion | Add source intake protocol |
| Concept synthesis | Docs may contain concepts, but project-scoped | Core behavior | Add concept/entity pages |
| Backlinks | Not central | Central | Add link map / backlink checks |
| Health checks | `grill-me` validates tasks | Wiki linting finds contradictions, missing info, stale pages | Add wiki health command |
| Visual outputs | Possible but not central | Markdown/Marp/charts are first-class | Add output filing rules |
| Knowledge compounding | Docs improve project state | Q&A outputs enrich research base | Add “file useful answer back” loop |
| Multi-source evidence | Not necessarily explicit | Source summaries + synthesis pages | Add evidence table conventions |

## Where your current setup is stronger

| Capability | Your setup advantage |
|---|---|
| Engineering safety | `grill-me` catches bad assumptions before docs/tasks updates |
| Execution continuity | `.tasks/` explicitly separates work-in-progress from canonical knowledge |
| Repo alignment | Docs map directly to implementation, env vars, APIs, schemas, feature flags |
| Agent operability | Skills are designed for coding-agent workflows, not only reading/research |
| Lower hallucination risk | Authoritative docs require validation before becoming canonical |

Best framing:

```text
Karpathy Wiki = research memory and synthesis layer.
project-docs = canonical engineering truth layer.
project-tasks = execution state layer.
grill-me = quality gate.
```

---

# 4. Recommended New Layer: `project-wiki` Skill

Add a sibling skill, not a replacement.

```text
repo/
  raw/
    sources/
    images/
    papers/
    repos/
  wiki/
    concepts/
    entities/
    decisions/
    source-summaries/
    indexes/
    unresolved/
  docs/
    architecture/
    api/
    deployment/
    runbooks/
  .tasks/
    active/
    completed/
  outputs/
    reports/
    slides/
    charts/
```

## Responsibilities

| Skill | Owns | Should not own |
|---|---|---|
| `project-wiki` | Research synthesis, concept pages, source summaries, backlinks, unresolved questions | Canonical implementation instructions |
| `project-docs` | Stable project docs, architecture, runbooks, API contracts, deployment, env vars | Raw source dumping or speculative research |
| `project-tasks` | Active work state, bookmarks, next actions, implementation progress | Durable conceptual explanations |
| `grill-me` | Assumption checks, contradiction checks, validation questions | Long-form writing |

## Promotion rule

```text
raw source
  → source summary
  → concept/entity synthesis page
  → decision note
  → project-docs update only if implementation-relevant and validated
```

This prevents the wiki from polluting canonical docs with speculative research.

---

# 5. Concrete Skill Behaviors to Implement

## `project-wiki ingest`

Purpose: convert raw documents into source summaries.

Input:

```text
/project-wiki ingest raw/sources/obsidian-web-clipper-note.md
```

Output:

```text
wiki/source-summaries/<slug>.md
```

Template:

```markdown
---
title:
source_url:
source_type:
captured_on:
compiled_on:
confidence: high | medium | low
status: summarized
related_concepts: []
claims:
  - claim:
    evidence:
    relevance:
---

# Summary

# Key Claims

# Useful Details

# Limitations / Biases

# Links to Concepts

# Candidate Follow-up Pages
```

## `project-wiki compile`

Purpose: update concept/entity pages from source summaries.

```text
/project-wiki compile topic="LLM wiki workflows"
```

Behavior:

1. Search relevant source summaries.
2. Update or create concept pages.
3. Add backlinks.
4. Add unresolved questions.
5. Do not alter `docs/` unless explicitly requested.

## `project-wiki ask`

Purpose: answer questions using wiki first, then raw/docs if needed.

```text
/project-wiki ask "How should our project-docs skill change after reading Karpathy's LLM Wiki pattern?"
```

Required output:

```markdown
# Answer
# Evidence
# Tradeoffs
# Recommended Changes
# Files to Update
# Should this be filed back?
```

## `project-wiki file-output`

Purpose: convert useful Q&A into durable wiki content.

```text
/project-wiki file-output outputs/reports/llm-wiki-comparison.md
```

Behavior:

- Extract stable insights.
- Update concept pages.
- Add a backlink to the original output.
- Mark unresolved claims.
- Avoid duplicating entire report unless it is itself a source.

## `project-wiki health-check`

Purpose: lint the wiki.

Checks:

| Check | Description |
|---|---|
| Orphan concepts | Pages with no inbound/outbound links |
| Stale sources | Source summaries not compiled into concepts |
| Contradictions | Claims that conflict across sources |
| Missing provenance | Claims without source links |
| Overgrown pages | Pages too broad and should be split |
| Duplicate concepts | Similar pages that should be merged |
| Promotion candidates | Wiki content that should be moved into `docs/` |
| Research gaps | Important unresolved questions |

---

# 6. Naming and Directory Recommendations

## Minimal version

```text
raw/
wiki/
docs/
.tasks/
outputs/
```

## Better version for coding repos

```text
knowledge/
  raw/
  wiki/
  outputs/
docs/
.tasks/
```

Reason: avoids confusing research wiki with product docs.

Recommended for your setup:

```text
knowledge/
  raw/
    articles/
    papers/
    repos/
    images/
    notes/
  wiki/
    concepts/
    entities/
    source-summaries/
    decisions/
    indexes/
    unresolved/
  outputs/
    reports/
    slides/
    charts/
docs/
.tasks/
```

---

# 7. Source and Claim Integrity Rules

## Claim tags

Use tags in wiki pages:

```markdown
- [OFFICIAL] Vendor documentation says...
- [PAPER] The paper reports...
- [COMMUNITY] Practitioners report...
- [INFERENCE] This suggests...
- [UNVERIFIED] Needs live verification...
```

## Evidence table pattern

```markdown
| Claim | Evidence | Source | Confidence | Notes |
|---|---|---|---|---|
| Markdown wiki reduces repeated retrieval work | Sequential queries can reuse compiled pages | Source | Medium | Depends on topic concentration |
```

## Contradiction block

```markdown
> [!warning] Contradiction
> Source A says X. Source B says Y.
> Current working interpretation: Z.
> Needs verification: ...
```

---

# 8. Risks and Failure Modes

| Risk | Why it matters | Mitigation |
|---|---|---|
| LLM-generated wiki drift | Agent may slowly rewrite knowledge into false coherence | Git diffs, source citations, health checks |
| Speculation promoted to docs | Research claims become engineering truth too early | Promotion gate via `grill-me` |
| Link rot / bad capture | Raw web sources may disappear or clip badly | Store source URL, capture date, original excerpt/metadata |
| Over-synthesis | Agent compresses away nuance | Keep source summaries separate from concept pages |
| Duplicate concepts | Wiki becomes messy at 100+ pages | Periodic merge/split health check |
| No provenance | Answers become hard to audit | Mandatory claim/evidence/source tables |
| Token creep | Wiki grows beyond convenient context | Index pages, page summaries, search CLI |
| Images ignored | Visual sources not incorporated into synthesis | Store images locally and create image notes |
| Human disengagement | Wiki becomes agent-only and untrusted | Obsidian review flow + changelog |
| Fine-tuning temptation too early | Training on unstable knowledge freezes errors | Delay until stable, high-quality corpus exists |

---

# 9. Fine-Tuning / Synthetic Data: Treat as Later-Stage

Karpathy mentions the natural desire to use synthetic data generation and fine-tuning so the model “knows” the wiki. This is directionally interesting but premature for your current project-skills setup.

Better staging:

| Stage | Action | Why |
|---|---|---|
| 1 | Markdown wiki + indexes | Maximum inspectability |
| 2 | CLI search over wiki | Useful at small scale |
| 3 | Health checks and source integrity | Prevents garbage accumulation |
| 4 | Synthetic Q&A generation | Creates training/eval material |
| 5 | Evaluation set | Measures whether agents answer better |
| 6 | Fine-tuning or adapters | Only after stable corpus and evals |

Do not fine-tune before you have:

- stable wiki schema
- source-quality tags
- contradiction handling
- regression evals
- clear task distribution
- proof that context/search is insufficient

---

# 10. Practical Improvements for Your Current Skills

## Add a `knowledge/` layer

Current:

```text
docs/
.tasks/
```

Proposed:

```text
knowledge/
  raw/
  wiki/
  outputs/
docs/
.tasks/
```

## Add promotion policy

```text
Wiki content can become docs content only when:
1. It is implementation-relevant.
2. It has source provenance or direct repo evidence.
3. `grill-me` has checked assumptions.
4. The agent states what changed and why.
```

## Add source-summary pages

Do not let raw sources jump directly into docs.

## Add output filing

After a useful research answer:

```text
outputs/reports/<date>-<topic>.md
```

Then agent asks:

```text
Should stable findings be filed into:
- wiki/concepts/
- wiki/decisions/
- docs/
- .tasks/
```

## Add wiki index files

```text
wiki/index.md
wiki/concepts/index.md
wiki/entities/index.md
wiki/decisions/index.md
wiki/unresolved/index.md
```

Each index should contain 1–3 sentence summaries per page so agents can cheaply navigate.

## Add health-check command

Run manually or pre-merge:

```text
/project-wiki health-check
```

Output:

```markdown
# Wiki Health Report

## Broken / Missing Links
## Stale Source Summaries
## Contradictions
## Duplicate Concepts
## Promotion Candidates
## New Article Candidates
## Recommended Next Actions
```

---

# 11. Agent Prompt: New `project-wiki` Skill Draft

```markdown
# project-wiki Skill

You maintain a repo-local LLM knowledge base for research and synthesis.

## Purpose

Convert raw research inputs into durable, linked Markdown knowledge that compounds over time. Keep this separate from canonical engineering docs and ephemeral task state.

## Directory Ownership

- `knowledge/raw/`: source captures, papers, articles, screenshots, repo notes, datasets.
- `knowledge/wiki/source-summaries/`: one summary per source.
- `knowledge/wiki/concepts/`: synthesized conceptual pages.
- `knowledge/wiki/entities/`: companies, tools, models, papers, repos, people.
- `knowledge/wiki/decisions/`: research-backed decision notes.
- `knowledge/wiki/unresolved/`: open questions and research gaps.
- `knowledge/outputs/`: generated reports, slides, charts, diagrams.

Do not write to `docs/` unless the user explicitly asks or the promotion policy is satisfied.

## Core Commands

### ingest
Summarize raw source files into source-summary pages with provenance.

### compile
Update concept/entity/decision pages from source summaries and existing wiki pages.

### ask
Answer complex questions by reading indexes first, then relevant wiki pages, then raw sources only if needed.

### file-output
Extract stable insights from generated outputs and file them back into the wiki.

### health-check
Find contradictions, stale sources, missing provenance, duplicate concepts, orphan pages, and promotion candidates.

## Rules

- Preserve source provenance.
- Tag claims as `[OFFICIAL]`, `[PAPER]`, `[COMMUNITY]`, `[INFERENCE]`, or `[UNVERIFIED]`.
- Prefer tables, schemas, examples, and diagrams over prose.
- Keep source summaries separate from synthesized pages.
- Never promote speculative research into canonical docs without validation.
- Keep pages small enough for future agents to read.
- Maintain index pages with short summaries.
- Use git diffs as the audit trail.
```

---

# 12. Recommended Next Implementation Task for Coding Agent

```markdown
Implement a minimal `project-wiki` skill beside existing `project-docs`, `project-tasks`, and `grill-me`.

Acceptance criteria:

1. Create `knowledge/` directory convention:
   - `knowledge/raw/`
   - `knowledge/wiki/source-summaries/`
   - `knowledge/wiki/concepts/`
   - `knowledge/wiki/entities/`
   - `knowledge/wiki/decisions/`
   - `knowledge/wiki/unresolved/`
   - `knowledge/outputs/`

2. Add templates:
   - source summary template
   - concept page template
   - decision note template
   - health-check report template

3. Add skill instructions for:
   - ingest
   - compile
   - ask
   - file-output
   - health-check

4. Add promotion policy from wiki to docs:
   - implementation relevance
   - provenance
   - validation
   - explicit changelog

5. Add index maintenance rules:
   - every wiki subdirectory has an `index.md`
   - each index entry has title, summary, source count, last updated, confidence

6. Add a sample workflow using the Karpathy LLM Wiki article/tweet as the first ingested source.
```

---

# 13. Final Recommendation

Adopt the pattern, but with stronger boundaries than Karpathy's casual version:

```text
LLM Wiki for research.
Project docs for canonical engineering truth.
Project tasks for execution state.
Grill-me for validation.
```

Your current system is already close to the engineering half of this. The missing half is a **research compiler**: source intake, concept synthesis, backlinks, health checks, and output filing.

The highest-ROI improvement is not vector search or fine-tuning. It is adding a small `project-wiki` skill with clear folder ownership, templates, claim tags, indexes, and promotion rules.
