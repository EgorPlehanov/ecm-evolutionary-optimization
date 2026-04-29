# Отчёт по оптимизации: ga_optimize_20260429T140903Z

## Метаданные
- метод: `ga`
- датасет: `data/numbers/20_dset_20260429T132020Z/train.json`
- оптимум `(B1, B2)`: `(28258, 386982)`
- objective: `1.5611369505729829`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `262`
- `best_eval_fraction`: `0.8291139240506329`
- `eval_per_sec`: `0.16446083426772196`
- `evaluation_count`: `316`
- `improvement_percent`: `91.443106283827`
- `max_plateau_evals`: `61`
- `median_plateau_evals`: `48.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.022151898734177215`
- `p90_plateau_evals`: `56.8`
- `time_to_best_sec`: `1529.9204995709006`
- `time_to_first_improvement_sec`: `64.81775996892247`
- `total_runtime_sec`: `1921.430212268955`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.4272151898734177` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.028481012658227847` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `28258.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `386982.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `13.694599759360182` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.7962404722283755` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `91.443106283827` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.022151898734177215` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.1930379746835443` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.04746835443037975` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`ga_optimize_20260429T140903Z_b1_b2_trajectory.png`](plots/ga_optimize_20260429T140903Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/ga_optimize_20260429T140903Z_b1_b2_trajectory.png)
- [`ga_optimize_20260429T140903Z_b1_ratio_heatmap.png`](plots/ga_optimize_20260429T140903Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/ga_optimize_20260429T140903Z_b1_ratio_heatmap.png)
- [`ga_optimize_20260429T140903Z_jump_plot.png`](plots/ga_optimize_20260429T140903Z_jump_plot.png)
![jump_plot](plots/ga_optimize_20260429T140903Z_jump_plot.png)
- [`ga_optimize_20260429T140903Z_progress_by_phase.png`](plots/ga_optimize_20260429T140903Z_progress_by_phase.png)
![progress_by_phase](plots/ga_optimize_20260429T140903Z_progress_by_phase.png)
- [`ga_optimize_20260429T140903Z_time_efficiency.png`](plots/ga_optimize_20260429T140903Z_time_efficiency.png)
![time_efficiency](plots/ga_optimize_20260429T140903Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/ga_optimize_20260429T140903Z_events.csv"}, {"file": "tables/ga_optimize_20260429T140903Z_new_best.csv"}, {"file": "tables/ga_optimize_20260429T140903Z_phase_summary.csv"}, {"file": "tables/ga_optimize_20260429T140903Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260429T144107Z`
- validation file: [`ga_validate_20260429T144107Z.json`](ga_validate_20260429T144107Z.json)
- dataset: `data/numbers/20_dset_20260429T132020Z/control.json`
- method: `ga`
- optimized params: `(B1, B2)=(28258, 386982)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `2.4124497480896756`
- baseline_mean_score: `5.081074883889727`
- relative_improvement_pct: `52.52087790048732`
- optimized_mean_time_sec: `1.9641468492231797`
- baseline_mean_time_sec: `1.6281843089545145`
- time_improvement_pct: `-20.6341836376247`
- optimized_mean_curves: `71.85`
- baseline_mean_curves: `110.42`
- curves_improvement_pct: `34.93026625611303`
- optimized_mean_success_rate: `0.8300000000000001`
- baseline_mean_success_rate: `0.53`
- success_rate_delta_pp: `30.000000000000004`
- trace plots:
  - curves_distribution_plot: [`ga_validate_20260429T144107Z_curves_distribution.png`](plots/ga_validate_20260429T144107Z_curves_distribution.png)
![curves_distribution_plot](plots/ga_validate_20260429T144107Z_curves_distribution.png)
  - curves_trace_plot: [`ga_validate_20260429T144107Z_curves_trace.png`](plots/ga_validate_20260429T144107Z_curves_trace.png)
![curves_trace_plot](plots/ga_validate_20260429T144107Z_curves_trace.png)
  - score_distribution_plot: [`ga_validate_20260429T144107Z_score_distribution.png`](plots/ga_validate_20260429T144107Z_score_distribution.png)
![score_distribution_plot](plots/ga_validate_20260429T144107Z_score_distribution.png)
  - score_trace_plot: [`ga_validate_20260429T144107Z_score_trace.png`](plots/ga_validate_20260429T144107Z_score_trace.png)
![score_trace_plot](plots/ga_validate_20260429T144107Z_score_trace.png)
  - time_distribution_plot: [`ga_validate_20260429T144107Z_time_distribution.png`](plots/ga_validate_20260429T144107Z_time_distribution.png)
![time_distribution_plot](plots/ga_validate_20260429T144107Z_time_distribution.png)
  - time_trace_plot: [`ga_validate_20260429T144107Z_time_trace.png`](plots/ga_validate_20260429T144107Z_time_trace.png)
![time_trace_plot](plots/ga_validate_20260429T144107Z_time_trace.png)

---
