"""Renderer-based layout checks reusable by custom Matplotlib paper figures.

Checks report geometry, not scientific correctness or aesthetic quality. No
artist is cropped, removed, moved, or shrunk to make a check pass.
"""
from __future__ import annotations

import math
import re

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.collections import LineCollection, PathCollection, PolyCollection
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.transforms import Bbox


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


def _legend_data_artists(fig, legend):
    """Yield supported data drawn before a legend in the same rendering layer."""
    supported = (Line2D, PathCollection, LineCollection, PolyCollection)
    if legend.axes is not None:
        axes = [legend.axes]
    else:
        # Figure legends draw relative to whole axes, regardless of the z-order
        # of the individual lines inside those axes.
        children = fig.get_children()
        if legend not in children:
            return
        legend_order = (legend.get_zorder(), children.index(legend))
        axes = [ax for ax in fig.axes if ax in children and
                (ax.get_zorder(), children.index(ax)) < legend_order]
    for ax in axes:
        if not ax.get_visible() or ax.get_animated() or ax.name != "rectilinear":
            continue
        children = ax.get_children()
        if legend.axes is not None:
            if legend not in children:
                continue
            legend_order = (legend.get_zorder(), children.index(legend))
        for index, artist in enumerate(children):
            if (not isinstance(artist, supported) or not artist.get_visible() or
                    artist.get_animated() or artist.get_agg_filter() is not None):
                continue
            if legend.axes is not None and (artist.get_zorder(), index) >= legend_order:
                continue
            yield artist


def _may_reach_legend(artist, bounds, renderer, dpi):
    """Cheap exclusions only; an unavailable collection extent is not empty."""
    if artist.get_clip_on():
        clip_box = artist.get_clip_box()
        if clip_box is not None and not clip_box.overlaps(bounds):
            return False
        clip_path = artist.get_clip_path()
        if clip_path is not None:
            clip_bounds = clip_path.get_fully_transformed_path().get_extents()
            if not clip_bounds.overlaps(bounds):
                return False
    # Effects can extend outside the nominal geometry. Their exact ink still
    # goes through the raster check, without the optional geometry prefilter.
    if artist.get_path_effects() or artist.get_sketch_params() is not None:
        return True
    extent = artist.get_window_extent(renderer)
    if np.isfinite(extent.extents).all():
        widths = ([artist.get_linewidth(), artist.get_markeredgewidth()]
                  if isinstance(artist, Line2D) else artist.get_linewidths())
        # Leave ample space for stroke joins, caps and antialiasing. This loose
        # bound never itself establishes an overlap.
        padding = 1 + 10 * max(widths, default=0) * dpi / 72
        return extent.padded(padding).overlaps(bounds)
    return True


def _legend_data_overlaps(fig, legend, renderer):
    """Intersect actual legend/data ink in a separate transparent Agg buffer."""
    if (not fig.get_visible() or legend.get_animated() or
            (legend.axes is not None and not legend.axes.get_visible())):
        return
    candidates = list(_legend_data_artists(fig, legend))
    if not candidates:
        return
    probe = RendererAgg(fig.bbox.width, fig.bbox.height, fig.dpi)
    legend.draw(probe)
    legend_ink = np.asarray(probe.buffer_rgba())[:, :, 3] > 0
    rows = np.flatnonzero(legend_ink.any(axis=1))
    columns = np.flatnonzero(legend_ink.any(axis=0))
    if not rows.size or not columns.size:
        return
    region = (slice(rows[0], rows[-1] + 1), slice(columns[0], columns[-1] + 1))
    # The rendered bounds include a frame shadow or other legend ink that may
    # extend beyond the nominal layout box. Agg rows run from top to bottom.
    height = legend_ink.shape[0]
    bounds = Bbox.from_extents(columns[0], height - rows[-1] - 1,
                               columns[-1] + 1, height - rows[0]).padded(1)
    legend_ink = legend_ink[region].copy()
    for artist in candidates:
        if not _may_reach_legend(artist, bounds, renderer, fig.dpi):
            continue
        probe.clear()
        artist.draw(probe)
        data_ink = np.asarray(probe.buffer_rgba())[region][:, :, 3] > 0
        overlap = np.count_nonzero(legend_ink & data_ink)
        if overlap:
            yield artist, int(overlap)


def audit_figure(fig, *, min_font_pt=None, tolerance_pt=.6, display_width_inches=None,
                 check_data_occlusion=False):
    """Inspect final pixel extents at the figure's declared physical size.

    Text overlaps use actual rendered bounding boxes, including rotated labels.
    This is conservative for diagonal labels and shaped glyphs; review flagged
    intersections visually. ``min_font_pt`` is an explicit project preference.
    ``display_width_inches`` optionally checks the effective typography after
    manuscript inclusion; it does not resize the figure or alter data geometry.

    ``check_data_occlusion`` opts into review-level legend/data overlap checks
    using separate transparent Agg renders at the figure's current DPI. Supported
    standard 2D artists are Line2D (lines, markers and errorbar caps), PathCollection
    (scatter), LineCollection (including errorbar stems), and PolyCollection
    (including fill_between uncertainty bands). Actual rendered ink, transparency,
    dashes and artist clipping are honored. A frameless legend contributes only
    its text/handle ink; a visible frame also contributes its painted area.
    Same-axes and figure-level legend draw order is respected.

    This is not a complete collision audit: overlaps between different axes,
    nested/subfigure ordering, 3D/polar axes, images, bar patches, meshes, custom
    artist subclasses and Agg filters are outside its coverage. Other intervening
    artists that already hide the data are not modeled. Subpixel contacts and
    backend differences need visual review; no report certifies all uncertainty
    or evidence is unobscured. No data geometry is changed.
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
        if check_data_occlusion:
            for artist, overlap in _legend_data_overlaps(fig, legend, renderer):
                label = artist.get_label() or ""
                add("legend_data_overlap", ", ".join(t.get_text() for t in legend.get_texts()),
                    other_text=label if label and not label.startswith("_") else type(artist).__name__,
                    artist_id=legend.get_gid(), data_artist_id=artist.get_gid(),
                    data_label=label, data_artist_type=type(artist).__name__,
                    overlap_pixels=overlap)
    return issues


def issue_message(issue):
    prefix = {"page_overflow": "Text leaves the page", "clipped_text": "Text is clipped",
              "custom_clip_review": "Custom text clip requires visual review",
              "small_text": "Text below declared minimum font size",
              "text_overlap": "Text overlaps", "legend_overflow": "Legend leaves the page",
              "legend_data_overlap": "Legend overlaps plotted data; review placement"}[issue["kind"]]
    return prefix + ": " + repr(issue["text"]) + (
        " / " + repr(issue["other_text"]) if "other_text" in issue else "")
