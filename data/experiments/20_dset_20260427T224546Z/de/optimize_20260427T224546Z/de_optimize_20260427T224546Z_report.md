# Отчёт по оптимизации: de_optimize_20260427T224546Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260427T224546Z/train.json`
- оптимум `(B1, B2)`: `(28430, 426878)`
- objective: `250284.6547049171`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `172`
- `best_eval_fraction`: `0.7818181818181819`
- `eval_per_sec`: `0.24928975630651878`
- `evaluation_count`: `220`
- `improvement_percent`: `60.290241135020516`
- `max_plateau_evals`: `48`
- `median_plateau_evals`: `20.0`
- `new_best_count`: `8`
- `new_best_rate`: `0.03636363636363636`
- `p90_plateau_evals`: `44.8`
- `time_to_best_sec`: `640.6142781399976`
- `time_to_first_improvement_sec`: `5.983996392002155`
- `total_runtime_sec`: `882.5146604269976`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.14545454545454545` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.06363636363636363` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `28430.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `426878.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `15.015054519873374` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.7258964716008701` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `60.290241135020516` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.03636363636363636` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.21818181818181817` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.35454545454545455` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`de_optimize_20260427T224546Z_b1_b2_trajectory.png`](plots/de_optimize_20260427T224546Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260427T224546Z_b1_b2_trajectory.png)
- [`de_optimize_20260427T224546Z_b1_ratio_heatmap.png`](plots/de_optimize_20260427T224546Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260427T224546Z_b1_ratio_heatmap.png)
- [`de_optimize_20260427T224546Z_jump_plot.png`](plots/de_optimize_20260427T224546Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260427T224546Z_jump_plot.png)
- [`de_optimize_20260427T224546Z_progress_by_phase.png`](plots/de_optimize_20260427T224546Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260427T224546Z_progress_by_phase.png)
- [`de_optimize_20260427T224546Z_time_efficiency.png`](plots/de_optimize_20260427T224546Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260427T224546Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/de_optimize_20260427T224546Z_events.csv"}, {"file": "tables/de_optimize_20260427T224546Z_new_best.csv"}, {"file": "tables/de_optimize_20260427T224546Z_phase_summary.csv"}, {"file": "tables/de_optimize_20260427T224546Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260427T230041Z`
- validation file: [`de_validate_20260427T230041Z.json`](de_validate_20260427T230041Z.json)
- dataset: `data/numbers/20_dset_20260427T224546Z/control.json`
- method: `de`
- optimized params: `(B1, B2)=(28430, 426878)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `219291.84718570416`
- baseline_mean_score: `532521.460566725`
- relative_improvement_pct: `58.82009206683853`
- optimized_mean_time_sec: `1.847185704198273`
- baseline_mean_time_sec: `1.4605667250207626`
- time_improvement_pct: `-26.4704770110393`
- optimized_mean_curves: `69.28999999999999`
- baseline_mean_curves: `102.52000000000001`
- curves_improvement_pct: `32.41318767069841`
- optimized_mean_success_rate: `0.85`
- baseline_mean_success_rate: `0.5700000000000001`
- success_rate_delta_pp: `27.999999999999993`
- trace plots:
  - curves_distribution_plot: [`de_validate_20260427T230041Z_curves_distribution.png`](plots/de_validate_20260427T230041Z_curves_distribution.png)
![curves_distribution_plot](plots/de_validate_20260427T230041Z_curves_distribution.png)
  - curves_trace_plot: [`de_validate_20260427T230041Z_curves_trace.png`](plots/de_validate_20260427T230041Z_curves_trace.png)
![curves_trace_plot](plots/de_validate_20260427T230041Z_curves_trace.png)
  - score_distribution_plot: [`de_validate_20260427T230041Z_score_distribution.png`](plots/de_validate_20260427T230041Z_score_distribution.png)
![score_distribution_plot](plots/de_validate_20260427T230041Z_score_distribution.png)
  - score_trace_plot: [`de_validate_20260427T230041Z_score_trace.png`](plots/de_validate_20260427T230041Z_score_trace.png)
![score_trace_plot](plots/de_validate_20260427T230041Z_score_trace.png)
  - time_distribution_plot: [`de_validate_20260427T230041Z_time_distribution.png`](plots/de_validate_20260427T230041Z_time_distribution.png)
![time_distribution_plot](plots/de_validate_20260427T230041Z_time_distribution.png)
  - time_trace_plot: [`de_validate_20260427T230041Z_time_trace.png`](plots/de_validate_20260427T230041Z_time_trace.png)
![time_trace_plot](plots/de_validate_20260427T230041Z_time_trace.png)

---
