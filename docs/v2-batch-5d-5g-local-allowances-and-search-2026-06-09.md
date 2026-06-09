# V2 Batch 5D-5G Local Allowances And Search - 2026-06-09

## Scope

This continuation completes the planned Batch 5D, 5E, 5F, and 5G work:

1. Batch 5D: resolve the deferred Miaoli/Pingtung allowance cards.
2. Batch 5E: add Yunlin, Chiayi City, Chiayi County, Hualien, and Taitung local monthly allowance coverage.
3. Batch 5F: refresh the 115年度 low-income/middle-low-income annual standard card and the "臺灣省/福建省" explanation.
4. Batch 5G: make common Taiwan search phrasing more forgiving.

## Added Cards

| Batch | Area | Card | Source posture |
| --- | --- | --- | --- |
| 5D | 苗栗縣 | 苗栗縣中低收入老人生活津貼 | Official township page, source dated 115-06-04. |
| 5D | 屏東縣 | 屏東縣身心障礙者生活補助 | Gov.tw service gateway plus 115年度 amount/standard cross-check. |
| 5D | 屏東縣 | 屏東縣中低收入老人生活津貼 | Gov.tw service gateway plus 115年度 amount/standard cross-check. |
| 5E | 雲林縣 | 雲林縣身心障礙者生活補助 | Official county page, source dated 115-06-08. |
| 5E | 雲林縣 | 雲林縣中低收入老人生活津貼 | Official county page checked on 2026-06-09. |
| 5E | 嘉義市 | 嘉義市身心障礙者生活補助 | Official city page, source dated 2026-01-01. |
| 5E | 嘉義市 | 嘉義市中低收入老人生活津貼 | Official city page, source dated 2026-01-01. |
| 5E | 嘉義縣 | 嘉義縣身心障礙者生活補助 | Gov.tw service gateway; page text may lag current amount, so the card is cross-check marked. |
| 5E | 嘉義縣 | 嘉義縣中低收入老人生活津貼 | County social bureau entry plus 115年度 amount/standard cross-check; stable detail page still needs follow-up. |
| 5E | 花蓮縣 | 花蓮縣身心障礙者生活補助 | Official county social affairs page checked on 2026-06-09. |
| 5E | 花蓮縣 | 花蓮縣中低收入老人生活津貼 | Official county social affairs page checked on 2026-06-09. |
| 5E | 臺東縣 | 臺東縣身心障礙者生活補助 | Taitung City official welfare-business list plus 115年度 amount/standard cross-check. |
| 5E | 臺東縣 | 臺東縣中低收入老人生活津貼 | Taitung City official welfare-business list plus 115年度 amount/standard cross-check. |

## Batch 5F Annual Standards

- Updated the annual-standard source URL to the MOHW 115年度臺灣省及福建省 low-income/middle-low-income announcement page.
- Kept the central annual-standard card as the canonical place for full 115年度 income, movable-asset, and real-estate thresholds.
- Updated source dates in the annual-standard override to `115年度公告；查核日2026-06-09`.
- Preserved the citizen-facing explanation that "臺灣省" is a standards category, not an application destination.
- Added search tags for `台灣省`, `臺灣省`, `福建省`, `金門`, `連江`, `低收`, and `中低收` wording.

## Batch 5G Search Checks

The app now expands common query variants:

- `台灣` / `臺灣`
- `台北` / `臺北`, `台中` / `臺中`, `台南` / `臺南`, `台東` / `臺東`
- `身障` / `身心障礙`
- `低收` / `低收入戶`
- `中低收` / `中低收入戶`
- `老人津貼`, `老人生活補助`, and `老人生活津貼`
- `公所`, `鄉鎮市公所`, and `區公所`

## Source Warning

Freshness produced one warning:

- `pingtung-disability-living-allowance-115`: Gov.tw returned an HTTP freshness failure during automated checking.

The public card remains because it is explicitly marked as an online service gateway plus cross-check, not as a complete local detail page. Future follow-up should replace it with a stable Pingtung County or township detail page if one becomes available.

## Verification

- `python scripts/build_source_registry.py`: 126 sources.
- `python scripts/crawl_sources.py --sources data\sources.json --out data\resources.json --sleep 0.1`: 480 base records, errors=0.
- `python scripts/convert_candidate_programs.py ...`: 71 reviewed foundation program pages; total records=551.
- `python scripts/check_freshness.py --sources data\sources.json --out data\freshness-report.json --timeout 3 --retries 0 --retry-sleep 0`: 126 URLs checked, warnings=1.
- `python scripts/validate_data.py`: validation passed, 551 records and 126 sources.
- `node scripts/build_static.mjs`: build completed.
- Browser search checks: `台東 老人津貼` returned `臺東縣中低收入老人生活津貼`; `身障 生活補助 嘉義市` returned `嘉義市身心障礙者生活補助`; `台灣省 低收` returned `115年度低收入戶、中低收入戶資格審核標準`.
- Mobile layout check at 390px width: no horizontal overflow detected.
- Noindex remained present in HTML meta robots, robots.txt, and Vercel header configuration.
