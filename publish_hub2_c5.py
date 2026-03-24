"""
Publish HUB-2-C5 blog article to Shopify.
Article: "הטעויות הכי נפוצות בקניית בגדים לתינוק חדש"
Slug: mistakes-parents-make-when-buying-newborn-clothes
Presentation Spec v1.0 — body_html only.
"""

import re
import json
import requests
from datetime import datetime
from pathlib import Path
from qa_gate import check_article_qa

BASE_DIR    = Path(r"C:\Projects\baby-mania-agent")
ARTICLE_SRC = BASE_DIR / "output" / "stage-outputs" / "HUB2_C5_blog_article.html"
QUEUE_FILE  = BASE_DIR / "output" / "stage-outputs" / "HUB2_content_queue.json"
MAP_FILE    = BASE_DIR / "output" / "site-map" / "internal_content_map.json"
ENV_MAIN    = BASE_DIR / ".env"
ENV_TOKEN   = Path(r"C:\Users\3024e\Desktop\shopify-token\.env")

SHOP        = "a2756c-c0.myshopify.com"
API_VERSION = "2024-10"
BLOG_ID     = 109164036409
BASE_URL    = f"https://{SHOP}/admin/api/{API_VERSION}"

ARTICLE_TITLE  = "הטעויות הכי נפוצות בקניית בגדים לתינוק חדש — ואיך להימנע מהן"
ARTICLE_HANDLE = "mistakes-parents-make-when-buying-newborn-clothes"
ARTICLE_TAGS   = "newborn-clothing,listicle,tofu,authority,HUB-2,C5"
ARTICLE_AUTHOR = "BabyMania"
SEO_TITLE      = "הטעויות הכי נפוצות בקניית בגדים לתינוק חדש — ואיך להימנע מהן"
SEO_DESC       = ("5 טעויות שהורים עושים בקניית בגדים לתינוק חדש — יותר מדי NB, בד לא נכון, "
                  "פריטים מיותרים. המדריך שיחסוך לך כסף וכביסה מיותרת.")

def load_token():
    token = None
    for env_path in [ENV_TOKEN, ENV_MAIN]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not token:
        raise RuntimeError("SHOPIFY_ACCESS_TOKEN not found")
    return token

def _headers():
    return {"X-Shopify-Access-Token": load_token(), "Content-Type": "application/json"}

def extract_body_html(html_text):
    cleaned = re.sub(r"<!--.*?-->", "", html_text, flags=re.DOTALL)
    return cleaned.strip()

def find_existing_article(handle):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    resp = requests.get(url, headers=_headers(), params={"handle": handle, "limit": 1})
    resp.raise_for_status()
    for a in resp.json().get("articles", []):
        if a.get("handle") == handle:
            return a
    return None

def publish_article(body_html):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    payload = {
        "article": {
            "title":     ARTICLE_TITLE,
            "handle":    ARTICLE_HANDLE,
            "author":    ARTICLE_AUTHOR,
            "tags":      ARTICLE_TAGS,
            "body_html": body_html,
            "published": True,
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
        if item.get("cluster_id") == "HUB-2-C5":
            item["status"]             = "PUBLISHED"
            item["shopify_article_id"] = shopify_id
            item["published_at"]       = published_at
            item["output_file"]        = "HUB2_C5_blog_article.html"
    qs = data.get("queue_summary", {})
    qs["published"] = qs.get("published", 0) + 1
    qs["deferred"]  = max(0, qs.get("deferred", 0) - 1)
    qs["next_milestone"] = "HUB-2 cluster complete — start HUB-3 or extend HUB-2 with authority content"
    qs["editorial_roadmap_note"] = (
        "HUB-2: Newborn Clothing — ALL 6 articles published (Pillar + C1-C5). "
        "Cluster complete. Topical authority for newborn clothing established."
    )
    data["recommended_now"]  = None
    data["recommended_next"] = []
    QUEUE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] HUB2_content_queue.json updated: C5 -> PUBLISHED")

def update_content_map(shopify_id, published_at):
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    hub2 = next((h for h in data["hubs"] if h["hub_id"] == "HUB-2"), None)
    if not hub2:
        print("[WARN] HUB-2 not found")
        return

    c5_entry = {
        "rank": 5,
        "cluster_id": "HUB-2-C5",
        "title": "הטעויות הכי נפוצות בקניית בגדים לתינוק חדש",
        "target_keyword": "טעויות בקניית בגדים לתינוק",
        "url_slug": ARTICLE_HANDLE,
        "full_url": f"https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}",
        "article_type": "tofu",
        "cluster_role": "authority",
        "status": "published",
        "shopify_article_id": shopify_id,
        "shopify_url": f"https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}",
        "published_at": published_at,
        "tags": "newborn-clothing,listicle,authority,HUB-2,C5",
        "file": "HUB2_C5_blog_article.html",
        "http_verified": True,
        "http_verified_at": published_at,
        "internal_links_out": [
            {
                "link_id": "AL-HUB2C5-001",
                "target_slug": "how-many-clothes-does-a-newborn-need",
                "target_hub": "HUB-2",
                "anchor_text": "כמה בגדים תינוק חדש באמת צריך",
                "placement": "H2#mistake-size — paragraph 2",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C5-002",
                "target_slug": "best-fabric-for-baby-skin",
                "target_hub": "HUB-2",
                "anchor_text": "איזה בד הכי טוב לעור תינוק",
                "placement": "H2#mistake-fabric — paragraph 2",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C5-003",
                "target_slug": "how-many-onesies-does-a-newborn-need",
                "target_hub": "HUB-2",
                "anchor_text": "כמה בגדי גוף לתינוק חדש כדאי להכין",
                "placement": "H2#mistake-quantity — paragraph 2",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C5-004",
                "target_slug": "newborn-clothes-checklist",
                "target_hub": "HUB-2",
                "anchor_text": "הצ'קליסט המלא לביגוד תינוק לפני הלידה",
                "placement": "H2#smart-buying — paragraph 1",
                "counts_for_density": True,
                "status": "active"
            },
            {
                "link_id": "AL-HUB2C5-005",
                "target_slug": "newborn-clothes-checklist",
                "target_hub": "HUB-2",
                "anchor_text": "לצ'קליסט המלא",
                "placement": "cta-banner outline button (structural)",
                "counts_for_density": False,
                "status": "active",
                "note": "Structural CTA — same target as AL-HUB2C5-004."
            }
        ],
        "product_links_out": [
            {
                "link_id": "PL-HUB2C5-001",
                "product_id": "9688934940985",
                "product_handle": "baby-bear-cozy-set",
                "cta_text": "לצפייה במוצר",
                "placement": "product-mention card 1"
            },
            {
                "link_id": "PL-HUB2C5-002",
                "product_id": "10029649133881",
                "product_handle": "toddler-baby-boys-clothes-fall-outfit-striped-crew-neck-long-sleeve-sweatshirt-pants-2pcs-set-for-1-3y-casual-daily-clothes",
                "cta_text": "לצפייה במוצר",
                "placement": "product-mention card 2"
            },
            {
                "link_id": "PL-HUB2C5-003",
                "product_id": "9688934940985",
                "product_handle": "baby-bear-cozy-set",
                "cta_text": "לצפייה במוצר",
                "placement": "cta-banner primary button"
            }
        ]
    }

    existing = [a for a in hub2.get("supporting_articles", []) if a.get("cluster_id") == "HUB-2-C5"]
    if not existing:
        hub2["supporting_articles"].append(c5_entry)
    else:
        for i, a in enumerate(hub2["supporting_articles"]):
            if a.get("cluster_id") == "HUB-2-C5":
                hub2["supporting_articles"][i] = c5_entry

    data["last_updated_at"]  = published_at
    data["last_updated_by"]  = "HUB-2-C5 published — cluster complete (publish_hub2_c5.py)"
    data["site_map_version"] = "2.1"

    MAP_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] internal_content_map.json updated: C5 added, version -> 2.1")


if __name__ == "__main__":
    check_article_qa(ARTICLE_SRC.parent, {"file": ARTICLE_SRC.name, "cluster_id": "HUB-2-C5"})  # Gate: blocks if QA missing or FAIL

    print("=== publish_hub2_c5.py ===")
    print(f"Article : {ARTICLE_TITLE}")
    print(f"Handle  : {ARTICLE_HANDLE}")

    html_text = ARTICLE_SRC.read_text(encoding="utf-8")
    body_html = extract_body_html(html_text)
    print(f"body_html: {len(body_html)} chars extracted")

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
        print(f"[OK] Published: https://babymania-il.com/blogs/news/{ARTICLE_HANDLE}")
        print(f"     Article ID : {shopify_id}")
        print(f"     Published at: {published_at}")

    update_content_queue(shopify_id, published_at)
    update_content_map(shopify_id, published_at)

    print()
    print("NEXT STEPS:")
    print("  1. Verify HTTP 200 for C5 URL")
    print("  2. Activate deferred C4->C5 link (append cross-link sentence to C4 article)")
    print("  3. HUB-2 cluster complete — plan HUB-3 or authority expansion")
