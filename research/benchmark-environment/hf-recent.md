# Recent benchmark and environment figure research

Snapshot: 2026-09-16. Discovery used the actual Hugging Face monthly lists for [March](https://huggingface.co/papers/month/2026-03), [June](https://huggingface.co/papers/month/2026-06), [August](https://huggingface.co/papers/month/2026-08), and [September](https://huggingface.co/papers/month/2026-09). September is a partial month. The dated pages worked even when the undated month URL did not.

This is a relevance- and diversity-driven convenience sample. Upvotes helped prioritize attention; they do not establish paper validity, figure quality, or an objective best-paper ranking. Counts below are the visible monthly-list vote numbers, not the GitHub stars that can appear after a title. Live paper-page counts sometimes differed. A month is the discovery/listing month, which can differ from the arXiv ID month.

We screened 17 papers against primary author sources. Six author figure assets were actually rendered and visually inspected. Three additional cases were read for setup/protocol detail; eight were screened at primary-abstract depth. Those levels are separate in [hf-recent.json](hf-recent.json), including exact figure paths and Git blob SHAs. No source artwork is redistributed. An attempted ALE teaser retrieval did not render successfully and is not a visual review.

| Monthly list | Candidates and visible votes |
|---|---|
| March | SocialOmni 247; EnterpriseOps-Gym 150; T2S-Bench 122; SWE-rebench V2 92 |
| June | Agents' Last Exam 391; EvoArena 145; Claw-SWE-Bench 72; GameCraft-Bench 60; RNG-Bench 52 |
| August | HarnessEval-W 341; EnvHarness 276; VBVR-Pro 271; FrontierChallenge 148; PAWBench 146; UrbanGround 112; MerchantBench 111 |
| September, partial | Terminal-Universe 295 |

## What the inspected figures teach

The strongest setup figures explain a **contract between a task, a tested system, and a judge**. They make it possible to answer: what enters the test, what the system can perceive or do, what changes, when a run ends, and which evidence determines success. This is a different communication job from showing the internals of the proposed algorithm.

The six visual reviews support several distinct compositions:

| Reference | Transferable visual device | Repair when adapting |
|---|---|---|
| [EnterpriseOps-Gym author overview](https://github.com/ServiceNow/EnterpriseOps-Gym/blob/main/assets/teaser.png) | A policy-constrained worked episode connects tool choices to observable verification failures; construction is in its own panel. | Trim feature prose and heavy framing for a publication-scale setup figure. |
| [SocialOmni task overview](https://github.com/MAC-AutoML/SocialOmni/blob/main/docs/assets/socialomni_overview.png) | Different context windows and a conditional interruption decision define what the task permits. | Give that task contract more space than composition statistics or performance radars. |
| [EvoArena environment overview](https://github.com/Aiden0526/EvoArena/blob/main/assets/evoarena_overview.png) | Aligned versions reveal changes to the environment while preserving task identity. | Explicitly label release transitions, which are different from steps within a run. |
| [HarnessEval-W evaluation pipeline](https://github.com/MirroS-Lab/HarnessEval-W/blob/main/assets/fig_pipeline.png) | A diagnostic judgment is tied to a specific generated frame and a visible failure. | Clearly distinguish evaluator agents from the model whose output is being evaluated. |
| [MerchantBench environment overview](https://github.com/KhanCold/merchantbench/blob/main/assets/method.png) | Persistent store state, order progression, and feedback delays make the source of difficulty tangible. | Split generic bidirectional arrows into named action and observation channels. |
| [EnvHarness interface comparison](https://github.com/google-research/envharness/blob/main/figs/example.jpg) | Repeated geometry locates interventions at reset, action, or observation boundaries. | Choose terminology from a single version; repository and paper labels differ. |

## Rules to carry into the third mode

1. **Activate only for a real setup to explain.** A proposed benchmark, dataset with a defined task/evaluation protocol, new environment, material environment adaptation, or central complex evaluation setting can warrant this figure. The routine use of established datasets is insufficient. A paper without such a setup keeps the teaser and method modes.
2. **Choose the scientific relationship before the layout.** An interactive world needs an action/observation loop. A static dataset needs a sample-to-prediction-to-scoring contract. A construction contribution needs a sourcing/filtering/validation/release pipeline. An evolving environment needs aligned states over time. These should not all become the same agent-and-box diagram.
3. **Use one concrete instance.** A task request, short input, scene, action, changed artifact, or checked property should anchor the figure. A catalog of domain names cannot explain a task.
4. **Separate what the agent sees from what the evaluator knows.** Mark hidden labels, reference artifacts, future frames, and latent simulator state when the protocol uses them. Keep evaluator-only paths outside agent input. If hidden access is undocumented, say it is unspecified rather than inventing a boundary.
5. **Show time honestly.** Reset, within-episode steps, delayed outcomes, new tasks, and version evolution are different events. Persistent memory or state must not silently disappear at a boundary. A simulator clock and decision clock may differ.
6. **Place the judge after the evidence it consumes.** Final-state checks, test suites, reference comparisons, human rubrics, and learned judges are different mechanisms. A fluent completion message is not a success criterion. Runtime feedback and post-run evaluation should not share an unlabeled arrow.
7. **Make controlled variation visible.** When comparing variants, preserve panel geometry and vary only the relevant condition. For stochastic benchmarks, show repeated runs and an outcome distribution rather than one attractive sample.
8. **Keep construction and execution distinguishable.** Use separate panels or bands when both are essential. Train/test partitioning belongs to construction or evaluation protocol; it should not look like a runtime branch chosen by the agent.

These are design inferences from the inspected examples and primary setup descriptions, not claims that every cited paper uses every device. The text-only PAWBench case motivates repeated-outcome views; ALE motivates a lifecycle with hidden references; RNG-Bench motivates visible versus remembered observations. Their figure aesthetics were not assessed in this pass.

## Useful text-only counterexamples

- [VBVR-Pro evaluation kit](https://github.com/Video-Reason/VBVR-Pro-Bench) defines both video and image-sequence outputs and task-specific deterministic evaluators. A universal environment loop would obscure this batch evaluation contract.
- [Agents' Last Exam, Sections 2–3](https://arxiv.org/html/2606.05405v1) distinguishes benchmark construction, execution lifecycle, and scoring. These are separately meaningful figure subjects.
- [RNG-Bench, Section 3](https://arxiv.org/html/2606.19338) makes hidden-state reconstruction central. Drawing the full game state directly as the model observation would change the evaluated problem.
- [FrontierChallenge](https://arxiv.org/abs/2608.24979v2) evaluates a deliverable bundle. A final-answer bubble cannot stand in for the required artifacts and completion gate.

For all other screened cases and their exact primary URLs, see the machine-readable ledger. No claims about exhaustive coverage, 17 close visual reviews, or benchmark superiority should be inferred from this research pass.
