# Design revision after the five reference papers

The first version emphasized evidence integrity and clean exports, but its examples frequently substituted labels for visual explanation. The user identified that shortcoming directly. The revised skill starts with the objects, transformations and relationships that make a particular paper understandable.

## Concrete changes

| Earlier behavior | Revised guidance and implementation |
| --- | --- |
| A conventional flowchart could become the final figure by default | Save a representation contract; choose the geometry that exposes the changed operation, persistent objects and reading path |
| Styling rules did more work than representation design | Use a concrete passage, code artifact, spatial scene, token identity, configuration or mathematical structure when its contents explain the method |
| A concept panel and chart could be merely adjacent | State what the example teaches and which experimental comparison measures its consequence |
| Good export/provenance scores could compensate for weak explanation | Review scientific integrity and communication through separate gates; remove the arbitrary 85/100 acceptance score |
| Uniform module shapes constrained the drawing vocabulary | Add portable semantic-object helpers and an editable illustrated reference sheet; keep custom composition available |
| A broad corpus count could suggest an achieved quality level | Record actual pixel inspections and concrete misunderstandings; assess the new drawings directly |

The [reference ledger](../research/reference-upgrade/README.md) covers ten author-hosted figure assets across the user's five papers, plus SEAL's algorithm. It distinguishes actual pixels from caption-only or inaccessible figures. It does not claim that all pages of those PDFs were inspected.

## Four new figure examples

| Example | What a reader can now follow | Observed repair |
| --- | --- | --- |
| [MAE method](../examples/mae-v2/figure.png) | One original landscape, four retained patch identities, packed visible inputs, position restoration, lightweight decoding and masked targets | Separated crowded restoration labels; added mask-token hatch redundancy and explicit random selection; clarified the shared learned mask token |
| [SEAL teaser](../examples/seal/seal-teaser.png) | A fictional passage becomes a learned edit, changes model weights and supports recall without the passage; three knowledge settings and filtered ARC provide evidence | Made the training-only reward return visible; bolded the actual best value in each setting, including the two settings where GPT-4.1 data leads |
| [SEAL method](../examples/seal/seal-method.png) | Candidate edits independently adapt copies of one policy; task outcomes and edit records control the next policy update | Added the context/edit/reward record; distinguished applying a configuration from treating configuration text as training data |
| [WMRL method](../examples/wmrl/wmrl-method.png) | Candidate groups split into paired anchor scoring and predicted scoring; a fitted correction precedes two gradient streams | Moved the split to the group objects; separated fitting from applying the calibration map; replaced an unreadable fusion fraction with explicit weights and a merge |

The [earlier MAE figure](../examples/mae-method/figure.png) remains available beside the redesign. This is a same-paper authored comparison, not an independent with/without-skill benchmark. The previous MAE figure includes a recognition lane; the new one deliberately scopes itself to pretraining to spend more space on representations and the main computation.

SEAL's 19 plotted values were checked against the v2 paper tables, including unfavorable comparisons and the oracle. The project-page result prose differs from the newer table, so the table is the numerical authority. No experimental outcomes were invented to make the new figures persuasive. MAE's scenes and SEAL's teaching passage/grids are explicitly schematic; WMRL's code sample is illustrative. The new method figures report no newly run experiments.

## Review evidence

A separate reviewer first interpreted the images without captions, code, briefs or the intended reading. Its [versioned review](independent-v2-review.md) records what it understood, the ambiguities it found, and the rechecks after repair. This is independent comprehension feedback from an agent, not a human usability study or a blinded comparison against another workflow.

The creator and primary agent also inspected actual rendered pixels, enlarged images, paper-width previews and PDF rasterizations. Grayscale proofs are included. The new exports are fixed-width 7-inch drafts with editable SVG text and vector PDF. The existing 49 numerical/renderer tests pass, and the revised skill passes its packaging validator. These checks establish bounded technical behavior; they are not an aesthetic score.

The updated skill calls for structural alternatives when a complex composition is unresolved. Because that instruction was added during this revision, the MAE and SEAL storyboard comparisons were made after their initial renderings. Their briefs record that timing; they are not retrospectively described as pre-draft experiments.

## Practical limits

The actual manuscript and venue template were not supplied. Figure heights vary with the explanation, and a single-column placement would require redesign. Full manuscript integration, a color-vision simulation and human reader testing have not been completed. Caption-level details remain necessary for exact reward selection, the ARC success unit, and WMRL's estimator normalization.

These custom examples use code plus SVG as editable sources. The new examples do not include native draw.io files; the earlier starter still exports them with its documented application-rendering limitation. Source paper artwork is not redistributed.

The revision demonstrates a more specific visual workflow and records real repairs. It does not establish a quantitative increase in figure quality, universal superiority, or an automatic guarantee of submission-ready output.
