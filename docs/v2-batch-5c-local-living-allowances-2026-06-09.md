# V2 Batch 5C Local Living Allowances - 2026-06-09

## Scope

Batch 5C expands the local monthly-allowance cards that ordinary residents are likely to search for first: disability living allowances and middle-low-income elderly living allowances.

This batch only adds cards when the official source can support the citizen-facing order:

1. 申請條件
2. 補助金額
3. 申請注意事項

## Added Cards

| Area | Card | Main source type | Source quality note |
| --- | --- | --- | --- |
| 新竹市 | 新竹市身心障礙者生活補助 | Official city application page | Conditions, amounts, documents, and district-office handling are listed. |
| 新竹市 | 新竹市中低收入老人生活津貼 | Official city application/print page | 115年度 thresholds, amounts, and district-office handling are listed. |
| 新竹縣 | 新竹縣身心障礙者生活補助 | Official county administration report | Confirms active 115年度 program and amounts; application details still point residents to township/city offices. |
| 新竹縣 | 新竹縣中低收入老人生活津貼 | Official county statistical brief | Confirms amount tiers and income thresholds; application details still point residents to township/city offices. |
| 苗栗縣 | 苗栗縣身心障礙者生活補助 | Official county application guide | Application guide has conditions, amounts, documents, and township/city-office handling; 115 guide listing confirms current listing. |
| 彰化縣 | 彰化縣身心障礙者生活補助 | Official county application page | 115年度 income/property conditions and monthly amounts are listed. |
| 彰化縣 | 彰化縣中低收入老人生活津貼 | Official county service page | Updated 2026-05-29 with conditions, amount tiers, documents, and handling office. |
| 南投縣 | 南投縣身心障礙者生活補助費 | Official 115 social assistance welfare handbook | Conditions, amounts, documents, and township/city-office handling are listed. |
| 南投縣 | 南投縣中低收入老人生活津貼 | Official county application PDF | Conditions, exclusions, amount tiers, documents, and 20-30 day handling note are listed. |

## Source Error Found During Build

The failed source was not one of the Batch 5C local cards.

- Source id: `sfaa-social-welfare-foundations`
- Public page: `https://swft.sfaa.gov.tw/fund/fh0300#`
- API endpoint: `https://swft.sfaa.gov.tw/api/main/foundBasic/found/searchFront`
- First failure: `WinError 10061` connection refused while rebuilding `data/resources.json`.
- Follow-up probe: public page returned `200 OK`; code-table API returned `200`; official POST search returned `355` foundation rows.
- Resolution: reran the crawler with a longer timeout. The full crawl completed with `467` base records and `errors=0`, then reviewed foundation program conversion restored the total dataset to `538` records.

## Deferred to Batch 5D

These items were intentionally not added in 5C because the current official source evidence was incomplete for conditions, amounts, and application notes:

- 苗栗縣中低收入老人生活津貼: official listing evidence was found, but the detail page with current amount/condition text still needs a better official source.
- 屏東縣身心障礙者生活補助: online application gateway evidence was found, but not enough official detail for citizen-facing conditions and amounts.
- 屏東縣中低收入老人生活津貼: online application gateway evidence was found, but not enough official detail for citizen-facing conditions and amounts.

## Next Batch Plan

- Batch 5D: resolve the deferred 苗栗/屏東 monthly allowances and add only source-backed cards.
- Batch 5E: continue non-municipality monthly allowance coverage for 雲林、嘉義市、嘉義縣、花蓮、臺東, prioritizing disability and middle-low-income elderly cards.
- Batch 5F: re-audit local low-income/middle-low-income basic-standard cards so the yearly thresholds, "臺灣省" explanation, and search terms remain clear after the allowance expansion.
- Batch 5G: run user-facing search and wording checks for common Taiwan queries such as `身障生活補助`, `老人生活津貼`, `低收入戶補助`, `中低收入戶`, and county names.

## Verification

- `python scripts/build_source_registry.py`: 113 sources.
- `python scripts/crawl_sources.py --sources data\sources.json --out data\resources.json`: 467 base records, errors=0.
- `python scripts/convert_candidate_programs.py ...`: 71 reviewed foundation program pages; total records=538.
- `python scripts/check_freshness.py --sources data\sources.json --out data\freshness-report.json --sleep 0.1 --timeout 5 --retries 0 --retry-sleep 0`: 113 URLs checked, warnings=0.
- `python scripts/validate_data.py`: validation passed, 538 records and 113 sources.
- `node scripts/build_static.mjs`: build completed.
- Duplicate same-name/provider/jurisdiction records: 0.
- Homepage count logic: 21 central public resources, 91 local public resources, 426 private resources.
- Target-card check: all 9 Batch 5C card names are present.
- Search checks: `新竹市 身障生活補助`, `新竹縣 老人生活津貼`, `苗栗縣 身障生活補助`, `彰化縣 中低收入老人`, `南投縣 身心障礙者生活補助費`, and `低收入戶 身障補助` all returned relevant results.
