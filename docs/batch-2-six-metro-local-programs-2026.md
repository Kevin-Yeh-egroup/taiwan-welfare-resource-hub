# Batch 2 Six-Municipality Local Programs - 2026-06-05

This batch adds program-level local public resources for the six municipalities.

## Scope

- Taipei, New Taipei, Taoyuan, Taichung, Tainan, and Kaohsiung.
- Two cards per municipality.
- Only official city/district/public-agency pages were used.
- Cards were added only when the page or paired official source gave concrete eligibility, benefit amount, application notes, or current-year evidence.

## Added Sources

| Municipality | Added cards |
| --- | --- |
| Taipei | 115 low-income rent subsidy; emergency assistance |
| New Taipei | 115 low-income application; 115 low-income home repair subsidy |
| Taoyuan | 115 low-income/middle-low-income qualification standard; low-income living assistance |
| Taichung | 115 low-income/middle-low-income standard; low-income benefit table |
| Tainan | low-income household living assistance; middle-low-income elderly living allowance |
| Kaohsiung | low-income living assistance; 115 weak medical assistance |

## Execution Result

- Source registry: 59 allowlisted sources.
- Public resource records: 435 records.
- Batch 2 local additions present: 12 of 12.
- Freshness check: 59 URLs checked, 0 warnings.
- Validation: `python scripts/validate_data.py` passed.
- Static build: `node scripts/build_static.mjs` passed.

## Notes

- The Taoyuan city-government announcement URL produced a 308 redirect loop in automated freshness checks, so the same official announcement was linked through the Taoyuan Dayuan District Office page.
- Some local program amounts are current checked official values but still require district-office or bureau confirmation, especially when household composition, school status, rent contract, or medical case review affects the final amount.
