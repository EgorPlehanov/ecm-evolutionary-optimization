# Отчёт по оптимизации: pso_optimize_20260420T151721Z

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260420T151523Z/train.json`
- оптимум `(B1, B2)`: `(100, 100)`
- objective: `0.48935747650148187`
- curves_per_n: `12`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `157`
- `best_eval_fraction`: `0.6709401709401709`
- `eval_per_sec`: `5.5560229273600354`
- `evaluation_count`: `234`
- `improvement_percent`: `16.676830569727986`
- `max_plateau_evals`: `77`
- `median_plateau_evals`: `15.0`
- `new_best_count`: `7`
- `new_best_rate`: `0.029914529914529916`
- `p90_plateau_evals`: `71.4`
- `time_to_best_sec`: `29.276462435999747`
- `time_to_first_improvement_sec`: `4.915300991999629`
- `total_runtime_sec`: `42.116523115999826`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8376068376068376` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.7863247863247863` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `100.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ⚠️ ВНИМАНИЕ | `100.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `1.0` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.6951300883827656` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `16.676830569727986` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.029914529914529916` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.32905982905982906` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.8547008547008547` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`pso_optimize_20260420T151721Z_b1_b2_trajectory.png`](plots/pso_optimize_20260420T151721Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260420T151721Z_b1_b2_trajectory.png)
- [`pso_optimize_20260420T151721Z_b1_ratio_heatmap.png`](plots/pso_optimize_20260420T151721Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260420T151721Z_b1_ratio_heatmap.png)
- [`pso_optimize_20260420T151721Z_jump_plot.png`](plots/pso_optimize_20260420T151721Z_jump_plot.png)
![jump_plot](plots/pso_optimize_20260420T151721Z_jump_plot.png)
- [`pso_optimize_20260420T151721Z_progress_by_phase.png`](plots/pso_optimize_20260420T151721Z_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260420T151721Z_progress_by_phase.png)
- [`pso_optimize_20260420T151721Z_time_efficiency.png`](plots/pso_optimize_20260420T151721Z_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260420T151721Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/pso_optimize_20260420T151721Z_events.csv"}, {"file": "tables/pso_optimize_20260420T151721Z_new_best.csv"}, {"file": "tables/pso_optimize_20260420T151721Z_phase_summary.csv"}, {"file": "tables/pso_optimize_20260420T151721Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260420T151724Z`
- validation file: [`pso_validate_20260420T151724Z.json`](pso_validate_20260420T151724Z.json)
- dataset: `data/numbers/20_dset_20260420T151523Z/control.json`
- method: `pso`
- optimized params: `(B1, B2)=(100, 100)`
- baseline params: `(B1, B2)=(11000, 220000)`
- curves_per_n: `24`
- curve_timeout_sec: `None`
- workers: `12`
- seed: `42`
- optimized_mean: `0.9985179424998023`
- baseline_mean: `3.957004737448892`
- relative_improvement_pct: `74.7658138225138`
- trace plot: [`pso_validate_20260420T151724Z_trace.png`](plots/pso_validate_20260420T151724Z_trace.png)
![validation-trace](plots/pso_validate_20260420T151724Z_trace.png)

---
