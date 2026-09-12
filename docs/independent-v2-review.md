# Independent figure-comprehension review, v2

Reviewed on 2026-09-12 by a separate agent assigned to interpret the exported images. This is a qualitative comprehension review, not an aesthetic score, a source-paper audit, or a claim about a population of readers.

For each initial figure, I viewed the PNG before reading its caption, brief, code, or previous reviews, then recorded my interpretation and concrete questions. Later revision checks were informed by those observations and the authors' descriptions of the repairs; they were not fresh blind tests. Captions and briefs were read only after the corresponding image-only interpretation had been communicated. I did not edit any figure.

## Review outcome

The initial WMRL image had two material information-flow ambiguities: the group split originated beside the candidate code, and ordinary predicted rewards entered the operation labeled as fitting the calibration map. The revised image resolves both. The initial SEAL teaser's emphasis could imply winning every knowledge setting, and its method omitted an explicit edit/reward training record; the revised pair resolves those problems. The MAE image had internally consistent patch identities and no comparable major routing failure. Its remaining questions concerned terminology and the prominence of its restoration detail.

The inspected WMRL and SEAL print previews carry their main mechanisms at seven inches wide. Small supporting labels still require closer reading. Exact estimator details, experimental scope, and domain-specific selection rules depend on the captions. These observations apply to the versions listed below; subsequent minor changes owned and checked by the root agent are not independently certified here.

## WMRL

### Initial image-only interpretation

An agent attempts to improve a classifier by producing executable candidate solutions in groups of at least two trajectories. A small anchor fraction, approximately 10%, receives both real-execution rewards and world-model predictions. Matched real/predicted rewards fit a monotone correction. The correction is applied to model rewards on the other groups. Separate real-reward and corrected-model-reward gradient streams are then combined according to their reliability to update the agent policy.

I understood the central proposal as spending real execution on a small anchor fraction, using those observations to correct cheaper model rewards, and weighting the resulting updates by their reliability.

### Observed problems and revised status

| Initial observation | Revised-image finding |
| --- | --- |
| The anchor/other branch left the candidate-code card, while the displayed group objects ended without entering that split. | **Resolved.** The branch now begins beside the group stack. |
| Other-group predicted rewards entered “Fit a monotone map,” implying that unmatched predictions trained the map. | **Resolved.** Anchor pairs alone enter fitting. A separate apply operation receives both the fitted map and other-group predictions. |
| Real and predicted values did not clearly connect into the matched-pair collection; the trusted stream began at the outer anchor region. | **Resolved.** Each reward output has an explicit pair-collection arrow, and the trusted stream starts at real reward `r`. |
| The fusion fraction was visually dense; `A` and the sum/mean meaning of the gradients were not defined. | **Resolved at schematic level.** `A` is labeled as group-relative advantage, both streams say they sum over their group sets, and weighted arrows converge into a sum/normalize operation. |
| `V` and the exact normalization were not self-contained. | **Caption-dependent.** The caption defines the variance quantities and supplies the group-count-weighted denominator. |

The actual inspected print preview is 770 × 431 pixels at 110 dpi, equivalent to seven inches wide. Principal stages, operations, stream equations, and group objects remain legible. The illustrative code, subscripts, and advantage gloss are small but subordinate. I found no new material information-flow failure in that revision.

### Caption/brief cross-check and limits

After the independent reading, the local caption and brief agreed with my interpretation. The caption also explains that relative weights are estimated from calibrated anchor residuals, rather than implying direct access to oracle variances. It gives

`g_hat = (w_E g_E + w_WM g_WM) / (w_E |G_E| + w_WM |G_WM|)`.

The figure condenses multi-turn behavior, variance warmup, and the return edge to the next policy iteration. Those are stated simplifications. I did not independently verify the cited source paper.

## SEAL

### Initial image-only interpretation

The model receives new information or a few-shot task and generates a self-edit used to adapt its parameters. For knowledge, an edit is rewritten training text; for a grid task, it is an augmentation/training configuration. The distinctive learning step is to train the edit-generating policy from the downstream performance of models actually adapted with its candidate edits.

The method starts several candidate adaptations from the same current parameters, tests the adapted copies on a held-out task, and selects rewarded context/edit pairs for SFT of the generator. I read this as reward-based edit selection followed by policy training, not as differentiation through the inner adaptation procedure.

The teaser's displayed knowledge results have the following winners:

| Setting | SEAL | GPT-4.1 data | What is supported |
| --- | ---: | ---: | --- |
| 1 passage, LoRA | 47.0 | 46.3 | SEAL has the largest reported point estimate, by 0.7 points. |
| 200 passages, full finetuning | 58.2 | 59.4 | GPT-4.1 data leads by 1.2 points. |
| 2,067 passages, full finetuning | 46.4 | 49.2 | GPT-4.1 data leads by 2.8 points. |

SEAL exceeds the base, passage-only, and self-generated-data baselines in all three settings. The settings change both passage count and adaptation procedure; the last column also has a different base-model accuracy. These columns do not isolate a passage-count effect.

On the depicted filtered ARC evaluation with Llama-3.2-1B, SEAL has 72.5% success versus 20% for self-edit without RL and 0% for ICL, below the 100% oracle. The visible scope is eight curated tasks and five edits/task, with uncertainty unreported. The figure does not establish performance beyond that evaluation.

### Observed problems and revised status

| Initial observation | Final inspected pair |
| --- | --- |
| The strongly highlighted SEAL row, including bold losing values, visually implied a win across all knowledge settings. | **Resolved.** Only the actual best value in each column is bold, with an explicit key. GPT-4.1's 59.4 and 49.2 are now the bold winners in their columns. SEAL identity still has a colored row. |
| The teaser's edit/finetune/recall sequence also described the no-RL baseline; its learning mechanism was absent. | **Resolved.** The edit generator is labeled RL-trained, and a dashed recall-reward return is explicitly marked as training only. |
| The outer policy-update operation received only score wires, without showing the context/edit records that train the generator. | **Resolved.** The revised method explicitly collects context, edit, and reward in an RL record before SFT on selected context/edit pairs. |
| Successful and failed candidates entered an identical bus, leaving their role in the update ambiguous. | **Resolved at schematic level.** They now enter the record collection; selection occurs afterward. The caption clarifies generic improving-edit selection versus best-candidate selection in the knowledge experiment. |
| Configuration edits entered generic SFT blocks as though their text were itself supervised training data. | **Resolved.** The inner blocks now say “Apply edit + SFT,” and the configuration example explicitly says it controls training. |

The final inspected teaser is 700 × 480 pixels at 100 dpi, and the method preview is 700 × 535 pixels at 100 dpi: both are seven inches wide. Main stages, candidate identity, and plotted values are readable at that size. The teaser's vertical feedback label and small experimental footers require closer reading. No further image change was necessary to resolve the material issues found in this review.

### Caption/brief cross-check and remaining limits

The local caption explicitly says to compare methods within columns because update settings differ. It states that SEAL leads only in the single-passage setting and trails GPT-4.1 data under continued pretraining. It identifies unreported uncertainty and the restricted ARC evaluation, and the method caption explains the training-only reward loop and domain-specific selection rule. These agree with the revised images.

The ARC aggregation unit was initially unclear from the image and supplied caption. I subsequently read the added caption paragraph, which defines success as a self-edit adaptation producing a correct held-out output, with five edits independently applied to each of eight curated evaluation tasks. It also states that tasks were selected for solvability under the oracle configuration. This resolves the local-caption measurement-unit question. The root agent verified that addition against primary Section 4.1; I did not independently inspect that source. The 0.7-point knowledge lead remains a reported point-estimate difference, not evidence of statistical superiority. The fictional passage and grid are plainly marked as illustrative examples.

## MAE

### Initial image-only interpretation

This is image-reconstruction pretraining. Four of sixteen patches, at original positions 2, 6, 11, and 15, remain visible. The four visible tokens enter the encoder in the displayed order 11, 2, 15, 6 with positional information; hidden patches do not enter the encoder. Four encoded latents and twelve mask placeholders are restored to their original sixteen positions. Decoder position embeddings are added, a lightweight decoder reconstructs pixels, and masked-only MSE compares the twelve hidden locations with their original image content.

The core architectural idea is a short visible-token encoder input followed by full-position reconstruction in a lighter decoder. The figure demonstrates mechanics and explicitly says no model was run; it is not reconstruction-quality or speed evidence.

### Observations and status

- **Identity/routing consistency:** visible patch IDs, shuffled sequence, restored positions, and blank visible locations in the target grid all agree. I found no material routing contradiction.
- **Selection terminology:** “Select 25%” did not specify random, fixed, or content-aware sampling. The initial choices could appear purposeful because they preserve parts of the tree. The root agent reports that a random-selection label was subsequently added; I did not re-inspect that revision.
- **Mask-token terminology:** `M × 12` initially left shared learned embeddings versus zero or distinct placeholders unclear. The caption explicitly defines copies of one shared learned mask token, resolving that terminology through the caption. I did not inspect a later image revision or claim that this clarification was added to the image.
- **Loss:** masked-only scoring is explicit, but predicted-side selection is implicit in the arrow from the complete reconstruction. Original-target provenance is given in text rather than by a long wire from the input. These are minor reading dependencies, not contradictory routes.
- **Hierarchy:** the large restoration inset places substantial attention on patch order. The brief explains that restoration is an expanded teaching detail; it does not claim unshuffling as an independent algorithmic novelty. The caption also says model stacks are schematic, not literal layer counts.

The initial image's main mechanism should remain identifiable at seven inches; patch IDs, the position-embedding note, and omission text are comparatively small. Unlike WMRL and SEAL, I did not independently inspect the final MAE physical-width proof in this pass. The later caption/brief reading agreed with the mechanism I inferred and documented the omitted projections, CLS token, attention details, and downstream task. I did not reverify the primary sources.

## Image identity record

Hashes refer to bytes present immediately before inspection. The first SEAL pair changed while its review was being written; its final checks are listed separately. The initial WMRL hash was not captured before the file was replaced, so it is not reconstructed or claimed here.

| Review point | Image | SHA256 |
| --- | --- | --- |
| SEAL initial | `seal-teaser.png` | `f834a825981704e36b37cfd18ef887ff087dd383524d097c57973eb2887eb9c0` |
| SEAL initial | `seal-method.png` | `db485fbaa637fba8ff5da4f8b7b83f2eb06cefa74f533360d14a07e742c11ac8` |
| MAE initial | `figure.png` | `f7f7eb672fb83292378678d57798a3ca2aa7a48d520660d754be6163e3ae5df9` |
| WMRL revised | `wmrl-method.png` | `6a62544efae57a89afd3ef5ed33805cabbd93bf8c870be32fe2731add4373158` |
| WMRL revised print | `wmrl-method-print.png` | `02cfe73a332858f6ea8a9351d22380e5a92d8cde4a76edf4a7bbd80fb0d20889` |
| SEAL final inspected | `seal-teaser.png` | `16282939ef43478bcc4a04dbae108337fc332d8f09e069d7ab45f213fdeb142e` |
| SEAL final inspected | `seal-method.png` | `bd627ee078f904e4d796a3f7919fa7df936775f355643d10129ca494de239a1a` |
| SEAL final print | `seal-teaser-print.png` | `c0cd209d39dad0393ea28fa4a8d71745de3690063e870f5e4665321cf3b26931` |
| SEAL final print | `seal-method-print.png` | `8aea003cc895bac18e7374e1fa6de788d6cac73210257daddea28fb02b480df9` |

Recorded modification times (UTC): initial SEAL teaser/method 16:53:09.972710 and 16:53:10.576720; MAE 16:56:26.668006; revised WMRL image/print 16:58:33.690061 and 16:58:33.766062; final inspected SEAL teaser/print 16:59:52.447333 and 16:59:52.503334; final inspected SEAL method/print 16:59:53.131344 and 16:59:53.207345.

## Review boundaries

This review evaluated what one independent reader could infer from the rendered images, then checked consistency against the local captions and briefs. It does not certify paper-source accuracy, export internals, accessibility, real model behavior, final venue fit, or every later revision. The source and export checks belong to the root workflow. The findings above distinguish observed repairs from changes reported by another reviewer, and preserve the limitations that remain after the material ambiguities were fixed.
