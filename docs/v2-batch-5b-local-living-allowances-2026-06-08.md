# V2 Batch 5B Local Living Allowances - 2026-06-08

## Scope

Batch 5B continues the local deep-dive after V2 Batch 5A. The goal is to add citizen-facing cards for current local monthly allowances that people commonly ask about first:

- disability living allowances;
- middle-low-income elderly living allowances;
- application conditions, benefit amounts, and application notes in the same order used by the public UI.

## Added Cards

| Jurisdiction | Resource | Source |
| --- | --- | --- |
| 臺中市 | 臺中市身心障礙者生活補助費 | 臺中市政府社會局 |
| 臺中市 | 臺中市中低收入老人生活津貼 | 臺中市政府社會局 |
| 高雄市 | 高雄市中低收入老人生活津貼 | 高雄市政府社會局長青綜合服務中心 |
| 高雄市 | 高雄市身心障礙者生活補助 | 高雄市政府社會局與高雄市官方區公所頁 |
| 基隆市 | 基隆市中低收入老人生活津貼 | 基隆市政府社會處 |
| 宜蘭縣 | 宜蘭縣中低收入老人生活津貼 | 宜蘭縣宜蘭市公所社會課頁 |
| 宜蘭縣 | 宜蘭縣身心障礙者生活補助 | 宜蘭縣宜蘭市公所社會課頁 |

## Review Notes

- 臺中市兩張卡採用市府社會局頁面作主來源，並以頁面列出的最後異動日期及網站更新日期標示 freshness。
- 高雄市中低收入老人生活津貼採用高雄市長青綜合服務中心頁面，該頁列出115年度申請條件、文件、服務窗口與金額。
- 高雄市身心障礙者生活補助以115年度更新的高雄市官方區公所頁面作資格來源，金額以高雄市官方區公所補助說明交叉確認。
- 宜蘭縣兩張卡目前採用宜蘭市公所社會課頁面，因其列有公所端送件與轉縣府核定流程；卡片文字提醒實際窗口仍以戶籍地公所確認。

## Verification

- Source registry: 104 allowlisted sources.
- Data build: 529 resource records.
- Freshness check: 104 URLs checked, 0 warnings.
- Duplicate check: 0 duplicate same-name/provider/jurisdiction records.
- Batch target check: all 7 Batch 5B cards present.
- Public UI count logic: 21 central public resources, 82 local public resources, and 426 private resources.
- Static build: completed.

GitHub push and Vercel Production verification are recorded separately in the production log after deployment.
