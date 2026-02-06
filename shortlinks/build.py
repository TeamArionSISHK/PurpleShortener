#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SITE_ROOT = ROOT.parent
LINKS_PATH = ROOT / "links.yaml"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
DIST_DIR = SITE_ROOT / "dist"
LOGO_SRC = SITE_ROOT / "outbound" / "logo.png"


def die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_links() -> dict:
    try:
        data = yaml.safe_load(LINKS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing {LINKS_PATH}")
    except yaml.YAMLError as exc:
        die(f"Invalid YAML: {exc}")

    if data is None:
        return {}
    if not isinstance(data, dict):
        die("links.yaml must contain a mapping of short codes to link entries")

    links = {}
    for code, entry in data.items():
        if not isinstance(code, str) or not code.strip():
            die("Each short code must be a non-empty string")
        if not isinstance(entry, dict):
            die(f"Entry for '{code}' must be a mapping")
        url = entry.get("url")
        if not isinstance(url, str) or not url.strip():
            die(f"Entry for '{code}' must include a non-empty 'url'")
        title = entry.get("title")
        if title is not None and not isinstance(title, str):
            die(f"Entry for '{code}' has invalid 'title' (must be a string)")
        links[code.strip()] = {
            "url": url.strip(),
            "title": title.strip() if isinstance(title, str) and title.strip() else None,
        }
    return links


def render(template: str, values: dict) -> str:
    output = template
    for key, value in values.items():
        output = output.replace(f\"{{{{{key}}}}}\", value)
    return output


def build() -> None:
    router_template = TEMPLATES_DIR / \"router.html\"
    outbound_template = TEMPLATES_DIR / \"outbound.html\"
    generate_template = TEMPLATES_DIR / \"generate.html\"

    for path in (router_template, outbound_template, generate_template):
        if not path.exists():
            die(f\"Missing template {path}\")
    if not ASSETS_DIR.exists():
        die(f\"Missing assets directory {ASSETS_DIR}\")

    links = load_links()

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    json_data = json.dumps(links, ensure_ascii=False, separators=(\",\", \":\")).replace(\"</\", \"<\\\\/\")
    (DIST_DIR / \"links.json\").write_text(json_data, encoding=\"utf-8\")

    shutil.copytree(ASSETS_DIR, DIST_DIR / \"assets\")

    logo_url = \"/outbound/logo.png\"
    (DIST_DIR / \"index.html\").write_text(
        render(
            router_template.read_text(encoding=\"utf-8\"),
            {\"links_url\": \"/links.json\", \"logo_url\": logo_url},
        ),
        encoding=\"utf-8\",
    )

    outbound_dir = DIST_DIR / \"outbound\"
    outbound_dir.mkdir(parents=True, exist_ok=True)
    (outbound_dir / \"index.html\").write_text(
        render(
            outbound_template.read_text(encoding=\"utf-8\"),
            {\"logo_url\": logo_url},
        ),
        encoding=\"utf-8\",
    )

    generate_dir = outbound_dir / \"generate\"
    generate_dir.mkdir(parents=True, exist_ok=True)
    (generate_dir / \"index.html\").write_text(
        render(
            generate_template.read_text(encoding=\"utf-8\"),
            {\"logo_url\": logo_url},
        ),
        encoding=\"utf-8\",
    )

    if LOGO_SRC.exists():
        shutil.copy2(LOGO_SRC, outbound_dir / \"logo.png\")

    redirects = (
        \"/links.json /links.json 200\\n\"
        \"/shortlinks/links.json /links.json 200\\n\"
        \"/outbound/generate /outbound/generate/index.html 200\\n\"
        \"/outbound/generate/ /outbound/generate/index.html 200\\n\"
        \"/outbound/generate/* /outbound/generate/index.html 200\\n\"
        \"/outbound /outbound/index.html 200\\n\"
        \"/outbound/ /outbound/index.html 200\\n\"
        \"/outbound/* /outbound/index.html 200\\n\"
        \"/* /index.html 200\\n\"
    )
    (DIST_DIR / \"_redirects\").write_text(redirects, encoding=\"utf-8\")


if __name__ == "__main__":
    build()
