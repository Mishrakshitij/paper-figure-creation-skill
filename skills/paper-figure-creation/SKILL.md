---
name: paper-figure-creation
description: Create or revise evidence-grounded paper figures, architecture diagrams, and experimental plots with visual examples, generated or web-sourced assets, meaningful icons and logos, precise editable connectors, and paper-size and zoomed visual review.
---

# Paper figure creation

Make the contribution understandable on first inspection, then make every detail defensible on close reading. Design an original visual argument from the manuscript, algorithm, and experimental evidence. Correct labels on connected boxes are only a starting point: the reader should see what the objects are, what changes, and why that change matters.

Prefer visually explanatory figures: show a recognizable input, the consequential transformation, and the output or decision. Use task scenes, meaningful icons, matched before/after examples, and a paper-specific analogy when they make that relationship easier to grasp. Consider a generated scene or object asset when pictorial content adds explanatory value. A clear symbolic figure remains appropriate when the algebra itself is the subject. Read [visual-elements.md](references/visual-elements.md) for asset selection, analogy mapping, visual references, and when to invoke image generation.

Do not turn the abstract or implementation notes into paragraphs inside boxes. For an overview or method figure, establish a small label budget before drawing (often 30–60 prose words at one-column width, adjusted to the scientific contract). Prefer short object/action labels; move configuration, caveats, losses, and full definitions to the caption or manuscript. Equations and essential axis labels earn space when they explain the operation. Enlarging meaningful visual objects takes priority over adding icons around existing text. Reject a redesign if its silhouettes and relationships become meaningless when prose labels are covered.

## Choose the job

| Requested figure | Design objective | Read next |
| --- | --- | --- |
| Introduction teaser / graphical abstract | Show the problem, one concrete example, the changed idea, and the strongest supported evidence | [teaser.md](references/teaser.md) |
| Method / architecture | Make the proposed computation reconstructable and its novelty localizable | [method.md](references/method.md) |
| Benchmark / environment setup, **only when present in the paper** | Explain the task population, one concrete case, the available information or interactions, and how evaluation works | [benchmark-environment.md](references/benchmark-environment.md) |
| Multiple figures | Select only applicable modes; share semantic colors, notation, component names and example identity | Selected references |
| Rework an existing figure | Inspect its source and rendered image; preserve correct semantics and repair specific communication failures | Relevant mode plus [review.md](references/review.md) |

Start with [visual-story.md](references/visual-story.md) when inventing a composition or repairing a weak figure. Read [evidence.md](references/evidence.md) before drawing numerical claims, [design-system.md](references/design-system.md) for physical styling and editable tools, and [semantic-primitives.md](references/semantic-primitives.md) when implementing worked examples. Use [pattern-atlas.md](references/pattern-atlas.md) for additional topology choices. Load these selectively; an ordinary figure request does not need the full research corpus.

### Conditional setup routing

Do not add a third figure merely because a paper reports results on named benchmarks. Select benchmark/environment mode only when the manuscript or its primary supplement actually describes a benchmark, task-construction process, environment, or substantive evaluation setup that the reader needs to understand. Record the source location and whether the setup is **new, adapted, or existing relative to this manuscript**. A described existing environment can qualify; do not relabel it as the paper's contribution. Passing mentions, result tables alone, related-work surveys and generic dataset names do not qualify.

If presence is unclear, leave this mode unselected, inspect the available setup section or supplement, and record the missing information. If the user explicitly requests a setup figure, ask for the smallest missing source detail after extracting what is available; never invent an environment. A benchmark paper may need a teaser and setup figure without an algorithm architecture figure. The three modes are choices, not a mandatory package.

## Establish a compact figure brief

Extract from available files before asking questions:

- **Reader and slot:** intended venue/template, one- or two-column width, target height, and selected figure mode(s).
- **One sentence:** “Given [input/problem], [specific change] enables [supported outcome] under [scope].” If this cannot be stated clearly, resolve the science before polishing the layout.
- **Example:** a small input and output that exposes the problem; identify whether it is observed experimental output or an illustrative schematic.
- **Visual vocabulary:** recognizable task objects, useful icons, before/after correspondence, and any analogy with its scientific mapping and limits. Choose observed, original vector, or generated assets deliberately; record the role of each pictorial element.
- **Novelty:** what computation, representation, training signal, or system arrangement changes relative to the relevant baseline.
- **Evidence:** source files/table cells, methods, metrics and directions, dataset/split, evaluation protocol, budget/hardware, uncertainty, and limitations.
- **Method contract, when relevant:** ordered operations, branch/merge semantics, tensor or object identities, trainable/frozen states, losses, and training versus inference paths.
- **Setup contract, only for an eligible setup figure:** source/version, new/adapted/existing status, unit of evaluation, instance construction, model-visible inputs, evaluator-only information, scoring and aggregation; for interactive environments also observations, actions, state changes, reset/persistence and termination. Use [benchmark-brief.md](assets/benchmark-brief.md).

Write the brief and unresolved assumptions beside the figure source. When dimensions are unknown, start with a 7-inch-wide two-column draft and state that assumption; confirm the actual template before calling it submission-ready. When a crucial mechanism or data value is absent, ask the smallest necessary question. Continue with a clearly marked schematic or evidence placeholders if useful; never manufacture results to fill the composition.

## Design before rendering

Inspect the actual pixels of any supplied visual references. Identify how their objects, correspondences, grouping and reading path explain the science; do not infer visual quality from captions or copy a paper's surface styling. Record inaccessible references as uninspected. A reference can motivate a grammar without making that grammar appropriate for this paper.

Turn the brief into a **representation contract**: the concrete input/output example, which marks denote which objects, what each transformation changes, the first-to-last reading path, and where novelty becomes visible. Save it with the source. Favor a small worked example when it reveals the mechanism; a purely symbolic architecture can be clearer when exact dimensions and operators are the contribution.

For a new complex figure, or when an existing composition has failed, sketch **three genuinely different compositions** before detailed drawing: change grouping, narrative order or the relation between overview and example, not merely colors. Select using the brief's communication needs. Routine local repairs can retain a proven composition. [visual-story.md](references/visual-story.md) gives concrete selection and repair recipes.

Before polishing, choose a **focal relationship**: the concrete object and visible change that should dominate the first glance. Give that relationship recognizable structure and richer detail; keep supporting configuration and conventional machinery quieter. Read [art-direction.md](references/art-direction.md) when a correct figure still looks generic or when the user wants the visual richness associated with image generation. It covers scene composition, visual transformations, selective depth and attention.

When the user asks for richer visuals or aesthetic architecture diagrams, make [visual-elements.md](references/visual-elements.md) and [art-direction.md](references/art-direction.md) part of the active workflow. Improve the representation, not just the palette: expose an operation inside its module, preserve one example across stages, or add a task vignette that explains the inputs. Use [hybrid-authoring.md](references/hybrid-authoring.md) when the selected composition benefits from generated imagery. If appropriate imagery is available, incorporate it into the completed figure rather than stopping at an image prompt.

Generated images, web-searched images, downloaded PNG/SVG assets, official logos, model illustrations, and transparent cutouts are all available design choices when they explain the paper. Read [asset-sourcing.md](references/asset-sourcing.md) for search, download, source recording, background removal, and integration. Prefer originals from the relevant project/creator; inspect the actual pixels rather than trusting a search thumbnail. Use image editing to remove an illustration's background when helpful, then inspect edge quality on the final backdrop. Preserve exact official logos and experimental observations; obtain a clean source when generative editing would alter their identity or evidence.

For a teaser, default to **30–40% of usable panel area for problem/example/idea and 60–70% for experimental evidence**. This is a layout preference, not a distribution of figure types or a license to invent evidence. Use 35:65 as a starting point. Adapt only for a concrete reason and record that reason. The first glance should reveal the task and the supported takeaway; the second should reveal the comparator and conditions.

For a setup figure, choose the visual family before drawing: construction and scoring for a static benchmark; a concrete episode inside an environment boundary for interactive tasks; aligned cases for setup variants. Separate construction from execution and evaluator-only information from agent-visible inputs. The teaser's area ratio does not apply. Read [benchmark-environment.md](references/benchmark-environment.md) for the contract, layout recipes and failure checks.

For a method figure, choose a topology that exposes the central operation: repeated candidate rows with aligned stages, paired baseline/proposal paths, a shared-state iteration, spatial geometry with a local operator inset, or another faithful structure. Plan branch and loop routing with the composition, before filling the available space.

Make scientific objects recognizable: a passage with a selected sentence, the same grid before and after an operation, retained token identities, low-rank factors with dimensions, or an observed scene with vector overlays. Use only the detail needed to explain the change. Let repeated identities retain position or encoding, and show the novel transformation inside its module rather than highlighting an opaque “Ours” box.

For diagrams with connectors, read [geometry-and-inspection.md](references/geometry-and-inspection.md). Assign named ports and route continuous paths around objects; do not hide a line under a label and mistake the resulting gap for a clean connector. Align related blocks, use deliberate routing channels and consistent spacing, and keep arrowheads attached to the intended target. Treat broken connectors, ambiguous crossings, wrong directions, clipping, text overflow, and unintended overlap as defects to repair before delivery. Neither a successful build nor an automatic geometry check proves this has been achieved.

## Build an editable, reproducible artifact

Prefer deterministic vector authoring: Matplotlib for experimental plots, SVG or native diagrams.net for geometry, and TikZ when the manuscript requires it. Use raster imagery only for real visual examples or clearly identified illustrations. Do not ask an image generator to draw quantitative axes, numbers, equations, or authoritative architecture wiring. When a generated or observed scene materially helps teach the task, use the [hybrid-authoring workflow](references/hybrid-authoring.md): keep the illustration as a sourced asset and construct exact labels, masks, relations and plots in editable vector layers. A hybrid PDF/SVG is not fully vector; disclose the asset boundary. Image generation remains optional, and a rich vector-only scene is often the appropriate choice.

The bundled engine is a starting point for compatible layouts. Use custom vector code or native diagram geometry when its grammar cannot express the chosen representation; do not simplify the scientific story merely to fit a renderer:

```bash
python scripts/validate_evidence.py figure.json
python scripts/render_figure.py figure.json --output output/figure --strict-layout
```

Run commands relative to this skill directory, or resolve its absolute path first. Read [spec-format.md](references/spec-format.md) and adapt an asset spec when using the engine. Keep raw evidence authoritative: plotted values are references to an evidence ledger, not independent numbers typed onto a canvas. For custom code, preserve the same provenance and review requirements even if its layout exceeds the bundled engine.

Choose one canonical geometry source. If editing a generated `.drawio` by hand, either migrate the changes back into the JSON/source or make `.drawio` canonical and regenerate its exports. Do not overwrite manual edits by rerunning stale code. Keep chart data and plotting code separate from the diagram editor's cosmetic adjustments.

## Review, repair, and stop

Read [review.md](references/review.md). Always inspect actual rendered pixels at intended print size as well as an enlarged view. Code inspection or successful export cannot establish visual quality. If image inspection is unavailable, say so and mark visual review incomplete.

Use `python scripts/inspect_figure.py figure.pdf --output-dir review --width-inches 5.5` when a reproducible PDF proof is useful; pass the actual manuscript width. Add targeted `--crop name:x0,y0,x1,y1` regions for dense connections, arrowheads, and text edges. Open the generated paper-size proof and enlarged crops with an image-viewing tool, record concrete defects, fix the editable source, and inspect the new exports again. Search and visually inspect relevant paper/reference images when a composition remains unclear; preserve the distinction between learning a visual grammar and copying artwork or scientific claims.

1. **Evidence check:** trace plotted marks and claims to source cells; recompute improvements; preserve unfavorable results and qualify incomparable baselines.
2. **Semantic check:** trace one example through the selected mode. For a method, verify arrows, merge operators, losses, conditioning, frozen states and inference access. For a setup, verify task construction, observation/action direction, state changes, information access, stopping and the exact success criterion; do not imply evaluation scores are training feedback unless the source says so.
3. **Visual check:** inspect a thumbnail for grouping and emphasis, then the paper-width export for comprehension and legibility. Check correspondences, example-to-operator alignment, novelty visibility, grayscale, collisions, crop, and consistency between related figures. A clean export can still fail to explain the method.
   Check each icon, scene and analogy as well: what scientific object or relationship does it explain, and could it imply an unmeasured result or nonexistent model component? Generated artwork and observed output must remain distinguishable. Decorative elements that compete with the mechanism should be simplified or removed.
4. **Independent check when available:** give a reviewer the figure and caption without the intended interpretation. Ask mode-specific questions: task/change/result for a teaser, computation for a method, or task/input/actions/visibility/success criterion for a setup. Compare their answer with the brief. Do not treat a self-assigned score as an independent comprehension test.
5. Repair the highest-impact observed failure, rerender, and recheck the affected criterion. Continue while concrete defects remain. If two revisions do not resolve a structural problem, change the layout rather than accumulating patches. Stop once hard gates pass and further changes are cosmetic; document material open limitations.

Never certify a figure as “publication-ready” solely because the validator passes. It cannot verify an external source, establish fair scientific comparison, or judge novelty. Do not claim the skill outperforms another agent or workflow without a matched, independently reviewed evaluation.

## Deliver

Return the requested figure(s), a concise caption, and editable sources. Normally include vector PDF for LaTeX/Overleaf, editable SVG, high-resolution PNG for preview or document insertion, data/spec/source code, and a brief review/provenance record. Include `.drawio` when that is the selected editable workflow. Read [delivery.md](references/delivery.md) for integration and export checks.

State any unresolved source, scientific, or visual issue precisely. External uploads, publishing, or repository pushes require the current task's authorization; creating a figure does not authorize submitting a paper or altering unrelated files.
