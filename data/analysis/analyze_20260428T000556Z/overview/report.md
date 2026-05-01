# Отчёт анализа: `overview`

## Навигация
- Путь: /overview
- Переход на нижний уровень:
  - [divisor_size=20](groups/divisor_size=20/report.md) (5 runs)

## Краткая сводка
- запусков в области: **5**
- медиана final objective: **216484.671131**
- IQR objective: **35983.424600**
- доля успеха (`objective <= 214301.230104`): **40.00%**
- медианное время выполнения: **882.515 сек**
- медианный прирост по validation: **61.709%**

## Executive summary
- лучший сегмент по objective: **20**
- лучший сегмент по validation gain: **20**
- statistically significant пар: **0**
- кандидаты на adoption: **нет**
- кандидаты под наблюдение: **20**
- кандидаты на понижение приоритета: **нет**

## Графики
- [final_objective_by_divisor_size.png](plots/final_objective_by_divisor_size.png)
![final_objective_by_divisor_size](plots/final_objective_by_divisor_size.png)
- [validation_gain_by_divisor_size.png](plots/validation_gain_by_divisor_size.png)
![validation_gain_by_divisor_size](plots/validation_gain_by_divisor_size.png)
- [pareto_runtime_gain_by_divisor_size.png](plots/pareto_runtime_gain_by_divisor_size.png)
![pareto_runtime_gain_by_divisor_size](plots/pareto_runtime_gain_by_divisor_size.png)
- [risk_vs_gain_by_divisor_size.png](plots/risk_vs_gain_by_divisor_size.png)
![risk_vs_gain_by_divisor_size](plots/risk_vs_gain_by_divisor_size.png)
- [time_to_best_by_divisor_size.png](plots/time_to_best_by_divisor_size.png)
![time_to_best_by_divisor_size](plots/time_to_best_by_divisor_size.png)
- [final_objective_by_method_overall.png](plots/final_objective_by_method_overall.png)
![final_objective_by_method_overall](plots/final_objective_by_method_overall.png)
- [final_objective_by_method_divisor_size=20.png](plots/final_objective_by_method_divisor_size=20.png)
![final_objective_by_method_divisor_size=20](plots/final_objective_by_method_divisor_size=20.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/runs.csv"}, {"file": "tables/summary.csv"}, {"file": "tables/compare_by_divisor_size.csv"}, {"file": "tables/method_ranking.csv"}, {"file": "tables/validation_gain_ranking.csv"}, {"file": "tables/coverage_matrix.csv"}, {"file": "tables/adoption_candidates.csv"}]'></div>

<script src="../../../../ecm_optimizer/analysis/tables-loader.js"></script>
