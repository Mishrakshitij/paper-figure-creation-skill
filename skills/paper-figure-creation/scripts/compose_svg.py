#!/usr/bin/env python3
"""Assemble static vector plots and illustrative raster assets in physical points.

The manifest is the canonical geometry source. This compositor does not validate
scientific evidence; its report records declarations and physical export checks.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

from PIL import Image

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)
NUMBER = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"
IDENTITY = (1., 0., 0., 1., 0., 0.)
UNITS = {"": 1., "px": 1., "pt": 96 / 72, "pc": 16., "in": 96., "mm": 96 / 25.4, "cm": 96 / 2.54}
ACTIVE = {"script", "foreignObject", "animate", "animateTransform", "animateMotion", "set", "a"}


def tag(name):
    return f"{{{SVG}}}{name}"


def finite(value, name, positive=False):
    value = float(value)
    if not math.isfinite(value) or (positive and value <= 0):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else ""))
    return value


def multiply(a, b):
    x, y, z, w, u, v = a
    p, q, r, s, t, k = b
    return (x*p+z*q, y*p+w*q, x*r+z*s, y*r+w*s, x*t+z*k+u, y*t+w*k+v)


def transform(value):
    result = IDENTITY
    pattern = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")
    residue = pattern.sub("", value or "")
    if residue.strip(" ,\t\r\n"):
        raise ValueError(f"Unsupported transform: {value}")
    for op, raw in pattern.findall(value or ""):
        numbers = [finite(x, "transform") for x in re.findall(NUMBER, raw)]
        if re.sub(NUMBER, "", raw).strip(" ,\t\r\n"):
            raise ValueError(f"Invalid transform: {value}")
        if op == "matrix" and len(numbers) == 6:
            matrix = tuple(numbers)
        elif op == "translate" and len(numbers) in (1, 2):
            matrix = (1, 0, 0, 1, numbers[0], numbers[1] if len(numbers) == 2 else 0)
        elif op == "scale" and len(numbers) in (1, 2):
            matrix = (numbers[0], 0, 0, numbers[-1], 0, 0)
        elif op == "rotate" and len(numbers) in (1, 3):
            angle = math.radians(numbers[0]); c, s = math.cos(angle), math.sin(angle)
            matrix = (c, s, -s, c, 0, 0)
            if len(numbers) == 3:
                x, y = numbers[1:]
                matrix = multiply(multiply((1, 0, 0, 1, x, y), matrix), (1, 0, 0, 1, -x, -y))
        elif op in ("skewX", "skewY") and len(numbers) == 1:
            k = math.tan(math.radians(numbers[0]))
            matrix = (1, 0 if op == "skewX" else k, k if op == "skewX" else 0, 1, 0, 0)
        else:
            raise ValueError(f"Unsupported transform: {value}")
        result = multiply(result, matrix)
    return result


def min_scale(matrix):
    a, b, c, d, _, _ = matrix
    trace = a*a+b*b+c*c+d*d
    determinant = (a*d-b*c)**2
    return math.sqrt(max(0, (trace-math.sqrt(max(0, trace*trace-4*determinant)))/2))


def length(value):
    match = re.fullmatch(rf"\s*({NUMBER})([a-z]*)\s*", str(value))
    if not match or match[2] not in UNITS:
        raise ValueError(f"Unsupported SVG length: {value}; use absolute units")
    return finite(match[1], "SVG length") * UNITS[match[2]]


def declarations(value):
    result = {}
    for item in value.split(";"):
        if not item.strip():
            continue
        if ":" not in item:
            raise ValueError(f"Malformed CSS declaration: {item}")
        key, val = item.split(":", 1)
        if "!important" in val or "var(" in val or key.strip().startswith("--"):
            raise ValueError("SVG CSS variables and !important are unsupported; inline computed styles first")
        result[key.strip()] = val.strip()
    return result


def selector_match(element, selector):
    """Only simple selectors: *, element, #id, .class, element.class, element#id."""
    match = re.fullmatch(r"(\*|[A-Za-z_][\w-]*)?([.#][A-Za-z_][\w-]*)?", selector)
    if not match or not any(match.groups()):
        raise ValueError(f"Unsupported CSS selector {selector!r}; inline computed styles first")
    name, suffix = match.groups()
    if name and name != "*" and element.tag.rsplit("}", 1)[-1] != name:
        return False
    if suffix and suffix.startswith("#"):
        return element.get("id") == suffix[1:]
    if suffix:
        return suffix[1:] in element.get("class", "").split()
    return True


def inline_styles(root):
    rules = []
    for style in root.iter(tag("style")):
        source = re.sub(r"/\*.*?\*/", "", style.text or "", flags=re.S)
        matches = list(re.finditer(r"([^{}]+)\{([^{}]*)\}", source))
        if re.sub(r"[^{}]+\{[^{}]*\}", "", source).strip() or "@" in source:
            raise ValueError("Unsupported SVG stylesheet; inline computed styles first")
        for match in matches:
            for selector in match[1].split(","):
                selector = selector.strip()
                selector_match(root, selector)  # Validate even if no matching elements.
                specificity = (100 if "#" in selector else 10 if "." in selector else 0) + (1 if selector[0].isalpha() else 0)
                rules.append((specificity, selector, declarations(match[2])))
    for element in root.iter():
        computed = {}
        for _, selector, styles in sorted(rules, key=lambda r: r[0]):
            if selector_match(element, selector):
                computed.update(styles)
        computed.update(declarations(element.get("style", "")))
        if computed:
            element.set("style", ";".join(f"{key}:{val}" for key, val in computed.items()))
    for parent in root.iter():
        for child in list(parent):
            if child.tag == tag("style"):
                parent.remove(child)


def sanitize_svg(raw, prefix):
    if re.search(br"<!\s*(DOCTYPE|ENTITY)", raw, re.I):
        # Matplotlib emits the standard SVG doctype without entities. Remove that
        # exact inert declaration; reject arbitrary DTDs and internal subsets.
        raw = re.sub(br'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1\.1//EN"\s+"http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd">', b"", raw)
        if re.search(br"<!\s*(DOCTYPE|ENTITY)", raw, re.I):
            raise ValueError("SVG DTDs/entities are unsupported")
    root = ET.fromstring(raw)
    if root.tag != tag("svg"):
        raise ValueError("Vector asset must be an SVG document")
    ids = {}
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1]
        if local in ACTIVE:
            raise ValueError(f"Active/linked SVG element is forbidden: {local}")
        if local == "svg" and element is not root:
            raise ValueError("Nested SVG viewports are unsupported; flatten their transforms first")
        for key, value in element.attrib.items():
            short = key.rsplit("}", 1)[-1]
            if short.lower().startswith("on"):
                raise ValueError("SVG event handlers are forbidden")
            if short in ("href", "src") and not value.startswith("#"):
                if not (local == "image" and re.fullmatch(r"data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/=\s]+", value)):
                    raise ValueError("External SVG resources are forbidden; embed raster images first")
            for target in re.findall(r"url\(\s*['\"]?([^)'\"]+)", value, re.I):
                if not target.strip().startswith("#"):
                    raise ValueError("External SVG resources are forbidden")
        if element.get("id"):
            name = element.get("id")
            if name in ids:
                raise ValueError(f"Duplicate ID inside vector asset: {name}")
            ids[name] = prefix + name
    # Check stylesheet URLs before inlining, too.
    for style in root.iter(tag("style")):
        for target in re.findall(r"url\(\s*['\"]?([^)'\"]+)", style.text or "", re.I):
            if not target.strip().startswith("#"):
                raise ValueError("External SVG stylesheet resource is forbidden")
    inline_styles(root)
    for element in root.iter():
        for key, value in list(element.attrib.items()):
            short = key.rsplit("}", 1)[-1]
            if short == "id":
                value = ids[value]
            elif short == "href" and value.startswith("#"):
                if value[1:] not in ids:
                    raise ValueError(f"Unresolved SVG reference: {value}")
                value = "#" + ids[value[1:]]
            else:
                def rewrite(match):
                    name = match[1]
                    if name not in ids:
                        raise ValueError(f"Unresolved SVG reference: #{name}")
                    return f"url(#{ids[name]})"
                value = re.sub(r"url\(\s*['\"]?#([^)'\"\s]+)['\"]?\s*\)", rewrite, value)
                if short in ("aria-labelledby", "aria-describedby"):
                    value = " ".join(ids.get(name, name) for name in value.split())
            element.set(key, value)
    return root


def font_size(styles, inherited):
    result = inherited
    for key, value in styles.items():
        if key == "font":
            match = re.search(rf"({NUMBER}(?:px|pt|pc|in|mm|cm))(?:\s*/[^\s]+)?\s", value)
            if not match:
                raise ValueError("Cannot audit SVG font shorthand; use explicit font-size")
            result = length(match[1])
        elif key == "font-size":
            result = inherited if value == "inherit" else length(value)
    return result


def text_audit(root, initial_matrix, raster_reports=None):
    labels = []
    def walk(element, matrix, inherited_size=16., hidden=False, in_defs=False):
        matrix = multiply(matrix, transform(element.get("transform", "")))
        style = {"font-size": element.get("font-size")} if element.get("font-size") else {}
        style.update(declarations(element.get("style", "")))
        size = font_size(style, inherited_size)
        hidden = hidden or style.get("display", element.get("display")) == "none" or style.get("visibility", element.get("visibility")) == "hidden"
        in_defs = in_defs or element.tag == tag("defs")
        if element.tag in (tag("text"), tag("tspan")) and element.text and element.text.strip() and not hidden and not in_defs:
            labels.append({"text": element.text.strip(), "font_size_pt": round(size * min_scale(matrix), 4)})
        if element.tag == tag("image") and not hidden and not in_defs and raster_reports is not None:
            href = element.get("href", element.get(f"{{{XLINK}}}href", ""))
            if href.startswith("data:"):
                payload = base64.b64decode(href.split(",", 1)[1])
                with Image.open(io.BytesIO(payload)) as bitmap:
                    iw, ih = bitmap.size
                sx, sy = length(element.get("width", "0"))/iw, length(element.get("height", "0"))/ih
                preserve = element.get("preserveAspectRatio", "xMidYMid meet")
                if preserve != "none":
                    sx = sy = (max if "slice" in preserve else min)(sx, sy)
                effective = multiply(matrix, (sx, 0, 0, sy, 0, 0))
                a, b, c, d, _, _ = effective
                trace = a*a+b*b+c*c+d*d
                max_scale = math.sqrt(max(0, (trace+math.sqrt(max(0, trace*trace-4*(a*d-b*c)**2)))/2))
                if max_scale <= 0:
                    raise ValueError("Embedded SVG raster has no positive physical dimensions")
                raster_reports.append({"id": element.get("id"), "pixel_dimensions": [iw, ih], "effective_ppi": round(72/max_scale, 2), "sha256": hashlib.sha256(payload).hexdigest()})
        for child in element:
            walk(child, matrix, size, hidden, in_defs)
    walk(root, initial_matrix)
    return labels


def asset_path(manifest_dir, root_name, filename):
    base = Path(manifest_dir).resolve()
    root = (base / root_name).resolve()
    try:
        root.relative_to(base)
        path = (root / filename).resolve()
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError("Asset path must remain inside the manifest's asset_root") from exc
    if Path(filename).is_absolute() or Path(root_name).is_absolute():
        raise ValueError("Asset paths must be relative")
    if not path.is_file():
        raise ValueError(f"Asset does not exist: {filename}")
    return path


def fit_box(box, intrinsic, fit):
    x, y, w, h = box; iw, ih = intrinsic
    if fit not in ("contain", "cover"):
        raise ValueError("fit must be contain or cover; stretching scientific geometry is unsupported")
    scale = (min if fit == "contain" else max)(w / iw, h / ih)
    return x + (w - iw * scale) / 2, y + (h - ih * scale) / 2, scale


def compose(spec, manifest_dir, output, formats=("svg", "pdf", "png"), dpi=300):
    width = finite(spec["canvas"]["width_pt"], "canvas width", True)
    height = finite(spec["canvas"]["height_pt"], "canvas height", True)
    dpi = finite(dpi, "dpi", True)
    if set(formats) - {"svg", "pdf", "png"}:
        raise ValueError("Supported formats are svg,pdf,png")
    root = ET.Element(tag("svg"), {"width": f"{width:g}pt", "height": f"{height:g}pt", "viewBox": f"0 0 {width:g} {height:g}"})
    ET.SubElement(root, tag("title")).text = spec.get("title", "Composed research figure")
    defs = ET.SubElement(root, tag("defs"))
    if spec["canvas"].get("background", "white") != "transparent":
        ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": str(width), "height": str(height), "fill": spec["canvas"].get("background", "white")})
    report = {"canvas_pt": [width, height], "canonical_geometry": "composition manifest", "scientific_evidence_validated": False, "assets": [], "labels": [], "warnings": [], "exports": []}
    seen = set()
    for index, asset in enumerate(spec.get("assets", [])):
        name = asset["id"]
        if not re.fullmatch(r"[A-Za-z_][\w-]*", name) or name in seen:
            raise ValueError("Asset IDs must be unique XML-style identifiers")
        seen.add(name)
        if not isinstance(asset.get("provenance"), dict) or not asset["provenance"]:
            raise ValueError(f"Asset {name} requires provenance declarations")
        path = asset_path(manifest_dir, spec.get("asset_root", "."), asset["path"])
        raw = path.read_bytes()
        box = [finite(value, f"{name} box") for value in asset["box_pt"]]
        if len(box) != 4 or min(box[2:]) <= 0:
            raise ValueError("box_pt must be [x,y,positive width,positive height]")
        if box[0] < 0 or box[1] < 0 or box[0]+box[2] > width or box[1]+box[3] > height:
            raise ValueError(f"Asset {name} box leaves the canvas")
        info = {"id": name, "path": asset["path"], "sha256": hashlib.sha256(raw).hexdigest(), "kind": asset["kind"], "box_pt": box, "provenance": asset["provenance"]}
        container = ET.SubElement(root, tag("g"), {"id": f"asset-{name}"})
        fit = asset.get("fit", "contain")
        if fit == "cover":
            if not asset.get("allow_crop", False):
                raise ValueError("cover requires allow_crop:true; never silently crop evidence")
            clip = ET.SubElement(defs, tag("clipPath"), {"id": f"clip-placement-{name}"})
            ET.SubElement(clip, tag("rect"), dict(zip(("x", "y", "width", "height"), map(str, box))))
            container.set("clip-path", f"url(#clip-placement-{name})")
            info["cropped"] = True
        if asset["kind"] == "vector":
            source = sanitize_svg(raw, f"import-{index}-")
            if source.get("viewBox"):
                view = [float(v) for v in re.split(r"[ ,]+", source.get("viewBox").strip())]
            else:
                view = [0., 0., length(source.get("width", "")), length(source.get("height", ""))]
            if len(view) != 4 or any(not math.isfinite(v) for v in view) or min(view[2:]) <= 0:
                raise ValueError(f"Invalid viewBox for {name}")
            tx, ty, scale = fit_box(box, view[2:], fit)
            matrix = (scale, 0, 0, scale, tx-scale*view[0], ty-scale*view[1])
            attrs = {key: val for key, val in source.attrib.items() if key not in {"width", "height", "viewBox", "version", "preserveAspectRatio", "x", "y", "transform"}}
            # Preserve root-level presentation styles and transforms on their own group.
            placed = ET.SubElement(container, tag("g"), {"transform": "matrix(" + " ".join(f"{v:.12g}" for v in matrix) + ")"})
            imported = ET.SubElement(placed, tag("g"), attrs)
            if source.get("transform"):
                imported.set("transform", source.get("transform"))
            for child in source:
                imported.append(child)
            embedded_rasters = []
            labels = text_audit(source, matrix, embedded_rasters)
            if embedded_rasters:
                info["embedded_rasters"] = embedded_rasters
                for raster in embedded_rasters:
                    if raster["effective_ppi"] < spec.get("quality", {}).get("minimum_raster_ppi", 300):
                        report["warnings"].append(f"Embedded raster in {name}: {raster['effective_ppi']} PPI")
            for label in labels:
                label["asset"] = name
            report["labels"].extend(labels)
            info["editable_text_count"] = len(labels)
            info["minimum_font_size_pt"] = min((item["font_size_pt"] for item in labels), default=None)
            if not labels:
                report["warnings"].append(f"Asset {name} has no auditable live text; inspect whether labels were converted to paths")
        elif asset["kind"] == "raster":
            with Image.open(io.BytesIO(raw)) as bitmap:
                iw, ih = bitmap.size
                mime = Image.MIME.get(bitmap.format)
            if mime not in {"image/png", "image/jpeg", "image/webp"}:
                raise ValueError("Raster assets must be PNG, JPEG or WebP")
            tx, ty, scale = fit_box(box, (iw, ih), fit)
            href = f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")
            ET.SubElement(container, tag("image"), {"x": str(tx), "y": str(ty), "width": str(iw*scale), "height": str(ih*scale), f"{{{XLINK}}}href": href})
            info.update(pixel_dimensions=[iw, ih], effective_ppi=round(72 / scale, 2))
            if info["effective_ppi"] < spec.get("quality", {}).get("minimum_raster_ppi", 300):
                report["warnings"].append(f"Asset {name}: effective raster resolution is {info['effective_ppi']} PPI")
        else:
            raise ValueError("Asset kind must be vector or raster")
        report["assets"].append(info)
    overlay_group = ET.SubElement(root, tag("g"), {"id": "authoritative-overlays"})
    for index, overlay in enumerate(spec.get("overlays", [])):
        kind = overlay["type"]
        attrs = {"fill": overlay.get("fill", "none"), "stroke": overlay.get("stroke", "#273244"), "stroke-width": str(finite(overlay.get("stroke_width_pt", 1), "stroke width"))}
        if "dash_pt" in overlay:
            attrs["stroke-dasharray"] = " ".join(str(finite(v, "dash")) for v in overlay["dash_pt"])
        if kind == "text":
            size = finite(overlay.get("font_size_pt", 8), "font size", True)
            x, y = finite(overlay["x"], "text x"), finite(overlay["y"], "text y")
            anchor = overlay.get("anchor", "start")
            if anchor not in ("start", "middle", "end"):
                raise ValueError("Text anchor must be start,middle,end")
            item = ET.SubElement(overlay_group, tag("text"), {"x": str(x), "y": str(y), "font-size": str(size), "font-family": overlay.get("font_family", "DejaVu Sans"), "font-weight": str(overlay.get("font_weight", "normal")), "fill": overlay.get("fill", "#172335"), "text-anchor": anchor})
            lines = str(overlay["text"]).split("\n")
            for line_index, line in enumerate(lines):
                ET.SubElement(item, tag("tspan"), {"x": str(x), "dy": "0" if line_index == 0 else str(size * 1.25)}).text = line
            report["labels"].append({"text": overlay["text"], "font_size_pt": size, "asset": "overlays"})
            if x < 0 or x > width or y < size or y+(len(lines)-1)*size*1.25 > height:
                report["warnings"].append(f"Overlay text {index} may leave the canvas")
        elif kind in ("rect", "ellipse"):
            keys = ("x", "y", "width", "height") if kind == "rect" else ("cx", "cy", "rx", "ry")
            attrs.update({key: str(finite(overlay[key], key)) for key in keys})
            if kind == "rect" and "radius_pt" in overlay:
                attrs["rx"] = str(finite(overlay["radius_pt"], "radius"))
            ET.SubElement(overlay_group, tag(kind), attrs)
        elif kind in ("arrow", "path"):
            if kind == "arrow":
                points = overlay["points"]
                if len(points) < 2 or any(len(p) != 2 for p in points):
                    raise ValueError("Arrow needs at least two [x,y] points")
                attrs["d"] = "M " + " L ".join(" ".join(str(finite(v, "arrow point")) for v in p) for p in points)
                marker_id = f"overlay-arrow-{index}"
                marker = ET.SubElement(defs, tag("marker"), {"id": marker_id, "viewBox": "0 0 8 8", "refX": "7", "refY": "4", "markerWidth": "5", "markerHeight": "5", "orient": "auto", "markerUnits": "strokeWidth"})
                ET.SubElement(marker, tag("path"), {"d": "M 0 0 L 8 4 L 0 8 Z", "fill": attrs["stroke"]})
                attrs["marker-end"] = f"url(#{marker_id})"
            else:
                if not re.fullmatch(r"[MmLlHhVvCcSsQqTtAaZz0-9eE+.,\s-]+", overlay["d"]):
                    raise ValueError("Unsupported SVG path data")
                attrs["d"] = overlay["d"]
            ET.SubElement(overlay_group, tag("path"), attrs)
        else:
            raise ValueError(f"Unsupported overlay type: {kind}")
    report["minimum_font_size_pt"] = min((item["font_size_pt"] for item in report["labels"]), default=None)
    minimum = spec.get("quality", {}).get("minimum_font_size_pt", 6.5)
    for item in report["labels"]:
        if item["font_size_pt"] < minimum:
            report["warnings"].append(f"Small text in {item['asset']}: {item['text']!r} is {item['font_size_pt']:g} pt (target {minimum:g} pt)")
    report["review_required"] = "Visual inspection is required: the compositor does not detect all overlaps, clipped glyphs, arrow crossings, or scientific errors"
    # Validate assembled attributes too, including user-supplied overlay colors.
    for element in root.iter():
        for value in element.attrib.values():
            for target in re.findall(r"url\(\s*[\'\"]?([^ )\'\"]+)", value, re.I):
                if not target.startswith("#"):
                    raise ValueError("External resources in overlay styles are forbidden")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    svg_path = output.with_suffix(".svg")
    ET.ElementTree(root).write(svg_path, encoding="utf-8", xml_declaration=True)
    report["exports"].append({"format": "svg", "path": str(svg_path), "verified": True, "check": "XML parsed; physical dimensions and asset references constructed"})
    for fmt in formats:
        if fmt == "svg":
            continue
        if not shutil.which("inkscape"):
            raise RuntimeError("Inkscape is required for PDF/PNG exports; canonical SVG was saved")
        target = output.with_suffix("." + fmt)
        command = ["inkscape", str(svg_path), "--export-area-page", f"--export-type={fmt}", f"--export-filename={target}"]
        if fmt == "png":
            command.append(f"--export-dpi={dpi:g}")
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if result.returncode or not target.is_file() or not target.stat().st_size:
            raise RuntimeError(f"Inkscape {fmt} export failed: {result.stderr.strip()}")
        check = "Inkscape completed and nonempty file exists"
        if fmt == "png":
            with Image.open(target) as bitmap:
                actual = bitmap.size
            expected = (round(width / 72 * dpi), round(height / 72 * dpi))
            if any(abs(a-b) > 1 for a, b in zip(actual, expected)):
                raise RuntimeError(f"PNG dimension mismatch: {actual} vs {expected}")
            check = f"PNG dimensions {actual[0]}×{actual[1]} checked against physical size at {dpi:g} DPI"
        verified = fmt == "png"
        if fmt == "pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                report["warnings"].append("PDF export exists but its page dimensions are unverified (pypdf unavailable)")
            else:
                pages = PdfReader(target).pages
                if len(pages) != 1 or abs(float(pages[0].mediabox.width)-width) > .02 or abs(float(pages[0].mediabox.height)-height) > .02:
                    raise RuntimeError("PDF page dimensions do not match the manifest")
                verified = True
                check = "Single PDF page and physical MediaBox dimensions verified; rendered appearance still requires inspection"
        report["exports"].append({"format": fmt, "path": str(target), "verified": verified, "check": check})
    report["manifest_sha256"] = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    output.with_suffix(".composition-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formats", default="svg,pdf,png")
    parser.add_argument("--dpi", type=float, default=300)
    args = parser.parse_args()
    spec = json.loads(args.manifest.read_text())
    report = compose(spec, args.manifest.parent, args.output, tuple(args.formats.split(",")), args.dpi)
    print(json.dumps({"exports": report["exports"], "minimum_font_size_pt": report["minimum_font_size_pt"], "warnings": report["warnings"]}, indent=2))


if __name__ == "__main__":
    main()
