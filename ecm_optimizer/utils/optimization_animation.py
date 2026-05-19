from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ecm_optimizer.utils.io_utils import read_json


def _load_matplotlib():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.animation as animation
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import Normalize

        return animation, plt, np, Normalize
    except ModuleNotFoundError:
        return None


def _evaluation_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    trace = payload.get("optimization_trace", payload.get("history", []))
    if not isinstance(trace, list):
        return []
    return [event for event in trace if isinstance(event, dict) and event.get("kind") == "evaluation"]


def _default_output_path(optimize_file: Path, output_path: Path | None) -> Path:
    if output_path is not None:
        return output_path
    return optimize_file.parent / "plots" / f"{optimize_file.stem}_evaluation_order.gif"


def _finite_range(values: list[float]) -> tuple[float, float]:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return 0.0, 1.0
    low = min(finite)
    high = max(finite)
    if low == high:
        pad = abs(low) * 0.05 if low else 1.0
        return low - pad, high + pad
    return low, high


def render_evaluation_order_animation(
    *,
    optimize_file: Path,
    output_path: Path | None = None,
    fps: int = 8,
    dpi: int = 120,
    max_frames: int | None = None,
    log_scale: bool = True,
) -> Path:
    """Render GIF/MP4 animation of optimizer evaluation order in B1/B2 space."""

    optimize_file = Path(optimize_file)
    payload = read_json(optimize_file)
    events = _evaluation_events(payload)
    if not events:
        raise ValueError(f"No evaluation events found in {optimize_file}")

    mpl = _load_matplotlib()
    if mpl is None:
        raise RuntimeError("matplotlib is required to render optimization animations")
    animation, plt, np, Normalize = mpl

    resolved_output = _default_output_path(optimize_file, output_path)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)

    frame_stride = 1
    if max_frames is not None and max_frames > 0 and len(events) > max_frames:
        frame_stride = math.ceil(len(events) / max_frames)
    frame_indices = list(range(0, len(events), frame_stride))
    if frame_indices[-1] != len(events) - 1:
        frame_indices.append(len(events) - 1)

    b1_values = [float(event["b1"]) for event in events]
    b2_values = [float(event["b2"]) for event in events]
    fitness_values = [float(event["fitness"]) for event in events]
    eval_ids = [int(event.get("eval", idx + 1)) for idx, event in enumerate(events)]

    config = payload.get("config", {})
    x_min = float(config.get("b1_min", _finite_range(b1_values)[0]))
    x_max = float(config.get("b1_max", _finite_range(b1_values)[1]))
    y_min = float(config.get("b2_min", _finite_range(b2_values)[0]))
    y_max = float(config.get("b2_max", _finite_range(b2_values)[1]))
    if log_scale:
        x_min = max(x_min, min(value for value in b1_values if value > 0) * 0.9)
        y_min = max(y_min, min(value for value in b2_values if value > 0) * 0.9)

    best_so_far_indices: list[int] = []
    best_idx = 0
    best_value = fitness_values[0]
    for idx, fitness in enumerate(fitness_values):
        if fitness < best_value:
            best_idx = idx
            best_value = fitness
        best_so_far_indices.append(best_idx)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.subplots_adjust(bottom=0.16, top=0.90)
    norm = Normalize(vmin=min(fitness_values), vmax=max(fitness_values))

    background = ax.scatter(
        b1_values,
        b2_values,
        c=fitness_values,
        cmap="viridis",
        norm=norm,
        s=20,
        alpha=0.18,
        linewidths=0,
    )
    path_line, = ax.plot([], [], color="0.15", linewidth=1.0, alpha=0.45)
    visited = ax.scatter([], [], c=[], cmap="viridis", norm=norm, s=34, edgecolors="white", linewidths=0.35)
    current = ax.scatter([], [], s=130, facecolors="none", edgecolors="tab:red", linewidths=2.0)
    best = ax.scatter([], [], marker="*", s=190, color="gold", edgecolors="black", linewidths=0.7, zorder=5)
    frame_caption = fig.text(0.12, 0.035, "", fontsize=10, va="bottom")

    ax.set_title("Evaluation order in B1/B2 search space")
    ax.set_xlabel("B1")
    ax.set_ylabel("B2")
    ax.grid(alpha=0.22)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")
    fig.colorbar(background, ax=ax, label="Fitness")

    def update(frame_idx: int):
        upto = frame_idx + 1
        path_line.set_data(b1_values[:upto], b2_values[:upto])
        visited.set_offsets([[b1_values[i], b2_values[i]] for i in range(upto)])
        visited.set_array(np.asarray(fitness_values[:upto]))
        current.set_offsets([[b1_values[frame_idx], b2_values[frame_idx]]])
        current_best_idx = best_so_far_indices[frame_idx]
        best.set_offsets([[b1_values[current_best_idx], b2_values[current_best_idx]]])
        frame_caption.set_text(
            f"eval {eval_ids[frame_idx]} / {eval_ids[-1]} | "
            f"B1={int(b1_values[frame_idx])}, B2={int(b2_values[frame_idx])}, "
            f"fitness={fitness_values[frame_idx]:.3g} | best={fitness_values[current_best_idx]:.3g}"
        )
        return path_line, visited, current, best, frame_caption

    ani = animation.FuncAnimation(fig, update, frames=frame_indices, interval=1000 / max(fps, 1), blit=False)
    suffix = resolved_output.suffix.lower()
    if suffix == ".gif":
        try:
            writer = animation.PillowWriter(fps=fps)
        except Exception as exc:  # pragma: no cover - depends on optional pillow install
            raise RuntimeError("Pillow is required for GIF output. Use .mp4 output or install pillow.") from exc
        ani.save(resolved_output, writer=writer, dpi=dpi)
    elif suffix == ".mp4":
        ani.save(resolved_output, writer=animation.FFMpegWriter(fps=fps), dpi=dpi)
    else:
        raise ValueError("Output extension must be .gif or .mp4")
    plt.close(fig)
    return resolved_output
