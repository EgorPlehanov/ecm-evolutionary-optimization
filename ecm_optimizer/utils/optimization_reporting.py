from __future__ import annotations

import csv
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

        if len(jump_fit) >= 2:
            delta_x = jump_eval[1:]
            deltas = [jump_fit[i - 1] - jump_fit[i] for i in range(1, len(jump_fit))]
            plt.figure(figsize=(10, 5))
            plt.bar(delta_x, deltas, color="tab:purple", width=0.8)
            plt.title("Прирост на каждом new_best (delta fitness)")
            plt.xlabel("Evaluation (new_best)")
            plt.ylabel("Delta fitness")
            plt.grid(alpha=0.3)
            delta_path = output_dir / f"{run_stem}_improvement_deltas.png"
            plt.tight_layout()
            plt.savefig(delta_path, dpi=150)
            plt.close()
            plots["improvement_deltas"] = delta_path

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

    elapsed = [float(event.get("elapsed_sec", 0.0)) for event in evaluation_events]
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
    plt.title("Эффективность по времени: качество и скорость оценок")
    time_efficiency_path = output_dir / f"{run_stem}_time_efficiency.png"
    fig.tight_layout()
    fig.savefig(time_efficiency_path, dpi=150)
    plt.close(fig)
    plots["time_efficiency"] = time_efficiency_path

    ratio_values = [(b2 / b1) if b1 != 0 else 0.0 for b1, b2 in zip(b1_values, b2_values)]
    plt.figure(figsize=(10, 5))
    hb = plt.hexbin(b1_values, ratio_values, C=fitness_values, reduce_C_function=min, gridsize=25, cmap="viridis")
    plt.title("Heatmap по (B1, B2/B1), цвет = min fitness в бинe")
    plt.xlabel("B1")
    plt.ylabel("B2 / B1")
    plt.grid(alpha=0.2)
    plt.colorbar(hb, label="Best fitness in bin")
    heatmap_path = output_dir / f"{run_stem}_b1_ratio_heatmap.png"
    plt.tight_layout()
    plt.savefig(heatmap_path, dpi=150)
    plt.close()
    plots["b1_ratio_heatmap"] = heatmap_path

    return RunArtifacts(stats=stats, plots=plots)


def _attention_flags(stats: dict[str, float | int | None]) -> dict[str, dict[str, str | float | bool | None]]:
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

    return {
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
                "best_fitness_in_phase",
                "improvement_in_phase",
                "phase_duration_sec",
            ],
        )
        writer.writeheader()
        eval_events = [event for event in history if event.get("kind") == "evaluation"]
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

    flags = _attention_flags(stats)
    summary_path = tables_dir / f"{run_stem}_run_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        summary_keys = sorted(stats.keys())
        flag_keys = sorted(flags.keys())
        fieldnames = summary_keys + [f"flag_{name}" for name in flag_keys]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        row: dict[str, Any] = {key: stats.get(key) for key in summary_keys}
        for name in flag_keys:
            row[f"flag_{name}"] = bool(flags[name]["triggered"])
        writer.writerow(row)
    files["run_summary_csv"] = summary_path

    report_path = output_dir / f"{run_stem}_report.md"
    method = context.get("method", "unknown")
    dataset = context.get("dataset", "")
    optimized = context.get("optimized", {})
    config = context.get("config", {})
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
    lines.extend(["", "## Таблицы данных"])
    report_dir = report_path.parent
    for key, path in files.items():
        rel = path.relative_to(report_dir)
        lines.append(f"- `{key}`: `{rel}`")
    lines.extend(["", "## Графики"])
    for name, path in sorted(plots.items()):
        rel = path.relative_to(report_dir)
        lines.append(f"- `{name}`: `{rel}`")
        lines.append(f"![{name}]({rel})")

    lines.extend(
        [
            "",
            "## Таблицы (сворачиваемые, подгружаются из CSV через JS)",
            "<script>",
            "function parseCsvSimple(text) {",
            "  return text.trim().split(/\\r?\\n/).map(row => row.split(','));",
            "}",
            "function renderHtmlTable(rows) {",
            "  if (!rows.length) return '<p>Пустой CSV.</p>';",
            "  const head = rows[0];",
            "  const body = rows.slice(1);",
            "  return '<table border=\"1\" cellpadding=\"4\" cellspacing=\"0\">'",
            "    + '<thead><tr>' + head.map(cell => `<th>${cell}</th>`).join('') + '</tr></thead>'",
            "    + '<tbody>'",
            "    + body.map(row => '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>').join('')",
            "    + '</tbody></table>';",
            "}",
            "function loadCsvTable(containerId, csvPath) {",
            "  const container = document.getElementById(containerId);",
            "  if (!container) return;",
            "  container.innerHTML = 'Загрузка...';",
            "  fetch(csvPath)",
            "    .then(response => {",
            "      if (!response.ok) throw new Error(`HTTP ${response.status}`);",
            "      return response.text();",
            "    })",
            "    .then(text => {",
            "      const rows = parseCsvSimple(text);",
            "      container.innerHTML = renderHtmlTable(rows);",
            "    })",
            "    .catch(err => {",
            "      container.innerHTML = `<p>Не удалось загрузить CSV: ${err}</p>`;",
            "    });",
            "}",
            "</script>",
        ]
    )
    for key, path in sorted(files.items()):
        rel = path.relative_to(report_dir)
        if not str(rel).endswith(".csv"):
            continue
        container_id = f"tbl_{key}"
        lines.extend(
            [
                f"<details><summary>Показать таблицу: {key} ({rel})</summary>",
                f"<div id=\"{container_id}\">Нажмите, чтобы загрузить таблицу.</div>",
                "<script>",
                f"loadCsvTable('{container_id}', '{rel}');",
                "</script>",
                "</details>",
            ]
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    files["report_md"] = report_path

    return AnalysisArtifacts(files=files, flags=flags)
