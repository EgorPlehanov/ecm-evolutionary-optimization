from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.analysis import AnalysisOptions, run_analysis
from ecm_optimizer.config import DATA_DIR, EXPERIMENTS_DIR
from ecm_optimizer.utils.io_utils import ensure_dir, utc_timestamp


@click.command("analyze")
@click.option(
    "--input",
    "input_entries",
    type=str,
    multiple=True,
    help=(
        "Путь к optimize-run JSON/папке run/верхней директории экспериментов. "
        "Можно передать несколько. "
        "Префикс '!' исключает наборы по пути/маске (например: --input '!*/rs/*'). "
        "Если переданы только исключения — базовый поиск идет по data/experiments."
    ),
)
@click.option(
    "--group-by",
    type=click.Choice(["method", "divisor_size", "dataset", "seed"], case_sensitive=False),
    multiple=True,
    help="Явный порядок уровней группировки. По умолчанию включена авто-группировка.",
)
@click.option(
    "--auto-grouping/--no-auto-grouping",
    default=True,
    show_default=True,
    help="Автоматически подбирать иерархию групп по входным данным.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    help="Каталог сохранения анализа. По умолчанию: data/analysis/analyze_<UTC_TIMESTAMP>/.",
)
@click.option(
    "--success-threshold",
    type=float,
    help="Порог качества для success-метрики (objective <= threshold). По умолчанию 25-й перцентиль финальных objective.",
)
@click.option("--max-eval-points", default=300, show_default=True, type=int, help="Параметр совместимости: пока сохраняется в metadata.")
@click.option("--max-time-points", default=200, show_default=True, type=int, help="Параметр совместимости: пока сохраняется в metadata.")
@click.option("--max-series-per-plot", default=10, show_default=True, type=int, help="Максимум серий на графике до агрегации.")
@click.option("--bootstrap-iterations", default=2000, show_default=True, type=int, help="Количество bootstrap-итераций для доверительных интервалов.")
@click.option("--alpha", default=0.05, show_default=True, type=float, help="Уровень значимости для статистических тестов.")
def analyze_command(
    input_entries: tuple[str, ...],
    group_by: tuple[str, ...],
    auto_grouping: bool,
    output_dir: Path | None,
    success_threshold: float | None,
    max_eval_points: int,
    max_time_points: int,
    max_series_per_plot: int,
    bootstrap_iterations: int,
    alpha: float,
) -> None:
    """Иерархический multi-run анализ optimize+validate результатов."""
    normalized_group_by = tuple(item.lower() for item in group_by)
    if not auto_grouping and not normalized_group_by:
        raise click.ClickException("Укажите --group-by ... или включите --auto-grouping.")

    resolved_output_dir = output_dir or ensure_dir(DATA_DIR / "analysis" / f"analyze_{utc_timestamp()}")

    artifacts = run_analysis(
        input_entries=list(input_entries),
        experiments_root=EXPERIMENTS_DIR,
        output_dir=resolved_output_dir,
        options=AnalysisOptions(
            success_threshold=success_threshold,
            max_eval_points=max_eval_points,
            max_time_points=max_time_points,
            group_by=normalized_group_by,
            auto_grouping=auto_grouping,
            max_series_per_plot=max_series_per_plot,
            bootstrap_iterations=bootstrap_iterations,
            alpha=alpha,
        ),
    )

    click.echo(f"analyzed_runs: {artifacts.total_runs}")
    click.echo(f"group_by: {', '.join(artifacts.group_by)}")
    click.echo(f"summary_file: {artifacts.summary_file}")
    click.echo(f"overview_report: {artifacts.overview_report}")
    click.echo(f"output_dir: {artifacts.output_dir}")
