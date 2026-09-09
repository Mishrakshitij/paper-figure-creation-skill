#!/usr/bin/env python3
"""Reproduce bounded PDF/caption harvesting from the published canonical URLs.

This script does not perform human/agent visual review and never assigns a
figure-quality score. PDF downloads are a local research cache, not deliverables.
Requires: pip install pymupdf
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request


CAPTION = re.compile(r"^(?:Figure|Fig\.)\s*(\d+)[.:]\s*(.*)", re.I | re.S)
TAGS = {
    "method_or_architecture": r"overview|architectur|framework|pipeline|schematic|workflow",
    "worked_example_or_problem": r"example|illustrat|toy |problem|task setup|motivating",
    "quantitative_comparison": r"accuracy|performance|comparison|baseline|error rate|results|outperform",
    "efficiency_or_tradeoff": r"efficien|speed|runtime|latency|memory|cost|trade.off|scaling|training time",
    "qualitative_outputs": r"qualitative|generated|reconstruct|render|visualiz|synthesis",
    "ablation_or_mechanism": r"ablation|effect of|impact of|without|component|sensitivity",
    "uncertainty_or_distribution": r"uncertainty|variance|confidence|distribution|standard deviation",
}


def download(url: str, target: Path, timeout: float) -> str:
    if target.exists() and target.stat().st_size > 100:
        return "cached"
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "paper-figure-research/1.0"})
    error = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
            if not data.startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF")
            temporary = target.with_suffix(".part")
            temporary.write_bytes(data)
            temporary.replace(target)
            return "downloaded"
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            error = exc
            if attempt == 0:
                time.sleep(0.5)
    raise RuntimeError(str(error))


def process(record: dict, args: argparse.Namespace) -> dict:
    result = {
        "paper_id": record["paper_id"],
        "title": record["title"],
        "pdf_url": record["pdf_url"],
        "visual_reviewed": False,
        "analyst_caption_reviewed": False,
        "caption_candidates": [],
    }
    try:
        import fitz
        target = args.cache / (record["paper_id"] + ".pdf")
        result["download_status"] = download(record["pdf_url"], target, args.timeout)
        result["pdf_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        with fitz.open(target) as document:
            result["pdf_page_count"] = len(document)
            result["pages_examined"] = min(args.pages, len(document))
            for page_index in range(result["pages_examined"]):
                page = document[page_index]
                for block in page.get_text("blocks", sort=True):
                    match = CAPTION.match(block[4].strip())
                    if not match:
                        continue
                    text = re.sub(r"\s+", " ", match.group(2)).strip()
                    result["caption_candidates"].append({
                        "figure": int(match.group(1)),
                        "pdf_page": page_index + 1,
                        "bbox": [round(float(n), 2) for n in block[:4]],
                        "tags_from_caption_keywords": [k for k, pattern in TAGS.items()
                                                       if re.search(pattern, text, re.I)],
                    })
                    # One short excerpt per paper; later candidates store no quotes.
                    if "caption_excerpt" not in result:
                        result["caption_excerpt"] = " ".join(text.split()[:22])
            result["screening_level"] = ("caption_candidates_extracted"
                                         if result["caption_candidates"] else "pdf_text_retrieved")
    except Exception as exc:
        result["screening_level"] = "metadata_catalogued"
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=Path(__file__).with_name("corpus-500.jsonl"))
    parser.add_argument("--output", type=Path, required=True,
                        help="Local output JSONL; existing files are not overwritten")
    parser.add_argument("--cache", type=Path, required=True,
                        help="Local scratch PDF cache, outside the published repository")
    parser.add_argument("--pages", type=int, default=6)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=45)
    args = parser.parse_args()
    if args.pages < 1 or args.workers < 1 or args.limit < 1:
        parser.error("pages, workers and limit must be positive")
    if args.output.exists():
        parser.error("output already exists; select a new path")
    records = [json.loads(line) for line in args.corpus.read_text().splitlines() if line.strip()][:args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            for result in executor.map(lambda row: process(row, args), records):
                output.write(json.dumps(result, ensure_ascii=False) + "\n")
                output.flush()
    print(f"Wrote {len(records)} records to {args.output}; no visual reviews were assigned.")


if __name__ == "__main__":
    main()
