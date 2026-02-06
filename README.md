# PurpleShortener
Team Arion's URL shortening web infrastructure.

## Overview
This repo builds a static short link site for Cloudflare Pages. Redirects are defined in `shortlinks/links.yaml` and compiled into static HTML files in `shortlinks/dist` by `shortlinks/build.py`.

It also contains a standalone outbound warning page in `outbound/` that is not part of the shortlink build.

## Project Layout
- `shortlinks/links.yaml` Redirect definitions.
- `shortlinks/build.py` Build script.
- `shortlinks/templates/redirect.html` HTML template for redirects.
- `shortlinks/dist/` Build output (generated).
- `.github/workflows/deploy.yml` GitHub Actions deploy workflow.
- `outbound/index.html` External redirect warning page (standalone).

## Requirements
- Python 3.11+

## Quick Start
1. Install dependencies:
```bash
pip install -r shortlinks/requirements.txt
```

2. Build the site:
```bash
python shortlinks/build.py
```

3. Open a generated page (example):
```bash
ls shortlinks/dist
```

## Managing Links
`shortlinks/links.yaml` is a mapping of short codes to URLs:

```yaml
home:
  url: https://teamarion.org
  title: Team Arion

pit:
  url: https://teamarion.org/pit-display
```

Rules:
- Each key is the short code (e.g. `home` becomes `/<code>/index.html`).
- `url` is required.
- `title` is optional; if omitted, the page title defaults to `Redirecting`.

After editing `links.yaml`, rerun the build.

## Build Output
Each link produces:
```
shortlinks/dist/<code>/index.html
```

Example:
- `home` becomes `shortlinks/dist/home/index.html` and will serve at `https://go.teamarion.org/home` on Cloudflare Pages.

## Deployment (Cloudflare Pages)
Deployment is handled by GitHub Actions on every push to `main`.

Workflow highlights:
- Installs Python dependencies
- Runs `shortlinks/build.py`
- Deploys `shortlinks/dist` to Cloudflare Pages

Required GitHub secrets:
- `CF_API_TOKEN`
- `CF_ACCOUNT_ID`

Set the Cloudflare Pages project name in `.github/workflows/deploy.yml` (`projectName`).

## Outbound Warning (Standalone)
The outbound warning page is a static, standalone artifact in `outbound/` and does not require GitHub Actions.

Usage:
- `https://go.teamarion.org/outbound/<encoded-url>`
- Example: `https://go.teamarion.org/outbound/https%3A%2F%2Fexample.com`

Notes:
- Add `logo.png` to `outbound/` to display the Team Arion logo.
- The page only allows `http` and `https` destinations.
- `?to=` query parameter is also supported as a fallback.

## Local Validation
To verify output after a build, check that each generated page contains:
- A meta refresh redirect
- A canonical link
- A fallback link in the body
- A title

## Troubleshooting
- If YAML is invalid, `build.py` exits with a clear error message.
- If no links are defined, the build completes with an empty `shortlinks/dist`.
