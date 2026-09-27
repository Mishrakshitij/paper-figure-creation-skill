#!/usr/bin/env python3
"""Render standalone, evidence-linked experimental graphs at physical print size.

The specification shares provenance/evidence/charts with render_figure.py.
CLI: render_graphs.py spec.json --output output/figure [--formats svg pdf png]
     [--styles paper-styles.json]

figure.preset "house" applies the house figure standard: 6 pt labels, 7.5 pt
panel titles, a 5.3 pt floor, role encodings (ours = large star in one hot
colour, ablation = hollow diamond, baseline = muted circle, reference = black
square), "(ours)" in legends and better-direction arrows from the evidence
ledger. A chart "pareto" block draws the non-dominated plotted points as a step
line; the frontier is computed, never typed.
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
PRESETS = ("classic", "house")
STYLE_FIELDS = ("color", "marker", "markerfacecolor", "linestyle")
# Shape and fill carry the role, so it survives grayscale; colour adds identity.
HOUSE_ROLES = {
    "proposed": {"colors": ["#D55E00"], "marker": "*", "markerfacecolor": None,
                 "linestyle": "-", "ms": 8.5, "lw": 1.6},
    "ablation": {"colors": ["#E69F00", "#A64B16", "#F0A860"], "marker": "D",
                 "markerfacecolor": "white", "linestyle": "--", "ms": 4.6, "lw": 1.1},
    "baseline": {"colors": ["#7C8894", "#4F6D87", "#9C8F7E", "#5F8479", "#8B7D98", "#56616B"],
                 "marker": "o", "markerfacecolor": None, "linestyle": "-", "ms": 4.6, "lw": 1.0},
    "reference": {"colors": ["#111111"], "marker": "s", "markerfacecolor": None,
                  "linestyle": ":", "ms": 4.4, "lw": 1.0},
}
# Series without a role (tasks, conditions) avoid the hot colour and the role shapes.
HOUSE_NEUTRAL = ["#3F6E9A", "#4E8A6E", "#86689A", "#6B7885", "#8F8360", "#5B6C5D"]
HOUSE_MARKERS = ["o", "^", "v", "P", "X", "d"]
ARROWS = {"higher": "\u2191", "lower": "\u2193"}
FRONTIER_GID = "pareto-frontier"
CAP_CLEARANCE_PT = 1.5


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


def _series_key(series):
    key = series.get("style_id", series.get("id", series.get("label")))
    if not isinstance(key, str) or not key:
        raise ValueError("Each graph series needs id, style_id, or label")
    return key


def _role_style(role, preset, counts, index):
    """Default encoding for a role; explicit series or registry fields win."""
    if preset == "house" and role in HOUSE_ROLES:
        spec = HOUSE_ROLES[role]
        n = counts.get(role, 0)
        counts[role] = n + 1
        return {"color": spec["colors"][n % len(spec["colors"])], "marker": spec["marker"],
                "markerfacecolor": spec["markerfacecolor"], "linestyle": spec["linestyle"],
                "ms": spec["ms"], "lw": spec["lw"], "role": role}
    if preset == "house":
        return {"color": HOUSE_NEUTRAL[index % len(HOUSE_NEUTRAL)],
                "marker": HOUSE_MARKERS[index % len(HOUSE_MARKERS)], "markerfacecolor": None,
                "linestyle": "-", "ms": 4.6, "lw": 1.0, "role": role}
    proposed = role == "proposed"
    return {"color": "#007D8A" if proposed else COLORS[index % len(COLORS)],
            "marker": MARKERS[index % len(MARKERS)], "markerfacecolor": None,
            "linestyle": "-", "ms": 5.5 if proposed else 4.6, "lw": 1.5 if proposed else 1.0,
            "role": role}


def _check_registry(registry):
    if not isinstance(registry, dict):
        raise ValueError("styles must map series ids or style_ids to style objects")
    for key, entry in registry.items():
        if not isinstance(entry, dict) or any(f not in STYLE_FIELDS + ("role",) for f in entry):
            raise ValueError(f"Style registry entry {key} may set only {', '.join(STYLE_FIELDS)} and role")
        if entry.get("role") is not None and entry["role"] not in HOUSE_ROLES:
            raise ValueError(f"Style registry entry {key} has an unknown role")


def _style_map(charts, preset="classic", registry=None):
    """One encoding per series key across panels, and across figures via a registry."""
    registry = registry or {}
    styles, counts = {}, {}
    for chart in charts:
        for series in chart["series"]:
            key = _series_key(series)
            fixed = registry.get(key, {})
            role = series.get("role", fixed.get("role"))
            if preset == "house" and role is not None and role not in HOUSE_ROLES:
                raise ValueError("House roles are proposed, ablation, baseline, or reference")
            for field in STYLE_FIELDS + ("role",):
                if field in fixed and field in series and fixed[field] != series[field]:
                    raise ValueError(f"Conflicting {field} for stable series {key} (style registry)")
            if key in styles:
                for field in STYLE_FIELDS:
                    if field in series and styles[key][field] != series[field]:
                        raise ValueError(f"Conflicting {field} for stable series {key}")
                # A method is ours in every panel or in none; classic tolerates an omitted role.
                if role != styles[key]["role"] and (preset == "house" or None not in (role, styles[key]["role"])):
                    raise ValueError(f"Conflicting role for stable series {key}")
                continue
            new = _role_style(role, preset, counts, len(styles))
            for field in STYLE_FIELDS:
                if field in fixed:
                    new[field] = fixed[field]
                if field in series:
                    new[field] = series[field]
            styles[key] = new
    return styles


def _axis_directions(chart, metrics):
    """Better direction per axis from the evidence ledger; a declared one must agree."""
    value_axis = "x" if chart["type"] in ("dot", "bar") else "y"
    found = {"x": None, "y": None}
    found[value_axis] = metrics.get(chart.get("metric_id"), {}).get("direction")
    if chart["type"] in ("line", "scatter") and chart.get("x_metric_id") in metrics:
        found["x"] = metrics[chart["x_metric_id"]].get("direction")
    for axis in ("x", "y"):
        declared = chart.get(axis + "direction")
        if declared is None:
            continue
        if declared not in ("higher", "lower", "none"):
            raise ValueError(axis + "direction must be higher, lower, or none")
        if declared != "none" and found[axis] in ARROWS and declared != found[axis]:
            raise ValueError(f"{axis}direction contradicts the evidence metric direction")
        found[axis] = None if declared == "none" else declared
    return found


def _directed_label(text, direction, axis, append):
    """Keep a typed arrow only if it matches the ledger; append one when asked."""
    text = text or ""
    up = "\u2191" in text or "\\uparrow" in text
    down = "\u2193" in text or "\\downarrow" in text
    if direction in ARROWS and up != down:
        if (direction == "higher") != up:
            raise ValueError(f"The {axis}-axis arrow contradicts the evidence metric direction")
        return text
    if append and direction in ARROWS and text and not (up or down):
        arrow = ARROWS[direction]
        return f"{text} {arrow}" if text.rstrip().endswith(")") else f"{text} ({arrow})"
    return text


def _pareto_front(chart, results, directions):
    """Non-dominated plotted points and their step outline, in plotting order."""
    cfg = chart.get("pareto")
    if not cfg:
        return None
    cfg = {} if cfg is True else cfg
    if not isinstance(cfg, dict):
        raise ValueError("pareto must be true or an object")
    if chart["type"] != "scatter":
        raise ValueError("A Pareto frontier needs a scatter chart with measured x and y")
    xdir, ydir = cfg.get("x", directions["x"]), cfg.get("y", directions["y"])
    if xdir not in ARROWS or ydir not in ARROWS:
        raise ValueError("A Pareto frontier needs a better direction on both axes")
    if (directions["x"] in ARROWS and xdir != directions["x"]) or (directions["y"] in ARROWS and ydir != directions["y"]):
        raise ValueError("Pareto directions contradict the evidence metric directions")
    include = cfg.get("series")
    names = {_series_key(s) for s in chart["series"]} | {s.get("id") for s in chart["series"]}
    if include is not None and (not isinstance(include, list) or not include or any(k not in names for k in include)):
        raise ValueError("pareto.series must list series ids or style_ids of this chart")
    points = []
    for series in chart["series"]:
        if include is not None and _series_key(series) not in include and series.get("id") not in include:
            continue
        xs = series.get("x_values", chart.get("x_values"))
        for x, y, rid in zip(xs, series["values"], series["result_ids"]):
            if x is not None and y is not None and not results[rid].get("missing"):
                points.append((x, y, rid))
    sx = 1 if xdir == "lower" else -1
    sy = 1 if ydir == "higher" else -1

    def dominates(q, p):
        return (sx*q[0] <= sx*p[0] and sy*q[1] >= sy*p[1]
                and (sx*q[0] < sx*p[0] or sy*q[1] > sy*p[1]))

    front = sorted((p for p in points if not any(dominates(q, p) for q in points)),
                   key=lambda p: (sx*p[0], -sy*p[1]))
    vx, vy = [], []
    for x, y, _ in front:
        if vx:  # corner (next x, previous y): the attainment staircase
            vx.append(x); vy.append(vy[-1])
        vx.append(x); vy.append(y)
    return {"x": vx, "y": vy, "result_ids": [p[2] for p in front], "config": cfg,
            "directions": {"x": xdir, "y": ydir}}


def _hide_intervals_inside_markers(ax, drawn):
    """An interval that ends within CAP_CLEARANCE_PT of its marker's edge cannot
    be read, and its caps collide with the marker. Hide that bar and its caps and
    report the interval, so the caption can state it; the data and the other
    axis's interval are untouched."""
    to_pt = 72 / ax.figure.dpi
    hidden = []
    for container, point, spans, ms, owners in drawn:
        _, caplines, barcols = container.lines
        for axis, span in spans.items():
            if span is None:
                continue
            ends = [(span[0], point[1]), (span[1], point[1])] if axis == "x" else [(point[0], span[0]), (point[0], span[1])]
            centre = ax.transData.transform(point)
            reach = max(abs(ax.transData.transform(e) - centre)[0 if axis == "x" else 1] for e in ends) * to_pt
            if reach >= ms / 2 + CAP_CLEARANCE_PT:
                continue
            for cap in caplines:
                if cap.get_marker() == ("|" if axis == "x" else "_"):
                    cap.set_visible(False)
            for col in barcols:
                segs = col.get_segments()
                horizontal = bool(segs) and abs(segs[0][0][1] - segs[0][1][1]) < 1e-12
                if horizontal == (axis == "x"):
                    col.set_visible(False)
            hidden.append({"result_id": owners[axis], "axis": axis, "reach_pt": round(float(reach), 2),
                           "marker_radius_pt": ms / 2})
    return hidden


def _legend_entries(axes):
    """Unique legend entries in series order; the computed frontier goes last."""
    entries = []
    for ax in axes:
        for handle, label in zip(*ax.get_legend_handles_labels()):
            if label not in [e[1] for e in entries]:
                entries.append((handle, label))
    entries.sort(key=lambda e: getattr(e[0], "get_gid", lambda: None)() == FRONTIER_GID)
    return [e[0] for e in entries], [e[1] for e in entries]


def _point_role_styles(series, n):
    """Per-point role encodings for one-series-per-chart dot plots."""
    roles = series["point_roles"]
    if not isinstance(roles, list) or len(roles) != n:
        raise ValueError("point_roles must align with values")
    counts, out = {}, []
    for role in roles:
        if role is not None and role not in HOUSE_ROLES:
            raise ValueError("point_roles are proposed, ablation, baseline, reference, or null")
        out.append(_role_style(role, "house", counts, len(out)))
    return out


def _draw_panel(ax, chart, results, styles, theme, index, options=None):
    options = options or {}
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
    directions = _axis_directions(chart, options.get("metrics", {}))
    front = _pareto_front(chart, results, directions)
    drawn = []
    group_width = .68 / len(series_list)
    for i, series in enumerate(series_list):
        vals = series["values"]
        key = _series_key(series)
        style = styles[key]
        label = series.get("label", key)
        # An empty or null label keeps the series out of the legend; never turn it into " (ours)".
        if label and options.get("mark_ours") and style["role"] == "proposed" and "(ours)" not in label.lower():
            label += " (ours)"
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
                    lw=style["lw"], linestyle=style["linestyle"], zorder=2)
        first = True
        offsets = series.get("point_label_offsets", [[4, 5] for _ in vals])
        labels = series.get("point_labels", ["" for _ in vals])
        aligns = series.get("point_label_align", ["auto" for _ in vals])
        role_styles = _point_role_styles(series, len(vals)) if "point_roles" in series else None
        point_colors = series.get("point_colors", [r["color"] for r in role_styles] if role_styles else [color for _ in vals])
        point_markers = series.get("point_markers", [r["marker"] for r in role_styles] if role_styles else [marker for _ in vals])
        if any(len(a) != len(vals) for a in (offsets, labels, aligns, point_colors, point_markers)):
            raise ValueError("Point label arrays must align with values")
        for j, (v, rid) in enumerate(zip(vals, series["result_ids"])):
            if v is None:
                continue
            point_color = point_colors[j]
            point_marker = point_markers[j]
            point_face = point_color if "point_colors" in series else face
            point_ms = style["ms"]
            if role_styles:
                point_face = role_styles[j]["markerfacecolor"] or point_color
                point_ms = role_styles[j]["ms"]
            interval = _uncertainty(results[rid])
            error = np.array([[v-interval[0]], [interval[1]-v]]) if interval else None
            xinterval = _uncertainty(results[series["x_result_ids"][j]]) if not categorical and "x_result_ids" in series else None
            xerror = np.array([[xs[j]-xinterval[0]], [xinterval[1]-xs[j]]]) if xinterval else None
            kwargs = dict(color=point_color, marker=point_marker, mfc=point_face, mec=point_color, mew=.8,
                          ms=point_ms, elinewidth=.9, capsize=2.0, label=label if first else None, zorder=3)
            if kind == "bar":
                ax.barh([xs[j]], [v], height=group_width*.82, color=point_color,
                        xerr=error, error_kw={"capsize": 2, "elinewidth": .9},
                        label=label if first else None, zorder=3)
            else:
                container = ax.errorbar([v] if categorical else [xs[j]], [xs[j]] if categorical else [v],
                                        xerr=error if categorical else xerror, yerr=None if categorical else error,
                                        linestyle="none", **kwargs)
                point = (v, xs[j]) if categorical else (xs[j], v)
                spans = {"x": interval if categorical else xinterval, "y": None if categorical else interval}
                owners = {"x": rid if categorical else series.get("x_result_ids", [None] * len(vals))[j],
                          "y": None if categorical else rid}
                drawn.append((container, point, spans, point_ms, owners))
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
    if front and len(front["result_ids"]) > 1:
        cfg = front["config"]
        ax.plot(front["x"], front["y"], color=cfg.get("color", theme["ink"]), lw=cfg.get("linewidth", .9),
                linestyle=cfg.get("linestyle", "-"), solid_joinstyle="miter", zorder=1.8, gid=FRONTIER_GID,
                label=cfg.get("label", "Pareto frontier") if cfg.get("legend", True) else None)
    for axis in ("x", "y"):
        scale = chart.get(axis + "scale", "linear")
        if scale not in ("linear", "log"):
            raise ValueError("Only explicit linear and log scales are supported")
        getattr(ax, "set_" + axis + "scale")(scale)
    if categorical:
        if options.get("mark_ours") and "point_roles" in series_list[0] and len(series_list) == 1:
            cats = [c + " (ours)" if r == "proposed" and "(ours)" not in c.lower() else c
                    for c, r in zip(cats, series_list[0]["point_roles"])]
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
    hidden = _hide_intervals_inside_markers(ax, drawn)
    arrows = options.get("direction_arrows", False)
    ax.set_xlabel(_directed_label(chart.get("xlabel", ""), directions["x"], "x", arrows), labelpad=6)
    ax.set_ylabel(_directed_label(chart.get("ylabel", ""), directions["y"], "y", arrows), labelpad=6)
    ax.tick_params(length=3, width=.6)
    if categorical:
        ax.tick_params(axis="y", length=0)
    ax.minorticks_off()
    panel_label = chart.get("panel_label", chr(97 + index))
    ax.set_title((panel_label + "  " if panel_label else "") + chart.get("title", ""),
                 loc="left", pad=9, fontsize=theme["panel_title_size"])
    if chart.get("legend", False):
        handles, labels = _legend_entries([ax])
        ax.legend(handles, labels, loc=chart.get("legend_loc", "best"), ncol=chart.get("legend_columns", 1))
    return {"axis_directions": directions,
            "pareto_result_ids": front["result_ids"] if front else None,
            "intervals_inside_marker": hidden}


def render_graphs(spec, out, formats=("svg", "pdf", "png"), styles=None):
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
    preset = settings.get("preset", "classic")
    if preset not in PRESETS:
        raise ValueError("figure.preset must be classic or house")
    house = preset == "house"
    # House: build at the template's \linewidth (5.5 in for ICLR/NeurIPS) and
    # include with width=\linewidth, so source and print sizes are equal.
    width = settings.get("width_in", 5.5 if house else 7.2)
    height = settings.get("height_in", 2.2 if house else 3.6)
    font = settings.get("font_pt", 6 if house else 8)
    floor = settings.get("min_font_pt", 5.3 if house else 7)
    hard_floor = 5.3 if house else 6
    dpi = settings.get("dpi", 300)
    panel_pt = settings.get("panel_title_pt", font + (1.5 if house else 1))
    title_pt = settings.get("title_pt", font + 2.5)
    if any(not finite(v) or v <= 0 for v in (width, height, font, dpi, floor, panel_pt, title_pt)) or font < hard_floor:
        raise ValueError(f"Positive physical dimensions/dpi and font_pt >= {hard_floor} required")
    registry = dict(styles or {})
    for key, entry in (spec.get("styles") or {}).items():
        if key in registry and registry[key] != entry:
            raise ValueError(f"Spec styles entry {key} contradicts the shared style registry")
        registry[key] = entry
    _check_registry(registry)
    options = {"metrics": {m["id"]: m for m in spec["evidence"]["metrics"]},
               "mark_ours": settings.get("mark_ours", house),
               "direction_arrows": settings.get("direction_arrows", house)}
    theme = load_theme(overrides={**spec.get("theme", {}), "font_size": font,
                                 "small_size": font, "panel_title_size": panel_pt,
                                 "title_size": title_pt, "dpi": dpi})
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
        style_map = _style_map(charts, preset, registry)
        axes, infos = [], []
        for i, chart in enumerate(charts):
            rect = chart.get("rect")
            if rect is not None and (len(rect) != 4 or any(not finite(v) for v in rect) or
                                     min(rect[:2]) < 0 or min(rect[2:]) <= 0 or rect[0]+rect[2] > 1 or rect[1]+rect[3] > 1):
                raise ValueError("rect must be a positive, on-page [left,bottom,width,height] fraction")
            ax = fig.add_axes(rect) if rect is not None else fig.add_subplot(grid[i//cols, i%cols])
            axes.append(ax)
            infos.append(_draw_panel(ax, chart, results, style_map, theme, i, options))
        if settings.get("title"):
            fig.text(layout.get("left", .09), .975, settings["title"], va="top",
                     fontsize=theme["title_size"], weight="bold")
        if settings.get("subtitle"):
            fig.text(layout.get("left", .09), .914, settings["subtitle"], va="top", fontsize=font, color=theme["muted"])
        if layout.get("shared_legend", False):
            handles, labels = _legend_entries(axes)
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
        if visible_fonts and min(visible_fonts) < floor:
            warnings.append(f"Text below {floor:g} pt at declared publication size; inspect readability")
        for chart, info in zip(charts, infos):
            for item in info["intervals_inside_marker"]:
                warnings.append(f"The {item['axis']} interval of {item['result_id']} ends at its marker's edge, "
                                "so its bar and caps are hidden; state the interval in the caption")
            front = info["pareto_result_ids"]
            if front is not None and len(front) < 2:
                warnings.append(f"Pareto frontier of panel '{chart.get('title', '')}' has one point, "
                                "which dominates the others; no step line drawn")
        layout_issues = audit_figure(
            fig, min_font_pt=floor,
            display_width_inches=settings.get("display_width_inches"),
            check_data_occlusion=settings.get("check_data_occlusion", True))
        warnings.extend(issue_message(item) for item in layout_issues)
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        for fmt in formats:
            metadata = {"Creator": "paper-figure-creation/render_graphs.py"} if fmt == "pdf" else None
            # No bbox_inches=tight: it changes declared physical size and type scale.
            fig.savefig(out.with_suffix("."+fmt), format=fmt, dpi=dpi, metadata=metadata)
        report = {"renderer": "render_graphs.py", "preset": preset, "physical_size_in": [width, height],
                  "minimum_text_pt": min(visible_fonts) if visible_fonts else None,
                  "formats": list(formats), "warnings": warnings, "evidence": evidence,
                  "layout_issues": layout_issues,
                  "data_occlusion_check_requested": settings.get("check_data_occlusion", True),
                  "panels": [{"title": c.get("title"), "type": c["type"],
                              "xlim": list(a.get_xlim()), "ylim": list(a.get_ylim()),
                              "plotted_result_ids": [rid for s in c["series"] for rid in s["result_ids"] if not results[rid].get("missing")],
                              "missing_result_ids": [rid for s in c["series"] for rid in s["result_ids"] if results[rid].get("missing")],
                              "axis_directions": info["axis_directions"],
                              "pareto_result_ids": info["pareto_result_ids"],
                              "intervals_inside_marker": info["intervals_inside_marker"]} for c, a, info in zip(charts, axes, infos)],
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
    parser.add_argument("--styles", type=Path,
                        help="shared style registry (series id -> color/marker/markerfacecolor/linestyle/role) "
                             "so every figure of the paper encodes a method the same way")
    args = parser.parse_args(argv)
    try:
        registry = json.loads(args.styles.read_text()) if args.styles else None
        report = render_graphs(json.loads(args.spec.read_text()), args.output, args.formats, registry)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
