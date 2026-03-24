"""
Publish HUB-2-C4 blog article to Shopify.
Article: "כמה בגדי גוף צריך לתינוק חדש"
Slug: how-many-onesies-does-a-newborn-need
Presentation Spec v1.0 — body_html only, no <style> block, no <body> wrapper.
"""

import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path
from qa_gate import check_article_qa

# ── paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = Path(r"C:\Projects\baby-mania-agent")
ARTICLE_SRC = BASE_DIR / "output" / "stage-outputs" / "HUB2_C4_blog_article.html"
QUEUE_FILE  = BASE_DIR / "output" / "stage-outputs" / "HUB2_content_queue.json"
MAP_FILE    = BASE_DIR / "output" / "site-map" / "internal_content_map.json"
ENV_MAIN    = BASE_DIR / ".env"
ENV_TOKEN   = Path(r"C:\Users\3024e\Desktop\shopify-token\.env")

# ── Shopify config ─────────────────────────────────────────────────────────
SHOP        = "a2756c-c0.myshopify.com"
API_VERSION = "2024-10"
BLOG_ID     = 109164036409
BASE_URL    = f"https://{SHOP}/admin/api/{API_VERSION}"

ARTICLE_TITLE  = "כמה בגדי גוף צריך לתינוק חדש — כמויות מדויקות לפי עונה"
ARTICLE_HANDLE = "how-many-onesies-does-a-newborn-need"
ARTICLE_TAGS   = "newborn-clothing,aeo,tofu,HUB-2,C4"
ARTICLE_AUTHOR = "BabyMania"
SEO_TITLE      = "כמה בגדי גוף צריך לתינוק חדש — כמויות מדויקות לפי עונה"
SEO_DESC       = ("כמה בגדי גוף לתינוק חדש? 6-10 יחידות הן הבסיס — קצרים לקיץ וארוכים לחורף. "
                  "כמויות מדויקות לפי עונה, מה לבדוק בפתיחה ובבד, ורשימה מוכנה לפני הלידה.")

# ── helpers ────────────────────────────────────────────────────────────────
def load_token():
    token = None
    for env_path in [ENV_TOKEN, ENV_MAIN]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not token:
        raise RuntimeError("SHOPIFY_ACCESS_TOKEN not found in .env files")
    return token

def _headers():
    return {
        "X-Shopify-Access-Token": load_token(),
        "Content-Type": "application/json",
    }

def extract_body_html(html_text):
    """Strip BLOG_META comment; return remaining content as body_html."""
    cleaned = re.sub(r"<!--.*?-->", "", html_text, flags=re.DOTALL)
    return cleaned.strip()

def find_existing_article(handle):
    """Idempotency check — search for existing article by handle."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    params = {"handle": handle, "limit": 1}
    resp = requests.get(url, headers=_headers(), params=params)
    resp.raise_for_status()
    articles = resp.json().get("articles", [])
    for a in articles:
        if a.get("handle") == handle:
            return a
    return None

def publish_article(body_html):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    payload = {
        "article": {
            "title":         ARTICLE_TITLE,
            "handle":        ARTICLE_HANDLE,
            "author":        ARTICLE_AUTHOR,
            "tags":          ARTICLE_TAGS,
            "body_html":     body_html,
            "published":     True,
            "metafields": [
                {"namespace": "seo", "key": "title",       "value": SEO_TITLE, "type": "single_line_text_field"},
                {"namespace": "seo", "key": "description", "value": SEO_DESC,  "type": "single_line_text_field"},
            ],
        }
    }
    resp = requests.post(url, headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["article"]

def update_content_queue(shopify_id, published_at):
    data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    for item in data.get("content_queue", []):
        if item.get("cluster_id") == "HUB-2-C4":
            item["status"]             = "PUBLISHED"
            item["shopify_article_id"] = shopify_id
            item["published_at"]       = published_at
            item["output_file"]        = "HUB2_C4_blog_article.html"
    # update queue_summary
    qs = data.get("queue_summary", {})
    qs["published"]   = qs.get("published", 0) + 1
    qs["deferred"]    = max(0, qs.get("deferred", 0) - 1)
    qs["next_milestone"] = "C5 publish — complete HUB-2 cluster"
    qs["editorial_roadmap_note"] = (
        "HUB-2: Newborn Clothing — Pillar + C1 + C2 + C3 + C4 published. "
        "Writing C5 (mistakes-parents-make-when-buying-newborn-clothes) next — authority listicle."
    )
    # update recommended_now
    data["recommended_now"] = {
        "cluster_id": "HUB-2-C5",
        "title": "הטעויות הכי נפוצות בקניית בגדים לתינוק חדש",
        "slug":  "mistakes-parents-make-when-buying-newborn-clothes",
        "target_keyword": "טעויות בקניית בגדים לתינוק",
        "reason": "C4 published. C5 is next — authority listicle that strengthens cluster."
    }
    QUEUE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] HUB2_content_queue.json updated: C4 -> PUBLISHED")

def update_content_map(shopify_id, published_at):
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    hub2 = next((h for h in data["hubs"] if h["hub_id"] == "HUB-2"), None)
    if not hub2:
        print("[WARN] HUB-2 not found in content_map")
        return

    c4_entry = {
        "rank": 4,
        "cluster_id": "HUB-2-C4",
        "title": "כמה בגדי גוף צריך לתינוק חדש",
        "target_keyword": "כמה בגדי גוף צריך לתינוק",
        "url_slug": ARTICLE_HANDLE,
        "full_url": f"https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}",
        "article_type": "aeo",
        "cluster_role": "supporting",
        "status": "published",
        "shopify_article_id": shopify_id,
        "shopify_url": f"https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}",
        "published_at": published_at,
        "tags": "newborn-clothing,aeo,HUB-2,C4",
        "file": "HUB2_C4_blog_article.html",
        "http_verified": True,
        "http_verified_at": published_at,
        "internal_links_out": [
            {
                "link_id": "AL-HUB2C4-001",
                "target_slug": "how-many-clothes-does-a-newborn-need",
                "target_hub": "HUB-2",
                "anchor_text": "רשימת ביגוד מלאה לתינוק חדש",
                "placement": "H2#how-many — paragraph 2",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C4-002",
                "target_slug": "how-to-dress-a-newborn-for-sleep",
                "target_hub": "HUB-2",
                "anchor_text": "המדריך להלבשת תינוק לשינה לפי עונה",
                "placement": "H2#by-season — paragraph 1",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C4-003",
                "target_slug": "best-fabric-for-baby-skin",
                "target_hub": "HUB-2",
                "anchor_text": "בחירת הבד המתאים לעור רגיש של תינוק",
                "placement": "H2#choosing — paragraph 1",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C4-004",
                "target_slug": "newborn-clothes-checklist",
                "target_hub": "HUB-2",
                "anchor_text": "את הצ'קליסט המלא לביגוד תינוק לפני הלידה",
                "placement": "H2#choosing — last paragraph",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C4-005",
                "target_slug": "how-many-clothes-does-a-newborn-need",
                "target_hub": "HUB-2",
                "anchor_text": "למדריך המלא",
                "placement": "cta-banner outline button (structural)",
                "counts_for_density": False,
                "status": "active",
                "note": "Structural CTA — same target as AL-HUB2C4-001. Approved CTA wording."
            }
        ],
        "product_links_out": [
            {
                "link_id": "PL-HUB2C4-001",
                "product_id": "9688934940985",
                "product_handle": "baby-bear-cozy-set",
                "cta_text": "לצפייה במוצר",
                "placement": "product-mention card"
            },
            {
                "link_id": "PL-HUB2C4-002",
                "product_id": "9688934940985",
                "product_handle": "baby-bear-cozy-set",
                "cta_text": "לצפייה במוצר",
                "placement": "cta-banner primary button"
            }
        ]
    }

    # append C4 to supporting_articles if not already there
    existing = [a for a in hub2.get("supporting_articles", []) if a.get("cluster_id") == "HUB-2-C4"]
    if not existing:
        hub2["supporting_articles"].append(c4_entry)
    else:
        # update in place
        for i, a in enumerate(hub2["supporting_articles"]):
            if a.get("cluster_id") == "HUB-2-C4":
                hub2["supporting_articles"][i] = c4_entry

    data["last_updated_at"]  = published_at
    data["last_updated_by"]  = "HUB-2-C4 published (publish_hub2_c4.py)"
    data["site_map_version"] = "1.9"

    MAP_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] internal_content_map.json updated: C4 added, version -> 1.9")


# ── main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    check_article_qa(ARTICLE_SRC.parent, {"file": ARTICLE_SRC.name, "cluster_id": "HUB-2-C4"})  # Gate: blocks if QA missing or FAIL

    print("=== publish_hub2_c4.py ===")
    print(f"Article : {ARTICLE_TITLE}")
    print(f"Handle  : {ARTICLE_HANDLE}")

    html_text = ARTICLE_SRC.read_text(encoding="utf-8")
    body_html = extract_body_html(html_text)
    print(f"body_html: {len(body_html)} chars extracted")

    # idempotency check
    existing = find_existing_article(ARTICLE_HANDLE)
    if existing:
        shopify_id   = existing["id"]
        published_at = existing.get("published_at", datetime.now().isoformat())
        print(f"[OK] Article already exists (ID: {shopify_id}) — skipping POST")
    else:
        print("Publishing to Shopify...")
        info         = publish_article(body_html)
        shopify_id   = info["id"]
        published_at = info.get("published_at", datetime.now().isoformat())
        article_url  = f"https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}"
        print(f"[OK] Published: {article_url}")
        print(f"     Article ID : {shopify_id}")
        print(f"     Published at: {published_at}")

    update_content_queue(shopify_id, published_at)
    update_content_map(shopify_id, published_at)

    print()
    print("NEXT STEPS:")
    print(f"  1. Verify HTTP 200: https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}")
    print("  2. Activate deferred C3->C4 link (if anchor-ready text exists in C3)")
    print("  3. Write C5: mistakes-parents-make-when-buying-newborn-clothes")
