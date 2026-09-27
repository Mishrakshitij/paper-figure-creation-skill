# Research graph recipes

Use only the recipe that answers the manuscript's question. These are design
contracts, not fixed layouts. Obtain missing measurements from project artifacts;
do not substitute plausible values or transfer published results to the user's work.

## Page-one Pareto teaser (quality versus cost)

Plot the headline quality metric on y against the cost a user pays on x:
tokens read per call, training accelerator-seconds, latency or trainable
parameters. Link both axes to results for the same method and context
(`x_metric_id`, `x_result_ids`), so the better directions come from the ledger.
Add `pareto: true`: the renderer computes the non-dominated points and draws the
staircase between the measured points, legend last. Under the house preset, our
settings are stars in one hot colour with "(ours)", ablations hollow diamonds,
baselines muted circles and prompted or reference models black squares. Use one
series per method with one point per setting, so each method has one legend
entry. When model families are evaluated separately, draw one aligned panel per
family with a shared y scale. `examples/graphs-house-pareto/` is a worked
example. A frontier describes these observations under these objectives; it
does not show that a method wins at matched cost.

## Scaling sweeps and training dynamics

Give each scalability axis its own graph in one styling: model size within a
family (parameters on x, often log), input or context length, number of rules
or updates, number of seeds, and cost. For RL training runs, show reward, KL
divergence, loss and completion length as aligned small multiples at the
recorded steps, one colour per method as in every other figure. Replace a graph
whose axis saturates and no longer separates the methods; state that result in
words instead.

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

Heatmaps need a visible colorbar, units, and explicit missing-cell styling. Under the house standard, cells show percentages in one number format, every heatmap keeps one orientation (for example methods as rows and tasks as columns) and one stated colour direction, each takes at most about 30% of a page, and several go in a 2 × 2 grid. Regenerate a heatmap from its data; never paste a stitched image.
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
