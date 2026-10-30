# Docs routing and first use

Read when docs configuration is missing or its routing must change. This skill
owns `<!-- BEGIN PROJECT DOCS -->` through `<!-- END PROJECT DOCS -->` in verified
applicable AGENTS.md, plus documentation/guidance explicitly assigned by the main
skill's ownership rules. General guidance ownership never overrides another
skill's marked section. Confirm workspace/project scope; cwd or a Git root alone
does not establish it.

1. Use established configuration or the operation-specific human-selected
   destination. Do not silently save a temporary selection as the new root.
2. During authorized docs maintenance, inspect/reuse a clearly identifiable
   existing conventional docs surface and register missing routing without
   redundant adoption approval. Confirm identity and ownership from contents and
   guidance, not folder existence. Read-only consultation authorizes no writes.
3. If neither configuration nor a suitable resource exists, propose
   `.work-context/projects/<project>/docs/` under the confirmed workspace. Obtain
   one approval for initialization and registration, then initialize only docs
   resources. Existing explicitly owned layouts such as `docs/` remain valid.
4. Ask about conflicting destinations or ownership. Report inaccessible configured
   resources instead of substituting another location. Preserve narrower write gates.

## Section

Creation-time example; use confirmed locations and existing useful entry points:

```markdown
<!-- BEGIN PROJECT DOCS -->
## Project Docs
Consult relevant entry points below for project decisions.
Load project-docs before maintaining documentation or owned guidance.

### Forecasting
Docs: .work-context/projects/forecasting/docs/
- [Architecture](.work-context/projects/forecasting/docs/architecture.md)
  — repository responsibilities and system boundaries.
<!-- END PROJECT DOCS -->
```

Link only a few canonical entry points, each with a consultation cue. A newly
initialized empty docs root need not have links or fabricated documents. Reading
project rules is distinct from loading the skill that maintains them. Put deeper
navigation and procedures in docs, not in this section.

## Targeted maintenance

New relative paths resolve from the declaring AGENTS.md directory, not cwd.
Legacy workspace-relative paths retain their recorded base until approved migration.
Markers/headings/labels and the minimal initial cue are defaults; routine changes
maintain confirmed paths and directly affected entry points. Preserve customized
behavior, outside text, other owners' blocks, and the section's position.

Reread before mutation; refuse duplicate/incomplete/nested/ambiguous markers and
unsafe paths. Reconcile concurrent changes safely, read back, and verify the owned
diff and links. Report partial routing failure while preserving valid primary docs
work. Migration of an existing central block needs identified scope and approval,
preserves custom text, and must leave no competing destination authority.
