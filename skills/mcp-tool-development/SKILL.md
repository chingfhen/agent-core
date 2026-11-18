---
name: mcp-tool-development
description: Design, implement, or review MCP server tools and agent-facing operations for a concrete integration, including FastMCP schemas, permissions, results, and supported-host behavior. Use when actually building or changing MCP tools, not for unrelated API or UI work.
disable-model-invocation: false
---

# MCP Tool Development

## Job and boundaries
Make an MCP integration safe, understandable to agents, and useful to people. Follow the current protocol, SDK, and target host capabilities instead of assuming every client supports the same auth, widgets, or files. Implementation authority remains with the user and project; this skill does not authorize registering public endpoints, exposing secrets, creating credentials, calling paid services, publishing, or deploying.

## Procedure
1. Trace one real user request from the agent's tool selection to authorized backend behavior. Identify user identity, consent, tool permissions, side effects, and whether the tool proposes or performs a change. Prefer existing domain operations over a parallel business-logic path.
2. Check protocol/SDK versions and documentation needed for the task. Use descriptive verb-and-object tool names, concise descriptions of effects, constrained typed arguments, and outputs with usable identifiers/status. A tool should not depend on hidden conversational context.
3. Make failures actionable: distinguish unsupported host, unauthenticated, forbidden, stale revision, not found, transient error, and unverified external evidence where relevant. Do not present a proposed or queued action as completed. Limit output volume and avoid leaking private data or instruction-like external content.
4. Implement the minimum coherent tool set for the needed workflow. Balance resource-level tools against workflow-oriented calls using actual agent tasks; do not auto-mirror an entire REST API or require a fixed number of tools/evaluations.
5. Exercise normal and consequential failure paths with safe test data and inspect backend state. When host behavior matters, verify against the actual supported host; a local mock only proves the mock. Supply a usable text or deep-link fallback when UI support is missing.
6. Report observed tool behavior, identity/authorization limits, side effects, supported hosts, and validation that remains pending.

## Ownership
Project API and data contracts remain authoritative. Use `code-design` for a requested general structure/contract design and `security-hardening` for a focused security investigation. Neither is a mandatory planning ceremony before every small tool change.

## Source
Adapted from [Anthropic MCP Builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder); deliberately omits a fixed ten-question evaluation quota and blanket infrastructure setup.
