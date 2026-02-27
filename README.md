# ECM Evolutionary Optimization

Репозиторий для НИР по проверке гипотезы: можно ли автоматически подобрать параметры GMP-ECM (`B1`, `B2`) с помощью дифференциальной эволюции так, чтобы уменьшить ожидаемое время факторизации по сравнению со стандартными табличными значениями.

## Что уже реализовано

- Каркас Python-пайплайна для:
  - запуска `gmp-ecm` и парсинга результата;
  - оценки фитнеса как эмпирического `E[T_success]`;
  - оптимизации `log10(B1), log10(B2)` через `scipy.optimize.differential_evolution`;
  - автоматической валидации найденных параметров против baseline;
  - генерации train/control наборов семипростых чисел (`N = p*q`) с настраиваемыми размерами множителей;
  - сохранения timestamped JSON-метаданных по каждому запуску optimize/validate.
- Документированный план НИР в `docs/research_plan_ru.md`.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1) Генерация train/control датасетов

```bash
PYTHONPATH=src python -m ecm_opt.cli generate-dataset \
  --target-digits 35 \
  --cofactor-digits 90 \
  --train-count 20 \
  --control-count 20 \
  --seed 42 \
  --output-dir data \
  --prefix d35
```

Команда создаёт:
- `data/d35_train.txt` — числа для оптимизации;
- `data/d35_control.txt` — отдельный контрольный набор;
- `data/d35_manifest.csv` — `n,p,q` для воспроизводимости.

### 2) Оптимизация параметров ECM (с автосохранением результата)

```bash
PYTHONPATH=src python -m ecm_opt.cli optimize \
  --dataset data/d35_train.txt \
  --ecm-bin ecm \
  --curves-per-n 50 \
  --popsize 16 \
  --maxiter 25 \
  --results-dir results \
  --workers -1 \
  --verbose
```

После завершения в консоль печатается `result_file=...` (например `results/optimize_20260101T120000Z.json`).
В файле сохраняются оптимизированные значения, конфиг запуска, detected target digits и автоматически подобранный baseline.

### 3) Валидация без ручного копирования opt/base

```bash
PYTHONPATH=src python -m ecm_opt.cli validate \
  --dataset data/d35_control.txt \
  --ecm-bin ecm \
  --opt-result-file results/optimize_20260101T120000Z.json \
  --curves-per-n 100 \
  --curve-timeout-sec 10 \
  --workers -1 \
  --results-dir results
```

- `opt` берётся автоматически из `--opt-result-file`.
- `base` подбирается автоматически из внутренней baseline-таблицы по `target_digits` из метаданных dataset/result.
- Если нужно, `base` можно явно переопределить `--base-b1/--base-b2`.
- `--workers N` включает multiprocessing по числам датасета (`1` — последовательно, `-1` — все ядра CPU).
- Если по числу не найдено ни одного фактора за `curves-per-n`, вместо `Infinity` применяется большой штраф по времени (чтобы оптимизатор продолжал сравнивать кандидаты, а не залипал на `inf`).
- Валидация также пишет timestamped JSON: `results/validate_*.json`.

## Структура

- `docs/research_plan_ru.md` — формализованный план экспериментов.
- `src/ecm_opt/dataset.py` — генерация и чтение метаданных train/control наборов.
- `src/ecm_opt/baseline.py` — автоматический выбор baseline.
- `src/ecm_opt/io_utils.py` — timestamped JSON I/O.
- `src/ecm_opt/ecm_runner.py` — запуск GMP-ECM.
- `src/ecm_opt/fitness.py` — оценка ожидаемого времени до успеха.
- `src/ecm_opt/optimizer.py` — настройка и запуск DE.
- `src/ecm_opt/validation.py` — сравнение optimized vs baseline.
- `src/ecm_opt/cli.py` — CLI (`generate-dataset`, `optimize`, `validate`).

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для DE и генерации датасетов используйте фиксированный `--seed`.
- Для финальной валидации увеличивайте `--curves-per-n`.
- Храните и версионируйте файлы `results/optimize_*.json` и `results/validate_*.json`.
