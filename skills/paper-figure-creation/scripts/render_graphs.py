#!/usr/bin/env python3
"""Render standalone, evidence-linked experimental graphs at physical print size.

The specification shares provenance/evidence/charts with render_figure.py.
CLI: render_graphs.py spec.json --output output/figure [--formats svg pdf png]
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import numpy as np

from figure_style import apply_theme, load_theme
from render_figure import check_chart_coordinates
from layout_quality import audit_figure, issue_message
from validate_evidence import validate_spec, finite

COLORS = ["#697783", "#B76D31", "#7564A2", "#5388A6", "#868445", "#A8657D"]
MARKERS = ["o", "s", "^", "v", "P", "X", "D", "d"]


def _uncertainty(result):
    """Read actual sourced intervals; never infer them from a method name."""
    u = result.get("uncertainty")
    if not u or result.get("missing"):
        return None
    if "value" in u:
        return (result["value"] - u["value"], result["value"] + u["value"])
    return (u["lower"], u["upper"])


def _check_uncertainty(chart, results, limits=None):
    for series in chart["series"]:
        links = [("x" if chart["type"] in ("dot", "bar") else "y", series["result_ids"])]
        if chart["type"] in ("line", "scatter") and "x_result_ids" in series:
            links.append(("x", series["x_result_ids"]))
        for axis, ids in links:
            bounds = (limits or {}).get(axis, chart.get(axis + "lim"))
            for rid in ids:
                result = results[rid]
                interval = _uncertainty(result)
                if interval is None:
                    continue
                lo, hi = interval
                if not lo <= result["value"] <= hi:
                    raise ValueError("An interval outside its point estimate needs a custom interval plot")
                if chart.get(axis + "scale") == "log" and lo <= 0:
                    raise ValueError("Uncertainty interval crosses a nonpositive log coordinate")
                if bounds is not None and (lo < min(bounds) or hi > max(bounds)):
                    raise ValueError("Uncertainty interval outside declared axis limits")


def _style_map(charts):
    styles = {}
    for chart in charts:
        for series in chart["series"]:
            key = series.get("style_id", series.get("id", series.get("label")))
            if not isinstance(key, str) or not key:
                raise ValueError("Each graph series needs id, style_id, or label")
            proposed = series.get("role") == "proposed"
            new = {"color": series.get("color", "#007D8A" if proposed else COLORS[len(styles) % len(COLORS)]),
                   "marker": series.get("marker", MARKERS[len(styles) % len(MARKERS)]),
                   "markerfacecolor": series.get("markerfacecolor"),
                   "linestyle": series.get("linestyle", "-")}
            if key in styles:
                for field in ("color", "marker", "markerfacecolor", "linestyle"):
                    if field in series and styles[key][field] != series[field]:
                        raise ValueError(f"Conflicting {field} for stable series {key}")
            else:
                styles[key] = new
    return styles


def _draw_panel(ax, chart, results, styles, theme, index):
    kind = chart.get("type")
    if kind not in {"dot", "bar", "line", "scatter"}:
        raise ValueError("Supported graph types: dot, bar, line, scatter; use a custom audited renderer for other types")
    if kind in {"dot", "bar"} and chart.get("yscale", "linear") != "linear":
        raise ValueError("Categorical row positions require a linear y axis")
    if kind == "bar" and chart.get("xscale", "linear") != "linear":
        raise ValueError("Bar charts require a linear value axis with a meaningful zero; use dots for log values")
    series_list = chart["series"]
    if not series_list or not any(s["values"] for s in series_list):
        raise ValueError("Every graph needs observations")
    check_chart_coordinates(chart)
    _check_uncertainty(chart, results)
    categorical = kind in ("dot", "bar")
    cats = chart.get("categories", [])
    if categorical and (not cats or any(len(s["values"]) != len(cats) for s in series_list)):
        raise ValueError("Categorical charts need categories aligned to every series")
    group_width = .68 / len(series_list)
    for i, series in enumerate(series_list):
        vals = series["values"]
        key = series.get("style_id", series.get("id", series.get("label")))
        style = styles[key]
        label = series.get("label", key)
        color, marker = style["color"], style["marker"]
        face = style["markerfacecolor"] or color
        xs = series.get("x_values", chart.get("x_values"))
        if kind == "line" and any(a >= b for a, b in zip(xs, xs[1:])):
            raise ValueError("Line x coordinates must strictly increase; do not connect unordered conditions")
        if categorical:
            xs = np.arange(len(vals)) + (i - (len(series_list) - 1) / 2) * group_width
        if kind == "line":
            # Nulls intentionally break lines. No interpolation or imputation.
            ax.plot(xs, [np.nan if v is None else v for v in vals], color=color,
                    lw=1.5 if series.get("role") == "proposed" else 1.0,
                    linestyle=style["linestyle"], zorder=2)
        first = True
        offsets = series.get("point_label_offsets", [[4, 5] for _ in vals])
        labels = series.get("point_labels", ["" for _ in vals])
        aligns = series.get("point_label_align", ["auto" for _ in vals])
        point_colors = series.get("point_colors", [color for _ in vals])
        point_markers = series.get("point_markers", [marker for _ in vals])
        if any(len(a) != len(vals) for a in (offsets, labels, aligns, point_colors, point_markers)):
            raise ValueError("Point label arrays must align with values")
        for j, (v, rid) in enumerate(zip(vals, series["result_ids"])):
            if v is None:
                continue
            point_color = point_colors[j]
            point_marker = point_markers[j]
            point_face = point_color if "point_colors" in series else face
            interval = _uncertainty(results[rid])
            error = np.array([[v-interval[0]], [interval[1]-v]]) if interval else None
            xinterval = _uncertainty(results[series["x_result_ids"][j]]) if not categorical and "x_result_ids" in series else None
            xerror = np.array([[xs[j]-xinterval[0]], [xinterval[1]-xs[j]]]) if xinterval else None
            kwargs = dict(color=point_color, marker=point_marker, mfc=point_face, mec=point_color, mew=.8,
                          ms=5.5 if series.get("role") == "proposed" else 4.6,
                          elinewidth=.9, capsize=2.0, label=label if first else None, zorder=3)
            if kind == "bar":
                ax.barh([xs[j]], [v], height=group_width*.82, color=point_color,
                        xerr=error, error_kw={"capsize": 2, "elinewidth": .9},
                        label=label if first else None, zorder=3)
            else:
                ax.errorbar([v] if categorical else [xs[j]], [xs[j]] if categorical else [v],
                            xerr=error if categorical else xerror, yerr=None if categorical else error,
                            linestyle="none", **kwargs)
            if labels[j] or chart.get("value_labels", False):
                text = labels[j] or format(v, chart.get("value_format", ".1f"))
                offset = offsets[j]
                align = aligns[j] if aligns[j] != "auto" else ("left" if offset[0] >= 0 else "right")
                ax.annotate(text, (v, xs[j]) if categorical else (xs[j], v),
                            xytext=offset, textcoords="offset points", fontsize=theme["small_size"],
                            color=point_color, ha=align, va="bottom" if offset[1] >= 0 else "top",
                            annotation_clip=False,
                            arrowprops={"arrowstyle": "-", "color": point_color, "lw": .55} if series.get("label_leaders") else None)
            first = False
    for axis in ("x", "y"):
        scale = chart.get(axis + "scale", "linear")
        if scale not in ("linear", "log"):
            raise ValueError("Only explicit linear and log scales are supported")
        getattr(ax, "set_" + axis + "scale")(scale)
    if categorical:
        ax.set_yticks(np.arange(len(cats)), cats)
        ax.set_ylim(len(cats) - .5, -.5)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0, pad=5)
        if kind == "bar":
            bounds = chart.get("xlim")
            if bounds is not None and (min(bounds) > 0 or max(bounds) < 0):
                raise ValueError("Bar charts must include zero; use a dot plot for a restricted range")
            ax.axvline(0, color=theme["muted"], lw=.7)
    else:
        ax.spines["left"].set_color(theme["muted"])
    ax.grid(axis="x" if categorical else "y", color=theme["grid"], lw=.55)
    ax.set_axisbelow(True)
    ax.margins(x=.09, y=.13)
    for axis in ("x", "y"):
        bounds = chart.get(axis + "lim")
        if bounds is not None:
            getattr(ax, "set_" + axis + "lim")(*bounds)
        active = getattr(ax, "get_" + axis + "lim")()
        if axis + "ticks" in chart:
            ticks = chart[axis + "ticks"]
            labels = chart.get(axis + "ticklabels")
            if labels is not None and len(labels) != len(ticks):
                raise ValueError("Tick labels must align with tick coordinates")
            getattr(ax, "set_" + axis + "ticks")(ticks, labels)
            getattr(ax, "set_" + axis + "lim")(*active)
    check_chart_coordinates(chart, ax.get_xlim(), ax.get_ylim())
    _check_uncertainty(chart, results, {"x": ax.get_xlim(), "y": ax.get_ylim()})
    ax.set_xlabel(chart.get("xlabel", ""), labelpad=6)
    ax.set_ylabel(chart.get("ylabel", ""), labelpad=6)
    ax.tick_params(length=3, width=.6)
    if categorical:
        ax.tick_params(axis="y", length=0)
    ax.minorticks_off()
    panel_label = chart.get("panel_label", chr(97 + index))
    ax.set_title((panel_label + "  " if panel_label else "") + chart.get("title", ""),
                 loc="left", pad=9, fontsize=theme["panel_title_size"])
    if chart.get("legend", False):
        ax.legend(loc=chart.get("legend_loc", "best"), ncol=chart.get("legend_columns", 1))


def render_graphs(spec, out, formats=("svg", "pdf", "png")):
    """Validate first, render at declared size, export every format from one figure."""
    evidence = validate_spec(spec)
    if not evidence["valid"]:
        raise ValueError("Evidence validation failed: " + json.dumps(evidence["errors"]))
    if spec.get("kind") != "graphs":
        raise ValueError("Standalone renderer expects kind: graphs")
    charts = spec.get("charts", [])
    if not charts:
        raise ValueError("At least one chart is required")
    formats = tuple(formats)
    if not formats or any(fmt not in ("svg", "pdf", "png") for fmt in formats):
        raise ValueError("Export formats must be svg, pdf, or png")
    settings = spec.get("figure", {})
    width, height = settings.get("width_in", 7.2), settings.get("height_in", 3.6)
    font = settings.get("font_pt", 8)
    dpi = settings.get("dpi", 300)
    if any(not finite(v) or v <= 0 for v in (width, height, font, dpi)) or font < 6:
        raise ValueError("Positive physical dimensions/dpi and font_pt >= 6 required")
    theme = load_theme(overrides={**spec.get("theme", {}), "font_size": font,
                                 "small_size": font, "panel_title_size": font + 1,
                                 "title_size": font + 2.5, "dpi": dpi})
    apply_theme(theme)
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    try:
        layout = spec.get("layout", {})
        cols = layout.get("cols", min(2, len(charts)))
        if not isinstance(cols, int) or isinstance(cols, bool) or cols <= 0:
            raise ValueError("layout cols must be a positive integer")
        rows = layout.get("rows", math.ceil(len(charts) / cols))
        if not isinstance(rows, int) or isinstance(rows, bool) or rows <= 0 or rows*cols < len(charts):
            raise ValueError("layout rows/cols must fit every chart")
        grid = fig.add_gridspec(rows, cols, left=layout.get("left", .09), right=layout.get("right", .98),
                                bottom=layout.get("bottom", .25), top=layout.get("top", .82),
                                wspace=layout.get("wspace", .32), hspace=layout.get("hspace", .45))
        results = {r["id"]: r for r in spec["evidence"]["results"]}
        styles = _style_map(charts)
        axes = []
        for i, chart in enumerate(charts):
            rect = chart.get("rect")
            if rect is not None and (len(rect) != 4 or any(not finite(v) for v in rect) or
                                     min(rect[:2]) < 0 or min(rect[2:]) <= 0 or rect[0]+rect[2] > 1 or rect[1]+rect[3] > 1):
                raise ValueError("rect must be a positive, on-page [left,bottom,width,height] fraction")
            ax = fig.add_axes(rect) if rect is not None else fig.add_subplot(grid[i//cols, i%cols])
            axes.append(ax)
            _draw_panel(ax, chart, results, styles, theme, i)
        if settings.get("title"):
            fig.text(layout.get("left", .09), .975, settings["title"], va="top",
                     fontsize=theme["title_size"], weight="bold")
        if settings.get("subtitle"):
            fig.text(layout.get("left", .09), .914, settings["subtitle"], va="top", fontsize=font, color=theme["muted"])
        if layout.get("shared_legend", False):
            handles, labels = [], []
            for ax in axes:
                hs, ls = ax.get_legend_handles_labels()
                for h, label in zip(hs, ls):
                    if label not in labels:
                        handles.append(h); labels.append(label)
            fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(.5, layout.get("legend_y", .035)),
                       ncol=layout.get("legend_columns", 4), columnspacing=1.2,
                       handletextpad=.4, handlelength=1.4, labelspacing=.6)
        if settings.get("note"):
            fig.text(layout.get("left", .09), .012, settings["note"], va="bottom", fontsize=font, color=theme["muted"])
        if settings.get("watermark"):
            fig.text(.98, .012, settings["watermark"], ha="right", va="bottom", fontsize=font, color=theme["warm"])
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        page = fig.bbox
        warnings = []
        visible_fonts = []
        for text in fig.findobj(Text):
            if not text.get_visible() or not text.get_text():
                continue
            bounds = text.get_window_extent(renderer)
            if bounds.width == 0 or bounds.height == 0:
                continue
            # Invisible tick labels outside the plotting domain are not exported.
            if text.axes is not None and text in text.axes.get_xticklabels() + text.axes.get_yticklabels():
                x, y = text.get_position()
                axis, coord = ("x", x) if text in text.axes.get_xticklabels() else ("y", y)
                lo, hi = sorted(getattr(text.axes, "get_"+axis+"lim")())
                if coord < lo or coord > hi:
                    continue
            visible_fonts.append(text.get_fontsize())
            if bounds.x0 < page.x0-.5 or bounds.x1 > page.x1+.5 or bounds.y0 < page.y0-.5 or bounds.y1 > page.y1+.5:
                warnings.append("Text leaves page: " + text.get_text())
        if visible_fonts and min(visible_fonts) < 7:
            warnings.append("Text below 7 pt at declared publication size; inspect readability")
        layout_issues = audit_figure(
            fig, min_font_pt=settings.get("min_font_pt", 7),
            display_width_inches=settings.get("display_width_inches"),
            check_data_occlusion=settings.get("check_data_occlusion", True))
        warnings.extend(issue_message(item) for item in layout_issues)
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        for fmt in formats:
            metadata = {"Creator": "paper-figure-creation/render_graphs.py"} if fmt == "pdf" else None
            # No bbox_inches=tight: it changes declared physical size and type scale.
            fig.savefig(out.with_suffix("."+fmt), format=fmt, dpi=dpi, metadata=metadata)
        report = {"renderer": "render_graphs.py", "physical_size_in": [width, height],
                  "minimum_text_pt": min(visible_fonts) if visible_fonts else None,
                  "formats": list(formats), "warnings": warnings, "evidence": evidence,
                  "layout_issues": layout_issues,
                  "data_occlusion_check_requested": settings.get("check_data_occlusion", True),
                  "panels": [{"title": c.get("title"), "type": c["type"],
                              "xlim": list(a.get_xlim()), "ylim": list(a.get_ylim()),
                              "plotted_result_ids": [rid for s in c["series"] for rid in s["result_ids"] if not results[rid].get("missing")],
                              "missing_result_ids": [rid for s in c["series"] for rid in s["result_ids"] if results[rid].get("missing")]} for c,a in zip(charts,axes)],
                  "review_limit": "Checks declared evidence, bounds, size, text overlap, and supported legend/data occlusion. Scientific truth and complete visual quality still require source and pixel review."}
        out.with_name(out.name + "-review.json").write_text(json.dumps(report, indent=2) + "\n")
        return report
    finally:
        plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formats", nargs="+", choices=("svg", "pdf", "png"), default=("svg", "pdf", "png"))
    args = parser.parse_args(argv)
    try:
        report = render_graphs(json.loads(args.spec.read_text()), args.output, args.formats)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
