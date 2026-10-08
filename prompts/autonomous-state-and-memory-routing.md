Depreciated for a skill instead.

# Autonomous State And Memory Routing

**Status:** Current

**Purpose:** Historical prompt snippet for repos that use `tasks/`, `docs/`, `source-material/`, and `archive/`.

Use `global/AGENTS.md` as the canonical live policy. This prompt remains only as source material for wording distilled into automatically loaded global guidance.

## Canonical Snippet

```md
### Autonomous State & Memory Routing

- **Stay in-repo; ask first.** Operate only within this repo. Don't read, search, or act on files outside it unless the user names an external path in the current request. If you need something outside the repo, or something is obviously human-gated — a judgment call, a fact only the user has, a one-sentence clarification — ask. Don't hunt the filesystem or spin in circles when the user can resolve it directly.

- **`docs/` and `tasks/` writes are skill-gated.** Reading them is free. Load `project-docs` before editing anything under `docs/`, and `project-tasks` before creating or editing anything under `tasks/`; those skills carry the maintenance rules.

- **Routing.** `docs/` = stable project truth (decisions, invariants, contracts, confirmed fixes); `tasks/backlog/` = deferred future work, dated `YYYY-MM-DD__slug.md`, with `tasks/backlog.md` as a thin index. `source-material/` = external references, research, and seed inputs. `archive/` = only content superseded by a newer canonical source.

- **Read-Relevant-Docs-first.** Make sure you are grounded with reading relevant `docs/`, before proceeding with any significant response or execution of work.  
```
