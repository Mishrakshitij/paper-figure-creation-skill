# Figure design system

Read this after choosing the visual argument in [visual-story.md](visual-story.md). Physical sizing, semantic styling and editable-tool choices should support that argument. The defaults here are authored design recommendations, not empirical findings or universal submission rules. Venue/year instructions take precedence. Sources were checked on 2026-09-09; verify the target venue again for a submission.

## Size the final figure first

Set the physical width before choosing font sizes. When unspecified, use the skill's 7-inch two-column draft and record that assumption. Obtain the actual manuscript width before final delivery. Redesign a dense two-column figure for one column rather than uniformly shrinking it.

| Item | Authored starting point | Adjust when |
|---|---|---|
| Main labels and axes | 8.5–10 pt at final size | Venue requires another size; final-size inspection finds crowding |
| Supporting labels and ticks | Prefer at least 8 pt | Verified venue guidance differs; remove secondary detail before shrinking |
| Panel label/title | 9.5–11 pt, modest emphasis | Hierarchy becomes unclear; avoid an oversized poster headline |
| Panel gap | About 3–5 mm | Axis labels, legends or inset connectors need more room |
| Node-to-node clearance | At least about 4 mm | Branches or connector labels need space |
| Data strokes | About 1.1–1.6 pt | Dense uncertainty bands or final-size print require adjustment |
| Axes/node boundaries | About 0.7–1.0 pt | Thin lines disappear in the actual output |

The current CVPR 2026 author kit specifies 3.25-inch columns, 6.875-inch total width, 9 pt Helvetica callouts, and asks authors to match figure fonts to body text and preserve print legibility. It also asks for a discriminative feature beyond color in plots. These are source-specific instructions, not permission to apply CVPR geometry to another venue. [CVPR author kit](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex)

Nature's guidance uses a different 5–7 pt figure-text range and asks for editable vector text/lines, standard fonts, labeled axes with units and accessible colors. Borrow the production principles; do not turn its font sizes into AI-conference defaults. [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)

## Establish hierarchy before styling

Set three levels: major regions visible in a thumbnail; objects and operations readable at paper size; local notation available on close inspection. Use region headings, position and spacing to establish order before assigning colors. A heavier boundary should identify a meaningful distinction, such as the proposed operation or an evaluation boundary, rather than surround every object equally.

Allocate room according to the question a region answers. Conventional machinery can be compact while a novel edit, alignment, update or aggregation deserves an expanded representation. Space between stages can carry flowing-object labels and make correspondence clearer; an arbitrary grid of equal boxes rarely serves every stage equally well.

Dense diagrams can remain legible when repeated units share a grammar: the same stage columns, object widths, local label positions and edge conventions. Preserve a clear main route and reserve separate routing channels for feedback, supervision or callouts. Avoid enclosing every nested concept in another rectangle; alignment and whitespace can often express the grouping.

## Use semantic tokens

Read `assets/theme.json` when using the bundled renderer. Keep the same roles across teaser, method and experimental panels; tokens can change for a paper's established style without changing scientific meaning.

| Role | Encoding | Guardrail |
|---|---|---|
| Proposed method/module | One accent + direct method name + distinctive marker or border | Highlight identifies the proposal; it does not assert significance or superiority |
| Primary baseline | Dark neutral + distinguishable marker/line style | Muted baselines must remain readable |
| Other baselines | Distinct dark-enough hues or grays + shape/line redundancy | Do not collapse several methods to indistinguishable pale lines |
| Conventional backbone | Pale neutral fill, dark text, visible boundary | “Conventional” does not mean unimportant or frozen |
| Novel operation | Accent boundary plus a visible input/output transformation or local operator | A color change and a method name alone cannot explain novelty |
| Training-only content | Labeled lane/group; optional warm accent | Do not encode training-only, loss and gradients identically without explaining it |
| Text | Dark neutral on plain background | Avoid colored paragraphs or text over busy examples |

Use one standard sans-serif family plus a compatible math font. Render symbols from the same notation used in the manuscript. Keep normal text and scientific labels editable when possible. Prefer flat fills and restrained boundaries for paper graphics; avoid effects that obscure objects or imply unsupported magnitude. An icon, miniature image or texture is useful when it conveys the actual task, object type or state. A field-valued gradient can be scientific data; a decorative gradient behind a module usually adds little.

Assign color after deciding what it means. It may distinguish candidate identity, modality, trainability or proposal status, but a single hue should not silently switch among those meanings in one figure. Keep persistent objects recognizable across panels. Use a local key or direct labels when several semantic families coexist. Do not enforce one accent if the mechanism genuinely requires multiple distinguishable states; do not add colors merely to make boxes look different.

## Choose object representations deliberately

| Object or relationship | Useful representation | Retain / omit |
|---|---|---|
| Passage or generated edit | Document with a short meaningful excerpt and selected span | Retain the fact or instruction that drives the example; omit unrelated prose |
| Prompt or configuration | Compact code/text card with a few actual or schematic fields | Retain consequential fields and mark omissions; avoid unreadable miniature code |
| Grid or image transformation | Matched crops/cells with shared geometry and targeted overlays | Retain correspondence; do not invent attention maps or prediction quality |
| Token or candidate identity | Repeated token/chip/row with stable label and redundant visual cue | Retain identity through selection and merging; avoid random colors |
| Tensor or low-rank operator | Matrix/factor geometry, dimensions, explicit operation | Retain algebra and shape change; omit decorative cell detail |
| Original/adapted model | The same model shape with a clear state/parameter label | Retain which weights change and which are reused; do not imply a new architecture |
| Agent/environment interaction | Repeated local interaction pattern plus separate update path | Retain what is observed versus predicted and where learning signals go |

Use these when they explain an otherwise hidden distinction. A conventional encoder may need only a labeled block. A generated edit that is the contribution often needs content. [semantic-primitives.md](semantic-primitives.md) supplies editable building blocks; it is not a mandatory visual vocabulary.

For a custom palette, `#0072B2` (proposal), `#5F6368`, `#986C00` and `#8E5681` are optional dark-enough starting colors on white; assign redundant markers. This custom set is not the exact Okabe–Ito palette, and a palette's name is not evidence that a particular rendered figure is accessible.

Target at least 4.5:1 for ordinary text and 3:1 for meaningful marks against adjacent backgrounds as practical accessibility checks. Check the actual palette and final rendering: a thin line can remain hard to see even when nominal contrast passes. Provide labels, shapes, line styles or keylines so hue is not the only cue. [W3C use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color), [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

## Compose evidence-heavy teasers

Use 35% concept/example and 65% evidence as the starting content-area allocation, with the requested 30–40%/60–70% range. Exclude outer caption/margins; include a plot's axes, labels, legend and claim annotation with its evidence region. Do not inflate evidence area with blank colored containers. This allocation comes from the user's preference, not a measured rule about successful papers.

Choose one dominant comparison and at most a few complementary panels. Each panel should answer a different scientific question. Pair quality versus budget with fixed-budget performance, for example, rather than repeating the same rank order three ways. Align chart baselines and panel titles. Let the strongest supported evidence receive the most room. Read `teaser.md` for the mode-specific story and chart selection.

Concept and data should share the same method names, example identity and semantic accent. The concept panel exposes the specific intervention; the empirical panel tests its consequence. A generic “Our model” box plus a winner badge does not establish that connection.

## Preserve method semantics

Assign edge styles by meaning, and define only the types present. A solid arrow can carry forward data, a dashed arrow training-only supervision, and a dotted connector an enlarged-detail callout. These are suggested conventions; the legend and manuscript semantics are authoritative.

Do not use one dashed style interchangeably for gradient updates, optional execution, frozen connections and supervision. Use separate lanes, labels or distinct styles when more than one meaning occurs. A callout connector is not computation. Crossings do not imply joins; merges need a visible operator or junction. Keep inset borders and labels out of the computational path. Read `method.md` for topology and mechanism details.

## Editable authoring choices

| Content | Canonical source | Useful exports |
|---|---|---|
| Experimental plot | Data + plotting code/spec | Vector PDF and plain SVG |
| Concept or method geometry | Native `.drawio`, SVG source or programmatic spec | PDF, SVG, PNG preview |
| Real visual example | Original image/output + crop/overlay specification | Embedded raster with vector labels |
| Manuscript caption and alt text | Separate text files | LaTeX/document text |

Never manually change a plotted coordinate, bar height or uncertainty extent inside a graphics editor. Regenerate from data. Cosmetic layout edits may be made in an editor, but preserve one canonical geometry source and record how to reproduce them.

For draw.io, generate uncompressed XML with stable unique IDs, valid parents and explicit edge endpoints. Its native structure supports editable shapes, connectors, layers and metadata. Validate structure and render with draw.io when available; a separate SVG renderer is not proof that the native file opens correctly. [draw.io generation reference](https://www.drawio.com/docs/reference/diagram-generation/)

Keep the native `.drawio` original even if an SVG includes embedded diagram data. Use plain/native text where possible; formatted SVG labels can introduce `foreignObject` compatibility problems. Fix the white background and colors for paper output so adaptive dark-mode styling cannot change the figure's meaning. [draw.io SVG export](https://www.drawio.com/docs/manual/export/export-to-svg/)

Mural is useful for storyboards, comparing layouts and reviewer annotations. Its documentation distinguishes procedural flowcharts from data-flow and schematic diagrams and provides PDF/PNG export. Use a board export as a review snapshot; keep exact plots and method primitives in the reproducible vector sources. [Mural diagram types](https://www.mural.co/blog/flowcharts), [Mural export](https://learn.mural.co/lessons/export-murals)

Keep required scripts, assets and references inside this installed skill. A single-skill install may omit repository-level shared files; the supplied Addy Osmani repository documents this exact portability issue. Avoid vendor-specific tool dependencies when plain data, code and SVG can preserve the workflow. [Addy repository portability note](https://github.com/addyosmani/agent-skills/blob/main/README.md), [Agent Skills specification](https://agentskills.io/specification)

Read `delivery.md` for manuscript insertion and export checks. An editable source, a vector export and a preview serve different purposes; retain all three when requested rather than treating a flattened PNG as the master.

## Setup-specific composition

For an eligible benchmark/environment figure, select the grammar in [benchmark-environment.md](benchmark-environment.md). Keep task, tested system, environment/state and evaluator distinguishable through labels and geometry as well as color. Use a concrete sample or interaction at the center, with construction and aggregation only as detailed as the paper needs. The teaser 35:65 area preference does not apply.
