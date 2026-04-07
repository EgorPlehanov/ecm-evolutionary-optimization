# Отчёт по оптимизации: bo_optimize_20260407T151158Z

## Метаданные
- метод: `bo`
- датасет: `data/numbers/20_dset_20260407T150927Z/train.json`
- оптимум `(B1, B2)`: `(1942, 1942)`
- objective: `0.8014524304016959`
- curves_per_n: `12`
- границы: `B1[1000.0, 12000.0]`, `B2[1000.0, 144000.0]`, `ratio_max=12.0`

## Ключевые статистики
- `best_eval`: `7`
- `best_eval_fraction`: `0.35`
- `eval_per_sec`: `3.3859629491008523`
- `evaluation_count`: `20`
- `improvement_percent`: `53.92937622982037`
- `max_plateau_evals`: `13`
- `median_plateau_evals`: `0.0`
- `new_best_count`: `4`
- `new_best_rate`: `0.2`
- `p90_plateau_evals`: `9.0`
- `time_to_best_sec`: `2.165911986026913`
- `time_to_first_improvement_sec`: `0.45446038799127564`
- `total_runtime_sec`: `5.906929421995301`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `late_best` | ✅ ОК | `0.36667307687168704` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `53.92937622982037` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ✅ ОК | `0.2` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.65` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |

## Графики
- [`bo_optimize_20260407T151158Z_b1_b2_trajectory.png`](plots/bo_optimize_20260407T151158Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/bo_optimize_20260407T151158Z_b1_b2_trajectory.png)
- [`bo_optimize_20260407T151158Z_b1_ratio_heatmap.png`](plots/bo_optimize_20260407T151158Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/bo_optimize_20260407T151158Z_b1_ratio_heatmap.png)
- [`bo_optimize_20260407T151158Z_convergence.png`](plots/bo_optimize_20260407T151158Z_convergence.png)
![convergence](plots/bo_optimize_20260407T151158Z_convergence.png)
- [`bo_optimize_20260407T151158Z_improvement_deltas.png`](plots/bo_optimize_20260407T151158Z_improvement_deltas.png)
![improvement_deltas](plots/bo_optimize_20260407T151158Z_improvement_deltas.png)
- [`bo_optimize_20260407T151158Z_jump_plot.png`](plots/bo_optimize_20260407T151158Z_jump_plot.png)
![jump_plot](plots/bo_optimize_20260407T151158Z_jump_plot.png)
- [`bo_optimize_20260407T151158Z_progress_by_phase.png`](plots/bo_optimize_20260407T151158Z_progress_by_phase.png)
![progress_by_phase](plots/bo_optimize_20260407T151158Z_progress_by_phase.png)
- [`bo_optimize_20260407T151158Z_raw_fitness.png`](plots/bo_optimize_20260407T151158Z_raw_fitness.png)
![raw_fitness](plots/bo_optimize_20260407T151158Z_raw_fitness.png)
- [`bo_optimize_20260407T151158Z_time_efficiency.png`](plots/bo_optimize_20260407T151158Z_time_efficiency.png)
![time_efficiency](plots/bo_optimize_20260407T151158Z_time_efficiency.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/bo_optimize_20260407T151158Z_events.csv' },
  { file: 'tables/bo_optimize_20260407T151158Z_new_best.csv' },
  { file: 'tables/bo_optimize_20260407T151158Z_phase_summary.csv' },
  { file: 'tables/bo_optimize_20260407T151158Z_run_summary.csv' },
];

function normalizeDateInput(value) {
  if (typeof value !== 'string') return value;
  return value.trim().replace(/^"|"$/g, '');
}

function isDateString(value) {
  if (typeof value !== 'string') return false;
  const v = normalizeDateInput(value);
  return /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}/.test(v);
}

function formatDateTime(value) {
  if (!isDateString(value)) return value;
  const v = normalizeDateInput(value);
  try {
    const date = new Date(v);
    if (!isNaN(date.getTime())) {
      const day = String(date.getUTCDate()).padStart(2, '0');
      const month = String(date.getUTCMonth() + 1).padStart(2, '0');
      const year = date.getUTCFullYear();
      const hours = String(date.getUTCHours()).padStart(2, '0');
      const minutes = String(date.getUTCMinutes()).padStart(2, '0');
      const seconds = String(date.getUTCSeconds()).padStart(2, '0');
      return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
    }
  } catch (e) {
    return value;
  }
  return value;
}

function roundNumber(v) {
  if (isDateString(v)) return formatDateTime(v);
  if (typeof v === 'string' && /^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}$/.test(v)) return v;
  const raw = normalizeDateInput(v);
  const n = parseFloat(raw);
  if (isNaN(n)) return raw;
  const rounded = Math.round(n * 1e9) / 1e9;
  return rounded.toLocaleString('en-US', { useGrouping: false, maximumFractionDigits: 9 });
}

function getTitleFromFile(filepath) {
  const filename = filepath.split('/').pop().replace('.csv', '');
  return filename.replace(/_\d{8}T\d{6}Z/, '').replace(/_/g, ' ');
}

async function createTable(config) {
  const resp = await fetch(config.file);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const text = await resp.text();
  const rows = text.trim().split(/\r?\n/).map(row => row.split(','));

  let html = '<table border="1" cellpadding="5">';
  rows.forEach((row, i) => {
    html += '<tr>';
    row.forEach(cell => {
      let content = cell;
      if (i !== 0) {
        content = formatDateTime(cell);
        content = roundNumber(content);
      }
      html += i === 0 ? `<th>${content}</th>` : `<td>${content}</td>`;
    });
    html += '</tr>';
  });
  html += '</table>';

  const title = getTitleFromFile(config.file);
  const rowCount = Math.max(0, rows.length - 1);

  return `
    <details>
      <summary><strong>${title}</strong> <a href="${config.file}">(CSV)</a> (${rowCount} записей)</summary>
      <div style="margin-top:10px; overflow-x:auto;">${html}</div>
    </details>
  `;
}

async function renderAllTables() {
  const container = document.getElementById('tables-container');
  if (!container) return;
  container.innerHTML = '<div>Загрузка таблиц...</div>';
  try {
    const tablesHtml = await Promise.all(tables.map(t => createTable(t)));
    container.innerHTML = tablesHtml.join('');
  } catch (err) {
    container.innerHTML = `<div>Ошибка загрузки таблиц: ${err}</div>`;
  }
}

renderAllTables();
</script>
