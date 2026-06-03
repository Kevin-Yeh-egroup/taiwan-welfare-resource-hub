# Completion Plan

This project now separates "complete enough for public navigation" from "exhaustive program-level crawl."

## Completed In This Pass

- Public production site is deployed through GitHub and Vercel.
- All 22 Taiwan county/city social welfare主管機關 entries are included as official local lookup windows.
- Major central social welfare, long-term care, health insurance subsidy, employment, and disability employment portals are included.
- Tainan open-data welfare-map rows are imported as individual resource cards.
- Sources keep freshness policy and remain under scheduled GitHub Actions checks.

## What "Complete" Means For V1

V1 is complete when a resident in any Taiwan county/city can:

1. Search by everyday need.
2. Find the official local social welfare office for their jurisdiction.
3. Find national hotlines and central portals for common cross-county needs.
4. See whether a source is an official entry, checked source, or needs review.
5. Follow a source URL to the government or official resource owner.

## Remaining Work For Exhaustive V2

- Import the missing DOCX/PDF source documents after they are placed in `source-docs/`.
- Replace official-entry records with program-level rows when a county/city publishes reliable open data.
- Add per-program eligibility normalization and application-document extraction.
- Add map display for records with latitude/longitude.
- Add manual review workflow for pages that block automated fetching, use non-HTML app shells, or require certificate handling.

## Current Limitation

The user-provided source files were listed in the conversation but were not present at the local `Downloads` paths or in `source-docs/` during this pass. The repository records that limitation and can rerun extraction once the files are available.
