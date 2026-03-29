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
