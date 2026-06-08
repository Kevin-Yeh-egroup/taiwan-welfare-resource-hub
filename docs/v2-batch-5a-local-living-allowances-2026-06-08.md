# V2 Batch 5A Local Living Allowances - 2026-06-08

V2 starts after the first SFAA foundation pass reached exhaustion at Batch I. The V2 expansion goal is no longer broad coverage. It is to add program-level cards that help a resident quickly answer: "Can I apply?", "How much is it?", and "Where do I go next?"

## Scope

Batch 5A focuses on local public-sector living allowances that ordinary residents commonly ask about:

- disability living allowances;
- middle-low-income elderly living allowances;
- pages with official eligibility, benefit amount, documents, or application path;
- pages that add more value than a broad social-bureau homepage.

## Added Cards

| County/city | Resource | Source |
| --- | --- | --- |
| 臺北市 | 臺北市身心障礙者生活補助 | https://dosw.gov.taipei/cp.aspx?n=C764A5808F9A3B08 |
| 新北市 | 新北市身心障礙者生活補助 | https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110049 |
| 臺北市 | 臺北市中低收入老人生活津貼 | https://dosw.gov.taipei/cp.aspx?n=FCF3DAE98DDA289F |
| 新北市 | 新北市中低收入老人生活津貼 | https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110027 |
| 桃園市 | 桃園市中低收入老人生活津貼 | https://e-services.tycg.gov.tw/TycgOnline/tycgOnline.action?Aid=AP03030000000078&func=description |

## Updated Existing Card

| County/city | Resource | Source |
| --- | --- | --- |
| 臺南市 | 臺南市中低收入老人生活津貼 | https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297 |

## Review Notes

- 臺北市 and 新北市 disability allowance pages include 115年度 income or property standards and monthly payment amounts by disability severity and household status.
- 臺北市, 新北市, 桃園市, and 臺南市 elderly allowance pages include monthly benefit amounts, income thresholds, application location, or documents. Tainan was already present from the earlier local batch, so V2 enriched the existing card instead of creating a duplicate.
- 桃園市 uses the stable e-services URL as the primary freshness URL because the official FAQ page currently triggers a Python 308 redirect loop during automated checks. The 115年度 condition source remains referenced inside the card.
- Pages that only list a unit homepage, old static table, activity recap, or unclear current intake were not used for this V2 batch.

## Verification

- `python scripts/build_source_registry.py` wrote 97 sources after de-duplicating the existing Tainan elderly allowance card.
- `python scripts/crawl_sources.py --sources data/sources.json --out data/resources.json` wrote 452 base records with 0 errors.
- `python scripts/convert_candidate_programs.py ...` converted 71 reviewed foundation program pages; total records are 522.
- `python scripts/check_freshness.py --sources data/sources.json --out data/freshness-report.json --sleep 0.1 --timeout 5 --retries 0 --retry-sleep 0` checked 97 URLs with 0 warnings after one transient retry.
- `python scripts/validate_data.py` passed with 522 records and 97 sources.
- `node scripts/build_static.mjs` passed.

## Next V2 Batch Candidates

- Batch 5B: continue local elderly/disability cash-support pages for Taichung, Kaohsiung, and non-municipality counties when official pages expose current amounts and documents.
- Batch 5C: local special-circumstances family assistance and child/youth economic support.
- Batch 6A: non-SFAA civil-society resources such as hospital foundations, religious charities, and regional charity associations.
- Batch 7A: candidate-only re-review with phone or newer-source confirmation for pages that look useful but lacked current intake proof.
