# Review, repair, and delivery

Use the foundation's [review guide](../foundation/references/review.md) and [delivery guide](../foundation/references/delivery.md) when needed.

## Inspect actual outputs

1. Validate declared evidence and arithmetic. Check important values against primary source cells; a URL in JSON is not verification. Preserve adverse outcomes and scope of every claim.
2. Inspect a thumbnail for reading order/focal operation, a render at manuscript dimensions for legibility, and enlarged pixels for intersections, routing, clipping, and alignment. Check the PDF-derived render too. A successful export is insufficient.
3. Trace one example through the figure. Verify object identity, count, operations, learned/frozen states, information access, and return routes. For graphs, identify every method/setting without relying on color alone and verify axes/units/uncertainty.
4. Inspect grayscale and approximate color-vision views when useful. Such simulations do not establish universal accessibility; redundant labels/markers remain necessary.
5. Ask an independent reviewer, when available, to explain the figure from its pixels and caption. Provide source material for scientific checking, but do not leak the expected interpretation into a comprehension check.
6. Record concrete defects and repair the highest-impact one first. Re-export and inspect the changed result. If repeated local fixes cannot resolve congestion, change the layout. Do not inflate a self-assigned aesthetic score into a measured quality claim.

## Deliver the artifact set

- `figure.pdf`: verified physical dimensions, vector marks/fonts where supported.
- `figure.svg`: editable text and geometry; embedded raster illustrations clearly identified.
- `figure.png`: high-resolution preview plus a paper-size proof when useful.
- Canonical source/spec and build command, exact data/source ledger, assets/prompts/rights notes, caption, and concise review record.
- Native `.drawio` only where this is the chosen workflow. State whether diagrams.net was actually opened/rendered; do not claim a PNG wrapped in a draw.io file is an editable diagram.

Do not claim full native-vector editability for a raster illustration. State that SVG text/paths are editable and raster inserts remain images. If one export format is unavailable/unverified, name it rather than silently promising the full set.

When manuscript integration is requested, update figure labels/references and captions, compile the actual template, inspect figure pages and neighbors for float placement, overflow, font-size changes, and cross-reference errors. Otherwise deliver the assets without pretending manuscript compilation was tested.

Finish with what changed, what was verified, and material unresolved issues. Stop after sufficient review; avoid optional repeated testing with no remaining concrete risk.
