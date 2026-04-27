from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from ecm_optimizer.core.fitness import fitness_with_stats
from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.utils.io_utils import write_json_atomic


def decode_candidate(x_log: tuple[float, float], config: OptimizationConfig) -> tuple[int, int]:
    """Преобразовать точку в логарифмическом пространстве в допустимые `(B1, B2)`."""
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])
    b1 = min(max(b1, int(config.b1_min)), int(config.b1_max))
    b2 = max(b2, b1, int(config.b2_min))
    b2 = min(b2, int(config.b2_max), int(b1 * config.ratio_max))
    return b1, b2


def candidate_from_rng(rng: random.Random, config: OptimizationConfig) -> tuple[float, float]:
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)
    return rng.uniform(low1, high1), rng.uniform(low2, high2)


@dataclass(frozen=True)
class EvaluatedPoint:
    x: tuple[float, float]
    score: float
    eval_id: int | None = None


@dataclass
class ProgressTracker:
    """Счётчик и форматированный вывод промежуточных этапов оптимизации."""

    method: str
    every: int = 5
    eval_count: int = 0
    best_score: float | None = None
    events: list[dict[str, float | int | str]] = field(default_factory=list)
    started_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    _start_monotonic: float = field(default_factory=time.perf_counter)
    _last_checkpoint_monotonic: float = 0.0

    def _elapsed_sec(self) -> float:
        return time.perf_counter() - self._start_monotonic

    def _timestamp_utc(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def on_evaluation(
        self,
        *,
        config: OptimizationConfig,
        x_log: tuple[float, float],
        score: float,
        metrics: dict[str, float | int] | None = None,
    ) -> None:
        self.eval_count += 1
        b1, b2 = decode_candidate(x_log, config)
        event: dict[str, float | int | str] = {
            "kind": "evaluation",
            "eval": self.eval_count,
            "b1": b1,
            "b2": b2,
            "fitness": score,
            "elapsed_sec": self._elapsed_sec(),
            "timestamp_utc": self._timestamp_utc(),
        }
        if metrics is not None:
            event.update(metrics)
            success_runs = metrics.get("success_runs")
            if isinstance(success_runs, int):
                event["successes"] = success_runs
        self.events.append(event)
        self._checkpoint(config=config)
        if not config.verbose:
            return
        if self.eval_count % self.every != 0:
            return
        print(
            f"[optimize:{self.method}] eval={self.eval_count} b1={b1} b2={b2} fitness={score}",
            flush=True,
        )

    def log_step(self, *, config: OptimizationConfig, message: str) -> None:
        self.events.append(
            {
                "kind": "step",
                "eval": self.eval_count,
                "message": message,
                "elapsed_sec": self._elapsed_sec(),
                "timestamp_utc": self._timestamp_utc(),
            }
        )
        self._checkpoint(config=config, force=True)
        if config.verbose:
            print(f"[optimize:{self.method}] {message}", flush=True)

    def on_new_best(
        self,
        *,
        config: OptimizationConfig,
        x_log: tuple[float, float],
        score: float,
        eval_id: int | None = None,
    ) -> None:
        if self.best_score is not None and score >= self.best_score:
            return
        self.best_score = score
        b1, b2 = decode_candidate(x_log, config)
        best_eval = self.eval_count if eval_id is None else eval_id
        self.events.append(
            {
                "kind": "new_best",
                "eval": best_eval,
                "b1": b1,
                "b2": b2,
                "fitness": score,
                "elapsed_sec": self._elapsed_sec(),
                "timestamp_utc": self._timestamp_utc(),
            }
        )
        self._checkpoint(config=config, force=True)
        if not config.verbose:
            return
        print(
            f"[optimize:{self.method}] new_best eval={best_eval} b1={b1} b2={b2} fitness={score}",
            flush=True,
        )

    def _checkpoint(self, *, config: OptimizationConfig, force: bool = False) -> None:
        checkpoint_cfg = config.method_params.get("_checkpoint", {})
        path = checkpoint_cfg.get("path")
        if not path:
            return
        now = time.perf_counter()
        min_interval_sec = float(checkpoint_cfg.get("min_interval_sec", 10.0))
        if not force and (now - self._last_checkpoint_monotonic) < min_interval_sec:
            return
        payload: dict[str, float | int | str | list[dict[str, float | int | str]] | None] = {
            "status": "in_progress",
            "method": self.method,
            "started_at_utc": self.started_at_utc,
            "updated_at_utc": self._timestamp_utc(),
            "eval_count": self.eval_count,
            "best_score": self.best_score,
            "optimization_trace": self.events,
        }
        write_json_atomic(Path(path), payload)
        self._last_checkpoint_monotonic = now


def evaluate_candidate(
    *,
    x_log: tuple[float, float],
    ecm_bin: str,
    numbers: list[int],
    config: OptimizationConfig,
    progress: ProgressTracker | None = None,
) -> EvaluatedPoint:
    """Вычислить fitness для кандидата в лог-пространстве."""
    b1, b2 = decode_candidate(x_log, config)
    score, metrics = fitness_with_stats(
        ecm_bin=ecm_bin,
        numbers=numbers,
        b1=b1,
        b2=b2,
        max_curves_per_n=config.max_curves_per_n,
        repeats_per_n=config.repeats_per_n,
        curve_timeout_sec=config.curve_timeout_sec,
        workers=config.workers,
    )
    if progress is not None:
        progress.on_evaluation(config=config, x_log=x_log, score=score, metrics=metrics)
        return EvaluatedPoint(x=x_log, score=score, eval_id=progress.eval_count)
    return EvaluatedPoint(x=x_log, score=score)


def evaluated_point_to_result(
    point: EvaluatedPoint,
    config: OptimizationConfig,
    history: list[dict[str, float | int | str]] | None = None,
) -> OptimizationResult:
    """Преобразовать оцененную точку в стандартный OptimizationResult."""
    b1, b2 = decode_candidate(point.x, config)
    return OptimizationResult(b1=b1, b2=b2, objective=point.score, history=history or [])
