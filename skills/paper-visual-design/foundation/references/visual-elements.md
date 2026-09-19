# Visual examples, icons, analogies, and generated assets

Use this for a new teaser or architecture figure, a visually flat diagram, or a request for richer paper graphics. Begin with the manuscript and implementation, then choose a visual representation that reveals the actual scientific operation. The aim is a figure that can be understood before every label is read.

## Choose a visual vocabulary for this paper

List the scientific objects the reader must track and assign useful representations. Keep object identity, geometry, and encoding consistent across panels.

| Object or relation | Useful visual element | Detail that earns the space |
| --- | --- | --- |
| An observed task | Actual simulator frame, dataset crop, or a labeled schematic scene | The object, target, and available observation |
| A history or trajectory | Filmstrip or small state sequence | Ordering, available past, executed actions |
| Appearance change | Matched images of the same state with a visible tint, mask, or exposure change | Physical state remains the same |
| Dynamics change | The same action with distinct schematic response arrows or trajectories | Action is controlled; response differs; schematic lengths are not measured results |
| Selection or attention | Repeated patches or tokens with a precise mask/selection overlay | Which identities survive and where they go |
| Latent alignment or calibration | Before/after coordinate sketch or feature strips with retained identities | What transformation changes and what it preserves |
| Frozen versus trained modules | Small lock or parameter-update glyph plus a text label | Weight state, distinct from whether activations vary |
| Iterative reasoning or planning | Candidate paths, a scoring operation, selected continuation | Which paths are imagined and which action is executed |

Draw original vector icons when the shape is simple; use a consistent stroke, viewpoint, corner treatment, and detail level. Label unfamiliar glyphs. Do not substitute decorative brains, robots, gears, or glowing networks for a specific mechanism. Existing icon assets may be used when their license permits the intended distribution; preserve attribution and source information. Do not use logos as a proxy for scientific evidence.

Choose a rich focal region and keep conventional encoders, configuration, and bookkeeping quieter. There is no universal icon count or required image quota. A numerical comparison may be clearest as a restrained plot with no illustration.

## Repair a text-heavy figure structurally

1. Identify the physical or scientific objects the reader should recognize before reading: a scene, a feature strip, a candidate set, a selected action. Allocate their area first. At final paper width, each important task frame must still show the task; token-sized thumbnails inside large text boxes fail this test.
2. Replace prose modules with visible operations: preserve identity across feature strips, branch alternative futures from one start, highlight a selected candidate, or repeat the same state under an appearance change. Symbols should encode a relation rather than serve as decoration.
3. Set a label budget appropriate to the figure (roughly 30–60 prose words for a compact overview is a useful starting point). Use short nouns/verbs instead of sentences. Keep necessary quantitative ticks, units, mathematical notation, and scientific distinctions even if the budget must increase.
4. Move implementation details to the caption or an existing method paragraph. A configuration list does not become an explanatory diagram when enclosed by rounded rectangles. Do not preserve the old layout merely because its arrows are technically correct.
5. Inspect with labels temporarily hidden or visually ignored. The reading direction, persistent example, change, and decision should still be recognizable. Compare the actual before/after pixels: a new palette, more whitespace, or added decorative icons alone does not resolve the failure.

Do not force this recipe onto an equation figure or an experimental plot. Evidence plots need reliable axes, comparison labels, uncertainty, and source traceability; embellishment must not obscure them.

## Use analogies with an explicit mapping

An analogy should teach a consequential distinction. Write down:

1. **Scientific relation:** the actual objects and operation.
2. **Analogy relation:** the familiar objects and operation.
3. **Mapping:** which parts correspond one-to-one.
4. **Limit:** what the analogy does not imply.

For example, separating a camera's colored filter from a surface's friction can illustrate observation versus transition changes. Keep the same scene and action recognizable; label the filter/response sketches as illustrative. This analogy does not establish learned causal identification, real-camera robustness, or a physical friction estimate.

For retrieval, a library lookup can explain selecting evidence, but should not imply that retrieved text becomes a weight update. For iterative editing, a marked-up document can expose a changed span, but should not imply the model sees an answer that is unavailable at deployment. Use an analogy only as far as its mapping remains faithful; put exact computation beside it when needed.

## Learn from references without copying the surface

Prefer figures in the provided manuscript, cited primary papers, official project pages, or sources supplied by the user. Inspect the actual visual before drawing lessons from it. Record a figure/page locator and the transferable idea: aligned branches, a persistent worked example, a useful inset, or a clear action/state loop. A paper title alone is not a visual reference.

Borrow the communication principle, then create original geometry and content for this method. Do not copy a paper's distinctive artwork or invent an inspected reference. If the source cannot be viewed, mark it uninspected and proceed with an original composition. A familiar visual style is useful only when it helps explain the present paper.

## Choose observed, vector, or generated imagery

Web-sourced imagery is also allowed: retrieve and inspect suitable project/model illustrations, official logos and icons, or other appropriately sourced assets. See [asset-sourcing.md](asset-sourcing.md) for search/download, background removal, identity preservation and asset metadata. Use [geometry-and-inspection.md](geometry-and-inspection.md) when adding these assets changes connector routing, spacing or text placement.

- **Observed evidence:** use original experimental outputs, simulator frames, or dataset examples when the image establishes what the system saw or did. Keep the selection rule, source identity, and crop. Never regenerate experimental evidence for aesthetics.
- **Original vector illustration:** prefer it when object geometry, ordering, token identity, or exact spatial relationships carry the explanation. Filmstrips, camera/filter icons, task silhouettes, and small coordinate sketches can be richer than a grid of labels while remaining fully editable.
- **Generated illustration:** use the available image-generation tool for text-free task vignettes, conceptual scene cutouts, or recognizable objects when these materially help explain the idea. Match the paper's restrained palette and viewpoint. Keep typography, axes, measurements, equations, masks, and architecture wiring in deterministic vector layers.

When generated imagery is selected, generate and inspect the actual asset, integrate the chosen asset, and render the complete figure. Do not finish with an unexecuted prompt or a flattened generated architecture diagram. If a tool or required input is unavailable, continue with an original vector example and report the limitation; do not invent successful generation.

An asset prompt should specify the explanatory subject, viewpoint, recognizable identities, restrained style, target crop, and space for overlays. Explicitly exclude text, plots, numbers, scientific arrows, and badges asserting success. For matched panels, reuse the same selected asset with deterministic crops/transforms instead of independently generating supposedly identical states. Do not use a photorealistic medical or robot image to imply an experiment that was never performed.

Follow [hybrid-authoring.md](hybrid-authoring.md) for asset authority and composition. Record the exact prompt, tool information actually available, selected file, checksum, dimensions, final display size, crop/transform, and illustrative status in the project. A rebuild must use the saved asset without requiring the image service. Caption generated content as illustrative wherever it could be mistaken for measured output; describe the deliverable as hybrid when it contains raster assets.

## Review explanatory value at the final size

Ask a reader to identify the task, the visible change, and the path through the method before providing the brief. Then check exact information access and compare their account with the source. A visually impressive picture can fail this check.

Inspect the focal region at thumbnail scale, the complete figure at manuscript size, and the exports enlarged. Check that icons remain recognizable, text is readable, arrows end on the intended objects, and images do not hide exact overlays. Preserve unfavorable results and all material comparison conditions. Remove an asset if it adds atmosphere but makes the scientific relationship harder to follow.
