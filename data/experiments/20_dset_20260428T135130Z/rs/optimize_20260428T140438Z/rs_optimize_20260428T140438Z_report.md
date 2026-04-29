# Отчёт по оптимизации: rs_optimize_20260428T140438Z

## Метаданные
- метод: `rs`
- датасет: `data/numbers/20_dset_20260428T135130Z/train.json`
- оптимум `(B1, B2)`: `(9043, 472323)`
- objective: `-0.19832577899229786`
- max_curves_per_n: `100`
- repeats_per_n: `3`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `35`
- `best_eval_fraction`: `0.5833333333333334`
- `eval_per_sec`: `0.345065387306613`
- `evaluation_count`: `60`
- `improvement_percent`: `102.35372583280918`
- `max_plateau_evals`: `25`
- `median_plateau_evals`: `3.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.11666666666666667`
- `p90_plateau_evals`: `18.7`
- `time_to_best_sec`: `98.84532648799359`
- `time_to_first_improvement_sec`: `5.768912048995844`
- `total_runtime_sec`: `173.88008825900033`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.016666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `9043.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `472323.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `52.23078624350326` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.5684683478004686` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `102.35372583280918` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.11666666666666667` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.4166666666666667` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.26666666666666666` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`rs_optimize_20260428T140438Z_b1_b2_trajectory.png`](plots/rs_optimize_20260428T140438Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/rs_optimize_20260428T140438Z_b1_b2_trajectory.png)
- [`rs_optimize_20260428T140438Z_b1_ratio_heatmap.png`](plots/rs_optimize_20260428T140438Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/rs_optimize_20260428T140438Z_b1_ratio_heatmap.png)
- [`rs_optimize_20260428T140438Z_jump_plot.png`](plots/rs_optimize_20260428T140438Z_jump_plot.png)
![jump_plot](plots/rs_optimize_20260428T140438Z_jump_plot.png)
- [`rs_optimize_20260428T140438Z_progress_by_phase.png`](plots/rs_optimize_20260428T140438Z_progress_by_phase.png)
![progress_by_phase](plots/rs_optimize_20260428T140438Z_progress_by_phase.png)
- [`rs_optimize_20260428T140438Z_time_efficiency.png`](plots/rs_optimize_20260428T140438Z_time_efficiency.png)
![time_efficiency](plots/rs_optimize_20260428T140438Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/rs_optimize_20260428T140438Z_events.csv"}, {"file": "tables/rs_optimize_20260428T140438Z_new_best.csv"}, {"file": "tables/rs_optimize_20260428T140438Z_phase_summary.csv"}, {"file": "tables/rs_optimize_20260428T140438Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260428T140735Z`
- validation file: [`rs_validate_20260428T140735Z.json`](rs_validate_20260428T140735Z.json)
- dataset: `data/numbers/20_dset_20260428T135130Z/control.json`
- method: `rs`
- optimized params: `(B1, B2)=(9043, 472323)`
- baseline params: `(B1, B2)=(11000, 220000)`
- max_curves_per_n: `150`
- repeats_per_n: `5`
- curve_timeout_sec: `None`
- workers: `56`
- seed: `42`
- optimized_mean_score: `4.463212242414839`
- baseline_mean_score: `8.731900410285792`
- relative_improvement_pct: `48.88612979189075`
- optimized_mean_time_sec: `1.5748147540279025`
- baseline_mean_time_sec: `1.604996620965976`
- time_improvement_pct: `1.8804941109413953`
- optimized_mean_curves: `94.89`
- baseline_mean_curves: `105.45`
- curves_improvement_pct: `10.014224751066859`
- optimized_mean_success_rate: `0.6100000000000001`
- baseline_mean_success_rate: `0.48`
- success_rate_delta_pp: `13.00000000000001`
- trace plots:
  - curves_distribution_plot: [`rs_validate_20260428T140735Z_curves_distribution.png`](plots/rs_validate_20260428T140735Z_curves_distribution.png)
![curves_distribution_plot](plots/rs_validate_20260428T140735Z_curves_distribution.png)
  - curves_trace_plot: [`rs_validate_20260428T140735Z_curves_trace.png`](plots/rs_validate_20260428T140735Z_curves_trace.png)
![curves_trace_plot](plots/rs_validate_20260428T140735Z_curves_trace.png)
  - score_distribution_plot: [`rs_validate_20260428T140735Z_score_distribution.png`](plots/rs_validate_20260428T140735Z_score_distribution.png)
![score_distribution_plot](plots/rs_validate_20260428T140735Z_score_distribution.png)
  - score_trace_plot: [`rs_validate_20260428T140735Z_score_trace.png`](plots/rs_validate_20260428T140735Z_score_trace.png)
![score_trace_plot](plots/rs_validate_20260428T140735Z_score_trace.png)
  - time_distribution_plot: [`rs_validate_20260428T140735Z_time_distribution.png`](plots/rs_validate_20260428T140735Z_time_distribution.png)
![time_distribution_plot](plots/rs_validate_20260428T140735Z_time_distribution.png)
  - time_trace_plot: [`rs_validate_20260428T140735Z_time_trace.png`](plots/rs_validate_20260428T140735Z_time_trace.png)
![time_trace_plot](plots/rs_validate_20260428T140735Z_time_trace.png)

---
