# Introduction teaser

## The argument

A useful teaser answers four questions in one reading path: what is difficult, what changes, what happens in a concrete example, and what measured evidence supports that change. Use the abstract to identify the claim, then use the experiments to limit it. The headline should not claim more than the plotted comparisons.

Start with the concept panel at roughly 35% of usable width or area and evidence at roughly 65%. This ratio is a preference supplied for this skill, not a conclusion from the literature study. The examples in the research corpus motivate visual patterns, not a universal layout frequency.

## Compose the concept panel

Show one small example rather than a list of application icons. Define the task in plain words, then draw the operation that changes it. A lay reader should be able to describe the situation; a domain reader should recognize the mechanism.

| Scientific change | Useful concept encoding | Avoid |
| --- | --- | --- |
| Process only visible patches | Same patch grid before selection and after reconstruction; highlight retained tokens | An encoder box that still appears to receive every masked token |
| Adapt a frozen network cheaply | Frozen weight path plus low-rank trainable branch merging at an explicit sum | A smaller generic model that falsely suggests distillation |
| Retrieve missing knowledge | Question, selected documents, grounded answer; corpus branch joins the generator | An unlabeled database icon attached to an arrow |
| Predict a set directly | Same scene with object queries and unordered detections | Invented attention maps or model predictions |
| Render from a scene representation | Camera ray, sampled positions, field values, composed pixel | Decorative 3D cubes without ray-to-pixel meaning |
| Iterative optimization or denoising | Shared state shown at selected steps, with iteration/time index | A line of differently named networks that looks unshared |

If a drawn example is illustrative, label it as a schematic in the panel or caption. “Illustrative” must be visible enough that it cannot be mistaken for an observed output. Reuse the same example across panels where it helps causal understanding. A before/after pair should hold input, crop, scale, and conditions constant.

## Pick evidence by question

| Question | Default plot | Required context |
| --- | --- | --- |
| Which methods perform better on one metric? | Horizontal dot plot; bars when magnitude relative to zero matters | Units, direction, full relevant baseline set, exact dataset/split |
| What quality-cost trade-off is achieved? | Scatter with direct labels, optionally two aligned panels | Hardware/budget/protocol; honest log axis if scales span orders of magnitude |
| How does performance change with compute/data/steps? | Lines at actual measured x values | No synthetic interpolation points; uncertainty if reported |
| Does the improvement generalize? | Small multiples with common scales where meaningful | One panel per comparable task/metric; identify missing values |
| Which component matters? | Ablation dot plot or paired differences | Same backbone/training protocol; distinguish components from competing methods |
| What fails? | Matched qualitative pairs plus quantitative scope | Representative selection rule and observed outputs |

Use one strong plot if it answers the claim. Add a second only when it supplies a distinct necessary axis, such as cost versus quality, robustness, or an ablation. Do not pack unrelated datasets into one axis to reach a desired visual density.

## Make the proposed method findable without distorting the comparison

Use one consistent accent for the proposed method and neutral but readable baselines. Different baseline families can use muted secondary colors or shapes. Use a redundant shape/line encoding so grayscale still works. Direct labels often beat a distant legend for small method sets. For crowded charts, separate panels or label only selected endpoints with a complete legend.

“All methods” means all relevant methods in the defined comparison set, not every method ever published. Record inclusion/exclusion rules and put a complete comparison in supplementary material when the teaser would become unreadable. Do not silently drop a stronger competitor, a failure regime, an ensemble marker, or a different data budget.

Only annotate an improvement that the evidence helper has recomputed. Prefer “+0.7 percentage points at 2.75× lower training time” only if the formulation is unambiguous; “2.75× speedup, 63.7% less training time” is clearer for elapsed time. State the baseline. Do not replace a modest measured gain with a decorative “30% better” badge. Avoid claiming a causal mechanism from an uncontrolled leaderboard comparison.

Keep a clear metric axis even when a headline supplies the numeric takeaway. A truncated dot-plot scale can resolve small differences when endpoints are explicit; bars normally start at zero. Do not add a false zero, broken axis, dual axis, or area encoding just to exaggerate separation.

## Teaser caption structure

One compact paragraph: identify the problem/example; explain the change; state what each plot measures; give comparison scope, data source, and uncertainty convention. Include a limitation if the main visual otherwise suggests a broader claim. Do not repeat every axis label or narrate color alone.
