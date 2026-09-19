# Review record

## Scientific review

Checked the supplied brief and the primary v2 source, §4.1/Eq. (3), Figure 1 labels, and deployment paragraph. Traced the same x through both branches. Dimensions compose as k→r→d; the frozen branch produces a d-vector; the merge is coordinate-wise addition. W₀ is frozen, only A and B are trainable, Gaussian/zero initialization preserves the original output, and the deployment matrix includes the same α/r factor as the forward expression. No gradient, objective, observed activations, or performance claims were introduced.

An independent agent viewed `figure-paper-size.png` against the supplied source and correctly reconstructed both the additive computation and deployment merge. It reported that labels are legible at seven inches, branch arrows are clear, and no scientific or visual repair was required.

## Pixel review and repairs

1. Inspected the first 144-dpi render at the full manuscript width. The diagram had clear routing and no clipping. The word “sum” sat unnecessarily far beneath the plus operator; moved it immediately to the operator's left. Tightened “random init.” to “Gaussian init.” to match the primary source more precisely.
2. Rebuilt all exports from the canonical Python source.
3. Inspected the revised PDF-derived 144-dpi proof, the enlarged 300-dpi PNG, and a grayscale proof. Verified no missing mathematical glyphs, label collisions, matrix/arrow intersections, clipped strokes, or broken branch routing. State labels preserve meaning in grayscale. No approximate color-vision simulation was needed because state is explicitly labeled.
4. Inspected the thumbnail for reading order: shared input → two branches → sum; the lower deployment panel is visually distinct.

## Export verification

- PDF: one page, **504 × 300 pt = 7 × 4.167 in**; verified by `pdfinfo`.
- PDF text: DejaVu Sans subsets embedded with Unicode mappings; verified by `pdffonts`.
- SVG: live text, editable vector objects, semantic panel groups, and no raster images.
- PNG: 2100 × 1250 pixels (300 dpi); paper-size proof: 1008 × 600 pixels (144 dpi).
- Canonical rebuild: `python build_figure.py`. All final exports were generated from this source.

## Scope and limits

No manuscript template or integration target was supplied, so no paper compilation was performed. Matrix silhouettes are symbolic and not proportional dimension drawings. The primary PDF could be read through the browser but was not downloaded locally (HTTP 403). No unresolved scientific or export-format issue remains in the delivered figure.
