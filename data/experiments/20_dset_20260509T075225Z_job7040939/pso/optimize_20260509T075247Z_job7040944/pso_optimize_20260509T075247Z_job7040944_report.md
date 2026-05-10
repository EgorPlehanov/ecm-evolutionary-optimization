# Отчёт по оптимизации: pso_optimize_20260509T075247Z_job7040944

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260509T075225Z_job7040939/train.json`
- оптимум `(B1, B2)`: `(25910, 2742610)`
- objective: `24716.452219673156`
- max_curves_per_n: `260`
- repeats_per_n: `8`
- границы: `B1[100.0, 100000.0]`, `B2[10000.0, 5000000.0]`, `ratio_max=5000.0`

## Ключевые статистики
- `best_eval`: `213`
- `best_eval_fraction`: `0.8452380952380952`
- `eval_per_sec`: `0.020896032118893227`
- `evaluation_count`: `252`
- `improvement_percent`: `89.37552142896722`
- `max_plateau_evals`: `47`
- `median_plateau_evals`: `17.0`
- `new_best_count`: `10`
- `new_best_rate`: `0.03968253968253968`
- `p90_plateau_evals`: `44.0`
- `time_to_best_sec`: `10368.112282327987`
- `time_to_first_improvement_sec`: `1056.7936715169926`
- `total_runtime_sec`: `12060.757098981994`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.1349206349206349` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.14682539682539683` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `25910.0` | `within 2% of log-range [100.0, 100000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `2742610.0` | `within 2% of log-range [10000.0, 5000000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `105.85140872250096` | `within 2% of log-range up to ratio_max=5000.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.8596568355732098` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `89.37552142896722` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.03968253968253968` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.1865079365079365` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.01984126984126984` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260509T075247Z_job7040944_b1_b2_trajectory.png`](plots/pso_optimize_20260509T075247Z_job7040944_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260509T075247Z_job7040944_b1_b2_trajectory.png)
- [`pso_optimize_20260509T075247Z_job7040944_b1_ratio_heatmap.png`](plots/pso_optimize_20260509T075247Z_job7040944_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260509T075247Z_job7040944_b1_ratio_heatmap.png)
- [`pso_optimize_20260509T075247Z_job7040944_jump_plot.png`](plots/pso_optimize_20260509T075247Z_job7040944_jump_plot.png)
![jump_plot](plots/pso_optimize_20260509T075247Z_job7040944_jump_plot.png)
- [`pso_optimize_20260509T075247Z_job7040944_progress_by_phase.png`](plots/pso_optimize_20260509T075247Z_job7040944_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260509T075247Z_job7040944_progress_by_phase.png)
- [`pso_optimize_20260509T075247Z_job7040944_time_efficiency.png`](plots/pso_optimize_20260509T075247Z_job7040944_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260509T075247Z_job7040944_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260509T075247Z_job7040944_events.csv"}, {"file": "tables/pso_optimize_20260509T075247Z_job7040944_new_best.csv"}, {"file": "tables/pso_optimize_20260509T075247Z_job7040944_phase_summary.csv"}, {"file": "tables/pso_optimize_20260509T075247Z_job7040944_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260509T111423Z`
- validation file: [`pso_validate_20260509T111423Z_job7040945.json`](pso_validate_20260509T111423Z_job7040945.json)
- dataset: `data/numbers/20_dset_20260509T075225Z_job7040939/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(25910, 2742610)`
- baseline params: `(B1, B2)=(11000, 1900000)`
- max_curves_per_n: `600`
- repeats_per_n: `80`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `666`
- optimized_mean_score: `28269.368688157083`
- baseline_mean_score: `36489.858140865574`
- relative_improvement_pct: `22.528148563839533`
- optimized_mean_time_sec: `2.5639126500657086`
- baseline_mean_time_sec: `3.167272532836557`
- time_improvement_pct: `19.049825252343833`
- optimized_mean_curves: `52.60484375`
- baseline_mean_curves: `96.34265625`
- curves_improvement_pct: `45.39817999879986`
- optimized_mean_success_rate: `0.9998437499999999`
- baseline_mean_success_rate: `0.9978125`
- success_rate_delta_pp: `0.2031249999999929`
- trace plots:
  - score_trace_plot: [`pso_validate_20260509T111423Z_job7040945_score_trace.png`](plots/pso_validate_20260509T111423Z_job7040945_score_trace.png)
![score_trace_plot](plots/pso_validate_20260509T111423Z_job7040945_score_trace.png)
  - score_distribution_plot: [`pso_validate_20260509T111423Z_job7040945_score_distribution.png`](plots/pso_validate_20260509T111423Z_job7040945_score_distribution.png)
![score_distribution_plot](plots/pso_validate_20260509T111423Z_job7040945_score_distribution.png)
  - success_trace_plot: [`pso_validate_20260509T111423Z_job7040945_success_trace.png`](plots/pso_validate_20260509T111423Z_job7040945_success_trace.png)
![success_trace_plot](plots/pso_validate_20260509T111423Z_job7040945_success_trace.png)
  - success_distribution_plot: [`pso_validate_20260509T111423Z_job7040945_success_distribution.png`](plots/pso_validate_20260509T111423Z_job7040945_success_distribution.png)
![success_distribution_plot](plots/pso_validate_20260509T111423Z_job7040945_success_distribution.png)
  - time_trace_plot: [`pso_validate_20260509T111423Z_job7040945_time_trace.png`](plots/pso_validate_20260509T111423Z_job7040945_time_trace.png)
![time_trace_plot](plots/pso_validate_20260509T111423Z_job7040945_time_trace.png)
  - time_distribution_plot: [`pso_validate_20260509T111423Z_job7040945_time_distribution.png`](plots/pso_validate_20260509T111423Z_job7040945_time_distribution.png)
![time_distribution_plot](plots/pso_validate_20260509T111423Z_job7040945_time_distribution.png)
  - curves_trace_plot: [`pso_validate_20260509T111423Z_job7040945_curves_trace.png`](plots/pso_validate_20260509T111423Z_job7040945_curves_trace.png)
![curves_trace_plot](plots/pso_validate_20260509T111423Z_job7040945_curves_trace.png)
  - curves_distribution_plot: [`pso_validate_20260509T111423Z_job7040945_curves_distribution.png`](plots/pso_validate_20260509T111423Z_job7040945_curves_distribution.png)
![curves_distribution_plot](plots/pso_validate_20260509T111423Z_job7040945_curves_distribution.png)

---
