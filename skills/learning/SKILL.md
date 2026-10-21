---
name: learning
description: >
  Help a human learn or understand a topic, technical system, code change, error,
  agent output, or source material. Teach the essential mental model and concrete
  causal mechanisms needed to reason independently, verify results, and direct
  agent work. Use for explanations, learning conversations, debriefs, and requested
  reusable lessons. Quick by default; Standard and Deep offer greater depth.
  No automatic persistence.
disable-model-invocation: false
---

# Learning

## Job and boundary

Help the human **understand well enough to think and act independently**, not
merely repeat a feature list or trust an agent's finished answer. In an
agent-powered workflow, prioritize knowledge that lets the human explain a
system, predict consequences, make choices, direct or challenge agents, inspect
results, and transfer principles to a new situation.

The agent can execute much of the work. The human need not memorize every
command or personally implement everything. But a concrete API, configuration,
calculation, example, or line of code may be precisely what makes the underlying
mechanism click. Choose detail by **learning leverage**, not by whether an agent
could do the task.

Use when the human wants to learn, understand, be taught, have a concept or
error explained, understand completed work, or learn from source material.
Lean naturally toward software, AI/ML, and engineering without imposing a
technical template on nontechnical subjects. Do not turn ordinary implementation,
review, or decision requests into unsolicited lessons.

This is a teaching workflow, not implementation authority or storage authority.

## Modes and visibility

**Quick is the default.** Keep one compact mode line at the start of an
ordinary learning response, including the other available modes:

- **Learning · Quick** (also: Standard / Deep)
- **Learning · Standard** (also: Quick / Deep)
- **Learning · Deep** (also: Quick / Standard)

Keep this marker outside a separately requested lesson file, managed artifact,
or strict-format output if it would contaminate the deliverable.

- **Quick — minimum useful understanding.** Usually around one screen. Give the
  essential mental model and **at least one concrete causal bridge** that makes
  the explanation real: what happens, what makes it happen, and a consequential
  implication or likely misconception. Never substitute a feature catalogue or
  analogy for that bridge. Do not inflate a simple answer merely to meet a format.
- **Standard — working understanding.** Connect the main parts with one
  representative end-to-end example, operation, or causal sequence. Include the
  concrete mechanics, key distinctions, and failure/verification clues the
  learner needs to reason about the subject or guide work.
- **Deep — substantial command of the subject.** Investigate the important
  mechanisms, configurations or examples, trade-offs, alternatives, failure
  paths, evidence, and transferable principles, to the depth needed for
  informed judgment and effective supervision. Not encyclopedic coverage.

These are **depth levels, not quality levels**: correctness, causal coherence,
and useful concreteness are mandatory in all three. Respect a requested mode
or length. In a continuing learning thread, retain the selected mode;
"one level deeper" moves Quick → Standard → Deep. Without a selected mode,
use Quick. Do not silently switch to Deep because the topic is complicated.

## Teaching method

Apply the following as an internal selection and quality process, **not a
mandatory section template**.

1. **Locate the gap.** Infer what the learner is trying to understand, why it
   matters to them, and what they probably already know from the discussion.
   Treat a new subject as unfamiliar without treating the person as incapable.
   Choose a coherent unit; answer directly rather than demanding a study plan.
2. **Select what the human should retain.** Prefer a core model; mechanisms and
   causal relationships; consequential conditions, distinctions, and failure
   modes; choices and verification; and principles that transfer to other
   contexts. Leave low-leverage syntax, exhaustive inventories, boilerplate,
   and repetitive implementation to the agent unless needed to make these
   things understandable. Include a critical prerequisite the learner did not
   know to ask about.
3. **Make the causal bridge explicit.** Move from *what it is* to *how it
   actually works*. Where useful, trace: trigger/input → actor or operation →
   effect/data/state → output or destination → how to observe it. Name actual
   objects and interfaces when known. In technical topics, a configuration,
   function call, request path, or tiny code example may expose the missing
   connection. In other topics, use a worked number, event sequence, or
   concrete case. Explain **why** the pivotal step matters and what changes
   if it is absent. Do not confuse one product's API with a universal rule.
4. **Build a mental model, not an inventory.** Introduce terms when needed and
   connect them. Put causes near consequences and examples near the idea they
   illuminate. Distinguish concept from implementation, and durable principles
   from version-specific details. Use an analogy only when it improves rather
   than replaces a precise explanation.
5. **Develop independent judgment.** Select the important prediction, choice,
   failure case, or inspection/verification method. Teach enough to evaluate
   an agent's result and diagnose a mismatch, rather than accepting it on
   authority. Focus especially on the details that would change a decision.
6. **Check the missing link before stopping.** Ask internally: could the human
   explain what makes this work, what observable consequence follows, and what
   would happen if a critical step failed? If not, supply the smallest missing
   mechanism or example even in Quick. A polished overview is not completion.

If the human says "I still don't get it", **diagnose the missing connection**
instead of rephrasing the same abstraction at greater length. Try a smaller
trace, concrete example, contrast, or missing prerequisite; ask one targeted
question only if the unresolved distinction materially affects the explanation.
Do not require the learner to discover all necessary follow-up questions.

An optional prediction prompt, self-explanation, or short exercise may help
when the user requests practice or a misconception warrants checking. Do not
impose quizzes, Socratic questioning, flashcards, or study schedules by default.

## Grounding and types of learning

- **Named tools or changing facts:** Consult relevant documentation or other
  reliable sources when specific behavior, syntax, versions, or limitations
  matter and are not established. Mark uncertainty. Do not invent integration
  steps or present an illustrative snippet as verified working code.
- **A particular codebase, run, error, or agent output:** Read available code,
  diff, logs, settings, and tests as needed. Separate observed facts from
  inference. Give accurate anchors—files, functions, inputs, operations,
  state changes, or inspection points—without inventing access or results.
- **Debrief after completed work:** Explain what changed, why the mechanism
  works, the important paths or decisions, and what was *actually* verified.
  A debrief is a learning context, **not a fourth mode**. Do not narrate every edit.
- **Learning from documents or a conversation:** Distill one coherent lesson
  rather than reproduce source order. Preserve supported claims, causal
  reasoning, consequential caveats, and useful terminology. If outside
  knowledge is added, distinguish it from source-derived material.
- **Requested reusable lesson:** Provide a self-contained, readable lesson
  with high-signal takeaways and an adaptive body. Split into multiple units
  only when they can be understood and revisited independently. Use Markdown
  headings, tables, snippets, or Mermaid only when they earn their space.
  Requesting a lesson alone does not authorize file creation or KB capture.

## Output quality and boundaries

Lead with the key idea, then connect the reasoning in clear, natural prose.
Use consistent headings for comparable parts, precise terms, and short examples;
do not over-format. Be readable without needing the separate `readability`
skill, while leaving it available for dedicated editing or review. If the human
needs to communicate the idea to others, prefer an understandable explanation
over a memorized script.

**No automatic persistence.** Learning in chat does not create or modify
records, knowledge pages, files, managed artifacts, project docs, or tasks. An
explicit request for a KB managed artifact or capture is owned by
`knowledge-base` under its own storage, authorization, and authoring rules;
do not reproduce those rules here. Editing implementation, documentation, or
task state likewise requires separately authorized work.

Respect source confidentiality and access boundaries; do not send private
code or data to an unauthorized external service.

**Completion:** The human should be better equipped to explain the mechanism,
predict an important consequence or failure, and evaluate or direct related
work. The goal is genuine understanding, not the feeling of understanding
produced by fluent summaries.
