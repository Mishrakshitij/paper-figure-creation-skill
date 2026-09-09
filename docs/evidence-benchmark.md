# Evidence and transfer benchmark

The machine-readable task set is [tests/benchmark_tasks.json](../tests/benchmark_tasks.json). It contains eight diverse visual transfer tasks and eight adversarial integrity prompts. The visual tasks are **defined, not run**. Adversarial cases link to passing validator tests; the natural-language agent responses themselves have not been benchmarked. Do not present either category as completed figure-quality evidence.

| Visual task | Domain | Main transfer challenge |
|---|---|---|
| DDPM method | Generative modeling | Forward/reverse processes, time conditioning, and training/sampling distinction |
| NeRF method | 3D vision | Geometry, ray queries, and volume rendering |
| DPO method | Language alignment | Paired data, fixed/reference components, exact loss dependencies |
| GAT method | Graph learning | Local neighborhoods and multihead aggregation |
| CLIP teaser | Multimodal learning | Concrete paired inputs and protocol-compatible evaluations |
| FlashAttention teaser | Systems | Memory hierarchy, hardware-specific cost evidence, honest speedup |
| SAM teaser | Segmentation | Prompt semantics, matched qualitative examples, mask provenance |
| Mamba teaser | Sequence modeling | Selective computation and scale/context-controlled comparisons |

Each task links an original paper and names the inputs the executor must retrieve. It deliberately supplies no recalled results. To run a task, pin the full paper, preserve exact evidence locations, generate the editable figure and publication-size preview, execute the numerical validator, and record an independent source/semantic review plus a visual review. Record input hashes or pinned versions, skill revision, model/agent identity, figure revision, defects found, and final outcome.

The adversarial prompts challenge absent experiments, missing baselines, omitted strong competitors, SD-to-CI relabeling, mismatched budgets/splits, percentage-point confusion, invented cost-axis positions, and unsupported significance. A task succeeds only when it produces a useful valid alternative and rejects the requested misleading presentation.

## Comparing the skill with an unguided baseline

Use identical source packets, target dimensions, renderer access, model, and effort budget. Randomize which skill condition is shown first, and anonymize figure labels before review. Have reviewers assess the rendered outputs before seeing the production notes. Use the same rubric and hard gates from [review.md](../skills/paper-figure-creation/references/review.md) for both conditions. Keep source accuracy and method fidelity as hard gates: beauty cannot compensate for a false result.

Capture the number and type of factual defects, readable labels at printed size, time required to identify the main claim, whether a reviewer can explain the proposed computation, and whether the editable source regenerates the delivered export. Keep individual reviewer judgments and uncertainty rather than inventing an aggregate quality percentage from an informal opinion. Report the number of papers, figures, conditions, and reviewers actually evaluated; do not extrapolate a small demonstration to a universal improvement claim.

## Executed integrity checks

```bash
python -m unittest discover -s tests -p test_evidence.py -v
```

The suite checks numeric finiteness, plot/ledger identity on both axes, exact declared comparison context, arithmetic and units, synthetic labeling, missing-value preservation, uncertainty metadata, comparator scope, and CLI behavior. It cannot verify external source truth, ensure literature completeness, or review prose annotations. The broader visual benchmark supplies the complementary human/agent review tasks.
