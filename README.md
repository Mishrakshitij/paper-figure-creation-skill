# Paper Figure Creation Skill

A portable agent skill for two AI-paper figure types:

- **Introduction teaser:** a concrete problem and proposed idea in roughly 35% of the usable area, with source-grounded experimental evidence in roughly 65%.
- **Method / architecture:** an editable explanation of the computation, branches, training signals, and actual proposed change.

The skill combines design instructions, a figure-pattern atlas, a semantic theme, editable templates, deterministic rendering, and numerical evidence checks. It supports a review-and-repair workflow rather than promising an automatic perfect figure.

![Original MAE teaser redraw](examples/mae-teaser/figure.png)

## Install

Clone this repository:

```bash
git clone https://github.com/Mishrakshitij/paper-figure-creation-skill.git
cd paper-figure-creation-skill
```

Copy the **entire** `skills/paper-figure-creation` folder into your agent's skill location. All runtime resources are inside that folder; the repository's research and gallery files are optional.

For Codex, a personal installation is:

```bash
mkdir -p ~/.agents/skills
cp -R skills/paper-figure-creation ~/.agents/skills/
```

For Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R skills/paper-figure-creation ~/.claude/skills/
```

If an installation already exists, review your local customizations before replacing it. Project-local `.agents/skills/` and `.claude/skills/` are alternatives. These paths follow the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills), checked September 2026. Other agents can load the standard [SKILL.md](skills/paper-figure-creation/SKILL.md) folder or read it explicitly; runtime capabilities still vary.

Example request:

> Use paper-figure-creation to create a teaser and method diagram from this manuscript and results file. Use the paper's actual methods and numbers, roughly 35% concept and 65% evidence in the teaser, and a 7-inch-wide draft. Export editable SVG, PDF, PNG, source data, and a caption. Review both figures at print size and fix concrete defects.

Codex also supports `$paper-figure-creation`; Claude Code supports `/paper-figure-creation`. Attach the manuscript, method description or code, result tables, and target venue template when available. The skill has no model-name or API-key dependency.

## Render a starter

The Python renderer needs Python 3.10+, Matplotlib and NumPy. The evidence validator uses the Python standard library.

```bash
python -m pip install -r requirements.txt
python skills/paper-figure-creation/scripts/render_figure.py \
  skills/paper-figure-creation/assets/teaser-template.json \
  --output output/teaser --strict-layout
python skills/paper-figure-creation/scripts/render_figure.py \
  skills/paper-figure-creation/assets/method-template.json \
  --output output/method --strict-layout
```

Starter values are visibly labeled synthetic and are only for layout. Replace them with a sourced evidence ledger before using a figure in a paper. Read the [spec format](skills/paper-figure-creation/references/spec-format.md). Custom SVG, Matplotlib or TikZ layouts remain valid when a method needs a different visual structure.

Outputs include editable-text SVG, vector PDF with embedded fonts, 300-DPI PNG and a bounded geometry report. Method figures also export native `.drawio` cells. Native diagrams.net application rendering has not been verified; `.drawio` is an editable graph export, with JSON/source as the canonical geometry. See the [example gallery](examples/README.md).

## Evidence and evaluation

The [research record](research/README.md) separates a 500-paper proceedings corpus, automated PDF/caption retrieval, and 20 close visual reviews of official paper-related assets. It does **not** claim 500 hand-reviewed figures, a representative survey, or an objective ranking of the 500 best papers.

The gallery contains original redraws for MAE, Transformer and LoRA. Numerical results are transcribed from papers, not newly reproduced experiments. Initial failures and subsequent repairs are recorded in the [evaluation report](docs/evaluation.md). An independent agent used the skill for the LoRA pair; this is a limited forward test, not proof of superiority over Claude, GPT, or another figure workflow.

```bash
python -m unittest discover -s tests -v
python examples/build_specs.py
```

The validator checks declared data, both chart axes, comparability, uncertainty and improvement arithmetic. It cannot verify a source merely because a URL is present, detect every misleading prose claim, or judge whether an omitted baseline matters. Scientific review and actual pixel inspection remain required.

## Provenance and license

The implementation and redraws are original. The supplied [Anthropic skills](https://github.com/anthropics/skills) and [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) informed packaging and evaluation practices; [research notes](research/skill-repository-lessons.md) identify the inspected sources. Original paper figures and full paper PDFs are not redistributed.

Original code and documentation are MIT licensed. Citations, paper titles, experimental facts, and linked third-party materials retain their respective provenance; this license does not grant rights to those authors' original figures.
