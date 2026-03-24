"""
migrate_to_accessories_fast.py
מעביר מוצרים לא-נעליים מ-template=shoes ל-template=accessories
מקביליות: 5 threads, progress כל 10 מוצרים
"""
import json
import os
import sys
import io
import time
from pathlib import Path
import requests
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── הגדרות ──────────────────────────────────────────────────────────────
REPORT_PATH  = Path("output/shoe_classification_report.json")
TOKEN_FILE   = Path(r"C:\Users\3024e\Desktop\shopify-token\.env")
SHOP         = "a2756c-c0.myshopify.com"
API_VERSION  = "2024-10"
BASE_URL     = f"https://{SHOP}/admin/api/{API_VERSION}/products"
PROGRESS_EVERY = 10

# classifications שצריך להעביר (נעליים אמיתיות — לא נוגעים)
MIGRATE_CLASSES = {
    "⚠️ ביגוד — template=shoes בטעות",
    "⚠️ אביזר/ציוד — template=shoes בטעות",
    "❓ לא ניתן לסווג",
}

# ── טעינת טוקן ──────────────────────────────────────────────────────────
load_dotenv(TOKEN_FILE)
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
if not TOKEN:
    print("❌ לא נמצא SHOPIFY_ACCESS_TOKEN בקובץ", TOKEN_FILE)
    sys.exit(1)

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

# ── פונקציות ────────────────────────────────────────────────────────────

def _request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """שולח בקשה עם retry על 429 — עד 3 ניסיונות, backoff 2 שניות"""
    for attempt in range(3):
        r = requests.request(method, url, headers=HEADERS, timeout=15, **kwargs)
        if r.status_code == 429:
            time.sleep(2)
            continue
        return r
    return r


def get_template(product_id: int) -> str | None:
    """מחזיר את template_suffix הנוכחי מה-API"""
    url = f"{BASE_URL}/{product_id}.json?fields=id,template_suffix"
    r = _request_with_retry("GET", url)
    if r.status_code == 200:
        return r.json()["product"].get("template_suffix") or ""
    return None


def set_template(product_id: int, suffix: str) -> bool:
    """מעדכן template_suffix למוצר"""
    url = f"{BASE_URL}/{product_id}.json"
    payload = {"product": {"id": product_id, "template_suffix": suffix}}
    r = _request_with_retry("PUT", url, json=payload)
    return r.status_code == 200


def process_product(item: dict) -> dict:
    """בודק ומעדכן מוצר אחד. מחזיר dict עם תוצאה."""
    pid   = item["id"]
    title = item["title"][:60]

    current = get_template(pid)
    if current is None:
        return {"id": pid, "status": "error", "detail": "failed to fetch", "title": title}

    if current == "accessories":
        return {"id": pid, "status": "already_accessories", "title": title}

    if current != "shoes":
        # לא shoes ולא accessories — לא נוגעים
        return {"id": pid, "status": "skipped", "detail": f"template={current!r}", "title": title}

    # current == "shoes" → עדכן
    ok = set_template(pid, "accessories")
    if ok:
        return {"id": pid, "status": "migrated", "title": title}
    else:
        return {"id": pid, "status": "error", "detail": "update failed", "title": title}


# ── ראשי ────────────────────────────────────────────────────────────────

def main():
    with open(REPORT_PATH, encoding="utf-8") as f:
        report = json.load(f)

    targets = [item for item in report if item["classification"] in MIGRATE_CLASSES]
    print(f"📋 נמצאו {len(targets)} מוצרים לבדיקה (ביגוד + אביזר + לא ניתן לסווג)")
    print(f"🐢 מריץ סדרתי, sleep 1s בין בקשות...\n")

    results   = []
    start     = time.time()

    for i, item in enumerate(targets, 1):
        res = process_product(item)
        results.append(res)
        time.sleep(1)

        if i % PROGRESS_EVERY == 0 or i == len(targets):
            elapsed = time.time() - start
            pct     = i / len(targets) * 100
            print(f"  [{i}/{len(targets)}] {pct:.0f}% — {elapsed:.1f}s elapsed")

    # ── סיכום ───────────────────────────────────────────────────────────
    migrated   = [r for r in results if r["status"] == "migrated"]
    already    = [r for r in results if r["status"] == "already_accessories"]
    errors     = [r for r in results if r["status"] == "error"]
    skipped    = [r for r in results if r["status"] == "skipped"]

    print("\n" + "═" * 55)
    print("✅ הועברו ל-accessories:   ", len(migrated))
    print("⏭️  כבר היו accessories:   ", len(already))
    print("⏩ דולגו (template אחר):  ", len(skipped))
    print("❌ נכשלו:                  ", len(errors))

    # בדיקת sanity — מוצרים שנשארו על shoes (לא אמורים להיות)
    still_shoes = [r for r in results if r.get("detail", "").startswith("template='shoes'")]
    print("🔴 נשארו על shoes:          ", len(still_shoes))
    print("═" * 55)
    print(f"⏱️  זמן כולל: {time.time() - start:.1f} שניות")

    if errors:
        print("\n❌ פרטי שגיאות:")
        for e in errors:
            print(f"   id={e['id']} | {e.get('detail','')} | {e['title']}")

    if skipped:
        print("\n⏩ פרטי דילוגים (template לא shoes ולא accessories):")
        for s in skipped:
            print(f"   id={s['id']} | {s.get('detail','')} | {s['title']}")


if __name__ == "__main__":
    main()
