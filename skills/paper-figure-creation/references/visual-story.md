# Turn the science into a visual story

Use this reference before styling a new complex figure or redesigning a figure that feels generic. The objective is to make the particular paper's reasoning visible. More icons, more panels, and greater density are not themselves improvements.

## Read visual references as explanations

Open the supplied figure image or render the relevant PDF page. Read the caption and surrounding method text to disambiguate the drawing, but keep these two observations separate: what the pixels communicate and what the prose supplies. A caption-only review cannot establish composition, legibility or visual quality.

For each useful reference, record one short observation in each column:

| Observe in the rendered figure | Transferable question for the new paper |
|---|---|
| Concrete objects: text passages, grids, trajectories, tensors, messages | Which object must the reader recognize to understand this task? |
| Correspondence: repeated example, aligned alternatives, retained token/color identities | What stays the same while the proposed operation changes something? |
| Structural emphasis: repeated rows, nested stages, perimeter feedback, local enlargement | Which relationship deserves the figure's largest organizing structure? |
| Detail allocation: one expanded operation, concise surrounding machinery | Where does the reader need to look inside a module? |
| Evidence organization: shared axes, task groups, endpoints or paired outcomes | Which comparison establishes the paper's claim most directly? |

Record the source URL, figure/page, image actually inspected, and the principle adopted. Do not equate a famous paper with an excellent figure, or treat an attractive design as proof of its scientific claims. Borrow a useful grammar; author a fresh composition with this paper's semantics and data.

## Extract the visual units

Read the abstract, method, one worked example and the relevant result table together. Write a short noun/verb/state map before drawing:

| Unit | Example | What belongs on the canvas |
|---|---|---|
| Object | Context passage, candidate edit, grid task, trajectory | A recognizable small instance or compact symbolic representation |
| Transformation | Select, rewrite, adapt, retrieve, aggregate | The visible input/output difference and a precise operation label |
| State | Original/adapted weights; observed/predicted environment | Distinct identity or state label that persists through later stages |
| Relation | Conditions, compares, supervises, updates, shares | A deliberately routed relation with one defined meaning |
| Evidence | Score after adaptation, quality at a fixed budget | A mark generated from the reported value and its comparison context |

For each proposed object, ask: if its label disappeared, would its shape or contents still convey useful information? A generic module box can legitimately stand for conventional machinery. It becomes inadequate when the reader needs its internal transformation to understand the contribution.

Choose a **minimum sufficient worked example**. It needs enough content to expose the difficulty and the proposed change, without becoming a second method section. For text, a meaningful sentence or a short structured field is often better than ornamental gray lines. For a grid, preserve the cells needed to see the transformation. For tensors, show dimensions and the operation rather than arbitrary decorative cells. Use observed examples when the figure makes a performance claim; clearly label invented teaching examples as schematic.

## Save a representation contract

Write this compact design note beside the figure source, in ordinary Markdown or structured data:

```text
Visual thesis: What relationship must a reader understand?
Example: The input, relevant intermediate state, and output; observed or schematic.
Object encodings: What each document/grid/token/matrix/state denotes.
Invariants: Identities, positions, scales, and conditions held constant.
Transformations: What visibly changes at each consequential operation.
Reading path: Entry point → main relation → outcome → supporting detail.
Novelty location: The specific visible operation or relationship carrying the proposal.
Detail boundary: What is omitted and where the caption explains it.
Evidence link: Which plotted comparison tests the illustrated consequence.
```

This is a design aid, not a new scientific specification. Check it against the manuscript. If the contract needs a claim the paper does not establish, revise the story before the graphics.

## Compare different compositions

For a complex new design or a failed composition, draw three rough thumbnails using the actual object names and representative content. Keep them cheap: rough geometry, example snippets and arrow routes are enough. Color variants of the same layout are one alternative.

| Composition | Choose when | Watch for |
|---|---|---|
| Matched baseline/proposal lanes | The contribution changes one part of an otherwise comparable process | Unequal scales or different examples can imply an unfair comparison |
| Shared example with a local operator enlargement | The core idea happens inside one otherwise conventional stage | An inset connector can be mistaken for forward computation |
| Aligned candidate rows and common scoring/update column | Several edits, agents or hypotheses undergo the same operations | Collapsing all rows into one arrow hides selection and correspondence |
| State trajectory with an outer update loop | A method changes a state repeatedly or learns how to adapt | A decorative loop can hide which state or parameters actually update |
| Spatial scene plus computation strip | Geometry, motion or a field is intrinsic to the method | An ordinary flowchart can discard the coordinate relationship |
| Concept above evidence, or concept beside evidence | The example and empirical consequence need different aspect ratios | Equal panel sizes can assign attention to the wrong part of the argument |

Choose the alternative that makes the critical relationship easiest to recover at the intended size. Record a sentence explaining the choice and one rejected trade-off. Existing, successful compositions need not be rebuilt for a label repair or data update.

## Build three scales of reading

At thumbnail scale, the reader should see the main grouping and which region carries the contribution or result. Use position, area and restrained contrast; do not rely on tiny labels.

At normal paper size, the reader should recognize the worked example, main operations and comparison. Align corresponding objects or stages so the eye can compare them directly. Keep labels near what they describe. A repeated document, token, state or branch should preserve enough visual identity to be recognized without rereading its name.

At close inspection, the reader can recover dimensions, state indices, local equations, conditions and source detail. Put these where they answer a local question rather than filling every open area. The caption can define omissions and evaluation conditions; it should not have to explain the entire visual route.

**Controlled density** means each region earns its space. Add detail when it resolves a specific ambiguity: which sentence became an edit, which candidate earned a reward, which gradient is fused, or which token survives selection. Remove detail that repeats a label, decorates empty space, or competes with the main relation. There is no universal box count, icon quota or density score.

## Repairs that change understanding

| Weak rendering | Concrete redesign | What to check afterward |
|---|---|---|
| `Passage → Model → Better answer` | Show one passage fact, the generated update artifact, the adaptation step, and a corresponding question/answer; label schematic content | The reader can tell whether the passage is an inference input or used only for adaptation |
| `Generate candidates → Evaluate → Learn` in three large boxes | Give candidates aligned rows; carry their identities through adaptation, evaluation and reward; route the policy update outside the rows | A reward can be traced to the candidate that produced it, and the update destination is explicit |
| Two architectures differ only by an accent-colored box | Align the unchanged context and enlarge the actual changed operation with its input/output representations | The reader can say what the proposal does without quoting the module's name |
| A grid icon beside `reasoning module` | Use the same small grid before/after the operation, preserving meaningful cells and adding only necessary transformation cues | The grid teaches the operation and is not mistaken for a measured success case |
| Several agent/environment boxes plus tangled arrows | Repeat a consistent row grammar; align shared stages; separate environment interaction from calibration or parameter-update paths | Repetition and shared information are distinguishable from independent components |
| Dense collection of performance panels | Group panels by the questions they answer; align comparable scales and remove redundant rank-order views | All relevant evidence remains represented, including inconvenient outcomes |
| A large `+30%` badge dominates small axes | Put the supported comparison in the plot with its baseline and units; make the concept reveal the intervention | The takeaway survives removal of the badge and stays within the evidence's scope |

These are conditional recipes, not templates to apply wholesale. In particular, a radar chart from a reference paper is appropriate only if its dimensions, normalization and comparisons make sense for the new evidence; attractive geometry alone is insufficient.

Use [semantic-primitives.md](semantic-primitives.md) for reusable vector ingredients. Their role is to reduce drawing effort while preserving paper-specific content, not to make different algorithms look identical. Complete the separate scientific and communication reviews in [review.md](review.md).
