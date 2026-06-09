# V2 Batch 6E Source Hardening

Date: 2026-06-09

## Scope

Batch 6E hardens sources that produced freshness warnings after Batch 6A-6D. The goal is to separate true broken links from temporary government-site transport failures.

## Fixed Source Anchors

Updated 4 warning targets:

- `miaoli-maternal-newborn-nutrition-115`
  - Changed from a news page to the Miaoli Social Affairs application note.
  - New URL: `https://www.miaoli.gov.tw/social_affairs/News_Content.aspx?n=682&s=147156`
- `hsinchu-city-disability-living-allowance-115`
  - Changed from a long Social Affairs application URL to the Hsinchu City regulation print page.
  - New URL: `https://law.hccg.gov.tw/LawContent.aspx?id=FL084082&media=print`
- `pingtung-disability-living-allowance-115`
  - Changed from a gov.tw page that returned 403/404 to the Pingtung one-stop service URL.
  - New URL: `https://onestop.pthg.gov.tw/eservice/apply_mode_directions2?itemId=2005`
- `yunlin-middle-low-income-elderly-allowance-115`
  - Changed from a slow/unstable Social Affairs detail URL to the current Yunlin Social Affairs announcement page.
  - New URL: `https://social.yunlin.gov.tw/News_Content.aspx?n=737&s=442453`

## Checker Improvement

`scripts/check_freshness.py` now separates:

- `warnings`: hard failures, such as broken URLs or non-retryable failures.
- `transientWarnings`: retryable transport failures, such as timeout, connection reset, or temporary 5xx behavior.

This keeps broken source work visible without letting slow government sites hide real 404-style problems.

## Verification

Commands run:

```powershell
python scripts/build_source_registry.py
python scripts/crawl_sources.py --sources data/sources.json --out data/resources.json
python scripts/convert_candidate_programs.py --resources data/resources.json --candidates data/foundation-program-candidates.json data/foundation-program-candidates-batch-b.json data/foundation-program-candidates-batch-c.json data/foundation-program-candidates-batch-d.json data/foundation-program-candidates-batch-e.json data/foundation-program-candidates-batch-f.json data/foundation-program-candidates-batch-g.json data/foundation-program-candidates-batch-h.json data/foundation-program-candidates-batch-i.json --allowlist data/formal-program-allowlist.json --out data/resources.json
python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json --timeout 2 --retries 0 --retry-sleep 0
python scripts/validate_data.py
node --check app.js
npm run build
```

Results:

- `data/sources.json`: 137 sources.
- `data/resources.json`: 562 records.
- Hard freshness warnings: 0.
- Transient freshness warnings: 3 retryable timeout cases retained in `transientWarnings`.
- `validate_data.py`: passed.
- `npm run build`: passed.

Transient warnings retained:

- `nantou-low-income-living-assistance-115`
- `penghu-after-school-care-subsidy-115`
- `county-taoyuan-social`

These are not suppressed; they are reclassified so future source-hardening can prioritize hard failures first and handle slow official sites separately.
