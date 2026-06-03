const state = {
  query: "",
  county: "",
  audience: "",
  category: "",
  currentOnly: false,
  group: "recommended",
  records: []
};

const labels = {
  "official-entry": "官方入口",
  "source-dated": "來源有日期",
  checked: "已檢查",
  "needs-review": "需再確認"
};

const groupLabels = {
  recommended: "建議先看",
  government: "政府／公所資源",
  foundation: "民間基金會",
  contact: "建議先電話確認",
  all: "全部結果"
};

const priorityNames = [
  "低收入戶及中低收入戶",
  "115年度低收入戶、中低收入戶資格審核標準",
  "1957福利諮詢專線",
  "1966長照服務專線與長照2.0",
  "萬海急難救助申請",
  "富邦慈善急難救助個案補助",
  "各級政府辦理保險對象健保費補助項目",
  "全國身心障礙福利服務入口網"
];

const els = {
  query: document.querySelector("#queryInput"),
  county: document.querySelector("#countyFilter"),
  audience: document.querySelector("#audienceFilter"),
  category: document.querySelector("#categoryFilter"),
  currentOnly: document.querySelector("#currentOnlyFilter"),
  results: document.querySelector("#results"),
  resultTitle: document.querySelector("#resultTitle"),
  resultCount: document.querySelector("#resultCount"),
  activeFilters: document.querySelector("#activeFilters"),
  resultsPanel: document.querySelector(".results-panel"),
  clearButton: document.querySelector("#clearButton"),
  applyFilterButton: document.querySelector("#applyFilterButton"),
  recordTotal: document.querySelector("#recordTotal"),
  countyTotal: document.querySelector("#countyTotal"),
  foundationProgramTotal: document.querySelector("#foundationProgramTotal"),
  currentYearTotal: document.querySelector("#currentYearTotal")
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
  optionList(els.county, uniqueSorted(records.map((record) => record.county)), "不限縣市");
  optionList(els.audience, uniqueSorted(records.flatMap((record) => record.audiences || [])), "不限身分");
  optionList(els.category, uniqueSorted(records.flatMap((record) => record.serviceCategories || [])), "不限類型");
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
    ...(record.documents || []),
    record.contact?.phone,
    record.contact?.email,
    record.contact?.address
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function queryTerms() {
  return state.query
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean);
}

function matchesQuery(record) {
  const terms = queryTerms();
  if (!terms.length) return true;
  const text = searchableText(record);
  return terms.every((term) => text.includes(term));
}

function matchesBaseFilters(record) {
  if (!matchesQuery(record)) return false;
  if (state.county && record.county !== state.county) return false;
  if (state.audience && !(record.audiences || []).includes(state.audience)) return false;
  if (state.category && !(record.serviceCategories || []).includes(state.category)) return false;
  if (state.currentOnly && record.freshness?.confidence !== "source-dated") return false;
  return true;
}

function isFoundationResource(record) {
  return record.source?.type === "foundation-program-page" || String(record.id || "").startsWith("sfaa-foundation-");
}

function isGovernmentResource(record) {
  const provider = `${record.provider || ""} ${record.source?.type || ""}`;
  return /衛生福利部|勞動部|政府|社會局|社家署|健保署|公所|官方|official|open-data/.test(provider) && !isFoundationResource(record);
}

function needsContact(record) {
  const text = [
    record.eligibility,
    ...(record.howToApply || []),
    record.freshness?.notes,
    record.source?.type
  ]
    .filter(Boolean)
    .join(" ");
  return /電話|洽詢|確認|需再|contact|foundation-program-page/.test(text);
}

function groupMatches(record) {
  if (state.group === "all") return true;
  if (state.group === "government") return isGovernmentResource(record);
  if (state.group === "foundation") return isFoundationResource(record);
  if (state.group === "contact") return needsContact(record);
  if (state.group === "recommended") return rankRecord(record) > 0 || priorityNames.includes(record.name);
  return true;
}

function rankRecord(record) {
  const terms = queryTerms();
  const name = String(record.name || "").toLowerCase();
  const provider = String(record.provider || "").toLowerCase();
  const tags = (record.needTags || []).join(" ").toLowerCase();
  const categories = (record.serviceCategories || []).join(" ").toLowerCase();
  const audiences = (record.audiences || []).join(" ").toLowerCase();
  const summary = String(record.summary || "").toLowerCase();
  let score = priorityNames.includes(record.name) ? 35 : 0;

  terms.forEach((term) => {
    if (name.includes(term)) score += 60;
    if (tags.includes(term)) score += 38;
    if (categories.includes(term)) score += 28;
    if (audiences.includes(term)) score += 22;
    if (summary.includes(term)) score += 12;
    if (provider.includes(term)) score += 8;
  });
  if (record.source?.type === "foundation-program-page") score += 8;
  if (record.freshness?.confidence === "source-dated") score += 5;
  if (record.source?.type === "official-program" || record.source?.type === "official-portal") score += 4;
  return score;
}

function statusText(status) {
  return labels[status] || "已收錄";
}

function needMeta(record) {
  const text = searchableText(record);
  if (/急難|救助|突發/.test(text)) return { tone: "urgent", mark: "急", label: "急難" };
  if (/低收入|中低收入|生活扶助|社會救助/.test(text)) return { tone: "income", mark: "低", label: "生活" };
  if (/醫療|健保|保費/.test(text)) return { tone: "medical", mark: "醫", label: "醫療" };
  if (/長照|居家|喘息|失智|照顧/.test(text)) return { tone: "care", mark: "照", label: "照顧" };
  if (/身心障礙|身障|輔具/.test(text)) return { tone: "disability", mark: "身", label: "身障" };
  if (/兒童|兒少|少年|家庭|寄養/.test(text)) return { tone: "child", mark: "兒", label: "兒少" };
  if (/獎學|助學|清寒|學生|就學/.test(text)) return { tone: "school", mark: "學", label: "就學" };
  if (isGovernmentResource(record)) return { tone: "government", mark: "政", label: "政府" };
  return { tone: "local", mark: "資", label: "資源" };
}

function assistanceText(record) {
  const categories = record.serviceCategories || [];
  const preferred = categories.find((item) => !["民間社福資源", "社福基金會", "其他", "方案級民間資源"].includes(item));
  return preferred || categories[0] || "依來源頁公告";
}

function firstStep(record) {
  const steps = record.howToApply || [];
  return steps[0] || "先開啟來源頁，確認資格、名額、文件與受理狀態。";
}

function documentHint(record) {
  const docs = record.documents || [];
  return docs.slice(0, 2).join("、") || "依來源頁公告";
}

function contactText(record) {
  const parts = [
    record.contact?.phone ? `電話：${record.contact.phone}` : "",
    record.contact?.email ? `Email：${record.contact.email}` : "",
    record.contact?.address ? `地址：${record.contact.address}` : ""
  ].filter(Boolean);
  return parts.length ? parts.join(" / ") : "請由來源頁確認最新聯絡方式。";
}

function listItems(items, ordered = false) {
  const tag = ordered ? "ol" : "ul";
  if (!items || !items.length) return "<p>依來源頁公告。</p>";
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
  const meta = needMeta(record);
  return `
    <article class="resource-card tone-${escapeHtml(meta.tone)}">
      <div class="card-top">
        <div class="card-mark" aria-hidden="true">${escapeHtml(meta.mark)}</div>
        <div>
          <p class="card-kind">${escapeHtml(meta.label)}</p>
          <h3>${escapeHtml(record.name)}</h3>
        </div>
        <span class="status-pill ${escapeHtml(confidence)}">${statusText(confidence)}</span>
      </div>

      <p class="summary">${escapeHtml(record.summary)}</p>

      <div class="meta-line">
        <span class="tag">${escapeHtml(record.county || "全國")}</span>
        ${(record.audiences || []).slice(0, 3).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
        ${(record.serviceCategories || []).slice(0, 2).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
      </div>

      <div class="quick-answer-grid">
        <div>
          <span>適合誰</span>
          <p>${escapeHtml((record.audiences || []).slice(0, 3).join("、") || record.eligibility || "依來源頁公告")}</p>
        </div>
        <div>
          <span>可以協助</span>
          <p>${escapeHtml(assistanceText(record))}</p>
        </div>
        <div>
          <span>下一步</span>
          <p>${escapeHtml(firstStep(record))}</p>
        </div>
        <div>
          <span>要準備</span>
          <p>${escapeHtml(documentHint(record))}</p>
        </div>
      </div>

      <details class="details-block">
        <summary>展開完整申請提醒</summary>
        <div class="details-grid">
          <div>
            <h4>誰適合先查</h4>
            <p>${escapeHtml(record.eligibility || "依來源頁或服務單位公告。")}</p>
          </div>
          <div>
            <h4>怎麼辦</h4>
            ${listItems(record.howToApply, true)}
          </div>
          <div>
            <h4>可能需要文件</h4>
            ${listItems(record.documents)}
          </div>
          <div>
            <h4>聯絡資訊</h4>
            <p>${escapeHtml(contactText(record))}</p>
          </div>
        </div>
      </details>

      <div class="card-actions">
        ${record.source?.url ? `<a class="primary-link" href="${escapeHtml(record.source.url)}" target="_blank" rel="noopener">查看申請/來源</a>` : ""}
        ${record.contact?.website ? `<a href="${escapeHtml(record.contact.website)}" target="_blank" rel="noopener">單位網站</a>` : ""}
      </div>
    </article>
  `;
}

function currentFilteredRecords() {
  return state.records
    .filter(matchesBaseFilters)
    .filter(groupMatches)
    .sort((a, b) => rankRecord(b) - rankRecord(a) || String(a.name).localeCompare(String(b.name), "zh-Hant"));
}

function renderActiveFilters() {
  const filters = [
    state.query ? `關鍵字：${state.query}` : "",
    state.county ? `縣市：${state.county}` : "",
    state.audience ? `身分／對象：${state.audience}` : "",
    state.category ? `協助類型：${state.category}` : "",
    state.currentOnly ? "只看來源有標示日期" : "",
    `目前分組：${groupLabels[state.group]}`
  ].filter(Boolean);

  els.activeFilters.innerHTML = filters.map((filter) => `<span class="filter-chip">${escapeHtml(filter)}</span>`).join("");
}

function render() {
  const baseCount = state.records.filter(matchesBaseFilters).length;
  const filtered = currentFilteredRecords();
  const visible = state.group === "all" ? filtered : filtered.slice(0, 36);

  els.resultTitle.textContent = groupLabels[state.group] || "查詢結果";
  els.resultCount.textContent =
    state.group === "all"
      ? `找到 ${filtered.length} 筆可參考資源`
      : `找到 ${baseCount} 筆可參考資源，先顯示 ${visible.length} 筆`;
  renderActiveFilters();
  syncGroupButtons();
  syncShortcutButtons();

  if (!visible.length) {
    els.results.innerHTML = `<div class="empty-state"><p>目前沒有找到符合條件的資源。可以改用比較短的說法，例如「低收入戶」、「急難」、「長照」，或先取消縣市、身分、日期限制。</p></div>`;
    return;
  }

  const moreNote =
    filtered.length > visible.length
      ? `<div class="more-note">這組還有 ${filtered.length - visible.length} 筆。可以切到「全部結果」，或用縣市、身分、關鍵字再縮小。</div>`
      : "";
  els.results.innerHTML = visible.map(renderRecord).join("") + moreNote;
}

function updateStats(records) {
  els.recordTotal.textContent = records.length;
  els.countyTotal.textContent = uniqueSorted(records.map((record) => record.county).filter((county) => county && county !== "全國")).length;
  els.foundationProgramTotal.textContent = records.filter((record) => record.source?.type === "foundation-program-page").length;
  els.currentYearTotal.textContent = records.filter((record) => record.freshness?.confidence === "source-dated").length;
}

function selectHasValue(select, value) {
  return [...select.options].some((option) => option.value === value);
}

function setSelectValue(select, value) {
  select.value = value && selectHasValue(select, value) ? value : "";
}

function syncControls() {
  els.query.value = state.query;
  setSelectValue(els.county, state.county);
  setSelectValue(els.audience, state.audience);
  setSelectValue(els.category, state.category);
  els.currentOnly.checked = state.currentOnly;
}

function scrollToResults() {
  window.requestAnimationFrame(() => {
    els.resultsPanel?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function syncShortcutButtons() {
  document.querySelectorAll("[data-need]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.need === state.query);
  });
  document.querySelectorAll("[data-audience]").forEach((button) => {
    const audience = button.dataset.audience || "";
    button.classList.toggle("is-active", Boolean(audience && state.audience === audience && state.query.includes(audience)));
  });
}

function applyShortcut({ query, audience = "", scroll = true }) {
  state.query = query;
  state.audience = audience;
  state.category = "";
  state.currentOnly = false;
  state.group = "recommended";
  syncControls();
  render();
  if (scroll) scrollToResults();
}

function setQuery(query, options = {}) {
  state.query = query;
  state.group = "recommended";
  syncControls();
  render();
  if (options.scroll) scrollToResults();
}

function setAudience(audience) {
  applyShortcut({ query: audience, audience });
}

function resetFilters() {
  state.query = "";
  state.county = "";
  state.audience = "";
  state.category = "";
  state.currentOnly = false;
  state.group = "recommended";
  syncControls();
  render();
}

function syncGroupButtons() {
  document.querySelectorAll("[data-group]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.group === state.group);
  });
}

function bindEvents() {
  els.query.addEventListener("input", (event) => {
    state.query = event.target.value;
    state.group = state.query ? "recommended" : state.group;
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
  els.currentOnly.addEventListener("change", (event) => {
    state.currentOnly = event.target.checked;
    render();
  });
  els.clearButton.addEventListener("click", resetFilters);
  els.applyFilterButton.addEventListener("click", () => setQuery("申請", { scroll: true }));

  document.querySelectorAll("[data-need]").forEach((button) => {
    button.addEventListener("click", () => applyShortcut({ query: button.dataset.need || "" }));
  });
  document.querySelectorAll("[data-audience]").forEach((button) => {
    button.addEventListener("click", () => setAudience(button.dataset.audience || ""));
  });
  document.querySelectorAll("[data-group]").forEach((button) => {
    button.addEventListener("click", () => {
      state.group = button.dataset.group || "recommended";
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
    els.resultCount.textContent = "資料載入失敗";
    els.results.innerHTML = `<div class="empty-state"><p>無法讀取 data/resources.json，請先確認資料檔已產生並重新整理頁面。</p></div>`;
    console.error(error);
  }
}

init();
