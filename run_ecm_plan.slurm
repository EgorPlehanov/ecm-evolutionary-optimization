#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH --partition=tornado
#SBATCH --time=3-00:00:00
#SBATCH --job-name=ecm_plan
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

set -euo pipefail

# Инициализация Environment Modules (как в инструкции СКЦ)
if [ -f /etc/profile.d/modules-basis.sh ]; then
  source /etc/profile.d/modules-basis.sh
fi

module purge

# На практике для scipy/openblas на СКЦ удобно использовать conda-вариант python.
# Делаем fallback на обычные python-модули, если conda-модуль недоступен.
PYTHON_MODULE=""
for mod in python/3.10_conda python/3.10 python/3.12; do
  if module load "$mod"; then
    PYTHON_MODULE="$mod"
    break
  fi
done

if [ -z "$PYTHON_MODULE" ]; then
  echo "ERROR: Не удалось загрузить ни один python-модуль (python/3.10_conda, python/3.10, python/3.12)." >&2
  exit 1
fi

echo "Loaded Python module: ${PYTHON_MODULE}"

# Рабочая директория проекта (директория, откуда вызван sbatch)
cd "${SLURM_SUBMIT_DIR}"

# Виртуальное окружение проекта (если подготовлено заранее)
if [ -d .venv ]; then
  source .venv/bin/activate
fi

# Локальная установка ECM обычно размещается в ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

# Ограничим OpenMP/BLAS-потоки в рамках выделенных ядер Slurm.
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

# Проверки доступности нужных CLI.
command -v ecm-optimizer >/dev/null 2>&1 || {
  echo "ERROR: ecm-optimizer не найден. Установите проект: pip install -e ." >&2
  exit 1
}

command -v ecm >/dev/null 2>&1 || {
  echo "ERROR: бинарник ecm не найден. Установите GMP-ECM (например в ~/.local/bin)." >&2
  exit 1
}

# Переопределение плана через переменную окружения на этапе sbatch.
# Примеры:
#   sbatch run_ecm_plan.slurm
#   sbatch --export=PLAN_NAME=tuned_all_methods_multiseed_20d run_ecm_plan.slurm
#   sbatch --export=PLAN_NAME=data/plans/full_all_methods_20_25_30.json run_ecm_plan.slurm
PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"

# Запуск плана (если PLAN_NAME без .json — CLI ищет файл в data/plans/)
srun ecm-optimizer run-plan --plan "${PLAN_NAME}"
