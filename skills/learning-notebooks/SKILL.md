---
name: learning-notebooks
description: >
  Create runnable, human-facing Jupyter notebooks that teach a mechanism
  hands-on — environment through the purpose-env workflow, teaching structure
  through learning + readability, launched for the human to run and inspect.
  Use for "make me a notebook to understand X", "hands-on walkthrough",
  "let me run it and see", or stewarding the notebooks library. Not for
  agent-executed scripts (that's project-scripts) or one-off code probes.
disable-model-invocation: false
---

# Learning Notebooks

## Job and boundary

Produce a notebook a human can **run, watch, and learn from** — every cell
either teaches or produces observable output, and the notebook is honest about
what each result proves and what it doesn't. The deliverable is understanding,
not automation.

Depends on three companion workflows, which are expected to be available:

- **manage-python-env** — owns all interpreter/package decisions. This skill
  never picks a Python or installs packages itself.
- **learning** — owns the teaching depth (Quick default) and the causal-bridge
  method. This skill applies it to notebook structure.
- **readability** — owns the writing quality of markdown cells.

Do not duplicate their rules; load them and follow them.

## Resolve the notebooks root

Use, in order: an explicit destination for this operation → a `Notebooks Root`
line in applicable `AGENTS.md` → `.work-context/notebooks/` beside the
configured context home. Report a missing/unwritable root; do not scatter
notebooks into random repo dirs.

Layout mirrors the KB convention:

```text
<notebooks>/
  INDEX.md                       # purpose, layout convention, run instructions, contents table
  YYYY-MM/
    <semantic>/                  # project/domain bucket (smart-search, infra, propensity, ...)
      <topic>/
        <name>.ipynb
        <requirements or notes>  # only if the env can't be assumed
```

Creation month and a shallow literal semantic folder; reuse names across
months. Keep `INDEX.md` current — one row per notebook with kernel/purpose.

## Environment (via manage-python-env)

1. Load `manage-python-env`. Reuse a compatible purpose env before creating;
   add the notebook's deps there (`uv add`), never ad-hoc `uv run --with`.
2. Ensure `ipykernel` is in that env, then register once:
   `python -m ipykernel install --user --name <env-name> --display-name "Python (<env-name>)"`.
3. Set the notebook's `kernelspec.metadata` to that registered name so the
   human isn't asked to pick.

## Authoring (via learning + readability)

Load both skills. Apply, at notebook scale:

- Open with a **Learning · mode** line, what running this proves, and the
  one-sentence mental model. Keep the marker inside the first markdown cell.
- One mental-model section early: smallest diagram/flow that makes the causal
  chain visible (ASCII or a markdown table, not decoration).
- Interleave: markdown explains → code produces observable output → markdown
  interprets. Every code cell says **expected output** in the markdown above it.
- Include a **"what this proves / what it doesn't"** section — the honesty that
  makes these notebooks trustworthy. Failed/blocked paths are findings, not
  hidden edge cases.
- Manual steps the code can't do (portal clicks, UI checks) get their own
  section with exact click paths and what each outcome means.
- Never print secrets; load `.env`-style files and assert presence instead.
- Markdown cells carry verified findings with their date — "verified
  2026-11-06" beats timeless claims that rot.

## Launch for the human

- Preferred: the workspace launcher if one exists (e.g. a
  `start-jupyterlab.cmd`-style script rooted at the notebooks dir).
- Fallback: run JupyterLab from a purpose env with jupyterlab installed:
  `uv run --project <env> --locked jupyter lab --ServerApp.root_dir=<notebooks>`
  as a background process; give the human the `?token=` URL.
- Environment quirk worth checking: `.cmd` launchers may not survive a
  bash-executed agent shell — invoke the underlying command directly.

## Verification and wrap-up

- If the human runs it live: read their outputs, interpret honestly, and
  update the notebook's findings cells to reflect what actually happened.
- The notebook is the durable artifact; consequential findings still route
  to their owners (KB records, tasks, docs) through the relevant skills —
  a notebook is not a substitute for persistence.
- Known-broken upstream behavior stays described as such; do not write the
  notebook as if the platform were healthier than evidence shows.
