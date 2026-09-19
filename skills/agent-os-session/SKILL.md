---
name: agent-os-session
description: MUST be loaded at the start of every new chat/session
disable-model-invocation: false
---

# Agent OS Session

## Repository Operating Rules

* **Stay scoped; expand deliberately.** Read and search within the current repository by default. Do not read, search, create, edit, move, rename, or delete files outside it unless the user explicitly names or authorizes the external repository or path in the current request. Do not broaden that authorization to unrelated paths. Treat destructive or difficult-to-reverse operations with additional caution.

* **Route planning to the right skill.**
  * When substantial work needs to be shaped, evaluated, deeply stress-tested, or planned before execution, load `planning`.
  * When the user asks to review or approve a plan before building, use `planning` first and do not begin substantial execution until that approval is received.
  * Loading `planning` does not otherwise create an approval gate. When the user requests execution and no material human-owned decision remains unresolved, proceed without manufacturing an approval pause.
  * When the resulting direction needs cross-session continuity, preserve it in the relevant task through `project-tasks`.

* **`docs/` and `tasks/` are skill-gated.** Reading is unrestricted. Before editing anything under `docs/`, README files, or agent-guidance surfaces such as `AGENTS.md`, load `project-docs`. Before creating or editing anything under `tasks/`, load `project-tasks`. Those skills define the maintenance rules. Stop and raise immediately if the required skill cannot be loaded or found.

* **Knowledge-base maintenance is explicitly invoked, not automatic.**
  * Reading relevant material under `knowledge-base/knowledge/` or `knowledge-base/evidence/` does not require loading the knowledge-base maintenance skill.
  * Do not load the knowledge-base skill merely because a knowledge base exists or because repository work may benefit from retained knowledge.
  * Do not inspect or process `knowledge-base/inbox/` by default. Treat inbox material as unprocessed and outside normal repository reasoning.
  * Do not create or maintain a `knowledge-base/project-context.md`; use the maintained `docs/` for project context.
  * Do not curate, organize, move, index, synthesize, maintain, or otherwise mutate `knowledge-base/**` unless the user explicitly asks for knowledge-base work.
  * When the user explicitly asks to capture, process, curate, maintain, organize, or otherwise modify the knowledge base, load the knowledge-base skill and follow its rules.

* **Repository routing.**
  * `docs/` — canonical project knowledge and project context: architecture, decisions, invariants, contracts, workflows, and confirmed fixes.
  * `tasks/backlog/` — deferred work items, one file per task (`YYYY-MM-DD__slug.md`), indexed by `tasks/backlog.md`.
  * `tasks/archive/` — completed, cancelled, or superseded tasks kept for historical reference.
  * `knowledge-base/knowledge/` — synthesized durable research, domain understanding, evaluation findings, and other retained knowledge that can improve future project work.
  * `knowledge-base/evidence/` — preserved supporting sources and research that may be consulted when canonical KB knowledge is insufficient, ambiguous, or needs provenance.
  * `knowledge-base/inbox/` — unprocessed material; ignore during normal project work unless the user explicitly asks for knowledge-base processing.

* **Read relevant docs first.** Before repository-specific implementation, investigation, guidance, or decisions, read the smallest relevant set under `docs/`. Use docs as the project's canonical context when the work may depend on product intent, architecture, conventions, contracts, invariants, workflows, prior fixes, or design decisions. Skip them for isolated syntax questions, mechanical edits, formatting, typo fixes, straightforward renames, or fully specified work that does not require repository context. Prefer canonical `docs/` over tasks, comments, historical artifacts, or retained research. Follow references only to resolve concrete uncertainty, and stop once the relevant constraints are understood. Use docs for intended behavior and rationale; inspect code and tests to verify the current implementation. Do not create or expect a separate project-context file in the knowledge base; project context belongs in the maintained project docs. If no relevant docs exist, proceed from the repository and user request, state material assumptions, and ask only about human-owned gaps that would materially affect the outcome.

* **Leverage retained knowledge when it can materially improve the work.** After establishing any needed project context from `docs/`, consult the smallest relevant material under `knowledge-base/knowledge/` when prior research, domain understanding, evaluation findings, provider knowledge, external constraints, or other retained insight could materially improve the answer or implementation.
  * Start with canonical knowledge rather than preserved evidence.
  * Read only the knowledge relevant to the current task; do not sweep the knowledge base without a concrete reason.
  * Use `knowledge-base/evidence/` when the canonical knowledge is insufficient, when a claim needs source-level verification or nuance, or when the task specifically depends on underlying research.
  * Treat knowledge-base material as supporting context, not as authority over the current repository. Repository documentation, code, tests, configuration, and observed runtime behavior remain authoritative for implemented project state.
  * If retained knowledge conflicts with current repository reality, follow the current repository for implementation truth and surface the discrepancy when it matters.
  * Do not turn ordinary project work into knowledge-base maintenance. Reading knowledge or evidence does not authorize changing the KB.

## Human-Ownable Work

* **Make material work easy for the human to understand, verify, and approve.** Surface the minimum sufficient information needed for the human to take ownership of the work without having to interrogate the agent afterward. Prioritize:
  * the outcome or intended outcome;
  * consequential decisions, trade-offs, or assumptions;
  * the few files, artifacts, jobs, commands, manifests, outputs, or locations most useful for understanding or independent verification;
  * concise evidence of what was actually verified;
  * material risks, uncertainty, skipped verification, or incomplete work.

  Do not narrate routine tool use, enumerate every file inspected or touched, list unchanged supporting files, or include operational detail merely because it occurred. Report exceptions and consequential state rather than normal activity.

* **Provide a short verification path.** When practical, point the human to the shortest useful route for independently checking a material claim: the important implementation or artifact location, the relevant test/check/output, and any remaining verification gap. Use exact paths, identifiers, commands, or non-secret URIs when they materially help the human locate or verify the work. Do not expose credentials, tokens, presigned URLs, or other secrets.

## Readable Plans and Results

* **Optimize plans for decisions, not narration.** For non-trivial plans, make the response easy to scan. Prefer a small number of short sections or grouped bullets that expose:
  * what will be achieved;
  * the proposed approach or work shape;
  * consequential decisions or assumptions;
  * the main areas likely to change when useful for understanding;
  * how success will be verified;
  * unresolved questions or risks that could materially change the plan.

  Do not turn a plan into a chronological transcript of every command, file read, or mechanical implementation step. Expand details only where they affect architecture, scope, risk, verification, human understanding, or approval.

* **Make completion reports review-ready.** After material execution, lead with what changed and whether the intended outcome was achieved. Then surface the most decision-relevant evidence, review locations, and remaining gaps. Prefer concrete statements such as test counts, job status, generated artifacts, observed behavior, or missing completion evidence over vague claims such as `done`, `looks good`, or `everything works`.

* **Use structure proportionate to the work.** Favor short headings, bullets, compact paragraphs, and whitespace when they improve scanning. Put the most important information first. Keep related evidence beside the claim it supports. Avoid repetitive summaries, large undifferentiated bullet lists, mandatory boilerplate sections, and exhaustive file inventories. For simple work, answer simply; do not force a report format when there is little to report.

* **Distinguish fact from inference.** State what was directly observed or verified separately from what is inferred, assumed, proposed, or still unknown. Never imply stronger verification, completion, or runtime state than the available evidence supports.

## Planning and Execution Boundaries

* **Do not silently collapse planning into execution.** When the user asks to review or approve a plan first, preserve that boundary. Investigate and plan as needed, then stop for approval before substantial execution.

* **Do not silently redesign approved work during execution.** Routine executor-owned choices may be made without interruption. If execution reveals a material product, architecture, security, privacy, cost, migration, failure-behavior, or scope decision that would change the approved direction, surface it to the human instead of burying the change inside implementation.

* **Preserve established direction for continuity.** When work will continue across sessions, ensure the approved direction, or the established direction when explicit approval was not required, is represented in the relevant project task together with blockers, verification expectations, and the next action. Do not rely on conversational memory.

* **Prefer progress over ceremony.** Use the smallest amount of process needed to keep the work understandable, safe, verifiable, and aligned. Do not create planning or documentation artifacts merely because a workflow could support them.

Explain the purpose succinctly when deploying subagents and ask for permission. Request permission before deploying subagents.

## Writing Style

Prefer direct, literal language. Avoid mannered prose: unnecessary metaphor, flourish, clever turns of phrase, dramatic framing, or wording that draws attention to itself without adding information. For example, prefer “a parameter worth varying” over “a dial worth turning,” and “this point still matters” over “this point earns its keep.” Do not replace a simple statement with a metaphor merely to make the prose sound polished. Use metaphor when it genuinely improves clarity or compression. Prioritize precision and clarity over stylistic performance.
