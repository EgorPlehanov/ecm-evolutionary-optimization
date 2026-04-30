# Отчёт анализа: `divisor_size=20`

## Навигация
- Путь: /[overview](../../report.md)/divisor_size=20
- Переход на нижний уровень:
  - [method=bo](groups/method=bo/report.md) (1 runs)
  - [method=de](groups/method=de/report.md) (1 runs)
  - [method=ga](groups/method=ga/report.md) (1 runs)
  - [method=pso](groups/method=pso/report.md) (1 runs)
  - [method=rs](groups/method=rs/report.md) (1 runs)

## Краткая сводка
- запусков в области: **5**
- медиана final objective: **235684.418936**
- IQR objective: **99249.760765**
- доля успеха (`objective <= 185518.020415`): **40.00%**
- медианное время выполнения: **855.771 сек**
- медианный прирост по validation: **59.638%**

## Executive summary
- лучший сегмент по objective: **pso**
- лучший сегмент по validation gain: **pso**
- statistically significant пар: **0**
- кандидаты на adoption: **нет**
- кандидаты под наблюдение: **bo, de, ga, pso, rs**
- кандидаты на понижение приоритета: **нет**

## Графики
- [final_objective_by_method.png](plots/final_objective_by_method.png)
![final_objective_by_method](plots/final_objective_by_method.png)
- [validation_gain_by_method.png](plots/validation_gain_by_method.png)
![validation_gain_by_method](plots/validation_gain_by_method.png)
- [pareto_runtime_gain_by_method.png](plots/pareto_runtime_gain_by_method.png)
![pareto_runtime_gain_by_method](plots/pareto_runtime_gain_by_method.png)
- [risk_vs_gain_by_method.png](plots/risk_vs_gain_by_method.png)
![risk_vs_gain_by_method](plots/risk_vs_gain_by_method.png)
- [time_to_best_by_method.png](plots/time_to_best_by_method.png)
![time_to_best_by_method](plots/time_to_best_by_method.png)
- [convergence_ribbons_top3_methods.png](plots/convergence_ribbons_top3_methods.png)
![convergence_ribbons_top3_methods](plots/convergence_ribbons_top3_methods.png)
- [final_objective_by_method_overall.png](plots/final_objective_by_method_overall.png)
![final_objective_by_method_overall](plots/final_objective_by_method_overall.png)
- [final_objective_by_method_dataset=20_dset_20260430T220555Z_job6992343.png](plots/final_objective_by_method_dataset=20_dset_20260430T220555Z_job6992343.png)
![final_objective_by_method_dataset=20_dset_20260430T220555Z_job6992343](plots/final_objective_by_method_dataset=20_dset_20260430T220555Z_job6992343.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/runs.csv"}, {"file": "tables/summary.csv"}, {"file": "tables/compare_by_method.csv"}, {"file": "tables/pairwise_significance_by_method.csv"}, {"file": "tables/pairwise_win_rate_by_method.csv"}, {"file": "tables/omnibus_tests_by_method.csv"}, {"file": "tables/method_comparison.csv"}, {"file": "tables/stability_table.csv"}, {"file": "tables/validation_gain_by_method.csv"}, {"file": "tables/adoption_candidates.csv"}]'></div>

<script src="../../../../../../ecm_optimizer/analysis/tables-loader.js"></script>
