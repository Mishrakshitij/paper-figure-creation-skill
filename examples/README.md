# Example gallery

These are original explanatory redraws using published data. They are not the original authors' artwork or new experimental reproductions. Each directory preserves source/specification, editable vector output, PDF and PNG.

| Paper | Teaser | Method | What the case tests |
| --- | --- | --- | --- |
| MAE | [PNG](mae-teaser/figure.png) · [PDF](mae-teaser/figure.pdf) · [SVG](mae-teaser/figure.svg) | [PNG](mae-method/figure.png) · [PDF](mae-method/figure.pdf) · [draw.io](mae-method/figure.drawio) | Real masking representation, cost-quality trade-off, training/inference separation |
| Transformer | [PNG](transformer-teaser/figure.png) · [PDF](transformer-teaser/figure.pdf) · [SVG](transformer-teaser/figure.svg) | [PNG](transformer-method/figure.png) · [PDF](transformer-method/figure.pdf) · [draw.io](transformer-method/figure.drawio) | Complete task-specific baseline list, ensemble labels, attention conditioning, correct repeated-block scope |
| LoRA | [PNG](lora/lora-teaser.png) · [PDF](lora/lora-teaser.pdf) · [SVG](lora/lora-teaser.svg) | [PNG](lora/lora-method.png) · [PDF](lora/lora-method.pdf) · [SVG](lora/lora-method.svg) | Independent use of the skill, two task comparisons, parameter budget, frozen/trainable branches |

![Original Transformer teaser redraw](transformer-teaser/figure.png)

![Original MAE method redraw](mae-method/figure.png)

![Original LoRA method redraw](lora/lora-method.png)

Rebuild the MAE/Transformer JSON specs with `python examples/build_specs.py`. Render each with the skill's `scripts/render_figure.py SPEC --output PATH --strict-layout`. LoRA uses its own source in `lora/` to exercise the skill's custom-layout route. Read the captions alongside the figures.

The [review history](review-history/) preserves initial outputs with known defects for audit, and [evaluation](../docs/evaluation.md) explains the repairs. Initial images are not approved examples. Synthetic starter templates are labeled separately from these reported-data redraws.
