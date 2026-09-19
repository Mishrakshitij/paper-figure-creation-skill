# Figure pattern atlas

This is a design reference, not a ranking of papers. Twenty author-hosted visual assets were actually displayed and inspected on 2026-09-09; paper captions and method text were cross-checked where accessible. A repository illustration can differ from its published counterpart. No original paper figures are bundled. These observations do not establish a statistically representative survey of AI figures.

## Choose the visual argument before choosing the style

| Reader's question | Useful composition | Source-grounded example | What to preserve |
|---|---|---|---|
| What bottleneck changes, and does it matter? | Problem → intervention beside measured result | [FlashAttention Fig. 1, PDF p. 2](https://arxiv.org/pdf/2205.14135v2) | Memory movement is the mechanism; the chart measures attention computation, not whole-model training. |
| How does an unfamiliar input become model tokens? | Concrete specimen → transformed representation → module, with one expanded block | [ViT Fig. 1, PDF p. 3](https://arxiv.org/pdf/2010.11929) | Keep the image-to-patches correspondence, class token, positional addition, and encoder inset. |
| How do existing modules support a new capability? | Frozen backbone + highlighted trainable bridge + concrete output | [BLIP-2 Fig. 1, PDF p. 1](https://arxiv.org/pdf/2301.12597v3) | Frozen-state symbols, two training stages, and a short input/output example. |
| Is the benefit an efficiency–quality trade-off? | Log-cost scatter or small multiples; direct labels | [LoRA Fig. 2 / Table 4, PDF p. 8](https://arxiv.org/pdf/2106.09685v2) | Trainable parameter count, evaluation split, actual variants, and results that do not improve. |
| Does appearance improve while speed changes? | Matched visual crops + quantitative trade-off | [3D Gaussian Splatting Fig. 1 and Table 1](https://arxiv.org/html/2308.04079v1) | Identical views and crops; distinguish a single scene's teaser values from dataset averages. |
| What persists over time? | One step shown clearly + named memory feedback | [SAM 2 Fig. 3](https://arxiv.org/html/2408.00714v2) | Memory carries past predictions and image features; a loop alone is insufficient. |

The requested 30–40% conceptual / 60–70% evidence split is a starting layout constraint for a hybrid teaser, not an empirical law inferred from these papers. FlashAttention provides a real hybrid example but does not itself follow that exact ratio. Use the ratio when the paper has enough comparable evidence; do not manufacture graphs to fill space.

## Actually inspected visual assets and critical lessons

Every asset link points to an author or official research repository. The figure locator describes the publication relationship, not an assertion that the raster is pixel-identical to the PDF.

| Paper / inspected asset | Publication relationship | Transferable design move | Limitation or adaptation |
|---|---|---|---|
| [DETR](https://github.com/facebookresearch/detr/blob/HEAD/.github/DETR.png) | Fig. 1, PDF p. 2 | Repeated gull image makes predicted-to-target matching tangible. | Mark matching as training-only; unmatched queries predict no-object. |
| [ViT](https://github.com/google-research/vision_transformer/blob/HEAD/vit_figure.png) | Fig. 1, PDF p. 3 | Picture patches retain their identity through tokenization; detail lives in an inset. | Many parallel arrows become clutter at column width. |
| [SAM](https://github.com/facebookresearch/segment-anything/blob/HEAD/assets/model_diagram.png) | Fig. 4; [caption](https://arxiv.org/html/2304.02643v1) verified | Large encoder, small prompt/decoder blocks, multiple scissors masks convey amortization and ambiguity. | Area suggests qualitative size, not a calibrated FLOPs ratio; text-prompt support must match the actual implementation being drawn. |
| [Latent Diffusion](https://github.com/CompVis/latent-diffusion/blob/HEAD/assets/modelfigure.png) | Fig. 3; [method](https://arxiv.org/html/2112.10752v2) verified | Nested pixel, latent, and conditioning regions explain where computation occurs. | Dense legend and tiny Q/K/V marks need enlargement or a separate inset. |
| [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting/blob/HEAD/assets/teaser.png) | Fig. 1 related bicycle comparison | Matched crops expose thin-structure quality alongside speed and training cost. | One scene is not aggregate evidence; two proposed settings trade quality against speed. |
| [Mamba](https://github.com/state-spaces/mamba/blob/HEAD/assets/selection.png) | Fig. 1, PDF p. 3 | Orange state streams and blue input-dependent selection reveal two interacting mechanisms. | State replication and channel count are schematic; label dimensions if used quantitatively. |
| [ControlNet](https://github.com/lllyasviel/ControlNet/blob/HEAD/github_page/sd.png) | Fig. 3; [caption](https://arxiv.org/html/2302.05543v3) verified | Gray locked blocks contrast with a blue trainable copy and zero-convolution links. | Long bypasses can disappear after reduction; label additive links and training state explicitly. |
| [Swin Transformer](https://github.com/microsoft/Swin-Transformer/blob/HEAD/figures/teaser.png) | Repository composite of hierarchy, shifted windows, blocks and stages | Spatial windows make cross-window communication concrete. | Composite contains several abstraction levels; separate overview and mechanism when small. |
| [CLIP](https://github.com/openai/CLIP/blob/HEAD/CLIP.png) | Rearranged Fig. 1 content, PDF p. 2 | Training pairing matrix and zero-shot label prompts share modality colors. | Keep training separate from deployment; matrix cells are similarities, not measured task accuracies. |
| [DDPM](https://github.com/hojonathanho/diffusion/blob/HEAD/resources/samples.png) | Repository sample montage; related to paper sample figures | Diverse image domains immediately communicate generative capability. | A montage alone provides neither algorithm semantics nor comparative evidence; do not imply cherry-picked examples are a distributional test. |
| [FlashAttention](https://github.com/Dao-AILab/flash-attention/blob/HEAD/assets/flashattn_banner.jpg) | Fig. 1, PDF p. 2 | Bottleneck diagram, tiling computation, and time decomposition form a compact causal story. | Hardware figures are version-specific; 7.6× concerns the reported attention benchmark. Never estimate exact component timings by eye. |
| [NeRF](https://github.com/bmild/nerf/blob/HEAD/imgs/pipeline.jpg) | Fig. 2, PDF p. 5 | The same two rays connect coordinate samples, network output, integration, and rendering loss. | Density depends on position; view direction conditions color. A generic joint-output box can hide this distinction. |
| [MLP-Mixer](https://github.com/google-research/vision_transformer/blob/HEAD/mixer_figure.png) | Fig. 1, PDF p. 2 | Matrix transposition visibly distinguishes token mixing from channel mixing. | Colors encode tensor organization; do not reuse them for unrelated module classes in the same figure. |
| [LoRA](https://github.com/microsoft/LoRA/blob/HEAD/examples/NLG/figures/LoRA_GPT3.PNG) | Earlier Fig. 2 variant; v2 PDF p. 8 adds Adapter(H) | Two aligned cost–accuracy plots expose efficiency across orders of magnitude. | Repository raster and latest PDF differ. Use source table values, not old curve interpolation; include missing baselines when appropriate. |
| [LLaVA](https://github.com/llava-vl/llava-vl.github.io/blob/HEAD/images/llava_arch.png) | Fig. 1, PDF p. 4 | Small projection bridge connects visual tokens to the language token stream. | The fan of token arrows becomes hairline clutter; compress it without suggesting bidirectional generation. |
| [BLIP-2](https://github.com/salesforce/LAVIS/blob/HEAD/projects/blip2/blip2_illustration.png) | Fig. 1, PDF p. 1 | Frozen towers, central query bridge, staged labels, and one example state the proposal. | Explain snowflakes in words; lengthy example text competes with the method. |
| [InstructBLIP](https://github.com/salesforce/LAVIS/blob/HEAD/projects/instructblip/comparison.png) | Fig. 5 variant, PDF p. 13 | Shared image/question and aligned response rows permit direct qualitative comparison. | Long prose is slow to scan; quote only the diagnostic spans, preserving meaning and selection provenance. |
| [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada-pytorch/blob/HEAD/docs/stylegan2-ada-training-curves.png) | Repository training benchmark; exact paper-figure match not established | Dataset/resolution small multiples keep GPU-count colors consistent and retain visible instability. | Axis ranges differ; identify each panel's scale. Do not smooth away spikes or equate unequal hardware budgets. |
| [EDM](https://github.com/NVlabs/edm/blob/HEAD/docs/teaser-1280x640.jpg) | Repository mathematical teaser; exact paper-figure match not established | A zoom inset connects local trajectory behavior with global sampling geometry. | Unlabeled density color and technical axes are insufficient for a lay teaser; add a plain-language explanation. |
| [SAM 2](https://github.com/facebookresearch/sam2/blob/HEAD/assets/model_diagram.png) | Fig. 3; [caption](https://arxiv.org/html/2408.00714v2) verified | Faded temporal copies and routed memory loops communicate streaming reuse. | Caption explicitly notes an omitted image-embedding input to the memory encoder; restore it when the task demands architectural completeness. |

## Apply the lessons

1. **Carry one example through the diagram.** Reuse the same image patch, sentence, object, ray or retrieval query at each relevant stage. Consistent identity reduces narration.
2. **Expose the intervention.** Highlight the changed connection or operation, not every module. Distinguish inherited, frozen, trainable, and training-only components with text plus style.
3. **Separate the overview from the mechanism.** One expanded block is usually enough. Put tensor dimensions at transformations, not on every decorative edge.
4. **Make the empirical claim local.** Attach dataset, split, unit, baseline and compute condition to the chart. Keep qualitative examples visibly separate from numerical measurements.
5. **Prefer trade-off honesty to a forced victory.** A proposed method can improve cost while losing slightly on one quality metric. LoRA and 3DGS are useful tests for this failure mode.
6. **Inspect the exported artifact on white and at final print size.** Several official transparent PNGs became difficult to read on a dark viewer background. Export an explicit white background unless transparency is required.
7. **Distinguish illustration from evidence.** Rays, masked-patch cartoons, example reconstructions and density sketches explain mechanisms. They do not count as new experimental results.

Additional text-only checks covered Transformer Fig. 1 / Table 2, ResNet Table 6, U-Net Fig. 1, and MAE Fig. 1 / Tables 1–2. Their original figure pixels were not inspected in this review. Exact transcription fixtures and caveats are maintained in the repository research records.

