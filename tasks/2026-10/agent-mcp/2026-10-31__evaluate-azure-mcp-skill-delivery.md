# Task: Evaluate and prototype remote MCP delivery of Agent Core skills

**File:** `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md`
**Created:** 2026-10-31
**Last Updated:** 2026-10-31
**Priority:** Next
**Status:** Active

**Goal:** Make canonical Agent Core instructions easier for hosted agents such as ChatGPT to discover and retrieve, using a small read-only MCP server, while gaining practical MCP development experience.

**Why:** Local Pi/OpenCode/Devin already discover native skills through `agent-core sync`. ChatGPT's GitHub connector fetches known files but does not automatically surface the registered skills, their descriptions, or applicable `AGENTS.md` as native instruction-discovery metadata.

**Current State:** The user explicitly resumed MCP planning on 2026-10-31; no implementation or deployment has occurred. Direct GitHub retrieval of `AGENTS.md`, `personal-skills.toml`, and `skills/knowledge-base/SKILL.md` was demonstrated. OpenAI developer docs describe creating a personal plugin from a custom MCP URL, while plan/permission documentation is not fully consistent; verify the user's actual Plus account with the published demo before treating connectivity as proven.

**Chosen Direction:** Investigate a **read-only, instruction-delivery-only** MVP. `chingfhen/agent-core` remains the single canonical source for SKILL.md, references, AGENTS.md, and existing native sync. No KB/task writes, tool execution, vector DB, skill duplication, or enforcement gateway.

**Proposed architecture (not yet approved):** A separate private `chingfhen/agent-core-mcp` service repository for MCP SDK dependencies, deployment, and cloud-specific configuration. It reads an allowlisted skill catalogue and full content/references from `chingfhen/agent-core` at runtime using narrowly scoped read-only GitHub access. Keeping the service separate protects the lean, standard-library-only `agent-core sync` runtime. A self-contained subproject in Agent Core is a viable alternative if the user prefers one repo. Do not copy the canonical skill files into the service as another maintained source.

**Discovery design issue:** Merely exposing generic `list_skills`/`read_skill` operations does not make agent selection automatic. Compare descriptive tool metadata and/or per-skill tool exposure against native plugin-packaged skills using ordinary fresh-chat prompts. The MCP client still decides when to call a tool.

**Hosting constraints:** Azure is preferred for learning, but the user wants essentially zero ongoing expense and acceptable cold starts. Azure Functions Flex Consumption (including storage charges) and Azure Container Apps scale-to-zero are candidates. Local MCP Inspector testing precedes provisioning. Favor stateless Streamable HTTP, no UI, and GitHub Actions deployment if a host is approved. Do not select paid/always-ready resources silently.

**Next Action (permitted now):** Confirm whether the user successfully connected and invoked the official demo MCP server in their Plus account; agree on repo ownership and initial deployment target; then prepare a narrow implementation plan. **Building code and provisioning/deploying infrastructure remain unapproved** until the user explicitly requests them.

**Blockers / Human Attention:** Account-level MCP availability must be confirmed; final repo/hosting choice and implementation permission are undecided. Credentials, Azure subscription, or GitHub Actions secret configuration would require user action at deployment time.

**Success Bar:** On an MCP-compatible client, retrieve an allowlisted skill and references with source commit identity; avoid broad private repository browsing, unauthorized data exposure, and duplicate skill copies. Demonstrate skill invocation from a natural request without the user naming paths, and measure selection reliability relative to GitHub-only access.

**Permission Boundary:** Planning and this task/index update only. No creation of a second repo, Azure services, secrets, connector registration, changes to production Agent Core skills or native sync, or cloud costs without separate authorization.

## Resume Context
- `AGENTS.md` and `README.md` — steward contract, zero-dependency sync runtime, canonical source and boundaries.
- `docs/consumer-repo-enrollment.md` and `personal-skills.toml` — native skill publishing and canonical registration.
- `skills/knowledge-base/SKILL.md` — skill content, references, and workflow example.
- [OpenAI custom MCP plugin quickstart](https://developers.openai.com/plugins/quickstart) — demo MCP connection and ChatGPT Work testing.
- [OpenAI plugin MCP server guide](https://developers.openai.com/plugins/build/mcp-server) — standard SDKs and HTTP transport.
- [OpenAI MCP connection guide](https://developers.openai.com/api/docs/guides/custom-mcp-server) — tool discovery and authentication.
- [Azure Functions MCP hosting](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-ai-enabled-apps) — Azure server options and support maturity; recheck before implementation.
