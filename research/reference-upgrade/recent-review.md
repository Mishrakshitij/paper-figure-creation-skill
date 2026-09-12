# Visual review: StudentSim and WMRL

Reviewed 2026-09-12. These are two of the user's five requested reference papers. The review below concerns actual pixels of author-maintained repository assets, with figure identity and page mapping checked against the paper's extracted PDF text. It is **not** a claim that complete PDF pages were rendered or inspected. No source artwork is redistributed here.

## Inspection record

| Paper | Asset visually inspected | Paper correspondence | Retrieval identifier |
|---|---|---|---|
| [StudentSim](https://arxiv.org/pdf/2609.01591), v1 | [fig_motivation.jpg](https://github.com/microsoft/StudentSim/blob/main/figures/fig_motivation.jpg) | Figure 1, printed page 2 | Git blob `ce4a44351b12a01bc35c3b8e4b4fb896df678c72` |
| StudentSim | [fig_metrics.jpg](https://github.com/microsoft/StudentSim/blob/main/figures/fig_metrics.jpg) | Figure 2(a), printed page 2 | Git blob `b33000887cc2b4e76b8e674cab5f72564307f0da` |
| StudentSim | [fig_performance.png](https://github.com/microsoft/StudentSim/blob/main/figures/fig_performance.png) | Figure 2(b), printed page 2 | Git blob `335b702aae348c3e993265a42232e7d48ae6101c` |
| [Scaling Automatic Research Agents via World Models](https://arxiv.org/pdf/2608.12564), v3 | [assets/teaser.png](https://github.com/xiyuanyang45/WMRL/blob/main/assets/teaser.png) | Figure 1, printed page 1 | Git blob `c0ac277986e5de75a8f4d95e50fc53c8508a32a3` |
| WMRL | [assets/method.png](https://github.com/xiyuanyang45/WMRL/blob/main/assets/method.png) | Figure 2, printed page 4 | Git blob `205dd9ceb6b5f287824c277e8fe27246bf1eaf16` |

StudentSim's `fig_training_pipeline.jpg` was identified and Figure 3's caption/text were read, but its 3.32 MB repository file returned empty binary content through the available file endpoint. A separate blob endpoint could not decode the JPEG. **No pixel-based assessment of that training figure is claimed.**

For the v1 comparison, the actual rendered repository files `examples/mae-teaser/figure.png` and `examples/transformer-method/figure.png` were viewed, and the skill's design-system and method references were read.

## StudentSim: the example teaches the metric

**Figure 1, motivation asset.** The visual argument begins with recognizable actors: teacher, real learner, simulated learner. Two feedback routes make the substitution legible. Blue binds real feedback to the slow/costly/sparse constraints; purple binds the simulator to the returning proxy-feedback route. The two learners share pose, book, and confused expression, making behavioral resemblance visible before the caption is read. The clock, currency, and sparsity symbols turn abstract constraints into distinct visual objects. The wide return arrow closes the practical loop back to the tutor.

Transfer the actor correspondence and feedback route, rather than copying the character artwork. For a new figure, a consistent small original vector actor can carry the same identity. Decorative similarity alone would fail: the important relationship is that the simulated learner substitutes for a specific learner's feedback.

**Figure 2(a), metric asset.** This is a worked example with four explicit states: human before/after and simulator before/after. Both rows show the same incorrect positive answer to a negative multiplication problem and the same corrected negative answer after guidance. Vertical dotted links mean matching; horizontal dotted arrows mean transition. These different geometric directions carry the distinction between the two evaluation criteria. Expressions reinforce state, while speech bubbles expose the exact response being compared. The example is doing explanatory work that a pair of boxes labeled “fidelity” and “responsiveness” could not do.

**Figure 2(b), performance asset.** The scatterplot reuses the two quantities just taught. Three directly labeled methods occupy three easy-to-compare regions. Marker shape and hue reinforce identity; labels identify baseline families as well as models. The proposed method's upper-right position answers the conceptual question introduced by the example. Exact plotted chess values are StudentSim (0.51, 0.91), prompted GPT-5.4 (0.23, 0.72), and Maia2 (0.45, 0.27). These are a particular domain comparison, not universal cross-domain coordinates.

**Why this matters for the skill.** Concept and chart are not merely adjacent. The concept panel establishes the semantics of the chart axes. Require an explicit sentence in the design brief: “This visual example teaches ___, which is measured by ___ in the evidence panel.” If that sentence is weak, revise the storyboard before styling.

Potential production improvements should remain distinct from the transferable idea: the asset's pale italic secondary labels can be weak at small size, and the large character drawings may consume too much room in a narrow paper layout. The lesson is semantic correspondence, not that every scientific diagram needs cartoons.

## WMRL: the layout exposes two different bottlenecks

**Figure 1, teaser asset.** Three panels progressively change scale: group-level RL overview, one trajectory's concrete contents, then the compute bottleneck. A fan-out turns one question into several candidate solutions, while alternating code and execution-output cards explain what happens inside those trajectories. Syntax-colored code, progress bars, timestamps, and a final score make “generation” and “execution” perceptually different. Those miniature artifacts are specific to automatic research; a generic document icon would lose that distinction.

The right panel uses aligned mini-plots and a shared capacity reference to show why one resource becomes limiting. Blue identifies generation in both the example and plot; warm orange identifies real execution. The method's alternative appears in the corresponding position with green. A highlighted capacity intersection gives the reader an explicit place to look. These curves are explanatory schematic curves in this overview; the figure does not supply a table of measured series behind them. A new skill output must label such a curve as schematic and must not turn it into reported numerical evidence.

The visual density is high but organized. Each panel answers a new question, each subobject has a clear role, and the same colors recur with the same meaning. Dashed vertical separators partition reasoning steps, rather than wrapping every label in another box.

**Figure 2, method asset.** Rows encode groups; alternating actor/environment objects encode interaction turns. The anchor group has paired real-environment and world-model rows, while other groups have only the predicted route. The extra row makes the costly exception visible. Two horizontal omissions preserve repetition without drawing every group or turn. Rewards then pass through a separate correction region, and corrected gradient streams meet in the final fusion region. Three footer phrases state the problem and the two interventions: bias/noise, bias correction, variance correction.

The layout distinguishes the scientific objects—trajectories, reward scalars, a learned correction function, gradient estimates—and places the function where it transforms rewards. Color alone is not expected to describe the operator. The repeated object vocabulary also lets the reader see which stage changed while the other stages remain comparable. Gray fat arrows and shadows are visible styling choices, but they are not the scientific reason this figure works.

**Why this matters for the skill.** A method figure should represent multiplicity, shared context, expensive exceptions, and data-type changes when these explain the proposal. A single row of “generate → score → update” boxes hides precisely the mechanism the paper contributes. Design should start from those relationships, then choose primitives and routing.

## Concrete shortcomings in the viewed v1 outputs

| v1 observation | Why it underperforms against these references | Required change |
|---|---|---|
| MAE concept shows an anonymous patch grid and the sentence “Reconstruct what is missing,” but no before/after visual content | The reader must imagine both the input and the reconstruction operation | Include a legitimate recognizable example, or an original clearly labeled schematic object with spatial identity preserved across masking and reconstruction |
| Transformer overview substitutes uniform labeled blocks for nearly every object | Input tokens, attention relations, feature transformations, and resulting text have little visual distinction | Depict token objects and one attention relationship where they teach the contribution; keep operations as operations rather than making all nouns into boxes |
| V1 overview omits residual wiring and moves that omission into a subtitle | A scientifically consequential relationship is not learned from the drawing | Select a scope that can show the necessary relation; use a purposeful inset or one complete representative block |
| Both examples devote large strips to title, subtitle, and footnote prose | Many pixels explain what should be visible, while the central diagram remains sparse | Move ancillary conditions to the caption; spend reclaimed area on concrete examples, mechanism detail, and readable chart content |
| The design guidance emphasizes avoiding decoration and exporting editable shapes | These are useful production constraints but do not select a compelling representation | Add a representation-design stage before styling, with explicit checks for object identity, before/after change, multiplicity, and concept-to-metric correspondence |

## Actionable principles for the next iteration

1. **Draw what the method operates on.** Choose at least one semantically meaningful object—token span, trajectory, board, image patch, response, reward pair—not a generic “input” rectangle. Use source-backed examples or label constructed examples as illustrative.
2. **Make the contrast visible in aligned states.** Preserve identity and position across baseline/proposed or before/after views. Change only the element that explains the proposal, then connect that change to a measured outcome.
3. **Let geometry carry distinctions.** Rows can mean groups or actors; columns can mean states or phases. A repeated layout is valuable when repetition is part of the method. Do not reduce every topology to a single pipeline.
4. **Use a few content-specific primitives consistently.** Code card, execution log, reward token, model, and calibration operator should look like different objects. Avoid building a large ornamental icon collection unrelated to the paper.
5. **Connect explanation to evidence.** Reuse the problem's dimensions in the plot axes or show exactly which measured quantity corresponds to the changed operation. Numerical claims must still trace to comparable reported experiments.
6. **Distinguish schematic explanation from measured evidence.** If a capacity curve or qualitative trajectory is drawn to explain a mechanism, label it. Reserve factual performance marks for source-backed values.
7. **Review design before production.** Ask a reviewer to identify the actors, intervention, why it helps, and evidence connection from the figure alone. Legible text and valid SVG are necessary but cannot answer those questions.

These observations support a design upgrade; they do not establish measured superiority of a new skill, and they do not imply that copying an author's exact artwork is the appropriate solution.
