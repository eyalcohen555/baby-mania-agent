#!/usr/bin/env python3
"""Publish HUB-9 Reborn Pillar to Shopify blog — single article only."""
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Users\3024e\Desktop\shopify-token\.env")

SHOP = "a2756c-c0.myshopify.com"
TOKEN = os.environ["SHOPIFY_ACCESS_TOKEN"]
BLOG_ID = "109164036409"
API_VERSION = "2024-10"
BASE_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

ARTICLE_FILE = r"C:\Projects\baby-mania-agent\output\hub9-reborn\HUB9_Pillar_blog_article.html"

META = {
    "title": "בובת ריבורן — המדריך המלא: מה זה, איך לבחור ולמי זה מתאים",
    "handle": "bobat-reborn-madrih-male-ma-ze-ech-livhor",
    "tags": "reborn,pillar,tofu,HUB-9,בובת-ריבורן",
    "seo_title": "בובת ריבורן — המדריך המלא: מה זה, איך לבחור ולמי זה מתאים",
    "meta_description": "גלו מה זו בובת ריבורן, מה ההבדל בין ויניל לסיליקון, איזו מידה לבחור ולמי זה מתאים. המדריך המלא לפני הקנייה.",
}


def read_html(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # Strip leading HTML comment block (metadata header)
    content = re.sub(r'^<!--.*?-->\s*', '', content, flags=re.DOTALL)
    return content.strip()


def publish_article(meta, body_html):
    payload = {
        "article": {
            "title": meta["title"],
            "handle": meta["handle"],
            "body_html": body_html,
            "tags": meta["tags"],
            "metafields": [
                {"namespace": "seo", "key": "title", "value": meta["seo_title"], "type": "single_line_text_field"},
                {"namespace": "seo", "key": "description", "value": meta["meta_description"], "type": "single_line_text_field"},
            ],
            "published": True,
        }
    }
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    resp = requests.post(url, headers=HEADERS, json=payload)
    return resp.status_code, resp.json()


def verify_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    a = resp.json()["article"]
    return {
        "id": a["id"],
        "handle": a["handle"],
        "published_at": a.get("published_at"),
        "url": f"https://babymania-il.com/blogs/news/{a['handle']}",
    }


def main():
    print("=" * 60)
    print("PUBLISH: HUB-9 Reborn Pillar")
    print("=" * 60)

    body_html = read_html(ARTICLE_FILE)
    print(f"Article loaded: {len(body_html)} chars")
    print(f"Title:  {META['title']}")
    print(f"Handle: {META['handle']}")
    print()

    print("Publishing to Shopify...")
    status, data = publish_article(META, body_html)

    if status == 201:
        article = data["article"]
        article_id = article["id"]
        print(f"  POST OK (201) — article id: {article_id}")

        print("Verifying...")
        info = verify_article(article_id)
        print()
        print("=" * 60)
        print("PUBLISH RESULT")
        print("=" * 60)
        print(f"  article_id:   {info['id']}")
        print(f"  handle:       {info['handle']}")
        print(f"  url:          {info['url']}")
        print(f"  published_at: {info['published_at']}")
        print(f"  status:       {'LIVE' if info['published_at'] else 'DRAFT'}")
        print("=" * 60)
    else:
        print(f"  FAILED ({status}): {data}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
