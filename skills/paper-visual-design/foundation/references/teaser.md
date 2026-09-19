# Introduction teaser

## The argument

A useful teaser answers four questions in one reading path: what is difficult, what changes, what happens in a concrete example, and what measured evidence supports that change. Use the abstract to identify the claim, then use the experiments to limit it. The headline should not claim more than the plotted comparisons.

Start with the concept panel at roughly 35% of usable width or area and evidence at roughly 65%. This ratio is a preference supplied for this skill, not a conclusion from the literature study. The examples in the research corpus motivate visual patterns, not a universal layout frequency.

Write the connection explicitly: “The concept shows [specific intervention]; plot A tests [its consequence]; plot B adds [a distinct condition or trade-off].” If these clauses describe unrelated stories, revise the selection or layout. A teaser should visually connect the abstract's idea and the experiments that support it.

## Choose the overall reading path

The 35:65 preference does not require a fixed left concept/right chart template. Compare a few compositions when the story is unresolved:

| Layout | Useful when | Main design test |
|---|---|---|
| Compact worked example beside one or two large plots | The mechanism is local and the evidence needs wide axes | Can the reader connect the visible intervention to the named method in the plots? |
| Example strip above aligned evidence panels | The setup requires a sequence or several corresponding objects | Does the example remain legible without taking over the evidence area? |
| Matched problem/proposal pair beside evidence | A changed action or outcome explains the contribution | Are input, crop, scale and conditions held constant across the pair? |
| Shared example with a small local operator inset and an evidence block | The novelty is hidden within an otherwise familiar process | Does the inset expose the change without duplicating the method figure? |

Let the task and intervention be recognizable at first glance, with the comparison accessible at ordinary paper size. A reader should not need to follow the detailed training loop before understanding why the experiments matter. Put that detail in the method figure.

## Compose the concept panel

Show one small example rather than a list of application icons. Define the task in plain words, then draw the operation that changes it. A lay reader should be able to describe the situation; a domain reader should recognize the mechanism.

Use enough actual content to make the setup meaningful: a selected passage fact and corresponding question, a retained versus discarded token, or a grid with an interpretable transformation. A document outline filled only with gray strokes can identify “text,” but it cannot teach how that text is edited. Conversely, a full paragraph or screenshot is excessive if only one fact matters. The representation contract in [visual-story.md](visual-story.md) helps choose that boundary.

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

A strong reference may use a dense radar, many small panels or a large benchmark summary. Reuse such a form only when the new data and reader's question justify it. Radar geometry can imply comparisons through arbitrary axis order, scales and filled area; aligned dot plots or small multiples often make metric-specific comparisons easier. Explain normalization if used and keep the original units recoverable. Do not copy chart types as a visual theme.

## Make the proposed method findable without distorting the comparison

Use one consistent accent for the proposed method and neutral but readable baselines. Different baseline families can use muted secondary colors or shapes. Use a redundant shape/line encoding so grayscale still works. Direct labels often beat a distant legend for small method sets. For crowded charts, separate panels or label only selected endpoints with a complete legend.

“All methods” means all relevant methods in the defined comparison set, not every method ever published. Record inclusion/exclusion rules and put a complete comparison in supplementary material when the teaser would become unreadable. Do not silently drop a stronger competitor, a failure regime, an ensemble marker, or a different data budget.

Only annotate an improvement that the evidence helper has recomputed. Prefer “+0.7 percentage points at 2.75× lower training time” only if the formulation is unambiguous; “2.75× speedup, 63.7% less training time” is clearer for elapsed time. State the baseline. Do not replace a modest measured gain with a decorative “30% better” badge. Avoid claiming a causal mechanism from an uncontrolled leaderboard comparison.

Keep a clear metric axis even when a headline supplies the numeric takeaway. A truncated dot-plot scale can resolve small differences when endpoints are explicit; bars normally start at zero. Do not add a false zero, broken axis, dual axis, or area encoding just to exaggerate separation.

## Teaser caption structure

One compact paragraph: identify the problem/example; explain the change; state what each plot measures; give comparison scope, data source, and uncertainty convention. Include a limitation if the main visual otherwise suggests a broader claim. Do not repeat every axis label or narrate color alone.
