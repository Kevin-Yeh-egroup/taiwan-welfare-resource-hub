const state = {
  query: "",
  county: "",
  audience: "",
  category: "",
  freshness: "",
  records: []
};

const labels = {
  "official-entry": "官方入口",
  "source-dated": "來源有日期",
  checked: "已檢查",
  "needs-review": "需人工確認"
};

const els = {
  query: document.querySelector("#queryInput"),
  county: document.querySelector("#countyFilter"),
  audience: document.querySelector("#audienceFilter"),
  category: document.querySelector("#categoryFilter"),
  freshness: document.querySelector("#freshnessFilter"),
  results: document.querySelector("#results"),
  resultCount: document.querySelector("#resultCount"),
  activeFilters: document.querySelector("#activeFilters"),
  clearButton: document.querySelector("#clearButton"),
  recordTotal: document.querySelector("#recordTotal"),
  countyTotal: document.querySelector("#countyTotal"),
  reviewTotal: document.querySelector("#reviewTotal")
};

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-Hant"));
}

function optionList(select, values, allLabel) {
  select.innerHTML = "";
  const all = document.createElement("option");
  all.value = "";
  all.textContent = allLabel;
  select.appendChild(all);
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function setupFilters(records) {
  optionList(els.county, uniqueSorted(records.map((record) => record.county)), "全部縣市");
  optionList(els.audience, uniqueSorted(records.flatMap((record) => record.audiences || [])), "全部對象");
  optionList(els.category, uniqueSorted(records.flatMap((record) => record.serviceCategories || [])), "全部服務");
}

function searchableText(record) {
  return [
    record.name,
    record.summary,
    record.provider,
    record.jurisdiction,
    record.county,
    ...(record.districts || []),
    ...(record.audiences || []),
    ...(record.serviceCategories || []),
    ...(record.needTags || []),
    record.eligibility,
    ...(record.howToApply || []),
    record.contact?.phone,
    record.contact?.address
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function matches(record) {
  const query = state.query.trim().toLowerCase();
  if (query && !searchableText(record).includes(query)) return false;
  if (state.county && record.county !== state.county) return false;
  if (state.audience && !(record.audiences || []).includes(state.audience)) return false;
  if (state.category && !(record.serviceCategories || []).includes(state.category)) return false;
  if (state.freshness && record.freshness?.confidence !== state.freshness) return false;
  return true;
}

function statusText(status) {
  return labels[status] || "待檢查";
}

function listItems(items, ordered = false) {
  const tag = ordered ? "ol" : "ul";
  if (!items || !items.length) return "<p>尚未整理</p>";
  return `<${tag}>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</${tag}>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderRecord(record) {
  const confidence = record.freshness?.confidence || "needs-review";
  const contactParts = [
    record.contact?.phone ? `電話：${record.contact.phone}` : "",
    record.contact?.email ? `Email：${record.contact.email}` : "",
    record.contact?.address ? `地址：${record.contact.address}` : ""
  ].filter(Boolean);

  return `
    <article class="resource-card">
      <header>
        <div>
          <h2>${escapeHtml(record.name)}</h2>
          <p class="summary">${escapeHtml(record.summary)}</p>
        </div>
        <span class="status-pill ${escapeHtml(confidence)}">${statusText(confidence)}</span>
      </header>

      <div class="meta-line">
        <span class="tag">${escapeHtml(record.county)}</span>
        ${(record.audiences || []).slice(0, 4).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
        ${(record.serviceCategories || []).slice(0, 3).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
      </div>

      <div class="card-grid">
        <div class="info-block">
          <h3>適合誰</h3>
          <p>${escapeHtml(record.eligibility || "需依個別辦法確認。")}</p>
        </div>
        <div class="info-block">
          <h3>怎麼使用</h3>
          ${listItems(record.howToApply, true)}
        </div>
        <div class="info-block">
          <h3>先準備</h3>
          ${listItems(record.documents)}
        </div>
        <div class="info-block">
          <h3>聯絡資訊</h3>
          <p>${contactParts.length ? escapeHtml(contactParts.join(" / ")) : "依來源頁面"}</p>
        </div>
      </div>

      <div class="card-actions">
        ${record.contact?.website ? `<a href="${escapeHtml(record.contact.website)}" target="_blank" rel="noopener">開啟網站</a>` : ""}
        ${record.source?.url ? `<a href="${escapeHtml(record.source.url)}" target="_blank" rel="noopener">查看來源</a>` : ""}
      </div>
    </article>
  `;
}

function renderActiveFilters() {
  const filters = [
    state.query ? `關鍵字：${state.query}` : "",
    state.county ? `縣市：${state.county}` : "",
    state.audience ? `對象：${state.audience}` : "",
    state.category ? `服務：${state.category}` : "",
    state.freshness ? `狀態：${statusText(state.freshness)}` : ""
  ].filter(Boolean);

  els.activeFilters.innerHTML = filters.map((filter) => `<span class="filter-chip">${escapeHtml(filter)}</span>`).join("");
}

function render() {
  const filtered = state.records.filter(matches);
  els.resultCount.textContent = `找到 ${filtered.length} 筆資源`;
  renderActiveFilters();
  if (!filtered.length) {
    els.results.innerHTML = `<div class="empty-state"><p>目前沒有符合條件的資源。請放寬縣市、對象或關鍵字。</p></div>`;
    return;
  }
  els.results.innerHTML = filtered.map(renderRecord).join("");
}

function updateStats(records) {
  els.recordTotal.textContent = records.length;
  els.countyTotal.textContent = uniqueSorted(records.map((record) => record.county).filter((county) => county !== "全國")).length;
  els.reviewTotal.textContent = records.filter((record) => record.freshness?.confidence === "needs-review").length;
}

function bindEvents() {
  els.query.addEventListener("input", (event) => {
    state.query = event.target.value;
    render();
  });
  els.county.addEventListener("change", (event) => {
    state.county = event.target.value;
    render();
  });
  els.audience.addEventListener("change", (event) => {
    state.audience = event.target.value;
    render();
  });
  els.category.addEventListener("change", (event) => {
    state.category = event.target.value;
    render();
  });
  els.freshness.addEventListener("change", (event) => {
    state.freshness = event.target.value;
    render();
  });
  els.clearButton.addEventListener("click", () => {
    state.query = "";
    state.county = "";
    state.audience = "";
    state.category = "";
    state.freshness = "";
    els.query.value = "";
    els.county.value = "";
    els.audience.value = "";
    els.category.value = "";
    els.freshness.value = "";
    render();
  });
  document.querySelectorAll("[data-need]").forEach((button) => {
    button.addEventListener("click", () => {
      state.query = button.dataset.need || "";
      els.query.value = state.query;
      render();
    });
  });
}

async function init() {
  try {
    const response = await fetch("data/resources.json", { cache: "no-store" });
    const data = await response.json();
    state.records = data.records || [];
    setupFilters(state.records);
    updateStats(state.records);
    bindEvents();
    render();
  } catch (error) {
    els.resultCount.textContent = "資料讀取失敗";
    els.results.innerHTML = `<div class="empty-state"><p>無法讀取 data/resources.json，請確認本機伺服器是從 repo 根目錄啟動。</p></div>`;
    console.error(error);
  }
}

init();
