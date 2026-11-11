---
name: learning-notebook
description: >
  Manage a human's guided Jupyter learning notebooks end to end. Use when asked
  to create, find, open, continue, extend, or organize a learning notebook or
  hands-on notebook lesson. Manage discovery, teaching, the Python environment,
  kernel, safe verification, and launch; not production analysis or code probes.
disable-model-invocation: false
---

# Learning Notebook

## Job and boundaries

Help the human learn a subject through a notebook they can read, run, change,
and revisit. The agent handles the journey: find or create the lesson, prepare
the environment, verify its kernel, and open the actual notebook when the host
permits. Do not make the human manage Jupyter or select an environment.

Use for requested learning notebooks and library stewardship, including “open
my X notebook” and “add a chapter on Y.” Do not turn ordinary explanations or
production analysis into notebooks. A notebook request authorizes the requested
local lesson or edit, affected index maintenance, necessary personal environment
dependencies, safe verification, and local Jupyter startup. Respect narrower
requests and local gates. It does not authorize changing team environments or
project source, KB/docs/task capture, publishing, destructive cleanup, private
data exposure, or unapproved paid or external effects.

Use sensible defaults without a questionnaire. If an unexpected condition creates
material uncertainty, a conflict, or a safety, access, cost, privacy, or ownership
decision that cannot be resolved within scope, explain it, propose a safe next
step and ask for approval before crossing the boundary. Diagnose ordinary errors
and make routine reversible choices without asking. Never conceal partial results.

## Resolve the collection and discover lessons

Use an explicit destination for this operation, then the `Learning Notebooks Root`
in applicable `AGENTS.md`. A one-time destination does not change saved
routing. Confirm the workspace scope from the human or guidance; neither cwd nor
a Git root alone establishes it. New relative paths resolve from the directory
containing the declaring `AGENTS.md`; preserve recorded legacy path bases.

When routing is missing during authorized notebook management, inspect and reuse
an unambiguous compatible existing collection if its identity and ownership are
established, and register its confirmed route without redundant adoption approval.
A folder name alone is not proof. If no suitable collection exists, propose
`<confirmed-workspace>/.work-context/learning-notebooks/` and obtain one approval
to initialize and register it. Report inaccessible roots or conflicting ownership
and ask; do not silently substitute or create a competing collection. Read-only
discovery does not authorize initialization or routing edits.

The skill owns only its marked section in verified applicable `AGENTS.md`.
During authorized management, maintain the confirmed route and discovery cue
only when that guidance is within the authorized write scope and local gates permit;
preserve human wording, other sections, stricter gates, and block position. Reread
before mutation; refuse duplicate, incomplete, nested, or ambiguous markers and
unsafe paths, reconcile concurrent edits, and verify the scoped result. Do not
modify global guidance without authorization. Example for an `AGENTS.md` at the
workspace root; substitute the actual confirmed path:

```markdown
<!-- BEGIN LEARNING NOTEBOOKS -->
## Learning Notebooks

Learning Notebooks Root: .work-context/learning-notebooks/

For existing learning notebooks, consult the root's INDEX.md or search the
collection by subject and known aliases. Ask if materially different matches
remain; report inaccessible paths or material search limits. Reading does not
authorize edits. Load learning-notebook to create, open, extend, or manage a
learning notebook; use manage-python-env for Python execution and environments.
<!-- END LEARNING NOTEBOOKS -->
```

To find a notebook, consult the index, then search relevant filenames and content
if the reference is imperfect or the index misses. An index miss does not prove
absence. Ask when materially different candidates remain; report missing access
or incomplete search rather than inventing a match. For an open request, open
the existing notebook without creating or editing a lesson. For an extension,
read the existing lesson and preserve the human's content and unrelated edits;
add the requested material in place. If safe concurrent editing cannot be
established, stop and ask before overwriting changes.

## Organize the collection

Keep an existing compatible organization. For a new collection use:

```text
<root>/
  INDEX.md
  python/2026-11/2026-11-10__python-generators.ipynb
  observability/2026-11/2026-11-10__tracing-fundamentals.ipynb
```

Reuse a short descriptive subject group, then creation month and date; dates
describe creation, not the events studied. Keep paths stable. Never overwrite or
rename an existing notebook to resolve a collision; choose a distinct slug.
Keep one lightweight index with links, titles, creation dates and descriptions,
grouped by subject and newest first within each group. Record the designated Python
purpose-project name there for future sessions, not a machine-specific absolute path;
its location comes from the configured Python Environment Root. Retain useful aliases
for discovery and update only affected entries. Check links after writes. If index or
routing maintenance fails, retain valid notebook work and report the partial
result. Do not automatically archive, delete, migrate, or create a second index.

## Teach through the notebook

Load `learning` to select the mental model, useful depth, causal explanation and
judgment; use `improve-readability` when dedicated writing review would help. Infer a
small coherent lesson from a clear request instead of demanding a syllabus.
Ground changing product behavior in reliable current sources and relevant project
evidence; cite useful sources in or near the lesson. Distinguish observed results
from examples and uncertainty.

Produce valid `.ipynb` content with explanations next to runnable cells. State
the learning goal, prerequisites, run order, and relevant external effects.
Show what to observe, what it means and, when useful, what it does not prove;
include a small change or contrast when it improves understanding. Use diagrams,
exercises, manual UI steps, and dated findings only when useful, not as a fixed
template. Make reruns and stateful cells clear. Prefer small synthetic or
explicitly authorized data; never put secrets or sensitive data in source,
saved outputs, indexes or reports. Do not install packages from notebook cells.

Prefer a real integration when essential and access and authorization permit.
If a real service is unavailable, explain the meaningful trade-off and ask before
substituting a materially different local demonstration. Never present a mock as
verified external behavior. When the human shares live results, help interpret
them; update the notebook when requested, distinguishing findings from expectations.

## Environment, verification, and opening

1. Load `manage-python-env` before any Python execution, interpreter probe, or
   dependency operation. Follow its root resolution, approval, compatibility,
   coordination, package-policy and execution rules. Use one designated personal
   purpose project across learning notebooks: use the purpose recorded in the
   collection index if compatible; otherwise reuse a suitable existing compatible
   purpose project when available, or use the name `learning-notebooks` under the
   confirmed Python Environment Root. If the recorded purpose is unavailable or
   incompatible, propose a safe remedy and ask before changing the designation.
   Do not create one per lesson.
   Add only necessary dependencies, including Jupyter and kernel support as needed.
   If a dependency or Python change would break other lessons, or the shared
   environment cannot safely be changed, propose a safe option and ask before an
   incompatible change or additional environment. Never modify a team `.venv` or
   team dependencies without the separate authorization that skill requires.
2. Verify the selected interpreter through `manage-python-env`. Start or reuse a
   suitable Jupyter server with localhost binding and authentication intact. Check
   any existing launcher/server for root, authentication and environment suitability;
   do not assume its kernel matches the server. Select a kernel and verify its actual
   `sys.executable` and prefix match the designated environment. If registration is
   necessary, prefer the owned distinct name `learning-notebooks`, display name
   `Python (Learning Notebooks)`; never overwrite an unrelated kernelspec. Set the
   notebook's kernelspec to the verified kernel where an edit is in scope; for an
   open-only request select it for the session without saving notebook changes. Stop
   and diagnose mismatch; do not fall back to system Python.
3. For new or modified lessons, validate notebook structure and run the safe main
   path from a fresh kernel in order when authorized. Check key observations; do not
   imply unexecuted cells ran. Avoid repeating external effects; obtain required
   approval before consequential or paid execution. Preserve useful safe output,
   remove sensitive or misleading generated output when safe, and avoid bulky output.
   Never discard a human's existing work merely to clean up. Explain any persistent
   resources actually created and their cleanup needs without deleting them. Give
   the human a fresh kernel when safe without repeating effects.
4. Open the actual notebook in the browser and leave the suitable server available
   when possible; reopen by starting or reusing a server on later requests. Verify
   reachability and kernel selection as far as the host permits. Do not claim a
   browser opened without observation. Keep authentication enabled and do not expose
   the server on a network to bypass restrictions. Treat token-bearing URLs as
   secrets: share only through an appropriate user-visible channel when needed.

If access, browser launch, packages, a kernel, or a service is blocked, preserve
valid work, explain what is verified and what is not, and propose the shortest safe
way forward. Report the notebook and environment paths, kernel, how to reconnect
or restart, any remaining human action, and how to stop a server started by this
session without affecting others. A file alone is not proof the journey works.
