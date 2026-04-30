#!/bin/bash
#SBATCH --job-name=ecm_plan_multi
#SBATCH --partition=tornado
#SBATCH --nodes=4
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

# Список планов через пробел: экспортируйте при sbatch.
# Пример:
# sbatch --export=PLAN_LIST="full_all_methods_20_25_30 tuned_all_methods_multiseed_20d" run_ecm_plan_multinode.slurm
PLAN_LIST="${PLAN_LIST:-full_all_methods_single_run_20d}"
read -r -a PLANS <<< "${PLAN_LIST}"
PLAN_COUNT="${#PLANS[@]}"

if [ "${PLAN_COUNT}" -eq 0 ]; then
  echo "ERROR: PLAN_LIST пуст." >&2
  exit 1
fi

if [ "${PLAN_COUNT}" -gt "${SLURM_NTASKS}" ]; then
  echo "ERROR: планов (${PLAN_COUNT}) больше, чем доступных задач (${SLURM_NTASKS})." >&2
  echo "Увеличьте --nodes/--ntasks-per-node или сократите PLAN_LIST." >&2
  exit 1
fi

echo "Проверка планов (dry-run validation)"
for plan in "${PLANS[@]}"; do
  echo "Validate: ${plan}"
  ecm-optimizer run-plan --plan "${plan}" --dry-run >/dev/null
done

TMP_MULTI_PROG="$(mktemp)"
trap 'rm -f "${TMP_MULTI_PROG}"' EXIT

for idx in "${!PLANS[@]}"; do
  printf "%s bash -lc 'ecm-optimizer run-plan --plan %q'\n" "${idx}" "${PLANS[$idx]}" >> "${TMP_MULTI_PROG}"
done

echo "Запуск ${PLAN_COUNT} plan(s) параллельно на ${PLAN_COUNT} task(s)"
srun --ntasks="${PLAN_COUNT}" --multi-prog "${TMP_MULTI_PROG}"
