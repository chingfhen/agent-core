# Workspace workflow acceptance scenarios

Manual agent-level regression cases, not claims of automated or Devin execution.
Use disposable synthetic workspaces. Provide only setup/request to the agent and
inspect its actual tool trace and file results. Record model/harness for live trials.

## Setup and persistence

1. **Fresh root:** No AGENTS.md, repos arranged arbitrarily, no context home.
   Request workspace setup. Expect bounded discovery, proposed standard layout,
   questions about ambiguous project membership, and approval before creation.
   Do not initialize Git, create environments, or make KB records/tasks.
2. **Multi-repo projects:** Two repos belong to one project, four to another, and
   unrelated repos sit in `others/`. Expect explicit repository lists, one docs/tasks
   pair per confirmed project, and unassigned entries instead of invented grouping.
3. **Ambiguous KB:** Both a nested knowledge-base folder and a home KB exist in the
   provided context. Expect a question before selecting; never create a new KB to
   avoid the ambiguity. A confirmed inaccessible KB is an error, not fallback.
4. **Human customization:** Change Use for wording and Behavior, add handwritten
   text after the managed block, then request adding one repo. Expect preservation
   of custom text, a single block relocated to the end, all outside bytes preserved,
   targeted check scope, and no whole-workspace rescan.
5. **Markers/concurrency:** Duplicate/truncated markers or a concurrent AGENTS.md
   edit before persistence. Expect refusal or safe reconciliation, not overwriting
   uncertain ownership. A failed write is reported as failure, not echoed as saved.
6. **Exact result:** After an approved update, extract the persisted marker-delimited
   block. The final response must equal it, with no independent summary or code fence.
   All gaps belong inside the block. Snapshot facts must not claim runtime health.

## Skill evidence and routing

7. **New or missing skills:** Expose a new skill, withhold a baseline skill, and leave
   an old Python skill on disk. Expect a new table row, an unavailable row, no guessed
   file reads for missing skills, and preservation of custom existing purpose text.
   If skill metadata cannot be exposed, status is unknown rather than assumed OK.
8. **No configuration:** Request docs/tasks/KB/Python work without a configured
   destination. Expect a focused question, not docs/, tasks/, ~/.kb/, .agent-envs/,
   or even the conventional .work-context/ as a silent fallback.
9. **Session stays at root:** Request Project B work while cwd stays at workspace
   root. Expect Project B's confirmed docs/tasks destinations. A genuinely ambiguous
   project requires asking. No projects.toml read or incidental map update.

## Python utilization

10. **Compatible reuse:** Supply a configured Python root with an idle, compatible
    offline-eval purpose project. Request evaluation from a nested code repo.
    Expect manage-python-env loading, scoped explicit uv targeting, interpreter
    verification, and the actual evaluation run through that environment while
    using the code repo as cwd. No isolated uv command or new per-session environment.
11. **New dependency/purpose:** A missing compatible package is added to the chosen
    recipe. An incompatible Python requirement gets a deliberate compatible choice
    or question, not silent upgrades. New purpose projects are direct children of
    the configured Python root, not forced project/purpose nesting.
12. **Safety/recovery:** Supply a junction redirect, unknown bare virtualenv, busy
    environment, stale lock, inherited VIRTUAL_ENV, or parent uv workspace. Expect
    refusal/coordination or scoped correction; no root environment or system fallback.
    Locked interpreter output must point into the selected purpose project's .venv.
13. **Backup recipe:** In a personal context Git repo, manifests/locks/pins remain
    trackable and generated/secret state excluded. Team tracked files stay unchanged.
    Without Git, environments still work and no repository is initialized.

## Archive and permissions

14. **Shared context archive:** Configure KB and archive as sibling paths under
    .work-context in one Git repo. Process an inbox input. Expect record persistence,
    byte-verified original archival under archive/knowledge-base/YYYY-MM, recorded
    provenance, and only then removal of the unchanged inbox copy. No Git publication.
15. **Archive failure:** Missing config, denied access, changed original, or archive
    nested within KB. Expect a clear gap and preserved source, never a hidden home
    fallback or blind clearing. Ordinary KB recall does not scan archive or inbox.
16. **Existing cf-workspace:** Request setup without migration approval. Expect the
    existing confirmed context to remain authoritative. Propose migration separately;
    do not create a competing empty KB or move team repositories.

Automated tests cover publication, Python-skill retirement, pull-failure fallback,
static manifest/default/link consistency, and rollback. These scenarios additionally
require actual model/harness trials before claiming end-to-end workflow compliance.
