# LoRA figure brief

Request: create an introduction teaser and a method diagram for LoRA from the original paper, with roughly one-third concept and two-thirds experimental evidence; preserve fair comparisons and editable publication figures.

Reader: AI research audience. Assumed slot: two columns, 7 inches wide. No manuscript template was supplied; these are reviewed publication-scale drafts, not venue-certified submissions.

Argument: learning low-rank updates to frozen language-model weights reduces the number of trained parameters while retaining strong, task-dependent validation performance in the reported GPT-3 experiments.

Teaser scope: the full eight-row GPT-3 comparison set in Table 4, for WikiSQL logical-form validation accuracy and MNLI-matched validation accuracy. Both tasks use percentages, with separate labeled scales. Include every method and both AdapterH/LoRA budgets. Preserve LoRA 4.7M's lower WikiSQL value than full fine-tuning. SAMSum is excluded from the small figure because adding a third distinct metric would reduce legibility; its complete Table 4 values remain in the data ledger. No additional methods, sweeps, combined LoRA-prefix methods, or new experiments are implied by this defined scope.

Example: question 'How many teams?' and SQL target 'SELECT COUNT(*) FROM teams'. This is an author-created schematic explaining NL-to-SQL, not an observed model prediction or a dataset sample. It is labeled as schematic and has no quantitative evidentiary role.

Composition alternatives before rendering:

1. Teaser A: concept at left (about 33%); method names and parameter counts plus aligned WikiSQL/MNLI dot plots at right (about 67%). Reading order is task, low-rank update, all comparisons. Each row directly identifies its budget. Selected because there are eight results, including two budgets for two methods.
2. Teaser B: concept at left (about 33%); two quality-versus-trainable-parameter scatterplots at right. This makes the cost-quality relationship spatial, but the seven small-budget points cluster within two orders of magnitude while full fine-tuning sits five orders away; a multi-family legend and point labels would compete with the available width. Retained as a storyboard only.
3. Method A: training residual branch above, merged inference below. Both lanes share x, h, W0, A, B, and scale s. Selected: the explicit sum exposes the proposed computation and the inference lane makes the merge concrete.
4. Method B: one residual branch with a side note 'merge for inference'. This is more compact but makes the inference graph less reconstructable. Retained as a storyboard only.

Canonical source: figure JSON files plus build_figures.py. SVG exports retain editable text/geometry but are editorial exports; edits to these exports must be migrated to the canonical source before rerendering.

Method contract:

| Object | Meaning and state |
| --- | --- |
| x | Input hidden vector, k dimensions, supplied to both branches |
| W0 | Pretrained d-by-k projection, frozen; still participates in the forward/backward computation |
| A | Trainable r-by-k matrix, Gaussian initialization |
| z = Ax | Rank-r intermediate |
| B | Trainable d-by-r matrix, zero initialization |
| s = alpha/r | Fixed scale on low-rank branch |
| Sum | Coordinate-wise W0x + s B(Ax), output h of dimension d |
| Loss | Conditional language-model objective downstream; only adapter factors are updated in this simplified weight-only view |
| Inference | Wmerged = W0 + s BA; compute h = Wmerged x, no separate LoRA branch |

This is one adapted projection, not an entire Transformer. The original experiments concentrate on attention projections; the pair does not assert a single universal rank/projection setting for Table 4. Biases, LayerNorm, attention, repeated layers, and the complete task head are omitted. Rank matrices represent symbolic dimensions, not measured matrix entries. Initialization and the scaling factor are retained.

Unresolved assumptions: actual venue width/font rules, final manuscript insertion, and whether task-specific LoRA configurations should be expanded beyond the simplified one-projection view. The paper reports task-level typical SD rather than entry-specific intervals for Table 4; the chart will not fabricate error bars or imply significance.
