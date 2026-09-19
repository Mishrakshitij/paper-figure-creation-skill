# Exports and manuscript integration

Keep the canonical spec/source, evidence ledger, caption, and review record beside the exports. Do not make the PNG the only editable artifact.

| Destination | Preferred artifact | Verification |
| --- | --- | --- |
| LaTeX / Overleaf | PDF with vector text/geometry and embedded example images when needed | Fonts embedded, no unintended Type 3 fonts, correct media box, crop and physical width |
| Word | SVG where supported; high-resolution PNG fallback | Inserted width, label readability, actual exported document rendering |
| Google Docs | High-resolution PNG when SVG import is unsuitable | Check target rendering and compression; preserve vector master externally |
| diagrams.net | Native uncompressed `.drawio` plus PDF/SVG | Nodes, edges, ports, text and grouping remain editable |
| Collaborative board | SVG/PNG preview and link to canonical source | Board edits do not silently desynchronize evidence |

These are workflow preferences, not universal venue requirements. Read the submission's current author guide and use its actual page template. Check the final manuscript PDF, not only a standalone figure export.

For a two-column LaTeX figure, a typical integration is:

```tex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/teaser.pdf}
  \caption{Replace with the source-grounded caption.}
  \label{fig:teaser}
\end{figure*}
```

For a single-column figure use `figure` and `\columnwidth`. Placement rules are template-dependent. Redesign a dense two-column diagram for a single column; shrinking it by half often destroys readability.

Useful local checks, when installed:

```bash
pdfinfo output/figure.pdf
pdffonts output/figure.pdf
pdftoppm -scale-to 1600 -png -singlefile output/figure.pdf output/figure-review
```

Inspect the resulting image. A PDF with no fonts may intentionally contain outlined SVG text, but retaining editable text in the source remains valuable. Keep PDFs and SVGs vector where possible; a vector container around a low-resolution bitmap does not restore detail.

If Poppler tools are absent, use an already available PDF renderer such as
PyMuPDF or pypdfium2 for the same visual proof. Render the actual exported PDF
at `inserted_width_inches * preview_ppi` pixels wide, retaining its aspect ratio,
selected page box and rotation. Record the PDF hash, renderer, page and dimensions;
inspect that proof and an enlarged detail. This fallback verifies neither font
embedding nor editable text by itself; record those checks separately instead
of declaring them passed because rasterization succeeded.

For PNG, compute required pixels from physical inches × target DPI. At 7 inches and 300 DPI, width is 2100 pixels. Do not resample a small image and claim new detail. Keep original image crops, common qualitative scales, and any required image permissions or attribution in provenance.

Generated examples in this repository are original explanatory redraws of published methods or data. They are not the authors' figures, new experiments, or reproductions of reported training runs.

For a hybrid figure, package the selected image asset and generation/provenance note with the build source. Keep exact labels and relations editable, record effective raster resolution at intended size, and verify a rasterized final PDF. Describe the result as hybrid instead of fully vector. See [hybrid-authoring.md](hybrid-authoring.md).

## Review the assembled document

When a manuscript is available, inspect the figure's actual page and adjacent pages after the final build. Float placement, barriers, and caption wrapping can strand a few lines on an otherwise empty page even when the figure itself is clean. Check caption continuity, figure references, unexpected blank space, and the applicable main-text page budget. Prefer removing repetitive caption wording or correcting placement over shrinking an already readable figure. Recheck affected pages after the repair; a standalone proof cannot verify pagination.

Inspect build diagnostics as well as pixels. Undefined or multiply defined labels and duplicate PDF destinations can produce incorrect links despite a successful compilation. Include `pdfTeX warning` messages in a LaTeX log review, not only `LaTeX Warning`, overfull, or underfull messages. Verify affected cross-reference and destination targets in the exported PDF when tools permit. Repair the conflicting labels or anchor construction instead of merely suppressing warnings. Record unresolved navigation or layout checks separately from a visually clean figure.

## Preserve the reviewed snapshot

For an automated or cached rendering pipeline, reuse an artifact only when its relevant dependency identities and exports still match the recorded snapshot. Dependencies can include imported rendering/validation helpers, data and selection records, assets, and model/checkpoint identities used to produce measurements. Record already validated hashes when available; do not recompute large checkpoint hashes unnecessarily. File existence or modification time alone cannot establish that an export represents current evidence, and checking inputs alone misses an altered output.

Serialize overlapping render/build operations, or review an immutable snapshot, so a background refresh cannot replace files during inspection. Record the exact manuscript PDF hash, figure page locations and inserted widths, plus proof-image identities. After any material source, caption, or layout change, rebuild and recheck the affected evidence or pages before updating that record. Keep the reviewed snapshot identifiable even if an evolving draft later changes. A simple one-off figure can use a short source-and-export record without introducing a cache or background process.
