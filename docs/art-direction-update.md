# Art direction and optional hybrid illustration

This revision responds to the observation that image-generated visuals can feel more engaging than a correct but uniformly boxed diagram. It adds decisions about composition and representation before rendering: a focal relationship, recognizable object structure, a visible transformation, purposeful spatial arrangement, selective depth, and a rhythm of detailed and quiet regions.

These are design hypotheses tested on concrete examples. The update does not assert that image generation is inherently better, that adding imagery always helps, or that the skill has a measured aesthetic advantage.

## What changed

The [art-direction guide](../skills/paper-figure-creation/references/art-direction.md) applies across the three existing figure modes. It asks what object and change deserve the first glance, then uses silhouettes, proximity, contrast, local detail and whitespace to support that relationship. It gives different devices for masking, editing, assembly, environment actions and controlled comparisons. It avoids making every object a card or every diagram three-dimensional.

The [hybrid-authoring guide](../skills/paper-figure-creation/references/hybrid-authoring.md) adds an optional route for illustrative assets. Image generation can provide a teaching scene; deterministic code supplies authoritative labels, masks, branches, axes and quantitative marks. The selected asset and prompt stay with the build source. Rebuilding a figure does not require calling an image service again.

The main skill routes to these references selectively. Its three scientific modes, evidence requirements and conditional benchmark/environment trigger remain unchanged. Actual clickable or animated interaction is a separate optional companion, not a property claimed for a static image.

## What was tested

| Case | Design change | Scientific boundary |
|---|---|---|
| [WebArena](../examples/webarena-v3/) | Larger overlapping browser states form the focal group; the agent and site taxonomy receive less attention; action is close to its target | Same task 601 and functional URL/DOM checks; original schematic UI and step, no execution or performance claim |
| [MAE](../examples/mae-hybrid/) | A generated natural scene supplies recognizable image content inside exact patch masking and restoration geometry | Illustrative input only; symbolic predictions, source-grounded vector computation and masked-only loss; no model run |

The [initial audit](art-direction-audit.md) inspected actual pixels from the previous WebArena, ReasoningGym and MAE examples. It found scientifically meaningful objects but insufficient distinction in visual weight between task, configuration and conventional machinery. The new examples are guided redesigns, with alternative composition thumbnails and source/review notes preserved beside their exports.

The MAE asset was created with the built-in image-generation tool. Its [exact prompt](../examples/mae-hybrid/assets/generation-prompt.txt) and selected image are included. The tool did not expose a model version, so none is inferred. A 600-pixel JPEG was derived for figure use from the generated 1254-pixel square scene; this is an export optimization, not an observed dataset image. The main figure remains hybrid: text and scientific geometry are editable vectors, while scene pixels are raster.

## Review and limits

The [independent review](art-direction-independent-review.md) records interpretations from pixels before consulting the design briefs, then compares the old and new figures at the same physical width. Gains and regressions are recorded individually rather than hidden behind an aggregate aesthetic score. A source-preserving visual redesign is distinct from a narrowed figure scope; contextual information moved to captions is identified.

Scientific and visual checks remain separate. One initial MAE label, “score 12 / 16,” could be mistaken for accuracy even though it referred to positions contributing to loss. It was flagged for replacement with explicit masked-slot language. This illustrates why visually attractive annotations still require semantic review.

The MAE redesign changes both input artwork and output representation: the earlier schematic reconstruction is replaced with symbolic prediction slots. Any perceived improvement therefore cannot be attributed solely to the generated scene.

The examples do not test a complete image-generated scientific diagram against a vector baseline. They test vector art direction and an illustrative generated asset inside precise graphics. No reader study or controlled superiority evaluation was performed. Standalone exports can be reviewed; final placement in a target manuscript remains untested.

## Independent forward test

A separate agent used the updated skill and the ReasoningGym provenance ledger to create an actual [SVG/PNG figure](../examples/reasoning-gym-forward/) without viewing the previous figure, drawing code, briefs or reviews. The resulting composition puts the complete generated entry and larger original animal illustrations at the center, with separate model and verifier routes. It is a vector-only result; the skill did not force image generation into a task that could be drawn accurately with simple paths.

Three targeted changes followed external review: remove an unsupported “Existing benchmark” label when the target-manuscript relation was unspecified; state that no model was run; and replace `size 10` with `10 entries` so dataset length is not confused with difficulty. The [initial preview](../examples/reasoning-gym-forward/before-scope-fix.png), final output and process notes preserve this distinction. The unassisted first result is not represented as flawless.

This test uses curated source facts, not an unseen full manuscript. One agent and one task cannot establish generalization or a causal improvement over the old skill. It supplies concrete evidence that the new instructions can produce an independently authored pictorial layout, and exposes assumptions worth correcting. The benchmark guide now defines new/adapted/existing relative to the target manuscript.

The skill package validator passes and the existing 61 code tests still pass. No renderer logic was changed in this revision. The custom WebArena illustration's JSON contract retains a documented failure of the legacy synthetic-data label guard: its exact wording check is not treated as proof of correctness or silently marked passed. The custom SVG workflow instead preserves source-contract review and explicit on-canvas schematic labeling.
