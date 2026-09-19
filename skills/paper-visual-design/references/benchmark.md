# Benchmark / environment setup — conditional

First verify eligibility against the manuscript or primary supplement. Record exact section/figure/code location and new/adapted/existing status relative to the target manuscript. Named datasets in result tables, benchmark mentions, and related-work surveys alone do not qualify. If unclear, continue other figures and resolve the source; never manufacture a setup.

Read the foundation's [benchmark/environment contract](../foundation/references/benchmark-environment.md) and use its [brief](../foundation/assets/benchmark-brief.md).

Choose the representation from what the setup actually is:

| Setup | Useful visual structure |
| --- | --- |
| Static dataset | Raw source → construction/filtering → one fully worked task → scoring |
| Procedural generator | Configuration and seed → generated instance → solution/evaluator, with variation axes |
| Interactive environment | One concrete state, model-visible observation, action, transition, termination, and evaluator boundary |
| Controlled benchmark variants | Shared task with changed variable highlighted; invariant context retained |

Show the unit of evaluation and a concrete instance large enough to understand. Separate model-visible inputs from evaluator-only answers/state. Specify allowed actions, resets/persistence, termination, scoring, and aggregation when applicable. A screenshot can ground a web/robotic environment, but do not place fake UI content into an observed-trace panel.

Generated scenes may illustrate an environment concept if clearly schematic. Use real, source-permitted screenshots for claims about an actual interface, and code-generated exact task objects when symbolic structure matters. Trace numeric coverage or benchmark statistics like any other evidence.

Do not duplicate the full benchmark construction in the teaser. Reuse its example identity and color meanings, then add the operational detail here. Do not label an existing environment as the new contribution.
