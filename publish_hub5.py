"""
Publish HUB-5 (Baby Gifts) — 7 articles to Shopify Blog
Blog: news (ID: 109164036409)
Hub: מתנות לתינוק
Written: 2026-03-15
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import requests
from shopify_client import _headers, BASE_URL
from qa_gate import preflight_qa_check, check_article_qa

BLOG_ID = 109164036409
HUB5_DIR = Path("C:/Projects/baby-mania-agent/output/hub5-baby-gifts")

# Article definitions — pillar first, then clusters in order
ARTICLES = [
    {
        "file": "HUB5_Pillar_blog_article.html",
        "cluster_id": "HUB-5-Pillar",
        "title": "מתנות לתינוק — המדריך המלא (בייבי שאוור, ברית, ביקור יולדת)",
        "handle": "matanot-letinok-madrih-male",
        "tags": "baby-gifts,HUB-5,pillar,מתנות-לתינוק,מתנה-ליולדת,בייבי-שאוור",
        "seo_title": "מתנות לתינוק — המדריך המלא לקנייה חכמה | BabyMania",
        "meta_description": "מדריך מלא למתנות לתינוק — בייבי שאוור, ברית, ביקור יולדת, ילד שני. מה לקנות, כמה להוציא, ואיך לבחור מתנה שתיזכרו עליה.",
    },
    {
        "file": "HUB5_C1_blog_article.html",
        "cluster_id": "HUB-5-C1",
        "title": "מה לקנות לבייבי שאוור כשהרשימה כבר נגמרה",
        "handle": "matanot-baby-shower-reshima-nigmeret",
        "tags": "baby-gifts,HUB-5,C1,בייבי-שאוור,מתנה-לבייבי-שאוור,מתנות-מקוריות",
        "seo_title": "מתנה לבייבי שאוור — רשימה שלא נגמרת | BabyMania",
        "meta_description": "הגעת לבייבי שאוור אחרי שכולם כבר קנו מהרשימה? הנה 10 מתנות מקוריות ושימושיות שתמיד עובדות — גם בלי רשימה.",
    },
    {
        "file": "HUB5_C2_blog_article.html",
        "cluster_id": "HUB-5-C2",
        "title": "מתנות מעשיות לתינוק שהורים חדשים באמת ישמחו עליהן",
        "handle": "matanot-maasiot-tinok-horeh-chadash",
        "tags": "baby-gifts,HUB-5,C2,מתנות-מעשיות,מתנה-לתינוק,הורים-חדשים",
        "seo_title": "מתנות מעשיות לתינוק שהורים באמת ישמחו | BabyMania",
        "meta_description": "לא רוצה לקנות עוד דבר שיישב בארון? הנה מתנות מעשיות לתינוק שהורים חדשים באמת צריכים ומשתמשים בהן כל יום.",
    },
    {
        "file": "HUB5_C3_blog_article.html",
        "cluster_id": "HUB-5-C3",
        "title": "מתנות יוקרה לתינוק — מה שישאר בזיכרון",
        "handle": "matanot-yokra-tinok-zechronot",
        "tags": "baby-gifts,HUB-5,C3,מתנות-יוקרה,מתנה-מפנקת,מתנה-מיוחדת-לתינוק",
        "seo_title": "מתנות יוקרה לתינוק שיישארו בזיכרון | BabyMania",
        "meta_description": "רוצה לתת מתנה שיזכרו עליך? הנה מתנות יוקרה לתינוק שמרגישות מיוחדות, נראות יפה ומשאירות רושם — בלי להסתבך.",
    },
    {
        "file": "HUB5_C4_blog_article.html",
        "cluster_id": "HUB-5-C4",
        "title": "מה אמא חדשה באמת צריכה אחרי הלידה",
        "handle": "ma-ima-chadasha-tzricha-achrei-lida",
        "tags": "baby-gifts,HUB-5,C4,אמא-חדשה,מתנה-ליולדת,אחרי-לידה,AEO",
        "seo_title": "מה אמא חדשה באמת צריכה אחרי לידה | BabyMania",
        "meta_description": "לא יודע מה לקנות לאמא החדשה? מדריך קצר על מה שאמא באמת צריכה אחרי לידה — לא מה שכולם קונים, אלא מה שעוזר.",
    },
    {
        "file": "HUB5_C5_blog_article.html",
        "cluster_id": "HUB-5-C5",
        "title": "מתנות לתינוק ראשון — המדריך לאנשים שלא מכירים תינוקות",
        "handle": "matanot-tinok-rishon-madrih",
        "tags": "baby-gifts,HUB-5,C5,תינוק-ראשון,מתנה-לתינוק-ראשון,מדריך-מתנות",
        "seo_title": "מתנות לתינוק ראשון — המדריך הפשוט | BabyMania",
        "meta_description": "לא מכיר תינוקות ולא יודע מה לקנות? המדריך הפשוט למתנות לתינוק ראשון — מה עובד, מה להימנע, ואיך לא להסתבך.",
    },
    {
        "file": "HUB5_C6_blog_article.html",
        "cluster_id": "HUB-5-C6",
        "title": "סט מתנה לתינוק — למה זה תמיד הפתרון הנכון",
        "handle": "set-matana-tinok-pitaron-nachon",
        "tags": "baby-gifts,HUB-5,C6,סט-מתנה,חבילת-מתנה,סט-ביגוד-לתינוק,מארז-מתנה",
        "seo_title": "סט מתנה לתינוק — למה זה הפתרון הנכון | BabyMania",
        "meta_description": "לא יודע מה לקנות? סט מתנה לתינוק תמיד עובד — מסביר מה לחפש, למה סט עדיף, ואילו סטים שווים את הכסף.",
    },
]


def read_body_html(filepath: Path) -> str:
    """Read HTML file and strip BLOG_META comment block."""
    content = filepath.read_text(encoding="utf-8")
    # Remove the leading comment block if present
    if content.startswith("<!--"):
        end = content.find("-->")
        if end != -1:
            content = content[end + 3:].lstrip()
    return content


def publish_article(article_def: dict) -> dict:
    """Publish a single article to Shopify blog."""
    # Gate: check QA immediately before each Shopify call
    check_article_qa(HUB5_DIR, article_def)

    filepath = HUB5_DIR / article_def["file"]

    if not filepath.exists():
        return {
            "cluster_id": article_def["cluster_id"],
            "status": "ERROR",
            "error": f"File not found: {filepath}",
        }

    body_html = read_body_html(filepath)

    payload = {
        "article": {
            "title": article_def["title"],
            "body_html": body_html,
            "handle": article_def["handle"],
            "tags": article_def["tags"],
            "published": True,
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

    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    response = requests.post(url, json=payload, headers=_headers())

    if response.status_code in (200, 201):
        data = response.json()["article"]
        return {
            "cluster_id": article_def["cluster_id"],
            "status": "PUBLISHED",
            "article_id": data["id"],
            "handle": data["handle"],
            "url": f"https://babymania-il.com/blogs/news/{data['handle']}",
            "published_at": data.get("published_at", ""),
        }
    else:
        return {
            "cluster_id": article_def["cluster_id"],
            "status": "ERROR",
            "http_status": response.status_code,
            "error": response.text[:500],
        }


def main():
    print(f"\n{'='*60}")
    print("BabyMania — HUB-5 Baby Gifts Publisher")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Articles: {len(ARTICLES)}")
    print(f"{'='*60}\n")

    # Pre-flight: validate ALL QA files before publishing anything
    preflight_qa_check(HUB5_DIR, ARTICLES, "HUB-5 Baby Gifts")

    results = []
    published = 0
    errors = 0

    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/{len(ARTICLES)}] Publishing: {article['cluster_id']} — {article['title'][:50]}...")

        result = publish_article(article)
        results.append(result)

        if result["status"] == "PUBLISHED":
            published += 1
            print(f"  [OK] PUBLISHED -> {result['url']}")
        else:
            errors += 1
            print(f"  [ERR] ERROR: {result.get('error', 'Unknown error')[:100]}")

        # Rate limit: 2 requests/sec
        if i < len(ARTICLES):
            time.sleep(0.6)

    # Save results
    results_data = {
        "hub_id": "HUB-5",
        "hub_name": "Baby Gifts",
        "published_at": datetime.now().isoformat(),
        "blog_id": BLOG_ID,
        "total": len(ARTICLES),
        "published": published,
        "errors": errors,
        "articles": results,
    }

    results_file = HUB5_DIR / "HUB5_PUBLISH_RESULTS.json"
    results_file.write_text(
        json.dumps(results_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{'='*60}")
    print(f"DONE -- {published}/{len(ARTICLES)} published, {errors} errors")
    print(f"Results saved: {results_file}")
    print(f"{'='*60}\n")

    if published > 0:
        print("Published URLs:")
        for r in results:
            if r["status"] == "PUBLISHED":
                print(f"  • [{r['cluster_id']}] {r['url']}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
