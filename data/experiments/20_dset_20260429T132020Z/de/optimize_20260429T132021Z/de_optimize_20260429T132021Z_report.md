# Отчёт по оптимизации: de_optimize_20260429T132021Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260429T132020Z/train.json`
- оптимум `(B1, B2)`: `(18490, 479445)`
- objective: `1.631240423159824`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `175`
- `best_eval_fraction`: `0.7954545454545454`
- `eval_per_sec`: `0.23670483943045853`
- `evaluation_count`: `220`
- `improvement_percent`: `57.20842288284682`
- `max_plateau_evals`: `68`
- `median_plateau_evals`: `17.0`
- `new_best_count`: `8`
- `new_best_rate`: `0.03636363636363636`
- `p90_plateau_evals`: `49.6`
- `time_to_best_sec`: `681.3501354389591`
- `time_to_first_improvement_sec`: `5.707130028982647`
- `total_runtime_sec`: `929.441536157974`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.05454545454545454` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.10454545454545454` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `18490.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `479445.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `25.929962141698216` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.7330747647188778` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `57.20842288284682` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.03636363636363636` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.3090909090909091` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.33181818181818185` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`de_optimize_20260429T132021Z_b1_b2_trajectory.png`](plots/de_optimize_20260429T132021Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260429T132021Z_b1_b2_trajectory.png)
- [`de_optimize_20260429T132021Z_b1_ratio_heatmap.png`](plots/de_optimize_20260429T132021Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260429T132021Z_b1_ratio_heatmap.png)
- [`de_optimize_20260429T132021Z_jump_plot.png`](plots/de_optimize_20260429T132021Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260429T132021Z_jump_plot.png)
- [`de_optimize_20260429T132021Z_progress_by_phase.png`](plots/de_optimize_20260429T132021Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260429T132021Z_progress_by_phase.png)
- [`de_optimize_20260429T132021Z_time_efficiency.png`](plots/de_optimize_20260429T132021Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260429T132021Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/de_optimize_20260429T132021Z_events.csv"}, {"file": "tables/de_optimize_20260429T132021Z_new_best.csv"}, {"file": "tables/de_optimize_20260429T132021Z_phase_summary.csv"}, {"file": "tables/de_optimize_20260429T132021Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T133605Z`
- validation file: [`de_validate_20260429T133605Z.json`](de_validate_20260429T133605Z.json)
- dataset: `data/numbers/20_dset_20260429T132020Z/control.json`
- method: `de`
- optimized params: `(B1, B2)=(18490, 479445)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.0467015838500724`
- baseline_mean_score: `6.370492076038167`
- relative_improvement_pct: `67.8721587057852`
- optimized_mean_time_sec: `1.3624727736436761`
- baseline_mean_time_sec: `1.5820194095012265`
- time_improvement_pct: `13.877619613198569`
- optimized_mean_curves: `65.53999999999999`
- baseline_mean_curves: `110.34`
- curves_improvement_pct: `40.60177632771435`
- optimized_mean_success_rate: `0.8400000000000001`
- baseline_mean_success_rate: `0.44000000000000006`
- success_rate_delta_pp: `40.0`
- trace plots:
  - curves_distribution_plot: [`de_validate_20260429T133605Z_curves_distribution.png`](plots/de_validate_20260429T133605Z_curves_distribution.png)
![curves_distribution_plot](plots/de_validate_20260429T133605Z_curves_distribution.png)
  - curves_trace_plot: [`de_validate_20260429T133605Z_curves_trace.png`](plots/de_validate_20260429T133605Z_curves_trace.png)
![curves_trace_plot](plots/de_validate_20260429T133605Z_curves_trace.png)
  - score_distribution_plot: [`de_validate_20260429T133605Z_score_distribution.png`](plots/de_validate_20260429T133605Z_score_distribution.png)
![score_distribution_plot](plots/de_validate_20260429T133605Z_score_distribution.png)
  - score_trace_plot: [`de_validate_20260429T133605Z_score_trace.png`](plots/de_validate_20260429T133605Z_score_trace.png)
![score_trace_plot](plots/de_validate_20260429T133605Z_score_trace.png)
  - time_distribution_plot: [`de_validate_20260429T133605Z_time_distribution.png`](plots/de_validate_20260429T133605Z_time_distribution.png)
![time_distribution_plot](plots/de_validate_20260429T133605Z_time_distribution.png)
  - time_trace_plot: [`de_validate_20260429T133605Z_time_trace.png`](plots/de_validate_20260429T133605Z_time_trace.png)
![time_trace_plot](plots/de_validate_20260429T133605Z_time_trace.png)

---
