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
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.transforms import IdentityTransform
from layout_quality import audit_figure, issue_message, wrap_text_artist
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


class LegendDataOverlapTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def scene(self, **legend_options):
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.set_axis_off()
        options = dict(loc="center", frameon=True, framealpha=1)
        options.update(legend_options)
        legend = ax.legend(handles=[Line2D([], [], label="Measured response")], **options)
        fig.canvas.draw()
        bounds = legend.get_window_extent(fig.canvas.get_renderer())
        center = ax.transData.inverted().transform(
            ((bounds.x0 + bounds.x1) / 2, (bounds.y0 + bounds.y1) / 2))
        return fig, ax, legend, bounds, center

    def overlaps(self, fig):
        return [issue for issue in audit_figure(fig, check_data_occlusion=True)
                if issue["kind"] == "legend_data_overlap"]

    def test_opt_in_finds_crossing_line_without_changing_evidence(self):
        fig, ax, legend, _, (x, y) = self.scene()
        line, = ax.plot([.05, .95], [y, y], label="Observed curve", gid="observed")
        legend.set_gid("series-key")
        before = (line.get_xydata().copy(), line.get_linewidth(),
                  fig.get_size_inches().copy(), legend.get_bbox_to_anchor().bounds)
        self.assertFalse(any(issue["kind"] == "legend_data_overlap" for issue in audit_figure(fig)))
        issues = self.overlaps(fig)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["data_artist_id"], "observed")
        self.assertEqual(issues[0]["artist_id"], "series-key")
        self.assertGreater(issues[0]["overlap_pixels"], 0)
        self.assertIn("Observed curve", issue_message(issues[0]))
        np.testing.assert_array_equal(line.get_xydata(), before[0])
        self.assertEqual(line.get_linewidth(), before[1])
        np.testing.assert_array_equal(fig.get_size_inches(), before[2])
        self.assertEqual(legend.get_bbox_to_anchor().bounds, before[3])

    def test_line_bbox_crossing_legend_is_not_a_collision(self):
        fig, ax, _, bounds, _ = self.scene()
        # The enclosing box contains the legend, but every segment goes around
        # its painted region. A bounding-box-only detector falsely flags this.
        points = [(bounds.x0 - 10, bounds.y1 + 10),
                  (bounds.x1 + 10, bounds.y1 + 10),
                  (bounds.x1 + 10, bounds.y0 - 10)]
        xy = ax.transData.inverted().transform(points)
        ax.plot(xy[:, 0], xy[:, 1], linewidth=1)
        self.assertEqual(self.overlaps(fig), [])

    def test_missing_line_segment_does_not_fill_gap(self):
        fig, ax, _, bounds, (_, y) = self.scene()
        left, right = ax.transData.inverted().transform(
            [(bounds.x0 - 8, bounds.y0), (bounds.x1 + 8, bounds.y0)])[:, 0]
        ax.plot([.02, left, np.nan, right, .98], [y, y, np.nan, y, y])
        self.assertEqual(self.overlaps(fig), [])

    def test_hidden_or_transparent_artists_and_hidden_legend_are_ignored(self):
        for hidden in ("artist", "axes", "legend", "transparent", "animated"):
            with self.subTest(hidden=hidden):
                fig, ax, legend, _, (x, y) = self.scene()
                line, = ax.plot([x], [y], marker="o", markersize=12)
                if hidden == "transparent":
                    line.set_alpha(0)
                elif hidden == "animated":
                    line.set_animated(True)
                else:
                    {"artist": line, "axes": ax, "legend": legend}[hidden].set_visible(False)
                self.assertEqual(self.overlaps(fig), [])

    def test_scatter_marker_geometry_reaches_legend_from_outside(self):
        fig, ax, _, bounds, _ = self.scene()
        # The center is outside the frame. The visible marker area extends into it.
        point = ax.transData.inverted().transform((bounds.x0 - 4, (bounds.y0 + bounds.y1) / 2))
        scatter = ax.scatter([point[0]], [point[1]], s=225, label="Observed point")
        original = scatter.get_offsets().copy()
        self.assertEqual([r["data_artist_type"] for r in self.overlaps(fig)], ["PathCollection"])
        np.testing.assert_array_equal(scatter.get_offsets(), original)

    def test_out_of_view_scatter_respects_clip_on(self):
        fig, ax, legend, _, _ = self.scene(loc="center left", bbox_to_anchor=(1.03, .5))
        ax.set_position([.1, .1, .45, .8])  # Room on-page for the external legend.
        fig.canvas.draw()
        bounds = legend.get_window_extent(fig.canvas.get_renderer())
        x, y = ax.transData.inverted().transform(
            ((bounds.x0 + bounds.x1) / 2, (bounds.y0 + bounds.y1) / 2))
        scatter = ax.scatter([x], [y], s=64)
        self.assertGreater(x, 1)
        self.assertEqual(self.overlaps(fig), [])
        scatter.set_clip_on(False)
        self.assertEqual(len(self.overlaps(fig)), 1)

    def test_custom_artist_clip_excludes_covered_data(self):
        fig, ax, _, bounds, _ = self.scene()
        y = ax.transData.inverted().transform((bounds.x1, bounds.y1 - 1))[1]
        line, = ax.plot([.05, .95], [y, y], linewidth=1)
        # This circular clip's bbox crosses the legend corner but its actual
        # circular area does not. The clip path, not just its bounds, matters.
        line.set_clip_path(Circle((bounds.x1 + 12, bounds.y1 + 12), 15,
                                  transform=IdentityTransform()))
        self.assertEqual(self.overlaps(fig), [])
        line.set_clip_on(False)
        self.assertEqual(len(self.overlaps(fig)), 1)

    def test_errorbar_stem_is_detected_when_point_is_clear(self):
        fig, ax, _, _, (x, y) = self.scene()
        ax.errorbar([x], [y - .2], yerr=[.3], fmt="o", capsize=4, label="Estimate")
        types = [r["data_artist_type"] for r in self.overlaps(fig)]
        self.assertEqual(types, ["LineCollection"])

    def test_uncertainty_band_is_detected_without_centerline_overlap(self):
        fig, ax, _, _, (x, y) = self.scene()
        band = ax.fill_between([x - .3, x + .3], [y - .1] * 2,
                               [y + .1] * 2, alpha=.25, label="Uncertainty")
        issues = self.overlaps(fig)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["data_label"], "Uncertainty")
        band.set_visible(False)
        self.assertEqual(self.overlaps(fig), [])

    def test_frameless_legend_ink_still_covers_data(self):
        fig, ax, legend, _, _ = self.scene(frameon=False)
        text_box = legend.get_texts()[0].get_window_extent(fig.canvas.get_renderer())
        y = ax.transData.inverted().transform((text_box.x0, (text_box.y0 + text_box.y1) / 2))[1]
        ax.plot([.05, .95], [y, y], linewidth=3)
        self.assertEqual(len(self.overlaps(fig)), 1)

    def test_transparent_legend_background_does_not_cover_whitespace(self):
        fig, ax, legend, bounds, _ = self.scene(frameon=False)
        # The bottom padding is inside the legend bbox but below all its ink.
        point = ax.transData.inverted().transform(((bounds.x0 + bounds.x1) / 2, bounds.y0 + 1))
        ax.scatter([point[0]], [point[1]], s=1, linewidths=0)
        self.assertEqual(self.overlaps(fig), [])
        legend.set_frame_on(True)
        self.assertEqual(len(self.overlaps(fig)), 1)

    def test_line_drawn_above_axes_legend_is_not_occluded(self):
        fig, ax, legend, _, (_, y) = self.scene()
        line, = ax.plot([.05, .95], [y, y], zorder=legend.get_zorder() + 1)
        self.assertEqual(self.overlaps(fig), [])
        line.set_zorder(legend.get_zorder())  # Legends follow data at tied order.
        self.assertEqual(len(self.overlaps(fig)), 1)

    def test_figure_legend_respects_axes_order_not_line_order(self):
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.set_axis_off()
        legend = fig.legend(handles=[Line2D([], [], label="Measured response")],
                            loc="center", frameon=True, framealpha=1)
        fig.canvas.draw()
        bounds = legend.get_window_extent(fig.canvas.get_renderer())
        (_, y) = ax.transData.inverted().transform(
            ((bounds.x0 + bounds.x1) / 2, (bounds.y0 + bounds.y1) / 2))
        ax.plot([.05, .95], [y, y], zorder=100)
        self.assertEqual(len(self.overlaps(fig)), 1)
        ax.set_zorder(legend.get_zorder() + 1)
        self.assertEqual(self.overlaps(fig), [])


if __name__ == "__main__":
    unittest.main()
