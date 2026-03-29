from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import time
from typing import Any


def _safe_float(value: float) -> float:
    if math.isnan(value) or math.isinf(value):
        return float("nan")
    return float(value)


@dataclass
class EvaluationEvent:
    eval: int
    b1: int
    b2: int
    fitness: float
    elapsed_sec: float


@dataclass
class StepEvent:
    name: str
    eval: int
    elapsed_sec: float


class RunTraceRecorder:
    """Collect per-evaluation and per-step events for one optimization run."""

    def __init__(self) -> None:
        self._start = time.perf_counter()
        self._best_so_far: float | None = None
        self._eval_counter = 0
        self.evaluations: list[EvaluationEvent] = []
        self.new_best_events: list[EvaluationEvent] = []
        self.steps: list[StepEvent] = []

    def record_step(self, name: str) -> None:
        self.steps.append(
            StepEvent(
                name=name,
                eval=self._eval_counter,
                elapsed_sec=time.perf_counter() - self._start,
            )
        )

    def record_evaluation(self, *, b1: int, b2: int, fitness: float) -> None:
        self._eval_counter += 1
        event = EvaluationEvent(
            eval=self._eval_counter,
            b1=int(b1),
            b2=int(b2),
            fitness=_safe_float(fitness),
            elapsed_sec=time.perf_counter() - self._start,
        )
        self.evaluations.append(event)
        if self._best_so_far is None or event.fitness < self._best_so_far:
            self._best_so_far = event.fitness
            self.new_best_events.append(event)


@dataclass
class RunReport:
    stats: dict[str, Any]
    artifacts: dict[str, str]


def _compute_stats(recorder: RunTraceRecorder) -> dict[str, Any]:
    evals = recorder.evaluations
    improvements = recorder.new_best_events
    if not evals:
        return {
            "evaluations": 0,
            "new_best_count": 0,
            "eval_per_sec": None,
            "time_to_first_improvement_sec": None,
            "time_to_best_sec": None,
            "percent_improvement": None,
            "max_plateau_length_evals": None,
        }

    elapsed_total = max(evals[-1].elapsed_sec, 1e-9)
    max_plateau = 0
    prev_best_eval = 0
    for ev in improvements:
        plateau_len = ev.eval - prev_best_eval - 1
        if plateau_len > max_plateau:
            max_plateau = plateau_len
        prev_best_eval = ev.eval
    tail_plateau = evals[-1].eval - prev_best_eval
    max_plateau = max(max_plateau, tail_plateau)

    percent_improvement = None
    if improvements:
        first_best = improvements[0].fitness
        final_best = improvements[-1].fitness
        if first_best != 0:
            percent_improvement = (first_best - final_best) / abs(first_best) * 100.0

    return {
        "evaluations": len(evals),
        "new_best_count": len(improvements),
        "eval_per_sec": len(evals) / elapsed_total,
        "time_to_first_improvement_sec": improvements[0].elapsed_sec if improvements else None,
        "time_to_best_sec": improvements[-1].elapsed_sec if improvements else None,
        "percent_improvement": percent_improvement,
        "max_plateau_length_evals": int(max_plateau),
        "elapsed_total_sec": elapsed_total,
    }


def _events_to_dict(recorder: RunTraceRecorder) -> dict[str, Any]:
    running_best = float("inf")
    eval_rows: list[dict[str, Any]] = []
    for ev in recorder.evaluations:
        running_best = min(running_best, ev.fitness)
        eval_rows.append(
            {
                "kind": "evaluation",
                "eval": ev.eval,
                "elapsed_sec": ev.elapsed_sec,
                "b1": ev.b1,
                "b2": ev.b2,
                "fitness": ev.fitness,
                "best_fitness_so_far": running_best,
            }
        )

    new_best_rows = [
        {
            "kind": "new_best",
            "eval": ev.eval,
            "elapsed_sec": ev.elapsed_sec,
            "b1": ev.b1,
            "b2": ev.b2,
            "fitness": ev.fitness,
        }
        for ev in recorder.new_best_events
    ]
    step_rows = [
        {
            "kind": "step",
            "name": st.name,
            "eval": st.eval,
            "elapsed_sec": st.elapsed_sec,
        }
        for st in recorder.steps
    ]
    return {"evaluations": eval_rows, "new_best": new_best_rows, "steps": step_rows}


def _save_plots(recorder: RunTraceRecorder, out_dir: Path, name_prefix: str) -> dict[str, str]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return {}

    if not recorder.evaluations:
        return {}

    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, str] = {}

    evals = recorder.evaluations
    xs_eval = [e.eval for e in evals]
    ys = [e.fitness for e in evals]

    running_best = []
    best = float("inf")
    for y in ys:
        best = min(best, y)
        running_best.append(best)

    def save(fig_name: str) -> tuple[Any, Any]:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        artifacts[fig_name] = str(out_dir / f"{name_prefix}_{fig_name}.png")
        return fig, ax

    fig, ax = save("convergence")
    ax.plot(xs_eval, running_best, label="best_fitness_so_far")
    ax.set_xlabel("eval")
    ax.set_ylabel("fitness")
    ax.set_title("Convergence curve")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(artifacts["convergence"], dpi=150)
    plt.close(fig)

    fig, ax = save("raw_fitness")
    ax.plot(xs_eval, ys, linewidth=1.0, alpha=0.9)
    ax.set_xlabel("eval")
    ax.set_ylabel("fitness")
    ax.set_title("Raw fitness trajectory")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(artifacts["raw_fitness"], dpi=150)
    plt.close(fig)

    fig, ax = save("jump_plot")
    if recorder.new_best_events:
        ax.scatter([e.eval for e in recorder.new_best_events], [e.fitness for e in recorder.new_best_events], s=25)
    ax.set_xlabel("eval")
    ax.set_ylabel("fitness")
    ax.set_title("Jump plot (new best events)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(artifacts["jump_plot"], dpi=150)
    plt.close(fig)

    fig, ax = save("b1_b2_trajectory")
    scatter = ax.scatter([e.b1 for e in evals], [e.b2 for e in evals], c=ys, s=18, cmap="viridis")
    ax.set_xlabel("B1")
    ax.set_ylabel("B2")
    ax.set_title("B1/B2 trajectory (colored by fitness)")
    ax.grid(True, alpha=0.3)
    fig.colorbar(scatter, ax=ax, label="fitness")
    fig.tight_layout()
    fig.savefig(artifacts["b1_b2_trajectory"], dpi=150)
    plt.close(fig)

    fig, ax = save("progress_by_phase")
    ax.plot(xs_eval, running_best, label="best_fitness_so_far")
    for st in recorder.steps:
        ax.axvline(st.eval, color="tab:red", alpha=0.2, linewidth=1)
    ax.set_xlabel("eval")
    ax.set_ylabel("fitness")
    ax.set_title("Progress by phase")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(artifacts["progress_by_phase"], dpi=150)
    plt.close(fig)

    return artifacts


def build_run_report(*, recorder: RunTraceRecorder, out_dir: Path, name_prefix: str) -> RunReport:
    stats = _compute_stats(recorder)
    artifacts = _save_plots(recorder, out_dir, name_prefix)
    event_payload = _events_to_dict(recorder)
    event_file = out_dir / f"{name_prefix}_trace.json"
    event_file.write_text(__import__("json").dumps(event_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    artifacts["trace_json"] = str(event_file)
    return RunReport(stats=stats, artifacts=artifacts)
