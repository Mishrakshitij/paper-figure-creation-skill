# Method and architecture figures

## Start from computational semantics

Read the method section, algorithm pseudocode, and implementation when available. Establish what is computed, by which module, on which representation. The diagram should distinguish the proposal from unchanged machinery without implying that every colored box is novel.

Before laying out modules, identify the relation the figure must teach: how an edit changes a model, how candidates are compared, how a state is iteratively refined, how information is shared, or how a local operator changes a representation. Put that relation into the representation contract in [visual-story.md](visual-story.md). A method figure should allow a reader to explain an operation, not merely repeat its name.

Write a compact node-and-edge contract before drawing:

| Item | Record |
| --- | --- |
| Node | Operation, input/output object, optional shape, parameter sharing, trainable/frozen state |
| Edge | Data flow, conditioning, control, gradient/update, skip/residual, or supervision |
| Merge | Sum, concatenation, attention, matching, or another named operator |
| Loss | Prediction input, target input, training-only status, parameters updated |
| Stage | Pretraining, fine-tuning, inference; what is reused or discarded |
| Iteration | State index, update rule, reused parameters, stop condition |

Pair this computational contract with a visual instance where useful. For example, carry one candidate edit through its own adapted state and evaluation result; or keep the same tokens before selection, after selection and at reconstruction. An illustrative instance must be labeled as such and must not imply measured success. Use exact shapes and symbolic operators instead when a natural-language example would obscure the mathematical contribution.

One arrow convention should have one meaning. Use solid arrows for forward data, a separately labeled dashed convention for a distinct relation, and a legend only for conventions actually present. A frozen weight can participate in forward and backward computation without being updated; “frozen” does not mean “detached.” Stop-gradient requires its own explicit symbol or label.

## Select an appropriate topology

- **Residual/adaptation:** branch around the changed block and use an explicit sum; include scale factors when part of the method.
- **Encoder/decoder:** indicate representation sizes or resolution stages; route skip links between their correct levels, not to the nearest convenient box.
- **Retrieval/generation:** show the corpus and query branches, retrieval output, generator conditioning, and citation/answer output.
- **Contrastive/self-distillation:** paired views, shared or distinct encoders, teacher update or stop-gradient, and where embeddings are compared.
- **Diffusion/iterative refinement:** distinguish training noise construction from generation trajectory; identify timestep conditioning and repeated/shared denoiser.
- **Spatial/rendering:** retain geometry, camera/ray coordinate meaning, aggregation, and rendering loss. Use a spatial panel plus computation inset if a flowchart obscures the method.
- **Training versus inference:** aligned lanes with shared component identity; label losses/targets as training-only and show removed modules explicitly.
- **Generate/adapt/evaluate:** aligned candidate rows with common stage columns; retain each candidate's identity through its adapted model and reward, then show the policy update separately.
- **Agent/environment learning:** repeat a readable interaction unit; distinguish actual observations, model predictions, calibration data and parameter updates. Show the destination of shared signals explicitly.

The macro view usually contains a few consequential stages. Reserve a detailed inset for the novel operator or a representation step needed to understand it; do not imply that a conventional step is itself novel. Do not enforce a fixed maximum box count if it erases a necessary branch, and do not expose every implementation class when it hides the proposal.

## Show the change inside the structure

| If the contribution is… | Make this visible | Keep conventional context compact |
|---|---|---|
| A generated learning artifact | A short edit, synthetic example or configuration and the update it controls | The language model architecture unless it also changes |
| A candidate-selection or reward procedure | Candidate-specific outcomes and the selection/weighting relation | Identical candidate processing machinery |
| A new representation | A small before/after instance, correspondence and important dimensions | Unchanged preprocessing and prediction heads |
| A fusion or correction operator | Its distinct inputs, local computation and corrected output | The upstream systems producing those inputs |
| A new training arrangement | Shared versus separate parameters, supervision sources and update destinations | A full deployment architecture already explained elsewhere |

For paired comparisons, align unchanged stages and reuse the same input. Highlight the changed relationship as well as the changed component. For local enlargement, connect the overview to an inset using a callout convention distinct from computation; give the inset enough input/output context to stand on its own. For nested learning loops, separate the within-example adaptation from the across-example policy update by region, path and labels. The loop must terminate on the state it actually updates.

Keep **fitting an operator** distinct from **applying it** when the inputs differ. For example, labeled anchor pairs fit a calibration map; other predicted scores enter its application, not its fitting data. Similarly, a generated configuration controls augmentation and optimization; its text need not be an SFT target. In a reward-selected update, make the selected training records recoverable, rather than drawing only a reward wire into the optimizer. These distinctions should be visible in ports, labels or local structure before the caption supplies exact formulas.

## Place and route

Lay out the main path left-to-right or top-to-bottom; group by computational role rather than by aesthetic symmetry. For repeated branches, align equivalent operations into columns or rows so differences can be read without tracing every connector. Give branch and skip edges routing channels before fitting labels. Place feedback on the perimeter when that clarifies the main route, with an explicit destination and direction. Connect at explicit ports and keep arrowheads visible. Route around unrelated nodes. Avoid a crossover that can be mistaken for a merge; label or separate unavoidable crossings.

Put labels in boxes when they name operations and on edges when they name flowing objects. Tensor shapes are valuable at changes of dimensionality, token count, resolution, or modality; repeating every shape can bury the idea. Keep notation consistent with the paper, define unfamiliar symbols, and prefer plain labels to unexplained abbreviations.

Show trainable/frozen state through text or a second encoding, not just color. Use the same accent for the actual novel component in the teaser and method figure. Do not recolor unchanged backbone blocks as “proposed” simply because they belong to the proposed system.

A repetition container is a scientific assertion: include only the operations that repeat. Keep one-time embedding, prediction, and pre/postprocessing outside it. Treat background rectangles as visual regions unless the editable source implements actual group parentage; verify group behavior before promising that grouped objects move together.

## Semantic trace review

Trace a single input and ask:

1. Can it reach the output through valid operations with compatible representations?
2. Does every branch join at the right point with the correct operator?
3. Are conditioning and supervision distinguishable from input data?
4. Are loss targets available only when they should be, without test leakage?
5. Is every updated/frozen/shared parameter state correct?
6. Does the inference path match actual deployment?
7. Can a reviewer point to the proposal without reading the full caption?
8. Can they describe what changes at that location, using the visible example or operator rather than the module's name alone?

When a paper is ambiguous, record the ambiguity instead of resolving it by attractive geometry. A faithful simplified diagram is preferable to a precise-looking invention. The caption should name omissions, such as omitted normalization or repeated layers, when they affect interpretation.
