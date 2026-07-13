# Bloat Pass

Over-engineering and complexity only. Correctness, security, and
performance belong in the risk register.

## Depth

- **Light — full baseline:** sweep dependency manifests, dead flags and
  configuration, and patterns already noticed during workflow tracing.
  Timeboxed: workflow risk outranks re-export hunting.
- **Deep — `bloat` focus:** the full hunt below, with global searches
  per signal.

## Tags

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Describe the shorter form.

## Hunt

Deps the stdlib or platform already ships, single-implementation
interfaces, factories with one product, wrappers that only delegate,
files exporting one thing, dead flags and config, hand-rolled stdlib,
speculative features.

These are search signals, not findings. A one-implementation interface,
delegating wrapper, or re-export file is not automatically waste.

## Proof standard

A cut-list item must establish:

1. the construct's current callers and runtime registration were
   searched;
2. no repository-local requirement justifies the flexibility;
3. removal preserves behaviour and public contracts;
4. the complexity creates material navigation, dependency, divergence,
   testing, or change-amplification cost;
5. unavailable cross-repository consumers are stated.

If removal safety depends on unresolved reflection, dynamic
registration, framework discovery, plugin loading, or external
consumers, do not place the item in the Cut list. Move the exact
question to Investigate and state what evidence would establish safe
removal. Record unavailable cross-repository consumers in Coverage.
Only high-confidence, behaviour-preserving cuts enter the Cut list.

## Output

One line per item, ranked biggest cut first:

```text
<tag> <what to cut> — <why removal is safe and materially useful>.
<replacement>. [path]
```

For `shrink:` describe the shorter form; do not construct a full patch.

End with, only when reasonably supported:

```text
estimated reduction: approximately <N> lines and <M> direct dependencies
```

Otherwise: `reduction not estimated without constructing a patch`.
Exact numbers only for a constructed, verified patch — false precision
lowers report credibility. Nothing to cut: `Lean already.`
