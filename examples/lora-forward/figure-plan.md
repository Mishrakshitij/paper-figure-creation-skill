# Figure plan: LoRA forward mechanism

- **Source:** Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models*, arXiv:2106.09685v2, Figure 1 (p. 1); §4.1 and Eq. (3) (p. 4). Primary version: https://arxiv.org/pdf/2106.09685v2. Supplied brief: `figure-forward-inputs/lora-method.md`.
- **Question:** How does LoRA adapt one linear map while keeping its pretrained weights fixed?
- **Message:** Parallel frozen and low-rank paths share the input, add their outputs, and can be merged for deployment.
- **Selected job:** Method / architecture, with a deployment panel.
- **Omitted jobs:** No separate teaser is needed for this focused request. No benchmark/setup: the brief provides no substantive benchmark contribution. No standalone graphs: no experiment measurements were supplied. No generated imagery: exact editable matrix geometry is the appropriate representation.
- **Size:** 7 × 4.167 inches, a two-column draft; no venue template supplied. Body labels 8.5–9.5 pt, primary math 10–15 pt.
- **Objects:** Symbolic x∈R^k → W₀x and A then B then α/r → coordinate-wise sum h∈R^d. W₀ is d×k; A is r×k; B is d×r. Only A and B train. No invented activation entries, grid counts, loss, optimizer, or task examples.
- **Example status:** Symbolic, not measured; matrix silhouettes are schematic and not to scale.
- **Uncertainty:** None needed; no empirical marks. No numerical results or claimed measured speedups.
- **Scale convention:** §4.1 first writes Eq. (3) without scaling, then specifies α/r. Use α/r consistently in the computation and merged matrix.

## Three composition sketches

The editable `composition-sketches.svg` records these distinct topologies.

1. **Shared-input horizontal branches + deployment strip (chosen):** Start at x, split into a large frozen map and A→rank-r bottleneck→B→scale; add on the right. A separate strip shows the merged deployment matrix. Both computation and phase distinction are visible without a backward route.
2. **Vertical residual fork:** Bottom input, large frozen matrix left, low-rank ladder right, sum at top. Faithful but a tall page shape compresses the explicit scale and initialization labels at seven-inch width.
3. **Algebra-first factorization:** Large matrix equation W₀ + (α/r)BA with dimension brackets, followed by a small input/output line. Best for parameter shapes, but makes the shared-input semantics less immediate.

## Scientific connectivity contract

| Object or edge | Meaning | Anchor |
|---|---|---|
| x fan-out | Same vector enters both paths | §4.1, before Eq. (3) |
| W₀ | Frozen d×k parameter matrix | §4.1, first paragraph |
| A then B | Trainable r×k and d×r factors, r≪min(d,k) | §4.1, first paragraph |
| α/r | Constant scale on the low-rank output | §4.1, after Eq. (3) |
| Circled + | Coordinate-wise sum of d-vectors | §4.1, before Eq. (3) |
| Initialization | A random Gaussian; B zero; update initially zero | §4.1 and Figure 1 |
| Merged matrix | W₀+(α/r)BA used as one linear map after training | §4.1, “No Additional Inference Latency”; scale carried through algebra |

All solid arrows denote forward vector data. There are no gradient or supervision arrows. The panel-b merge equation defines parameters; it is not a forward data edge.

## Build and review

- Canonical geometry and text: `build_figure.py`; editable export `figure.svg`.
- Build: `python build_figure.py` from this directory (Python 3, Pillow, Inkscape, Poppler).
- Matrix objects, text, arrows, and equations use SVG elements; no raster inserts.
- Exports: 7-inch PDF, editable SVG, 300-dpi PNG, 144-dpi paper-size and PDF-derived proofs, grayscale and thumbnail.
- Review: source check → thumbnail → publication-size pixels → enlarged pixels → PDF-derived pixels → independent scientific/comprehension check → repairs.
- Detailed findings and any limitations are recorded in `review-notes.md`.
