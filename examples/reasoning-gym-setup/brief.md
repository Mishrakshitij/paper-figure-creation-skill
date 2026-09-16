# Figure brief

- **Mode:** benchmark/environment setup.
- **Eligibility:** present. Reasoning Gym introduces procedural reasoning task generators and verifiers; this setup is a material contribution, described in paper §2.
- **Setup family shown:** procedural generation with single-turn evaluation. The source calls these reasoning environments, and supports RL training; the selected drawing shows the evaluation interface, not the entire training system.
- **Claim:** an entry separates the question exposed to a model from the reference and metadata used by a task-specific verifier.
- **One unit:** one generated leg-counting question and its candidate answer.
- **Construction:** `leg_counting`, `size=10`, `seed=42`, otherwise default configuration, as in the pinned README Quickstart. The drawing expands the first generated entry, not all ten.
- **Model-visible input:** the text question. Wording is condensed into the question line and quantity labels. The two animal pictures are explanatory artwork for readers, not images passed to the model.
- **Evaluator-held input:** reference answer and generated metadata. This is the chosen evaluation flow; the library also makes entries available to a caller for other purposes.
- **Candidate:** illustrative answer `4`, not a measured output from a named model.
- **Scoring:** the task's `score_answer` checks the candidate against the entry. The README asserts that verifying the reference answer yields `1.0`. The single displayed score is not an aggregate metric or a performance comparison.
- **Observation/action/state loop:** not applicable to this selected single-turn path. Do not invent reset, step, tool, or persistent-world interfaces.
- **Training reward:** omitted. The paper's training reward can include format components; this figure does not equate training reward with evaluation accuracy.
- **Generalization limit:** other tasks may have several valid solutions and task-specific scoring. Do not infer universal binary scoring or string equality from the numerical example.
- **Figure footprint:** 7 × 4.15 in; body labels 8.5–9.5 pt; editable vector artwork.

## Composition decision

Three composition thumbnails were rendered before the detailed figure:

1. **Two information lanes:** setup forks into a visible question and evaluator-held reference; the candidate crosses into evaluation. Selected because the separation of information is the main setup fact.
2. **Construction funnel:** good for explaining task mixtures and dataset assembly, but the model/reference boundary receives less space.
3. **One-entry magnifier:** emphasizes task readability, but collapses generator configuration and verification into a weak sequence.

The selected layout uses a concrete question to make the benchmark tangible, then follows that same entry to verification. Color is redundant with spatial lanes, labels, and arrow direction. A dashed line separates the model-visible upper path from the evaluator-held lower path. Configuration remains outside those lanes because it belongs to the caller, not the model's input.

## Scope and source versions

The discovery page is June 2025; the inspected paper is arXiv v2, 20 October 2025. The detailed API/example comes from README commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7`, read on 16 September 2026. This is a documented interface study, not a claim that the later README exactly matches every experiment in the earlier paper.
