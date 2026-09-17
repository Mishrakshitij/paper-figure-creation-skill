#!/usr/bin/env python3
"""Original vector art direction for a sourced WebArena setup.

No episode is executed; the UI, ID 42 and illustrated click are schematic.
Requires matplotlib, Pillow and PyMuPDF. SVG text is editable; PDF has TrueType.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

W, H = 7, 4.95
INK = "#182E3B"
MUTED = "#536978"
BLUE = "#276589"
TEAL = "#137D73"
PALE = "#EDF5F6"
RULE = "#B7C8CD"
GOLD = "#886024"


def text(ax, x, y, s, size=9, color=INK, weight="normal", **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   va="center", **kw)


def rect(ax, x, y, w, h, fill="white", edge=RULE, radius=.05, lw=.8, **kw):
    p = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=edge, linewidth=lw, **kw)
    ax.add_patch(p)
    return p


def arrow(ax, points, color=BLUE, width=1.15, zorder=5):
    for a, b in zip(points[:-2], points[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=width,
                solid_capstyle="round", zorder=zorder)
    p = FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>",
                        color=color, lw=width, mutation_scale=9,
                        zorder=zorder, shrinkA=0, shrinkB=0)
    ax.add_patch(p)


def shadow(ax, x, y, w, h):
    # Tiny, local depth cue: the foreground state is a second browser snapshot.
    # No scientific meaning is assigned to z-depth.
    rect(ax, x+.025, y-.035, w, h, fill="#E3EBEE", edge="none", zorder=2)


def chrome(ax, x, y, w, h, color=BLUE):
    shadow(ax, x, y, w, h)
    rect(ax, x, y, w, h, edge=color, lw=1, zorder=3)
    rect(ax, x+.007, y+h-.285, w-.014, .278, fill=PALE,
         edge="none", radius=.04, zorder=4)
    for i in range(3):
        ax.add_patch(Circle((x+.12+i*.075, y+h-.14), .021,
                            facecolor=RULE, edgecolor="none", zorder=5))
    text(ax, x+.40, y+h-.14, "Forum  /f/nyc", 8.7, MUTED, zorder=5)
    ax.plot([x+.01, x+w-.01], [y+h-.286]*2, color=RULE, lw=.6, zorder=5)


def make_figure(out: Path):
    fig = plt.figure(figsize=(W, H), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(0, H)); ax.axis("off")

    text(ax, .22, 4.71, "WebArena", 14, weight="bold")
    text(ax, 6.78, 4.71, "Tasks on self-hosted websites", 9.5, MUTED, ha="right")
    text(ax, .22, 4.37, "Goal", 9.1, BLUE, weight="bold")
    text(ax, .63, 4.37, "Ask a suitable forum whether a car is necessary in New York City.", 9.1)

    # The larger source page establishes the task object. The smaller foreground
    # page keeps the same URL and question so a reader can identify what changed.
    x, y, w, h = 2.54, 2.46, 4.12, 1.69
    chrome(ax, x, y, w, h)
    text(ax, x+.19, 3.64, "1  Write a post", 10.4, weight="bold", zorder=5)
    text(ax, x+.19, 3.36, "Title", 8.6, MUTED, zorder=5)
    rect(ax, x+.17, 2.99, w-.34, .27, fill="#F5F8F9", radius=.025, zorder=4)
    text(ax, x+.29, 3.125, "is car necessary in NYC", 10.0, zorder=5)
    # Sparse semantic content: no decorative fake menu, account or test scores.
    text(ax, x+.19, 2.73, "Text entered", 8.7, MUTED, zorder=5)
    rect(ax, x+w-1.22, 2.59, 1.04, .29, fill=BLUE, edge=BLUE, radius=.04, zorder=5)
    text(ax, x+w-.70, 2.735, "[42] Post", 9.3, "white", "bold", ha="center", zorder=6)
    ax.add_patch(Polygon([(6.51,2.94),(6.43,2.70),(6.62,2.77)],
                        facecolor="white",edgecolor=INK,lw=.8,zorder=7))

    # The replaceable tested system is deliberately subordinate to its task.
    rect(ax, .22, 2.80, 1.47, .70, fill=PALE, edge=BLUE, radius=.075, zorder=3)
    text(ax, .955, 3.29, "Web agent", 10, BLUE, "bold", ha="center", zorder=4)
    text(ax, .955, 3.01, "click [42]", 9.2, BLUE, ha="center",
         family="DejaVu Sans Mono", zorder=4)
    arrow(ax, [(2.51,3.30),(1.72,3.30)])
    text(ax, 2.115, 3.48, "observe", 8.5, BLUE, ha="center")
    arrow(ax, [(1.72,3.01),(2.51,3.01)])
    text(ax, 2.115, 2.82, "act", 8.5, BLUE, ha="center")
    text(ax, .22, 2.60, "[42] accessibility target", 8.5, MUTED)
    text(ax, .22, 2.38, "After navigation + typing", 8.5, MUTED)

    # Overlay only the empty lower margin of the earlier page, never text/arrows.
    x2, y2, w2, h2 = 3.59, 1.15, 3.18, 1.39
    chrome(ax, x2, y2, w2, h2, color=TEAL)
    text(ax, x2+.17, 2.05, "2  Published post", 10.2, TEAL, "bold", zorder=5)
    ax.add_patch(Polygon([(x2+.22,1.81),(x2+.16,1.72),(x2+.28,1.72)],
                        facecolor=RULE, edgecolor="none", zorder=5))
    text(ax, x2+.38, 1.75, "is car necessary in NYC", 9.1, weight="bold", zorder=5)
    ax.plot([x2+.39,x2+w2-.17],[1.48]*2,color=RULE,lw=.6,zorder=5)
    text(ax, x2+.39, 1.34, "Same question; changed website state", 8.5, MUTED, zorder=5)
    # A direct short edge attaches the action target to its illustrative effect.
    arrow(ax, [(6.56,2.71),(6.88,2.71),(6.88,2.18),(6.79,2.18)],
          color=TEAL, width=1.1, zorder=6)
    # This is observation feedback, never a learning reward from the evaluator.
    arrow(ax, [(3.56,1.86),(.105,1.86),(.105,3.10),(.20,3.10)], color=TEAL)
    text(ax, 2.21, 2.025, "next observation", 9, TEAL, ha="center")

    # Evaluation remains a different lane. The only edge arriving here comes
    # from the completed website state; reference checks do not feed the agent.
    text(ax, .22, 1.40, "At completion", 9.2, GOLD, "bold")
    text(ax, .22, 1.19, "Private reference checks", 8.8, GOLD)
    text(ax, 4.43, 1.025, "final URL + post DOM", 8.5, GOLD)
    arrow(ax, [(4.23,1.135),(4.23,.965)], color=GOLD, width=.9)
    rect(ax, .22, .38, 4.40, .57, fill="#FCF6EA", edge="#CFBA92", radius=.04)
    text(ax, .37, .765, "URL contains /f/nyc", 9, GOLD)
    text(ax, .37, .55, "Post DOM contains the requested question", 9, GOLD)
    arrow(ax, [(4.65,.66),(5.00,.66)], color=GOLD)
    text(ax, 5.17, .77, "Success", 10.2, GOLD, "bold")
    text(ax, 5.17, .54, "if both checks pass", 8.8, GOLD)
    text(ax, .22, .16, "Task 601 · v0.2.0 · schematic UI, target ID and step; no agent run.", 8.5, MUTED)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    text_bounds = []
    outside = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text():
            continue
        b = t.get_window_extent(renderer)
        text_bounds.append({"text":t.get_text(), "font_pt":t.get_fontsize(),
                            "bbox_px":[round(z,2) for z in b.bounds]})
        if b.x0 < -.2 or b.y0 < -.2 or b.x1 > fig.bbox.x1+.2 or b.y1 > fig.bbox.y1+.2:
            outside.append(t.get_text())
    if outside:
        raise ValueError(f"Text outside page: {outside}")
    for extension in ("svg", "pdf", "png"):
        fig.savefig(out/f"figure.{extension}", dpi=220, facecolor="white")
    plt.close(fig)
    # A PDF raster is the print proof: this checks the exported PDF rather than
    # merely exporting another Matplotlib PNG from the same canvas.
    import fitz
    from PIL import Image
    doc = fitz.open(out/"figure.pdf")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(110/72,110/72), alpha=False)
    pix.save(out/"print-proof.png")
    Image.open(out/"print-proof.png").convert("L").save(out/"grayscale-proof.png",optimize=True)
    report = {
        "width_in":W,"height_in":H,"main_png_dpi":220,"pdf_proof_dpi":110,
        "minimum_font_pt":min(x["font_pt"] for x in text_bounds),
        "text_outside_canvas":outside,
        "no_agent_run":True,"all_labels_vector_text":True,
        "notes":["UI, target ID and step are illustrative; source task checks are unchanged.",
                 "Geometry checks only page bounds; visual inspection is required.",
                 "No target manuscript provided; seven-inch placement only."],
        "text_bounds":text_bounds,
    }
    (out/"export-check.json").write_text(json.dumps(report,indent=2)+"\n")


def thumbnails(out: Path):
    fig, axs = plt.subplots(1,3,figsize=(10.5,2.25),facecolor="white")
    for ax in axs:
        ax.set(xlim=(0,3.4),ylim=(0,2.15)); ax.axis("off")
    names = ["A · Foreground state change", "B · Horizontal browser strip", "C · Role lanes"]
    for ax, name in zip(axs,names): text(ax,.05,2.04,name,8.6,weight="bold")
    a=axs[0]
    rect(a,.06,1.00,.7,.4,fill=PALE); text(a,.41,1.20,"Agent",7.3,ha="center")
    rect(a,1.12,.92,1.96,.82); text(a,1.30,1.47,"Compose",8)
    rect(a,1.75,.44,1.51,.62,edge=TEAL); text(a,1.91,.72,"Published",8,TEAL)
    arrow(a,[(.79,1.13),(1.09,1.13)])
    arrow(a,[(1.70,.69),(.41,.69),(.41,.97)],color=TEAL,width=.8)
    text(a,.07,.18,"Private URL + DOM checks → success",7.5,GOLD)
    a=axs[1]
    for x, width, name in [(.05,1.12,"Before"),(1.39,.56,"Agent"),(2.19,1.13,"After")]:
        rect(a,x,.83,width,.7,fill=PALE if name=="Agent" else "white")
        text(a,x+width/2,1.18,name,7.8,ha="center")
    arrow(a,[(1.2,1.18),(1.36,1.18)],width=.7);arrow(a,[(1.98,1.18),(2.16,1.18)],width=.7)
    text(a,.08,.36,"Checks → success",8,GOLD)
    text(a,.08,.10,"Even weighting reduces the visual focus",7.1,MUTED)
    a=axs[2]
    for y, name in [(1.46,"Task and observations"),(.95,"Agent ↔ website"),(.44,"Private evaluation")]:
        rect(a,.08,y,3.18,.35,fill=PALE);text(a,.20,y+.175,name,8)
    text(a,.08,.10,"Clear roles; little visible state change",7.1,MUTED)
    fig.subplots_adjust(left=.015,right=.985,top=.98,bottom=.02,wspace=.11)
    for ext in ("svg","png"):fig.savefig(out/f"composition-thumbnails.{ext}",dpi=110)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parent)
    p.add_argument("--thumbnails-only",action="store_true")
    args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    matplotlib.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none",
                               "pdf.fonttype":42,"ps.fonttype":42})
    thumbnails(args.output_dir)
    if not args.thumbnails_only:make_figure(args.output_dir)

if __name__=="__main__":main()
