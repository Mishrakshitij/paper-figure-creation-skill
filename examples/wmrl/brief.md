# WMRL method figure: design brief

This is a **guided reference-based design exercise**, created after inspecting the user's supplied WMRL paper and its author-maintained figure assets. It is an original explanatory composition, not an official figure or an independent blind test of the skill.

## Scientific scope

Source: [Scaling Automatic Research Agents via World Models, arXiv:2608.12564v3](https://arxiv.org/pdf/2608.12564v3), 10 September 2026. Method locations: Section 3.1 and Equation (1), printed page 4; Section 3.2 and Equation (2), pages 4–5; Section 3.3 and Equations (4)–(5), pages 5–6; Figure 2, page 4. The figure source examined as pixels was the [author repository method asset](https://github.com/xiyuanyang45/WMRL/blob/main/assets/method.png), blob `205dd9ceb6b5f287824c277e8fe27246bf1eaf16`.

The model generates groups of candidates. Each group contains at least two trajectories. Every group receives predicted rewards; approximately 10% of groups also receive real-execution rewards. Paired predictions and real outcomes fit an online monotone calibration map. The real rewards supply the anchor-group gradient stream, and calibrated predictions supply the other-group stream. An inverse-variance combination forms the policy update.

The task label and code are constructed explanatory examples. They are not benchmark records, released experiment outputs, or measured model behavior. The figure contains no performance chart. The approximate anchor fraction is a method setting supported by Section 3.3, footnote 2, rather than an improvement claim.

## Representation contract

| Scientific object/relation | Drawn object | Purpose |
|---|---|---|
| Research task | Short concrete question card | Establish the agent's practical task |
| Agent policy | Original vector model glyph and explicit policy notation | Separate an actor from a data object |
| Candidate solution | Stacked code sheets with a marked illustrative snippet | Show that the method grades executable research candidates |
| Group multiplicity | Three stacked group tokens, indexed first/second/last | Preserve groups as objects distinct from individual trajectories |
| Anchor exception | A region containing both a terminal-shaped real sandbox and a world-model globe | Show why a small subset costs more and supplies ground truth |
| Paired reward data | Explicit `(prediction, real reward)` set | Make shared candidate identity the calibration input |
| Correction function | Separate fit and apply operations, with only paired anchor data entering fit | Prevent ordinary predicted rewards from appearing to train the calibrator |
| Training streams | Two aligned reward → advantage → gradient strips | Preserve which rewards actually update each group |
| Variance correction | Explicit inverse-variance multipliers and a sum/normalize merge | Show the second contribution at a readable size; preserve the full normalization in the caption |

Blue identifies policy/generated candidates, orange real execution, green predicted or corrected world-model scores, and purple calibration/fusion. Direct labels duplicate every color meaning. Arrows indicate information flow; no unlabeled gradient arrow is mixed with data flow. Mathematical gradient objects are explicitly named.

## Composition and intentional simplifications

The 7 × 3.92 inch figure uses three reading stages, with most vertical space allocated to the exceptional anchor route and the two corrections. It avoids the source figure's long alternating interaction rows and instead exposes one concrete generated artifact, followed by the group-level correction machinery.

Multi-turn internals are condensed. The source's within-group normalization, variance-estimation warmup, running residual statistics, and update loop return edge are deferred to the paper and caption. The update follows the conceptual inverse-variance form in Equation (5), not a claim that the implementation receives oracle variances. `g_E` and `g_WM` are sums of group gradient estimates. The figure says so explicitly; the full denominator appears in the caption.

Main labels are approximately 8–8.5 pt; support labels are 7–7.5 pt. The illustrative code is 6.5 pt and the mathematical weight operators are 9.8 pt. A one-column version would require redesign. An actual venue's manuscript dimensions have not been supplied.

## Design decision

The reference's transferable strength is how it reveals paired scoring, correction, and stream multiplicity. The new figure preserves that semantic structure while adding a concrete candidate artifact and a different composition. It does not copy the author's robot, globe, color values, shadows, layout coordinates, or image pixels.
