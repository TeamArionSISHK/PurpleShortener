# PurpleShortener
Team Arion's URL shortening web infrastructure.

> [!TIP]
> ***How to use?***
> 
> **Short links:** Edit `shortlinks/links.yaml`, push to `main`, and wait a few minutes for Cloudflare to rebuild.  
> **Outbound links:** Use `https://go.teamarion.org/outbound/generate` to generate a site-leaving warning page.
> 
> Changes usually appear after the next deploy finishes.

> [!NOTE]
> This service is for Team Arion members only.

## Overview
This repo builds a static short link router plus outbound warning pages for Cloudflare Pages. Redirects are defined in `shortlinks/links.yaml` and compiled into `dist/` by `shortlinks/build.py`.

## Project Layout
- `shortlinks/links.yaml` Redirect definitions.
- `shortlinks/build.py` Build script.
- `shortlinks/templates/router.html` Router page template.
- `shortlinks/templates/outbound.html` Outbound warning template.
- `shortlinks/templates/generate.html` Generator template.
- `shortlinks/assets/site.css` Shared theme styles.
- `shortlinks/assets/router.js` Router logic.
- `shortlinks/assets/outbound.js` Outbound warning logic.
- `shortlinks/assets/generate.js` Generator logic.
- `outbound/logo.png` Logo source for outbound pages.
- `dist/` Build output (generated).
- `.github/workflows/deploy.yml` GitHub Actions workflow.

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

3. Inspect output:
```bash
ls dist
```

## Managing Links
`shortlinks/links.yaml` is a mapping of short codes to URLs:

```yaml
home:
  url: https://teamarion.org
  title: Team Arion

instagram:
  url: https://www.instagram.com/teamarionhk/
```

Rules:
- Each key is the short code (e.g. `home` becomes `/home`).
- `url` is required.
- `title` is optional; if omitted, the page title defaults to `Redirecting`.

After editing `links.yaml`, rerun the build.

## Build Output
The build produces:
- `dist/index.html` Router page that reads the URL path.
- `dist/links.json` Lookup table generated from `links.yaml`.
- `dist/assets/` Shared CSS/JS assets.
- `dist/outbound/index.html` Outbound warning page.
- `dist/outbound/generate/index.html` Outbound link generator.
- `dist/outbound/logo.png` (if `outbound/logo.png` exists).
- `dist/_redirects` Rewrite rules for Cloudflare Pages.

Example:
- `home` becomes `https://go.teamarion.org/home` via the router page.

## Deployment (Cloudflare Pages)
Cloudflare builds and serves `dist/`. GitHub Actions can still run the build for CI validation, but it does not deploy.

Workflow highlights:
- Installs Python dependencies
- Runs `shortlinks/build.py`

Cloudflare Pages settings:
- Framework preset: `None`
- Build command: `pip install -r shortlinks/requirements.txt && python shortlinks/build.py`
- Build output directory: `dist`
- Root directory (advanced): leave blank

## Outbound Warning
Usage:
- `https://go.teamarion.org/outbound/<encoded-url>`
- Example: `https://go.teamarion.org/outbound/https%3A%2F%2Fexample.com`

Notes:
- The page only allows `http` and `https` destinations.
- `?to=` query parameter is also supported as a fallback.

Generator:
- `https://go.teamarion.org/outbound/generate`

## Local Validation
To verify output after a build, confirm these files exist in `dist/`:
- `index.html`
- `links.json`
- `_redirects`
- `assets/site.css`

## Troubleshooting
- If YAML is invalid, `build.py` exits with a clear error message.
- If no links are defined, the build completes with an empty lookup table.
