"""
Activate staged internal links in published Shopify blog articles.
Fetches current body_html, wraps anchor text with <a> tags, PUTs back.
"""

import re
import time
import requests
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409

ACTIVATIONS = [
    {
        "article": "white-noise-for-babies",
        "article_id": 681272115513,
        "links": [
            {
                "id": "AL-C1-001",
                "anchor": "\u05d4\u05de\u05d3\u05e8\u05d9\u05da \u05d4\u05de\u05dc\u05d0 \u05dc\u05e9\u05d9\u05e0\u05ea \u05ea\u05d9\u05e0\u05d5\u05e7\u05d5\u05ea \u05d1\u05dc\u05d9\u05dc\u05d4",
                "href": "https://www.babymania-il.com/blogs/news/how-to-help-baby-sleep-through-the-night",
            },
            {
                "id": "AL-C1-002",
                "anchor": "\u05e9\u05d2\u05e8\u05ea \u05e9\u05d9\u05e0\u05d4 \u05e7\u05d1\u05d5\u05e2\u05d4 \u05d5\u05e2\u05e7\u05d1\u05d9\u05ea",
                "href": "https://www.babymania-il.com/blogs/news/baby-sleep-routine",
            },
        ],
    },
    {
        "article": "all-in-one-baby-sleep-solution",
        "article_id": 681272246585,
        "links": [
            {
                "id": "AL-C4-001",
                "anchor": "\u05d4\u05de\u05d3\u05e8\u05d9\u05da \u05d4\u05de\u05dc\u05d0 \u05dc\u05e9\u05d9\u05e0\u05ea \u05ea\u05d9\u05e0\u05d5\u05e7\u05d5\u05ea \u05d1\u05dc\u05d9\u05dc\u05d4",
                "href": "https://www.babymania-il.com/blogs/news/how-to-help-baby-sleep-through-the-night",
            },
            {
                "id": "AL-C4-002",
                "anchor": "\u05e8\u05e2\u05e9 \u05dc\u05d1\u05df \u05dc\u05ea\u05d9\u05e0\u05d5\u05e7\u05d5\u05ea \u2014 \u05d4\u05d0\u05dd \u05d6\u05d4 \u05e2\u05d5\u05d1\u05d3?",
                "href": "https://www.babymania-il.com/blogs/news/white-noise-for-babies",
            },
        ],
    },
]


def fetch_body_html(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    resp = requests.get(url, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()["article"]["body_html"]


def wrap_anchor(html, anchor_text, href):
    """Wrap bare anchor_text with <a href> — only if not already linked."""
    # Check if already wrapped
    if f'href="{href}"' in html or f"href='{href}'" in html:
        already = True
        return html, already, False

    # Escape for regex
    escaped = re.escape(anchor_text)

    # Match anchor text NOT already inside an <a> tag
    # Negative lookbehind: not preceded by > (inside tag) — use word boundary
    pattern = r"(?<!href=[\"'])(?<![>=])(" + escaped + r")(?![^<]*</a>)"

    # More robust: match text that is not inside an existing <a href
    # Strategy: replace only the first occurrence that is not already linked
    new_html, count = re.subn(
        r"(?<![\"'>])(" + escaped + r")(?=(?:[^<]|<(?!/?a\b))*?(?:<|$))",
        lambda m: f'<a href="{href}">{m.group(1)}</a>',
        html,
        count=1,
    )

    if count == 0:
        return html, False, False  # text not found

    return new_html, False, True  # wrapped successfully


def put_body_html(article_id, body_html):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(url, headers=_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["article"]


def verify_link(article_id, href):
    body = fetch_body_html(article_id)
    return href in body


results = []

for group in ACTIVATIONS:
    art_name = group["article"]
    art_id = group["article_id"]

    print(f"\nFetching {art_name} (id={art_id})...")
    body = fetch_body_html(art_id)
    modified = False

    for link in group["links"]:
        anchor = link["anchor"]
        href = link["href"]

        new_body, already, wrapped = wrap_anchor(body, anchor, href)

        if already:
            status = "ALREADY_ACTIVE"
            body = new_body
        elif wrapped:
            body = new_body
            modified = True
            status = "WRAPPED"
            print(f"  [{link['id']}] Wrapped: {anchor[:40]}")
        else:
            status = "NOT_FOUND"
            print(f"  [{link['id']}] WARNING: anchor text not found in HTML")

        results.append({
            "link_id": link["id"],
            "article": art_name,
            "anchor": anchor,
            "href": href,
            "wrap_status": status,
        })

    if modified:
        print(f"  PUTting updated body_html...")
        put_body_html(art_id, body)
        time.sleep(1)

        # Verify each link
        refreshed = fetch_body_html(art_id)
        for r in results:
            if r["article"] == art_name and r["wrap_status"] in ("WRAPPED",):
                r["verified"] = r["href"] in refreshed
    else:
        for r in results:
            if r["article"] == art_name:
                r["verified"] = r["wrap_status"] == "ALREADY_ACTIVE"

    time.sleep(1)


print()
print("=" * 72)
print("ACTIVATION RESULTS")
print("=" * 72)
print(f"{'ID':<12} {'Article':<32} {'Wrap':<14} {'Verified'}")
print("-" * 72)
for r in results:
    print(
        f"{r['link_id']:<12} {r['article']:<32} {r['wrap_status']:<14} {str(r.get('verified','—'))}"
    )

print()
print("=" * 72)
print("DETAIL")
print("=" * 72)
for r in results:
    print(f"\n  {r['link_id']}")
    print(f"    Article: {r['article']}")
    print(f"    Anchor:  {r['anchor']}")
    print(f"    Target:  {r['href']}")
    print(f"    Status:  {r['wrap_status']}  |  Verified: {r.get('verified','—')}")
