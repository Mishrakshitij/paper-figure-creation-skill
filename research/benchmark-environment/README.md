# Benchmark and environment figure research

Research snapshot: **16 September 2026**. This pass supports a conditional third figure mode. It extends, rather than replaces, the earlier proceedings corpus and visual-design revision.

## What was actually reviewed

| Slice | Paper entries screened against primary sources | Papers with actual image inspection | Record |
|---|---:|---:|---|
| Earlier Hugging Face months | 19 | 5 | [Notes](hf-earlier.md), [machine-readable ledger](hf-earlier.json) |
| Recent Hugging Face months | 17 | 6 | [Notes](hf-recent.md), [machine-readable ledger](hf-recent.json) |
| Established benchmarks and environments | 15 | 6 | [Notes](landmarks.md), [machine-readable ledger](landmarks.json) |
| Total | **51** | **17** | No claim that all 51 figures were inspected |

The 51 entries are distinct papers/projects in this pass. Primary screening ranges from abstracts to detailed setup/code reading; each ledger records its depth. The 17 visual reviews used actual author-hosted image pixels and record asset paths and Git blob hashes. Original figure artwork is linked, not redistributed. Text-only entries supply candidate families or setup facts, not evidence of visual quality.

Hugging Face discovery used nine dated monthly indexes: [June 2024](https://huggingface.co/papers/month/2024-06), [December 2024](https://huggingface.co/papers/month/2024-12), [March 2025](https://huggingface.co/papers/month/2025-03), [June 2025](https://huggingface.co/papers/month/2025-06), [December 2025](https://huggingface.co/papers/month/2025-12), [March 2026](https://huggingface.co/papers/month/2026-03), [June 2026](https://huggingface.co/papers/month/2026-06), [August 2026](https://huggingface.co/papers/month/2026-08), and [September 2026](https://huggingface.co/papers/month/2026-09). September is incomplete as of retrieval. Listing month can differ from the arXiv identifier's month.

Visible upvotes helped prioritize candidates within relevant families. They are recorded as observed snapshots, not fixed ranks, visual-quality ratings or scientific-validity judgments. Primary papers, official repositories, project sites, ICLR proceedings and PMLR sources establish setup facts. Hugging Face's generated summaries were not treated as authoritative scientific descriptions. This is a purposeful design sample, not an exhaustive or representative survey of the best papers.

## What changed in the skill

The common design lesson is to make the **task contract** visible: one concrete case, what the tested system can access or do, and the actual criterion used to evaluate its output or changed state. A benchmark figure has a different job from both a performance teaser and an algorithm architecture.

| Visual evidence | Design inference used in the skill | Caution retained |
|---|---|---|
| WebArena and VisualWebArena | Anchor environments with recognizable websites and real task intents; connect interaction to functional evaluation | A reference trajectory is not automatically the scoring rule |
| OSWorld | Separate task configuration, running environment, agent interface and evaluation machinery | A screenshot is only an observation of the machine, not its full state |
| SWE-bench and BigCodeBench | Show executable artifacts and the test boundary; teach evaluation with an actual issue or code example | Distinguish task-construction test validation from evaluating a submitted solution |
| ALFWorld and ToolBench | Use domain-specific scenes or tool payloads to explain actions | A generic “environment” icon hides action constraints and state changes |
| ReasoningGym | Concrete question/answer examples make task families legible; show procedural generation separately from model evaluation | Do not force a static task into an agent loop or universalize one scoring function |
| TheAgentCompany and EnterpriseOps-Gym | Couple recognizable tasks, tools and state with concrete checkpoint or policy checks | Construction and one evaluated episode require separate reading paths |
| VS-Bench | Keep environment categories distinct from evaluation modes | Source versions changed task counts and modes; freeze one version |
| DAComp | Carry the same business question through task design, repository construction and final artifact | Changing artifacts must preserve task identity |
| SocialOmni | Show the full-context versus prefix-only access boundary | Future context must not appear available to the tested interaction system |
| HarnessEval-W | Ground each diagnostic judgment in a visible artifact or frame | Evaluator models must not be mistaken for the system under test |
| MerchantBench | Persistent state, an order lifecycle and different clocks explain delayed consequences | Agent decisions and simulator steps can use different time scales |
| EnvHarness | Align reset, action and observation interfaces across variants | Terminology differs across source snapshots; avoid silently mixing them |
| EvoArena | Repeated task snapshots reveal changes across world releases | Release evolution is not an ordinary within-episode action |

These are authored inferences from the recorded sources. They do not imply that all listed figures are ideal: dense taxonomy panels, tiny labels, broad bidirectional arrows and mixed version terminology were retained as cautions rather than copied.

## Conditional use

Select the third mode when the paper or its primary supplement describes a benchmark, task construction, environment or substantive evaluation workflow that merits explanation. Preserve whether it is new, adapted or existing. A result table on familiar benchmarks, a related-work mention or a learned vector named “environment” does not suffice.

If source evidence is incomplete, record `unclear` and retrieve the relevant section before drawing. No setup means no setup figure. A benchmark paper may need this figure without needing an algorithm architecture figure.

## Worked examples and verification

- [WebArena setup](../../examples/webarena-setup/) tests an interactive website task with a visible state change and separate URL/DOM evaluation. It uses a real configured task but an explicitly schematic action/UI, not an observed agent run.
- [ReasoningGym setup](../../examples/reasoning-gym-setup/) tests procedural construction and static response scoring, including an evaluator-only reference route. It uses a documented generated entry and an illustrative candidate, not measured model performance.

The [implementation and review report](../../docs/benchmark-environment-update.md) separates code checks, authored routing fixtures, figure comprehension review and remaining limits. These examples demonstrate two compositions; they do not establish general superiority across benchmark papers.
