"""
Publish HUB-1 Baby Sleep articles to Shopify blogs/news.
Publish order: Pillar → C1 → C2 → C4
"""

import re
import sys
import time
import requests
from pathlib import Path
from shopify_client import _headers, BASE_URL
from qa_gate import preflight_qa_check, check_article_qa, check_product_links

BLOG_ID = 109164036409
STAGE_DIR = Path(r"C:\Projects\baby-mania-agent\output\stage-outputs")

ARTICLES = [
    {
        "file": "10085913231673_blog_article_1.html",
        "cluster_id": "HUB-1-pillar",
        "title": "איך לעזור לתינוק לישון בלילה — המדריך המלא להורים עייפים",
        "handle": "how-to-help-baby-sleep-through-the-night",
        "cluster": "HUB-1-pillar",
        "tags": "baby-sleep,pillar,tofu,HUB-1",
    },
    {
        "file": "10085913231673_blog_article_2.html",
        "cluster_id": "HUB-1-C1",
        "title": "רעש לבן לתינוקות: האם זה באמת עובד?",
        "handle": "white-noise-for-babies",
        "cluster": "HUB-1-C1",
        "tags": "baby-sleep,white-noise,aeo,HUB-1",
    },
    {
        "file": "10085913231673_blog_article_4.html",
        "cluster_id": "HUB-1-C2",
        "title": "שגרת שינה לתינוק: מדריך צעד-אחר-צעד להורים חדשים",
        "handle": "baby-sleep-routine",
        "cluster": "HUB-1-C2",
        "tags": "baby-sleep,sleep-routine,tofu,HUB-1",
    },
    {
        "file": "10085913231673_blog_article_3.html",
        "cluster_id": "HUB-1-C4",
        "title": "מכשיר שינה אחד-לכל לתינוק: מה חשוב לבדוק לפני הקנייה?",
        "handle": "all-in-one-baby-sleep-solution",
        "cluster": "HUB-1-C4",
        "tags": "baby-sleep,all-in-one,bofu,hidden-diamond,HUB-1",
    },
]

# ── QA Pre-flight — all articles must pass before any publish ─────────────────
preflight_qa_check(STAGE_DIR, ARTICLES, "HUB-1 Baby Sleep")


def extract_body_html(html_text):
    """Extract <style> block + page-wrap div for Shopify body_html."""
    # Extract <style> block
    style_match = re.search(r"(<style>.*?</style>)", html_text, re.DOTALL)
    style_block = style_match.group(1) if style_match else ""

    # Extract content inside <body>
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html_text, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else html_text

    return f"{style_block}\n{body_content}"


def create_article(blog_id, title, handle, body_html, tags):
    """POST a new article to Shopify."""
    url = f"{BASE_URL}/blogs/{blog_id}/articles.json"
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


def verify_article(article_id, blog_id):
    """GET article and return its URL."""
    url = f"{BASE_URL}/blogs/{blog_id}/articles/{article_id}.json"
    resp = requests.get(url, headers=_headers())
    resp.raise_for_status()
    a = resp.json()["article"]
    return {
        "id": a["id"],
        "handle": a["handle"],
        "published_at": a.get("published_at"),
        "url": f"https://babymania-il.com/blogs/news/{a['handle']}",
    }


results = []

for i, art in enumerate(ARTICLES, 1):
    check_article_qa(STAGE_DIR, art)  # per-article gate — blocks if QA missing or FAIL
    filepath = STAGE_DIR / art["file"]
    print(f"\n[{i}/4] Publishing {art['cluster']} — {art['title'][:50]}...")

    html_text = filepath.read_text(encoding="utf-8")
    body_html = extract_body_html(html_text)
    check_product_links(body_html, art["cluster_id"])

    article = create_article(
        blog_id=BLOG_ID,
        title=art["title"],
        handle=art["handle"],
        body_html=body_html,
        tags=art["tags"],
    )

    info = verify_article(article["id"], BLOG_ID)

    results.append({
        "cluster": art["cluster"],
        "title": art["title"],
        "shopify_id": article["id"],
        "handle": info["handle"],
        "url": info["url"],
        "published_at": info["published_at"],
        "status": "published" if info["published_at"] else "draft",
    })

    print(f"  ✓ Published: {info['url']}")
    time.sleep(0.5)  # rate-limit buffer


# ── Print results table ──────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("PUBLISH RESULTS")
print("=" * 80)

for r in results:
    print(f"\n  Cluster:     {r['cluster']}")
    print(f"  Handle:      {r['handle']}")
    print(f"  URL:         {r['url']}")
    print(f"  Status:      {r['status']}")
    print(f"  Shopify ID:  {r['shopify_id']}")
    print(f"  Published:   {r['published_at']}")

print("\n" + "=" * 80)
print(f"Total published: {len(results)}/4")
print("=" * 80)
