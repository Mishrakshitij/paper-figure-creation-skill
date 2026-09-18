"""Renderer-based layout checks reusable by custom Matplotlib paper figures.

Checks report geometry, not scientific correctness or aesthetic quality. No
artist is cropped, removed, moved, or shrunk to make a check pass.
"""
from __future__ import annotations

import math
import re

from matplotlib.legend import Legend
from matplotlib.text import Text


def wrap_text_artist(artist, max_width_px, renderer):
    """Wrap at word boundaries using the actual font; keep equations unbroken.

    Existing hard line breaks remain. An indivisible overlong word is retained
    for the bounds checker to report, never truncated or silently reduced.
    """
    if not math.isfinite(max_width_px) or max_width_px <= 0:
        raise ValueError("text width must be finite and positive")
    original = artist.get_text()
    lines = []
    for paragraph in original.split("\n"):
        words = re.findall(r"\$[^$]*\$|\S+", paragraph)
        current = ""
        for word in words:
            candidate = (current + " " + word).strip()
            artist.set_text(candidate)
            if current and artist.get_window_extent(renderer).width > max_width_px:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    artist.set_text("\n".join(lines))
    return artist.get_window_extent(renderer).width <= max_width_px


def _drawn_text(fig):
    excluded = set()
    for ax in fig.axes:
        if not ax.get_visible():
            excluded.update(id(t) for t in ax.findobj(match=Text))
        for axis in (ax.xaxis, ax.yaxis):
            if not ax.axison or not axis.get_visible():
                excluded.update(id(t) for t in axis.findobj(match=Text))
                continue
            lo, hi = sorted(axis.get_view_interval())
            tol = (hi - lo) * 1e-10
            for tick in [*axis.get_major_ticks(), *axis.get_minor_ticks()]:
                location = tick.get_loc()
                if not tick.get_visible() or not math.isfinite(location) or not lo-tol <= location <= hi+tol:
                    excluded.update((id(tick.label1), id(tick.label2)))
    return [t for t in fig.findobj(match=Text)
            if id(t) not in excluded and t.get_visible() and t.get_text().strip()]


def audit_figure(fig, *, min_font_pt=None, tolerance_pt=.6, display_width_inches=None):
    """Inspect final pixel extents at the figure's declared physical size.

    Text overlaps use actual rendered bounding boxes, including rotated labels.
    This is conservative for diagonal labels and shaped glyphs; review flagged
    intersections visually. ``min_font_pt`` is an explicit project preference.
    ``display_width_inches`` optionally checks the effective typography after
    manuscript inclusion; it does not resize the figure or alter data geometry.
    """
    scale = 1.0
    if display_width_inches is not None:
        if not math.isfinite(display_width_inches) or display_width_inches <= 0:
            raise ValueError("display width must be finite and positive")
        scale = display_width_inches / fig.get_figwidth()
    if min_font_pt is not None and (not math.isfinite(min_font_pt) or min_font_pt <= 0):
        raise ValueError("minimum font size must be finite and positive")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    tolerance = tolerance_pt * fig.dpi / 72
    items, issues = [], []

    def add(kind, text, **extra):
        issues.append({"kind": kind, "text": text, **extra})

    for artist in _drawn_text(fig):
        bounds = artist.get_window_extent(renderer)
        if bounds.width <= 0 or bounds.height <= 0:
            continue
        label = artist.get_text()
        identity = artist.get_gid()
        if (bounds.x0 < -tolerance or bounds.y0 < -tolerance or
                bounds.x1 > fig.bbox.width+tolerance or bounds.y1 > fig.bbox.height+tolerance):
            add("page_overflow", label, artist_id=identity)
        # Clip-on must never exempt a label from the audit: it can hide glyphs.
        if artist.get_clip_on():
            clip = artist.get_clip_box()
            if clip is not None and (bounds.x0 < clip.x0-tolerance or bounds.x1 > clip.x1+tolerance or
                                     bounds.y0 < clip.y0-tolerance or bounds.y1 > clip.y1+tolerance):
                add("clipped_text", label, artist_id=identity)
            path = artist.get_clip_path()
            if path is not None:
                add("custom_clip_review", label, artist_id=identity)
        effective_font = artist.get_fontsize() * scale
        if min_font_pt is not None and effective_font < min_font_pt:
            add("small_text", label, font_size_pt=artist.get_fontsize(),
                effective_font_size_pt=effective_font, minimum_pt=min_font_pt,
                display_width_inches=display_width_inches)
        items.append((artist, bounds))
    for index, (a, box_a) in enumerate(items):
        for b, box_b in items[index+1:]:
            dx = min(box_a.x1, box_b.x1) - max(box_a.x0, box_b.x0)
            dy = min(box_a.y1, box_b.y1) - max(box_a.y0, box_b.y0)
            if dx > tolerance and dy > tolerance:
                add("text_overlap", a.get_text(), other_text=b.get_text(),
                    artist_id=a.get_gid(), other_artist_id=b.get_gid())
    for legend in fig.findobj(match=Legend):
        if not legend.get_visible():
            continue
        bounds = legend.get_window_extent(renderer)
        if (bounds.x0 < -tolerance or bounds.y0 < -tolerance or
                bounds.x1 > fig.bbox.width+tolerance or bounds.y1 > fig.bbox.height+tolerance):
            add("legend_overflow", ", ".join(t.get_text() for t in legend.get_texts()))
    return issues


def issue_message(issue):
    prefix = {"page_overflow": "Text leaves the page", "clipped_text": "Text is clipped",
              "custom_clip_review": "Custom text clip requires visual review",
              "small_text": "Text below declared minimum font size",
              "text_overlap": "Text overlaps", "legend_overflow": "Legend leaves the page"}[issue["kind"]]
    return prefix + ": " + repr(issue["text"]) + (
        " / " + repr(issue["other_text"]) if "other_text" in issue else "")
