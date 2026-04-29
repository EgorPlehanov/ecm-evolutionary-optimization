# Отчёт по оптимизации: pso_optimize_20260429T112107Z

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260429T110546Z/train.json`
- оптимум `(B1, B2)`: `(100, 100)`
- objective: `2.185431040132353`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `126`
- `best_eval_fraction`: `0.5384615384615384`
- `eval_per_sec`: `0.8531426939928418`
- `evaluation_count`: `234`
- `improvement_percent`: `3.8711225817367807`
- `max_plateau_evals`: `108`
- `median_plateau_evals`: `5.0`
- `new_best_count`: `11`
- `new_best_rate`: `0.04700854700854701`
- `p90_plateau_evals`: `65.30000000000001`
- `time_to_best_sec`: `161.76573658600682`
- `time_to_first_improvement_sec`: `43.81756830099039`
- `total_runtime_sec`: `274.2800799370161`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8376068376068376` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8247863247863247` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `100.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ⚠️ ВНИМАНИЕ | `100.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `1.0` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.5897830298983202` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ⚠️ ВНИМАНИЕ | `3.8711225817367807` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.04700854700854701` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.46153846153846156` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.9102564102564102` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260429T112107Z_b1_b2_trajectory.png`](plots/pso_optimize_20260429T112107Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260429T112107Z_b1_b2_trajectory.png)
- [`pso_optimize_20260429T112107Z_b1_ratio_heatmap.png`](plots/pso_optimize_20260429T112107Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260429T112107Z_b1_ratio_heatmap.png)
- [`pso_optimize_20260429T112107Z_jump_plot.png`](plots/pso_optimize_20260429T112107Z_jump_plot.png)
![jump_plot](plots/pso_optimize_20260429T112107Z_jump_plot.png)
- [`pso_optimize_20260429T112107Z_progress_by_phase.png`](plots/pso_optimize_20260429T112107Z_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260429T112107Z_progress_by_phase.png)
- [`pso_optimize_20260429T112107Z_time_efficiency.png`](plots/pso_optimize_20260429T112107Z_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260429T112107Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260429T112107Z_events.csv"}, {"file": "tables/pso_optimize_20260429T112107Z_new_best.csv"}, {"file": "tables/pso_optimize_20260429T112107Z_phase_summary.csv"}, {"file": "tables/pso_optimize_20260429T112107Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T112544Z`
- validation file: [`pso_validate_20260429T112544Z.json`](pso_validate_20260429T112544Z.json)
- dataset: `data/numbers/20_dset_20260429T110546Z/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(100, 100)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.376332272327331`
- baseline_mean_score: `2.2384806875214736`
- relative_improvement_pct: `-6.158265540297857`
- optimized_mean_time_sec: `0.45191468796227124`
- baseline_mean_time_sec: `1.4431487558083609`
- time_improvement_pct: `68.68550895093713`
- optimized_mean_curves: `150.0`
- baseline_mean_curves: `100.17999999999999`
- curves_improvement_pct: `-49.730485126771825`
- optimized_mean_success_rate: `0.0`
- baseline_mean_success_rate: `0.5700000000000001`
- success_rate_delta_pp: `-57.00000000000001`
- trace plots:
  - curves_distribution_plot: [`pso_validate_20260429T112544Z_curves_distribution.png`](plots/pso_validate_20260429T112544Z_curves_distribution.png)
![curves_distribution_plot](plots/pso_validate_20260429T112544Z_curves_distribution.png)
  - curves_trace_plot: [`pso_validate_20260429T112544Z_curves_trace.png`](plots/pso_validate_20260429T112544Z_curves_trace.png)
![curves_trace_plot](plots/pso_validate_20260429T112544Z_curves_trace.png)
  - score_distribution_plot: [`pso_validate_20260429T112544Z_score_distribution.png`](plots/pso_validate_20260429T112544Z_score_distribution.png)
![score_distribution_plot](plots/pso_validate_20260429T112544Z_score_distribution.png)
  - score_trace_plot: [`pso_validate_20260429T112544Z_score_trace.png`](plots/pso_validate_20260429T112544Z_score_trace.png)
![score_trace_plot](plots/pso_validate_20260429T112544Z_score_trace.png)
  - time_distribution_plot: [`pso_validate_20260429T112544Z_time_distribution.png`](plots/pso_validate_20260429T112544Z_time_distribution.png)
![time_distribution_plot](plots/pso_validate_20260429T112544Z_time_distribution.png)
  - time_trace_plot: [`pso_validate_20260429T112544Z_time_trace.png`](plots/pso_validate_20260429T112544Z_time_trace.png)
![time_trace_plot](plots/pso_validate_20260429T112544Z_time_trace.png)

---
