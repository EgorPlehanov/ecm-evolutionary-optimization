from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.utils.optimization_animation import render_evaluation_order_animation


@click.command("animate-trace")
@click.argument("optimize_file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Путь к итоговой анимации (.gif или .mp4). По умолчанию: plots/<stem>_evaluation_order.gif.",
)
@click.option("--fps", default=8, show_default=True, type=int, help="Кадров в секунду для анимации.")
@click.option("--dpi", default=120, show_default=True, type=int, help="DPI итогового файла.")
@click.option(
    "--max-frames",
    default=None,
    type=int,
    help="Максимум кадров. Если оценок больше, команда равномерно проредит трассу.",
)
@click.option(
    "--log-scale/--linear-scale",
    default=True,
    show_default=True,
    help="Использовать логарифмические оси B1/B2.",
)
def animate_trace_command(
    optimize_file: Path,
    output_path: Path | None,
    fps: int,
    dpi: int,
    max_frames: int | None,
    log_scale: bool,
) -> None:
    """Построить GIF/MP4 порядка оценок по optimize JSON."""

    try:
        rendered = render_evaluation_order_animation(
            optimize_file=optimize_file,
            output_path=output_path,
            fps=fps,
            dpi=dpi,
            max_frames=max_frames,
            log_scale=log_scale,
        )
    except (RuntimeError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"animation_file: {rendered}")
