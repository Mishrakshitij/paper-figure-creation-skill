# Physical SVG composition

Use `scripts/compose_svg.py` to assemble **already validated** graphs, precise
vector explanations, and generated illustrative assets. A JSON manifest is the
single source for placements and authoritative overlay geometry. The tool is a
compositor, not an evidence validator or automatic scientific illustrator.

```sh
python scripts/compose_svg.py composition.json --output output/figure --formats svg,pdf,png
```

The SVG is always saved as the canonical editable export. PDF and PNG use
Inkscape; PNG defaults to 300 DPI (`--dpi 600` changes this). Pillow is required;
`pypdf` additionally verifies the exported PDF page dimensions. A missing export
backend is an explicit error, not a claim that all formats succeeded.

## Manifest

**Every canvas coordinate, placement, overlay font size, stroke width, and radius
is in physical points (72 points = 1 inch).** SVG's internal user units are set
so one authored unit is one final point. Do not put `8` on a 1024-unit canvas and
call it 8-point publication text.

```json
{
  "title": "Self-adaptation: mechanism and measured results",
  "canvas": {"width_pt": 504, "height_pt": 270, "background": "white"},
  "asset_root": ".",
  "quality": {"minimum_font_size_pt": 7, "minimum_raster_ppi": 300},
  "assets": [
    {
      "id": "memory", "kind": "raster", "path": "assets/memory.png",
      "box_pt": [15, 55, 115, 90], "fit": "contain",
      "provenance": {
        "role": "generated illustration, not experimental evidence",
        "source": "image generation tool", "prompt_file": "assets/prompt.txt",
        "license_status": "generated asset; tool terms apply"
      }
    },
    {
      "id": "results", "kind": "vector", "path": "results.svg",
      "box_pt": [180, 30, 314, 220], "fit": "contain",
      "provenance": {
        "role": "measured results", "source": "evidence.json",
        "build_command": "python build_results.py"
      }
    }
  ],
  "overlays": [
    {"type": "text", "x": 12, "y": 18, "text": "a  Adapt from an example", "font_size_pt": 9, "font_weight": "bold"},
    {"type": "text", "x": 180, "y": 18, "text": "b  Compare all methods", "font_size_pt": 9, "font_weight": "bold"},
    {"type": "arrow", "points": [[60, 155], [60, 175], [120, 175]], "stroke": "#147D92", "stroke_width_pt": 1.2}
  ]
}
```

Asset paths must be relative to `asset_root`, which itself must remain inside
the manifest directory. Symlinks cannot escape this root. Put the manifest at a
common parent of required assets, or copy those assets into its folder and keep
provenance. Do not point a figure manifest at arbitrary absolute file paths.

`box_pt` is `[x, y, width, height]`, with a top-left origin. `contain` preserves
aspect ratio and centers the complete asset. `cover` requires `allow_crop:true`
and clips to that box; never crop a graph's ticks, methods, or unfavorable data.
Stretching is intentionally unsupported. Assets paint in listed order, followed
by overlays; use a vector asset for more intricate, interleaved diagram layers.

## Authoritative overlays

- `text`: `x`, `y` (first baseline), `text`, `font_size_pt`; optional `font_family`
  (default DejaVu Sans), `font_weight`, `fill`, `anchor` (`start`, `middle`, `end`).
  Newlines become editable tspans at 1.25 line spacing. Text is not automatically
  wrapped; decide line breaks from the actual scientific phrasing.
- `rect`: `x`, `y`, `width`, `height`, optional `radius_pt`.
- `ellipse`: `cx`, `cy`, `rx`, `ry`.
- `arrow`: `points`, an ordered list of at least two `[x,y]` points. Choose the
  actual route; the tool does not infer a scientific dependency or avoid nodes.
- `path`: SVG `d` path data, for exact custom geometry.
- All shapes support `fill`, `stroke`, `stroke_width_pt`, and `dash_pt`.

Equations with complex typography should be imported from a controlled vector
source; inspect their final size. No default scale bar is provided. A scientific
scale bar requires explicit physical calibration and evidence outside this tool.

## Imported vectors and portability

Set Matplotlib `svg.fonttype = 'none'` to keep labels editable. SVG imports retain
live text, paths, clips, gradients, and static geometry. IDs and all `url(#...)`
and fragment references receive per-import prefixes to prevent collisions.
Simple tag, class, ID, and universal CSS selectors are computed into inline
styles, so a plot's global `*` style cannot restyle neighboring assets. Inline
styles and presentation attributes are preserved. Active content, linked
resources, arbitrary DTDs, nested SVG viewports, CSS variables, `!important`,
complex selectors, and unresolved references fail explicitly. Export a flat
static SVG with inline computed styles if an input uses unsupported features.
PNG/JPEG/WebP assets are embedded as data URIs. Inline raster images already
inside imported SVGs are retained and included in the PPI audit. No imported
plot is flattened to a bitmap merely to simplify composition.

## Report and review

`figure.composition-report.json` records the manifest hash, source-file hashes,
declared provenance, exact canvas size, final font sizes after imported SVG
transforms, minimum readable-text estimate, and effective raster PPI. Imported
SVG font sizes use SVG/CSS unit conversion before the placement scale; numeric
manifest overlay sizes are final physical points. Anisotropic transformations
use the smallest glyph scale for a conservative font-size warning and the
largest pixel scale for a conservative raster-resolution estimate.

No live text in an imported SVG triggers a warning: its labels may have been
converted to paths. Provenance declarations are recorded, not independently
verified. The report says scientific evidence was **not** validated here; run
the evidence/graph workflow before assembly.

Exports have separate verification records: SVG XML/constructed dimensions,
PNG pixel dimensions at the requested DPI, and (when `pypdf` is present) PDF
page count/MediaBox. These checks do not establish visual quality. Render and
inspect at final manuscript size and enlarged, including overlaps, clipped
glyphs, repeated IDs, arrow routing, and the placement of every data series.
Regenerate all exports from the manifest after fixes. Native `.drawio` is not
produced by this compositor; supply it only when that tool is the canonical
geometry authoring source and its exports were separately inspected.
