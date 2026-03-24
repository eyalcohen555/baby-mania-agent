"""
Publish HUB-6 (Baby Shoes) — 7 articles to Shopify Blog
Blog: news (ID: 109164036409)
Hub: נעלי תינוקות וילדים
Written: 2026-03-19
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
HUB6_DIR = Path("C:/Projects/baby-mania-agent/output/hub6-baby-shoes")

# Article definitions — pillar first, then clusters in order
ARTICLES = [
    {
        "file": "HUB6_Pillar_blog_article.html",
        "cluster_id": "HUB-6-Pillar",
        "title": "נעלי תינוק — המדריך המלא לבחירת נעל שתשמור על הרגל הגדלה",
        "handle": "bchira-naale-tinok-madrih-male",
        "tags": "baby-shoes,HUB-6,pillar,נעלי-תינוק,נעלי-ילדים,נעל-לצעד-ראשון",
        "seo_title": "נעלי תינוק — המדריך המלא לבחירה נכונה | BabyMania",
        "meta_description": "איך לבחור נעלי תינוק? 8 דברים שחייבים לבדוק לפני קנייה — מידה, סוליה, חומרים, סגירה ועוד. המדריך המלא לנעל שתשמור על הרגל הגדלה.",
    },
    {
        "file": "HUB6_C1_blog_article.html",
        "cluster_id": "HUB-6-C1",
        "title": "נעל לצעד ראשון — מה שכל הורה צריך לדעת לפני שקונים",
        "handle": "naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat",
        "tags": "baby-shoes,HUB-6,C1,נעל-לצעד-ראשון,צעד-ראשון,נעלי-תינוק",
        "seo_title": "נעל לצעד ראשון — המדריך להורים | BabyMania",
        "meta_description": "מתי מתחילים לנעול תינוק? מה חייבת לכלול נעל לצעד ראשון? 5 דברים שכל הורה צריך לדעת לפני שקונים את הנעל הראשונה.",
    },
    {
        "file": "HUB6_C2_blog_article.html",
        "cluster_id": "HUB-6-C2",
        "title": "סוליה גמישה בנעלי ילדים — למה זה משנה הרבה יותר ממה שחשבתם",
        "handle": "solya-gmisha-naale-yeladim-mah-hahevdel",
        "tags": "baby-shoes,HUB-6,C2,סוליה-גמישה,נעלי-ילדים,נעלי-תינוק",
        "seo_title": "סוליה גמישה בנעלי ילדים — למה זה חשוב | BabyMania",
        "meta_description": "מה ההבדל בין סוליה גמישה לסוליה קשיחה בנעלי ילדים? למה זה קריטי לפיתוח הרגל? כל מה שצריך לדעת על סוליה לנעל תינוק.",
    },
    {
        "file": "HUB6_C3_blog_article.html",
        "cluster_id": "HUB-6-C3",
        "title": "מדידת נעלי ילדים — כך תמדדו נכון בבית (ותחסכו כאב ראש)",
        "handle": "mida-nachon-naale-yeladim-kacha-memdim-babayit",
        "tags": "baby-shoes,HUB-6,C3,מידת-נעל,מדידת-נעל,נעלי-ילדים",
        "seo_title": "איך למדוד נעלי ילדים בבית — מדריך מהיר | BabyMania",
        "meta_description": "כיצד למדוד נכון את כף הרגל של הילד לפני קנייה? טבלת מידות, שיטת המדידה הנכונה, וכמה פעמים צריך למדוד מחדש בשנה.",
    },
    {
        "file": "HUB6_C4_blog_article.html",
        "cluster_id": "HUB-6-C4",
        "title": "נעלי גן לילדים — מה שכדאי לדעת לפני שהסמסטר מתחיל",
        "handle": "naale-gan-yeladim-mah-kday-ladaat",
        "tags": "baby-shoes,HUB-6,C4,נעלי-גן,נעלי-ילדים,סגירה-ללא-שרוכים",
        "seo_title": "נעלי גן לילדים — המדריך לבחירה נכונה | BabyMania",
        "meta_description": "איזה נעלי גן לילדים לבחור? מה חשוב — סגירה, סוליה, או גודל? מדריך קצר לנעל שתשרוד את כל שנת הגן ותעזור לילד להיות עצמאי.",
    },
    {
        "file": "HUB6_C5_blog_article.html",
        "cluster_id": "HUB-6-C5",
        "title": "מתי מחליפים נעלי ילד — הסימנים שהורים פעמים רבות מפספסים",
        "handle": "matay-lechahlif-naale-yeled-hassimanim",
        "tags": "baby-shoes,HUB-6,C5,החלפת-נעליים,גדילת-ילדים,נעלי-ילדים",
        "seo_title": "מתי להחליף נעלי ילד — הסימנים | BabyMania",
        "meta_description": "מתי צריך להחליף נעלי ילד? 5 סימנים שאומרים שהגיע הזמן — גם אם הנעל נראית שלמה. כמה פעם בשנה צריך להחליף בכל גיל.",
    },
    {
        "file": "HUB6_C6_blog_article.html",
        "cluster_id": "HUB-6-C6",
        "title": "חומרים נושמים בנעלי תינוקות — מה זה אומר ולמה זה שווה לבדוק",
        "handle": "chomrim-noshmim-naale-tinoket-mah-levakesh",
        "tags": "baby-shoes,HUB-6,C6,חומרים-נושמים,נעלי-תינוק,נוחות",
        "seo_title": "חומרים נושמים בנעלי תינוקות — מה לחפש | BabyMania",
        "meta_description": "מה הם חומרים נושמים בנעלי תינוקות ולמה הם חשובים? רשת אוויר, בד טבעי, ריפוד מאווורר — כך בוחרים נעל שלא גורמת לבעיות.",
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
    check_article_qa(HUB6_DIR, article_def)

    filepath = HUB6_DIR / article_def["file"]

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
    print("BabyMania — HUB-6 Baby Shoes Publisher")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Articles: {len(ARTICLES)}")
    print(f"NOTE: GSC indexing — DO NOT submit until user confirms Pillar in incognito")
    print(f"{'='*60}\n")

    # Pre-flight: validate ALL QA files before publishing anything
    preflight_qa_check(HUB6_DIR, ARTICLES, "HUB-6 Baby Shoes")

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
        "hub_id": "HUB-6",
        "hub_name": "Baby Shoes",
        "published_at": datetime.now().isoformat(),
        "blog_id": BLOG_ID,
        "total": len(ARTICLES),
        "published": published,
        "errors": errors,
        "gsc_indexing": "PENDING — do not submit until pillar reviewed in incognito",
        "articles": results,
    }

    results_file = HUB6_DIR / "HUB6_PUBLISH_RESULTS.json"
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

    print("\n⚠️  GSC: לא לאנדקס עד לאישור המשתמש אחרי בדיקת פילר בגלישה בסתר.\n")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
