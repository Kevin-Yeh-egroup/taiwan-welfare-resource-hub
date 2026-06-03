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
  - `dpl_CtgEMFYBkq5XZRWdMhzzXeFnF3jU` from `c68f36448e15ca46b31f60224ed15c4f637c0528`
  - `dpl_8wf9Q6UqPZ2fdQrFJQDzjDNB2mhb` from `0dd738b9d3d7767a71c38da47df8f02b12b64f3b`
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

- `data/resources.json` returned 24 records with status `generated`.
- Browser screenshot `work/production-desktop-loaded.png` confirmed the live page loads the search UI and resource cards.
- Local validation command passed: `python scripts/validate_data.py`.

## GitHub Actions

- Workflow: `Freshness Check`
- Path: `.github/workflows/freshness-check.yml`
- GitHub workflow state: `active`
- Repository Actions permission: `enabled=True`, `allowed_actions=all`

## Remaining Notes

- The Taipei map source still needs certificate/freshness review from the crawler side.
- Kevin-provided source documents were not available at the original Downloads paths during setup; place them in `source-docs/` and rerun extraction when available.
- Noindex is intentionally retained. It is not access control; the site is public and link-accessible.
