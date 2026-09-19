# Aesthetic composition and overflow repair

Use this when polishing a paper figure, reducing visual clutter, or fixing text,
legend, connector, crop or multi-panel layout problems. Keep the scientific
content and intended final physical width fixed while comparing revisions.

## Give the page a deliberate visual hierarchy

- Choose one focal relationship: the changed state, the matched comparison, or
  the novel operation. Give it more usable area and contrast. Let configuration,
  conventional modules and explanatory notes recede through spacing and lighter
  boundaries, while preserving readable text.
- Align repeated objects and panel headings on common baselines. Use a small
  spacing rhythm consistently (for example 2, 4 and 8 mm at final size), with a
  larger gap between semantic groups than within a group. These are starting
  values, not a replacement for measuring the manuscript slot.
- Establish three type roles: panel heading, content, supporting label. Use
  restrained weight differences and a shared math style. Avoid all-bold labels,
  centered paragraphs, excessive title size, and a different font per object.
- Keep semantic colors stable across figures. Use dark text, quiet backgrounds,
  and an accent for the focal relationship. Baselines and negative results must
  remain equally readable. Check grayscale and use marker/line redundancy.
- Prefer an aligned example, a before/after pair, or a shared-state diagram when
  it makes the mechanism visible. Remove redundant enclosing boxes and ornaments
  before removing scientific information. Whitespace should separate meanings.
- Place explanatory prose in the caption when the figure itself can show the
  relationship. Retain units, uncertainty meaning, critical information boundaries,
  and qualifiers wherever their absence would change the interpretation.

An aesthetic pass succeeds when the reading order and comparison are easier to
recover at the same size. It need not add illustrations, shadows, gradients or
extra color. Compare actual renders, not a self-assigned beauty score.

## Publication finish criteria

For a premium finish, review these observable properties in the final render:

1. **Composition:** the first glance finds a clear focal relationship; panel
   hierarchy matches the narrative, with balanced margins and intentional white
   space. No panel is made artificially dominant by an oversized heading.
2. **Typography:** a consistent type scale, aligned headings, readable equations,
   and no awkward single-word last lines or crowded superscripts. Inspect actual
   glyphs for font fallback and clipping, especially in vector-to-PDF export.
3. **Geometry:** related panels align; repeated objects share dimensions; corner
   radii, stroke weights, arrowheads and internal padding follow the same grammar.
   Nodes may vary in size when their scientific roles need different room.
4. **Routing:** the forward path is easy to follow; feedback uses its own lane;
   arrows attach to meaningful ports; intersections cannot be mistaken for joins.
   Labels do not straddle connectors or disappear into neighboring nodes.
5. **Evidence styling:** comparable plots share axes/units where appropriate;
   uncertainty is visible; legends retain every method; measured and illustrative
   elements are clearly distinguished. Color highlights a role, not an invented
   significance claim.
6. **Production:** the PDF works at the intended column width, with no overlap,
   overflow, crop, orphaned legend, or unreadably reduced detail. Check grayscale
   and an enlarged export for stroke/raster/font defects.

Record concrete repairs such as “moved the legend into a measured two-row band”
or “aligned all intervention examples to the same stage columns.” Avoid certifying
a premium aesthetic from a numeric score or a zero-warning script alone.

## Plan space for text before placing data or nodes

Reserve distinct areas for the main title, panel titles, tick/axis labels, the
data or method objects, legends and notes. Measure the longest realistic labels
and all legend entries, not placeholder text. Short English labels are a poor
stress test for equations, long dataset names or two-line method names.

Use the real renderer after fonts, math, DPI and final figure dimensions are set.
Character counts cannot reliably predict width. A label may be inside the page
and still overlap a neighboring panel, another label, a node or the plotted data.
Clipping a label does not solve its overflow.

| Observed defect | Preferred repair | Avoid |
|---|---|---|
| Label wider than node | Shorten without changing meaning; wrap at word boundaries; enlarge node and rebalance its neighbors | Truncating identifiers, breaking an equation, or reducing all labels |
| Wrapped label hits a detail line | Allocate separate title/body areas or increase node height | More line breaks in the same fixed height |
| Long tick labels consume plot area | Horizontal orientation, measured wrapping, a larger label gutter, or a full-width panel | Arbitrary rotation and tiny type as the default |
| Legend runs off the canvas | Use multiple rows/columns, a dedicated band, or direct labels; retain every series | Dropping methods or shrinking until invisible |
| Legend obscures marks | Place it outside the data region and reserve its height/width explicitly | Assuming `loc="best"` proves no data are hidden |
| Labels/annotations collide | Reposition in a reserved callout lane with a leader, or simplify wording | Moving data points or deleting inconvenient annotations |
| Arrows cross text or unrelated boxes | Reserve routing lanes, use explicit ports and waypoints, move label and route together | A white text background that merely masks the crossing |
| Error bars are cut by axis limits | Expand limits to contain the full declared interval or use an explicitly annotated broken interval with a suitable custom renderer | Quietly clipping uncertainty while the estimate is visible |
| Content reaches the paper edge | Reallocate margins and rerender at the same physical width | `bbox_inches="tight"` as a blanket fix that changes the final size |
| Reduced manuscript export is unreadable | Recompose for the actual column width and check effective point sizes | Calling a large-screen preview publication ready |

Change one cause at a time. If local repairs keep colliding with each other,
change the panel arrangement or split the figure. Do not conceal missing facts
or an unresolved design choice with cosmetic layout changes.

## Bundled checks and opt-in wrapping

The renderer now writes structured `layout_issues` in its `.qa.json`, covering
rendered text intersections, page and clip-box overflow, legend bounds, and an
optional minimum type size. `--strict-layout` returns failure on warnings.
Explicit error bars must fit the plotted domain; the renderer refuses a clipped
interval even if its point estimate would be visible.

For a node, set `"wrap_label": true` to wrap using the actual font metrics and
`"text_padding_pt": 4` to reserve inner side margins. This keeps the font size
and every word. An unbreakable overlong token stays intact and is reported. Check
height after wrapping: the helper does not change node topology or resize nodes.
Native diagrams.net text remains editable and may wrap differently on export;
inspect its final rendering independently.

Set `figure.min_font_pt` only when the project or venue has a chosen floor; the
skill does not impose one universal font requirement. Effective text size after
LaTeX scaling is `source_font_pt * inserted_width / source_width`.

Custom Matplotlib figures can reuse the same checks:

```python
from layout_quality import audit_figure
issues = audit_figure(fig, min_font_pt=8, check_data_occlusion=True)
# Use 8 pt only if it is this paper's floor; inspect all reported collisions.
```

Bounds for rotated text are conservative; visually inspect flagged intersections.
Custom clip paths are explicitly flagged for review rather than silently treated
as safe. Optional `check_data_occlusion=True` (JSON:
`figure.check_data_occlusion: true`) reports intersections between actual legend
ink and supported 2D line, scatter, errorbar and filled-band ink. It respects
artist clipping and supported draw order, including frameless legends. Its
current-DPI raster check does not cover bars, images, meshes, polar/3D axes,
cross-axes overlays or arbitrary custom artists. Treat findings as a reason to
inspect and repair legend placement; an empty report is not full visual approval.
Automated checks cannot judge every mark/legend collision, font fallback,
arrowhead tangency, contrast interaction, SVG editor behavior or PDF crop.

## Deliver a verified rendering

Review the exact exported PDF/SVG, then a rasterized proof of the PDF at its final
manuscript size. Inspect the page after LaTeX inclusion for crop and scaling.
Keep the original-size PDF, editable source, rendered preview and QA record
together. State which checks were actually run and which require manual review.
Do not report “all issues fixed” based only on a zero-warning geometry report.
