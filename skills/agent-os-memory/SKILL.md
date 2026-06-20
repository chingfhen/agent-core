---
name: agent-os-memory
description: Use proactively in memory-enabled Agent OS repos whenever durable user or repo knowledge may affect the task, when the user asks to remember or recall something, or when a completed task reveals a reusable preference, constraint, decision, procedure, or unusual resolved failure. Load relevant memory before consequential work and capture only high-signal durable updates; do not use for raw transcripts, scratch notes, routine task status, or facts better stored in code, docs, or task files.
disable-model-invocation: false
---

# Agent OS Memory

Use this skill to make durable Agent OS memory useful during execution. Memory is a scoped recall and capture layer, not a task log, transcript store, or replacement for repo files.

## When To Use

- Use proactively before consequential work when prior user preferences, repo constraints, durable decisions, or known pitfalls could change the approach.
- Use when resuming a repo after context loss and the task depends on local conventions or prior decisions.
- Use when the user asks to remember, recall, search memory, preserve a preference, or explain what was previously decided.
- Use after work only if the task revealed durable knowledge that is likely to help future sessions.
- Do not use for casual chat, trivial edits, raw command output, active task status, or information already easy to recover from current repo files.

## Memory Availability

1. Read `.agent-os.json` from the repo root.
2. Capture `agent_os_path`, `scope`, `scope_id`, and `memory_enabled`.
3. If the manifest is missing, invalid, or `memory_enabled` is `false`, memory is unavailable in this repo. Say so briefly when relevant, then continue using normal repo context.
4. Do not inspect or edit Agent OS memory storage directly. Use only the Agent OS memory command below.

## Recall Flow

1. Turn the current task into one to three targeted memory queries. Prefer specific concepts, tools, decisions, errors, repo names, or user preferences over broad searches.
2. Inspect available topics when you do not already know the right topic:
   - `uv run "<agent_os_path>/scripts/memory.py" list --scope <scope> --scope-id <scope_id>`
3. Search for relevant memory:
   - `uv run "<agent_os_path>/scripts/memory.py" search "<query>" --scope <scope> --scope-id <scope_id>`
4. Apply only memory that is relevant to the current scope and task.
5. Treat memory as advisory context. Current user instructions, system/developer instructions, and repo files win over retrieved memory.
6. If memory conflicts with current repo truth or user instructions, surface the conflict briefly and follow the higher-priority source unless the user clarifies otherwise.
7. Do not dump memory results into the response. Mention retrieved memory only when it materially affected the work or when the user asked about memory.

## Capture Gate

Capture only high-signal durable knowledge. Good candidates are:

- Explicit user preferences likely to recur across sessions.
- Stable repo or environment constraints that are not reliably obvious from code or docs.
- Durable decisions and rationale that should shape future work.
- Validated repeatable procedures that worked in this repo.
- Unusual resolved failures, edge cases, or diagnostics likely to recur.

Do not capture:

- Raw transcripts, routine command output, stack traces without a reusable resolution, or large logs.
- Scratch reasoning, temporary implementation notes, or ordinary task progress.
- Guesses, unverified claims, speculative plans, or stale information.
- Secrets, credentials, private tokens, or sensitive personal data.
- Facts already better represented in source code, tests, `README.md`, `AGENTS.md`, docs, or active task files.
- Generic engineering knowledge that belongs in a reusable skill or tool instead of repo/user memory.

Use the better surface when one exists: source code and tests for behavior, docs for durable repo contracts, `tasks/` for active handoff, and memory for scoped context that future agents should recall but cannot reliably rediscover.

## Capture Flow

1. Before writing, inspect existing topics and search for near-duplicates.
2. Reuse an existing `topic_key` whenever it fits. Updating an existing topic in the active scope can be autonomous when the capture gate is clearly met.
3. Keep memory content concise, stable, and actionable. Write the distilled fact, preference, decision, procedure, or failure resolution; do not paste raw session history.
4. Include useful keywords for later discovery.
5. For a quick update to an existing topic, prefer inline content:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content "<note>"`
6. For longer content, use a temporary UTF-8 file and pass it as content:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content-file "<path>"`
7. If no suitable `topic_key` exists, stop and ask the human to approve the new `topic_key` before writing. Recommend the exact key and the distilled content you intend to save.
8. After approval, retry with `--allow-new-topic-key`:
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content "<note>" --allow-new-topic-key`
   - `uv run "<agent_os_path>/scripts/memory.py" write --scope <scope> --scope-id <scope_id> --topic-key <topic_key> --keyword <keyword> --content-file "<path>" --allow-new-topic-key`

## Boundaries

- Agent OS memory is separate from any model-native memory. Do not assume native memory is complete, scoped to this repo, or inspectable.
- Agent OS memory is separate from repo docs and active task files. Do not duplicate durable contracts or task handoff that belongs there.
- Deletion is not an executor workflow. If memory is stale, write a clearer replacement under the same topic when allowed, or ask the user what should supersede it.
