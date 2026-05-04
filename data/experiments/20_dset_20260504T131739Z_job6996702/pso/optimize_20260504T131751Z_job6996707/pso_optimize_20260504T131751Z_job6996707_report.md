# Отчёт по оптимизации: pso_optimize_20260504T131751Z_job6996707

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260504T131739Z_job6996702/train.json`
- оптимум `(B1, B2)`: `(30000, 600000)`
- objective: `14651.193108181662`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `211`
- `best_eval_fraction`: `0.9017094017094017`
- `eval_per_sec`: `0.1721464789405887`
- `evaluation_count`: `234`
- `improvement_percent`: `98.27723113782417`
- `max_plateau_evals`: `71`
- `median_plateau_evals`: `16.0`
- `new_best_count`: `10`
- `new_best_rate`: `0.042735042735042736`
- `p90_plateau_evals`: `47.0`
- `time_to_best_sec`: `1215.381971883995`
- `time_to_first_improvement_sec`: `45.69034294501762`
- `total_runtime_sec`: `1359.9225673839974`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8632478632478633` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8076923076923077` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `30000.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ⚠️ ВНИМАНИЕ | `600000.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `20.0` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.8937140989004642` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `98.27723113782417` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.042735042735042736` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.3034188034188034` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.07692307692307693` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260504T131751Z_job6996707_b1_b2_trajectory.png`](plots/pso_optimize_20260504T131751Z_job6996707_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260504T131751Z_job6996707_b1_b2_trajectory.png)
- [`pso_optimize_20260504T131751Z_job6996707_b1_ratio_heatmap.png`](plots/pso_optimize_20260504T131751Z_job6996707_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260504T131751Z_job6996707_b1_ratio_heatmap.png)
- [`pso_optimize_20260504T131751Z_job6996707_jump_plot.png`](plots/pso_optimize_20260504T131751Z_job6996707_jump_plot.png)
![jump_plot](plots/pso_optimize_20260504T131751Z_job6996707_jump_plot.png)
- [`pso_optimize_20260504T131751Z_job6996707_progress_by_phase.png`](plots/pso_optimize_20260504T131751Z_job6996707_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260504T131751Z_job6996707_progress_by_phase.png)
- [`pso_optimize_20260504T131751Z_job6996707_time_efficiency.png`](plots/pso_optimize_20260504T131751Z_job6996707_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260504T131751Z_job6996707_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260504T131751Z_job6996707_events.csv"}, {"file": "tables/pso_optimize_20260504T131751Z_job6996707_new_best.csv"}, {"file": "tables/pso_optimize_20260504T131751Z_job6996707_phase_summary.csv"}, {"file": "tables/pso_optimize_20260504T131751Z_job6996707_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260504T134050Z`
- validation file: [`pso_validate_20260504T134050Z_job6996708.json`](pso_validate_20260504T134050Z_job6996708.json)
- dataset: `data/numbers/20_dset_20260504T131739Z_job6996702/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(30000, 600000)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `117549.36179587475`
- baseline_mean_score: `441540.93758015876`
- relative_improvement_pct: `73.37747153410109`
- optimized_mean_time_sec: `1.5775361795874778`
- baseline_mean_time_sec: `1.2608937580158819`
- time_improvement_pct: `-25.11253779778071`
- optimized_mean_curves: `67.74`
- baseline_mean_curves: `114.32000000000001`
- curves_improvement_pct: `40.74527641707489`
- optimized_mean_success_rate: `0.8300000000000001`
- baseline_mean_success_rate: `0.44000000000000006`
- success_rate_delta_pp: `39.0`
- trace plots:
  - curves_distribution_plot: [`pso_validate_20260504T134050Z_job6996708_curves_distribution.png`](plots/pso_validate_20260504T134050Z_job6996708_curves_distribution.png)
![curves_distribution_plot](plots/pso_validate_20260504T134050Z_job6996708_curves_distribution.png)
  - curves_trace_plot: [`pso_validate_20260504T134050Z_job6996708_curves_trace.png`](plots/pso_validate_20260504T134050Z_job6996708_curves_trace.png)
![curves_trace_plot](plots/pso_validate_20260504T134050Z_job6996708_curves_trace.png)
  - score_distribution_plot: [`pso_validate_20260504T134050Z_job6996708_score_distribution.png`](plots/pso_validate_20260504T134050Z_job6996708_score_distribution.png)
![score_distribution_plot](plots/pso_validate_20260504T134050Z_job6996708_score_distribution.png)
  - score_trace_plot: [`pso_validate_20260504T134050Z_job6996708_score_trace.png`](plots/pso_validate_20260504T134050Z_job6996708_score_trace.png)
![score_trace_plot](plots/pso_validate_20260504T134050Z_job6996708_score_trace.png)
  - time_distribution_plot: [`pso_validate_20260504T134050Z_job6996708_time_distribution.png`](plots/pso_validate_20260504T134050Z_job6996708_time_distribution.png)
![time_distribution_plot](plots/pso_validate_20260504T134050Z_job6996708_time_distribution.png)
  - time_trace_plot: [`pso_validate_20260504T134050Z_job6996708_time_trace.png`](plots/pso_validate_20260504T134050Z_job6996708_time_trace.png)
![time_trace_plot](plots/pso_validate_20260504T134050Z_job6996708_time_trace.png)

---
