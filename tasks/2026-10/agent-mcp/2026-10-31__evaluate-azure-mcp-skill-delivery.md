# Task: Evaluate and prototype remote MCP delivery of Agent Core skills

**File:** `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md`
**Created:** 2026-10-31
**Last Updated:** 2026-10-31
**Priority:** Next
**Status:** Active

**Goal:** Make canonical Agent Core instructions easier for hosted agents such as ChatGPT to discover and retrieve, using a small read-only MCP server, while gaining practical MCP development experience.

**Why:** Local Pi/OpenCode/Devin already discover native skills through `agent-core sync`. ChatGPT's GitHub connector fetches known files but does not automatically surface the registered skills, their descriptions, or applicable `AGENTS.md` as native instruction-discovery metadata.

**Current State:** On 2026-10-31 the user approved the repository, hosting, and scope below. **ChatGPT Plus MCP capability is verified end-to-end:** the user installed the sample custom MCP plugin and ChatGPT successfully called `mcp__MCP_Test__roll_dice` with `sides=20`, receiving `4`. Direct retrieval of Agent Core files via GitHub was also tested. No new MCP repo, code, Azure resources, or deployment yet.

**Chosen Direction (approved 2026-10-31):** Build toward a **read-only, instruction-delivery-only** MCP MVP. Use a separate private `chingfhen/agent-core-mcp` service repository and Azure Functions with scale-to-zero (Flex Consumption is the initial target), zero always-ready instances, and GitHub Actions deployment once approved. `chingfhen/agent-core` remains the sole canonical source for SKILL.md, references, AGENTS.md, and existing native sync. No KB/task writes, vector DB, replicated skill content, or enforcement gateway. Hosting must minimize costs; Azure Functions' storage/networking are not necessarily free.

**Architecture:** The new private service repository owns its SDK dependencies, tests, and Azure delivery workflow independently of Agent Core's zero-dependency local sync runtime. The service fetches allowlisted canonical skills, reference files, and applicable guidance from `chingfhen/agent-core` via narrowly scoped read-only GitHub credentials. Tool surface should be small and stateless; use MCP Streamable HTTP. Do not ship maintained copies of skills.

**Discovery design issue:** Merely exposing generic `list_skills`/`read_skill` operations does not make agent selection automatic. Compare descriptive tool metadata and/or per-skill tool exposure against native plugin-packaged skills using ordinary fresh-chat prompts. The MCP client still decides when to call a tool.

**Authentication and dependency design (researched, not yet approved):** Distinguish three trust boundaries: (1) ChatGPT → MCP: OAuth user authorization, with Microsoft Entra ID and Azure Functions' built-in MCP authentication (currently preview) as the preferred experiment; no Google Cloud account or new database should be needed. ChatGPT requires MCP protected-resource/OAuth metadata, PKCE S256, supported client registration or configured static client and exact redirect URI; Entra's lack of DCR means test pre-registered ChatGPT client compatibility. Validate issuer, audience, scopes, expiry and one permitted user; do not assume Azure Easy Auth automatically works with ChatGPT. (2) MCP → private GitHub Agent Core: fine-grained PAT limited to `chingfhen/agent-core` Contents:read (simplest initial path), held in encrypted Azure Function app settings; consider GitHub App tokens only if the PAT's lifetime/rotation becomes cumbersome. No Google OAuth or GitHub user sign-in needed. (3) GitHub Actions → Azure: use Azure OIDC federated credentials for passwordless deployment; app registration and constrained Azure RBAC required. Azure Functions requires a Storage account; it is billed separately from Flex free executions, so zero total cloud cost is not guaranteed. Azure Key Vault is optional for an initial personal MVP; secret storage and rotation still needed. No external vector DB, Redis, Firebase, or paid auth provider is planned.

**Hosting implementation fork to validate:** Azure Functions offers native MCP extension triggers and SDK-based self-hosted MCP (the latter documented as preview). MCP extension defaults to a system-key requirement that ChatGPT might not supply; when OAuth is enabled, configure the endpoint for anonymous *Function-key* access while enforcing OAuth before serving private content, never leaving it publicly unprotected. Confirm exact transport URL and metadata routes experimentally. Use the official MCP SDK locally for learning, and select the Functions integration compatible with reliable ChatGPT OAuth and fast scale-to-zero.

**Hosting constraints:** Azure Functions **Flex Consumption**, scale-to-zero, no always-ready instances; cold starts may still occur despite faster scaling. Verify SDK-based MCP hosting support/current preview requirements. Monthly execution free grants do not cover required Azure Storage or all networking/logging charges. Set spending safeguards and obtain explicit resource/deployment approval before any Azure changes. Favor Python official MCP SDK, stateless Streamable HTTP, minimal dependencies, local MCP Inspector testing, and GitHub Actions CI/CD. Python is a proposed executor detail, not a user-approved language choice.

**Next Action (permitted now):** Prepare a small design/implementation proposal for the separate `agent-core-mcp` repository. Spike/prove Azure Functions MCP hosting with OAuth and ChatGPT's plugin before treating production auth as supported. Verify endpoint/metadata, static OAuth client registration and ChatGPT redirect compatibility, source authorization, and invocation from natural prompts. **Repo creation, code implementation, Azure provisioning, credentials, and deployment still require separate explicit authorization.**

**Blockers / Human Attention:** ChatGPT Plus MCP tool access is verified. Remaining: implement/deploy authorization, choose/validate compatible Microsoft Entra ID registration and MCP discovery; obtain explicit permission before creating code or billable Azure resources; set up a read-only GitHub credential and Azure subscription/cost guardrails at deployment time.

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
