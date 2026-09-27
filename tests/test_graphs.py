"""Failure-oriented checks for standalone quantitative publication exports."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
from render_graphs import COLORS, MARKERS, main as render_graphs_main, render_graphs, _style_map
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


def svg_text(path):
    root = ET.parse(path).getroot()
    return [" ".join("".join(t.itertext()).split()) for t in root.iter("{http://www.w3.org/2000/svg}text")]


def frontier(points, xdir, ydir):
    """Independent brute-force Pareto set for the renderer's step line."""
    sx, sy = (1 if xdir == "lower" else -1), (1 if ydir == "higher" else -1)
    keep = [p for p in points if not any(
        sx*q[0] <= sx*p[0] and sy*q[1] >= sy*p[1] and (sx*q[0] < sx*p[0] or sy*q[1] > sy*p[1]) for q in points)]
    return [p[2] for p in sorted(keep, key=lambda p: (sx*p[0], -sy*p[1]))]


class HouseStyleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "figure"
        here = ROOT / "examples/graphs-house-pareto"
        self.spec = json.loads((here / "graphs.spec.json").read_text())
        self.styles = json.loads((here / "paper-styles.json").read_text())

    def test_house_roles_mark_ours_and_arrows_follow_the_ledger(self):
        report = render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        self.assertEqual(report["warnings"], [])
        self.assertEqual(report["preset"], "house")
        self.assertGreaterEqual(report["minimum_text_pt"], 5.3)
        texts = svg_text(self.out.with_suffix(".svg"))
        self.assertIn("LoRA (ours)", texts)
        self.assertNotIn("Full FT (ours)", texts)
        self.assertEqual(texts.count("Accuracy (%) \u2191"), 2)
        self.assertEqual(texts.count("Trainable parameters (millions, log) \u2193"), 2)
        styles = _style_map(self.spec["charts"], "house", self.styles)
        self.assertEqual((styles["lora"]["marker"], styles["lora"]["color"]), ("*", "#D55E00"))
        self.assertEqual((styles["ft"]["marker"], styles["ft"]["color"]), ("s", "#111111"))
        baselines = [styles[k] for k in ("bitfit", "preembed", "prelayer", "adapter")]
        self.assertEqual({b["marker"] for b in baselines}, {"o"})
        self.assertEqual(len({b["color"] for b in baselines}), 4)
        self.spec["charts"][0]["series"].append(
            {"id": "lora_noinit", "role": "ablation", "values": [], "result_ids": [], "x_values": [], "x_result_ids": []})
        ablation = _style_map(self.spec["charts"], "house", self.styles)["lora_noinit"]
        self.assertEqual((ablation["marker"], ablation["markerfacecolor"]), ("D", "white"))

    def test_arrow_or_direction_that_contradicts_the_ledger_is_refused(self):
        chart = self.spec["charts"][0]
        chart["ylabel"] = "Accuracy (%) \u2193"
        with self.assertRaisesRegex(ValueError, "contradicts the evidence metric direction"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        self.assertFalse(self.out.with_suffix(".svg").exists())
        chart["ylabel"] = "Accuracy (%)"
        chart["ydirection"] = "lower"
        with self.assertRaisesRegex(ValueError, "contradicts the evidence metric direction"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        chart["ydirection"] = "none"
        chart.pop("pareto")
        render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        texts = svg_text(self.out.with_suffix(".svg"))
        self.assertIn("Accuracy (%)", texts)
        self.assertEqual(texts.count("Accuracy (%) \u2191"), 1)

    def test_pareto_frontier_is_the_non_dominated_set(self):
        report = render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        for chart, panel in zip(self.spec["charts"], report["panels"]):
            points = [(x, y, rid) for s in chart["series"]
                      for x, y, rid in zip(s["x_values"], s["values"], s["result_ids"])]
            self.assertEqual(panel["pareto_result_ids"], frontier(points, "lower", "higher"))
        self.assertEqual(report["panels"][0]["pareto_result_ids"], ["preembed_wiki", "lora4_wiki", "lora37_wiki"])
        chart = self.spec["charts"][0]
        chart["pareto"]["series"] = ["ft", "bitfit", "preembed", "prelayer", "adapter"]
        report = render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        points = [(x, y, rid) for s in chart["series"] if s["id"] != "lora"
                  for x, y, rid in zip(s["x_values"], s["values"], s["result_ids"])]
        self.assertEqual(report["panels"][0]["pareto_result_ids"], frontier(points, "lower", "higher"))
        self.assertNotIn("lora4_wiki", report["panels"][0]["pareto_result_ids"])
        chart["pareto"] = {"x": "higher"}
        with self.assertRaisesRegex(ValueError, "Pareto directions contradict"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        chart["pareto"] = {"series": ["no_such_method"]}
        with self.assertRaisesRegex(ValueError, "pareto.series"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        template = json.loads((ROOT / "skills/paper-figure-creation/assets/graphs-template.json").read_text())
        template["charts"][0]["pareto"] = True
        with self.assertRaisesRegex(ValueError, "scatter chart"):
            render_graphs(template, self.out, ("svg",))

    def test_style_registry_fixes_encodings_across_figures(self):
        styles = dict(self.styles, bitfit={"role": "baseline", "color": "#AA3377"})
        render_graphs(self.spec, self.out, ("svg",), styles=styles)
        self.assertIn("#aa3377", self.out.with_suffix(".svg").read_text().lower())
        self.spec["charts"][1]["series"][1]["color"] = "#000000"
        with self.assertRaisesRegex(ValueError, "style registry"):
            render_graphs(self.spec, self.out, ("svg",), styles=styles)
        self.spec["charts"][1]["series"][1].pop("color")
        self.spec["styles"] = {"bitfit": {"role": "baseline", "color": "#123456"}}
        with self.assertRaisesRegex(ValueError, "contradicts the shared style registry"):
            render_graphs(self.spec, self.out, ("svg",), styles=styles)
        self.spec.pop("styles")
        self.spec["charts"][1]["series"][5]["role"] = "baseline"
        with self.assertRaisesRegex(ValueError, "Conflicting role for stable series lora \\(style registry\\)"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        with self.assertRaisesRegex(ValueError, "Conflicting role for stable series lora$"):
            render_graphs(self.spec, self.out, ("svg",))
        spec_path = Path(self.tmp.name) / "spec.json"
        styles_path = Path(self.tmp.name) / "styles.json"
        self.spec["charts"][1]["series"][5].pop("role")
        spec_path.write_text(json.dumps(self.spec))
        styles_path.write_text(json.dumps(self.styles))
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            code = render_graphs_main([str(spec_path), "--output", str(self.out), "--formats", "svg",
                                       "--styles", str(styles_path)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(printed.getvalue())["preset"], "house")

    def test_type_floor_follows_the_preset(self):
        self.spec["figure"]["font_pt"] = 5
        with self.assertRaisesRegex(ValueError, "font_pt >= 5.3"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        self.spec["figure"]["font_pt"] = 5.5
        report = render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        self.assertFalse(any(i["kind"] == "small_text" for i in report["layout_issues"]))
        self.spec["figure"]["preset"] = "classic"
        with self.assertRaisesRegex(ValueError, "font_pt >= 6"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        self.spec["figure"]["preset"] = "poster"
        with self.assertRaisesRegex(ValueError, "preset"):
            render_graphs(self.spec, self.out, ("svg",), styles=self.styles)

    def test_point_roles_encode_rows_of_a_dot_plot(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/graphs-template.json").read_text())
        spec["figure"]["preset"] = "house"
        series = spec["charts"][0]["series"][0]
        series.pop("point_colors"); series.pop("point_markers")
        series["point_roles"] = ["baseline", "reference", "proposed"]
        render_graphs(spec, self.out, ("svg",))
        texts = svg_text(self.out.with_suffix(".svg"))
        self.assertIn("Proposed (ours)", texts)
        self.assertIn("Baseline A", texts)
        series["point_roles"] = ["baseline", "proposed"]
        with self.assertRaisesRegex(ValueError, "point_roles must align"):
            render_graphs(spec, self.out, ("svg",))

    def test_interval_at_the_marker_edge_is_hidden_and_reported(self):
        results = {r["id"]: r for r in self.spec["evidence"]["results"]}
        for rid, half in (("lora4_wiki", 0.05), ("lora37_wiki", 1.5)):
            results[rid]["uncertainty"] = {"type": "sd", "value": half, "source_id": results[rid]["source_id"],
                                           "source_location": "Test-only reported SD"}
        report = render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        hidden = report["panels"][0]["intervals_inside_marker"]
        self.assertEqual([(h["result_id"], h["axis"]) for h in hidden], [("lora4_wiki", "y")])
        self.assertTrue(any("lora4_wiki" in w and "caption" in w for w in report["warnings"]))
        self.assertEqual(report["panels"][1]["intervals_inside_marker"], [])

    def test_empty_label_never_becomes_ours(self):
        for chart in self.spec["charts"]:
            chart["series"][5]["label"] = ""
        render_graphs(self.spec, self.out, ("svg",), styles=self.styles)
        texts = svg_text(self.out.with_suffix(".svg"))
        self.assertFalse(any("(ours)" in t for t in texts))
        self.assertIn("Pareto frontier", texts)

    def test_classic_defaults_are_unchanged(self):
        charts = [{"series": [{"id": "a"}, {"id": "b", "role": "proposed"}, {"id": "c", "role": "baseline"}]},
                  {"series": [{"id": "b"}]}]
        styles = _style_map(charts)
        self.assertEqual((styles["a"]["color"], styles["a"]["marker"], styles["a"]["ms"]), (COLORS[0], MARKERS[0], 4.6))
        self.assertEqual((styles["b"]["color"], styles["b"]["marker"], styles["b"]["ms"], styles["b"]["lw"]),
                         ("#007D8A", MARKERS[1], 5.5, 1.5))
        self.assertEqual((styles["c"]["color"], styles["c"]["marker"]), (COLORS[2], MARKERS[2]))


if __name__ == "__main__":
    unittest.main()
