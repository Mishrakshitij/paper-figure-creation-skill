# Semantic objects for custom figures

Use `scripts/semantic_primitives.py` when an algorithm is easier to understand through its **actual objects**: a passage, changed token, parameter state, low-rank factor, discrete input/output example, or generated configuration. These are optional Matplotlib drawing functions. They do not prescribe a page layout or replace a method-specific illustration.

The reference sheet is `assets/semantic-primitives.svg` (editable text) and `.png`. Every object and value on it is an **illustrative schematic**. It is a vocabulary sheet, not an example of a finished paper figure or evidence of figure quality.

## Choose an object by what the reader needs to understand

| Reader's question | Drawing function | Content the author must supply |
|---|---|---|
| What information does the model receive? | `document` | Short, faithful passage or question; explicit line breaks |
| What did the algorithm change? | `token_strip` | Actual tokens and explicit changed-token indices |
| Which model, and which parameters? | `model_tile` | Model identity; frozen/trainable state, with symbols matching the paper |
| What shape or structure makes the operation possible? | `matrix` | Actual array dimensions and values; shared color limits or a categorical palette |
| What happens to one concrete example? | `grid_pair` | Input and output arrays and the transformation label |
| What choices does the controller generate? | `config_card` | Actual key/value settings, or visibly labeled schematic values |
| Did this candidate answer pass the binary test? | `reward_mark` | Explicit Boolean outcome; use labeled numbers for graded rewards |
| What flows, updates, or returns? | `routed_arrow` | Explicit waypoints, direction, edge type, and a concise operation label |

The colors are arguments. Reuse a consistent mapping within the paper; do not assign novelty, trainability, or correctness from color alone. A check and cross have different geometry, a changed token is underlined, and a parameter chip spells out its state.

## Coordinates and output

`inch_canvas(width, height)` makes a figure with one axis data unit equal to one physical inch. Each object takes `ax, x, y` at its **lower-left** corner; rectangular objects also take `w, h`. Font sizes are points. Keep the axis limits and full-figure extent unchanged. Save without `bbox_inches="tight"` or `tight_layout`, which would alter the specified page dimensions.

Objects return a `Bounds(x, y, w, h)` with `port("left" | "right" | "top" | "bottom")`. These are geometric connection points, not automatic routing. Add a small endpoint gap when a visible separation helps; route return paths through reserved space. `routed_arrow` returns a Matplotlib arrow artist.

SVG labels remain live text. PDF font type is set to 42 for TrueType embedding. An export is still subject to the regular rendering, manuscript-size, and source-fidelity review. These helpers do not implement clipping checks, automatic wrapping, complete collision detection, or claim validation.

## A minimal composition

Run from the repository root, or put the installed skill's `scripts` directory on the Python path:

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path("skills/paper-figure-creation/scripts").resolve()))
from semantic_primitives import inch_canvas, document, model_tile, routed_arrow

fig, ax = inch_canvas(5.0, 1.8)
# This short passage is a constructed example, not a reported experiment.
context = document(ax, 0.15, 0.45, 1.65, 1.05,
                   title="Illustrative context",
                   lines=["Blue cells become", "orange cells."])
model = model_tile(ax, 2.75, 0.52, 1.70, 0.89,
                   label="Adapted model", state="parameters θ′")
routed_arrow(ax,
             [(context.port("right")[0] + 0.05, 0.97), (2.69, 0.97)],
             label="read", label_offset=(0, 0.14))
ax.text(0.15, 0.18, "Illustrative schematic", fontsize=7)
fig.savefig("example.svg", metadata={"Date": None})
fig.savefig("example.pdf")
fig.savefig("example.png", dpi=300)
```

For an actual method diagram, decide first whether this edge represents conditioning, training data, or a parameter update. A generic “read” arrow alone does not explain a learning algorithm. Draw the mechanism that matters: separate the inner update from outer optimization, show a candidate self-edit's content, identify the frozen branch, or expand the low-rank operation. The useful primitive is the one that makes this distinction visible.

## Important arguments

- `document(..., title=..., lines=[...], fontsize=8, title_size=8.5, fold=.17)`. Height is checked against the number of lines; width remains the author's responsibility. Do not reduce text below the manuscript's readable size to fit a long passage. Select a shorter faithful excerpt or enlarge the object.
- `token_strip(..., tokens, changed=[...], widths=[...], height=.28)`. Token widths have a rough default based on character count. Supply widths after inspecting unusual tokens, math, or non-Latin text.
- `model_tile(..., label=..., state=..., detail="...")`. A model and its parameter state occupy separate regions. Set `state="frozen θ₀"` only when the source supports that statement.
- `matrix(..., values, palette={value: color}, labels=False)`. Categorical palettes must cover every value. Alternatively, use numeric `cmap`, `vmin`, and `vmax`. Rows are drawn top-to-bottom in the same order as the input. Cell dimensions come directly from the requested width, height, and array shape; choose a common cell size when comparing discrete grids.
- `grid_pair(..., before, after, palette=..., cell=.16, gap=.45, arrow_label="...")`. The two shapes may differ. Cell size is shared; the caller controls the space for a meaningful edge label.
- `config_card(..., entries=[("epochs", "2"), ...], title="...")`. Short keys and values align in columns. Keep the provenance of any reported hyperparameters in the figure spec or caption.
- `reward_mark(..., positive=True, size=.26)`. It represents a binary pass/fail result. A check does not mean an unspecified high reward, correctness on every task, or a statistically significant benefit.
- `routed_arrow(ax, points, label="...", label_at=None, label_offset=(0,.08), dashed=False, arrow=True)`. If no `label_at` is supplied, the longest segment is used. Labels have a small white backing; inspect crossings and avoid using that backing to hide a line that should remain visible.

## Rebuild and review the vocabulary sheet

```bash
python skills/paper-figure-creation/scripts/semantic_primitives.py \
  --demo --output skills/paper-figure-creation/assets/semantic-primitives
```

This writes SVG and PNG only. The six-panel sheet is 7 × 6.02 inches; its smallest explanatory text is 7 points. View it at the intended physical size and inspect the complete composition, not isolated glyphs. A visually clear icon cannot rescue a missing causal relationship or unsupported claim.
