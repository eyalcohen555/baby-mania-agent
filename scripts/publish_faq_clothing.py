#!/usr/bin/env python3
"""
publish_faq_clothing.py
-----------------------
Updates baby_mania.faq metafield for ALL products with
template_suffix="clothing" using the same FIXED_FAQ as
publish_faq_only.py (clothing-test).

Touches ONLY:  product.metafields.baby_mania.faq
Does NOT touch: hero, benefits, care, fabric, sizes, urgency,
                template order, pipeline, other metafields.
"""
import io, os, sys, json, requests, time
from pathlib import Path
from dotenv import load_dotenv

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
BASE  = f"https://{SHOP}/admin/api/{API}"

# Identical FIXED_FAQ — same as publish_faq_only.py (clothing-test)
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
        "answer": "ניתן לבחור בין שני סוגי משלוח:\n\nמשלוח עד הבית: 5–9 ימי עסקים\nמשלוח לנקודת חלוקה: 6–11 ימי עסקים\n\nימי העסקים אינם כוללים שישי, שבת, ערבי חג ויום ההזמנה.",
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
        "question": "הסיפור שלנו",
        "answer": "BabyMania הוא מותג לביגוד ונעלי תינוקות שנולד מתוך חוויית הורות אמיתית. אנחנו זוג הורים לשבעה ילדים והקמנו את החנות בשנת 2020 אחרי אינספור חיפושים אחר בגדים יפים ונוחים לתינוקות. את הפריטים שאנחנו בוחרים לאתר אנחנו קודם כל מלבישים לילדים שלנו ורק אז מציעים אותם בחנות.",
    },
]

FAQ_VALUE = json.dumps(FIXED_FAQ, ensure_ascii=False)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_all_clothing_products():
    """Paginate through all products with template_suffix='clothing'."""
    products = []
    params = {
        "limit": 250,
        "fields": "id,title,handle,template_suffix",
        "template_suffix": "clothing",
    }
    while True:
        resp = requests.get(f"{BASE}/products.json", headers=HDR,
                            params=params, timeout=15)
        resp.raise_for_status()
        batch = resp.json().get("products", [])
        products.extend(batch)
        if len(batch) < 250:
            break
        params = {"limit": 250, "fields": "id,title,handle,template_suffix",
                  "template_suffix": "clothing", "since_id": batch[-1]["id"]}
    return products


def get_faq_metafield_id(pid):
    """Return existing baby_mania.faq metafield ID, or None."""
    resp = requests.get(
        f"{BASE}/products/{pid}/metafields.json",
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


def write_faq(pid):
    """Create or update baby_mania.faq. Returns (ok, http_status)."""
    existing_id = get_faq_metafield_id(pid)
    if existing_id:
        resp = requests.put(
            f"{BASE}/products/{pid}/metafields/{existing_id}.json",
            headers=HDR,
            json={"metafield": {"id": existing_id, "value": FAQ_VALUE, "type": "json"}},
            timeout=10,
        )
    else:
        resp = requests.post(
            f"{BASE}/products/{pid}/metafields.json",
            headers=HDR,
            json={"metafield": {
                "namespace": "baby_mania", "key": "faq",
                "value": FAQ_VALUE, "type": "json",
            }},
            timeout=10,
        )
    return resp.status_code in (200, 201), resp.status_code


def verify_faq(pid):
    """Read back FAQ and return (count, q3_question, q3_answer)."""
    resp = requests.get(
        f"{BASE}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "key": "faq"},
        timeout=10,
    )
    if resp.status_code != 200:
        return 0, "", ""
    for mf in resp.json().get("metafields", []):
        if mf.get("key") == "faq":
            try:
                items = json.loads(mf["value"])
                q3 = items[2] if len(items) > 2 else {}
                return len(items), q3.get("question", ""), q3.get("answer", "")
            except Exception:
                return 0, "", ""
    return 0, "", ""


# ─── Main ─────────────────────────────────────────────────────────────────────

# Safety gate — prevents accidental bulk overwrite of all clothing FAQ metafields
_CONFIRM_FLAG = "--confirm-bulk-faq-overwrite"
if _CONFIRM_FLAG not in sys.argv:
    print("=" * 65)
    print("BLOCKED: publish_faq_clothing.py")
    print("=" * 65)
    print()
    print("This script overwrites baby_mania.faq for ALL clothing products.")
    print("It BYPASSES the 06-validator pipeline gate entirely.")
    print()
    print(f"Re-run with:  python scripts/publish_faq_clothing.py {_CONFIRM_FLAG}")
    print()
    sys.exit(1)

# Guard: refuse if FIXED_FAQ contains the forbidden question title
for _q in FIXED_FAQ:
    if "מי אנחנו" in _q.get("question", ""):
        print("ERROR: FIXED_FAQ contains forbidden question title 'מי אנחנו?'")
        print("       Update to 'הסיפור שלנו' before running.")
        sys.exit(1)

if not TOKEN:
    print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
    sys.exit(1)

print("=" * 65)
print("BabyMania — FAQ Publish: template_suffix='clothing'")
print("=" * 65)

# Step 1 — collect all clothing products
print("\n[1] Fetching all products with template_suffix='clothing'...")
products = get_all_clothing_products()
print(f"    Found: {len(products)} products")

if not products:
    print("    Nothing to update.")
    sys.exit(0)

# Step 2 — update each product
print(f"\n[2] Updating FAQ metafield ({len(products)} products)...")
print("-" * 65)

results = {}
ok_count   = 0
fail_count = 0

for i, p in enumerate(products, 1):
    pid   = str(p["id"])
    title = p.get("title", "")[:40]

    ok, status = write_faq(pid)
    results[pid] = {"write_ok": ok, "http_status": status, "title": title}

    mark = "OK" if ok else "FAIL"
    print(f"  [{i:3}/{len(products)}] {mark} ({status})  {title}")

    if ok:
        ok_count += 1
    else:
        fail_count += 1

    # Rate limiting: ~2 req/s (get + put = 2 calls per product)
    time.sleep(0.5)

# Step 3 — verify 3 products
print(f"\n[3] Verifying spot-check (3 products)...")
sample_pids = [str(p["id"]) for p in products[:3]]
verify_results = {}
for pid in sample_pids:
    count, q3_q, q3_a = verify_faq(pid)
    has_59   = "5–9"  in q3_a
    has_611  = "6–11" in q3_a
    verify_results[pid] = {
        "items_count": count,
        "q3_correct": has_59 and has_611,
        "q3_question": q3_q,
        "q3_answer": q3_a,
    }
    time.sleep(0.3)

# ─── Reports ──────────────────────────────────────────────────────────────────
print()
print("=" * 65)
failed_pids = [pid for pid, r in results.items() if not r["write_ok"]]
all_verified = all(v["q3_correct"] for v in verify_results.values())

print("SYSTEM STATE:  FAQ publisher — clothing production (fixed FAQ)")
print(f"PRODUCT STATE: {ok_count}/{len(products)} written OK  |  {fail_count} failures")
print(f"ISSUES FOUND:  {failed_pids[:5] if failed_pids else 'none'}")
print(f"RISK LEVEL:    {'LOW' if not failed_pids else 'HIGH — see failures'}")
print()
print("─── Spot-check results ──────────────────────────────────────")
for pid, v in verify_results.items():
    title = results[pid]["title"]
    print(f"\n  product id  : {pid}")
    print(f"  title       : {title}")
    print(f"  items count : {v['items_count']}")
    print(f"  Q3          : {v['q3_question']}")
    print(f"  A3          :")
    print(f"    {v['q3_answer'].replace(chr(10), chr(10)+'    ')}")
    print(f"  contains 5–9: {'yes' if '5–9' in v['q3_answer'] else 'NO'}")
    print(f"  contains 6–11: {'yes' if '6–11' in v['q3_answer'] else 'NO'}")
    print(f"  Q3 correct  : {'yes' if v['q3_correct'] else 'NO'}")

print()
print("─── Summary ─────────────────────────────────────────────────")
print(f"  total clothing products  : {len(products)}")
print(f"  updated OK               : {ok_count}")
print(f"  failed                   : {fail_count}")
print(f"  Q3 verified correct      : {'yes' if all_verified else 'NO'}")
print(f"  FAQ clothing closed      : {'yes' if not failed_pids and all_verified else 'NO'}")

# Save report
out = BASE_DIR / "output/faq_clothing_publish_report.json"
out.parent.mkdir(exist_ok=True)
out.write_text(
    json.dumps({
        "total": len(products),
        "ok": ok_count,
        "failed": fail_count,
        "failed_pids": failed_pids,
        "spot_check": verify_results,
    }, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"\n  Report saved: {out}")
