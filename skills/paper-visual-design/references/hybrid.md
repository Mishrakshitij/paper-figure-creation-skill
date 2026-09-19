# Hybrid illustration + editable SVG

Use image generation for a useful illustrative object, scene, or composition exploration. Keep the model's output away from scientific authority: text, equations, graph marks, architecture connections, task-state transitions, and claims must come from deterministic source-backed authoring.

Read [composition schema](../foundation/references/composition-spec.md) for `compose_svg.py` and the foundation's [hybrid design guide](../foundation/references/hybrid-authoring.md) for additional context.

## Decide what deserves generation

Write an asset inventory: intended meaning, approximate final size, exact overlay area, illustrative/observed status, and whether simple vector construction would be clearer. Useful assets include a recognizable input scene, a cutaway of a physical apparatus, or a restrained material rendering. Avoid merely decorating an already clear box with a generic brain/robot icon. Use real scientific images/screenshots for observed evidence; generation must not impersonate them.

A prompt should specify subject, scientific role, camera/view, restrained palette, background/alpha, empty label zones, final-size simplicity, and exclusions. Ask for **no text, numbers, arrows, axes, legends, watermark, or invented measurements**. Generate separate assets when independent placement matters. Keep the accepted image and exact prompt; record tool/date and model only if exposed. Do not invent a license for generated content; record that it was generated for this project and that publication policy/rights have not been independently verified.

Inspect the asset before assembly. Reject an attractive image that changes object count, anatomy, perspective, identity, or implies an unsupported mechanism. Preserve the same accepted asset/example through stages instead of independently regenerating inconsistent versions. If generation is unavailable, use a source-permitted asset or vector representation and say which route was actually used.

## Compose in physical points

Use a canonical manifest with a canvas in **points (72 pt = 1 in)**. Place vector panels and raster assets in `box_pt` rectangles. Embed local assets so the SVG is self-contained. Author exact text, arrows, and simple geometry as overlays; use imported SVG for complex scientific internals. Keep one geometry source: the manifest and its source assets, or a native editor document, never mutually stale copies.

Build charts at final slot dimensions. An 8 pt label in a plot scaled by 0.5 becomes 4 pt; declaring `font_size_pt` while writing that number into a 1024-pixel viewBox does not make it points. Check transformed effective type size, not just a source font-size string. Check raster effective PPI at placed size. No default scale bar is valid for an uncalibrated scientific image.

The compositor prefixes imported IDs/references, preserves vector text/paths, and embeds raster pixels. It can flag geometry issues but cannot certify meaning or all visual collisions. Do not edit a composed SVG by hand and then silently overwrite it from the old manifest.

## Export and review

Export PDF/PNG from the canonical assembled SVG with Inkscape when available. If export support is unavailable, deliver the verified SVG and clearly state missing formats. Inspect the PDF-rendered page as well as the SVG preview: fonts, clipping, masks, markers, and transparencies can differ.

Report which regions are generated illustrations, which examples are constructed, and which marks are reported evidence. A hybrid figure need not look like a generated image; its goal is clear explanation with exact science and editable structure.
