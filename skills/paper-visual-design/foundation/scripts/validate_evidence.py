#!/usr/bin/env python3
"""Check a figure's declared evidence and arithmetic; not scientific truth.

Dependency-free API: validate_spec(spec) -> JSON-compatible report.
CLI: python validate_evidence.py figure.json [--output report.json]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


def finite(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def member(value, collection):
    return isinstance(value, str) and value in collection


def validate_spec(spec):
    report = {"valid": False, "errors": [], "warnings": [], "computed_claims": []}

    def issue(code, path, message, warning=False):
        report["warnings" if warning else "errors"].append({"code": code, "path": path, "message": message})

    def objects(value, path):
        if not isinstance(value, list):
            issue("invalid_shape", path, "Expected an array of objects.")
            return []
        out = []
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                issue("invalid_shape", f"{path}[{i}]", "Expected an object.")
            else:
                out.append((i, item))
        return out

    def index(value, path):
        out = {}
        for i, item in objects(value, path):
            key = item.get("id")
            if not nonempty(key):
                issue("missing_id", f"{path}[{i}]", "A nonempty string id is required.")
            elif key in out:
                issue("duplicate_id", f"{path}[{i}].id", f"Duplicate id: {key}.")
            else:
                out[key] = item
        return out

    if not isinstance(spec, dict):
        issue("invalid_shape", "$", "The figure specification must be an object.")
        return report
    if spec.get("version") != 1 or isinstance(spec.get("version"), bool):
        issue("schema_version", "version", "Supported version is the integer 1.")
    if not member(spec.get("kind"), {"teaser", "method", "benchmark", "graphs"}):
        issue("figure_kind", "kind", "Expected teaser, method, benchmark, or graphs.")
    if not member(spec.get("status"), {"draft", "final"}):
        issue("figure_status", "status", "Declare draft or final.")

    provenance = spec.get("provenance", {})
    if not isinstance(provenance, dict):
        issue("invalid_shape", "provenance", "Expected an object.")
        provenance = {}
    data_status = provenance.get("data_status")
    if not member(data_status, {"reported", "synthetic", "mixed"}):
        issue("data_status", "provenance.data_status", "Declare reported, synthetic, or mixed.")
    sources = index(provenance.get("sources", []), "provenance.sources")
    if not sources:
        issue("missing_sources", "provenance.sources", "At least one precise source is required, including for method diagrams.")
    for key, source in sources.items():
        path = f"provenance.sources[{key}]"
        if not member(source.get("kind"), {"paper", "artifact", "synthetic"}):
            issue("source_kind", path + ".kind", "Expected paper, artifact, or synthetic.")
        for field in ("locator", "location"):
            if not nonempty(source.get(field)):
                issue("source_location", path + "." + field, "Provide a retrievable locator and exact table/row/page/file/line location.")
    has_synthetic = any(s.get("kind") == "synthetic" for s in sources.values())
    if has_synthetic and data_status == "reported":
        issue("synthetic_disguised", "provenance.data_status", "A synthetic source cannot be declared reported data.")
    if member(data_status, {"synthetic", "mixed"}) or has_synthetic:
        if spec.get("status") != "draft":
            issue("synthetic_final", "status", "Synthetic numerical evidence is for labeled drafts only.")
        figure = spec.get("figure", {})
        if not isinstance(figure, dict):
            figure = {}
        visible = str(figure.get("subtitle", "")) + " " + str(figure.get("watermark", ""))
        if not re.search(r"\b(synthetic|illustrative)\b", visible, re.I):
            issue("synthetic_label", "figure.subtitle", "Include a visible SYNTHETIC DATA or ILLUSTRATIVE DATA label in subtitle or watermark.")
        issue("synthetic_not_evidence", "provenance", "Draft synthetic values establish layout only; they do not support paper claims.", True)

    # A benchmark/environment figure is conditional on an actual setup in the
    # paper. These fields record the eligibility decision and its source; they
    # cannot establish that the cited source says what the author claims.
    if spec.get("kind") == "benchmark":
        setup = spec.get("benchmark_setup")
        if not isinstance(setup, dict):
            issue("benchmark_setup", "benchmark_setup", "Provide the source-backed benchmark/environment setup contract.")
            setup = {}
        if setup.get("presence") != "present":
            issue("benchmark_presence", "benchmark_setup.presence", "Use a benchmark figure only when the paper contains a verified setup; absent or unclear does not qualify.")
        if not member(setup.get("source_id"), sources):
            issue("benchmark_source", "benchmark_setup.source_id", "Reference a declared source establishing that the benchmark/environment setup exists.")
        if not nonempty(setup.get("source_location")):
            issue("benchmark_source", "benchmark_setup.source_location", "Give the exact section, figure, appendix, or code location establishing the setup.")
        if not member(setup.get("contribution"), {"new_benchmark", "new_environment", "adapted_setup", "existing_setup"}):
            issue("benchmark_contribution", "benchmark_setup.contribution", "Distinguish a new benchmark/environment from an adapted or existing setup.")
        family = setup.get("family")
        if not member(family, {"static_benchmark", "interactive_environment", "mixed"}):
            issue("benchmark_family", "benchmark_setup.family", "Declare static_benchmark, interactive_environment, or mixed.")
        for field in ("unit_of_evaluation", "instance_construction", "evaluation"):
            if not nonempty(setup.get(field)):
                issue("benchmark_contract", "benchmark_setup." + field, "Describe this setup component from the source; do not invent missing settings.")
        for field in ("agent_visible", "evaluator_only"):
            value = setup.get(field)
            if not isinstance(value, list) or any(not nonempty(item) for item in value):
                issue("benchmark_visibility", "benchmark_setup." + field, "Declare an array of information descriptions; use [] when this category is empty.")
        # Static datasets do not imply actions, episodes, resets, or an agent
        # loop. A mixed setup includes an interactive component, so the same
        # episode contract is required for that component.
        if member(family, {"interactive_environment", "mixed"}):
            for field in ("observation", "actions", "state_transition", "reset", "termination"):
                if not nonempty(setup.get(field)):
                    issue("benchmark_episode", "benchmark_setup." + field, "Describe the interactive component's episode contract from the source.")
        for i, node in objects(spec.get("nodes", []), "nodes"):
            if "visibility" in node and not member(node["visibility"], {"agent", "evaluator", "public"}):
                issue("benchmark_node_visibility", f"nodes[{i}].visibility", "Optional visibility must be agent, evaluator, or public; this metadata does not hide a node from the reader.")

    evidence = spec.get("evidence", {})
    if not isinstance(evidence, dict):
        issue("invalid_shape", "evidence", "Expected an object.")
        evidence = {}
    metrics = index(evidence.get("metrics", []), "evidence.metrics")
    results = index(evidence.get("results", []), "evidence.results")
    claims = index(evidence.get("claims", []), "evidence.claims")
    for key, metric in metrics.items():
        if not member(metric.get("direction"), {"higher", "lower"}):
            issue("metric_direction", f"evidence.metrics[{key}].direction", "Declare higher or lower; the validator does not infer desirability.")
        if not nonempty(metric.get("unit")):
            issue("metric_unit", f"evidence.metrics[{key}].unit", "Declare a unit; use percent for values such as 74.2%, or fraction for 0.742.")
    valid_results = {}
    no_uncertainty = []
    for key, result in results.items():
        path = f"evidence.results[{key}]"
        error_count = len(report["errors"])
        if not nonempty(result.get("method_id")):
            issue("method_id", path + ".method_id", "A stable method id is required.")
        if not member(result.get("metric_id"), metrics):
            issue("unknown_metric", path + ".metric_id", "Reference a declared metric.")
        if not member(result.get("source_id"), sources):
            issue("unknown_source", path + ".source_id", "Reference a declared source with an exact location.")
        comparison = result.get("comparison")
        if not isinstance(comparison, dict):
            issue("comparison_context", path + ".comparison", "Declare dataset, split, budget, and any relevant protocol.")
            comparison = {}
        for field in ("dataset", "split", "budget"):
            if not nonempty(comparison.get(field)):
                issue("comparison_context", path + ".comparison." + field, "A nonempty comparison condition is required; do not guess unknown settings.")
        missing = result.get("missing", False)
        value = result.get("value")
        if missing is not False and missing is not True:
            issue("missing_flag", path + ".missing", "missing must be a boolean.")
        if missing is True:
            if value is not None:
                issue("missing_imputation", path + ".value", "A missing result must have value null, never an imputed zero.")
        elif not finite(value):
            issue("nonfinite_value", path + ".value", "Reported values must be finite numbers; null requires missing:true.")
        uncertainty = result.get("uncertainty")
        if uncertainty is None:
            if missing is not True:
                no_uncertainty.append(key)
        elif missing is True:
            issue("missing_uncertainty", path + ".uncertainty", "A missing result cannot have error bars.")
        elif not isinstance(uncertainty, dict):
            issue("invalid_shape", path + ".uncertainty", "Expected an uncertainty object.")
        else:
            up = path + ".uncertainty"
            typ = uncertainty.get("type")
            if not member(typ, {"sd", "se", "ci", "range"}):
                issue("uncertainty_type", up + ".type", "Use sd, se, ci, or range; these are not interchangeable.")
            symmetric = "value" in uncertainty
            bounded = "lower" in uncertainty and "upper" in uncertainty
            if symmetric == bounded:
                issue("uncertainty_extent", up, "Provide either nonnegative value (symmetric half width) or lower and upper bounds.")
            elif symmetric:
                if not finite(uncertainty["value"]) or uncertainty["value"] < 0:
                    issue("uncertainty_extent", up + ".value", "Error-bar half width must be finite and nonnegative.")
            elif not finite(uncertainty["lower"]) or not finite(uncertainty["upper"]) or uncertainty["lower"] > uncertainty["upper"]:
                issue("uncertainty_extent", up, "Uncertainty bounds must be finite and ordered lower <= upper.")
            elif finite(value) and not uncertainty["lower"] <= value <= uncertainty["upper"]:
                issue("uncertainty_outside", up, "Point estimate lies outside the declared interval; confirm the estimator and interval method.", True)
            # Explicit provenance prevents quietly relabeling SD as a CI or inventing error bars.
            if not member(uncertainty.get("source_id"), sources) or not nonempty(uncertainty.get("source_location")):
                issue("uncertainty_source", up, "Uncertainty requires source_id and an exact source_location of its own.")
            if "n" in uncertainty and (not isinstance(uncertainty["n"], int) or isinstance(uncertainty["n"], bool) or uncertainty["n"] < 2):
                issue("uncertainty_n", up + ".n", "If known, n must be an integer >= 2; omit unknown n.")
            if typ == "ci":
                if not finite(uncertainty.get("level")) or not 0 < uncertainty["level"] < 1:
                    issue("ci_level", up + ".level", "A confidence interval requires level in (0,1), e.g. 0.95.")
                if not nonempty(uncertainty.get("method")):
                    issue("ci_method", up + ".method", "State the reported/calculated CI method; never convert SD to CI by renaming it.")
            if not nonempty(uncertainty.get("variation")):
                issue("uncertainty_variation", up, "Describe the variation captured (seeds, test samples, splits, etc.) in the caption.", True)
        if len(report["errors"]) == error_count:
            valid_results[key] = result
    if no_uncertainty:
        issue("uncertainty_unreported", "evidence.results", "No uncertainty is declared for: " + ", ".join(no_uncertainty) + ". Do not fabricate intervals or assert significance.", True)

    def comparable(a, b, path, for_claim=True, tradeoff=False):
        if a.get("metric_id") != b.get("metric_id"):
            issue("incomparable_metric", path, "A claim must compare the same metric and unit.")
            return False
        ac, bc = a.get("comparison"), b.get("comparison")
        if tradeoff and isinstance(ac, dict) and isinstance(bc, dict):
            ac, bc = {k: v for k, v in ac.items() if k != "budget"}, {k: v for k, v in bc.items() if k != "budget"}
        if ac != bc:
            issue("incomparable_context", path, "Dataset, split, budget, protocol, and every declared comparison condition must match exactly.")
            return False
        if for_claim and (a.get("missing") or b.get("missing")):
            issue("missing_claim", path, "A missing result cannot support a numerical claim.")
            return False
        ak = sources.get(a.get("source_id"), {}).get("kind") if isinstance(a.get("source_id"), str) else None
        bk = sources.get(b.get("source_id"), {}).get("kind") if isinstance(b.get("source_id"), str) else None
        if (ak == "synthetic") != (bk == "synthetic"):
            issue("mixed_claim", path, "Do not compare a synthetic result with a reported result.")
            return False
        return True

    for key, claim in claims.items():
        path = f"evidence.claims[{key}]"
        typ = claim.get("type")
        if not member(typ, {"relative_improvement", "absolute_difference", "percentage_point_difference", "speedup", "reduction", "all_methods_superiority"}):
            issue("claim_type", path + ".type", "Unsupported claim type; use a declared arithmetic operation.")
            continue
        proposed_id = claim.get("proposed_result_id")
        baseline_id = claim.get("baseline_result_id")
        if not member(proposed_id, valid_results):
            issue("claim_result", path, "Proposed result is missing, unknown, or invalid.")
            continue
        p = valid_results[proposed_id]
        metric = metrics[p["metric_id"]]
        direction = metric.get("direction")
        if not member(direction, {"higher", "lower"}):
            continue
        if typ == "all_methods_superiority":
            baseline_ids = claim.get("baseline_result_ids")
            if not isinstance(baseline_ids, list) or not baseline_ids or any(not isinstance(x, str) for x in baseline_ids):
                issue("superiority_scope", path, "List baseline_result_ids for every other declared method in the same comparison context.")
                continue
            eligible = {rid for rid, r in results.items() if r.get("method_id") != p["method_id"] and r.get("metric_id") == p["metric_id"] and r.get("comparison") == p["comparison"]}
            if set(baseline_ids) != eligible or len(set(baseline_ids)) != len(baseline_ids):
                issue("superiority_scope", path, "All-methods claim must include every declared competing result in this context, without duplicates.")
                continue
            deltas = []
            for bid in baseline_ids:
                b = valid_results.get(bid)
                if b is None:
                    issue("claim_result", path, f"Baseline {bid} is unknown or invalid.")
                elif comparable(p, b, path):
                    deltas.append((p["value"] - b["value"]) * (1 if direction == "higher" else -1))
            if len(deltas) != len(baseline_ids):
                continue
            if min(deltas) <= 0:
                issue("false_superiority", path, "Proposed method does not strictly outperform every declared comparator; ties are not superiority.")
                continue
            report["computed_claims"].append({"id": key, "type": typ, "value": min(deltas), "unit": metric["unit"], "display": "Best among declared comparators", "proposed_result_id": proposed_id, "baseline_result_ids": baseline_ids})
            issue("limited_superiority_scope", path, "This checks only declared comparators and point estimates, not all published methods or statistical significance.", True)
            continue
        if not member(baseline_id, valid_results):
            issue("claim_result", path, "Baseline result is missing, unknown, or invalid.")
            continue
        b = valid_results[baseline_id]
        if not comparable(p, b, path):
            continue
        if p["method_id"] == b["method_id"] and not claim.get("within_method", False):
            issue("same_method_claim", path, "Methods are identical; for an explicit within-method comparison declare within_method:true.")
            continue
        pv, bv = p["value"], b["value"]
        if typ in {"relative_improvement", "reduction"} and bv <= 0:
            issue("invalid_denominator", path, "Relative improvement/reduction requires a strictly positive baseline; choose an absolute difference otherwise.")
            continue
        if typ == "relative_improvement":
            value, unit = (pv - bv) / bv * 100 * (1 if direction == "higher" else -1), "%"
        elif typ == "absolute_difference":
            value, unit = pv - bv, metric["unit"]
        elif typ == "percentage_point_difference":
            if metric["unit"] != "percent":
                issue("percentage_point_unit", path, "Percentage-point difference requires unit percent (e.g. 70, not 0.70). Convert fraction values explicitly first.")
                continue
            value, unit = pv - bv, "pp"
        elif typ == "speedup":
            if direction != "lower" or not member(metric["unit"], {"seconds", "milliseconds", "microseconds", "minutes", "hours", "s", "ms", "us"}):
                issue("speedup_metric", path, "Speedup uses positive elapsed-time values and a lower-is-better time metric.")
                continue
            if pv <= 0 or bv <= 0:
                issue("invalid_denominator", path, "Speedup requires positive baseline and proposed times.")
                continue
            value, unit = bv / pv, "x"
        else:
            if direction != "lower" or pv < 0:
                issue("reduction_metric", path, "Reduction requires a nonnegative lower-is-better metric.")
                continue
            value, unit = (bv - pv) / bv * 100, "%"
        if not finite(value):
            issue("nonfinite_claim", path, "Claim arithmetic overflowed; use finite well-scaled inputs.")
            continue
        decimals = claim.get("decimals", 1)
        if not isinstance(decimals, int) or isinstance(decimals, bool) or not 0 <= decimals <= 6:
            issue("claim_precision", path + ".decimals", "decimals must be an integer from 0 to 6.")
            continue
        if "display_value" in claim:
            stated = claim["display_value"]
            if not finite(stated) or not math.isclose(stated, round(value, decimals), abs_tol=1e-9, rel_tol=1e-12):
                issue("claim_arithmetic", path + ".display_value", f"Declared display value disagrees with computed {value:.{decimals}f} {unit}.")
        display = f"{value:.{decimals}f}{'%' if unit == '%' else '×' if unit == 'x' else ' ' + unit}"
        report["computed_claims"].append({"id": key, "type": typ, "value": value, "unit": unit, "display": display, "baseline_result_id": baseline_id, "proposed_result_id": proposed_id})

    for i, chart in objects(spec.get("charts", []), "charts"):
        path = f"charts[{i}]"
        mid = chart.get("metric_id")
        if not member(mid, metrics):
            issue("chart_metric", path + ".metric_id", "Declare a known metric_id for every quantitative chart.")
        tradeoff = chart.get("comparison_mode") == "tradeoff"
        if tradeoff and (chart.get("type") != "scatter" or not member(chart.get("x_metric_id"), metrics)):
            issue("tradeoff_axes", path, "Tradeoff comparison needs a scatter chart with a sourced quantitative x metric.")
            tradeoff = False
        if tradeoff:
            issue("tradeoff_budget", path, "Different budgets may be shown as a labeled tradeoff; matched-budget improvement claims still require matching contexts.", True)
        peers = {}
        for j, series in objects(chart.get("series", []), path + ".series"):
            sp = f"{path}.series[{j}]"
            values, ids = series.get("values"), series.get("result_ids")
            if not isinstance(values, list) or not isinstance(ids, list) or len(values) != len(ids):
                issue("chart_linkage", sp, "values and result_ids must be equal-length arrays; every plotted value needs evidence.")
                continue
            categories = chart.get("categories")
            if isinstance(categories, list) and len(categories) != len(values):
                issue("chart_length", sp, "categories must align with every series value.")
            if member(chart.get("type"), {"line", "scatter"}):
                xs = series.get("x_values", chart.get("x_values"))
                if not isinstance(xs, list) or len(xs) != len(values) or any(not finite(x) for x in xs):
                    issue("chart_x_values", path + ".x_values", "Line/scatter x_values must be finite and align with series values.")
                elif "x_metric_id" in chart:
                    xmid = chart["x_metric_id"]
                    xids = series.get("x_result_ids")
                    if not member(xmid, metrics) or not isinstance(xids, list) or len(xids) != len(xs):
                        issue("chart_x_linkage", sp, "A quantitative x metric requires known x_metric_id and aligned x_result_ids.")
                    else:
                        for k, (x, xid) in enumerate(zip(xs, xids)):
                            xr = results.get(xid) if isinstance(xid, str) else None
                            if xr is None or xr.get("metric_id") != xmid or not finite(xr.get("value")) or not math.isclose(x, xr["value"], rel_tol=1e-12, abs_tol=1e-12):
                                issue("chart_x_mismatch", f"{sp}.x_values[{k}]", "Quantitative x coordinate must equal its linked evidence result and metric.")
                            yr = results.get(ids[k]) if isinstance(ids[k], str) else None
                            if xr and yr and (xr.get("method_id") != yr.get("method_id") or xr.get("comparison") != yr.get("comparison")):
                                issue("chart_xy_context", f"{sp}.x_values[{k}]", "X and Y results for one point must describe the same method and comparison context.")
                elif not member(chart.get("x_source_id"), sources) or not nonempty(chart.get("x_source_location")):
                    issue("chart_x_source", path, "Independent-variable x coordinates require x_source_id and an exact x_source_location.")
            errors = series.get("errors")
            if errors is not None and (not isinstance(errors, list) or len(errors) != len(values)):
                issue("chart_error_length", sp + ".errors", "Error bars must align with values.")
                errors = None
            for k, (value, rid) in enumerate(zip(values, ids)):
                vp = f"{sp}.values[{k}]"
                result = results.get(rid) if isinstance(rid, str) else None
                if result is None:
                    issue("chart_result", vp, "Unknown result_id.")
                    continue
                if result.get("metric_id") != mid:
                    issue("chart_metric", vp, "Plotted result metric differs from chart metric.")
                if result.get("missing") is True:
                    if value is not None:
                        issue("missing_imputation", vp, "Keep missing plotted values null; do not replace them with zero.")
                elif not finite(value) or not finite(result.get("value")) or not math.isclose(value, result["value"], rel_tol=1e-12, abs_tol=1e-12):
                    issue("chart_value_mismatch", vp, "Plotted number does not equal its evidence result.")
                if k in peers:
                    comparable(result, peers[k], vp, for_claim=False, tradeoff=tradeoff)
                else:
                    peers[k] = result
                if errors is not None and k < len(errors) and errors[k] is not None:
                    u = result.get("uncertainty")
                    if not isinstance(u, dict) or not finite(u.get("value")) or not finite(errors[k]) or not math.isclose(errors[k], u["value"], rel_tol=1e-12, abs_tol=1e-12):
                        issue("chart_error_mismatch", vp, "Symmetric plotted errors must equal the sourced uncertainty.value; asymmetric intervals need a custom renderer.")
        if "claim_id" in chart:
            if not member(chart["claim_id"], claims):
                issue("chart_claim", path + ".claim_id", "Reference a declared claim.")
            else:
                claim = claims[chart["claim_id"]]
                proposed_id = claim.get("proposed_result_id")
                proposed = results.get(proposed_id) if isinstance(proposed_id, str) else None
                if proposed:
                    claim_metric = proposed.get("metric_id")
                    fields = []
                    if claim_metric == mid:
                        fields.append("result_ids")
                    if claim_metric == chart.get("x_metric_id"):
                        fields.append("x_result_ids")
                    if not fields:
                        issue("chart_claim_metric", path + ".claim_id", "The annotated claim's metric must be shown on this chart's value or quantitative x axis.")
                    else:
                        baseline_ids = claim.get("baseline_result_ids", []) if claim.get("type") == "all_methods_superiority" else [claim.get("baseline_result_id")]
                        if isinstance(baseline_ids, list) and all(isinstance(rid, str) for rid in baseline_ids):
                            required = {proposed_id, *baseline_ids}
                            plotted_axes = []
                            for field in fields:
                                plotted = set()
                                chart_series = chart.get("series", [])
                                for series in chart_series if isinstance(chart_series, list) else []:
                                    if isinstance(series, dict) and isinstance(series.get(field), list):
                                        plotted.update(rid for rid in series[field] if isinstance(rid, str))
                                plotted_axes.append(plotted)
                            if not any(required <= plotted for plotted in plotted_axes):
                                issue("chart_claim_scope", path + ".claim_id", "Every proposed and baseline result supporting this annotation must be plotted on the corresponding metric axis of this chart.")
    report["valid"] = not report["errors"]
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        report = validate_spec(spec)
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [{"code": "input_error", "path": str(args.spec), "message": str(exc)}], "warnings": [], "computed_claims": []}, indent=2))
        return 2
    serialized = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
