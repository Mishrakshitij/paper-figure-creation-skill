# Standalone experimental graphs

Use `scripts/render_graphs.py` for standalone comparison, convergence, ablation,
scaling, or tradeoff panels. It consumes the **same** version-1 provenance and
evidence ledger as the teaser renderer, with `kind: "graphs"`. Keep plots driven
by data; image generation is never the source of plot marks, axes, or numbers.

```sh
python scripts/render_graphs.py experiment.spec.json --output figures/results \
  [--styles paper-styles.json]
```

Outputs: `results.svg`, `results.pdf`, `results.png`, `results-review.json`.
SVG text stays editable. PDF/PNG/SVG share one Matplotlib geometry source.
`bbox_inches="tight"` is deliberately not used because it changes physical size.
Native `.drawio` is not an experimental-plot export format.

## Plot selection

| Scientific question | Chart | Required care |
| --- | --- | --- |
| Compare a scalar across methods | `dot` | Stable method ordering; interval type stated if reported |
| Compare magnitudes with meaningful zero | `bar` | Zero must remain inside the value axis; prefer dot for small differences |
| Progress over an ordered numerical variable | `line` | Increasing sourced x coordinates; null observations break the line |
| Accuracy versus resources | `scatter` | Both quantitative axes linked to results for the same method/context; explicit log scale if useful |
| Matrix, distribution, survival, or another specialized question | Custom vector plotting code | Reuse the evidence ledger; document additional transformations and validate the intended statistical meaning |

Do not imply equal-budget superiority from a resource tradeoff. A proposed method
can lose on some settings. Preserve those results and state the scope of any claim.

## Fields

Top-level `provenance`, `evidence.metrics`, `evidence.results`, and
`evidence.claims` follow [the shared spec](spec-format.md).

- `figure`: `width_in`, `height_in`, `font_pt` (physical points), `dpi` (default
  300); optional `min_font_pt`, `panel_title_pt`, `title_pt`,
  `display_width_inches` for manuscript scaling, and `check_data_occlusion`
  (default true); optional `title`, `subtitle`, `note`, `watermark`. A long
  caption belongs in the manuscript, not a tiny figure footer.
- `figure.preset` selects the defaults:

  | Preset | Size and type | Encodings |
  |---|---|---|
  | `classic` (default) | 7.2 × 3.6 in, 8 pt text, 9 pt panel titles; below 6 pt refused, below `min_font_pt` (7) flagged | Cycled palette and markers; `role: proposed` gets the teal accent |
  | `house` | 5.5 × 2.2 in (the ICLR/NeurIPS `\linewidth`), 6 pt text, 7.5 pt panel titles; below 5.3 pt refused and flagged | Role encodings, "(ours)" in legends, arrows from the ledger ([house-figure-standard.md](house-figure-standard.md)) |

  `mark_ours` and `direction_arrows` switch the "(ours)" suffix and the arrows
  on or off in either preset.
- `layout`: integer `rows`, `cols`; normalized `left`, `right`, `bottom`, `top`;
  `wspace`, `hspace`; `shared_legend`, `legend_columns`, `legend_y`. These are
  composition controls, not automatic design recommendations.
- Each chart: `type`, `metric_id`, `title`, `xlabel`, `ylabel`, `series`;
  optional `panel_label`, `xlim`, `ylim`, `xscale`/`yscale` (`linear` or `log`),
  `xticks`, `yticks`, `xticklabels`, `yticklabels`, `legend`, `legend_loc`,
  `legend_columns`, `value_labels`, `value_format`.
- A chart can override the grid with `rect: [left,bottom,width,height]` in figure
  fractions. This is useful for aligned plots in a composed multi-panel figure.
- `dot`/`bar` require `categories`, aligned to every series.
- `line`/`scatter` use `x_values` on the chart or series. For an experimental
  independent variable, provide `x_source_id` and `x_source_location`. For a
  measured x metric, provide chart `x_metric_id` and series `x_result_ids`.
- A series requires `id`, `values`, `result_ids`; optional `label`, `role`,
  `style_id`, `color`, `marker`, `markerfacecolor`, `linestyle`. A stable
  id/style_id keeps its style and role across panels; contradictory explicit
  styles are rejected. Use hollow markers or shapes as well as color.
- `role` is `proposed`, `ablation`, `baseline` or `reference`. Under `house`
  it sets the default encoding: a large vermillion star, a hollow warm diamond,
  a muted circle and a black square. Explicit style fields override it. A
  series without a role (a task or a condition) gets a neutral colour that
  avoids the hot colour and the role shapes. For a one-series dot plot with one
  method per category, aligned `point_roles` encode each row the same way.
- A style registry fixes encodings across all figures of a paper. Pass it as
  `--styles paper-styles.json` (or `render_graphs(..., styles=...)`), or put it
  in the spec's `styles`. It maps a series id or style_id to `role`, `color`,
  `marker`, `markerfacecolor` or `linestyle`. A series or a spec `styles` entry
  that contradicts the shared registry is rejected.
- Direct labeling: `point_labels`, `point_label_offsets` (physical points),
  `point_label_align` (`left`, `center`, `right`, or `auto`), and `label_leaders`.
  Arrays must align with values. `value_labels: true` prints the actual values.
- For a single series with one method per category, use aligned `point_colors`
  and `point_markers`. This preserves rows without inventing missing values or
  staggering every method into a separate series.

## Direction arrows and Pareto frontiers

The better direction of a metric axis comes from the ledger's
`metrics[].direction`: the value axis of every chart, and the x axis of a line or
scatter chart with `x_metric_id`. With `direction_arrows` (on under `house`),
the renderer appends "↑" or "↓" to the axis label, or "(↑)" when the label does
not end in a parenthesis. A typed arrow, or a chart's `xdirection` /
`ydirection`, that contradicts the ledger stops the build. `ydirection: "none"`
suppresses the arrow on that axis.

A scatter chart's `pareto` block (`true` or an object) draws the non-dominated
plotted points as a step line. Optional fields: `series` (ids or style_ids that
compete; default all), `x`/`y` (directions, which must agree with the ledger;
needed when an axis has no ledger direction), `label` (default "Pareto
frontier"), `legend`, `color`, `linewidth`, `linestyle`. Missing results never
join the frontier, the line stops at the outermost measured points, and the
legend lists it last. The review JSON records each panel's `axis_directions`
and `pareto_result_ids`. A frontier describes these observations under these
objectives; it does not certify a statistically better method.

## Evidence linkage

Every nonmissing plotted number must equal its linked evidence result. Quantitative
x/y results must describe the exact same method and comparison context. If one
reported parameter count applies to multiple tasks, create task-context references
to the same source row/count and record that applicability; never weaken context
checks. `comparison_mode: "tradeoff"` can display differing budgets across methods,
but numerical improvement claims still require matched conditions.

The renderer reads uncertainty directly from the result's sourced `uncertainty`
object (`sd`, `se`, `ci`, or `range`). Symmetric and asymmetric intervals are
supported. The caption must state what the interval means and varies over. Never
assign a task-level typical SD to each row or invent bands for visual richness.
Explicit bounds cannot hide observations or their uncertainty intervals; log axes
reject nonpositive coordinates. An interval that ends within 1.5 pt of its
marker's edge cannot be read at print size, and its caps collide with the
marker (common with the house star). The renderer hides that bar and its caps,
keeps the other axis's interval, and lists it under the panel's
`intervals_inside_marker` with a warning: state that interval in the caption. Bars require a linear value axis with a meaningful
zero; categorical row axes must remain linear. No automatic statistical significance is inferred.

## Review and compose

Inspect exported pixels at the declared paper width and enlarged. The review JSON
checks source linkage, reported axis bounds, effective font size, page overflow,
text overlap, and supported legend/data occlusion using the preserved layout audit;
it **does not certify** scientific truth or detect every label collision. Adjust
the composition, shorten labels, or enlarge panels when needed. Render again after
each repair. When assembling with generated assets, import the SVG as vector
content at the intended physical size; inspect any resulting effective font scale.

`assets/graphs-template.json` is explicitly synthetic and cannot be final evidence.
`assets/paper-styles-template.json` starts a paper's style registry.
`examples/graphs-lora/` is a real-data, all-settings tradeoff example with a concise
provenance record and reproducible build command. `examples/graphs-house-pareto/`
renders the same ledger under the house preset, with a registry and a computed
frontier.
