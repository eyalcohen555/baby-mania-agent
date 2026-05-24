"""Build the 3 required output files.

Sources of truth (priority):
  1. Shopify SKU + variants  (authoritative for what's actually sold)
  2. Shopify handle keywords (Shopify-controlled, used to *describe* model)
  3. AliExpress identity      (confirmed only when image-hash overlaps)
  4. AliExpress specs         (UNKNOWN — could not be reliably scraped)

Anything we couldn't verify -> UNKNOWN. No fabricated data.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "_shopify_raw.json").read_text(encoding="utf-8"))
VER = json.loads((ROOT / "_ali_verified2.json").read_text(encoding="utf-8"))

# Manual identity records (image-hash matches from _ali_verified2.json)
VERIFIED = {p["shopify_pid"]: p for p in VER["per_product"]}

# Notes on best-known model name (from Shopify handle, not Ali)
MODEL_NAME = {
    9689589383481: "Levi (vinyl/cloth or silicone body, 49cm)",
    9690182385977: "BZDoll 55cm full silicone",
    9690182418745: "BZDoll 60cm soft silicone",
    9690182451513: "LouLou 50cm cloth body",
    9690247627065: "NPK Levi (awake) 49cm",
    9690247659833: "Maddie 50cm full vinyl",
}

# Safety-flag scan keywords (canonical English forms)
SAFETY_KEYWORDS = [
    ("handmade", "מוצהר בכותרת AliExpress / handle כ-handmade"),
    ("full silicone", "מוצהר full silicone — לא אומת"),
    ("medical grade", "טענה רפואית — נדרש אימות"),
    ("safety certified", "טענת בטיחות — נדרש אימות"),
    ("en71", "תקן EN71 — נדרש אימות"),
    ("magnetic pacifier", "מוצץ מגנטי — מסוכן לתינוקות"),
    ("therapy", "טענה טיפולית — לא לשימוש בקופי"),
    ("anxiety", "טענת חרדה — לא לשימוש בקופי"),
    ("dementia", "טענת דמנציה — לא לשימוש בקופי"),
    ("bath safe", "טענה לאמבטיה — נדרש אימות"),
    ("waterproof", "טענת waterproof — נדרש אימות"),
]


def scan_safety(text):
    text_l = text.lower()
    flags = []
    for kw, note in SAFETY_KEYWORDS:
        # word-boundary or hyphenated boundary
        pattern = r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])"
        if re.search(pattern, text_l):
            flags.append({"term": kw, "note": note})
    # explicit "CE " (avoid false positives by requiring boundary)
    if re.search(r"\bce\b", text_l):
        flags.append({"term": "CE", "note": "טענת CE — נדרש אימות מהיבואן/יצרן"})
    return flags


def shopify_size_from_sku(skus):
    """Extract size token (e.g., 49cm, 60cm) from SKU string list."""
    sizes = []
    for sku in skus:
        for m in re.finditer(r"(\d{2,3}\s*cm)", sku, re.IGNORECASE):
            sizes.append(m.group(1).lower().replace(" ", ""))
    return sorted(set(sizes))


def shopify_size_from_handle(handle):
    """Extract '49cm' / '55cm' / '60cm' style tokens from handle."""
    found = re.findall(r"(\d{2,3})\s*cm", handle, re.IGNORECASE)
    return sorted({f"{n}cm" for n in found})


def shopify_inch_from_handle(handle):
    found = re.findall(r"(\d{2})\s*-?inches?", handle, re.IGNORECASE)
    return sorted({f"{n}inch" for n in found})


def body_type_from_handle(handle):
    h = handle.lower()
    tags = []
    if "cloth-body" in h or "cloth body" in h:
        tags.append("cloth body")
    if "vinyl" in h:
        tags.append("vinyl")
    if "silicone" in h:
        tags.append("silicone")
    if "full-vinyl" in h or "full vinyl" in h:
        tags.append("full vinyl")
    if "full-silicone" in h or "full silicone" in h:
        tags.append("full silicone")
    return tags


def main():
    products = []
    for prod in RAW["products"]:
        pid = prod["id"]
        ver = VERIFIED.get(pid, {})
        skus = [v.get("sku", "") for v in prod.get("variants", [])]
        sizes_sku = shopify_size_from_sku(skus)
        sizes_handle = shopify_size_from_handle(prod["handle"])

        # Variant analysis
        variant_options = sorted({
            (v.get("option1") or "").strip()
            for v in prod.get("variants", [])
            if v.get("option1")
        })
        body_types_in_options = []
        for v in prod.get("variants", []):
            o1 = (v.get("option1") or "").lower()
            sku = (v.get("sku") or "").lower()
            if "cloth body" in o1 or "cloth body" in sku or "עשוי בד" in o1:
                body_types_in_options.append("cloth body")
            if "silicone body" in o1 or "silicone body" in sku or "סילקון" in o1 or "סיליקון" in o1:
                body_types_in_options.append("silicone body")
        body_types_in_options = sorted(set(body_types_in_options))

        # Identity from verification
        identity_confirmed = bool(ver.get("identity_confirmed"))
        ali_item = ver.get("matched_item")
        shared = ver.get("shared_hashes", [])

        # Known explicit user fact for Levi#1
        size_ali = "UNKNOWN"
        size_mismatch = False
        if pid == 9689589383481:
            size_ali = "46cm"  # provided by user in task
            if "49cm" in sizes_sku:
                size_mismatch = True

        # Safety flags scanned only from Shopify-controlled text (handle).
        # The AliExpress page content was JS-rendered and could not be
        # reliably scraped, so we don't flag from there to avoid false flags.
        flags = scan_safety(prod["handle"])

        # SKU vs SKU mismatches (within product)
        sku_mismatches = []
        if pid == 9689589383481:
            sku_mismatches.append({
                "field": "size",
                "shopify_sku": "49cm",
                "aliexpress": "46cm",
                "note": "Shopify SKU מציין 49cm, אך מקור AliExpress מציין 46cm",
            })

        # AliExpress URL (only if confirmed)
        ali_url = ""
        if ali_item:
            ali_url = f"https://www.aliexpress.com/item/{ali_item}.html"

        entry = {
            "shopify_pid": str(pid),
            "shopify_title": prod["title"],
            "shopify_handle": prod["handle"],
            "shopify_status": prod["status"],
            "model_short": MODEL_NAME.get(pid, "UNKNOWN"),
            "aliexpress_item_id": ali_item or "",
            "aliexpress_url": ali_url,
            "aliexpress_title": "UNKNOWN",  # could not reliably extract
            "identity_confirmed": identity_confirmed,
            "identity_evidence": {
                "method": "image-hash overlap (Shopify CDN filename vs AliExpress page DOM)",
                "shared_hashes": shared,
                "shared_count": len(shared),
                "candidates_tested": [t["id"] for t in ver.get("tested", [])],
            },
            "specs": {
                "size_aliexpress": size_ali,
                "size_shopify_sku": sizes_sku[0] if sizes_sku else "UNKNOWN",
                "size_shopify_handle": sizes_handle,
                "size_mismatch": size_mismatch,
                "inches_in_handle": shopify_inch_from_handle(prod["handle"]),
                "weight": "UNKNOWN",
                "body_material": "UNKNOWN",
                "body_material_from_handle": body_type_from_handle(prod["handle"]),
                "body_type_from_variants": body_types_in_options,
                "body_type": "UNKNOWN",
                "hair_type": "UNKNOWN",
                "eye_type": "UNKNOWN",
                "eye_type_from_variants": [
                    o for o in variant_options
                    if "eye" in o.lower() or "eyes" in o.lower()
                ],
                "gender_option": "UNKNOWN",
                "clothes_included": "UNKNOWN",
                "accessories": [],
                "washable": "UNKNOWN",
                "age_recommendation": "UNKNOWN",
                "available_options_names": [o["name"] for o in (prod.get("options") or [])],
                "available_variants_titles": [v["title"] for v in prod["variants"]],
                "variant_count": len(prod["variants"]),
                "in_stock_total": sum(
                    (v.get("inventory_quantity") or 0) for v in prod["variants"]
                ),
            },
            "safety_flags": flags,
            "sku_mismatches": sku_mismatches,
            "shopify_main_image": prod.get("image_main"),
            "shopify_image_count": len(prod.get("images") or []),
        }
        products.append(entry)

    # ── 1. tech specs ─────────────────────────────────────────────────────
    (ROOT / "reborn-tech-specs.json").write_text(
        json.dumps({"products": products}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ── 2. reviews ────────────────────────────────────────────────────────
    reviews_obj = {
        "products": [
            {
                "shopify_pid": p["shopify_pid"],
                "aliexpress_item_id": p["aliexpress_item_id"],
                "reviews_accessible": False,
                "reviews_note": "REVIEWS NOT ACCESSIBLE — AliExpress reviews API חסום ב-captcha בסביבה זו",
                "reviews": [],
            }
            for p in products
        ]
    }
    (ROOT / "reborn-reviews.json").write_text(
        json.dumps(reviews_obj, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ── 3. diff table ─────────────────────────────────────────────────────
    md = []
    md.append("# ריבורן — טבלת השוואה בין 6 הדגמים")
    md.append("")
    md.append("מסמך מחקר פנימי. **אסור להעתיק לקופי מכירתי** עד אימות מהיבואן.")
    md.append("")
    md.append("## טבלת השוואה ראשית")
    md.append("")
    md.append(
        "| PID | דגם | מידה (SKU) | מידה (handle) | גוף — מ-handle | וריאנטים | בוצע אימות מול AliExpress | Ali item | Safety flags |"
    )
    md.append("|---|---|---|---|---|---|---|---|---|")
    for p in products:
        s = p["specs"]
        confirm_emoji = "✅" if p["identity_confirmed"] else "❌"
        flag_str = ", ".join(f["term"] for f in p["safety_flags"]) or "—"
        md.append(
            "| {pid} | {model} | {ssku} | {shand} | {body} | {vc} | {conf} | {ali} | {flags} |".format(
                pid=p["shopify_pid"],
                model=p["model_short"],
                ssku=s["size_shopify_sku"],
                shand=", ".join(s["size_shopify_handle"]) or "—",
                body=", ".join(s["body_material_from_handle"]) or "—",
                vc=s["variant_count"],
                conf=f"{confirm_emoji} ({p['identity_evidence']['shared_count']} hashes)",
                ali=p["aliexpress_item_id"] or "—",
                flags=flag_str,
            )
        )
    md.append("")
    md.append("## מה משותף לכל הדגמים (מתוך Shopify)")
    md.append("- כולם vendor = `BABY MANIA`")
    md.append("- כולם status = `active`")
    md.append("- כולם לא משויכים ל-product_type")
    md.append("- כולם בלי תגיות (tags ריק)")
    md.append("")
    md.append("## מה שונה בין הדגמים")
    md.append("- **מספר וריאנטים**: נע בין 1 (Maddie / Loulou / BZDoll-60cm) ל-13 (BZDoll-55cm צבעים)")
    md.append("- **מידה ב-SKU**: 49cm (Levi#1, NPK-Levi#2) / 60cm (BZDoll-60cm) / אין בכלל (BZDoll-55cm, Loulou, Maddie)")
    md.append("- **סוג גוף**: cloth body / silicone body (Levi#1 מציע שניהם); full vinyl (Maddie); full silicone (BZDoll-55cm לפי handle)")
    md.append("- **אופציות**: צבע (BZDoll-55cm) / עיניים (NPK-Levi#2 brown vs blue) / חומר (Levi#1) / מידה (BZDoll-60cm) / ברירת מחדל (Maddie, Loulou)")
    md.append("")
    md.append("## שדות חייבים להיות ייחודיים לכל דף מוצר")
    md.append("- שם דגם (Levi / BZDoll-55 / BZDoll-60 / LouLou / NPK-Levi / Maddie)")
    md.append("- מידה — חלק עם 49cm/60cm במידה ב-SKU, חלק רק ב-handle")
    md.append("- מתאר גוף (vinyl / silicone / cloth)")
    md.append("- וריאנטים (צבע/עיניים/מידה — לפי מה שזמין)")
    md.append("- תמונה ראשית (כל דגם תמונה משלו)")
    md.append("- handle (כל דגם handle ייחודי)")
    md.append("")
    md.append("## נתונים חסרים (UNKNOWN) — חיים בקובץ ה-JSON")
    md.append("- משקל בפועל — לא חולץ מ-AliExpress")
    md.append("- בגדים כלולים בקופסה — לא חולץ")
    md.append("- אביזרים נוספים — לא חולץ")
    md.append("- ניתן לרחיצה / waterproof אמיתי — מופיע בכותרות אבל לא אומת")
    md.append("- גיל מומלץ — לא אומת")
    md.append("- תעודות בטיחות (CE / EN71) — לא אומת — אין להזכיר בלי אסמכתא")
    md.append("- חומר גוף מדויק לכל דגם — handle בלבד, לא AliExpress")
    md.append("- AliExpress title — לא חולץ")
    md.append("")
    md.append("## סיכונים לפני כתיבת קופי")
    md.append("1. **mismatch גודל ב-Levi#1**: Shopify SKU=49cm, AliExpress=46cm — לבדוק מה השלוח בפועל")
    md.append("2. **טענת full silicone (BZDoll-55cm)**: מופיע ב-handle אבל בפועל כנראה vinyl+silicone parts — חובה אימות בטרם שיווק")
    md.append("3. **טענת waterproof (Maddie)**: מופיע ב-handle. אסור לכתוב 'מתאים לאמבטיה' בלי בדיקה")
    md.append("4. **טענת handmade**: מופיעה ב-3 דגמים — עבודת מכונה בפועל בסין; להימנע מהבטחה")
    md.append("5. **3 מ-6 לא אומתו לפי image-hash**: ייתכן שאינם זהים לפריט שזיהינו ב-Web Search")
    md.append("6. **טענות רפואיות (therapy/anxiety/dementia)**: לא נמצאו ב-handle — חשוב שלא יופיעו גם בקופי")
    md.append("7. **תקנים (CE/EN71)**: לא קיים מידע מהיצרן בידינו — אין להציג בדף המוצר")
    md.append("")
    md.append("## הצעה: מבנה סקשן \"פרטי הדגם\"")
    md.append("")
    md.append("**עקרון**: chips קטנים, מובייל-first, פרימיום מינימליסטי. לא טבלה.")
    md.append("מקסימום 6 chips לכל מוצר. כל chip = label + value קצר. אם אין ערך אמיתי — chip לא יופיע.")
    md.append("")
    md.append("**שדות מומלצים** (לפי הזמינות בנתונים):")
    md.append("- 📏 **גודל** — מתוך SKU או handle (49cm / 55cm / 60cm)")
    md.append("- 🧸 **סוג גוף** — cloth body / silicone body / full vinyl / full silicone (מ-handle)")
    md.append("- 👁️ **עיניים** — אם יש וריאנט: brown / blue")
    md.append("- 🎨 **צבעים זמינים** — מספר הצבעים (לדוגמה 13)")
    md.append("- 💧 **מים/אמבטיה** — *רק אם אומת מהיבואן* — אחרת לא להציג")
    md.append("- 📦 **מה כלול** — *רק אם יודעים*. ברירת מחדל: לא להציג")
    md.append("")
    md.append("**שדות שאסור להציג עכשיו** (חוסר ידע):")
    md.append("- משקל מדויק")
    md.append("- גיל מומלץ")
    md.append("- תעודות בטיחות (CE/EN71)")
    md.append("- handmade")
    md.append("- מתאים לטיפול/חרדה/דמנציה")
    md.append("")
    md.append("---")
    md.append("**מקורות נתונים**: Shopify Admin API (קריאה בלבד) + AliExpress item pages (Playwright) + WebSearch לאיתור מועמדים.")
    md.append("")
    (ROOT / "reborn-diff-table.md").write_text("\n".join(md), encoding="utf-8")

    print("WROTE:")
    print(" - reborn-tech-specs.json")
    print(" - reborn-reviews.json")
    print(" - reborn-diff-table.md")


if __name__ == "__main__":
    main()
