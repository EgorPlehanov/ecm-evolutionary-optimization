# Отчёт по оптимизации: de_optimize_20260407T150158Z

## Метаданные
- метод: `de`
- датасет: `data/numbers/20_dset_20260407T150118Z/train.json`
- оптимум `(B1, B2)`: `(1473, 1473)`
- objective: `0.6376503233332187`
- curves_per_n: `12`
- границы: `B1[1000.0, 12000.0]`, `B2[1000.0, 144000.0]`, `ratio_max=12.0`

## Ключевые статистики
- `best_eval`: `41`
- `best_eval_fraction`: `0.22777777777777777`
- `eval_per_sec`: `4.530871226684651`
- `evaluation_count`: `180`
- `improvement_percent`: `3.0925063119218903`
- `max_plateau_evals`: `139`
- `median_plateau_evals`: `19.0`
- `new_best_count`: `3`
- `new_best_rate`: `0.016666666666666666`
- `p90_plateau_evals`: `104.80000000000003`
- `time_to_best_sec`: `10.059171120054089`
- `time_to_first_improvement_sec`: `0.21777722402475774`
- `total_runtime_sec`: `39.72745880304137`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `late_best` | ✅ ОК | `0.2532044944008349` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ⚠️ ВНИМАНИЕ | `3.0925063119218903` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.016666666666666666` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ⚠️ ВНИМАНИЕ | `0.7722222222222223` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |

## Графики
- [`de_optimize_20260407T150158Z_b1_b2_trajectory.png`](plots/de_optimize_20260407T150158Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/de_optimize_20260407T150158Z_b1_b2_trajectory.png)
- [`de_optimize_20260407T150158Z_b1_ratio_heatmap.png`](plots/de_optimize_20260407T150158Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/de_optimize_20260407T150158Z_b1_ratio_heatmap.png)
- [`de_optimize_20260407T150158Z_convergence.png`](plots/de_optimize_20260407T150158Z_convergence.png)
![convergence](plots/de_optimize_20260407T150158Z_convergence.png)
- [`de_optimize_20260407T150158Z_improvement_deltas.png`](plots/de_optimize_20260407T150158Z_improvement_deltas.png)
![improvement_deltas](plots/de_optimize_20260407T150158Z_improvement_deltas.png)
- [`de_optimize_20260407T150158Z_jump_plot.png`](plots/de_optimize_20260407T150158Z_jump_plot.png)
![jump_plot](plots/de_optimize_20260407T150158Z_jump_plot.png)
- [`de_optimize_20260407T150158Z_progress_by_phase.png`](plots/de_optimize_20260407T150158Z_progress_by_phase.png)
![progress_by_phase](plots/de_optimize_20260407T150158Z_progress_by_phase.png)
- [`de_optimize_20260407T150158Z_raw_fitness.png`](plots/de_optimize_20260407T150158Z_raw_fitness.png)
![raw_fitness](plots/de_optimize_20260407T150158Z_raw_fitness.png)
- [`de_optimize_20260407T150158Z_time_efficiency.png`](plots/de_optimize_20260407T150158Z_time_efficiency.png)
![time_efficiency](plots/de_optimize_20260407T150158Z_time_efficiency.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/de_optimize_20260407T150158Z_events.csv' },
  { file: 'tables/de_optimize_20260407T150158Z_new_best.csv' },
  { file: 'tables/de_optimize_20260407T150158Z_phase_summary.csv' },
  { file: 'tables/de_optimize_20260407T150158Z_run_summary.csv' },
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
