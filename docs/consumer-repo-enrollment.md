# Consumer Repo Enrollment

**Last Updated:** 2026-06-21

**Status:** Current

**Source Of Truth:** Defines how consumer repos are enrolled into Agent OS v1 and how executor-facing local skill aliases behave.

**Update When:** Steward enrollment workflow, repo-local manifest schema, harness alias policy, or manifest-consumer rules change.

### Read First

- Consumer repos are enrolled per device by steward workflows, not by manual repo editing.
- The steward-managed local skill surfaces are `.claude/skills/*` for Claude and `.opencode/skills/*` for OpenCode.
- Executors consume ordinary repo-local skill aliases and do not need to know whether the installed surface is canonical, symlinked, or copied.
- `.agent-os.json` is generated repo-local state and gitignored by default.
- On Windows, enrollment prefers symlinks and falls back to directory junctions when symlink privileges are unavailable.
- Trust the setup only when the selected skills are live aliases; copied local skill directories are transitional and should be auto-replaced by steward workflows.
- Consumer repos do not receive a shared bootstrap skill; executor skills that need Agent OS context read `.agent-os.json` directly.

### Scope

This document covers repo-local manifests, local skill surface installs, ignore policy, steward safety rules, and manifest-consumer expectations for consumer repos.

### Not Here

- Canonical skill authoring in `skills/`
- Live implementation status or open task sequencing
- Memory ledger internals beyond how consumer repos opt into memory behavior

### Current Contract

#### Enrollment Model

- Each consumer repo is enrolled per device by a steward workflow.
- Enrollment writes a repo-local `.agent-os.json`, installs selected local skill aliases, updates repo ignore rules for steward-managed outputs, and records device-local steward state.
- Enrollment does not require an existing Git worktree; if `.gitignore` is missing, the steward creates it.
- Device-local steward state is untracked.
- This system does not depend on modifying consumer repo `AGENTS.md` files.
- Enrollment and sync both converge the repo toward live aliases rather than copied skill directories.

#### Generated Consumer-Repo Surfaces

- `.agent-os.json`
- Local skill aliases under `.claude/skills/*`, which are consumed by Claude
- Local skill aliases under `.opencode/skills/*`, which are consumed by OpenCode
- Exact managed ignore entries for the generated surfaces above

- Official OpenCode docs confirm project skill discovery for `.opencode/skills/*`.
- Steward enroll and sync keep the same canonical skill set aligned across both managed surfaces.
- Codex repo-local skill semantics remain future work.
- Exact or divergent local copies under those alias paths are not the trusted steady state; they are auto-replaced on enroll and sync.

#### Manifest Schema V1

- `version`
- `repo_id`
- `scope`
- `scope_id`
- `agent_os_path`
- `memory_enabled`

Canonical schema: `schemas/agent-os-manifest.schema.json`

Example file: `schemas/examples/consumer-repo.agent-os.example.json`

Example:

```json
{
  "version": 1,
  "repo_id": "consumer-repo",
  "scope": "repo",
  "scope_id": "consumer-repo",
  "agent_os_path": "C:\\Users\\chingfhen\\Documents\\ching\\agent-core\\agent-core",
  "memory_enabled": false
}
```

- `agent_os_path` remains in the manifest so future scripts and memory tooling can still locate the canonical repo.
- `.agent-os.json` is gitignored by default because it carries per-user and per-device integration state.

#### Manifest Consumers

- Consumer repos do not receive a shared bootstrap skill.
- Executor skills that need repo-local Agent OS context read `.agent-os.json` directly.
- `agent-os-memory` is the current canonical executor skill that consumes manifest fields.
- If a future executor skill needs manifest context, keep that read local to the skill instead of reintroducing a separate shared bootstrap step.
- `uv run scripts/enroll_repo.py sync --repo <path>` removes retired `agent-os-bootstrap` aliases and stale registry references from older enrollments.

#### Link Strategy

- The first installer command is `uv run scripts/enroll_repo.py`.
- Default link mode is `auto`: try a directory symlink first.
- On Windows, if symlink creation fails because the current client lacks the required privilege, fall back to a directory junction.
- The actual link mode used for a repo is recorded in `.agent-os-state/enrollments.json` so repair runs can reuse the same behavior.
- The local steward registry also remembers the working device link mode so later repo enrollments can skip repeated failed symlink probes.
- When you already know the machine lacks symlink privileges, use `--link-mode junction` to skip the failed symlink probe and finish faster.

#### Live Alias Guarantee

- After a successful enroll or sync, the selected skills should be live aliases to the canonical `~/agent-os/skills/*` directories.
- For this workflow, both directory symlinks and directory junctions count as live aliases.
- Exact or divergent copied skill directories do not satisfy the guarantee even if they happen to match the canonical content today.
- Edits propagate both ways through a live alias: changing the canonical skill updates the consumer repo immediately, and editing through the consumer path edits the canonical source.
- `uv run scripts/enroll_repo.py verify --repo <path>` returns success only when the repo is in that live-alias steady state.

#### Ignore Policy

- Gitignore `.agent-os.json` by default.
- Gitignore exact steward-managed alias paths by default.
- If a repo already ignores a broader harness path, reuse that coverage rather than duplicating narrower ignore entries.
- Do not rely on Git to ignore symlinks or alias installs automatically.

#### Steward Safety Model

- Preflight every planned target path as `missing`, `managed`, or `conflict`.
- `managed` means the path is already steward-installed, clearly points at the expected Agent OS skill target, or is a matching local skill directory that should be auto-replaced.
- Create `missing` paths automatically.
- Repair or replace only clearly `managed` paths automatically.
- Matching local skill directories are auto-replaced with live aliases and reported as a notice to the human.
- A local directory that declares a different skill name, is a file, or points at some unrelated location is still a `conflict` and must not be overwritten automatically.
- Stop and ask before replacing a `conflict` path that is an unrelated real file or directory.
- Do not wipe whole harness directories when only exact managed alias paths are steward-owned.

#### Memory Integration Boundary

- `memory_enabled` in `.agent-os.json` controls whether memory behavior should be available in that repo.
- Memory instructions belong in `agent-os-memory`, which reads `.agent-os.json` directly when memory is enabled.
- Memory remains a pilot; the canonical truth stays append-only in `memory/memories.jsonl`, while generated search state in `memory/memory.sqlite` and `MEMORY_INDEX.md` remains disposable.
- When `memory_enabled` is true, stewards may also install the local `agent-os-memory` skill so executors can use list/search/write flows without direct knowledge of `jsonl` or `sqlite` internals.
- Topic discovery should come from generated list/search commands exposed by that skill, not from a hand-maintained registry in consumer repos.
- Steward agents still own canonical memory tooling and publication in `~/agent-os`; enabling memory in a consumer repo does not make that repo the source of truth.

### Related Surfaces

| Surface | Path | Why It Matters |
| ------- | ---- | -------------- |
| Repo architecture | `README.md` | High-level orientation and top-level boundaries for Agent OS. |
| Steward contract | `AGENTS.md` | Defines steward-agent operating rules and overwrite safety behavior. |
| Memory skill | `skills/agent-os-memory/SKILL.md` | Executor-facing list/search/write memory guidance for memory-enabled repos. |
| Enrollment script | `scripts/enroll_repo.py` | Implements enrollment, repair, local registry updates, and Windows link fallback behavior. |
| Memory script | `scripts/memory.py` | Canonical steward memory tooling behind the local memory skill. |
| Manifest schema | `schemas/agent-os-manifest.schema.json` | Defines the v1 `.agent-os.json` contract. |
| Verification command | `uv run scripts/enroll_repo.py verify --repo <path>` | Confirms whether a repo is in the trusted live-alias steady state. |
| Active memory task | `tasks/2026-06-19__agent-os-memory-real-repo-validation-bookmark.md` | Tracks the next real enrolled-repo validation pass for memory-enabled repos. |

### Decisions

| Date | Decision | Rationale |
| ---- | -------- | --------- |
| 2026-06-19 | Consumer repos are enrolled per device by steward workflows. | Repo setup should be repeatable and steward-managed rather than relying on manual manifest placement. |
| 2026-06-19 | Executors consume repo-local skill aliases. | Executor agents should use ordinary local skill names without caring about canonical provenance. |
| 2026-06-19 | `.agent-os.json` is gitignored by default. | The manifest contains per-user and per-device integration state and should not confuse teammates. |
| 2026-06-19 | Managed ignore rules default to exact alias paths. | Narrow ignores avoid masking other repo-owned harness files. |
| 2026-06-21 | Consumer repos do not receive a shared bootstrap skill. | Only `agent-os-memory` currently needs manifest context, so skill-local reads are simpler than a separate bootstrap layer. |
| 2026-06-21 | Shared local project skills sync to both `.claude/skills` and `.opencode/skills`. | Claude and OpenCode should each receive the same canonical skills through their native project-local discovery paths. |
| 2026-06-19 | Windows enrollment defaults to symlink with junction fallback. | The first pilot lacked symlink privileges, so a non-destructive fallback was required to complete setup. |
| 2026-06-19 | Device-local enrollment state lives in `.agent-os-state/enrollments.json`. | Repair runs need a local registry without tracked repo noise. |
| 2026-06-19 | Consumer-repo skill copies are transitional and auto-replaced. | The whole value of the system depends on trustworthy live canonical updates rather than stale duplicates. |
