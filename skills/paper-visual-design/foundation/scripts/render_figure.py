#!/usr/bin/env python3
"""Render editable scientific teaser, method, and benchmark figures from JSON.

This renderer is a deterministic starter, not an automatic scientific designer.
Write the figure's story, select evidence and choose geometry before rendering.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Ellipse, Polygon
import numpy as np

from figure_style import apply_theme, load_theme
from layout_quality import audit_figure, issue_message, wrap_text_artist

PORTS = {"left": (0, .5), "right": (1, .5), "top": (.5, 1), "bottom": (.5, 0)}


def text(ax, x, y, label, theme, size=None, **kw):
    return ax.text(x, y, str(label), fontsize=size or theme["font_size"],
                   color=kw.pop("color", theme["ink"]), **kw)


def box(ax, x, y, w, h, theme, fill=None, edge=None, radius=.015,
        dashed=False, linewidth=None, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill or theme["paper"], edgecolor=edge or theme["grid"],
        linewidth=linewidth or theme["line_width"],
        linestyle=(0, (3, 2)) if dashed else "solid", zorder=zorder)
    ax.add_patch(p)
    return p


def arrow(ax, points, theme, kind="solid", color=None, head=True, lw=None):
    color = color or theme["muted"]
    style = (0, (3, 2)) if kind in ("skip", "dashed", "training") else "solid"
    if len(points) > 2:
        p = np.asarray(points)
        ax.plot(p[:-1, 0], p[:-1, 1], color=color, linewidth=lw or 1,
                linestyle=style, solid_capstyle="round", zorder=1)
    p = FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>" if head else "-",
                         mutation_scale=8, color=color, linewidth=lw or 1,
                         linestyle=style, shrinkA=0, shrinkB=0, zorder=1)
    ax.add_patch(p)


def tile_grid(ax, rect, rows, cols, theme, selected=None, labels=None, mask=None):
    x, y, w, h = rect
    gap = min(w / cols, h / rows) * .10
    tw, th = w / cols, h / rows
    selected = set(selected or [])
    mask = set(mask or [])
    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            cx, cy = x + col * tw, y + (rows - 1 - row) * th
            fill = theme["accent_light"] if i in selected else theme["panel"]
            edge = theme["accent"] if i in selected else theme["grid"]
            if i in mask:
                fill, edge = theme["paper"], theme["grid"]
            ax.add_patch(Rectangle((cx + gap / 2, cy + gap / 2), tw - gap,
                                  th - gap, facecolor=fill, edgecolor=edge, lw=.65, zorder=2.5))
            if labels and i < len(labels) and i not in mask:
                text(ax, cx + tw / 2, cy + th / 2, labels[i], theme,
                     size=theme["small_size"], ha="center", va="center", zorder=3)
            elif i in mask:
                text(ax, cx + tw / 2, cy + th / 2, "·", theme,
                     color=theme["muted"], ha="center", va="center", zorder=3)


def draw_concept(ax, concept, theme):
    """Small, task-specific representation, never a large generic process box."""
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    title = concept.get("title", "Problem → proposal")
    ax.set_title("a  " + title, loc="left", pad=13)
    kind = concept.get("kind", "token_grid")
    text(ax, 0, .93, concept.get("input_label", "Input"), theme,
         size=theme["small_size"], color=theme["muted"], va="top")
    if kind in ("token_grid", "spatial"):
        rows, cols = concept.get("rows", 3), concept.get("cols", 4)
        selected = concept.get("selected", [1, 5, 6, 10])
        tile_grid(ax, (.03, .58, .72, .28), rows, cols, theme,
                  selected=selected, labels=concept.get("labels"), mask=concept.get("mask"))
        if kind == "spatial":
            # Geometry is schematic; selected cells denote regions, not measured saliency.
            x, y, w, h = concept.get("region", [.39, .57, .20, .21])
            ax.add_patch(Rectangle((x, y), w, h, fill=False,
                                  edgecolor=theme["warm"], lw=1.2))
        arrow(ax, [(.39, .55), (.39, .42)], theme, color=theme["accent"])
        text(ax, .47, .485, concept.get("operation_label", "Select useful tokens"),
             theme, size=theme["small_size"], va="center")
        selected_labels = [concept.get("labels", [""] * (rows * cols))[i]
                           for i in selected if i < len(concept.get("labels", [""] * (rows * cols)))]
        tile_grid(ax, (.03, .29, .72, .10), 1, max(1, len(selected)), theme,
                  selected=list(range(len(selected))), labels=selected_labels)
        text(ax, 0, .20, concept.get("output_label", "Less work; useful information kept"),
             theme, weight="bold", va="top")
    elif kind == "retrieval":
        box(ax, .02, .70, .71, .16, theme, fill=theme["panel"])
        text(ax, .055, .78, concept.get("query", "Which evidence answers this?"),
             theme, size=theme["small_size"], va="center")
        arrow(ax, [(.375, .68), (.375, .57)], theme)
        docs = concept.get("documents", ["Relevant A", "Distractor", "Relevant B"])
        selected = set(concept.get("selected", [0, 2]))
        for i, label in enumerate(docs):
            yy = .49 - i * .115
            color = theme["accent"] if i in selected else theme["grid"]
            box(ax, .02, yy, .71, .09, theme,
                fill=theme["accent_light"] if i in selected else theme["panel"], edge=color)
            text(ax, .055, yy + .045, label, theme, size=theme["small_size"], va="center")
        text(ax, 0, .12, concept.get("output_label", "Retrieve evidence before generation"),
             theme, weight="bold", va="top")
    elif kind == "matrix":
        values = np.asarray(concept.get("values", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
        ax.imshow(values, extent=(.04, .72, .32, .86), aspect="auto", cmap="Blues",
                  vmin=concept.get("vmin", 0), vmax=concept.get("vmax", 1), interpolation="nearest")
        text(ax, .38, .27, concept.get("matrix_label", "Sparse interaction pattern"),
             theme, size=theme["small_size"], ha="center", va="top")
        text(ax, 0, .14, concept.get("output_label", "Keep the interactions that matter"),
             theme, weight="bold", va="top")
    elif kind == "custom":
        # Exactly the same expressive node/edge grammar as a method panel.
        draw_method_contents(ax, concept, theme)
    else:
        raise ValueError(f"Unsupported concept kind {kind!r}")
    if concept.get("note"):
        text(ax, 0, -.03, concept["note"], theme, size=theme["small_size"],
             color=theme["muted"], va="top")


def series_color(series, index, theme):
    return theme["accent"] if series.get("role") == "proposed" else theme["baseline_colors"][index % len(theme["baseline_colors"]) ]


def chart_claim(chart, spec):
    cid = chart.get("claim_id")
    if not cid:
        return None
    claims = spec.get("evidence", {}).get("claims", [])
    claim = next((c for c in claims if c["id"] == cid), None)
    if not claim:
        raise ValueError(f"Chart references unknown claim {cid}")
    computed = next((c for c in spec.get("_computed_claims", []) if c["id"] == cid), None)
    if not computed: raise ValueError(f"Claim {cid} did not validate")
    return chart.get("claim_label", "") + computed["display"]


def check_chart_coordinates(chart, active_xlim=None, active_ylim=None):
    """Never silently hide declared observations through bounds or log masking."""
    kind=chart.get("type","dot")
    horizontal=kind in ("dot","bar")
    if horizontal and chart.get("yscale")=="log":
        raise ValueError("Categorical chart axes cannot use a log scale")
    if kind=="bar" and chart.get("xscale")=="log":
        raise ValueError("Bar charts require a zero baseline and cannot use a log value axis")
    limits={"x":active_xlim if active_xlim is not None else chart.get("xlim"),
            "y":active_ylim if active_ylim is not None else chart.get("ylim")}
    for axis,bounds in limits.items():
        if bounds is not None:
            if len(bounds)!=2 or any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in bounds) or bounds[0]==bounds[1]:
                raise ValueError(f"{axis} limits must contain two distinct finite values")
            if chart.get(axis+"scale")=="log" and min(bounds)<=0:
                raise ValueError(f"Log {axis} limits must be positive")
    for series in chart["series"]:
        values=series["values"]
        independent=series.get("x_values",chart.get("x_values",list(range(len(values)))))
        for i,value in enumerate(values):
            if value is None: continue
            coords={"x":value} if horizontal else {"x":independent[i],"y":value}
            if any(v is None for v in coords.values()): continue
            for axis,v in coords.items():
                if not math.isfinite(v):
                    raise ValueError("Chart coordinates must be finite or explicit missing nulls")
                if chart.get(axis+"scale")=="log" and v<=0:
                    raise ValueError(f"Nonpositive log {axis} coordinate in series {series.get('id',series.get('label',''))}, point {i}: {v}")
                bounds=limits[axis]
                if bounds is not None:
                    lo,hi=sorted(bounds)
                    tol=max(1,abs(lo),abs(hi))*1e-10
                    if v<lo-tol or v>hi+tol:
                        raise ValueError(f"Data point outside {axis} limits: series {series.get('id',series.get('label',''))}, point {i}, value {v}, limits {list(bounds)}")
            uncertainty = series.get("errors")
            if uncertainty is not None and uncertainty[i] is not None:
                error = uncertainty[i]
                axis = "x" if horizontal else "y"
                if not isinstance(error, (int, float)) or not math.isfinite(error) or error < 0:
                    raise ValueError("Error extents must be finite and nonnegative")
                endpoints = (value-error, value+error)
                if chart.get(axis+"scale") == "log" and endpoints[0] <= 0:
                    raise ValueError(f"Uncertainty extends outside log {axis} domain")
                if limits[axis] is not None:
                    lo, hi = sorted(limits[axis])
                    tol = max(1, abs(lo), abs(hi))*1e-10
                    if endpoints[0] < lo-tol or endpoints[1] > hi+tol:
                        raise ValueError(f"Uncertainty outside {axis} limits: point {i}, interval {endpoints}")


def draw_chart(ax, chart, spec, theme, index=0):
    check_chart_coordinates(chart)
    kind = chart.get("type", "dot")
    series = chart["series"]
    cats = chart.get("categories", [])
    if not series:
        raise ValueError("A chart needs at least one series")
    n = len(series[0]["values"])
    if not cats:
        cats = [str(i + 1) for i in range(n)]
    if len(cats) != n or any(len(s["values"]) != n for s in series):
        raise ValueError("Categories, values and each series must have equal length")
    positions = np.arange(n, dtype=float)
    width = .66 / len(series)
    markers = ["o", "s", "^", "D", "v", "P"]
    for i, s in enumerate(series):
        values = np.asarray([np.nan if v is None else v for v in s["values"]], dtype=float)
        if np.isinf(values).any():
            raise ValueError("Chart values must be finite or explicit missing nulls")
        color = series_color(s, i, theme)
        offset = (i - (len(series) - 1) / 2) * width
        errors = s.get("errors")
        label = s.get("label", s.get("id", "Method"))
        if kind in ("dot", "bar"):
            y = positions + offset
            point_roles = s.get("point_roles", [s.get("role", "baseline")] * n)
            if len(point_roles) != n: raise ValueError("point_roles must align with values")
            for j, (v, yy) in enumerate(zip(values, y)):
                pcolor = theme["accent"] if point_roles[j] == "proposed" else color
                if s.get("point_roles") and point_roles[j] != "proposed":
                    pcolor = theme["baseline_colors"][i % len(theme["baseline_colors"]) ]
                err = errors[j] if errors is not None else None
                if kind == "dot":
                    ax.errorbar([v], [yy], xerr=err, fmt=markers[i % len(markers)],
                                color=pcolor, markeredgecolor=theme["paper"], markeredgewidth=.45,
                                markersize=5.7 if point_roles[j] == "proposed" else 5,
                                elinewidth=1, capsize=2.1, label=label if j == 0 else None, zorder=3)
                else:
                    ax.barh([yy], [v], height=width * .81, color=pcolor, edgecolor=theme["paper"],
                            linewidth=.4, xerr=err, error_kw={"capsize": 2, "elinewidth": .8},
                            label=label if j == 0 else None)
            if chart.get("value_labels", kind == "bar"):
                for v, yy in zip(values, y):
                    if not np.isfinite(v): continue
                    ax.annotate(format(v, chart.get("value_format", ".1f")), (v, yy),
                                xytext=(4, 0), textcoords="offset points", va="center",
                                fontsize=theme["small_size"], color=color)
        elif kind in ("line", "scatter"):
            x = s.get("x_values", chart.get("x_values", positions))
            if len(x) != n:
                raise ValueError("x_values must align with series values")
            ax.errorbar(x, values, yerr=errors, color=color, marker=markers[i % len(markers)],
                        markersize=4.2, linestyle="-" if kind == "line" else "none",
                        linewidth=1.5 if s.get("role") == "proposed" else 1,
                        capsize=2, label=label, zorder=3)
            for j, point_label in enumerate(s.get("point_labels", [])):
                if not point_label or not np.isfinite(values[j]): continue
                offsets = s.get("point_label_offsets", [[4, 5]] * n)
                ax.annotate(point_label, (x[j], values[j]), xytext=offsets[j],
                            textcoords="offset points", fontsize=theme["small_size"], color=color,
                            ha="left" if offsets[j][0] >= 0 else "right", va="bottom")
        else:
            raise ValueError(f"Unsupported chart type {kind!r}")
    ax.set_title(chr(98 + index) + "  " + chart["title"], loc="left", pad=13)
    if kind in ("dot", "bar"):
        ax.set_yticks(positions, cats)
        ax.set_ylim(n - .5, -.6)
        ax.grid(axis="x", color=theme["grid"], lw=.65, zorder=0)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0, pad=5)
        if kind == "bar":
            lo, hi = chart.get("xlim", [0, max(v for s in series for v in s["values"] if v is not None) * 1.16])
            if lo != 0:
                raise ValueError("Bar charts must use a zero baseline; use dot for a restricted range")
            ax.set_xlim(lo, hi)
        elif chart.get("xlim"):
            ax.set_xlim(*chart["xlim"])
        else:
            ax.margins(x=.15)
    else:
        ax.grid(axis="y", color=theme["grid"], lw=.65, zorder=0)
        if not chart.get("x_values") and not any(s.get("x_values") for s in series):
            ax.set_xticks(positions, cats)
        if chart.get("xlim"):
            ax.set_xlim(*chart["xlim"])
        if chart.get("ylim"):
            ax.set_ylim(*chart["ylim"])
    if chart.get("xscale"): ax.set_xscale(chart["xscale"])
    if chart.get("yscale"): ax.set_yscale(chart["yscale"])
    ax.set_axisbelow(True)
    ax.set_xlabel(chart.get("xlabel", ""), labelpad=6)
    ax.set_ylabel(chart.get("ylabel", ""), labelpad=6)
    ax.tick_params(length=3, width=.6)
    active_xlim,active_ylim=ax.get_xlim(),ax.get_ylim()
    if chart.get("xticks"):
        ax.set_xticks(chart["xticks"])
    if chart.get("yticks"):
        ax.set_yticks(chart["yticks"])
    # Matplotlib expands limits when explicit ticks are set. Restore the true
    # plotting domain so out-of-range ticks cannot override a user's limits.
    ax.set_xlim(active_xlim); ax.set_ylim(active_ylim)
    check_chart_coordinates(chart,ax.get_xlim(),ax.get_ylim())
    legend_loc = chart.get("legend_loc", "lower right" if kind in ("dot", "bar") else "best")
    if chart.get("legend", True):
        if legend_loc == "below":
            ax.legend(loc="upper center", bbox_to_anchor=(.5, -.28), ncol=min(3, len(series)),
                      handlelength=1.4, handletextpad=.55, columnspacing=.8, borderaxespad=0)
        else:
            ax.legend(loc=legend_loc, handlelength=1.4, handletextpad=.55,
                      borderaxespad=.25, labelspacing=.4)
    claim = chart_claim(chart, spec)
    if claim:
        ax.text(0, 1.015, claim, transform=ax.transAxes, fontsize=theme["small_size"],
                color=theme["accent"], va="bottom")


def node_port(node, port):
    u, v = port if isinstance(port, (list, tuple)) else PORTS.get(port, (.5, .5))
    return [node["x"] + u * node["w"], node["y"] + v * node["h"]]


def edge_points(edge, nodes):
    return [node_port(nodes[edge["source"]], edge.get("source_port", "right")),
            *edge.get("via", []),
            node_port(nodes[edge["target"]], edge.get("target_port", "left"))]


def draw_method_contents(ax, spec, theme):
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    for group_index, group in enumerate(spec.get("groups", [])):
        box(ax, group["x"], group["y"], group["w"], group["h"], theme,
            fill=group.get("fill", theme["panel"]), edge=theme["grid"], radius=.008, zorder=0)
        label = text(ax, group["x"] + .013, group["y"] + group["h"] - .018,
                     group["label"], theme, size=theme["small_size"], color=theme["muted"], va="top")
        label.set_gid(f"group-label:{group_index}")
    nodes = {n["id"]: n for n in spec["nodes"]}
    for edge_index, edge in enumerate(spec.get("edges", [])):
        pts = edge_points(edge, nodes)
        color = theme["accent"] if edge.get("role") == "proposed" else theme["muted"]
        arrow(ax, pts, theme, edge.get("kind", "solid"), color=color,
              head=edge.get("arrow", True))
        if edge.get("label"):
            pos = edge.get("label_position")
            if not pos:
                a, b = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
                pos = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + .035]
            label = text(ax, *pos, edge["label"], theme, size=theme["small_size"],
                         ha="center", va="center", zorder=5,
                         bbox={"facecolor": theme["paper"], "edgecolor": "none", "pad": 1})
            label.set_gid(f"edge-label:{edge_index}")
    for n in nodes.values():
        x, y, w, h = (n[k] for k in ("x", "y", "w", "h"))
        accent = n.get("role") == "proposed"
        fill = n.get("fill", theme["accent_light"] if accent else theme["paper"])
        edge = theme["accent"] if accent else theme["muted"]
        shape = n.get("shape", "box")
        if shape == "circle":
            ax.add_patch(Ellipse((x + w / 2, y + h / 2), w, h,
                                facecolor=fill, edgecolor=edge, lw=1, zorder=2))
        elif shape == "diamond":
            ax.add_patch(Polygon([(x, y+h/2), (x+w/2,y+h), (x+w,y+h/2), (x+w/2,y)],
                                 facecolor=fill,edgecolor=edge,lw=1,zorder=2))
        elif shape != "text":
            box(ax, x, y, w, h, theme, fill=fill, edge=edge, radius=.008,
                dashed=n.get("state") == "frozen", linewidth=1.1 if accent else .8)
        representation = n.get("representation")
        if representation:
            r = representation
            tile_grid(ax, (x+w*.16, y+h*.42, w*.68, h*.44),
                      r.get("rows", 2), r.get("cols", 4), theme,
                      selected=r.get("selected"), labels=r.get("labels"), mask=r.get("mask"))
            label_y = y+h*(.30 if n.get("state") or n.get("detail") else .23)
        else:
            label_y = y+h*(.57 if n.get("state") or n.get("detail") else .5)
        a = text(ax, x+w/2, label_y, n.get("label", ""), theme,
                 size=n.get("font_size", theme["font_size"]), weight="bold" if accent else "normal",
                 ha="center", va="center", zorder=3)
        a.set_gid("node-label:" + n["id"])
        if n.get("wrap_label", False):
            ax.figure.canvas.draw()
            width_px = ax.transData.transform((x+w, y))[0] - ax.transData.transform((x, y))[0]
            padding = float(n.get("text_padding_pt", 4)) * ax.figure.dpi / 72
            wrap_text_artist(a, width_px - 2*padding, ax.figure.canvas.get_renderer())
        detail = n.get("detail") or (n.get("state") if n.get("state") in ("frozen", "trainable") else None)
        if detail:
            a = text(ax, x+w/2, y+h*(.09 if representation else .22), detail, theme, size=theme["small_size"],
                     color=theme["accent"] if accent else theme["muted"], ha="center", va="center", zorder=3)
            a.set_gid("node-detail:" + n["id"])
    for label_index, label in enumerate(spec.get("annotations", [])):
        artist = text(ax, label["x"], label["y"], label["text"], theme,
             size=label.get("font_size", theme["small_size"]),
             color=theme["accent"] if label.get("role") == "proposed" else theme["muted"],
             ha=label.get("ha", "left"), va=label.get("va", "center"))
        artist.set_gid(f"annotation:{label_index}")


def drawio_export(spec, path, theme):
    """Uncompressed native diagrams.net XML with editable cells and routed edges."""
    W, H = round(spec.get("figure", {}).get("width_in", 7.2) * 100), round(spec.get("figure", {}).get("height_in", 3.6) * 100)
    top = .79 if spec.get("figure", {}).get("subtitle") else .83
    def X(x): return (.035 + .93 * x) * W
    def Y(y): return (1 - .11 - (top - .11) * y) * H
    doc = ET.Element("mxfile", host="app.diagrams.net", version="24.7.17")
    kind = spec.get("kind", "method")
    diagram = ET.SubElement(doc, "diagram", id=kind,
                            name="Benchmark / environment" if kind == "benchmark" else "Method")
    model = ET.SubElement(diagram, "mxGraphModel", dx=str(W), dy=str(H), grid="1", gridSize="10", page="1", pageScale="1", pageWidth=str(W), pageHeight=str(H), math="0", shadow="0")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    def cell(n, group=False):
        accent = n.get("role") == "proposed"
        fill = n.get("fill", theme["accent_light"] if accent else theme["paper"])
        edge = n.get("edge",theme["accent"] if accent else theme["muted"])
        shape = {"circle": "ellipse", "diamond": "rhombus", "text": "text"}.get(n.get("shape"), "rectangle")
        style = f"shape={shape};rounded=1;arcSize=8;whiteSpace=wrap;html=0;align={n.get('align','center')};fillColor={fill};strokeColor={edge};fontFamily={theme['font_family']};fontColor={theme['ink']};fontSize={n.get('font_size',theme['font_size'])*100/72:.2f};"
        if n.get("state") == "frozen": style += "dashed=1;"
        if group: style += "verticalAlign=top;align=left;spacing=10;fillColor=" + theme["panel"] + ";"
        value = n.get("label", "")
        if n.get("representation"): style += "verticalAlign=bottom;spacingBottom=8;"
        detail = n.get("detail") or n.get("state")
        if detail: value += "\n" + detail
        c = ET.SubElement(root, "mxCell", id=n["id"], value=value, style=style, vertex="1", parent="1")
        ET.SubElement(c, "mxGeometry", x=str(X(n["x"])), y=str(Y(n["y"]+n["h"])), width=str(n["w"]*.93*W), height=str(n["h"]*(top-.11)*H), **{"as":"geometry"})
    for i,g in enumerate(spec.get("groups", [])):
        cell({"id":f"group-{i}",**g}, True)
    for n in spec["nodes"]:
        cell(n)
        r = n.get("representation")
        if r:
            rows,cols = r.get("rows",2),r.get("cols",4)
            for row in range(rows):
                for col in range(cols):
                    i = row*cols+col
                    masked=i in r.get("mask",[])
                    selected=i in r.get("selected",[]) and not masked
                    labels=r.get("labels",[])
                    tile_label="·" if masked else (labels[i] if i<len(labels) else "")
                    cell({"id":f"{n['id']}-tile-{i}", "x":n["x"]+n["w"]*.16+col*n["w"]*.68/cols,
                          "y":n["y"]+n["h"]*.42+(rows-1-row)*n["h"]*.44/rows,
                          "w":n["w"]*.68/cols*.90,"h":n["h"]*.44/rows*.90,
                          "label":tile_label,"font_size":theme["small_size"],
                          "fill":theme["paper"] if masked else (theme["accent_light"] if selected else theme["panel"]),
                          "edge":theme["accent"] if selected else theme["grid"],
                          "role":"proposed" if selected else "baseline"})
    for i,e in enumerate(spec.get("edges", [])):
        sp,tp=e.get("source_port","right"),e.get("target_port","left")
        sx,sy = sp if isinstance(sp,(list,tuple)) else PORTS.get(sp,(.5,.5))
        tx,ty = tp if isinstance(tp,(list,tuple)) else PORTS.get(tp,(.5,.5))
        color = theme["accent"] if e.get("role") == "proposed" else theme["muted"]
        arrow_head="block" if e.get("arrow",True) else "none"
        style = f"edgeStyle=none;rounded=0;html=0;endArrow={arrow_head};endFill={int(e.get('arrow',True))};strokeColor={color};fontFamily={theme['font_family']};fontSize={theme['small_size']*100/72:.2f};exitX={sx};exitY={1-sy};exitDx=0;exitDy=0;entryX={tx};entryY={1-ty};entryDx=0;entryDy=0;"
        if e.get("kind") in ("skip","dashed","training"): style += "dashed=1;"
        c = ET.SubElement(root,"mxCell",id=f"edge-{i}", value=e.get("label",""),style=style,edge="1",parent="1",source=e["source"],target=e["target"])
        geo = ET.SubElement(c,"mxGeometry",relative="1",**{"as":"geometry"})
        if e.get("via"):
            arr = ET.SubElement(geo,"Array",**{"as":"points"})
            for x,y in e["via"]: ET.SubElement(arr,"mxPoint",x=str(X(x)),y=str(Y(y)))
    for i, annotation in enumerate(spec.get("annotations", [])):
        cell({"id":f"annotation-{i}","shape":"text","x":annotation["x"],"y":annotation["y"]-.025,
              "w":min(.65,1-annotation["x"]),"h":.05,"label":annotation["text"],"align":annotation.get("ha","left"),"font_size":annotation.get("font_size",theme["small_size"])})
    for i, (key, yy, size) in enumerate((("title",.02,theme["title_size"]),("subtitle",.12,theme["small_size"]),("note",.94,theme["small_size"]))):
        if spec.get("figure",{}).get(key):
            c=ET.SubElement(root,"mxCell",id=f"page-{key}",value=spec["figure"][key],
                style=f"text;html=0;align=left;verticalAlign=top;fontFamily={theme['font_family']};fontSize={size*100/72:.2f};fontColor={theme['ink']};",vertex="1",parent="1")
            ET.SubElement(c,"mxGeometry",x=str(.035*W),y=str(yy*H),width=str(.93*W),height=str(.07*H),**{"as":"geometry"})
    ET.indent(doc)
    ET.ElementTree(doc).write(path, encoding="utf-8", xml_declaration=True)


def geometry_check(spec):
    errors, warnings = [], []
    if spec.get("kind")=="teaser" and spec.get("concept",{}).get("kind")=="custom":
        ce,cw=geometry_check({**spec["concept"],"kind":"method"})
        return ["Concept: "+e for e in ce],["Concept: "+w for w in cw]
    if spec.get("kind") not in ("method", "benchmark"): return errors,warnings
    nodes = spec.get("nodes", [])
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)): errors.append("Node IDs must be unique")
    for n in nodes:
        if any(not isinstance(n[k], (int,float)) or not math.isfinite(n[k]) for k in ("x","y","w","h")):
            errors.append(f"Non-numeric geometry: {n['id']}"); continue
        if n["w"] <= 0 or n["h"] <= 0 or n["x"] < 0 or n["y"] < 0 or n["x"]+n["w"] > 1.00001 or n["y"]+n["h"] > 1.00001:
            errors.append(f"Node outside normalized canvas: {n['id']}")
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            if min(a["x"]+a["w"],b["x"]+b["w"])-max(a["x"],b["x"]) > .002 and min(a["y"]+a["h"],b["y"]+b["h"])-max(a["y"],b["y"]) > .002:
                errors.append(f"Overlapping nodes: {a['id']} / {b['id']}")
    node_map={n["id"]:n for n in nodes}
    for e in spec.get("edges", []):
        if e["source"] not in ids or e["target"] not in ids:
            errors.append(f"Unknown edge endpoint: {e}")
        for port_key in ("source_port","target_port"):
            port=e.get(port_key,"right" if port_key=="source_port" else "left")
            if isinstance(port,str):
                if port not in PORTS: errors.append(f"Unknown port {port!r}")
            elif not isinstance(port,(list,tuple)) or len(port)!=2 or any(not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 or v>1 for v in port):
                errors.append("Node ports must be named sides or normalized [u,v]")
        for pt in e.get("via", []):
            if len(pt) != 2 or any(not math.isfinite(v) or v<0 or v>1 for v in pt): errors.append("Edge waypoint outside normalized canvas")
    if not errors:
        def crosses(a,b,n):
            # Liang-Barsky clipping against the strict interior of an unrelated node.
            x0,x1=n["x"]+.002,n["x"]+n["w"]-.002
            y0,y1=n["y"]+.002,n["y"]+n["h"]-.002
            dx,dy=b[0]-a[0],b[1]-a[1]
            t0,t1=0.,1.
            for pp,qq in ((-dx,a[0]-x0),(dx,x1-a[0]),(-dy,a[1]-y0),(dy,y1-a[1])):
                if abs(pp)<1e-12:
                    if qq<0: return False
                else:
                    ratio=qq/pp
                    if pp<0: t0=max(t0,ratio)
                    else: t1=min(t1,ratio)
                    if t0>t1: return False
            return t1-t0>1e-6
        for e in spec.get("edges",[]):
            pts=edge_points(e,node_map)
            for n in nodes:
                if n["id"] in (e["source"],e["target"]): continue
                if any(crosses(a,b,n) for a,b in zip(pts,pts[1:])):
                    warnings.append(f"Edge {e['source']} -> {e['target']} crosses node {n['id']}")
    return errors,warnings


def text_geometry_check(fig, spec, ax):
    """Catch node labels too large for their boxes using final renderer bounds."""
    if spec.get("kind") not in ("method","benchmark","custom"): return []
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    nodes = {n["id"]:n for n in spec["nodes"]}
    warnings = []
    for artist in ax.texts:
        gid = artist.get_gid()
        if gid and gid.startswith(("group-label:", "edge-label:", "annotation:")):
            bb = artist.get_window_extent(renderer)
            for n in nodes.values():
                lo = ax.transData.transform((n["x"], n["y"]))
                hi = ax.transData.transform((n["x"]+n["w"], n["y"]+n["h"]))
                dx = min(bb.x1, hi[0]) - max(bb.x0, lo[0])
                dy = min(bb.y1, hi[1]) - max(bb.y0, lo[1])
                if dx > 1 and dy > 1:
                    warnings.append(f"Diagram label intersects node {n['id']}: {artist.get_text()!r}")
        if not gid or not gid.startswith("node-"): continue
        n = nodes[gid.split(":",1)[1]]
        lo = ax.transData.transform((n["x"],n["y"]))
        hi = ax.transData.transform((n["x"]+n["w"],n["y"]+n["h"]))
        bb = artist.get_window_extent(renderer)
        if bb.x0 < lo[0]+2 or bb.x1 > hi[0]-2 or bb.y0 < lo[1]+1 or bb.y1 > hi[1]-1:
            warnings.append(f"Text may overflow node {n['id']}: {artist.get_text()!r}")
    return warnings


def render(spec, output, formats=("svg","pdf","png"), theme_path=None):
    from validate_evidence import validate_spec
    validation = validate_spec(spec)
    if not validation["valid"]:
        raise ValueError("Evidence validation failed: " + "; ".join(e["message"] for e in validation["errors"]))
    spec = dict(spec)
    spec["_computed_claims"] = validation.get("computed_claims", [])
    theme = load_theme(theme_path, spec.get("theme"))
    apply_theme(theme)
    errors,warnings = geometry_check(spec)
    if errors: raise ValueError("; ".join(errors))
    f = spec.get("figure", {})
    kind = spec["kind"]
    width,height = f.get("width_in",7.2), f.get("height_in",3.15 if kind=="teaser" else 3.6)
    if width < 3 or height < 1.5: raise ValueError("Canvas too small for these starter renderers")
    fig = plt.figure(figsize=(width,height), layout=None)
    title = f.get("title")
    subtitle = f.get("subtitle")
    if title: fig.text(.035,.945,title,fontsize=theme["title_size"],weight="bold",va="top")
    if subtitle: fig.text(.035,.858,subtitle,fontsize=theme["small_size"],color=theme["muted"],va="top")
    data_status = spec.get("provenance",{}).get("data_status")
    if data_status in ("synthetic","mixed"):
        watermark_size = f.get("watermark_font_pt", max(6.5, f.get("min_font_pt") or 0))
        fig.text(.965,.02,"SYNTHETIC DATA · DESIGN DEMO" if data_status=="synthetic" else "MIXED REPORTED / SYNTHETIC DATA",
                 fontsize=watermark_size,color=theme["warm"],ha="right",va="bottom")
    if f.get("note"):
        fig.text(.035,.025,f["note"],fontsize=theme["small_size"],color=theme["muted"],va="bottom")
    if kind == "teaser":
        charts = spec.get("charts", [])
        if not 1 <= len(charts) <= 2: raise ValueError("Teaser starter supports one or two charts")
        share = f.get("concept_fraction", .35)
        if not .25 <= share <= .45: raise ValueError("concept_fraction must be .25–.45; use .30–.40 by default")
        left=.04; right=.035; gap=.095 if len(charts)==1 else .09
        top=.74 if subtitle else .78
        bottom=.30 if f.get("shared_legend") else (.23 if f.get("note") else .21)
        concept_ax=fig.add_axes([left,bottom,share-.045,top-bottom])
        draw_concept(concept_ax,spec["concept"],theme)
        if spec["concept"].get("kind")=="custom":
            warnings += ["Concept: "+w for w in text_geometry_check(fig,spec["concept"],concept_ax)]
        x0=left+share+(.105 if charts[0].get("ylabel") else .065)
        chart_w=(1-right-x0-(len(charts)-1)*gap)/len(charts)
        chart_axes=[]
        for i,c in enumerate(charts):
            ax=fig.add_axes([x0+i*(chart_w+gap),bottom,chart_w,top-bottom])
            chart_axes.append(ax)
            draw_chart(ax,{**c, "legend":False} if f.get("shared_legend") else c,spec,theme,i)
        # Reserve each evidence panel's own label gutter. Tick labels are measured
        # in rendered pixels, so long method names cannot leak into the concept.
        fig.canvas.draw()
        rr=fig.canvas.get_renderer()
        evidence_left=left+share+.01
        evidence_width=1-right-evidence_left
        for i,ax in enumerate(chart_axes):
            panel_left=evidence_left+i*evidence_width/len(charts)
            pos=ax.get_position()
            ytexts=[ax.yaxis.label,*ax.get_yticklabels()]
            visible=[t.get_window_extent(rr).x0 for t in ytexts if t.get_visible() and t.get_text()]
            if visible:
                current_left=min(visible)/fig.bbox.width
                shift=max(0,panel_left-current_left)
                if pos.width-shift < .12:
                    raise ValueError("Chart labels leave too little data area; shorten labels, wrap names, or use a larger layout")
                ax.set_position([pos.x0+shift,pos.y0,pos.width-shift,pos.height])
        if f.get("shared_legend"):
            legend_items = {}
            for chart_ax in chart_axes:
                handles, labels = chart_ax.get_legend_handles_labels()
                for handle, label in zip(handles, labels):
                    legend_items.setdefault(label, handle)
            # Reserve every chart's series and wrap columns to the available page
            # width. Never omit an entry or shrink its type to force a fit.
            for ncols in range(max(1, len(legend_items)), 0, -1):
                legend = fig.legend(list(legend_items.values()), list(legend_items),
                                    loc="lower center", bbox_to_anchor=(.5,.07),
                                    ncol=ncols, handlelength=1.5, columnspacing=1.6)
                fig.canvas.draw()
                if legend.get_window_extent(fig.canvas.get_renderer()).width <= fig.bbox.width*.93 or ncols == 1:
                    break
                legend.remove()
        fig.add_artist(plt.Line2D([left+share-.025]*2,[bottom-.03,top+.06],transform=fig.transFigure,color=theme["grid"],lw=.7))
    elif kind in ("method", "benchmark"):
        top=.79 if subtitle else .83
        ax=fig.add_axes([.035,.11,.93,top-.11])
        draw_method_contents(ax,spec,theme)
        warnings += text_geometry_check(fig,spec,ax)
    else: raise ValueError(f"Unknown figure kind: {kind}")
    layout_issues = audit_figure(fig, min_font_pt=f.get("min_font_pt"),
                                display_width_inches=f.get("display_width_inches"),
                                check_data_occlusion=f.get("check_data_occlusion", False))
    warnings += [issue_message(issue) for issue in layout_issues]
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    products=[]
    for fmt in formats:
        if fmt not in ("svg","pdf","png"): raise ValueError(f"Unsupported output {fmt}")
        path=output.with_suffix("."+fmt)
        metadata={"Creator":"paper-figure-creation"} if fmt in ("pdf","svg") else None
        if fmt=="svg": metadata["Date"]=None
        if fmt=="pdf": metadata.update({"CreationDate":None,"ModDate":None})
        fig.savefig(path,dpi=theme["dpi"],metadata=metadata)
        products.append(str(path))
    if kind in ("method", "benchmark"):
        path=output.with_suffix(".drawio"); drawio_export(spec,path,theme); products.append(str(path))
    plt.close(fig)
    report={"figure_kind":kind,"dimensions_in":[width,height],"font_size_pt":theme["font_size"],
            "products":products,"errors":errors,"warnings":warnings,"layout_issues":layout_issues,
            "data_occlusion_check_requested":f.get("check_data_occlusion", False),
            "verification_scope":"Chart point visibility and log domains; method/benchmark/custom-concept node bounds, edge-node intersections, node text containment; rendered text collisions, page/clip-box text overflow, legend bounds and optional minimum font size. Optional legend/data ink checks cover supported 2D artists only. Rotated text uses conservative bounding boxes; custom clip paths and unsupported geometry require visual review. Benchmark eligibility is a declared source-backed contract, not verified scientific truth. Human visual and scientific review remain required."}
    output.with_suffix(".qa.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("spec",type=Path)
    p.add_argument("--output",required=True,type=Path,help="Output path stem (extension optional)")
    p.add_argument("--formats",default="svg,pdf,png")
    p.add_argument("--theme",type=Path)
    p.add_argument("--strict-layout",action="store_true",help="Return failure if bounded geometry checks warn")
    args=p.parse_args()
    try:
        spec=json.loads(args.spec.read_text())
        if spec.get("version")!=1: raise ValueError("Expected figure spec version 1")
        report=render(spec,args.output,args.formats.split(","),args.theme)
        print(json.dumps(report,indent=2))
        if args.strict_layout and report["warnings"]: return 2
    except (ValueError,KeyError,TypeError) as exc:
        print(f"Render failed: {exc}",file=sys.stderr); return 2
    return 0

if __name__=="__main__":
    raise SystemExit(main())
