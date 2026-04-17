# Отчёт анализа: `overview`

## Навигация
- Путь: /overview
- Переход на нижний уровень:
  - [divisor_size=20](groups/divisor_size=20/report.md) (45 runs)
  - [divisor_size=25](groups/divisor_size=25/report.md) (45 runs)
  - [divisor_size=30](groups/divisor_size=30/report.md) (45 runs)

## Краткая сводка
- запусков в области: **135**
- медиана final objective: **0.754058**
- IQR objective: **0.235766**
- доля успеха (`objective <= 0.678229`): **25.19%**
- медианное время выполнения: **57.824 сек**
- медианный прирост по validation: **60.624%**

## Executive summary
- лучший сегмент по objective: **20**
- лучший сегмент по validation gain: **30**
- statistically significant пар: **3**
- кандидаты на adoption: **20, 25, 30**
- кандидаты под наблюдение: **нет**
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
- [final_objective_by_method_divisor_size=25.png](plots/final_objective_by_method_divisor_size=25.png)
![final_objective_by_method_divisor_size=25](plots/final_objective_by_method_divisor_size=25.png)
- [final_objective_by_method_divisor_size=30.png](plots/final_objective_by_method_divisor_size=30.png)
![final_objective_by_method_divisor_size=30](plots/final_objective_by_method_divisor_size=30.png)

## Таблицы

<div id="tables-container" data-tables='[{"file": "tables/runs.csv"}, {"file": "tables/summary.csv"}, {"file": "tables/compare_by_divisor_size.csv"}, {"file": "tables/pairwise_significance_by_divisor_size.csv"}, {"file": "tables/pairwise_win_rate_by_divisor_size.csv"}, {"file": "tables/omnibus_tests_by_divisor_size.csv"}, {"file": "tables/method_ranking.csv"}, {"file": "tables/validation_gain_ranking.csv"}, {"file": "tables/coverage_matrix.csv"}, {"file": "tables/adoption_candidates.csv"}]'></div>

<script src="../../../../ecm_optimizer/analysis/tables-loader.js"></script>
