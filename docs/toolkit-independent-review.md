# Independent scientific and visual review

Reviewed 2026-09-19. Scope: `examples/graphs-lora/lora-tradeoff.png` and `examples/seal-composed/seal-teaser.png`, their fixed-size proofs, SVG/PDF dimensions, source captions/READMEs, and the cited primary papers. The original rendered images were inspected before captions or design plans. No design plan or previous review was used to decide the findings. No figure or implementation was changed.

## First reading from the pixels

**LoRA:** two scatterplots compare accuracy with trainable parameter count. LoRA is near full fine-tuning on WikiSQL and higher on MNLI-matched while using dramatically fewer trainable parameters. Other adaptation methods remain visible, and increasing the LoRA parameter count does not uniformly improve the two task results.

**SEAL:** a passage is rewritten by a language model; the rewrite is used to update parameters; the adapted model is asked a question without the passage. The evidence panel says SEAL narrowly leads the single-passage setting, whereas GPT-4.1-generated data leads both larger settings. The drawing reads as an adaptation pathway, not an explanation of the RL training loop.

## Source fidelity

All eight LoRA settings, both accuracy columns, and trainable parameter counts agree with [LoRA v2, Table 4](https://arxiv.org/pdf/2106.09685v2). The lower WikiSQL value for the smaller LoRA setting is preserved. The paper gives typical task-level fluctuations, not separate uncertainty estimates for these entries; omitting invented error bars is appropriate. Accuracy here means validation accuracy, and WikiSQL specifically uses logical-form accuracy.

All 15 SEAL marks and value labels agree with [Self-Adapting Language Models v2, Table 2](https://arxiv.org/html/2506.10943v2#S4.T2). The model, no-context evaluation, and LoRA versus full-fine-tuning settings are correctly identified. Both unfavorable comparisons remain explicit. Sections 3–4 support the arrow order and the caption's distinction between adaptation and prior RL training. The illustrative passage is marked as constructed; the notebook provenance distinguishes generated illustration from evidence.

## Concrete findings and caveats

| Figure | Observation | Consequence and proportionate response |
|---|---|---|
| SEAL | Panel a says “Fine-tune on self-edit,” without naming the original passage as training input. | Minor standalone semantic omission: the caption correctly says that synthetic-data rows also use the passage, and the primary paper describes this combination. Labeling the box “Fine-tune on passage + self-edit” would make the panel self-contained. This does not invalidate the plotted evidence. |
| LoRA | The MNLI-matched 37.7M LoRA diamond and 40.1M AdapterH cross partly overlap at final size. | Both points exist and their coordinates are correct, but precise identification requires the legend and enlarged view. Retain the real positions; a local label or inset is an optional solution if exact comparison becomes a priority. This is a readability limitation, not a data error. |
| LoRA | The visible metric label is only “Accuracy (%).” | Add validation/logical-form scope in a publication caption or axis description. The source link enables recovery, but a detached figure has incomplete evaluation metadata. |
| SEAL | The headline verb “leads” accompanies a small mean difference without uncertainty. | The caption correctly limits this to highest mean. Keep that wording and avoid claims of statistical significance. No significance assertion is present in the supplied caption. |

No incorrect arrow direction, omitted comparator, fabricated uncertainty, numeric mismatch, clipping, or text collision was found. The SEAL arrows correctly progress from generation to parameter adaptation to no-context questioning. Omitting the outer RL loop is acceptable for this teaser because both the footer and caption identify its role and scope. The constructed question does not include a fabricated measured answer.

## Physical size and readability

PDF page dimensions are 518.4 × 284.4 pt for LoRA (7.2 × 3.95 inches) and 504 × 342 pt for SEAL (7 × 4.75 inches). SVG canvas dimensions agree. Body text is 8 pt at these dimensions, including the imported SEAL chart, rather than a larger source panel subsequently reduced below the declared size.

The LoRA proof is 792 × 435 pixels at about 110 ppi. The SEAL proof is 504 × 342 pixels at about 72 ppi. I inspected both actual proofs as well as the enlarged exports. Labels remain decipherable at their intended two-column widths; the SEAL chart values and footer are the smallest, lowest-emphasis content and should not be reduced further. Color is reinforced by shape or direct labels. The crowded LoRA pair noted above is the only observed mark-separation limitation.

These are screen inspections of physical-size proofs, not a printed-page or manuscript-integration test. No venue template was supplied, so this review does not certify readability after unknown downstream resizing.

## Disposition

The figures communicate their intended scientific comparisons and preserve the reported evidence. No major scientific defect was found. The SEAL adaptation label and LoRA metric scope merit small clarification; the close LoRA markers are a documented precision-reading limitation. Further cosmetic changes are not justified by this review.

## Reinspection after revisions

Reinspected the revised LoRA high-resolution export and print proof, a fresh rasterization of its PDF, and the revised SEAL print and PDF proofs on 2026-09-19. Also read the newly added `examples/graphs-lora/caption.md`.

| Earlier finding | Status after reinspection |
|---|---|
| SEAL adaptation input | Resolved. The box now says “Fine-tune on passage + self-edit” over two lines. Both inputs are explicit, the parameter-update symbols remain readable, and the added line causes no clipping or collision. |
| LoRA nearby MNLI markers | Identification resolved. Separate leader labels name LoRA 37.7M at 91.6 and AdapterH 40.1M at 91.5. The marks remain physically close at their true coordinates, but the labels make both identities and values recoverable at final size. The leaders end at the appropriate points and do not create a false trajectory. |
| LoRA evaluation metadata | Resolved in the accompanying caption. It explicitly identifies validation results, WikiSQL logical-form accuracy, and MNLI-matched classification accuracy. It also distinguishes trainable parameter count from compute or latency. The caption should accompany the figure when reused. |
| SEAL interpretation of small mean differences | Remains a stated evidence limitation, not a defect. The caption restricts the ranking to reported means; the figure still discloses the absence of uncertainty. |

No new clipping, label collision, arrow ambiguity, or altered quantitative meaning was observed in the revised pixels. The original physical sizes and minimum-text constraints remain applicable. The actionable clarification findings are resolved; unknown downstream resizing and manuscript integration remain outside this review.
