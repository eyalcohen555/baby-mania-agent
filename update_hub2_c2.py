"""
Update HUB-2 C2 in Shopify — activate deferred C2->C3 anchor link.
Article: newborn-clothes-checklist (ID: 681356132665)
Change: adds C3 link in H2#day-night paragraph (line ~590)
"""

import re
import requests
from pathlib import Path
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
ARTICLE_ID = 681356132665
STAGE_DIR = Path(r"C:\Projects\baby-mania-agent\output\stage-outputs")
ARTICLE_FILE = "HUB2_C2_blog_article.html"
C3_SLUG = "how-to-dress-a-newborn-for-sleep"
C3_URL = f"https://babymania-il.com/blogs/news/{C3_SLUG}"


def extract_body_html(html_text: str) -> str:
    """Strip BLOG_META comment; return remaining content as body_html."""
    cleaned = re.sub(r"<!--.*?-->", "", html_text, flags=re.DOTALL)
    return cleaned.strip()


def update_article(article_id: int, body_html: str) -> dict:
    """PUT updated body_html to Shopify article."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(url, headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["article"]


def verify_article(article_id: int) -> dict:
    """GET article and return key fields."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    resp = requests.get(url, headers=_headers())
    resp.raise_for_status()
    a = resp.json()["article"]
    return {
        "id": a["id"],
        "handle": a["handle"],
        "updated_at": a.get("updated_at"),
        "url": f"https://babymania-il.com/blogs/news/{a['handle']}",
    }


# ── Main ──────────────────────────────────────────────────────────────────────

filepath = STAGE_DIR / ARTICLE_FILE
print(f"\nUpdating HUB-2-C2 — Article ID {ARTICLE_ID}")
print(f"  File: {filepath}")

html_text = filepath.read_text(encoding="utf-8")
body_html = extract_body_html(html_text)

# Verify C3 link is present in updated file
if C3_URL not in body_html:
    print(f"  [ERROR] C3 link not found in body_html. Aborting.")
    raise SystemExit(1)

print(f"  [OK] C3 link found in body_html")
print(f"  body_html length: {len(body_html)} chars")
print(f"  Sending PUT to Shopify...")

article = update_article(ARTICLE_ID, body_html)
info = verify_article(ARTICLE_ID)

print(f"\n  [OK] Updated: {info['url']}")
print(f"  Article ID:  {info['id']}")
print(f"  Updated at:  {info['updated_at']}")

print("\n" + "=" * 70)
print("C2 UPDATE COMPLETE")
print("=" * 70)
print(f"  Article:    newborn-clothes-checklist")
print(f"  URL:        {info['url']}")
print(f"  Link added: {C3_URL}")
print(f"  Anchor:     how-to-dress-a-newborn-for-sleep")
print(f"  Updated:    {info['updated_at']}")
print("=" * 70)
