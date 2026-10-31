# Task: Evaluate Azure MCP delivery for Agent Core skills

**File:** `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md`
**Created:** 2026-10-31
**Last Updated:** 2026-10-31
**Priority:** Later
**Status:** On Hold

**Goal:** Explore a small, read-only MCP server that makes canonical Agent Core skills discoverable and retrievable by remote AI clients (particularly ChatGPT), while gaining practical MCP development and deployment experience.

**Why:** Local Pi/OpenCode/Devin skill discovery already works through `agent-core sync`. In hosted ChatGPT, the GitHub connector can fetch known files but does not automatically expose skills as native discovery metadata. The human wants reliable instruction discovery without repeatedly naming repository paths.

**Chosen Direction:** Investigate only; no Azure implementation/hosting choice approved. Preserve `chingfhen/agent-core` as the single canonical skills source and existing native skill sync unchanged. Azure Functions and Azure Container Apps are candidates, not commitments. The user prefers zero ongoing hosting cost and low cold-start latency.

**Current State:** No MCP server built or deployed. The private GitHub connector successfully fetched `AGENTS.md`, `personal-skills.toml`, and `skills/knowledge-base/SKILL.md` in ChatGPT on 2026-10-31. Current ChatGPT Plus custom external MCP connection availability is a product limitation; a native ChatGPT skill/plugin route is being investigated first. MCP access alone would not guarantee skill invocation or compliance.

**Next Action:** **Not yet authorized to implement.** When the user resumes this task, verify current ChatGPT Plus MCP/plugin support and whether a native plugin already solves skill discovery. If MCP remains worthwhile for interoperable clients or learning, propose a minimal implementation and hosting/cost trade-off for approval.

**Re-entry Condition:** The user explicitly asks to revisit Azure MCP development, or the plugin experiment establishes an unmet delivery requirement.

**Success Bar (if implementation is later approved):** A compatible MCP client can discover a bounded skill catalogue, fetch full `SKILL.md` and selectively fetch references from the current canonical GitHub repository, with source revision and secure read-only access. Test default skill selection from a natural-language request versus direct GitHub retrieval. No duplicate skills store, KB writes, task execution, credential leakage, or unnoticed cloud charges.

**Permission Boundary:** This task saves investigation context only. Do not provision Azure resources, create secrets, change existing skill distribution, register an external MCP connector, or modify production skills without separate authorization.

## Resume Context
- `AGENTS.md` — Agent Core steward constraints and current skill distribution boundary.
- `docs/consumer-repo-enrollment.md` — existing native skill publication/sync contract.
- `personal-skills.toml` — canonical selected skill list.
- `skills/knowledge-base/SKILL.md` — example skill and selective reference-loading conventions.
- OpenAI Help Center: [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-codexOpenAI) and [Custom MCP servers](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) — re-check current plan eligibility on resumption.
