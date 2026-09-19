# Working in this repository

Read `skills/paper-visual-design/SKILL.md` first for paper-figure requests. Select only applicable workflows. Read `README.md` for repository navigation and build commands.

- Preserve the user's scientific and visual preferences. Plan a new complex figure before rendering; keep a concrete source/evidence contract and explore three distinct compositions.
- Treat standalone graphs as a first-class workflow. Generate illustrative assets only; construct exact scientific labels, topology, and quantitative marks with editable vector tools.
- Select benchmark/environment figures only when the paper describes a substantive setup. Do not infer a new benchmark contribution from dataset names in a results table.
- Edit shared tools and foundation guidance in `skills/paper-figure-creation/`. `skills/paper-visual-design/foundation/` is a generated copy, not a second hand-maintained source. Run `python scripts/sync_visual_design_bundle.py` after changing the foundation, then `--check`.
- Keep example source, data, geometry, asset provenance, caption, and review beside its exports. Do not silently hand-edit an export and then overwrite it from stale source. Preserve earlier examples unless a requested correction requires changing them.
- Use existing tests plus focused failure-oriented checks for changes to evidence, export, or composition behavior. Run `python -m unittest discover -s tests -v` before publication. Documentation-only edits do not need invented tests.
- Inspect actual rendered pixels at intended manuscript size and enlarged. Report unverified formats and manuscript integration honestly. A passing validator cannot establish scientific truth or visual quality.
- Keep research scope accurate. Record exact reference versions and licenses; do not copy third-party code or artwork without appropriate authorization and license compliance.
