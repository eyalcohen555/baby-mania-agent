"""
upload_hub5_images.py — HUB-5 Image Fix
==========================================
מחליף URL תמונות שבורות (1/0891/5765/7897) בתמונות מוצר אמיתיות
מה-CDN הנכון (1/0864/9677/2409) ומעדכן את Shopify.

Article IDs from HUB5_PUBLISH_RESULTS.json:
  Pillar : 681842737465
  C1     : 681842770233
  C2     : 681842803001
  C3     : 681842835769
  C4     : 681842868537
  C5     : 681842901305
  C6     : 681842934073
"""

import sys
import time
import json
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

import requests
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
HUB5_DIR = Path("C:/Projects/baby-mania-agent/output/hub5-baby-gifts")

# ── Real CDN base ──────────────────────────────────────────────────────────────
CDN = "https://cdn.shopify.com/s/files/1/0864/9677/2409/files"

# ── URL mapping: broken filename → real CDN URL ───────────────────────────────
# Pillar: מדריך מלא למתנות לתינוק
PILLAR_IMGS = {
    "baby-gift-ideas-israel-hero.jpg":
        f"{CDN}/ChatGPT_Image_Jan_27_2026_04_09_17_PM.png?v=1769524436",
    "baby-shower-gift-ideas-israel.jpg":
        f"{CDN}/ChatGPT_Image_Jan_27_2026_04_55_58_PM.png?v=1769526177",
    "new-mom-gift-visit-hospital-israel.jpg":
        f"{CDN}/ChatGPT_Image_Jan_27_2026_03_49_41_PM.png?v=1769521890",
}

# C1: בייבי שאוור
C1_IMGS = {
    "baby-shower-gift-ideas-israel.jpg":
        f"{CDN}/42f49328-1594-4fdf-8cc2-b359667445cf.jpg?v=1746697744",
    "baby-shower-gift-list-empty.jpg":
        f"{CDN}/Sa20037070c8244d0b0c21bf4f9e88e4dd.webp?v=1769523493",
    "baby-clothes-size-guide-gifting.jpg":
        f"{CDN}/62adf992-df02-464f-9d63-1a55a4a0d863.jpg?v=1728924099",
}

# C2: מתנות מעשיות
C2_IMGS = {
    "practical-baby-gifts-new-parents.jpg":
        f"{CDN}/d43e6f3d-436b-4497-96b5-976fa2f37f76.jpg?v=1770538773",
    "newborn-daily-essentials-gift.jpg":
        f"{CDN}/Sf0ff4b7bd0114877a25db722551fc8a7b.webp?v=1769519949",
    "what-not-to-buy-baby-gifts.jpg":
        f"{CDN}/S420b0837e75640f7a93143f65d5009c7X.webp?v=1760535705",
}

# C3: מתנות יוקרה
C3_IMGS = {
    "luxury-baby-gift-premium-set.jpg":
        f"{CDN}/c6d89a5c8bf622eaab351179cc5fb0b7.jpg?v=1729800915",
    "lino-baby-set-knit-european.jpg":
        f"{CDN}/Sa20037070c8244d0b0c21bf4f9e88e4dd_b8ed8e5c-f014-4db9-9714-75a8a8b80925.webp?v=1769523493",
    "luxury-baby-gift-list-flatlay.jpg":
        f"{CDN}/2b05a6e8b835b68b3c155f570ce24bf2_b2f0eacc600a.jpg?v=1769528813",
    "luxury-baby-gift-wrapping-box.jpg":
        f"{CDN}/047bc011-6dd2-4533-9388-616eeac202f3.jpg?v=1770538773",
}

# C4: מה אמא חדשה צריכה
C4_IMGS = {
    "new-mom-postpartum-needs-gift.jpg":
        f"{CDN}/ChatGPT_Image_Jan_27_2026_05_13_48_PM.png?v=1769527042",
    "what-not-to-buy-new-mom-gift.jpg":
        f"{CDN}/Secda05f8ceb2459bb18479877e23bbf5F.webp?v=1745508459",
    "lumi-romper-newborn-cotton.jpg":
        f"{CDN}/S39567ae13db44b12b09db2ff0405810db.webp?v=1769526177",
    "visit-new-mom-bring-food-gift.jpg":
        f"{CDN}/b46fe081-4471-486e-a69b-09e4eff6e96f.jpg?v=1730028486",
}

# C5: מתנות לתינוק ראשון
C5_IMGS = {
    "first-baby-gift-guide-israel.jpg":
        f"{CDN}/ChatGPT_Image_Feb_8_2026_09_42_46_AM.png?v=1770536862",
    "baby-gift-practical-checklist.jpg":
        f"{CDN}/Sadc180df6b7d4aecaa3615405d4976a4L.webp?v=1769519949",
    "baby-gift-what-not-to-buy.jpg":
        f"{CDN}/S9a6a9251711a44fbae1fc113f9880916N.webp?v=1754215955",
}

# C6: סט מתנה לתינוק
C6_IMGS = {
    "baby-gift-bundle-set-premium.jpg":
        f"{CDN}/ChatGPT_Image_Feb_8_2026_10_15_06_AM.png?v=1770538773",
    "baby-gift-set-coordinating-fabric.jpg":
        f"{CDN}/S7ed254d9be004833b16756470a11464eh.webp?v=1760206928",
    "baby-gift-bundle-budget-guide.jpg":
        f"{CDN}/58bff239-2a25-4192-92d8-7f4203e1f895.jpg?v=1728924099",
}

# ── Article definitions ────────────────────────────────────────────────────────
ARTICLES = [
    {
        "cluster_id": "HUB-5-Pillar",
        "article_id": 681842737465,
        "file": "HUB5_Pillar_blog_article.html",
        "img_map": PILLAR_IMGS,
    },
    {
        "cluster_id": "HUB-5-C1",
        "article_id": 681842770233,
        "file": "HUB5_C1_blog_article.html",
        "img_map": C1_IMGS,
    },
    {
        "cluster_id": "HUB-5-C2",
        "article_id": 681842803001,
        "file": "HUB5_C2_blog_article.html",
        "img_map": C2_IMGS,
    },
    {
        "cluster_id": "HUB-5-C3",
        "article_id": 681842835769,
        "file": "HUB5_C3_blog_article.html",
        "img_map": C3_IMGS,
    },
    {
        "cluster_id": "HUB-5-C4",
        "article_id": 681842868537,
        "file": "HUB5_C4_blog_article.html",
        "img_map": C4_IMGS,
    },
    {
        "cluster_id": "HUB-5-C5",
        "article_id": 681842901305,
        "file": "HUB5_C5_blog_article.html",
        "img_map": C5_IMGS,
    },
    {
        "cluster_id": "HUB-5-C6",
        "article_id": 681842934073,
        "file": "HUB5_C6_blog_article.html",
        "img_map": C6_IMGS,
    },
]


def fix_html_images(html: str, img_map: dict) -> tuple[str, int]:
    """Replace broken image src URLs with real ones. Returns (fixed_html, count)."""
    count = 0
    for broken_filename, real_url in img_map.items():
        broken_url = f"https://cdn.shopify.com/s/files/1/0891/5765/7897/files/{broken_filename}"
        if broken_url in html:
            html = html.replace(broken_url, real_url)
            count += 1
    return html, count


def update_shopify_article(article_id: int, body_html: str) -> dict:
    """Update article body_html in Shopify."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(url, json=payload, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()["article"]


def main():
    print(f"\n{'='*65}")
    print("BabyMania — HUB-5 Image Fix")
    print(f"Replacing broken CDN URLs with real product images")
    print(f"{'='*65}\n")

    results = []
    total_imgs = 0

    for i, art in enumerate(ARTICLES, 1):
        cid = art["cluster_id"]
        filepath = HUB5_DIR / art["file"]

        print(f"[{i}/7] {cid} — {art['file']}")

        if not filepath.exists():
            print(f"  [ERR] File not found: {filepath}")
            results.append({"cluster_id": cid, "status": "ERROR", "error": "file not found"})
            continue

        # Read and fix HTML
        original_html = filepath.read_text(encoding="utf-8")
        fixed_html, img_count = fix_html_images(original_html, art["img_map"])

        print(f"  Images fixed in HTML: {img_count}/{len(art['img_map'])}")

        if img_count == 0:
            print(f"  [WARN] No broken URLs found — skipping Shopify update")
            results.append({"cluster_id": cid, "status": "SKIPPED", "imgs_fixed": 0})
            continue

        # Save fixed HTML locally
        filepath.write_text(fixed_html, encoding="utf-8")
        print(f"  Local file updated.")

        # Update Shopify
        try:
            updated = update_shopify_article(art["article_id"], fixed_html)
            total_imgs += img_count
            print(f"  [OK] Shopify updated — article {updated['id']}")
            results.append({
                "cluster_id": cid,
                "status": "UPDATED",
                "article_id": updated["id"],
                "imgs_fixed": img_count,
                "updated_at": updated.get("updated_at", ""),
            })
        except requests.exceptions.HTTPError as e:
            print(f"  [ERR] Shopify update failed: {e.response.status_code} — {e.response.text[:200]}")
            results.append({"cluster_id": cid, "status": "ERROR", "error": str(e)})

        if i < len(ARTICLES):
            time.sleep(0.6)

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("RESULTS:")
    for r in results:
        status = r["status"]
        imgs = r.get("imgs_fixed", 0)
        print(f"  {status:8s}  {r['cluster_id']:15s}  תמונות: {imgs}")

    updated = [r for r in results if r["status"] == "UPDATED"]
    errors = [r for r in results if r["status"] == "ERROR"]
    print(f"\nסה\"כ מאמרים עודכנו: {len(updated)}/7")
    print(f"סה\"כ תמונות הוחלפו: {total_imgs}")
    if errors:
        print(f"שגיאות: {len(errors)}")
    print(f"{'='*65}\n")

    # Save results
    results_file = HUB5_DIR / "HUB5_IMAGE_FIX_RESULTS.json"
    results_file.write_text(
        json.dumps({"hub_id": "HUB-5", "results": results, "total_images_fixed": total_imgs},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Results saved: {results_file}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
