# Отчёт по оптимизации: bo_optimize_20260420T151738Z

## Метаданные
- метод: `bo`
- датасет: `data/numbers/20_dset_20260420T151523Z/train.json`
- оптимум `(B1, B2)`: `(191, 1005)`
- objective: `0.5206911849988956`
- curves_per_n: `12`
- границы: `B1[100.0, 30000.0]`, `B2[100.0, 600000.0]`, `ratio_max=100.0`

## Ключевые статистики
- `best_eval`: `36`
- `best_eval_fraction`: `0.9473684210526315`
- `eval_per_sec`: `3.692153108942363`
- `evaluation_count`: `38`
- `improvement_percent`: `25.374263523105267`
- `max_plateau_evals`: `26`
- `median_plateau_evals`: `2.0`
- `new_best_count`: `5`
- `new_best_rate`: `0.13157894736842105`
- `p90_plateau_evals`: `14.5`
- `time_to_best_sec`: `9.894262572000116`
- `time_to_first_improvement_sec`: `0.2101147360003779`
- `total_runtime_sec`: `10.292234414000177`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ✅ ОК | `0.07894736842105263` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.0` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ✅ ОК | `191.0` | `within 2% of log-range [100.0, 30000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `1005.0` | `within 2% of log-range [100.0, 600000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `5.261780104712042` | `within 2% of log-range up to ratio_max=100.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ⚠️ ВНИМАНИЕ | `0.9613328043268512` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `25.374263523105267` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.13157894736842105` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.6842105263157895` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.5263157894736842` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`bo_optimize_20260420T151738Z_b1_b2_trajectory.png`](plots/bo_optimize_20260420T151738Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/bo_optimize_20260420T151738Z_b1_b2_trajectory.png)
- [`bo_optimize_20260420T151738Z_b1_ratio_heatmap.png`](plots/bo_optimize_20260420T151738Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/bo_optimize_20260420T151738Z_b1_ratio_heatmap.png)
- [`bo_optimize_20260420T151738Z_jump_plot.png`](plots/bo_optimize_20260420T151738Z_jump_plot.png)
![jump_plot](plots/bo_optimize_20260420T151738Z_jump_plot.png)
- [`bo_optimize_20260420T151738Z_progress_by_phase.png`](plots/bo_optimize_20260420T151738Z_progress_by_phase.png)
![progress_by_phase](plots/bo_optimize_20260420T151738Z_progress_by_phase.png)
- [`bo_optimize_20260420T151738Z_time_efficiency.png`](plots/bo_optimize_20260420T151738Z_time_efficiency.png)
![time_efficiency](plots/bo_optimize_20260420T151738Z_time_efficiency.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/bo_optimize_20260420T151738Z_events.csv"}, {"file": "tables/bo_optimize_20260420T151738Z_new_best.csv"}, {"file": "tables/bo_optimize_20260420T151738Z_phase_summary.csv"}, {"file": "tables/bo_optimize_20260420T151738Z_run_summary.csv"}]'></div>

<script src="../../../../../ecm_optimizer/analysis/tables-loader.js"></script>

## Validation runs

### Validation run `20260420T151741Z`
- validation file: [`bo_validate_20260420T151741Z.json`](bo_validate_20260420T151741Z.json)
- dataset: `data/numbers/20_dset_20260420T151523Z/control.json`
- method: `bo`
- optimized params: `(B1, B2)=(191, 1005)`
- baseline params: `(B1, B2)=(11000, 220000)`
- curves_per_n: `24`
- curve_timeout_sec: `None`
- workers: `12`
- seed: `42`
- optimized_mean: `1.0505445300018437`
- baseline_mean: `3.1455646140002047`
- relative_improvement_pct: `66.60235414252485`
- trace plot: [`bo_validate_20260420T151741Z_trace.png`](plots/bo_validate_20260420T151741Z_trace.png)
![validation-trace](plots/bo_validate_20260420T151741Z_trace.png)

---
