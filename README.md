# ECM Evolutionary Optimization

Репозиторий для НИР по проверке гипотезы: можно ли автоматически подобрать параметры GMP-ECM (`B1`, `B2`) с помощью дифференциальной эволюции так, чтобы уменьшить ожидаемое время факторизации по сравнению со стандартными табличными значениями.

## Что уже реализовано

- Каркас Python-пайплайна для:
  - запуска `gmp-ecm` и парсинга результата;
  - оценки baseline-независимого composite-фитнеса:
    успех факторизации и время факторизации имеют равный приоритет, число кривых — вторичный критерий;
  - оптимизации `log10(B1), log10(B2)` через `scipy.optimize.differential_evolution`;
  - автоматической валидации найденных параметров против baseline;
  - генерации train/control наборов семипростых чисел (`N = p*q`) с настраиваемыми размерами множителей;
  - сохранения JSON-метаданных по каждому запуску optimize/validate.
- Документированный план НИР в `docs/research_plan_ru.md`.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 1) Генерация train/control датасетов

```bash
ecm-optimizer generate \
  --target-digits 35 \
  --cofactor-digits 90 \
  --train-count 20 \
  --control-count 20
```

Команда создаёт:
- `data/numbers/<TARGET_DIGITS>_dset_<UTC_TIMESTAMP>/train.json` — числа для оптимизации;
- `data/numbers/<TARGET_DIGITS>_dset_<UTC_TIMESTAMP>/control.json` — отдельный контрольный набор;
- `data/numbers/<TARGET_DIGITS>_dset_<UTC_TIMESTAMP>/manifest.json` — `n,p,q` для воспроизводимости;
- `data/numbers/<TARGET_DIGITS>_dset_<UTC_TIMESTAMP>/generation.json` — метаданные и параметры генерации.

### 2) Оптимизация параметров ECM

```bash
ecm-optimizer optimize \
  --max-curves-per-n 80 \
  --repeats-per-n 3 \
  --de-popsize 16 \
  --de-maxiter 25 \
  --b1-min 1e3 \
  --b1-max 1e9 \
  --b2-min 1e3 \
  --b2-max 1e11 \
  --ratio-max 100 \
```

После завершения в консоль печатаются `result_file=...` и пути до PNG-графиков. JSON-файл сохраняется в `data/experiments/<DATASET_FOLDER>/<METHOD>_optimize_<UTC_TIMESTAMP>.json`, где `<METHOD>` — всегда короткий код (`de`, `rs`, `pso`, `bo`, `ga`).

В конце каждого run автоматически строятся:
- `jump_plot` — только события `new_best` + приросты `delta fitness`;
- `b1_b2_trajectory` — динамика `B1/B2` по evaluation;
- `progress_by_phase` — best-so-far + raw fitness + маркеры `step`-этапов;
- `time_efficiency` — качество во времени и rolling `eval/sec`;
- `b1_ratio_heatmap` — `B1 vs B2` (colored by fitness) и heatmap `B1 vs B2/B1`.

Ключевые метрики (`time_to_first_improvement_sec`, `time_to_best_sec`, `new_best_count`, `eval_per_sec`, `improvement_percent`, `max_plateau_evals`) сохраняются внутри optimize-JSON в поле `run_stats`.

Для генерации PNG-графиков используется `matplotlib` (входит в зависимости проекта).

Поддерживаемые значения `--method`:
- `de` / `differential-evolution` — дифференциальная эволюция;
- `rs` / `random-search` — случайный поиск;
- `pso` / `particle-swarm-optimization` — роевой поиск в лог-пространстве;
- `bo` / `bayesian-optimization` — surrogate-based поиск с LCB-критерием;
- `ga` / `genetic-algorithm` — генетический алгоритм с элитизмом и мутациями.

Параметры алгоритмов разделены по префиксам:
- `--de-popsize`, `--de-maxiter` для DE;
- `--rs-budget` для Random Search;
- `--pso-swarm-size`, `--pso-iterations` для PSO;
- `--bo-initial-samples`, `--bo-iterations`, `--bo-candidate-pool` для BO;
- `--ga-population-size`, `--ga-generations`, `--ga-mutation-prob` для GA.

Важно:
- `--method` нужно передавать явно (значения по умолчанию нет);
- при `--method de` нужно передавать `--de-popsize` и `--de-maxiter`;
- при выборе `--method rs|pso|bo|ga` соответствующие method-specific параметры тоже нужно передавать явно.

`--dataset` можно передать как полный путь к JSON-файлу/папке или как имя папки внутри `data/numbers` (например `35_dset_<UTC_TIMESTAMP>`).

Поддерживаемый формат датасетов: JSON `ecm_dataset_v1`.

### Логика fitness (актуальная)

Для каждой пары `(B1, B2)` считается средняя метрика по train-набору:
- `success_rate` — доля успешных repeated-run запусков;
- `mean_time_to_outcome_sec` — среднее время до успеха или лимита;
- `mean_curves_to_outcome` — среднее число кривых до исхода.

Итоговый `score` (минимизируется) считается без привязки к baseline:
- `success_penalty = 1 - success_rate`;
- `time_term = log(1 + mean_time_to_outcome_sec)`;
- `curves_term = log(1 + mean_curves_to_outcome)`.

Композиция score:
- `SUCCESS_WEIGHT * success_penalty`;
- `TIME_WEIGHT * time_term`;
- `CURVE_WEIGHT * curves_term`.

В текущей конфигурации `SUCCESS_WEIGHT == TIME_WEIGHT`, поэтому успех и время равноприоритетны,
а `CURVE_WEIGHT` меньше и выступает как вторичный стабилизатор.

### 3) Валидация

```bash
ecm-optimizer validate
```

`--opt-result-file` можно передать как полный путь к JSON-файлу или только имя файла (поиск в `data/experiments/<DATASET_FOLDER>/`). Если не передавать, будет взят последний `*_optimize_*.json` (для выбранного датасета, либо глобально если `--dataset` не задан).

Если `--dataset` не указан, он берётся из поля `dataset` в выбранном optimize-результате. Если не заданы `--max-curves-per-n` и `--curve-timeout-sec`, они также подтягиваются из `config` optimize-результата.


### 4) Автоматизированный прогон по плану

```bash
ecm-optimizer run-plan --plan example_full_run
```

Также поддерживается короткий вызов без флага:

```bash
ecm-optimizer run-plan example_full_run
```

Планы хранятся в `data/plans/` (можно передавать и полный путь к JSON).

Формат плана:
- `params` — (опционально) общий словарь параметров в начале плана;
- `operations` — список шагов (неограниченное количество);
- `type` — один из `generate`, `optimize`, `validate`, `analyze`;
- `label` — опциональная метка результата шага;
- `args` — аргументы CLI-команды в формате `--kebab-case`;
- повторяемые блоки: вместо `type` можно задать `repeat` + вложенный `operations`:
  - `repeat: 3` — выполнить вложенные операции 3 раза (`iter.index = 0..2`);
  - `repeat: {"count": 3, "as": "run"}` — то же, но переменная цикла будет `run`;
  - `repeat: {"values": {"seed": [11, 22, 33]}}` — количество итераций берётся по длине списка;
  - `repeat: {"count": 3, "values": {"seed": [...]}}` — `count` должен совпадать с длинами всех списков;
  - `repeat.iterate` управляет комбинированием нескольких списков в `values` (по умолчанию `zip`):
    - `zip` — объединение по индексу (длины списков должны совпадать);
    - `product` — декартово произведение списков;
    - `concat` — склейка в один поток (на итерации присутствует одно поле из `values`).
  - внутри блока доступны `{{iter.index}}` и поля из `values` (например `$ref:iter.seed` или `{{iter.seed}}`).
  - repeat-блок можно пометить `label`, чтобы после выполнения получить метаданные итераций:
    - `<label>.values.<field>` — список значений поля (например `seed_runs.values.seed`);
    - `<label>.iterations` — список объектов итераций (`index` + все поля).
- для построения списка ссылок по значениям итерации используйте `$map_ref`:
  `{"$map_ref": {"items": {"$ref": "seed_runs.values.seed"}, "template": "dataset_main_{{item}}.dataset_dir"}}`.
- `$map_ref` также может принимать объект именованных списков:
  - по умолчанию используется `iterate: "zip"` (элементы объединяются по индексу, длины списков должны совпадать):
    `{"$map_ref": {"items": {"size": {"$ref": "params.target_digits_list"}, "seed": {"$ref": "params.seed_list"}}, "template": "dataset_{{item.size}}_{{item.seed}}.dataset_dir"}}`
  - `iterate: "product"` строит декартово произведение списков;
  - `iterate: "concat"` склеивает элементы списков в один поток (каждый элемент будет вида `{"<name>": value}`).
- для разворачивания словаря параметров в `args` используйте `$spread_ref`:
  - базово: `{"$spread_ref": {"ref": "params.search"}}` (ключи с `_` автоматически станут `-`);
  - короткая форма без дополнительных опций: `{"$spread_ref": "params.search"}`;
  - выборочно: `{"$spread_ref": {"ref": "params.search", "include": ["b1_min", "b1_max"]}}`;
  - исключения: `{"$spread_ref": {"ref": "params.search", "exclude": ["ratio_max"]}}`;
  - переименование: `{"$spread_ref": {"ref": "params.search", "rename": {"b1_min": "b1-min"}}}`;
  - можно передать список спредов: `"$spread_ref": ["params.shared_opt_args", "params.method_opt.{{iter.method}}", "params.search"]`
    или объектами `"$spread_ref": [{...}, {...}]`.
- ссылки между шагами/параметрами: `{"$ref": "<label>.<field>"}` или строка `$ref:<label>.<field>`.
  Для общих параметров используйте label `params`, например: `{"$ref": "params.shared.max_curves_per_n"}`.
- shortcut для `analyze`: можно передать `dataset` (строку или список), и `run-plan` автоматически
  преобразует его в `input=data/experiments/<dataset_name>`. Это удобно вместо длинного списка `opt_*.result_file`.

Пример выбора вложенного набора параметров по значению цикла:

```json
{
  "params": {
    "search": {
      "d20": {"b1_min": 1000, "b1_max": 12000, "b2_min": 1000, "b2_max": 144000, "ratio_max": 12},
      "d30": {"b1_min": 2000, "b1_max": 22000, "b2_min": 2000, "b2_max": 244000, "ratio_max": 22}
    }
  },
  "operations": [
    {
      "repeat": {"values": {"digit_key": ["d20", "d30"]}},
      "operations": [
        {
          "type": "optimize",
          "args": {
            "method": "de",
            "$spread_ref": {
              "ref": "params.search.{{iter.digit_key}}",
              "include": ["b1_min", "b1_max", "ratio_max"]
            }
          }
        }
      ]
    }
  ]
}
```

Пример (фрагмент):

```json
{
  "params": {
    "shared": {
      "max_curves_per_n": 12,
      "curve_timeout_sec": 5
    }
  },
  "operations": [
    {"type": "generate", "label": "gen1", "args": {"target-digits": 20}},
    {
      "type": "optimize",
      "args": {
        "dataset": {"$ref": "gen1.dataset_dir"},
        "method": "rs",
        "rs-budget": 20,
        "max-curves-per-n": {"$ref": "params.shared.max_curves_per_n"},
        "curve-timeout-sec": {"$ref": "params.shared.curve_timeout_sec"}
      }
    }
    ,
    {
      "repeat": {
        "values": {
          "seed": [101, 202, 303]
        }
      },
      "operations": [
        {
          "type": "generate",
          "label": "gen_seed_{{iter.seed}}",
          "args": {
            "target-digits": 20,
            "seed": {"$ref": "iter.seed"}
          }
        }
      ]
    }
  ]
}
```

План **одного полного прогона по всем методам для `target-digits=20` под новую composite-логику**
(`max-curves-per-n` + `repeats-per-n` на optimize/validate):

```bash
ecm-optimizer run-plan --plan full_all_methods_single_run_20d
```

Файл плана: `data/plans/full_all_methods_single_run_20d.json`.

### Референс по B1/B2 и ожидаемому числу кривых (ECM)

Для выбора `max-curves-per-n` в планах ориентируемся на таблицу из исходного проекта ECM:
https://gitlab.inria.fr/zimmerma/ecm/

Ниже оставлены только нужные нам поля: `digits`, оптимальный `B1`, `B2` (default), и ожидаемое число кривых `N(B1,B2,D)` (default poly).

| digits D | optimal B1 | default B2 | expected curves N(B1,B2,D) |
|---:|---:|---:|---:|
| 20 | 11e3 | 1.9e6 | 74 |
| 25 | 5e4 | 1.3e7 | 214 |
| 30 | 25e4 | 1.3e8 | 430 |
| 35 | 1e6 | 1.0e9 | 904 |
| 40 | 3e6 | 5.7e9 | 2350 |
| 45 | 11e6 | 3.5e10 | 4480 |
| 50 | 43e6 | 2.4e11 | 7553 |
| 55 | 11e7 | 7.8e11 | 17769 |
| 60 | 26e7 | 3.2e12 | 42017 |
| 65 | 85e7 | 1.6e13 | 69408 |

Во всех актуальных планах:
- для `target-digits=20` используется запасной бюджет `max-curves-per-n=100` (optimize) и `150` (validate);
- для мульти-размерных планов (`20/25/30`) бюджеты масштабируются по размеру: `100/300/600` (optimize) и `150/450/900` (validate).

План **мульти-seed тюнинга** (`target-digits=20`, seeds `17/2718/31415`, все методы + общий analyze):

```bash
ecm-optimizer run-plan --plan tuned_all_methods_multiseed_20d
```

Файл плана: `data/plans/tuned_all_methods_multiseed_20d.json`.

План **полного мульти-прогона по нескольким размерам делителей** (`target-digits=20,25,30`) с финальным общим анализом:

```bash
ecm-optimizer run-plan --plan full_all_methods_20_25_30
```

Файл плана: `data/plans/full_all_methods_20_25_30.json`.

Проверка плана без фактического запуска:

```bash
ecm-optimizer run-plan --plan tuned_all_methods_multiseed_20d --dry-run
```

Файл плана: `data/plans/tuned_all_methods_multiseed_20d.json`.

В опорном плане используется единый `seed` на шаге `generate`; для `optimize`/`validate` seed не задаётся отдельно, поэтому команды автоматически берут seed датасета.
Параметр `workers` в плане не указан, значит используется поведение CLI по умолчанию (`-1`, все доступные CPU).
Параметры плана облегчены для быстрого старта: уменьшены размеры датасета, `max-curves-per-n` и бюджеты/итерации оптимизаторов.


### 5) Иерархический multi-run анализ (optimize + validate)

```bash
ecm-optimizer analyze \
  --input data/experiments/20_dset_20260330T134425Z
```

Команда строит иерархический анализ с авто-детектом группировок и использует данные валидации:
- root `overview/report.md` со сводными выводами;
- дерево `groups/` по автоматически выбранным уровням (`divisor_size`, `dataset`, `method`, `seed`) или по `--group-by`;
- на каждом уровне: `report.md`, `tables/runs.csv`, `tables/summary.csv`, сравнительная таблица `compare_by_<dimension>.csv`;
- сравнительные графики в `plots/` по активному уровню группировки;
- метрики реального эффекта из `*_validate_*.json` (relative improvement + absolute gain).
- отчеты формируются на русском языке; графики вставляются как ссылка + изображение, таблицы рендерятся встроенным JS-скриптом в стиле optimize-отчетов.

По умолчанию (без `--input`) анализатор автоматически берет **все** optimize-результаты из `data/experiments`.

Поведение `--input` упрощено:
- если передан конкретный run (`.../optimize_<TS>/` или `..._optimize_<TS>.json`), анализируется только этот запуск;
- если передана верхняя папка, рекурсивно ищутся все `*_optimize_*.json` внутри неё;
- если `--input` начинается с `!`, это правило исключения (по пути/маске/подстроке), например `--input "!*/rs/*"`;
- если переданы только исключения (`!`), базовый набор берется из `data/experiments`, а затем исключается по правилам.

По умолчанию результат сохраняется в `data/analysis/analyze_<UTC_TIMESTAMP>/` (или в `--output-dir`) и включает:
- `analysis_summary.json` — манифест анализа, параметры запуска, список найденных run-файлов и ссылки на узлы дерева;
- `overview/report.md` — верхнеуровневый отчёт по всем входным данным;
- вложенные папки `overview/groups/...` для детального анализа по областям.

Группировка:
- `--auto-grouping` включен по умолчанию;
- для ручного порядка уровней используйте `--no-auto-grouping --group-by ...`;
- поддерживаемые ключи: `divisor_size`, `dataset`, `method`, `seed`.

## Структура пакета

- `ecm_optimizer/cli/` — команды `generate`, `optimize`, `validate`.
- `ecm_optimizer/core/` — генерация задачи, запуск ECM, fitness, baseline и validation.
- `ecm_optimizer/optimizers/` — базовый интерфейс и реализации DE/RS/PSO/BO/GA.
- `ecm_optimizer/analysis/` — иерархический multi-run анализ и генерация markdown-отчетов/таблиц/графиков.
- `ecm_optimizer/utils/` — JSON I/O, logging и seed utilities.
- `ecm_optimizer/config.py` — централизованные константы и пути.
- `ecm_optimizer/models.py` — dataclass-модели конфигурации и результатов.
- `data/numbers/` — датасеты.
- `data/experiments/` — результаты optimize/validate.

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для генерации датасетов и оптимизатора используйте фиксированный `--seed`.
- Для независимых этапов применяются детерминированные производные seed'ы через `seed_utils`.
- Для финальной валидации увеличивайте `--max-curves-per-n`.
