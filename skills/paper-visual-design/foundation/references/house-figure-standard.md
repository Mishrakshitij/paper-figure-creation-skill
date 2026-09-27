# House figure standard

This is the figure standard of the repository owner's papers and research
group. It collects standing instructions from the owner and from the group's
figure reviews. For a paper that follows it, it replaces the generic starting
points elsewhere in this skill, such as the 8.5 to 10 pt labels in
[design-system.md](design-system.md). The venue template and an explicit
request from the paper's authors override it.

The bundled graph renderer implements the parts that code can check. Set
`figure.preset: "house"` in a graph spec (see [graphs-spec.md](graphs-spec.md))
and render every figure of the paper with one style registry
(`--styles paper-styles.json`). The repository's `examples/graphs-house-pareto/`
shows the result on real data.

## Contents

Teaser · Role encodings · Axes · Size and type · Colour · Captions · Space ·
Diagrams · Results graphs · Regenerating · Provenance · Checklist

## 1. The page-one teaser shows the trade-off

- **Plot quality against the cost that matters** when the headline claim is a
  trade-off. The cost is what a user pays: tokens read per call, training
  accelerator-seconds, latency, or trainable parameters. Put the headline
  quality metric on y and the cost on x.
- **Draw the Pareto frontier as a step line.** A chart `pareto` block computes
  the non-dominated plotted points from the ledger's metric directions and draws
  their staircase. Never draw a frontier by hand, and never extend it past the
  measured points.
- **Label axes in plain words with units**, for example "Tokens per call" and
  "Strict adherence (%)". Use a log axis when the costs span orders of
  magnitude, and say "log" in the label.
- **Do not invent a cost axis.** When the claim has no trade-off, the evidence
  panel is the strongest supported comparison, such as a dot plot of the main
  metric, in the same encodings.
- **One panel per model family** when families are evaluated separately. Use
  aligned small multiples with a shared y scale, each with its own frontier.
- **Keep Figure 1 on page 1**, together with the start of the introduction.
  When fonts grow, keep the teaser's size on the page and tighten its layout
  instead. When the teaser also has a concept panel, the 35:65 split in
  [teaser.md](teaser.md) still applies.

## 2. One encoding per role, in every figure and table

| Role | Marker | Colour | Renderer role |
|---|---|---|---|
| Our method | Large star, "(ours)" in the legend | One fixed hot colour (vermillion `#D55E00`) | `proposed` |
| Our ablations and variants | Hollow diamond | The same warm family (orange, burnt orange) | `ablation` |
| Baselines | Muted circle | Desaturated greys and blues | `baseline` |
| Prompted models and references | Black square | Black | `reference` |

- **Keep the encoding identical across the paper**, so a reader sees at a
  glance what is ours. Tables follow it: our rows are lightly shaded and end in
  "(ours)", and the best value in each column is bold.
- **Fix the encodings once per paper in a style registry.** A registry maps
  each method id to its role, and optionally to a colour or marker. Every
  figure renders with it, so a baseline keeps its colour even when a figure
  omits other methods. The renderer rejects a series that contradicts the
  registry.
- In LaTeX, one definition serves the figures' colour and the tables' shading:

  ```latex
  % preamble: \usepackage[table]{xcolor}
  \definecolor{ours}{HTML}{D55E00}
  % header: Success (\%) $\uparrow$ & Questions $\downarrow$ \\
  \rowcolor{ours!10} \method{} (ours) & \textbf{65.1} & \textbf{1.8} \\
  ```

  `ours!10` is a 10% tint, inside the 15% limit of section 5.
- **Never reuse the hot colour** for a baseline, a task or a highlight.
- **Muted circles differ only in shade.** When a reader must tell baselines
  apart, label them directly or name them in the caption. Give one a distinct
  marker in the registry only when the comparison needs it.

## 3. Every axis says which direction is better

- Every axis label and every metric column header carries an up or down
  arrow: "Accuracy (%) ↑", "Tokens per call (↓)".
- The house preset appends the arrow from the evidence ledger's metric
  `direction`. It refuses a typed arrow or a declared `ydirection` that
  contradicts the ledger. Arrows go only on metric axes; a training-step axis
  has no better direction.
- Give each metric its formula and one sentence of intuition in the text
  before any result, and report a worst-case or macro companion next to a
  headline average.

## 4. Size and type at print size

- **Build at the template's `\linewidth`** and include with
  `\includegraphics[width=\linewidth]{...}`, never `0.8\linewidth`. Then the
  source and printed sizes are equal. The text width is 5.5 in for ICLR and
  NeurIPS. For ICML and CVPR, a column is 3.25 in and the full width is 6.75 in
  and 6.875 in.
- **Labels about 6 pt, panel titles about 7.5 pt, nothing below about
  5.3 pt** at print size. The house preset sets these, refuses a base font
  below 5.3 pt and reports any smaller text.
- **A scaled figure scales its text.** Effective size = source size × included
  width / built width. Pass `display_width_inches` to audit a figure that must
  be scaled.

## 5. Colour, scales and tints

- **One colour per task or condition, everywhere.** The overview figure
  introduces them, and later captions refer back ("colours mark tasks as in
  Figure 2").
- **One colour scale per quantity across figures.** A quantity keeps its scale
  and its direction (which end means more) in every figure.
- **Tints stay at 15% opacity or less**, so colour helps reading without
  clutter.
- **Category tags get pale chips**: a small rounded box in a light tint of the
  tag's colour behind a tag such as "gold" (pale gold) or "injected" (pale red).

## 6. Captions and text inside figures

- **The caption's first sentence is bold and states the takeaway.** The rest
  says what is plotted and the evidence grade: n, seeds, hosts, complete runs.
  Legends carry n and the seed count when they differ between series.
- **State an interval the figure cannot show.** An error bar shorter than the
  star is unreadable, so the renderer hides it and warns. Give that interval in
  the caption instead ("±0.1 questions, smaller than the marker").
- **No key lines that repeat the caption.** Remove an in-figure title, subtitle
  or note such as "test examples; bold: influential" when the caption says it.
- **In the prose, state the point first, then cite the figure inside the
  sentence**: "..., as Figure 1a shows". Never open with "Figure 1a shows
  that ...".
- **Leave a caption the authors edited alone** unless they ask for a change.

## 7. Dense and compact

- **Prefer a graph over a paragraph or a long table.** Use full-width figures
  with two or three panels, or rows of three or four small plots.
- **Wrap smaller figures and tables** with `wrapfigure`. The wrap fixes the
  height of the text beside it, so cut text outside the wrap region. The
  wrapped text must be at least as tall as the figure, or the wrap leaks into
  later headings.
- **Never leave a page that holds only one figure.** Merge it with a
  neighbouring figure or squeeze it into the text.
- **Heatmaps**:
  - cells show percentages, in one number format across heatmaps;
  - rows and columns keep one orientation in every heatmap, for example
    methods as rows and tasks as columns;
  - the colour direction is fixed and stated, for example darker means better;
  - a heatmap takes at most about 30% of a page, and several go in a 2 × 2
    grid.
- **Long appendix tables become graphs.** Report mean ± SD instead of per-seed
  rows, and keep the number of appendix tables small.

## 8. Concept and method diagrams

- **Two diagrams, as editable vectors (TikZ or SVG).** One is a concept figure
  of the problem and the loop. The other is a high-level diagram of how the
  method works. An image-generation draft may guide the layout, but the final
  figure stays vector art.
- **Numbered steps match the text.** Subtle circled numbers ①②③ in the figure
  match the steps (i), (ii), (iii) in the method section, with the figure's
  words identical to the text's. In TikZ, one macro keeps them subtle and
  identical across figures:

  ```latex
  \newcommand{\stepmark}[1]{\tikz[baseline=(s.base)]\node[circle,draw=black!45,
    text=black!70,inner sep=0.6pt,font=\sffamily\tiny](s){#1};}
  ```
- **Use clean flows of icons and arrows** with minimal text and generic labels,
  such as "LLM agent" or "judge", not model ids. Drop seed numbers, multipliers
  such as "8×", asterisks, and formulas used as labels.
- **Be faithful to the method.** Show the actual initialization, what is frozen
  and what is trained, and the data flow. A figure that starts training from
  the base model when training starts from the SFT checkpoint is wrong.
- **Show only what the reader has met.** A figure that uses methods the text
  has not yet introduced needs simplifying or a pointer.
- **Tolerate no geometry defects**: text overflowing a box, overlapping
  elements, connectors cutting through boxes. In the compiled PDF, check that
  every text box renders its text. A box that shows only quotation marks means
  a broken macro or font.

## 9. Results graphs across the paper

- **Use one plot style for all result plots**: the same fonts, encodings,
  grids and legend placement.
- **Show scalability, one graph per axis**: model size, input or context
  length, number of rules or updates, number of seeds, and cost. Keep one
  styling across the graphs, with log axes where the range is wide. Put
  parameter count on x for a model-size sweep within a family.
- **Show training dynamics for RL runs** as aligned small multiples: reward, KL
  divergence, loss and completion length at the recorded steps.
- **Replace a plot whose axis does not discriminate methods.** A saturated axis
  is a result to report in words, not a figure to polish.
- **Answer the reviewer before the review.** Rank the questions a reviewer
  would ask, and answer the top ones with a figure each, folded into the
  analysis.

## 10. Regenerate, don't redesign

When data or a metric changes:

- keep the figure's layout and encodings as close as possible;
- update every label;
- improve it only subtly: task-coloured headers, a light separation between
  groups, a neutral tint for the reference row, bold for the best entry.

Improve a figure the authors like incrementally, and redesign only when asked
or when the science changed.

## 11. Provenance: plots come from result artifacts

- Plot from the project's result files or its reproduction manifest. Never plot
  numbers typed from the paper, TikZ mock-ups, or a collaborator's stitched
  PNGs; regenerate those from the data.
- Values read from the paper are comparison targets only. A figure traced from
  pixels is a labelled redraw, not a reproduction.
- Record how each figure was produced, at the lowest sufficient level:
  - *render*, from the exact plotted table;
  - *aggregate*, from saved per-run outputs;
  - *selected points*, by rerunning only the missing points;
  - *full*, by rerunning the whole figure.
- Keep the plotting code, data, spec and review record next to the figure, in
  the project repository.
- A project README or walkthrough may add interactive HTML charts built from the
  same data. The paper uses the static vector export.

## 12. House checklist

Check before delivering any figure for a paper that follows this standard:

- [ ] Page-one teaser shows the trade-off, with a computed step frontier where a cost axis exists
- [ ] Ours is a hot-colour star labelled "(ours)"; ablations are hollow diamonds, baselines muted circles, references black squares
- [ ] The same registry encodes every figure; tables shade our rows and bold the best value
- [ ] Every metric axis and column header has the right ↑ or ↓
- [ ] Built at `\linewidth` and included with `width=\linewidth`; labels about 6 pt, nothing below 5.3 pt at print size
- [ ] One colour per task, one scale per quantity, tints at 15% or less
- [ ] The bold first caption sentence states the takeaway; no in-figure line repeats the caption
- [ ] No page holds a single figure; heatmaps follow section 7; wrapped text is at least as tall as its figure
- [ ] Method steps ①②③ match (i)(ii)(iii) word for word; labels generic; initialization and frozen parts faithful
- [ ] Every plotted value traces to a result artifact; the reproduction level is recorded
