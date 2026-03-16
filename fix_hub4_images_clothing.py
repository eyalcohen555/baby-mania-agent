#!/usr/bin/env python3
"""
Fix HUB-4 articles — round 2:
  Replace all images (featured + body) with clothing/cotton products only.
  Filter keywords: romper, cotton, bodysuit, סרבל, אוברול, חליפה, בגד גוף, כותנה
  Exclude: sandals, shoes, נעל, נעליים
"""

import sys
import json
import re
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, "C:/Projects/baby-mania-agent")
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
BROKEN_CDN_FRAGMENT = "0891/5765/7897"

CLOTHING_KEYWORDS = [
    "romper", "cotton", "bodysuit", "סרבל", "אוברול",
    "חליפה", "בגד גוף", "כותנה", "outfit", "sweatshirt",
    "pants", "set", "sleeve", "infant", "newborn", "toddler",
]
EXCLUDE_KEYWORDS = ["sandal", "shoe", "נעל", "נעליים", "sock", "גרב"]

HUB4_ARTICLES = [
    {
        "id": 681481797945,
        "role": "Pillar",
        "file": "C:/Users/3024e/Downloads/קלוד קוד/teams/organic/hub4-sensitive-baby-skin/HUB4_Pillar_blog_article.html",
        "featured_alt": "טיפול בעור רגיש של תינוק — ביגוד כותנה רך ועדין",
    },
    {
        "id": 681481830713,
        "role": "C1",
        "file": "C:/Users/3024e/Downloads/קלוד קוד/teams/organic/hub4-sensitive-baby-skin/HUB4_C1_blog_article.html",
        "featured_alt": "בדי כותנה לתינוק עם עור רגיש — בד רך ונושם",
    },
    {
        "id": 681481863481,
        "role": "C2",
        "file": "C:/Users/3024e/Downloads/קלוד קוד/teams/organic/hub4-sensitive-baby-skin/HUB4_C2_blog_article.html",
        "featured_alt": "למה כותנה טבעית הטובה ביותר לתינוקות",
    },
    {
        "id": 681481896249,
        "role": "C3",
        "file": "C:/Users/3024e/Downloads/קלוד קוד/teams/organic/hub4-sensitive-baby-skin/HUB4_C3_blog_article.html",
        "featured_alt": "סימנים לעור רגיש בתינוק — ביגוד מתאים",
    },
    {
        "id": 681481929017,
        "role": "C4",
        "file": "C:/Users/3024e/Downloads/קלוד קוד/teams/organic/hub4-sensitive-baby-skin/HUB4_C4_blog_article.html",
        "featured_alt": "בגדי יילוד בטוחים לעור — חליפת כותנה BabyMania",
    },
]


def get_clothing_images():
    """Return images from products whose title matches clothing keywords."""
    resp = requests.get(
        f"{BASE_URL}/products.json",
        headers=_headers(),
        params={"limit": 250},
    )
    resp.raise_for_status()
    products = resp.json()["products"]

    valid = []
    skipped = []

    for p in products:
        title_lower = p["title"].lower()

        # Skip if any exclude keyword matches
        if any(kw in title_lower for kw in EXCLUDE_KEYWORDS):
            skipped.append(p["title"])
            continue

        # Accept if any clothing keyword matches
        if not any(kw.lower() in title_lower for kw in CLOTHING_KEYWORDS):
            continue

        for img in p.get("images", []):
            src = img.get("src", "")
            if "0864/9677/2409" not in src:
                continue
            valid.append(
                {
                    "product_id": p["id"],
                    "product_title": p["title"],
                    "image_src": src,
                    "image_alt": img.get("alt") or p["title"],
                }
            )

    return valid, skipped


def get_current_article(article_id):
    """Fetch live body_html from Shopify (not local file)."""
    resp = requests.get(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(),
    )
    resp.raise_for_status()
    return resp.json()["article"]


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


def replace_images_in_html(html, images, article_idx):
    """
    Replace EVERY <img> src in the html with a clothing image.
    Strategy: each unique src gets its own image (round-robin from the pool).
    Returns (fixed_html, replacements_list).
    """
    img_pattern = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', re.IGNORECASE)
    seen = {}      # original src → replacement index
    counter = [0]  # mutable counter for closure

    def replacer(m):
        prefix, src, suffix = m.group(1), m.group(2), m.group(3)
        if src not in seen:
            pool_idx = (article_idx * 5 + counter[0]) % len(images)
            seen[src] = pool_idx
            counter[0] += 1
        img = images[seen[src]]
        return prefix + img["image_src"] + suffix

    fixed = img_pattern.sub(replacer, html)

    replacements = [
        {
            "original_filename": orig.split("/")[-1].split("?")[0],
            "replacement_src": images[idx]["image_src"],
            "product": images[idx]["product_title"],
        }
        for orig, idx in seen.items()
    ]
    return fixed, replacements


def main():
    print("=" * 65)
    print("HUB-4 Image Fix (clothing only) — BabyMania")
    print("=" * 65)

    # ── 1. Collect clothing images ───────────────────────────────────
    print("\n[1] Fetching clothing/cotton images from CDN 0864/9677/2409...")
    images, skipped = get_clothing_images()

    unique_products = list({i["product_id"]: i["product_title"] for i in images}.items())
    print(f"    Clothing products found : {len(unique_products)}")
    print(f"    Total images available  : {len(images)}")
    print(f"    Excluded (shoes etc.)   : {len(skipped)}")
    print("\n    Products used:")
    for pid, ptitle in unique_products:
        count = sum(1 for i in images if i["product_id"] == pid)
        print(f"    · [{pid}] {ptitle} ({count} images)")

    if not images:
        print("\n    ERROR: No clothing images found — aborting.")
        sys.exit(1)

    # ── 2. Update each article ───────────────────────────────────────
    print("\n[2] Updating 5 HUB-4 articles (live body_html from Shopify)...")
    results = []

    for idx, article in enumerate(HUB4_ARTICLES):
        print(f"\n    [{article['role']}] id={article['id']}")

        # Fetch the CURRENT live HTML (already has previous replacements)
        live = get_current_article(article["id"])
        html = live.get("body_html", "")

        fixed_html, replacements = replace_images_in_html(html, images, idx)

        remaining_broken = html.count(BROKEN_CDN_FRAGMENT)

        # Featured image: first image in the pool slice for this article
        featured = images[idx % len(images)]
        print(f"    Images replaced in body : {len(replacements)}")
        for r in replacements:
            print(f"    · {r['original_filename']} → {r['replacement_src'].split('/')[-1].split('?')[0]}")
            print(f"      ({r['product']})")
        print(f"    Featured: {featured['image_src'].split('/')[-1].split('?')[0]}")
        print(f"      ({featured['product_title']})")

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
                    "featured_image": featured["image_src"],
                    "featured_product": featured["product_title"],
                    "shopify_confirmed_featured": shopify_featured,
                    "images_replaced_in_body": len(replacements),
                    "broken_cdn_remaining": remaining_broken,
                    "replacements": replacements,
                }
            )
            print(f"    OK — updated on Shopify")
        except Exception as exc:
            results.append(
                {
                    "role": article["role"],
                    "article_id": article["id"],
                    "status": "failed",
                    "error": str(exc),
                }
            )
            print(f"    FAILED: {exc}")

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    for r in results:
        icon = "OK" if r["status"] == "success" else "FAIL"
        if r["status"] == "success":
            print(
                f"  [{icon}] {r['role']:6} ({r['article_id']}) "
                f"— {r['images_replaced_in_body']} imgs replaced "
                f"— featured: {r['featured_image'].split('/')[-1].split('?')[0]}"
            )
            print(f"           product: {r['featured_product']}")
        else:
            print(f"  [{icon}] {r['role']:6} ({r['article_id']}) — {r.get('error')}")

    out_path = "C:/Projects/baby-mania-agent/HUB4_IMAGE_FIX_CLOTHING_RESULTS.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {"images_pool_size": len(images), "articles": results},
            f, ensure_ascii=False, indent=2,
        )
    print(f"\n  Results -> {out_path}")


if __name__ == "__main__":
    main()
