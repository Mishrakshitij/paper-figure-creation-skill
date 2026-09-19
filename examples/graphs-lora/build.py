#!/usr/bin/env python3
"""Rebuild the two sourced LoRA scatter plots without a plotting GUI."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
from render_graphs import render_graphs

if __name__ == "__main__":
    report = render_graphs(json.loads((HERE / "graphs.spec.json").read_text()), HERE / "lora-tradeoff")
    print(json.dumps({"warnings": report["warnings"], "formats": report["formats"],
                      "physical_size_in": report["physical_size_in"]}, indent=2))
