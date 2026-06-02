# Research Notes

Research date: 2026-06-02.

## Direction

The directory should not be a prose archive. It should behave like a public service finder:

- search by everyday words;
- browse by need and life situation;
- filter by city, district, audience, service category, and freshness;
- show "who this helps", "what you can get", "how to apply", "what to prepare", and "who to contact";
- keep source evidence and update state visible.

## Why This Structure

Open Referral HSDS models human services as organizations, services, locations, and service-at-location records. This prevents the common problem where one agency page hides several different services, locations, eligibility rules, or phone numbers.

Findhelp's public search pattern points to location-first search, category browsing, personal filters, program filters, income eligibility filters, and persistent selected filters.

Government design-system guidance for filters emphasizes using filters only when they are genuinely needed, showing selected filters, and supporting removal of filters.

Inform USA standards emphasize update verification procedures, database curator review, interim updates between annual verification, and alternate verification methods when providers do not respond.

Taiwan examples show the same direction:

- MOHW e寶箱 describes a user-centered, theme-based, audience-based integrated service portal.
- Tainan publishes a social welfare map dataset with JSON fields for name, coordinates, address, phone, URL, target audience, service type, district, and content.
- Tainan's map UI exposes service audience, service category, item, district, and search radius.
- Taichung's welfare resource network links people to service centers, welfare stations, disability daily-life resources, and current resource locations.
- Taipei's map example frames resources as map-based lookup for welfare facilities by everyday needs.

## Implementation Implications

- Keep both a card list and map-ready coordinates where available.
- Prefer official open data and APIs over page scraping.
- Do not hide stale state. A stale but source-backed record is safer than a confident-looking card without dates.
- Treat December and January as high-risk update windows.
- Keep crawler output reviewable before publication.
