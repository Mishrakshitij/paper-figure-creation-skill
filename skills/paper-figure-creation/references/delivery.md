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

For PNG, compute required pixels from physical inches × target DPI. At 7 inches and 300 DPI, width is 2100 pixels. Do not resample a small image and claim new detail. Keep original image crops, common qualitative scales, and any required image permissions or attribution in provenance.

Generated examples in this repository are original explanatory redraws of published methods or data. They are not the authors' figures, new experiments, or reproductions of reported training runs.

For a hybrid figure, package the selected image asset and generation/provenance note with the build source. Keep exact labels and relations editable, record effective raster resolution at intended size, and verify a rasterized final PDF. Describe the result as hybrid instead of fully vector. See [hybrid-authoring.md](hybrid-authoring.md).
