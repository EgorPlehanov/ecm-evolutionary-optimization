from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DATA_DIR, EXPERIMENTS_DIR
from ecm_optimizer.utils.io_utils import ensure_dir, utc_timestamp
from ecm_optimizer.utils.multi_run_analysis import AnalysisOptions, generate_multi_run_artifacts


@click.command("analyze")
@click.option(
    "--input",
    "input_paths",
    type=click.Path(path_type=Path),
    multiple=True,
    help="Путь к optimize-run JSON/папке run/верхней директории экспериментов. Можно передать несколько.",
)
@click.option(
    "--group-by",
    type=click.Choice(["method", "divisor_size", "dataset"], case_sensitive=False),
    multiple=True,
    help="Уровень группировки графиков/статистики. По умолчанию: divisor_size + method.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    help="Каталог сохранения анализа. По умолчанию: data/analysis/analyze_<UTC_TIMESTAMP>/.",
)
@click.option(
    "--success-threshold",
    type=float,
    help="Порог качества для success-profile (objective <= threshold). По умолчанию берется 25-й перцентиль финальных objective.",
)
@click.option("--max-eval-points", default=300, show_default=True, type=int, help="Максимум точек на оси eval для overlay-кривой.")
@click.option("--max-time-points", default=200, show_default=True, type=int, help="Максимум точек на оси time для overlay-кривой.")
def analyze_command(
    input_paths: tuple[Path, ...],
    group_by: tuple[str, ...],
    output_dir: Path | None,
    success_threshold: float | None,
    max_eval_points: int,
    max_time_points: int,
) -> None:
    """Сравнительный multi-run анализ по optimize-результатам."""
    resolved_group_by = tuple(item.lower() for item in group_by) if group_by else ("divisor_size", "method")
    resolved_output_dir = output_dir or ensure_dir(DATA_DIR / "analysis" / f"analyze_{utc_timestamp()}")

    artifacts = generate_multi_run_artifacts(
        input_paths=list(input_paths),
        experiments_root=EXPERIMENTS_DIR,
        output_dir=resolved_output_dir,
        options=AnalysisOptions(
            success_threshold=success_threshold,
            max_eval_points=max_eval_points,
            max_time_points=max_time_points,
            group_by=resolved_group_by,
        ),
    )

    click.echo(f"analyzed_runs: {artifacts.total_runs}")
    click.echo(f"groups: {', '.join(artifacts.group_labels)}")
    click.echo(f"summary_file: {artifacts.summary_file}")
    click.echo(f"analyzer_params_file: {artifacts.analyzer_params_file}")
    click.echo("plot_files:")
    for plot_name, plot_path in artifacts.plots.items():
        click.echo(f"  {plot_name}: {plot_path}")
