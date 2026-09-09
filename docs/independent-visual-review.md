# Independent redraw review

Reviewer: visual_research subagent. Initial review: 2026-09-09. This records the first PNG versions displayed during the review; root and the renderer agent were actively revising them. No figure specifications or renderer code were modified by this reviewer.

Reviewed actual pixels of:
- examples/mae-teaser/figure.png
- examples/mae-method/figure.png
- examples/transformer-teaser/figure.png
- examples/transformer-method/figure.png

Also read each figure.json and figure.qa.json and inspected both method .drawio XML exports. Sources: [MAE Figure 1, Section 3, Tables 1–2](https://arxiv.org/pdf/2111.06377) and [Transformer Figure 1, Section 3, Table 2](https://arxiv.org/pdf/1706.03762v7). This is a scientific and visual review, not a usability experiment with human readers.

## Initial disposition

**Not yet ready for release.** The scientific values are correct, but clipping, panel collisions and two misleading architecture routes/groups remain. Empty machine-QA error arrays do not resolve these issues; the QA reports appropriately acknowledge their limited scope.

## MAE teaser

Correct:
- Exactly four of sixteen patch cells are selected, matching the 25% visible fraction.
- Values correspond to Table 2: 84.2/42.4, 84.9/15.4, 84.8/11.6.
- The 63.7% time reduction and +0.7 percentage-point callout correctly compare the two 8-block-decoder rows.
- Scope includes architecture, dataset, training duration and TPU count. The bottom note identifies this as an ablation.

Blocking:
1. **Time axis lacks tick labels entirely.** A plot of cost against quality cannot be decoded if the reader cannot recover cost. Show readable ticks, or annotate all three exact times; prefer both.
2. **The baseline label is cut off at the right edge.** In the displayed PNG only “Encoder with” remains, hiding the defining mask-token difference. Anchor the label to the left of the point or wrap inside the panel.
3. **The vertical accuracy label sits over the divider.** Reserve chart-axis padding inside the evidence region; do not borrow the conceptual panel's space.

Improve:
- The cartoon does not actually show reconstruction: it ends in four blank tokens followed by prose. A small reconstructed patch grid or a visibly marked lightweight decoder would complete the visual explanation while retaining the evidence allocation.
- Make the 63.7% headline readable near the compared points or in a compact data-linked callout; it is currently only a small footer.
- Explicitly label “encoder with mask tokens; 8-block decoder” so all comparison conditions can be recovered from the plot.
- The existing 7-inch / 8.5-point design is for a full-width paper figure. Reducing it to one column would make labels too small.

## MAE method

Correct:
- Pre-training and recognition are separated.
- The proposed encoder sees visible patches only.
- Mask tokens enter after the encoder, and the decoder is removed for recognition.
- The footer accurately discloses omitted projections and positions and states masked-only loss.

Blocking:
1. **The masked-target bypass crosses through the Mask tokens node.** Because the path is occluded behind the box and reappears as an arrow into MSE loss, it looks as if mask-token embeddings are the loss target. Route the original-image target line below the node and into the loss, with an unambiguous arrowhead.

Improve:
- Use a label such as “MSE on masked patches” directly in the loss node; the loss domain should not rely only on a footer.
- Consider “fine-tuned encoder” or “initialized from pretraining” in the recognition branch. “Pretrained weights” beneath “recognition after fine-tuning” can imply the weights were not updated.
- A subtle weight-transfer annotation between the two encoders would make reuse explicit. It must be a parameter-transfer cue, not a forward tensor edge.
- The main operation chain is easy to follow, but the generic “Pixels” node could read “Predicted patches” to make the loss operands clearer.

## Transformer teaser

Correct:
- All eight reported EN–DE values match Table 2.
- Ensemble entries are explicitly labeled.
- The unmeasured example is described as illustrative connectivity.
- The note correctly avoids an equal-compute claim.

Blocking:
1. **Method labels from the right plot spill over the conceptual panel.** “GNMT + RL (ensemble)” crosses the Self-attention box, and several other y-axis labels sit left of the separator. Reserve a distinct label column entirely inside the evidence region, wrap labels, or use a plot layout that places labels inside that panel.
2. The collision makes both the algorithm and benchmark unreadable, so shrinking fonts alone is not an acceptable fix.

Improve:
- Three tokens converging into one box looks like sequence pooling. Preserve an output token per input (or a short three-token output row) to illustrate contextualization.
- Add one derived, baseline-named outcome such as “+2.37 BLEU vs MoE” if the teaser is meant to communicate the advantage immediately. Do not express BLEU as accuracy percentage.
- A source/translation pair would support the translation task more directly than “The cat sat” alone, but the existing schematic is acceptable if explicitly framed as encoder context sharing.

## Transformer method

Correct:
- Cross-attention receives keys and values from the encoder and queries from the masked decoder path.
- Target input is shifted right, and output goes through linear projection and softmax.
- The caption states that the drawing is a macro schematic with residual wiring, dropout and feedback omitted.

Blocking:
1. **The “ENCODER STACK × N” group encloses embedding/position addition.** That operation is not repeated at each encoder layer.
2. **The “DECODER STACK × N” group encloses target inputs, embeddings, output linear/softmax and next-token output.** Those operations are not repeated inside every decoder block. Draw the repeat container only around masked self-attention, cross-attention and FFN; move one-time I/O outside it, or rename the broad region and add a separate repeat marker.

Improve:
- State the original ordering explicitly: residual addition followed by LayerNorm after each sublayer. The current subtitle says only “normalization” and could describe modern pre-norm implementations.
- Label attention as multi-head; this is part of the 2017 method, even at macro level.
- For the canonical model, N=6 is available from the source. If N remains symbolic, say why.
- The left/right stacks are structurally easy to identify, but the decoder traversal turns upward, rightward, then downward. It remains understandable at current size; avoid further branching without a layout change.

## Caption and evidence completeness

The raster/PDF footer is a short explanatory note, not a full paper caption. The figures identify “Table 2” but do not name the source paper/authors or provide a citation key. A publication-ready delivery should include a companion caption with:
- a concise takeaway and panel descriptions;
- exact source table and paper citation;
- dataset, split, metric direction and compute scope;
- acknowledgment that plots redraw published values and the cartoon is illustrative;
- no invented uncertainty bars where the source does not report per-entry dispersion.

Do not place long provenance URLs inside an already crowded figure. Keep full citation text in the manuscript caption and machine-readable evidence file.

## diagrams.net fidelity review

The inspected method exports contain editable vertices, edges, labels and page text rather than a single embedded raster. This is a good starting point. XML inspection alone does **not** establish rendering parity with diagrams.net.

Verified in XML:
- scientific node and edge labels are present;
- actual line breaks are serialized as XML newlines;
- edge sources and targets are explicit;
- patch tiles and group backgrounds are editable objects.

Remaining checks for an actual diagrams.net render:
- Explicit waypoint geometry must retain the routed target bypass; source/target relationships alone will not prevent crossing the Mask tokens box.
- Compare font size and line wrapping in a diagrams.net export at the same physical page width.
- Group backgrounds should use the same light border as the PDF, and title/bold emphasis should remain consistent.
- Conceptual group membership is currently visual: nodes are siblings under the root layer rather than children of group containers. Dragging the background may not move its contents. Do not promise fully functional grouping unless that behavior is implemented.
- Captions and page text need the same bounds and clipping checks as nodes.

## Re-review pending

Root will signal updated renders. The second review should explicitly mark each blocking issue resolved or still present and inspect the new PNG pixels again. No final quality score is assigned at this stage.



## Post-repair review: MAE and Transformer

A second actual-pixel inspection of the four updated PNGs was completed on 2026-09-09.

| Initial blocker | Updated observation | Result |
|---|---|---|
| MAE teaser missing time ticks | Readable 5–45 hour ticks now appear. | Resolved |
| MAE teaser baseline text clipped | Complete “Encoder with mask tokens” label now fits left of the point. | Resolved |
| MAE teaser vertical label on divider | Accuracy label and tick labels have their own chart margin. | Resolved |
| Transformer teaser method labels over concept | All method names now remain right of the divider. | Resolved |
| MAE method targets routed through Mask tokens | Dashed target path now goes below that box and turns directly into MSE loss. | Resolved |
| Transformer repeated groups included one-time operations | Encoder/decoder groups now enclose only repeated attention/FFN operations; embeddings and prediction head are outside. | Resolved |

**Disposition for these four updated renders: pass for the declared schematic scope, conditional on adding the complete companion captions already planned by root.** No new blocking pixel or source-semantic defect was found.

Specific improvements are visible: the Transformer subtitle now explicitly gives the original post-norm equation; the MAE note explains dashed supervision edges; and both chart panels can be read without interference from the conceptual panels.

Remaining nonblocking design opportunities:
- The MAE teaser still explains reconstruction mostly in words instead of showing a reconstructed grid.
- The Transformer teaser still has a single output arrow under attention; the text correctly says context for each token, but multiple output tokens would communicate that more directly.
- Attention can be labeled “multi-head” and N can be set to 6 in the canonical Transformer caption.
- MAE recognition could label its encoder “fine-tuned from pretrained weights.”
These are refinements, not reasons to reopen the repaired layout gate.

The export is designed at full paper width (7 inches); passing this review does not authorize shrinking the same artwork to one column. diagrams.net rendering parity and functional group dragging remain unverified by this reviewer.

## LoRA independent pixels-first assessment

The first LoRA teaser and method PNGs were inspected before reading their source specifications or implementation. The reviewer had previously audited the LoRA paper, so this is **blind to the implementation**, not a blinded first-time-user study or a comprehension timing experiment.

From the teaser pixels alone, the following were recoverable:
- **Task:** adapt a language model to downstream work, illustrated by an NL-to-SQL example.
- **Proposal:** leave W0 frozen and learn two smaller matrices B and A whose product supplies the weight update.
- **Evidence:** eight GPT-3 adaptation settings, parameter counts in millions, and separate WikiSQL/MNLI-m validation-accuracy axes.
- **Qualified result:** 4.7M LoRA is 0.4 percentage points lower on WikiSQL and 2.2 percentage points higher on MNLI-m than full fine-tuning. The proposed method is not presented as winning every metric.

From the method pixels alone:
- Input x branches through W0 and A→B→alpha/r.
- W0 is frozen; A has Gaussian initialization and B zero initialization.
- A maps from k to r, B from r to d.
- The branches combine to output h.
- Deployment merges W0+sBA once, leaving one dense projection.

These statements match the source audit of LoRA Section 4 and Table 4. No source value or shape error was found. The initial merge node was a blank circle, however, so addition was supplied by the nearby equation rather than the diagram itself.

Initial LoRA pixel defects sent to its author:
1. “Method” and “Trained (M)” column headings overlap in the teaser.
2. The method merge circle lacks the essential plus sign.
3. The B initialization label is too close to the task-loss sentence.

The author has acknowledged the defects and is regenerating the affected regions. A focused recheck will follow; the remaining layout does not need repeated review absent further changes.


### LoRA v3 focused recheck

Actually viewed the updated `lora-teaser-print.png` and `lora-method-print.png` on 2026-09-09. The Method / Trainable (M) headings are now separated, the addition node contains a visible plus sign, and the B initialization label no longer crowds the task-loss sentence. Task, trainable/frozen states, A→B→scaling order, and merged inference remain readable at the provided print-preview scale.

**LoRA disposition: pass; no remaining blocker from this reviewer.** The displayed negative WikiSQL and positive MNLI-m differences are especially useful: the figure communicates the actual trade-off rather than forcing a uniform superiority claim. The author separately reports inspecting full-size PNG, PDF raster and grayscale; those separate inspections are the author's evidence, not additional inspections claimed by this reviewer.
