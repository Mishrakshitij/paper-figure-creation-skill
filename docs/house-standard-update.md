# House figure standard: update and validation (25 September 2026)

## Why

The owner's papers follow a figure standard set by the owner and their research
group's figure reviews. This skill's generic defaults contradicted it in
several places:

- 8 to 9 pt labels instead of about 6 pt with a 5.3 pt floor;
- one teal accent instead of role encodings;
- no Pareto frontier for the page-one teaser;
- no better-direction arrows on axes;
- no way to keep a method's colour identical across all figures of a paper.

## What changed

- **`references/house-figure-standard.md`** (new, in the foundation). It covers:
  - the page-one teaser plotting quality against cost, with a computed step
    frontier;
  - the role encodings: star (ours), hollow diamond (ablation), muted circle
    (baseline), black square (reference);
  - arrows on axes and table headers;
  - `\linewidth` builds with 6 pt labels, 7.5 pt panel titles and a 5.3 pt
    floor;
  - one colour per task, one scale per quantity, and tints at 15% or less;
  - bold-takeaway captions, with no in-figure lines that repeat them;
  - compact layouts, including wrapped figures and the heatmap rules;
  - method diagrams whose ①②③ match the text's (i)(ii)(iii);
  - "regenerate, don't redesign";
  - plots only from result artifacts, recording the reproduction level;
  - a checklist.

  Both SKILL.md files route to it. The venue template and the authors'
  explicit requests take precedence.
- **`render_graphs.py`**:
  - `figure.preset: "house"` sets the house sizes and the role encodings, adds
    "(ours)" to legends, and adds arrows from the evidence ledger;
  - `role` covers `proposed`, `ablation`, `baseline` and `reference`, and
    `point_roles` does the same for one-series dot plots;
  - a style registry (`--styles` / `styles=`) fixes encodings across figures
    and rejects contradictions;
  - axis arrows or declared directions that contradict the ledger stop the
    build;
  - a scatter `pareto` block computes the non-dominated plotted points and
    draws their staircase, legend last. The review JSON reports
    `axis_directions` and `pareto_result_ids`;
  - an interval ending within 1.5 pt of its marker's edge is hidden with its
    caps and reported (`intervals_inside_marker`), so the caption states it;
  - an empty or null legend label never becomes " (ours)".

  The `classic` preset keeps the earlier defaults, so every earlier example
  renders as before.
- **Other guidance:**
  - graph recipes for the Pareto teaser, scaling sweeps, RL training dynamics
    and the heatmap rules;
  - updated sizes in planning and graphs;
  - LaTeX snippets for house table rows and step marks, both compiled with
    tectonic;
  - `assets/paper-styles-template.json`.
- **Example:** `examples/graphs-house-pareto/`, the LoRA Table 4 ledger under the
  house preset, with a registry, a computed frontier and direct labels for two
  near-identical MNLI points.

## Verification

- `python -m unittest discover -s tests`: 117 tests pass (9 new, 1 skipped as
  before). The new tests cover:
  - role encodings and "(ours)";
  - arrows from the ledger, and the refusal of contradicting arrows or
    directions;
  - the frontier against an independent brute-force non-dominated set, a
    restricted competitor set, and refusals for contradicting directions,
    unknown series and non-scatter charts;
  - the registry across figures and through the CLI;
  - the preset type floors;
  - `point_roles`;
  - hidden intervals at the marker edge, and empty labels;
  - unchanged classic defaults.
- The example was inspected as a 300 dpi PNG, and as its PDF rasterized at
  150 dpi in colour and in grayscale. The PDF is 5.5 × 2.25 in with embedded
  DejaVu Sans, "(ours)" and both arrows are in the text layer, and the minimum
  text is 6.0 pt.
- **Independent forward test.** A fresh agent received only the skill and a
  request in the owner's words: "make the evidence panel of the page-one teaser:
  task success versus questions asked per task, from Table 1 ... Use my usual
  figure style". The paper was a synthetic evaluation fixture. The agent passed
  all 10 assertions:
  - the house preset, 6 pt text at a 3.52 in panel slot, and
    `width=\linewidth`;
  - the star with "(ours)", the black square for the prompted agent, and muted
    circles;
  - the computed frontier (Prompted → ASKR) and both arrows;
  - the exact Table 1 values, with no invented error bar for the row that has
    none;
  - a bold-takeaway caption with the evidence grade, and a style registry.

  It also flagged the fixture's planted contradictions (seed count, test-split
  selection, training budget, a misattributed headline gain). It found two
  renderer issues, both fixed here and covered by tests: caps of a ±0.1
  interval colliding with the star, and the empty-label edge case. No old-skill
  baseline was run. Most assertions test features the old renderer did not
  have.
- The bundle was re-synced and checked with `scripts/sync_visual_design_bundle.py --check`.

## Limits

- Four muted baseline circles differ only in shade in grayscale. The standard
  says to label them directly or name them in the caption when a reader must
  tell them apart.
- Heatmaps, tables and method diagrams follow the standard through guidance
  and snippets. The bundled renderer draws dot, bar, line and scatter charts
  only.
- `inspect_figure.py` needs `pdfinfo`, which was not installed on the
  validation machine, so PDF proofs used PyMuPDF instead.
- A frontier describes the plotted observations under the declared
  objectives. It does not certify a statistically better method.
