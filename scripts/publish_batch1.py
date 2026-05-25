"""
*** DEPRECATED — DO NOT USE ***

This script uses markdown.markdown() directly without bm_html_converter.py.
It produces plain HTML without BabyMania class structure (BUG-3).
Articles published via this script were fixed in-place on 2026-05-24.

USE INSTEAD: scripts/organic/publish_organic_batch.py
"""

import sys
sys.exit(
    "BLOCKED: This script is deprecated (BUG-3 — no BabyMania HTML structure).\n"
    "Use scripts/organic/publish_organic_batch.py instead."
)

# ---- archived code below (never reached) ----
import time
sys.stdout.reconfigure(encoding='utf-8')
import re
import requests
import markdown
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
BASE_DIR = Path(r"C:\Projects\baby-mania-agent\output\organic")

BATCH_1 = [
    {"file": "hub1-extension/HUB1_C5.md", "hub": "HUB-1/C5"},
    {"file": "hub1-extension/HUB1_C6.md", "hub": "HUB-1/C6"},
    {"file": "hub2-extension/HUB2_C6.md", "hub": "HUB-2/C6"},
    {"file": "hub3-extension/HUB3_C5.md", "hub": "HUB-3/C5"},
    {"file": "hub3-extension/HUB3_C6.md", "hub": "HUB-3/C6"},
    {"file": "hub4-extension/HUB4_C5.md", "hub": "HUB-4/C5"},
]


def parse_frontmatter(text):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter found")
    fm_raw, body = match.group(1), match.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm, body.strip()


def md_to_html(body_md):
    # Remove image placeholders (alt-placeholder-*)
    body_md = re.sub(r'!\[.*?\]\(alt-placeholder-[^\)]*\)\n?\*.*?\*\n?', '', body_md)
    html = markdown.markdown(body_md, extensions=['extra', 'nl2br'])
    return html


def article_exists(handle):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json?handle={handle}&limit=1"
    r = requests.get(url, headers=_headers())
    if r.status_code == 200:
        articles = r.json().get('articles', [])
        return len(articles) > 0 and articles[0].get('handle') == handle
    return False


def publish_article(title, handle, body_html, tags):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    payload = {
        "article": {
            "title": title,
            "handle": handle,
            "body_html": body_html,
            "published": True,
            "tags": tags,
        }
    }
    r = requests.post(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()["article"]


def main():
    print(f"=== BATCH 1 PUBLISH — {len(BATCH_1)} articles ===\n")
    results = []

    for i, item in enumerate(BATCH_1, 1):
        filepath = BASE_DIR / item["file"]
        hub = item["hub"]

        print(f"[{i}/{len(BATCH_1)}] {hub} — {filepath.name}")

        if not filepath.exists():
            print(f"  ❌ FILE NOT FOUND: {filepath}")
            results.append({"hub": hub, "status": "MISSING"})
            continue

        text = filepath.read_text(encoding="utf-8")
        fm, body_md = parse_frontmatter(text)

        slug = fm.get("slug", "")
        title = fm.get("title", "")
        hub_tag = fm.get("hub", "").lower().replace("-", "")
        tags = f"organic,{hub_tag},batch1"

        print(f"  slug: {slug}")
        print(f"  title: {title[:60]}")

        if article_exists(slug):
            print(f"  ⚠️  SKIP — כבר קיים ב-Shopify")
            results.append({"hub": hub, "slug": slug, "status": "ALREADY_EXISTS"})
            continue

        body_html = md_to_html(body_md)
        article = publish_article(title, slug, body_html, tags)

        live_url = f"https://babymania-il.com/blogs/news/{article['handle']}"
        print(f"  [OK] PUBLISHED - ID: {article['id']}")
        print(f"  URL: {live_url}")
        results.append({"hub": hub, "slug": slug, "id": article["id"], "url": live_url, "status": "PUBLISHED"})

        if i < len(BATCH_1):
            print("  pause 3s...")
            time.sleep(3)

        print()

    print("\n=== BATCH 1 SUMMARY ===")
    for r in results:
        icon = "[OK]" if r["status"] == "PUBLISHED" else ("[SKIP]" if r["status"] == "ALREADY_EXISTS" else "[ERR]")
        print(f"  {icon} {r['hub']} — {r.get('slug','?')} [{r['status']}]")
        if r.get("url"):
            print(f"      {r['url']}")

    published = sum(1 for r in results if r["status"] == "PUBLISHED")
    print(f"\nסה\"כ: {published}/{len(BATCH_1)} פורסמו")


if __name__ == "__main__":
    main()
