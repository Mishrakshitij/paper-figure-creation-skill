# Evidence and claim protocol

Use this before drawing a quantitative teaser or adding quantitative annotations to a method figure. The validator checks declarations and arithmetic. It cannot establish that a source is truthful, that transcription is correct, that the listed baselines are complete, or that a visual claim is scientifically justified. Human/source review remains required.

## Establish an evidence ledger

1. Read the supplied abstract, introduction, method, experimental setup, relevant tables, and figure captions. Pin the paper version or artifact commit. A paper title or abstract alone cannot support table values or precise architectural connections.
2. Record each value with a stable result id, method id, metric id, exact dataset and split, resource/evaluation conditions, and source id. The source must include a retrievable locator and an exact location: table + row + column, page + panel, or file + row/line/key. A result-level `source_location` can refine a shared source location.
3. Include every method relevant to the claimed comparison. Keep deliberately omitted baselines and the reason in the working notes. State the comparison scope in the caption; a handful of declared comparators cannot establish superiority over all published methods.
4. Transcribe reported values at their reported precision. Prefer experiment files or tables. If only a plot exists, obtain the original data when possible; otherwise record digitization, calibration, approximate precision, and its limits. Never silently estimate a point from a screenshot.
5. Verify the input and output semantics of each method node and arrow independently of the visual layout. Record training-only modules, frozen weights, parameter sharing, retrieval boundaries, losses, and inference behavior from the method source.

The [NeurIPS checklist](https://neurips.cc/public/guides/PaperChecklist) connects claims to experimental scope, asks for evaluation/training details, and calls for precise definitions of uncertainty, its variability source, and its calculation. These requirements motivate this protocol; consult the submission venue's current rules separately.

## Comparability comes before a headline

Match dataset version, split, evaluation protocol, prompt/decoding setup, backbone/checkpoint, data access, training and inference budget, and hardware when relevant. Put all material conditions in `comparison`, including fields beyond the required `dataset`, `split`, and `budget`. The executable helper compares declared conditions exactly; it cannot notice an omitted confounder. Do not fill unknown conditions with a guess or a shared string that merely hides a mismatch.

If two results differ in relevant conditions, either find a valid comparison, display the conditions explicitly as a tradeoff, or omit the numerical gain claim. A cost-quality scatter may use `comparison_mode: "tradeoff"` with a sourced quantitative x metric to show different resource budgets. This relaxes budget matching for plotting only. Dataset, split, and other declared conditions still match, and a matched-budget gain claim remains blocked.

Qualitative comparisons use the same examples, crop, resolution, postprocessing, and display scale. Choose examples with a stated sampling rule. Do not choose a failure only for the baseline and an easy case only for the proposed method. An illustrative reconstruction is labeled as an illustration and is not presented as an experiment output.

## Arithmetic vocabulary

Let `b` be baseline and `p` proposed. All numerical claims link to result ids; use the helper's computed value rather than hand-written arithmetic.

| Claim type | Calculation | Meaning and restriction |
|---|---|---|
| `relative_improvement` | `100 * (p-b)/b` for higher; `100 * (b-p)/b` for lower | Percent improvement relative to a positive baseline; negative values are regressions. |
| `absolute_difference` | `p-b` | Signed difference in the metric's unit; the sign is not reoriented for lower-is-better metrics. |
| `percentage_point_difference` | `p-b` | Percentage points, only when stored unit is `percent`, such as 70.0. |
| `speedup` | `b/p` | Ratio of positive elapsed times, for a lower-is-better time metric. |
| `reduction` | `100 * (b-p)/b` | Percent reduction for a nonnegative lower-is-better metric and positive baseline. |
| `all_methods_superiority` | Strictly better point estimate than every declared competing result in the same context | Requires the complete declared comparator list, rejects ties, and does not establish statistical significance or completeness of the literature. |

Synthetic arithmetic examples: 70% to 91% is **+21 percentage points**, or **30% relative improvement**. 100 ms to 50 ms is **2× speedup** and **50% latency reduction**. These are different statements. Do not call the latter “200% faster.” A desired “30% better” headline is a hypothesis until the paper's results support it.

For a fraction-valued metric, convert to percent explicitly before calculating percentage points and record the transformation. Never rename a unit without transforming its values. Do not average unrelated metrics, ratios, or per-dataset percentages to produce a new headline without an explicit, justified aggregation protocol.

## Uncertainty and missing results

- Declare `sd`, `se`, `ci`, or `range`; their meanings differ. Record the source of variation (seeds, data splits, sampled test items, etc.), exact uncertainty provenance, known sample size, and any computation method.
- A confidence interval needs its level and method. Never relabel SD as CI, invent run counts, or infer significance from a visual gap. If raw replicates are available, use a justified statistical procedure and preserve the calculation script and inputs as an artifact source.
- Preserve asymmetric bounds. The portable renderer accepts sourced symmetric half widths in `series.errors`; asymmetric intervals need a custom renderer with the same evidence check.
- If uncertainty was not reported, omit error bars and say so when material. A warning is preferable to invented precision. Do not imply deterministic results merely because intervals are absent.
- A missing value is `{"value": null, "missing": true}` in the ledger and `null` in the chart. Render a gap or “not reported”; never use zero, interpolation, or a connected line across missing measurements without an explicitly justified model.

## Drafts without experiment data

First create a sourced method diagram or a concept-only storyboard and list the exact data needed to finish the results panel. If a numerical layout demonstration is useful, label it visibly **SYNTHETIC DATA** or **ILLUSTRATIVE DATA**, set `status: "draft"`, mark synthetic sources, and keep it out of submission-ready output. Mixed real and synthetic values must be visibly distinguished and cannot support cross-type comparisons. The helper disallows a final synthetic numerical figure.

An arbitrary toy input used to explain a sourced mechanism can be labeled “illustrative input” without treating the entire paper's real numerical results as synthetic. It must not be mistaken for a measured output, a representative dataset sample, or a reconstruction produced by the method.

## Executable contract

The common figure JSON has `version: 1`, `kind: "teaser" | "method"`, and `status: "draft" | "final"`. Full visual fields are described in [spec-format.md](spec-format.md).

```json
{
  "provenance": {
    "data_status": "reported",
    "sources": [{
      "id": "table2", "kind": "paper",
      "locator": "https://arxiv.org/pdf/PAPER_IDv2",
      "location": "Table 2, task X, baseline/proposed rows, accuracy column"
    }]
  },
  "evidence": {
    "metrics": [{"id": "acc", "label": "Accuracy", "direction": "higher", "unit": "percent"}],
    "results": [],
    "claims": []
  }
}
```

This is a structural illustration with a placeholder locator, not a complete or verified figure. Replace it with exact source metadata. A result has `id`, `method_id`, `metric_id`, `value`, `source_id`, and `comparison: {dataset, split, budget, ...}`. An uncertainty object has `type`, either symmetric `value` or `lower`/`upper`, `source_id`, `source_location`, optional `n`, and optional `variation`; `ci` additionally requires `level` in `(0,1)` and `method`.

Every chart declares `metric_id`; every series has aligned `values` and `result_ids`. Quantitative x coordinates use `x_metric_id` plus per-series `x_values` and `x_result_ids`. An independent-variable schedule instead uses chart `x_values` (or per-series overrides), `x_source_id`, and exact `x_source_location`. Each x/y pair must describe the same method and experiment. A chart's `claim_id` links a declared computation to its annotation: its metric must appear on that chart, and every supporting proposed/baseline result must be plotted on the corresponding axis. A scatter can therefore annotate a sourced cost reduction on its x axis while showing accuracy on y. `display_value` is optional, checked against the computed rounding at `decimals` (default 1), and is never a source for the computation.

```bash
python scripts/validate_evidence.py path/to/figure.json --output path/to/evidence-report.json
```

API: `validate_spec(spec)` returns `valid`, `errors`, `warnings`, and `computed_claims`. The CLI exits 0 for a valid declaration, 1 for validation failures, and 2 for unreadable/invalid JSON. Do not treat exit 0 as scientific approval. Resolve errors; then review warnings and inspect the actual source, figure, caption, method semantics, axis choices, and baseline scope.

## Final source review

Before calling an output final, compare every plotted number to its exact source, independently recompute the headline, inspect both axes and unit transforms, and read the caption with the figure at its intended printed size. Check all prose annotations as well as the ledger: arbitrary title text is outside the numerical helper's scope. Remove unsupported “best,” “state of the art,” “significant,” “30%,” causal, and generalization claims. Keep the evidence ledger, source locations, computed report, editable figure, and caption together.
