# Docs routing and first use

Read when docs configuration is missing, routing must change, or a discovery-cue
refresh is authorized. This skill owns `<!-- BEGIN PROJECT DOCS -->` through
`<!-- END PROJECT DOCS -->` in verified
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
For project meaning, decisions, constraints, or established procedures, consult the
relevant entry points below. For an imperfect reference or missing entry, search
filenames/content in the confirmed docs root using likely subjects and known aliases.
Read the actual document; navigation is not authority. Verify consequential claims
against appropriate evidence (including code/runtime for implementation claims).
Reading or using docs does not require project-docs or authorize maintenance.
Ask about materially ambiguous project identity; report inaccessible resources or
material search limits rather than substituting. Load project-docs when docs
maintenance is requested or delegated, including an authorized handoff/closeout;
respect the human's chosen timing.

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
Keep these reader cues usable without the maintenance skill. Use recognizable
subject names and existing aliases in entry-point descriptions where helpful;
verify affected links during maintenance, without cataloguing every document here.

## Targeted maintenance

New relative paths resolve from the declaring AGENTS.md directory, not cwd.
Legacy workspace-relative paths retain their recorded base until approved migration.
Markers/headings/labels and the minimal initial cue are defaults; routine changes
maintain confirmed paths and directly affected entry points. Preserve customized
behavior, outside text, other owners' blocks, and the section's position.

During a human-authorized docs-maintenance pass, minimally add or refresh the owned
discovery cue when guidance changes are within authorized scope and the cue is absent
or outdated. A separately requested cue-only refresh is also valid. Replace a
conflicting old default, not genuinely customized human behavior or stricter gates;
ask about conflicting custom instructions. Skip equivalent guidance and unrelated
audits. Reading, source edits, and publication do not themselves authorize a refresh.

Reread before mutation; refuse duplicate/incomplete/nested/ambiguous markers and
unsafe paths. Reconcile concurrent changes safely, read back, and verify the owned
diff and links. Report partial routing failure while preserving valid primary docs
work. Migration of an existing central block needs identified scope and approval,
preserves custom text, and must leave no competing destination authority.
