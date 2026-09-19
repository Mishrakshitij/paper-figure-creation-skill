# Hybrid illustration and precise scientific graphics

Use this only when a pictorial asset helps explain the paper. A hybrid figure combines an illustrative or observed image with deterministic scientific geometry. Its goal is stronger recognition and visual storytelling while preserving source accuracy, editability and reproducibility.

Assets can be generated, supplied, or downloaded from web/image search. Read [asset-sourcing.md](asset-sourcing.md) for retrieving actual originals, using official logos/icons, transparent cutouts and background removal. Searching is a way to obtain visual material or inspect design references, not a substitute for source verification. Exact connector geometry and label placement follow [geometry-and-inspection.md](geometry-and-inspection.md).

## Assign authority to each layer

| Layer | Appropriate source/authoring | What it may establish |
|---|---|---|
| Observed example or result | Actual dataset, experiment, screenshot or simulation output with provenance | Only the observation supported by that source |
| Illustrative scene | Original vector art or generated raster illustration, labeled as illustrative | A teaching example or problem context, not measured behavior |
| Scientific structure | SVG, Matplotlib, diagrams.net or TikZ geometry from the source contract | Exact branches, masks, positions, operations and information access |
| Numerical evidence | Plotting code using an evidence ledger | Values, uncertainty, scales and comparisons supported by the data |
| Typography and annotations | Editable text placed after composition | Exact names, equations, units, qualifiers and panel references |

Use image generation for a scene or illustrative asset, not for precise diagrams, charts or information that must be exact. Do not rely on a prompt asking for correct arrows or numbers as a substitute for scientific construction and review. Existing observed results must not be regenerated to look cleaner or more favorable.

## Prepare a compact asset brief

Before generating, define what the asset contributes and where it will appear:

```text
Role: illustrative input / task vignette / observed example from supplied data
Explanatory purpose: what the reader recognizes from this asset
Subject and view: only the objects and viewpoint that serve that purpose
Visual identity: distinctive features that survive small display or patch extraction
Composition: intended shape and space needed for vector overlays
Style: compatible palette, texture and detail level for this paper
Exclude: text, axes, numerical results, scientific arrows and authoritative labels
Status: generated illustration, not an observed experiment or model prediction
```

Preserve source assets for real examples. For a generated asset, save the exact prompt, available tool/model information, date and selected file with the project; do not guess a model version that the tool does not expose. State that regeneration may differ. A build should use the committed selected asset and run without an image-generation service or API key.

Examples of useful requests: a recognizable natural scene used to explain image patch masking; a text-free environment vignette for a clearly schematic navigation task; an original object cutout that helps identify a manipulated item. A text passage, UI form or code diff with authoritative contents is usually easier to author directly as vectors.

## Compose with an explicit asset boundary

Choose the asset's display rectangle and the coordinate system for overlays. Keep text, chart marks, important arrowheads and exact state changes in deterministic layers. Use actual pixel crops or masks from the same asset when a method requires correspondence; do not independently regenerate each panel and assume object identities stayed fixed.

For a masked-image teaching example, preserve the patch indices, show only visible content entering the encoder, restore positions according to the method, and label symbolic predictions as symbolic. Do not paste ground truth into the prediction panel and present it as a model reconstruction. A generated input remains illustrative even when the mask geometry is exact.

For environment figures, a generated background may supply context while visible objects, action targets and evaluator conditions remain source-grounded. If the illustration invents spatial relations that affect the task, it is the wrong asset. Prefer a vector scene when geometry itself carries the scientific claim.

Keep a simple asset ledger: relative path, provenance/status, checksum, pixel dimensions, display size, and any crop/resampling or format conversion. Provide an alt description. Avoid embedding the same large image repeatedly when shared assets, extracted patches or a smaller adequate export solve the problem.

## Export honestly

- Deliver the build source and selected assets together; resolve assets relative to the project, not a temporary download location.
- Preserve live vector text and scientific geometry in SVG/PDF. Embed needed raster assets so exports do not depend on missing external links.
- Describe the artifact as **hybrid**, and identify which elements are raster versus editable vectors. Do not call a PDF fully vector because its extension is `.pdf`.
- Choose raster resolution from its final physical display size. Record effective pixels per inch and inspect the export; resolution alone does not prove legibility.
- Keep generated imagery clearly identified in the figure or caption wherever a reader might otherwise take it as real data or an observed prediction.

## Review the asset and the complete figure separately

Inspect the asset for subject recognition, malformed details, unwanted marks and conflicts with the intended task. Then inspect the assembled figure for crop/identity consistency, correct overlays, readable text, exact wiring and any ambiguity between illustration and evidence.

Check a rasterized final PDF as well as the standalone preview. Verify that image embedding has not flattened labels or introduced different crops. Compare the complete result against a vector-only option when the illustrative layer might compete with the scientific transformation. Keep the image only if it serves the explanation.

If an image-generation tool is unavailable, continue with original vector illustration or user-supplied assets and say which route was used. Do not silently install a new service, require credentials or claim a generated preview was produced. Apply the hosting tool's normal instructions when generation is available.
