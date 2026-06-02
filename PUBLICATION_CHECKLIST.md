# Publication Checklist

## Sensitivity

- [ ] Public viewing is acceptable.
- [ ] No private source documents are included.
- [ ] No personal data, internal notes, cookies, tokens, or `.vercel` files are included.
- [ ] Review-stage noindex remains enabled unless Kevin separately approves indexing.

## GitHub

- [ ] Dedicated repo slug confirmed.
- [ ] Repo visibility confirmed.
- [ ] `main` branch contains production-ready static site.
- [ ] `.gitignore` excludes source documents, secrets, and Vercel local metadata.

## Vercel

- [ ] Dedicated Vercel project confirmed.
- [ ] Production branch is `main`.
- [ ] Deployment status is `READY`.
- [ ] Stable alias is dedicated to this project.

## Verification

- [ ] `python scripts/validate_data.py` passes.
- [ ] Browser preview checked on desktop and mobile widths.
- [ ] `curl -I -L <url>` returns `200 OK`.
- [ ] `X-Robots-Tag: noindex, nofollow, noarchive` is present.
- [ ] HTML meta robots is present.
- [ ] `robots.txt` returns `Disallow: /`.
