# SEAL: original figure redesigns

These examples answer a concrete critique of the first release: a valid graph and a sequence of labeled boxes are insufficient for a strong paper figure. Documents, parameter chips, candidate lanes, domain-specific contents and a distinct reward return make the method visible.

![SEAL teaser](seal-teaser.png)

![SEAL method](seal-method.png)

Rebuild from the repository root:

```bash
python examples/seal/create_specs.py
python examples/seal/build_figures.py
```

Or use `python build_figures.py --skill-root /path/to/paper-figure-creation` after copying this directory and the installed skill. Runtime dependencies: matplotlib, numpy, Pillow. Evidence validation runs against the current JSON specification before every build. No network is required.

Edit the semantic content and exact table values in `create_specs.py`; edit the bespoke composition in `build_figures.py`. SVG text remains editable, PDF embeds fonts, and PNG exports at 300 dpi. This composition is not represented by a generic box-layout JSON schema. The SVG is the editable vector deliverable; no native draw.io export is claimed.

See [brief](brief.md), [captions](captions.md), [review](review.md), [exact data](reported-tables.json), and the JSON provenance specifications. These are original pedagogical redesigns, not figures endorsed by the paper authors. The input illustrations and rewards are explicitly schematic; the plotted results are reported.
