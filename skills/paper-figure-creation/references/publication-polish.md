# Coordinated publication polish

Use this for requests to make an existing paper feel polished, cohesive or
premium. Improve the reader's ability to find the comparison and understand its
limits. A table or restrained statistical plot can be the strongest visual;
illustration is optional and should explain a scientific object or operation.

## Establish a small visual system

Inspect the manuscript and current exported figures first. Record actual figure
widths, body/caption typography, existing semantic colors and how dense the page
is. Keep venue styles intact. Choose a restrained set of reusable tokens:

- One compatible type family, with a modest title/body/supporting hierarchy.
- Dark text, quieter but legible axis/secondary labels, and a semantic accent.
- Consistent panel letters, title alignment, data strokes, marker sizes and gaps.
- A white page background, light reference grids where useful, and deliberate
  whitespace around the main comparison. Avoid a decorative frame per panel.

Use tokens consistently across related figures without forcing all figures into
the same grid. Color may identify a method or evidence role; it must not silently
mean significance or superiority. Maintain redundant shapes or line styles when
the reader needs to distinguish groups in grayscale. Compare actual print-size
proofs before changing a venue's type scale to match a screen preference.

## Refine quantitative figures

1. Name each panel's question and order panels in the argument's reading order.
   Dataset headings and endpoint headings should have distinct positions or
   typographic levels. Repeated long axis titles can become a shared heading
   when every panel has the same unit and the mapping remains clear.
2. Choose geometry for the comparison: horizontal estimates and intervals for
   long labels; aligned small multiples for different endpoints; direct labels
   when a legend would force repeated lookup. Use the existing best structure
   when it already works. Do not add a chart solely to decorate a count table.
3. Reduce visual competition: keep meaningful ticks and zero/reference lines,
   lighten redundant grid lines, remove unnecessary upper/right spines, align
   label gutters, and allocate a measured band for legends and footnotes.
4. Keep all estimates, intervals, denominators, baselines and negative results.
   Unknown outcomes require a distinct mark or an explicit table/caption link;
   they are not zeros. A displayed percentage needs a defined denominator.
   Capacity, source recovery, issuer recovery and behavioral utility are different
   endpoints even when all use percent units.
5. Comparable panels should normally use comparable scales. A zoom or inset may
   reveal a small effect, but label the changed domain and preserve the full
   uncertainty extent. Never move an estimate, clip an error bar, reorder groups
   by observed success without disclosure, or use a truncated bar baseline to
   create a stronger visual result.
6. Use extra detail selectively: a short panel subtitle, a primary-condition
   label, a reference marker, or an uncertainty note can improve interpretation.
   Avoid winner badges, headline gains without a matched comparison, or colored
   background areas that look like confidence regions.

For tables accompanying figures, preserve venue typography; align comparable
number precision, label units in the header and use whitespace/clean horizontal
rules instead of a dense boxed grid. Keep unknown markers and denominator notes
legible. Table numerators and figure estimates must come from the same ledger.

## Make the change reviewable

Keep the old export and its source hash. Create a derived styled version with
the same data/uncertainty commitments, then compare old and new at the same
physical width. Record concrete changes: aligned endpoint headings, a dedicated
legend row, clearer distinction between primary estimates and controls, or
recovered space for long labels. Do not substitute a numerical beauty score for
viewing the figures.

For custom Matplotlib code, reuse `figure_style.apply_theme` when appropriate,
then compose with explicit axes bounds or a well-spaced GridSpec. Run:

```python
issues = audit_figure(fig, min_font_pt=8, display_width_inches=5.5)
```

Those sizes are an example paper setting, not a universal venue requirement.
The effective type size is source points multiplied by inserted/source width.
Repair undersized text by recomposing at the final size, rather than merely
increasing the PNG resolution. Inspect the vector PDF, paper-width raster proof,
grayscale proof and final manuscript page. Any crop, overlap, unresolved glyph,
ambiguous connection or unreadable scientific label remains a delivery defect.

Publish only the reviewed version under the task's existing authorization.
An updated skill should improve later figures without forcing a successful
existing figure through needless redesign or changing the scientific claims.
