#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
LINKS_PATH = ROOT / "links.yaml"
TEMPLATE_PATH = ROOT / "templates" / "index.html"
DIST_DIR = ROOT / "dist"


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


def build() -> None:
    if not TEMPLATE_PATH.exists():
        die(f"Missing template {TEMPLATE_PATH}")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    links = load_links()

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    json_data = json.dumps(links, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (DIST_DIR / "links.json").write_text(json_data, encoding="utf-8")

    index_html = template.replace("{{links_json}}", json_data)
    (DIST_DIR / "index.html").write_text(index_html, encoding="utf-8")

    redirects = "/links.json /links.json 200\\n/* /index.html 200\\n"
    (DIST_DIR / "_redirects").write_text(redirects, encoding="utf-8")


if __name__ == "__main__":
    build()
