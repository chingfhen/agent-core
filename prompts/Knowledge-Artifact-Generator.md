# Knowledge Artifact Generator

Create a clear, accurate Markdown knowledge artifact about:

**[TOPIC]**

Use the following material when provided:

**[SOURCE MATERIAL, CONVERSATION, CODE, ERROR, DATA, DOCUMENTS, OR LINKS]**

The artifact may cover a technical, scientific, professional, analytical, or general knowledge topic.

## Objective

Help the reader build an accurate and durable mental model of the topic.

Choose the clearest structure, depth, and format for the specific topic. Do not mechanically follow a fixed template.

Use the shortest form that establishes an accurate and durable mental model without omitting essential context.

## Internal Preparation

Before writing, determine internally:

* the central idea the reader must understand,
* the most likely misunderstanding,
* any prerequisite that must be explained for the artifact to stand alone,
* the important causes, mechanisms, relationships, boundaries, assumptions, evidence, or decision rules,
* what can safely be omitted,
* and which format will make the topic easiest to reconstruct later.

Perform this analysis internally. Do not expose the planning process, information classification, or quality check in the artifact.

Choose a structure appropriate to the topic. For example:

* a concept may need explanation and comparison,
* an architecture may need a flow diagram,
* an error may need symptom → cause → diagnosis → resolution,
* a design decision may need options → trade-offs → decision rule,
* a process may need stages or a lifecycle,
* a scientific topic may need claim → mechanism → evidence → limitations,
* and a historical or general topic may require a different structure.

Do not include a section or format merely because it appears in an example.

## Accuracy and Sources

Treat provided material as context, not automatically as ground truth.

When tools are available, verify material claims that are uncertain, time-sensitive, contested, or dependent on version, jurisdiction, provider, organization, or environment. Never claim that verification occurred unless a source was actually checked.

Prefer the most authoritative source for the claim, such as:

* official documentation, standards, and specifications for technologies,
* legislation, regulators, and professional guidance for legal or regulated topics,
* systematic reviews, professional guidelines, and original research for scientific claims,
* and primary records or reputable scholarship for historical claims.

Do not invent missing facts.

Clearly qualify:

* uncertainty,
* assumptions,
* interpretations,
* recommendations,
* conflicting evidence,
* and unresolved questions.

When credible interpretations differ, represent the disagreement briefly and fairly rather than selecting one without justification.

When source material describes a specific project, organization, provider, environment, or implementation, distinguish clearly between:

* the general principle,
* the local implementation or decision,
* and any recommendation or interpretation.

Do not present a local choice as a universal rule.

## Scope Control

Internally classify available information as:

```text
Must understand
Useful to recognize
Reference only
Optional detail
```

Write mainly from **Must understand**.

Include **Useful to recognize** only when it strengthens the mental model.

Usually omit:

* exhaustive lists,
* lookup-only material,
* obscure exceptions,
* historical trivia,
* long command references,
* repeated explanations,
* and implementation details that do not improve understanding.

Optimize for understanding, not completeness.

## Teaching Principles

Use correct terminology, but explain important terms plainly when first introduced.

Prefer explanations that allow the reader to reconstruct the answer from first principles. Do not rely only on memorized rules when the underlying reason can be explained concisely.

Prefer causal explanations over disconnected facts. Where relevant, make clear:

* what causes what,
* how the mechanism works,
* what each concept, actor, component, variable, or stage is responsible for,
* what initiates an action,
* what receives or responds,
* what depends on what,
* and where the boundaries lie.

When a distinction matters, explain:

* what something does,
* what it does not do,
* what it owns,
* and how it differs from the concept most likely to be confused with it.

Do not force systems-style analysis onto topics where it does not help.

## Format and Style

Choose only the formats that materially improve understanding, such as:

* concise prose,
* bullets,
* comparison tables,
* ASCII diagrams,
* timelines,
* equations,
* examples,
* decision rules,
* or troubleshooting flows.

Examples, diagrams, glossaries, prerequisites, comparisons, related concepts, retrieval questions, and next-topic recommendations are optional.

Include them only when they add real teaching value.

The artifact should be:

* self-contained,
* easy to scan,
* concise without becoming cryptic,
* precise,
* free of unnecessary repetition,
* and useful when reopened months later.

Avoid filler, decorative structure, vague analogies, marketing language, and walls of text.

Analogies may support an explanation, but they must not replace the actual model.

## Active-Learning Readiness

The artifact may later be used to generate retrieval questions, comparisons, explanations, and application exercises.

Therefore, state important ideas explicitly, preserve enough context for correct interpretation, and make important relationships and distinctions clear.

Do not turn the artifact into a worksheet unless questions or exercises genuinely improve the artifact itself.

## Final Requirement

Before returning, remove unnecessary detail and confirm that the artifact is accurate, self-contained, and organized around the clearest mental model for the topic.

Return only the completed Markdown artifact.
