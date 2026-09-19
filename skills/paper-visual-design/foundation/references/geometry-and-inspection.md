# Connection geometry and pixel inspection

Use this reference when authoring or repairing diagrams with arrows, grouped
objects, callouts, or tightly spaced labels. A correct graph can still render as
a broken or ambiguous picture. Check the exported pixels as well as the source.
For typography and physical dimensions, use [design-system.md](design-system.md);
for the scientific claim, use [evidence.md](evidence.md).

## Define the connection before placing it

For each consequential connection, identify:

| Item | Concrete decision |
| --- | --- |
| Source | Which visible object produces this information? A whole sequence, its first element, or one terminal state are different sources. |
| Destination | Which visible object receives it? Identify the particular input port, not just the neighborhood of a box. |
| Meaning | Forward data, conditioning, supervision, execution feedback, comparison distance, or a descriptive leader. |
| Direction | Arrowhead location; use a headless segment for a distance measure or callout when no directed operation is intended. |
| Route | Source port → ordered waypoints → destination port. |
| Label | Text, side of the route, and clearance; a label must not mask or be crossed by the path. |

Distinguish arrow-shaped **data objects**, such as control-vector glyphs, from
arrows carrying information between objects. A small container, bracket, or
consistent repeated-tile arrangement can establish that distinction without a
paragraph of explanation.

When a controller outputs several commands but executes only the first, point
the execution connection at that selected command's port. If an edge instead
enters the whole sequence, visibly group the sequence and give that group a port.
Do not leave the reader to infer that an arrow aimed at an unselected element
actually means a different element.

## Build geometry from anchors

1. Set the intended printed width before laying out nodes. Establish a small set
   of column centers, row baselines, component bounds, and routing gutters.
2. Give repeated objects common dimensions and explicit ports: for example,
   `history.output`, `adapter.history_input`, `adapter.goal_input`, and
   `selected_block.execute`. Derive port coordinates from object bounds. In TikZ,
   use named anchors or declared coordinates; in SVG or plotting code, keep bounds
   and port calculations in one geometry structure.
3. Reserve the connector lanes before filling the space with labels. A feedback
   loop generally belongs in an outside gutter. Two distinct inputs should enter
   distinct ports unless the scientific operation actually merges them.
4. Draw a routing skeleton and check source/destination identity before styling.
   Add the objects and labels, then recheck the paths against their final bounds.

At each destination, the final segment should approach the selected boundary
cleanly: horizontal for a west/east port, vertical for a north/south port, or a
deliberate tangent for a curved boundary. A route aimed at a corner is acceptable
only when that corner is the intended port. Stop the arrow tip on the boundary
or at a small, consistent optical clearance; do not bury it inside text or leave
it floating conspicuously outside the object. Account for the arrowhead's full
length, not just the path endpoint.

Inspect short connectors especially closely. A head that consumes the final
straight segment can appear detached or sit directly on an elbow even when its
tip technically reaches the target. Set arrowhead length/width explicitly and
leave visible shaft before the head; as a starting check, make the final straight
segment at least three times the tip length. For a roughly 5.5-inch method figure,
2.5–3 pt heads with 4–5 mm connection gaps can work well; inspect the actual result
instead of applying these numbers universally. Give command-vector glyphs their
own style, and use group ports for matrices/sequences rather than starting a
connector in the empty space between their constituent tiles.

Prefer one continuous path per edge with one intentional terminal arrowhead.
Manually assembled line segments can acquire tiny gaps, doubled joints, or extra
heads after scaling. If a tool requires segments, use exactly shared endpoint
coordinates and inspect their joins in the final export. Set the desired corner
and line-cap style explicitly rather than relying on a renderer's default.

## Route, separate, and align

- Use a consistent primary reading direction. A reversal or outer feedback loop
  should have a reason visible in the object arrangement.
- Use a small family of bends, usually orthogonal or gently curved routes. Avoid
  arbitrary diagonal doglegs used only to rescue an overcrowded layout.
- Align comparable frame crops, feature strips, candidate rows, panel titles,
  and baselines by shared coordinates. Apply equal padding to repeated objects;
  perceived whitespace matters as well as mathematical bounding boxes.
- Keep sufficient clearance around unrelated text, heads, and parallel paths.
  At final print size, about 1.5–2 mm around a nearby label and several millimeters
  between major components are useful starting points, not universal standards.
  Increase space when a head, descender, or bend still appears crowded.
- Make a branch originate at one explicit anchor. Make a merge terminate at a
  visible junction or operation. Do not accidentally imply a junction because
  unrelated lines share a pixel or overlap for a short distance.
- First try to eliminate crossings by changing port sides, object order, or
  routing lanes. If a crossing is necessary, distinguish it from a join with a
  continuous bridge or another unambiguous local convention. Add a junction dot
  only when the graph really joins; explain an unusual convention in the key.

Uniform alignment does not require equal prominence. Give the scientific example
and changed operation more area; keep conventional machinery quiet. Nested boxes
and perfectly aligned paragraphs do not substitute for a visible transformation.

## Prevent false breaks and overpainting

Two common failures need different repairs:

| Visible defect | Typical source | Repair |
| --- | --- | --- |
| A wire disappears under a word and resumes later | Opaque label background drawn over the path | Move the label beside the wire or reroute the wire around its full text bounds. |
| A wire runs through a symbol or heading | Path drawn over earlier text, or an unreserved text region | Move the label or route; changing draw order alone may only turn an overlap into a hidden break. |
| Arrowhead appears detached from its target | Hardcoded endpoint does not track the resized object | Attach to the object's named boundary port and rerender. |
| A collector appears disconnected from its terminal dots | Bus starts beyond the visible marker edge | Connect to each marker boundary if a bus is intended; otherwise make the headless bracket convention explicit. |
| Several routes look like one thick wire | Coincident coordinates or insufficient parallel clearance | Separate the lanes or represent the actual shared trunk and its branch junction explicitly. |

Define a deliberate layer order: background regions → nonforeground connectors
→ objects and data marks → text, with arrowheads kept visible at their ports.
The exact layering can vary by authoring tool, but all connector paths must avoid
unrelated text and object interiors. A high z-order does not repair a bad route;
a white rectangle does not repair a crossing when the required wire is continuous.
Intentional dashed supervision is different from accidental missing segments.

For grouping and clipping, inspect the real text extents after font selection and
typesetting. Character counts do not predict label width. Include glyph ascenders,
descenders, arrowheads, strokes, raster assets, and shadows in export bounds. A
figure that fits before font substitution or manuscript rescaling may not fit
afterward. Do not solve overflow by silently shrinking critical text below the
agreed paper-size font range.

## Inspect the exported artifact at several scales

Use the actual PDF/SVG export as the source for raster proofs; do not rely only
on a design-tool screenshot. Keep the view size explicit.

1. **Whole figure at intended paper width.** For a 5.5-inch figure, a 550-pixel
   proof at 100 dpi is a useful screen proxy. Actual physical size depends on the
   display; also verify the PDF dimensions in points. Check grouping, reading
   direction, readable text, and whether the visual objects explain the idea.
2. **Enlarged export.** Inspect a high-resolution rendering at roughly 200–400%
   of the paper-width proof. Follow every consequential edge continuously from
   its source, through every bend, to its arrowhead and target.
3. **Targeted crops.** Open crops of branch/merge points, terminal heads, tight
   bends, labels near paths, small mathematical symbols, panel edges, and image
   masks. Include surrounding geometry so the intended target remains apparent.
4. **Grayscale proof.** Check that method identities, selected/rejected paths,
   group boundaries, and data points remain distinguishable. This is not a full
   color-vision accessibility test; add an appropriate simulation when necessary.
5. **Final manuscript page.** Check the inserted figure and caption together.
   Confirm scaling, nearby floats, crop, caption spacing, and legibility again.

For a local PDF, these optional Poppler commands produce reproducible proofs:

```bash
pdfinfo figure.pdf
pdftoppm -singlefile -png -r 100 figure.pdf proof-paper
pdftoppm -singlefile -png -r 300 figure.pdf proof-detail
pdftoppm -singlefile -gray -png -r 100 figure.pdf proof-gray
```

For a correctly sized PDF, the first raster preserves the chosen 100-dpi scale.
Use an available image viewer to inspect the results. Merely creating these files,
checking dimensions, or passing collision tests is not pixel inspection. When
cropping raster proofs, record the crop bounds or object names; do not mistake a
crop edge for clipping in the original export. If visual inspection is unavailable,
state which checks remain unperformed.

Automated text-bound, endpoint, collision, or overflow checks can prioritize
inspection. They cannot establish that an arrow points to the correct scientific
object, that a crossing is understandable, or that a drawing teaches the idea.

## Use visual references when they resolve a design problem

When supplied references exist, inspect their actual pixels. When the visual
grammar remains unclear, targeted visual search can help locate a small number
of relevant original paper figures or authoring examples. Prefer examples with
the same relationship to communicate—shared operators, candidate branches, or
factor combinations—rather than merely the same research keyword.

Record the source URL or file/page, what was inspected, and the transferable
principle. For example: “separate input ports make the shared operator visible,”
not “copy these colors.” Adapt the composition to the current method and evidence;
do not copy measured paths, numerical values, or decorative assets into a new
claim. If reference pixels are inaccessible, say they were not inspected. Search
is useful when it changes a design decision, not as a compulsory ritual for every
small repair.

## Repair observed defects, then recheck

Keep a concise defect record with object/edge ID, location, observed problem,
repair, and the proof used to verify it. Fix wrong connectivity first, then hidden
or crossed paths, clipped labels, ambiguous grouping, and finally cosmetic
spacing. Reopen the affected crop after each repair and then inspect the whole
figure: moving one label can obstruct another route.

If repeated local adjustments cannot preserve both a continuous connection and
readable labels, revise the composition or allocate a new routing lane. Do not
accumulate opaque patches. Stop when the inspected material defects are resolved
and remaining changes are cosmetic; state any unresolved limitation. Report
“no material defect found in these views,” not guaranteed perfect geometry or
publication readiness based on a validator alone.
