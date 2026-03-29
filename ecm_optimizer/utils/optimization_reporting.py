from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path





def _load_matplotlib_pyplot():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except ModuleNotFoundError:
        return None


@dataclass(frozen=True)
class RunArtifacts:
    stats: dict[str, float | int | None]
    plots: dict[str, Path]


def _max_plateau(evaluation_events: list[dict[str, float | int | str]], new_best_evals: set[int]) -> int:
    max_gap = 0
    current_gap = 0
    for event in evaluation_events:
        eval_id = int(event["eval"])
        if eval_id in new_best_evals:
            max_gap = max(max_gap, current_gap)
            current_gap = 0
        else:
            current_gap += 1
    return max(max_gap, current_gap)


def build_run_statistics(history: list[dict[str, float | int | str]]) -> dict[str, float | int | None]:
    evaluation_events = [event for event in history if event.get("kind") == "evaluation"]
    new_best_events = [event for event in history if event.get("kind") == "new_best"]
    elapsed_values = [float(event.get("elapsed_sec", 0.0)) for event in history if "elapsed_sec" in event]
    total_runtime_sec = max(elapsed_values) if elapsed_values else 0.0

    if not evaluation_events:
        return {
            "evaluation_count": 0,
            "new_best_count": 0,
            "total_runtime_sec": total_runtime_sec,
            "time_to_first_improvement_sec": None,
            "time_to_best_sec": None,
            "eval_per_sec": None,
            "improvement_percent": None,
            "max_plateau_evals": None,
        }

    total_evals = len(evaluation_events)
    total_elapsed = float(evaluation_events[-1].get("elapsed_sec", 0.0))
    first_fitness = float(evaluation_events[0]["fitness"])
    best_fitness = min(float(event["fitness"]) for event in evaluation_events)
    new_best_evals = {int(event["eval"]) for event in new_best_events}

    time_to_first_improvement_sec: float | None = None
    if new_best_events:
        time_to_first_improvement_sec = float(new_best_events[0].get("elapsed_sec", 0.0))

    best_event = min(evaluation_events, key=lambda event: float(event["fitness"]))
    time_to_best_sec = float(best_event.get("elapsed_sec", 0.0))

    improvement_percent: float | None = None
    if first_fitness != 0:
        improvement_percent = ((first_fitness - best_fitness) / abs(first_fitness)) * 100.0

    return {
        "evaluation_count": total_evals,
        "new_best_count": len(new_best_events),
        "total_runtime_sec": total_runtime_sec,
        "time_to_first_improvement_sec": time_to_first_improvement_sec,
        "time_to_best_sec": time_to_best_sec,
        "eval_per_sec": (total_evals / total_elapsed) if total_elapsed > 0 else None,
        "improvement_percent": improvement_percent,
        "max_plateau_evals": _max_plateau(evaluation_events, new_best_evals),
    }


def _convergence_series(evaluation_events: list[dict[str, float | int | str]]) -> tuple[list[int], list[float]]:
    evals: list[int] = []
    best_so_far: list[float] = []
    current_best: float | None = None
    for event in evaluation_events:
        eval_id = int(event["eval"])
        fitness = float(event["fitness"])
        if current_best is None or fitness < current_best:
            current_best = fitness
        evals.append(eval_id)
        best_so_far.append(current_best)
    return evals, best_so_far


def generate_run_artifacts(
    *,
    history: list[dict[str, float | int | str]],
    output_dir: Path,
    run_stem: str,
) -> RunArtifacts:
    output_dir.mkdir(parents=True, exist_ok=True)

    evaluation_events = [event for event in history if event.get("kind") == "evaluation"]
    new_best_events = [event for event in history if event.get("kind") == "new_best"]
    step_events = [event for event in history if event.get("kind") == "step"]

    stats = build_run_statistics(history)

    plots: dict[str, Path] = {}
    if not evaluation_events:
        return RunArtifacts(stats=stats, plots=plots)

    plt = _load_matplotlib_pyplot()
    if plt is None:
        return RunArtifacts(stats=stats, plots=plots)

    eval_ids = [int(event["eval"]) for event in evaluation_events]
    fitness_values = [float(event["fitness"]) for event in evaluation_events]
    b1_values = [float(event["b1"]) for event in evaluation_events]
    b2_values = [float(event["b2"]) for event in evaluation_events]

    conv_x, conv_y = _convergence_series(evaluation_events)

    plt.figure(figsize=(10, 5))
    plt.plot(conv_x, conv_y, color="tab:blue", linewidth=1.8)
    plt.title("Convergence curve")
    plt.xlabel("Evaluation")
    plt.ylabel("Best fitness so far")
    plt.grid(alpha=0.3)
    convergence_path = output_dir / f"{run_stem}_convergence.png"
    plt.tight_layout()
    plt.savefig(convergence_path, dpi=150)
    plt.close()
    plots["convergence"] = convergence_path

    plt.figure(figsize=(10, 5))
    plt.plot(eval_ids, fitness_values, color="tab:orange", linewidth=1.2)
    plt.title("Raw fitness trajectory")
    plt.xlabel("Evaluation")
    plt.ylabel("Fitness")
    plt.grid(alpha=0.3)
    raw_path = output_dir / f"{run_stem}_raw_fitness.png"
    plt.tight_layout()
    plt.savefig(raw_path, dpi=150)
    plt.close()
    plots["raw_fitness"] = raw_path

    if new_best_events:
        plt.figure(figsize=(10, 5))
        jump_eval = [int(event["eval"]) for event in new_best_events]
        jump_fit = [float(event["fitness"]) for event in new_best_events]
        plt.scatter(jump_eval, jump_fit, color="tab:green", s=28)
        plt.plot(jump_eval, jump_fit, color="tab:green", alpha=0.6, linewidth=1.0)
        plt.title("Jump plot (new best events)")
        plt.xlabel("Evaluation")
        plt.ylabel("Fitness")
        plt.grid(alpha=0.3)
        jump_path = output_dir / f"{run_stem}_jump_plot.png"
        plt.tight_layout()
        plt.savefig(jump_path, dpi=150)
        plt.close()
        plots["jump_plot"] = jump_path

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    axes[0].plot(eval_ids, b1_values, label="B1", linewidth=1.2)
    axes[0].plot(eval_ids, b2_values, label="B2", linewidth=1.2)
    axes[0].set_title("B1/B2 trajectory")
    axes[0].set_xlabel("Evaluation")
    axes[0].set_ylabel("Parameter value")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    scatter = axes[1].scatter(b1_values, b2_values, c=fitness_values, cmap="viridis", s=16)
    axes[1].set_title("B1 vs B2 (colored by fitness)")
    axes[1].set_xlabel("B1")
    axes[1].set_ylabel("B2")
    axes[1].grid(alpha=0.3)
    fig.colorbar(scatter, ax=axes[1], label="Fitness")
    b1b2_path = output_dir / f"{run_stem}_b1_b2_trajectory.png"
    fig.tight_layout()
    fig.savefig(b1b2_path, dpi=150)
    plt.close(fig)
    plots["b1_b2_trajectory"] = b1b2_path

    plt.figure(figsize=(10, 5))
    plt.plot(conv_x, conv_y, color="tab:blue", linewidth=1.6)
    ymin = min(conv_y)
    ymax = max(conv_y)
    if ymin == ymax:
        ymax = ymin + 1.0
    for idx, step_event in enumerate(step_events):
        event_eval = int(step_event.get("eval", 0))
        label = str(step_event.get("message", "step"))
        plt.axvline(event_eval, color="tab:red", alpha=0.2, linewidth=1.0)
        if idx < 12:
            plt.text(event_eval, ymax, label[:28], rotation=90, va="top", ha="right", fontsize=7)
    plt.ylim(ymin, ymax)
    plt.title("Progress by phase")
    plt.xlabel("Evaluation")
    plt.ylabel("Best fitness so far")
    plt.grid(alpha=0.3)
    phase_path = output_dir / f"{run_stem}_progress_by_phase.png"
    plt.tight_layout()
    plt.savefig(phase_path, dpi=150)
    plt.close()
    plots["progress_by_phase"] = phase_path

    return RunArtifacts(stats=stats, plots=plots)
