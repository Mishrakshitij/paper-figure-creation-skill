# Brief and representation contract

**Slot:** Method-section figure for MAE pretraining, 7 inches wide × 4.15 inches high. Main labels use at least 8.5 pt; persistent patch identities use 7.3–8 pt. No target manuscript or venue template was provided.

**Reader takeaway:** The encoder processes only four visible patches; the lightweight decoder receives all sixteen restored positions, and the training loss scores only the twelve masked positions.

**Rendering question:** Can a recognizable, rich input scene and restrained depth make patch content and identity more immediate while retaining exact scientific structure? This is a qualitative one-paper experiment, not a performance or preference benchmark.

## Scientific sources

- [He et al., Masked Autoencoders Are Scalable Vision Learners, Section 3 and Figure 1, v3](https://arxiv.org/pdf/2111.06377v3).
- [Official `models_mae.py`](https://github.com/facebookresearch/mae/blob/main/models_mae.py), implementation previously inspected for the vector example; recorded blob SHA `880e28f8225fa9b56d7ba2963c2cb2c9d6f3d896`.
- The earlier [MAE source brief](../mae-v2/brief.md) records patch projection, encoder position embeddings, masking, decoder projection, shared mask tokens, unshuffling, decoder positions, pixel prediction and masked-only MSE. The hybrid example changes depiction, not these operations.

## Asset provenance

- `assets/fox-input.jpg` is an AI-generated illustrative photograph of a fox in a mountain meadow. It was generated for this example on 2026-09-17, then downsampled/encoded to 600 × 600 JPEG by the parent authoring workflow.
- SHA-256: `5296a3fbe52c8d6b9aae87a9c39bd3114e65d236b276271895d2e7ca8f866fd5`.
- The generation prompt is committed in `assets/generation-prompt.txt`.
- The same committed pixel array supplies the full input, visible input, packed patches and original target branch. Each 4 × 4 cell is a 150 × 150 crop. Source IDs are row-major; retained IDs are 2, 6, 11 and 15; the packed sequence is 11, 2, 15, 6.
- No generated reconstruction or target image is introduced. The source is not an empirical sample; image generation is nondeterministic, while rebuilding from the committed asset is deterministic in data and geometry.

## Representation contract

| Object | Mark | Meaning and limit |
| --- | --- | --- |
| Original image | Generated fox scene with a 4 × 4 grid | A recognizable synthetic teaching input; not a dataset example |
| Visible input patches | Four literal crops, teal borders and persistent IDs | Same pixels and IDs in full, masked and packed views |
| Removed input patches | Opaque warm tiles with diagonal strokes | Content withheld from the encoder; the hidden photograph is not visible through the tiles |
| Packed sequence | Four separate crop tiles in order 11, 2, 15, 6 | Patch content after packing; patch embedding is abstracted, and `+ pos.` denotes original encoder position information |
| Encoder | Larger teal stack | Visible-only computation; depicted layer count is schematic |
| Visible latents | Four blue cells with original patch IDs | Learned decoder-input representations after projection, not image pixels |
| Mask latents | Twelve warm cells with diagonal strokes | Copies of one shared learned mask token; position IDs do not indicate separate mask-token parameters |
| Restoration | Explicit 4 × 4 latent grid | Original spatial order after unshuffling; decoder position embeddings follow restoration |
| Decoder | Smaller warm stack | Lightweight decoder; depicted layer count is schematic |
| Pixel predictions | Sixteen symbolic slots | Predictions exist for all positions; no predicted image is supplied or implied |
| Scored positions | Twelve warm outlined prediction slots with solid corner marks | Only the positions masked at input contribute to the loss |
| Original targets | Same source crops at masked positions, visible positions blanked | Ground-truth pixel content used in the training-only supervision branch |
| Loss | MSE fed by predictions and original targets | Masked-only training objective; no fabricated score or model output |

Projection layers and the CLS token are omitted. The packed tokens already contain encoder position information; the decoder receives projected visible latents and shared mask-token copies. Image tiles encode semantic content rather than literal embedding dimensions.

## Composition decision

Three rough sketches were rendered before the detailed figure:

1. **Staggered image example and expanded restoration — selected.** Gives the image and mask an immediately recognizable relationship while the restored 16-position grid is large enough to inspect. The training-only target branch fits beneath the decoder.
2. **Straight six-stage strip.** Simple reading direction, but the example images and restored identities become small at seven inches.
3. **Large central image with split encoding/scoring lanes.** Gives the image the most area, but makes restoration less prominent and encourages the reader to compare lanes instead of following pretraining.

The depth effect is restricted to stacks and separated tokens. Shadows do not encode a metric, an additional module or literal layer count.
