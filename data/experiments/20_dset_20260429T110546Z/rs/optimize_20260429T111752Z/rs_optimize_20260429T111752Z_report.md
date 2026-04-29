# Отчёт по оптимизации: rs_optimize_20260429T111752Z

## Метаданные
- метод: `rs`
- датасет: `data/numbers/20_dset_20260429T110546Z/train.json`
- оптимум `(B1, B2)`: `(18335, 449991)`
- objective: `1.820565268119669`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `55`
- `best_eval_fraction`: `0.9166666666666666`
- `eval_per_sec`: `0.3561178670942976`
- `evaluation_count`: `60`
- `improvement_percent`: `20.139609236863038`
- `max_plateau_evals`: `30`
- `median_plateau_evals`: `2.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.11666666666666667`
- `p90_plateau_evals`: `18.099999999999998`
- `time_to_best_sec`: `147.45687789598014`
- `time_to_first_improvement_sec`: `1.5401083729811944`
- `total_runtime_sec`: `168.4835430739913`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `18335.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `449991.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `24.542732478865556` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.875200480745012` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `20.139609236863038` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.11666666666666667` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.5` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.26666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`rs_optimize_20260429T111752Z_b1_b2_trajectory.png`](plots/rs_optimize_20260429T111752Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/rs_optimize_20260429T111752Z_b1_b2_trajectory.png)
- [`rs_optimize_20260429T111752Z_b1_ratio_heatmap.png`](plots/rs_optimize_20260429T111752Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/rs_optimize_20260429T111752Z_b1_ratio_heatmap.png)
- [`rs_optimize_20260429T111752Z_jump_plot.png`](plots/rs_optimize_20260429T111752Z_jump_plot.png)
![jump_plot](plots/rs_optimize_20260429T111752Z_jump_plot.png)
- [`rs_optimize_20260429T111752Z_progress_by_phase.png`](plots/rs_optimize_20260429T111752Z_progress_by_phase.png)
![progress_by_phase](plots/rs_optimize_20260429T111752Z_progress_by_phase.png)
- [`rs_optimize_20260429T111752Z_time_efficiency.png`](plots/rs_optimize_20260429T111752Z_time_efficiency.png)
![time_efficiency](plots/rs_optimize_20260429T111752Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/rs_optimize_20260429T111752Z_events.csv"}, {"file": "tables/rs_optimize_20260429T111752Z_new_best.csv"}, {"file": "tables/rs_optimize_20260429T111752Z_phase_summary.csv"}, {"file": "tables/rs_optimize_20260429T111752Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T112043Z`
- validation file: [`rs_validate_20260429T112043Z.json`](rs_validate_20260429T112043Z.json)
- dataset: `data/numbers/20_dset_20260429T110546Z/control.json`
- method: `rs`
- optimized params: `(B1, B2)=(18335, 449991)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.079782670215061`
- baseline_mean_score: `2.2587397409944345`
- relative_improvement_pct: `7.922872543987106`
- optimized_mean_time_sec: `1.7218731862166898`
- baseline_mean_time_sec: `1.5002071478840662`
- time_improvement_pct: `-14.77569538615168`
- optimized_mean_curves: `83.24`
- baseline_mean_curves: `104.49000000000001`
- curves_improvement_pct: `20.336874342042314`
- optimized_mean_success_rate: `0.79`
- baseline_mean_success_rate: `0.58`
- success_rate_delta_pp: `21.000000000000007`
- trace plots:
  - curves_distribution_plot: [`rs_validate_20260429T112043Z_curves_distribution.png`](plots/rs_validate_20260429T112043Z_curves_distribution.png)
![curves_distribution_plot](plots/rs_validate_20260429T112043Z_curves_distribution.png)
  - curves_trace_plot: [`rs_validate_20260429T112043Z_curves_trace.png`](plots/rs_validate_20260429T112043Z_curves_trace.png)
![curves_trace_plot](plots/rs_validate_20260429T112043Z_curves_trace.png)
  - score_distribution_plot: [`rs_validate_20260429T112043Z_score_distribution.png`](plots/rs_validate_20260429T112043Z_score_distribution.png)
![score_distribution_plot](plots/rs_validate_20260429T112043Z_score_distribution.png)
  - score_trace_plot: [`rs_validate_20260429T112043Z_score_trace.png`](plots/rs_validate_20260429T112043Z_score_trace.png)
![score_trace_plot](plots/rs_validate_20260429T112043Z_score_trace.png)
  - time_distribution_plot: [`rs_validate_20260429T112043Z_time_distribution.png`](plots/rs_validate_20260429T112043Z_time_distribution.png)
![time_distribution_plot](plots/rs_validate_20260429T112043Z_time_distribution.png)
  - time_trace_plot: [`rs_validate_20260429T112043Z_time_trace.png`](plots/rs_validate_20260429T112043Z_time_trace.png)
![time_trace_plot](plots/rs_validate_20260429T112043Z_time_trace.png)

---
