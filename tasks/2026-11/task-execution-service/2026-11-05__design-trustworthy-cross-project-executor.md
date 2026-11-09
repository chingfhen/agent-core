# Task: Harden and validate a trustworthy cross-project Task Execution Service

**File:** `tasks/2026-11/task-execution-service/2026-11-05__design-trustworthy-cross-project-executor.md`
**Created:** 2026-11-05
**Last Updated:** 2026-11-09
**Priority:** Later
**Status:** On Hold

**Goal:** Design and eventually prove one trustworthy execution service on a Fly Sprite with OpenCode for **both** authorized delegated project work and automatic Knowledge Base synthesis/background maintenance. Unify the queue, dispatcher, executor, audit and recovery lifecycle rather than maintaining two independent pipelines; preserve project-task continuity and agent-consumable synthesized KB knowledge.

**Why:** The human values **one comprehensible pipeline**, auditability, traceability, bounded permissions, local continuation, and low interactive-session token costs. KB capture should stay lightweight while background agents autonomously maintain synthesized knowledge. Avoid building a second task manager, duplicate dispatch infrastructure, or mandatory human review of routine KB synthesis.

**Current State:** Direction discussed on 2026-11-04–09; **the unified queue/dispatch design remains unresolved and earlier concrete proposals did not satisfy the human**. No Sprite, dispatcher, queue, worker, credentials, background KB process or audit integration has been deployed or verified. Intentionally on hold for a fresh discussion, not for implementation.

**Chosen Direction (principles, not technical design):** **One persistent Sprite, OpenCode primary, globally synced Agent Core skills and one unified durable job queue/execution/audit foundation**, with distinct scoped authority per workload. GitHub Actions is the proposed trigger to wake Sprite when KB records change; its transport and the queue location are undecided. Keep task and Git permissions authoritative, preserve local continuation, and avoid full FirstMate-style orchestration. **Do not treat Sprite SQLite, GitHub Actions-as-queue, a particular wake endpoint, or separate pipelines as selected.**

## Fresh-session design brief — 2026-11-09

**The question to solve:** How do *authorized human project delegation* and *automatic KB maintenance* become two job types inside **one actual operational pipeline** without parallel queueing, orchestration, or audit systems? The human wants a new agent to reconsider the architecture, not mechanically implement the assistant's previous proposals.

### Agreed boundaries

- **Fast foreground KB capture:** The main agent writes reusable `records/` and maintains record indexes at the end of sessions with minimal token/time cost. It should eventually stop synthesizing `knowledge/` synchronously.
- **Background owner:** A background worker becomes the **sole maintainer of `knowledge/`**, using new `records/` plus selectively relevant existing knowledge/evidence. Its output is mainly for future agents. Eventual consistency is acceptable; no human review of routine knowledge-page updates is desired. Allow no-op when synthesis adds no value. Broader Anthropic-style historical dreaming is interesting but may have a separate cadence/budget.
- **One executor, several workload types:** Both KB synthesis and human-delegated work must share the service's job submission, queue, execution, status, observability and audit mechanisms. A durable queue **exists conceptually by decision**; its implementation and authoritative home remain open. Avoid inventing a Markdown Project Task for every synthesis run. Conversely, project work continues to reference existing authorized Project Tasks or an approved execution brief.
- **Trigger direction:** KB records pushed to GitHub `main` should be able to trigger GitHub Actions, which wakes Sprite and submits work. Exact dispatch method, acknowledgment/durability semantics, retries, and whether the same gateway serves clients such as ChatGPT, local OpenCode and GitLab remain undecided. The Sprite should sleep when idle and remain awake during active work using a tested job hold.
- **Fully agent-managed knowledge:** Automated changes to `knowledge/` need grounded sources, validation, protection against concurrent writers and durable audit receipts. This does **not** authorize background agents to edit production Agent Core skills or promote new `AGENTS.md` rules.
- **One Sprite/OpenCode:** Reuse persistent checkouts, installed skills and sessions if beneficial, but prove the cost/complexity advantage rather than assuming GitHub-hosted execution is categorically wrong.

### Unresolved questions for next discussion

1. What is the smallest **single job contract** that naturally describes both a standing, event-triggered KB synthesis operation and an explicitly authorized Project Task execution, without pretending the two have identical approval requirements?
2. Where does a job become **durably queued before acknowledgment**, especially if Sprite is sleeping, unreachable or crashes? Compare queue placement and transport options from first principles, rather than automatically choosing Sprite SQLite, a GitHub queue, HTTP endpoint or `sprite exec`.
3. Who owns trigger handling, wake-up, deduplication, backlog catch-up, concurrency, retries, cancellation and active-run hold? How can new KB records be processed without lost or duplicated commits?
4. What is the single audit contract connecting trigger → queued job → attempt → actual OpenCode sessions → verification → final Git outputs/cost? Distinguish dispatch accepted from execution completed and verified.
5. Is **KB synthesis/background maintenance the best first proof of the unified delegation service**, or does it require a small prerequisite proof of generic queue/executor behavior? Give a reasoned phased plan, not a premature implementation.
6. What cheaper model/provider and private-data boundary is acceptable for unattended maintenance, and how should uncertain corrections fail safely?

**Next permitted action:** On explicit human resumption, read this brief and the sources below, then discuss and compare genuinely different unified architectures, choose a leading design with clear trade-offs, and seek human approval **before** implementation, account changes, cloud spending, model authentication or skill edits. Do not create the infrastructure simply because this task is saved.

**Deliverables for the next planning round:**
- A **unified job/queue/dispatch contract** that works for both KB synthesis and approved project delegation, with clear ownership of pending state, execution status, results and audit evidence.
- A minimal consumer/onboarding contract and hard **service-level and job-specific readiness gates**, with exact fail-closed behavior, conditional permissions and a way to prove required skills have actually loaded.
- A small standardized **execution receipt** contract, task→attempt→OpenCode parent/child-session→Git evidence association, retention/access plan, and human-facing task checkpoint rules. Flexible project-defined deliverable formats.
- A proportionate isolation/credential/security and authorization design, addressing why Git worktree alone is not a sandbox; protected audit storage, duplicate requests, interruptions and cancellation.
- A staged, low-risk acceptance plan comparing native OpenCode capabilities, official Fly MCP access and a minimal wrapper; no speculative permanent supervisory architecture.
- Later, on explicit authorization, a harmless proof-of-concept demonstrating remote execution, accurate result status, audit retrieval, Git/Project Task local continuation and safe rejection on failed gates.

**Success Bar (for planning):** A fresh agent can propose a coherent **single-pipeline design handling both KB and project jobs**, show how a sleeping Sprite accepts and durably queues requests, identify who owns audits/retries/permissions, compare alternatives fairly and describe verifiable readiness/failure checks; the human approves the design before implementation. **Success Bar (later pilot):** Task submitted through one client; valid gates passed; authorized OpenCode run in isolated scope; actual sessions and output evidence linked automatically; failed checks do not mark acceptance; local OpenCode can resume from Git/task; read-only review and a deliberate rejection/failure are fully traceable. This pilot is not yet authorized.

**Decisions and constraints:**
- **Project Tasks owns durable intent/permissions/continuation.** Use project `AGENTS.md` for routing and review behavior; do not impose AdReadyClips conventions universally or silently close tasks.
- Three outputs: (A) flexible deliverable at an approved accessible location; (B) standardized deterministic receipt covering authorization, revisions, attempt/session IDs, verification and private audit links; (C) Project Task checkpoint through the canonical skill when authorized, or a proposed checkpoint otherwise.
- Three outcomes: **execution finished**, **verification passed**, **task accepted** are distinct. Neither model self-report nor draft PR/MR constitutes acceptance.
- Optional independent **LLM-as-judge** is qualitative evidence, not formal proof, and must never override tests or authorize deployment. For skill comparisons, consider blinded/reordered inputs and scenario-based evaluation.
- Make startup and task-specific **readiness gates hard fail-closed**: committed Agent Core and global OpenCode skill availability, actual Project Tasks load for saved tasks, conditional loading of Project Docs/KB/Agent Lessons, runtime/model/session capture, enrolled project, valid task/success bar/authorization, enforceable scopes/limits, isolation, immutable attempt/audit storage, delivery destination and ability to cancel/recover. Verify actual skill load before substantive work; do not accept model claims as evidence.
- Start with read-only and bounded branch-write/review profiles. Git branch/commit/push rights only when explicitly approved; no inherent merge/deploy/destructive rights or unbounded spend. Use separate credentials/sandbox enforcement when needed.
- Prefer a small registry + file-based attempt store; no mandatory database, vector search, fleet scheduler, or default LLM supervisor. Keep Sprite asleep when idle, with job-aware active-work hold for actual executions.
- **No implementation, new repository, provider sign-in, cost, custom MCP, cloud provisioning, modifying production skills, merge or deployment permitted in this deferred task.**

**Next Action (permitted only when human resumes):** Start with the 2026-11-09 unified-pipeline questions above, especially **what constitutes one job and where the queue lives**. Develop a genuinely satisfactory architecture for KB synthesis as a first workload alongside project delegation, then seek design approval before proposing any implementation. Do not implement merely because this task exists.

**Blockers / Human Attention:** User deliberately paused because earlier concrete queue/transport recommendations were unsatisfactory. Unified job/queue semantics, wake/dispatch protocol, audit retention, failure recovery, security, real OpenCode skill/session verification, provider cost and Sprite execution lifecycle remain untested. Sprite has not been provisioned. Explicit design and implementation approvals are separate.

## Resume Context
- Fresh KB-memory design source: `chingfhen/knowledge-base` `main:knowledge-base/records/2026-11/agent-workflows/2026-11-09--anthropic-components-of-agent-memory-and-dreaming.md` — fast capture, independent KB and eventual background dreaming. The present task advances that concept but has not implemented it.
- Canonical current docs: `docs/workspace-configuration.md#interactive-capture-and-deferred-offline-memory-maintenance` — currently in-session capture and deferred background work; don't mistake the proposed future design for deployed behavior.
- Private KB record: `chingfhen/knowledge-base` `main:knowledge-base/records/2026-11/agent-workflows/2026-11-05--trustworthy-cross-project-task-execution-service.md` — current decisions and readiness contract.
- Earlier KB: `knowledge-base/managed/2026-10-25--personal-agent-workspace-architecture.md` and `knowledge-base/managed/2026-10-25--sprite-opencode-first-setup-runbook.md` in the same private repo — approved baseline architecture, not executed.
- `knowledge-base/records/2026-10/agent-workflows/2026-10-25--delegation-ci-task-attempts-and-observability.md` — task/attempt/session distinction and review policy.
- This repo: `skills/project-tasks/SKILL.md`, `skills/project-docs/SKILL.md`, `skills/knowledge-base/SKILL.md`, `docs/consumer-repo-enrollment.md` — canonical workflow and global OpenCode skill publication.
- Related, different workstream: `tasks/2026-11/chatgpt-skill-loaders/2026-11-05__evaluate-thin-native-skill-loaders.md` — native ChatGPT skill discovery deferred separately; `tasks/2026-10/agent-mcp/2026-10-31__evaluate-azure-mcp-skill-delivery.md` — prior read-only Azure skill MCP plan, **not required** for Task Execution Service.
