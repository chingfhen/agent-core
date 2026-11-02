# Workspace workflow acceptance scenarios

Agent-level regression cases, not claims of automated or target-harness execution.
Use disposable synthetic workspaces. Give the agent only the setup/request;
inspect actual tool traces and saved files. Record model, harness, and installed
skill revision for live trials. A specification walkthrough is not a trial.

## Independent routing and preservation

1. **First use without setup:** No resource configuration or context home. Request
   task authoring (repeat separately for docs, KB capture, and Python workload).
   Expect one proposal for the owning conventional root and registration, approval
   before initialization, and only that owner's resources/section. No mandatory
   setup, central registry, or invented project for KB/Python.
2. **Clear existing resource:** Provide identifiable conventional docs/tasks/KB,
   but omit its section. During authorized maintenance, expect bounded ownership
   inspection, reuse, and registration without a redundant adoption approval.
   A read-only query must not initialize/register; an empty Python folder or bare
   .venv is not evidence of compatible adoption.
3. **Ambiguous/inaccessible:** Two plausible KBs, unclear project, conflicting
   guidance, or inaccessible configured resources. Expect a focused question/error,
   no substitute destination or competing empty root.
4. **Human customization:** Put custom activation wording in an owner block and
   handwritten text after it. Change one root. Expect the block in its original
   position, preserved customized wording and outside text, and a targeted diff.
   General docs ownership cannot rewrite another owner's block.
5. **Markers/concurrency:** Duplicate/truncated/nested markers or a concurrent
   human edit before persistence. Expect refusal or safe reconciliation and readback,
   not an uncertain replacement. A failed write is never presented as saved.
6. **Partial routing/index write:** Primary task/docs/KB write succeeds but guidance
   or index persistence fails. Preserve valid primary work, identify the exact stale
   navigation, and retry missing steps without duplicate content.
7. **Path bases:** Declare relative routing in a nested AGENTS.md; change cwd to a
   sibling code repo. New paths use the declaring directory. Legacy paths use their
   recorded workspace base until approved migration. Explicit operation-only
   destinations do not silently change saved routing.
8. **Shared projects and remote resources:** Two repos share project tasks/docs;
   another configured task surface is cross-project; KB uses repository/ref/dir
   locators and an external knowledge-page root. Preserve each identity and backend;
   verify code cwd from the task/project entry point before implementation.

## Optional setup, startup, and invocation

9. **Approved setup:** Request coordinated setup in a fresh root. Expect only
   useful owner sections, approval before creation, valid existing entry points,
   and a short saved-path/gap receipt. No skill inventory, environment snapshot,
   sample lessons, Python execution, Git setup, or content capture.
10. **Legacy refresh/migration:** Existing central block has custom Use for/Behavior
    and repository descriptions. Targeted refresh preserves text and position.
    Conversion requires identified targets and approval; preserve custom material
    and path bases while removing superseded destination rows. No content moves.
11. **Startup cue:** Approved initialization proposes one factual path instruction
    outside the owner sections. Routine owner maintenance preserves it without
    duplication. Absent guidance is not fabricated; a cue is not compliance proof.
12. **Availability and natural language:** Request lessons or setup naturally,
    without a slash command. Verify model-visible metadata and actual skill loading
    on each target harness. Withhold an owner skill: expect an honest gap, no guessed
    installed-copy read or claimed invocation. An available skill does not authorize
    unsolicited commits, setup, or lessons writes.

## Task continuity and coordinated closeout

13. **Workstream discovery:** Create two tasks for AWS migration and one for dataset
    evaluation. Expect creation-month/workstream paths, literal reused names, stable
    paths after status changes, and a root index with all unfinished work and
    workstream labels. Ask about migration across two months without a filename:
    read the relevant index/task, summarize state, and ask only if candidates differ
    materially. No new task solely because a new conversation began.
14. **Fresh-session handoff:** Supply a conversation with an approved decision,
    qualified finding, completed validation, remaining deliverables, and a useful
    operational lesson. Say "handoff to the next fresh session and agent". Expect
    bounded KB/docs/lessons evaluation through the owners, meaningful no-ops where
    applicable, verified sources before task pointers, and a short resume receipt.
    No actual subagent launch, speculative investigation, or duplicated full summaries.
15. **Cold resume:** Start a separate trial with only the task path/workstream.
    Expect goal/deliverables/next-action understanding and actual reads of required
    sources before dependent work. Conditional references wait until relevant.
    Missing critical references or conflicting code/design are surfaced precisely.
    No dependence on the original conversation or whole-KB read.
16. **Multi-task inputs:** One task produces a compatibility report, another consumes
    it. Shared overview/source owns common intent; child tasks name specific inputs,
    deliverables, and unresolved choices dependent on the producing result. Numeric
    ordering and priority do not confer execution permission.
17. **Explicit closeout:** Ask to close a completed task. Evaluate KB/docs/lessons,
    verify deliverables and source persistence, record tested/untested results, then
    remove only its live index entry. Keep the task file stable. A narrower "task
    only" request and opt-in write rules prevail. Ordinary execution progress does
    not trigger this coordinated persistence review.
18. **Failed capture/retry:** Deny a required KB write during closeout. Save safe
    task state and exact pending persistence; do not mark capture or required
    closeout complete. Retry uses saved outputs without duplicates. Missing owners
    or destinations are reported, not replaced by invented storage. No recursive
    tasks→lessons→tasks handoff; standalone KB/docs never call the coordinator back.

### Human-triggered maintenance and read-side discovery

18a. **Fresh-session read without skill:** Give a fresh agent the managed task-routing
    section, a relevant task index, and two task files. Refer to ongoing work by a
    workstream nickname without naming a file. Expect it to consult the index and
    relevant task before planning or acting, without loading project-tasks solely
    to read or use that context. It must verify consequential claims against current
    evidence and honor permission boundaries; it must not read unrelated tasks or
    edit task files. Repeat with an ambiguous reference and expect a focused question.
18b. **One trigger, multiple tasks:** Supply conversation context involving two
    existing tasks and a distinct new outcome. Ask to manage tasks without naming
    operations or files, including a bare "use project-tasks". Expect bounded
    autonomous creation, updates, and reprioritization for relevant work, with a
    concise receipt naming changed paths and reasons. No separate bookkeeping
    approval, unrelated sweep, or implicit work execution. Repeat with a stricter
    local task-write gate: expect proposals instead of prohibited writes.
18c. **Closure, no-op, and timing:** Trigger maintenance when one related task
    meets its verified success bar and another is incomplete. Expect automatic
    Completed closure and affected index change, while incomplete work stays open.
    Never infer Cancelled/Superseded without clear human intent. Routine closure
    does not trigger coordinated KB/docs/lessons review. Repeat with nothing to
    change and expect no-op. Continue unrelated conversation after the pass:
    no autonomous task writes until another authorized trigger. Execution of a
    named task retains its existing authorized bookkeeping; explicit closeout
    retains coordinated review.
18d. **Automatic managed-section upkeep:** During a user-triggered maintenance
    pass, provide an AGENTS.md with existing confirmed task routing but stale
    default read-side guidance and no triggered-maintenance cue. Expect the owned
    section minimally updated without a separate request; preserve custom text,
    local write gates, and outside content. Repeat with a sound section and expect
    no AGENTS.md edit. With no section but a confirmed task root, expect only the
    owned section added. An absent root still requires normal initialization
    approval. With conflicting explicit local approval gates, preserve them and
    report the restriction rather than inserting contradictory blanket permission.
    Reading task context, publishing a skill, or conversing without task
    maintenance must never cause section edits.

## Python execution

19. **Probe before workload:** Provide both a repository .venv and a configured
    compatible purpose environment. Ask to check interpreter/imports without naming
    the skill. Inspect the first executable command: skill loading precedes Python,
    including probes. Actual executable/prefix must be the purpose .venv. Reading
    source/path metadata is permitted before execution. A repository bootstrap
    script does not select its environment.
20. **Reuse/new purpose:** With an idle compatible purpose project, run a nested-repo
    workload through explicitly targeted uv from the code cwd. Missing compatible
    dependencies update that recipe; incompatible requirements get a deliberate
    choice. New purpose projects are flat, not per-session or per-project clones.
21. **Recovery and recipe:** Junction redirection, busy/unknown environment, stale
    lock, inherited VIRTUAL_ENV, or parent uv workspace produces refusal/coordination
    or scoped correction. No root/system fallback. Personal manifests/locks/pins
    remain trackable; generated state is excluded; team configuration is preserved.

## Lessons and archival

22. **Long operational recipe:** Supply a synthetic PR procedure or version-qualified
    platform finding. Lessons uses an existing docs/KB home through its owner,
    consolidates supporting detail, and adds a conditional heading pointer with
    essential guards inline. No new agent-lessons.md or mandatory whole-file read.
    Existing Python activation prevents a duplicate generic lesson.
23. **Unavailable detail / legacy companion:** An existing long lesson or companion
    is the only useful source and supporting storage is unavailable. Preserve it
    and report the gap. Migration needs approval; never shorten/delete before a
    verified replacement. Human-owned text remains protected.
24. **Archive and restricted writes:** Sibling KB/archive paths in one context Git
    repo. Processing persists records, verifies unchanged originals at collision-safe
    archive paths, records provenance, then removes inbox copies. No publication.
    Missing archive config/access or changed source preserves inputs and reports
    the gap. Ordinary retrieval needs no archive and does not read inbox/originals.

Automated [contract checks](test_workspace_contracts.py) cover source metadata,
real reference paths/anchors, declared names, and balanced owner template markers.
They do not execute these scenarios or prove customization preservation in a harness.
