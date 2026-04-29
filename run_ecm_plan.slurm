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

# Автокоммит и отправка новых/изменённых результатов в git.
# По умолчанию включено. Отключить можно через:
#   sbatch --export=GIT_AUTOPUSH=0 run_ecm_plan.slurm
# По умолчанию добавляются:
#   - все *.out и *.err в корне проекта
#   - вся папка data
GIT_AUTOPUSH="${GIT_AUTOPUSH:-1}"

if [ "${GIT_AUTOPUSH}" = "1" ]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "WARN: git не найден, пропускаю автокоммит результатов." >&2
    exit 0
  fi

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "WARN: текущая директория не является git-репозиторием, пропускаю автокоммит." >&2
    exit 0
  fi

  echo "Автодобавление результатов в git: *.out *.err data/"
  git add --all -- ./*.out ./*.err data/ 2>/dev/null || true

  if git diff --cached --quiet; then
    echo "Новых изменений результатов для коммита нет."
  else
    COMMIT_MESSAGE="results: update after plan ${PLAN_NAME} (job ${SLURM_JOB_ID:-manual})"
    git commit -m "${COMMIT_MESSAGE}"

    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    if [ "${CURRENT_BRANCH}" = "HEAD" ]; then
      echo "WARN: detached HEAD, пропускаю git push." >&2
      exit 0
    fi

    git push origin "${CURRENT_BRANCH}"
    echo "Результаты отправлены в origin/${CURRENT_BRANCH}"
  fi
fi