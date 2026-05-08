# Эксперимент `20_dset_20260505T214657Z_job7012254` — сводка

## 1) Общие параметры эксперимента

- **Размер делителя (`target_digits`)**: `20`.
- **Обучающая выборка**: `80` чисел (`train.json`).
- **Контрольная выборка**: `80` чисел (`control.json`).
- **Seed**: `42`.
- **Параметры валидации**: `max_curves_per_n=600`, `repeats_per_n=80`.
- **Параметры оптимизации**: `max_curves_per_n=260`, `repeats_per_n=8`.

## 2) Метрики по методам (BO, DE, RS, PSO, GA)

> Ниже — агрегированные значения из журнала `docs/experiment_results_journal_ru.md` для блока `[RUN-2026-05-05-214657Z]`.

| Метод | B1 | B2 | Score baseline (`score_base`) | Score validation (`score_val`) | Δ score | Time validation (`time_val`, сек) | Δ time | Curves validation (`curves_val`) | Δ curves | Success rate (`success_rate_val`) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BO  | 26729 | 2126731 | 37325.69 | 27844.52 | -9481.17 (-25.40%) | 2.5143 | -0.73 (-22.48%) | 54.03 | -43.78 (-44.76%) | 1.0000 |
| DE  | 38271 | 2713793 | 36652.99 | 27670.37 | -8982.62 (-24.51%) | 2.5544 | -0.63 (-19.78%) | 42.53 | -53.70 (-55.80%) | 1.0000 |
| RS  | 26901 | 2959183 | 36443.01 | 28181.66 | -8261.34 (-22.67%) | 2.5631 | -0.60 (-19.01%) | 51.02 | -44.91 (-46.81%) | 0.9998 |
| PSO | 49999 | 3000000 | 36731.76 | 27875.72 | -8856.05 (-24.11%) | 2.6009 | -0.59 (-18.51%) | 37.33 | -58.98 (-61.24%) | 1.0000 |
| GA  | 37480 | 2545245 | 36482.86 | 27203.36 | -9279.51 (-25.44%) | 2.5088 | -0.66 (-20.86%) | 42.31 | -53.30 (-55.75%) | 1.0000 |

## 3) Графики (`.png` в `plots`)

### Сравнение score (baseline vs validation)
Общий график по всем методам в эксперименте не найден; доступны отдельные графики по методам:
- `data/experiments/20_dset_20260505T214657Z_job7012254/bo/optimize_20260505T214714Z_job7012261/plots/bo_validate_20260506T000600Z_job7012262_score_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/de/optimize_20260505T214714Z_job7012255/plots/de_validate_20260506T051949Z_job7012256_score_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/rs/optimize_20260505T214714Z_job7012257/plots/rs_validate_20260506T002038Z_job7012258_score_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/pso/optimize_20260505T214714Z_job7012259/plots/pso_validate_20260506T051020Z_job7012260_score_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/ga/optimize_20260505T224607Z_job7012263/plots/ga_validate_20260506T075907Z_job7012264_score_distribution.png`

### Сравнение числа кривых (baseline vs validation)
Общий график по всем методам не найден; доступны отдельные:
- `data/experiments/20_dset_20260505T214657Z_job7012254/bo/optimize_20260505T214714Z_job7012261/plots/bo_validate_20260506T000600Z_job7012262_curves_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/de/optimize_20260505T214714Z_job7012255/plots/de_validate_20260506T051949Z_job7012256_curves_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/rs/optimize_20260505T214714Z_job7012257/plots/rs_validate_20260506T002038Z_job7012258_curves_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/pso/optimize_20260505T214714Z_job7012259/plots/pso_validate_20260506T051020Z_job7012260_curves_distribution.png`
- `data/experiments/20_dset_20260505T214657Z_job7012254/ga/optimize_20260505T224607Z_job7012263/plots/ga_validate_20260506T075907Z_job7012264_curves_distribution.png`

### GA: динамика оптимизации
- `data/experiments/20_dset_20260505T214657Z_job7012254/ga/optimize_20260505T224607Z_job7012263/plots/ga_optimize_20260505T224607Z_job7012263_progress_by_phase.png`

### PSO: траектория поиска
- `data/experiments/20_dset_20260505T214657Z_job7012254/pso/optimize_20260505T214714Z_job7012259/plots/pso_optimize_20260505T214714Z_job7012259_b1_b2_trajectory.png`

## 4) Ключевые фрагменты SLURM-сценариев

### `run_ecm_plan.slurm`
```bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH --partition=tornado
#SBATCH --time=3-00:00:00
#SBATCH --job-name=ecm_plan
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"
srun ecm-optimizer run-plan --plan "${PLAN_NAME}"
```

### `run_ecm_plan_multinode.slurm`
```bash
#SBATCH --job-name=ecm_plan_multi
#SBATCH --partition=tornado
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=02:00:00
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"

ecm-optimizer run-plan-slurm \
  --plan "${PLAN_NAME}" \
  --dry-run

srun --ntasks=1 --nodes=1 ecm-optimizer run-plan-slurm \
  --plan "${PLAN_NAME}" \
  --worker
```

## 5) Ссылка на программный комплекс

- GitHub-репозиторий: `<укажите URL удалённого origin (в локальном git remote URL не задан).>`
