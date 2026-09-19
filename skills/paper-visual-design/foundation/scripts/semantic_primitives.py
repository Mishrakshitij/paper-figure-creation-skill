#!/usr/bin/env python3
"""Small, optional semantic objects for bespoke scientific diagrams.

Geometry is in inches on an unscaled axis made by ``inch_canvas``; font sizes
are points. Objects return their bounding rectangle for deliberate routing.
The caller chooses the actual content, evidence, composition, and meaning.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath
import numpy as np

INK = "#253448"
MUTED = "#647286"
LINE = "#BEC9D4"
TEAL = "#087F8C"
PALE_TEAL = "#E7F4F3"
PURPLE = "#7756A0"
PALE_PURPLE = "#F0EBF7"
ORANGE = "#C66D2B"
PALE_ORANGE = "#FFF0E1"


@dataclass(frozen=True)
class Bounds:
    """Inch rectangle; named ports keep connecting edges off object interiors."""
    x: float
    y: float
    w: float
    h: float

    def port(self, side: str) -> tuple[float, float]:
        ports = {"left": (self.x, self.y + self.h / 2),
                 "right": (self.x + self.w, self.y + self.h / 2),
                 "top": (self.x + self.w / 2, self.y + self.h),
                 "bottom": (self.x + self.w / 2, self.y)}
        if side not in ports:
            raise ValueError(f"Unknown port {side!r}; choose left/right/top/bottom")
        return ports[side]


def _bounds(x: float, y: float, w: float, h: float) -> Bounds:
    if not np.all(np.isfinite([x, y, w, h])) or w <= 0 or h <= 0:
        raise ValueError("Coordinates must be finite, with positive width and height")
    return Bounds(float(x), float(y), float(w), float(h))


def inch_canvas(width: float, height: float):
    """Create a full-bleed axis with one data unit = one physical inch.

    Preserve limits, equal aspect, and the full figure extent when exporting.
    Do not call tight_layout or savefig(bbox_inches='tight'): those change the
    requested physical page dimensions. The axis is deliberately undecorated.
    """
    _bounds(0, 0, width, height)
    mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                         "text.color": INK, "svg.fonttype": "none",
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "svg.hashsalt": "semantic-primitives-v2"})
    fig = plt.figure(figsize=(width, height), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1], xlim=(0, width), ylim=(0, height))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _text(ax, x, y, text, *, size=8, color=INK, weight="normal", **kwargs):
    return ax.text(x, y, str(text), fontsize=size, color=color, weight=weight,
                   zorder=5, **kwargs)


def _card(ax, x, y, w, h, *, face="white", edge=LINE, radius=0.06, linewidth=0.9):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=face, edgecolor=edge, linewidth=linewidth,
                         zorder=2)
    ax.add_patch(box)
    return box


def document(ax, x, y, w, h, *, title: str, lines: Sequence[str],
             face="white", edge=LINE, accent=TEAL, ink=INK,
             fontsize=8, title_size=8.5, fold=0.17) -> Bounds:
    """A folded document with caller-supplied title and readable short content.

    No placeholder strokes stand in for scientific content. Line breaks are
    explicit; leave enough width and height for the supplied text at print size.
    """
    b = _bounds(x, y, w, h)
    if not 0 < fold < min(w, h) / 2:
        raise ValueError("fold must be positive and less than half the shorter side")
    line_height = fontsize * 1.30 / 72
    if 0.42 + len(lines) * line_height > h:
        raise ValueError("Document height is too small for its content and font size")
    points = [(x, y), (x+w, y), (x+w, y+h-fold),
              (x+w-fold, y+h), (x, y+h)]
    ax.add_patch(Polygon(points, closed=True, facecolor=face, edgecolor=edge,
                         linewidth=0.9, zorder=2))
    ax.add_patch(Polygon([(x+w-fold, y+h), (x+w-fold, y+h-fold),
                          (x+w, y+h-fold)], closed=True, facecolor="#E4EBF1",
                         edgecolor=edge, linewidth=0.7, zorder=3))
    ax.add_patch(Rectangle((x+0.11, y+h-0.27), 0.035, 0.13,
                           facecolor=accent, linewidth=0, zorder=3))
    _text(ax, x+0.21, y+h-0.205, title, size=title_size, color=ink,
          weight="bold", va="center")
    for i, line in enumerate(lines):
        _text(ax, x+0.13, y+h-0.41-i*line_height, line,
              size=fontsize, color=ink, va="top")
    return b


def token_strip(ax, x, y, tokens: Sequence[str], *, changed: Iterable[int] = (),
                widths: Sequence[float] | None = None, height=0.28,
                gap=0.025, fontsize=7.7, face="#F2F5F8", edge=LINE,
                changed_face=PALE_ORANGE, changed_edge=ORANGE,
                ink=INK) -> Bounds:
    """Explicit tokens, with a second encoding (underline) for changed tokens.

    Defaults estimate widths; supply widths when matching a particular token
    vocabulary or phrase. ``changed`` indexes are validated, never inferred.
    """
    if not tokens:
        raise ValueError("Provide at least one token")
    selected = set(changed)
    if any(not isinstance(i, int) or i < 0 or i >= len(tokens) for i in selected):
        raise ValueError("changed must contain valid token indices")
    if widths is None:
        widths = [max(0.27, len(str(t))*fontsize*0.56/72+0.14) for t in tokens]
    if len(widths) != len(tokens):
        raise ValueError("widths must have one value per token")
    if gap < 0 or any(v <= 0 for v in widths):
        raise ValueError("Widths must be positive and gap nonnegative")
    b = _bounds(x, y, sum(widths)+gap*(len(tokens)-1), height)
    xpos = x
    for i, (token, width) in enumerate(zip(tokens, widths)):
        is_changed = i in selected
        _card(ax, xpos, y, width, height,
              face=changed_face if is_changed else face,
              edge=changed_edge if is_changed else edge, radius=0.035,
              linewidth=1.0 if is_changed else 0.65)
        _text(ax, xpos+width/2, y+height/2+0.008, token, size=fontsize,
              ha="center", va="center", color=ink)
        if is_changed:
            ax.plot([xpos+0.065, xpos+width-0.065], [y+0.045, y+0.045],
                    color=changed_edge, lw=1.3, zorder=4)
        xpos += width + gap
    return b


def model_tile(ax, x, y, w, h, *, label: str, state: str,
               detail: str = "", face=PALE_TEAL, edge=TEAL,
               state_face="white", ink=INK, fontsize=8.5) -> Bounds:
    """Model identity and parameter state occupy separate, readable regions.

    State is a caller-supplied statement such as 'frozen θ₀' or 'trainable Δθ';
    the helper never chooses or infers what is trainable.
    """
    b = _bounds(x, y, w, h)
    if h < 0.65:
        raise ValueError("Model tile needs at least 0.65 inch for identity and state")
    _card(ax, x, y, w, h, face=face, edge=edge, linewidth=1.0)
    # Parameter chip is inside the tile, not an unsupported icon or a logo.
    chip_y = y+0.10
    _card(ax, x+0.09, chip_y, w-0.18, 0.27, face=state_face,
          edge=edge, radius=0.04, linewidth=0.65)
    _text(ax, x+w/2, chip_y+0.135, state, size=fontsize-0.4,
          color=edge, ha="center", va="center")
    _text(ax, x+w/2, y+h-0.20, label, size=fontsize, color=ink,
          weight="bold", ha="center", va="center")
    if detail:
        _text(ax, x+w/2, y+0.46, detail, size=fontsize-1,
              color=ink, ha="center", va="center")
    return b


def matrix(ax, x, y, w, h, values: Sequence[Sequence[float]], *,
           palette: Mapping[float, str] | None = None, cmap="Blues",
           vmin=None, vmax=None, labels=False, fontsize=7.2,
           edge="white", outline=LINE, linewidth=0.8) -> Bounds:
    """An actual cell array; shape and values must come from the caller.

    Use a complete ``palette`` for categorical grids. For numeric matrices,
    pass common vmin/vmax when colors must be comparable across matrices.
    No reshaping, imputation, normalization of the input values, or random data.
    """
    b = _bounds(x, y, w, h)
    data = np.asarray(values, dtype=float)
    if data.ndim != 2 or data.size == 0 or not np.isfinite(data).all():
        raise ValueError("Matrix values must form a finite, nonempty 2D array")
    if palette is not None:
        missing = set(data.flat) - set(palette)
        if missing:
            raise ValueError(f"Categorical palette omits values: {sorted(missing)}")
        color = lambda v: palette[v]
    else:
        low = float(data.min()) if vmin is None else float(vmin)
        high = float(data.max()) if vmax is None else float(vmax)
        if not np.isfinite([low, high]).all() or high < low:
            raise ValueError("Color limits must be finite and ordered")
        norm = mpl.colors.Normalize(low, high) if high > low else lambda v: 0.5
        color_map = mpl.colormaps.get_cmap(cmap)
        color = lambda v: color_map(norm(v))
    rows, cols = data.shape
    cw, ch = w/cols, h/rows
    for row in range(rows):
        for col in range(cols):
            value = data[row, col]
            ax.add_patch(Rectangle((x+col*cw, y+(rows-row-1)*ch), cw, ch,
                                   facecolor=color(value), edgecolor=edge,
                                   linewidth=linewidth, zorder=2))
            if labels:
                rgba = mpl.colors.to_rgba(color(value))
                luminance = sum(a*b for a, b in zip(rgba[:3], [0.2126, 0.7152, 0.0722]))
                _text(ax, x+(col+0.5)*cw, y+(rows-row-0.5)*ch,
                      f"{value:g}", size=fontsize, ha="center", va="center",
                      color="white" if luminance < 0.45 else INK)
    ax.add_patch(Rectangle((x, y), w, h, facecolor="none", edgecolor=outline,
                           linewidth=0.75, zorder=3))
    return b


def grid_pair(ax, x, y, before, after, *, cell=0.16, gap=0.45,
              palette: Mapping[float, str], labels=("Input", "Output"),
              arrow_label="", fontsize=8, ink=INK) -> Bounds:
    """Paired discrete examples with identical cell size and an explicit arrow.

    The input and output may have different shapes. Their actual dimensions
    remain visible; ``gap`` should accommodate an optional arrow label.
    """
    left, right = np.asarray(before), np.asarray(after)
    if left.ndim != 2 or right.ndim != 2 or cell <= 0 or gap <= 0:
        raise ValueError("Pair needs 2D arrays and positive cell size and gap")
    lh, lw = left.shape[0]*cell, left.shape[1]*cell
    rh, rw = right.shape[0]*cell, right.shape[1]*cell
    height = max(lh, rh)
    a = matrix(ax, x, y+(height-lh)/2, lw, lh, left, palette=palette)
    b = matrix(ax, x+lw+gap, y+(height-rh)/2, rw, rh, right, palette=palette)
    routed_arrow(ax, [(x+lw+0.05, y+height/2),
                      (x+lw+gap-0.05, y+height/2)], color=ink,
                 label=arrow_label, label_offset=(0, 0.11), fontsize=fontsize-1)
    for obj, label in ((a, labels[0]), (b, labels[1])):
        _text(ax, obj.x+obj.w/2, y+height+0.12, label, size=fontsize,
              color=ink, ha="center", va="bottom")
    return _bounds(x, y, lw+gap+rw, height+0.26)


def config_card(ax, x, y, w, h, entries: Sequence[tuple[str, str]], *,
                title="Adaptation settings", face="#F7F8FB", edge=LINE,
                key_color=PURPLE, ink=INK, fontsize=7.8) -> Bounds:
    """Named key/value settings with aligned columns, not illegible pseudo-code."""
    b = _bounds(x, y, w, h)
    if not entries:
        raise ValueError("Provide at least one configuration entry")
    row_h = max(0.19, fontsize*1.40/72)
    if 0.44+len(entries)*row_h > h:
        raise ValueError("Configuration height is too small for its rows")
    _card(ax, x, y, w, h, face=face, edge=edge)
    _text(ax, x+0.12, y+h-0.20, title, size=fontsize+0.5,
          weight="bold", color=ink, va="center")
    ax.plot([x+0.12, x+w-0.12], [y+h-0.35, y+h-0.35],
            color=edge, linewidth=0.65, zorder=3)
    for i, (key, value) in enumerate(entries):
        row_y = y+h-0.48-i*row_h
        _text(ax, x+0.13, row_y, key, size=fontsize, color=key_color,
              fontfamily="DejaVu Sans Mono", va="center")
        _text(ax, x+w-0.13, row_y, value, size=fontsize, color=ink,
              fontfamily="DejaVu Sans Mono", ha="right", va="center")
    return b


def reward_mark(ax, x, y, *, positive: bool, size=0.26,
                color=None, face=None, linewidth=1.8) -> Bounds:
    """Vector check/cross, with both shape and color encoding an actual outcome.

    This is a binary correctness mark, not a depiction of arbitrary reward.
    Use an explicitly labeled numeric annotation for non-binary rewards.
    """
    b = _bounds(x, y, size, size)
    color = color or (TEAL if positive else "#B65047")
    face = face or (PALE_TEAL if positive else "#FAECEA")
    _card(ax, x, y, size, size, face=face, edge="none", radius=size*0.20)
    if positive:
        vertices = [(x+0.23*size, y+0.51*size),
                    (x+0.43*size, y+0.29*size),
                    (x+0.79*size, y+0.73*size)]
        codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.LINETO]
    else:
        vertices = [(x+0.28*size, y+0.28*size), (x+0.72*size, y+0.72*size),
                    (x+0.28*size, y+0.72*size), (x+0.72*size, y+0.28*size)]
        codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.MOVETO, MplPath.LINETO]
    ax.add_patch(PathPatch(MplPath(vertices, codes), facecolor="none",
                           edgecolor=color, lw=linewidth, capstyle="round",
                           joinstyle="round", zorder=4))
    return b


def routed_arrow(ax, points: Sequence[tuple[float, float]], *, color=INK,
                 linewidth=1.0, head=8, dashed=False, label="",
                 label_at=None, label_offset=(0, 0.08), fontsize=7.5,
                 arrow=True):
    """Polyline through caller-selected waypoints; no automatic topology.

    Labels sit on an explicitly chosen coordinate or the longest segment's
    midpoint. Route first, then inspect the label at final print size. Arrow
    direction and line style must be explained wherever their meaning differs.
    """
    vertices = np.asarray(points, dtype=float)
    if vertices.ndim != 2 or vertices.shape[0] < 2 or vertices.shape[1] != 2 or not np.isfinite(vertices).all():
        raise ValueError("Arrow needs at least two finite (x,y) points")
    if np.any(np.linalg.norm(np.diff(vertices, axis=0), axis=1) == 0):
        raise ValueError("Consecutive arrow waypoints must differ")
    path = MplPath(vertices, [MplPath.MOVETO]+[MplPath.LINETO]*(len(vertices)-1))
    patch = FancyArrowPatch(path=path, arrowstyle="-|>" if arrow else "-",
                            mutation_scale=head, linewidth=linewidth,
                            linestyle=(0, (3, 2)) if dashed else "-",
                            color=color, capstyle="round", joinstyle="round",
                            zorder=1)
    ax.add_patch(patch)
    if label:
        if label_at is None:
            longest = np.argmax(np.linalg.norm(np.diff(vertices, axis=0), axis=1))
            label_at = (vertices[longest]+vertices[longest+1])/2
        _text(ax, label_at[0]+label_offset[0], label_at[1]+label_offset[1], label,
              size=fontsize, color=color, ha="center", va="center",
              bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6})
    return patch


def demo(output: Path):
    """Illustrative, non-evidential visual vocabulary and one small composition."""
    fig, ax = inch_canvas(7, 6.02)
    _text(ax, 0.22, 5.76, "Make the scientific objects visible", size=13, weight="bold")
    _text(ax, 0.22, 5.52, "Optional building blocks for a paper-specific composition", size=9, color=MUTED)

    # Panels only organize this reference sheet; actual paper layouts are free.
    panels = [(0.22, 3.80), (3.66, 3.80), (0.22, 2.11),
              (3.66, 2.11), (0.22, 0.42), (3.66, 0.42)]
    titles = ["A  Content carries the task", "B  Identity is separate from state",
              "C  Shape reveals the factorization", "D  Show a concrete transformation",
              "E  Expose the controllable settings", "F  Compose around the operation"]
    notes = ["Changed tokens use an underline as well as color.",
             "Only the adapter is trainable in this example.",
             "B is 4 × 2; A is 2 × 5. Product rank is at most 2.",
             "Schematic rule: recolor the blue cells orange.",
             "Illustrative settings; these are not recommendations.",
             "Here, the check denotes a correct test answer."]
    for (x, y), title, note in zip(panels, titles, notes):
        ax.plot([x, x+3.12], [y+1.43, y+1.43], color="#DFE5EB", lw=0.7)
        _text(ax, x, y+1.54, title, size=8.6, weight="bold", va="center")
        _text(ax, x, y+0.01, note, size=7.0, color=MUTED, va="bottom")

    document(ax, 0.26, 4.37, 2.72, 0.77, title="Task context",
             lines=["A blue object appears twice."], fontsize=8)
    token_strip(ax, 0.26, 4.00, ["blue", "→", "orange"], changed=[2],
                widths=[0.63, 0.32, 0.80])
    _text(ax, 2.16, 4.14, "self-edit", size=7.7, color=ORANGE, va="center")

    model_tile(ax, 3.71, 4.09, 1.36, 0.99, label="Base model",
               state="frozen θ₀", detail="existing knowledge", face="#F1F4F7", edge="#63778B")
    model_tile(ax, 5.35, 4.09, 1.36, 0.99, label="Adapter",
               state="trainable Δθ", detail="task update", face=PALE_PURPLE, edge=PURPLE)
    _text(ax, 5.21, 4.56, "+", size=15, ha="center", color=MUTED)

    pal = {0: "#EDF2F7", 1: "#BDDBE1", 2: "#70ABB9", 3: "#216C80"}
    matrix(ax, 0.39, 2.52, 0.45, 0.80, [[1, 2], [3, 1], [2, 3], [1, 1]], palette=pal)
    matrix(ax, 1.30, 2.72, 1.10, 0.40, [[1, 2, 3, 1, 2], [3, 1, 2, 3, 1]], palette=pal)
    _text(ax, 0.62, 3.43, "B", size=9, weight="bold", ha="center")
    _text(ax, 1.85, 3.26, "A", size=9, weight="bold", ha="center")
    _text(ax, 1.07, 2.92, "×", size=13, ha="center", va="center")
    _text(ax, 2.80, 3.03, "= ΔW", size=11, ha="center", va="center")
    _text(ax, 2.80, 2.74, "4 × 5", size=8, color=MUTED, ha="center")

    grids = {0: "#EFF2F5", 1: "#579CC6", 2: "#D8934E"}
    before = [[0, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
    after = [[0, 2, 0, 0], [0, 2, 0, 2], [0, 0, 0, 2], [0, 0, 0, 0]]
    grid_pair(ax, 4.00, 2.50, before, after, cell=0.19, gap=0.70,
              palette=grids, arrow_label="recolor")

    config_card(ax, 0.26, 0.72, 2.27, 1.10,
                [("learning_rate", "1e−4"), ("epochs", "2"), ("loss", "answer")],
                title="Generated configuration", fontsize=7.5)
    reward_mark(ax, 2.76, 1.40, positive=True)
    reward_mark(ax, 2.76, 0.95, positive=False)

    paper = document(ax, 3.72, 0.94, 0.93, 0.83, title="Test",
                     lines=["Blue", "→ ?"], fontsize=8, title_size=8)
    model = model_tile(ax, 5.10, 0.97, 1.17, 0.78, label="Adapted LM",
                       state="θ′", fontsize=8.1)
    reward = reward_mark(ax, 6.49, 1.24, positive=True, size=0.27)
    routed_arrow(ax, [(paper.x+paper.w+0.03, 1.37), (model.x-0.035, 1.37)],
                 label="ask", label_offset=(0, 0.16), fontsize=7.4)
    routed_arrow(ax, [(model.x+model.w+0.025, 1.37), (reward.x-0.035, 1.37)], head=7)
    _text(ax, 5.70, 0.68, 'Answer: “orange”', size=7.8, color=TEAL, ha="center")

    _text(ax, 0.22, 0.16, "ILLUSTRATIVE SCHEMATIC • No experimental results or paper-specific claims", size=7,
          color=MUTED)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(output.with_suffix(".png"), dpi=220)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Render the illustrative reference sheet")
    parser.add_argument("--output", type=Path, default=Path("semantic-primitives"),
                        help="Output stem (writes .svg and .png)")
    args = parser.parse_args()
    if args.demo:
        demo(args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
