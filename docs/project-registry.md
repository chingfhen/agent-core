# Project Registry

The project registry tells registry-aware workflows, including `project-docs` and `project-tasks`, where project-owned files live on the current machine.

It is machine-local configuration. The [knowledge-base skill](../skills/knowledge-base/SKILL.md) does not read this registry: it uses an explicit current root, applicable agent instructions, or the local `~/.kb/` default. Its archive default is `~/.kb-archive/`.

## Registry Location

Always use:

```text
~/.agent-core/projects.toml
```

Do not commit this file to Git.

Each machine maintains its own registry because filesystem paths differ between machines.

## Project Entry

Example:

```toml
[projects.smart-search]
description = "OCBC Smart Search"
root = "/home/cdsw/smart-search-workspace"
docs = "/home/cdsw/smart-search-workspace/docs"
tasks = "/home/cdsw/smart-search-workspace/tasks"
```

Another machine may contain completely different projects and paths.

## Fields

- `description` — optional human-readable description.
- `root` — local filesystem root used to identify the project.
- `docs` — exact location owned by the project documentation workflow.
- `tasks` — exact location owned by the project task workflow.
- `knowledge_base` — legacy field, no longer consumed by the knowledge-base skill. Existing machine-local values may remain, but an intended custom KB root must be selected through the skill's current configuration rules.

A project may omit a surface it does not use.

## Resolution

When a registry-aware workflow runs:

1. Read `~/.agent-core/projects.toml`.
2. Identify the project whose `root` contains the current working directory.
3. Use the exact configured surface for that workflow.

For example, if the active project contains:

```toml
tasks = "/home/cdsw/smart-search-workspace/tasks"
```

then the project-task workflow creates, reads, updates, moves, and deletes task files only within:

```text
/home/cdsw/smart-search-workspace/tasks
```

It must not choose another nearby `tasks/` directory.

Likewise:

```toml
docs = "/home/cdsw/smart-search-workspace/docs"
```

means the project documentation workflow uses that configured docs location.

The registry does not select a KB root. Do not automatically copy a legacy `knowledge_base` value into agent guidance or remove it during ordinary KB work.

If no matching project or required surface is configured, follow the owning workflow's explicit fallback rules rather than guessing from nearby folders.

## Mutation Reporting

After creating, editing, moving, or deleting a project-owned file, report the exact resolved path or location to the human.

Example:

```text
Created task:
/home/cdsw/smart-search-workspace/tasks/2026-09-30__evaluate-search.md
```

This is a cheap observability check so the human can immediately see which project surface was changed.

## Ownership

The human owns project-registry configuration.

Agents may modify `~/.agent-core/projects.toml` only when explicitly asked to register, remove, or change a project.

Normal project workflows read the registry but do not modify it.

## Principle

The registry defines locations only for workflows that explicitly consume it.

Git repository boundaries do not define these locations.

A project's `docs` or `tasks` may live inside a Git repository, outside it, or elsewhere entirely. The KB has its own independent location rules.