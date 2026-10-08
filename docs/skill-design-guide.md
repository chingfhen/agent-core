---
title: Skill Design Guide
description: Canonical criteria for designing, invoking, consolidating, publishing, and retiring Agent Core skills.
updated: 2026-10-08
---

# Skill Design Guide

## The objective

A skill should make a **distinctive job repeatable** without changing unrelated behavior.

It must be discoverable by two users:
- **Human:** Can I remember its name and know when to call it?
- **Agent:** Does its description identify the circumstances when it should activate?

A good skill is easy to reach, scoped enough to trust, and cheap to maintain. More skills are not automatically better.

## Before creating a skill

1. **Search the catalogue and existing skills** for the same outcome, not just similar names.
2. **Name the failure or recurring task** that the new skill would address.
3. **Compare alternatives:** update an existing skill, add a mode, put a rule in a project-owned document, keep a reference page, or create a new skill.
4. Create a skill only if it has an independently useful invocation trigger or must enforce a separate workflow boundary. Otherwise consolidate.
5. Confirm the target tool/harness and dependencies can actually support the proposed behavior.

The burden of proof is on a *new* skill, not on keeping the old skill untouched.

## Naming and invocation

Choose a short, literal, memorable name that suggests an action or outcome: `explain-tech`, `project-tasks`, `human-unblock`.

Avoid internal implementation terminology that the human would never naturally reach for. A name is a user interface, not just a directory.

The YAML `description` should say **when to use it** and distinguish it from nearest neighbors. Avoid long synonym lists or claims that it governs every task.

Select invocation deliberately:
- **Agent-discoverable:** The agent must recognize a relevant situation proactively. Keep the trigger narrow enough to avoid accidental activation.
- **Explicit invocation:** The human wants a voluntary mode or specialized utility. Where the harness supports it, disable autonomous invocation.
- **Reference material:** No invocation needed; place it under `docs/` or a skill-local `references/` file, not in a redundant skill.

Do not treat invocation flags as universal across harnesses without checking their behavior.

## Responsibility boundaries

Use **one skill per job**. Similar *steps* do not imply duplicate skills when outcomes differ.

Keep these boundaries clear:
- `planning`: select and justify the direction.
- `engineering`: implement approved work.
- `project-tasks`: make unfinished work portable.
- `project-docs`: maintain settled project truth.
- `knowledge-base`: manage evidence and knowledge.
- `learning-markdown`: author lessons; not automatic KB persistence.
- `approval-gate`: support a consequential approval.
- `human-unblock`: clear a human-owned obstacle during execution.

A new mode within one skill is preferable to a second skill when the **goal is the same** and only depth, timing, or presentation changes. Name available modes clearly and use a sensible default.

Avoid binding general behavior to one environment unless the skill is intentionally environment-specific (e.g., Windows `uv`). State exclusions where cross-environment use could be harmful.

## Writing the skill

Keep the entry `SKILL.md` short enough to scan. Put the working contract first:
1. Trigger and objective.
2. Critical boundaries and non-goals.
3. Action procedure or decision rules.
4. Observable completion and honest reporting.

For longer workflows, keep essential steps in `SKILL.md` and move rarely used reference detail into named companion files, linked with **when to read** cues. Don't hide essential gates in a reference appendix.

Prefer concrete behavioral instructions to slogans. Each rule should change the result under a plausible condition. Remove:
- repetitions and generic exhortations;
- superseded procedures or stale tool assumptions;
- rigid templates that do not improve the output;
- new abstractions added only for imagined future needs.

Require verifiable completion where it matters, but do not turn ordinary work into ceremony.

## Consolidation and retirement

When overlap appears:
1. Compare **user-facing outcome, invocation trigger, authority, outputs, and side effects**.
2. Choose one canonical owner; move any genuinely useful unique behavior into it.
3. Inspect direct dependencies and update only affected references.
4. Archive superseded skill sources with recoverable history; remove active copies.
5. Reconcile the catalogue and installation manifest.
6. Verify there are no dangling active references or broken declared skill paths.

A skill can be **retained but uninstalled** when it is useful rarely. Don't delete useful specialized capabilities simply to reach a numeric target.

## Catalogue versus installation

- `docs/skills-catalog.md` is the **discovery map**: purpose, trigger, scope, and status of retained skills.
- `skills/<name>/SKILL.md` is the **behavior source**.
- `personal-skills.toml` is the **authoritative personal installation list**. Only its declared skills are published by `agent-core sync`; merely placing a folder in `skills/` does not install it.
- `archive/skills/` holds historical, superseded content, not active invocation targets.

Use these statuses in the catalogue: **Active (installed)**, **Dormant (retained, not installed)**, **Archived (historical)**.

The manifest reflects skills the human actively uses **or deliberately wants available to their agents**. Occasional skills may remain dormant. Do not infer manifest membership automatically.

Removing a manifest entry does **not** automatically uninstall an already published copy: current sync is non-destructive for removed entries. Do not promise that a removed skill disappears locally without explicit retirement or clean-up.

## Practical quality test

Before shipping or revising a skill, ask:
- Would the human know **when to reach for it**, from its name alone?
- Would an agent activate it for the right task, not unrelated ones?
- Would two retained skills disagree about who owns the same action?
- Does its completion criterion make success distinguishable from confidence?
- Could this be a small mode, a reference, or an edit to an existing skill?
- Will a future maintenance change require editing only **one authoritative source**?

If the answers are poor, revise or consolidate before expanding the inventory.
