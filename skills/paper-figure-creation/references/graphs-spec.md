# Standalone experimental graphs

Use `scripts/render_graphs.py` for standalone comparison, convergence, ablation,
scaling, or tradeoff panels. It consumes the **same** version-1 provenance and
evidence ledger as the teaser renderer, with `kind: "graphs"`. Keep plots driven
by data; image generation is never the source of plot marks, axes, or numbers.

```sh
python scripts/render_graphs.py experiment.spec.json --output figures/results
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
  300); optional `min_font_pt` (default 7), `display_width_inches` for manuscript scaling,
  and `check_data_occlusion` (default true); optional `title`, `subtitle`, `note`, `watermark`. The default font is
  8 pt. Below 6 pt is refused; below 7 pt is flagged for review. A long caption
  belongs in the manuscript, not a tiny figure footer.
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
- A series requires `id`, `values`, `result_ids`; optional `label`, `role`
  (`proposed`), `style_id`, `color`, `marker`, `markerfacecolor`, `linestyle`.
  A stable id/style_id keeps its style across panels; contradictory explicit
  styles are rejected. Use hollow markers or shapes as well as color.
- Direct labeling: `point_labels`, `point_label_offsets` (physical points),
  `point_label_align` (`left`, `center`, `right`, or `auto`), and `label_leaders`.
  Arrays must align with values. `value_labels: true` prints the actual values.
- For a single series with one method per category, use aligned `point_colors`
  and `point_markers`. This preserves rows without inventing missing values or
  staggering every method into a separate series.

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
reject nonpositive coordinates. Bars require a linear value axis with a meaningful
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
`examples/graphs-lora/` is a real-data, all-settings tradeoff example with a concise
provenance record and reproducible build command.
