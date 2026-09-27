#!/usr/bin/env python3
"""Rebuild the house-style LoRA Pareto teaser from its spec and the paper's style registry."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
from render_graphs import render_graphs

if __name__ == "__main__":
    spec = json.loads((HERE / "graphs.spec.json").read_text())
    # One registry per paper keeps each method's role, colour and marker identical in every figure.
    styles = json.loads((HERE / "paper-styles.json").read_text())
    report = render_graphs(spec, HERE / "house-pareto", styles=styles)
    print(json.dumps({"warnings": report["warnings"], "physical_size_in": report["physical_size_in"],
                      "minimum_text_pt": report["minimum_text_pt"],
                      "pareto": {p["title"]: p["pareto_result_ids"] for p in report["panels"]}}, indent=2))
