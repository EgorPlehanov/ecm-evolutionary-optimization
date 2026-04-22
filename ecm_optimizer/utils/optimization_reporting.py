from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any



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


@dataclass(frozen=True)
class AnalysisArtifacts:
    files: dict[str, Path]
    flags: dict[str, dict[str, str | float | bool | None]]


def _tables_loader_src(report_dir: Path) -> str:
    repo_root = Path(__file__).resolve().parents[2]
    loader_path = repo_root / "ecm_optimizer" / "analysis" / "tables-loader.js"
    return os.path.relpath(loader_path, start=report_dir).replace(os.sep, "/")


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


def _plateau_lengths(evaluation_events: list[dict[str, float | int | str]], new_best_evals: set[int]) -> list[int]:
    lengths: list[int] = []
    current_gap = 0
    for event in evaluation_events:
        eval_id = int(event["eval"])
        if eval_id in new_best_evals:
            lengths.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1
    lengths.append(current_gap)
    return lengths


def _percentile(values: list[int], q: float) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    rank = (len(sorted_values) - 1) * q
    lo = int(rank)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = rank - lo
    return float(sorted_values[lo] + frac * (sorted_values[hi] - sorted_values[lo]))


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
            "median_plateau_evals": None,
            "p90_plateau_evals": None,
            "new_best_rate": None,
            "best_eval": None,
            "best_eval_fraction": None,
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
    best_eval = int(best_event.get("eval", 0))

    improvement_percent: float | None = None
    if first_fitness != 0:
        improvement_percent = ((first_fitness - best_fitness) / abs(first_fitness)) * 100.0

    plateau_lengths = _plateau_lengths(evaluation_events, new_best_evals)

    return {
        "evaluation_count": total_evals,
        "new_best_count": len(new_best_events),
        "new_best_rate": (len(new_best_events) / total_evals) if total_evals else None,
        "total_runtime_sec": total_runtime_sec,
        "time_to_first_improvement_sec": time_to_first_improvement_sec,
        "time_to_best_sec": time_to_best_sec,
        "best_eval": best_eval,
        "best_eval_fraction": (best_eval / total_evals) if total_evals else None,
        "eval_per_sec": (total_evals / total_elapsed) if total_elapsed > 0 else None,
        "improvement_percent": improvement_percent,
        "max_plateau_evals": _max_plateau(evaluation_events, new_best_evals),
        "median_plateau_evals": float(median(plateau_lengths)) if plateau_lengths else None,
        "p90_plateau_evals": _percentile(plateau_lengths, 0.9),
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


def _rolling_mean(values: list[float], window: int) -> list[float]:
    if not values:
        return []
    window = max(1, window)
    result: list[float] = []
    running_sum = 0.0
    for idx, value in enumerate(values):
        running_sum += value
        if idx >= window:
            running_sum -= values[idx - window]
        count = min(idx + 1, window)
        result.append(running_sum / count)
    return result


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

    if new_best_events:
        jump_eval = [int(event["eval"]) for event in new_best_events]
        jump_fit = [float(event["fitness"]) for event in new_best_events]
        fig, ax_fitness = plt.subplots(figsize=(10, 5))
        ax_fitness.scatter(jump_eval, jump_fit, color="tab:green", s=28)
        ax_fitness.plot(jump_eval, jump_fit, color="tab:green", alpha=0.6, linewidth=1.0)
        ax_fitness.set_title("Jump plot + improvement deltas (new best events)")
        ax_fitness.set_xlabel("Evaluation (new_best)")
        from matplotlib.ticker import MaxNLocator
        ax_fitness.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax_fitness.set_ylabel("Fitness", color="tab:green")
        ax_fitness.tick_params(axis="y", labelcolor="tab:green")
        ax_fitness.grid(alpha=0.3)

        if len(jump_fit) >= 2:
            delta_x = jump_eval[1:]
            deltas = [jump_fit[i - 1] - jump_fit[i] for i in range(1, len(jump_fit))]
            ax_delta = ax_fitness.twinx()
            ax_delta.bar(delta_x, deltas, color="tab:purple", width=0.8, alpha=0.35)
            ax_delta.set_ylabel("Delta fitness", color="tab:purple")
            ax_delta.tick_params(axis="y", labelcolor="tab:purple")

        jump_path = output_dir / f"{run_stem}_jump_plot.png"
        fig.tight_layout()
        fig.savefig(jump_path, dpi=150)
        plt.close(fig)
        plots["jump_plot"] = jump_path

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(eval_ids, b1_values, label="B1", linewidth=1.2)
    ax.plot(eval_ids, b2_values, label="B2", linewidth=1.2)
    ax.set_title("B1/B2 trajectory")
    ax.set_xlabel("Evaluation")
    ax.set_ylabel("Parameter value")
    ax.legend()
    ax.grid(alpha=0.3)
    b1b2_path = output_dir / f"{run_stem}_b1_b2_trajectory.png"
    fig.tight_layout()
    fig.savefig(b1b2_path, dpi=150)
    plt.close(fig)
    plots["b1_b2_trajectory"] = b1b2_path

    elapsed = [float(event.get("elapsed_sec", 0.0)) for event in evaluation_events]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(elapsed, conv_y, color="tab:blue", linewidth=1.8, label="Best fitness so far")
    ax.plot(elapsed, fitness_values, color="tab:orange", linewidth=1.1, alpha=0.8, label="Raw fitness")
    all_fitness_values = conv_y + fitness_values
    ymin = min(all_fitness_values)
    ymax = max(all_fitness_values)
    if ymin == ymax:
        ymax = ymin + 1.0
    for idx, step_event in enumerate(step_events):
        event_time = float(step_event.get("elapsed_sec", 0.0))
        label = str(step_event.get("message", "step"))
        ax.axvline(event_time, color="tab:red", alpha=0.2, linewidth=1.0)
        if idx < 12:
            ax.text(event_time, ymax, label[:28], rotation=90, va="top", ha="right", fontsize=7)
    if len(elapsed) >= 2 and len(eval_ids) == len(elapsed):
        eval_tick_count = min(8, len(eval_ids))
        if eval_tick_count >= 2:
            tick_indices = [round(i * (len(eval_ids) - 1) / (eval_tick_count - 1)) for i in range(eval_tick_count)]
            tick_indices = sorted(set(tick_indices))
            top_axis = ax.twiny()
            top_axis.set_xlim(ax.get_xlim())
            top_axis.set_xticks([elapsed[idx] for idx in tick_indices])
            top_axis.set_xticklabels([str(eval_ids[idx]) for idx in tick_indices])
            top_axis.set_xlabel("Evaluation")
            top_axis.tick_params(axis="x", labelsize=8)
    ax.set_ylim(ymin, ymax)
    ax.set_title("Progress by phase: best-so-far and raw fitness")
    ax.set_xlabel("Elapsed seconds")
    ax.set_ylabel("Fitness")
    ax.legend()
    ax.grid(alpha=0.3)
    phase_path = output_dir / f"{run_stem}_progress_by_phase.png"
    fig.tight_layout()
    fig.savefig(phase_path, dpi=150)
    plt.close(fig)
    plots["progress_by_phase"] = phase_path

    inst_eval_per_sec: list[float] = []
    for idx, t_cur in enumerate(elapsed):
        if idx == 0:
            dt = t_cur
        else:
            dt = t_cur - elapsed[idx - 1]
        inst_eval_per_sec.append((1.0 / dt) if dt > 0 else 0.0)
    smooth_eval_per_sec = _rolling_mean(inst_eval_per_sec, window=5)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(elapsed, conv_y, color="tab:blue", linewidth=1.6, label="Best fitness so far")
    ax1.set_xlabel("Elapsed seconds")
    ax1.set_ylabel("Best fitness so far", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.grid(alpha=0.3)
    ax2 = ax1.twinx()
    ax2.plot(elapsed, smooth_eval_per_sec, color="tab:red", linewidth=1.2, alpha=0.8, label="Rolling eval/sec")
    ax2.set_ylabel("Eval/sec (rolling)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    if len(elapsed) >= 2 and len(eval_ids) == len(elapsed):
        eval_tick_count = min(8, len(eval_ids))
        if eval_tick_count >= 2:
            tick_indices = [round(i * (len(eval_ids) - 1) / (eval_tick_count - 1)) for i in range(eval_tick_count)]
            tick_indices = sorted(set(tick_indices))
            top_axis = ax1.twiny()
            top_axis.set_xlim(ax1.get_xlim())
            top_axis.set_xticks([elapsed[idx] for idx in tick_indices])
            top_axis.set_xticklabels([str(eval_ids[idx]) for idx in tick_indices])
            top_axis.set_xlabel("Evaluation")
            top_axis.tick_params(axis="x", labelsize=8)
    plt.title("Эффективность по времени: качество и скорость оценок")
    time_efficiency_path = output_dir / f"{run_stem}_time_efficiency.png"
    fig.tight_layout()
    fig.savefig(time_efficiency_path, dpi=150)
    plt.close(fig)
    plots["time_efficiency"] = time_efficiency_path

    ratio_values = [(b2 / b1) if b1 != 0 else 0.0 for b1, b2 in zip(b1_values, b2_values)]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    scatter = axes[0].scatter(b1_values, b2_values, c=fitness_values, cmap="viridis", s=16)
    axes[0].set_title("B1 vs B2 (colored by fitness)")
    axes[0].set_xlabel("B1")
    axes[0].set_ylabel("B2")
    axes[0].grid(alpha=0.3)
    fig.colorbar(scatter, ax=axes[0], label="Fitness")

    hb = axes[1].hexbin(
        b1_values,
        ratio_values,
        C=fitness_values,
        reduce_C_function=min,
        gridsize=25,
        cmap="viridis",
    )
    axes[1].set_title("Heatmap: B1 vs B2/B1 (min fitness in bin)")
    axes[1].set_xlabel("B1")
    axes[1].set_ylabel("B2 / B1")
    axes[1].grid(alpha=0.2)
    fig.colorbar(hb, ax=axes[1], label="Best fitness in bin")
    heatmap_path = output_dir / f"{run_stem}_b1_ratio_heatmap.png"
    fig.tight_layout()
    fig.savefig(heatmap_path, dpi=150)
    plt.close(fig)
    plots["b1_ratio_heatmap"] = heatmap_path

    return RunArtifacts(stats=stats, plots=plots)


def _attention_flags(
    stats: dict[str, float | int | None],
    *,
    history: list[dict[str, float | int | str]] | None = None,
    config: dict[str, Any] | None = None,
    optimized: dict[str, Any] | None = None,
) -> dict[str, dict[str, str | float | bool | None]]:
    evaluation_count = int(stats.get("evaluation_count") or 0)
    max_plateau = float(stats.get("max_plateau_evals") or 0.0)
    new_best_rate = float(stats.get("new_best_rate") or 0.0)
    total_runtime_sec = float(stats.get("total_runtime_sec") or 0.0)
    time_to_best_sec = float(stats.get("time_to_best_sec") or 0.0)
    improvement_percent = float(stats.get("improvement_percent") or 0.0)

    plateau_ratio = (max_plateau / evaluation_count) if evaluation_count > 0 else None
    late_best_ratio = (time_to_best_sec / total_runtime_sec) if total_runtime_sec > 0 else None

    plateau_alert = bool(plateau_ratio is not None and plateau_ratio > 0.5)
    late_best_alert = bool(late_best_ratio is not None and late_best_ratio > 0.85)
    low_signal_alert = bool(new_best_rate < 0.03) if evaluation_count > 0 else False
    low_improvement_alert = bool(improvement_percent < 10.0) if evaluation_count > 0 else False

    flags: dict[str, dict[str, str | float | bool | None]] = {
        "plateau_too_long": {
            "triggered": plateau_alert,
            "value": plateau_ratio,
            "threshold": "> 0.50",
            "severity": "high" if plateau_alert else "ok",
            "action": "Увеличить exploration или добавить политику рестартов.",
            "description": "Слишком длинное плато: улучшений почти нет на большом участке запуска.",
        },
        "late_best": {
            "triggered": late_best_alert,
            "value": late_best_ratio,
            "threshold": "> 0.85",
            "severity": "medium" if late_best_alert else "ok",
            "action": "Усилить ранний поиск или пересмотреть бюджет/инициализацию.",
            "description": "Лучшее решение найдено слишком поздно относительно общего времени.",
        },
        "low_signal": {
            "triggered": low_signal_alert,
            "value": new_best_rate,
            "threshold": "< 0.03",
            "severity": "high" if low_signal_alert else "ok",
            "action": "Перенастроить exploration и сделать переоценку top-k кандидатов.",
            "description": "Слишком низкая плотность новых best-событий (слабый сигнал оптимизации).",
        },
        "low_improvement": {
            "triggered": low_improvement_alert,
            "value": improvement_percent,
            "threshold": "< 10%",
            "severity": "medium" if low_improvement_alert else "ok",
            "action": "Сузить границы поиска или изменить параметры метода.",
            "description": "Итоговый прирост качества слишком мал.",
        },
    }

    if history and config:
        eval_events = [event for event in history if event.get("kind") == "evaluation"]
        b1_min = config.get("b1_min")
        b1_max = config.get("b1_max")
        b2_min = config.get("b2_min")
        b2_max = config.get("b2_max")
        ratio_max = config.get("ratio_max")
        total = len(eval_events)

        def _boundary_share(values: list[float], low: float | None, high: float | None, tol_frac: float = 0.02) -> float | None:
            if not values or low is None or high is None:
                return None
            span = abs(high - low)
            tol = span * tol_frac
            touches = sum(1 for value in values if value <= (low + tol) or value >= (high - tol))
            return touches / len(values)

        def _boundary_share_log(values: list[float], low: float | None, high: float | None, tol_frac: float = 0.02) -> float | None:
            if not values or low is None or high is None:
                return None
            if low <= 0 or high <= 0:
                return _boundary_share(values, low, high, tol_frac=tol_frac)
            log_low = math.log10(low)
            log_high = math.log10(high)
            log_span = abs(log_high - log_low)
            log_tol = log_span * tol_frac
            touches = 0
            valid = 0
            for value in values:
                if value <= 0:
                    continue
                valid += 1
                log_value = math.log10(value)
                if log_value <= (log_low + log_tol) or log_value >= (log_high - log_tol):
                    touches += 1
            if valid == 0:
                return None
            return touches / valid

        b1_values = [float(event["b1"]) for event in eval_events if event.get("b1") is not None]
        b2_values = [float(event["b2"]) for event in eval_events if event.get("b2") is not None]
        ratio_values = [
            float(event["b2"]) / float(event["b1"])
            for event in eval_events
            if event.get("b1") not in (None, 0, 0.0) and event.get("b2") is not None
        ]

        b1_boundary_share = _boundary_share_log(
            b1_values,
            float(b1_min) if b1_min is not None else None,
            float(b1_max) if b1_max is not None else None,
        )
        b2_boundary_share = _boundary_share_log(
            b2_values,
            float(b2_min) if b2_min is not None else None,
            float(b2_max) if b2_max is not None else None,
        )
        ratio_low = min(ratio_values) if ratio_values else None
        ratio_boundary_share = _boundary_share_log(
            ratio_values,
            ratio_low if ratio_low is not None else 1e-12,
            float(ratio_max) if ratio_max is not None else None,
        )

        boundary_share_threshold = 0.10
        flags["b1_hits_boundary"] = {
            "triggered": bool(b1_boundary_share is not None and b1_boundary_share > boundary_share_threshold),
            "value": b1_boundary_share,
            "threshold": "> 0.10",
            "severity": "medium" if b1_boundary_share is not None and b1_boundary_share > boundary_share_threshold else "ok",
            "action": "Расширить диапазон B1, если упор в границу повторяется.",
            "description": "Большая доля оценок проходит близко к границам B1.",
        }
        flags["b2_hits_boundary"] = {
            "triggered": bool(b2_boundary_share is not None and b2_boundary_share > boundary_share_threshold),
            "value": b2_boundary_share,
            "threshold": "> 0.10",
            "severity": "medium" if b2_boundary_share is not None and b2_boundary_share > boundary_share_threshold else "ok",
            "action": "Расширить диапазон B2, если упор в границу повторяется.",
            "description": "Большая доля оценок проходит близко к границам B2.",
        }
        flags["ratio_hits_boundary"] = {
            "triggered": bool(ratio_boundary_share is not None and ratio_boundary_share > boundary_share_threshold),
            "value": ratio_boundary_share,
            "threshold": "> 0.10",
            "severity": "medium" if ratio_boundary_share is not None and ratio_boundary_share > boundary_share_threshold else "ok",
            "action": "Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1.",
            "description": "Большая доля оценок проходит близко к границе отношения B2/B1.",
        }

        if optimized:
            best_b1 = optimized.get("b1")
            best_b2 = optimized.get("b2")
            if best_b1 is not None and b1_min is not None and b1_max is not None:
                if float(b1_min) > 0 and float(b1_max) > 0 and float(best_b1) > 0:
                    log_best_b1 = math.log10(float(best_b1))
                    log_b1_min = math.log10(float(b1_min))
                    log_b1_max = math.log10(float(b1_max))
                    log_b1_tol = abs(log_b1_max - log_b1_min) * 0.02
                    best_on_b1_boundary = log_best_b1 <= log_b1_min + log_b1_tol or log_best_b1 >= log_b1_max - log_b1_tol
                else:
                    b1_span = abs(float(b1_max) - float(b1_min))
                    b1_tol = b1_span * 0.02
                    best_on_b1_boundary = float(best_b1) <= float(b1_min) + b1_tol or float(best_b1) >= float(b1_max) - b1_tol
                flags["best_b1_on_boundary"] = {
                    "triggered": best_on_b1_boundary,
                    "value": float(best_b1),
                    "threshold": f"within 2% of log-range [{b1_min}, {b1_max}]",
                    "severity": "high" if best_on_b1_boundary else "ok",
                    "action": "Проверить расширенный диапазон B1 вокруг текущей границы.",
                    "description": "Лучший найденный B1 лежит на границе диапазона.",
                }
            if best_b2 is not None and b2_min is not None and b2_max is not None:
                if float(b2_min) > 0 and float(b2_max) > 0 and float(best_b2) > 0:
                    log_best_b2 = math.log10(float(best_b2))
                    log_b2_min = math.log10(float(b2_min))
                    log_b2_max = math.log10(float(b2_max))
                    log_b2_tol = abs(log_b2_max - log_b2_min) * 0.02
                    best_on_b2_boundary = log_best_b2 <= log_b2_min + log_b2_tol or log_best_b2 >= log_b2_max - log_b2_tol
                else:
                    b2_span = abs(float(b2_max) - float(b2_min))
                    b2_tol = b2_span * 0.02
                    best_on_b2_boundary = float(best_b2) <= float(b2_min) + b2_tol or float(best_b2) >= float(b2_max) - b2_tol
                flags["best_b2_on_boundary"] = {
                    "triggered": best_on_b2_boundary,
                    "value": float(best_b2),
                    "threshold": f"within 2% of log-range [{b2_min}, {b2_max}]",
                    "severity": "high" if best_on_b2_boundary else "ok",
                    "action": "Проверить расширенный диапазон B2 вокруг текущей границы.",
                    "description": "Лучший найденный B2 лежит на границе диапазона.",
                }
            if best_b1 not in (None, 0, 0.0) and best_b2 is not None and ratio_max is not None:
                best_ratio = float(best_b2) / float(best_b1)
                if float(ratio_max) > 0 and best_ratio > 0:
                    log_ratio_max = math.log10(float(ratio_max))
                    log_best_ratio = math.log10(best_ratio)
                    ratio_low_for_tol = ratio_low if ratio_low is not None and ratio_low > 0 else 1e-12
                    log_ratio_tol = abs(log_ratio_max - math.log10(ratio_low_for_tol)) * 0.02
                    best_on_ratio_boundary = log_best_ratio >= log_ratio_max - log_ratio_tol
                else:
                    ratio_tol = abs(float(ratio_max)) * 0.02
                    best_on_ratio_boundary = best_ratio >= float(ratio_max) - ratio_tol
                flags["best_ratio_on_boundary"] = {
                    "triggered": best_on_ratio_boundary,
                    "value": best_ratio,
                    "threshold": f"within 2% of log-range up to ratio_max={ratio_max}",
                    "severity": "high" if best_on_ratio_boundary else "ok",
                    "action": "Увеличить ratio_max и перепроверить локальный поиск в новой области.",
                    "description": "Лучшее отношение B2/B1 находится у верхней границы ratio_max.",
                }

        if total == 0:
            for key in ("b1_hits_boundary", "b2_hits_boundary", "ratio_hits_boundary"):
                if key in flags:
                    flags[key]["value"] = None

    return flags


def generate_analysis_artifacts(
    *,
    history: list[dict[str, float | int | str]],
    stats: dict[str, float | int | None],
    plots: dict[str, Path],
    output_dir: Path,
    run_stem: str,
    context: dict[str, Any],
) -> AnalysisArtifacts:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    files: dict[str, Path] = {}

    events = [event for event in history if event.get("kind") in {"evaluation", "new_best", "step"}]
    eval_events = [event for event in history if event.get("kind") == "evaluation"]
    successes_by_eval: dict[int, int] = {}
    for event in eval_events:
        eval_id = event.get("eval")
        successes = event.get("successes")
        if isinstance(eval_id, int) and isinstance(successes, int):
            successes_by_eval[eval_id] = successes
    new_best_events = [event for event in history if event.get("kind") == "new_best"]
    events_path = tables_dir / f"{run_stem}_events.csv"
    with events_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "event_idx",
                "kind",
                "eval",
                "elapsed_sec",
                "b1",
                "b2",
                "ratio",
                "fitness",
                "successes",
                "is_new_best",
                "message",
                "timestamp_utc",
            ],
        )
        writer.writeheader()
        for idx, event in enumerate(events, start=1):
            b1 = event.get("b1")
            b2 = event.get("b2")
            ratio = (float(b2) / float(b1)) if b1 not in (None, 0, 0.0) and b2 is not None else None
            writer.writerow(
                {
                    "event_idx": idx,
                    "kind": event.get("kind"),
                    "eval": event.get("eval"),
                    "elapsed_sec": event.get("elapsed_sec"),
                    "b1": b1,
                    "b2": b2,
                    "ratio": ratio,
                    "fitness": event.get("fitness"),
                    "successes": event.get("successes"),
                    "is_new_best": event.get("kind") == "new_best",
                    "message": event.get("message", ""),
                    "timestamp_utc": event.get("timestamp_utc", ""),
                }
            )
    files["events_csv"] = events_path

    new_best_path = tables_dir / f"{run_stem}_new_best.csv"
    with new_best_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "new_best_idx",
                "eval",
                "elapsed_sec",
                "b1",
                "b2",
                "ratio",
                "fitness",
                "successes",
                "delta_abs_vs_prev_best",
                "delta_pct_vs_prev_best",
                "plateau_since_prev_new_best",
            ],
        )
        writer.writeheader()
        prev_best_fitness: float | None = None
        prev_best_eval: int | None = None
        for idx, event in enumerate(new_best_events, start=1):
            fitness = float(event["fitness"])
            eval_id = int(event.get("eval", 0))
            b1 = event.get("b1")
            b2 = event.get("b2")
            ratio = (float(b2) / float(b1)) if b1 not in (None, 0, 0.0) and b2 is not None else None
            delta_abs: float | None = None
            delta_pct: float | None = None
            plateau = None
            if prev_best_fitness is not None:
                delta_abs = prev_best_fitness - fitness
                if prev_best_fitness != 0:
                    delta_pct = (delta_abs / abs(prev_best_fitness)) * 100.0
            if prev_best_eval is not None:
                plateau = max(0, eval_id - prev_best_eval - 1)
            writer.writerow(
                {
                    "new_best_idx": idx,
                    "eval": eval_id,
                    "elapsed_sec": event.get("elapsed_sec"),
                    "b1": b1,
                    "b2": b2,
                    "ratio": ratio,
                    "fitness": fitness,
                    "successes": successes_by_eval.get(eval_id, event.get("successes")),
                    "delta_abs_vs_prev_best": delta_abs,
                    "delta_pct_vs_prev_best": delta_pct,
                    "plateau_since_prev_new_best": plateau,
                }
            )
            prev_best_fitness = fitness
            prev_best_eval = eval_id
    files["new_best_csv"] = new_best_path

    step_events = [event for event in history if event.get("kind") == "step"]
    phase_summary_path = tables_dir / f"{run_stem}_phase_summary.csv"
    with phase_summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "phase_idx",
                "phase_label",
                "eval_from",
                "eval_to",
                "eval_count",
                "new_best_count",
                "successes_sum",
                "success_rate",
                "best_fitness_in_phase",
                "improvement_in_phase",
                "phase_duration_sec",
            ],
        )
        writer.writeheader()
        prev_eval = 0
        prev_time = 0.0
        prev_phase_best: float | None = None
        for idx, step in enumerate(step_events, start=1):
            eval_to = int(step.get("eval", prev_eval))
            eval_from = prev_eval + 1
            phase_eval_events = [
                ev
                for ev in eval_events
                if int(ev.get("eval", 0)) >= eval_from and int(ev.get("eval", 0)) <= eval_to
            ]
            phase_new_best = [
                ev
                for ev in new_best_events
                if int(ev.get("eval", 0)) >= eval_from and int(ev.get("eval", 0)) <= eval_to
            ]
            phase_best = min((float(ev["fitness"]) for ev in phase_eval_events), default=None)
            phase_successes = sum(int(ev.get("successes", 0)) for ev in phase_eval_events)
            improvement = None
            if prev_phase_best is not None and phase_best is not None:
                improvement = prev_phase_best - phase_best
            phase_time = float(step.get("elapsed_sec", prev_time))
            writer.writerow(
                {
                    "phase_idx": idx,
                    "phase_label": step.get("message", f"phase_{idx}"),
                    "eval_from": eval_from,
                    "eval_to": eval_to,
                    "eval_count": len(phase_eval_events),
                    "new_best_count": len(phase_new_best),
                    "successes_sum": phase_successes,
                    "success_rate": (phase_successes / len(phase_eval_events)) if phase_eval_events else None,
                    "best_fitness_in_phase": phase_best,
                    "improvement_in_phase": improvement,
                    "phase_duration_sec": phase_time - prev_time,
                }
            )
            prev_eval = eval_to
            prev_time = phase_time
            if phase_best is not None:
                prev_phase_best = phase_best
    files["phase_summary_csv"] = phase_summary_path

    config = context.get("config", {})
    optimized = context.get("optimized", {})
    flags = _attention_flags(stats, history=history, config=config, optimized=optimized)
    summary_path = tables_dir / f"{run_stem}_run_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        for key in sorted(stats.keys()):
            writer.writerow({"metric": key, "value": stats.get(key)})
        for name in sorted(flags.keys()):
            writer.writerow({"metric": f"flag_{name}", "value": bool(flags[name]["triggered"])})
    files["run_summary_csv"] = summary_path

    report_path = output_dir / f"{run_stem}_report.md"
    method = context.get("method", "unknown")
    dataset = context.get("dataset", "")
    best_obj = optimized.get("objective")
    lines: list[str] = [
        f"# Отчёт по оптимизации: {run_stem}",
        "",
        "## Метаданные",
        f"- метод: `{method}`",
        f"- датасет: `{dataset}`",
        f"- оптимум `(B1, B2)`: `({optimized.get('b1')}, {optimized.get('b2')})`",
        f"- objective: `{best_obj}`",
        f"- curves_per_n: `{config.get('curves_per_n')}`",
        f"- границы: `B1[{config.get('b1_min')}, {config.get('b1_max')}]`, `B2[{config.get('b2_min')}, {config.get('b2_max')}]`, `ratio_max={config.get('ratio_max')}`",
        "",
        "## Ключевые статистики",
    ]
    for key in sorted(stats):
        lines.append(f"- `{key}`: `{stats[key]}`")
    lines.extend(
        [
            "",
            "## Флаги внимания",
            "",
            "| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for name in sorted(flags):
        item = flags[name]
        marker = "⚠️" if item["triggered"] else "✅"
        status = "ВНИМАНИЕ" if item["triggered"] else "ОК"
        lines.append(
            f"| `{name}` | {marker} {status} | `{item['value']}` | `{item['threshold']}` | {item['description']} | {item['action']} |"
        )
    report_dir = report_path.parent
    lines.extend(["", "## Графики"])
    for name, path in sorted(plots.items()):
        rel = path.relative_to(report_dir)
        lines.append(f"- [`{rel.name}`]({rel})")
        lines.append(f"![{name}]({rel})")

    lines.extend(["", "## Таблицы"])
    table_specs: list[str] = []
    for key, path in sorted(files.items()):
        rel = path.relative_to(report_dir)
        if not str(rel).endswith(".csv"):
            continue
        table_specs.append(str(rel))
    table_configs = [{"file": rel} for rel in table_specs]
    data_tables = json.dumps(table_configs, ensure_ascii=False)
    loader_src = _tables_loader_src(report_dir)
    lines.extend(
        [
            "",
            f"<div id=\"tables-container\" data-tables='{data_tables}'></div>",
            "",
            f"<script src=\"{loader_src}\"></script>",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    files["report_md"] = report_path

    return AnalysisArtifacts(files=files, flags=flags)
