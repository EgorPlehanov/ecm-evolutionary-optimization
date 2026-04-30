#!/bin/bash
#SBATCH --job-name=ecm_plan_multi
#SBATCH --partition=tornado
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=02:00:00
#SBATCH --output=data/slurm_runs/%x-%j.out
#SBATCH --error=data/slurm_runs/%x-%j.err

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

mkdir -p data/slurm_runs
RUN_ROOT="data/slurm_runs/job_${SLURM_JOB_ID}"
mkdir -p "${RUN_ROOT}/steps" "${RUN_ROOT}/state"
exec > >(tee -a "${RUN_ROOT}/controller.out") 2> >(tee -a "${RUN_ROOT}/controller.err" >&2)

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
STEP_PARTITION="${STEP_PARTITION:-tornado}"
STEP_CPUS_PER_TASK="${STEP_CPUS_PER_TASK:-28}"
STEP_TIME_LIMIT="${STEP_TIME_LIMIT:-12:00:00}"
STEP_LOG_DIR="${STEP_LOG_DIR:-${RUN_ROOT}/steps}"
STEP_STATE_FILE="${STEP_STATE_FILE:-${RUN_ROOT}/state/plan_state.json}"

echo "Проверка плана (dry-run validation): ${PLAN_NAME}"
ecm-optimizer run-plan-slurm \
  --plan "${PLAN_NAME}" \
  --partition "${STEP_PARTITION}" \
  --cpus-per-task "${STEP_CPUS_PER_TASK}" \
  --time-limit "${STEP_TIME_LIMIT}" \
  --log-dir "${STEP_LOG_DIR}" \
  --state-file "${STEP_STATE_FILE}" \
  --dry-run >/dev/null

echo "Оркестратор: ${PLAN_NAME}"
echo "Controller node(s): ${SLURM_NNODES}, tasks: ${SLURM_NTASKS}, cpu/task: ${SLURM_CPUS_PER_TASK}"
echo "Step resources: partition=${STEP_PARTITION}, cpus-per-task=${STEP_CPUS_PER_TASK}, time=${STEP_TIME_LIMIT}"
echo "Step logs: ${STEP_LOG_DIR}, state: ${STEP_STATE_FILE}"

# Оркестратор сабмитит шаги плана как отдельные sbatch jobs с afterok-зависимостями.
# Независимые ветки графа выполняются параллельно и могут быть размещены на разных нодах.
srun --ntasks=1 --nodes=1 ecm-optimizer run-plan-slurm \
  --plan "${PLAN_NAME}" \
  --partition "${STEP_PARTITION}" \
  --cpus-per-task "${STEP_CPUS_PER_TASK}" \
  --time-limit "${STEP_TIME_LIMIT}" \
  --log-dir "${STEP_LOG_DIR}" \
  --state-file "${STEP_STATE_FILE}"
