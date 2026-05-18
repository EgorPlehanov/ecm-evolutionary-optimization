# Отбор источников после выполнения поисковых запросов

Файл фиксирует, какие найденные источники действительно стоит использовать в ВКР, а какие результаты поиска можно не включать в основной список литературы. Логика отбора: оставлять первоисточники, сильные обзоры, источники для методологии эксперимента и источники, напрямую связанные с параметрами ECM/GMP-ECM.

## 1. Обязательное ядро источников

Эти источники стоит включать в ВКР почти наверняка.

### 1.1. ECM, гладкие числа и параметры B1/B2

| Источник | Где найден | Зачем нужен |
|---|---|---|
| Lenstra Jr. H. W. Factoring integers with elliptic curves, 1987 | уже есть в `REPORTS/sources/markdown/0__main` | первоисточник ECM |
| Brent R. P. Some Integer Factorization Algorithms Using Elliptic Curves, 1986 | уже есть в `REPORTS/sources/markdown/1__Brent_elliptic_curve_method_factorization` | вторая стадия ECM |
| Montgomery P. L. Speeding the Pollard and Elliptic Curve Methods of Factorization, 1987 | уже есть в `REPORTS/sources/markdown/6__Lenstra_elliptic_curve_factorization_1987` | форма Монтгомери, ускорение ECM |
| Silverman R. D., Wagstaff Jr. S. S. A Practical Analysis of the Elliptic Curve Factoring Algorithm, 1993 | `Silverman_Wagstaff_Practical_Analysis_Elliptic_Curve_Factoring_Algorithm.json`, также уже есть в markdown | практический выбор параметров, связь B1/B2 и вероятности успеха |
| Zimmermann P., Dodson B. 20 Years of ECM, 2006 | `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json`, `Brent_Suyama_elliptic_curve_method_stage_2_B2.json`, также уже есть в markdown | практические параметры GMP-ECM, обзор улучшений |
| Zimmermann P. GMP-ECM implementation, 2000 | уже есть в `REPORTS/sources/markdown/11__GMP-ECM` | обоснование GMP-ECM как базовой реализации |
| Bernstein D. J. et al. ECM using Edwards curves, 2013 | `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json`, также уже есть в markdown | сравнение альтернативных реализаций ECM с GMP-ECM |
| Bouvier C., Imbert L. Faster cofactorization with ECM using mixed representations, 2020/2019 | `CADO-NFS_ECM_cofactorization.json`, `NFS_cofactorization_elliptic_curve_method_parameters.json` | роль ECM в CADO-NFS и кофакторизации |
| Canfield E. R., Erdős P., Pomerance C. On a problem of Oppenheim concerning factorisatio numerorum, 1983 | запрос `Canfield_Erdos_Pomerance_smooth_numbers.json` не вытащил точную запись в топ | теоретическая основа распределения гладких чисел; нужно добрать точную запись |

### 1.2. Эвристические методы оптимизации

| Метод | Источник | Где найден | Статус |
|---|---|---|---|
| Differential Evolution (DE) | Storn R., Price K. Differential Evolution - a simple and efficient heuristic for global optimization over continuous spaces, 1997 | `Differential_Evolution_Storn_Price_Journal_of_Global_Optimization.json` | брать обязательно |
| DE | Price K., Storn R., Lampinen J. Differential Evolution: A Practical Approach to Global Optimization, 2005 | `Differential_Evolution_Price_Storn_Lampinen.json` | брать как книгу/практическое описание |
| DE | Das S., Suganthan P. N. Differential Evolution: A Survey of the State-of-the-Art, 2010/2011 | `Differential_Evolution_global_optimization_survey.json` | брать как обзор, если нужна глубина по DE |
| Genetic Algorithm (GA) | Holland J. H. Adaptation in Natural and Artificial Systems, 1975 | `Adaptation_in_Natural_and_Artificial_Systems_Holland_genetic_algorithm.json` | брать обязательно |
| GA | Goldberg D. E. Genetic Algorithms in Search, Optimization, and Machine Learning, 1989 | `Genetic_Algorithms_in_Search_Optimization_and_Machine_Learning_Goldberg.json` | брать обязательно |
| Particle Swarm Optimization (PSO) | Kennedy J., Eberhart R. Particle Swarm Optimization, 1995 | `Particle_Swarm_Optimization_Kennedy_Eberhart_1995.json` | брать обязательно |
| PSO | Clerc M. Particle Swarm Optimization, 2010 | `Particle_Swarm_Optimization_Clerc_Kennedy_constriction.json` | брать как книгу; точную статью Clerc-Kennedy про constriction лучше добрать отдельно |
| Bayesian Optimization (BO) | Jones D. R., Schonlau M., Welch W. J. Efficient Global Optimization of Expensive Black-Box Functions, 1998 | `Efficient_Global_Optimization_Jones_Schonlau_Welch_1998.json` | брать обязательно |
| BO | Snoek J., Larochelle H., Adams R. P. Practical Bayesian Optimization of Machine Learning Algorithms, 2012 | `Practical_Bayesian_Optimization_of_Machine_Learning_Algorithms_Snoek_Larochelle_Adams.json` | брать обязательно |
| BO | Wang X. et al. Recent Advances in Bayesian Optimization, 2023 | `Bayesian_optimization_expensive_black-box_survey.json` | брать как современный обзор, если нужен обзор BO |
| Random search | Bergstra J., Bengio Y. Random Search for Hyper-Parameter Optimization, 2012 | `Random_Search_for_Hyper-Parameter_Optimization_Bergstra_Bengio.json` | брать обязательно как baseline |

### 1.3. Automatic algorithm configuration и black-box optimization

| Источник | Где найден | Зачем нужен |
|---|---|---|
| Hutter F., Hoos H. H., Leyton-Brown K., Stützle T. ParamILS: An Automatic Algorithm Configuration Framework, 2009 | `ParamILS_automatic_algorithm_configuration_Hutter_Hoos_Stutzle.json` | обосновать постановку автоматической настройки алгоритма |
| Hutter F., Hoos H. H., Leyton-Brown K. Sequential Model-Based Optimization for General Algorithm Configuration, 2011 | `Sequential_Model-Based_Algorithm_Configuration_SMAC_Hutter_Hoos_Leyton-Brown.json` | SMAC и model-based algorithm configuration |
| Hutter F., Hoos H. H., Leyton-Brown K. An Evaluation of Sequential Model-Based Optimization for Expensive Blackbox Functions, 2013 | `Sequential_Model-Based_Algorithm_Configuration_SMAC_Hutter_Hoos_Leyton-Brown.json` | дорогие black-box функции |
| López-Ibáñez M. et al. The irace package: Iterated Racing for Automatic Algorithm Configuration, 2016 | `irace_iterated_racing_automatic_algorithm_configuration.json` | racing-подход и автоматическая конфигурация |
| Conn A. R., Scheinberg K., Vicente L. N. Introduction to Derivative-Free Optimization, 2009 | `derivative-free_optimization_noisy_functions_Conn_Scheinberg_Vicente.json` | общая рамка derivative-free optimization; запись есть не в топе выдачи |

### 1.4. Статистическое сравнение стохастических алгоритмов

Эти источники нужны для главы с экспериментами и статистической валидацией, но текущие JSON по большинству запросов фактически пустые. Их лучше добрать точными запросами.

| Источник | Зачем нужен | Статус текущего поиска |
|---|---|---|
| Mann H. B., Whitney D. R. On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other, 1947 | непараметрическое сравнение двух выборок | JSON пустой |
| Efron B., Tibshirani R. An Introduction to the Bootstrap, 1993 | доверительные интервалы bootstrap | JSON пустой |
| Vargha A., Delaney H. D. A Critique and Improvement of the CL Common Language Effect Size Statistics, 2000 | мера эффекта A12 / stochastic superiority | JSON пустой |
| Cliff N. Dominance statistics: Ordinal analyses to answer ordinal questions, 1993 | Cliff's delta, альтернатива A12 | JSON пустой |
| Demšar J. Statistical Comparisons of Classifiers over Multiple Data Sets, 2006 | сравнение нескольких алгоритмов на наборах задач | JSON пустой |
| Holm S. A Simple Sequentially Rejective Multiple Test Procedure, 1979 | поправка на множественные сравнения | JSON пустой |

## 2. Источники второго приоритета

Эти источники можно использовать, если в тексте понадобится расширить обзор, но они не обязательны для основного доказательства.

| Источник/группа | Где найдено | Когда использовать |
|---|---|---|
| Li Z. Elliptic Curve Factoring Method via FFTs with Division Polynomials, 2006 | `elliptic_curve_method_parameter_selection_B1_B2.json` | если нужна деталь про альтернативные ECM-подходы |
| Miele A. On the Analysis of Public-Key Cryptologic Algorithms, 2015 | `elliptic_curve_method_parameter_selection_B1_B2.json` | если нужна связка GPU/cofactorization/NFS |
| Miele A. et al. Cofactorization on Graphics Processing Units, 2014 | `elliptic_curve_method_parameter_selection_B1_B2.json`, уже есть в markdown | если нужна практическая роль ECM в NFS |
| Brent R. P. Factorization of the Tenth and Eleventh Fermat Numbers, 1996/1999 | `Fermat_numbers_elliptic_curve_method_factorization_Brent.json` | как пример результативности ECM на специальных числах |
| Gaj K. et al. Area-time efficient implementation of ECM in reconfigurable hardware, 2009/2010 | `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json` | если в обзоре нужны FPGA-реализации |
| Robinson O. New implementation of ECM using Edwards and Hessian curves, 2015 | `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json`, `Brent_Suyama_elliptic_curve_method_stage_2_B2.json` | если нужна альтернатива GMP-ECM |
| Cosset R. Factorization with genus 2 curves, 2010 | `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json`, `Brent_Suyama_elliptic_curve_method_stage_2_B2.json` | если нужна гиперэллиптическая ветка |

## 3. Что не брать в основной список литературы

### 3.1. Слишком шумные или нерелевантные выдачи

| Файл | Решение | Причина |
|---|---|---|
| `genetic_algorithm_parameter_optimization_black-box.json` | не брать в основной список | выдача в основном про частные ML/engineering-приложения, а не про базовые GA для ВКР |
| `Particle_Swarm_Optimization_black-box_optimization_survey.json` | не брать, кроме возможного общего обзора population-based metaheuristics | выдача слишком общая и не дает первоисточник PSO |
| `Bayesian_optimization_noisy_objective_black-box_optimization.json` | не брать в основной список | выдача современная, разрозненная, много прикладных работ; для ВКР достаточно Jones/Snoek/обзора Wang |
| `stochastic_simulation_optimization_ranking_and_selection_black-box.json` | не брать в основной список | тема simulation optimization шире, чем требуется; можно вернуться, если будет раздел про ranking and selection |
| `Msieve_ECM_factorization.json` | не брать в основной список | в основном шум и косвенные упоминания; для систем факторизации лучше использовать CADO-NFS/cofactorization |
| `YAFU_ECM_factorization_GMP-ECM.json` | не брать в основной список | выдача не дает сильного научного источника про YAFU/ECM |
| `ECM_RSA-like_semiprime_factorization.json` | не брать | найденная запись нерелевантна теме |
| `GMP-ECM_user_guide_B1_B2_curves.json` | не брать как научный источник | выдача не нашла руководство GMP-ECM; лучше использовать локальную/официальную документацию GMP-ECM отдельно |
| `Zimmermann_GMP-ECM_parameters_expected_curves.json` | не брать как источник по GMP-ECM | выдача вернула Cosset, а не ожидаемые таблицы GMP-ECM |

### 3.2. Дубли

| Дубль | Что оставить |
|---|---|
| `ECM_B1_B2_expected_number_of_curves_GMP-ECM.json` и `Brent_Suyama_elliptic_curve_method_stage_2_B2.json` оба находят Zimmermann & Dodson | оставить одну запись Zimmermann & Dodson 2006 |
| `CADO-NFS_ECM_cofactorization.json` и `NFS_cofactorization_elliptic_curve_method_parameters.json` оба находят Bouvier & Imbert | оставить Bouvier & Imbert |
| `Silverman_Wagstaff_Practical_Analysis_Elliptic_Curve_Factoring_Algorithm.json` содержит много посторонних записей | оставить только Silverman & Wagstaff 1993 |
| `Fermat_numbers_elliptic_curve_method_factorization_Brent.json` содержит Robinson и другие уже найденные источники | оставить Brent по Fermat numbers только как пример, если нужен |

## 4. Минимальный список для текста ВКР

Если нужно не раздувать список литературы, достаточно примерно 28-35 источников:

1. Lenstra 1987 - ECM.
2. Brent 1986 - stage 2 ECM.
3. Montgomery 1987 - ускорение ECM.
4. Silverman, Wagstaff 1993 - практический анализ ECM и B1/B2.
5. Zimmermann, Dodson 2006 - 20 years of ECM и GMP-ECM.
6. Zimmermann 2000 - GMP-ECM implementation.
7. Canfield, Erdős, Pomerance 1983 - гладкие числа.
8. Bouvier, Imbert 2020/2019 - ECM в CADO-NFS/cofactorization.
9. Bernstein et al. 2013 - Edwards curves как альтернативная реализация ECM.
10. Storn, Price 1997 - Differential Evolution.
11. Price, Storn, Lampinen 2005 - практическое описание Differential Evolution.
12. Holland 1975 - Genetic Algorithms.
13. Goldberg 1989 - Genetic Algorithms.
14. Kennedy, Eberhart 1995 - Particle Swarm Optimization.
15. Clerc 2010 или Clerc, Kennedy 2002 - PSO/constriction.
16. Jones, Schonlau, Welch 1998 - Efficient Global Optimization.
17. Snoek, Larochelle, Adams 2012 - Bayesian optimization.
18. Wang et al. 2023 - современный обзор Bayesian optimization.
19. Bergstra, Bengio 2012 - Random Search baseline.
20. Hutter et al. 2009 - ParamILS.
21. Hutter et al. 2011 - SMAC.
22. Hutter et al. 2013 - expensive black-box functions.
23. López-Ibáñez et al. 2016 - irace.
24. Conn, Scheinberg, Vicente 2009 - derivative-free optimization.
25. Mann, Whitney 1947 - непараметрический тест.
26. Efron, Tibshirani 1993 - bootstrap.
27. Vargha, Delaney 2000 - effect size A12.
28. Holm 1979 - multiple testing correction.
29. Demšar 2006 - сравнение нескольких алгоритмов.

Дополнительно можно оставить Brent по числам Ферма, Miele et al. по GPU/cofactorization и Gaj/Pelzl/Zimmermann по FPGA только если в главе 1 нужен широкий обзор реализаций ECM.

## 5. Что нужно добрать точными запросами

Ниже запросы только для тех мест, где текущий поиск дал пустой или неправильный JSON, но источник нужен методологически.

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"The particle swarm`" `"explosion stability convergence`" `"Kennedy`" `"Clerc`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"Introduction to Derivative-Free Optimization`" `"Conn`" `"Scheinberg`" `"Vicente`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"On a test of whether one of two random variables is stochastically larger than the other`" `"Mann`" `"Whitney`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"An Introduction to the Bootstrap`" `"Efron`" `"Tibshirani`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"A critique and improvement of the CL common language effect size statistics`" `"Vargha`" `"Delaney`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"A simple sequentially rejective multiple test procedure`" `"Holm`" `"1979`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"Statistical comparisons of classifiers over multiple data sets`" `"Demsar`" `"2006`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

```powershell
python REPORTS/sources/google_scholar_cli.py `
  --query "`"On a problem of Oppenheim concerning factorisatio numerorum`" `"Canfield`" `"Erdos`" `"Pomerance`"" `
  --limit 10 `
  --output REPORTS/sources/originals
```

Для GMP-ECM user guide лучше не искать через Google Scholar. Это скорее документация проекта, ее стоит брать из официального сайта/README/локальной установленной документации, а в списке литературы оформлять как электронный ресурс.
