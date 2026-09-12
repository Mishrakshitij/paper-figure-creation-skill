# Reference review: BAT and Qwen-Drive-1.0

Review date: 2026-09-12. This is a design critique of two user-selected papers and the current skill examples, not a ranking of their scientific quality. Two official figure assets were actually inspected as rendered images. Other figures below were located or read through captions only. Original reference artwork is not redistributed.

## Inspection record

| Paper | Asset inspected as pixels | Stable locator / identity | Scope |
|---|---|---|---|
| BAT: Behavior-Aware Human-Like Trajectory Prediction for Autonomous Driving, arXiv 2312.06371 | Architecture corresponding to Figure 3, historical official repository asset | [Framework3.png](https://github.com/Petrichor625/BATraj-Behavior-aware-Model/blob/2c46570a0099dd7bc27c88f95a5d9ef727a2efd1/Figures/Framework3.png); blob `70ae3a4a03149af06906c8c5891ce3b8545dbe1c` | Full image inspected. Historical snapshot is necessary because the current repository removed its original Figures directory. Exact pixel equivalence to the final paper PDF was not verified. |
| Qwen-Drive-1.0: An Initial Step towards a Vision-Language Foundation Model for Autonomous Driving, arXiv 2609.00111 | Introductory performance overview corresponding to Figure 1 | [intro.png](https://github.com/QwenLM/Qwen-Drive-1.0/blob/ac4d2300ad255ab9e0bb4a54b1b699280b0eed51/assets/intro.png); blob `79c5e84ff06d69be04fb7e426492c88ff48bb6e5` | Full image inspected. Exact equivalence to the report's current numerical results was not established. |

BAT Figure 1's [polar-versus-grid pooling comparison](https://arxiv.org/html/2312.06371v2#S1.F1) was read through its caption and surrounding text; its image was not successfully inspected. Qwen's [architecture and method text](https://arxiv.org/html/2609.00111v1#S2.F2) was read, but its [overview.png](https://github.com/QwenLM/Qwen-Drive-1.0/blob/ac4d2300ad255ab9e0bb4a54b1b699280b0eed51/assets/overview.png) could not be obtained as image bytes through the available connector. The file exceeds the contents endpoint's inline-content limit. The large Qwen PDF was also rejected by the web retrieval service. These limitations must not be relabeled as visual reviews.

## What the inspected figures accomplish

### BAT architecture

The input and output are full road scenes, not boxes bearing those names. Repeated car silhouettes preserve vehicle identities; colored bodies distinguish ego, surrounding, pooling, and unrelated vehicles. Lane markings and interaction ellipses make spatial relationships visible before the module labels are read.

The middle uses unequal parallel bands: a behavior path above, interaction and priority mechanisms centrally, and position information below. Recurrent operations, feature slabs, vectors, and attention bars have different visual forms. An enlargement cone links a feature region to a detailed attention operation. The decoder contains its own hierarchy, explicit addition operators, and a repeated recurrent stack. The final road scene contains several trajectory possibilities with probability labels.

This density supports three reading depths: traffic task; branches and module arrangement; internal representation and fusion. Some choices still deserve scrutiny: many dashed container borders compete, certain decoder connections are long, and perspective slabs add visual weight. The transferable strength is meaningful representational variety and connected scales, not copying every decoration. [Official architecture asset](https://github.com/Petrichor625/BATraj-Behavior-aware-Model/blob/2c46570a0099dd7bc27c88f95a5d9ef727a2efd1/Figures/Framework3.png)

### Qwen performance overview

Two large radial assemblies organize the evidence. Four outer arcs establish task families; benchmark names sit close to their respective bar groups. The proposed model has a consistent saturated purple and white numeric labels, while comparator bars use lighter fills and dark values. Each assembly has its own compact legend.

The center illustrations carry task cues: inspection and visual understanding on one side, geometric scene representation and a trajectory on the other. They provide an entry point into otherwise dense experimental content. Exact numbers, benchmark groups, families, and overall capability breadth form distinct levels of hierarchy.

Radial arrangement is not automatically the best quantitative encoding: it rotates labels and makes lengths across groups harder to compare. Mixed metric scales and lower-is-better scores require explicit handling, and the pictured comparator set and numbers must be reconciled with source tables before reuse. Preserve this figure's coherent visual identity and hierarchy while independently selecting honest, readable chart geometry for the new paper. [Official overview asset](https://github.com/QwenLM/Qwen-Drive-1.0/blob/ac4d2300ad255ab9e0bb4a54b1b699280b0eed51/assets/intro.png)

## Concrete gaps in the current skill outputs

The existing MAE method image and LoRA teaser were inspected locally for this comparison. Their scientific organization is useful, but the visual language is substantially narrower than the user's references.

| Current behavior | Communication consequence | Design change to test |
|---|---|---|
| MAE's reconstruction output is the word “Pixels” in a rectangle | The reader cannot see what reconstructing the missing content means | Carry one recognizable image through patching, visible-token selection, reassembly, prediction, and target comparison |
| Most method operations use similar outlined boxes | Objects, transformations, learned representations, and control signals look alike | Assign explicit visual forms to these categories; use geometry to show what changes |
| Large headings and outer gray containers dominate the available area | The figure resembles an explanatory slide, with little mechanism detail at intermediate scale | Reduce headline weight; spend the recovered area on a scientifically useful representation or inset |
| LoRA's concept is a weight equation followed by an isolated SQL example | The task example and weight change are nearby, but their causal connection is mostly supplied by text | Trace the same task instance through frozen and adapted model behavior, with the update branch visibly attached |
| QA emphasizes correctness, overlap removal, and successful exports | A clean but generic diagram can satisfy the existing stopping criteria | Add a reference-relative communication critique and a visible mechanism test before declaring the design complete |

## Original design implications for the revision

1. **Specify visual objects before layout.** For every critical noun in the brief, choose an observable representation: document with excerpt, token sequence, road scene, model state, ranked candidate set, sparse matrix, or reconstruction. State which feature of the object carries meaning. Do not add an icon merely to decorate a box.
2. **Choose three depths deliberately.** The whole figure should reveal the task and changed idea; the middle scale should show major branches or experimental questions; one selected inset should explain the novel operation. All three must remain legible at the intended paper width.
3. **Preserve an example's identity.** Use consistent content, marks, and role colors so that the reader follows a specific example across representations. A new thumbnail at each stage can falsely imply a changing input.
4. **Give novelty local geometry.** Show the insertion, selection, reweighting, generation, update, or fusion itself. A colored enclosing label is insufficient. Where the key mechanism cannot be understood from the current geometry, redesign the geometry.
5. **Use varied marks within a restrained visual system.** A theme should standardize typography, line weight, semantic colors, and spacing. It should not force every scientific object into a universal rounded rectangle.
6. **Evaluate a visible upgrade.** Produce a new figure with a stronger task representation and mechanism inset, inspect it beside the old output at the same physical width, and record what a reader can now infer from the marks. Do not count extra details, corpus size, or passing unit tests as a substitute for that judgment.

These are proposed design requirements derived from the critique. They have not yet been validated as a general improvement over another figure-generation workflow.
