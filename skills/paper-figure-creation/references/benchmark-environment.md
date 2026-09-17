# Benchmark and environment setup figures

Read this only after the setup-presence decision in SKILL.md. This third mode answers: **what task is evaluated, in what setting, with what access, and what counts as success?** It can explain a newly proposed benchmark, an adapted setup, or a substantive existing environment used in the paper. Preserve that distinction. Benchmark scores and model internals belong in this figure only when needed to explain the setup; they usually have separate teaser and method homes.

## Establish eligibility and scope

Record `present`, `absent` or `unclear`, with a manuscript or primary supplement location. A section specifying task construction, environment interactions, an executable test protocol, or a concrete evaluation workflow supports `present`. A table listing ImageNet, MMLU or SWE-bench results does not, by itself. Do not use a title keyword or the mere existence of experiments as the gate.

Use `absent` when the supplied manuscript scope explicitly contains no eligible setup; use `unclear` when relevant source material is missing or only an unsupported setup claim is available. Both leave the mode unselected. These labels describe the available evidence, not an assertion about unseen pages.

When setup information is partial, distinguish omission in the figure from absence in the source. Read the relevant supplement or official implementation when available. If the paper has an eligible setup but omits an important detail, label it unresolved in the brief; omit an unsupported visual assertion. An explicitly requested speculative design must remain an illustrative proposal, never a reconstruction of a published setup.

Classify new, adapted or existing **relative to the target manuscript**, not the age of a public benchmark or the fact that it has a repository. If no target-manuscript relation is established, record that uncertainty in the brief and omit an unsupported novelty/status label from a standalone explanatory figure. Do not invent a relation simply to satisfy a renderer field.

Use the actual task as the unit of explanation: one question, repository issue, household episode, multi-turn conversation, simulation run, or generated artifact. Avoid mixing an individual episode, a dataset split and the final leaderboard into a single unlabeled flow.

## Extract the setup contract

Complete [benchmark-brief.md](../assets/benchmark-brief.md) before composition. Use source descriptions rather than plausible defaults. The following fields are a reasoning aid; only applicable fields belong on the canvas.

| Contract | Questions to resolve | Visual consequence |
|---|---|---|
| Scope and provenance | What is new? Which paper/release/configuration defines it? | Label new, adapted or existing setup; freeze terminology and counts to one version |
| Task population | Where do instances come from? Human annotation, mined artifacts, generation, simulation? Which filtering/validation stages matter? | Small construction strip, selected example, optional split boundary |
| Unit of evaluation | What begins and ends one case? Is a run a single task or a chain? | One persistent case identity across the figure |
| Visible information | What prompt, files, scene, history, tools, policies or reference material can the system access? | Concrete input objects inside a clearly labeled access region |
| Actions or outputs | Text answer, patch, tool call, UI action, physical motion, media artifact? | A readable payload, not an arrow labeled only “interaction” |
| State and transition | What changes after an action? What persists? Is observation partial or delayed? | Before/after state or a local transition inset; observation distinct from full state |
| Initialization and stopping | What is sampled/reset? What carries across episodes? Time, tool, turn or resource budget? | Initialization and stop markers; do not invent a universal reset or horizon |
| Evaluator access | Which targets, tests, database fields, rubrics or future frames are unavailable to the tested system? | Separate evaluator lane and explicit reference route |
| Scoring and aggregation | What is checked? Outcome, intermediate constraints, trajectory, human judgment? How do per-case scores combine? | Show the actual check and score unit; use aggregation only if it clarifies the protocol |
| Controls | Which splits, difficulty settings, agent interfaces, seeds or versions change, and which stay fixed? | Aligned variants or compact configuration strip |

For noninteractive tasks, actions, state transitions and reset can be not applicable. For dynamic worlds, distinguish agent time, simulator time and delayed events if that distinction affects evaluation. For benchmark construction, distinguish generation-time validation from the later evaluation of a tested model.

Do not assume everything outside the agent is private: a policy, webpage, test file or simulator field may be visible in a particular setup. Do not assume all evaluation is exact match, all tests are hidden, or every task yields a binary reward. Trace the source's actual information access and metric.

## Choose a visual grammar

Sketch three distinct compositions for a new complex figure, then choose the one that best exposes the setup's defining difficulty. Use the fewest panels that preserve the important relationships. These are alternatives, not a fixed panel checklist.

| Setup family | Effective composition | Concrete objects to show |
|---|---|---|
| Static or procedural benchmark | Construction across the top; one generated example below; model output and task-specific evaluator on separate routes | Source artifact, configuration/seed, question, reference, candidate, check |
| Interactive software or tool environment | Environment boundary with before/action/after; agent adjacent; private evaluation below | Browser view, issue/patch, tool payload, changed record, tested condition |
| Embodied or spatial environment | Scene/map centered; local observation inset; action and changed scene; goal/constraint check | Reachable objects, visible field, motion, goal region, forbidden condition |
| Multi-turn or multi-agent task | Short aligned lanes for roles, messages/actions and evolving shared state | One conversation turn, tool result or shared artifact; role-specific visibility |
| Construction pipeline | Same task identity through sourcing, design, validation and release, plus a final worked instance | Real artifacts that change at each stage; explicit rejection/filter gates |
| Controlled environment variants | Repeated aligned cases with fixed interfaces and selective emphasis on what changes | Same reset/action/observation interface, changed rule or observation |
| Evolving or delayed-feedback world | State snapshots or timeline with distinct event and agent clocks | Persistent state, release changes, delayed effects, outcome horizon |

A setup can fit more than one visual family. Choose its primary composition by the figure's central question, then use a subordinate inset for the second concern. The JSON schema's narrower `family` field describes execution semantics (static, interactive or mixed), not the chosen visual composition.

**Static/procedural recipe.** Show a compact source or generator configuration and one resulting task. Branch the public question toward the tested model and the reference toward a task-specific verifier. Carry the model's candidate to the verifier. If the paper reports multiple task-specific scoring functions, label this example's rule and state that the broader benchmark varies. A static benchmark does not need a fabricated action/observation loop.

**Interactive recipe.** Start from one task intent and recognizable state. Show a specific action payload and its local effect. Return the next observation to the agent using a distinct directed route. Put private outcome checking outside the agent loop. Include only the initialization, persistence and stopping details necessary to understand this task. A generic agent↔environment double arrow rarely explains enough by itself.

**Construction plus execution recipe.** Use a small upstream strip for how tasks are built, then devote the main area to one evaluated case. Link the strip to the selected case by identity. Keep model evaluation separate from task-quality validation. If construction itself is the contribution, reverse the emphasis and make the runtime example an inset.

**Controlled variants recipe.** Align the same example, actor and interfaces across conditions. Highlight the changed rule, resource, observation or transition. Do not move every object between panels: the reader should see what changed without repeatedly consulting a legend. A version-to-version change is not an action within an episode; name the time axis.

## Make the task visible

Replace abstract nouns with the smallest scientifically useful object: an actual issue and changed code line, a short form with a submitted value, a grid before and after a move, a generated question and answer rule, or an audio/video prefix with its prediction boundary. Use original vector redraws or properly attributed example assets. Simplified interface geometry should be labeled schematic; do not imply a stylized UI is an observed screenshot.

Preserve identity across panels. The post, file, object, task ID or generated sample being evaluated must be recognizably the one the system acted on. Limit example text to the portion that reveals the challenge or criterion. Give the success test a concrete object to inspect: final database state, produced patch, response string, constraint set or recorded trajectory.

Use a stable visual vocabulary within the paper:

- A neutral task/input color; a distinct tested-system color; a restrained environment/state color; an evaluator/reference accent.
- Region labels and line styles in addition to color. “Model-visible input” and “Evaluator-only reference” should remain understandable in grayscale.
- Solid directed arrows for actual data or action flow; clearly labeled thin/dashed connectors for explanatory links or references. Do not rely on dashed lines alone to define privacy.
- A stop marker after the last applicable action; an output score without a feedback arrow unless the source feeds it back. If the figure also covers training, give training feedback its own labeled path.

Colors need not match these suggested roles across unrelated papers; meanings must remain stable within related figures. Keep captions and arrows consistent with the manuscript's actor names. A benchmark judge may itself use models: distinguish those evaluator models from the system under test.

## Sources of useful design patterns

These examples motivate authored design guidance, not universal requirements or a ranking of figure quality. Inspect their actual images if using them as visual references; an accessible README does not establish that its images were inspected. Bind details to a specific source version.

| Primary reference | Transferable idea | Misreading to prevent |
|---|---|---|
| [WebArena](https://github.com/web-arena-x/webarena) | Concrete websites and task intents, browser interaction, programmatic outcome checks | Treating success as matching one reference action sequence |
| [OSWorld](https://github.com/xlang-ai/OSWorld) | Task configuration, running computer environment and evaluation infrastructure in separate regions | Confusing the observation with all underlying machine state |
| [ReasoningGym](https://github.com/open-thought/reasoning-gym) | Task families taught through actual input/answer examples; configurable procedural generation | Inventing a dynamic environment or a single universal scoring rule |
| [TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany) | Recognizable workplace roles and tools combined with checkpoint evaluation | Compressing all progress into an unexplained final checkmark |
| [EnterpriseOps-Gym](https://github.com/ServiceNow/EnterpriseOps-Gym) | Construction stages separated from a concrete tool-and-record episode | Omitting policy constraints or confusing task validation with agent success |
| [MerchantBench](https://github.com/KhanCold/merchantbench) | Persistent business state, order lifecycle and different feedback delays | Collapsing simulator time and agent decision time |
| [SocialOmni](https://github.com/MAC-AutoML/SocialOmni) | Full-context perception versus prefix-only interaction | Leaking future context through a visually shared input |
| [EnvHarness](https://github.com/google-research/envharness) | Aligned reset/action/observation interfaces across controlled variants | Changing layout and terminology so much that the intervention disappears |
| [EvoArena](https://github.com/Aiden0526/EvoArena) | Repeated task/world snapshots make evolving conditions visible | Drawing release changes as if they were ordinary agent actions |

Monthly Hugging Face lists can help discover candidates across dates and fields. Record the dated list, observed vote count and retrieval date; votes can change and indicate attention, not scientific validity or visual quality. Follow the paper/project to verify facts and inspect pixels. Do not infer layout from an abstract or an AI-generated summary. Separate metadata screening, primary text reading and actual visual inspection in any research report.

## Build and verify

For the bundled engine use `kind: "benchmark"` and a `benchmark_setup` contract; see [spec-format.md](spec-format.md) and [benchmark-template.json](../assets/benchmark-template.json). The template is visibly synthetic. The validator rejects absent/unclear eligibility and incomplete declared contracts; it cannot prove that the declaration matches the paper. Node visibility is review metadata, not automated information-flow verification. Custom vector compositions remain appropriate when a concrete environment cannot be expressed by the starter's nodes.

Review actual pixels at final width. Ask a reviewer, initially without the brief:

1. What is one task, and what must the tested system produce or accomplish?
2. What can it see, and what actions or outputs can it choose?
3. What changes or persists? For a static task, is the absence of an interaction loop clear?
4. What does the evaluator inspect, and what counts as success or partial credit?
5. Which information is private, and is any arrow liable to imply that it reaches the tested system?
6. What is new in this paper versus existing infrastructure?

Then check the answer against the source contract. Inspect reset/termination, timing, split boundaries and aggregation where applicable. A figure with polished icons but an unexplained evaluator fails; a simple sample-to-verifier diagram can succeed. Repair concrete misunderstandings and record them. Distinguish rendered-figure review from final-manuscript placement, which may still be unavailable.

The caption should name the setup and version, define the selected task, explain input/action/observation and scoring, identify schematic elements, and state any omitted scope. Do not claim measured performance or universal task coverage from a single illustrative case.
