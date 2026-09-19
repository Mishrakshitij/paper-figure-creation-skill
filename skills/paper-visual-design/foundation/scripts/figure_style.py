"""Shared publication defaults. Dimensions are inches; typography is points."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib as mpl

DEFAULT_THEME = {
    "font_family": "DejaVu Sans", "font_size": 8.5,
    "title_size": 12, "panel_title_size": 9.5, "small_size": 8.0,
    "ink": "#17232B", "muted": "#64717A", "accent": "#007D8A",
    "accent_light": "#E6F2F3", "warm": "#CC7733", "warm_light": "#FFF0E0",
    "baseline_colors": ["#667580", "#986C00", "#8E5681", "#37454F"],
    "grid": "#DCE2E5", "paper": "#FFFFFF", "panel": "#F6F8F9",
    "line_width": 0.9, "dpi": 300
}

def load_theme(path=None, overrides=None):
    theme = dict(DEFAULT_THEME)
    if path:
        theme.update(json.loads(Path(path).read_text()))
    if overrides:
        theme.update(overrides)
    return theme

def apply_theme(theme):
    mpl.rcParams.update({
        "font.family": theme["font_family"], "font.size": theme["font_size"],
        "text.color": theme["ink"], "axes.labelcolor": theme["ink"],
        "axes.edgecolor": theme["grid"], "xtick.color": theme["muted"],
        "ytick.color": theme["ink"], "axes.labelsize": theme["font_size"],
        "xtick.labelsize": theme["small_size"], "ytick.labelsize": theme["small_size"],
        "axes.titlesize": theme["panel_title_size"], "axes.titleweight": "bold",
        "axes.linewidth": theme["line_width"], "savefig.dpi": theme["dpi"],
        "figure.facecolor": theme["paper"], "axes.facecolor": theme["paper"],
        "savefig.facecolor": theme["paper"], "svg.fonttype": "none",
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.hashsalt": "paper-figure-creation-v1",
        "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False, "legend.fontsize": theme["small_size"],
    })
