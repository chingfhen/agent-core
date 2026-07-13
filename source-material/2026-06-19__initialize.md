Here is the complete, unambiguous technical specification. You can copy this directly into a HANDOFF.md or README.md file in your new repository, and a coding agent will have all the context, schemas, boundaries, and rules it needs to build the Agent OS exactly as we designed it.
```markdown
# Agent OS: Implementation Handoff & Architecture Spec

## System Objective
Agent OS is a lightweight, portable orchestration layer that provides coding agents (Claude Code, OpenCode, etc.) with reliable cross-harness semantic memory, dynamically hydrated skills, and deterministic script-based APIs. 

**Core Principle:** One canonical source of truth (`~/agent-os`). Everything else (harness installations, search indices) is disposable and generated. 

---

## 1. Human-in-the-Loop Boundaries (Strict Rules for Agents)
The system enforces strict operational boundaries. The coding agent implementing and using this OS MUST adhere to the following autonomous vs. manual permissions:

**Fully Autonomous Actions (No Prompting Required):**
* Updating or superseding an *existing* memory `topic_key` within the current scope.
* Regenerating SQLite indexes and markdown maps from the `jsonl` ledger.
* Running `sync_skills` to Nuke & Pave harness symlinks.
* Reading local `.agent-os.json` context files.

**Requires Explicit Human Permission (Stop and Ask):**
* **Creating a NEW `topic_key`:** If the agent wants to save a memory but a relevant `topic_key` does not exist in the active scope, it MUST stop and propose the new key to the human.
* **Promoting a Skill:** Creating a new global skill in `~/agent-os/skills/` from a local workflow requires human review.
* **Destructive Deletions:** Any removal of data from the canonical `memories.jsonl` (which should theoretically be append-only).

---

## 2. Directory Architecture
```text
agent-os/
├─ HANDOFF.md              # This file
├─ MEMORY_INDEX.md         # Auto-generated low-token map of available topics
├─ skills/                 # Canonical markdown operating instructions
│  └─ project-docs/
│     └─ SKILL.md
├─ memory/                 # The Semantic Memory engine
│  ├─ memories.jsonl       # Append-only canonical truth (Git tracked)
│  └─ memory.sqlite        # Disposable FTS search index (Git ignored)
├─ repo-profiles/          # Project-specific capability maps
└─ scripts/                # The API: Single-file Python scripts using PEP 723 (uv)

```
## 3. The Memory Subsystem (Schema & Topic Keys)
Memory handles durable knowledge, not operating instructions. Contradictions are managed by replacing facts under a categorical topic_key, rather than deleting old lines.
**Memory Schema (Pydantic enforced):**
 * id (UUID4)
 * created_at (ISO8601 Timestamp)
 * scope (Enum: global, personal, repo, experiment)
 * scope_id (String: e.g., adreadyclip, or null for global/personal)
 * topic_key (String: e.g., deployment_strategy, ci_cd_config)
 * status (Enum: active, superseded)
 * content (String/Markdown)
 * keywords (List of Strings)
**The Supersede Logic:**
When add_memory.py receives a payload with a topic_key that already exists in the active scope + scope_id, the script automatically sets the old entry's status to superseded in the SQLite index and appends the new entry to the .jsonl. The agent does not need to look up UUIDs.
## 4. Script APIs & Dependency Management
Agents interact with the OS *only* via the Python scripts in scripts/. Direct file writing to .jsonl, .sqlite, or ~/.claude/skills is forbidden.
**Dependency Strategy:**
 * All scripts MUST use uv with PEP 723 inline metadata. No requirements.txt or global virtual environments.
 * Example script header:
```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = ["pydantic", "sqlite-utils"]
  # ///

```
**LLM-Optimized Error Handling:**
 * Standard stack traces are forbidden.
 * Scripts MUST catch Pydantic validation errors and system exceptions, printing actionable instructions to stdout so the agent knows exactly how to self-correct.
 * *Example:* SYSTEM ERROR: Validation failed. 'keywords' must be an array of strings. Action: Retry tool call with correct format.
**Core Scripts to Implement:**
 1. add_memory.py: Validates schema, handles supersede logic via topic_key, appends to .jsonl, updates .sqlite, and regenerates MEMORY_INDEX.md.
 2. search_memory.py: Queries .sqlite using FTS5 text matching. Also supports a --list-topics flag for a specific scope.
 3. sync_skills.py: Implements "Nuke and Pave". Wipes ~/.claude/skills (or target harness), then loops through ~/agent-os/skills generating absolute-path symlinks.
## 5. Context Hydration (Local Project Integration)
To prevent agents from loading the wrong context, project repositories connect to the OS via a lightweight local JSON manifest.
**File:** .agent-os.json (Placed at the root of a project like adreadyclip)
```json
{
  "agent_os_path": "~/agent-os",
  "scope": "repo",
  "scope_id": "adreadyclip",
  "repo_profile": "~/agent-os/repo-profiles/adreadyclip.md"
}

```
**Bootstrap Routine:** When an agent boots in a repository, it reads this file to locate the canonical OS, identify its operational scope boundaries, and hydrate its context.
## 6. Implementation Sequence for the Coding Agent
To build this system, execute these steps in order:
 1. **Scaffold Directories:** Create the folder structure defined in Section 2.
 2. **Memory Core:** Create memory/memories.jsonl and initialize an empty memory.sqlite database using sqlite-utils.
 3. **API Scripts:** Write the add_memory.py and search_memory.py scripts. Ensure they utilize inline uv dependencies and strict Pydantic schemas. Write unit tests or dry-run them.
 4. **Skill Syncing:** Write the sync_skills.py script using the Nuke and Pave method for symlink generation.
 5. **Index Generator:** Write a lightweight script that parses memories.jsonl and rewrites MEMORY_INDEX.md grouped by active scope and topic keys.
 6. **Lint & Verify:** Write a pre-flight script (agent_os_lint.py) that checks the health of symlinks, local JSON manifests, and SQLite checksums against the .jsonl truth.
```

```
