# Project Rules

This repository is a public-facing Taiwan social welfare resource directory.

## Safety

- Do not commit secrets, private source documents, raw personal data, or downloaded government files unless Kevin explicitly approves.
- Keep review-stage noindex controls in place until Kevin approves search indexing.
- Crawlers must use an allowlist, rate limits, and source evidence. Do not bypass robots.txt, login walls, CAPTCHA, or paywalls.
- Treat scraped content as "needs verification" unless an official open-data API or source timestamp confirms freshness.

## Data Quality

- Every resource should keep source URL, source organization, last checked date, and a freshness status.
- Prefer structured data from official open-data portals over scraping prose pages.
- Keep citizen-facing copy short: who it helps, what it offers, where it applies, how to apply, what to prepare, who to contact.

## Deployment

- GitHub repo creation, pushing, Vercel linking, Production deploys, and removing noindex require Kevin approval.
- The scheduled GitHub Action is a draft until the repository is pushed and Actions are enabled.
