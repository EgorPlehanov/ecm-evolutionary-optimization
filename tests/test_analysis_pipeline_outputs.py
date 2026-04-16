from __future__ import annotations

import json
from pathlib import Path

from ecm_optimizer.analysis import AnalysisOptions, run_analysis


def _write_run(run_dir: Path, method: str, objective: float, seed: int) -> None:
    run_path = run_dir / f"{method}_optimize_20260101T00000{seed}Z.json"
    payload = {
        "dataset": str(run_dir / "dataset/train.json"),
        "config": {"method": method, "seed": seed},
        "optimized": {"method": method, "objective": objective},
        "run_stats": {
            "evaluation_count": 3,
            "total_runtime_sec": 10.0,
            "time_to_best_sec": 3.0,
        },
        "optimization_trace": [
            {"kind": "evaluation", "eval": 1, "fitness": objective + 0.2, "elapsed_sec": 1.0},
            {"kind": "evaluation", "eval": 2, "fitness": objective + 0.1, "elapsed_sec": 2.0},
            {"kind": "evaluation", "eval": 3, "fitness": objective, "elapsed_sec": 3.0},
        ],
    }
    run_path.write_text(json.dumps(payload), encoding="utf-8")


def test_analysis_generates_manifest_and_stats(tmp_path: Path) -> None:
    experiments_root = tmp_path / "experiments"
    run_dir = experiments_root / "20_dset_20260101T000000Z"
    run_dir.mkdir(parents=True)

    _write_run(run_dir, method="de", objective=0.8, seed=1)
    _write_run(run_dir, method="ga", objective=0.6, seed=2)

    output_dir = tmp_path / "analysis"
    artifacts = run_analysis(
        input_entries=[str(experiments_root)],
        experiments_root=experiments_root,
        output_dir=output_dir,
        options=AnalysisOptions(
            success_threshold=0.7,
            max_eval_points=100,
            max_time_points=100,
            max_series_per_plot=10,
            group_by=("method",),
            auto_grouping=False,
        ),
    )

    assert artifacts.summary_file.exists()
    manifest_file = output_dir / "manifest.json"
    assert manifest_file.exists()

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0.0"
    assert manifest["coverage_summary"]["total_runs"] == 2

    overview_report = output_dir / "overview" / "report.md"
    assert overview_report.exists()
    report_text = overview_report.read_text(encoding="utf-8")
    assert "Executive summary" in report_text
    assert "method_ranking.csv" in report_text

    stats_file = output_dir / "overview" / "stats" / "pairwise_mannwhitney_holm.json"
    assert stats_file.exists()
