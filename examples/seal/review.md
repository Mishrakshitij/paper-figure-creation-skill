# Visual review and revision record

Actual rendered source-reference images inspected: SEAL overview; knowledge-incorporation setup; few-shot setup. Original source files were retrieved from the authors' public website repository but are not redistributed here.

The first rendered drafts are retained in `teaser-v1-review.png` and `method-v1-review.png`. Later pre-review versions are retained as `*-v2-review.png` and `*-v3-review.png`. The composition comparison sheet is a late design comparison, produced after the initial draft; it is not evidence of a pre-draft thumbnail step.

| Actual problem in first render | Revision |
| --- | --- |
| Teaser panel title crossed the vertical separator into the next title | Replaced it with a shorter action sequence; shortened the evidence heading |
| Adjacent passage-setting headers touched | Reduced header text size slightly while preserving exact regime identities |
| The update arrow disappeared behind the adaptation background | Raised connector z-order; the parameter change is now visible |
| The method return arrow crossed the current-policy label | Routed the return around the outer left gutter into the model's left port |
| The inner-update equation crowded the third model chip | Used a short loop label and moved the candidate lane upward |
| Inset footers collided across the center boundary | Replaced them with one centered schematic-disclosure line |
| A grid-transform arrow disappeared behind its card | Corrected connector z-order consistently |

Scientific checks: all 19 plotted values come from current evidence objects; the live validator passes. Every Table 2 row and regime is retained, including the two columns where GPT-4.1 data exceeds SEAL. Every Table 1 method is retained, including the oracle. The source does not provide entry-specific uncertainty for these tables, so no error bars or significance claims are supplied. The fictional example is visibly labeled. Each method candidate starts at the same current weights; the independent branches are not a chain of accumulating updates. The generic reward symbols must not be read as actual experimental outcomes.

Exports: 7-inch-wide PDFs and live-text SVGs, 300 dpi PNGs, 100 dpi physical-size previews and grayscale previews. Text/canvas bounds are checked by the build. Full-image pixel review was used for the revisions above. This is a scoped design demonstration, not a blinded superiority experiment or a venue submission check.

Subsequent root and independent image-only review produced concrete semantic revisions:

- The teaser initially could describe untrained synthetic-data finetuning. Added the dashed recall-reward return and “RL training only” label, and identified the writer as RL-trained.
- The ARC microplots now explicitly state their 0–100 scale.
- The SEAL row keeps an identity highlight, while numerical bolding now follows the actual winner in each knowledge column. GPT-4.1 is visibly best in both continued-pretraining columns.
- Added an RL record object carrying context, edit and reward before the policy-update step, so the selection object is explicit.
- The inner operation now says “Apply edit + SFT”; the few-shot inset says its configuration controls training. This avoids presenting configuration text as an SFT target.
- Labeled the grid pair as an augmentation and stated that the knowledge update trains on passage plus self-edit.

The final PDF was rasterized independently with PyMuPDF at 100 dpi and inspected alongside a grayscale preview. No source figures, source PDFs, or third-party image files are redistributed.
