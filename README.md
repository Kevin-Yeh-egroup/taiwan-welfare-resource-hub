# Taiwan Welfare Resource Hub

可搜尋、可篩選、可定期檢查更新的台灣社會福利資源目錄雛形。

這個 repo 先把三件事做好：

1. 把來源文件和網頁整理成可追溯的 `sources`。
2. 把福利資源轉成民眾看得懂的卡片資料。
3. 用定期檢查報告提醒哪些來源可能跨年度更新、失效或需要人工確認。

## Current Status

- 本機 Git repo 已建立。
- 靜態網站可直接部署到 Vercel。
- Review-stage `noindex` 已啟用：公開連結可看，但先不建議被搜尋引擎收錄。
- 使用者提供的 Downloads 文件目前在本機路徑讀不到，已保留 `source-docs/` 與抽取腳本，檔案補上後可重新抽 URL seeds。

## Local Preview

```powershell
python -m http.server 4173
```

Then open:

```text
http://localhost:4173
```

## Data Workflow

```powershell
python scripts/extract_source_urls.py source-docs --out data/extracted-urls.json
python scripts/crawl_sources.py --sources data/sources.json --out data/resources.json
python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json
python scripts/validate_data.py
```

`extract_source_urls.py` supports `.docx` and `.pdf`. PDF extraction uses `pypdf` if installed.

## Public Production Plan

Recommended route:

1. Kevin approves public release posture and repo slug.
2. Create a dedicated public GitHub repository, for example `taiwan-welfare-resource-hub`.
3. Push `main`.
4. Create/link a dedicated Vercel project from GitHub.
5. Confirm Production branch is `main`.
6. Verify:
   - site returns `200 OK`;
   - `X-Robots-Tag: noindex, nofollow, noarchive` is present;
   - HTML has meta robots;
   - `robots.txt` blocks crawling during review.

## Update Cadence

Draft schedule:

- Normal months: weekly freshness check.
- December and January: daily source freshness check, because government and NGO welfare pages often roll year-specific amounts, forms, and qualification rules.
- Open-data sources with declared annual update frequency still get cross-year checks, not just annual checks.

## Source Documents

Put Kevin-provided PDFs/DOCXs in `source-docs/` before running extraction. Do not commit the raw documents unless Kevin approves.
