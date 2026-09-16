# Benchmark and environment figure landmarks

Reviewed 2026-09-16. This purposive sample covers **15 works** and **six actual pixel inspections** of official repository assets. Nine additional cases were read for their benchmark contracts; they are not counted as visual inspections. The separate monthly-paper study supplies recent Hugging Face discovery. These are useful design precedents, not a claim that popularity proves visual quality.

The machine-readable [ledger](landmarks.json) records source URLs, version scope, exact image Git blob hashes, factual anchors, observations, and limitations. No original artwork is redistributed.

## What the six inspected images teach

| Precedent | What the pixels communicate well | What an original figure should improve |
|---|---|---|
| [WebArena overview](https://github.com/web-arena-x/webarena/blob/main/media/overview.png) | A contained world, external task request, action/feedback loop, independent functional evaluation. | Replace some domain logos with one actual state change; show what the agent can observe. |
| [VisualWebArena overview](https://github.com/web-arena-x/visualwebarena/blob/main/media/overview.png) | Repeated webpage/goal pairs; image evidence inside the goal makes the need for vision tangible. | Give the success criterion its own compact space. |
| [OSWorld infrastructure](https://github.com/OS-World/OS-World.github.io/blob/main/static/images/environment_infrastructure_.png) | Configuration highlights correspond to setup, retrieval, postprocessing, and metric components; containment explains responsibility. | Reduce source-code density at publication width; retain only the fields needed to understand the example. |
| [SWE-bench teaser](https://github.com/SWE-bench/swe-bench.github.io/blob/master/img/teaser.png) | Issue plus repository becomes a changed repository; a before/after test matrix defines success. | Separate task construction from solving when explaining benchmark creation. |
| [ALFWorld teaser](https://github.com/alfworld/alfworld/blob/master/media/alfworld_teaser.png) | A text transcript and embodied frames make the abstraction boundary visible. | Clarify correspondence without suggesting one text action equals one motor action. |
| [ToolBench overview](https://github.com/OpenBMB/ToolBench/blob/master/assets/overview.png) | Construction, training, and inference use different paths; the dataset persists as a concrete artifact between stages. | Include training only when the paper contributes it; benchmark-only figures should not inherit the full pipeline. |

The strongest common feature is a **visible contract**: what arrives, what can be done, what changes, and how the result is checked. A room screenshot, website collage, or collection of domain icons can establish setting, but cannot by itself explain that contract. The new figure type therefore needs a task instance and an evaluator, with clear ownership of the information each receives.

## Three distinct compositions

**Interactive environment.** Place a concrete world or interface at the center. Show the current observation reaching the agent, an action altering state, and the next observation returning. Put task initialization and the final evaluator on separate paths. WebArena, OSWorld, ALFWorld, and continuous-control settings differ in action semantics; the diagram should preserve those differences.

**Benchmark construction.** Show source material becoming candidate tasks, then annotated or validated instances, then the released split or task package. Draw acceptance and rejection conditions if they are consequential. A small retained instance should display the public input and the evaluator-only reference. SWE-bench and BrowseComp show why viability, difficulty filtering, and final scoring must not be merged.

**Task suite or static evaluation.** Show representative task types around a shared evaluation contract, not a fake environment loop. GAIA has questions and optional attachments whose answers can require tools; this does not make the benchmark a fully resettable simulator. AgentBench combines domain-specific interactions, so the shared interface and score aggregation must be explicit.

All three can be combined when the paper actually contains both construction and environment contributions. Use neighboring panels with one shared task instance. Do not add construction gates, held-out splits, stochasticity, agent memory, private state, or feedback that the source never specifies.

## A verified interactive fixture: WebArena task 601

The original [paper](https://arxiv.org/html/2307.13854v4) explains the environment contract in Sections 2.1–2.4, evaluation in Section 3.2, reset in Appendix A.2, and original baseline termination in Appendices A.6/A.9. The [v0.2.0 task file](https://github.com/web-arena-x/webarena/blob/v0.2.0/config_files/test.raw.json), Git blob `91e88d7c3bce867b7f7608c8229c84b7be11ef1e`, contains a concrete Reddit task, ID 601.

| Field | Source-backed interpretation |
|---|---|
| Goal | Publish the question “is car necessary in NYC” in the appropriate forum. |
| Initial context | Logged-in Reddit user; start at the site's root. |
| Agent observation | Browser URL/tabs and focused-page content. The original text baseline uses accessibility-tree element IDs. |
| Available interaction | Browser actions such as click, type, scroll, tab operations, and URL navigation. |
| Site change | A new post is created; a compact demonstration may show the post form and resulting post. |
| Evaluator | Check the resulting URL against `/f/nyc`, then inspect the post body for the requested question. |
| Exact implementation | `url_match` plus `program_html`; the locator reads `.submission__inner` text at the resulting post URL. |
| Reset | This instance has `require_reset: false`; the environment provides reset machinery when needed. |
| Termination | The agent can issue `stop`; the original baseline also imposes an experiment-specific transition budget and early-stop rules. |

An original drawn UI, arbitrary element IDs, or a shortened trace must be labeled **schematic**. They are not a recorded benchmark trajectory. The setup figure should not imply that evaluator queries or reference checks appear in the agent's observation, nor that the private checker grants capabilities unavailable through browser actions. The v0.2.0 file has a pre-existing duplicate-line syntax defect elsewhere; the task above was inspected as a bounded source record, not obtained by silently repairing the full dataset.

## Additional text-grounded cases

The ledger includes [AgentBench v0.2](https://github.com/THUDM/AgentBench/tree/v0.2), [GAIA](https://huggingface.co/datasets/gaia-benchmark/GAIA), [tau-bench v1](https://arxiv.org/html/2406.12045v1), [BEHAVIOR-1K](https://arxiv.org/abs/2403.09227v1), [Procgen's ICML proceedings](https://proceedings.mlr.press/v119/cobbe20a.html), [DeepMind Control Suite](https://github.com/google-deepmind/dm_control/tree/main/dm_control/suite), [Terminal-Bench 2.0's ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html), [BrowseComp's official release](https://openai.com/index/browsecomp/), and [WebShop](https://github.com/princeton-nlp/webshop). Their setup facts diversify the design rules; none is labeled pixel-reviewed.

Important distinctions exposed by these sources include simulated user dialogue versus tool responses, train/test level generation versus episode execution, reference solutions versus agent inputs, observations versus simulator state, and single-run success versus repeated-run reliability. In particular, tau-bench's `pass^k` is not `pass@k`.

## Scope and access limits

Official project pages, repositories, dataset cards, and conference proceedings were used alongside papers. OpenReview's SWE-bench forum presented a browser challenge; the official project page supplied accessible source facts. The AgentBench image fetch returned metadata without image content, so it was not counted as inspected. GAIA's gated data was not accessed or copied. Exact source images remain with their owners.

These observations motivate design rules and concrete example figures. They do not establish measured comprehension improvement or justify selecting a paper only because it has many votes.
