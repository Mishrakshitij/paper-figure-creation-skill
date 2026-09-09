"""Adversarial and numerical tests. All values below are synthetic test fixtures."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/paper-figure-creation/scripts/validate_evidence.py"
module_spec = importlib.util.spec_from_file_location("validate_evidence", SCRIPT)
validator = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(validator)


def fixture():
    return {
        "version": 1, "kind": "teaser", "status": "draft",
        "figure": {"subtitle": "SYNTHETIC DATA — test fixture"},
        "provenance": {"data_status": "synthetic", "sources": [{
            "id": "fixture", "kind": "synthetic", "locator": "tests/test_evidence.py", "location": "fixture()"}]},
        "evidence": {
            "metrics": [{"id": "accuracy", "label": "Accuracy", "direction": "higher", "unit": "percent"}],
            "results": [
                {"id": "base", "method_id": "baseline", "metric_id": "accuracy", "value": 70,
                 "comparison": {"dataset": "toy", "split": "test", "budget": "same 10 epochs"}, "source_id": "fixture"},
                {"id": "ours", "method_id": "proposed", "metric_id": "accuracy", "value": 91,
                 "comparison": {"dataset": "toy", "split": "test", "budget": "same 10 epochs"}, "source_id": "fixture"}],
            "claims": [{"id": "gain", "type": "relative_improvement", "baseline_result_id": "base",
                        "proposed_result_id": "ours", "display_value": 30, "decimals": 1}]},
        "charts": [{"type": "dot", "metric_id": "accuracy", "categories": ["toy"], "series": [
            {"id": "baseline", "label": "Baseline", "values": [70], "result_ids": ["base"]},
            {"id": "proposed", "label": "Proposed", "values": [91], "result_ids": ["ours"]}], "claim_id": "gain"}]
    }


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.spec = fixture()

    def report(self):
        return validator.validate_spec(self.spec)

    def codes(self):
        return {e["code"] for e in self.report()["errors"]}

    def test_relative_improvement_is_30_percent(self):
        report = self.report()
        self.assertTrue(report["valid"], report)
        self.assertAlmostEqual(report["computed_claims"][0]["value"], 30)
        self.assertEqual(report["computed_claims"][0]["display"], "30.0%")

    def test_percentage_points_are_not_relative_percent(self):
        c = self.spec["evidence"]["claims"][0]
        c.update(type="percentage_point_difference", display_value=21)
        self.assertTrue(self.report()["valid"])
        self.assertEqual(self.report()["computed_claims"][0]["unit"], "pp")
        c["display_value"] = 30
        self.assertIn("claim_arithmetic", self.codes())

    def test_percentage_points_require_percent_scale(self):
        self.spec["evidence"]["metrics"][0]["unit"] = "fraction"
        self.spec["evidence"]["claims"][0]["type"] = "percentage_point_difference"
        self.assertIn("percentage_point_unit", self.codes())

    def test_reversed_metric_direction_changes_improvement_sign(self):
        self.spec["evidence"]["metrics"][0]["direction"] = "lower"
        self.assertIn("claim_arithmetic", self.codes())
        self.assertAlmostEqual(self.report()["computed_claims"][0]["value"], -30)

    def test_invalid_metric_direction_is_rejected(self):
        self.spec["evidence"]["metrics"][0]["direction"] = "auto"
        self.assertIn("metric_direction", self.codes())

    def test_nonfinite_and_boolean_values_are_rejected(self):
        for value in (math.nan, math.inf, -math.inf, True):
            with self.subTest(value=value):
                self.spec["evidence"]["results"][0]["value"] = value
                self.assertIn("nonfinite_value", self.codes())

    def test_zero_baseline_cannot_generate_infinite_improvement(self):
        self.spec["evidence"]["results"][0]["value"] = 0
        self.spec["charts"][0]["series"][0]["values"] = [0]
        self.assertIn("invalid_denominator", self.codes())

    def test_speedup_is_ratio_of_elapsed_times(self):
        self.spec["evidence"]["metrics"][0].update(unit="seconds", direction="lower")
        self.spec["evidence"]["results"][0]["value"] = 100
        self.spec["evidence"]["results"][1]["value"] = 50
        self.spec["charts"][0]["series"][0]["values"] = [100]
        self.spec["charts"][0]["series"][1]["values"] = [50]
        c = self.spec["evidence"]["claims"][0]
        c.update(type="speedup", display_value=2)
        self.assertTrue(self.report()["valid"])
        self.assertEqual(self.report()["computed_claims"][0]["display"], "2.0×")
        c.update(type="reduction", display_value=50)
        self.assertTrue(self.report()["valid"])
        self.assertEqual(self.report()["computed_claims"][0]["display"], "50.0%")

    def test_accuracy_ratio_cannot_be_called_speedup(self):
        self.spec["evidence"]["claims"][0]["type"] = "speedup"
        self.assertIn("speedup_metric", self.codes())

    def test_incomparable_split_budget_dataset_and_protocol_fail(self):
        for field, value in (("split", "validation"), ("budget", "100 epochs"), ("dataset", "another dataset"), ("protocol", "extra pretraining")):
            with self.subTest(field=field):
                self.spec = fixture()
                self.spec["evidence"]["results"][1]["comparison"][field] = value
                self.assertIn("incomparable_context", self.codes())

    def test_missing_context_is_not_guessed(self):
        del self.spec["evidence"]["results"][0]["comparison"]["budget"]
        self.assertIn("comparison_context", self.codes())

    def test_source_requires_exact_location(self):
        del self.spec["provenance"]["sources"][0]["location"]
        self.assertIn("source_location", self.codes())

    def test_unknown_source_is_rejected(self):
        self.spec["evidence"]["results"][0]["source_id"] = "imagined"
        self.assertIn("unknown_source", self.codes())

    def test_synthetic_cannot_be_final_or_unlabeled(self):
        self.spec["status"] = "final"
        self.spec["figure"]["subtitle"] = "Results"
        self.assertTrue({"synthetic_final", "synthetic_label"}.issubset(self.codes()))

    def test_reported_status_cannot_hide_synthetic_source(self):
        self.spec["provenance"]["data_status"] = "reported"
        self.assertIn("synthetic_disguised", self.codes())

    def test_missing_result_stays_a_gap_and_cannot_support_claim(self):
        self.spec["evidence"]["results"][0].update(value=None, missing=True)
        self.spec["charts"][0]["series"][0]["values"] = [None]
        self.assertIn("missing_claim", self.codes())
        self.spec["evidence"]["claims"] = []
        del self.spec["charts"][0]["claim_id"]
        self.assertTrue(self.report()["valid"], self.report())
        self.spec["charts"][0]["series"][0]["values"] = [0]
        self.assertIn("missing_imputation", self.codes())

    def test_missing_result_cannot_be_encoded_as_zero(self):
        self.spec["evidence"]["results"][0].update(value=0, missing=True)
        self.assertIn("missing_imputation", self.codes())

    def test_plotted_value_cannot_diverge_from_evidence(self):
        self.spec["charts"][0]["series"][1]["values"] = [99]
        self.assertIn("chart_value_mismatch", self.codes())

    def test_unknown_chart_result_and_unlinked_values_fail(self):
        self.spec["charts"][0]["series"][0]["result_ids"] = ["unknown"]
        self.assertIn("chart_result", self.codes())
        self.spec["charts"][0]["series"][0]["result_ids"] = []
        self.assertIn("chart_linkage", self.codes())

    def test_chart_annotation_cannot_claim_an_unplotted_metric(self):
        self.spec["evidence"]["metrics"].append({"id": "latency", "direction": "lower", "unit": "milliseconds"})
        for i, (rid, number) in enumerate((("base_time", 100), ("ours_time", 70))):
            r = copy.deepcopy(self.spec["evidence"]["results"][i])
            r.update(id=rid, metric_id="latency", value=number)
            self.spec["evidence"]["results"].append(r)
        self.spec["evidence"]["claims"][0].update(type="reduction", baseline_result_id="base_time", proposed_result_id="ours_time")
        self.assertIn("chart_claim_metric", self.codes())

    def test_chart_annotation_requires_its_specific_results_to_be_plotted(self):
        hidden = copy.deepcopy(self.spec["evidence"]["results"][1])
        hidden.update(id="hidden_ours", method_id="another_proposed_variant", value=84)
        self.spec["evidence"]["results"].append(hidden)
        self.spec["evidence"]["claims"][0].update(proposed_result_id="hidden_ours", display_value=20)
        self.assertIn("chart_claim_scope", self.codes())

    def test_scatter_annotation_can_claim_its_sourced_x_metric(self):
        chart = self.spec["charts"][0]
        chart.update(type="scatter", x_metric_id="params")
        self.spec["evidence"]["metrics"].append({"id": "params", "direction": "lower", "unit": "millions"})
        for i, (rid, number) in enumerate((("base_params", 100), ("ours_params", 5))):
            r = copy.deepcopy(self.spec["evidence"]["results"][i])
            r.update(id=rid, metric_id="params", value=number)
            self.spec["evidence"]["results"].append(r)
            chart["series"][i].update(x_values=[number], x_result_ids=[rid])
        self.spec["evidence"]["claims"][0].update(type="reduction", baseline_result_id="base_params", proposed_result_id="ours_params", display_value=95)
        self.assertTrue(self.report()["valid"], self.report())

    def test_all_method_claim_cannot_omit_stronger_baseline(self):
        stronger = copy.deepcopy(self.spec["evidence"]["results"][0])
        stronger.update(id="stronger", method_id="stronger", value=93)
        self.spec["evidence"]["results"].append(stronger)
        self.spec["evidence"]["claims"] = [{"id": "gain", "type": "all_methods_superiority", "proposed_result_id": "ours", "baseline_result_ids": ["base"]}]
        self.assertIn("superiority_scope", self.codes())
        self.spec["evidence"]["claims"][0]["baseline_result_ids"].append("stronger")
        self.assertIn("false_superiority", self.codes())

    def test_tie_is_not_strict_superiority(self):
        self.spec["evidence"]["results"][0]["value"] = 91
        self.spec["charts"][0]["series"][0]["values"] = [91]
        self.spec["evidence"]["claims"] = [{"id": "gain", "type": "all_methods_superiority", "proposed_result_id": "ours", "baseline_result_ids": ["base"]}]
        self.assertIn("false_superiority", self.codes())

    def test_unreported_uncertainty_is_a_warning_not_invented(self):
        report = self.report()
        self.assertTrue(report["valid"])
        self.assertIn("uncertainty_unreported", {x["code"] for x in report["warnings"]})

    def test_fake_ci_and_error_bars_fail(self):
        self.spec["evidence"]["results"][0]["uncertainty"] = {"type": "ci", "value": 2}
        self.assertTrue({"uncertainty_source", "ci_method", "ci_level"}.issubset(self.codes()))
        self.spec["evidence"]["results"][0]["uncertainty"] = {
            "type": "sd", "value": 2, "source_id": "fixture", "source_location": "fixture SD", "n": 3, "variation": "seeds"}
        self.spec["charts"][0]["series"][0]["errors"] = [2]
        self.assertTrue(self.report()["valid"])
        self.spec["charts"][0]["series"][0]["errors"] = [0.2]
        self.assertIn("chart_error_mismatch", self.codes())

    def test_ci_level_uses_fraction_and_extent_cannot_be_negative(self):
        self.spec["evidence"]["results"][0]["uncertainty"] = {
            "type": "ci", "value": -1, "source_id": "fixture", "source_location": "fixture CI", "level": 95, "method": "synthetic fixture", "n": 1}
        self.assertTrue({"uncertainty_extent", "ci_level", "uncertainty_n"}.issubset(self.codes()))

    def test_quantitative_x_coordinates_have_independent_provenance(self):
        chart = self.spec["charts"][0]
        chart.update(type="scatter", x_metric_id="params")
        self.spec["evidence"]["metrics"].append({"id": "params", "direction": "lower", "unit": "millions"})
        for i, (rid, number) in enumerate((("base_params", 100), ("ours_params", 5))):
            r = copy.deepcopy(self.spec["evidence"]["results"][i])
            r.update(id=rid, metric_id="params", value=number)
            self.spec["evidence"]["results"].append(r)
            chart["series"][i].update(x_values=[number], x_result_ids=[rid])
        self.assertTrue(self.report()["valid"], self.report())
        chart["series"][1]["x_values"] = [1]
        self.assertIn("chart_x_mismatch", self.codes())

    def test_x_and_y_cannot_mix_different_method_runs(self):
        chart = self.spec["charts"][0]
        chart.update(type="scatter", x_metric_id="accuracy")
        chart["series"][0].update(x_values=[91], x_result_ids=["ours"])
        chart["series"][1].update(x_values=[70], x_result_ids=["base"])
        self.assertIn("chart_xy_context", self.codes())

    def test_sourced_tradeoff_allows_budget_difference_but_not_gain_claim(self):
        chart = self.spec["charts"][0]
        chart.update(type="scatter", x_metric_id="params", comparison_mode="tradeoff")
        self.spec["evidence"]["metrics"].append({"id": "params", "direction": "lower", "unit": "millions"})
        self.spec["evidence"]["results"][1]["comparison"]["budget"] = "5M trainable parameters"
        for i, (rid, number) in enumerate((("base_params", 100), ("ours_params", 5))):
            r = copy.deepcopy(self.spec["evidence"]["results"][i])
            r.update(id=rid, metric_id="params", value=number)
            self.spec["evidence"]["results"].append(r)
            chart["series"][i].update(x_values=[number], x_result_ids=[rid])
        self.assertIn("incomparable_context", self.codes())
        self.spec["evidence"]["claims"] = []
        del chart["claim_id"]
        self.assertTrue(self.report()["valid"], self.report())

    def test_line_checkpoint_schedule_needs_source(self):
        self.spec["charts"][0].update(type="line", x_values=[1])
        self.assertIn("chart_x_source", self.codes())
        self.spec["charts"][0].update(x_source_id="fixture", x_source_location="epoch schedule")
        self.assertTrue(self.report()["valid"])

    def test_method_without_results_still_needs_source(self):
        self.spec.update(kind="method", evidence={}, charts=[])
        self.assertTrue(self.report()["valid"])
        self.spec["provenance"]["sources"] = []
        self.assertIn("missing_sources", self.codes())

    def test_duplicate_ids_fail(self):
        self.spec["evidence"]["results"].append(copy.deepcopy(self.spec["evidence"]["results"][0]))
        self.assertIn("duplicate_id", self.codes())

    def test_malformed_shapes_and_unhashable_refs_return_errors(self):
        self.assertFalse(validator.validate_spec([])["valid"])
        self.spec["kind"] = []
        self.spec["evidence"]["results"][0]["source_id"] = []
        self.spec["evidence"]["claims"][0]["proposed_result_id"] = []
        self.spec["charts"][0]["series"].append("invalid")
        self.assertFalse(self.report()["valid"])

    def test_cli_exit_status_and_machine_readable_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            path.write_text(json.dumps(self.spec), encoding="utf-8")
            process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertTrue(json.loads(process.stdout)["valid"])
            self.spec["evidence"]["claims"][0]["display_value"] = 999
            path.write_text(json.dumps(self.spec), encoding="utf-8")
            process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 1)
            path.write_text("{", encoding="utf-8")
            process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)


if __name__ == "__main__":
    unittest.main()
