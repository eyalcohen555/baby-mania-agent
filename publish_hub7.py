"""
Publish HUB-7 (Baby Safety) — 6 articles to Shopify Blog
Blog: news (ID: 109164036409)
Hub: בטיחות תינוק
Written: 2026-03-23
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
from qa_gate import check_product_links

BLOG_ID = 109164036409
HUB7_DIR = Path("C:/Projects/baby-mania-agent/output/hub7")

# Article definitions — pillar first, then clusters in writing order
ARTICLES = [
    {
        "file": "HUB7_Pillar_blog_article.html",
        "cluster_id": "HUB-7-Pillar",
        "title": "איך ליצור סביבה בטוחה לתינוק — המדריך המלא",
        "handle": "sviva-betua-letinok-madrih-male",
        "tags": "baby-safety,HUB-7,pillar,בטיחות-תינוק,שינה-בטוחה,סביבה-בטוחה-לתינוק",
        "seo_title": "בטיחות תינוק — המדריך המלא ליצירת סביבה בטוחה | BabyMania",
        "meta_description": "איך ליצור סביבה בטוחה לתינוק? כל מה שצריך לדעת על שינה בטוחה, מניעת התחממות, ביגוד בטוח ובטיחות לילה — מדריך מלא להורים. | BabyMania",
    },
    {
        "file": "HUB7_C1_blog_article.html",
        "cluster_id": "HUB-7-C1",
        "title": "כללי שינה בטוחה לתינוק — מה שכל הורה חייב לדעת",
        "handle": "klalei-shina-betua-letinok",
        "tags": "baby-safety,HUB-7,C1,שינה-בטוחה,כללי-שינה-בטוחה,בטיחות-שינה-תינוק",
        "seo_title": "כללי שינה בטוחה לתינוק — המדריך להורים | BabyMania",
        "meta_description": "מה כללי שינה בטוחה לתינוק? כל הכללים הברורים — מה שמים במיטה, כמה שמיכות, טמפרטורת חדר. לא תיאוריה — הנחיות מעשיות. | BabyMania",
    },
    {
        "file": "HUB7_C2_blog_article.html",
        "cluster_id": "HUB-7-C2",
        "title": "טעויות נפוצות בשינה בטוחה לתינוק — ומה לעשות אחרת",
        "handle": "tauyot-shina-betua-tinok",
        "tags": "baby-safety,HUB-7,C2,טעויות-שינה,שינה-בטוחה,AEO",
        "seo_title": "טעויות נפוצות בשינה בטוחה לתינוק — ואיך לתקן | BabyMania",
        "meta_description": "יש טעויות בשינה בטוחה שהורים עושים בלי לדעת. הנה הנפוצות ביותר — ואיך לתקן אותן בקלות. | BabyMania",
    },
    {
        "file": "HUB7_C3_blog_article.html",
        "cluster_id": "HUB-7-C3",
        "title": "איך למנוע התחממות יתר בתינוק — הסימנים שחשוב להכיר",
        "handle": "minuat-hitchamamut-yeter-betinok",
        "tags": "baby-safety,HUB-7,C3,התחממות-יתר,תינוק-חם,שכבות-בגדים-תינוק",
        "seo_title": "התחממות יתר בתינוק — סימנים ואיך למנוע | BabyMania",
        "meta_description": "איך יודעים שתינוק חם מדי? הסימנים שצריך להכיר, כמה שכבות בגדים לתינוק, וטמפרטורת חדר מומלצת — כל מה שצריך. | BabyMania",
    },
    {
        "file": "HUB7_C4_blog_article.html",
        "cluster_id": "HUB-7-C4",
        "title": "ביגוד בטוח לתינוק — מה לחפש ומה להימנע ממנו",
        "handle": "bigud-batua-letinok-mah-levakesh",
        "tags": "baby-safety,HUB-7,C4,ביגוד-בטוח-לתינוק,בגדי-תינוק-בטוחים,חומרים-בטוחים",
        "seo_title": "ביגוד בטוח לתינוק — מה לחפש ומה להימנע ממנו | BabyMania",
        "meta_description": "איזה ביגוד בטוח לתינוק? חומרים מומלצים, מה אסור בביגוד תינוק, ואיך בוחרים נכון — מדריך ברור להורים. | BabyMania",
    },
    {
        "file": "HUB7_C5_blog_article.html",
        "cluster_id": "HUB-7-C5",
        "title": "בטיחות לילה לתינוק — מה בודקים לפני שהולכים לישון",
        "handle": "betihut-layla-letinok-bdikot-lifney-shina",
        "tags": "baby-safety,HUB-7,C5,בטיחות-לילה,בדיקות-בטיחות-תינוק,שגרת-לילה-בטוחה",
        "seo_title": "בטיחות לילה לתינוק — מה בודקים לפני השינה | BabyMania",
        "meta_description": "מה בודקים לפני שתינוק הולך לישון? רשימת בדיקות בטיחות לילה ברורה — טמפרטורה, מיטה, ביגוד, ניטור. | BabyMania",
    },
]


def _qa_filepath(article_file: str) -> Path:
    """Derive Agent 10.5 content_review QA file path from article filename."""
    qa_filename = article_file.replace("_blog_article.html", "_content_review.json")
    return HUB7_DIR / qa_filename


def preflight_qa_check() -> None:
    """Validate all 6 QA files pass before publishing anything."""
    print(f"\n{'─'*60}")
    print(f"QA PRE-FLIGHT — HUB-7 Baby Safety ({len(ARTICLES)} articles)")
    print(f"{'─'*60}")

    passed = []
    failed = []
    missing = []

    for article in ARTICLES:
        cluster_id = article["cluster_id"]
        qa_path = _qa_filepath(article["file"])

        if not qa_path.exists():
            missing.append((cluster_id, str(qa_path)))
            print(f"  [MISS] {cluster_id} — QA file not found")
            continue

        try:
            qa_data = json.loads(qa_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            missing.append((cluster_id, f"unreadable: {e}"))
            print(f"  [MISS] {cluster_id} — QA file unreadable: {e}")
            continue

        result = qa_data.get("overall_review", "UNKNOWN")
        if result == "PASS":
            passed.append(cluster_id)
            print(f"  [PASS] {cluster_id}")
        else:
            action = qa_data.get("action_required", True)
            failed.append((cluster_id, result))
            print(f"  [FAIL] {cluster_id} — {result} | action_required={action}")

    total_blocked = len(failed) + len(missing)
    print(f"{'─'*60}")
    print(f"Pre-flight: {len(passed)} PASS  |  {len(failed)} FAIL  |  {len(missing)} MISSING")

    if total_blocked > 0:
        print(f"\n[BLOCKED] {total_blocked} article(s) did not pass QA. Nothing published.")
        print(f"{'─'*60}\n")
        sys.exit(1)

    print(f"All {len(passed)} articles passed QA. Proceeding to publish.")
    print(f"{'─'*60}\n")


def read_body_html(filepath: Path) -> str:
    """Read HTML file and strip leading BLOG_META comment block if present."""
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("<!--"):
        end = content.find("-->")
        if end != -1:
            content = content[end + 3:].lstrip()
    return content


def publish_article(article: dict) -> dict:
    """Publish a single article to Shopify blog."""
    # Per-article QA check immediately before the API call
    qa_path = _qa_filepath(article["file"])
    if not qa_path.exists():
        return {"cluster_id": article["cluster_id"], "status": "ERROR", "error": "QA file missing"}
    qa_data = json.loads(qa_path.read_text(encoding="utf-8"))
    if qa_data.get("overall_review") != "PASS":
        return {"cluster_id": article["cluster_id"], "status": "ERROR", "error": "QA not PASS"}

    filepath = HUB7_DIR / article["file"]
    if not filepath.exists():
        return {"cluster_id": article["cluster_id"], "status": "ERROR", "error": f"File not found: {filepath}"}

    body_html = read_body_html(filepath)
    check_product_links(body_html, article["cluster_id"])

    payload = {
        "article": {
            "title": article["title"],
            "body_html": body_html,
            "handle": article["handle"],
            "tags": article["tags"],
            "published": True,
            "metafields": [
                {
                    "namespace": "seo",
                    "key": "title",
                    "value": article["seo_title"],
                    "type": "single_line_text_field",
                },
                {
                    "namespace": "seo",
                    "key": "description",
                    "value": article["meta_description"],
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
            "cluster_id": article["cluster_id"],
            "status": "PUBLISHED",
            "article_id": data["id"],
            "handle": data["handle"],
            "url": f"https://babymania-il.com/blogs/news/{data['handle']}",
            "published_at": data.get("published_at", ""),
        }
    else:
        return {
            "cluster_id": article["cluster_id"],
            "status": "ERROR",
            "http_status": response.status_code,
            "error": response.text[:500],
        }


def main():
    print(f"\n{'='*60}")
    print("BabyMania — HUB-7 Baby Safety Publisher")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Articles: {len(ARTICLES)}")
    print(f"{'='*60}")

    preflight_qa_check()

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
            print(f"  [ERR] ERROR: {result.get('error', 'Unknown')[:100]}")

        if i < len(ARTICLES):
            time.sleep(0.6)

    # Save results
    results_data = {
        "hub_id": "HUB-7",
        "hub_name": "Baby Safety",
        "published_at": datetime.now().isoformat(),
        "blog_id": BLOG_ID,
        "total": len(ARTICLES),
        "published": published,
        "errors": errors,
        "articles": results,
    }

    results_file = HUB7_DIR / "HUB7_PUBLISH_RESULTS.json"
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
