# Conditional benchmark and environment figures

The skill now supports a third figure mode for papers that actually describe a benchmark, environment, task-construction process or substantive evaluation setup. It explains **what is tested, what the system sees or does, and how success is judged**. The original teaser and method modes remain available; an agent chooses relevant modes rather than automatically producing three figures.

## Research behind the change

The [research record](../research/benchmark-environment/README.md) contains 51 distinct paper/project entries, including 36 discovered through nine dated Hugging Face monthly lists. Seventeen author-hosted figure assets were actually inspected. The remaining reviews are explicitly text-only and range in depth. Official project sites, repositories and proceedings complement arXiv. Upvotes support discovery, not a claim that these are objectively the best diagrams.

The design guidance differentiates static/procedural benchmarks, interactive environments, construction pipelines, controlled variants and evolving worlds. It calls for one concrete case, preserved object identity, explicit information access, task-specific scoring, and source-grounded state/reset/timing semantics when applicable. The teaser's 35:65 area preference does not apply to setup figures.

## Implementation

- The [skill router](../skills/paper-figure-creation/SKILL.md) selects this mode only after locating substantive setup evidence. It distinguishes new, adapted and existing setups. Results tables and benchmark names alone do not trigger it.
- The [setup guide](../skills/paper-figure-creation/references/benchmark-environment.md) and [brief](../skills/paper-figure-creation/assets/benchmark-brief.md) cover source extraction, visual families, concrete examples, private evaluator routes and mode-specific review.
- The JSON engine supports `kind: benchmark`, with a source-anchored eligibility and setup contract. Static tasks require no invented episode fields; interactive/mixed tasks require observation, actions, transition, reset and termination descriptions.
- Benchmark figures use the existing vector geometry and export SVG, PDF, PNG and editable diagrams.net cells. A visibly synthetic template documents the interface. Custom vector layouts remain appropriate for richer task representations.

The declared contract does not automatically verify source truth or information leakage. Node visibility is metadata, not a private-information security mechanism. Native diagrams.net XML is checked structurally; application rendering has not been verified.

## Original examples

| Example | Distinct design problem | Source/illustration boundary |
|---|---|---|
| [WebArena](../examples/webarena-setup/) | Website/task context, one observation/action/state change, separate functional evaluator | Real v0.2.0 task 601; original schematic UI, element ID and single action; no agent run |
| [ReasoningGym](../examples/reasoning-gym-setup/) | Configurable task generation, model-visible question, private entry data and task-specific verifier | Documented generated entry; illustrative model response; no measured performance |

Both examples began with three different composition sketches. Their build scripts, editable vectors, captions, source notes and print-size proofs are preserved beside the figures. They are guided design iterations, not blind use of the skill and not matched comparisons against another workflow.

## Validation

The automated suite contains **61 passing tests**, including **12 new benchmark tests** for conditional eligibility, source references, static/interactive contract differences, geometry, text and diagrams.net export. Existing teaser/method tests still pass.

An independent agent, with expected answers withheld, applied the skill to [14 authored manuscript-fragment fixtures](../tests/setup-routing-cases.json). All 14 presence/selection decisions matched the predefined expectations: seven selected, five absent and two unclear. [Observed answers](../tests/setup-routing-observed.json) and [comparison record](../tests/setup-routing-assessment.json) are preserved. This is a small instruction-following check, not a real-paper generalization benchmark. Reviewer feedback led to clearer absent/unclear definitions and separation of visual composition families from the renderer's execution-family field.

Both final PDFs were separately rasterized and visually inspected at 110 dpi: 7-inch width, intact text, one vector page each and no embedded raster images. SVG text remains editable. This checks standalone exports, not placement in a manuscript.

The [independent figure review](benchmark-independent-review.md) records pixel-first interpretations before consulting source briefs, plus specific repairs and remaining limitations. Actual final-manuscript placement remains untested because no target manuscript/template was supplied. Passing code checks alone does not establish scientific or visual publication readiness.
