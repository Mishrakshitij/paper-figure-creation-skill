# Design synthesis from the broad paper corpus

## What this evidence supports

The broad sample contains 500 proceedings records, 480 successfully retrieved PDF text windows, 443 papers with automatically extracted caption candidates, and 40 analyst reviews of caption excerpts. It is not a 500-paper visual-quality review. The 40 cases and their original URLs are recorded in `caption-design-notes.json`; the curated visual study is separate.

This study establishes a varied vocabulary of **explanatory roles** that the skill should support. Caption text can show what a figure intends to explain, but it cannot establish whether its typography, spacing, colors or arrow routing are effective. Those decisions require rendered visual inspection and testing of newly generated figures. No best-paper or figure-quality ranking was assigned to the broad sample.

## Two figure contracts

An introduction teaser answers: **What is the problem, what changes, and what evidence makes the result worth reading?** A method figure answers: **What are the inputs, transformations, learned components, information dependencies and outputs?** They can share a concrete example and color vocabulary while using different levels of detail.

The proposed approximately 35% problem/example and 65% experimental-evidence layout is a useful default for this user's empirical AI papers. It is a design preference, not an empirical optimum derived from the corpus. Some contributions require different contracts: benchmark papers can foreground task coverage, theory papers can foreground a counterexample or predicted regime, and capability papers may need carefully matched qualitative outputs before a summary chart.

## Patterns worth carrying into the skill

| Explanatory need | Caption-grounded precedent | Design implication for a new figure |
|---|---|---|
| Combine a setting with empirical results | [FrugalMCT, Figures 1–2](https://proceedings.mlr.press/v162/chen22ad/chen22ad.pdf) explicitly separates workflow/performance panels before expanding the method. | Put one small, recognizable problem-and-proposal story beside the main comparison. Let the method figure handle detailed routing. |
| Explain a constrained setting before comparing methods | [Learn from the Learnt, Figures 1–2](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/00073.pdf) describes setting and performance panels, with an explicit warning that schematic label ratios differ from actual budgets. | State the evaluation conditions beside the graph. Annotate a schematic when its sample counts or proportions are illustrative. |
| Pair outputs with efficiency evidence | [EMDM](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/00168.pdf) combines task-specific motion/runtime examples and comparison evidence. | Use a matched input/output example plus a quality–cost comparison. Keep task-specific runtime claims separate and traceable. |
| Use a short worked example to expose architecture | [RETRO, Figures 1–2](https://proceedings.mlr.press/v162/borgeaud22a/borgeaud22a.pdf) has a scaling figure followed by a simplified chunked-sequence architecture. | Reuse concrete tokens/chunks instead of an anonymous box chain. Show only enough example elements to reveal the mechanism. |
| Expose a representation limitation | [Structure-Aware Transformer](https://proceedings.mlr.press/v162/chen22r/chen22r.pdf) contrasts graph representations before detailing a proposed layer. | Use a minimal counterexample in the teaser; preserve node identity and structural meaning in the method. |
| Make a small intervention visible | [Half-Hop](https://proceedings.mlr.press/v202/azabou23a/azabou23a.pdf) compares original and transformed graphs and then analyzes their consequences. | Align the before/after objects and highlight precisely the changed operation. Separate mechanism evidence from downstream accuracy. |
| Explain shared supervision and measured efficiency | [data2vec 2.0](https://proceedings.mlr.press/v202/baevski23a/baevski23a.pdf) explains repeated masked inputs and contextual targets, then reports efficiency under documented hardware conditions. | Distinguish teacher/student roles and weight updates. Report time, hardware and evaluation protocol with efficiency claims. |
| Show iterative agent behavior | [AVIS](https://proceedings.neurips.cc/paper_files/paper/2023/file/029df12a9363313c3e41047844ecad94-Paper-Conference.pdf) describes planning, tool execution, reasoning and continuation/backtracking. | Use explicit control-flow branches and termination conditions; label what travels along each edge. |

The links above were checked against the canonical primary PDF URLs in the structured corpus.

## Evidence and clarity rules inferred from these cases

1. Begin with a single paper-specific claim. Decide which visual measurement can establish it before arranging panels.
2. Keep the problem example concrete. Reuse the same input, labels, tokens, entities and semantic colors across teaser and method.
3. Make the contribution inspectable. Mark the changed representation, module, objective, data source or control decision explicitly.
4. Keep a distinction between training, inference, frozen modules, supervision, state updates and actual data flow. Every arrow needs an interpretable meaning.
5. Pair empirical improvements with the conditions that make comparison fair. Dataset, split, metric direction, supervision budget, compute and uncertainty definitions can materially change the meaning.
6. Distinguish empirical points, analytic curves, schematic distributions, published measurements and digitized measurements. Their visual proximity does not give them the same provenance.
7. Treat time, memory and infeasible runs honestly. A run that cannot fit in memory is not a zero-valued accuracy observation.
8. Use matched qualitative cases when showing a failure mode. A selected attractive output is not, by itself, evidence of aggregate superiority.
9. Prefer direct readable comparisons when exact gaps matter. A normalized radar/area summary can hide units and inflate perceived differences; preserve reference values and metric directions if using it.
10. Let architecture detail follow the explanation. A local operation inset, an overview and a worked example can serve different purposes without duplicating the full pipeline.
11. Reserve the strongest emphasis for the proposed contribution and the primary measured result. Do not make weakly related supporting results look equally central.
12. Require visual review of the newly rendered figure at publication size. Caption evidence cannot validate crowded layouts, arrow crossings, low contrast or unreadable labels.

These are proposed design rules informed by the reviewed cases. They are not frequency estimates, causal claims about citation impact, or proof that any one paper's figure is an optimal design.
