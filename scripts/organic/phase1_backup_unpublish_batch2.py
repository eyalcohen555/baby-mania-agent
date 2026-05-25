"""
Phase 1 — INCIDENT FIX: Backup + Unpublish Batch 2 damaged articles.

Actions:
  1. GET each article by ID → save full JSON backup
  2. PUT published=false for each article
  3. GET verify each article is unpublished

SAFETY: This script ONLY unpublishes Batch 2 articles. No creates. No deletes.
"""

import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409

BATCH2_ARTICLES = [
    {"id": 689005199673,  "hub": "HUB-7/C6"},
    {"id": 689005232441,  "hub": "HUB-8/C6"},
    {"id": 689005265209,  "hub": "HUB-16/Pillar"},
    {"id": 689005297977,  "hub": "HUB-16/C1"},
    {"id": 689005330745,  "hub": "HUB-16/C2"},
    {"id": 689005363513,  "hub": "HUB-16/C3"},
]

BACKUP_DIR = Path(r"C:\Projects\baby-mania-agent\output\organic\backups")


def get_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()["article"]


def unpublish_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "published": False}}
    r = requests.put(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()["article"]


def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"batch2-live-damaged-before-fix-{ts}.json"

    print(f"=== PHASE 1 — BACKUP + UNPUBLISH BATCH 2 ===")
    print(f"Articles: {len(BATCH2_ARTICLES)}")
    print(f"Backup: {backup_path}\n")

    # Step 1: Backup
    print("--- STEP 1: BACKUP ---")
    backups = []
    for item in BATCH2_ARTICLES:
        aid = item["id"]
        hub = item["hub"]
        try:
            article = get_article(aid)
            backups.append(article)
            print(f"  [BACKUP] {hub} — ID:{aid} — title: {article['title'][:50]}")
            print(f"           published: {article['published_at']}, handle: {article['handle']}")
        except Exception as e:
            print(f"  [ERROR] {hub} — ID:{aid} — {e}")
            raise

    backup_path.write_text(json.dumps(backups, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Saved {len(backups)} articles -> {backup_path}\n")

    # Step 2: Unpublish
    print("--- STEP 2: UNPUBLISH ---")
    unpublish_results = []
    for i, item in enumerate(BATCH2_ARTICLES, 1):
        aid = item["id"]
        hub = item["hub"]
        try:
            result = unpublish_article(aid)
            pub_at = result.get("published_at")
            status = "UNPUBLISHED" if pub_at is None else f"STILL-PUBLISHED({pub_at})"
            print(f"  [{i}/6] {hub} — ID:{aid} — {status}")
            unpublish_results.append({"hub": hub, "id": aid, "published_at": pub_at, "ok": pub_at is None})
        except Exception as e:
            print(f"  [ERROR] {hub} — ID:{aid} — {e}")
            raise
        if i < len(BATCH2_ARTICLES):
            time.sleep(1)

    print()

    # Step 3: Verify
    print("--- STEP 3: VERIFY ---")
    all_clear = True
    for item in BATCH2_ARTICLES:
        aid = item["id"]
        hub = item["hub"]
        try:
            article = get_article(aid)
            pub_at = article.get("published_at")
            if pub_at is None:
                print(f"  [OK] {hub} - ID:{aid} - confirmed unpublished")
            else:
                print(f"  [FAIL] {hub} — ID:{aid} — still published: {pub_at}")
                all_clear = False
        except Exception as e:
            print(f"  [ERROR] {hub} — ID:{aid} — {e}")
            all_clear = False

    print()
    if all_clear:
        print("=== PHASE 1 COMPLETE — all 6 articles unpublished ===")
        print(f"Backup saved: {backup_path}")
        print("NEXT: Phase 2 — fix md_to_html pipeline")
    else:
        print("=== PHASE 1 FAILED — some articles still published ===")
        print("DO NOT proceed to Phase 2 until all 6 are unpublished.")
        sys.exit(1)


if __name__ == "__main__":
    main()
