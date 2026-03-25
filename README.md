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
- `data/numbers/dset_<UTC_TIMESTAMP>/train.json` — числа для оптимизации;
- `data/numbers/dset_<UTC_TIMESTAMP>/control.json` — отдельный контрольный набор;
- `data/numbers/dset_<UTC_TIMESTAMP>/manifest.json` — `n,p,q` для воспроизводимости;
- `data/numbers/dset_<UTC_TIMESTAMP>/generation.json` — метаданные и параметры генерации.

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

После завершения в консоль печатается `result_file=...`, а JSON-файл сохраняется в `data/experiments/<DATASET_FOLDER>/optimize_<METHOD>_<UTC_TIMESTAMP>.json`, где `<METHOD>` — всегда короткий код (`de`, `rs`, `pso`, `bo`, `ga`).

Поддерживаемые значения `--method`:
- `de` / `differential-evolution` — реализовано;
- `rs` / `random-search` — реализовано;
- `pso` / `particle-swarm-optimization` — зарезервировано под будущую реализацию (пока команда вернёт ошибку);
- `bo` / `bayesian-optimization` — зарезервировано под будущую реализацию (пока команда вернёт ошибку);
- `ga` / `genetic-algorithm` — зарезервировано под будущую реализацию (пока команда вернёт ошибку).

Параметры алгоритмов разделены по префиксам:
- `--de-popsize`, `--de-maxiter` для DE;
- `--rs-budget` для Random Search.

`--dataset` можно передать как полный путь к JSON-файлу/папке или как имя папки внутри `data/numbers` (например `dset_<UTC_TIMESTAMP>`).

Поддерживаемый формат датасетов: JSON `ecm_dataset_v1`.

### 3) Валидация

```bash
ecm-optimizer validate
```

`--opt-result-file` можно передать как полный путь к JSON-файлу или только имя файла (поиск в `data/experiments/<DATASET_FOLDER>/`). Если не передавать, будет взят последний `optimize_*.json` (для выбранного датасета, либо глобально если `--dataset` не задан).

Если `--dataset` не указан, он берётся из поля `dataset` в выбранном optimize-результате. Если не заданы `--curves-per-n` и `--curve-timeout-sec`, они также подтягиваются из `config` optimize-результата.

## Структура пакета

- `ecm_optimizer/cli/` — команды `generate`, `optimize`, `validate`.
- `ecm_optimizer/core/` — генерация задачи, запуск ECM, fitness, baseline и validation.
- `ecm_optimizer/optimizers/` — базовый интерфейс, differential evolution и random search.
- `ecm_optimizer/utils/` — JSON I/O, logging и seed utilities.
- `ecm_optimizer/config.py` — централизованные константы и пути.
- `ecm_optimizer/models.py` — dataclass-модели конфигурации и результатов.
- `data/numbers/` — датасеты.
- `data/experiments/` — результаты optimize/validate.

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для генерации датасетов и оптимизатора используйте фиксированный `--seed`.
- Для независимых этапов применяются детерминированные производные seed'ы через `seed_utils`.
- Для финальной валидации увеличивайте `--curves-per-n`.
