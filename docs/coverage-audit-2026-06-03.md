# Coverage Audit - 2026-06-03

This audit checks the current V1 resource hub against official Taiwan welfare sources, with emphasis on central resources, county/city coverage, and common questions from economically vulnerable residents.

## Current Coverage

- Current dataset after Batch 3B southern/eastern local expansion: 459 resource records, 83 sources.
- County/city coverage: all 22 Taiwan county/city social welfare authorities are present as official local-government entry records.
- Central coverage already present: MOHW welfare e-box, 1957 welfare hotline, MOHW low-income/middle-low-income page, 115 annual low-income/middle-low-income standards, low-income/middle-low-income FAQ, emergency assistance, social welfare service centers/social safety net, 1966 long-term care, NHI premium subsidy dataset, TaiwanJobs, disability employment resources.
- Batch 0/1 central additions: national pension premium subsidy, special-circumstances families, disability welfare, childcare and parenting support, elder welfare, education tuition reduction, labor subsidy and employment support, 115 central rent subsidy, and 113 protection hotline.
- Batch 2 local additions: 12 program-level six-municipality cards across Taipei, New Taipei, Taoyuan, Taichung, Tainan, and Kaohsiung.
- Batch 3A local additions: 12 program-level cards across Keelung, Hsinchu City, Hsinchu County, Miaoli, Changhua, Nantou, and Yunlin.
- Batch 3B local additions: 12 program-level cards across Chiayi City, Chiayi County, Pingtung, Yilan, Hualien, and Taitung.
- Civil-society coverage now includes the SFAA official directory of national social-welfare foundations: 355 foundation records.

## Main Finding

V1 is complete as an official-entry directory, but not yet complete as a resident-ready welfare answer tool.

The largest gap is not missing county governments. The gap is that many high-frequency questions are only reachable through broad portals, not as direct resource cards with current-year eligibility, documents, application location, and action wording.

## High-Priority Missing Or Thin Central Records

| Priority | Missing or thin resource | Why it matters | Official source checked |
| --- | --- | --- | --- |
| P0 | 115年度低收入戶、中低收入戶資格審核標準 | Residents ask "do I qualify this year?" before they know which office to call. This should be a standalone, searchable card. | https://dep.mohw.gov.tw/dosaasw/fp-566-84223-103.html |
| P0 | Social assistance FAQ for low-income/middle-low-income applications | Explains income threshold logic, documents, actual residence requirement, review process, and appeal. Current site only points to the broad page. | https://dep.mohw.gov.tw/dosaasw/cp-572-5035-103.html |
| P0 | Emergency assistance / urgent relief | Economic-crisis users often need immediate aid, not annual qualification identity. | https://www.mohw.gov.tw/cp-190-226-1.html |
| P0 | Social welfare service centers / social safety net | Useful when the user has multiple problems and does not know which single subsidy applies. | https://mohw.gov.tw/ss/cp-4530-50091-204.html |
| P1 | National Pension premium subsidy and 115 premium amounts | Low-income and middle-low-income status affects national pension premium burden. | https://dep.mohw.gov.tw/DOSI/cp-308-602-102.html |
| P1 | Low-income and middle-low-income housing subsidy | Housing/rent is a common pressure point and is cross-ministry, so users may not find it through MOHW alone. | https://www.nlma.gov.tw/ch/legislation/regsearch/1250 |
| P1 | Special circumstances family assistance | Important for single-parent, domestic violence, bereavement, pregnancy, and sudden-crisis households. | https://dep.mohw.gov.tw/DOPS/cp-1287-14940-105.html |
| P1 | Disability welfare page and assistive-device resources | Current dataset has county entries and disability employment, but not a citizen-friendly central disability welfare card. | https://www.mohw.gov.tw/cp-88-235-1.html |
| P1 | Childcare services and childcare subsidy | Parents often search by "托育", "育兒", "保母", not by social bureau name. | https://mohw.gov.tw/fp-88-230-1.html |
| P2 | Elderly welfare and middle-low-income elderly living allowance | Existing long-term-care card is not enough for cash allowance and elderly local resource questions. | https://www.mohw.gov.tw/cp-88-224-1.html |
| P2 | My E-Government local application service pages | Some local low-income application pages contain documents, processing time, and office contacts; coverage is uneven but useful for V2. | https://www.gov.tw/ |

## Low-Income / Middle-Low-Income Current-Year Finding

The current hub has a "低收入戶及中低收入戶" card, but it does not expose the 115年度 thresholds directly.

For 115年度, MOHW publishes a one-page official standard table. It includes separate income, movable-property, and real-estate limits for Taiwan Province, Taipei, New Taipei, Taoyuan, Taichung, Tainan, Kaohsiung, and Fujian Province. The hub should make this visible as a table or calculator-like guide, with a clear warning that final review still depends on local government review and household composition.

## County / City Coverage Finding

No county/city social welfare authority is missing at the entry level.

What is still missing:

- direct low-income/middle-low-income application pages for each city/county or district office;
- local emergency assistance pages;
- local disability living allowance pages;
- local elderly living allowance pages;
- local special-circumstances family pages;
- local childcare and child/youth assistance pages;
- open-data rows outside Tainan where available.

The practical next step is not to add more generic county cards. It is to add program-level county cards only when the source page has specific application, eligibility, document, or contact details.

## Product / Usability Review

Current strengths:

- The first screen is a real search tool, not a landing page.
- Search works by everyday keywords and county/category filters.
- Cards have citizen-facing labels: who it is for, how to use, documents, contact, source.
- noindex review posture is correct for a public-but-not-final resource.

Current friction:

- Users who search "低收入戶資格", "115年低收標準", "急難救助", "租屋補助", "國民年金補助" may get broad portals instead of a direct answer.
- The "官方入口" status is honest, but ordinary users may perceive it as less helpful than "可直接申請 / 有年度標準 / 有電話".
- County cards are broad and repeated; they help coverage but can make the result list feel generic.
- There is no "我現在遇到什麼狀況?" guided path, such as "沒錢吃飯/繳房租", "想申請低收入戶", "突然失業或生病", "有小孩", "照顧老人/身障家人".

## Recommended V2

1. Add the remaining P1 central records as standalone cards before adding more local pages.
2. Add a "經濟弱勢快速入口" section above results with four paths: 低收/中低收資格, 急難救助, 房租/住宅, 保費/醫療.
3. Add a 115年度低收/中低收 threshold table and link to the MOHW PDF/source page.
4. Tag source types more clearly: "年度標準", "可申辦", "諮詢轉介", "地方入口", "開放資料".
5. For county V2, add local program cards only when a page has concrete details. Avoid duplicating broad bureau homepages.

## P0 Follow-Up Implemented

- Added standalone central cards for 115年度低收入戶/中低收入戶資格審核標準, low-income/middle-low-income FAQ, 急難救助, and 社會福利服務中心/社會安全網.
- Updated quick-search buttons toward economic-vulnerability questions: low-income/middle-low-income, 115 annual standard, emergency aid, social welfare center, premium subsidy, and civil-society foundations.
- Rebuilt the data pipeline with 459 records, 83 sources, 83 freshness URLs, and 0 freshness warnings after Batch 3B.

## SFAA Foundation Follow-Up Implemented

- Added the official SFAA source: https://swft.sfaa.gov.tw/fund/fh0300#
- Crawled the public list API and each public detail record, excluding embedded images and PDF bytes.
- Imported 355 national social-welfare foundations as citizen-facing cards with county, district, phone, email, website, service object, service type, status, source update date, and source notes.
- All 355 imported foundations were returned by the live 2026-06-03 official query with status `A`, mapped in the cards as "運作中".
- 163 of the 355 foundation records have a 2026 source update date; the latest observed source update was 2026-06-02.
- Important limitation: this confirms the foundation is listed as operating in the official registry. It does not guarantee every foundation currently has an open assistance program; users should confirm annual programs, quota, service area, and required documents from the foundation website or phone.
- Updated 桃園市政府社會局 from `http://sab.tycg.gov.tw/` to `https://sab.tycg.gov.tw/` to avoid scheduled freshness timeout.

## Batch 3B Follow-Up Implemented

- Added official local cards for Chiayi City, Chiayi County, Pingtung County, Yilan County, Hualien County, and Taitung County.
- The batch emphasizes resident-facing pages with current-year eligibility, subsidy amount, and application notes.
- Fixed the Taichung 115 low-income/middle-low-income annual-standard card to use the stable official article path and expose income, movable-property, and real-estate thresholds together.
- Remaining local expansion: Penghu, Kinmen, and Lienchiang, followed by deeper civil-society program confirmation.
