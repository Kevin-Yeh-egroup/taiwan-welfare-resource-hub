# Batch 0/1 Central Crawl Plan - 2026-06-04

This note records the first executable crawl expansion for current-year Taiwan welfare resources.

## Scope

- Current-year baseline: 2026-06-04, Taiwan ROC year 115.
- Required public categories: central public resources, local public resources, civil-society resources.
- This batch focuses on Batch 0 and Batch 1 only:
  - Batch 0: source manifest, validity rules, reusable detail overrides.
  - Batch 1: high-demand central resources that residents commonly ask about.

## Batch 0 Rules

### Current-Year Validity

- `source-dated`: source explicitly shows ROC 115, year 2026, a 2026 update date, or an active 2026 application period.
- `checked`: official source is reachable and remains a current service entrance, but the page does not itself show a 2026 program date.
- `needs-review`: source lacks official evidence, has stale dates, depends on a PDF/JS-only page that cannot be parsed reliably, or contains conflicting details.

### Public Safety

- Do not publish raw private source documents, personal data, protected addresses, or case-level content.
- Protection services such as domestic violence, child protection, elder protection, disability protection, shelter, and placement should expose only the official hotline, official entry page, and safe next step.
- noindex remains review-stage search control only; it is not privacy protection.

### Data Pattern

- `data/sources.json` remains the allowlisted crawl source registry.
- `data/resource-detail-overrides.json` preserves citizen-facing detail fields after source crawling:
  - `applicationConditions`
  - `benefitItems`
  - `howToApply`
  - `documents`
  - source notes and freshness overrides
- `scripts/crawl_sources.py` merges detail overrides by record id after importing all sources.

## Batch 1 Added Central Sources

| ID | Resource | Current-year signal | Role |
| --- | --- | --- | --- |
| `mohw-national-pension-premium-115` | 115年國民年金保險費與弱勢補助 | Official MOHW page lists 115 premium amounts | Central annual standard |
| `mohw-special-circumstances-family` | 特殊境遇家庭扶助 | MOHW page checked 115-06-02 | Central family support |
| `mohw-disability-welfare` | 身心障礙福利入口 | Official MOHW live portal | Central disability entry |
| `mohw-childcare-services` | 托育服務與育兒支持 | Official MOHW live portal | Central childcare entry |
| `mohw-elderly-welfare` | 老人福利與中低收入老人生活津貼入口 | Official MOHW live portal | Central elder entry |
| `moe-dream-aid-tuition-reduction` | 教育部圓夢助學網：學雜費減免 | Page updated 115-06-04 | Central education aid |
| `wda-labor-subsidy` | 勞動部勞工補助與就業促進資源 | Official WDA live portal | Central labor aid |
| `moi-rent-subsidy-115` | 115年300億元中央擴大租金補貼 | 115 application period | Central housing/rent |
| `mohw-113-protection-hotline` | 113保護專線與關懷e起來 | Page checked 115-06-02 | Central protection hotline |

## Execution Result

- Source registry: 47 allowlisted sources.
- Public resource records: 423 records.
- Batch 1 central additions present: 9 of 9.
- Freshness check: 47 URLs checked, 0 warnings.
- Validation: `python scripts/validate_data.py` passed.
- Static build: `node scripts/build_static.mjs` passed.
- Local UI check: low-income quick filter opens results, the old "看申請方式" label is absent, and the 115 low-income/middle-low-income standard card now renders `申請條件` -> `補助項目與金額` -> `申請注意事項`.

## Follow-Up Batches

- Batch 2: six municipalities, only program-level local pages with concrete eligibility, amount, documents, or contact details.
- Batch 3: non-six-municipality counties and cities, with special attention to remote, Indigenous, and rural service delivery.
- Batch 4: outlying islands, separating transport, outreach, and small-island service rules.
- Batch 5: civil-society services, using official foundation/charity registries as the legitimacy baseline and public platforms only as candidate discovery.
