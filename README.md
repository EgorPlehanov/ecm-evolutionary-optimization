# ECM Evolutionary Optimization

Репозиторий для НИР по проверке гипотезы: можно ли автоматически подобрать параметры GMP-ECM (`B1`, `B2`) с помощью дифференциальной эволюции так, чтобы уменьшить ожидаемое время факторизации по сравнению со стандартными табличными значениями.

## Что уже реализовано

- Каркас Python-пайплайна для:
  - запуска `gmp-ecm` и парсинга результата;
  - оценки фитнеса как эмпирического `E[T_success]`;
  - оптимизации `log10(B1), log10(B2)` через `scipy.optimize.differential_evolution`;
  - валидации найденных параметров против baseline.
- Документированный план НИР в `docs/research_plan_ru.md`.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Пример запуска оптимизации (при установленном `ecm` в PATH):

```bash
python -m ecm_opt.cli optimize \
  --dataset data/train_35d.txt \
  --ecm-bin ecm \
  --curves-per-n 50 \
  --popsize 16 \
  --maxiter 25
```

## Структура

- `docs/research_plan_ru.md` — формализованный план экспериментов.
- `src/ecm_opt/ecm_runner.py` — запуск GMP-ECM.
- `src/ecm_opt/fitness.py` — оценка ожидаемого времени до успеха.
- `src/ecm_opt/optimizer.py` — настройка и запуск DE.
- `src/ecm_opt/validation.py` — сравнение optimized vs baseline.
- `src/ecm_opt/cli.py` — CLI.

## Примечания по воспроизводимости

- Фиксируйте версию GMP-ECM, Python и SciPy.
- Для DE используйте фиксированный `--seed`.
- Для финальной валидации увеличивайте `--curves-per-n`.
