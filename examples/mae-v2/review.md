# MAE v2 review record

Date: 2026-09-12. Scope: standalone 7-inch-wide method figure. The author inspected actual PNG pixels, grayscale, and the exported physical-width page proof. Independent review is tracked separately by the coordinating reviewer.

## Observed changes

| Version | Observed failure or gap | Repair / outcome |
|---|---|---|
| Earlier MAE example → v2 | Most stages were text in similarly shaped boxes, including a “Pixels” output; the specific reconstruction operation was not visible | Introduced a coherent vector scene, actual patch-content crops, persistent IDs, architectural asymmetry, restoration correspondence, and original masked targets |
| Initial v2 | Restoration label encroached on the encoder; long captions collided near the packed-token strip | Broke restoration labels into centered lines, shortened token captions, and separated visible/hidden counts; initial image retained in `review-history/initial.png` |
| Revised v2 grayscale | Blue and warm pale latent fills were insufficiently distinct in the small restored grid | Added a diagonal mark to each mask token, matching the hidden-patch mark; inset retains numeric IDs as further redundancy |
| Independent reader | Selection could be mistaken for content-aware choice | Changed the first stage heading to “Randomly keep 25%”; caption and brief clarify the shared learned M token and the inset's teaching role |

## Independent comprehension review

The coordinating reviewer relayed an independent reader's recovery of the four-of-sixteen visible-only route, persistent identities, unshuffling, and masked-only loss. No major routing defect was reported. The reader requested explicit random selection and clarification that M is a shared learned mask token; these are addressed in the heading and caption. The inset attracts substantial attention, so the brief distinguishes it from the central encoder/decoder asymmetry. This is a scoped qualitative review, not an experimentally calibrated comprehension score.

## Checks completed

- Primary implementation operations checked against the caption and visible branch semantics.
- Exactly four visible IDs are preserved across original image, masked image, packed tokens, restored grid, and inset. The order 11, 2, 15, 6 is consistently unshuffled back to row-major positions.
- Twelve original target patches remain; the four visible positions are blank in the target grid.
- No empirical performance values, uncertainty intervals, or measured reconstruction results are supplied. The output image and caption explicitly state the illustrative status.
- All text extents remain inside the 7 × 3.95-inch canvas; enlarged image inspection found no remaining main-label collisions after revision.
- SVG text remains editable and vector scene primitives are preserved. PDF uses embedded TrueType fonts; PNG is exported at 300 dpi.
- The final-size page proof was inspected. Essential operation labels are approximately 8–9 pt; small patch IDs are supporting correspondence cues also enlarged in the inset. The figure is intended for two-column width, not uniform shrinking into one column.

## Limits

The two MAE versions have different scope: v2 omits the earlier downstream-recognition lane. This is an intentional same-paper redesign, not a controlled test of general skill superiority. The abstract scene does not substitute for real reconstruction examples when a paper's argument depends on measured qualitative performance. The actual manuscript and full color-vision simulations were not available. There is no claim that successful export or automated text checks establish visual quality.
