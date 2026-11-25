# Agent Behaviors

Read after Agent Builder root for human-directed persistent behavior maintenance. Ordinary consultation/application and read-only review need no maintenance skill. Root owns scope, resource resolution, shared guidance, permissions, coordination and reporting. This module owns preserving and refining explicit human intent, not inferring preferences from experience.

## Intent and cue

Canonical cue: **remember this behavior**. Also recognize "update your future behavior", "from now on", "for future sessions", "I prefer that my agents...", "refine my behaviors" or "remove this behavior" when the request clearly conveys persistent intent. No magic words required. A clear request to persist a behavior authorizes its bounded maintenance subject to the root's resource initialization and local write gates. A request to show/review behaviors is read-only unless the human also asks for changes.

Distinguish a standing preference, explicit recurring constraint or permanent correction from a choice for today's task, a temporary exception, a complaint, an observed agent mistake or an inferred pattern. "Keep this response short" is local; "from now on, keep responses concise" is persistent. "Why didn't you reuse uv?" is a lead for operational learning, not a preference to transcribe; "for future Python work, reuse my purpose environments" conveys persistent intent. If unclear, honor the current request without persisting it; clarify only if the unresolved meaning materially affects a requested durable change. Do not demand a confirmation for clearly expressed durable intent. A lesson can be justified by evidence without human preference; use lessons.md for that distinct job.

## One human-reviewable resource

Default: `.work-context/behaviors.md` under the confirmed workspace context root. Agent scope by default; qualify narrower project, repository, activity or environment preferences explicitly. Resolve/reuse existing compatible resources and obtain approval for a new resource under root rules. Preserve existing paths and legacy guidance pending authorized migration. An inaccessible configured file is a gap, not permission to create a competing file.

Maintain one living Markdown document for the human to find, read, correct and refine directly. Use a clear title and natural semantic headings as needed (e.g. Communication, Planning and decision-making, Engineering); no compulsory categories, IDs, dates, scores, metadata or separate index. Preserve precise intent and important qualifiers, use plain actionable wording, and avoid request chronology or speculative interpretation. Existing independently owned guidance remains authoritative; link to its established rule instead of copying or absorbing it without permission. Record all admitted managed human preferences in the reviewable file, including those projected inline, so the human can review their complete managed set.

A possible document shape (illustrative, never seed placeholders):
    
    # Agent Behaviors
    ## Communication
    - [Explicit persistent preference, with exceptions if needed.]
    ## Engineering
    - When [applicable scope], [human-directed behavior].

## Maintain intent, not a log

1. Establish the human's intended behavior, persistent scope, exceptions and any existing rule it changes from the available conversation and relevant authoritative guidance. Consult only affected headings; do not scan unrelated work. Objective efficiency evidence is not a prerequisite for an explicit human preference.
2. Check for equivalent instructions, conflicts, owner and permissions. Integrate or consolidate semantically equivalent wording; do not generalize a local preference or turn a one-time exception into permanent policy. A clear durable human correction supersedes the affected earlier preference in its scope. Do not silently weaken, remove or materially reinterpret human intent; if durable human-owned instructions conflict, preserve the applicable stricter constraint pending clarification. A preference cannot override higher-priority policy or grant authority outside its verified scope.
3. Choose the smallest effective expression. Update the relevant heading in the living file rather than appending repeated requests. Keep rare or detailed activity-specific instructions behind conditional retrieval. Project facts and detailed procedures stay with docs; a reference can preserve the behavioral consequence without duplicating their contents. For genuinely essential universal preferences or before-action constraints, maintain concise consistent inline projections in AGENTS.md; the human-reviewable file is canonical for these managed preferences. Use matching headings or direct pointers when necessary; do not turn every preference into another AGENTS.md bullet.
4. Persist and verify the changed resource and affected inline projections/cues using root safeguards. Prefer coherent changes; verify supporting detail before replacing inline detail. Human edits to the file are explicit authority when ownership/intent is clear; reconcile affected projections during authorized maintenance without overwriting the human's change. If discrepancy could change an action materially, report it and preserve binding constraints until resolved. Do not rewrite external or unowned instructions. A review or explicit request that adds no meaning can be a no-op.

## Default AGENTS.md guidance fragment

Root owns the one managed block. Adapt this fragment to confirmed paths and existing instructions only during authorized setup or maintenance. Omit when no resource or qualifying inline instruction exists; never paste placeholders or create a second block.

    ## Agent Behaviors
    Behaviors: [confirmed behaviors.md locator]

    Before substantial work or a choice likely governed by a human preference
    (e.g. communication, planning, research, delegation or engineering), consult
    the relevant behavior headings; use a direct heading or targeted text search
    when the scope is known. Apply applicable persistent preferences; skip
    unrelated sections and redundant reads when context already suffices.
    Essential universal behaviors and pre-action constraints stay inline.
    If required detail is unavailable or contradictory, report the gap and
    respect applicable constraints before dependent action.
    Reading/application needs no Agent Builder invocation and authorizes no writes.
    Load Agent Builder for explicit behavior maintenance.

Add only essential inline behavior projections or useful conditional pointers as warranted. A direct link before a rare high-impact activity may be preferable to another universal read. Do not require reading the whole file at every startup or on trivial requests.

## Completion

Verify the exact changed file/heading, unchanged unrelated human intent, applicable scope, affected inline projections and locators. A future agent should recognize when to consult the preference and act consistently without loading this module. Report meaningful changes, exact destinations and material access/conflict/verification gaps; no duplicate report, compulsory benchmark or claim of harness compliance from saved text alone. The human should be able to inspect and refine their preferences independently.
