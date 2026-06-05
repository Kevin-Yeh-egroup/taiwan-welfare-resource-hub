# Batch 3C Offshore Local Programs - 2026-06-05

This batch adds program-level local public resources for Taiwan's offshore counties: Penghu, Kinmen, and Lienchiang.

## Scope

- Penghu County, Kinmen County, and Lienchiang County.
- Nine cards total.
- Only official county/city, public-agency, or official local-law pages were used.
- Cards were added when the page gave concrete eligibility, benefit amount, application notes, or current-year evidence.

## Added Sources

| County | Added cards | Official source examples |
| --- | --- | --- |
| Penghu County | low/middle-low-income living assistance; emergency assistance; 115 after-school care subsidy for disadvantaged children | https://www.penghu.gov.tw/society/home.jsp?act=view&dataserno=201309260005&id=234 |
| Kinmen County | 115 low-income living assistance; emergency assistance; pre-registration new immigrant social assistance | https://social.kinmen.gov.tw/cp.aspx?n=99ff9571f64e278f&s=7A1D5BD79C00DCCC |
| Lienchiang County | low/middle-low-income living assistance; emergency assistance; low-income and vulnerable child/youth medical assistance | https://law.matsu.gov.tw/LawContent.aspx?id=GL000391&kw= |

## Execution Result

- Source registry: 92 allowlisted sources.
- Public resource records: 468 records.
- Batch 3C local additions present: 9 of 9.
- Freshness check: 92 URLs checked, 0 warnings.
- Validation: `python scripts/validate_data.py` passed.
- Static build: `node scripts/build_static.mjs` passed.

## Notes

- Penghu is shown as using the Taiwan Province standard column for low-income and middle-low-income review.
- Kinmen and Lienchiang are shown as using the Fujian Province standard column for low-income and middle-low-income review.
- The "province" language is kept as a review-standard category only; users still apply through their township/city office or local government, not through a province-level office.
- One transient freshness timeout appeared for an existing Taoyuan source during the first full check; a direct GET returned `200`, and the second full check finished with 0 warnings.
- Broad county/city coverage is now complete at the planned Batch 3 level. The next useful work is deeper verification of local bureau subpages, township office pages, and civil-society program pages.
