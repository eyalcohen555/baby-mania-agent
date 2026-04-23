"""
publish_hub9_clusters.py
Single-use script — publish HUB-9 clusters C1-C6 to Shopify.
Order: C2 → C1 → C3 → C4 → C5 → C6 (per approved plan)
"""

import json
import os
import requests
from datetime import datetime

# ─── Config ──────────────────────────────────────────────────────────────────
SHOP_URL    = "a2756c-c0.myshopify.com"
ACCESS_TOKEN = "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"
API_VERSION  = "2024-10"
BLOG_ID      = 109164036409
BASE          = f"https://{SHOP_URL}/admin/api/{API_VERSION}"
HEADERS       = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
}
OUTPUT_DIR = r"C:\Projects\baby-mania-agent\output\hub9-reborn"

# ─── Publish plan — ORDERED ──────────────────────────────────────────────────
CLUSTERS = [
    {
        "id": "C2",
        "file": "HUB9_C2_blog_article.html",
        "title": "בגדי ריבורן — מה לובשים, איזה מידה מתאימה ואיפה מוצאים",
        "handle": "bigdei-reborn-ma-hilobshot-eizeh-midah-matima",
    },
    {
        "id": "C1",
        "file": "HUB9_C1_blog_article.html",
        "title": "איך לבחור בובת ריבורן — מדריך לרוכש הראשון",
        "handle": "eich-livhor-bobat-reborn-madrih-larokhesh-harishon",
    },
    {
        "id": "C3",
        "file": "HUB9_C3_blog_article.html",
        "title": "בובת ריבורן כמתנה — מי זה מתאים לו ומה לבקש",
        "handle": "bobat-reborn-kematana-mi-matim-mah-levakesh",
    },
    {
        "id": "C4",
        "file": "HUB9_C4_blog_article.html",
        "title": "איך לטפל בבובת ריבורן — שמירה, ניקוי ואחסון",
        "handle": "eich-letapel-bobat-reborn-shmirah-nikuy-achsun",
    },
    {
        "id": "C5",
        "file": "HUB9_C5_blog_article.html",
        "title": "ריבורן לילדים vs. ריבורן לאספנים — מה ההבדל ואיזה מתאים לכם",
        "handle": "reborn-leyeladim-vs-reborn-leasefanim-mah-hahedel",
    },
    {
        "id": "C6",
        "file": "HUB9_C6_blog_article.html",
        "title": "השוואת בובות ריבורן — מידות, חומרים ותכונות: כל הדגמים במקום אחד",
        "handle": "hashvahat-bobot-reborn-midot-khomrim-tekhunyot",
    },
]

BLOG_BASE_URL = "https://babymania-il.com/blogs/news"


def publish_article(cluster: dict) -> dict:
    """POST article to Shopify. Returns result dict."""
    file_path = os.path.join(OUTPUT_DIR, cluster["file"])
    with open(file_path, "r", encoding="utf-8") as f:
        body_html = f.read()

    payload = {
        "article": {
            "title": cluster["title"],
            "body_html": body_html,
            "handle": cluster["handle"],
            "published": True,
        }
    }

    url = f"{BASE}/blogs/{BLOG_ID}/articles.json"
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)

    if resp.status_code != 201:
        return {
            "id": cluster["id"],
            "status": "FAIL",
            "http_code": resp.status_code,
            "error": resp.text[:500],
        }

    data = resp.json()["article"]
    final_handle = data.get("handle", cluster["handle"])
    return {
        "id": cluster["id"],
        "status": "PASS",
        "article_id": data["id"],
        "handle": final_handle,
        "url": f"{BLOG_BASE_URL}/{final_handle}",
        "published_at": data.get("published_at", ""),
    }


def verify_article(result: dict) -> dict:
    """GET article from Shopify to confirm it's live."""
    url = f"{BASE}/blogs/{BLOG_ID}/articles/{result['article_id']}.json"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        return {**result, "verify": "FAIL", "verify_code": resp.status_code}
    data = resp.json()["article"]
    return {
        **result,
        "verify": "PASS",
        "published_at_confirmed": data.get("published_at", ""),
        "url_ok": True,
    }


def main():
    results = []
    print("=" * 60)
    print("HUB-9 CLUSTER PUBLISH — START")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    for cluster in CLUSTERS:
        print(f"\n[PUBLISH] {cluster['id']}: {cluster['title'][:50]}...")
        result = publish_article(cluster)

        if result["status"] == "FAIL":
            print(f"  FAIL -- HTTP {result['http_code']}: {result['error']}")
            results.append(result)
            print("\nSTOPPING -- publish failed.")
            break

        print(f"  PASS -- article_id={result['article_id']}, handle={result['handle']}")
        print(f"  URL: {result['url']}")

        # Verify
        print(f"  [VERIFY] {cluster['id']}...")
        verified = verify_article(result)
        if verified["verify"] == "PASS":
            print(f"  VERIFY PASS -- published_at={verified['published_at_confirmed']}")
        else:
            print(f"  VERIFY FAIL -- HTTP {verified.get('verify_code')}")
            results.append(verified)
            print("\nSTOPPING -- verify failed.")
            break

        results.append(verified)

    # Output JSON for next step (placeholder replacement)
    output_file = os.path.join(OUTPUT_DIR, "HUB9_CLUSTER_PUBLISH_RESULTS.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"RESULTS SAVED: {output_file}")
    print("=" * 60)
    print("\nPUBLISH SUMMARY:")
    for r in results:
        status = r.get("status", "?")
        verify = r.get("verify", "—")
        article_id = r.get("article_id", "—")
        url = r.get("url", "—")
        print(f"  {r['id']} | {status} / verify:{verify} | id={article_id} | {url}")

    all_pass = all(r.get("status") == "PASS" and r.get("verify") == "PASS" for r in results)
    print(f"\nFINAL: {'ALL PASS ✓' if all_pass else 'PARTIAL / FAIL ✗'}")
    print(f"Articles published: {sum(1 for r in results if r.get('status') == 'PASS')}/6")


if __name__ == "__main__":
    main()
