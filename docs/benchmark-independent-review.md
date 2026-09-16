# Independent review of benchmark setup figures

This review begins with rendered pixels, before reading each figure's caption, brief, source ledger, or build script. The review uses each full figure and its available 7-inch print proof. The final manuscript and surrounding paragraphs were not available, so integration into a paper has not been verified. No numerical quality score is assigned.

## WebArena: first reading from pixels

Reviewed `examples/webarena-setup/figure.png` and `examples/webarena-setup/print-proof.png` before reading author explanations. The initial interpretation was sent to the coordinating agent before source comparison.

- **Task and system:** A web agent completes user tasks on self-hosted shopping, forum, code-hosting, and content-administration sites, with auxiliary tools and reference sites. The concrete task is to ask an appropriate forum whether a car is necessary in New York City.
- **Inputs, actions, and observations:** The goal and current page are the agent's inputs. The shown interaction occurs after earlier navigation and typing. The agent sees a prepared new-post form and issues `click [42]` to submit it. The footnote explains that observations can contain URL/tabs plus a screenshot, HTML, or accessibility tree.
- **Change and persistence:** The current form becomes a submitted question in `/f/nyc`. A return arrow labels the changed website state as the next observation. Persistence across later steps is implied by the state change and feedback loop; it is not separately labeled.
- **Checker and success:** The completed episode supplies its final URL and post DOM. Evaluator-only checks require the correct forum and the requested question. Both must pass for success.
- **Visibility:** The evaluation region separates reference checks from the agent's interaction. The screenshot-like page and numbered target mix two visual conventions; the footnote explains that `[42]` illustrates an accessibility-tree target. The agent does not appear to receive evaluator-only reference checks.
- **Legibility:** No obscured text, crossing arrows, or clipping was apparent in the initial print proof. The footer carries the smallest text and the observation-format distinction depends on reading it. The main interaction remains comprehensible without it, but the precise observation representation does not.
- **Evidence limits:** The footer explicitly identifies the UI, element ID, and sequence as illustrative and says no agent was run. This review does not treat the pictured success as an experimental result. No grayscale proof was available at the initial review.

### Caption and source-contract comparison

After recording the initial reading, reviewed `caption.md`, `brief.md`, `source-ledger.json`, and `setup-contract.json`, then the available grayscale print proof.

- The visible task, question string, target forum, final-URL/post-content checks, and conditional success agree with the pinned task-601 contract recorded in those documents. This is comparison with the accompanying source ledger, not a second independent retrieval of the upstream repository.
- The figure's abbreviated episode omits login/start configuration, the task's `require_reset: false`, and an explicit stop action. The brief and caption explain the after-navigation scope; those omissions do not change the shown transition or checker. The figure should not be reused as a complete episode specification without those qualifications.
- The caption explicitly states that different valid action sequences can satisfy the functional checks. The figure shows one illustrative click and does not encode that click as the required reference trajectory.
- The caption distinguishes the synthetic UI/target/trace from source-backed evaluation criteria, consistent with the pixel-only reading.
- In grayscale, the agent loop and evaluation lane remain distinct through labels, layout, the divider, and arrow direction. The forum selection retains bold type. Meaning does not depend solely on blue, teal, or ochre.
- A localized repair was requested and accepted: replace the low-information sublabel `one allowed action` beneath `click [42]` with `accessibility target`, so interpretation of the target ID does not depend entirely on the footer. The final color and grayscale print proofs were inspected: the replacement is legible, fits without collision, and resolves this concern. No further repair was requested.

## Reasoning Gym: first reading from pixels

Reviewed `examples/reasoning-gym-setup/figure.png`, `print-proof.png`, and `grayscale-proof.png` before opening caption, brief, source ledger, or build script. The print proofs are rendered at 110 dpi at the intended 7-inch width. The author readiness note mentioned a repaired collision and the `TEXT QUESTION` label before inspection; no source documents or intended data-flow explanation were read. The initial interpretation was then sent to the coordinating agent.

- **Task and system:** A procedural `leg_counting` task generator, configured with seed 42, size 10, and default parameters, produces ten entries. One selected entry asks for the total legs of one sea slug and one deer.
- **Inputs and output:** Only the question goes to a reasoning model. The model returns illustrative candidate answer `4`. The task verifier receives that candidate together with the reference entry and returns score `1.0`.
- **Change and persistence:** This is a generate–answer–verify setup. It does not depict an environment whose state changes after an action, and there is no invented observation/action loop. The figure does not claim that generation updates the model or that verification is fed into training.
- **Checker and success:** The reference answer is `4`; metadata records animal counts. A task-specific `score_answer` verifier gives the shown candidate a documented score of `1.0`. The footer warns that other tasks use their own verifiers and can accept multiple valid solutions.
- **Visibility:** A labeled dashed boundary and separate routing hold the reference answer and metadata with the evaluator. The model receives only the question. The animals are explanatory drawings of a text question; both the header and footer identify the input as text.
- **Legibility:** No overlap, clipped label, or ambiguous crossing was found in the inspected proofs. All the main flow labels and the footer remain readable in the supplied print-size rendering. Grayscale removes color distinctions but preserves the question/reference access boundary and the input paths into the verifier.
- **Evidence limits:** The figure calls candidate `4` illustrative and its `1.0` score documented; it does not establish that a particular model produced the answer. The full text question appears condensed into a short question plus quantity labels. The caption should explicitly identify that condensation or quote the full source prompt.

### Caption and source-contract comparison

After recording the initial reading, reviewed `brief.md`, `caption.md`, `sources.json`, and the author's `review.md`. Re-inspected the final PDF-derived color print proof and grayscale proof.

- The brief and ledger identify the same task, seed, dataset size, selected animal counts, reference answer, and documented verification result that were visible in the pixels. They trace the concrete example to a pinned README snapshot. This review compares the drawing with that ledger; it does not independently rerun the generator or retrieve the upstream snapshot.
- The source documents specify that the expanded entry is the first of ten. The drawing says one selected example, which is compatible but less specific. This does not change the illustrated evaluation unit.
- The caption now explicitly says the question wording is condensed into the short prompt and animal-count labels, resolving the initial fidelity concern. The animal pictures are described as reader aids, consistently with the visible `TEXT QUESTION` label and schematic note.
- `HELD BY EVALUATOR` describes the selected evaluation flow. The brief acknowledges that the library exposes full entries to its caller; the drawing should not be reused to claim that the API itself enforces secrecy or that all callers withhold answers.
- The paper revision and pinned later implementation snapshot are identified separately. The result is a documented interface explanation, not an exact reconstruction of the paper's earlier experiment. The candidate and score qualifications prevent an illustrative correct answer from becoming a claim of measured model accuracy.
- The omitted RL training loop, reward-format terms, curriculum, task mixture, and train/evaluation split are explicit scope limits. The picture does not imply a training-feedback edge or a universal verifier.
- The final PDF-derived print proof retains readable labels and the animal/count separation. The grayscale proof retains the visibility boundary and routing. No further picture repair was requested after the caption clarification.

## Disposition and limits

Both final figures have been inspected at their declared seven-inch width in color and grayscale. The initial readings distinguish an interactive website state transition from procedural single-turn generation and verification. The two review findings were addressed: WebArena moved the accessibility-target explanation into the interaction area, and Reasoning Gym's caption identifies the condensed wording.

No remaining overlap, clipping, or ambiguous information-flow edge was found in the final inspected proofs. This does not establish how the figures fit a final manuscript, whether a smaller reproduction remains legible, or whether an experiment was executed. Final manuscript placement remains unreviewed.
