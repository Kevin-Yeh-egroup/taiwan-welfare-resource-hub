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

## GitHub Actions

- Workflow: `Freshness Check`
- Path: `.github/workflows/freshness-check.yml`
- GitHub workflow state: `active`
- Repository Actions permission: `enabled=True`, `allowed_actions=all`

## Remaining Notes

- The SFAA official page and several public sources require the allowlisted SSL fallback during checks because their certificate chain triggers Python's strict certificate validation; the freshness report has 0 failed-source warnings.
- Kevin-provided source documents were not available at the original Downloads paths during setup; place them in `source-docs/` and rerun extraction when available.
- Noindex is intentionally retained. It is not access control; the site is public and link-accessible.
