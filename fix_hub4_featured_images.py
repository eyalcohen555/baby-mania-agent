#!/usr/bin/env python3
"""
Update featured images only for 5 HUB-4 articles.
Each article gets a different product/keyword.
"""

import sys
import json
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, "C:/Projects/baby-mania-agent")
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
CDN = "0864/9677/2409"

# Each article: which keywords to match (in order of preference), alt text
ARTICLE_TARGETS = [
    {
        "id": 681481797945,
        "role": "Pillar",
        "keywords": ["romper", "סרבל"],
        "alt": "סרבל כותנה רך לתינוק עם עור רגיש — BabyMania",
    },
    {
        "id": 681481830713,
        "role": "C1",
        "keywords": ["bodysuit", "בגד גוף"],
        "alt": "בגד גוף כותנה נושם לתינוק — הבד הטוב ביותר לעור רגיש",
    },
    {
        "id": 681481863481,
        "role": "C2",
        "keywords": ["cotton", "כותנה"],
        "alt": "חליפת כותנה טבעית לתינוק — למה כותנה הטובה ביותר לעור רגיש",
    },
    {
        "id": 681481896249,
        "role": "C3",
        "keywords": ["onesie", "אוברול"],
        "alt": "אוברול לתינוק עם עור רגיש — סימנים ובחירת ביגוד נכון",
    },
    {
        "id": 681481929017,
        "role": "C4",
        "keywords": ["חליפה", "set"],
        "alt": "חליפת תינוק בטוחה לעור יילוד — מדריך בחירת ביגוד ראשון",
    },
]


def get_all_products():
    resp = requests.get(
        f"{BASE_URL}/products.json",
        headers=_headers(),
        params={"limit": 250},
    )
    resp.raise_for_status()
    return resp.json()["products"]


def find_best_image(products, keywords, used_product_ids):
    """
    Find the first product image that:
    - Matches any of the given keywords (in title, case-insensitive)
    - Has an image from CDN 0864/9677/2409
    - Product not already used in a previous article
    Returns (product_title, image_src) or None.
    """
    for kw in keywords:
        for p in products:
            if p["id"] in used_product_ids:
                continue
            if kw.lower() not in p["title"].lower():
                continue
            for img in p.get("images", []):
                src = img.get("src", "")
                if CDN in src:
                    return p["title"], src, p["id"]
    return None, None, None


def set_featured_image(article_id, image_src, alt):
    payload = {
        "article": {
            "id": article_id,
            "image": {"src": image_src, "alt": alt},
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
    print("HUB-4 Featured Image Diversification — BabyMania")
    print("=" * 65)

    print("\n[1] Loading products...")
    products = get_all_products()
    print(f"    {len(products)} products loaded")

    print("\n[2] Matching products to articles...")
    used_ids = set()
    selections = []

    for target in ARTICLE_TARGETS:
        title, src, pid = find_best_image(products, target["keywords"], used_ids)
        if src:
            used_ids.add(pid)
            selections.append({**target, "product_title": title, "image_src": src, "product_id": pid})
            print(f"    [{target['role']}] keywords={target['keywords']}")
            print(f"           product : {title}")
            print(f"           image   : {src.split('/')[-1].split('?')[0]}")
        else:
            selections.append({**target, "product_title": None, "image_src": None, "product_id": None})
            print(f"    [{target['role']}] NO MATCH for {target['keywords']}")

    print("\n[3] Updating featured images on Shopify...")
    results = []

    for sel in selections:
        role = sel["role"]
        if not sel["image_src"]:
            print(f"    [{role}] SKIP — no image found")
            results.append({"role": role, "article_id": sel["id"], "status": "skipped"})
            continue

        try:
            updated = set_featured_image(sel["id"], sel["image_src"], sel["alt"])
            confirmed = (updated.get("image") or {}).get("src", "N/A")
            results.append({
                "role": role,
                "article_id": sel["id"],
                "status": "success",
                "product": sel["product_title"],
                "image_src": sel["image_src"],
                "shopify_confirmed": confirmed,
            })
            print(f"    [{role}] OK — {sel['product_title']}")
            print(f"           {sel['image_src'].split('/')[-1].split('?')[0]}")
        except Exception as exc:
            results.append({"role": role, "article_id": sel["id"], "status": "failed", "error": str(exc)})
            print(f"    [{role}] FAILED: {exc}")

    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    for r in results:
        icon = "OK" if r["status"] == "success" else ("SKIP" if r["status"] == "skipped" else "FAIL")
        line = f"  [{icon}] {r['role']:6} ({r['article_id']})"
        if r["status"] == "success":
            line += f" — {r['product']}"
        elif r["status"] == "failed":
            line += f" — {r.get('error')}"
        print(line)

    out_path = "C:/Projects/baby-mania-agent/HUB4_FEATURED_IMAGES_RESULTS.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n  Results -> {out_path}")


if __name__ == "__main__":
    main()
