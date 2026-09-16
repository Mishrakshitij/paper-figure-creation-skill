# Earlier Hugging Face monthly selection: benchmark and environment figures

Reviewed on **2026-09-16**. This slice covers **19 papers from five monthly indexes**, with **five actual author-image inspections**. The remaining entries are primary-source abstract or setup screens. It is not an exhaustive monthly survey or a claim that every selected paper has excellent figures. The companion [JSON ledger](hf-earlier.json) records per-paper URLs, review depth, source versions, votes, and image fingerprints.

## Discovery and source discipline

The accessible monthly pages were [June 2024](https://huggingface.co/papers/month/2024-06), [December 2024](https://huggingface.co/papers/month/2024-12), [March 2025](https://huggingface.co/papers/month/2025-03), [June 2025](https://huggingface.co/papers/month/2025-06), and [December 2025](https://huggingface.co/papers/month/2025-12). Their visible vote counts guided discovery, followed by selection for different task mechanics. Votes measure community attention, not correctness or visual quality.

Counts in the ledger are those visible in the retrieved **monthly index**, potentially cached, not historical month-end counts. Paper detail pages sometimes differed: BigCodeBench showed 50 on its detail page versus 47 in the monthly index; XLand-100B showed 89 versus 88. We preserve the index values instead of silently treating these views as one live snapshot.

| Paper | Monthly index | Visible votes | Setup distinction | Review |
|---|---|---:|---|---|
| MultiFinBen | 2025-06 | 94 | Languages, modalities and task difficulty | Primary abstract |
| DeepResearch Bench | 2025-06 | 74 | Research reports plus two evaluator families | Abstract and author README |
| Reasoning Gym | 2025-06 | 74 | Procedural tasks and task-specific verification | Full-text setup, README, pixels |
| VS-Bench | 2025-06 | 58 | Multi-agent visual games | Abstract, author site, pixels |
| SWE-Factory | 2025-06 | 54 | Construction of executable issue tasks | Primary abstract |
| Mind2Web 2 | 2025-06 | 52 | Live search with task-specific judge agents | Abstract and author README |
| AmbiK | 2025-06 | 47 | Paired ambiguous kitchen instructions | Primary abstract |
| Creation-MMBench | 2025-03 | 48 | Image-conditioned creativity and instance rubrics | Primary abstract |
| LEGO-Puzzles | 2025-03 | 35 | Visual questions versus assembly planning | Primary abstract |
| SPIN-Bench | 2025-03 | 34 | Planning, games and negotiation | Primary abstract |
| ProcessBench | 2024-12 | 87 | Earliest erroneous reasoning step | Primary abstract |
| TheAgentCompany | 2024-12 | 51 | Workplace software, colleagues and checkpoints | Author README and pixels |
| XLand-100B | 2024-06 | 88 | Learning histories in a reused environment | Primary abstract |
| MMLU-Pro | 2024-06 | 57 | Revised static questions and answer options | Primary abstract |
| BigCodeBench | 2024-06 | 47 | Function specification and execution tests | Abstract, author README, pixels |
| CRAG | 2024-06 | 46 | Factual QA with mock retrieval APIs | Primary abstract |
| DAComp | 2025-12 | 160 | Engineering and analysis with different judges | Abstract, author README, pixels |
| Envision | 2025-12 | 94 | Causally ordered image generation | Primary abstract |
| NL2Repo-Bench | 2025-12 | 52 | Requirements and empty workspace to repository | Primary abstract |

Primary links and the individual design inferences are in the ledger. Protocol details absent from this screen, especially held-out splits, budgets, stopping conditions and score aggregation, must be checked in the source before producing a figure.

## What the inspected figures teach

### Reasoning Gym: show a specimen, not only a category name

The [author example image](https://github.com/open-thought/reasoning-gym/blob/49b07130b3fcd12f2d064bba7c43869543a0e7e7/assets/examples.png) uses three colored category columns. Each contains an actual question and response: logic wiring, numeric grids, rendered text or game notation. Concrete problem content makes the task recognizable before reading prose.

For a new figure, borrow that specificity, not the original dense page of text. A small generator/configuration area can feed one large worked question; the target answer and metadata belong beside the verifier. The [official interface](https://github.com/open-thought/reasoning-gym/blob/49b07130b3fcd12f2d064bba7c43869543a0e7e7/README.md) distinguishes question, answer, metadata and response scoring. Some tasks admit multiple valid solutions, so a universal equality-to-one-gold-string diagram would be false.

### TheAgentCompany: connect capabilities to concrete surroundings

The [architecture image](https://github.com/TheAgentCompany/TheAgentCompany/blob/98b68ef82a47690c316f42fddb05baafaab56851/docs/images/TAC_architecture.png) integrates three things: a workplace populated by applications and colleagues, an agent with separate action and observation arrows, and role-specific task examples. A small worked checkpoint strip explains scoring.

This is a strong pattern when the evaluation depends on changes in an external environment. Keep the task instruction, working environment and assessor distinguishable. A drawing should not imply that checkpoint feedback is available during an episode unless the protocol actually exposes it.

### VS-Bench: distinguish task population from evaluation mode

The [current overview](https://github.com/vs-bench/vs-bench.github.io/blob/04dc9c284b1779c541096611cb84627a6ae4c074/website/img/overview.png) groups actual game views by interaction type, then uses a separate column for perception, prediction and online decision-making. That separation prevents one large collection of game pictures from standing in for an explanation of the evaluation.

The same visual world can support different tasks. Draw what the agent sees and what it must produce for each protocol. A next-action prediction example is not an environment rollout. The model-logo column is less transferable: in a space-constrained setup figure, concrete task content is usually more useful than a roster of evaluated models.

### DAComp: preserve one example through different artifact types

The [task overview](https://github.com/ByteDance-Seed/DAComp/blob/027ccaf20f0d3743d9291fd575d9bc785a5fe3db/assets/dacomp.png) grounds the benchmark in a business question, then shows a design document, SQL repository, repository changes, and an analytical report. The same example maintains continuity while the object shape changes.

The portable principle is to explain task families through the artifacts they require. The [paper](https://arxiv.org/abs/2512.04324) distinguishes execution-based engineering assessment from rubric-based analysis assessment; a new diagram should preserve that distinction. Decorative agent cartoons and miniature result plots are optional, not the reason this figure communicates.

### BigCodeBench: expose the task contract

The [author task specimen](https://github.com/bigcode-bench/bigcode-bench.github.io/blob/81f563565f3c8e63d2baacec0fcbc5c0500e45e6/asset/task.png) is a code-window view containing a signature, docstring, requirements and examples. It makes the input contract tangible, though it is not itself a full evaluation diagram.

For a benchmark figure, retain a short meaningful excerpt and pair it with the candidate code artifact and execution-test evaluator. Clearly distinguish Complete and Instruct prompt formats if both matter. Do not draw the evaluator's tests as model input without protocol evidence.

## A reusable design grammar

The design should answer **what an item is, what the model receives, what it can do or return, and how success is decided**.

| Setup family | Dominant visual object | Relationships worth drawing | Common misrepresentation |
|---|---|---|---|
| Static benchmark | One concrete input/output specimen | Task pool → visible item → response → assessor | Adding a fictitious interaction loop |
| Procedural benchmark | Generator controls plus worked item | Configuration/seed → item; answer/metadata → verifier | Calling generated examples a fixed dataset split without evidence |
| Interactive environment | Scene, browser or tool workspace | Goal → agent; action ↔ observation; final state/trace → judge | Making privileged state or reward visible to the agent by accident |
| Benchmark construction | Source artifacts and acceptance gates | Acquisition → annotation/filtering/validation → released tasks | Merging authoring, training and evaluation into one pipeline |
| Multi-agent setting | Distinct participants and information surfaces | Shared state, private observations, action exchange | Giving all agents the same information implicitly |
| Open-ended evaluation | Candidate artifact plus criterion structure | Candidate + reference/rubric → evaluator → defined score | Treating subjective criteria as exact ground truth |

These are alternatives to combine only when necessary. A benchmark figure does not inherit the introduction teaser's concept/result area ratio. Its job is to explain the evaluation setup; result charts belong in it only when they support that job.

## Activation and fidelity implications

- Activate this third figure mode when the paper actually defines a benchmark, dataset evaluation protocol, testbed, simulation, or substantive environment setup that needs explanation.
- An algorithm paper that merely lists standard benchmark scores does not need an extra benchmark figure.
- Reused environments can warrant an environment figure when the setup is essential, but the figure and caption must identify what is reused and what the paper contributes. XLand-100B illustrates this distinction.
- Avoid inventing hidden tests, splits, reset conditions, action limits, seeded sampling, human judges, or reward access. Use only verified protocol details.
- Label illustrative tasks as illustrative. A synthetic worked example can clarify mechanics without being misrepresented as an actual dataset item.
- Draw outputs using their real form: code patch, ordered frames, error index, report with citations, action sequence or database state. Uniform text boxes erase these distinctions.

## Version and access findings

The currently inspected VS-Bench asset has **ten environments and three evaluation modes**, consistent with its [April 2026 revision](https://arxiv.org/abs/2506.02387v3). The June 2025 HF abstract still describes eight environments and two evaluation dimensions. Likewise, LEGO-Puzzles' [August 2026 revision](https://arxiv.org/abs/2503.19990v4) adds an explicit planning set beyond the earlier HF description. A figure must be tied to one paper/protocol version.

DeepResearch Bench's repository README was readable, but its framework image returned an empty payload through the connector. It is recorded as text-only, not counted among the five visual inspections. Original author images are fingerprinted and linked, not redistributed.
