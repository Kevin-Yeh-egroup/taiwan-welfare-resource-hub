# Foundation Program Crawl Batch 4C - 2026-06-05

## Purpose

Batch 4C continues the review-first civil-society crawl from the official SFAA social-welfare foundation directory. This pass uses Batch F to scan the next operating foundation websites after Batch A-E, then converts only pages that a resident, social worker, or frontline operator can use as a real welfare resource.

Formal cards are added only when the page gives a concrete service, subsidy, eligibility clue, benefit item, application note, document rule, contact route, or service area. Generic homepages, activity recaps, fundraising pages, transparency pages, news, volunteer recruitment, and broad unit-introduction pages remain candidate-only.

## Crawl Command

```powershell
python scripts/crawl_foundation_program_candidates.py --batch F --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --limit 30 --out data/foundation-program-candidates-batch-f.json
```

## Crawl Result

- Selected foundations: 30
- Websites attempted: 30
- Websites with candidates: 22
- Pages fetched: 116
- Candidate pages: 63
- High-confidence candidates: 53
- Medium-confidence candidates: 7
- Low-confidence candidates: 3
- Crawl errors: 8

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0168-candidate-34af127abfa6` | 漢慈兒少生活陪讀服務 | http://www.hfoundation.org.tw/service-children/ |
| `sfaa-foundation-a0309-candidate-5a8e5befebc6` | 基督徒救世會婦幼家庭關懷服務 | https://www.csstpe.org.tw/List.aspx?mid=50 |
| `sfaa-foundation-a0238-candidate-80ac46eb7164` | 信義公益基金會急難救助 | https://www.sinyicharity.org.tw/assistance |
| `sfaa-foundation-a0055-candidate-d6be38ea763b` | 善牧家庭暴力保護服務 | https://www.goodshepherd.org.tw/contents/text?id=49 |
| `sfaa-foundation-a0055-candidate-ee54b88868a1` | 善牧兒童保護與支持服務 | https://www.goodshepherd.org.tw/contents/text?id=48 |
| `sfaa-foundation-a0201-candidate-6a424369cdcd` | 台灣關愛基金會文山婦幼服務中心 | https://www.twhhf.org/zh-hant/service/123 |
| `sfaa-foundation-a0148-candidate-8aa845f65fa5` | 華科聽覺照顧獎補助學金 | https://www.psa.org.tw/services-2/hear-2/subsidy_scholarship/ |
| `sfaa-foundation-a0140-candidate-74888132fe95` | 全聯物資銀行身心障礙及婦女服務類 | https://www.pxmart.org.tw/project/2/4 |
| `sfaa-foundation-a0266-candidate-f2ff897a6dff` | 業成員工愛心基金補助計畫 | https://www.gisfoundation.org.tw/service06.html |
| `sfaa-foundation-b0009-candidate-a9a8794d9120` | 永信社會福利基金會長照與社區照顧服務 | https://www.ysswf.com/service.php |

## Review Notes

- 漢慈、救世會、善牧、關愛基金會 pages are concrete family, children, women, or protection-service pages with target groups and service content a frontline operator can match.
- 信義急難救助 is actionable because it explains aid categories, referral path, and application timing rules; it is not presented as direct personal self-application.
- 華科, 全聯, and 業成 pages are actionable because they include subsidy, partnership, scholarship, or application-period information, even though the actual route may require organization-level or annual intake confirmation.
- 永信服務項目 page is included as a long-term/community care service card because it lists specific service lines such as A-unit coordination, residential care, day care, home service, and other community-care programs.

## Kept Candidate-Only

- Older or static pages without clear current intake, such as thin legacy pages, were kept candidate-only until a current service page is found.
- Broad service directories, homepages, contact pages, news, outcomes, fundraising, financial disclosure, and volunteer pages were not converted because they do not tell a resident how to use a welfare resource.
- Unit-level pages that describe an organization but do not provide eligibility, service content, amount, intake, or application clues were kept candidate-only.

## Data Changes

- `data/foundation-program-candidates-batch-f.json` stores Batch F candidate crawl output and remains non-public by default.
- `data/formal-program-allowlist.json` now has 47 reviewed program cards, up from 37.
- Public records should increase from 483 to 493 after rebuild.
- GitHub Actions now includes Batch F when converting reviewed foundation program pages.
