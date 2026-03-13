"""
Activate deferred C4->C5 link.
Updates C4 article in Shopify and registers AL-HUB2C4-006 in content_map.
"""

import re
import json
import requests
from pathlib import Path

BASE_DIR    = Path(r"C:\Projects\baby-mania-agent")
ARTICLE_SRC = BASE_DIR / "output" / "stage-outputs" / "HUB2_C4_blog_article.html"
MAP_FILE    = BASE_DIR / "output" / "site-map" / "internal_content_map.json"
ENV_MAIN    = BASE_DIR / ".env"
ENV_TOKEN   = Path(r"C:\Users\3024e\Desktop\shopify-token\.env")

SHOP        = "a2756c-c0.myshopify.com"
API_VERSION = "2024-10"
BLOG_ID     = 109164036409
ARTICLE_ID  = 681363439929   # C4 Shopify article ID
BASE_URL    = f"https://{SHOP}/admin/api/{API_VERSION}"

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
    resp = requests.put(url, headers=_headers(), json={"article": {"id": article_id, "body_html": body_html}})
    resp.raise_for_status()
    return resp.json()["article"]

def update_content_map(updated_at):
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    hub2 = next((h for h in data["hubs"] if h["hub_id"] == "HUB-2"), None)
    if not hub2:
        return
    c4 = next((a for a in hub2["supporting_articles"] if a.get("cluster_id") == "HUB-2-C4"), None)
    if not c4:
        return

    new_link = {
        "link_id": "AL-HUB2C4-006",
        "target_slug": "mistakes-parents-make-when-buying-newborn-clothes",
        "target_hub": "HUB-2",
        "anchor_text": "הטעויות הנפוצות ביותר בקניית בגדים לתינוק",
        "placement": "H2#choosing — last paragraph (appended cross-link sentence after C5 publish)",
        "counts_for_density": True,
        "status": "active",
        "activated_at": updated_at,
        "method": "appended cross-link sentence — C5 was deferred at C4 generation time"
    }
    links = c4.setdefault("internal_links_out", [])
    if not any(l.get("link_id") == "AL-HUB2C4-006" for l in links):
        links.append(new_link)

    data["last_updated_at"]  = updated_at
    data["last_updated_by"]  = "HUB-2-C4 updated — C4->C5 deferred link activated (update_hub2_c4_add_c5_link.py)"
    data["site_map_version"] = "2.2"

    MAP_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] internal_content_map.json: AL-HUB2C4-006 added, version -> 2.2")

if __name__ == "__main__":
    print("=== Activate deferred C4->C5 link ===")
    html_text = ARTICLE_SRC.read_text(encoding="utf-8")
    body_html = extract_body_html(html_text)
    print(f"body_html: {len(body_html)} chars")

    result = update_article(ARTICLE_ID, body_html)
    updated_at = result.get("updated_at", "2026-03-10T20:00:00+02:00")
    print(f"[OK] Updated: https://babymania-il.com/blogs/news/how-many-onesies-does-a-newborn-need")
    print(f"     Article ID : {ARTICLE_ID}")
    print(f"     Updated at : {updated_at}")

    update_content_map(updated_at)
    print()
    print("[OK] C4->C5 deferred link activated")
    print("     Return: C4_LINK_TO_C5_ACTIVATED")
