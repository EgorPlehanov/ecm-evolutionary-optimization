#!/bin/bash
#SBATCH --job-name=ecm_plan_multi
#SBATCH --partition=tornado
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH --time=3-00:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

set -euo pipefail

if [ -f /etc/profile.d/modules-basis.sh ]; then
  source /etc/profile.d/modules-basis.sh
fi

module purge
PYTHON_MODULE=""
for mod in python/3.10_conda python/3.10 python/3.12; do
  if module load "$mod"; then
    PYTHON_MODULE="$mod"
    break
  fi
done

if [ -z "$PYTHON_MODULE" ]; then
  echo "ERROR: Не удалось загрузить python-модуль." >&2
  exit 1
fi

echo "Loaded Python module: ${PYTHON_MODULE}"
cd "${SLURM_SUBMIT_DIR}"

if [ -d .venv ]; then
  source .venv/bin/activate
fi

export PATH="$HOME/.local/bin:$PATH"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

command -v ecm-optimizer >/dev/null 2>&1 || { echo "ERROR: ecm-optimizer не найден." >&2; exit 1; }
command -v ecm >/dev/null 2>&1 || { echo "ERROR: бинарник ecm не найден." >&2; exit 1; }

# Один план: задается через PLAN_NAME.
# Пример:
# sbatch --export=PLAN_NAME=full_all_methods_single_run_20d run_ecm_plan_multinode.slurm
PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"

echo "Проверка плана (dry-run validation): ${PLAN_NAME}"
ecm-optimizer run-plan --plan "${PLAN_NAME}" --dry-run >/dev/null

echo "Запуск одного плана: ${PLAN_NAME}"
echo "Выделено нод: ${SLURM_NNODES}, задач: ${SLURM_NTASKS}, CPU/задача: ${SLURM_CPUS_PER_TASK}"

# Один orchestrator-процесс run-plan.
# Внутренняя параллельность обеспечивается параметрами workers в шагах optimize/validate плана.
srun --ntasks=1 --nodes=1 ecm-optimizer run-plan --plan "${PLAN_NAME}"
