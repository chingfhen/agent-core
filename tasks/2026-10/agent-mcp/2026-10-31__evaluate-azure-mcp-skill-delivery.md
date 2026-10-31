# Task: Evaluate and prototype remote MCP delivery of Agent Core skills

**File:** `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md`
**Created:** 2026-10-31
**Last Updated:** 2026-10-31
**Priority:** Next
**Status:** Active

**Goal:** Make canonical Agent Core instructions easier for hosted agents such as ChatGPT to discover and retrieve, using a small read-only MCP server, while gaining practical MCP development experience.

**Why:** Local Pi/OpenCode/Devin already discover native skills through `agent-core sync`. ChatGPT's GitHub connector fetches known files but does not automatically surface the registered skills, their descriptions, or applicable `AGENTS.md` as native instruction-discovery metadata.

**Current State:** On 2026-10-31 the user approved the repository, hosting, and scope decisions below. Screenshots from the Plus account show **Plugins → Add custom MCP server** with server URL and authentication controls. This demonstrates access to the creation UI, **not yet a successfully registered or invoked MCP tool**. Direct GitHub retrieval of canonical Agent Core files has been demonstrated. No new repo, MCP code, Azure resources, or deployment exists yet.

**Chosen Direction (approved 2026-10-31):** Build toward a **read-only, instruction-delivery-only** MCP MVP. Use a separate private `chingfhen/agent-core-mcp` service repository and Azure Functions with scale-to-zero (Flex Consumption is the initial target), zero always-ready instances, and GitHub Actions deployment once approved. `chingfhen/agent-core` remains the sole canonical source for SKILL.md, references, AGENTS.md, and existing native sync. No KB/task writes, vector DB, replicated skill content, or enforcement gateway. Hosting must minimize costs; Azure Functions' storage/networking are not necessarily free.

**Architecture:** The new private service repository owns its SDK dependencies, tests, and Azure delivery workflow independently of Agent Core's zero-dependency local sync runtime. The service fetches allowlisted canonical skills, reference files, and applicable guidance from `chingfhen/agent-core` via narrowly scoped read-only GitHub credentials. Tool surface should be small and stateless; use MCP Streamable HTTP. Do not ship maintained copies of skills.

**Discovery design issue:** Merely exposing generic `list_skills`/`read_skill` operations does not make agent selection automatic. Compare descriptive tool metadata and/or per-skill tool exposure against native plugin-packaged skills using ordinary fresh-chat prompts. The MCP client still decides when to call a tool.

**Hosting constraints:** Azure Functions **Flex Consumption**, scale-to-zero, no always-ready instances; cold starts may still occur despite faster scaling. Verify SDK-based MCP hosting support/current preview requirements. Monthly execution free grants do not cover required Azure Storage or all networking/logging charges. Set spending safeguards and obtain explicit resource/deployment approval before any Azure changes. Favor Python official MCP SDK, stateless Streamable HTTP, minimal dependencies, local MCP Inspector testing, and GitHub Actions CI/CD. Python is a proposed executor detail, not a user-approved language choice.

**Next Action (permitted now):** Have the user create the OpenAI-documented public example plugin with **No authentication** and the URL `https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp`, install it, and test `roll_dice` in ChatGPT Work; capture actual success/failure. Then prepare a narrow implementation proposal around the already-approved repo/hosting/scope choices. **Code implementation, repo creation, Azure provisioning, credentials, and deployment remain separately gated pending explicit authorization.**

**Blockers / Human Attention:** Actual MCP tool invocation on ChatGPT Plus remains unverified (only the UI was observed). The user has settled the repo, platform, and scope choices. Later: implementation permission; private MCP endpoint access/authentication method; private GitHub read-only credentials; and Azure subscription/storage/cost settings, when deploying.

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
