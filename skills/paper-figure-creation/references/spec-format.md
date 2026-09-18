# Figure specification v1

The renderer is a starter implementation, not a replacement for figure design. JSON is the editable source of truth. Read `evidence.md` for the independent validator's exact evidence requirements.

## Run

```bash
python scripts/validate_evidence.py figure.json --output evidence-report.json
python scripts/render_figure.py figure.json --output output/figure --strict-layout
```

The output stem becomes `.svg` (editable text), `.pdf` (embedded TrueType fonts), `.png` (300 dpi), `.qa.json`, and for method or benchmark figures `.drawio` (native editable diagrams.net XML). Export keeps the exact specified dimensions. The drawing engine uses Matplotlib and NumPy. A separate PDF artifact marker may be required by the hosting environment before authoring PDFs.

## Common envelope

```json
{
  "version": 1,
  "kind": "teaser",
  "status": "draft",
  "figure": {
    "width_in": 7.2,
    "height_in": 3.3,
    "title": "A short, evidence-supported takeaway",
    "subtitle": "SYNTHETIC DATA — an illustrative design example",
    "note": "Explain the comparison scope in the caption."
  },
  "provenance": {
    "data_status": "synthetic",
    "sources": [{"id": "demo", "kind": "synthetic", "locator": "Design demonstration", "location": "Hand-authored illustrative values"}]
  },
  "evidence": {"metrics": [], "results": [], "claims": []}
}
```

`kind` is `teaser`, `method`, or conditionally `benchmark`. Use `status: final` only for reported data. Synthetic/mixed figures receive a visible watermark. `theme` optionally overrides keys in `assets/theme.json`. All font sizes are points; exported width/height are inches. Default normal type is 8.5 pt at 7.2 inches. Judge at final print width before reducing fonts.

## Teaser concept

`figure.concept_fraction` defaults to 0.35; normal target is 0.30–0.40. Evidence fills the remainder. `concept` has `title`, `input_label`, `output_label`, optional `note`, and one of:

- `kind: token_grid`: `rows`, `cols`, `labels` (row-major strings), `selected` (zero-based token indices), optional `mask`, `operation_label`. Draws tokens, selection and retained tokens.
- `kind: spatial`: token-grid fields plus `region: [x,y,w,h]`, a schematic bounding rectangle in the concept panel's normalized coordinates.
- `kind: retrieval`: `query`, `documents` (short strings), `selected` (document indices). Draws the query and a selected evidence stack.
- `kind: matrix`: 2-D `values`, optional `vmin`, `vmax`, `matrix_label`. Pattern values are illustrative unless backed by evidence; do not label an invented pattern as attention, saliency or a measured statistic.
- `kind: custom`: `nodes`, `edges`, `groups`, `annotations` use the method grammar below within the concept panel. For unusual mechanisms, use this or edit original SVG rather than force a stock picture.

Keep panel titles to a few words; insert explicit `\n` where needed. Use concrete task examples, not a generic Input → Model → Output chain.

## Teaser charts

`charts` holds one or two chart objects:

```json
{
  "type": "dot",
  "title": "Quality on held-out tasks",
  "metric_id": "accuracy",
  "categories": ["Task A", "Task B"],
  "xlabel": "Accuracy (%) ↑",
  "xlim": [60, 90],
  "series": [{
    "id": "proposed", "label": "Proposed", "role": "proposed",
    "values": [82.1, 85.0], "result_ids": ["a-proposed", "b-proposed"]
  }]
}
```

- `dot` and `bar` are horizontal. `xlim` controls the numeric axis; bars must start at zero. Restricted-range dots are permissible with explicit ticks.
- `line` and `scatter` use `x_values` (numbers), `xlabel`, `ylabel`, optional `xlim`, `ylim`, `xscale: log` or `yscale: log`. Per-series `x_values` override the chart values. Link measured horizontal values using `x_result_ids` and chart `x_metric_id`.
- Categories and every series values array must have equal length. Use missing `null` observations with corresponding evidence marked missing; they render as gaps. Do not interpolate missing experiments.
- `role: proposed` uses the single teal accent. Baselines use neutral colors and distinct marker shapes. Always retain a text legend.
- Optional series `errors` is an aligned array of symmetric half-widths backed by uncertainty records. This starter does not render asymmetric intervals; extend it or use a separate plotting script faithfully.
- Use `figure.shared_legend: true` for matching method series across two panels; it reserves a separate legend row. `legend: false` disables a chart legend when direct labels already identify methods. Per-series `point_roles` can accent a proposed method among categorical rows. `point_labels` and `point_label_offsets: [[dx,dy],...]` add direct scatter/line labels in point offsets.

Optional chart fields: `xticks`, `yticks`, `value_labels`, `value_format` (Python format such as `.1f`), `legend_loc` (Matplotlib location, or `below`), `claim_id` (validated evidence claim), `claim_label` (non-numeric prefix).
- Use label text to indicate direction (`↑` / `↓`) and units. State source/table/figure and uncertainty meaning in the caption; do not bury source citations in tiny plot text.

Every y/value observation must map to one evidence `result_id`; duplicate provenance is checked rather than trusted. Claim arithmetic comes from the evidence validator. A chart claim must concern its plotted metric (or its measured x metric), and all claim operands must occur among that axis’s plotted result IDs. The renderer validates before plotting; it does not establish that the cited source was transcribed accurately.

## Method geometry

Use manual normalized `[0,1]` coordinates. Origin is lower left. The canvas is the plot area below the title; positions do not include page margins.

```json
{
  "nodes": [
    {"id":"input", "x":0.01, "y":0.39, "w":0.15, "h":0.22, "label":"Input tokens", "representation":{"rows":2,"cols":4,"selected":[1,3,5]}},
    {"id":"backbone", "x":0.27, "y":0.39, "w":0.21, "h":0.22, "label":"Backbone", "state":"frozen"},
    {"id":"proposal", "x":0.59, "y":0.39, "w":0.22, "h":0.22, "label":"Proposed block", "state":"trainable", "role":"proposed"}
  ],
  "edges": [
    {"source":"input","target":"backbone"},
    {"source":"backbone","target":"proposal","source_port":"right","target_port":"left"}
  ]
}
```

Nodes require unique `id`, `x,y,w,h`, `label`. Optional: `state: frozen|trainable`, `detail` (overrides visible state label; if used, include the state meaning elsewhere), `role: proposed`, `shape: box|circle|diamond|text`, `font_size`, `fill`, `representation: {rows,cols,selected,labels,mask}`. Boxes can carry a miniature token/grid representation. Frozen blocks have a dashed border and explicit frozen text.

Edges require `source`, `target`. Optional: `source_port`/`target_port` (`left`, `right`, `top`, `bottom`, or normalized `[u,v]`), `via: [[x,y],...]`, `kind: solid|skip|dashed|training`, `role: proposed`, `arrow: false`, `label`, `label_position: [x,y]`. Routes are exact polyline waypoints; the renderer does not infer architecture or route around obstacles automatically. Distinguish control/training/skip paths in the figure key, not merely by color.

`groups` are background regions `{x,y,w,h,label,fill?}`. `annotations` are free labels `{x,y,text,role?,font_size?,ha?,va?}`. Explicitly separate training and inference; include losses, parameter sharing, tensor shapes, repeated layers and stop-gradient where scientifically needed. A branched DAG can use the same ports for parallel branches and exact `via` points for residual paths. Recurrent architectures can contain cycles, so no topological-order restriction is imposed.

The native draw.io export preserves editable nodes, representations (including masked cells) and routed edges, including `arrow: false` headless connectors. It is an independent editorial copy, not guaranteed pixel-identical to SVG/PDF. Reimport edits into the JSON spec or document which file becomes authoritative before regenerating.

## Benchmark / environment eligibility and contract

Use `kind: benchmark` only when the paper contains a benchmark, environment, or substantive evaluation setup that needs explanation. A new method's ordinary dataset list does not automatically warrant this figure. Read [benchmark-environment.md](benchmark-environment.md) to choose a paper-specific composition; `assets/benchmark-template.json` is an illustrative interaction scaffold, not a universal design.

The renderer requires a compact `benchmark_setup` contract. The following static example demonstrates fields only; replace every description with verified source content:

```json
{
  "kind": "benchmark",
  "benchmark_setup": {
    "presence": "present",
    "source_id": "paper",
    "source_location": "Section 3 and Figure 2",
    "contribution": "new_benchmark",
    "family": "static_benchmark",
    "unit_of_evaluation": "One question paired with an image",
    "instance_construction": "Source images are annotated, checked, and assigned to disjoint splits",
    "agent_visible": ["Image", "Question"],
    "evaluator_only": ["Held-out reference answer"],
    "evaluation": "Compare each model response with the reference using the source's scoring rule"
  }
}
```

`source_id` must reference `provenance.sources`; `source_location` must pinpoint where the setup is established. `presence` may be recorded as `absent` or `unclear` during planning, but the validator blocks rendering a benchmark figure until it is `present`. Do not change this value merely to pass validation. Resolve uncertainty from the paper or omit the figure. An illustrative synthetic setup is permitted only as a visibly labeled draft under the ordinary synthetic-source gates.

| Field | Required content |
| --- | --- |
| `contribution` | `new_benchmark`, `new_environment`, `adapted_setup`, or `existing_setup`; do not imply an existing benchmark is proposed by the paper. |
| `family` | `static_benchmark`, `interactive_environment`, or `mixed`. |
| `unit_of_evaluation` | What one question, instance, episode, submission, or trial means. |
| `instance_construction` | How tasks are obtained and prepared, with split/reset distinctions where relevant. |
| `agent_visible` | Explicit array of information available to the evaluated model/agent, not just model weights or inputs by guesswork. |
| `evaluator_only` | Explicit array of information reserved for evaluation; `[]` is valid when there is none. |
| `evaluation` | What is scored, by what rule, and at which stage; name actual rewards versus terminal evaluation separately. |

For `interactive_environment` and `mixed`, also provide nonempty `observation`, `actions`, `state_transition`, `reset`, and `termination` descriptions. Describe the interactive portion of mixed setups specifically. If the source states that there is no reset, record that fact; do not fabricate a conventional episodic reset. A source detail that remains unknown must be resolved or the design kept outside the validated final path. Static benchmarks require **none** of these episode fields and must not acquire an invented observation–action loop to fit a template.

Use the same manual `nodes`, `edges`, `groups`, and `annotations` geometry as methods. Benchmark nodes optionally declare `visibility: agent|evaluator|public` for audit metadata. This does not automatically style or hide nodes. Make the information boundary visible with explicit region labels and purposeful routes. The validator does not infer leakage from arbitrary arrows: a scientific reviewer must check whether each link denotes an observation, action, state transfer, score, or training signal. Structured `benchmark_setup` prose is not automatically printed on the figure; choose the visible labels and caption deliberately.

These checks establish a complete declared contract and reject an ineligible figure. They cannot verify source accuracy, protocol validity, private-information leakage, or benchmark novelty. Numbers, result charts, uncertainty, and comparisons remain subject to the same evidence checks as other figure kinds.

## Bounded checks and review

Hard checks reject plotted finite observations outside the active limits, nonpositive logarithmic coordinates, overlapping/out-of-bounds nodes and unknown endpoints. Method and benchmark geometry share the same node and text checks; these also run recursively for custom teaser concepts. Chart y-label gutters are measured and reserved inside their evidence panel. Pixel-based text containment reports potential overflowing node labels and off-page text; `--strict-layout` exits nonzero for those warnings. Edge crossings through unrelated nodes also warn. These checks do **not** certify scientific correctness, edge-edge crossings, legend collisions, overall text overlap or readability. Inspect PNG and PDF at final size and a grayscale/thumbnail view; revise the source and rerender. All final evidence, architecture, and setup semantics still need human scientific review.
# Layout quality extensions

`figure.min_font_pt` optionally declares this figure's minimum readable font
size. Optional `figure.display_width_inches` supplies the actual manuscript
insertion width; the audit checks font sizes after that scale factor without
changing the exported canvas. At half the source width, 9 pt becomes 4.5 pt.
The synthetic/mixed-data watermark respects the source-size floor automatically;
after reduction it must still pass the same effective-size audit.
`figure.watermark_font_pt` may explicitly set its size, which remains subject
to the same legibility and overflow checks. Nodes accept `wrap_label: true`
and `text_padding_pt` (default 4) to wrap
labels at measured word boundaries without shrinking or discarding text.
The QA JSON includes structured `layout_issues`; `--strict-layout` fails when
these produce warnings. Shared legends include series from every chart and
choose enough rows to fit the available width. Their height, label collisions
and final PDF appearance still require review. See
[layout-and-overflow.md](layout-and-overflow.md) for repair decisions.
