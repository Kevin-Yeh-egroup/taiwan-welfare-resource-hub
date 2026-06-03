# Foundation Program Crawl Batch A - 2026-06-03

This batch extends the SFAA foundation registry crawl from organization-level records into foundation website pages.

## Scope

- Source base: SFAA-imported foundation records in `data/resources.json`.
- Batch size: 30 foundation websites.
- Selection rule: real organization website, then prioritize 2026 source updates, high-demand service categories, and recognizable national foundations.
- Crawl limits: robots-aware, max 6 pages per site, max 3 candidate pages per foundation, review-only output.
- Output: `data/foundation-program-candidates.json`.

## Result

- Selected foundations: 30.
- Pages fetched: 109.
- Candidate pages: 60.
- Foundations with at least one candidate: 23.
- Confidence labels: 56 high, 3 medium, 1 low.
- Errors: 4 websites/pages failed because of timeout or closed connection.

## Examples Of Strong Candidates

| Foundation | Candidate page | Why it matters |
| --- | --- | --- |
| 財團法人萬海航運社會福利慈善事業基金會 | https://wanhai-charity.org.tw/emergency-application/ | Direct emergency aid application page. |
| 財團法人台灣兒童暨家庭扶助基金會 | https://www.ccf.org.tw/service/domestic/61d7d3917b3ca | Poverty-related child/youth family support service page. |
| 財團法人愛盲基金會 | https://www.tfb.org.tw/contents/text?id=113 | Scholarship/resource application page for visually impaired people. |
| 財團法人永大社會福利基金會 | https://yungtay.org/socialwelfare/ | Social-welfare service page with high service keyword density. |
| 財團法人富邦慈善基金會 | https://www.fuboncharity.org.tw/chinese/help/info | Assistance information page. |

## Crawl Failures

These are not data failures; they are website access failures in this run and can be retried in a later batch.

- 財團法人國泰人壽慈善基金會: website timed out.
- 財團法人中視慈善愛心基金會: remote end closed connection.
- 財團法人群馨慈善事業基金會: website timed out.
- 財團法人為恭社會福利基金會: website timed out.

## Quality Gate

This batch is intentionally not merged into `data/resources.json`.

Candidate pages are not yet public resource cards. Before conversion, each page needs manual or stronger rule-based review for:

- current-year intake or program validity;
- eligibility;
- application steps;
- required documents;
- contact channel;
- whether the page is a donation/fundraising page rather than a service for residents.

The validator enforces `mode: candidate-only`, `reviewStatus: candidate-review-required`, and `canConvertToResource: false`.
