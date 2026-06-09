# Taiwan Welfare Resource Hub

台灣社會福利資源查詢工具，目標是讓一般民眾可以用「遇到什麼困難」來查找政府與民間社福資源，而不是只看到一串單位簡介。

## Current Status

- Public GitHub repo: https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub
- Vercel Production: https://taiwan-welfare-resource-hub.vercel.app/
- Review-stage `noindex` 保留中：HTML meta robots、`robots.txt`、Vercel `X-Robots-Tag` 都會阻擋搜尋引擎索引。
- Current dataset: 562 resource records from 137 allowlisted sources.
- Foundation coverage: 355 official SFAA national social-welfare foundation records queried on 2026-06-03.
- Reviewed foundation program cards: 71 manually allowlisted program/service pages converted from candidate crawls.
- Batch 0/1 central expansion: 9 high-demand nationwide cards for national pension premium subsidy, special-circumstances families, disability welfare, childcare, elder welfare, education tuition reduction, labor subsidy, 115 rent subsidy, and 113 protection hotline.
- Batch 2 local expansion: 12 six-municipality program cards covering Taipei, New Taipei, Taoyuan, Taichung, Tainan, and Kaohsiung local benefits with concrete eligibility, amounts, and application notes.
- Batch 3A local expansion: 12 northern/central non-municipality program cards covering Keelung, Hsinchu City, Hsinchu County, Miaoli, Changhua, Nantou, and Yunlin.
- Batch 3B local expansion: 12 southern/eastern non-municipality program cards covering Chiayi City, Chiayi County, Pingtung, Yilan, Hualien, and Taitung.
- Batch 3C local expansion: 9 offshore county program cards covering Penghu, Kinmen, and Lienchiang.
- Batch 4A foundation deep crawl: 8 reviewed civil-society program cards for Moxian, Garden of Hope, Joyce McMillan, Spinal Cord Injury, and Hondao service pages.
- Batch 4B foundation deep crawl: 7 reviewed civil-society program cards for VTCIDD Taoyuan disability services, Saint Island scholarships/living assistance, Mega charity emergency/medical relief, and Shing Yi social assistance.
- Batch 4C foundation deep crawl: 10 reviewed civil-society program cards for Han Ci child after-school services, Christian Salvation Service women/children support, Sinyi emergency assistance, Good Shepherd protection services, Taiwan Caring Foundation migrant women/children support, PSA hearing subsidies/scholarships, PX Mart material-bank partnerships, GIS employee charity subsidies, and Yung Shin long-term/community care.
- Batch 4D foundation deep crawl: 12 reviewed civil-society program cards for Chinese Culture child/elder care, hearing life-reconstruction/family support, Pearl S. Buck new immigrant family services, Yude elder/LTC transport, Sunshine burn/facial-difference reconstruction, Oldyes community/home care, Syin-Lu early intervention/disability care, and Children Are Us care services.
- Batch 4E foundation deep crawl: 7 reviewed civil-society program cards for Mercyland cancer-family assistance and scholarships, Sin Te adult disability residential/aging support, Taiwan Blind Institute life reconstruction, YCSWF adult day care, and Huashan three-loss elder home-based services.
- Batch 4F foundation review: 5 additional civil-society cards for Chang Yung-Fa case assistance, Chung Hua Tang emergency/low-income/student/medical aid, Eting application forms, Mustard Seed child placement support, and Chuan Cheng long-term/disability service windows; the existing Wan Hai emergency assistance card was also enriched with conditions, benefit items, documents, and 2025/08/01 online-application notes.
- V2 Batch 5A local deep-dive: 5 new official city program cards for Taipei/New Taipei disability living allowances and Taipei/New Taipei/Taoyuan middle-low-income elderly living allowances; the existing Tainan elderly allowance card was de-duplicated and enriched with official eligibility, benefit amounts, documents, and application notes.
- V2 Batch 5B local deep-dive: 7 new official local allowance cards for Taichung, Kaohsiung, Keelung, and Yilan, focused on disability living allowances and middle-low-income elderly living allowances with eligibility, benefit amounts, and application notes.
- V2 Batch 5C local deep-dive: 9 new official local allowance cards for Hsinchu City, Hsinchu County, Miaoli, Changhua, and Nantou, focused on disability living allowances and middle-low-income elderly living allowances with eligibility, benefit amounts, and application notes.
- V2 Batch 5D local deep-dive: 3 new official/cross-checked cards for Miaoli middle-low-income elderly living allowance and Pingtung disability/elderly living allowances.
- V2 Batch 5E local deep-dive: 10 new official/cross-checked cards for Yunlin, Chiayi City, Chiayi County, Hualien, and Taitung disability living allowances and middle-low-income elderly living allowances.
- V2 Batch 5F annual-standard audit: refreshed the 115年度 low-income/middle-low-income standard card, Taiwan/Fujian source links, and "臺灣省" explanation/search terms.
- V2 Batch 5G Taiwan search/UX pass: added common Taiwan query synonyms such as `台/臺`, `身障/身心障礙`, `低收/低收入戶`, `中低收/中低收入戶`, and elder-allowance wording.
- V2 Batch 6A local closure: 8 new official/cross-checked cards for Taoyuan, Tainan, Penghu, Kinmen, and Lienchiang disability living allowances and middle-low-income elder allowances, with local-confirmation labels where current detail pages are incomplete.
- V2 Batch 6D high-intent central expansion: 3 new nationwide cards for family caregiver support, low-income student grants, and child/youth economic support; the 115 rent-subsidy card now points to the MOI official update and hotline.
- UX-1 search and no-result pass: added high-demand query synonyms, source-confidence rows, match-reason chips, no-result suggestions, and quick tiles for rent pressure and caregiver support.
- V2 Batch 6E source hardening: replaced 4 unstable warning sources with stronger official anchors and split freshness output into hard `warnings` versus retryable `transientWarnings`.
- QA-1/UX-2 operating layer: added county-by-need coverage matrix, source-health summary, batch-gate candidates, 60-second guided query path, and missing-data-aware no-result messaging.

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
python scripts/convert_candidate_programs.py --resources data/resources.json --candidates data/foundation-program-candidates.json data/foundation-program-candidates-batch-b.json data/foundation-program-candidates-batch-c.json data/foundation-program-candidates-batch-d.json data/foundation-program-candidates-batch-e.json data/foundation-program-candidates-batch-f.json data/foundation-program-candidates-batch-g.json data/foundation-program-candidates-batch-h.json data/foundation-program-candidates-batch-i.json --allowlist data/formal-program-allowlist.json --out data/resources.json
python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json --timeout 5 --retries 0 --retry-sleep 0
python scripts/build_operational_artifacts.py
python scripts/validate_data.py
node scripts/build_static.mjs
```

Optional candidate crawl batches:

```powershell
python scripts/crawl_foundation_program_candidates.py --limit 30 --out data/foundation-program-candidates.json
python scripts/crawl_foundation_program_candidates.py --batch B --previous data/foundation-program-candidates.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-b.json
python scripts/crawl_foundation_program_candidates.py --batch C --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-c.json
python scripts/crawl_foundation_program_candidates.py --batch D --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-d.json
python scripts/crawl_foundation_program_candidates.py --batch E --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --limit 30 --out data/foundation-program-candidates-batch-e.json
python scripts/crawl_foundation_program_candidates.py --batch F --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --limit 30 --out data/foundation-program-candidates-batch-f.json
python scripts/crawl_foundation_program_candidates.py --batch G --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --limit 30 --out data/foundation-program-candidates-batch-g.json
python scripts/crawl_foundation_program_candidates.py --batch H --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --previous data/foundation-program-candidates-batch-g.json --limit 30 --out data/foundation-program-candidates-batch-h.json
python scripts/crawl_foundation_program_candidates.py --batch I --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --previous data/foundation-program-candidates-batch-g.json --previous data/foundation-program-candidates-batch-h.json --limit 30 --out data/foundation-program-candidates-batch-i.json
```

`crawl_foundation_program_candidates.py` is review-first. Candidate pages stay non-public until a reviewed entry is added to `data/formal-program-allowlist.json`.

## Source Policy

- SFAA foundation importer uses the official public directory at `https://swft.sfaa.gov.tw/fund/fh0300#`, its public list/detail API, and code tables for city, district, service object, and service type.
- Foundation records show whether the official directory lists the organization as operating, but program-level eligibility, intake status, quota, documents, and service area still require source-page or phone confirmation.
- Raw PDFs/DOCXs from Kevin-provided source materials belong in `source-docs/`. Do not commit raw documents unless Kevin approves.

## Public Production Verification

The stable public route is GitHub `main` -> Vercel Production. Verify:

- site returns `200 OK`;
- `X-Robots-Tag: noindex, nofollow, noarchive` is present;
- HTML has `<meta name="robots" content="noindex,nofollow,noarchive">`;
- `robots.txt` blocks crawling during review.

## Update Cadence

GitHub Actions runs:

- weekly freshness checks in normal months;
- daily checks in December and January, because social-welfare programs often update amounts, forms, thresholds, or yearly intake rules across the calendar year.

The scheduled workflow rebuilds `data/sources.json`, refreshes `data/resources.json`, converts reviewed foundation program pages, checks source freshness, validates data, builds the static site, and commits changed JSON back to `main`.
