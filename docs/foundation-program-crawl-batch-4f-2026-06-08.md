# Foundation Program Review Batch 4F - 2026-06-08

## Purpose

Batch 4F closes the first pass through SFAA foundation websites and continues review from the A-H candidate backlog. The goal is to publish only pages that ordinary residents, family caregivers, students, social workers, or frontline operators can use as real welfare resources.

Formal cards are added only when the page provides a concrete service, subsidy, aid category, eligibility clue, benefit item, application route, document rule, contact route, service area, or fee rule. Homepages, donation drives, activity recaps, transparency pages, news-only pages, old pages without an intake route, and pages that state intake is paused remain candidate-only.

## Crawl Command

```powershell
python scripts/crawl_foundation_program_candidates.py --batch I --previous data/foundation-program-candidates.json --previous data/foundation-program-candidates-batch-b.json --previous data/foundation-program-candidates-batch-c.json --previous data/foundation-program-candidates-batch-d.json --previous data/foundation-program-candidates-batch-e.json --previous data/foundation-program-candidates-batch-f.json --previous data/foundation-program-candidates-batch-g.json --previous data/foundation-program-candidates-batch-h.json --limit 30 --out data/foundation-program-candidates-batch-i.json
```

## Crawl Result

- Selected foundations: 0
- Websites attempted: 0
- Websites with candidates: 0
- Pages fetched: 0
- Candidate pages: 0
- High-confidence candidates: 0
- Medium-confidence candidates: 0
- Low-confidence candidates: 0
- Crawl errors: 0
- Interpretation: A-H already covered all 192 eligible foundation websites selected by the current priority rules. Batch I records that exhaustion point and keeps the run auditable.

## Converted To Public Cards

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0052-candidate-0f868ac833fc` | 張榮發慈善基金會個案救助 | https://www.cyff-charity.org.tw/zh-tw/help.php |
| `sfaa-foundation-b0017-candidate-b1edb6253a64` | 崇華堂急難、低收生活、助學與醫療補助 | https://caituanfarenchonghuatangshehuifulicishanshiyejijinhui4.webnode.tw/%E8%A3%9C%E5%8A%A9%E7%94%B3%E8%AB%8B%E8%BE%A6%E6%B3%95/ |
| `sfaa-foundation-a0163-candidate-de714b2974a5` | 義廷急難救助、低收扶助、醫療補助與清寒獎助學金表單 | https://www.eting.org.tw/download.html |
| `sfaa-foundation-a0001-candidate-e8e3122333b6` | 芥菜種會家的扶助兒少安置服務 | https://www.mustard.org.tw/OnePageTabPic.aspx?mid=67&id=57 |
| `sfaa-foundation-a0127-candidate-fceb1227947d` | 全成長照、身障評估與急難醫療扶助服務窗口 | http://www.homeservice.org.tw/ap/cust_view.aspx?bid=172 |

## Enriched Existing Card

| Candidate | Public card | Source |
| --- | --- | --- |
| `sfaa-foundation-a0120-candidate-cb6bb18de2b3` | 萬海急難救助與生活扶助 | https://wanhai-charity.org.tw/emergency-application/ |

The Wan Hai card already existed, so Batch 4F did not duplicate it. This pass expanded it with resident-facing conditions, benefit items, required documents, and the 2025-08-01 online-application rule.

## Review Notes

- 張榮發 was converted with a reviewed `sourceUrl` override from the candidate analysis page to the actual `我需要幫忙` application page. The card emphasizes that individual direct applications are not accepted and a recognized referral unit must sign or stamp the application.
- 崇華堂 was converted because the source lists aid categories, applicant groups, and documents for emergency relief, low-income living aid, student aid, and medical aid. The page is older, so the card explicitly tells users to confirm current intake before sending.
- 義廷 was converted as a form-entry resource. The source lists downloadable application forms and 2026 site footer/contact details, but does not publish complete thresholds or amounts, so the card is careful about confirmation before filing.
- 芥菜種會 was converted because the page gives an actual child/youth placement service, target ages, family dysfunction scenarios, service contents, and contact route. The site footer indicated an update through 2026-05-28 during review.
- 全成 was converted as a service-window card rather than a fixed cash-aid card. It is useful for Taichung-area long-term care, disability evaluation, community/day care, emergency aid, medical aid, and low-/middle-low-income aid routing, but all fees and eligibility must be confirmed with the relevant service point.
- 萬海 was enriched because the current source gives all-year intake, eligibility, benefit categories, transfer-unit rules, document requirements, and online filing notes.

## Kept Candidate-Only

- 林登山急難救助 stayed candidate-only for now because the page is useful but dates to 2016 and does not show a current-year intake rule. It may be reviewed later by phone or with a newer source.
- 久鑫救助/資料下載 stayed candidate-only because the source page states `暫停受理`, even though the site has 2026 public-information links.
- 富邦家庭照顧者喘息之旅 stayed candidate-only because the page is a 2026 activity/news recap for an event already held on 2026-05-15, not a currently open application route.
- 萬海 `2026 讓愛閃耀` stayed candidate-only because it is primarily a fundraising/designated-donation and organization-support project, not a direct resident-facing welfare resource.
- Several high-scoring homepages and disclosure pages stayed candidate-only because they point to organizations or reports rather than specific resident-facing service entry points.

## Data Changes

- `data/foundation-program-candidates-batch-i.json` stores the Batch I exhaustion run and remains non-public.
- `data/formal-program-allowlist.json` now has 71 reviewed program cards, up from 66.
- Public records should increase from 512 to 517 after rebuild.
- GitHub Actions and the README conversion command now include Batch I, even though it currently has zero candidates.
