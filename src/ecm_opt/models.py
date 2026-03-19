from dataclasses import dataclass
import os


NO_SUCCESS_PENALTY_MULTIPLIER = 10.0


def resolve_workers(workers: int | None) -> int:
    """Нормализовать число процессов, запрошенное пользователем.

    Args:
        workers: Желаемое число worker-процессов. Значения `None` и `0`
            означают последовательный режим, отрицательные — все доступные CPU.

    Returns:
        Эффективное число worker-процессов для выполнения задачи.
    """
    if workers is None or workers == 0:
        return 1
    if workers < 0:
        return os.cpu_count() or 1
    return workers


@dataclass(frozen=True)
class EvaluationResult:
    """Статистика многократного запуска ECM для одного числа `n`."""

    n: int
    successes: int
    curves: int
    total_seconds: float

    @property
    def expected_time(self) -> float:
        """Оценить ожидаемое время успеха для данного `n`.

        Returns:
            Среднее время на успешное нахождение множителя либо штрафная оценка,
            если успехов не было.
        """
        if self.successes == 0:
            return self.total_seconds * NO_SUCCESS_PENALTY_MULTIPLIER
        return self.total_seconds / self.successes


@dataclass(frozen=True)
class OptimizationConfig:
    """Параметры запуска дифференциальной эволюции и измерений ECM."""

    b1_min: float = 1e3
    b1_max: float = 1e9
    ratio_max: float = 100.0
    curves_per_n: int = 50
    popsize: int = 16
    maxiter: int = 25
    seed: int = 42
    curve_timeout_sec: float | None = None
    workers: int = 1
    verbose: bool = False


@dataclass(frozen=True)
class OptimizationResult:
    """Лучшее решение, найденное оптимизатором."""

    b1: int
    b2: int
    objective: float
