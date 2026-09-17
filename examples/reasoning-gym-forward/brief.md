# Figure brief and representation contract

- **Reader / slot:** AI-paper reader; benchmark setup; 7-inch-wide two-column figure, no specific venue supplied. Planned height approximately 4 inches.
- **Eligibility:** present. Supplied source ledger cites arXiv v2 Section 2 for generators, controls and algorithmic verification, and the pinned README Quickstart / Training interface for the actual example and evaluation call.
- **Status:** target-manuscript relationship is unspecified. The initial figure treated Reasoning Gym as existing infrastructure from the perspective of this explanatory request; that was an assumption, so the on-canvas “Existing benchmark” label was removed before delivery. The source ledger alone does not establish whether the target manuscript proposes or uses the benchmark.
- **Source snapshot:** arXiv 2505.24760v2 (2025-10-20); README commit 49b07130b3fcd12f2d064bba7c43869543a0e7e7. Their dates are not combined with the discovery month.
- **One sentence:** A configurable procedural generator creates questions with evaluator references, allowing a model's answer to be checked using the complete generated entry.
- **Task population / construction:** procedural tasks with task-specific complexity configuration. Concrete task leg_counting, size 10, seed 42.
- **Evaluation unit:** one generated question and one candidate text answer. Selected first entry contains one sea slug and one deer, with reference answer 4.
- **Model input:** question text only in the documented evaluation interface. No images, answer field or metadata are shown reaching the model.
- **Candidate:** illustrative response 4. It is not measured model behavior.
- **Evaluator input:** candidate answer and complete entry (question, answer, metadata). Answer and metadata are not sent to the model in this depicted interface.
- **Scoring:** task-specific algorithmic verification. The reference answer has documented score 1.0. This is a reference-answer check, not a model accuracy result. No aggregate, universal binary reward, universal string matching or training feedback is claimed. Some tasks admit multiple valid solutions.
- **Interactions / stopping:** static question-answer example; interactive states, resets and action loops do not apply. No inference or training budget is supplied.

## Representation contract

**Visual thesis:** One concrete generated task has two information routes: its question goes to the model, while its complete entry and the model's candidate meet at a task-specific verifier.

**Focal relationship:** The animal-counting question becomes an answer, then receives a reference-backed check. The text and original vector animal vignette make the task recognizable; the question arrow originates beside the text, not the illustration.

**Objects:** A generated-entry sheet holds a paraphrased question, a clearly labeled original schematic animal illustration, and a separately labeled evaluator-only reference band. The conventional model is compact. Its response is a distinct answer slip, not a performance chart. The verifier explicitly receives both candidate and complete entry.

**Invariants:** The entry identity, example animals and answer value remain the same through both branches. Dark solid arrows are actual interface data flow. Dashed separation and explicit labels denote withheld entry fields, not a training signal.

**Reading path:** Construction settings → generated-entry sheet → model → candidate → verifier; reference route follows beneath the model path.

**Novelty:** No novelty relation to the target manuscript is asserted. The diagram explains the sourced Reasoning Gym setup.

**Detail boundary:** No task catalogue, split, aggregation, model architecture, training loop, difficulty parameter values or accuracy claims. The question is a faithful paraphrase of the ledger rather than an unverified exact quotation. Animal artwork is explanatory and is not a model input.

**Evidence:** Only the supplied sources.json is used. No existing figure, build script, brief, review or expected answer was inspected. The source ledger's account of an author image was not treated as an image personally inspected in this test.

## Three composition sketches

See composition-sketches.svg. These were authored before detailed drawing.

1. **Split generated-entry sheet (selected):** Large task sheet on the left; question/model/candidate across the upper route and the complete entry/verifier below. Gives the recognizable example the most room while keeping access boundaries explicit.
2. **Horizontal assembly line:** Configuration, generated entry, model and verifier in four columns with a long reference bypass. Quicker left-to-right overview, but at 7 inches the actual task and candidate become small and the reference route dominates.
3. **Access lanes:** Top model-visible lane and bottom evaluator lane share a small task source at left. Strong privacy separation, but splits the concrete entry and makes the animal question secondary to the lane architecture.

**Authoring choice:** Native editable SVG generated deterministically by a standalone Python script, with original vector animal shapes. Raster image generation would add an asset boundary without improving this simple countable scene. All text, geometry and routes remain editable.
