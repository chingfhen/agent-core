# Code Design — focused review scenarios

These are author-review scenarios, not recorded runtime test results. Apply the same request and code to a baseline agent and the skill-assisted agent when a behavioral trial is authorized; compare evidenced design consequences and unnecessary work, not answer length.

| Request / situation | Expected distinction |
| --- | --- |
| Design a trip-edit module used by two real adapters. | Activate; locate domain-rule and state ownership and expose a useful interface without inventing unrelated frameworks. |
| Refactor duplicated approval rules into one owner, with code-edit authorization. | Trace the real rule and callers, consolidate only shared semantics, preserve contracts and check affected behavior. |
| Review maintainability where a predicate secretly mutates state. | Cite the hidden caller obligation and propose an honest interface or structure; review stays read-only. |
| A long coherent function has local state and a clear contract. | Do not split it by line count; a grounded no-change result is valid. |
| Similar snippets encode independent policies. | Do not force a shared abstraction based on visual similarity. |
| Implement an ordinary endpoint, fix a typo, or rename a variable. | Do not activate on generic coding wording. |
| Rewrite a Markdown skill or save tasks. | Do not activate or impose code checks on prose. |
| A structural review reveals an authorization defect. | Report the evidenced issue; do not silently fix it or expand into an audit. |
| A requested refactor unexpectedly changes transaction or error behavior. | Treat the change as a regression or explicit contract decision, not cosmetic improvement. |
