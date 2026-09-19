# Provenance

- Requested subject and constraints came from `figure-forward-inputs/lora-method.md`; no repository examples were read.
- Scientific source: Edward Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models*, arXiv:2106.09685v2, dated 16 October 2021. https://arxiv.org/pdf/2106.09685v2
- Source accessed through the browser on 19 September 2026. Relevant source anchors: Figure 1, p. 1; §4.1 and Eq. (3), p. 4; deployment paragraph continuing onto p. 5. The source's scaling paragraph is included explicitly in both forward and merged formulas.
- A local primary-PDF download returned HTTP 403; no source PDF is bundled. The primary text and figure labels were available through the browser. Review of the generated artifact uses local rendered pixels.
- Original geometry and placement authored for this task in `build_figure.py`. The figure redraws the described mechanism rather than copying the paper artwork. No generated imagery, external graphical assets, empirical data, or measured activation values are present.
- Typography: DejaVu Sans (installed open-source font); PDF embeds subsets. SVG keeps live text and vector geometry. All marks are vector; there are no image elements.
- Grey with explicit “FROZEN” denotes pretrained weights; amber with explicit “A and B trainable” denotes adaptation parameters. Solid arrows denote forward vector flow. Panel b is a separate deployment phase.
- Editing: edit `build_figure.py` and rebuild; treat it as the canonical source. `figure.svg` is directly editable, but source regeneration overwrites manual SVG edits.
- Build requirements: Python 3, Pillow, Inkscape 1.2.2, Poppler (`pdftoppm`, `pdfinfo`, `pdffonts`). Run `python build_figure.py` in this directory.
