# Отчёт по оптимизации: pso_optimize_20260407T143922Z

## Метаданные
- метод: `pso`
- датасет: `data/numbers/20_dset_20260407T143642Z/train.json`
- оптимум `(B1, B2)`: `(1000, 1000)`
- objective: `0.6614213145512622`
- curves_per_n: `12`
- границы: `B1[1000.0, 30000.0]`, `B2[1000.0, 600000.0]`, `ratio_max=20.0`

## Ключевые статистики
- `best_eval`: `89`
- `best_eval_fraction`: `0.3803418803418803`
- `eval_per_sec`: `3.9164402685319546`
- `evaluation_count`: `234`
- `improvement_percent`: `41.8162259230794`
- `max_plateau_evals`: `145`
- `median_plateau_evals`: `10.5`
- `new_best_count`: `7`
- `new_best_rate`: `0.029914529914529916`
- `p90_plateau_evals`: `63.79999999999998`
- `time_to_best_sec`: `23.865827336034272`
- `time_to_first_improvement_sec`: `8.077046616992448`
- `total_runtime_sec`: `59.74823231599294`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `late_best` | ✅ ОК | `0.39943988986676776` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `41.8162259230794` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.029914529914529916` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.6196581196581197` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |

## Графики
- [`pso_optimize_20260407T143922Z_b1_b2_trajectory.png`](plots/pso_optimize_20260407T143922Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/pso_optimize_20260407T143922Z_b1_b2_trajectory.png)
- [`pso_optimize_20260407T143922Z_b1_ratio_heatmap.png`](plots/pso_optimize_20260407T143922Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/pso_optimize_20260407T143922Z_b1_ratio_heatmap.png)
- [`pso_optimize_20260407T143922Z_convergence.png`](plots/pso_optimize_20260407T143922Z_convergence.png)
![convergence](plots/pso_optimize_20260407T143922Z_convergence.png)
- [`pso_optimize_20260407T143922Z_improvement_deltas.png`](plots/pso_optimize_20260407T143922Z_improvement_deltas.png)
![improvement_deltas](plots/pso_optimize_20260407T143922Z_improvement_deltas.png)
- [`pso_optimize_20260407T143922Z_jump_plot.png`](plots/pso_optimize_20260407T143922Z_jump_plot.png)
![jump_plot](plots/pso_optimize_20260407T143922Z_jump_plot.png)
- [`pso_optimize_20260407T143922Z_progress_by_phase.png`](plots/pso_optimize_20260407T143922Z_progress_by_phase.png)
![progress_by_phase](plots/pso_optimize_20260407T143922Z_progress_by_phase.png)
- [`pso_optimize_20260407T143922Z_raw_fitness.png`](plots/pso_optimize_20260407T143922Z_raw_fitness.png)
![raw_fitness](plots/pso_optimize_20260407T143922Z_raw_fitness.png)
- [`pso_optimize_20260407T143922Z_time_efficiency.png`](plots/pso_optimize_20260407T143922Z_time_efficiency.png)
![time_efficiency](plots/pso_optimize_20260407T143922Z_time_efficiency.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/pso_optimize_20260407T143922Z_events.csv' },
  { file: 'tables/pso_optimize_20260407T143922Z_new_best.csv' },
  { file: 'tables/pso_optimize_20260407T143922Z_phase_summary.csv' },
  { file: 'tables/pso_optimize_20260407T143922Z_run_summary.csv' },
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
