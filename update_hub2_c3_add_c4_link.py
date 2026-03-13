"""
Activate deferred C3->C4 link.
Adds cross-link sentence to HUB2_C3_blog_article.html, updates Shopify article,
and registers AL-HUB2C3-005 in internal_content_map.json.
"""

import os
import re
import json
import requests
from pathlib import Path

BASE_DIR    = Path(r"C:\Projects\baby-mania-agent")
ARTICLE_SRC = BASE_DIR / "output" / "stage-outputs" / "HUB2_C3_blog_article.html"
MAP_FILE    = BASE_DIR / "output" / "site-map" / "internal_content_map.json"
ENV_MAIN    = BASE_DIR / ".env"
ENV_TOKEN   = Path(r"C:\Users\3024e\Desktop\shopify-token\.env")

SHOP        = "a2756c-c0.myshopify.com"
API_VERSION = "2024-10"
BLOG_ID     = 109164036409
ARTICLE_ID  = 681362456889   # C3 Shopify article ID
BASE_URL    = f"https://{SHOP}/admin/api/{API_VERSION}"

C4_URL = "https://babymania-il.com/blogs/news/how-many-onesies-does-a-newborn-need"

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

def update_article(article_id, body_html):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(url, headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["article"]

def update_content_map(updated_at):
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    hub2 = next((h for h in data["hubs"] if h["hub_id"] == "HUB-2"), None)
    if not hub2:
        print("[WARN] HUB-2 not found")
        return
    c3 = next((a for a in hub2["supporting_articles"] if a.get("cluster_id") == "HUB-2-C3"), None)
    if not c3:
        print("[WARN] C3 not found in content_map")
        return

    new_link = {
        "link_id": "AL-HUB2C3-005",
        "target_slug": "how-many-onesies-does-a-newborn-need",
        "target_hub": "HUB-2",
        "anchor_text": "כמה בגדי גוף לתינוק חדש כדאי להכין",
        "placement": "H2#room-temp — last paragraph (appended cross-link sentence after C4 publish)",
        "counts_for_density": True,
        "status": "active",
        "activated_at": updated_at,
        "method": "appended cross-link sentence — C4 was deferred at C3 generation time"
    }
    links = c3.setdefault("internal_links_out", [])
    if not any(l.get("link_id") == "AL-HUB2C3-005" for l in links):
        links.append(new_link)

    data["last_updated_at"]  = updated_at
    data["last_updated_by"]  = "HUB-2-C3 updated — C3->C4 deferred link activated (update_hub2_c3_add_c4_link.py)"
    data["site_map_version"] = "2.0"

    MAP_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] internal_content_map.json: AL-HUB2C3-005 added, version -> 2.0")

if __name__ == "__main__":
    print("=== Activate deferred C3->C4 link ===")
    html_text = ARTICLE_SRC.read_text(encoding="utf-8")
    body_html = extract_body_html(html_text)
    print(f"body_html: {len(body_html)} chars")

    result = update_article(ARTICLE_ID, body_html)
    updated_at = result.get("updated_at", "2026-03-10T20:00:00+02:00")
    print(f"[OK] Updated: https://babymania-il.com/blogs/news/how-to-dress-a-newborn-for-sleep")
    print(f"     Article ID : {ARTICLE_ID}")
    print(f"     Updated at : {updated_at}")

    update_content_map(updated_at)
    print()
    print("[OK] C3->C4 deferred link activated")
    print("     Return: C3_LINK_TO_C4_ACTIVATED")
