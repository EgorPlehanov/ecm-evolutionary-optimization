# Отчёт по оптимизации: ga_optimize_20260407T151333Z

## Метаданные
- метод: `ga`
- датасет: `data/numbers/20_dset_20260407T150927Z/train.json`
- оптимум `(B1, B2)`: `(1113, 1689)`
- objective: `0.7383682288054843`
- curves_per_n: `12`
- границы: `B1[1000.0, 12000.0]`, `B2[1000.0, 144000.0]`, `ratio_max=12.0`

## Ключевые статистики
- `best_eval`: `137`
- `best_eval_fraction`: `0.3494897959183674`
- `eval_per_sec`: `4.207528954866781`
- `evaluation_count`: `392`
- `improvement_percent`: `13.621212636107696`
- `max_plateau_evals`: `255`
- `median_plateau_evals`: `28.5`
- `new_best_count`: `5`
- `new_best_rate`: `0.012755102040816327`
- `p90_plateau_evals`: `157.5`
- `time_to_best_sec`: `33.040283322974574`
- `time_to_first_improvement_sec`: `6.729498339991551`
- `total_runtime_sec`: `93.16645780002`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `late_best` | ✅ ОК | `0.35463710978359725` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `13.621212636107696` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.012755102040816327` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.6505102040816326` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |

## Графики
- [`ga_optimize_20260407T151333Z_b1_b2_trajectory.png`](plots/ga_optimize_20260407T151333Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/ga_optimize_20260407T151333Z_b1_b2_trajectory.png)
- [`ga_optimize_20260407T151333Z_b1_ratio_heatmap.png`](plots/ga_optimize_20260407T151333Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/ga_optimize_20260407T151333Z_b1_ratio_heatmap.png)
- [`ga_optimize_20260407T151333Z_convergence.png`](plots/ga_optimize_20260407T151333Z_convergence.png)
![convergence](plots/ga_optimize_20260407T151333Z_convergence.png)
- [`ga_optimize_20260407T151333Z_improvement_deltas.png`](plots/ga_optimize_20260407T151333Z_improvement_deltas.png)
![improvement_deltas](plots/ga_optimize_20260407T151333Z_improvement_deltas.png)
- [`ga_optimize_20260407T151333Z_jump_plot.png`](plots/ga_optimize_20260407T151333Z_jump_plot.png)
![jump_plot](plots/ga_optimize_20260407T151333Z_jump_plot.png)
- [`ga_optimize_20260407T151333Z_progress_by_phase.png`](plots/ga_optimize_20260407T151333Z_progress_by_phase.png)
![progress_by_phase](plots/ga_optimize_20260407T151333Z_progress_by_phase.png)
- [`ga_optimize_20260407T151333Z_raw_fitness.png`](plots/ga_optimize_20260407T151333Z_raw_fitness.png)
![raw_fitness](plots/ga_optimize_20260407T151333Z_raw_fitness.png)
- [`ga_optimize_20260407T151333Z_time_efficiency.png`](plots/ga_optimize_20260407T151333Z_time_efficiency.png)
![time_efficiency](plots/ga_optimize_20260407T151333Z_time_efficiency.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/ga_optimize_20260407T151333Z_events.csv' },
  { file: 'tables/ga_optimize_20260407T151333Z_new_best.csv' },
  { file: 'tables/ga_optimize_20260407T151333Z_phase_summary.csv' },
  { file: 'tables/ga_optimize_20260407T151333Z_run_summary.csv' },
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
