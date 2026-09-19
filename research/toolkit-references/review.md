# Reference review: research figures and hybrid composition

Reviewed on **2026-09-19**. This update inspected **five repositories, one marketplace listing, 20 source/license files and four rendered PNG assets**. Some files were inspected through targeted excerpts; the ledger distinguishes these. Upstream programs were not executed, and reference PDFs were not audited at physical manuscript size. This is a focused implementation review, not a claim to have reviewed hundreds of papers.

The [source ledger](source-ledger.json) records exact commits, paths, licenses, observations and limitations. No third-party code, figure artwork or icons from this review are redistributed.

## What the references contribute

| Reference | Useful principle | Adaptation needed here |
|---|---|---|
| [codex-paper-figure-skill](https://github.com/pengqianhan/codex-paper-figure-skill/blob/5538ad98a8724ecb4ed70102514cd9e51c00c0ee/codex-paper-figure-skill/SKILL.md) | Establish a dependency graph, explore an image reference, reconstruct editable draw.io objects. | Use generated imagery for composition and recognizable assets; keep scientific wiring, labels and quantitative evidence authoritative in vector source. |
| [figures4papers](https://github.com/ChenLiu-1996/figures4papers/blob/3c181f85e82c6f24948fcaaf3be6696102b41d8d/scientific-figure-making/SKILL.md) | Consistent methods, spare axes, dedicated legend space and task-specific plotting examples. | Make graphs a first-class workflow. Audit statistics and final dimensions rather than inheriting all plotting defaults. |
| [nature-figure](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-figure/references/multipanel-evidence-architecture.md) | Assign panels complementary roles in one scientific argument; test whether each panel changes the inference. | Plan the central claim and supporting evidence before allocating space. Preserve unfavorable or bounding evidence. |
| [academic-plotting](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/academic-plotting/SKILL.md) | Separate numerical charts from illustrations; extract structure from manuscript context. | Replace raster-authoritative diagrams with an editable hybrid assembly. Chart selection must follow the scientific question, not only table shape. |
| [research-skills figures pipeline](https://github.com/neuromechanist/research-skills/blob/af4f609f395d825ea2d2dadddc223be70ae904da/plugins/figures/skills/scientific-figure/SKILL.md) | Create components separately, assemble SVG, measure effective font sizes and export. | Build a real compositor with explicit physical units, local assets and reproducible geometry. Review imported SVG definitions and resizing. |

The [MCP Market listing](https://mcpmarket.com/tools/skills/scientific-figures-for-research) describes an older monolithic `scientific-figures` version with react-pdf composition. Its current upstream separates SVG composition, plotting, transparent icons, diagram primitives and figure QA. The current source is the implementation reference; the listing is discovery context.

## What the rendered assets actually show

These observations are visual readings, not independent verification of the papers' claims.

- **[Peng CRISPR example](https://github.com/pengqianhan/codex-paper-figure-skill/blob/5538ad98a8724ecb4ed70102514cd9e51c00c0ee/outputs/icon-crispr/demo-icon-crispr-preview.png):** five evenly spaced cards create a clear sequence and recognizable domains. Most scientific detail remains in prose, and generic icons conceal transformations. Adopt its editability and routing discipline; do not make this equal-card arrangement the quality ceiling.
- **[ImmunoStruct results](https://github.com/ChenLiu-1996/figures4papers/blob/3c181f85e82c6f24948fcaaf3be6696102b41d8d/assets/ImmunoStruct_results_IEDB.png):** the component-inclusion matrix aligned with outcome rows makes ablations interpretable. Mechanism, performance and explanatory views have different jobs. At reduced size, dense annotations need careful review; visible bars also use nonzero baselines.
- **[RNAGenScape teaser](https://github.com/ChenLiu-1996/figures4papers/blob/3c181f85e82c6f24948fcaaf3be6696102b41d8d/assets/RNAGenScape_teaser.png):** the same manifold appears twice and only the trajectory behavior changes. This directly exposes the proposed difference. Transfer the principle of a stable worked example, not the artwork or its scientific assertions.
- **[Nature heatmap atlas](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-figure/assets/chart-atlas/atlas-03-heatmaps.png):** tidy alignment alone does not establish valid encoding. Several panels titled “sequential” annotate negative values while their displayed colorbars start at zero. A template needs a semantic audit before reuse.

## Verified implementation traps

1. **Physical points are not arbitrary SVG units.** In the reviewed [overlay implementation](https://github.com/neuromechanist/research-skills/blob/af4f609f395d825ea2d2dadddc223be70ae904da/plugins/figures/skills/ai-full-figure/scripts/overlay_labels.py), `font_size_pt` is written as a unitless number in a pixel-sized viewBox. Inference from that geometry: 8 units on a 1024-unit-wide, 89-mm canvas is approximately **1.97 pt**, not 8 pt. Convert units through the complete scale or author in physical points.
2. **Variable names do not define uncertainty.** Chen's [raw data](https://github.com/ChenLiu-1996/figures4papers/blob/3c181f85e82c6f24948fcaaf3be6696102b41d8d/figure_ImmunoStruct/raw_data.py) divides the third column by `sqrt(5)` inside an array called `std`, while leaving the first two columns unscaled. Require the actual experiment's interval definition.
3. **A polished demo can carry unsuitable defaults.** The corresponding [bar script](https://github.com/ChenLiu-1996/figures4papers/blob/3c181f85e82c6f24948fcaaf3be6696102b41d8d/figure_ImmunoStruct/plot_bars.py) uses large source canvases and cropped bar axes. Prefer final-size authoring, zero baselines for bars, or clearly scaled dot/interval comparisons.
4. **Descriptions can disagree with code.** Orchestra's plotting skill calls a mean ± standard-deviation example a confidence band and describes a `YlOrRd` heatmap as diverging. Verify the statistic and encoding rather than trusting the heading.
5. **Automated checks complement scientific review.** The [independent QA workflow](https://github.com/neuromechanist/research-skills/blob/af4f609f395d825ea2d2dadddc223be70ae904da/plugins/figures/skills/figure-qa/SKILL.md) usefully separates measurement from visual judgment. Add manuscript/evidence context to scientific review: geometrically valid arrows can still encode a false mechanism.

## Licensing and reuse

| Repository | Observed root license | Treatment in this update |
|---|---|---|
| pengqianhan/codex-paper-figure-skill | MIT | Cited design ideas; no copied code or icons. |
| ChenLiu-1996/figures4papers | **CC BY-NC 4.0** | Reference inspection only; no copied implementation or artwork. |
| Yuan1z0825/nature-skills | Apache-2.0 | Original implementation; bundled third-party assets have separate terms. |
| Orchestra-Research/AI-Research-SKILLs | MIT | Original implementation and prose. |
| neuromechanist/research-skills | BSD-3-Clause | Original implementation and prose. |

License file links are pinned in the ledger. Nature's bundled Chen notice, dated 2026-08-03, predates the current Chen license and refers to a MIT root license; the reviewed current Nature root license is Apache-2.0. This mismatch is a reason to inspect current upstream and file-specific notices, not to infer unrestricted asset rights.

## Design consequences for this toolkit

Start with one planner that chooses teaser, method, conditional benchmark/environment or standalone graphs. The plan fixes the scientific message, panel roles, dimensions, evidence references and three candidate compositions for a complex figure.

Build precise plots independently and import them as vectors. Generate only the illustrative material that improves recognition; distinguish it from experimental evidence. Assemble images, editable objects, exact labels and plot panels from one geometry source, preserving typography at final size.

A new benchmark/environment illustration is conditional on the manuscript actually describing such a setup. Review the exported pixels and the scientific mappings separately. A successful render is necessary, but cannot certify accuracy, legibility or explanatory quality by itself.

