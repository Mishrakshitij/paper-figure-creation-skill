---
name: paper-visual-design
description: Plan, create, and improve scientifically faithful figures and experimental graphs for research papers. Use for architecture diagrams, method figures, conceptual illustrations, graphical abstracts, introduction teasers, benchmark or environment setup figures when the manuscript contains a substantive setup, ablations, performance plots, qualitative comparisons, and paper figure improvements. Combine optional image-generated illustrative assets with precise editable vector authoring and source-grounded quantitative charts; deliver and inspect publication-size PDF, SVG, and PNG.
---

# Paper visual design

Make the scientific explanation visible. Plan before drawing; use the paper's actual objects, transformations, and evidence. Preserve the user's standing instructions, existing figure identities, and local skill customizations.

## Route the task

Read the relevant manuscript, equations, methods, results, and available code. Extract facts before asking for missing information. For an existing figure, inspect its rendered pixels and editable source first.

| Reader's question | Workflow | Read |
| --- | --- | --- |
| What is the problem, what changes, and why care? | Teaser / graphical abstract | [teaser](references/teaser.md) |
| How does the computation work? | Method / architecture | [method](references/method.md) |
| What is the task or environment and how is success measured? | Benchmark / setup, conditional | [benchmark](references/benchmark.md) |
| How do methods, budgets, or variants compare? | Standalone graphs | [graphs](references/graphs.md); [ML graph recipes](references/graph-recipes.md) when relevant |
| Where do observed cases differ, and what can explain the difference? | Qualitative / technical comparison | [qualitative comparisons](references/qualitative.md) |
| How can illustrations and plots form one editable figure? | Hybrid assembly, used with any applicable route | [hybrid](references/hybrid.md) |
| Which figures belong in this paper? | Select applicable jobs; share notation and palette | [planning](references/planning.md) |

A figure suite is not automatically four figures. Do not invent an algorithm for a benchmark paper. Do not add a setup figure just because experiments use named datasets. Select setup only when a substantive setup is described in the manuscript or primary supplement; record its location and whether it is new, adapted, or existing relative to this paper. If evidence is unclear, leave it unselected and resolve the missing source.

For dense layouts and paper-wide polish, also use the preserved foundation guides: [publication polish](foundation/references/publication-polish.md), [layout and overflow](foundation/references/layout-and-overflow.md), [asset sourcing](foundation/references/asset-sourcing.md), and [geometry and inspection](foundation/references/geometry-and-inspection.md). These contain the existing manuscript-scaled typography, wrapping, legend-occlusion, named-port routing, and PDF inspection workflows.

Always read [planning](references/planning.md) for a new complex figure and [review and delivery](references/review-delivery.md) before finishing. Read only the selected workflow references, not the whole bundle.

## Standing design contract

1. **Understand the science first.** Identify the central message, inputs, outputs, components, transformations, relationships, and exact supporting sources. Resolve contradictions before drawing the affected mechanism. Never invent mechanisms, results, or claims. Continue unaffected work while recording missing facts.
2. **Design a visual explanation.** Show what enters, what changes, and why the proposal matters. Use recognizable scientific objects, component internals, and a small worked example when useful. Keep the example identity consistent across stages. Use short labels; put detailed explanation in captions.
3. **Explore composition before polish.** For a new complex figure, sketch three meaningfully different layouts. Choose the clearest reading order and focal operation. Plan branches, merges, and feedback before detailed object placement. A small correction to an existing figure does not require three new layouts.
4. **Combine generation with precision.** Use image generation when it improves composition or supplies a useful illustrative asset. Author authoritative labels, equations, arrows, architecture wiring, and quantitative plots with editable vector tools. Distinguish generated illustrations and constructed examples from experimental evidence. Record external asset sources and rights. If generation is unavailable, use an honest vector route; do not claim it was used.
5. **Apply a coherent publication style.** Keep typography, semantic colors, spacing, alignment, and panel labels consistent. Use visual detail to explain the mechanism. Preserve meaning without color and readability at the actual manuscript dimensions. Avoid decorative detail that competes with the focal operation.
6. **Preserve scientific accuracy.** Trace connections to the method and marks to data. Distinguish training, calibration, inference, and evaluation; show learned/frozen states and information access correctly. Never fabricate uncertainty, significance, missing measurements, or favorable baseline selection.
7. **Review and iterate.** Inspect rendered pixels at manuscript size and enlarged. Check meaning, arrow routing, overlaps, clipping, type size, and consistency. Use an independent scientific/comprehension reviewer when available. Repair concrete defects and inspect the revised export before declaring completion.
8. **Deliver editable, reproducible artifacts.** Supply PDF, editable SVG, PNG previews, source, assets, data, and brief provenance. Provide native draw.io where appropriate and verified. Maintain one canonical geometry source; do not hand-edit exports while continuing to overwrite them from stale code. State unverified formats.
9. **Integrate when requested.** Update manuscript references and captions, compile, and inspect actual figure pages and neighboring pages. Report what changed, what was verified, and remaining issues.

## Production sequence

1. Save a compact `figure-plan.md` using [the plan template](assets/figure-plan.md). Record selected/omitted jobs, source anchors, target size, one-sentence message, example status, evidence, layouts, and build/review order. For a simple graph, keep this brief; do not introduce an approval gate.
2. Build the evidence and method/setup contract. Use the same source-backed ledger for standalone graphs and teaser panels. Distinguish relative percent improvement from percentage-point differences and name the baseline.
3. Choose the scientific representation and layout. Freeze the meaning and connectivity before styling. Build separate plot panels at their final physical dimensions; reserve space for legends and captions before combining them.
4. Create vector structure and optional illustrative assets. Keep generated text, decorative arrows, and invented graph traces out of the authoritative diagram. Use shared example IDs, names, colors, and symbols across figures.
5. Render, inspect, and repair. Check both scientific fidelity and visual comprehension. Passing a JSON validator is not proof of either. Stop when concrete defects are resolved; document source or capability limits instead of endless cosmetic scoring.
6. Deliver and integrate as requested. Keep a concise build command, source/version notes, reviewed dimensions, and unresolved issues beside the output.

## Bundled tools and companion skills

This skill is self-contained. Its `foundation/` directory is a versioned bundle of the existing **paper-figure-creation** skill, preserving its detailed design/evidence instructions in `foundation/GUIDE.md`, plus templates, primitives, and scripts. The guide is not a second skill entry point. Resolve paths relative to this SKILL.md; do not assume a repository checkout exists. Commands below use `SKILL_ROOT` for this folder:

```bash
python "$SKILL_ROOT/foundation/scripts/validate_evidence.py" figure.json
python "$SKILL_ROOT/foundation/scripts/render_graphs.py" graphs.json --output output/graphs
python "$SKILL_ROOT/foundation/scripts/render_figure.py" method.json --output output/method --strict-layout
python "$SKILL_ROOT/foundation/scripts/compose_svg.py" composition.json --output output/figure --formats svg,pdf,png
```

Install Python dependencies from `foundation/requirements.txt` in the working environment when needed. Hybrid PDF/PNG export additionally needs Inkscape; editable SVG assembly remains available without it. Use custom SVG, Matplotlib, TikZ, or native draw.io when the starter grammar would weaken the explanation.

Read [companion integration](references/companions.md) if `codex-paper-figure-skill` or another figure skill is installed. Reuse its useful native-editing workflow without replacing local preferences or requiring a second installation. The generated bundle's origin and checksums are in `foundation-bundle.json`.
