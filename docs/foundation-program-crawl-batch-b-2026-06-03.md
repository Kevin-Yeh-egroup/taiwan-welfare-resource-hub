# Foundation Program Crawl Batch B - 2026-06-03

Batch B continues the review-first foundation website crawl after Batch A.

## Scope

- Source base: SFAA-imported foundation records in `data/resources.json`.
- Exclusion: foundations already selected in `data/foundation-program-candidates.json`.
- Selection filter: SFAA `sourceUpdatedAt` in 2026 and a real organization website, excluding SFAA fallback pages.
- Batch size: 30 foundation websites.
- Crawl limits: robots-aware, max 6 pages per site, max 3 candidate pages per foundation.
- Output: `data/foundation-program-candidates-batch-b.json`.

## Result

- Selected foundations: 30.
- Pages fetched: 133.
- Candidate pages: 69.
- Foundations with at least one candidate: 23.
- Confidence labels: 56 high, 9 medium, 4 low.
- Candidate types: 56 official-service-page, 7 news-or-activity, 6 possible-program-page.
- Errors: 6 websites failed because of closed connection, timeout, 404, or DNS failure.
- Combined Batch A + B candidate pages: 129.
- Batch A/B foundation overlap: 0.

## Examples Of Strong Candidates

| Foundation | Candidate page | Why it matters |
| --- | --- | --- |
| 財團法人天主教失智老人社會福利基金會 | https://www.cfad.org.tw/service/32 | Dementia and elderly service page. |
| 財團法人切膚之愛社會福利慈善事業基金會 | https://www.sgwlf.org.tw/service.php?cID=5 | Long-term care/social-welfare service category page. |
| 財團法人利河伯社會福利基金會 | https://www.rehoboth-welfare.org.tw/OnePage.aspx?mid=33&id=42 | Scholarship/application page. |
| 財團法人門諾社會福利慈善事業基金會 | https://www.mf.org.tw/official/service?equal%5Bclassid%5D=1 | Foundation service page. |
| 財團法人中國信託慈善基金會 | https://www.ctbcfoundation.org/taiwan-dream/index.aspx | Child/youth community support project page. |
| 財團法人陳綢阿嬤社會福利基金會 | https://lst.org.tw/%E6%9C%8D%E5%8B%99%E5%85%A7%E5%AE%B9/%E9%99%B3%E7%B6%A2%E5%85%92%E5%B0%91%E4%B8%AD%E5%BF%83/%E5%85%92%E7%AB%A5%E6%9C%8D%E5%8B%99/ | Child and family service page. |

## Crawl Failures

These are website access failures, not rejected welfare records.

- 財團法人伊甸社會福利基金會: remote host forcibly closed connection.
- 財團法人台灣獅子會基金會: remote end closed connection.
- 財團法人新聯陽社會福利慈善事業基金會: official registry URL returned 404.
- 財團法人台灣之愛社會福利慈善公益事業基金會: website timed out.
- 財團法人明緯公益基金會: website returned 404.
- 財團法人玉山志工社會福利慈善事業基金會: DNS lookup failed.

## Quality Gate

Batch B remains candidate-only. It does not change `data/resources.json`.

Before converting any candidate into a public resource card, review:

- whether the page is service-facing rather than donation/fundraising-facing;
- current-year intake or validity;
- eligibility and service area;
- application steps and documents;
- contact channel;
- whether the page is a broad project page that needs a more specific subpage.

The validator now checks all `data/foundation-program-candidates*.json` files.
