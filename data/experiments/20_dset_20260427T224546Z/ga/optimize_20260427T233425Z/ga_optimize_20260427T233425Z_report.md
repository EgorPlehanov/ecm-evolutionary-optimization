# Отчёт по оптимизации: ga_optimize_20260427T233425Z

## Метаданные
- метод: `ga`
- датасет: `data/numbers/20_dset_20260427T224546Z/train.json`
- оптимум `(B1, B2)`: `(30000, 415232)`
- objective: `216484.67113078677`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `225`
- `best_eval_fraction`: `0.7120253164556962`
- `eval_per_sec`: `0.16974392528896634`
- `evaluation_count`: `316`
- `improvement_percent`: `80.31958289738415`
- `max_plateau_evals`: `91`
- `median_plateau_evals`: `21.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.022151898734177215`
- `p90_plateau_evals`: `90.3`
- `time_to_best_sec`: `1213.9269830180056`
- `time_to_first_improvement_sec`: `64.3195593910059`
- `total_runtime_sec`: `1861.6278232580007`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.3829113924050633` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.0379746835443038` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `30000.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `415232.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `13.841066666666666` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.6520782338187954` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `80.31958289738415` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.022151898734177215` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.2879746835443038` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.04746835443037975` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`ga_optimize_20260427T233425Z_b1_b2_trajectory.png`](plots/ga_optimize_20260427T233425Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/ga_optimize_20260427T233425Z_b1_b2_trajectory.png)
- [`ga_optimize_20260427T233425Z_b1_ratio_heatmap.png`](plots/ga_optimize_20260427T233425Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/ga_optimize_20260427T233425Z_b1_ratio_heatmap.png)
- [`ga_optimize_20260427T233425Z_jump_plot.png`](plots/ga_optimize_20260427T233425Z_jump_plot.png)
![jump_plot](plots/ga_optimize_20260427T233425Z_jump_plot.png)
- [`ga_optimize_20260427T233425Z_progress_by_phase.png`](plots/ga_optimize_20260427T233425Z_progress_by_phase.png)
![progress_by_phase](plots/ga_optimize_20260427T233425Z_progress_by_phase.png)
- [`ga_optimize_20260427T233425Z_time_efficiency.png`](plots/ga_optimize_20260427T233425Z_time_efficiency.png)
![time_efficiency](plots/ga_optimize_20260427T233425Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/ga_optimize_20260427T233425Z_events.csv"}, {"file": "tables/ga_optimize_20260427T233425Z_new_best.csv"}, {"file": "tables/ga_optimize_20260427T233425Z_phase_summary.csv"}, {"file": "tables/ga_optimize_20260427T233425Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260428T000530Z`
- validation file: [`ga_validate_20260428T000530Z.json`](ga_validate_20260428T000530Z.json)
- dataset: `data/numbers/20_dset_20260427T224546Z/control.json`
- method: `ga`
- optimized params: `(B1, B2)=(30000, 415232)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `187131.92893496965`
- baseline_mean_score: `587841.5721590911`
- relative_improvement_pct: `68.16626489214597`
- optimized_mean_time_sec: `1.928934969669499`
- baseline_mean_time_sec: `1.572159091059366`
- time_improvement_pct: `-22.693369941952078`
- optimized_mean_curves: `67.13`
- baseline_mean_curves: `107.84`
- curves_improvement_pct: `37.75037091988131`
- optimized_mean_success_rate: `0.8800000000000001`
- baseline_mean_success_rate: `0.52`
- success_rate_delta_pp: `36.00000000000001`
- trace plots:
  - curves_distribution_plot: [`ga_validate_20260428T000530Z_curves_distribution.png`](plots/ga_validate_20260428T000530Z_curves_distribution.png)
![curves_distribution_plot](plots/ga_validate_20260428T000530Z_curves_distribution.png)
  - curves_trace_plot: [`ga_validate_20260428T000530Z_curves_trace.png`](plots/ga_validate_20260428T000530Z_curves_trace.png)
![curves_trace_plot](plots/ga_validate_20260428T000530Z_curves_trace.png)
  - score_distribution_plot: [`ga_validate_20260428T000530Z_score_distribution.png`](plots/ga_validate_20260428T000530Z_score_distribution.png)
![score_distribution_plot](plots/ga_validate_20260428T000530Z_score_distribution.png)
  - score_trace_plot: [`ga_validate_20260428T000530Z_score_trace.png`](plots/ga_validate_20260428T000530Z_score_trace.png)
![score_trace_plot](plots/ga_validate_20260428T000530Z_score_trace.png)
  - time_distribution_plot: [`ga_validate_20260428T000530Z_time_distribution.png`](plots/ga_validate_20260428T000530Z_time_distribution.png)
![time_distribution_plot](plots/ga_validate_20260428T000530Z_time_distribution.png)
  - time_trace_plot: [`ga_validate_20260428T000530Z_time_trace.png`](plots/ga_validate_20260428T000530Z_time_trace.png)
![time_trace_plot](plots/ga_validate_20260428T000530Z_time_trace.png)

---
