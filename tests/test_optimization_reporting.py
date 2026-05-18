from __future__ import annotations

import unittest

from ecm_optimizer.utils.optimization_reporting import _log10_search_projection


class OptimizationReportingProjectionTests(unittest.TestCase):
    def test_log10_search_projection_uses_optimizer_coordinates(self) -> None:
        log_b1, log_b2, log_ratio, fitness = _log10_search_projection(
            [
                {"kind": "evaluation", "b1": 100, "b2": 10000, "fitness": 3.0},
                {"kind": "evaluation", "b1": 1000, "b2": 1000000, "fitness": 1.5},
            ]
        )

        self.assertEqual(log_b1, [2.0, 3.0])
        self.assertEqual(log_b2, [4.0, 6.0])
        self.assertEqual(log_ratio, [2.0, 3.0])
        self.assertEqual(fitness, [3.0, 1.5])

    def test_log10_search_projection_skips_non_positive_values(self) -> None:
        log_b1, log_b2, log_ratio, fitness = _log10_search_projection(
            [
                {"kind": "evaluation", "b1": 0, "b2": 1000, "fitness": 9.0},
                {"kind": "evaluation", "b1": 10, "b2": 1000, "fitness": 2.0},
            ]
        )

        self.assertEqual(log_b1, [1.0])
        self.assertEqual(log_b2, [3.0])
        self.assertEqual(log_ratio, [2.0])
        self.assertEqual(fitness, [2.0])


if __name__ == "__main__":
    unittest.main()
