from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    n: int
    successes: int
    curves: int
    total_seconds: float

    @property
    def expected_time(self) -> float:
        if self.successes == 0:
            return float("inf")
        return self.total_seconds / self.successes


@dataclass(frozen=True)
class OptimizationConfig:
    b1_min: float = 1e3
    b1_max: float = 1e9
    ratio_max: float = 100.0
    curves_per_n: int = 50
    popsize: int = 16
    maxiter: int = 25
    seed: int = 42


@dataclass(frozen=True)
class OptimizationResult:
    b1: int
    b2: int
    objective: float
