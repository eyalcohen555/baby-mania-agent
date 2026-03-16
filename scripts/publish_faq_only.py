#!/usr/bin/env python3
"""
publish_faq_only.py
-------------------
Writes baby_mania.faq metafield for the 8 clothing-test products.
Does NOT touch templates, hero, fabric, or any other section.
Each product gets exactly the same 6 fixed Q&A items — no dynamic logic.
"""
import io, os, sys, json, requests, time
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")
tok_path = Path.home() / "Desktop/shopify-token/.env"
if tok_path.exists():
    load_dotenv(tok_path, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
API   = "2024-10"
HDR   = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# Fixed FAQ — identical for ALL clothing-test products. No dynamic logic.
FIXED_FAQ = [
    {
        "question": "האם הבגד נעים לעור התינוק?",
        "answer": "הבגד עשוי מבד רך ונעים למגע שנבחר כדי להיות נוח לעור התינוק. העיצוב מאפשר תנועה חופשית ונוחות במהלך היום.",
    },
    {
        "question": "איך אדע איזו מידה לבחור?",
        "answer": "ניתן לבחור מידה לפי גיל התינוק. בדף המוצר מופיעה טבלת מידות שתעזור לבחור את המידה המתאימה. אם מתלבטים בין שתי מידות מומלץ לבחור את הגדולה יותר.",
    },
    {
        "question": "כמה זמן לוקח המשלוח?",
        "answer": "זמן המשלוח הוא 6–11 ימי עסקים. ניתן לבחור בין משלוח עד הבית לבין משלוח חינם לנקודת חלוקה. ימי העסקים אינם כוללים שישי, שבת, ערבי חג ויום ההזמנה.",
    },
    {
        "question": "האם ניתן להחזיר או להחליף?",
        "answer": "כן. ניתן לפנות אלינו תוך 14 יום מקבלת המוצר. אם הבגד לא נלבש ונשמר במצב חדש ניתן לבצע החלפה או החזרה.",
    },
    {
        "question": "האם הבגד מתאים כמתנה ללידה?",
        "answer": "כן. רבים מהלקוחות שלנו בוחרים את הבגדים כמתנה ללידה. העיצוב העדין והבד הנעים הופכים אותו למתנה שימושית ונעימה להורים ולתינוק.",
    },
    {
        "question": "מי אנחנו?",
        "answer": "BabyMania הוא מותג לביגוד ונעלי תינוקות שנולד מתוך חוויית הורות אמיתית. אנחנו זוג הורים לשבעה ילדים והקמנו את החנות בשנת 2020 אחרי אינספור חיפושים אחר בגדים יפים ונוחים לתינוקות. את הפריטים שאנחנו בוחרים לאתר אנחנו קודם כל מלבישים לילדים שלנו ורק אז מציעים אותם בחנות.",
    },
]

# All 10 clothing-test product IDs (verified 2026-03-16)
PRODUCT_IDS = [
    "10009173033273",
    "10029648970041",
    "10029649101113",
    "10029649133881",
    "9657091293497",
    "9673732292921",
    "9687596728633",
    "9688660312377",
    "9688932909369",
    "9688934940985",
]


def get_existing_faq_metafield_id(pid):
    """Return the metafield ID if baby_mania.faq already exists, else None."""
    resp = requests.get(
        f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "key": "faq"},
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    for mf in resp.json().get("metafields", []):
        if mf.get("key") == "faq":
            return mf["id"]
    return None


def write_faq(pid, items):
    """Create or update baby_mania.faq metafield for a product."""
    value = json.dumps(items, ensure_ascii=False)
    existing_id = get_existing_faq_metafield_id(pid)

    if existing_id:
        # Update existing
        resp = requests.put(
            f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields/{existing_id}.json",
            headers=HDR,
            json={"metafield": {"id": existing_id, "value": value, "type": "json"}},
            timeout=10,
        )
    else:
        # Create new
        resp = requests.post(
            f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
            headers=HDR,
            json={"metafield": {
                "namespace": "baby_mania",
                "key": "faq",
                "value": value,
                "type": "json",
            }},
            timeout=10,
        )

    return resp.status_code in (200, 201), resp.status_code


def verify_faq(pid):
    """Read back the faq metafield and return (items_count, first_question_preview)."""
    resp = requests.get(
        f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "key": "faq"},
        timeout=10,
    )
    if resp.status_code != 200:
        return 0, ""
    for mf in resp.json().get("metafields", []):
        if mf.get("key") == "faq":
            try:
                items = json.loads(mf["value"])
                first_q = items[0]["question"] if items else ""
                return len(items), first_q
            except Exception:
                return 0, ""
    return 0, ""


# ─── Main ────────────────────────────────────────────────────────────────────

if not TOKEN:
    print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
    sys.exit(1)

print("=" * 60)
print("BabyMania — FAQ Publish (metafield only)")
print("=" * 60)

results = {}
for pid in PRODUCT_IDS:
    items = FIXED_FAQ  # same 6 questions for every product
    ok, status = write_faq(pid, items)
    count, preview = verify_faq(pid) if ok else (0, "")
    results[pid] = {
        "write_ok": ok,
        "http_status": status,
        "items_count": count,
        "first_question": preview,
    }
    mark = "OK" if (ok and count == 6) else "FAIL"
    print(f"[{pid}] {mark}  items={count}  q1={preview[:40]}")
    time.sleep(0.4)

# ─── Report ──────────────────────────────────────────────────────────────────
print()
print("=" * 60)
failed = [p for p, r in results.items() if not r["write_ok"] or r["items_count"] != 6]
risk = "LOW" if not failed else f"HIGH — {len(failed)} failures"

print("SYSTEM STATE:  FAQ publisher v2.0 — fixed FAQ, no dynamic logic")
print(f"PRODUCT STATE: {len(PRODUCT_IDS) - len(failed)}/{len(PRODUCT_IDS)} written successfully")
print(f"ISSUES FOUND:  {failed if failed else 'none'}")
print(f"RISK LEVEL:    {risk}")
print("NEXT STEP:     " + ("Verify in storefront bm-store-faq section" if not failed else "Re-run for failed products"))
print()
print("─── Per Product ─────────────────────────────────────────────────────")
for pid, r in results.items():
    print(f"  product id:            {pid}")
    print(f"  template:              clothing-test")
    print(f"  faq metafield written: {'yes' if r['write_ok'] else 'no'}")
    print(f"  items count:           {r['items_count']}")
    print(f"  first question:        {r['first_question'][:60]}")
    print()

# Save report
out = Path(__file__).parent.parent / "output" / "faq_publish_report.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Report saved: {out}")
