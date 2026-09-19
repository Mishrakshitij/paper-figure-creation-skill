"""Failure-oriented checks for standalone quantitative publication exports."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
from render_graphs import render_graphs
from validate_evidence import validate_spec


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "figure"
        self.spec = json.loads((ROOT / "examples/graphs-lora/graphs.spec.json").read_text())

    def test_task_context_is_required_for_each_xy_pair(self):
        self.assertTrue(validate_spec(self.spec)["valid"])
        self.spec["evidence"]["results"][1]["comparison"] = {
            "dataset": "Unrelated task", "split": "test", "budget": "Unknown"}
        report = validate_spec(self.spec)
        self.assertTrue(any(e["code"] == "chart_xy_context" for e in report["errors"]))
        with self.assertRaisesRegex(ValueError, "Evidence validation failed"):
            render_graphs(self.spec, self.out, ("svg",))
        self.assertFalse(self.out.with_suffix(".svg").exists())

    def test_fixed_size_svg_text_and_png_resolution(self):
        report = render_graphs(self.spec, self.out, ("svg", "pdf", "png"))
        self.assertEqual(report["warnings"], [])
        self.assertEqual([len(p["plotted_result_ids"]) for p in report["panels"]], [8, 8])
        tree = ET.parse(self.out.with_suffix(".svg"))
        self.assertEqual(tree.getroot().attrib["width"], "518.4pt")
        self.assertEqual(tree.getroot().attrib["height"], "284.4pt")
        self.assertGreater(len(tree.findall('.//{http://www.w3.org/2000/svg}text')), 20)
        with Image.open(self.out.with_suffix(".png")) as im:
            self.assertEqual(im.size, (2160, 1185))
            self.assertAlmostEqual(im.info["dpi"][0], 300, delta=.1)
        self.assertTrue(self.out.with_suffix(".pdf").read_bytes().startswith(b"%PDF"))

    def test_bounds_must_include_points_and_reported_uncertainty(self):
        self.spec["charts"][0]["ylim"] = [64, 76]
        with self.assertRaisesRegex(ValueError, "Data point outside"):
            render_graphs(self.spec, self.out, ("svg",))
        self.spec["charts"][0]["ylim"] = [61.5, 76]
        result = self.spec["evidence"]["results"][0]
        result["uncertainty"] = {"type": "range", "lower": 70, "upper": 78,
                                 "source_id": result["source_id"], "source_location": "Test-only reported range"}
        with self.assertRaisesRegex(ValueError, "Uncertainty interval outside"):
            render_graphs(self.spec, self.out, ("svg",))

    def test_log_tradeoff_checks_x_uncertainty(self):
        result = self.spec["evidence"]["results"][1]
        result["uncertainty"] = {"type": "range", "lower": 0, "upper": result["value"] + 1,
                                 "source_id": result["source_id"], "source_location": "Test-only reported range"}
        with self.assertRaisesRegex(ValueError, "nonpositive log coordinate"):
            render_graphs(self.spec, self.out, ("svg",))

    def test_fabricated_value_never_reaches_export(self):
        self.spec["charts"][0]["series"][0]["values"][0] += 1
        with self.assertRaisesRegex(ValueError, "Evidence validation failed"):
            render_graphs(self.spec, self.out, ("svg",))
        self.assertFalse(self.out.with_suffix(".svg").exists())

    def test_method_style_does_not_change_between_panels(self):
        self.spec["charts"][1]["series"][0]["color"] = "red"
        with self.assertRaisesRegex(ValueError, "Conflicting color"):
            render_graphs(self.spec, self.out, ("svg",))

    def test_manuscript_scaling_uses_preserved_layout_audit(self):
        self.spec["figure"]["display_width_inches"] = 3.6
        original = copy.deepcopy(self.spec["evidence"])
        report = render_graphs(self.spec, self.out, ("svg",))
        self.assertTrue(report["data_occlusion_check_requested"])
        self.assertTrue(any(i["kind"] == "small_text" and i["effective_font_size_pt"] == 4
                            for i in report["layout_issues"]))
        self.assertEqual(self.spec["evidence"], original)

    def test_categorical_log_axes_cannot_hide_zero_or_drop_rows(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/graphs-template.json").read_text())
        spec["charts"][0].pop("xlim", None)
        spec["charts"][0]["type"] = "bar"
        spec["charts"][0]["xscale"] = "log"
        with self.assertRaisesRegex(ValueError, "linear value axis"):
            render_graphs(spec, self.out, ("svg",))
        self.assertFalse(self.out.with_suffix(".svg").exists())
        spec["charts"][0]["type"] = "dot"
        spec["charts"][0]["xscale"] = "linear"
        spec["charts"][0]["yscale"] = "log"
        with self.assertRaisesRegex(ValueError, "Categorical row positions"):
            render_graphs(spec, self.out, ("svg",))

    def test_template_is_labeled_synthetic_and_zero_baseline_is_required(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/graphs-template.json").read_text())
        self.assertTrue(validate_spec(spec)["valid"])
        spec["status"] = "final"
        self.assertFalse(validate_spec(spec)["valid"])
        spec["status"] = "draft"
        spec["charts"][0]["type"] = "bar"
        with self.assertRaisesRegex(ValueError, "Bar charts must include zero"):
            render_graphs(spec, self.out, ("svg",))


if __name__ == "__main__":
    unittest.main()
