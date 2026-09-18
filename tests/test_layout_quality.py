"""Exercise actual rendered overflow and preservation of text/evidence."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/paper-figure-creation/scripts"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from layout_quality import audit_figure, wrap_text_artist
from render_figure import check_chart_coordinates, render


class LayoutQualityTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_annotation_collision_is_reported(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.axis("off")
        ax.text(.3, .5, "Private evaluator")
        ax.text(.31, .5, "Visible worker")
        issues = audit_figure(fig)
        self.assertEqual([r["kind"] for r in issues], ["text_overlap"])

    def test_clipped_label_is_not_exempted(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.axis("off")
        ax.text(.97, .5, "Important output", clip_on=True)
        kinds = {r["kind"] for r in audit_figure(fig)}
        self.assertIn("clipped_text", kinds)

    def test_hidden_axes_text_does_not_create_false_collisions(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.text(.3, .5, "hidden")
        ax.text(.3, .5, "hidden")
        ax.set_visible(False)
        self.assertEqual(audit_figure(fig), [])

    def test_legend_and_font_size_are_measured(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.plot([0, 1], [0, 1], label="A very long experimental comparison label"*3)
        ax.legend(loc="upper left")
        ax.text(.5, .5, "Tiny", fontsize=5)
        issues = audit_figure(fig, min_font_pt=8)
        self.assertIn("legend_overflow", {r["kind"] for r in issues})
        self.assertTrue(any(r["kind"] == "small_text" and r["text"] == "Tiny" for r in issues))

    def test_wrapping_preserves_all_words_and_font(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        value = "Calibrated ownership recovery with independent evidence"
        artist = ax.text(.1, .5, value, fontsize=10)
        fig.canvas.draw()
        self.assertTrue(wrap_text_artist(artist, 115, fig.canvas.get_renderer()))
        self.assertEqual(artist.get_text().split(), value.split())
        self.assertGreater(len(artist.get_text().splitlines()), 1)
        self.assertEqual(artist.get_fontsize(), 10)

    def test_manuscript_scaling_checks_effective_type_without_changing_geometry(self):
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.axis("off")
        text = ax.text(.2, .5, "Measured outcome", fontsize=9)
        before = (fig.get_size_inches().copy(), text.get_position(), text.get_fontsize())
        self.assertFalse(any(r["kind"] == "small_text" for r in audit_figure(fig, min_font_pt=8)))
        issues = audit_figure(fig, min_font_pt=8, display_width_inches=3.5)
        issue = next(r for r in issues if r["kind"] == "small_text")
        self.assertEqual(issue["effective_font_size_pt"], 4.5)
        self.assertTrue((fig.get_size_inches() == before[0]).all())
        self.assertEqual((text.get_position(), text.get_fontsize()), before[1:])

    def test_invalid_display_width_is_rejected(self):
        fig, _ = plt.subplots()
        for width in (0, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                audit_figure(fig, display_width_inches=width)

    def test_renderer_propagates_manuscript_size_to_layout_audit(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/method-template.json").read_text())
        spec["figure"].update(min_font_pt=8, display_width_inches=2)
        with tempfile.TemporaryDirectory() as d:
            report = render(spec, Path(d) / "figure", formats=("svg",))
        issues = [issue for issue in report["layout_issues"] if issue["kind"] == "small_text"]
        self.assertTrue(issues)
        self.assertTrue(all(issue["effective_font_size_pt"] < 8 for issue in issues))

    def test_unbreakable_word_is_retained_and_equation_is_not_split(self):
        fig, ax = plt.subplots()
        artist = ax.text(.1, .5, "Unbreakable_Identifier_0123456789")
        fig.canvas.draw()
        original = artist.get_text()
        self.assertFalse(wrap_text_artist(artist, 10, fig.canvas.get_renderer()))
        self.assertEqual(artist.get_text(), original)
        artist.set_text("Score $a + b$ result")
        wrap_text_artist(artist, 50, fig.canvas.get_renderer())
        self.assertIn("$a + b$", artist.get_text())

    def test_uncertainty_cannot_be_clipped_when_point_is_visible(self):
        chart = {"type": "dot", "xlim": [0, 1], "series": [{"values": [.9], "errors": [.2]}]}
        with self.assertRaisesRegex(ValueError, "Uncertainty outside"):
            check_chart_coordinates(chart)
        chart["xlim"] = [0, 1.2]
        check_chart_coordinates(chart)

    def test_wrapping_node_does_not_silently_shrink_label(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/method-template.json").read_text())
        spec["nodes"] = [{"id": "test", "x": .1, "y": .2, "w": .35, "h": .6,
                          "label": "Independent calibration with held out contributors",
                          "wrap_label": True}]
        spec["groups"] = []
        spec["edges"] = []
        spec["annotations"] = []
        with tempfile.TemporaryDirectory() as d:
            report = render(copy.deepcopy(spec), Path(d)/"figure", formats=("svg",))
            self.assertFalse(any("overflow node test" in w for w in report["warnings"]))
            self.assertIn("Independent calibration", (Path(d)/"figure.svg").read_text())

    def test_annotation_cannot_hide_inside_unrelated_node(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/method-template.json").read_text())
        node = spec["nodes"][0]
        spec.setdefault("annotations", []).append({"x": node["x"]+.01,
                                                   "y": node["y"]+node["h"]*.9,
                                                   "text": "Misplaced callout"})
        with tempfile.TemporaryDirectory() as d:
            report = render(spec, Path(d)/"figure", formats=("svg",))
        self.assertTrue(any("Diagram label intersects node" in w and "Misplaced callout" in w
                            for w in report["warnings"]))

    def test_synthetic_disclosure_respects_legibility_floor(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/method-template.json").read_text())
        spec["figure"]["min_font_pt"] = 8
        with tempfile.TemporaryDirectory() as d:
            report = render(spec, Path(d)/"figure", formats=("svg",))
            self.assertIn("SYNTHETIC DATA", (Path(d)/"figure.svg").read_text())
        self.assertFalse(any(r["kind"] == "small_text" and "SYNTHETIC" in r.get("text", "")
                             for r in report["layout_issues"]))

    def test_explicit_tiny_disclosure_is_still_rejected(self):
        spec = json.loads((ROOT / "skills/paper-figure-creation/assets/method-template.json").read_text())
        spec["figure"].update(min_font_pt=8, watermark_font_pt=5)
        with tempfile.TemporaryDirectory() as d:
            report = render(spec, Path(d)/"figure", formats=("svg",))
        self.assertTrue(any(r["kind"] == "small_text" and "SYNTHETIC" in r.get("text", "")
                            for r in report["layout_issues"]))


if __name__ == "__main__":
    unittest.main()
