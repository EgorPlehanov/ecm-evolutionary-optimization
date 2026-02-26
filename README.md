# ECM Evolutionary Optimization

Репозиторий для НИР по проверке гипотезы: можно ли автоматически подобрать параметры GMP-ECM (`B1`, `B2`) с помощью дифференциальной эволюции так, чтобы уменьшить ожидаемое время факторизации по сравнению со стандартными табличными значениями.

## Что уже реализовано

- Каркас Python-пайплайна для:
  - запуска `gmp-ecm` и парсинга результата;
  - оценки фитнеса как эмпирического `E[T_success]`;
  - оптимизации `log10(B1), log10(B2)` через `scipy.optimize.differential_evolution`;
  - валидации найденных параметров против baseline;
  - генерации train/control наборов семипростых чисел (`N = p*q`) с настраиваемыми размерами множителей.
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

### 2) Оптимизация параметров ECM

```bash
PYTHONPATH=src python -m ecm_opt.cli optimize \
  --dataset data/d35_train.txt \
  --ecm-bin ecm \
  --curves-per-n 50 \
  --popsize 16 \
  --maxiter 25
```


Для быстрого smoke-теста и видимого прогресса используйте:

```bash
PYTHONPATH=src python -m ecm_opt.cli optimize \
  --dataset data/d35_train.txt \
  --ecm-bin ecm \
  --curves-per-n 1 \
  --popsize 4 \
  --maxiter 1 \
  --b1-max 100000 \
  --ratio-max 20 \
  --curve-timeout-sec 5 \
  --verbose
```

### 3) Валидация против baseline

```bash
PYTHONPATH=src python -m ecm_opt.cli validate \
  --dataset data/d35_control.txt \
  --ecm-bin ecm \
  --opt-b1 100000 \
  --opt-b2 3000000 \
  --base-b1 50000 \
  --base-b2 1000000 \
  --curves-per-n 100
```

## Структура

- `docs/research_plan_ru.md` — формализованный план экспериментов.
- `src/ecm_opt/dataset.py` — генерация семипростых train/control наборов.
- `src/ecm_opt/ecm_runner.py` — запуск GMP-ECM.
- `src/ecm_opt/fitness.py` — оценка ожидаемого времени до успеха.
- `src/ecm_opt/optimizer.py` — настройка и запуск DE.
- `src/ecm_opt/validation.py` — сравнение optimized vs baseline.
- `src/ecm_opt/cli.py` — CLI (`generate-dataset`, `optimize`, `validate`).

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для DE и генерации датасетов используйте фиксированный `--seed`.
- Для финальной валидации увеличивайте `--curves-per-n`.
