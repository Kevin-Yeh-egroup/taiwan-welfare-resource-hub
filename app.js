const state = {
  query: "",
  county: "",
  audience: "",
  category: "",
  currentOnly: false,
  group: "recommended",
  records: [],
  coverage: null,
  sourceHealth: null,
  batchGate: null
};

const labels = {
  "official-entry": "官方入口",
  "official-report": "官方報告",
  "official-statistical-brief": "官方統計",
  "source-dated": "來源有日期",
  "source-dated-list": "日期清單",
  "needs-local-confirmation": "需向公所確認",
  checked: "已檢查",
  "needs-review": "需再確認"
};

const groupLabels = {
  recommended: "建議先看",
  central: "公部門中央資源",
  local: "公部門地方資源",
  private: "民間資源",
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
  applyFilterButton: document.querySelector("#applyFilterButton"),
  centralResourceTotal: document.querySelector("#centralResourceTotal"),
  localResourceTotal: document.querySelector("#localResourceTotal"),
  privateResourceTotal: document.querySelector("#privateResourceTotal"),
  coverageSummary: document.querySelector("#coverageSummary"),
  hardWarningTotal: document.querySelector("#hardWarningTotal"),
  transientWarningTotal: document.querySelector("#transientWarningTotal"),
  batchGateMode: document.querySelector("#batchGateMode"),
  batchGateList: document.querySelector("#batchGateList"),
  guidedPath: document.querySelector("#guidedPath"),
  decisionAid: document.querySelector("#decisionAid")
};

const hiddenDisplayValues = new Set(["none"]);

function displayValues(values) {
  return (values || []).filter((value) => value && !hiddenDisplayValues.has(String(value).trim().toLowerCase()));
}

function uniqueSorted(values) {
  return [...new Set(displayValues(values))].sort((a, b) => a.localeCompare(b, "zh-Hant"));
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
    ...(record.applicationConditions || []).flatMap((item) => [item.label, item.requirement, item.note, item.sourceDate]),
    record.taiwanProvinceNote?.title,
    record.taiwanProvinceNote?.text,
    ...(record.taiwanProvinceNote?.areas || []),
    ...(record.incomeStandardGroups || []).flatMap((group) => [
      group.label,
      group.sourceDate,
      ...(group.items || []).flatMap((item) => [item.region, item.income, item.movableAssets, item.realEstate, item.note])
    ]),
    ...(record.relatedPrograms || []).flatMap((program) => [
      program.name,
      program.summary,
      ...(program.audiences || []),
      ...(program.serviceCategories || []),
      ...(program.needTags || []),
      program.eligibility
    ]),
    ...(record.benefitItems || []).flatMap((item) => [item.label, item.amount, item.unit, item.note, item.sourceDate]),
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

const querySynonyms = [
  ["台灣", "臺灣"],
  ["台北", "臺北"],
  ["台中", "臺中"],
  ["台南", "臺南"],
  ["台東", "臺東"],
  ["低收", "低收入戶"],
  ["中低收", "中低收入戶"],
  ["身障", "身心障礙"],
  ["殘障", "身心障礙", "身障"],
  ["身障津貼", "身障生活補助", "身心障礙者生活補助"],
  ["老人津貼", "老人生活津貼"],
  ["老人生活補助", "老人生活津貼"],
  ["老人生活津貼", "中低收入老人生活津貼"],
  ["長輩補助", "老人生活津貼", "中低收入老人生活津貼"],
  ["公所", "鄉鎮市公所", "區公所"],
  ["金門連江", "福建省", "金門", "連江"],
  ["租屋", "租金補貼", "房租", "房租補助", "住宅補貼"],
  ["房租", "租金補貼", "租屋補助"],
  ["照顧者", "家庭照顧者", "喘息", "長照"],
  ["顧老人", "家庭照顧者", "長照", "1966"],
  ["輔具", "生活輔具", "輔具補助", "身心障礙"],
  ["復康巴士", "交通接送", "長照交通", "身障交通"],
  ["小孩", "兒童", "兒少", "兒少家庭"],
  ["小朋友", "兒童", "兒少", "兒少家庭"],
  ["單親", "特殊境遇家庭", "家庭支持"],
  ["學費", "學雜費減免", "助學金", "清寒獎學金"],
  ["助學", "助學金", "學雜費減免", "低收入戶學生"],
  ["繳不起健保", "健保費補助", "保費補助"],
  ["不知道找誰", "1957", "社會福利服務中心", "社福中心"],
];

function queryTermGroups() {
  return queryTerms().map((term) => {
    const variants = new Set([term]);
    querySynonyms.forEach((group) => {
      if (group.includes(term)) {
        group.forEach((variant) => variants.add(variant.toLowerCase()));
      }
    });
    return [...variants];
  });
}

function matchesQuery(record) {
  const termGroups = queryTermGroups();
  if (!termGroups.length) return true;
  const text = searchableText(record);
  return termGroups.every((group) => group.some((term) => text.includes(term)));
}

function matchesBaseFilters(record) {
  if (!matchesQuery(record)) return false;
  if (state.county && record.county !== state.county && !isPublicCentralResource(record)) return false;
  if (state.audience && !(record.audiences || []).includes(state.audience)) return false;
  if (state.category && !(record.serviceCategories || []).includes(state.category)) return false;
  if (state.currentOnly && !hasDatedSource(record)) return false;
  return true;
}

function hasDatedSource(record) {
  const confidence = record.freshness?.confidence || "";
  return Boolean(record.freshness?.sourceUpdatedAt) || ["source-dated", "source-dated-list", "checked", "official-report", "official-statistical-brief"].includes(confidence);
}

function parentFoundationId(record) {
  if (record.parentFoundationId) return record.parentFoundationId;
  const match = String(record.id || "").match(/^foundation-program-([a-z]\d{4})-/i);
  return match ? `sfaa-foundation-${match[1]}` : "";
}

function hydrateRelatedPrograms(records) {
  const byId = new Map(records.map((record) => [record.id, record]));
  records.forEach((record) => {
    record.relatedPrograms = [];
  });
  records.forEach((record) => {
    if (record.source?.type !== "foundation-program-page") return;
    const parentId = parentFoundationId(record);
    const parent = byId.get(parentId);
    if (!parent) return;
    record.parentFoundationId = parentId;
    parent.relatedPrograms.push(record);
  });
  records.forEach((record) => {
    if (record.relatedPrograms?.length) {
      record.relatedPrograms.sort((a, b) => String(a.name).localeCompare(String(b.name), "zh-Hant"));
    }
  });
  return records;
}

function isFoundationResource(record) {
  return record.source?.type === "foundation-program-page" || String(record.id || "").startsWith("sfaa-foundation-");
}

function isPrivateResource(record) {
  return isFoundationResource(record);
}

function isPublicCentralResource(record) {
  if (isPrivateResource(record)) return false;
  const sourceType = record.source?.type || "";
  const scope = `${record.county || ""} ${record.jurisdiction || ""}`;
  if (/全國|全省|中央/.test(scope)) return true;
  return /official-(portal|hotline|program|annual-standard|faq|service-network)/.test(sourceType);
}

function isPublicLocalResource(record) {
  if (isPrivateResource(record) || isPublicCentralResource(record)) return false;
  const sourceType = record.source?.type || "";
  const provider = `${record.provider || ""} ${sourceType}`;
  return /政府|社會局|社會處|衛生局|公所|open-data|official-map|official-local/.test(provider);
}

function isGovernmentResource(record) {
  const provider = `${record.provider || ""} ${record.source?.type || ""}`;
  return /衛生福利部|勞動部|政府|社會局|社家署|健保署|公所|官方|official|open-data/.test(provider) && !isPrivateResource(record);
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
  if (state.group === "central") return isPublicCentralResource(record);
  if (state.group === "local") return isPublicLocalResource(record);
  if (state.group === "private") return isPrivateResource(record);
  if (state.group === "contact") return needsContact(record);
  if (state.group === "recommended") return rankRecord(record) > 0 || priorityNames.includes(record.name);
  return true;
}

function rankRecord(record) {
  const terms = queryTermGroups().flat();
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
  if (record.relatedPrograms?.length) score += 10;
  if (record.freshness?.confidence === "source-dated") score += 5;
  if (record.source?.type === "official-program" || record.source?.type === "official-portal") score += 4;
  return score;
}

function statusText(status) {
  return labels[status] || "已收錄";
}

function sourceConfidence(record) {
  const confidence = record.freshness?.confidence || "needs-review";
  const sourceType = record.source?.type || "";
  if (confidence === "needs-local-confirmation") {
    return {
      level: "confirm",
      label: "需向公所確認",
      note: "找到官方入口或法規線索，但最新受理細節仍要打給戶籍地公所或主管機關。"
    };
  }
  if (/cross-check/.test(sourceType)) {
    return {
      level: "confirm",
      label: "交叉查核",
      note: "來源可用，但年度金額、文件或細節仍以送件窗口核定為準。"
    };
  }
  if (hasDatedSource(record)) {
    return {
      level: "strong",
      label: "來源較完整",
      note: "來源頁有日期、更新時間或已完成年度查核。"
    };
  }
  if (isGovernmentResource(record)) {
    return {
      level: "entry",
      label: "官方入口",
      note: "可先用來找到主管機關，再確認今年度資格與申請文件。"
    };
  }
  return {
    level: "review",
    label: "需再確認",
    note: "民間方案與名額可能變動，申請前請電話確認。"
  };
}

function renderSourceConfidence(record) {
  const info = sourceConfidence(record);
  const checked = record.freshness?.lastChecked ? `查核：${record.freshness.lastChecked}` : "查核日未標示";
  return `
    <div class="source-confidence source-${escapeHtml(info.level)}">
      <strong>${escapeHtml(info.label)}</strong>
      <span>${escapeHtml(info.note)}</span>
      <small>${escapeHtml(checked)}</small>
    </div>
  `;
}

function matchedTerms(record) {
  const groups = queryTermGroups();
  if (!groups.length) return [];
  const text = searchableText(record);
  return [...new Set(groups.map((group) => group.find((term) => text.includes(term))).filter(Boolean))].slice(0, 4);
}

function renderMatchReasons(record) {
  const matches = matchedTerms(record);
  const reasons = [
    ...matches.map((term) => `符合「${term}」`),
    state.county && record.county === state.county ? `縣市是${state.county}` : "",
    state.audience && (record.audiences || []).includes(state.audience) ? `身分含${state.audience}` : ""
  ].filter(Boolean);
  if (!reasons.length) return "";
  return `
    <div class="match-reasons" aria-label="查詢命中原因">
      ${reasons.slice(0, 5).map((reason) => `<span>${escapeHtml(reason)}</span>`).join("")}
    </div>
  `;
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

function renderBenefitItems(record) {
  const items = record.benefitItems || [];
  if (!items.length) return "";
  const visible = items.slice(0, 5);
  return `
    <section class="benefit-block" aria-label="補助項目與金額">
      <div class="benefit-heading">
        <span>補助項目與金額</span>
        <small>${escapeHtml(record.benefitSourceNote || "金額會因年度、縣市、資格或審查結果不同，申請前請以來源頁或承辦單位為準。")}</small>
      </div>
      <div class="benefit-list">
        ${visible
          .map(
            (item) => `
              <div class="benefit-item">
                <strong>${escapeHtml(item.label)}</strong>
                <p class="benefit-amount">${escapeHtml([item.amount, item.unit].filter(Boolean).join(" "))}</p>
                ${item.note ? `<p>${escapeHtml(item.note)}</p>` : ""}
                ${item.sourceDate || item.sourceUrl ? `<small>${item.sourceDate ? `來源日期：${escapeHtml(item.sourceDate)}` : ""}${item.sourceDate && item.sourceUrl ? " / " : ""}${item.sourceUrl ? `<a href="${escapeHtml(item.sourceUrl)}" target="_blank" rel="noopener">金額來源</a>` : ""}</small>` : ""}
              </div>
            `
          )
          .join("")}
      </div>
    </section>
  `;
}

function renderApplicationConditions(record) {
  const items = record.applicationConditions || [];
  const hasStandards = (record.incomeStandardGroups || []).length;
  const hasProvinceNote = Boolean(record.taiwanProvinceNote);
  if (!items.length && !hasStandards && !hasProvinceNote) return "";
  const visible = items.slice(0, 6);
  return `
    <section class="condition-block" aria-label="申請條件">
      <div class="condition-heading">
        <span>申請條件先看</span>
        <small>${escapeHtml(record.conditionSourceNote || "資格會因年度、縣市、家庭人口與審查結果不同，送件前請以來源頁或承辦單位為準。")}</small>
      </div>
      ${renderTaiwanProvinceNote(record)}
      ${renderIncomeStandardGroups(record)}
      ${visible.length ? `
        <div class="condition-list">
          ${visible
            .map(
              (item) => `
                <div class="condition-item">
                  <strong>${escapeHtml(item.label)}</strong>
                  <p>${escapeHtml(item.requirement)}</p>
                  ${item.note ? `<small>${escapeHtml(item.note)}</small>` : ""}
                  ${item.sourceDate || item.sourceUrl ? `<small>${item.sourceDate ? `來源日期：${escapeHtml(item.sourceDate)}` : ""}${item.sourceDate && item.sourceUrl ? " / " : ""}${item.sourceUrl ? `<a href="${escapeHtml(item.sourceUrl)}" target="_blank" rel="noopener">條件來源</a>` : ""}</small>` : ""}
                </div>
              `
            )
            .join("")}
        </div>
      ` : ""}
    </section>
  `;
}

function renderTaiwanProvinceNote(record) {
  const note = record.taiwanProvinceNote;
  if (!note) return "";
  return `
    <div class="province-note">
      <strong>${escapeHtml(note.title)}</strong>
      <p>${escapeHtml(note.text)}</p>
      ${(note.areas || []).length ? `<small>${escapeHtml(note.areas.join("、"))}</small>` : ""}
    </div>
  `;
}

function renderIncomeStandardGroups(record) {
  const groups = record.incomeStandardGroups || [];
  if (!groups.length) return "";
  return `
    <div class="standard-groups">
      ${groups
        .map(
          (group) => `
            <div class="standard-group">
              <div class="standard-group-heading">
                <strong>${escapeHtml(group.label)}</strong>
                <small>${escapeHtml(group.sourceDate || "")}${group.sourceUrl ? ` / <a href="${escapeHtml(group.sourceUrl)}" target="_blank" rel="noopener">官方標準來源</a>` : ""}</small>
              </div>
              <div class="standard-card-grid">
                ${(group.items || [])
                  .map(
                    (item) => `
                      <div class="standard-card">
                        <strong>${escapeHtml(item.region)}</strong>
                        <dl>
                          <div><dt>平均所得</dt><dd>${escapeHtml(item.income)}</dd></div>
                          <div><dt>動產限額</dt><dd>${escapeHtml(item.movableAssets)}</dd></div>
                          <div><dt>不動產限額</dt><dd>${escapeHtml(item.realEstate)}</dd></div>
                        </dl>
                        ${item.note ? `<small>${escapeHtml(item.note)}</small>` : ""}
                      </div>
                    `
                  )
                  .join("")}
              </div>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

function renderApplicationMethod(record) {
  const steps = record.howToApply || [];
  if (!steps.length) return "";
  return `
    <section class="method-block" aria-label="申請注意事項">
      <div class="method-heading">
        <span>申請注意事項</span>
        <small>${escapeHtml(record.applicationMethodSourceNote || "實際受理窗口、期限、文件與線上申辦注意事項，請以來源頁或承辦單位公告為準。")}</small>
      </div>
      <ol class="method-list">
        ${steps.map((step) => `<li>${escapeHtml(step)}</li>`).join("")}
      </ol>
    </section>
  `;
}

function renderRelatedPrograms(programs) {
  if (!programs.length) return "";
  return `
    <section class="related-programs" aria-label="旗下可查方案">
      <div class="related-heading">
        <span>旗下可查方案</span>
        <small>同一單位的具體服務，先收在這裡，避免結果頁重複出現。</small>
      </div>
      <div class="related-program-list">
        ${programs
          .map(
            (program) => `
              <div class="related-program">
                <div class="related-program-main">
                  <strong>${escapeHtml(program.name)}</strong>
                  <p>${escapeHtml(program.summary || program.eligibility || "依來源頁公告。")}</p>
                  <small>${escapeHtml((program.serviceCategories || []).slice(0, 3).join("、") || "方案資訊")}</small>
                  <details class="related-program-detail">
                    <summary>查看資源說明</summary>
                    ${renderApplicationConditions(program)}
                    ${renderBenefitItems(program)}
                    ${renderApplicationMethod(program)}
                    <div class="related-source-link">
                      ${program.source?.url ? `<a href="${escapeHtml(program.source.url)}" target="_blank" rel="noopener">開啟來源頁</a>` : ""}
                    </div>
                  </details>
                </div>
              </div>
            `
          )
          .join("")}
      </div>
    </section>
  `;
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
  const visibleAudiences = displayValues(record.audiences);
  const visibleCategories = displayValues(record.serviceCategories);
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
        ${visibleAudiences.slice(0, 3).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
        ${visibleCategories.slice(0, 2).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
      </div>

      ${renderSourceConfidence(record)}
      ${renderMatchReasons(record)}
      ${renderApplicationConditions(record)}
      ${renderBenefitItems(record)}
      ${renderApplicationMethod(record)}
      ${renderRelatedPrograms(record.visibleRelatedPrograms || [])}

      <div class="quick-answer-grid">
        <div>
          <span>適合誰</span>
          <p>${escapeHtml(visibleAudiences.slice(0, 3).join("、") || record.eligibility || "依來源頁公告")}</p>
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
            <h4>申請注意事項</h4>
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

function statusLabel(status) {
  return {
    "local-strong": "地方強來源",
    "local-entry": "地方入口",
    "local-needs-confirmation": "地方需確認",
    "central-ok": "中央可用",
    "central-fallback": "中央 fallback",
    "private-only": "民間為主",
    gap: "資料缺口"
  }[status] || status;
}

function findCoverageCell(county, query) {
  if (!state.coverage || !county) return null;
  const row = (state.coverage.rows || []).find((item) => item.county === county);
  if (!row) return null;
  const text = String(query || "").toLowerCase();
  return (row.cells || []).find((cell) => {
    const need = (state.coverage.needs || []).find((item) => item.id === cell.needId);
    return need && (need.terms || []).some((term) => text.includes(String(term).toLowerCase()));
  }) || null;
}

function renderGuidedPath(filteredCount = 0) {
  if (!els.guidedPath) return;
  const steps = [
    {
      label: "1 選縣市",
      value: state.county || "不限縣市",
      state: state.county ? "done" : "active"
    },
    {
      label: "2 選狀況",
      value: state.query || state.category || "先選遇到的問題",
      state: state.query || state.category ? "done" : "pending"
    },
    {
      label: "3 看窗口",
      value: filteredCount ? "看資格、文件、下一步" : "用官方 fallback",
      state: filteredCount ? "done" : "pending"
    }
  ];
  els.guidedPath.innerHTML = steps
    .map(
      (step) => `
        <div class="guided-step is-${escapeHtml(step.state)}">
          <span>${escapeHtml(step.label)}</span>
          <strong>${escapeHtml(step.value)}</strong>
        </div>
      `
    )
    .join("");
}

function renderDecisionAid(filtered) {
  if (!els.decisionAid) return;
  const first = filtered[0];
  const coverageCell = findCoverageCell(state.county, state.query || state.category);
  let message = "先看前幾張卡的資格、文件、下一步，再開來源頁確認。";
  let tone = "steady";
  if (!state.county && !state.query && !state.category) {
    message = "先從縣市或遇到的狀況開始，結果會優先排出較相關的卡片。";
  } else if (!filtered.length) {
    message = "查不到不代表沒有福利，先改用社會局、公所、1957或社福中心查詢。";
    tone = "alert";
  } else if (coverageCell && ["gap", "central-fallback", "private-only"].includes(coverageCell.status)) {
    message = `這個主題目前是「${statusLabel(coverageCell.status)}」，申請前要再問所在地社會局處或公所。`;
    tone = "caution";
  } else if (first && sourceConfidence(first).level === "strong") {
    message = "第一批結果已有較完整來源，先比對資格和應備文件，再用來源頁確認。";
  }
  els.decisionAid.className = `decision-aid tone-${tone}`;
  els.decisionAid.innerHTML = `
    <strong>下一步</strong>
    <span>${escapeHtml(message)}</span>
  `;
}

function renderOperationalPanels() {
  if (els.coverageSummary && state.coverage?.summary) {
    const summary = state.coverage.summary;
    const strong = summary.strongOrCentralOkPairs || 0;
    const total = summary.totalPairs || 0;
    const attention = summary.attentionPairs || 0;
    els.coverageSummary.textContent = `目前 ${strong}/${total} 個縣市與需求組合已有較穩來源，${attention} 個組合列入觀察或補強。`;
  }
  if (els.hardWarningTotal && state.sourceHealth?.summary) {
    els.hardWarningTotal.textContent = state.sourceHealth.summary.hardWarnings ?? 0;
    els.transientWarningTotal.textContent = state.sourceHealth.summary.transientWarnings ?? 0;
  }
  if (els.batchGateMode && state.batchGate?.decision) {
    const mode = state.batchGate.decision.recommendedMode || "maintain-and-target";
    els.batchGateMode.textContent = mode === "maintain-and-target" ? "缺口驅動" : mode;
  }
  if (els.batchGateList && state.batchGate?.topCandidates) {
    const candidates = state.batchGate.topCandidates.slice(0, 6);
    if (!candidates.length) {
      els.batchGateList.innerHTML = `<p>目前沒有高優先新增批次，先維持來源健康與搜尋體驗。</p>`;
      return;
    }
    els.batchGateList.innerHTML = candidates
      .map(
        (item) => `
          <button type="button" data-gap-county="${escapeHtml(item.county)}" data-gap-query="${escapeHtml(item.query)}">
            <strong>${escapeHtml(item.county)} ${escapeHtml(item.needLabel)}</strong>
            <span>${escapeHtml(statusLabel(item.status))}</span>
          </button>
        `
      )
      .join("");
  }
}

function groupVisibleRecords(records) {
  const visibleIds = new Set(records.map((record) => record.id));
  const childrenByParent = new Map();

  records.forEach((record) => {
    if (record.source?.type !== "foundation-program-page") return;
    const parentId = parentFoundationId(record);
    if (!parentId || !visibleIds.has(parentId)) return;
    if (!childrenByParent.has(parentId)) childrenByParent.set(parentId, []);
    childrenByParent.get(parentId).push(record);
  });

  return records
    .filter((record) => {
      if (record.source?.type !== "foundation-program-page") return true;
      const parentId = parentFoundationId(record);
      return !parentId || !visibleIds.has(parentId);
    })
    .map((record) =>
      childrenByParent.has(record.id)
        ? { ...record, visibleRelatedPrograms: childrenByParent.get(record.id) }
        : record
    );
}

function renderActiveFilters() {
  const filters = [
    state.query ? `資源主題：${state.query}` : "",
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
  const visibleCards = groupVisibleRecords(visible);
  const collapsedCount = visible.length - visibleCards.length;
  const groupLabel = groupLabels[state.group] || "查詢結果";
  const hasBaseFilter = Boolean(state.query || state.county || state.audience || state.category || state.currentOnly);

  els.resultTitle.textContent = groupLabel;
  els.resultCount.textContent =
    state.group === "all"
      ? `找到 ${filtered.length} 筆可參考資源${collapsedCount ? `，合併顯示為 ${visibleCards.length} 張卡` : ""}`
      : `${groupLabel} ${filtered.length} 筆，先顯示 ${visibleCards.length} 張卡${collapsedCount ? `（已收合 ${collapsedCount} 筆同單位方案）` : ""}${hasBaseFilter && baseCount !== filtered.length ? `；目前篩選共 ${baseCount} 筆` : ""}`;
  renderActiveFilters();
  renderGuidedPath(filtered.length);
  renderDecisionAid(filtered);
  syncGroupButtons();
  syncShortcutButtons();

  if (!visible.length) {
    els.results.innerHTML = renderEmptyState();
    return;
  }

  const moreNote =
    filtered.length > visible.length
      ? `<div class="more-note">這組還有 ${filtered.length - visible.length} 筆。可以切到「全部結果」，或用縣市、身分、資源類別再縮小。</div>`
      : "";
  els.results.innerHTML = visibleCards.map(renderRecord).join("") + moreNote;
}

function renderEmptyState() {
  const countyHint = state.county ? `${state.county} 社會局 公所` : "社會局 公所";
  const currentQuery = state.query.trim();
  const shortQuery = currentQuery.split(/\s+/)[0] || "低收入戶";
  const coverageCell = findCoverageCell(state.county, currentQuery || state.category);
  const gapText = coverageCell && ["gap", "central-fallback", "private-only"].includes(coverageCell.status)
    ? `目前覆蓋矩陣標示為「${statusLabel(coverageCell.status)}」，這比較像資料需要補強，不代表沒有資源。`
    : "這可能是關鍵字太窄、縣市限制太細，或資料仍在補強。";
  const suggestions = [
    countyHint,
    shortQuery,
    "1957 福利諮詢",
    "社福中心"
  ].filter(Boolean);
  const unique = [...new Set(suggestions)].slice(0, 4);
  return `
    <div class="empty-state detailed-empty">
      <div>
        <strong>目前沒有找到完全符合的資源</strong>
        <p>${escapeHtml(gapText)}</p>
        <p>先放寬條件通常比較快：取消縣市或身分限制，再用短一點的詞搜尋。若是急迫狀況，可以先問1957或所在地社會局處。</p>
      </div>
      <div class="empty-actions">
        ${unique.map((item) => `<button type="button" data-empty-query="${escapeHtml(item)}">${escapeHtml(item)}</button>`).join("")}
        <button type="button" data-empty-action="broaden">放寬所有條件</button>
      </div>
    </div>
  `;
}

function updateStats(records) {
  els.centralResourceTotal.textContent = records.filter(isPublicCentralResource).length;
  els.localResourceTotal.textContent = records.filter(isPublicLocalResource).length;
  els.privateResourceTotal.textContent = records.filter(isPrivateResource).length;
}

function selectHasValue(select, value) {
  return [...select.options].some((option) => option.value === value);
}

function setSelectValue(select, value) {
  select.value = value && selectHasValue(select, value) ? value : "";
}

function syncControls() {
  if (els.query && els.query.value !== state.query) {
    els.query.value = state.query;
  }
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

function showResourceDescriptions() {
  state.query = els.query?.value.trim() || "";
  const hasNarrowingFilter = Boolean(state.query || state.county || state.audience || state.category || state.currentOnly);
  state.group = hasNarrowingFilter ? "all" : "recommended";
  syncControls();
  render();
  scrollToResults();
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
    render();
  });
  els.query.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      showResourceDescriptions();
    }
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
  els.applyFilterButton.addEventListener("click", showResourceDescriptions);
  els.results.addEventListener("click", (event) => {
    const button = event.target.closest("[data-empty-query], [data-empty-action]");
    if (!button) return;
    if (button.dataset.emptyAction === "broaden") {
      resetFilters();
      scrollToResults();
      return;
    }
    state.query = button.dataset.emptyQuery || "";
    state.county = "";
    state.audience = "";
    state.category = "";
    state.currentOnly = false;
    state.group = "all";
    syncControls();
    render();
    scrollToResults();
  });

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
  els.batchGateList?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-gap-query]");
    if (!button) return;
    state.county = button.dataset.gapCounty || "";
    state.query = button.dataset.gapQuery || "";
    state.audience = "";
    state.category = "";
    state.currentOnly = false;
    state.group = "all";
    syncControls();
    render();
    scrollToResults();
  });
}

async function loadOptionalJson(path) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.warn(`Unable to load ${path}`, error);
    return null;
  }
}

async function init() {
  try {
    bindEvents();
    document.body.classList.remove("is-booting");
    const [data, coverage, sourceHealth, batchGate] = await Promise.all([
      loadOptionalJson("data/resources.json"),
      loadOptionalJson("data/coverage-matrix.json"),
      loadOptionalJson("data/source-health-summary.json"),
      loadOptionalJson("data/batch-gate.json")
    ]);
    if (!data) throw new Error("Unable to load data/resources.json");
    state.records = hydrateRelatedPrograms(data.records || []);
    state.coverage = coverage;
    state.sourceHealth = sourceHealth;
    state.batchGate = batchGate;
    setupFilters(state.records);
    syncControls();
    updateStats(state.records);
    renderOperationalPanels();
    render();
  } catch (error) {
    els.resultCount.textContent = "資料載入失敗";
    els.results.innerHTML = `<div class="empty-state"><p>無法讀取 data/resources.json，請先確認資料檔已產生並重新整理頁面。</p></div>`;
    console.error(error);
  }
}

init();
