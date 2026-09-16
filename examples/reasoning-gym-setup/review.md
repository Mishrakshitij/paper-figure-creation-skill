# Review record

This is a guided, source-grounded example. It is not an independent user study or a blind test of the skill.

## Scientific check

- The task name, size 10, seed 42, first-entry animal counts, reference answer 4, and verifying-reference score 1.0 match the pinned README Quickstart.
- The model candidate is explicitly illustrative. The example does not claim an experiment was executed.
- The prompt is text; animal drawings are reader aids. The label and schematic note make this explicit.
- The reference and metadata feed the verifier. They do not feed the model.
- No environment interaction loop, reset function, training-feedback edge, dataset-wide score, or performance improvement is invented.
- The final note prevents a one-answer arithmetic example from implying that every Reasoning Gym task has a unique answer or binary string-match scorer.
- The library's broader RL role is acknowledged in the caption/brief but omitted from the chosen evaluation-only scope.

## Pixel review and repair

The author inspected the actual reference image `assets/examples.png` before designing this figure. Its use of concrete question/answer cards informed the choice to anchor the figure in one readable task. The source artwork is not reproduced here.

Three small composition alternatives were rendered and inspected before the detailed figure. The initial detailed render had two visible problems: a deer antler touched the question line, and the entry-stack pictogram collided with its label. The deer was resized and the stack/label were separated. The title spacing was also widened.

The repaired color figure, PDF-derived 110 dpi print proof, and grayscale proof were inspected. Labels are readable at the intended seven-inch footprint. The information boundary survives grayscale through spatial separation, explicit labels, and directed arrows. No label is outside the canvas, as recorded in `geometry-check.json`; that check does not substitute for visual review.

## Remaining scope limits

- This one task is deliberately simple; it does not depict the breadth or relative difficulty of the task collection.
- Task mixture, curriculum adaptation, train/evaluation splits, and paper-level aggregation are not shown because they are outside this selected interface explanation.
- The source is a pinned later README plus the paper's October 2025 revision; the drawing should not be presented as an exact reconstruction of the original paper's experimental configuration.

Independent review, when available, is recorded separately in the repository's benchmark review documentation.
