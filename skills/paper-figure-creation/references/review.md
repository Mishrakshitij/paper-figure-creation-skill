# Review figures and improve the skill

Review scientific integrity and visual communication separately. This is an authored review instrument, not a validated scale of design quality. Record the exact output version, source snapshot, intended physical width, reviewer and date. A successful script or high aesthetic score cannot compensate for a false claim or wrong architecture.

## Blocking gates

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

## Inspect the rendered artifact

1. Render the final PDF/SVG inside a page at the intended manuscript width. Inspect that page at final size for readability and balance.
2. Inspect a larger rasterization for overlaps, incorrect glyphs, clipped labels, arrow endpoints, unexpected rasterization and line joins.
3. Inspect grayscale. Where color carries essential distinctions, also examine an appropriate color-vision simulation. Do not call grayscale alone a complete color-accessibility test.
4. Cross-check values against the ledger and names/symbols against the manuscript. Trace one actual example through the diagram, including branches and shared state.
5. Check the same figure in the final manuscript PDF. Caption spacing and document rescaling can introduce problems absent from the standalone export.

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

## Optional scored review

Score each dimension 0–4 and record why: 0 = absent/wrong, 1 = major defects, 2 = usable with material ambiguity, 3 = clear with minor defects, 4 = strong and verified. Weighted points = weight × rating / 4. For a genuinely inapplicable dimension, report it separately and normalize only the remaining weights; do not award free points.

| Dimension | Weight | A strong result |
|---|---:|---|
| Evidence integrity and scope | 25 | Source chain, correct arithmetic, transparent conditions and uncertainty |
| Scientific semantics | 20 | Correct computation and explicit proposed change |
| Immediate comprehension | 20 | Main problem/change/result or method route recoverable without explanation |
| Composition and final-size legibility | 15 | Readable hierarchy, aligned panels, deliberate spacing and little visual obstruction |
| Accessibility and consistency | 10 | Redundant encodings, adequate contrast, grayscale survival and useful alt text |
| Editability and reproducibility | 10 | Data/spec/source preserved and outputs regenerable |

A suggested internal target is all applicable gates passing, at least 85/100, and no applicable dimension below 3. This is a chosen quality bar, not evidence that a figure is objectively excellent. The core stopping condition remains that no concrete material defect is unresolved; do not run extra reviews merely to increase a score.

## Independent comprehension check

When a reviewer is available, show the figure at final size without the intended interpretation. Ask them to state the takeaway and identify the proposed change; then allow the caption and ask them to trace the method or interpret the comparison. Give the brief afterward and record discrepancies.

A five-second first-view prompt and a 30-second trace prompt are useful informal probes, not calibrated performance measurements. A self-assigned score is not an independent comprehension test. Report the reviewer’s actual answer and any disagreement instead of claiming that a figure “passes at a glance” solely because its creator understands it.

## Repair and stop

Fix the highest-impact observed failure first: incorrect science, then unreadable or ambiguous information, then composition and polish. Re-render and recheck the affected criterion. Change the layout when repeated local fixes produce crowding. Preserve before/after views and a short revision record:

| Version | Observed failure | Change | Verification | Remaining limitation |
|---|---|---|---|---|
| v1 → v2 | Legend covers primary baseline | Move legend and enlarge plot | Baseline label and point visible at final width | Published source has no uncertainty estimate |

Do not change evidence inputs or weaken review gates while presenting the result as a purely visual improvement. Stop once applicable gates pass, no concrete material defect remains and further edits are cosmetic. If a missing source blocks a gate, finish a clearly marked editable draft and identify the unresolved source.

## Evaluating a skill revision

Use matched tasks with the same manuscript/data, model capabilities, target width and output requirements. Compare with-skill outputs against genuinely independent baseline outputs; do not deliberately author a poor baseline. Hold out papers from different method families and include missing-data or overclaiming prompts.

Blind condition labels and randomize review order when practical. Report structural/factual checks separately from subjective judgments. Preserve per-case outputs and concrete revisions. A small collection of examples demonstrates behavior; it does not establish general superiority, a quantitative gain in visual quality, or that hundreds of papers were visually reviewed.

The supplied Anthropic skill-creator demonstrates iteration on realistic tasks and comparison with a baseline, while Addy's review/constraint skills emphasize explicit criteria and evidence. These informed the workflow, not the numerical weights above. [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Addy review](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md), [Addy constraints](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md)
