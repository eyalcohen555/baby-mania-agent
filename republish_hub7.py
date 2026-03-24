"""
Republish HUB-7 (Baby Safety) — UPDATE existing 6 articles on Shopify
- C5: full rewrite (new content)
- C1, C2, C3, C4: image + product updates only
- Pillar: image updates only
Uses article IDs from HUB7_PUBLISH_RESULTS.json
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

import requests
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409
HUB7_DIR = Path("C:/Projects/baby-mania-agent/output/hub7")

# Load existing article IDs from publish results
PUBLISH_RESULTS = json.loads(
    (HUB7_DIR / "HUB7_PUBLISH_RESULTS.json").read_text(encoding="utf-8")
)
ARTICLE_IDS = {a["cluster_id"]: a["article_id"] for a in PUBLISH_RESULTS["articles"]}

# Map cluster_id to local HTML file
FILE_MAP = {
    "HUB-7-Pillar": "HUB7_Pillar_blog_article.html",
    "HUB-7-C1": "HUB7_C1_blog_article.html",
    "HUB-7-C2": "HUB7_C2_blog_article.html",
    "HUB-7-C3": "HUB7_C3_blog_article.html",
    "HUB-7-C4": "HUB7_C4_blog_article.html",
    "HUB-7-C5": "HUB7_C5_blog_article.html",
}


def read_body_html(filepath: Path) -> str:
    """Read HTML file and strip leading BLOG_META comment block if present."""
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("<!--"):
        end = content.find("-->")
        if end != -1:
            content = content[end + 3:].lstrip()
    return content


def update_article(cluster_id: str) -> dict:
    """Update an existing article's body_html on Shopify."""
    article_id = ARTICLE_IDS.get(cluster_id)
    if not article_id:
        return {"cluster_id": cluster_id, "status": "ERROR", "error": "No article_id found"}

    filepath = HUB7_DIR / FILE_MAP[cluster_id]
    if not filepath.exists():
        return {"cluster_id": cluster_id, "status": "ERROR", "error": f"File not found: {filepath}"}

    body_html = read_body_html(filepath)

    payload = {
        "article": {
            "id": article_id,
            "body_html": body_html,
        }
    }

    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    response = requests.put(url, json=payload, headers=_headers())

    if response.status_code == 200:
        data = response.json()["article"]
        return {
            "cluster_id": cluster_id,
            "status": "UPDATED",
            "article_id": data["id"],
            "handle": data["handle"],
            "url": f"https://babymania-il.com/blogs/news/{data['handle']}",
            "updated_at": data.get("updated_at", ""),
        }
    else:
        return {
            "cluster_id": cluster_id,
            "status": "ERROR",
            "http_status": response.status_code,
            "error": response.text[:500],
        }


def main():
    print(f"\n{'='*60}")
    print("BabyMania — HUB-7 REPUBLISH (update existing articles)")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Articles to update: {len(FILE_MAP)}")
    print(f"{'='*60}\n")

    # Show article IDs
    for cid, aid in ARTICLE_IDS.items():
        print(f"  {cid}: article_id={aid}")
    print()

    results = []
    updated = 0
    errors = 0

    for cluster_id in FILE_MAP:
        print(f"Updating: {cluster_id} (id={ARTICLE_IDS.get(cluster_id, '?')})...")

        result = update_article(cluster_id)
        results.append(result)

        if result["status"] == "UPDATED":
            updated += 1
            print(f"  [OK] UPDATED -> {result['url']}")
        else:
            errors += 1
            print(f"  [ERR] {result.get('error', 'Unknown')[:100]}")

        time.sleep(0.5)

    # Save results
    results_data = {
        "hub_id": "HUB-7",
        "action": "REPUBLISH",
        "republished_at": datetime.now().isoformat(),
        "blog_id": BLOG_ID,
        "total": len(FILE_MAP),
        "updated": updated,
        "errors": errors,
        "changes": [
            "C5: full rewrite — new angle, new content, new product (Baby Bear Cozy Set)",
            "C1: images → Tempio/Alure/LumiBear, product → Tempio",
            "C2: images → WarmNest/WinterSuit/BearCozy, product → WarmNest",
            "C3: images → LUMI/Gemini/GirlsOnesie, product → LUMI",
            "C4: images → Lino/LumiBear/Veloura (product unchanged)",
            "Pillar: unchanged",
        ],
        "articles": results,
    }

    results_file = HUB7_DIR / "HUB7_REPUBLISH_RESULTS.json"
    results_file.write_text(
        json.dumps(results_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{'='*60}")
    print(f"DONE — {updated}/{len(FILE_MAP)} updated, {errors} errors")
    print(f"Results saved: {results_file}")
    print(f"{'='*60}\n")

    if updated > 0:
        print("Updated URLs:")
        for r in results:
            if r["status"] == "UPDATED":
                print(f"  [{r['cluster_id']}] {r['url']}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
