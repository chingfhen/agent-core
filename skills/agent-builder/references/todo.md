# Todo — a human-readable action list

Read only when the human asks for Todo (e.g. "update my todo", "sync todo", "show my todo"). Apply root resource resolution, permissions and maintenance mode. Showing an existing list is read-only; updating is scoped to the list. Never load or update Todo as an automatic part of general sync, tasks, checkpoints, handoff, migration or setup.

## Keep one predictable list

Reuse the confirmed existing todo file. For first use, propose `todo.md` in the confirmed project context alongside tasks/docs, or in the agent context root for genuinely workspace-wide actions. An exact approved request counts for initialization; otherwise obtain the root's required approval. Keep the location stable; preserve existing filenames and backends. Do not create a new project, registry, dashboard or task merely to house an item. If scope or destination is materially ambiguous, ask; report inaccessible destinations rather than substituting.

Use this exact heading structure and ordinary Markdown bullets:

    # Todo

    ## Human
    - Test the login flow on your phone.

    ## Agent
    - Fix the login error after the human approves the change.

    ## Waiting
    - Hosting access — waiting for the administrator to approve it.

Keep all three sections in this order; use "None." for an empty section. Human means something the human can act on, Agent means work assigned to the agent (include any required approval in plain language), Waiting means an external dependency or other condition prevents progress. Put each action in its most useful section once, highest attention first. Do not duplicate the human's clearing action as a separate waiting item unless distinct work is actually blocked. Keep the first screen useful; no fixed item limit, dates, statuses, scores or completion history required.

## Update lightly

Use the existing list, current conversation and already available task/index context; consult a specific source only when needed to avoid a misleading item. Add, amend or remove items based on confirmed changes, including human-reported completion. Preserve still-open unrelated items; don't infer completion from silence. Small standalone actions can live here without task files. For substantial work link the actual task when available; task files and actual evidence own detailed state, plans and permissions. If sources conflict or cannot be checked, flag the uncertainty rather than claim completion. A todo never grants execution permission. No broad backlog audit, routine task changes, automatic refresh, separate research or new workflow. If task state needs changing, respect the separate tasks gate.

## Write for the human

The reader should know what deserves attention within ten seconds without reading a task or learning technical vocabulary. Start each actionable bullet with a concrete verb; say what to do and what outcome matters, using familiar words, active voice and short sentences. Name an actual product, file or system if needed to identify the action. Replace abstract phrases ("reconcile migration parity") with the action ("check that the new skill can still do what the old skills did"). Include why only if it changes what the human needs to do. Keep implementation detail, acronyms that are not needed, reasoning and acceptance evidence in the linked task. Preserve necessary accuracy, approval and blocker information; don't oversimplify into an unclear or unsafe instruction.

This is the practical audience-design and cognitive-load rule: put the reader's action first, avoid assuming they know the agent's background, and prefer everyday language. See [plain-language guidelines](https://www.plainlanguage.gov/guidelines/) for the underlying writing approach; no research or readability scoring during an update.

Write only meaningful changes, check the saved list and directly affected links, return its location and any real limitation. No extra report or mandatory summary.
