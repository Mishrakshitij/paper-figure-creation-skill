# WMRL figure review

## What was reviewed

The authoring agent viewed the actual author repository's WMRL teaser and method assets, checked the paper's PDF text around Sections 3.1–3.3, and drew an original 7 × 3.92 inch method composition. The exercise was guided by those references. It is not a held-out or blind benchmark and does not establish superiority over another skill.

The generated color PNG, the 110 dpi physical-size proof, a Poppler rendering of the actual PDF, the grayscale proof, and export properties were checked. All five PDF font subsets were embedded CID TrueType fonts. No actual printed sheet or manuscript integration has been reviewed.

## Defects found and revisions

| Observed problem | Revision | Scientific/visual effect |
|---|---|---|
| The grading split initially left the code sheet before the group tokens | Move the split to the group-token output | Makes the unit of anchor selection visible |
| One calibration box received both paired anchor data and other-group predictions | Separate **Fit** and **Apply**, with only anchor pairs entering Fit | Removes the implication that unpaired predicted rewards train the calibrator |
| The conceptual inverse-variance fraction was too small at the intended size | Show explicit inverse-variance multiplication, merge, and normalization; move the exact denominator to the caption | Keeps the second contribution readable while preserving mathematical scope |
| `A` and the gradient sum convention depended on the caption | Define `A` in the figure and label sum scope for both streams | Makes the principal update objects understandable from the figure |
| Small explanatory text competed with primary operations | Shorten labels and raise the main labels to approximately 8–8.5 pt | Improves physical-size readability |
| Internal scorer arrows were hidden behind the anchor background | Lower that background's drawing layer | Keeps the reward-generation edges visible |
| The green fusion-input arrow crossed its heading | Route it into the weight's side through a reserved channel | Removes a visual collision and clarifies which factor multiplies which stream |

The fit/apply distinction and formula readability were also raised by a separate reviewer through the root agent; those comments were acted on before the revised preview was sent back. Independent re-review status belongs in the repository's aggregate review record rather than being assumed here.

## Semantic trace

1. A task conditions the policy, which produces candidate solutions collected into groups.
2. The group-level branch selects anchors or other groups. The approximate 10% anchor label is a paper method setting.
3. Anchors receive both real and predicted rewards. Their shared-candidate score pairs are the only displayed data feeding the calibration fit.
4. The fitted map and other-group predictions enter a separate Apply operation.
5. True rewards form the anchor gradient sum; corrected predictions form the other-group gradient sum. `A` is identified as group-relative advantage.
6. Separate inverse-variance multipliers weight those sums before normalization and a policy update.

The figure does not claim that raw predictions from other groups supervise the fit, that the world model becomes ground truth, that the variances are known exactly, or that the illustrated code produced an experimental result. The conceptual weighting formula and its implementation caveat remain in the caption.

## Remaining scope and production limits

The code snippet is 6.5 pt, marked illustrative, and optional for understanding the correction algorithm. Main labels are larger. A one-column version would need redesign. Multi-turn interactions, variance-estimation warmup and full within-group normalization are condensed or captioned. The source is deterministic Python geometry plus editable SVG, not a native draw.io document. The figure uses no copied author image assets and no generated empirical curves.

Automated export checks detect text outside the canvas and embedded PDF fonts; they do not establish semantic correctness or overall visual quality. Those conclusions rely on the actual source/figure inspections listed above.
