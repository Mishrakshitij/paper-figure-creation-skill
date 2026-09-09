# Research basis for AI paper figure creation

The research supports a practical design skill with two outputs: an evidence-heavy introduction teaser and a faithful method diagram. It combines broad automated paper screening, a smaller set of caption interpretations, close visual study, primary design/tool guidance, and original redraw tests.

## Coverage

| Evidence layer | Actual coverage | What it establishes |
| --- | ---: | --- |
| Proceedings corpus | 500 papers | Bibliographic candidates from official proceedings |
| PDF text retrieval | 480 papers | Readable bounded PDF text windows |
| Automated caption candidates | 443 papers; 1,068 passages | Candidate figure numbers/pages and caption keywords; extraction can be noisy |
| Analyst caption interpretation | 40 papers | Original notes on the described figure's semantic purpose |
| Close visual study | 20 papers' official repository assets | Actual inspected pixels; some assets are repository versions or supplements |
| Additional curated text-only study | 4 papers | Method/caption understanding without claiming pixel review |
| Verified redraw datasets | 5 cases | Source-located experimental values and scientific caveats |
| Completed original redraws | 6 figures across 3 papers | Executed examples of both figure types, with review and repair |

Counts describe different evidence levels and can overlap; they should not be summed as distinct papers. This is **not a 500-paper visual review or an objective ranking of the best figures**. The broad corpus is a convenience sample with author-order and access bias. The curated set was chosen for useful and diverse representational patterns, not a validated quality score.

The broad sample contains 100 papers each from [ICML 2021](https://proceedings.mlr.press/v139/), [ICML 2022](https://proceedings.mlr.press/v162/), [ICML 2023](https://proceedings.mlr.press/v202/), [ECCV 2024](https://www.ecva.net/papers.php), and [NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023). The [coverage manifest](coverage.json) records retrieval counts by stratum, and the [methodology](corpus-methodology.md) explains selection and failure states. Neither venue acceptance nor a popular paper automatically implies a good figure.

## Findings that changed the skill

**Represent the scientific object.** The strongest inspected examples use a representation that carries meaning: camera rays and field samples for NeRF, a patch sequence for ViT, low-rank factors for LoRA, or memory levels for FlashAttention. A generic module box can organize the flow but cannot alone reveal the contribution. The [pattern atlas](../skills/paper-figure-creation/references/pattern-atlas.md) records exact inspected assets, their relation to each paper, and the resulting design lesson.

**Connect concept and evidence through the same change.** A teaser is coherent when the example explains the intervention measured by its plot. FlashAttention's inspected asset is a particularly relevant hybrid of bottleneck, proposed operation and runtime evidence. This motivated a concept-plus-evidence layout route, not a requirement that every paper imitate its composition. The roughly 35:65 allocation is an editorial preference for this skill, not a measured literature optimum. [FlashAttention paper](https://arxiv.org/abs/2205.14135).

**Preserve trade-offs visibly.** Published results do not always support a single winner. The verified LoRA table includes a smaller variant that is below full fine-tuning on WikiSQL while above it on MNLI-m. The verified 3D Gaussian Splatting case has mixed quality metrics and different hardware conditions. This motivated typed metric direction, exact comparison scope, both-axis provenance, and explicit negative results in the redraws. [LoRA](https://arxiv.org/abs/2106.09685), [3D Gaussian Splatting](https://arxiv.org/abs/2308.04079).

**Separate stages and parameter state.** Diagrams become misleading when pretraining-only modules appear in inference or frozen components appear to be updated. The skill therefore asks for a node/edge contract, named merge operations, repetition scope, and training/inference separation before geometry. Close visual examples such as ControlNet and the MAE redraw motivated those distinctions. [ControlNet](https://arxiv.org/abs/2302.05543), [MAE](https://arxiv.org/abs/2111.06377).

**Use actual physical dimensions.** Publication legibility is a property of the exported page at its intended width. Design defaults cannot substitute for a venue template: CVPR's figure guidance and Nature's specifications differ. The skill separates editable geometry and font tokens from venue-specific checks. [CVPR formatting source](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex), [Nature specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/).

**Keep the data authoritative and the diagram editable.** Plotting code should own numerical marks. Native diagrams.net cells can own editable mechanism geometry, while SVG and PDF provide publication export. Mural is useful for story planning and review snapshots; it should not become an independent store of hand-adjusted experimental values. [draw.io generation](https://www.drawio.com/docs/reference/diagram-generation/), [Mural export](https://learn.mural.co/lessons/export-murals).

**Review can improve the reusable machinery.** Actual redraw inspection found failures in gutters, tick handling, routing, grouping and label layering. Fixes were incorporated into the renderer or the instructions only when a concrete failure justified them. The [evaluation report](../docs/evaluation.md) separates executed checks from proposed future benchmarks. A few successful examples do not establish general superiority or a numerical gain in visual quality.

## Audit files

- [corpus-500.jsonl](corpus-500.jsonl) and [CSV](corpus-500.csv): canonical paper URLs, evidence levels and short excerpts, at most 22 words per paper.
- [caption-design-notes.json](caption-design-notes.json): 40 caption interpretations, with stated limits on visual inference.
- [visual-review-ledger.json](visual-review-ledger.json): 20 actual visual asset reviews and explicit exclusions.
- [verified-fixtures.json](verified-fixtures.json): five source-grounded datasets and method semantics.
- [skill-repository-lessons.md](skill-repository-lessons.md): supplied repository analysis and inspected file identifiers.
- [screen_corpus.py](screen_corpus.py): reproducible local PDF/caption harvesting using canonical URLs; requires PyMuPDF and ordinary network access. Keep downloaded PDFs outside the published repository. It does not perform visual review or rank figure quality.

Original PDFs, full paper text and original figure images are not redistributed. Author/source links make the evidence inspectable. Further work can improve representativeness, enlarge the close visual sample and run a matched, blinded baseline comparison across agents; those studies have not been completed here.
