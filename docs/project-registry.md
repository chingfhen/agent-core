# Project Registry

The project registry tells agents where project-owned files live on the current machine.

It is machine-local configuration.

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
knowledge_base = "/home/cdsw/smart-search-workspace/knowledge-base"
```

Another machine may contain completely different projects and paths.

## Fields

- `description` — optional human-readable description.
- `root` — local filesystem root used to identify the project.
- `docs` — exact location owned by the project documentation workflow.
- `tasks` — exact location owned by the project task workflow.
- `knowledge_base` — exact knowledge-base root. Usually a local filesystem path, but workflows that support another backend may use its supported root representation.

A project may omit a surface it does not use.

## Resolution

When a file-producing workflow runs:

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

```toml
knowledge_base = "/home/cdsw/smart-search-workspace/knowledge-base"
```

means the knowledge-base workflow uses that configured knowledge-base root.

If no matching project or required surface is configured, do not guess a writable location.

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

The registry defines where personal project workflow files belong.

Git repository boundaries do not define these locations.

A project's `docs`, `tasks`, or `knowledge_base` may live inside a Git repository, outside it, or elsewhere entirely.