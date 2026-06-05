# Foundation Program Crawl Batch 4B - 2026-06-05

## Purpose

Batch 4B continues the review-first civil-society crawl from the official SFAA social-welfare foundation directory. This pass had two tracks:

- Batch D: continue only foundations with current-year signals.
- Batch E: continue operating foundations even when a page does not clearly expose a 115年度/2026 marker, then keep weaker pages candidate-only unless a resident can act on them.

Formal cards are added only when the page gives a usable service, subsidy, eligibility clue, benefit item, application path, document rule, contact path, or service area. Activity recaps, homepages, generic news, donation pages, and paused programs remain candidate-only.

## Crawl Commands

```powershell
python scripts/crawl_foundation_program_candidates.py --batch D --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-d.json
python scripts/crawl_foundation_program_candidates.py --batch E --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --limit 30 --out data/foundation-program-candidates-batch-e.json
```

## Crawl Result

Batch D:

- Selected foundations: 3
- Websites attempted: 3
- Websites with candidates: 2
- Pages fetched: 13
- Candidate pages: 6
- High-confidence candidates: 6
- Crawl errors: 0

Batch E:

- Selected foundations: 30
- Websites attempted: 30
- Websites with candidates: 24
- Pages fetched: 114
- Candidate pages: 65
- High-confidence candidates: 55
- Medium-confidence candidates: 6
- Low-confidence candidates: 4
- Crawl errors: 3

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-d0006-candidate-75642a798b70` | 桃園市身心障礙者恆愛日間托育服務中心 | https://www.vtcidd.org/OnePage.aspx?mid=50&id=17 |
| `sfaa-foundation-d0006-candidate-b392c5cefa53` | 桃園市身心障礙者服務中心 | https://www.vtcidd.org/OnePage.aspx?mid=51&id=18 |
| `sfaa-foundation-d0006-candidate-7d2679360efc` | 啟智技藝訓練中心楊梅服務區 | https://www.vtcidd.org/OnePage.aspx?mid=48&id=15 |
| `sfaa-foundation-a0196-candidate-034ead9def9a` | 聖島助學專案 | https://www.saint-island-charity.org/Allowance/Allowance_01.aspx |
| `sfaa-foundation-a0196-candidate-83a2fc5a3a89` | 聖島雪炭專案 | https://www.saint-island-charity.org/Allowance/Allowance_02.aspx |
| `sfaa-foundation-a0136-candidate-b8df06d012d9` | 兆豐慈善急難救助與醫療補助 | https://www.megacharity.org.tw/CharityCare?ID=5 |
| `sfaa-foundation-a0038-candidate-4c33f0e877fa` | 興毅基金會社會救助服務 | https://www.shingyifundweb.org/category/service/social-assistance-service |

## Review Notes

- 啟智技藝訓練中心 pages are concrete service pages with service object, capacity, content, center contact, and 2026 site footer signals.
- 聖島助學 and雪炭 pages are actionable because they explain target families, possible subsidy items, required documents, and the common referral-first application path.
- 兆豐慈善 has clear application method rules: institution referral only, no personal application, required forms, and registered mail. Benefit language uses example ranges only where the source shows actual cases.
- 興毅社會救助 is actionable because it states the referral units and required referral/application forms, plus food-bank and rural emergency service areas.

## Kept Candidate-Only

- 久鑫公益基金會 pages were not converted because the download page shows 2026/115 materials but also says applications are temporarily paused.
- Broad social-vote, event, news, activity, donation, and transparency pages were kept candidate-only because they do not tell a resident how to apply for help now.
- Thin application-form pages without eligibility, benefit, intake, or service-area context were kept candidate-only until a better page is found.

## Data Changes

- `data/foundation-program-candidates-batch-d.json` and `data/foundation-program-candidates-batch-e.json` store candidate crawl output and remain non-public by default.
- `data/formal-program-allowlist.json` now has 37 reviewed program cards, up from 30.
- Public records should increase from 476 to 483 after rebuild.
- The homepage status block now shows current counts for public central resources, public local resources, and civil-society resources.
