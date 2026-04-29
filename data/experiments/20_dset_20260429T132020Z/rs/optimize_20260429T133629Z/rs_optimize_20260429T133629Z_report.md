# Отчёт по оптимизации: rs_optimize_20260429T133629Z

## Метаданные
- метод: `rs`
- датасет: `data/numbers/20_dset_20260429T132020Z/train.json`
- оптимум `(B1, B2)`: `(25951, 417950)`
- objective: `2.436366540313032`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `24`
- `best_eval_fraction`: `0.4`
- `eval_per_sec`: `0.351343825250062`
- `evaluation_count`: `60`
- `improvement_percent`: `86.66483699107775`
- `max_plateau_evals`: `36`
- `median_plateau_evals`: `2.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.11666666666666667`
- `p90_plateau_evals`: `15.699999999999996`
- `time_to_best_sec`: `67.6852618609555`
- `time_to_first_improvement_sec`: `1.5283917370252311`
- `total_runtime_sec`: `170.77288880001288`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `25951.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `417950.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `16.105352394898077` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.3963466469213373` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `86.66483699107775` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.11666666666666667` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.6` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.26666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`rs_optimize_20260429T133629Z_b1_b2_trajectory.png`](plots/rs_optimize_20260429T133629Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/rs_optimize_20260429T133629Z_b1_b2_trajectory.png)
- [`rs_optimize_20260429T133629Z_b1_ratio_heatmap.png`](plots/rs_optimize_20260429T133629Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/rs_optimize_20260429T133629Z_b1_ratio_heatmap.png)
- [`rs_optimize_20260429T133629Z_jump_plot.png`](plots/rs_optimize_20260429T133629Z_jump_plot.png)
![jump_plot](plots/rs_optimize_20260429T133629Z_jump_plot.png)
- [`rs_optimize_20260429T133629Z_progress_by_phase.png`](plots/rs_optimize_20260429T133629Z_progress_by_phase.png)
![progress_by_phase](plots/rs_optimize_20260429T133629Z_progress_by_phase.png)
- [`rs_optimize_20260429T133629Z_time_efficiency.png`](plots/rs_optimize_20260429T133629Z_time_efficiency.png)
![time_efficiency](plots/rs_optimize_20260429T133629Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/rs_optimize_20260429T133629Z_events.csv"}, {"file": "tables/rs_optimize_20260429T133629Z_new_best.csv"}, {"file": "tables/rs_optimize_20260429T133629Z_phase_summary.csv"}, {"file": "tables/rs_optimize_20260429T133629Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T133922Z`
- validation file: [`rs_validate_20260429T133922Z.json`](rs_validate_20260429T133922Z.json)
- dataset: `data/numbers/20_dset_20260429T132020Z/control.json`
- method: `rs`
- optimized params: `(B1, B2)=(25951, 417950)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.2538216450831823`
- baseline_mean_score: `4.797331136137473`
- relative_improvement_pct: `53.01926047786173`
- optimized_mean_time_sec: `1.667318265006179`
- baseline_mean_time_sec: `1.4316325024026446`
- time_improvement_pct: `-16.462727844470816`
- optimized_mean_curves: `67.39`
- baseline_mean_curves: `102.1`
- curves_improvement_pct: `33.996082272282074`
- optimized_mean_success_rate: `0.82`
- baseline_mean_success_rate: `0.56`
- success_rate_delta_pp: `25.99999999999999`
- trace plots:
  - curves_distribution_plot: [`rs_validate_20260429T133922Z_curves_distribution.png`](plots/rs_validate_20260429T133922Z_curves_distribution.png)
![curves_distribution_plot](plots/rs_validate_20260429T133922Z_curves_distribution.png)
  - curves_trace_plot: [`rs_validate_20260429T133922Z_curves_trace.png`](plots/rs_validate_20260429T133922Z_curves_trace.png)
![curves_trace_plot](plots/rs_validate_20260429T133922Z_curves_trace.png)
  - score_distribution_plot: [`rs_validate_20260429T133922Z_score_distribution.png`](plots/rs_validate_20260429T133922Z_score_distribution.png)
![score_distribution_plot](plots/rs_validate_20260429T133922Z_score_distribution.png)
  - score_trace_plot: [`rs_validate_20260429T133922Z_score_trace.png`](plots/rs_validate_20260429T133922Z_score_trace.png)
![score_trace_plot](plots/rs_validate_20260429T133922Z_score_trace.png)
  - time_distribution_plot: [`rs_validate_20260429T133922Z_time_distribution.png`](plots/rs_validate_20260429T133922Z_time_distribution.png)
![time_distribution_plot](plots/rs_validate_20260429T133922Z_time_distribution.png)
  - time_trace_plot: [`rs_validate_20260429T133922Z_time_trace.png`](plots/rs_validate_20260429T133922Z_time_trace.png)
![time_trace_plot](plots/rs_validate_20260429T133922Z_time_trace.png)

---
