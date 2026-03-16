#!/usr/bin/env python3
"""
Fix HUB-4 articles:
  1. Delete old article 676685971769 (sleeping bag draft)
  2. Fetch valid product images from CDN 0864/9677/2409
  3. For each of 5 HUB-4 articles:
       - Replace 15 broken CDN URLs (0891/5765/7897) with real store images
       - Set a featured image per article
"""

import sys
import json
import re
import requests

# Force UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, "C:/Projects/baby-mania-agent")
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
ARTICLE_TO_DELETE = 676685971769
BROKEN_CDN_FRAGMENT = "0891/5765/7897"
CORRECT_CDN_FRAGMENT = "0864/9677/2409"

HUB4_ARTICLES = [
    {
        "id": 681481797945,
        "role": "Pillar",
        "file": "C:/Users/3024e/Downloads/\u05e7\u05dc\u05d5\u05d3 \u05e7\u05d5\u05d3/teams/organic/hub4-sensitive-baby-skin/HUB4_Pillar_blog_article.html",
        "featured_alt": "\u05d8\u05d9\u05e4\u05d5\u05dc \u05d1\u05e2\u05d5\u05e8 \u05e8\u05d2\u05d9\u05e9 \u05e9\u05dc \u05ea\u05d9\u05e0\u05d5\u05e7 \u2014 \u05d1\u05d9\u05d2\u05d5\u05d3 \u05db\u05d5\u05ea\u05e0\u05d4 \u05e8\u05da \u05d5\u05e2\u05d3\u05d9\u05df",
    },
    {
        "id": 681481830713,
        "role": "C1",
        "file": "C:/Users/3024e/Downloads/\u05e7\u05dc\u05d5\u05d3 \u05e7\u05d5\u05d3/teams/organic/hub4-sensitive-baby-skin/HUB4_C1_blog_article.html",
        "featured_alt": "\u05d1\u05d3\u05d9 \u05db\u05d5\u05ea\u05e0\u05d4 \u05dc\u05ea\u05d9\u05e0\u05d5\u05e7 \u05e2\u05dd \u05e2\u05d5\u05e8 \u05e8\u05d2\u05d9\u05e9 \u2014 \u05d1\u05d3 \u05e8\u05da \u05d5\u05e0\u05d5\u05e9\u05dd",
    },
    {
        "id": 681481863481,
        "role": "C2",
        "file": "C:/Users/3024e/Downloads/\u05e7\u05dc\u05d5\u05d3 \u05e7\u05d5\u05d3/teams/organic/hub4-sensitive-baby-skin/HUB4_C2_blog_article.html",
        "featured_alt": "\u05dc\u05de\u05d4 \u05db\u05d5\u05ea\u05e0\u05d4 \u05d8\u05d1\u05e2\u05d9\u05ea \u05d4\u05d8\u05d5\u05d1\u05d4 \u05d1\u05d9\u05d5\u05ea\u05e8 \u05dc\u05ea\u05d9\u05e0\u05d5\u05e7\u05d5\u05ea",
    },
    {
        "id": 681481896249,
        "role": "C3",
        "file": "C:/Users/3024e/Downloads/\u05e7\u05dc\u05d5\u05d3 \u05e7\u05d5\u05d3/teams/organic/hub4-sensitive-baby-skin/HUB4_C3_blog_article.html",
        "featured_alt": "\u05e1\u05d9\u05de\u05e0\u05d9\u05dd \u05dc\u05e2\u05d5\u05e8 \u05e8\u05d2\u05d9\u05e9 \u05d1\u05ea\u05d9\u05e0\u05d5\u05e7 \u2014 \u05d1\u05d9\u05d2\u05d5\u05d3 \u05de\u05ea\u05d0\u05d9\u05dd",
    },
    {
        "id": 681481929017,
        "role": "C4",
        "file": "C:/Users/3024e/Downloads/\u05e7\u05dc\u05d5\u05d3 \u05e7\u05d5\u05d3/teams/organic/hub4-sensitive-baby-skin/HUB4_C4_blog_article.html",
        "featured_alt": "\u05d1\u05d2\u05d3\u05d9 \u05d9\u05d9\u05dc\u05d5\u05d3 \u05d1\u05d8\u05d5\u05d7\u05d9\u05dd \u05dc\u05e2\u05d5\u05e8 \u2014 \u05d7\u05dc\u05d9\u05e4\u05ea \u05db\u05d5\u05ea\u05e0\u05d4 BabyMania",
    },
]


def get_products_with_images():
    """Get product images from CDN 0864/9677/2409, prefer cotton/baby clothing items."""
    resp = requests.get(
        f"{BASE_URL}/products.json",
        headers=_headers(),
        params={"limit": 50},
    )
    resp.raise_for_status()
    products = resp.json()["products"]

    valid = []
    for p in products:
        for img in p.get("images", []):
            src = img.get("src", "")
            if CORRECT_CDN_FRAGMENT in src:
                valid.append(
                    {
                        "product_id": p["id"],
                        "product_title": p["title"],
                        "image_src": src,
                        "image_alt": img.get("alt") or p["title"],
                    }
                )
    return valid


def delete_article(article_id):
    resp = requests.delete(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(),
    )
    return resp.status_code


def update_article_full(article_id, body_html, featured_src, featured_alt):
    payload = {
        "article": {
            "id": article_id,
            "body_html": body_html,
            "image": {"src": featured_src, "alt": featured_alt},
        }
    }
    resp = requests.put(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(),
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["article"]


def main():
    print("=" * 65)
    print("HUB-4 Image Fix — BabyMania")
    print("=" * 65)

    # ── 1. Delete old draft article ──────────────────────────────────
    print(f"\n[1] Deleting article {ARTICLE_TO_DELETE} (sleeping-bag draft)...")
    delete_status = delete_article(ARTICLE_TO_DELETE)
    if delete_status == 200:
        print(f"    ✓ Deleted (HTTP 200)")
    else:
        print(f"    ✗ Status {delete_status} — may already be gone")

    # ── 2. Collect valid product images ─────────────────────────────
    print(f"\n[2] Fetching product images (CDN {CORRECT_CDN_FRAGMENT})...")
    images = get_products_with_images()
    print(f"    Found {len(images)} images from {len(set(i['product_id'] for i in images))} products")
    for img in images:
        print(f"    · {img['product_title']}")
        print(f"      {img['image_src']}")

    if not images:
        print("    ERROR: No valid images — aborting article updates.")
        sys.exit(1)

    # ── 3. Update each HUB-4 article ────────────────────────────────
    print(f"\n[3] Updating 5 HUB-4 articles...")
    results = []

    for idx, article in enumerate(HUB4_ARTICLES):
        print(f"\n    [{article['role']}] id={article['id']}")

        with open(article["file"], "r", encoding="utf-8") as f:
            html = f.read()

        # Find all unique broken URLs in this article
        broken_pattern = re.compile(
            r"https://cdn\.shopify\.com/s/files/1/0891/5765/7897/[^\s\"'<>]+"
        )
        broken_urls = list(dict.fromkeys(broken_pattern.findall(html)))  # unique, ordered
        print(f"    Broken URLs: {len(broken_urls)}")

        # Replace each unique broken URL with a different valid image (round-robin)
        fixed_html = html
        replacements = []
        for j, broken in enumerate(broken_urls):
            replacement = images[(idx * 3 + j) % len(images)]
            fixed_html = fixed_html.replace(broken, replacement["image_src"])
            replacements.append(
                {
                    "original": broken,
                    "replacement": replacement["image_src"],
                    "product": replacement["product_title"],
                }
            )
            print(f"    · {broken.split('/')[-1]} → {replacement['image_src'].split('/')[-1]}")

        remaining = len(re.findall(BROKEN_CDN_FRAGMENT, fixed_html))

        # Featured image for this article
        featured = images[idx % len(images)]
        print(f"    Featured: {featured['image_src'].split('/')[-1]}")

        try:
            updated = update_article_full(
                article["id"],
                fixed_html,
                featured["image_src"],
                article["featured_alt"],
            )
            shopify_featured = (updated.get("image") or {}).get("src", "N/A")
            results.append(
                {
                    "role": article["role"],
                    "article_id": article["id"],
                    "status": "success",
                    "featured_image_set": featured["image_src"],
                    "shopify_confirmed_featured": shopify_featured,
                    "broken_urls_fixed": len(broken_urls),
                    "broken_urls_remaining": remaining,
                    "replacements": replacements,
                }
            )
            print(f"    ✓ Updated on Shopify")
        except Exception as exc:
            results.append(
                {
                    "role": article["role"],
                    "article_id": article["id"],
                    "status": "failed",
                    "error": str(exc),
                }
            )
            print(f"    ✗ FAILED: {exc}")

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"  Draft deleted (id {ARTICLE_TO_DELETE}): {'YES' if delete_status == 200 else 'NO (status ' + str(delete_status) + ')'}")
    total_fixed = 0
    for r in results:
        icon = "✓" if r["status"] == "success" else "✗"
        if r["status"] == "success":
            total_fixed += r["broken_urls_fixed"]
            print(
                f"  {icon} {r['role']:6} ({r['article_id']}) — "
                f"{r['broken_urls_fixed']} broken fixed, "
                f"{r['broken_urls_remaining']} remaining — "
                f"featured: {r['featured_image_set'].split('/')[-1]}"
            )
        else:
            print(f"  {icon} {r['role']:6} ({r['article_id']}) — FAILED: {r.get('error')}")
    print(f"\n  Total broken URLs fixed: {total_fixed}")

    # Save results file
    out = {
        "article_deleted": ARTICLE_TO_DELETE,
        "delete_status": delete_status,
        "images_available": len(images),
        "articles": results,
    }
    out_path = "C:/Projects/baby-mania-agent/HUB4_IMAGE_FIX_RESULTS.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n  Results → {out_path}")


if __name__ == "__main__":
    main()
