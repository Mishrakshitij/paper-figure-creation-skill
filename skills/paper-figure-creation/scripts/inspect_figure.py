#!/usr/bin/env python3
"""Render a PDF figure at paper width and make reproducible inspection crops.

Requires Python 3.10+ and its standard library, plus existing ``pdfinfo`` and ``pdftoppm``.
``pdftotext`` is optional; no packages are installed. Example::

    python inspect_figure.py paper/figures/method.pdf --output-dir /tmp/method-review \
        --width-inches 5.5 --page 1 \
        --crop contexts:0.35,0.05,0.72,0.52 \
        --crop goal-loop:0.48,0.58,0.99,0.99

Crop coordinates are fractions of the **displayed, rotated MediaBox**, with the
origin at its top left: name:x0,y0,x1,y1. Crops use the 300-pixels-per-display-inch
detail render, so they enlarge connectors/labels by 3x relative to the 100-ppi
paper preview. The report records actual dimensions, scaling, pixel crop bounds,
commands, and SHA-256 hashes. Open both previews and each crop; trace connectors
from source to arrowhead, check junctions/crossings and label clearance, then
inspect the complete figure in its manuscript context. Re-run after repairs.

``inspection_required`` always remains true. Text bounds are only a conservative
extracted-word boundary check: outlined/raster/missing/clipped text can be absent,
and mathematical glyph boxes can overhang. This does NOT detect all text overlap,
arrow continuity, endpoints, crossings, semantics, or visual quality. Rendering
success is not visual approval. The JSON output list is authoritative; unrelated
old files in a reused output directory are not part of the current run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
from datetime import datetime, timezone
import xml.etree.ElementTree as ET


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, text=True, capture_output=True,
                            env={**os.environ, "LC_ALL": "C"}, timeout=120)
    if result.returncode:
        raise ValueError(f"{Path(command[0]).name} failed: {result.stderr.strip()[:2000]}")
    return result.stdout


def crop_argument(value: str) -> tuple[str, tuple[float, ...]]:
    try:
        name, raw = value.split(":", 1)
        box = tuple(float(part) for part in raw.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("crop must be name:x0,y0,x1,y1") from exc
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name):
        raise argparse.ArgumentTypeError("crop names need 1–64 letters, digits, underscores or hyphens")
    if (len(box) != 4 or not all(math.isfinite(x) for x in box)
            or not (0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1)):
        raise argparse.ArgumentTypeError("crop bounds must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1")
    return name, box


def page_info(pdf: Path, page: int, executable: str) -> dict:
    info = run([executable, "-box", "-f", str(page), "-l", str(page), str(pdf)])
    count = re.search(r"^Pages:\s+(\d+)", info, re.M)
    box = re.search(r"^Page\s+(?:\d+\s+)?MediaBox:\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)", info, re.M)
    rotation = re.search(r"^Page\s+(?:\d+\s+)?rot:\s+(-?\d+)", info, re.M)
    if not count or not box or not rotation:
        raise ValueError("could not read selected page count, MediaBox and rotation from pdfinfo")
    points = [float(v) for v in box.groups()]
    width, height = points[2] - points[0], points[3] - points[1]
    angle = int(rotation.group(1)) % 360
    if not all(math.isfinite(v) for v in points) or min(width, height) <= 0 or angle % 90:
        raise ValueError("invalid PDF page dimensions or rotation")
    if page > int(count.group(1)):
        raise ValueError(f"page {page} exceeds this PDF's {count.group(1)} pages")
    display_width, display_height = (height, width) if angle in (90, 270) else (width, height)
    return {"page": page, "page_count": int(count.group(1)), "box": "MediaBox",
            "media_box_points": points, "width_points": width, "height_points": height,
            "rotation_degrees": angle, "displayed_width_points": display_width,
            "displayed_height_points": display_height}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"renderer did not produce a valid PNG: {path.name}")
    return struct.unpack(">II", header[16:24])


def inspect_text_bounds(xml: str, tolerance: float = 0.5,
                        displayed_page_points: tuple[float, float] | None = None) -> dict:
    """Flag word boxes beyond the selected displayed page, not text overlap."""
    tree = ET.fromstring(xml)
    pages = [node for node in tree.iter() if node.tag.rsplit("}", 1)[-1] == "page"]
    if len(pages) != 1:
        raise ValueError("text extractor did not return exactly one selected page")
    page = pages[0]
    extracted_size = [float(page.attrib["width"]), float(page.attrib["height"])]
    # Poppler's bbox coordinates follow rotation but its page attributes do not.
    width, height = displayed_page_points or extracted_size
    if not all(math.isfinite(v) and v > 0 for v in (width, height)):
        raise ValueError("text extractor returned invalid page dimensions")
    count, flags = 0, []
    for word in page.iter():
        if word.tag.rsplit("}", 1)[-1] != "word":
            continue
        bounds = [float(word.attrib[k]) for k in ("xMin", "yMin", "xMax", "yMax")]
        if not all(math.isfinite(v) for v in bounds) or bounds[0] > bounds[2] or bounds[1] > bounds[3]:
            raise ValueError("text extractor returned an invalid word bounding box")
        count += 1
        if (bounds[0] < -tolerance or bounds[1] < -tolerance
                or bounds[2] > width + tolerance or bounds[3] > height + tolerance):
            flags.append({"text": "".join(word.itertext()), "bbox_points": bounds})
    return {"status": "checked" if count else "no_extractable_text", "words_checked": count,
            "extractor_page_points": extracted_size, "checked_page_points": [width, height],
            "tolerance_points": tolerance,
            "potential_out_of_bounds_words": flags,
            "limitations": "Extracted-word bounds only; cannot establish absence of clipping, overlap, missing text or connector defects."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--width-inches", type=float, default=5.5)
    parser.add_argument("--page", type=int, default=1, help="one-based PDF page (default: 1)")
    parser.add_argument("--crop", type=crop_argument, action="append", default=[], metavar="NAME:X0,Y0,X1,Y1")
    args = parser.parse_args()
    try:
        if not math.isfinite(args.width_inches) or not 0 < args.width_inches <= 30:
            raise ValueError("width-inches must be finite and greater than 0, at most 30")
        if args.page < 1:
            raise ValueError("page must be at least 1")
        names = [name for name, _ in args.crop]
        if len(names) != len(set(names)):
            raise ValueError("crop names must be unique")
        source = args.input_pdf.expanduser().resolve()
        if not source.is_file():
            raise ValueError(f"input PDF does not exist: {source}")
        output = args.output_dir.expanduser().resolve()
        executables = {name: shutil.which(name) for name in ("pdfinfo", "pdftoppm", "pdftotext")}
        for name in ("pdfinfo", "pdftoppm"):
            if not executables[name]:
                raise ValueError(f"required existing tool is unavailable: {name}")
        source_hash = sha256(source)
        dimensions = page_info(source, args.page, executables["pdfinfo"])
        scale = args.width_inches * 72 / dimensions["displayed_width_points"]
        height_inches = dimensions["displayed_height_points"] * scale / 72
        if round(args.width_inches * 300) < 1 or args.width_inches * height_inches * 300**2 > 100_000_000:
            raise ValueError("requested detail image is empty or exceeds 100 million pixels")
        planned_names = ["paper_width.png", "detail.png", "inspection_report.json"] + [f"crop_{name}.png" for name in names]
        if any(output / name == source for name in planned_names):
            raise ValueError("an output would overwrite the source PDF")
        output.mkdir(parents=True, exist_ok=True)
        report = {"schema_version": 1, "created_at_utc": datetime.now(timezone.utc).isoformat(),
                  "source": {"path": str(source), "sha256": source_hash, **dimensions},
                  "display": {"width_inches": args.width_inches, "height_inches": height_inches,
                              "scale_from_pdf_page": scale}, "inspection_required": True,
                  "automatically_checks_arrow_continuity_or_overlap": False, "outputs": {},
                  "review": ["Open the paper-width preview for hierarchy and readable labels.",
                             "Open detail and every crop; trace each line from source through bends/junctions to its arrowhead.",
                             "Check endpoint gaps, crossings, arrow direction, node/label spacing and clipping.",
                             "Inspect the assembled manuscript; rendering success is not visual approval."]}
        with tempfile.TemporaryDirectory(prefix=".inspect-", dir=output) as tmp:
            stage = Path(tmp)
            def render(name: str, ppi: int, crop: tuple[int, int, int, int] | None = None) -> dict:
                prefix = stage / name
                target_pixels = round(args.width_inches * ppi)
                # pdftoppm's x/y scaling axes precede page rotation.
                scale_x, scale_y = ((-1, target_pixels) if dimensions["rotation_degrees"] in (90, 270)
                                    else (target_pixels, -1))
                command = [executables["pdftoppm"], "-png", "-singlefile", "-f", str(args.page),
                           "-l", str(args.page), "-scale-to-x", str(scale_x),
                           "-scale-to-y", str(scale_y)]
                if crop:
                    for option, value in zip(("-x", "-y", "-W", "-H"), crop):
                        command.extend((option, str(value)))
                command.extend((str(source), str(prefix)))
                run(command)
                path = prefix.with_suffix(".png")
                width_px, height_px = png_size(path)
                if not crop and width_px != target_pixels:
                    raise ValueError("renderer width differs from the requested physical display scale")
                return {"path": str(output / path.name), "sha256": sha256(path),
                        "width_pixels": width_px, "height_pixels": height_px,
                        "requested_pixels_per_display_inch": ppi,
                        "command": command[:-1] + [str(output / name)]}
            report["outputs"]["paper_width"] = render("paper_width", 100)
            report["outputs"]["detail"] = detail = render("detail", 300)
            for role in ("paper_width", "detail"):
                entry = report["outputs"][role]
                entry["effective_pixels_per_display_inch"] = entry["width_pixels"] / args.width_inches
                entry["equivalent_source_dpi"] = entry["width_pixels"] * 72 / dimensions["displayed_width_points"]
            report["outputs"]["crops"] = []
            for name, box in args.crop:
                width, height = detail["width_pixels"], detail["height_pixels"]
                x, y = math.floor(box[0] * width), math.floor(box[1] * height)
                right, bottom = math.ceil(box[2] * width), math.ceil(box[3] * height)
                pixels = (x, y, right - x, bottom - y)
                entry = render(f"crop_{name}", 300, pixels)
                entry.update(name=name, normalized_bounds=list(box), pixel_crop_xywh=list(pixels),
                             coordinate_origin="top-left of displayed rotated MediaBox",
                             effective_pixels_per_display_inch=detail["effective_pixels_per_display_inch"])
                if (entry["width_pixels"], entry["height_pixels"]) != pixels[2:]:
                    raise ValueError(f"crop {name} output dimensions differ from requested bounds")
                report["outputs"]["crops"].append(entry)
            if executables["pdftotext"]:
                try:
                    xml = run([executables["pdftotext"], "-bbox", "-f", str(args.page), "-l",
                               str(args.page), str(source), "-"])
                    report["text_bounds"] = inspect_text_bounds(
                        xml, displayed_page_points=(dimensions["displayed_width_points"],
                                                    dimensions["displayed_height_points"]))
                except (ValueError, KeyError, ET.ParseError, subprocess.TimeoutExpired) as exc:
                    report["text_bounds"] = {"status": "unavailable", "reason": str(exc)}
            else:
                report["text_bounds"] = {"status": "unavailable", "reason": "pdftotext is not installed"}
            if sha256(source) != source_hash:
                raise ValueError("source PDF changed during inspection; rerun against one stable export")
            for artifact in stage.glob("*.png"):
                artifact.replace(output / artifact.name)
            manifest = stage / "inspection_report.json"
            manifest.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
            manifest.replace(output / manifest.name)
        print(output / "inspection_report.json")
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
