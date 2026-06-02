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

## HSDS Mapping

- `provider` maps toward HSDS `organization`.
- `name`, `summary`, `eligibility`, `serviceCategories`, `audiences`, `howToApply` map toward HSDS `service`.
- `contact.address`, `contact.phone`, latitude, longitude, and districts map toward HSDS `location`, `phone`, `address`, and `service_area`.
- `source` and `freshness` map toward HSDS `metadata`.

The first release keeps records denormalized for public readability. A future exporter can generate HSDS JSON or CSV once the source corpus is stable.
