# Figure brief and representation contract

**Reader and slot:** AI-paper method section, assumed two-column width of 7 inches and height 3.95 inches. No target manuscript or venue template was supplied. This is a reviewed example draft, not a submission certification.

**One sentence:** Given an image, encoding only its visible patches and reconstructing missing content with a lightweight decoder makes MAE's asymmetric pretraining mechanism visible.

**Scope:** Pretraining only. The previous MAE example also contained downstream recognition; that lane was deliberately removed to give the novel pretraining mechanism sufficient physical area. No speed or accuracy result is plotted here.

## Source checks

- Paper: [Masked Autoencoders Are Scalable Vision Learners, Section 3 and Figure 1](https://arxiv.org/pdf/2111.06377v3), also recorded in `research/verified-fixtures.json` from the earlier source review.
- Primary implementation: [facebookresearch/mae/models_mae.py](https://github.com/facebookresearch/mae/blob/main/models_mae.py), read 2026-09-12; retrieved blob SHA `880e28f8225fa9b56d7ba2963c2cb2c9d6f3d896`.
- Checked operations: patch projection and encoder position addition; shuffled masking and retained identities; visible-only encoding; decoder projection; shared mask-token copies; original-order restoration; decoder position addition; pixel prediction; MSE averaged only over masked patches.
- Patchwise embedding and original encoder position information are represented by the packed-token label and explained in the caption; the raw-to-token projection is not separately drawn. The illustrated scene patches in that strip communicate token content, not literal token dimensionality.

## Representation contract

| Scientific object | Visual mark | Meaning and limit |
|---|---|---|
| Image / original target | Same procedural vector landscape | Recognizable content correspondence; neither a dataset image nor a model result |
| Patch identity | Row-major IDs 1–16; retained IDs 2, 6, 11, 15 | Same IDs throughout; no new content between input and visible-token strip |
| Hidden input patch | Warm pale tile with diagonal mark | Removed from the encoder input |
| Visible-token content | Cropped pieces of the same landscape, reordered 11, 2, 15, 6 | A countable short sequence; projection and positional information abstracted |
| Encoder / decoder | Larger teal stack / smaller warm stack | Architectural asymmetry; stack multiplicity is schematic |
| Encoded visible token | Blue latent tile with persistent position ID in the inset | A learned representation, not a second image patch |
| Decoder mask token | Warm latent tile with diagonal mark, originating from M × 12 | Twelve copies of one learned token; IDs in the restored row name spatial positions, not distinct mask parameters |
| Reconstruction | Slightly changed landscape, labeled illustrative | A visual explanation of prediction, not evidence of actual accuracy |
| Masked-only objective | Original target grid with visible positions blanked, feeding MSE | Only twelve masked positions are scored; no numerical error is invented |

**Reading path:** Original patch image → countable mask → packed visible tokens → larger encoder → restored latent grid → smaller decoder → illustrated reconstruction. The restoration callout adds a second reading depth. The original-target grid and MSE form the supervision branch.

**Novelty location:** The short encoder input is visible as four patches, while the decoder receives all sixteen positions. The inset exposes how missing positions re-enter the computation instead of hiding that operation in a box label.

**Detail priority:** Visible-only encoding and encoder/decoder asymmetry are the central MAE proposal. Position restoration is expanded as a teaching detail because the earlier figure hid how four tokens become sixteen positions; unshuffling is not presented as an independent novel algorithm. The caption explicitly identifies M as one shared learned mask token.

## Composition comparison

The first v2 draft preceded loading the updated three-composition requirement. Three rough thumbnails were then authored and compared as a late design check; `storyboards.png` preserves that comparison. They are not retroactively presented as pre-drawing exploration.

| Alternative | Strength | Tradeoff / decision |
|---|---|---|
| A: Example pipeline plus restoration inset | Maintains one intuitive reading direction and preserves exact ID correspondence at a second scale | Retained. Upper route needs careful label spacing; repaired after actual pixel inspection. |
| B: U-shaped route around a worked example | Gives restoration more central area | Reverses direction for reconstruction and makes loss routing harder to distinguish at this small height. |
| C: Full-token versus visible-token routes | Makes computational asymmetry explicit relative to a comparator | Adds a second model path not needed to reconstruct the method and crowds out original targets. Better suited to a controlled ablation teaser with corresponding results. |

**Unresolved:** No manuscript insertion proof, empirical model reconstruction, or full color-vision simulation. Grayscale and a physical-width page proof are included. The design comparison is qualitative and covers this one paper.
