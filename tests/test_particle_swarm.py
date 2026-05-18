from __future__ import annotations

import math
import unittest
from unittest.mock import patch

from ecm_optimizer.models import OptimizationConfig
from ecm_optimizer.optimizers.heuristic_common import EvaluatedPoint
from ecm_optimizer.optimizers.particle_swarm import ParticleSwarmOptimizer, _clamp_position_and_velocity


class ParticleSwarmBoundaryTests(unittest.TestCase):
    def test_clamp_damps_outward_velocity_at_upper_bound(self) -> None:
        position, velocity = _clamp_position_and_velocity(
            position=(3.2, 4.8),
            velocity=(0.6, -0.2),
            bounds=((1.0, 3.0), (2.0, 5.0)),
            boundary_damping=0.0,
        )

        self.assertEqual(position, (3.0, 4.8))
        self.assertEqual(velocity, (-0.0, -0.2))

    def test_clamp_reflects_with_configured_damping(self) -> None:
        position, velocity = _clamp_position_and_velocity(
            position=(0.5, 5.5),
            velocity=(-0.8, 1.2),
            bounds=((1.0, 3.0), (2.0, 5.0)),
            boundary_damping=0.25,
        )

        self.assertEqual(position, (1.0, 5.0))
        self.assertEqual(velocity, (0.2, -0.3))

    def test_optimizer_does_not_keep_outward_velocity_after_boundary_hit(self) -> None:
        calls: list[tuple[float, float]] = []

        def fake_candidate_from_rng(_rng, _config):
            return (1.0, 1.0)

        def fake_evaluate_candidate(*, x_log, ecm_bin, numbers, config, progress):
            calls.append(x_log)
            return EvaluatedPoint(x=x_log, score=math.dist(x_log, (2.0, 2.0)), eval_id=len(calls))

        config = OptimizationConfig(
            b1_min=10.0,
            b1_max=100.0,
            b2_min=10.0,
            b2_max=100.0,
            popsize=1,
            maxiter=1,
            seed=1,
            method_params={
                "pso": {
                    "swarm_size": 1,
                    "iterations": 1,
                    "inertia": 1.0,
                    "cognitive": 0.0,
                    "social": 10.0,
                    "velocity_scale": 10.0,
                    "boundary_damping": 0.0,
                }
            },
        )

        with patch("ecm_optimizer.optimizers.particle_swarm.candidate_from_rng", fake_candidate_from_rng), patch(
            "ecm_optimizer.optimizers.particle_swarm.evaluate_candidate", fake_evaluate_candidate
        ):
            result = ParticleSwarmOptimizer().optimize(ecm_bin="ecm", numbers=[15], config=config)

        self.assertLessEqual(result.b1, int(config.b1_max))
        self.assertLessEqual(result.b2, int(config.b2_max))
        self.assertGreaterEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
