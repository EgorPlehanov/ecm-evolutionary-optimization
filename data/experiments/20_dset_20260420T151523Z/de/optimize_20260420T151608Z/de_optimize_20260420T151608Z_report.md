# Отчёт по оптимизации: de_optimize_20260420T151608Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260420T151523Z/train.json`
- оптимум `(B1, B2)`: `(106, 144)`
- objective: `0.4872670474996994`
- curves_per_n: `12`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `218`
- `best_eval_fraction`: `0.990909090909091`
- `eval_per_sec`: `5.157896022594529`
- `evaluation_count`: `220`
- `improvement_percent`: `82.5631345535168`
- `max_plateau_evals`: `120`
- `median_plateau_evals`: `7.5`
- `new_best_count`: `9`
- `new_best_rate`: `0.04090909090909091`
- `p90_plateau_evals`: `49.79999999999997`
- `time_to_best_sec`: `42.27790835299993`
- `time_to_first_improvement_sec`: `0.695814147999954`
- `total_runtime_sec`: `42.653484773999935`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.04090909090909091` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.0` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `106.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `144.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `1.3584905660377358` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.991194707232246` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `82.5631345535168` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.04090909090909091` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.5454545454545454` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.5136363636363637` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`de_optimize_20260420T151608Z_b1_b2_trajectory.png`](plots/de_optimize_20260420T151608Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260420T151608Z_b1_b2_trajectory.png)
- [`de_optimize_20260420T151608Z_b1_ratio_heatmap.png`](plots/de_optimize_20260420T151608Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260420T151608Z_b1_ratio_heatmap.png)
- [`de_optimize_20260420T151608Z_jump_plot.png`](plots/de_optimize_20260420T151608Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260420T151608Z_jump_plot.png)
- [`de_optimize_20260420T151608Z_progress_by_phase.png`](plots/de_optimize_20260420T151608Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260420T151608Z_progress_by_phase.png)
- [`de_optimize_20260420T151608Z_time_efficiency.png`](plots/de_optimize_20260420T151608Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260420T151608Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/de_optimize_20260420T151608Z_events.csv"}, {"file": "tables/de_optimize_20260420T151608Z_new_best.csv"}, {"file": "tables/de_optimize_20260420T151608Z_phase_summary.csv"}, {"file": "tables/de_optimize_20260420T151608Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260420T151611Z`
- validation file: [`de_validate_20260420T151611Z.json`](de_validate_20260420T151611Z.json)
- dataset: `data/numbers/20_dset_20260420T151523Z/control.json`
- method: `de`
- optimized params: `(B1, B2)=(106, 144)`
- baseline params: `(B1, B2)=(11000, 220000)`
- curves_per_n: `24`
- curve_timeout_sec: `None`
- workers: `12`
- seed: `42`
- optimized_mean: `1.0053403774993512`
- baseline_mean: `3.2000019380508773`
- relative_improvement_pct: `68.58313223048532`
- trace plot: [`de_validate_20260420T151611Z_trace.png`](plots/de_validate_20260420T151611Z_trace.png)
![validation-trace](plots/de_validate_20260420T151611Z_trace.png)

---
