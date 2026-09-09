# Captions

**Introduction teaser.** LoRA learns low-rank updates to frozen language-model weights. The NL-to-SQL example is schematic. Right: all eight GPT-3 method/parameter settings in Table 4 of Hu et al., arXiv:2106.09685v2, for WikiSQL logical-form and MNLI-matched validation accuracy; parameter counts are millions. Training uses two epochs and batch size 128, with method-specific learning-rate tuning and best-validation selection. The two axes have separate ranges. The paper gives typical seed SD (approximately 0.5 and 0.1 percentage points), not entry-specific intervals; no significance claim is made. At 4.7M trainable parameters, LoRA is 0.4 points below full fine-tuning on WikiSQL and 2.2 points above on MNLI-m.

**Method.** One LoRA-adapted projection during training and merged inference, redrawn from Sections 4.1–4.2 of Hu et al. Both branches receive the same hidden vector. Only the low-rank factors A and B are trained; their scaled output is added to the frozen projection. Gaussian A and zero B initialize the update to zero. The conditional language-model loss is applied downstream; other Transformer computation is omitted. For a fixed task, the scaled update can be merged into the dense weight. Symbolic grids denote matrix shapes, not measured entries.

Source: [LoRA: Low-Rank Adaptation of Large Language Models, v2](https://arxiv.org/pdf/2106.09685v2).

# Alternative text

Teaser: A symbolic frozen matrix plus two thin trainable matrices explains LoRA, beside an illustrative question-to-SQL pair. Eight aligned rows compare trainable parameter counts and validation accuracy for full fine-tuning, BitFit, two prefix variants, two AdapterH budgets, and two LoRA budgets. LoRA points are diamonds and highlighted rows; other methods use open circles. The 4.7M LoRA row reports 73.4% WikiSQL and 91.7% MNLI-m, while full fine-tuning reports 73.8% and 89.5% with 175255.8M trainable parameters.

Method: Input x splits into a frozen W0 projection and a trainable A then B low-rank branch. The latter is multiplied by alpha/r; both paths meet at a plus sign to form h. A has r-by-k dimensions, B has d-by-r dimensions, and W0 has d-by-k dimensions. A starts Gaussian and B starts zero. An inference lane uses the merged weight W0 plus the scaled BA product between x and h.
