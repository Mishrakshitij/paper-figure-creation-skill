# Review figures and improve the skill

Review scientific integrity and visual communication separately. This is an authored review instrument, not a validated scale of design quality. Record the exact output version, source snapshot, intended physical width, reviewer and date. A successful script cannot establish that a figure explains the paper; visual polish cannot compensate for a false claim or wrong architecture.

## Scientific and production gates

Use `pass`, `fail` or `not_applicable` with an evidence note. A failure leaves the figure a draft.

| Gate | What to verify | Blocking example |
|---|---|---|
| Traceable results | Every plotted result maps to data or an exact published source location | A plausible baseline value was generated to complete the chart |
| Correct claim arithmetic | Named metric/direction/comparator; correct denominator and units | “30% better” confuses percentage points with relative change |
| Fair comparison | Declared comparison set and compatible protocol; qualifications shown | Different test splits, compute or metrics are ranked without disclosure |
| Honest chart geometry | Scales, transforms, aggregation and uncertainty match the evidence | Missing methods rendered as zero, fake error bars, misleading cropped bars |
| Correct method | Nodes, edges, losses, states and data access match the manuscript | Training labels appear as available inference inputs |
| Usable output | File opens; critical text/marks visible at intended size; no clipped glyphs | SVG exists but labels disappear in the exported manuscript PDF |

For digitized results, mark extraction as approximate and preserve source/extraction uncertainty. Do not silently convert approximate readings into precise headline claims. For synthetic examples, retain the synthetic label in the image, caption and metadata. If uncertainty is unavailable, disclose that fact instead of fabricating it.

NeurIPS asks claims in the abstract/introduction to match experimental scope, and asks authors to identify variability sources and error-bar calculation/meaning. These support provenance and uncertainty checks; they do not imply that every individual chart must show an invented interval. [NeurIPS checklist](https://neurips.cc/public/guides/PaperChecklist)

## Communication gates

Apply these to the intended reader and figure slot. They concern observed failures of understanding, not a mandatory illustration style. A simple symbolic diagram can pass; a richly illustrated diagram can fail.

| Gate | Evidence of success | Blocking failure |
|---|---|---|
| Recoverable visual thesis | A reader identifies the central relationship or supported comparison before studying minor labels | Every region has equal emphasis and the main point is unclear |
| Visible contribution | The reader can explain the changed operation or relationship from the diagram | The only explanation of novelty is the name or color of an opaque module |
| Meaningful representations | Chosen examples or symbols reveal the distinction needed to understand the task | Decorative documents, grids or icons suggest context but hide the actual operation |
| Recoverable correspondence | Repeated objects, paired alternatives and candidate-specific results can be matched | The reader cannot tell which result belongs to which candidate, input or state |
| Coherent reading path | Main flow, local detail and feedback can be followed at paper size | A callout looks like computation, or feedback obscures the forward route |
| Evidence-to-idea connection | A teaser's comparison tests the consequence the concept panel illustrates | The concept and attractive benchmark panels tell unrelated stories |

Record a specific observation for each applicable gate. If the figure does not need repeated objects, mark correspondence not applicable with a reason. Do not add icons, branches or panels simply to satisfy a checklist. If source-reference pixels were unavailable, distinguish that missing reference analysis from inspection of the newly rendered artifact.

## Inspect the rendered artifact

1. Inspect a thumbnail without reading small text. Identify the entry point, main grouping, emphasized relationship and outcome. This checks hierarchy, not small-label legibility.
2. Render the final PDF/SVG inside a page at the intended manuscript width. Inspect that page at final size for the worked example, reading path, comparison and labels. Judge density by whether these remain recoverable, not by counting objects.
3. Inspect a larger rasterization for overlaps, incorrect glyphs, clipped labels, arrow endpoints, unexpected rasterization and line joins.
4. Inspect grayscale. Where color carries essential distinctions, also examine an appropriate color-vision simulation. Do not call grayscale alone a complete color-accessibility test.
5. Cross-check values against the ledger and names/symbols against the manuscript. Trace one actual or explicitly schematic example through the diagram, including branches and shared state. Check that the figure does not present a schematic outcome as experimental evidence.
6. Check the same figure in the final manuscript PDF. Caption spacing and document rescaling can introduce problems absent from the standalone export.

Measure labels in final printed points, not just design-canvas pixels. Text overlap detection can flag geometry but cannot establish comprehension. Palette contrast tests cannot prove that thin marks survive printing. If visual inspection or the final manuscript is unavailable, record the relevant check as incomplete.

## Mode-specific questions

| Teaser | Method |
|---|---|
| Can a reader name the problem, specific intervention and supported result? | Can a reader identify the input, output and proposed computation? |
| Does the concept example actually expose the task's difficulty? | Can one example be traced through every scientifically meaningful branch? |
| Is the proposal linked across concept and evidence through name and encoding? | Is novelty localized inside the mechanism, not only named on an outer box? |
| Is approximately 60–70% of useful content area devoted to empirical evidence, or is deviation justified? | Are inference, training-only content, supervision and update paths correctly distinguished? |
| Do axis labels, conditions, comparator and uncertainty support the headline? | Are joins, repetition, dimensions, memory access and loss terms faithful to the paper? |
| Do complementary plots add different evidence without hiding unfavorable regimes? | Can a callout, crossing or bidirectional arrow be misread as a computation? |

## Record defects, not a substitute quality score

Keep a short review table with the observed misunderstanding, its consequence and a proposed repair. An aggregate score can conceal an opaque contribution behind good export or provenance scores. This workflow therefore uses separate gates and concrete observations as its acceptance record. If a study needs numerical ratings, define the rating protocol in advance and retain the individual judgments; do not interpret an internal threshold as proof of publication quality.

## Independent comprehension check

When a reviewer is available, show the figure at final size without the intended interpretation. Ask them to state the takeaway and identify what changes, rather than asking whether the figure looks good. For a teaser, ask which evidence supports that change and under what scope. For a method, ask them to follow one example, identify the updated state and explain the proposed operation. Then allow the caption for notation and conditions. Give the brief afterward and record discrepancies.

A five-second first-view prompt and a 30-second trace prompt are useful informal probes, not calibrated performance measurements. A self-assigned score is not an independent comprehension test. Report the reviewer’s actual answer and any disagreement instead of claiming that a figure “passes at a glance” solely because its creator understands it.

Ask about a plausible misreading suggested by the geometry: “Does the original passage reach the model at evaluation?”, “Which candidate receives this reward?”, or “Is this connector an input or a parameter update?” Do not prompt the correct interpretation before the reviewer answers. A reader who needs the author to explain the arrows has found a communication defect even when every edge is technically correct.

## Repair and stop

Fix the highest-impact observed failure first: incorrect science, then missing or ambiguous explanation, then legibility and polish. Re-render and recheck the affected criterion. A missing mechanism needs a new representation; an unclear relationship may need new grouping or aligned lanes; neither is repaired by recoloring boxes. Change the layout when repeated local fixes produce crowding. Preserve before/after views and a short revision record:

| Version | Observed failure | Change | Verification | Remaining limitation |
|---|---|---|---|---|
| v1 → v2 | Legend covers primary baseline | Move legend and enlarge plot | Baseline label and point visible at final width | Published source has no uncertainty estimate |

Do not change evidence inputs or weaken review gates while presenting the result as a purely visual improvement. Stop once applicable gates pass, no concrete material defect remains and further edits are cosmetic. If a missing source blocks a gate, finish a clearly marked editable draft and identify the unresolved source.

## Evaluating a skill revision

Use matched tasks with the same manuscript/data, model capabilities, target width and output requirements. Compare with-skill outputs against genuinely independent baseline outputs; do not deliberately author a poor baseline. Hold out papers from different method families and include missing-data or overclaiming prompts.

Blind condition labels and randomize review order when practical. Report structural/factual checks separately from subjective judgments. Preserve per-case outputs and concrete revisions. A small collection of examples demonstrates behavior; it does not establish general superiority, a quantitative gain in visual quality, or that hundreds of papers were visually reviewed.

The supplied Anthropic skill-creator demonstrates iteration on realistic tasks and comparison with a baseline, while Addy's review/constraint skills emphasize explicit criteria and evidence. These informed the workflow; they do not validate a particular diagram's quality. [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Addy review](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md), [Addy constraints](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md)
