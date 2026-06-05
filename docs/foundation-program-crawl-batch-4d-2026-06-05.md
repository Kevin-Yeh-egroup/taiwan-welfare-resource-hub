# Foundation Program Crawl Batch 4D - 2026-06-05

## Purpose

Batch 4D continues the review-first civil-society crawl from the official SFAA social-welfare foundation directory. This pass uses Batch G to scan the next operating foundation websites after Batch A-F, then converts only pages that a resident, family caregiver, social worker, or frontline operator can use as a real welfare resource.

Formal cards are added only when the page gives a concrete service, subsidy, eligibility clue, benefit item, application note, document rule, contact route, service area, or fee rule. Generic homepages, activity recaps, fundraising pages, transparency pages, annual reports, news, training-only pages, and broad unit-introduction pages remain candidate-only.

## Crawl Command

```powershell
python scripts/crawl_foundation_program_candidates.py --batch G --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --limit 30 --out data/foundation-program-candidates-batch-g.json
```

## Crawl Result

- Selected foundations: 30
- Websites attempted: 30
- Websites with candidates: 22
- Pages fetched: 116
- Candidate pages: 61
- High-confidence candidates: 53
- Medium-confidence candidates: 7
- Low-confidence candidates: 1
- Crawl errors: 6

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0013-candidate-34e878262b7e` | 中華文化台北兒童福利中心 | https://www.ccswf.org.tw/ChcfPortal/institution/childWelfare.do |
| `sfaa-foundation-a0013-candidate-4794b07d535c` | 中華文化翠柏新村老人安養與長照服務 | https://www.ccswf.org.tw/ChcfPortal/institution/elderlyCare.do |
| `sfaa-foundation-a0282-candidate-67fe0eebf45a` | 婦聯聽覺健康臺北市聽覺生活重建與家庭支持服務 | https://dosw.gov.taipei/cp.aspx?n=58AD92A8DB2B1952 |
| `sfaa-foundation-a0325-candidate-2eac3aadc0f0` | 台灣賽珍珠新住民子女及家庭服務 | https://www.psbf.org.tw/OnePage.aspx?mid=66&id=61 |
| `sfaa-foundation-a0325-candidate-a1b4382d49a1` | 賽珍珠桃園市南區新住民家庭服務中心 | https://www.psbf.org.tw/OnePage.aspx?mid=96&id=243 |
| `sfaa-foundation-b0026-candidate-9e2651ce416b` | 毓得老人關懷與臺中長照交通接送服務 | https://www.yude.org.tw/productClassify/tws_txt/index/1000029600 |
| `sfaa-foundation-a0031-candidate-6b17801ca4b1` | 陽光燒傷顏損重建服務 | https://www.sunshine.org.tw/service/index/all |
| `sfaa-foundation-a0225-candidate-464d2818be8c` | 老五老社區餐食與交通接送服務 | https://www.ofo.org.tw/service/generational |
| `sfaa-foundation-a0225-candidate-333bb3fee81a` | 老五老居家照顧與喘息服務 | https://www.ofo.org.tw/service/pro |
| `sfaa-foundation-a0078-candidate-b300ddc97406` | 心路早期療育服務 | https://www.syinlu.org.tw/service/service_item/1 |
| `sfaa-foundation-a0078-candidate-1492027b9cc4` | 心路智能障礙者照顧服務 | https://www.syinlu.org.tw/service/service_item/7 |
| `sfaa-foundation-a0100-candidate-cb4a2923b6bc` | 喜憨兒心智障礙照顧服務 | https://www.c-are-us.org.tw/service/care_service |

## Review Notes

- 中華文化、婦聯聽覺健康、賽珍珠、毓得、陽光、老五老、心路、喜憨兒 pages were converted because they describe concrete services or fee/eligibility clues that people can use for referral and first-step inquiry.
- 毓得 was included because the page gives long-term-care transportation pickup areas and fee tiers for low-income, mid-low-income, and general users.
- 婦聯聽覺健康 was mapped through the Taipei Department of Social Welfare service page because the official city page gives the disability category, service items, and contact route for the commissioned provider.
- Several services are not cash subsidies. Their benefit sections therefore use service/fee language and tell the user to confirm final fees, subsidy identity, quota, and intake with the service unit.

## Kept Candidate-Only

- 三立慈善基金會, 王月蘭慈善基金會, 台灣基督教福利會, 微風慈善基金會, 全聯佩樺圓夢社福基金會, and 創世社會福利基金會 generic home, contact, news, annual activity, wish, or explanation pages stayed candidate-only because they do not provide a current direct resource card by themselves.
- 第一社福 training news, admission lists, course pages, and outcome recaps stayed candidate-only because they are event or training administration pages rather than resident-facing welfare resources.
- 黃烈火社會福利基金會 transparency, budget, ledger, and annual report pages stayed candidate-only because they are governance disclosures, not application-ready services.
- 創世政府補助説明 stayed candidate-only because it explains public subsidy rules and risks duplicating existing public benefit cards without adding a foundation-run intake route.

## Data Changes

- `data/foundation-program-candidates-batch-g.json` stores Batch G candidate crawl output and remains non-public by default.
- `data/formal-program-allowlist.json` now has 59 reviewed program cards, up from 47.
- Public records should increase from 493 to 505 after rebuild.
- GitHub Actions now includes Batch G when converting reviewed foundation program pages.
