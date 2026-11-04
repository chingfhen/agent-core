# Task: Harden and validate a trustworthy cross-project Task Execution Service

**File:** `tasks/2026-11/task-execution-service/2026-11-05__design-trustworthy-cross-project-executor.md`
**Created:** 2026-11-05
**Last Updated:** 2026-11-05
**Priority:** Later
**Status:** On Hold

**Goal:** Design and eventually prove a minimal cross-project Task Execution Service on one Fly Sprite with OpenCode. Permit approved work to be delegated from ChatGPT or laptop OpenCode; return durable deliverables, machine-generated audit evidence and a normal Project Task checkpoint, enabling continued work from local OpenCode.

**Why:** The human values **trust in delegation, deterministic traceability, stable permissions and ordinary local task continuation** more than a live remote agent session or an elaborate multi-agent fleet. FirstMate is useful inspiration, but native OpenCode skills/subagents and existing Agent Core Project Tasks should carry most of the workflow.

**Current State:** Conceptual direction discussed/accepted 2026-11-04–05 and recorded in the private KB; no Sprite setup, Task Execution Service, wrapper, dispatcher, MCP dispatch, security boundary, model authentication or end-to-end audit validation implemented. The earlier approved one-Sprite/OpenCode setup guide remains the starting dependency. This task preserves a future investigation/hardening workstream, not authority to create cloud resources.

**Chosen Direction:** **One Sprite, one globally synced Agent Core skill installation, OpenCode primary, a small deterministic execution wrapper, lightweight durable attempt registry, project-specific permissions and existing project Git policies.** The task itself remains in its existing project Tasks location. A future CLI and optional authenticated MCP adapter should call the same executor operations. Default to continuing locally from the saved Project Task and fetched Git branch; remote session inspection is optional for diagnosis. Avoid a second task database, mandatory live-session handoff, separate Azure read-only skill MCP or full FirstMate fleet.

**Deliverables for the next planning round:**
- A minimal consumer/onboarding contract and hard **service-level and per-task readiness gates**, with exact fail-closed behavior, conditional permissions and a way to prove required skills have actually loaded.
- A small standardized **execution receipt** contract, task→attempt→OpenCode parent/child-session→Git evidence association, retention/access plan, and human-facing task checkpoint rules. Flexible project-defined deliverable formats.
- A proportionate isolation/credential/security and authorization design, addressing why Git worktree alone is not a sandbox; protected audit storage, duplicate requests, interruptions and cancellation.
- A staged, low-risk acceptance plan comparing native OpenCode capabilities, official Fly MCP access and a minimal wrapper; no speculative permanent supervisory architecture.
- Later, on explicit authorization, a harmless proof-of-concept demonstrating remote execution, accurate result status, audit retrieval, Git/Project Task local continuation and safe rejection on failed gates.

**Success Bar (for planning):** A fresh agent can propose an implementable minimum prototype, distinguish observed tool capability from untested assumptions and describe pass/fail checks for all key trust requirements; human explicitly approves design before implementation. **Success Bar (later pilot):** Task submitted through one client; valid gates passed; authorized OpenCode run in isolated scope; actual sessions and output evidence linked automatically; failed checks do not mark acceptance; local OpenCode can resume from Git/task; read-only review and a deliberate rejection/failure are fully traceable. This pilot is not yet authorized.

**Decisions and constraints:**
- **Project Tasks owns durable intent/permissions/continuation.** Use project `AGENTS.md` for routing and review behavior; do not impose AdReadyClips conventions universally or silently close tasks.
- Three outputs: (A) flexible deliverable at an approved accessible location; (B) standardized deterministic receipt covering authorization, revisions, attempt/session IDs, verification and private audit links; (C) Project Task checkpoint through the canonical skill when authorized, or a proposed checkpoint otherwise.
- Three outcomes: **execution finished**, **verification passed**, **task accepted** are distinct. Neither model self-report nor draft PR/MR constitutes acceptance.
- Optional independent **LLM-as-judge** is qualitative evidence, not formal proof, and must never override tests or authorize deployment. For skill comparisons, consider blinded/reordered inputs and scenario-based evaluation.
- Make startup and task-specific **readiness gates hard fail-closed**: committed Agent Core and global OpenCode skill availability, actual Project Tasks load for saved tasks, conditional loading of Project Docs/KB/Agent Lessons, runtime/model/session capture, enrolled project, valid task/success bar/authorization, enforceable scopes/limits, isolation, immutable attempt/audit storage, delivery destination and ability to cancel/recover. Verify actual skill load before substantive work; do not accept model claims as evidence.
- Start with read-only and bounded branch-write/review profiles. Git branch/commit/push rights only when explicitly approved; no inherent merge/deploy/destructive rights or unbounded spend. Use separate credentials/sandbox enforcement when needed.
- Prefer a small registry + file-based attempt store; no mandatory database, vector search, fleet scheduler, or default LLM supervisor. Keep Sprite asleep when idle, with job-aware active-work hold for actual executions.
- **No implementation, new repository, provider sign-in, cost, custom MCP, cloud provisioning, modifying production skills, merge or deployment permitted in this deferred task.**

**Next Action (permitted only when human resumes):** Revisit this task and its linked KB record; inspect current OpenCode/Sprite/Fly MCP interfaces and existing FirstMate patterns; produce a concise minimal design with readiness contract, audit/receipt schema, security model and end-to-end test plan. Then seek approval for one small, safe Sprite/runtime prototype. Do not implement merely because the task exists.

**Blockers / Human Attention:** User intentionally paused until a later session. Security enforcement vs broad Fly MCP shell tools, verified skill-loading observation, remote OpenCode session trace availability, Git branch/checkpoint publication, model/hosting cost and authentication are not yet tested. Sprite has not been provisioned. Await explicit approval before spending or external changes.

## Resume Context
- Private KB record: `chingfhen/knowledge-base` `main:knowledge-base/records/2026-11/agent-workflows/2026-11-05--trustworthy-cross-project-task-execution-service.md` — current decisions and readiness contract.
- Earlier KB: `knowledge-base/managed/2026-10-25--personal-agent-workspace-architecture.md` and `knowledge-base/managed/2026-10-25--sprite-opencode-first-setup-runbook.md` in the same private repo — approved baseline architecture, not executed.
- `knowledge-base/records/2026-10/agent-workflows/2026-10-25--delegation-ci-task-attempts-and-observability.md` — task/attempt/session distinction and review policy.
- This repo: `skills/project-tasks/SKILL.md`, `skills/project-docs/SKILL.md`, `skills/knowledge-base/SKILL.md`, `docs/consumer-repo-enrollment.md` — canonical workflow and global OpenCode skill publication.
- Related, different workstream: `tasks/2026-11/chatgpt-skill-loaders/2026-11-05__evaluate-thin-native-skill-loaders.md` — native ChatGPT skill discovery deferred separately; `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md` — prior read-only Azure skill MCP plan, **not required** for Task Execution Service.
