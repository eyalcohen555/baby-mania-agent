"""
Publish HUB-4 (Sensitive Baby Skin) — 5 articles to Shopify Blog
Blog: news (ID: 109164036409)
"""

import json
import re
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import requests
from shopify_client import _headers, BASE_URL
from qa_gate import preflight_qa_check, check_article_qa

BLOG_ID = 109164036409
HUB4_DIR = Path(r"C:\Users\3024e\Downloads\קלוד קוד\teams\organic\hub4-sensitive-baby-skin")

# Article definitions in publish order
ARTICLES = [
    {
        "file": "HUB4_Pillar_blog_article.html",
        "cluster_id": "HUB-4-Pillar",
        "title": "איך לטפל בעור רגיש של תינוק — המדריך המלא",
        "handle": "how-to-care-for-sensitive-baby-skin",
        "tags": "sensitive-skin,HUB-4,pillar,עור רגיש תינוק",
        "seo_title": "איך לטפל בעור רגיש של תינוק — המדריך המלא | BabyMania",
        "meta_description": "מדריך מקיף לטיפול בעור רגיש של תינוק — סימנים, בחירת בד, שגרת טיפול וטעויות נפוצות. כל מה שהורים חדשים צריכים לדעת.",
    },
    {
        "file": "HUB4_C1_blog_article.html",
        "cluster_id": "HUB-4-C1",
        "title": "הבדים הטובים ביותר לעור רגיש של תינוק",
        "handle": "best-fabrics-for-sensitive-baby-skin",
        "tags": "sensitive-skin,HUB-4,C1,בד לעור רגיש תינוק",
        "seo_title": "הבדים הטובים ביותר לעור רגיש של תינוק | BabyMania",
        "meta_description": "השוואה בין סוגי בדים לתינוקות עם עור רגיש — כותנה, במבוק, פוליאסטר ועוד. מדריך מעשי לבחירת הבד הנכון.",
    },
    {
        "file": "HUB4_C2_blog_article.html",
        "cluster_id": "HUB-4-C2",
        "title": "למה כותנה היא הבחירה הנכונה לתינוקות",
        "handle": "why-cotton-is-best-for-babies",
        "tags": "sensitive-skin,HUB-4,C2,כותנה לתינוקות",
        "seo_title": "למה כותנה היא הבחירה הנכונה לתינוקות | BabyMania",
        "meta_description": "כותנה טבעית היא הבד העדיף לתינוקות — נושם, רך ולא מגרה. מדריך ליתרונות כותנה בכל עונה ואיך לבחור בגד איכותי.",
    },
    {
        "file": "HUB4_C3_blog_article.html",
        "cluster_id": "HUB-4-C3",
        "title": "סימני עור רגיש בתינוקות — איך מזהים ומה עושים",
        "handle": "signs-your-baby-has-sensitive-skin",
        "tags": "sensitive-skin,HUB-4,C3,aeo,סימני עור רגיש תינוק",
        "seo_title": "סימני עור רגיש בתינוקות — איך מזהים ומה עושים | BabyMania",
        "meta_description": "5 הסימנים המובילים שעור התינוק רגיש — אדמומיות, יובש, פריחה ועוד. מדריך מהיר לזיהוי ולטיפול ראשוני.",
    },
    {
        "file": "HUB4_C4_blog_article.html",
        "cluster_id": "HUB-4-C4",
        "title": "ביגוד בטוח לעור רגיש של יילוד — מה חשוב לבדוק",
        "handle": "what-clothes-are-safe-for-newborn-skin",
        "tags": "sensitive-skin,HUB-4,C4,ביגוד בטוח יילוד עור רגיש",
        "seo_title": "ביגוד בטוח לעור רגיש של יילוד — מה חשוב לבדוק | BabyMania",
        "meta_description": "6 דברים לבדוק לפני הלבשת תינוק עם עור רגיש — תוויות, כביסה ראשונה, סוג בד וטיפים לפי עונה. צ'קליסט מעשי להורים.",
    },
]


def read_body_html(filepath: Path) -> str:
    """Read HTML file content."""
    return filepath.read_text(encoding="utf-8")


def publish_article(article_def: dict) -> dict:
    """Publish a single article to Shopify blog."""
    check_article_qa(HUB4_DIR, article_def)  # Gate: blocks if QA missing or FAIL
    filepath = HUB4_DIR / article_def["file"]
    body_html = read_body_html(filepath)

    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    payload = {
        "article": {
            "title": article_def["title"],
            "handle": article_def["handle"],
            "body_html": body_html,
            "published": True,
            "tags": article_def["tags"],
            "author": "BabyMania",
            "metafields": [
                {
                    "namespace": "seo",
                    "key": "title",
                    "value": article_def["seo_title"],
                    "type": "single_line_text_field",
                },
                {
                    "namespace": "seo",
                    "key": "description",
                    "value": article_def["meta_description"],
                    "type": "single_line_text_field",
                },
            ],
        }
    }

    resp = requests.post(url, headers=_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()["article"]

    return {
        "cluster_id": article_def["cluster_id"],
        "shopify_article_id": data["id"],
        "handle": data["handle"],
        "published_at": data.get("published_at"),
        "url": f"https://babymania-il.com/blogs/news/{data['handle']}",
    }


def verify_http(url: str) -> int:
    """Verify article is accessible via public URL."""
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return resp.status_code
    except Exception:
        return 0


def main():
    results = []

    # Pre-flight: validate ALL QA files before publishing anything
    preflight_qa_check(HUB4_DIR, ARTICLES, "HUB-4 Sensitive Baby Skin")

    print("=" * 60)
    print("PUBLISHING HUB-4: Sensitive Baby Skin")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Articles: {len(ARTICLES)}")
    print("=" * 60)

    for i, article_def in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{len(ARTICLES)}] Publishing: {article_def['cluster_id']}")
        print(f"  Title: {article_def['title']}")
        print(f"  Handle: {article_def['handle']}")

        try:
            result = publish_article(article_def)
            print(f"  Shopify ID: {result['shopify_article_id']}")
            print(f"  Published at: {result['published_at']}")

            # Brief pause before HTTP verify
            time.sleep(2)

            status_code = verify_http(result["url"])
            result["http_status"] = status_code
            print(f"  HTTP verify: {status_code}")

            results.append(result)

        except requests.exceptions.HTTPError as e:
            print(f"  ERROR: {e}")
            print(f"  Response: {e.response.text[:500] if e.response else 'N/A'}")
            results.append({
                "cluster_id": article_def["cluster_id"],
                "error": str(e),
            })
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                "cluster_id": article_def["cluster_id"],
                "error": str(e),
            })

    # Summary
    print("\n" + "=" * 60)
    print("PUBLISH SUMMARY")
    print("=" * 60)

    success = [r for r in results if "shopify_article_id" in r]
    failed = [r for r in results if "error" in r]

    for r in success:
        http = r.get("http_status", "?")
        print(f"  PASS  {r['cluster_id']} — ID: {r['shopify_article_id']} — HTTP {http}")

    for r in failed:
        print(f"  FAIL  {r['cluster_id']} — {r['error']}")

    print(f"\nPublished: {len(success)}/{len(ARTICLES)}")

    # Save results
    output_path = HUB4_DIR / "HUB4_PUBLISH_RESULTS.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "hub_id": "HUB-4",
            "hub_name": "Sensitive Baby Skin",
            "blog_id": BLOG_ID,
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
            "articles": results,
            "success_count": len(success),
            "fail_count": len(failed),
        }, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {output_path}")
    return len(failed) == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
