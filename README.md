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
  --control-count 20 \
  --seed 42 \
  --output-dir data/numbers \
  --prefix d35
```

Команда создаёт:
- `data/numbers/d35_<UTC_TIMESTAMP>/train.json` — числа для оптимизации;
- `data/numbers/d35_<UTC_TIMESTAMP>/control.json` — отдельный контрольный набор;
- `data/numbers/d35_<UTC_TIMESTAMP>/manifest.json` — `n,p,q` для воспроизводимости;
- `data/numbers/d35_<UTC_TIMESTAMP>/generation.json` — метаданные и параметры генерации.

### 2) Оптимизация параметров ECM

```bash
ecm-optimizer optimize \
  --dataset d35_<UTC_TIMESTAMP> \
  --ecm-bin ecm \
  --curves-per-n 50 \
  --popsize 16 \
  --maxiter 25 \
  --b1-min 1e3 \
  --b1-max 1e9 \
  --b2-min 1e3 \
  --b2-max 1e11 \
  --ratio-max 100 \
  --results-dir data/experiments \
  --workers -1 \
  --verbose
```

После завершения в консоль печатается `result_file=...`, а JSON-файл сохраняется в `data/experiments/`.

`--dataset` можно передать как полный путь к JSON-файлу/папке или как имя папки внутри `data/numbers` (например `d35_<UTC_TIMESTAMP>`).

Важно: поддерживается только новый JSON-формат датасетов (`ecm_dataset_v1`), обратная совместимость со старыми `txt/csv` датасетами удалена.

### 3) Валидация

```bash
ecm-optimizer validate \
  --dataset d35_<UTC_TIMESTAMP> \
  --ecm-bin ecm \
  --opt-result-file data/experiments/optimize_train_42.json \
  --curves-per-n 100 \
  --curve-timeout-sec 10 \
  --workers -1 \
  --results-dir data/experiments
```

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
