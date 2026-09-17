# Review record

## Scope and status

Reviewed example draft. This is a guided design demonstration using one known paper, not a blind generalization test, submission certification, user study or measured quality improvement.

## Author pixel review

The author inspected the full PNG, repaired overlapping mask-token annotation/restore-position text, and inspected the 110 dpi PDF proof at the intended seven-inch width. The first arrangement also left four prediction slots blank; these now contain faint symbolic pixel marks so that the drawing communicates all sixteen predictions while reserving warm emphasis for the twelve scored positions.

The inspected proof communicates the central encoder asymmetry, exact four-patch correspondence, shared mask-token insertion, restored positions and the target branch. It uses recognizable photo content for input identity without presenting synthetic output as an experimental reconstruction.

The root review identified that “score 12 / 16” could be read as an empirical result. That label was replaced by “12 masked slots”; the numerical construction remains a patch count, not an evaluation score.

Independent review identified that the explicit random-selection cue had been lost from the previous vector example. The input transition now says “75% at random,” and the caption specifies a random subset. The caption also states that each symbolic prediction slot represents one patch’s pixels. The floating unshuffle/decoder-position note remains above the restoration–decoder route; the caption gives its exact operation order. A grayscale PDF proof was added for a bounded check of redundant cues.

The independent grayscale check found that the twelve scored output slots relied too strongly on color. Small solid corner marks were added only to these twelve slots; all sixteen retain symbolic pixel bars. The caption explains the corner marks. Color and grayscale PDF proofs were regenerated and inspected at seven-inch width.

## Checks

- Retained patch IDs: 2, 6, 11, 15. Packed IDs: 11, 2, 15, 6. All packed crops come from the committed source array.
- Encoder input count: 4; decoder position count: 16; loss position count: 12.
- Removed patches are opaque. Original target cells at visible positions are blanked.
- All sixteen predicted positions are symbolic; no synthetic reconstruction or empirical accuracy is shown.
- Original targets use the same source image as the input.
- Geometry checks report no text outside the canvas. Actual label/arrow interactions were visually inspected; containment checks alone cannot establish readability.
- SVG retains editable text and vector paths; raster image content is embedded. PDF retains fonts and text. This is a hybrid artifact, not a fully vector artifact.

## Limits

No insertion into a target manuscript, physical print, participant comprehension test, empirical model inference, or full color-vision simulation was performed. Color distinctions are reinforced with diagonal mask strokes, persistent patch IDs, solid output-slot corner marks, spatial position and direct labels. The original fox scene's finer texture does not survive very small thumbnail display, so clarity depends on the seven-inch figure width rather than texture alone.
