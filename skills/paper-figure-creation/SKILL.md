---
name: paper-figure-creation
description: Create or revise evidence-grounded introduction teasers and method or architecture diagrams for AI research papers, with editable vector sources, reproducible experimental plots, and visual review at publication size. Use for academic paper figures, graphical abstracts, and Overleaf or Word figure exports.
---

# Paper figure creation

Make the contribution understandable on first inspection, then make every detail defensible on close reading. Produce original scientific figures from the manuscript, algorithm, and experimental evidence. A figure is an argument with traceable evidence, not an advertisement for the proposed method.

## Choose the job

| Requested figure | Design objective | Read next |
| --- | --- | --- |
| Introduction teaser / graphical abstract | Show the problem, one concrete example, the changed idea, and the strongest supported evidence | [teaser.md](references/teaser.md) |
| Method / architecture | Make the proposed computation reconstructable and its novelty localizable | [method.md](references/method.md) |
| Both | Share semantic colors, notation, component names, and example identity; allocate detail differently | Both references |
| Rework an existing figure | Inspect its source and rendered image; preserve correct semantics and repair specific communication failures | Relevant mode plus [review.md](references/review.md) |

Read [evidence.md](references/evidence.md) before drawing numerical claims. Read [design-system.md](references/design-system.md) for physical sizing and editable-tool choices. Use [pattern-atlas.md](references/pattern-atlas.md) when the appropriate visual grammar is unclear. These references are selective; do not load the full research corpus for an ordinary figure request.

## Establish a compact figure brief

Extract from available files before asking questions:

- **Reader and slot:** intended venue/template, one- or two-column width, target height, and teaser versus method.
- **One sentence:** “Given [input/problem], [specific change] enables [supported outcome] under [scope].” If this cannot be stated clearly, resolve the science before polishing the layout.
- **Example:** a small input and output that exposes the problem; identify whether it is observed experimental output or an illustrative schematic.
- **Novelty:** what computation, representation, training signal, or system arrangement changes relative to the relevant baseline.
- **Evidence:** source files/table cells, methods, metrics and directions, dataset/split, evaluation protocol, budget/hardware, uncertainty, and limitations.
- **Method contract:** ordered operations, branch/merge semantics, tensor or object identities, trainable/frozen states, losses, and training versus inference paths.

Write the brief and unresolved assumptions beside the figure source. When dimensions are unknown, start with a 7-inch-wide two-column draft and state that assumption; confirm the actual template before calling it submission-ready. When a crucial mechanism or data value is absent, ask the smallest necessary question. Continue with a clearly marked schematic or evidence placeholders if useful; never manufacture results to fill the composition.

## Design before rendering

Create two small composition alternatives in source or scratch. Compare their reading order, evidence area, and where the contribution becomes visible. Choose the simpler one that preserves the scientific distinctions.

For a teaser, default to **30–40% of usable panel area for problem/example/idea and 60–70% for experimental evidence**. This is a layout preference, not a distribution of figure types or a license to invent evidence. Use 35:65 as a starting point. Adapt only for a concrete reason and record that reason. The first glance should reveal the task and the supported takeaway; the second should reveal the comparator and conditions.

For a method figure, choose a topology that matches the algorithm: sequence, residual branch, encoder/decoder with skip links, two-stage training/inference, retrieval plus generation, iterative refinement, or multiscale hierarchy. Avoid forcing distinct methods into the same row of rounded boxes.

Use representational marks where the science needs them: patch grids for masking, tokens for sequences, paired views for contrastive learning, camera rays for rendering, documents for retrieval, or a matrix pair for low-rank updates. Generic “Input → Our module → Better output” diagrams hide the very idea the figure must explain.

## Build an editable, reproducible artifact

Prefer deterministic vector authoring: Matplotlib for experimental plots, SVG or native diagrams.net for geometry, and TikZ when the manuscript requires it. Use raster imagery only for real visual examples or clearly identified illustrations. Do not ask an image generator to draw quantitative axes, numbers, equations, or authoritative architecture wiring.

The bundled engine is an optional starting point, not a ceiling on design:

```bash
python scripts/validate_evidence.py figure.json
python scripts/render_figure.py figure.json --output output/figure --strict-layout
```

Run commands relative to this skill directory, or resolve its absolute path first. Read [spec-format.md](references/spec-format.md) and adapt an asset spec when using the engine. Keep raw evidence authoritative: plotted values are references to an evidence ledger, not independent numbers typed onto a canvas. For custom code, preserve the same provenance and review requirements even if its layout exceeds the bundled engine.

Choose one canonical geometry source. If editing a generated `.drawio` by hand, either migrate the changes back into the JSON/source or make `.drawio` canonical and regenerate its exports. Do not overwrite manual edits by rerunning stale code. Keep chart data and plotting code separate from the diagram editor's cosmetic adjustments.

## Review, repair, and stop

Read [review.md](references/review.md). Always inspect actual rendered pixels at intended print size as well as an enlarged view. Code inspection or successful export cannot establish visual quality. If image inspection is unavailable, say so and mark visual review incomplete.

1. **Evidence check:** trace plotted marks and claims to source cells; recompute improvements; preserve unfavorable results and qualify incomparable baselines.
2. **Semantic check:** trace one example through the method; verify arrows, merge operators, losses, conditioning, frozen states, and what exists at inference.
3. **Visual check:** inspect the paper-width export, grayscale preview, text extents, label collisions, edge crossings, crop, and consistency between related figures.
4. **Independent check when available:** give a reviewer the figure and caption without the intended interpretation. Ask them to state the task, change, result, and method path. Compare their answer with the brief. Do not treat a self-assigned score as an independent comprehension test.
5. Repair the highest-impact observed failure, rerender, and recheck the affected criterion. Continue while concrete defects remain. If two revisions do not resolve a structural problem, change the layout rather than accumulating patches. Stop once hard gates pass and further changes are cosmetic; document material open limitations.

Never certify a figure as “publication-ready” solely because the validator passes. It cannot verify an external source, establish fair scientific comparison, or judge novelty. Do not claim the skill outperforms another agent or workflow without a matched, independently reviewed evaluation.

## Deliver

Return the requested figure(s), a concise caption, and editable sources. Normally include vector PDF for LaTeX/Overleaf, editable SVG, high-resolution PNG for preview or document insertion, data/spec/source code, and a brief review/provenance record. Include `.drawio` when that is the selected editable workflow. Read [delivery.md](references/delivery.md) for integration and export checks.

State any unresolved source, scientific, or visual issue precisely. External uploads, publishing, or repository pushes require the current task's authorization; creating a figure does not authorize submitting a paper or altering unrelated files.
