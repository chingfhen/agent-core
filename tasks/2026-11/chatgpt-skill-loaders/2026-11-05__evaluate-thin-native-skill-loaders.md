# Task: Evaluate native ChatGPT thin skill loaders for Agent Core

**File:** `tasks/2026-11/chatgpt-skill-loaders/2026-11-05__evaluate-thin-native-skill-loaders.md`
**Created:** 2026-11-05
**Last Updated:** 2026-11-05
**Priority:** Later
**Status:** On Hold

**Goal:** Evaluate a low-maintenance way for ChatGPT to discover and use the canonical Agent Core Project Tasks, Project Docs, Knowledge Base and other relevant skills as native ChatGPT skills, without standing up the separate read-only Azure MCP service.

**Why:** ChatGPT can already read and edit the private repositories using its GitHub connector, but canonical `SKILL.md` discovery and correct activation are not native. A thin ChatGPT skill describing its triggers and pointing to GitHub may offer native discovery without replicated, independently maintained instructions or hosting costs.

**Current State:** Discussion on 2026-11-05 identified ChatGPT's Skills creation/upload UI and proposed thin native skill loaders. Concept only: no loader, packaging, publishing, automatic updates or invocation reliability tested. The previously approved Azure read-only skill-delivery MCP proposal is a separate active task; the human intends to close it later, but has **not authorized closure now**.

**Candidate Direction (not approved for implementation):** Keep `chingfhen/agent-core` as the sole authoritative source. Package minimal ChatGPT-native skill descriptions with direct GitHub pointers so the model retrieves the current canonical `SKILL.md`, relevant references and applicable `AGENTS.md` before operating. Assess whether ChatGPT plugin skills can reliably call existing GitHub tools, what the loader contains, how to keep it aligned with current canonical skill descriptions, and whether a generated full-skill package is more reliable. Do not assume a GitHub URL in a skill grants access or guarantees loading.

**Success Bar:** Compare thin loader, generated complete native skill package, and GitHub-only discovery using representative fresh-chat requests (task handoff, managed artifact update, KB capture). Confirm canonical content/source commit used, trigger accuracy, adherence to permission boundaries, absence of independently edited copies, latency/tool-call overhead, and any release/update requirements. Recommend the minimum effective approach or no change.

**Next Action:** When the human explicitly resumes: inspect current OpenAI native skill/plugin authoring rules; make a small design and test plan with canonical Github references; request authorization before creating, installing, or publishing any plugin/skill.

**Permission Boundary:** Deferred research/planning only. No plugin creation, upload, code, deployment, skill edits, KB changes, or closure of the Azure MCP task without a later explicit request.

## Resume Context
- `skills/project-tasks/SKILL.md`, `skills/project-docs/SKILL.md`, and `skills/knowledge-base/SKILL.md` in `chingfhen/agent-core` — canonical instructions and references.
- `docs/consumer-repo-enrollment.md` and `personal-skills.toml` — existing native Pi/Devin/OpenCode skill distribution; do not alter.
- `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md` — older Azure MCP instruction-delivery plan and measured Plus MCP access.
- OpenAI plugin/Skills documentation current at time of resumption — verify constraints rather than relying on this planning note.
