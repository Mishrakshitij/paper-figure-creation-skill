# Art direction for scientific explanation

Use this when a scientifically correct figure still feels generic, visually flat or difficult to grasp. Image generation often offers richer visual possibilities; treat that as a design opportunity to test, not proof that a generated figure is more accurate or easier to understand. The useful target is a memorable **visual relationship**, with the paper's semantics intact.

This guidance applies to teaser, method and eligible benchmark/environment figures. It does not create a fourth scientific figure mode. Begin with the representation contract in [visual-story.md](visual-story.md), then make the following decisions before polishing a render.

## Direct attention toward a relationship

Name the first thing a reader should see as a noun plus a visible change: “the same page after submission,” “a few image patches restored to their positions,” or “one example under two different observation rules.” A title, method logo or generic model box rarely supplies that relationship.

Make the focal objects form the strongest visual group. Use their size, proximity, contrast and surrounding whitespace together. Give conventional machinery and configuration less visual weight when they are context. A large quiet region can make a small meaningful change easier to see; filling every region with a card has the opposite effect.

Do not prescribe a universal focal-area percentage. In a teaser, the established concept/evidence allocation still applies: attention may come from an annotated data relationship while plots retain most usable area. In a method, emphasize the changed operation. In a setup figure, emphasize the task or interaction that defines the evaluation challenge.

## Give objects recognizable structure

Choose a small vocabulary of domain objects before choosing box styles. Useful silhouettes include browser windows, document sheets, token strips, scene patches, spatial maps, code diffs, tree branches and timelines. Use the internal detail that reveals their role: the actual changed line, the clicked control, the retained patch identity, the visible part of a scene.

An object should earn its illustration by explaining something. Avoid a decorative robot for every model, a city for a set of websites, or a glowing brain for an unspecified computation. A compact conventional block is appropriate for machinery the paper does not need to explain. A uniform family of rounded cards is appropriate only when the objects really have parallel roles.

Choose viewpoint deliberately. Frontal views support reading text and comparing state. Top-down views reveal spatial constraints. An exploded view can expose assembly or restoration. Use perspective locally when it clarifies ownership, stacking or occlusion; keep plots, matrices that require exact alignment, and authoritative text in readable planes.

## Draw the visual verb inside the objects

An arrow states a relation; the objects should reveal the consequential change. Choose a device that matches the operation:

| Scientific operation | Useful visual device | Preserve |
|---|---|---|
| Select, mask or prune | Same object with selected content retained and other content removed or explicitly masked | Stable identities and actual selection rule |
| Rewrite or edit | Aligned text/code before and after, with the changed span visible | Unchanged context and source versus illustrative status |
| Restore, assemble or fuse | Parts and destination slots, a local assembly view, or aligned contributor rows | Exact correspondence and merge semantics |
| Act on an environment | Action adjacent to its target, then the same state after the effect | Observation/action direction and private evaluator boundary |
| Compare conditions | Matched views with a selective change cue | Same example, scales and controlled conditions |
| Iterate or update | A state sequence with an explicitly routed update path | Which state changes and what remains fixed |

Do not add every device at once. If showing the transformation forces illegible density, use a local enlargement and simplify surrounding stages. A correspondence line or explanatory leader must not look like an extra computational input.

## Stage space to explain causality

Put actions near their targets and outcomes where the eye naturally continues. Group by ownership or stage with alignment and whitespace before adding enclosing frames. Use an environment boundary, training lane or evaluation region when it encodes a real distinction.

Reserve clear routes for connections before filling objects. Keep observation, action, scoring and parameter-update routes distinct when their meanings differ. An elegant continuous path must not imply access to a hidden answer, future context or training-only label. Depth cannot fix a wrong arrow.

Arrange one rich explanatory region with quieter support. A worked browser task can carry concrete UI detail while the agent is a compact label. An image-patch transformation can carry texture while encoder/decoder machinery remains simple. Configuration can become a small strip if it does not explain the novelty. Retain the on-canvas qualifiers needed to prevent scientific misreadings; move secondary detail to the caption.

## Use material and depth cues only where they help

Subtle layering can denote a stack, an inset can expose an interior operation, and a restrained shadow can separate an illustrative foreground object from its background. Maintain a consistent viewpoint and lighting for related pictorial objects. Avoid giving every rectangle the same shadow or gradient.

Depth, thickness, area and glow can be read as quantity or importance. Do not let decorative stack thickness imply token count, perspective distort chart values, a bright border imply trainability, or realistic rendering turn a schematic outcome into apparent evidence. Use exact repeated elements when count matters, and explicit symbolic notation when it does not.

## Choose the authoring strategy

| Strategy | Choose it when | Keep exact |
|---|---|---|
| Vector scene and diagram | Geometry, UI, tokens, symbolic objects and local changes explain the task | Object identities, labels, relation endpoints and all quantitative marks |
| Hybrid illustration plus vectors | Recognizable image content, texture or a scene materially helps teach the task | Scientific wiring, masks, coordinates, text, equations, scales and data plots |
| Text-free concept illustration | Exploring a pictorial subject or supplying a nontechnical problem vignette | Do not treat this illustration as a verified architecture, experiment or result |

Read [hybrid-authoring.md](hybrid-authoring.md) for asset generation and composition. Image generation is optional. Its absence should not prevent a rich vector composition; its availability should not force a raster asset into a symbolic problem. Export format alone does not determine whether a figure is editable: an SVG containing a flat screenshot is still mostly raster artwork.

## Review what the composition actually communicates

Compare before and after using the same task, source facts and intended size. If the redesign removes material content, record the changed scope instead of calling it a fair visual-only comparison.

First show the figure without its design brief. Ask the reviewer what draws attention first, what changes, and which object they follow next. Then ask the mode-specific science questions. Inspect a thumbnail for dominance, the final-size proof for comprehension, and enlarged details for rendering defects. Check that grayscale preserves necessary distinctions.

Record concrete differences: “the reader now notices the state change before the taxonomy,” “the photo hides the mask pattern,” or “the private answer route is clearer in the older version.” A richer figure may be worse; retain or restore the clearer design when appropriate. Do not award an aggregate beauty score and call it scientific validation.

If “interactive” means actual clicking, hovering or animation, treat that as an optional companion deliverable with a static publication figure. Do not claim a PNG, SVG preview or cinematic composition is interactive by itself.
