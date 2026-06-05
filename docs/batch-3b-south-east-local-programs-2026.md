# Batch 3B Southern/Eastern Local Programs - 2026-06-05

This batch adds program-level local public resources for southern and eastern counties/cities outside the six municipalities.

## Scope

- Chiayi City, Chiayi County, Pingtung County, Yilan County, Hualien County, and Taitung County.
- Twelve cards total.
- Only official county/city or public-agency pages were used.
- Cards were added when the page gave concrete eligibility, benefit amount, application notes, or current-year evidence.

## Added Sources

| County/city | Added cards | Official source examples |
| --- | --- | --- |
| Chiayi City | 115 low-income living assistance; low/middle-low-income medical assistance | https://social.chiayi.gov.tw/News_Content.aspx?n=397&s=843107 |
| Chiayi County | 115 low-income assistance; emergency assistance | https://sabcc.cyhg.gov.tw/cp.aspx?n=4930 |
| Pingtung County | 115 low-income living assistance; low/middle-low-income employment transportation subsidy | https://www.pthg.gov.tw/planjdp/cp.aspx?n=A4164DF4295ED9D4 |
| Yilan County | low-income and middle-low-income qualification guidance; long-term-care transportation | https://sntroot.e-land.gov.tw/cp.aspx?n=10407&s=1855 |
| Hualien County | low-income and middle-low-income subsidy standards; emergency assistance | https://sa.hl.gov.tw/Detail_sp/e600e5783a3d43859f310d41a8d2a089 |
| Taitung County | 115 learning equipment subsidy; medical assistance | https://taisoc.taitung.gov.tw/WebSite/Service/serviceDetail.aspx?menuid=lW%2bfKiAxClc%3d&page=1&id=pKJCfMLiUNA%3d |

## Execution Result

- Source registry: 83 allowlisted sources.
- Public resource records: 459 records.
- Batch 3B local additions present: 12 of 12.
- Freshness check: 83 URLs checked, 0 warnings.
- Validation: `python scripts/validate_data.py` passed.
- Static build: `node scripts/build_static.mjs` passed.

## Notes

- The Yilan low-income card uses the current Yilan City Office page because the county social-affairs page observed during research still showed older threshold text despite a newer footer date.
- The Taichung 115 annual-standard card was also corrected during this batch: the official article path was changed to `https://www.society.taichung.gov.tw/3101150/post`, and the card now lists income, movable-property, and real-estate thresholds together.
- Remaining local batch: offshore counties Penghu, Kinmen, and Lienchiang. After that, the next useful expansion is deeper civil-society program confirmation, not more broad portal cards.
