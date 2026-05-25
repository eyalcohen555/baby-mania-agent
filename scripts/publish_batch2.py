"""
*** DEPRECATED — DO NOT USE ***

This script used markdown.markdown() directly without bm_html_converter.py.
It produced damaged HTML: JSON-LD as visible text, [IMG_ALT_N:] markers visible,
no BabyMania class structure (BUG-1 + BUG-2 + BUG-3).
Articles published via this script were fixed in-place on 2026-05-24.

USE INSTEAD: scripts/organic/publish_organic_batch.py
"""

import sys
sys.exit(
    "BLOCKED: This script is deprecated (BUG-1/2/3 pipeline bugs).\n"
    "Use scripts/organic/publish_organic_batch.py instead."
)

# ---- archived code below (never reached) ----
"""
Original docstring:
Publish Batch 2 — 6 organic articles to Shopify blog.
Schedule: Sunday 24.05.2026
Articles: HUB-7 C6, HUB-8 C6, HUB-16 Pillar, C1, C2, C3
"""

import sys
import time
import argparse
sys.stdout.reconfigure(encoding="utf-8")
import re
import requests
import markdown
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
BASE_DIR = Path(r"C:\Projects\baby-mania-agent\output\organic")

BATCH_2 = [
    {"file": "hub7-extension/HUB7_C6.md",    "hub": "HUB-7/C6"},
    {"file": "hub8-extension/HUB8_C6.md",    "hub": "HUB-8/C6"},
    {"file": "hub16-crocs/HUB16_Pillar.md",  "hub": "HUB-16/Pillar"},
    {"file": "hub16-crocs/HUB16_C1.md",      "hub": "HUB-16/C1"},
    {"file": "hub16-crocs/HUB16_C2.md",      "hub": "HUB-16/C2"},
    {"file": "hub16-crocs/HUB16_C3.md",      "hub": "HUB-16/C3"},
]


def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter found")
    fm_raw, body = match.group(1), match.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            fm[k.strip()] = v.strip()
    return fm, body.strip()


def md_to_html(body_md):
    # Strip alt-placeholder-* image markers (not yet replaced with CDN URLs)
    body_md = re.sub(
        r"!\[.*?\]\(alt-placeholder-[^\)]*\)\n?\*.*?\*\n?", "", body_md
    )
    # Strip local images/ paths (relative — not valid on Shopify CDN)
    # These are approved images awaiting CDN upload in a future step
    body_md = re.sub(
        r"!\[([^\]]*)\]\(images/[^\)]+\)\n?(\*alt:.*?\*)?\n?", "", body_md
    )
    html = markdown.markdown(body_md, extensions=["extra", "nl2br"])
    return html


def article_exists(handle):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json?handle={handle}&limit=1"
    r = requests.get(url, headers=_headers())
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        return len(articles) > 0 and articles[0].get("handle") == handle
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Actually publish to Shopify")
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()
    live = args.live

    mode = "LIVE" if live else "DRY-RUN"
    print(f"=== BATCH 2 PUBLISH [{mode}] — {len(BATCH_2)} articles ===\n")
    if not live:
        print("  [DRY-RUN] No Shopify writes. Add --live to publish.\n")

    results = []

    for i, item in enumerate(BATCH_2, 1):
        filepath = BASE_DIR / item["file"]
        hub = item["hub"]

        print(f"[{i}/{len(BATCH_2)}] {hub} — {filepath.name}")

        if not filepath.exists():
            print(f"  MISSING FILE: {filepath}")
            results.append({"hub": hub, "status": "MISSING"})
            continue

        text = filepath.read_text(encoding="utf-8")
        fm, body_md = parse_frontmatter(text)

        slug  = fm.get("slug", "")
        title = fm.get("title", "")
        hub_tag = fm.get("hub", "").lower().replace("-", "")
        tags = f"organic,{hub_tag},batch2"

        # Count what gets stripped
        placeholders_stripped = len(re.findall(r"alt-placeholder-\w+", body_md))
        local_imgs_stripped   = len(re.findall(r"!\[[^\]]*\]\(images/[^\)]+\)", body_md))

        print(f"  slug:  {slug}")
        print(f"  title: {title[:65]}")
        print(f"  tags:  {tags}")
        if placeholders_stripped:
            print(f"  [strip] {placeholders_stripped} alt-placeholder(s) removed")
        if local_imgs_stripped:
            print(f"  [strip] {local_imgs_stripped} local image(s) removed (awaiting CDN upload)")

        body_html = md_to_html(body_md)
        print(f"  html:  {len(body_html):,} chars")

        if not live:
            results.append({"hub": hub, "slug": slug, "status": "DRY-RUN-OK"})
            print()
            continue

        if article_exists(slug):
            print(f"  SKIP — already exists on Shopify")
            results.append({"hub": hub, "slug": slug, "status": "ALREADY_EXISTS"})
            print()
            continue

        article = publish_article(title, slug, body_html, tags)
        live_url = f"https://babymania-il.com/blogs/news/{article['handle']}"
        print(f"  PUBLISHED — ID: {article['id']}")
        print(f"  URL: {live_url}")
        results.append({
            "hub": hub, "slug": slug,
            "id": article["id"], "url": live_url,
            "status": "PUBLISHED"
        })

        if i < len(BATCH_2):
            print("  pause 3s...")
            time.sleep(3)

        print()

    print(f"\n=== BATCH 2 SUMMARY [{mode}] ===")
    for r in results:
        s = r["status"]
        icon = "OK" if s in ("PUBLISHED", "DRY-RUN-OK") else ("SKIP" if s == "ALREADY_EXISTS" else "ERR")
        print(f"  [{icon}] {r['hub']} — {r.get('slug','?')} [{s}]")
        if r.get("url"):
            print(f"       {r['url']}")

    if live:
        published = sum(1 for r in results if r["status"] == "PUBLISHED")
        print(f"\nTotal: {published}/{len(BATCH_2)} published")
        print("\nNEXT STEP: submit GSC indexing for each published URL")
    else:
        ok = sum(1 for r in results if r["status"] == "DRY-RUN-OK")
        print(f"\nDry-run: {ok}/{len(BATCH_2)} ready")
        print("Run with --live after Ayal approval.")


if __name__ == "__main__":
    main()
