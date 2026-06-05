# Production Log - 2026-06-03

## GitHub

- Repository: `Kevin-Yeh-egroup/taiwan-welfare-resource-hub`
- Visibility: public
- URL: `https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub`
- Production branch: `main`
- Note: Vercel is connected to GitHub and creates a new Production deployment for each pushed `main` commit. The stable URL should be treated as the current pointer.

## Vercel

- Account/team: `egroup-task3s-projects`
- Project: `taiwan-welfare-resource-hub`
- Project ID: `prj_pgs9AuZOuFeqwVLaB0yazcnNR5x3`
- Org/team ID: `team_lOk9yHNRxLRBcdrU9DATWODG`
- Verified production deployments:
  - `dpl_9gpH1CJXJ2Ey1wB81bqjNRvAyv8v` from `c6eae5ca2c5a5abba3aeaa0f42146e2fe5572335`
  - `dpl_CtgEMFYBkq5XZRWdMhzzXeFnF3jU` from `c68f36448e15ca46b31f60224ed15c4f637c0528`
  - `dpl_8wf9Q6UqPZ2fdQrFJQDzjDNB2mhb` from `0dd738b9d3d7767a71c38da47df8f02b12b64f3b`
  - `dpl_BAmatL7kDMJjqwTfwmU9Pjd8bkLQ` from `12332e4b3d4c61832f0f3f9364d216e14a359258`
  - `dpl_Hj9Fykc3wKe3PiH5k59zLpb269hX` from `edbda91`
  - `dpl_bQi7vYNQRR8R8udDLpXDmW77t7WR` from `d172a09b4ae0866ab5b5bfe4488da378816f24b6`
  - `dpl_8owvjFeyazSqtKky4iGcmuzyo33d` from `0ed5c3426c561ec2bbbcde929ea8ab3ea7a429bd`
- Stable URL: `https://taiwan-welfare-resource-hub.vercel.app/`
- Deployment source: GitHub `main`
- Vercel source metadata: `source=git`, repo visibility `public`, branch alias `taiwan-welfare-resource-hub-git-main-egroup-task3s-projects.vercel.app`

## Noindex Verification

- `curl -I -L https://taiwan-welfare-resource-hub.vercel.app/` returned `200 OK`.
- Response header includes `X-Robots-Tag: noindex, nofollow, noarchive`.
- HTML includes `<meta name="robots" content="noindex,nofollow,noarchive">`.
- `robots.txt` returns:

```text
User-agent: *
Disallow: /
```

## Application Verification

- `data/resources.json` returned 411 records with status `generated`.
- SFAA official foundation records: 355.
- SFAA records with 2026 source update dates: 163.
- Search-data checks: `民間基金會` matches 355 records; `芥菜種會` matches `財團法人基督教芥菜種會`.
- Local and production HTTP/data checks confirmed the live page loads the updated UI and resource JSON.
- Local validation command passed: `python scripts/validate_data.py`.

## Batch 3A Production Verification - 2026-06-05

- Commit: `12332e4b3d4c61832f0f3f9364d216e14a359258`
- Deployment: `dpl_BAmatL7kDMJjqwTfwmU9Pjd8bkLQ`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`, `robots.txt` `200`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present; `robots.txt` includes `Disallow: /`
- Data verification: 447 records, 71 sources, 71 freshness URLs checked, 0 freshness warnings
- Batch 3A verification: 12 of 12 added northern/central local cards present
- Production browser verification: county filter `苗栗縣` showed 3 cards and included both `苗栗縣低收入戶與中低收入戶產婦及新生兒營養補助` and `苗栗縣低收入戶及中低收入戶傷病住院看護費用補助`; cards showed `申請條件先看`, `補助項目與金額`, and `申請注意事項`
- Runtime logs: `vercel logs --since 1h --level error` returned no logs
- Screenshot note: local screenshot saved to `work/batch-3a-local-miaoli-results.png`; Production screenshot capture timed out in the browser tool, but DOM and HTTP verification succeeded

## Batch 3B Production Verification - 2026-06-05

- Commit: `edbda91`
- Deployment: `dpl_Hj9Fykc3wKe3PiH5k59zLpb269hX`
- Deployment URL: `https://taiwan-welfare-resource-fzg7rztmg-egroup-task3s-projects.vercel.app`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`, `data/sources.json` `200`, `data/freshness-report.json` `200`, `robots.txt` `200`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present; `robots.txt` includes `Disallow: /`
- Data verification: 459 records, 83 sources, 83 freshness URLs checked, 0 freshness warnings
- Batch 3B verification: 12 of 12 added southern/eastern local cards present
- Production browser verification: county filter `臺東縣` showed 5 cards and included both `臺東縣115年度脫貧支持服務計畫購置學習設備補助` and `臺東縣中低收傷病醫療費用補助`; cards showed `申請條件`, `補助項目與金額`, and `申請注意事項`
- Runtime logs: `vercel logs --since 1h --level error` returned no logs

## Batch 3C Production Verification - 2026-06-05

- Commit: `a9282bd`
- Deployment: `dpl_GZm1m2oC2HXMnUyzpa1FcAPHfKKJ`
- Deployment URL: `https://taiwan-welfare-resource-f68gxru7c-egroup-task3s-projects.vercel.app`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`, `data/sources.json` `200`, `data/freshness-report.json` `200`, `robots.txt` `200`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present; `robots.txt` includes `Disallow: /`
- Data verification: 468 records, 92 sources, 92 freshness URLs checked, 0 freshness warnings
- Batch 3C verification: 9 of 9 added offshore local cards present
- Production browser verification: county filter `連江縣` showed all three added program cards: `連江縣低收入戶及中低收入戶生活扶助`, `連江縣政府民眾急難救助`, and `連江縣低收入戶及弱勢兒少醫療補助`; cards showed `申請條件`, `補助項目與金額`, and `申請注意事項`
- Runtime logs: `vercel logs --since 1h --level error` returned no logs

## Batch 4A Production Verification - 2026-06-05

- Commit: `d172a09b4ae0866ab5b5bfe4488da378816f24b6`
- Deployment: `dpl_bQi7vYNQRR8R8udDLpXDmW77t7WR`
- Deployment URL: `https://taiwan-welfare-resource-dnoh1190f-egroup-task3s-projects.vercel.app`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`, `robots.txt` `200`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present; `robots.txt` includes `Disallow: /`
- Data verification: 476 records, 92 sources, 92 freshness URLs checked, 0 freshness warnings
- Batch 4A verification: 8 of 8 reviewed foundation program cards present; reviewed foundation program total is 30
- Added civil-society program pages: `墨仙急難救助金`, `墨仙小樹苗成長方案`, `勵馨親密關係暴力／家庭暴力被害人服務`, `勵馨性暴力防治服務`, `勵馨兒童與青少年服務`, `瑪喜樂身心障礙者就業服務`, `脊髓損傷家庭經濟協助`, and `弘道老人福利基金會長者服務`
- Production browser verification: `民間資源` group showed `476` records and `30` foundation programs; `墨仙急難救助金` expanded in-page with `申請條件先看`, `補助項目與金額`, `申請注意事項`, `依個案核定`, and `開啟來源頁`; old related-program text `查看方案` was absent
- Runtime logs: `vercel logs --since 1h --level error` returned no logs

## Batch 4B Production Verification - 2026-06-05

- Commit: `77acb970f8b0046ee5881e478430af37239f4f37`
- Deployment: `dpl_HWRJsH1rT1vTs1DqLDKQBFw5hCTG`
- Deployment URL: `https://taiwan-welfare-resource-3krvx5yv1-egroup-task3s-projects.vercel.app`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`; `index.html` references `app.js?v=20260605-batch4b`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present
- Data verification: 483 records, 92 sources, 92 freshness URLs checked, 0 freshness warnings
- Batch 4B verification: 7 of 7 reviewed foundation program cards present; reviewed foundation program total is 37
- Added civil-society program pages: `桃園市身心障礙者恆愛日間托育服務中心`, `桃園市身心障礙者服務中心`, `啟智技藝訓練中心楊梅服務區`, `聖島助學專案`, `聖島雪炭專案`, `兆豐慈善急難救助與醫療補助`, and `興毅基金會社會救助服務`
- Production browser verification: homepage status grid shows `公部門中央資源 21`, `公部門地方資源 70`, and `民間資源 392`; cards still show `申請條件`, `補助項目與金額`, and `申請注意事項`
- Runtime log check: not run because the Vercel CLI was not available in PATH; Vercel deployment state, HTTP checks, data checks, and browser verification all passed

## Batch 4C Production Verification - 2026-06-05

- Commit: `0ed5c3426c561ec2bbbcde929ea8ab3ea7a429bd`
- Deployment: `dpl_8owvjFeyazSqtKky4iGcmuzyo33d`
- Deployment URL: `https://taiwan-welfare-resource-a3xrz99zq-egroup-task3s-projects.vercel.app`
- Target/status: Production / Ready
- Stable URL verified: `https://taiwan-welfare-resource-hub.vercel.app/`
- HTTP verification: page `200`, `data/resources.json` `200`, `robots.txt` `200`; `index.html` references `app.js?v=20260605-batch4c`
- Noindex verification: `X-Robots-Tag: noindex, nofollow, noarchive`; HTML meta robots present; `robots.txt` includes `Disallow: /`
- Data verification: 493 records, 92 sources, 92 freshness URLs checked, 0 freshness warnings
- Batch 4C verification: 10 of 10 reviewed foundation program cards present; reviewed foundation program total is 47
- Added civil-society program pages: `漢慈兒少生活陪讀服務`, `基督徒救世會婦幼家庭關懷服務`, `信義公益基金會急難救助`, `善牧家庭暴力保護服務`, `善牧兒童保護與支持服務`, `台灣關愛基金會文山婦幼服務中心`, `華科聽覺照顧獎補助學金`, `全聯物資銀行身心障礙及婦女服務類`, `業成員工愛心基金補助計畫`, and `永信社會福利基金會長照與社區照顧服務`
- Production browser verification: homepage status grid shows `公部門中央資源 21`, `公部門地方資源 70`, and `民間資源 402`; filtering `臺北市` + `社工或轉介單位` + `急難救助(短期、臨時性補助)` found 3 cards including `信義公益基金會急難救助`, with `申請條件`, `補助項目與金額`, and `申請注意事項`
- Runtime log check: not run because the Vercel CLI was not available in PATH; Vercel deployment state, HTTP checks, data checks, and browser verification all passed

## GitHub Actions

- Workflow: `Freshness Check`
- Path: `.github/workflows/freshness-check.yml`
- GitHub workflow state: `active`
- Repository Actions permission: `enabled=True`, `allowed_actions=all`

## Remaining Notes

- The SFAA official page and several public sources require the allowlisted SSL fallback during checks because their certificate chain triggers Python's strict certificate validation; the freshness report has 0 failed-source warnings.
- Kevin-provided source documents were not available at the original Downloads paths during setup; place them in `source-docs/` and rerun extraction when available.
- Noindex is intentionally retained. It is not access control; the site is public and link-accessible.
