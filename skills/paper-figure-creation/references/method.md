# Method and architecture figures

## Start from computational semantics

Read the method section, algorithm pseudocode, and implementation when available. Establish what is computed, by which module, on which representation. The diagram should distinguish the proposal from unchanged machinery without implying that every colored box is novel.

Write a compact node-and-edge contract before drawing:

| Item | Record |
| --- | --- |
| Node | Operation, input/output object, optional shape, parameter sharing, trainable/frozen state |
| Edge | Data flow, conditioning, control, gradient/update, skip/residual, or supervision |
| Merge | Sum, concatenation, attention, matching, or another named operator |
| Loss | Prediction input, target input, training-only status, parameters updated |
| Stage | Pretraining, fine-tuning, inference; what is reused or discarded |
| Iteration | State index, update rule, reused parameters, stop condition |

One arrow convention should have one meaning. Use solid arrows for forward data, a separately labeled dashed convention for a distinct relation, and a legend only for conventions actually present. A frozen weight can participate in forward and backward computation without being updated; “frozen” does not mean “detached.” Stop-gradient requires its own explicit symbol or label.

## Select an appropriate topology

- **Residual/adaptation:** branch around the changed block and use an explicit sum; include scale factors when part of the method.
- **Encoder/decoder:** indicate representation sizes or resolution stages; route skip links between their correct levels, not to the nearest convenient box.
- **Retrieval/generation:** show the corpus and query branches, retrieval output, generator conditioning, and citation/answer output.
- **Contrastive/self-distillation:** paired views, shared or distinct encoders, teacher update or stop-gradient, and where embeddings are compared.
- **Diffusion/iterative refinement:** distinguish training noise construction from generation trajectory; identify timestep conditioning and repeated/shared denoiser.
- **Spatial/rendering:** retain geometry, camera/ray coordinate meaning, aggregation, and rendering loss. Use a spatial panel plus computation inset if a flowchart obscures the method.
- **Training versus inference:** aligned lanes with shared component identity; label losses/targets as training-only and show removed modules explicitly.

The macro view usually contains a few consequential stages. Nest a detailed inset only around the novel operator. Do not enforce a fixed maximum box count if it erases a necessary branch, and do not expose every implementation class when it hides the proposal.

## Place and route

Lay out the main path left-to-right or top-to-bottom; group by computational role rather than by aesthetic symmetry. Give branch and skip edges routing channels before fitting labels. Connect at explicit ports and keep arrowheads visible. Route around unrelated nodes. Avoid a crossover that can be mistaken for a merge; label or separate unavoidable crossings.

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

When a paper is ambiguous, record the ambiguity instead of resolving it by attractive geometry. A faithful simplified diagram is preferable to a precise-looking invention. The caption should name omissions, such as omitted normalization or repeated layers, when they affect interpretation.
