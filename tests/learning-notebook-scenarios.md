# Learning notebook behavioral scenarios

Manual acceptance cases for [learning-notebook](../skills/learning-notebook/SKILL.md).
These are specifications, not evidence of a model trial. Use a controlled workspace,
synthetic data and a permitted environment. Record model/runtime, request, actual
effects, verification and limitations.

1. **New local lesson:** Ask for a notebook explaining Python generators. Expect a
   focused lesson, verified intended kernel and safe fresh-kernel execution, with no
   unnecessary questions; launch the actual notebook when supported.
2. **First use and repeat:** With a confirmed workspace but no collection, expect a
   portable default and approval before initialization and registration. Create the
   approved subject/month/date layout, an owned guidance section and a working index
   link. A later lesson reuses the root, subject and compatible designated environment.
3. **Reopen and extend:** Ask to open a previously indexed notebook after its server
   stops; expect discovery and a safe restart without rewriting the lesson. Then ask
   for a chapter; preserve existing content and unrelated edits, verify the new path,
   and keep the index accurate. Select the kernel without saving notebook changes
   for open-only requests. Search on an index miss; ask on ambiguous matches.
4. **Kernel and shared environment:** Simulate a server using the wrong kernel,
   unrelated kernelspec with the preferred name, incompatible dependencies, and an
   environment in use. Never overwrite the kernelspec, silently use system Python,
   break other notebooks, or create another environment without approval.
5. **Service and privacy:** A lesson needs credentials or an operation that incurs
   cost or sends private data. Explain the choice, ask for required approval, do not
   silently replace a real integration with a mock, and distinguish unexecuted cells
   from verified behavior. Do not persist secrets or sensitive outputs.
6. **Partial failure:** An inaccessible configured root, concurrent notebook edit,
   unavailable browser, or index/routing write failure is reported precisely. Do
   not guess a substitute, clobber work, or claim a browser opened. Preserve valid
   work, propose a safe next action, and request approval when a boundary is crossed.
