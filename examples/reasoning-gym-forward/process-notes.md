# Process, decisions and limitations

The source input was the supplied sources.json only. The applicable skill and its benchmark, story, art-direction, design, evidence, primitive, review and delivery references were read. No existing example figures, build scripts, briefs, reviews or expected outputs were inspected. No external visual reference was used.

Three original composition thumbnails preceded detailed drawing. The split generated-entry sheet was selected to keep a concrete task large while showing the question-only model route and complete-entry evaluator route. The animal vignette was drawn as original SVG paths; labels explicitly distinguish it from model input. Vector authoring kept the countable animals, labels and routes editable without a raster asset boundary. The canonical geometry source is build_figure.py; regenerate with Python and Inkscape. Do not independently hand-edit the export and then rerun stale geometry.

Outputs are 7 × 4.125 inches. The high-resolution PNG is 2100 × 1238 pixels at 300 dpi. The SVG has 34 live text objects and no embedded raster image. The smallest text is 8 pt at the intended width. No PDF was requested for this test.

Rendered pixels were inspected at 7-inch width (96-dpi proof), at larger resolution, at thumbnail size, and in grayscale. The first render showed the generator heading too close to its right boundary and the deer antler intruding into the question region. The heading was shifted and slightly reduced, and the deer was reduced/repositioned. The rerender preserves four distinct legs, question-to-model and complete-entry-to-verifier routes, readable access labels and separated arrows. Grayscale retains those distinctions through labels, geometry and the dashed field boundary; it is not a complete color-vision test.

Scientific limits: question wording is paraphrased from the source facts rather than transcribed from the README. Candidate 4 is illustrative. Score 1.0 is documented for the reference answer, not a measured model run. The figure does not specify difficulty values, model architecture, splits, aggregate metrics, training feedback or every task-specific scoring rule. Full primary sources were not re-fetched. No venue template or final manuscript placement was available, so this is a standalone paper-sized figure, not certification of submission compliance.


After review of the actual pixels, the parent noted that the target manuscript’s relation to Reasoning Gym was unspecified. The initial “Existing benchmark” label was an unsupported scope assumption. The initial PNG is preserved as before-scope-fix.png; only that on-canvas label was removed in the final render, and the brief now records the unresolved relation.

An independent reviewer saw paper-width-proof.png and then the caption without the brief or source facts. They identified the leg-counting task, text-only model input, illustrative candidate 4, and complete entry plus candidate reaching the verifier. They understood 1.0 as the documented reference-answer check after reading the caption and reported no visible collision. Their concrete ambiguity was: “the image alone could suggest that 1.0 is the displayed candidate’s evaluated result.” This limitation remains documented; the on-canvas qualifiers and caption are needed, and no measured model output is claimed.


A second bounded external-feedback repair made the candidate’s provenance explicit on the canvas: the footer now reads “Illustrative candidate; no model run. Scoring rules vary by task.” The caption explicitly retains “No aggregate accuracy is shown.” No other geometry or content changed in this repair. The original before-scope-fix.png remains unchanged. The final paper-width render was inspected after this footer replacement.

## Repository review repair

After copying this forward-test output into the repository, the root reviewer changed the configuration label from `size 10` to `10 entries` following independent feedback: dataset size could otherwise be confused with puzzle difficulty beside “Configurable complexity.” This is a third small external-feedback repair after the unsupported status label and no-run disclosure. The initial PNG remains unmodified; the final SVG/PNG were rebuilt from the updated label.
