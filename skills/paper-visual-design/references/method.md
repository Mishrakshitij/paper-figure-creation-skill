# Method / architecture

Use the foundation's [method contract](../foundation/references/method.md), [visual story](../foundation/references/visual-story.md), and [semantic primitives](../foundation/references/semantic-primitives.md) selectively.

Extract input/output objects, operators, branch/merge meaning, tensor/representation dimensions, parameter sharing, learned/frozen components, objective, and phase-specific information access. Cite source locations for every substantive connection. Resolve an uncertain arrow before drawing it as fact.

Show recognizable objects and their contents: tokens with stable indices, retrieved documents with consistent evidence identities, matrix factors with compatible dimensions, candidate edits with their corresponding adapted states. Enlarge the new operation. Use a small local example to make its effect visible.

Preserve the topology through visual polish:

- A sum, concatenation, selection, and shared conditioning are different operators.
- Distinguish data flow, gradient/update flow, supervision, and feedback using labels plus line styles.
- Route feedback outside the main reading path. Put a return arrow into the operation it updates, not a decorative enclosing box.
- Separate training, calibration, inference, and evaluation lanes when access or behavior differs. A test evaluator does not imply test labels are visible to the model.
- Show independent candidate copies as independent branches; do not accidentally imply sequential weight updates.

Choose an editable geometry route: custom SVG/TikZ/Matplotlib for exact scientific objects, or native draw.io for interactive editing. A generated whole-figure composition may be a reference, but rebuild authoritative wiring and text. Keep one canonical source and verify native application exports if claiming draw.io delivery.

Caption the concrete mechanism and scope. A reviewer should be able to trace one example and identify the proposal without guessing what arrows mean.
