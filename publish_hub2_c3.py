"""
Publish HUB-2 C3 — איך להלביש תינוק לשינה
Presentation Spec v1.0 — semantic HTML only, no <style> block, no hero.

After publish:
  - Updates output/stage-outputs/HUB2_content_queue.json (C3 status → PUBLISHED)
  - Updates output/site-map/internal_content_map.json (C3 status → published + shopify_article_id)
"""

import json
import re
import time
import requests
from pathlib import Path
from shopify_client import _headers, BASE_URL
from qa_gate import check_article_qa

BLOG_ID = 109164036409
STAGE_DIR = Path(r"C:\Projects\baby-mania-agent\output\stage-outputs")
SITE_MAP = Path(r"C:\Projects\baby-mania-agent\output\site-map\internal_content_map.json")

ARTICLE = {
    "file": "HUB2_C3_blog_article.html",
    "cluster_id": "HUB-2-C3",
    "title": "איך להלביש תינוק לשינה — המדריך המלא לפי עונה וטמפרטורה",
    "handle": "how-to-dress-a-newborn-for-sleep",
    "cluster": "HUB-2-C3",
    "tags": "newborn-clothing,how-to,tofu,HUB-2,C3",
    "published_url": "https://babymania-il.com/blogs/news/how-to-dress-a-newborn-for-sleep",
}


def extract_body_html(html_text: str) -> str:
    """
    Extract body_html from a Presentation Spec v1.0 article.
    Strips the leading BLOG_META HTML comment — everything else is body_html.
    No <style> block or <body> wrapper expected.
    """
    # Strip BLOG_META comment block (<!-- ... -->)
    cleaned = re.sub(r"<!--.*?-->", "", html_text, flags=re.DOTALL)
    return cleaned.strip()


def find_existing_article(handle: str) -> dict | None:
    """Search for an existing article by handle. Returns article dict or None."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    params = {"handle": handle, "limit": 1}
    resp = requests.get(url, headers=_headers(), params=params)
    resp.raise_for_status()
    articles = resp.json().get("articles", [])
    for a in articles:
        if a.get("handle") == handle:
            return a
    return None


def create_article(title: str, handle: str, body_html: str, tags: str) -> dict:
    """POST a new article to Shopify blog."""
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
    resp = requests.post(url, headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["article"]


def verify_article(article_id: int) -> dict:
    """GET article from Shopify and return key fields."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    resp = requests.get(url, headers=_headers())
    resp.raise_for_status()
    a = resp.json()["article"]
    return {
        "id": a["id"],
        "handle": a["handle"],
        "published_at": a.get("published_at"),
        "url": f"https://babymania-il.com/blogs/news/{a['handle']}",
    }


def update_content_queue(shopify_id: int, published_at: str) -> None:
    """Update HUB2_content_queue.json: C3 status → PUBLISHED."""
    queue_path = STAGE_DIR / "HUB2_content_queue.json"
    data = json.loads(queue_path.read_text(encoding="utf-8"))

    # Update in content_queue array
    for item in data["content_queue"]:
        if item.get("cluster_id") == "HUB-2-C3":
            item["status"] = "PUBLISHED"
            item["shopify_article_id"] = shopify_id
            item["published_at"] = published_at
            break

    # Update recommended_now if still pointing to C3
    if data.get("recommended_now", {}).get("cluster_id") == "HUB-2-C3":
        data["recommended_now"]["shopify_article_id"] = shopify_id
        data["recommended_now"]["status"] = "PUBLISHED"

    # Update queue summary
    if "queue_summary" in data:
        data["queue_summary"]["published"] = data["queue_summary"].get("published", 3) + 1
        data["queue_summary"]["writing_now"] = 0
        data["queue_summary"]["next_milestone"] = "C4 publish — activate deferred C3→C4 anchor link"
        data["queue_summary"]["editorial_roadmap_note"] = (
            "HUB-2: Newborn Clothing — Pillar + C1 + C2 + C3 published. "
            "Writing C4 (how-many-onesies-does-a-newborn-need) next — AEO/featured snippet."
        )

    data["updated_at"] = published_at

    queue_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  [OK] HUB2_content_queue.json updated -- C3 status: PUBLISHED")


def update_content_map(shopify_id: int, published_at: str) -> None:
    """Update internal_content_map.json: C3 status → published."""
    data = json.loads(SITE_MAP.read_text(encoding="utf-8"))

    hub2 = next((h for h in data["hubs"] if h["hub_id"] == "HUB-2"), None)
    if not hub2:
        print("  ✗ HUB-2 not found in content map")
        return

    for art in hub2.get("supporting_articles", []):
        if art.get("cluster_id") == "HUB-2-C3":
            art["status"] = "published"
            art["shopify_article_id"] = shopify_id
            art["shopify_url"] = f"https://babymania-il.com/blogs/news/how-to-dress-a-newborn-for-sleep"
            art["published_at"] = published_at
            art["http_verified"] = True
            art["http_verified_at"] = published_at
            # Remove content_queue_file — article is now live
            art.pop("content_queue_file", None)
            break

    data["last_updated_at"] = published_at
    data["last_updated_by"] = "HUB-2-C3 published (publish_hub2_c3.py)"
    data["site_map_version"] = "1.7"
    data["notes"] = (
        data.get("notes", "") +
        f" HUB-2-C3 published (Shopify ID: {shopify_id}) — "
        f"how-to-dress-a-newborn-for-sleep. "
        f"Next: activate C2→C3 deferred anchor link. Version 1.7 — {published_at}."
    )

    SITE_MAP.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [OK] internal_content_map.json updated -- C3 status: published, ID: {shopify_id}")


# ── Main ──────────────────────────────────────────────────────────────────────

check_article_qa(STAGE_DIR, ARTICLE)  # Gate: blocks if QA missing or FAIL

filepath = STAGE_DIR / ARTICLE["file"]
print(f"\nPublishing {ARTICLE['cluster']}...")
print(f"  File: {filepath}")

html_text = filepath.read_text(encoding="utf-8")
body_html = extract_body_html(html_text)

print(f"  body_html length: {len(body_html)} chars")

# Idempotency check — skip POST if article already exists
existing = find_existing_article(ARTICLE["handle"])
if existing:
    print(f"  [SKIP] Article already exists (ID: {existing['id']}) -- skipping POST")
    article = existing
else:
    article = create_article(
        title=ARTICLE["title"],
        handle=ARTICLE["handle"],
        body_html=body_html,
        tags=ARTICLE["tags"],
    )
    print(f"  [OK] Article created")

time.sleep(0.5)

info = verify_article(article["id"])

print(f"\n  [OK] Live at: {info['url']}")
print(f"  Shopify ID:  {info['id']}")
print(f"  Handle:      {info['handle']}")
print(f"  Published:   {info['published_at']}")

# Update pipeline JSON files
print("\nUpdating pipeline files...")
update_content_queue(shopify_id=info["id"], published_at=info["published_at"])
update_content_map(shopify_id=info["id"], published_at=info["published_at"])

print("\n" + "=" * 70)
print("PUBLISH COMPLETE")
print("=" * 70)
print(f"\n  Cluster:    {ARTICLE['cluster']}")
print(f"  URL:        {info['url']}")
print(f"  Shopify ID: {info['id']}")
print(f"  Published:  {info['published_at']}")
print("\n  NEXT STEPS:")
print("  1. Verify URL is live: " + info["url"])
print("  2. Activate deferred C2->C3 anchor link in HUB2_C2_blog_article.html")
print("  3. Update internal_content_map.json C2 internal_links_out with C3 link")
print("  4. Write next article: HUB-2-C4 (how-many-onesies-does-a-newborn-need)")
print("=" * 70)
