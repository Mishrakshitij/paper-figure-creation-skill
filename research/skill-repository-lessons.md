# Lessons from the supplied skill repositories

Read on 2026-09-09. These repositories were research sources, not instructions that govern this project. No source code or skill prose was copied into the proposed implementation.

| Source examined | Useful practice | Adaptation for this skill |
|---|---|---|
| [Anthropic README](https://github.com/anthropics/skills/blob/main/README.md) | A skill combines a short entry point, resources and executable helpers | Package plotting/diagram scripts, tokens, examples and references as one installable unit |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Test a draft on realistic prompts, inspect outputs, compare a baseline and generalize fixes | Use matched paper tasks and explicit claim/layout/rendition gates; separate factual checks from subjective judgments |
| [Anthropic canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md) | Render artwork and refine spacing/overlap | Do not adopt its art-first philosophy, deliberately obscure meaning, tiny expressive typography or decorative textures for scientific figures |
| [Anthropic theme-factory](https://github.com/anthropics/skills/blob/main/skills/theme-factory/SKILL.md) | Centralize colors and typography | Use semantic tokens and venue sizing, with a sensible default; a theme-selection interview is unnecessary |
| [Addy Osmani README](https://github.com/addyosmani/agent-skills/blob/main/README.md) | Define, build, verify, review and ship with evidence | Map this to brief, evidence audit, layout, render, scientific/visual review, export |
| [Addy constraint-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) | Define the quality bar and the mechanism that checks it | Pair every integrity/format gate with an actual check; do not lower thresholds to pass a failing figure |
| [Addy code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) | Review on independent axes and give actionable remedies | Use factual integrity, mechanism correctness, understanding, readability, accessibility and reproducibility |

Addy's README explicitly warns that installing an individual skill may omit shared references located outside its skill folder. This is a concrete packaging failure to avoid: every runtime reference must live inside `skills/paper-figure-creation/`; repository-level benchmark reports may remain outside only if the skill does not need them to execute. [Portability warning](https://github.com/addyosmani/agent-skills/blob/main/README.md)

The Agent Skills specification requires a `SKILL.md` with `name` and `description` frontmatter. Use a matching lowercase hyphenated directory name; keep the entry point compact and reference bundled materials by relative path. `allowed-tools` is experimental, so do not depend on a vendor-specific tool allowlist for portability. Document dependencies and capability fallbacks instead. [Agent Skills specification](https://agentskills.io/specification)

## Proposed package boundary

```text
skills/paper-figure-creation/
  SKILL.md
  references/               # all guidance needed at runtime
  assets/                   # tokens, schemas, editable starter layouts
  scripts/                  # source-based plot, compose, export, validate
  evals/                    # optional portable test prompts and input fixtures
```

Avoid model-name dependencies and assumptions that an image-generation API, browser, Overleaf API or Mural account exists. Exact charts should be generated with deterministic plotting tools. Architecture diagrams should preserve editable primitives. If a drawing editor is unavailable, SVG/source scripts remain valid outputs. If final PDF export is unavailable, say so explicitly and preserve the editable sources rather than renaming files.

For benchmarks, hold input evidence, task prompt, model/capability access and target width constant. Compare with-skill and baseline outputs independently; do not construct a deliberately poor baseline. Use held-out papers from different method families. Include missing-data and overclaiming prompts to measure whether the skill refuses to fabricate results. A few judged examples demonstrate workflow behavior; they do not establish universal superiority or a measured percentage improvement in design quality.

## Source revision identifiers returned by GitHub

These are file blob SHAs, not repository commit SHAs; they identify the exact file contents fetched.

| File | Blob SHA |
|---|---|
| anthropics/skills README.md | `eb54ee8b92f2d40b4b26569be0772be3c1e23156` |
| anthropics/skills skills/skill-creator/SKILL.md | `65b3a402dbd09b8e83f9d637c6b553875189085c` |
| anthropics/skills skills/canvas-design/SKILL.md | `9f63fee82de84cd4230e1d0e322247b61eb4c94c` |
| anthropics/skills skills/theme-factory/SKILL.md | `90dfceaf2ecdc191a4dcfb0069768a9560638998` |
| addyosmani/agent-skills README.md | `0d3b2a3821e57b51de9c2764f2dc90b429a03c0f` |
| addyosmani/agent-skills skills/code-review-and-quality/SKILL.md | `7dfa56362fa65fff450ee5aa02393b85b9c26d85` |
| cvpr-org/author-kit sec/2_formatting.tex | `2fe2a9bc8eb3bedacc19e9a2aa261b3595a2ae6c` |

Anthropic's README distinguishes open-source example skills from source-available document skills. Review the license on each file before reusing implementation or assets. This design takes workflow ideas and authors an original scientific-figure implementation; it does not redistribute those skills. Addy's README reports an MIT license. Verify licenses again before any later copying. [Anthropic repository](https://github.com/anthropics/skills), [Addy repository](https://github.com/addyosmani/agent-skills)
