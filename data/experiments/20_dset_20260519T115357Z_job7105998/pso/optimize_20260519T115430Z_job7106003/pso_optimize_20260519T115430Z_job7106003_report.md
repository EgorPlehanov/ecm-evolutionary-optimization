# Отчёт по оптимизации: pso_optimize_20260519T115430Z_job7106003

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260519T115357Z_job7105998/train.json`
- оптимум `(B1, B2)`: `(52298, 2726216)`
- objective: `25799.227981843866`
- max_curves_per_n: `260`
- repeats_per_n: `8`
- границы: `B1[100.0, 1000000.0]`, `B2[10000.0, 100000000.0]`, `ratio_max=100000.0`

## Ключевые статистики
- `best_eval`: `228`
- `best_eval_fraction`: `0.9047619047619048`
- `eval_per_sec`: `0.010867143870142343`
- `evaluation_count`: `252`
- `improvement_percent`: `94.34236861422737`
- `max_plateau_evals`: `141`
- `median_plateau_evals`: `11.0`
- `new_best_count`: `6`
- `new_best_rate`: `0.023809523809523808`
- `p90_plateau_evals`: `85.20000000000003`
- `time_to_best_sec`: `21990.360062132`
- `time_to_first_improvement_sec`: `2878.4481347180003`
- `total_runtime_sec`: `23189.173294139`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.03968253968253968` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.04365079365079365` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `52298.0` | `within 2% of log-range [100.0, 1000000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `2726216.0` | `within 2% of log-range [10000.0, 100000000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `52.1284943974913` | `within 2% of log-range up to ratio_max=100000.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.9483028904566427` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `94.34236861422737` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.023809523809523808` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.5595238095238095` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.04365079365079365` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260519T115430Z_job7106003_b1_b2_trajectory.png`](plots/pso_optimize_20260519T115430Z_job7106003_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260519T115430Z_job7106003_b1_b2_trajectory.png)
- [`pso_optimize_20260519T115430Z_job7106003_b1_ratio_heatmap.png`](plots/pso_optimize_20260519T115430Z_job7106003_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260519T115430Z_job7106003_b1_ratio_heatmap.png)
- [`pso_optimize_20260519T115430Z_job7106003_jump_plot.png`](plots/pso_optimize_20260519T115430Z_job7106003_jump_plot.png)
![jump_plot](plots/pso_optimize_20260519T115430Z_job7106003_jump_plot.png)
- [`pso_optimize_20260519T115430Z_job7106003_progress_by_phase.png`](plots/pso_optimize_20260519T115430Z_job7106003_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260519T115430Z_job7106003_progress_by_phase.png)
- [`pso_optimize_20260519T115430Z_job7106003_time_efficiency.png`](plots/pso_optimize_20260519T115430Z_job7106003_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260519T115430Z_job7106003_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260519T115430Z_job7106003_events.csv"}, {"file": "tables/pso_optimize_20260519T115430Z_job7106003_new_best.csv"}, {"file": "tables/pso_optimize_20260519T115430Z_job7106003_phase_summary.csv"}, {"file": "tables/pso_optimize_20260519T115430Z_job7106003_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260519T182113Z`
- validation file: [`pso_validate_20260519T182113Z_job7106004.json`](pso_validate_20260519T182113Z_job7106004.json)
- dataset: `data/numbers/20_dset_20260519T115357Z_job7105998/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(52298, 2726216)`
- baseline params: `(B1, B2)=(11000, 1900000)`
- max_curves_per_n: `600`
- repeats_per_n: `80`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `1001`
- optimized_mean_score: `27131.85334207522`
- baseline_mean_score: `35917.53282104856`
- relative_improvement_pct: `24.46069868647747`
- optimized_mean_time_sec: `2.536523615457522`
- baseline_mean_time_sec: `3.121632188354856`
- time_improvement_pct: `18.743674385472506`
- optimized_mean_curves: `35.33234375`
- baseline_mean_curves: `94.02421875`
- curves_improvement_pct: `62.42208207659263`
- optimized_mean_success_rate: `1.0`
- baseline_mean_success_rate: `0.99765625`
- success_rate_delta_pp: `0.23437499999999778`
- trace plots:
  - score_trace_plot: [`pso_validate_20260519T182113Z_job7106004_score_trace.png`](plots/pso_validate_20260519T182113Z_job7106004_score_trace.png)
![score_trace_plot](plots/pso_validate_20260519T182113Z_job7106004_score_trace.png)
  - score_distribution_plot: [`pso_validate_20260519T182113Z_job7106004_score_distribution.png`](plots/pso_validate_20260519T182113Z_job7106004_score_distribution.png)
![score_distribution_plot](plots/pso_validate_20260519T182113Z_job7106004_score_distribution.png)
  - success_trace_plot: [`pso_validate_20260519T182113Z_job7106004_success_trace.png`](plots/pso_validate_20260519T182113Z_job7106004_success_trace.png)
![success_trace_plot](plots/pso_validate_20260519T182113Z_job7106004_success_trace.png)
  - success_distribution_plot: [`pso_validate_20260519T182113Z_job7106004_success_distribution.png`](plots/pso_validate_20260519T182113Z_job7106004_success_distribution.png)
![success_distribution_plot](plots/pso_validate_20260519T182113Z_job7106004_success_distribution.png)
  - time_trace_plot: [`pso_validate_20260519T182113Z_job7106004_time_trace.png`](plots/pso_validate_20260519T182113Z_job7106004_time_trace.png)
![time_trace_plot](plots/pso_validate_20260519T182113Z_job7106004_time_trace.png)
  - time_distribution_plot: [`pso_validate_20260519T182113Z_job7106004_time_distribution.png`](plots/pso_validate_20260519T182113Z_job7106004_time_distribution.png)
![time_distribution_plot](plots/pso_validate_20260519T182113Z_job7106004_time_distribution.png)
  - curves_trace_plot: [`pso_validate_20260519T182113Z_job7106004_curves_trace.png`](plots/pso_validate_20260519T182113Z_job7106004_curves_trace.png)
![curves_trace_plot](plots/pso_validate_20260519T182113Z_job7106004_curves_trace.png)
  - curves_distribution_plot: [`pso_validate_20260519T182113Z_job7106004_curves_distribution.png`](plots/pso_validate_20260519T182113Z_job7106004_curves_distribution.png)
![curves_distribution_plot](plots/pso_validate_20260519T182113Z_job7106004_curves_distribution.png)

---
