# Foundation Program Crawl Batch C - 2026-06-05

## Purpose

Batch C continues the review-first civil-society crawl. The crawler used the official SFAA social-welfare foundation directory as the foundation legitimacy baseline, then inspected foundation websites for pages that can become citizen-facing resource cards.

Formal cards are added only when the page is useful for public lookup: it must show a specific service, subsidy, application rule, intake path, eligibility clue, documents, or a service page that a resident or frontline worker can act on. Homepages, activity recaps, annual reports, fundraising pages, and generic news remain candidate-only.

## Crawl Command

```powershell
python scripts/crawl_foundation_program_candidates.py --batch C --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --only-current-year --limit 30 --out data/foundation-program-candidates-batch-c.json
```

## Crawl Result

- Selected foundations: 30
- Websites attempted: 30
- Websites with candidates: 23
- Pages fetched: 111
- Candidate pages: 63
- High-confidence candidates: 49
- Medium-confidence candidates: 13
- Low-confidence candidates: 1
- Crawl errors: 11

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0285-candidate-a0d6c6c1aa67` | 墨仙急難救助金 | https://www.moxian.org/service1.html |
| `sfaa-foundation-a0285-candidate-d064d45f6df5` | 墨仙小樹苗成長方案 | https://www.moxian.org/service2.html |
| `sfaa-foundation-a0106-candidate-31317b5b1e92` | 勵馨親密關係暴力／家庭暴力被害人服務 | https://www.goh.org.tw/services/intimate-violence/ |
| `sfaa-foundation-a0106-candidate-e2c62d99e2a3` | 勵馨性暴力防治服務 | https://www.goh.org.tw/services/prevention/ |
| `sfaa-foundation-a0106-candidate-6e18e3b42a09` | 勵馨兒童與青少年服務 | https://www.goh.org.tw/services/children-youth/ |
| `sfaa-foundation-a0203-candidate-8be1c3936e2c` | 瑪喜樂身心障礙者就業服務 | https://www.joyce929.org.tw/OnePage.aspx?tid=199 |
| `sfaa-foundation-a0283-candidate-470a7eb02f58` | 脊髓損傷家庭經濟協助 | https://www.scif.org.tw/article.php?lang=tw&tb=3&cid=71 |
| `sfaa-foundation-a0186-candidate-a41968fd1d3d` | 弘道老人福利基金會長者服務 | https://www.hondao.org.tw/service |

## Review Notes

- 墨仙 pages have the strongest application detail in this batch. The emergency relief page has concrete referral rules, required documents, and benefit categories; the small-tree program page has a 115年度 intake period and unit-level application requirements.
- 勵馨 pages are service pages, not cash subsidy pages. They are still valuable because protection-service users and frontline workers need a clear path for safety planning, legal, housing, counseling, placement, pregnancy/youth parent, and employment support.
- 瑪喜樂 is a concrete disability employment service page with vocational evaluation, supported employment, workplace development, and training content.
- 脊髓損傷家庭經濟協助 is a concrete emergency assistance page with time limit, same-cause rule, and assistance categories.
- 弘道 is a broader service overview. It was converted because it is a usable gateway for elder-service lookup, but card language makes clear that individual plan eligibility, service area, and quota must be confirmed.

## Kept Candidate-Only

- Activity recap pages and photo/news pages, because they do not tell a resident how to apply or what support is available now.
- Annual work-plan, budget, or public-accountability pages, because they are organization transparency documents rather than service entry points.
- Internship or volunteer recruitment pages, because the service target is not a welfare recipient.
- Generic homepages and news index pages, unless the page itself clearly functions as a service entry point.

## Data Changes

- `data/foundation-program-candidates-batch-c.json` stores the candidate crawl output and remains non-public by default.
- `data/formal-program-allowlist.json` now has 30 reviewed program cards, up from 22.
- `scripts/convert_candidate_programs.py` now carries reviewed `applicationConditions`, `benefitItems`, and source-note fields into generated resource records.
- Related programs under a foundation card now expand in-page with `查看資源說明`, showing application conditions, benefit items, application notes, and a separate source-page link.
- Public records should increase from 468 to 476 after rebuild.

## Next Batch Candidates

Continue with another 30-foundation batch, but keep the same conversion gate. Good next targets are pages with explicit current-year intake, emergency relief, scholarships, assistive devices, home repair, caregiver support, and regional service centers. Avoid converting broad donation campaigns or impact reports without a service path.
