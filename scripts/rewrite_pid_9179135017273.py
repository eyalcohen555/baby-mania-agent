#!/usr/bin/env python3
"""
rewrite_pid_9179135017273.py
-----------------------------
Full live rewrite of baby_mania.accordion_blocks, baby_mania.faq, baby_mania.benefits
for PID 9179135017273 (נעלי בובה נסיכותיות דגם פרפר, נגד החלקה - נויה) ONLY.

APPROVAL_TIER: T2
DO NOT TOUCH: any other PID, theme, template, title, SEO fields.
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

TARGET_PID = "9179135017273"

# ─── New Content ─────────────────────────────────────────────────────────────

NEW_ACCORDION_BLOCKS = [
    {
        "title": "ילדה שבחרה לנעול לבד — שינוי שמתחיל בבוקר",
        "desc": "יש הבדל בין נעל שמנעילים לה לבין נעל שהיא מבקשת. כשהעיצוב מושך אותה — הנסיכה, הפרפר, הצבע — היא מגיעה לנעל לבד. ילדה שמצליחה לנעול לבד יוצאת עם תחושה של 'יכולתי'. הבוקר הבא קצת יותר קל. ואתה קצת פחות רודף.",
        "connection": "הנעל הזו הפכה את שלב הנעילה מויכוח לרצון."
    },
    {
        "title": "נעל אחת — אירוע, גן, תמונות",
        "desc": "לקנות נעל רק לאירוע שנועלת פעם בשנה זו פשרה. הנעל הזו עובדת בשני עולמות: הגימור הנסיכותי מתאים לשמלה חגיגית ולתמונות, והסוליה הנוחה מאפשרת לה לנעול גם לגן ביום רגיל. ילדה שמרגישה נסיכה גם בגן — לא מורידה.",
        "connection": "נעל שנועלים גם כשאין אירוע — שווה את הכסף."
    },
    {
        "title": "צעד ראשון צריך לחוש את הרצפה",
        "desc": "ילדה שמתחילה ללכת לא צריכה נעל קשיחה — היא צריכה נעל שמאפשרת לכף הרגל לחוש את המשטח. הסוליה הקלה בנעל הזו מאפשרת גמישות בכף הרגל, מחזיקה על אריחים חלקים ולא מכביד את הצעד. פחות עיכוב, יותר ביטחון.",
        "connection": "כשהצעד הראשון יציב, השאר בא לבד."
    }
]

NEW_FAQ = [
    {
        "question": "מי אנחנו?",
        "answer": "BabyMania הוא מותג לביגוד ונעלי תינוקות שנולד מתוך חוויית הורות אמיתית. אנחנו זוג הורים לשבעה ילדים והקמנו את החנות בשנת 2020 אחרי אינספור חיפושים אחר בגדים יפים ונוחים לתינוקות. את הפריטים שאנחנו בוחרים לאתר אנחנו קודם כל מלבישים לילדים שלנו ורק אז מציעים אותם בחנות."
    },
    {
        "question": "האם הנעל מתאימה לאירועים וגם לגן?",
        "answer": "כן. עיצוב הפרפר והגימור החגיגי מתאים לאירועים — ובגלל שהיא נוחה ונועלת מהר, היא עובדת גם לגן ביום רגיל. נעל אחת לכל המקרים."
    },
    {
        "question": "איך בוחרים מידה?",
        "answer": "מודדים את אורך כף הרגל מהעקב עד קצה האצבע הארוכה ביותר. השוו לטבלת המידות שבדף המוצר. בין שתי מידות — עולים מידה."
    },
    {
        "question": "האם הנעל מתאימה כמתנה?",
        "answer": "בהחלט. עיצוב הפרפר הופך אותה למתנת לידה, יום הולדת או חג שנראית טוב גם בלי אריזה מיוחדת. כדאי לציין את המידה בהזמנה."
    },
    {
        "question": "האם ניתן להחזיר או להחליף?",
        "answer": "כן. ניתן לפנות אלינו תוך 14 יום מקבלת המוצר. אם הנעל לא נועלה ונשמרה במצב חדש — ניתן לבצע החלפה או החזרה."
    },
    {
        "question": "מה זמני המשלוח?",
        "answer": "משלוח עד הבית מגיע תוך 5–8 ימי עסקים. איסוף מנקודת איסוף תוך 6–11 ימי עסקים. ההזמנה נשלחת תוך 1–3 ימי עסקים. ימי עסקים אינם כוללים שישי, שבת וערבי חג. מספר מעקב יישלח למייל."
    }
]

NEW_BENEFITS = [
    {
        "icon": "✨",
        "title": "עיצוב פרפר שכובש",
        "body": "הילדה מגיעה אליה לבד — פחות ויכוחים, יוצאים בזמן"
    },
    {
        "icon": "🛡️",
        "title": "אנטי-סליפ על כל משטח",
        "body": "אריחים, פרקט, מדרכה אחרי גשם — הסוליה מחזיקה"
    },
    {
        "icon": "⚡",
        "title": "כניסה בתנועה אחת",
        "body": "נועלת בלי לשבת — גם בשלושים שניות לפני היציאה"
    },
    {
        "icon": "👑",
        "title": "גימור נסיכותי",
        "body": "שמלה, חליפה, לוק גן — נראית נכון בכולם"
    },
    {
        "icon": "🤗",
        "title": "נשארת ברגל עד הסוף",
        "body": "הילדה לא מורידה — האירוע עובר שלם בלי חיפוש"
    },
    {
        "icon": "🎁",
        "title": "מתנה שעובדת",
        "body": "יפה גם בלי אריזה — מתאים ללידה, יום הולדת או חג"
    }
]

METAFIELDS_TO_WRITE = {
    "accordion_blocks": NEW_ACCORDION_BLOCKS,
    "faq": NEW_FAQ,
    "benefits": NEW_BENEFITS,
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_metafield_id(pid, key):
    """Return the ID of an existing baby_mania.{key} metafield, or None."""
    resp = requests.get(
        f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "key": key},
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    for mf in resp.json().get("metafields", []):
        if mf.get("key") == key:
            return mf["id"]
    return None


def write_metafield(pid, key, value_obj):
    """Create or update baby_mania.{key} metafield with JSON value."""
    value = json.dumps(value_obj, ensure_ascii=False)
    existing_id = get_metafield_id(pid, key)

    if existing_id:
        resp = requests.put(
            f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields/{existing_id}.json",
            headers=HDR,
            json={"metafield": {"id": existing_id, "value": value, "type": "json"}},
            timeout=15,
        )
    else:
        resp = requests.post(
            f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
            headers=HDR,
            json={"metafield": {
                "namespace": "baby_mania",
                "key": key,
                "value": value,
                "type": "json",
            }},
            timeout=15,
        )

    ok = resp.status_code in (200, 201)
    return ok, resp.status_code


def read_back_metafield(pid, key):
    """Read back a metafield and return its parsed value or None."""
    resp = requests.get(
        f"https://{SHOP}/admin/api/{API}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "key": key},
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    for mf in resp.json().get("metafields", []):
        if mf.get("key") == key:
            try:
                return json.loads(mf["value"])
            except Exception:
                return None
    return None


# ─── Main ────────────────────────────────────────────────────────────────────

if not TOKEN:
    print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
    sys.exit(1)

print("=" * 65)
print(f"BabyMania — Full Metafield Rewrite for PID {TARGET_PID}")
print("=" * 65)
print(f"Target: נעלי בובה נסיכותיות דגם פרפר, נגד החלקה - נויה")
print(f"Fields: accordion_blocks, faq, benefits")
print()

# ─── Write Phase ─────────────────────────────────────────────────────────────

write_results = {}
for key, data in METAFIELDS_TO_WRITE.items():
    print(f"Writing {key}...", end=" ")
    ok, status = write_metafield(TARGET_PID, key, data)
    write_results[key] = {"ok": ok, "status": status}
    mark = "OK" if ok else f"FAIL (HTTP {status})"
    print(mark)
    time.sleep(0.5)

print()

# ─── Read-Back Verification ───────────────────────────────────────────────────

print("Running read-back verification...")
print()

all_pass = True

# --- accordion_blocks ---
acc = read_back_metafield(TARGET_PID, "accordion_blocks")
acc_exists     = acc is not None
acc_type_ok    = isinstance(acc, list)
acc_count_ok   = isinstance(acc, list) and len(acc) == 3
acc_keys_ok    = all(
    isinstance(b, dict) and "title" in b and "desc" in b and "connection" in b
    for b in (acc or [])
)

print(f"  accordion_blocks exists:        {'YES' if acc_exists else 'NO'}")
print(f"  accordion_blocks type=list:     {'YES' if acc_type_ok else 'NO'}")
print(f"  accordion_blocks count=3:       {'YES' if acc_count_ok else 'NO'}")
print(f"  accordion keys (t/d/c) present: {'YES' if acc_keys_ok else 'NO'}")

if not (acc_exists and acc_type_ok and acc_count_ok and acc_keys_ok):
    all_pass = False

# --- faq ---
faq = read_back_metafield(TARGET_PID, "faq")
faq_exists   = faq is not None
faq_type_ok  = isinstance(faq, list)
faq_count_ok = isinstance(faq, list) and 5 <= len(faq) <= 6

# Check for "מי אנחנו"
faq_has_mi_anachnu = any(
    "מי אנחנו" in item.get("question", "") for item in (faq or [])
)
# Check for "זמני משלוח"
faq_has_shipping = any(
    "משלוח" in item.get("question", "") for item in (faq or [])
)
# Check for duplicate mida questions
mida_questions = [
    item for item in (faq or [])
    if "מידה" in item.get("question", "") or "מדידה" in item.get("question", "")
]
faq_no_dup_mida = len(mida_questions) <= 1

print()
print(f"  faq exists:                     {'YES' if faq_exists else 'NO'}")
print(f"  faq type=list:                  {'YES' if faq_type_ok else 'NO'}")
print(f"  faq count 5-6:                  {'YES' if faq_count_ok else 'NO'} ({len(faq) if isinstance(faq, list) else 'N/A'})")
print(f"  'מי אנחנו' present:             {'YES' if faq_has_mi_anachnu else 'NO'}")
print(f"  'זמני משלוח' present:            {'YES' if faq_has_shipping else 'NO'}")
print(f"  no duplicate mida questions:    {'YES' if faq_no_dup_mida else 'NO'}")

if not (faq_exists and faq_type_ok and faq_count_ok and faq_has_mi_anachnu and faq_has_shipping and faq_no_dup_mida):
    all_pass = False

# --- benefits ---
ben = read_back_metafield(TARGET_PID, "benefits")
ben_exists    = ben is not None
ben_type_ok   = isinstance(ben, list)
ben_count_ok  = isinstance(ben, list) and len(ben) == 6
ben_no_empty  = all(
    item.get("body", "").strip() != "" for item in (ben or [])
)
BROKEN_TOKENS = ["בדף", "שלושה כיוונים בדף", "נראית שחשבו", "שלושה כיוונים"]
ben_no_broken = not any(
    any(tok in item.get("body", "") or tok in item.get("title", "") for tok in BROKEN_TOKENS)
    for item in (ben or [])
)

print()
print(f"  benefits exists:                {'YES' if ben_exists else 'NO'}")
print(f"  benefits type=list:             {'YES' if ben_type_ok else 'NO'}")
print(f"  benefits count=6:               {'YES' if ben_count_ok else 'NO'} ({len(ben) if isinstance(ben, list) else 'N/A'})")
print(f"  no empty bodies:                {'YES' if ben_no_empty else 'NO'}")
print(f"  no truncated/broken text:       {'YES' if ben_no_broken else 'NO'}")

if not (ben_exists and ben_type_ok and ben_count_ok and ben_no_empty and ben_no_broken):
    all_pass = False

# ─── Update publisher.json on disk ───────────────────────────────────────────

stage_dir = BASE_DIR / "output" / "stage-outputs"
publisher_path = stage_dir / f"{TARGET_PID}_publisher.json"
try:
    existing = json.loads(publisher_path.read_text(encoding="utf-8"))
    existing["metafields"]["accordion_blocks"] = NEW_ACCORDION_BLOCKS
    existing["metafields"]["faq"] = NEW_FAQ
    existing["metafields"]["benefits"] = NEW_BENEFITS
    publisher_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    print(f"  publisher.json updated on disk: YES")
except Exception as e:
    print()
    print(f"  publisher.json update: FAILED ({e})")

# ─── Final Report ─────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("LIVE WRITE SUMMARY")
print("=" * 65)
for key, r in write_results.items():
    print(f"  {key:<25} rewritten: {'YES' if r['ok'] else 'NO'}")

print()
print("READ-BACK VERIFICATION")
print(f"  accordion_blocks exists:      {'YES' if acc_exists else 'NO -- FAIL'}")
print(f"  accordion_blocks type:        {'json (list)' if acc_type_ok else 'WRONG'}")
print(f"  accordion_blocks structure:   {'list[3]' if acc_count_ok else 'WRONG'}")
print(f"  accordion keys present:       {'YES' if acc_keys_ok else 'NO -- FAIL'}")
print(f"  faq exists:                   {'YES' if faq_exists else 'NO -- FAIL'}")
print(f"  faq type:                     {'json (list)' if faq_type_ok else 'WRONG'}")
print(f"  faq count:                    {len(faq) if isinstance(faq, list) else 'N/A'}")
print(f"  'מי אנחנו' exists:            {'YES' if faq_has_mi_anachnu else 'NO -- FAIL'}")
print(f"  'זמני משלוח' exists:           {'YES' if faq_has_shipping else 'NO -- FAIL'}")
print(f"  duplicate mida question:      {'NO' if faq_no_dup_mida else 'YES -- FAIL'}")
print(f"  benefits exists:              {'YES' if ben_exists else 'NO -- FAIL'}")
print(f"  benefits type:                {'json (list)' if ben_type_ok else 'WRONG'}")
print(f"  benefits count:               {len(ben) if isinstance(ben, list) else 'N/A'}")
print(f"  truncated text remains:       {'NO' if ben_no_broken else 'YES -- FAIL'}")

risk = "נמוך" if all_pass else "גבוה — read-back FAIL לפחות על שדה אחד"
verdict = "PASS" if all_pass else "FAIL"

print()
print(f"RISK LEVEL:     {risk}")
print(f"OVERALL:        {verdict}")
print()
if all_pass:
    print("NEXT STEP:      manual storefront review for PID 9179135017273 only")
    print(f"  URL: https://www.babymania-il.com/products/נעלי-בובה-פרפר-נגד-החלקה-נויה")
else:
    failed_fields = [k for k, r in write_results.items() if not r["ok"]]
    print(f"NEXT STEP:      re-run for failed fields: {failed_fields}")
