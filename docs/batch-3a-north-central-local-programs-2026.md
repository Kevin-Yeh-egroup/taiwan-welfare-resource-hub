# Batch 3A Northern/Central Local Programs - 2026-06-05

This batch adds program-level local public resources for northern and central counties/cities outside the six municipalities.

## Scope

- Keelung City, Hsinchu City, Hsinchu County, Miaoli County, Changhua County, Nantou County, and Yunlin County.
- Twelve cards total.
- Only official county/city or public-agency pages were used.
- Cards were added when the page or official document gave concrete eligibility, benefit amount, application notes, or current-year evidence.

## Added Sources

| County/city | Added cards |
| --- | --- |
| Keelung City | 115 low-income/middle-low-income application; disability living assistance |
| Hsinchu City | 115 low-income/middle-low-income application; weak medical assistance |
| Hsinchu County | low-income household computer equipment subsidy; employment incentive |
| Miaoli County | 115 maternal/newborn nutrition subsidy; hospital care subsidy |
| Changhua County | 115 low-income living assistance; 115 long-term-care transportation |
| Nantou County | 115 low-income living assistance |
| Yunlin County | 115 low-income/middle-low-income application |

## Execution Result

- Source registry: 71 allowlisted sources.
- Public resource records: 447 records.
- Batch 3A local additions present: 12 of 12.
- Freshness check: 71 URLs checked, 0 warnings.
- Validation: `python scripts/validate_data.py` passed.
- Static build: `node scripts/build_static.mjs` passed.

## Notes

- This batch favors cards with current-year dates, official PDFs, or county/city application guidance over broad bureau homepages.
- Some local amounts still depend on household category, disability level, actual care days, transportation distance, or case review. Cards keep the official source link and tell residents to confirm with the local office before applying.
- Remaining local batches should continue with southern/eastern counties, offshore counties, and deeper civil-society program review.
