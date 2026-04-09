# Отчёт по оптимизации: ga_optimize_20260409T105027Z

## Метаданные
- метод: `ga`
- датасет: `data/numbers/25_dset_20260409T103515Z/train.json`
- оптимум `(B1, B2)`: `(2000, 2656)`
- objective: `0.7393588161212392`
- curves_per_n: `12`
- границы: `B1[2000.0, 45000.0]`, `B2[2000.0, 900000.0]`, `ratio_max=24.0`

## Ключевые статистики
- `best_eval`: `245`
- `best_eval_fraction`: `0.7753164556962026`
- `eval_per_sec`: `3.896140278484017`
- `evaluation_count`: `316`
- `improvement_percent`: `67.66020132565542`
- `max_plateau_evals`: `82`
- `median_plateau_evals`: `32.5`
- `new_best_count`: `7`
- `new_best_rate`: `0.022151898734177215`
- `p90_plateau_evals`: `74.3`
- `time_to_best_sec`: `64.07994703698205`
- `time_to_first_improvement_sec`: `9.33168351300992`
- `total_runtime_sec`: `81.10601972800214`

## Флаги внимания

| Флаг | Статус | Текущее значение | Порог | Что это значит | Что делать |
|---|---|---:|---:|---|---|
| `b1_hits_boundary` | ⚠️ ВНИМАНИЕ | `0.5158227848101266` | `> 0.10` | Большая доля оценок проходит близко к границам B1. | Расширить диапазон B1, если упор в границу повторяется. |
| `b2_hits_boundary` | ✅ ОК | `0.0` | `> 0.10` | Большая доля оценок проходит близко к границам B2. | Расширить диапазон B2, если упор в границу повторяется. |
| `best_b1_on_boundary` | ⚠️ ВНИМАНИЕ | `2000.0` | `within 2% of log-range [2000.0, 45000.0]` | Лучший найденный B1 лежит на границе диапазона. | Проверить расширенный диапазон B1 вокруг текущей границы. |
| `best_b2_on_boundary` | ✅ ОК | `2656.0` | `within 2% of log-range [2000.0, 900000.0]` | Лучший найденный B2 лежит на границе диапазона. | Проверить расширенный диапазон B2 вокруг текущей границы. |
| `best_ratio_on_boundary` | ✅ ОК | `1.328` | `within 2% of log-range up to ratio_max=24.0` | Лучшее отношение B2/B1 находится у верхней границы ratio_max. | Увеличить ratio_max и перепроверить локальный поиск в новой области. |
| `late_best` | ✅ ОК | `0.7900763377598989` | `> 0.85` | Лучшее решение найдено слишком поздно относительно общего времени. | Усилить ранний поиск или пересмотреть бюджет/инициализацию. |
| `low_improvement` | ✅ ОК | `67.66020132565542` | `< 10%` | Итоговый прирост качества слишком мал. | Сузить границы поиска или изменить параметры метода. |
| `low_signal` | ⚠️ ВНИМАНИЕ | `0.022151898734177215` | `< 0.03` | Слишком низкая плотность новых best-событий (слабый сигнал оптимизации). | Перенастроить exploration и сделать переоценку top-k кандидатов. |
| `plateau_too_long` | ✅ ОК | `0.25949367088607594` | `> 0.50` | Слишком длинное плато: улучшений почти нет на большом участке запуска. | Увеличить exploration или добавить политику рестартов. |
| `ratio_hits_boundary` | ✅ ОК | `0.0759493670886076` | `> 0.10` | Большая доля оценок проходит близко к границе отношения B2/B1. | Увеличить ratio_max, если хорошие точки упираются в ограничение отношения B2/B1. |

## Графики
- [`ga_optimize_20260409T105027Z_b1_b2_trajectory.png`](plots/ga_optimize_20260409T105027Z_b1_b2_trajectory.png)
![b1_b2_trajectory](plots/ga_optimize_20260409T105027Z_b1_b2_trajectory.png)
- [`ga_optimize_20260409T105027Z_b1_ratio_heatmap.png`](plots/ga_optimize_20260409T105027Z_b1_ratio_heatmap.png)
![b1_ratio_heatmap](plots/ga_optimize_20260409T105027Z_b1_ratio_heatmap.png)
- [`ga_optimize_20260409T105027Z_jump_plot.png`](plots/ga_optimize_20260409T105027Z_jump_plot.png)
![jump_plot](plots/ga_optimize_20260409T105027Z_jump_plot.png)
- [`ga_optimize_20260409T105027Z_progress_by_phase.png`](plots/ga_optimize_20260409T105027Z_progress_by_phase.png)
![progress_by_phase](plots/ga_optimize_20260409T105027Z_progress_by_phase.png)
- [`ga_optimize_20260409T105027Z_time_efficiency.png`](plots/ga_optimize_20260409T105027Z_time_efficiency.png)
![time_efficiency](plots/ga_optimize_20260409T105027Z_time_efficiency.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/ga_optimize_20260409T105027Z_events.csv' },
  { file: 'tables/ga_optimize_20260409T105027Z_new_best.csv' },
  { file: 'tables/ga_optimize_20260409T105027Z_phase_summary.csv' },
  { file: 'tables/ga_optimize_20260409T105027Z_run_summary.csv' },
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
