# Отчёт по оптимизации: de_optimize_20260429T110547Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260429T110546Z/train.json`
- оптимум `(B1, B2)`: `(8803, 483601)`
- objective: `1.8675693726390064`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `176`
- `best_eval_fraction`: `0.8`
- `eval_per_sec`: `0.32028230882769204`
- `evaluation_count`: `220`
- `improvement_percent`: `13.911051936017923`
- `max_plateau_evals`: `80`
- `median_plateau_evals`: `38.0`
- `new_best_count`: `5`
- `new_best_rate`: `0.022727272727272728`
- `p90_plateau_evals`: `64.5`
- `time_to_best_sec`: `525.5476249720086`
- `time_to_first_improvement_sec`: `5.852665870974306`
- `total_runtime_sec`: `686.8944523180253`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.04090909090909091` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.03636363636363636` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `8803.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `483601.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `54.9359309326366` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.7651068125509992` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `13.911051936017923` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.022727272727272728` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.36363636363636365` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.3409090909090909` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`de_optimize_20260429T110547Z_b1_b2_trajectory.png`](plots/de_optimize_20260429T110547Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260429T110547Z_b1_b2_trajectory.png)
- [`de_optimize_20260429T110547Z_b1_ratio_heatmap.png`](plots/de_optimize_20260429T110547Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260429T110547Z_b1_ratio_heatmap.png)
- [`de_optimize_20260429T110547Z_jump_plot.png`](plots/de_optimize_20260429T110547Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260429T110547Z_jump_plot.png)
- [`de_optimize_20260429T110547Z_progress_by_phase.png`](plots/de_optimize_20260429T110547Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260429T110547Z_progress_by_phase.png)
- [`de_optimize_20260429T110547Z_time_efficiency.png`](plots/de_optimize_20260429T110547Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260429T110547Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/de_optimize_20260429T110547Z_events.csv"}, {"file": "tables/de_optimize_20260429T110547Z_new_best.csv"}, {"file": "tables/de_optimize_20260429T110547Z_phase_summary.csv"}, {"file": "tables/de_optimize_20260429T110547Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T111728Z`
- validation file: [`de_validate_20260429T111728Z.json`](de_validate_20260429T111728Z.json)
- dataset: `data/numbers/20_dset_20260429T110546Z/control.json`
- method: `de`
- optimized params: `(B1, B2)=(8803, 483601)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.4169863105907594`
- baseline_mean_score: `2.242048291248556`
- relative_improvement_pct: `-7.802598187784065`
- optimized_mean_time_sec: `1.629120597144356`
- baseline_mean_time_sec: `1.414855014726054`
- time_improvement_pct: `-15.143995687769362`
- optimized_mean_curves: `107.09`
- baseline_mean_curves: `101.0`
- curves_improvement_pct: `-6.029702970297033`
- optimized_mean_success_rate: `0.47000000000000003`
- baseline_mean_success_rate: `0.54`
- success_rate_delta_pp: `-7.000000000000001`
- trace plots:
  - curves_distribution_plot: [`de_validate_20260429T111728Z_curves_distribution.png`](plots/de_validate_20260429T111728Z_curves_distribution.png)
![curves_distribution_plot](plots/de_validate_20260429T111728Z_curves_distribution.png)
  - curves_trace_plot: [`de_validate_20260429T111728Z_curves_trace.png`](plots/de_validate_20260429T111728Z_curves_trace.png)
![curves_trace_plot](plots/de_validate_20260429T111728Z_curves_trace.png)
  - score_distribution_plot: [`de_validate_20260429T111728Z_score_distribution.png`](plots/de_validate_20260429T111728Z_score_distribution.png)
![score_distribution_plot](plots/de_validate_20260429T111728Z_score_distribution.png)
  - score_trace_plot: [`de_validate_20260429T111728Z_score_trace.png`](plots/de_validate_20260429T111728Z_score_trace.png)
![score_trace_plot](plots/de_validate_20260429T111728Z_score_trace.png)
  - time_distribution_plot: [`de_validate_20260429T111728Z_time_distribution.png`](plots/de_validate_20260429T111728Z_time_distribution.png)
![time_distribution_plot](plots/de_validate_20260429T111728Z_time_distribution.png)
  - time_trace_plot: [`de_validate_20260429T111728Z_time_trace.png`](plots/de_validate_20260429T111728Z_time_trace.png)
![time_trace_plot](plots/de_validate_20260429T111728Z_time_trace.png)

---
