---
title: "Cross-Harness Agent Memory: Shared Memory Contracts, Memory Extraction, and Temporal Memory"
generated_on: 2026-06-20
scope: "Memory architectures for multi-agent workflows spanning Claude Code, OpenCode, Codex, repository agents, and custom memory systems. Focused on memory contracts, extraction pipelines, and temporal memory management."
purpose: "External knowledge ingestion artifact intended for downstream repository agents."
status: "Active"
---

## Definitions & Core Architecture

### Problem Definition

Modern agent ecosystems increasingly operate across:

```text
Claude Code
OpenCode
Codex
Cursor
Repository Agents
Custom Internal Agents
```

The primary architectural challenge is not memory storage.

The challenge is maintaining:

```text
Consistency
Relevance
Temporal Accuracy
Cross-Agent Interoperability
```

over long-lived memory collections.

### Architectural Layers

Common architecture observed across memory systems:

```text
Agent
  ↓
Memory Extraction
  ↓
Memory Contract
  ↓
Memory Storage
  ↓
Memory Retrieval
  ↓
Memory Ranking
  ↓
Context Injection
```

Memory storage implementations vary:

| Layer | Common Implementations |
|---------|---------|
| Extraction | LLM-based classification |
| Contract | JSON schemas |
| Storage | Postgres, SQLite, Vector DB, Graph DB |
| Retrieval | Vector search, graph traversal |
| Ranking | Similarity + recency + importance |
| Injection | Prompt augmentation |

[VERIFIED] Memory frameworks including Mem0, Zep, Graphiti, LangMem, and Supermemory all implement variations of this pipeline.

---

## Cross-Harness Memory Contract

### Objective

Enable multiple independent agents to read and write memory without requiring shared internal implementations.

### Core Principle

Memory portability depends more on the schema than the storage backend.

A shared contract permits:

```text
Claude Code writes memory
       ↓
OpenCode reads memory
       ↓
Codex updates memory
       ↓
Repository Agent retrieves memory
```

without coupling agents to specific frameworks.

---

### Minimal Memory Contract

```json
{
  "memory_id": "uuid",
  "memory_type": "decision",
  "content": "Veo Fast selected for CTA scenes",
  "project": "adreadyclips",
  "source_agent": "claude-code",
  "created_at": "2026-06-20T00:00:00Z",
  "updated_at": "2026-06-20T00:00:00Z",
  "importance_score": 0.92,
  "status": "active"
}
```

---

### Common Memory Categories

Observed memory categories across production systems:

| Type | Description |
|---------|---------|
| user_preference | Stable user preferences |
| project_fact | Repository/project knowledge |
| decision | Architectural decisions |
| failure | Known failures |
| lesson | Generalized learning |
| workflow | Repeatable process |
| temporary_state | Session-specific context |
| task | In-progress work |
| relationship | Entity relationships |
| constraint | Hard system limitations |

[COMMUNITY] Most long-lived systems eventually introduce memory type hierarchies.

---

### Source Attribution

Memory systems increasingly track origin metadata.

Example:

```json
{
  "source_agent": "opencode",
  "source_session": "session-123",
  "source_artifact": "research.md"
}
```

Benefits:

```text
Traceability
Conflict resolution
Memory auditing
Trust verification
```

---

## Memory Extraction

### Core Problem

Naive memory systems store excessive information.

This creates:

```text
Noise Accumulation
Retrieval Pollution
Context Inflation
Memory Conflicts
```

over time.

---

### Extraction Pipeline

Common pipeline:

```text
Conversation
      ↓
Candidate Facts
      ↓
Classification
      ↓
Importance Scoring
      ↓
Memory Creation
```

---

### Candidate Memory Types

#### User Preference

Example:

```text
User prefers Azure Container Apps.
```

Characteristics:

```text
High persistence
Frequently reused
Rarely changes
```

---

#### Project Decision

Example:

```text
AdReadyClips uses FFmpeg packaging.
```

Characteristics:

```text
Project-specific
Often referenced
May evolve
```

---

#### Failure Memory

Example:

```text
Kling portrait mode produced letterboxing artifacts.
```

Characteristics:

```text
High engineering value
Prevents repeated mistakes
```

---

#### Temporary State

Example:

```text
Currently debugging Supabase queue issue.
```

Characteristics:

```text
Rapid expiration
Low long-term value
```

Typically excluded from permanent memory.

---

### Importance Scoring

Observed dimensions:

| Dimension | Description |
|---------|---------|
| Reuse Frequency | Likelihood of future retrieval |
| Project Impact | Architectural significance |
| User Significance | Personal relevance |
| Longevity | Expected lifespan |
| Uniqueness | Novelty vs duplication |

---

### Memory Consolidation

Memory growth requires consolidation.

Without consolidation:

```text
100 memories
↓
1000 memories
↓
10000 memories
↓
Retrieval degradation
```

Common approaches:

| Method | Description |
|---------|---------|
| Deduplication | Merge duplicates |
| Summarization | Compress clusters |
| Promotion | Convert observations into rules |
| Aging | Reduce importance over time |
| Archival | Move inactive memory |

---

### Example Consolidation

Raw memories:

```text
Used Veo Fast for CTA
Used Veo Fast for product demo
Used Veo Fast for animation
```

Consolidated memory:

```text
Veo Fast is currently the preferred video provider for AdReadyClips workflows.
```

[COMMUNITY] Consolidation quality often determines long-term memory usefulness more than embedding quality.

---

## Temporal Memory

### Core Problem

Facts change.

Traditional vector memory assumes facts remain valid indefinitely.

This assumption fails.

---

### Example

Timeline:

```text
2025:
Use Kling

2026:
Use Veo Fast

2027:
Use Future Provider X
```

Naive retrieval:

```text
Kling
Veo Fast
Future Provider X
```

Correct retrieval:

```text
Current:
Future Provider X

Historical:
Kling
Veo Fast
```

---

### Temporal State Model

Memory systems increasingly separate:

```text
Current Truth
Historical Truth
```

---

### Temporal Memory Contract

```json
{
  "memory_id": "uuid",
  "content": "Veo Fast selected",
  "valid_from": "2026-01-01",
  "valid_to": "2027-03-15",
  "status": "superseded"
}
```

---

### State Transitions

```text
Active
   ↓
Superseded
   ↓
Archived
```

rather than:

```text
Active
   ↓
Deleted
```

---

### Contradiction Handling

Example:

```text
Memory A:
Preferred provider = Kling

Memory B:
Preferred provider = Veo Fast
```

Possible resolution strategies:

| Strategy | Description |
|---------|---------|
| Latest Wins | Most recent memory replaces previous |
| Importance Wins | Higher confidence memory replaces lower |
| Human Review | Explicit approval required |
| Temporal Graph | Preserve both with validity windows |

---

### Knowledge Graph Approaches

Graphiti and related graph-memory systems model:

```text
User
 └── prefers ──> Claude

Project
 └── uses ──> Veo Fast

Project
 └── previously_used ──> Kling
```

Advantages:

```text
Temporal reasoning
Relationship tracking
Fact evolution
```

Tradeoffs:

```text
Higher complexity
Graph maintenance
Additional retrieval logic
```

---

### Temporal Retrieval Ranking

Observed ranking signals:

| Signal | Purpose |
|---------|---------|
| Similarity | Semantic match |
| Recency | Newer memories favored |
| Importance | High-value memories favored |
| Frequency | Frequently referenced memories favored |
| Temporal Validity | Active memories favored |
| Relationship Strength | Connected memories favored |

Modern systems increasingly combine multiple ranking dimensions.

[COMMUNITY] Similarity-only retrieval becomes insufficient as memory volume grows.

---

## Failure Modes & Error Shapes

### Memory Explosion

Symptoms:

```text
Rapid memory growth
Increasing retrieval latency
Duplicate memories
Context pollution
```

Root Cause:

```text
Over-aggressive memory creation
```

---

### Stale Truth

Symptoms:

```text
Outdated architectural decisions retrieved
Deprecated workflows resurfacing
```

Root Cause:

```text
No temporal validity model
```

---

### Retrieval Pollution

Symptoms:

```text
Relevant memory buried
Excessive irrelevant recall
```

Root Cause:

```text
Similarity-only retrieval
```

---

### Cross-Agent Drift

Symptoms:

```text
Claude writes one format
Codex writes another
OpenCode cannot interpret either
```

Root Cause:

```text
No shared memory contract
```

---

## Open Questions For Repository Agents

- Should memory storage remain centralized or allow per-project memory namespaces?
- Which memory categories should be permanently persisted versus session-scoped?
- What importance scoring model best aligns with local repository workflows?
- Should memory consolidation occur synchronously during writes or asynchronously in background jobs?
- Is temporal validity represented via timestamps, graph edges, or explicit state transitions?
- How should conflicting memories from different agents be resolved?
- What retrieval ranking weights should be assigned to similarity, recency, importance, and temporal validity?
- Which repository artifacts (AGENTS.md, CLAUDE.md, research artifacts, handoff documents) are authoritative memory sources versus derived memory outputs?
- What monitoring should detect memory explosion, retrieval degradation, and stale-truth accumulation?
- What retention policies should govern archival and deletion of historical memories?