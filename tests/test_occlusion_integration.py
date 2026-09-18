"""A JSON-controlled legend repair preserves evidence and clears real overlap."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib as mpl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
import render_figure as engine


class OcclusionIntegrationTests(unittest.TestCase):
    def test_reserved_legend_repairs_overlap_without_changing_evidence(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/teaser-template.json").read_text())
        evidence = copy.deepcopy(spec["evidence"])
        spec["figure"].update(check_data_occlusion=True, shared_legend=False)
        spec["charts"][0]["legend_loc"] = "center"
        spec["charts"][1]["legend"] = False
        apply_theme = engine.apply_theme

        def framed_legend(theme):
            apply_theme(theme)
            mpl.rcParams.update({"legend.frameon": True, "legend.framealpha": 1})

        with tempfile.TemporaryDirectory() as directory, mpl.rc_context(), patch.object(
                engine, "apply_theme", side_effect=framed_legend):
            out = Path(directory) / "figure"
            covered = engine.render(spec, out, formats=("svg",))
            self.assertTrue(any(x["kind"] == "legend_data_overlap" for x in covered["layout_issues"]))
            self.assertTrue(any("Legend overlaps plotted data" in x for x in covered["warnings"]))
            self.assertTrue(json.loads(out.with_suffix(".qa.json").read_text())["data_occlusion_check_requested"])

            spec["figure"]["check_data_occlusion"] = False
            unchecked = engine.render(spec, out, formats=("svg",))
            self.assertFalse(any(x["kind"] == "legend_data_overlap" for x in unchecked["layout_issues"]))

            spec["figure"].update(check_data_occlusion=True, shared_legend=True)
            repaired = engine.render(spec, out, formats=("svg",))
            self.assertEqual(repaired["layout_issues"], [])
            self.assertEqual(spec["evidence"], evidence)


if __name__ == "__main__":
    unittest.main()
