# Data Model

The public UI uses a simplified citizen-facing record while keeping enough fields to map later into Open Referral HSDS.

## Core Fields

- `id`: stable local id.
- `name`: citizen-facing resource name.
- `summary`: one sentence saying what help is available.
- `provider`: agency, NGO, facility, or dataset owner.
- `jurisdiction`: nationwide, county/city, or district.
- `county`, `districts`: geography filters.
- `audiences`: people the resource is intended for, such as older adults, children, disabled people, caregivers, low-income households.
- `serviceCategories`: need-based categories, such as food, housing, care, cash support, employment, transport, legal, safety.
- `needTags`: everyday words people may search.
- `eligibility`: short plain-language eligibility summary.
- `howToApply`: action steps or contact path.
- `documents`: likely documents to prepare, if known.
- `contact`: phone, address, website, opening notes.
- `source`: source URL, source type, source organization.
- `freshness`: last checked date, source updated date, confidence, and notes.
- `applicationConditions`: citizen-facing "申請條件" blocks. Use this when a source has clear eligibility rules.
- `benefitItems`: citizen-facing "補助項目與金額" blocks. Use exact amounts when the official source gives them; otherwise state the official basis for local or case-by-case calculation.
- `incomeStandardGroups`: structured income/asset/real-estate standard tables, currently used for 115年度低收入戶 and 中低收入戶 standards.

## Detail Overrides

`data/resource-detail-overrides.json` preserves manually reviewed, citizen-facing details after each source crawl. `scripts/crawl_sources.py` merges overrides by record id after importing allowlisted sources.

Use overrides for stable interpretation layers such as:

- application conditions;
- benefit amounts and calculation notes;
- application caveats;
- current-year freshness evidence.

Do not use overrides to bypass source evidence. Each override should still keep source URLs and source dates where available.

## HSDS Mapping

- `provider` maps toward HSDS `organization`.
- `name`, `summary`, `eligibility`, `serviceCategories`, `audiences`, `howToApply` map toward HSDS `service`.
- `contact.address`, `contact.phone`, latitude, longitude, and districts map toward HSDS `location`, `phone`, `address`, and `service_area`.
- `source` and `freshness` map toward HSDS `metadata`.

The first release keeps records denormalized for public readability. A future exporter can generate HSDS JSON or CSV once the source corpus is stable.
