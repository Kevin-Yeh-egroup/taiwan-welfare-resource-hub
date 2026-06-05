# Taiwan Welfare Resource Hub

台灣社會福利資源查詢工具，目標是讓一般民眾可以用「遇到什麼困難」來查找政府與民間社福資源，而不是只看到一串單位簡介。

## Current Status

- Public GitHub repo: https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub
- Vercel Production: https://taiwan-welfare-resource-hub.vercel.app/
- Review-stage `noindex` 保留中：HTML meta robots、`robots.txt`、Vercel `X-Robots-Tag` 都會阻擋搜尋引擎索引。
- Current dataset: 435 resource records from 59 allowlisted sources.
- Foundation coverage: 355 official SFAA national social-welfare foundation records queried on 2026-06-03.
- Reviewed foundation program cards: 22 manually allowlisted program/service pages converted from candidate crawls.
- Batch 0/1 central expansion: 9 high-demand nationwide cards for national pension premium subsidy, special-circumstances families, disability welfare, childcare, elder welfare, education tuition reduction, labor subsidy, 115 rent subsidy, and 113 protection hotline.
- Batch 2 local expansion: 12 six-municipality program cards covering Taipei, New Taipei, Taoyuan, Taichung, Tainan, and Kaohsiung local benefits with concrete eligibility, amounts, and application notes.

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
python scripts/convert_candidate_programs.py --resources data/resources.json --candidates data/foundation-program-candidates.json data/foundation-program-candidates-batch-b.json --allowlist data/formal-program-allowlist.json --out data/resources.json
python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json
python scripts/validate_data.py
node scripts/build_static.mjs
```

Optional candidate crawl batches:

```powershell
python scripts/crawl_foundation_program_candidates.py --limit 30 --out data/foundation-program-candidates.json
python scripts/crawl_foundation_program_candidates.py --batch B --previous data/foundation-program-candidates.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-b.json
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
