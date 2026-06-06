# Foundation Program Crawl Batch 4E - 2026-06-07

## Purpose

Batch 4E continues the review-first civil-society crawl from the official SFAA social-welfare foundation directory. This pass uses Batch H to scan the next unprocessed foundation websites after Batch A-G, then converts only pages that a resident, family caregiver, student, social worker, or frontline operator can use as a real welfare resource.

Formal cards are added only when the page gives a concrete service, subsidy, scholarship, eligibility clue, benefit item, application note, document rule, contact route, service area, or fee rule. Homepages, activity recaps, fundraising pages, transparency pages, annual reports, news-only pages, training-only pages, and broad unit-introduction pages remain candidate-only.

## Crawl Command

```powershell
python scripts/crawl_foundation_program_candidates.py --batch H --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --previous data/foundation-program-candidates-batch-g.json --limit 30 --out data/foundation-program-candidates-batch-h.json
```

## Crawl Result

- Selected foundations: 9
- Websites attempted: 9
- Websites with candidates: 7
- Pages fetched: 33
- Candidate pages: 17
- High-confidence candidates: 14
- Medium-confidence candidates: 3
- Low-confidence candidates: 0
- Crawl errors: 1

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0223-candidate-abc7d406ea81` | 育田脆弱癌友家庭扶助計畫 | https://www.mercyland.org.tw/?page_id=269 |
| `sfaa-foundation-a0223-candidate-127d72d00a4d` | 育田癌友家庭子女育秧獎助學金 | https://www.mercyland.org.tw/?page_id=4252 |
| `sfaa-foundation-d0003-candidate-0b1be0e7d2ae` | 心德慈化教養院成人心智障礙住宿照顧與諮詢服務 | https://www.sinte.org/m2/m.php?id=1&mid=1&m2id=70&category=x |
| `sfaa-foundation-d0003-candidate-b73f614cba19` | 心德慈化教養院憨老服務 | https://www.sinte.org/m2/m.php?id=1&mid=2&m2id=7&category=x |
| `sfaa-foundation-d0001-candidate-770c492f8098` | 台灣盲人重建院視障生活重建服務 | https://www.ibt.org.tw/RWD01/List.aspx?tid=86 |
| `sfaa-foundation-a0095-candidate-ad308abaabfa` | 育成永明發展中心成人日間照顧服務 | https://www.ycswf.org.tw/branch_detail/14 |
| `sfaa-foundation-a0099-candidate-ee737e2b1774` | 華山三失長輩到宅服務 | https://www.elder.org.tw/contents/text?id=25 |

## Review Notes

- 育田兩個115年度頁面 were converted because they provide current-year periods, eligibility, amounts or service items, documents, application path, and contact rules. The cancer-family assistance card is explicitly marked as professional-referral only.
- 心德服務概況 and 憨老服務 pages were converted because they identify target groups, residential care, professional consultation, aging disability support, family support, and contact routes.
- 台灣盲人重建院 was converted from the service-point candidate using a reviewed service-page override so the public source points to the life-reconstruction page instead of a generic contact page.
- 育成 and 華山 were converted with reviewed service-page overrides because the candidate crawl found broader pages, while the verified service pages provide clearer resident-facing eligibility and service details.

## Kept Candidate-Only

- 聖道兒少福利基金會 homepage, 育成 homepage/about pages, 華山 homepage/news pages, 公益傳播 homepage, and 台灣盲人重建院 activity news stayed candidate-only because they are not application-ready resource pages by themselves.
- 心德 donation, subsidy ledger, and disclosure pages stayed candidate-only because they are governance or donation records rather than resident-facing welfare resources.
- 台灣盲人重建院 vocational training pages have useful current-year signals, but this pass converted only the broader life-reconstruction service card to avoid over-counting one provider until the exact course intake details are reviewed separately.
- 中國國民黨身心障礙者保護基金會 website failed DNS lookup during the crawl and remains unconverted.

## Data Changes

- `data/foundation-program-candidates-batch-h.json` stores Batch H candidate crawl output and remains non-public by default.
- `data/formal-program-allowlist.json` now has 66 reviewed program cards, up from 59.
- Public records should increase from 505 to 512 after rebuild.
- `scripts/convert_candidate_programs.py` now supports a reviewed `sourceUrl` override for cases where the candidate proves the foundation but a more precise service page should be the public source.
- GitHub Actions now includes Batch H when converting reviewed foundation program pages.
