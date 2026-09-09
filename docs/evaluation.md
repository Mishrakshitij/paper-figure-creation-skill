# Executed evaluation and revisions

Six original paper figures were created: a teaser and method diagram for each of MAE, Transformer and LoRA. MAE and Transformer exercise the bundled renderer. An independent agent used the skill and primary LoRA paper without root's example sources to produce the LoRA pair through a custom deterministic layout.

This was a development and forward-testing exercise. No matched with-skill versus without-skill trial was completed, and no claim of quantitative design superiority is justified. The independent visual reviewer knew the source papers; the LoRA comprehension check was blind to the implementation and brief, not a blinded first-time-reader experiment. No timed human comprehension study was performed.

## Executed checks

The repository test suite covers evidence arithmetic and linkage, invalid/missing data, incomparable claims, uncertainty provenance, renderer output dimensions, editable SVG text, native draw.io structure, and bounded geometry failures. Run it with:

```bash
python -m unittest discover -s tests -v
```

The skill frontmatter/package validator passed. Actual generated PNGs and PDF rasterizations were inspected. PDFs use embedded fonts; template PNGs have the declared size and 300-DPI density. Native `.drawio` XML was parsed and its nodes, endpoints and routes checked; rendering in the diagrams.net application was not tested. Group backgrounds are visual regions, not necessarily editor parent groups.

For the LoRA forward test, the source table includes every reported GPT-3 row and both tasks. The output retained the smaller variant's unfavorable WikiSQL result, avoided invented per-entry intervals and showed the low-rank branch merging with frozen weights. See its source, captions and review notes in [examples/lora](../examples/lora/).

## Observed failures and repairs

| Case | Initial observed failure | Implemented repair | Verification |
| --- | --- | --- | --- |
| MAE teaser | Per-series scatter x-values caused time ticks to disappear | Preserve numeric ticks when coordinates are supplied per series | Time values readable in regenerated PNG |
| MAE teaser | Baseline label clipped at page edge; y label over divider | Reposition label; measure and reserve chart-label gutters | Source labels fit and panels separate |
| Transformer teaser | Long method labels overlapped concept panel | Measure y-label extents and move plot within evidence region | All eight methods remain readable |
| MAE method | Target supervision passed through mask-token box | Route the target path below the unrelated node; add edge-node warning | Correct target-to-loss path visible |
| Transformer method | Repetition groups included one-time embedding and output operations | Restrict containers to repeated blocks; explicitly identify post-norm structure | Group semantics and method trace re-reviewed |
| LoRA teaser | Table heading collision | Separate method/parameter headings | Final-width independent recheck passed |
| LoRA method | Merge plus hidden by shape layering; crowded annotations | Raise symbol and adjust annotation positions | Explicit addition and labels visible |
| Renderer review | Inactive auto ticks falsely triggered page clipping | Exclude only ticks outside active limits | Regression check distinguishes hidden ticks from real clipping |
| Evidence review | Claim could be attached to an unrelated chart | Check metric and referenced plotted results | Regression tests prevent misleading claim placement |
| Renderer review | Limits could hide data; custom concept geometry escaped checks | Check active plot limits/log coordinates and recurse into custom geometry | Focused regression tests |

Initial failed previews are preserved in [examples/review-history](../examples/review-history/). They document concrete changes, not an intentionally degraded baseline. [Independent review notes](independent-visual-review.md) record what the reviewer observed and which defects were resolved.

## Limits

- The figures use a stated 7-inch-wide draft, not a compiled submission with a supplied venue template. Final manuscript integration remains a check for each real paper.
- Declared-source validation does not independently prove the source, fairness, baseline completeness, prose truth or statistical significance.
- Grayscale and palette checks are useful but do not constitute a complete accessibility study.
- The bundled renderer intentionally supports a limited family of plots and diagram primitives. The custom LoRA case demonstrates the intended escape route, preserving evidence and review requirements.
- The eight additional visual tasks in the [benchmark definitions](../tests/benchmark_tasks.json) are future transfer tests, not completed figures. Adversarial natural-language prompts are also distinct from executed unit tests.

The stopping condition was removal of observed material defects within the declared schematic scope, with explicit export and scientific limitations. Further cosmetic revisions were not treated as new evidence of quality.
