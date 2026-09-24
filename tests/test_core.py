import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from learning_experiment_platform import core


class CoreTests(unittest.TestCase):
    def test_assignment_and_effect_size(self):
        assignment = core.assign(range(6))
        self.assertEqual(set(assignment.values()), {"treatment", "control"})
        self.assertGreater(core.cohens_d([8, 9, 10], [5, 6, 7]), 0)

    def test_gain_requires_paired_values(self):
        self.assertEqual(core.gain([3, 5], [2, 1]), [1, 4])
        with self.assertRaises(ValueError):
            core.gain([3], [1, 2])


if __name__ == "__main__":
    unittest.main()
