# Taiwan Welfare Resource Hub

可搜尋、可篩選、可定期檢查更新的台灣社會福利資源目錄雛形。

這個 repo 先把三件事做好：

1. 把來源文件和網頁整理成可追溯的 `sources`。
2. 把福利資源轉成民眾看得懂的卡片資料。
3. 用定期檢查報告提醒哪些來源可能跨年度更新、失效或需要人工確認。

## Current Status

- Public GitHub repo: https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub
- Vercel Production: https://taiwan-welfare-resource-hub.vercel.app/
- Review-stage `noindex` 已啟用：公開連結可看，但先不建議被搜尋引擎收錄。
- V1 目標是全台官方入口可查：22 縣市社會局處、中央福利/長照/健保/就業入口，加上可匯入的逐筆開放資料與全國性社福財團法人名錄。
- Current dataset: 411 resource records, including 355 official SFAA national social-welfare foundation records queried on 2026-06-03.
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
python scripts/build_source_registry.py
python scripts/extract_source_urls.py source-docs --out data/extracted-urls.json
python scripts/crawl_sources.py --sources data/sources.json --out data/resources.json
python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json
python scripts/validate_data.py
node scripts/build_static.mjs
```

`extract_source_urls.py` supports `.docx` and `.pdf`. PDF extraction uses `pypdf` if installed.

The SFAA foundation importer uses the official public directory at `https://swft.sfaa.gov.tw/fund/fh0300#`, its public list/detail API, and code tables for city, district, service object, and service type. It records official `A` status as "運作中" but still asks users to confirm current-year program availability with each foundation.

## Public Production Verification

The stable public route is GitHub `main` -> Vercel Production. Verify:

- site returns `200 OK`;
- `X-Robots-Tag: noindex, nofollow, noarchive` is present;
- HTML has meta robots;
- `robots.txt` blocks crawling during review.

## Update Cadence

Draft schedule:

- Normal months: weekly freshness check.
- December and January: daily source freshness check, because government and NGO welfare pages often roll year-specific amounts, forms, and qualification rules.
- Open-data sources with declared annual update frequency still get cross-year checks, not just annual checks.
- GitHub Actions rebuilds `data/sources.json`, refreshes `data/resources.json`, checks freshness, validates data, and commits changed JSON back to `main`.

## Source Documents

Put Kevin-provided PDFs/DOCXs in `source-docs/` before running extraction. Do not commit the raw documents unless Kevin approves.
