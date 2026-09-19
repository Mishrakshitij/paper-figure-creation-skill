# Standalone experimental graphs

A graph is a first-class deliverable and can also supply an exact vector panel to a teaser. Read [evidence](../foundation/references/evidence.md), [graph schema](../foundation/references/graphs-spec.md), and the executable renderer as needed. Use the same evidence ledger as other figures; never maintain a second unchecked set of chart numbers.

## Select the encoding from the question

| Question | Preferred encoding | Conditions |
| --- | --- | --- |
| Which method performs better? | Aligned dots/intervals; bars when magnitude from zero matters | Include relevant baselines; dot axes may zoom with clear bounds |
| How does performance vary with continuous budget/time? | Line/scatter with measured x values | Connect only meaningful ordered quantities; log axes explicit |
| What accuracy/cost tradeoff exists? | Scatter, optionally a justified Pareto frontier | Trace both axes; do not call parameter count latency or compute |
| Which components help? | Ablation dots or bars aligned with a component-presence matrix | Match protocol; preserve row order across matrix and plot |
| How does a method behave across tasks? | Aligned small multiples | Share scales for comparable metrics; separate incompatible units |
| What is the distribution or variability? | Raw points, ECDF, box/violin as justified | Require raw samples or reported summaries; do not invent samples |
| Which method/task pairs are strong? | Heatmap with explicit scale and missing-cell marks | Use custom Matplotlib if the bundled renderer lacks the encoding |

The bundled renderer supports dot/bar/line/scatter; it is a safe starting point, not a ceiling. Use original custom plotting code for a justified encoding and retain all provenance/physical-size review requirements.

For model-size versus Elo, ablation matrices, training curves, and task heatmaps, use [research graph recipes](graph-recipes.md). These recipes describe the scientific decisions; they do not provide invented measurements.

## Preserve comparisons and uncertainty

- Match dataset/split/protocol/budget when asserting improvement. Clearly separate conditions that differ. Do not hide favorable or unfavorable settings by selecting a convenient default.
- Keep each chart value tied to a result ID; trace x values too. A parameter count reused across datasets needs a source-backed task-context reference, not relaxed comparability checks.
- Keep method identity and color stable across panels; distinguish settings such as ranks/budgets explicitly. Use marker shape, line style, or direct labels as well as color.
- Distinguish SD, SEM, CI, and min/max from the source definition, not a variable named `std`. Record sample count and aggregation when known. Never invent uncertainty bands because a plot looks empty.
- Distinguish absent measurements from zero. Do not interpolate missing experiments without an explicit analytical reason and visible disclosure.
- Use zero-based bar axes. For meaningful zoomed comparisons use dots/intervals; show any log scale plainly. Do not use perspective/3D bars, smoothing that creates unsupported trends, or oversized visual effects.
- Do not add statistical significance symbols without a real analysis and stated test.

## Publication geometry

Build at the actual panel width in inches/points. Prefer approximately 8–9 pt labels as a draft starting point, subject to the template. Reserve margins for long method names and legends before rendering. Do not create a poster-size graph and shrink it to fit. Preserve editable SVG text (`svg.fonttype='none'`) and embedded PDF fonts where supported. Use vector marks for ordinary plots; rasterize only genuinely dense data layers with a recorded resolution.

Keep grids light, axes economical, and the proposed method identifiable through one consistent accent. Avoid eight unrelated bright colors when direct labels and a neutral baseline family would work. Keep every method identifiable in grayscale. Align comparable panels and show units/directions in concise labels.

Render the standalone graph first, then import the SVG into a larger composition. Inspect the effective type size after import. Deliver source data, exact extraction locations, plotting specification/code, PDF/SVG/PNG, and a caption stating protocol, uncertainty, and limitations.
