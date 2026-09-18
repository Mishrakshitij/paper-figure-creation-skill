# Qualitative comparisons that explain the evidence

Use this when a paper needs to show what changed on the same case, or when an
attractive example is being used to explain a mechanism. It complements
[evidence.md](evidence.md) and [publication-polish.md](publication-polish.md).
Choose only the views needed for the scientific question; do not impose a fixed
panel count or turn a simple output comparison into a new experiment.

## Choose the comparison before the layout

Record the example identity, split, checkpoints, conditions, budget and selection
rule. A fixed ordering within declared outcome categories is reproducible;
choosing whichever case makes the largest visual gain requires disclosure.
Distinguish random or representative sampling from a gallery conditioned on
success, failure, disagreement or an error category.

A positive case explains that case. It does not estimate how frequently the
method helps. When highlighting wins, state the selection scope and provide
the corresponding failures or a linked complete comparison inventory. Preserve
mixed findings within a winning example: a successful output can coexist with
worse intermediate calibration or prediction. Do not replace an inconvenient
panel with a more favorable case while retaining the original case label.

## Build a visible argument

A useful reading order for a difficult comparison is **observed evidence →
task criterion → matched diagnostic**. Use it when each view answers a different
question, rather than as a universal three-panel template.

| Reader's question | Useful view | Evidence boundary |
|---|---|---|
| What visibly happened? | Aligned outputs, a filmstrip, a spatial overlay or an interaction trace | Actual recorded outputs; mark illustrative content separately. |
| What made the outcome correct or incorrect? | Native criterion curve, localized error map, constraint markers or exact evaluator conditions | Show the quantity the evaluator uses, with units and thresholds. |
| What part of the computation differs? | Paired predictions, residuals or component measurements under matched inputs | A measured association does not alone establish a causal explanation. |

Let images carry recognizable object and motion information. Use short labels
to name the consequential difference, with the experimental contract in the
caption. Make correspondences explicit through alignment and consistent method
colors; do not rely on paragraphs explaining which image belongs to which
measurement. Curves, dots and overlays should clarify the example, not compete
with it for space.

## Keep the visual comparison matched

Use the same case, goal or reference, crop, magnification, resolution and
postprocessing wherever comparison requires them. Apply overlays consistently.
If local zooms help, retain a shared overview and mark their regions. Preserve
the identity and geometry of observed outputs; generated replacements or
background removal must not alter experimental evidence.

For sequences, align panels by the meaningful common coordinate: acquisition
time, native environment steps, interaction count, inference budget or another
declared axis. Indexing saved frames is insufficient when recording intervals
differ. Distinguish method identifiers from status colors, and retain redundant
labels or marker shapes for grayscale reading.

Separate **each method's stopping endpoint** from an **equal-time or equal-budget
comparison**. Label different stopping times explicitly. Do not present one
method's early endpoint opposite another's later endpoint as simultaneous
observations, extend a stopped trace as if measured, or substitute a nearby
sample silently. Mark unavailable observations and explain their absence.

## Show the actual correctness criterion

Read the evaluator instead of inferring success from visual proximity. Preserve
multi-condition logic: if success requires several constraints jointly, display
those constraints or an exactly equivalent, explicitly defined diagnostic.
Do not invent a combined score or threshold on a convenient summary norm.
State relevant coordinate conventions, normalization and stopping rules.

A goal image may contain decorative markers, acquisition artifacts or objects
that are not scored. Identify the actual reference. Distinguish transient
success, final correctness, validity checks and cumulative reward when the
task treats them differently. For static tasks, the same care applies to
regional correctness, class-specific criteria and structured-output constraints.

## Recover missing diagnostics without changing the case

Prefer saved intermediate outputs. If an authorized analysis reconstructs an
execution, preserve the recorded inputs, actions or tool calls, initialization,
checkpoint and termination. Verify fidelity against the original record and
available state/output anchors before using reconstructed diagnostics.
Record the source versions, reconstruction procedure and any mismatch. A fresh
execution, resampled output or improved trajectory is a new result, not a
replacement for missing observations from the displayed case.

When fidelity cannot be established, keep the existing observations and mark
the diagnostic unavailable. Do not infer intermediate values from a smooth
curve drawn between endpoints. Newly measured diagnostics remain distinguishable
from those stored during the original experiment.

## Pair predictions on identical inputs and targets

To compare prediction quality, give both models the same observed history,
available context, actions or requested operation, and target. When comparing
different realized behavior traces, evaluate both predictors on each trace
separately; the traces themselves are not matched counterfactual outcomes.

Check that errors share a meaningful target space. Learned latent coordinates,
normalization, target encoders, decoding and preprocessing can differ even when
the metric name is identical. Establish common coordinates or choose a valid
shared observable; do not compare incompatible latent errors. Keep future
observations out of model-visible context unless the declared diagnostic
explicitly studies a different information setting.

Respect actual prediction boundaries. Exclude incomplete action blocks or
missing next observations when a full transition is required. Do not pad a
terminal segment, invent a target or relabel a shorter horizon as comparable.
Report exclusions and their rule; show gaps rather than connected fabricated
values. Paired dots are useful when each connection denotes one truly shared
input/target pair.

## Keep the conclusion at the tested level

Observed success, forecast accuracy, representation alignment, action ranking
and causal usefulness of a component are separate claims. Lower prediction
error on an executed action does not establish better ranking among unexecuted
candidates. A favorable representation diagnostic does not establish a better
decision. A mechanism explanation needs an appropriate controlled intervention
or ablation; a qualitative figure cannot supply that evidence by decoration.

Use scoped captions such as “on this matched case” when appropriate. Retain
counterexamples and unfavorable component measurements. If the requested
explanation needs a new experiment, identify the missing test without claiming
it has been performed or silently expanding figure-editing work.

## Targeted review prompts

Inspect the final manuscript-size rendering and ask:

- Can a reader match each observation to its case, method, time and diagnostic?
- Does the sampling rule explain both the highlighted examples and omissions?
- Are crops, references, scales and stopping endpoints fairly comparable?
- Does the marked success condition reproduce the evaluator's actual logic?
- Are replayed observations faithful, and are predictions paired on identical
  inputs and targets with missing transitions visible?
- Does the caption separate what happened, what was measured and what remains
  an untested explanation?

Then inspect enlarged crops for obscured evidence, clipped diagnostic labels,
ambiguous leaders and overlays that hide the relevant difference. Repair the
observed issue in the editable source and recheck at the intended paper width.
