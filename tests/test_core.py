import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from learning_experiment_platform import core


COMPLETE_RECORDS = [
    {"participant_id": "T1", "assigned_group": "treatment", "pre": 60, "post": 78},
    {"participant_id": "T2", "assigned_group": "treatment", "pre": 64, "post": 80},
    {"participant_id": "T3", "assigned_group": "treatment", "pre": 68, "post": 82},
    {"participant_id": "C1", "assigned_group": "control", "pre": 61, "post": 68},
    {"participant_id": "C2", "assigned_group": "control", "pre": 65, "post": 70},
    {"participant_id": "C3", "assigned_group": "control", "pre": 69, "post": 72},
]

ATTRITION_RECORDS = [
    *COMPLETE_RECORDS[:3],
    COMPLETE_RECORDS[3],
    {"participant_id": "C2", "assigned_group": "control", "pre": 65, "post": None},
    COMPLETE_RECORDS[5],
]


class CoreTests(unittest.TestCase):
    def test_assignment_is_reproducible(self):
        ids = list(range(10))
        self.assertEqual(core.assign(ids, seed=7), core.assign(ids, seed=7))

    def test_assignment_is_balanced(self):
        assignment = core.assign(range(9), seed=3)
        counts = {
            group: list(assignment.values()).count(group)
            for group in core.GROUPS
        }
        self.assertLessEqual(abs(counts["treatment"] - counts["control"]), 1)

    def test_assignment_rejects_duplicates(self):
        with self.assertRaises(ValueError):
            core.assign(["A", "A"])

    def test_assignment_requires_two_participants(self):
        with self.assertRaises(ValueError):
            core.assign(["A"])

    def test_mean_rejects_non_finite_values(self):
        with self.assertRaises(ValueError):
            core.mean([1, math.nan])

    def test_mean_rejects_boolean_values(self):
        with self.assertRaises(ValueError):
            core.mean([1, True])

    def test_gain_is_paired_post_minus_pre(self):
        self.assertEqual(core.gain([3, 5], [2, 1]), [1, 4])

    def test_gain_requires_equal_lengths(self):
        with self.assertRaises(ValueError):
            core.gain([3], [1, 2])

    def test_cohens_d_positive_when_treatment_is_higher(self):
        self.assertGreater(core.cohens_d([8, 9, 10], [5, 6, 7]), 0)

    def test_cohens_d_returns_none_when_pooled_sd_is_zero(self):
        self.assertIsNone(core.cohens_d([10, 10, 10], [5, 5, 5]))

    def test_cohens_d_requires_two_per_group(self):
        with self.assertRaises(ValueError):
            core.cohens_d([1], [0, 1])

    def test_bootstrap_ci_is_reproducible(self):
        first = core.bootstrap_mean_difference_ci(
            [8, 9, 10], [5, 6, 7], iterations=300, seed=5
        )
        second = core.bootstrap_mean_difference_ci(
            [8, 9, 10], [5, 6, 7], iterations=300, seed=5
        )
        self.assertEqual(first, second)

    def test_bootstrap_ci_orders_bounds(self):
        low, high = core.bootstrap_mean_difference_ci(
            [8, 9, 10], [5, 6, 7], iterations=300, seed=5
        )
        self.assertLessEqual(low, high)

    def test_bootstrap_ci_validates_confidence(self):
        with self.assertRaises(ValueError):
            core.bootstrap_mean_difference_ci(
                [1, 2], [0, 1], confidence=1.0
            )

    def test_experiment_record_is_serializable_metadata(self):
        record = core.experiment_record(
            "EXP-001",
            "Retrieval practice improves delayed performance.",
            "post-test score",
            assignment_seed=17,
        )
        self.assertEqual(record["assignment_seed"], 17)
        self.assertEqual(record["experiment_id"], "EXP-001")

    def test_experiment_record_requires_text_fields(self):
        with self.assertRaises(ValueError):
            core.experiment_record("", "hypothesis", "outcome")

    def test_analyze_experiment_counts_groups(self):
        result = core.analyze_experiment(
            COMPLETE_RECORDS,
            bootstrap_iterations=300,
        )
        self.assertEqual(result["participant_count"], 6)
        self.assertEqual(
            result["assigned_counts"],
            {"treatment": 3, "control": 3},
        )
        self.assertEqual(
            result["observed_counts"],
            {"treatment": 3, "control": 3},
        )

    def test_analyze_experiment_calculates_gains(self):
        result = core.analyze_experiment(
            COMPLETE_RECORDS,
            bootstrap_iterations=300,
        )
        self.assertAlmostEqual(result["gain_means"]["treatment"], 16.0)
        self.assertAlmostEqual(result["gain_means"]["control"], 5.0)
        self.assertAlmostEqual(result["gain_mean_difference"], 11.0)

    def test_analyze_experiment_produces_effects_and_ci(self):
        result = core.analyze_experiment(
            COMPLETE_RECORDS,
            bootstrap_iterations=300,
            bootstrap_seed=9,
        )
        self.assertIsNotNone(result["post_cohens_d"])
        self.assertIsNotNone(result["gain_cohens_d"])
        self.assertEqual(len(result["post_mean_difference_ci"]), 2)
        self.assertEqual(len(result["gain_mean_difference_ci"]), 2)

    def test_analyze_experiment_reports_attrition(self):
        result = core.analyze_experiment(
            ATTRITION_RECORDS,
            bootstrap_iterations=300,
        )
        self.assertEqual(result["attrition_counts"]["control"], 1)
        self.assertAlmostEqual(result["attrition_rates"]["control"], 1 / 3)
        self.assertIn("attrition_present", result["analysis_flags"])
        self.assertIn(
            "differential_attrition_review",
            result["analysis_flags"],
        )

    def test_analyze_experiment_keeps_assignment_groups(self):
        result = core.analyze_experiment(
            COMPLETE_RECORDS,
            assignment_method="seeded_random",
            bootstrap_iterations=300,
        )
        self.assertEqual(result["assignment_method"], "seeded_random")
        self.assertEqual(
            result["analysis_method"],
            "complete_case_by_assigned_group",
        )

    def test_analyze_experiment_rejects_duplicate_ids(self):
        records = [dict(record) for record in COMPLETE_RECORDS]
        records[1]["participant_id"] = records[0]["participant_id"]
        with self.assertRaises(ValueError):
            core.analyze_experiment(records)

    def test_analyze_experiment_rejects_invalid_group(self):
        records = [dict(record) for record in COMPLETE_RECORDS]
        records[0]["assigned_group"] = "other"
        with self.assertRaises(ValueError):
            core.analyze_experiment(records)

    def test_analyze_experiment_rejects_non_finite_pre(self):
        records = [dict(record) for record in COMPLETE_RECORDS]
        records[0]["pre"] = math.inf
        with self.assertRaises(ValueError):
            core.analyze_experiment(records)

    def test_small_observed_group_marks_effect_unestimable(self):
        records = [
            {"participant_id": "T1", "assigned_group": "treatment", "pre": 1, "post": 2},
            {"participant_id": "T2", "assigned_group": "treatment", "pre": 2, "post": None},
            {"participant_id": "C1", "assigned_group": "control", "pre": 1, "post": 1},
            {"participant_id": "C2", "assigned_group": "control", "pre": 2, "post": 2},
        ]
        result = core.analyze_experiment(records, bootstrap_iterations=300)
        self.assertIsNone(result["post_cohens_d"])
        self.assertIn("small_observed_group", result["analysis_flags"])
        self.assertIn(
            "post_effect_not_estimable",
            result["analysis_flags"],
        )


if __name__ == "__main__":
    unittest.main()
