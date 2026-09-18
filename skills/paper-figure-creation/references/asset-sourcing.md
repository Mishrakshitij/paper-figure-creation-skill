# Sourcing and preparing visual assets

Use generated illustrations, web-searched images, downloaded PNGs/SVGs, official logos, model illustrations, or original vector objects when they make the paper easier to understand. A recognizable model mark can identify a named component; a task image can establish the setting; a clean object cutout can expose an operation. None is mandatory. A numerical plot may need no pictorial asset at all.

This workflow complements [visual-elements.md](visual-elements.md) and [hybrid-authoring.md](hybrid-authoring.md). It covers obtaining and preparing assets; the manuscript and experimental records still determine the scientific content.

## 1. Decide what the image represents

Give each proposed asset one explicit role before searching or generating:

| Role | Suitable source | What it may communicate |
| --- | --- | --- |
| Observed input, prediction, or result | Actual dataset or experiment output | The specific recorded observation or result |
| Named model, software, organization, or instrument | Official logo, product image, model card, project repository, or original labeled illustration | Identity, not endorsement or performance |
| Concept, task vignette, or object analogy | Generated illustration, appropriately sourced image, or original vector drawing | An illustrative explanation, not experimental evidence |
| Exact mechanism or measured comparison | Editable vector geometry and source-linked plotting code | Operations, information access, quantities, and uncertainty |

Write the intended crop, final display size, and the feature that must remain recognizable. Prefer a real experimental image when it establishes what a model saw or produced. Do not regenerate evidence for a more attractive result. A downloaded model illustration is a visual reference or credited asset; its architecture is not automatically the architecture implemented in this paper.

## 2. Search for an appropriate original

Use available web search and image search to discover candidates. Search with the specific object/model name and terms such as “official logo,” “brand assets,” “transparent PNG,” “SVG,” “press kit,” or “project figure.” For benchmark observations, start with the official dataset, simulator, paper, or project repository.

Open the original source page and inspect the actual candidate image. An image-search thumbnail, search snippet, or recognizable filename does not establish source identity, image quality, or reuse terms. Follow the image to its publisher; prefer the official project, model provider, instrument maker, dataset owner, or primary paper where relevant. For a paper figure, record the figure/page locator and distinguish learning from its composition from reusing its artwork.

Official transparent SVG/PNG files are usually the best starting point for logos and named components: they preserve geometry and often avoid background removal entirely. Logos are allowed when they serve identification. Keep a nearby text label if readers may not recognize the mark, and do not use a logo as evidence of model quality or as an endorsement badge.

Record the source-page URL, direct asset URL when available, creator/organization, access date, and the license, attribution, or brand-guidance page that the source actually provides. Preserve any attribution required for the intended use. If terms are absent, record “not stated” or “not verified”; do not invent a license. Missing metadata alone is not a reason to stop all local figure work: continue the authorized composition, use another suitable source where helpful, and record the unresolved asset-specific condition for distribution. Respect any known restriction rather than describing all downloaded images as freely reusable.

## 3. Download, retain, and inspect

Download the original file into a project asset directory, with a stable descriptive name. Keep an untouched copy and compute its SHA256 checksum before editing. Do not rely on a remote URL, browser cache, expiring download link, or image service during the final paper build. Keep source credentials or signed-link secrets out of the provenance record; a stable public source page is preferable when the direct download URL is temporary.

Check the file type and dimensions, then inspect the local pixels with the available image viewer. Look for watermarks, unwanted text, missing objects, misleading perspective, compression artifacts, false transparency, or tiny details that disappear at the intended print size. Verify that a supposed transparent PNG actually has useful alpha rather than a baked-in checkerboard. Inspect an SVG as rendered pixels as well as retaining its editable source.

For generated assets, use the available image-generation tool and actually produce and inspect the chosen image. Save its exact prompt, tool/model information exposed by the tool, creation date, selected file and checksum. Do not guess an unavailable model version. Generate recognizable scene content or text-free objects; author scientific labels, plots, equations and wiring separately. Reuse the selected asset across matched panels so object identity is preserved. A rebuild must not require regenerating it.

## 4. Remove backgrounds or prepare cutouts when useful

Background removal is appropriate when the background competes with the intended object, prevents clean placement, or hides a meaningful relation. Keep a task's spatial context when that context is scientifically relevant. Removing a background does not turn an illustrative object into observed evidence.

1. **Check for a ready transparent original first.** Prefer an official transparent logo, SVG, or product cutout over editing a flattened screenshot. Use the supplied light/dark variant when available instead of inventing a recoloring.
2. **Inspect before editing.** Open the local source image. Identify foreground boundaries, fine structures, holes, shadows, reflections and text that must survive. Keep the original unchanged.
3. **Use the available image-editing tool.** In Codex, use `imagegen` for background removal and other image editing unless the user explicitly requests another approach; follow its current tool instructions. Reference the inspected local file when available, request a transparent background, and save a distinct derived asset. Do not silently replace the required tool with a Python masking pipeline. If the tool is unavailable, retain the original in a suitable frame or use an existing transparent/vector asset and state that removal was not completed.
4. **Make the edit narrowly specified.** For example: “Remove only the background and return a transparent cutout. Preserve this object's silhouette, internal details, colors, proportions and orientation. Keep thin structures and holes. Do not add text, redraw components or alter the subject.” For a real observation, never request changes to task state or measured output under the name of cleanup.
5. **Inspect the actual derived file.** Check that alpha was produced. Compare original and derived images side by side at high zoom, then composite the cutout over light, dark and intended figure backgrounds. Inspect edge halos, color fringes, jagged contours, accidentally erased interiors, lost thin parts, altered text and residual background islands. Then inspect again at the final physical display size: large-image cleanliness does not guarantee a clean small cutout.
6. **Accept only a faithful result.** If the tool changes object identity or leaves distracting edge defects, repair the specific issue with the editing tool or select a better original. Preserve the previous versions and provenance. Do not describe an uninspected or failed cutout as complete.

### Preserve official logo integrity

Do not ask a generative model to recreate, approximate, restyle, or “improve” an official logo. Obtain the official artwork and preserve its shape, lettering, proportions, approved colors and relevant clear space. A generic generated model/robot illustration must not be presented as the provider's official mark.

For a flattened logo, first look for the official transparent equivalent. If an image-editing tool is used only to isolate the supplied mark, compare the result closely with the original and reject any changed lettering, contour, color or proportions. Background removal does not authorize redrawing. When exact preservation cannot be established, keep the official original on a neutral panel or use a text label; do not substitute an AI-redrawn mark. Follow the source's actual brand guidance without imposing a blanket prohibition on logos in research figures.

## 5. Record original and derived authority

Keep a small asset ledger beside the figure. Use actual values and explicit unknowns:

```yaml
asset_id: camera_cutout
role: illustrative object
status: sourced photograph; not an experimental observation
source_page: https://example.org/original-page
source_asset: https://example.org/assets/original.png
creator: source-provided name, or not stated
accessed_at: recorded date
license_or_terms: source-provided identifier and URL, or not verified
attribution: exact required credit, or not stated
original_file: assets/original/camera.png
original_sha256: computed checksum
derived_file: assets/derived/camera_cutout.png
derived_sha256: computed checksum
edit: background removed; subject retained
edit_tool: actual tool and exposed model information
edit_prompt_file: assets/prompts/camera_cutout.txt
pixel_dimensions: [actual_width, actual_height]
crop: none, or exact source rectangle
display_size_inches: [actual_width, actual_height]
other_transforms: actual scaling, conversion or resampling
review: before/after inspected; edge and final-size checks recorded
```

For an official logo, record that identity explicitly. For generated art, replace the web-source fields with the generation prompt and available tool provenance. For observations, add dataset/episode/frame/sample identity and the selection rule. Record the original and each accepted derivative separately; do not replace the original checksum with the edited file's checksum. Add an alt description and the local attribution location when relevant.

## 6. Compose and review the whole figure

Place the selected asset into the editable figure source. Keep all exact scientific content—text, equations, measurements, masks, data marks, connectors and information boundaries—in deterministic vector layers. A logo should identify its component without hiding the component's operation. A photo should clarify the task without suggesting an unperformed experiment. Remove assets that add atmosphere but obscure the comparison.

Render the complete figure and inspect both enlarged and at manuscript size. Check cropping, contrast, alpha edges, text legibility and whether the illustration can be mistaken for results. Preserve negative outcomes and material conditions. Embed the saved assets in PDF/SVG exports and deliver them with the source; disclose raster/vector boundaries rather than calling a hybrid PDF fully vector.

Verify raster quality in the actual exported PDF/SVG as well as the source PNG. A high-resolution original can be silently resampled by the plotting backend. For example, set export DPI explicitly when a Matplotlib PDF/SVG contains images, and use `pdfimages -list figure.pdf` when available to inspect the embedded resolution. Record source resolution and effective export resolution separately. Inspect the final raster layer at its displayed size and in a crop; vector labels staying sharp can hide a blurred illustration.

Searching, downloading, preparing local assets, and building the requested figure are normal steps of authorized local figure work. Do not introduce another approval gate merely because an asset is generated, sourced from the web, or has had its background removed. External publishing follows the user's existing authorization and applicable source conditions; local figure preparation is not itself a publication action.
