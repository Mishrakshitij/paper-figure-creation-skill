# LoRA figures

Reviewed drafts at 7-inch two-column width. Use `lora-teaser.pdf` and `lora-method.pdf` in LaTeX; SVG files preserve editable vector text and geometry. PNGs are 2100 pixels wide at 300 dpi. Final venue/template insertion still needs checking.

The author-created graphics show published results; no training runs were reproduced. Data come from the original [LoRA paper, version 2](https://arxiv.org/pdf/2106.09685v2), Table 4 and Sections 4.1, 4.2, 5.5, and D.4. `table4.json` retains all eight rows, including SAMSum columns omitted from the compact teaser.

`create_specs.py` writes the evidence and figure specifications. `build_figures.py` is the canonical geometry/plot source; it validates both current specifications live, writes fresh reports, and reads the validator's recomputed claims. The JSON uses the paper-figure-creation evidence envelope and a custom deterministic renderer. It is not a drop-in method spec for the bundled renderer because geometry is authored in Python.

Reproduce with Python 3 and `matplotlib`, `numpy`, and `Pillow`:

```bash
python create_specs.py
python build_figures.py --skill-root /path/to/paper-figure-creation
```

When this example is inside the skill repository, the script discovers `skills/paper-figure-creation/scripts/validate_evidence.py` in an ancestor and `--skill-root` is unnecessary. It stops if the current evidence fails validation or the validator is unavailable; saved reports are not trusted as validation of edited specifications. The helper verifies declared data linkage and arithmetic; source transcription and scientific meaning require independent review.

Supporting files: `brief.md`, `captions.md`, `review.md`, the specs/ledger, and the reproducible scripts. `*-print.png` and `*-grayscale.png` support visual QA; they are not the high-resolution submission images. The source SVGs use regular editable text rather than outlined glyphs. Cosmetic SVG edits must be transferred back to Python/specs before regeneration.
