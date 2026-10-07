# Task: Install Personal Skills and Guidance Globally

**File:** `tasks/2026-10-07__global-personal-skill-sync-and-guidance.md`
**Created:** 2026-10-07
**Last Updated:** 2026-10-07
**Priority:** Now
**Status:** Active

**Goal:** Replace per-project Agent Core skill deployment with one machine-level sync that installs the owner's personal skills and global agent guidance for Pi, Codex, OpenCode, and Claude Code.

**Why:** The configured Agent Core skills are personal workflows that should remain available across projects. Copying them into each project creates stale duplicates, repeated update work, local ownership metadata, and possible conflicts with genuinely project-specific skills. The mandatory `agent-os-session` skill is also less reliable than guidance loaded automatically by each harness.

**Success Bar:** On a new Windows computer with Git, CMD, and a supported Python installation, the owner can clone this repository to `%USERPROFILE%\.agent-core`, run a CMD installer without PowerShell, `uv`, `pip`, or downloaded Python packages, and then run `agent-core sync`. Sync fast-forwards the clean checkout, safely publishes the configured personal skills and global guidance, reports what it did, and leaves unrelated user and project content untouched. Subsequent updates require only `agent-core sync`.

**Chosen Direction:**

- Keep the canonical private checkout fixed at `~/.agent-core`.
- Rename `core-skills.toml` to `personal-skills.toml`; keep the list manual and authoritative rather than inferring every directory under `skills/`.
- Install real managed skill copies under `~/.agents/skills/`, which is supported globally by Pi, Codex, and OpenCode.
- Expose the same installed skills to Claude Code through managed links or Windows directory junctions under `~/.claude/skills/`; do not maintain a second independently editable skill copy.
- Replace `agent-os-session` with one concise canonical `global/AGENTS.md`, published as complete managed files to each harness's native global instruction location.
- Make `agent-core sync` the normal command. Retain the old project-local apply path only long enough to provide explicit migration and deprecation behavior.
- Use a standard-library-only Python implementation and a CMD-first installer. Determine the oldest practical Python version through a bounded compatibility check before locking the package requirement.

**Current State:**

- The current launcher and copy engine implement `agent-core apply --here` and plain Git-root apply into project-local `.agents/skills/`.
- `README.md`, `AGENTS.md`, `docs/agent-core-operating-manual.md`, and `docs/consumer-repo-enrollment.md` describe that project-local workflow as current.
- `tasks/2026-09-15__simplify-private-skill-distribution-bookmark.md` is closed and accurately records the superseded design; keep it as history.
- `core-skills.toml` currently includes both `agent-os-session` and the stale repository `knowledge-base` skill.
- The canonical Knowledge Base workflow now lives in Google Drive at `My Drive/Agents/My General Knowledge Base/_workflow/SKILL.md`, Drive file ID `1S6Y_RIRZUkxcY59v_XuRrVIi6LHYCubX`. Its Google Drive adapter is file ID `1fyZMXQq7YTm_X8fphdprjIl6BmXwZu1f`.
- Pi, Codex, and OpenCode document `~/.agents/skills/` as a user-global Agent Skills location. Claude Code documents `~/.claude/skills/` as its personal skill location and supports symlinked skill folders.
- Pi's user-global guidance path is `~/.pi/agent/AGENTS.md`; Codex uses `~/.codex/AGENTS.md`; OpenCode uses `~/.config/opencode/AGENTS.md`; Claude Code uses `~/.claude/CLAUDE.md`.
- This working tree already contains uncommitted approved edits to `skills/project-tasks/SKILL.md` and `skills/project-docs/SKILL.md`, plus a pre-existing untracked `NUL` entry. Preserve those changes and do not treat them as part of this task's implementation.

**Next Action:** In a fresh session, load the required steward, planning, project-docs, and project-tasks guidance; inspect current code and tests; then perform the bounded Python/discovery compatibility checks in Phase 1 before implementing the approved global sync contract.

**Blockers:** None for Phase 1. Before publishing the final installer, verify that OpenCode does not expose duplicate names when it scans both `~/.agents/skills/` and Claude's linked entries. If identical real-path links are not deduplicated, stop at that phase and present a non-duplicating fallback rather than silently changing OpenCode's environment or shipping duplicate skills.

**Human Attention:**

- Global availability does not make every repository skill personal. Only `personal-skills.toml` controls publication; project-specific skills remain project-owned.
- The installer may manage only exact declared skill destinations and exact global guidance files. It must preserve unrelated skills such as existing third-party entries under `~/.agents/skills/`.
- The global guidance source must be materially shorter than the current session skill and contain only rules useful before project-specific guidance or on-demand skills are loaded.
- Do not configure OAuth, MCP credentials, Git credentials, secrets, or office-machine security policy. Those remain separate machine-local setup.

**Permission Boundary:** The owner approved this distribution redesign, creation of the global guidance source, removal of the production `agent-os-session` skill after its durable rules are migrated, and removal of the stale repository `knowledge-base` skill. The canonical Drive KB skill must not be deleted or rewritten as part of this task.

**Verification:** Use automated standard-library tests plus manual harness discovery checks. Do not claim future-agent behavior solely from file existence or prose review.

**Docs Sync:** Not Synced

**Target Docs:** `README.md`, `AGENTS.md`, `docs/agent-core-operating-manual.md`, `docs/consumer-repo-enrollment.md`, and any directly affected project-registry documentation.

**Relevant Code:** `agent_core/bootstrap.py`, `agent_core/apply.py`, `tests/test_agent_core.py`, `pyproject.toml`, `core-skills.toml`, `skills/agent-os-session/`, and `skills/knowledge-base/`.

## Desired New-Computer Workflow

CMD must be sufficient on Windows:

```cmd
git clone <private-repo-url> "%USERPROFILE%\.agent-core"
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
agent-core sync
```

The installer must not require PowerShell. A PowerShell installer may remain or be added as an optional convenience, and a small POSIX installer may be retained when useful, but neither may be required for the Windows path.

The CMD installer should use an available supported `py` or `python` interpreter to install a small command shim in a user-owned bin directory. Update the user PATH without `setx` truncation risk, elevated privileges, `uv`, `pip`, or modifying system-wide configuration. Use only standard-library Python and normal Windows user facilities. Print an exact result and tell the owner when a new terminal is required.

After initial setup, `agent-core sync` is the only normal update command.

## Target Installation Layout

### Personal skills

```text
~/.agents/skills/<personal-skill>/
```

These are real managed copies published from the committed repository sources selected by `personal-skills.toml`.

Claude Code receives managed aliases:

```text
~/.claude/skills/<personal-skill>
    -> ~/.agents/skills/<personal-skill>
```

Use directory junctions on Windows when they provide an unprivileged, reliable implementation; use symlinks where appropriate on other systems. Preserve one installed content authority. Do not silently fall back to independent duplicate copies if that causes Pi or OpenCode to discover duplicate skill names.

### Global guidance

Create one canonical repository source:

```text
global/AGENTS.md
```

Publish it as complete Agent Core-managed files to:

| Harness | Destination |
| --- | --- |
| Pi | `~/.pi/agent/AGENTS.md` |
| Codex | `~/.codex/AGENTS.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |

Absent or empty destination files may be initialized. Refuse a non-empty unowned destination rather than overwriting it. Once owned, refuse local modifications unless the owner explicitly resolves them; do not add a force path by default.

## Global Guidance Contract

Distill—not mechanically copy—the useful content of `skills/agent-os-session/SKILL.md` into `global/AGENTS.md`.

Keep rules that must shape behavior before an on-demand skill or project file would normally load:

- stay within explicitly authorized scope;
- use planning when the human requests plan review before execution;
- preserve planning-versus-execution permission boundaries;
- load `project-docs` and `project-tasks` before mutating their owned surfaces;
- read relevant project docs before repository-specific decisions;
- invoke KB maintenance only when explicitly requested;
- use the canonical Drive KB workflow and report when it cannot be accessed instead of falling back to the stale repository skill;
- ask permission before deploying subagents;
- report outcomes, consequential decisions, verification, and remaining gaps honestly;
- use direct, literal language.

Remove duplicated detail already owned by `planning`, `project-docs`, `project-tasks`, or the Drive KB skill. Remove assumptions that every project contains local `docs/`, `tasks/`, or `knowledge-base/` directories. Remove the startup instruction and visible confirmation for loading `agent-os-session`; global guidance is loaded automatically.

Project-specific instructions remain in each project's `AGENTS.md`, `CLAUDE.md`, or equivalent and layer with the global guidance.

## Sync Contract

`agent-core sync` should retain the current launcher's useful safety properties:

1. resolve the fixed `~/.agent-core` checkout;
2. require the canonical checkout to be clean;
3. fast-forward with ordinary authenticated Git;
4. cross a fresh-process boundary before running the newly pulled implementation;
5. require configured source files to match committed content;
6. validate every source and destination before changing any;
7. preserve unrelated global skills and parent-directory content;
8. stage and fingerprint real skill copies;
9. update skill copies, Claude links, and guidance files as one coherent operation with backup and rollback;
10. publish machine-local ownership only after successful replacement;
11. refuse unsupported filesystem entries, unowned collisions, and modified managed content;
12. never modify repository `.gitignore` files or project source merely to expose global skills.

Place machine-local ownership state outside the tracked checkout or in another location that cannot make the canonical Git worktree dirty. Document the exact location and recovery behavior. Keep the implementation standard-library-only.

Removing an item from `personal-skills.toml` should remain non-destructive by default unless a separately explicit prune or migration operation is invoked. Do not infer the personal list from all `skills/` directories.

## Cheap Observability

Every sync should make the result easy to verify without producing a long diagnostic transcript.

On success, report at least:

- resolved canonical checkout and commit;
- selected manifest and configured skill count;
- shared skill destination and counts for added, updated, recreated, and unchanged entries;
- changed skill names, while allowing unchanged names to be summarized by count;
- Claude alias destination and alias count/status;
- each global guidance destination and whether it was added, updated, or unchanged;
- ownership-state location;
- whether a harness restart or reload is needed.

On refusal or failure, report the exact conflicting destination, why it is unsafe, and the smallest human action needed. Do not expose credentials or unrelated user paths. Successful output is evidence of completed filesystem operations, not proof that every harness used the content correctly.

## Legacy Migration and Removal

### Retire production sources

After `global/AGENTS.md` contains the retained behavior and its installation is tested:

- remove `agent-os-session` from the personal manifest;
- delete `skills/agent-os-session/`;
- remove the requirement to load it from this repository's `AGENTS.md` and all directly affected docs;
- remove `knowledge-base` from the personal manifest;
- delete the stale `skills/knowledge-base/` directory and its local backend helpers;
- point global guidance to the canonical Google Drive skill and adapter instead of maintaining another workflow copy.

Do not modify or delete the Drive canonical skill.

### Retire project-local managed copies

Provide an explicit migration command, provisionally:

```text
agent-core retire-local --here
```

It should:

- operate only on the exact selected directory;
- read existing Agent Core ownership records;
- remove only managed skill copies whose fingerprints still match;
- preserve modified, tracked, unowned, or unrelated `.agents` content;
- remove only Agent Core's exact obsolete ownership and local-exclusion entries;
- fail with actionable detail rather than partially guessing;
- never scan arbitrary repositories automatically.

Keep `agent-core apply --here` and plain apply only as documented deprecated compatibility during migration, or remove them only after the migration path and owner-facing instructions make existing installations recoverable. Do not silently retarget an old project-local command to a global destination.

## Implementation Plan

### Phase 1: Verify compatibility assumptions

- Inventory the current Python APIs and syntax that require Python 3.11.
- Run or adapt the existing suite under available Python 3.9 and 3.10 interpreters when possible.
- Select the oldest practical supported Python that needs only small, maintainable standard-library changes. Target 3.9+ if reasonable; prefer an honest 3.10+ or existing 3.11+ requirement over adding a general TOML parser, vendoring a dependency, or creating substantial compatibility code solely for a lower version number.
- Confirm current Pi, Codex, OpenCode, and Claude global skill discovery behavior.
- Test whether OpenCode deduplicates Claude aliases that resolve to the same installed skill. Do not proceed with a duplicate-name design.

Publish the chosen minimum Python version and discovery result into the task before downstream implementation if they materially alter the approved layout.

### Phase 2: Establish the global publication contract

Rename the manifest, define exact source and destination ownership, define machine-local state, and update the bootstrap command model around `sync`. Preserve current source tracking, clean checkout, fresh-process, conflict refusal, rollback, and additive-removal safety.

### Phase 3: Implement bare installation and sync

Build the CMD-first installer, command shim, global skill publisher, Claude aliases, guidance publisher, ownership state, rollback, and concise observability. Keep all runtime code dependency-free.

### Phase 4: Replace session routing and remove stale skills

Create and validate `global/AGENTS.md`, publish it to native harness paths, update repository-specific `AGENTS.md`, then remove the two explicitly retired production skill directories and their manifest entries.

### Phase 5: Migrate legacy project installs

Implement and test the explicit safe retirement command. Validate one representative prior `apply --here` installation without touching unrelated `.agents` content.

### Phase 6: Synchronize durable guidance

Rewrite the repository architecture, operating manual, distribution contract, package metadata, steward guidance, and directly affected links so global sync is the only normal workflow. Keep the closed 2026-09-15 task as historical evidence rather than rewriting it.

## Verification Contract

### Automated tests

Extend the standard-library test suite to cover:

- manifest rename and strict validation;
- source tracking and committed-content requirements;
- first global sync and repeat no-op sync;
- added, updated, recreated, unchanged, removed-from-config, and locally modified skill states;
- preservation of unrelated entries under `~/.agents/skills/` and `~/.claude/skills/`;
- Claude alias or junction identity and broken-link recovery;
- all-target preflight before any mutation;
- backup and rollback across skills, aliases, guidance, and ownership publication;
- absent, empty, non-empty unowned, unchanged owned, modified owned, and missing managed guidance files;
- clean-checkout refusal, pull failure, and fresh-process implementation loading;
- CMD shim generation and safe user-PATH handling without PowerShell, `uv`, or `pip`;
- legacy project-copy retirement, tracked/modified refusal, unrelated-content preservation, state cleanup, and exact exclusion cleanup;
- output summaries and actionable failure messages;
- the selected minimum Python version.

Run the suite directly with supported Python interpreters, not only through `uv`:

```text
python -m unittest discover -s tests -v
python -m compileall -q agent_core tests scripts
```

`uv` may still be used by maintainers as an optional convenience, but no installation or runtime acceptance criterion may depend on it.

### Harness checks

On an isolated test home before touching real user-global files:

1. Run the CMD installer path without PowerShell.
2. Run `agent-core sync` and inspect its concise report.
3. Confirm each configured personal skill exists once under the intended user-global discovery model.
4. Confirm Pi, Codex, and OpenCode discover the shared `~/.agents/skills/` entries.
5. Confirm Claude discovers the linked `~/.claude/skills/` entries.
6. Confirm Pi and OpenCode do not expose duplicate skill names because of Claude compatibility scanning.
7. Confirm each harness loads its global guidance and still layers project-specific guidance.
8. Modify one managed target and confirm the next sync refuses all replacements before mutation.
9. Add an unrelated third-party skill and confirm sync leaves it unchanged.
10. Verify exact global paths and IDs/fingerprints from machine-local ownership state.

### Migration check

Create or use an isolated representation of the former `apply --here` state. Run the explicit retirement command and prove that it removes only unchanged managed copies and exact Agent Core metadata while preserving unrelated and modified project content.

## Completion Conditions

The task is complete only when:

- the documented three-command CMD setup works without PowerShell, `uv`, or `pip`;
- `agent-core sync` is safe, repeatable, observable, and atomic across all configured global outputs;
- personal skills are globally discoverable without duplicate names;
- global guidance replaces the session skill and loads through native harness mechanisms;
- `skills/agent-os-session/` and the stale `skills/knowledge-base/` are removed locally only after their required routing has a canonical replacement;
- existing project-local installations have a safe explicit migration path;
- unrelated global and project content survives all tested success and failure paths;
- the lowest supported Python version is tested and documented honestly;
- current docs and guidance no longer direct the owner to `agent-core apply --here` for normal personal use;
- the final report gives exact changed repository paths, generated global destinations used during verification, test results, remaining migration actions, and any harness behavior that could not be proven automatically.
