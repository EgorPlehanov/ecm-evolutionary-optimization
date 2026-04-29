# Отчёт по оптимизации: de_optimize_20260428T135130Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260428T135130Z/train.json`
- оптимум `(B1, B2)`: `(7713, 133971)`
- objective: `-0.3467059700566294`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `142`
- `best_eval_fraction`: `0.6454545454545455`
- `eval_per_sec`: `0.29747550849157833`
- `evaluation_count`: `220`
- `improvement_percent`: `131.1810469616701`
- `max_plateau_evals`: `78`
- `median_plateau_evals`: `20.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.031818181818181815`
- `p90_plateau_evals`: `59.8`
- `time_to_best_sec`: `471.41900664099376`
- `time_to_first_improvement_sec`: `9.876260210992768`
- `total_runtime_sec`: `739.5571381869959`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.00909090909090909` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.00909090909090909` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `7713.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `133971.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `17.369506028782574` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.6374341917605779` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `131.1810469616701` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.031818181818181815` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.35454545454545455` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.16818181818181818` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`de_optimize_20260428T135130Z_b1_b2_trajectory.png`](plots/de_optimize_20260428T135130Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260428T135130Z_b1_b2_trajectory.png)
- [`de_optimize_20260428T135130Z_b1_ratio_heatmap.png`](plots/de_optimize_20260428T135130Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260428T135130Z_b1_ratio_heatmap.png)
- [`de_optimize_20260428T135130Z_jump_plot.png`](plots/de_optimize_20260428T135130Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260428T135130Z_jump_plot.png)
- [`de_optimize_20260428T135130Z_progress_by_phase.png`](plots/de_optimize_20260428T135130Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260428T135130Z_progress_by_phase.png)
- [`de_optimize_20260428T135130Z_time_efficiency.png`](plots/de_optimize_20260428T135130Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260428T135130Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/de_optimize_20260428T135130Z_events.csv"}, {"file": "tables/de_optimize_20260428T135130Z_new_best.csv"}, {"file": "tables/de_optimize_20260428T135130Z_phase_summary.csv"}, {"file": "tables/de_optimize_20260428T135130Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260428T140400Z`
- validation file: [`de_validate_20260428T140400Z.json`](de_validate_20260428T140400Z.json)
- dataset: `data/numbers/20_dset_20260428T135130Z/control.json`
- method: `de`
- optimized params: `(B1, B2)=(7713, 133971)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `9.753411037952954`
- baseline_mean_score: `5.712222922172258`
- relative_improvement_pct: `-70.74633064642202`
- optimized_mean_time_sec: `1.3865572644973871`
- baseline_mean_time_sec: `1.5635987985142856`
- time_improvement_pct: `11.322695705901117`
- optimized_mean_curves: `116.87`
- baseline_mean_curves: `102.91`
- curves_improvement_pct: `-13.565251190360517`
- optimized_mean_success_rate: `0.37`
- baseline_mean_success_rate: `0.5900000000000001`
- success_rate_delta_pp: `-22.000000000000007`
- trace plots:
  - curves_distribution_plot: [`de_validate_20260428T140400Z_curves_distribution.png`](plots/de_validate_20260428T140400Z_curves_distribution.png)
![curves_distribution_plot](plots/de_validate_20260428T140400Z_curves_distribution.png)
  - curves_trace_plot: [`de_validate_20260428T140400Z_curves_trace.png`](plots/de_validate_20260428T140400Z_curves_trace.png)
![curves_trace_plot](plots/de_validate_20260428T140400Z_curves_trace.png)
  - score_distribution_plot: [`de_validate_20260428T140400Z_score_distribution.png`](plots/de_validate_20260428T140400Z_score_distribution.png)
![score_distribution_plot](plots/de_validate_20260428T140400Z_score_distribution.png)
  - score_trace_plot: [`de_validate_20260428T140400Z_score_trace.png`](plots/de_validate_20260428T140400Z_score_trace.png)
![score_trace_plot](plots/de_validate_20260428T140400Z_score_trace.png)
  - time_distribution_plot: [`de_validate_20260428T140400Z_time_distribution.png`](plots/de_validate_20260428T140400Z_time_distribution.png)
![time_distribution_plot](plots/de_validate_20260428T140400Z_time_distribution.png)
  - time_trace_plot: [`de_validate_20260428T140400Z_time_trace.png`](plots/de_validate_20260428T140400Z_time_trace.png)
![time_trace_plot](plots/de_validate_20260428T140400Z_time_trace.png)

---
