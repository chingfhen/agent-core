# Next prompt — copy-ready continuation

Read only when the human explicitly asks for a Next prompt, a handoff prompt or a prompt/message for the next agent/session. Ordinary handoff still returns the root's short resume cue; do not generate this prompt automatically. A prompt-only request is read-only. If combined with sync or handoff, finish the authorized maintenance first and use the actual saved outcome; never start an extra sync or create a task just to produce a prompt.

Return one copy-ready prompt in a plain Markdown code block (or an equivalent native copyable text surface). Address the next agent directly. Keep a predictable order, omitting details that add no value:

    Continue [workspace/project and current objective].
    Read [exact task, docs or other saved locators and relevant guidance].
    Current state: [only essential progress, unresolved issue or verification gap].
    Next: [the next requested/permitted action and any material approval boundary].

Use exact usable locators and identify the repository/ref or local workspace where necessary. Point to the existing task rather than duplicating its plan, decisions and evidence. For work with no formal task, include the minimum self-contained context needed to continue accurately. Mention necessary skills or constraints only when relevant; distinguish accepted decisions, reported findings, unverified work and outstanding approvals. If maintenance or a required source was unavailable, disclose that in the prompt where it affects continuity. Do not claim a save that failed, imply the next agent has access it may not have, include secrets or transfer restricted context, or turn the prompt into new execution authority.

No separate handoff file, template system, mandatory headings beyond the simple order, or duplicate narrative. The human should be able to copy the prompt straight into a fresh session.
