# Отчёт по оптимизации: pso_optimize_20260428T140816Z

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260428T135130Z/train.json`
- оптимум `(B1, B2)`: `(8681, 114812)`
- objective: `-0.17941550481208682`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `211`
- `best_eval_fraction`: `0.9017094017094017`
- `eval_per_sec`: `0.2572520578642307`
- `evaluation_count`: `234`
- `improvement_percent`: `102.30798577407514`
- `max_plateau_evals`: `151`
- `median_plateau_evals`: `16.0`
- `new_best_count`: `6`
- `new_best_rate`: `0.02564102564102564`
- `p90_plateau_evals`: `74.20000000000005`
- `time_to_best_sec`: `827.3693174529908`
- `time_to_first_improvement_sec`: `47.672911165995174`
- `total_runtime_sec`: `909.613792928998`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.06837606837606838` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.17094017094017094` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `8681.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `114812.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `13.225665245939409` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.9095830822758566` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `102.30798577407514` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.02564102564102564` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.6452991452991453` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.1752136752136752` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260428T140816Z_b1_b2_trajectory.png`](plots/pso_optimize_20260428T140816Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260428T140816Z_b1_b2_trajectory.png)
- [`pso_optimize_20260428T140816Z_b1_ratio_heatmap.png`](plots/pso_optimize_20260428T140816Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260428T140816Z_b1_ratio_heatmap.png)
- [`pso_optimize_20260428T140816Z_jump_plot.png`](plots/pso_optimize_20260428T140816Z_jump_plot.png)
![jump_plot](plots/pso_optimize_20260428T140816Z_jump_plot.png)
- [`pso_optimize_20260428T140816Z_progress_by_phase.png`](plots/pso_optimize_20260428T140816Z_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260428T140816Z_progress_by_phase.png)
- [`pso_optimize_20260428T140816Z_time_efficiency.png`](plots/pso_optimize_20260428T140816Z_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260428T140816Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260428T140816Z_events.csv"}, {"file": "tables/pso_optimize_20260428T140816Z_new_best.csv"}, {"file": "tables/pso_optimize_20260428T140816Z_phase_summary.csv"}, {"file": "tables/pso_optimize_20260428T140816Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260428T142330Z`
- validation file: [`pso_validate_20260428T142330Z.json`](pso_validate_20260428T142330Z.json)
- dataset: `data/numbers/20_dset_20260428T135130Z/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(8681, 114812)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `6.367955156542946`
- baseline_mean_score: `2.0638214626558344`
- relative_improvement_pct: `-208.55164905341786`
- optimized_mean_time_sec: `1.441022998230619`
- baseline_mean_time_sec: `1.4618449678686738`
- time_improvement_pct: `1.4243623705468935`
- optimized_mean_curves: `121.10999999999999`
- baseline_mean_curves: `96.22`
- curves_improvement_pct: `-25.867802951569306`
- optimized_mean_success_rate: `0.33999999999999997`
- baseline_mean_success_rate: `0.58`
- success_rate_delta_pp: `-24.0`
- trace plots:
  - curves_distribution_plot: [`pso_validate_20260428T142330Z_curves_distribution.png`](plots/pso_validate_20260428T142330Z_curves_distribution.png)
![curves_distribution_plot](plots/pso_validate_20260428T142330Z_curves_distribution.png)
  - curves_trace_plot: [`pso_validate_20260428T142330Z_curves_trace.png`](plots/pso_validate_20260428T142330Z_curves_trace.png)
![curves_trace_plot](plots/pso_validate_20260428T142330Z_curves_trace.png)
  - score_distribution_plot: [`pso_validate_20260428T142330Z_score_distribution.png`](plots/pso_validate_20260428T142330Z_score_distribution.png)
![score_distribution_plot](plots/pso_validate_20260428T142330Z_score_distribution.png)
  - score_trace_plot: [`pso_validate_20260428T142330Z_score_trace.png`](plots/pso_validate_20260428T142330Z_score_trace.png)
![score_trace_plot](plots/pso_validate_20260428T142330Z_score_trace.png)
  - time_distribution_plot: [`pso_validate_20260428T142330Z_time_distribution.png`](plots/pso_validate_20260428T142330Z_time_distribution.png)
![time_distribution_plot](plots/pso_validate_20260428T142330Z_time_distribution.png)
  - time_trace_plot: [`pso_validate_20260428T142330Z_time_trace.png`](plots/pso_validate_20260428T142330Z_time_trace.png)
![time_trace_plot](plots/pso_validate_20260428T142330Z_time_trace.png)

---
