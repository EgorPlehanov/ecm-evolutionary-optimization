# ECM Evolutionary Optimization

Репозиторий для НИР по проверке гипотезы: можно ли автоматически подобрать параметры GMP-ECM (`B1`, `B2`) с помощью дифференциальной эволюции так, чтобы уменьшить ожидаемое время факторизации по сравнению со стандартными табличными значениями.

## Что уже реализовано

- Каркас Python-пайплайна для:
  - запуска `gmp-ecm` и парсинга результата;
  - оценки фитнеса как эмпирического `E[T_success]`;
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
  --curves-per-n 50 \
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
- `convergence` — best fitness so far по eval;
- `raw_fitness` — fitness по всем evaluation;
- `jump_plot` — только события `new_best`;
- `b1_b2_trajectory` — динамика `B1/B2` и scatter `B1 vs B2`;
- `progress_by_phase` — convergence + маркеры `step`-этапов.

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

### 3) Валидация

```bash
ecm-optimizer validate
```

`--opt-result-file` можно передать как полный путь к JSON-файлу или только имя файла (поиск в `data/experiments/<DATASET_FOLDER>/`). Если не передавать, будет взят последний `*_optimize_*.json` (для выбранного датасета, либо глобально если `--dataset` не задан).

Если `--dataset` не указан, он берётся из поля `dataset` в выбранном optimize-результате. Если не заданы `--curves-per-n` и `--curve-timeout-sec`, они также подтягиваются из `config` optimize-результата.


### 4) Автоматизированный прогон по плану

```bash
ecm-optimizer run-plan --plan example_full_run
```

Планы хранятся в `data/plans/` (можно передавать и полный путь к JSON).

Формат плана:
- `params` — (опционально) общий словарь параметров в начале плана;
- `operations` — список шагов (неограниченное количество);
- `type` — один из `generate`, `optimize`, `validate`, `analyze`;
- `label` — опциональная метка результата шага;
- `args` — аргументы CLI-команды в формате `--kebab-case`;
- ссылки между шагами/параметрами: `{"$ref": "<label>.<field>"}` или строка `$ref:<label>.<field>`.
  Для общих параметров используйте label `params`, например: `{"$ref": "params.shared.curves_per_n"}`.

Пример (фрагмент):

```json
{
  "params": {
    "shared": {
      "curves_per_n": 12,
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
        "curves-per-n": {"$ref": "params.shared.curves_per_n"},
        "curve-timeout-sec": {"$ref": "params.shared.curve_timeout_sec"}
      }
    }
  ]
}
```

Опорный план для сравнения всех методов (generate + optimize/validate для `de`, `rs`, `pso`, `bo`, `ga`):

```bash
ecm-optimizer run-plan --plan baseline_all_methods
```


Дополнительный план полного мульти-прогона по нескольким размерам делителей (`target-digits=20,25,30`) с финальным общим анализом:

```bash
ecm-optimizer run-plan --plan full_all_methods_multi_divisors
```

Файл плана: `data/plans/full_all_methods_multi_divisors.json`.

Проверка плана без фактического запуска:

```bash
ecm-optimizer run-plan --plan baseline_all_methods --dry-run
```

Файл плана: `data/plans/baseline_all_methods.json`.

В опорном плане используется единый `seed` на шаге `generate`; для `optimize`/`validate` seed не задаётся отдельно, поэтому команды автоматически берут seed датасета.
Параметр `workers` в плане не указан, значит используется поведение CLI по умолчанию (`-1`, все доступные CPU).
Параметры плана облегчены для быстрого старта: уменьшены размеры датасета, `curves-per-n` и бюджеты/итерации оптимизаторов.


### 5) Сравнительный multi-run анализ (все методы сразу)

```bash
ecm-optimizer analyze \
  --input data/experiments/20_dset_20260330T134425Z
```

Команда строит сравнительные графики и агрегированную статистику по нескольким run:
- overlay convergence: один комбинированный PNG (два subplot: `eval` и `time`);
- boxplot финального `objective`;
- violin `time_to_best`;
- pareto `objective vs elapsed`;
- success profile: один комбинированный PNG (два subplot: `eval` и `time`) для заданного `--success-threshold` (или auto-порогу).

По умолчанию (без `--input`) анализатор автоматически берет **все** optimize-результаты из `data/experiments`.

Поведение `--input` упрощено:
- если передан конкретный run (`.../optimize_<TS>/` или `..._optimize_<TS>.json`), анализируется только этот запуск;
- если передана верхняя папка, рекурсивно ищутся все `*_optimize_*.json` внутри неё;
- если `--input` начинается с `!`, это правило исключения (по пути/маске/подстроке), например `--input "!*/rs/*"`;
- если переданы только исключения (`!`), базовый набор берется из `data/experiments`, а затем исключается по правилам.

По умолчанию результат сохраняется в `data/analysis/analyze_<UTC_TIMESTAMP>/` (или в `--output-dir`) и обязательно включает:
- `multi_run_summary.json` — агрегированные метрики;
- `multi_run_summary.json` также содержит секцию `analysis_run` с параметрами запуска анализатора и списками найденных run-файлов;
- PNG-графики сравнения.

Группировка графиков/статистики задаётся `--group-by` (можно передавать несколько раз), основные уровни:
- `divisor_size` (размер делителя / target digits),
- `method` (метод оптимизации).

## Структура пакета

- `ecm_optimizer/cli/` — команды `generate`, `optimize`, `validate`.
- `ecm_optimizer/core/` — генерация задачи, запуск ECM, fitness, baseline и validation.
- `ecm_optimizer/optimizers/` — базовый интерфейс и реализации DE/RS/PSO/BO/GA.
- `ecm_optimizer/utils/` — JSON I/O, logging, seed utilities и отчёты по оптимизации (графики/статистика).
- `ecm_optimizer/config.py` — централизованные константы и пути.
- `ecm_optimizer/models.py` — dataclass-модели конфигурации и результатов.
- `data/numbers/` — датасеты.
- `data/experiments/` — результаты optimize/validate.

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для генерации датасетов и оптимизатора используйте фиксированный `--seed`.
- Для независимых этапов применяются детерминированные производные seed'ы через `seed_utils`.
- Для финальной валидации увеличивайте `--curves-per-n`.
