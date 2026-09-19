# LoRA method figure

A 7-inch-wide method figure explaining the shared-input low-rank adaptation path and its merged deployment form, based on arXiv:2106.09685v2, §4.1 and Figure 1.

## Deliverables

- `figure.pdf`: manuscript-ready vector export, 7 × 4.167 in.
- `figure.svg`: editable text and vector geometry.
- `figure.png`: 300-dpi preview.
- `build_figure.py`: canonical geometry and reproducible build.
- `figure-plan.md`: selected figure jobs, source-backed connectivity, three layout choices.
- `composition-sketches.svg`: rough alternate compositions.
- `caption.md`: draft manuscript caption.
- `provenance.md`: sources, conventions, tools and editability.
- `review-notes.md`: source check, independent review, pixel repairs and verification.
- `figure-paper-size.png`, `figure-pdf-proof.png`, `figure-grayscale.png`, `figure-thumbnail.png`: review proofs.

## Rebuild

```bash
python build_figure.py
```

Requires Python 3, Pillow, Inkscape and Poppler. SVG edits are possible, but rebuilding overwrites them; preserve lasting changes in the Python source.
