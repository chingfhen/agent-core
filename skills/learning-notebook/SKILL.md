---
name: learning-notebook
description: >
  Create a guided, runnable Jupyter notebook that helps a human understand a
  technical subject through explanation and hands-on code. Use when the human
  asks for a learning notebook or an interactive notebook lesson. Organize it
  in the confirmed notebook collection, prepare and verify its Python environment,
  run safe checks, and open it in Jupyter when possible.
disable-model-invocation: false
---

# Learning Notebook

## Job and boundaries

Turn a learning question into a notebook the human can read, run, change, and
use to understand a real mechanism. Deliver the whole experience: a focused
lesson, a usable Python environment and kernel, safe verification, and an open
notebook when the machine permits it. Optimize for understanding, not notebook
length or a showcase of features.

Use for a requested learning notebook or interactive notebook lesson, not every
request for an explanation or notebook used for production analysis. A request
authorizes creating the requested notebook, its collection navigation, necessary
personal environment dependencies, safe verification, and local Jupyter startup,
subject to local permissions and the boundaries below. It does not authorize
changing project source or team environments, capturing to the KB, updating project
docs or tasks, publishing work, exposing private data, or incurring unapproved
external effects. Respect a narrower request, review-only scope, and stricter gates.

## Scope the learning

Infer the human's goal, likely familiarity, and useful depth from the request and
context. Make a sensible small lesson for a clear request; do not demand a syllabus,
fixed lesson format, or a long questionnaire. Select a concrete causal path and
keep peripheral product features out. Use `learning` to choose the mental model,
mechanism, important observations, and decisions; use `readability` to make the
lesson easy to follow without losing necessary qualifications.

If a missing choice would materially change the lesson, access, cost, data exposure,
or safety, investigate what can be established first, then ask one focused question
at a time. Use `grilling` when the human requests deeper interrogation or unresolved
dependent scope decisions genuinely warrant it; don't turn an ordinary clear notebook
request into a grilling session. Once enough is known, proceed.

Prefer a real, minimal integration when it is central to the requested understanding
and access, authorization, and safe execution allow it. A service-backed lesson may
need credentials, network access, a paid account, or human action. If those are
missing, explain the trade-off and ask only when the choice between waiting for the
real integration and a clearly labeled local demonstration would materially change
the lesson. Never silently substitute a mock for a real service or imply a local
result proves the external integration worked. A local lesson is appropriate when it
actually teaches the requested mechanism without that service.

## Resolve the notebook collection

1. Use the human's explicitly selected destination for this operation or the
   `Learning Notebooks Root` in applicable `AGENTS.md`. A one-time destination
   does not silently change saved routing. Confirm the personal workspace scope;
   cwd or a Git root alone does not establish it. Resolve new relative paths from
   the directory containing the declaring guidance; preserve recorded legacy bases.
2. When routing is missing, inspect and reuse an unambiguous, compatible personal
   notebook collection only when its identity and ownership are established. Do
   not adopt a folder just because of its name. Report inaccessible configured
   roots and ask about ambiguous ownership or conflicting destinations; never
   silently create a competing collection.
3. If no collection is configured or suitable, propose
   `<confirmed-workspace>/.work-context/learning-notebooks/` and obtain one approval
   before initializing and registering it. A human-selected one-time destination
   can be used without registering it. Respect narrower local write gates.
4. For approved persistent registration, load `project-docs` before changing
   applicable agent guidance. Add or maintain only this skill's marked section,
   preserving other sections and human wording. Reread before writing; refuse
   duplicate, nested, incomplete, or ambiguous markers and reconcile concurrent
   edits without overwriting them. Do not write routing merely because a collection
   was read, and do not modify global guidance without authorization.

Creation-time routing cue, customized to the confirmed location:

```markdown
<!-- BEGIN LEARNING NOTEBOOKS -->
## Learning Notebooks
Learning Notebooks Root: <confirmed location>
For notebook discovery, consult the collection's INDEX.md. Load learning-notebook
when creating a guided, runnable notebook lesson.
<!-- END LEARNING NOTEBOOKS -->
```

Use the existing collection's established organization when compatible. For a new
collection, use one shallow semantic group and creation month, for example:

```text
<root>/
  INDEX.md
  arize-observability/
    2026-11/
      2026-11-07__tracing-fundamentals.ipynb
```

Choose a meaningful subject group and a short descriptive slug. Reuse groups;
create only needed directories. Dates are creation dates, not claims about the
events being studied. Keep paths stable; never overwrite or rename an existing
notebook to resolve a collision. Select a distinct descriptive name instead.
Keep `INDEX.md` as a lightweight discovery point, grouped by subject and ordered
newest first within each group. Link the actual notebook and give its title, date,
and a short description; maintain only affected entries and preserve unrelated
content. Read back and verify the link. If index or routing maintenance fails,
preserve the valid notebook and report the partial result. Don't create a second
catalogue or automatically archive, delete, or migrate existing lessons.

The notebook collection is not a KB, project docs, or task surface. Read relevant
existing context where useful, but use `knowledge-base`, `project-docs`, and
`project-tasks` for their own explicitly authorized writes and location rules.
Creating a notebook alone does not authorize capture or maintenance there.

## Design the notebook

Ground product-specific APIs and changing behavior in relevant current, reliable
sources; use project code and docs when the request concerns that project. Cite
useful sources near the lesson or at its end. Distinguish confirmed facts, illustrative
code, and uncertainties; do not invent behavior or imply an unexecuted example ran.

Create a valid `.ipynb` with readable Markdown and executable code cells. At the
start, state the learning goal, prerequisites, how to run the cells in order, and
any external access, cost, data, or resource effects. Then build a short coherent
path appropriate to the topic:

- Explain the key idea and the causal connection the code will reveal.
- Introduce a small operation, show how to observe its result, and explain what
  the result means and what it does not establish.
- When useful, change one meaningful input or component, predict or compare the
  result, and show a failure clue or decision that transfers to real work.
- End with concise takeaways or next steps only when useful; don't force quizzes,
  diagrams, exercises, or a fixed number of sections.

Place explanations next to the cells they clarify. Minimize boilerplate while
exposing the important operations. Make the main path runnable in order from a
fresh kernel, with expected observations rather than invented exact outputs. Make
stateful cells and rerun behavior clear; avoid destructive operations and isolate
optional actions. Use small synthetic or explicitly authorized data. Never put
credentials, private data, or sensitive service output into notebook source, saved
outputs, logs, indexes, or reports. Use existing approved secret mechanisms rather
than prompting the human to paste secrets into a cell.

Use a diagram only if it makes a real relationship easier to understand. The
`mermaid-markdown` skill targets Markdown files, not notebook cells; do not assume
it can edit notebooks or that Jupyter renders Mermaid. When renderer support is
unknown, prefer a simple text explanation or another supported representation;
include a textual equivalent for an informative visual.

## Prepare, verify, and open

1. Load `manage-python-env` before any Python command or dependency operation.
   Select or create a compatible purpose project under its confirmed root, honor
   its routing, shared-environment coordination, package-policy and permission
   rules, and execute through that project. Add only needed lesson dependencies,
   including Jupyter and kernel support when needed. Do not use a team `.venv`
   or alter team manifests unless explicitly authorized under that skill's rules.
2. Verify the selected interpreter using `manage-python-env`. Start the Jupyter
   server through that same purpose environment, select a kernel whose actual
   `sys.executable` and prefix resolve to that environment, and verify the match.
   Do not assume server and kernel use the same Python or overwrite another
   kernelspec. If a dedicated kernelspec is needed, use an owned, distinct name
   and report it. Stop and diagnose a mismatch rather than falling back to system
   Python or installing packages from notebook cells.
3. Validate notebook structure and execute the main path from a fresh kernel in
   order when safe and authorized. Check important outputs against the documented
   behavior, and correct failures within scope. Distinguish a validated local path
   from unexecuted service-dependent cells; don't claim full execution if access,
   permissions, cost, data sensitivity, or another blocker prevented it. Avoid
   executing the same external effects twice merely to verify; never run
   consequential or paid operations without the required approval.
4. Check saved notebook content and outputs for secrets, private data, and bulky or
   misleading transient output. Prefer a clean starting notebook when appropriate;
   do not remove useful, safe teaching output without reason. Warn about effects
   and cleanup for any persistent resources actually created. Do not delete
   resources or other people's data without authorization.
5. Keep the Jupyter server bound to localhost with its normal authentication enabled,
   open the actual notebook in the user's browser, and leave that server available
   for the learning session. Provide a fresh kernel for the human after validation
   where safe, without repeating external effects. Verify the server is reachable
   and the notebook/kernel selection as far as the environment permits; do not
   claim the browser opened without observing it. Do not disable authentication or
   expose the server on a network interface to work around access. Treat
   token-bearing URLs as secrets: don't persist or log them unnecessarily; share
   a connection link only through an appropriate user-visible channel when needed.

If browser launch, local access, packages, or required service access is blocked,
preserve the notebook and report exactly what was verified, the blocker, and the
shortest safe way to continue. Never report a notebook as fully ready solely
because a file exists. Provide the notebook path, environment and interpreter,
kernel, how to reconnect or restart the server, and any remaining human action;
identify the server started by this session so the human can stop it without
affecting unrelated sessions. Do not promise a working browser or service when
the environment does not allow one.
