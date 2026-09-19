# Research graph recipes

Use only the recipe that answers the manuscript's question. These are design
contracts, not fixed layouts. Obtain missing measurements from project artifacts;
do not substitute plausible values or transfer published results to the user's work.

## Model size versus Elo

Use a scatterplot with parameter count on x and the reported rating on y. A log x
axis often suits widely separated sizes; label its unit and scale. State whether
size means total, active, or trainable parameters, especially for mixture-of-experts
or adapter models. Do not interpret size as measured compute, memory, or latency.

Keep exact model/checkpoint identities and a single evaluation snapshot. Record
the rating source, date/version, population or task subset, judge or human protocol,
and reported interval definition. Scores from separate rating pools need separate
panels or a justified common calibration; equal numeric ratings do not establish
comparability across unrelated leaderboards. Record unknown details as unknown.

- Use shape for model family or training recipe and a consistent accent for the
  focal model. Separate SFT, SFT+GRPO, and SFT+DPO when they are actual evaluated
  variants. Do not infer their scores from an earlier discussion of the method.
- Plot reported uncertainty directly. Derive intervals from raw comparisons only
  with a documented rating estimator and resampling unit; arbitrary error bars,
  row-wise SD, and uncertainty inferred from a rounded score are inappropriate.
- Keep measurements at their true coordinates. Use label offsets with leaders or
  an inset for nearby models. Connect points only when a measured within-family
  sequence makes that connection meaningful; no line through unrelated models.
- Show the tradeoff without claiming causal effects of size. A frontier describes
  these observations and objectives, not a statistically certified winner.
- Avoid percentage-improvement claims on Elo's arbitrary origin. Report a rating
  difference within the same pool and distinguish it from win rate.

With the bundled renderer use `type: scatter`, a rating `metric_id`, a parameter
`x_metric_id`, and paired `result_ids` / `x_result_ids`. Both results must match
the same checkpoint and evaluation context. Keep a common y scale for comparable
panels; include a readable caption with the rating snapshot and interval meaning.

## Component ablation with an inclusion matrix

Align one method/variant per row with columns for actual component states, then
place a dot/interval result panel beside the matrix. Use explicit symbols for
present, absent, frozen, or changed; a blank must not ambiguously mean missing
data. Preserve the exact same row order in both panels. Keep the full system and
relevant removals, including negative or null effects. Matched protocol and budget
are necessary for a component-effect claim; annotate deviations. Do not construct
unrun component combinations to complete the grid. Use custom Matplotlib for the
matrix and import it as SVG at final size through the hybrid compositor.

## Learning curves and resource scaling

Plot actual recorded steps, tokens, wall time, or compute with units. Align runs
on the scientifically relevant variable, not merely their array index. Unequal
evaluation schedules need explicit alignment or separate traces; do not silently
interpolate into a common grid. Missing observations break lines. If smoothing
serves readability, disclose the method/window and retain a view of measured
variation; do not use smoothed values to estimate uncertainty or time-to-threshold.
With multiple seeds, state the aggregation, sample count at each budget, and what
bands represent. A single run cannot supply between-seed uncertainty. Use sourced
line charts for ordered measurements and scatter for disconnected budgets.

## Task heatmaps and distributions

Heatmaps need a visible colorbar, units, and explicit missing-cell styling.
Separate incompatible metrics or use a disclosed normalization whose reference
is recorded. Use a sequential scale for magnitude and a centered diverging scale
for signed changes. A numeric annotation must map to its actual color scale.

For distributions, prefer visible observations or an ECDF when sample support
matters. Box and violin plots require raw observations or clearly identified
reported summaries; never synthesize samples from a mean and error bar. State
whether observations are seeds, tasks, examples, or participants. A panel combining
these units without a documented aggregation changes the scientific question.

## Final-size review

Review at the manuscript's physical width: identify every model, read each unit,
locate missing values, and distinguish intervals without color. Move long protocol
details into the caption. A standalone graph and its inset in a teaser need separate
size checks. Keep data/specification, derivations, plotting code, caption, and
SVG/PDF/PNG together. If data is missing, complete the source contract and layout
plan, state the gap, and withhold the unsupported numerical panel.
