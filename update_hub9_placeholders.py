"""
update_hub9_placeholders.py
Replace all [CLUSTER-URL:Cx] and [HUB-2-PILLAR-URL] placeholders in 7 HTML files,
then PUT each updated article back to Shopify.
"""

import os
import requests
from datetime import datetime

SHOP_URL     = "a2756c-c0.myshopify.com"
ACCESS_TOKEN = "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"
API_VERSION  = "2024-10"
BLOG_ID      = 109164036409
BASE         = f"https://{SHOP_URL}/admin/api/{API_VERSION}"
HEADERS      = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
}
OUTPUT_DIR = r"C:\Projects\baby-mania-agent\output\hub9-reborn"

BLOG_BASE = "https://babymania-il.com/blogs/news"

CLUSTER_URLS = {
    "C1": f"{BLOG_BASE}/eich-livhor-bobat-reborn-madrih-larokhesh-harishon",
    "C2": f"{BLOG_BASE}/bigdei-reborn-ma-hilobshot-eizeh-midah-matima",
    "C3": f"{BLOG_BASE}/bobat-reborn-kematana-mi-matim-mah-levakesh",
    "C4": f"{BLOG_BASE}/eich-letapel-bobat-reborn-shmirah-nikuy-achsun",
    "C5": f"{BLOG_BASE}/reborn-leyeladim-vs-reborn-leasefanim-mah-hahedel",
    "C6": f"{BLOG_BASE}/hashvahat-bobot-reborn-midot-khomrim-tekhunyot",
}
HUB2_PILLAR_URL = f"{BLOG_BASE}/how-many-clothes-does-a-newborn-need"

ARTICLES = [
    {"name": "Pillar", "file": "HUB9_Pillar_blog_article.html",  "article_id": 685558825273},
    {"name": "C1",     "file": "HUB9_C1_blog_article.html",      "article_id": 686018756921},
    {"name": "C2",     "file": "HUB9_C2_blog_article.html",      "article_id": 686018724153},
    {"name": "C3",     "file": "HUB9_C3_blog_article.html",      "article_id": 686018789689},
    {"name": "C4",     "file": "HUB9_C4_blog_article.html",      "article_id": 686018822457},
    {"name": "C5",     "file": "HUB9_C5_blog_article.html",      "article_id": 686018855225},
    {"name": "C6",     "file": "HUB9_C6_blog_article.html",      "article_id": 686018887993},
]


def resolve_placeholders(html: str) -> tuple[str, int]:
    count = 0
    for cx, url in CLUSTER_URLS.items():
        placeholder = f"[CLUSTER-URL:{cx}]"
        n = html.count(placeholder)
        if n:
            html = html.replace(placeholder, url)
            count += n
    n = html.count("[HUB-2-PILLAR-URL]")
    if n:
        html = html.replace("[HUB-2-PILLAR-URL]", HUB2_PILLAR_URL)
        count += n
    return html, count


def put_article(article_id: int, body_html: str) -> dict:
    url = f"{BASE}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(url, headers=HEADERS, json=payload, timeout=60)
    return {"http_code": resp.status_code, "ok": resp.status_code == 200}


def main():
    print("=" * 60)
    print("HUB-9 PLACEHOLDER UPDATE + PUT")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    all_ok = True
    for art in ARTICLES:
        file_path = os.path.join(OUTPUT_DIR, art["file"])
        print(f"\n[{art['name']}] Reading {art['file']}...")
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        updated_html, replaced = resolve_placeholders(html)
        print(f"  Placeholders replaced: {replaced}")

        # Save updated file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_html)
        print(f"  File saved.")

        # PUT to Shopify
        print(f"  [PUT] article_id={art['article_id']}...")
        result = put_article(art["article_id"], updated_html)
        if result["ok"]:
            print(f"  PUT PASS -- HTTP 200")
        else:
            print(f"  PUT FAIL -- HTTP {result['http_code']}")
            all_ok = False
            print("\nSTOPPING -- PUT failed.")
            break

    print("\n" + "=" * 60)
    print(f"FINAL: {'ALL PASS' if all_ok else 'FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
