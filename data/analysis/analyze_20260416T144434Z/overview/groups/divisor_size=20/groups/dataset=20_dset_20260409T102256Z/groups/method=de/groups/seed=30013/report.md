# Отчёт анализа: `seed=30013`

## Навигация
- Путь: /[overview](../../../../../../../../report.md)/[divisor_size=20](../../../../../../report.md)/[dataset=20_dset_20260409T102256Z](../../../../report.md)/[method=de](../../report.md)/seed=30013
- Нижних уровней группировки нет.

## Краткая сводка
- запусков в области: **3**
- медиана final objective: **0.638592**
- IQR objective: **0.019749**
- доля успеха (`objective <= 0.678229`): **100.00%**
- медианное время выполнения: **57.490 сек**
- медианный прирост по validation: **37.274%**

## Графики
- [final_objective_by_seed.png](plots/final_objective_by_seed.png)
![final_objective_by_seed](plots/final_objective_by_seed.png)
- [validation_gain_by_seed.png](plots/validation_gain_by_seed.png)
![validation_gain_by_seed](plots/validation_gain_by_seed.png)

## Таблицы

<div id="tables-container"></div>

<script>
const tables = [
  { file: 'tables/runs.csv' },
  { file: 'tables/summary.csv' },
  { file: 'tables/compare_by_seed.csv' },
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

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isPathLike(value) {
  if (typeof value !== 'string') return false;
  const v = normalizeDateInput(value);
  if (!v) return false;
  const pathOnly = v.split('?')[0].split('#')[0];
  if (!pathOnly || /^\d+(\.\d+)?$/.test(pathOnly)) return false;
  return /^(?:\.{1,2}\/|\/|[A-Za-z0-9_.\-/]+\.[A-Za-z0-9]+)$/.test(pathOnly);
}

function parseLinkValue(value) {
  const v = normalizeDateInput(value);
  const [withoutHash, hashPart] = String(v).split('#', 2);
  const [pathPart, queryPart] = withoutHash.split('?', 2);
  const params = new URLSearchParams(queryPart || '');
  const displayName = params.get('display_name');
  params.delete('display_name');
  return {
    path: pathPart || '',
    displayName,
    query: params.toString(),
    hash: hashPart || '',
  };
}

function toProjectRootHref(pathValue) {
  const v = normalizeDateInput(pathValue);
  if (!v) return v;
  if (/^[A-Za-z][A-Za-z\d+.-]*:/.test(v) || v.startsWith('//')) return v;
  const normalized = v.replace(/^\.{1,2}\//, '').replace(/^\/+/, '');
  return `/${normalized}`;
}

function renderBodyCell(cell, columnName) {
  const raw = normalizeDateInput(cell);
  if (isPathLike(raw)) {
    const parsed = parseLinkValue(raw);
    const hrefBase = toProjectRootHref(parsed.path);
    const query = parsed.query ? `?${parsed.query}` : '';
    const hash = parsed.hash ? `#${parsed.hash}` : '';
    const href = `${hrefBase}${query}${hash}`;
    const label = parsed.displayName || raw;
    return `<td><a href="${encodeURI(href)}">${escapeHtml(label)}</a></td>`;
  }
  let content = formatDateTime(cell);
  content = roundNumber(content);
  return `<td>${escapeHtml(content)}</td>`;
}

async function createTable(config) {
  const resp = await fetch(config.file);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const text = await resp.text();
  const rows = text.trim().split(/\r?\n/).map(row => row.split(','));

  let html = '<table border="1" cellpadding="5">';
  rows.forEach((row, i) => {
    html += '<tr>';
    row.forEach((cell, columnIndex) => {
      const columnName = rows[0][columnIndex] || '';
      html += i === 0 ? `<th>${escapeHtml(cell)}</th>` : renderBodyCell(cell, columnName);
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
