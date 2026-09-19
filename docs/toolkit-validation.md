# Toolkit validation — 19 September 2026

## Scope and preservation

The revision adds a self-contained `paper-visual-design` front door, standalone graphs, and physical-point SVG assembly. It retains the existing foundation and integrates the six remote commits through `436ea49b7c677210ed67cf1c44624db6ff6a3068`, including qualitative comparisons, asset sourcing, connector routing, publication polish, manuscript-scaled typography, wrapping, legend/data occlusion, and PDF inspection. No existing paper examples were removed.

The skill's foundation is generated from `skills/paper-figure-creation`. Its instructions are preserved as `foundation/GUIDE.md` so a personal installation has exactly one discoverable `SKILL.md`. Checksums and the renamed source are recorded in `foundation-bundle.json`. The original skill remains separately usable.

## Executed checks

- **108 tests passed:** 89 existing checks after integrating the newer remote work, plus 19 graph/composition checks. These cover source-linked values and both axes, comparison context, missing values, uncertainty, conditional setup eligibility, coordinates, layout/occlusion, SVG import references, font scaling, raster resolution, and real export dimensions.
- The skill metadata validator passed in the actual personal-skills checkout. All local Markdown links resolve; the bundle matches the canonical foundation. There is one skill entry point.
- LoRA standalone graphs preserve all eight settings and both task metrics. SVG, PDF, PNG and actual-size PDF proofs were inspected. Leader labels clarify two close measurements without changing coordinates; a caption states validation and task-specific accuracy scope.
- SEAL standalone graphs and the hybrid teaser preserve all 15 Table 2 values. The generated notebook is illustrative; text, arrows, parameter symbols and plots remain editable vectors. Final minimum text is 8 pt; the inserted image is 586 ppi. PDF size, rendered appearance and grayscale were checked.
- A fresh agent used the new planner/method workflow with a primary LoRA source, without reading the example gallery. It selected the applicable method/deployment explanation, declined unsupported graph/setup jobs, considered three compositions, built original editable geometry, and inspected/repaired its exports. See [forward-task plan](../examples/lora-forward/figure-plan.md) and [review notes](../examples/lora-forward/review-notes.md).
- An independent reviewer inspected the graph/teaser pixels before reading design plans, then checked primary source values and scientific meaning. Repairs and reinspection are recorded in [the independent review](toolkit-independent-review.md).

## Concrete review repairs

1. Shortened narrow SEAL graph headers that touched in the first render.
2. Kept the same opening year throughout the constructed passage example.
3. Clarified that SEAL fine-tunes on the original passage **plus** the self-edit.
4. Added separated leader labels for nearby LoRA/AdapterH MNLI observations.
5. Added the LoRA validation/logical-form metric definition to the caption.
6. In the independent method task, moved a remote sum label next to its operator and clarified initialization wording.

No data jitter, invented uncertainty, favorable-only condition selection, or generated quantitative marks were used to solve visual problems.

## Limits

This is a targeted implementation and example evaluation, not a controlled study proving superiority over other agents or paper figures. The new reference review inspected five repositories, 20 source/license files and four rendered assets; earlier metadata retrieval is not represented as hundreds of close figure reviews. No venue template or manuscript integration target was supplied, so actual manuscript compilation and surrounding-page inspection were not performed. The new examples use SVG/source as their editable route; no new native draw.io export is claimed.

## Completion verification

The completion pass rebuilt the LoRA graphs and SEAL graph/composition exports,
reinspected the actual-size teaser and graph PDF proof, reran all 108 tests, and
checked the deterministic foundation bundle. The added regression rejects
log-scaled bars (undefined zero baseline) and log-scaled categorical positions
(which can hide the first category). Added research graph recipes cover
model-size/Elo comparability, component-ablation matrices, learning curves,
heatmaps, and distributions. No user-specific experimental measurements were
available or invented. The earlier independent review above remains the record
of that pass; these completion checks are a separate direct review.
