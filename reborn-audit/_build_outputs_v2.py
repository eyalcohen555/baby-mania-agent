"""Build final 3 output files for round 2.

Decision rules:
  verified           : ≥3 shared image hashes (and title/size match)
  likely             : 0 shared hashes BUT title + size match (Shopify re-cropped)
  needs_manual_review: Eyal must decide (multi-doll page, shared URL across PIDs, image-search URL)
  not_verified       : no overlap, title/size don't match

Only "verified" + "likely" specs may feed the future "פרטי הדגם" section,
and only fields that are *actually visible* on the AliExpress page.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHOPIFY = json.loads((ROOT / "_shopify_raw_v2.json").read_text(encoding="utf-8"))
ROUND2C = json.loads((ROOT / "_ali_round2c.json").read_text(encoding="utf-8"))

# Manual decision table — encodes our reasoning per PID
# Order matches user's task numbering (1..10).
MANUAL = [
    # 1
    {
        "pid": 9690182385977,
        "primary_url": "https://he.aliexpress.com/item/1005007060038271.html",
        "primary_item_id": "1005007060038271",
        "status": "needs_manual_review",
        "reason": "Multi-doll page. Ali listing says 50cm/20inch but Shopify product is 55cm/22inch. 0 shared image hashes. Eyal must specify the exact variant in the listing.",
        "mismatches": [
            {"field": "size", "shopify": "55cm (handle) / no size in SKU",
             "ali": "50cm/20inch", "note": "MISMATCH or wrong listing"}
        ],
    },
    # 2
    {
        "pid": 10190523040057,
        "primary_url": "https://he.aliexpress.com/item/1005008896313230.html",
        "primary_item_id": "1005008896313230",
        "status": "verified",
        "reason": "7 shared image hashes. Size 50cm matches Shopify (50 ס\"מ).",
    },
    # 3
    {
        "pid": 10190523072825,
        "primary_url": "https://he.aliexpress.com/item/1005008275277733.html",
        "primary_item_id": "1005008275277733",
        "status": "verified",
        "reason": "5 shared image hashes. Size 20inch (~50cm) matches Shopify Maddie 50 ס\"מ.",
    },
    # 4
    {
        "pid": 10190523007289,
        "primary_url": "https://he.aliexpress.com/item/1005008672285275.html",
        "primary_item_id": "1005008672285275",
        "status": "verified",
        "reason": "6 shared image hashes. Size 13Inch (~33cm) matches Shopify Pascale 33 ס\"מ.",
    },
    # 5  (Meadow 46cm)
    {
        "pid": 10190522777913,
        "primary_url": "https://he.aliexpress.com/item/1005007170009461.html",
        "primary_item_id": "1005007170009461",
        "status": "needs_manual_review",
        "reason": "URL shared with PID 10190522810681. 0 shared image hashes on this Ali page (it's the Felicia listing, NOT Meadow). Eyal must provide a separate URL for Meadow.",
        "mismatches": [
            {"field": "model", "shopify": "Meadow 46cm",
             "ali": "Felicia 18-19in", "note": "Wrong listing — Meadow not represented"}
        ],
    },
    # 6  (Felicia 46cm)
    {
        "pid": 10190522810681,
        "primary_url": "https://he.aliexpress.com/item/1005007170009461.html",
        "primary_item_id": "1005007170009461",
        "status": "verified",
        "reason": "4 shared image hashes. Ali title is Felicia, size 18-19 inches (~46cm) matches Shopify Felicia 46 ס\"מ.",
    },
    # 7  (NPK Levi awake 49cm)
    {
        "pid": 9690247627065,
        "primary_url": "https://he.aliexpress.com/item/1005009088718947.html",
        "primary_item_id": "1005009088718947",
        "status": "likely",
        "reason": "0 shared image hashes (Shopify likely re-cropped images), but Ali title contains 'לווי' (Levi) and ממדים=19inch matches Shopify SKU 49cm.",
    },
    # 8  (LouLou 50cm — two URLs)
    {
        "pid": 9690182451513,
        "primary_url": "https://he.aliexpress.com/item/1005005188539088.html",
        "primary_item_id": "1005005188539088",
        "status": "verified",
        "reason": "Primary: 4 shared image hashes (MRB store). Secondary listing 1005007525021217 also matches with 2 shared hashes — same doll, two sellers.",
        "secondary_url": "https://he.aliexpress.com/item/1005007525021217.html",
        "secondary_item_id": "1005007525021217",
    },
    # 9  (BZDoll 60cm — image search URL; use previous round match)
    {
        "pid": 9690182418745,
        "primary_url": "https://he.aliexpress.com/item/1005006863845547.html",
        "primary_item_id": "1005006863845547",
        "status": "verified",
        "reason": "Image-search URL doesn't resolve to a single item. Carrying forward previous match 1005006863845547 (5 shared image hashes from round 1). Need fresh manual link to refresh specs.",
        "from_round1": True,
    },
    # 10  (Levi #1, 49cm SKU)
    {
        "pid": 9689589383481,
        "primary_url": "https://he.aliexpress.com/item/1005005317212200.html",
        "primary_item_id": "1005005317212200",
        "status": "likely",
        "reason": "0 shared image hashes in this round (round 1 had 1 shared). Ali title 'Reborn Levi' matches. Ali ממדים=17-18 inches (~43-46cm). Shopify SKU=49cm. SIZE MISMATCH.",
        "mismatches": [
            {"field": "size", "shopify": "49cm (SKU)",
             "ali": "17-18 inches (43-46cm)",
             "note": "Shopify SKU=49cm but Ali source page = 17-18 inches (43-46cm). MISMATCH — Eyal must decide actual shipped size."}
        ],
    },
]


def shopify_product(pid):
    for p in SHOPIFY["products"]:
        if p["id"] == pid:
            return p
    return None


def round2c_entry(pid, item_id):
    for e in ROUND2C:
        if e["pid"] == pid and (e["item_id"] == item_id or (item_id is None and e["item_id"] is None)):
            return e
    # fallback by url
    return None


def round2c_for_url(url):
    for e in ROUND2C:
        if e["url"] == url:
            return e
    return None


def size_extract(s):
    if not s:
        return ""
    m = re.search(r"(\d{2,3})\s*(?:cm|ס\"מ|ס״מ)", s)
    return f"{m.group(1)}cm" if m else ""


def safety_canonical(ali_safety_list, shopify_handle):
    """Return canonical bilingual flag list combining both sources."""
    canonical = []
    seen = set()

    def add(term, present_in_ali, present_in_handle, hebrew_text=""):
        key = term.lower()
        if key in seen:
            return
        seen.add(key)
        canonical.append({
            "term": term,
            "hebrew": hebrew_text,
            "present_in_aliexpress": present_in_ali,
            "present_in_shopify_handle": present_in_handle,
        })

    sh = shopify_handle.lower()
    ali_set = set(s.lower() for s in ali_safety_list)
    for term, he in [
        ("handmade", "עבודת יד"),
        ("full silicone", "סיליקון מלא"),
        ("medical grade", "רפואי"),
        ("ce", "CE"),
        ("en71", "EN71"),
        ("magnetic pacifier", "מוצץ מגנטי"),
        ("waterproof", "עמיד למים"),
        ("bath safe", "מותאם לאמבטיה"),
        ("therapy", "טיפול"),
        ("anxiety", "חרדה"),
        ("dementia", "דמנציה"),
    ]:
        ali_present = (term in ali_set) or (he in ali_safety_list)
        handle_present = term.replace(" ", "-") in sh or term in sh
        if ali_present or handle_present:
            add(term, ali_present, handle_present, he)
    return canonical


def build_product_entry(decision):
    pid = decision["pid"]
    shopify_p = shopify_product(pid)
    primary_id = decision["primary_item_id"]
    r = round2c_for_url(decision["primary_url"])

    # spec_pairs from Ali; map to canonical field names
    ali_specs = (r["spec_pairs"] if r else {}) or {}

    def get_spec(*keys_he):
        for k_he in keys_he:
            for sp_k, sp_v in ali_specs.items():
                if k_he in sp_k:
                    return sp_v
        return "UNKNOWN"

    ali_size_raw = get_spec("ממדים", "Dimensions", "size", "Size")
    # Sometimes "13Inch" -> convert to cm-estimate (note: NOT authoritative)
    ali_gender = get_spec("מגדר", "Gender")

    # Shopify SKU info
    sku_sizes = []
    for v in shopify_p["variants"]:
        for m in re.finditer(r"(\d{2,3})\s*cm", v.get("sku", ""), re.IGNORECASE):
            sku_sizes.append(f"{m.group(1)}cm")
    sku_sizes = sorted(set(sku_sizes))

    # Build mismatches
    mismatches = decision.get("mismatches", [])

    # safety flags
    safety_present_ali = r["safety_present"] if r else []
    safety = safety_canonical(safety_present_ali, shopify_p["handle"])

    # Unknown fields list — what could not be reliably extracted
    unknown_fields = []
    field_results = {
        "size": ali_size_raw,
        "weight": "UNKNOWN",        # never in spec table
        "body_material": "UNKNOWN", # never in spec table
        "body_type": "UNKNOWN",
        "hair_type": "UNKNOWN",
        "eye_type": "UNKNOWN",
        "gender": ali_gender,
        "clothes_included": "UNKNOWN",
        "accessories": [],
        "washable": "UNKNOWN",
        "bath_safe": "UNKNOWN",
        "age_recommendation": "UNKNOWN",
        "certificates": "UNKNOWN",
    }
    for k, v in field_results.items():
        if v == "UNKNOWN" or v == []:
            unknown_fields.append(k)

    # Evidence
    screenshots = r["screenshots"] if r else []
    secondary_block = None
    if decision.get("secondary_url"):
        r2 = round2c_for_url(decision["secondary_url"])
        if r2:
            secondary_block = {
                "url": decision["secondary_url"],
                "item_id": decision["secondary_item_id"],
                "ali_title": r2["ali_title"],
                "shared_hashes": r2["shared_hashes"],
                "screenshots": r2["screenshots"],
                "spec_pairs": r2["spec_pairs"],
            }

    safe_for_pdp = decision["status"] in ("verified",)

    return {
        "shopify_pid": str(pid),
        "shopify_title": shopify_p["title"],
        "shopify_handle": shopify_p["handle"],
        "shopify_status": shopify_p["status"],
        "shopify_sku_sizes": sku_sizes,
        "shopify_variant_count": len(shopify_p["variants"]),
        "aliexpress_url": decision["primary_url"],
        "aliexpress_item_id": primary_id,
        "aliexpress_title": r["ali_title"] if r else "UNKNOWN",
        "source_status": decision["status"],
        "status_reason": decision["reason"],
        "evidence": {
            "shared_image_hashes": r["shared_hashes"] if r else [],
            "shared_image_hashes_count": len(r["shared_hashes"]) if r else 0,
            "screenshots": screenshots,
            "ali_spec_pairs_raw": ali_specs,
            "from_round1": decision.get("from_round1", False),
            "secondary": secondary_block,
        },
        "specs": field_results,
        "mismatches": mismatches,
        "unknown_fields": unknown_fields,
        "safety_flags_present": safety,
        "safe_for_product_page": safe_for_pdp,
        "shopify_main_image": shopify_p.get("image_main"),
    }


def main():
    products = [build_product_entry(d) for d in MANUAL]

    # 1. tech specs
    (ROOT / "reborn-tech-specs.json").write_text(
        json.dumps({"products": products}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 2. reviews
    reviews = {
        "products": [
            {
                "shopify_pid": p["shopify_pid"],
                "aliexpress_item_id": p["aliexpress_item_id"],
                "reviews_accessible": False,
                "reviews_note": ("REVIEWS NOT ACCESSIBLE — AliExpress reviews endpoint "
                                  "blocked by baxia (anti-bot). Manual access required."),
                "reviews": [],
            }
            for p in products
        ]
    }
    (ROOT / "reborn-reviews.json").write_text(
        json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 3. diff table (Hebrew Markdown)
    md = []
    md.append("# ריבורן — מקור אמת מוצרי (סבב 2, מקושר ידנית)")
    md.append("")
    md.append("> מסמך מחקר פנימי. אסור להעתיק לקופי שיווקי. רק שדות 'verified' מותרים לדף המוצר.")
    md.append("")
    md.append("## טבלת השוואה")
    md.append("")
    md.append("| # | Shopify PID | מקור AliExpress | סטטוס | גודל (Ali) | גודל (Shopify) | מגדר (Ali) | רחיץ | אביזרים | חסר עיקרי | שמיש לדף מוצר | הערה לאייל |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    titles_short = {
        9690182385977: "BZDoll 55cm (multi-doll page)",
        10190523040057: "50cm ויניל-סיליקון",
        10190523072825: "Maddie 50cm",
        10190523007289: "Pascale 33cm פה פתוח",
        10190522777913: "Meadow 46cm",
        10190522810681: "Felicia 46cm",
        9690247627065: "NPK Levi 19inch (awake)",
        9690182451513: "LouLou 50cm cloth body",
        9690182418745: "BZDoll 60cm",
        9689589383481: "Levi (vinyl/silicone choice)",
    }
    for i, p in enumerate(products, 1):
        pid = int(p["shopify_pid"])
        ali = p["aliexpress_item_id"] or "—"
        status = p["source_status"]
        size_ali = p["specs"]["size"] or "UNKNOWN"
        size_sh = ",".join(p["shopify_sku_sizes"]) or "—"
        gender = p["specs"]["gender"] or "UNKNOWN"
        washable = p["specs"]["washable"]
        accessories = ", ".join(p["specs"]["accessories"]) if p["specs"]["accessories"] else "—"
        missing = ", ".join(p["unknown_fields"][:4]) if p["unknown_fields"] else "—"
        usable = "✅" if p["safe_for_product_page"] else "❌"
        # note for Eyal
        note = ""
        for d in MANUAL:
            if d["pid"] == pid:
                note = d.get("reason", "")
                break
        # Pull mismatch-text inline
        if p["mismatches"]:
            note = "MISMATCH: " + p["mismatches"][0]["note"]
        md.append("| {i} | {pid} | {ali} | {st} | {sa} | {ss} | {g} | {w} | {acc} | {miss} | {u} | {n} |".format(
            i=i, pid=pid, ali=ali, st=status,
            sa=size_ali, ss=size_sh, g=gender, w=washable, acc=accessories,
            miss=missing, u=usable, n=note[:80]
        ))
    md.append("")
    md.append("## ממצאים חשובים")
    md.append("")
    md.append("**MISMATCHES שדורשים הכרעת אייל:**")
    for p in products:
        if p["mismatches"]:
            md.append(f"- PID {p['shopify_pid']}: " + "; ".join(
                f"{mm['field']}: Shopify={mm['shopify']} | Ali={mm['ali']}" for mm in p["mismatches"]
            ))
    md.append("")
    md.append("**NEEDS MANUAL REVIEW:**")
    for p in products:
        if p["source_status"] == "needs_manual_review":
            md.append(f"- PID {p['shopify_pid']}: {p['status_reason']}")
    md.append("")
    md.append("## שדות שנמצאו vs UNKNOWN")
    md.append("")
    md.append("**מה כן נמצא ב-AliExpress spec table** (אצל כל המוצרים שאומתו):")
    md.append("- ממדים (גודל) — בעברית, בפורמט מעורב (cm/inch)")
    md.append("- מגדר — Girls / יוניסקס / לשני המינים")
    md.append("- BJD / תכונה SD — כולם 'בובה'")
    md.append("- מצב — 'פריטים במלאי'")
    md.append("")
    md.append("**מה לא נמצא בשום spec table** (UNKNOWN לכל המוצרים):")
    md.append("- משקל")
    md.append("- חומר גוף מדויק (vinyl/silicone/cloth)")
    md.append("- סוג גוף מלא")
    md.append("- סוג שיער (שתול / מצויר)")
    md.append("- צבע עיניים")
    md.append("- בגדים כלולים")
    md.append("- אביזרים נוספים")
    md.append("- ניתן לרחיצה / האם מתאים לאמבטיה")
    md.append("- גיל מומלץ")
    md.append("- תעודות / CE / EN71")
    md.append("")
    md.append("**טענות שמופיעות בעמוד AliExpress** (סומנו אבל לא מאשרים אותן):")
    for p in products:
        if p["safety_flags_present"]:
            terms = [f["term"] for f in p["safety_flags_present"] if f["present_in_aliexpress"]]
            if terms:
                md.append(f"- PID {p['shopify_pid']}: {', '.join(terms)}")
    md.append("")
    md.append("## האם אפשר להשתמש במפרט לדף מוצר?")
    md.append("")
    md.append("**כן** — רק לאחר אישור הסטטוס 'verified' ורק לשדות שלא UNKNOWN:")
    for p in products:
        if p["safe_for_product_page"]:
            md.append(f"- PID {p['shopify_pid']} ({titles_short.get(int(p['shopify_pid']),'')}): גודל, מגדר. שאר השדות UNKNOWN.")
    md.append("")
    md.append("**לא** — לא לפני אישור אייל:")
    for p in products:
        if not p["safe_for_product_page"]:
            md.append(f"- PID {p['shopify_pid']} ({titles_short.get(int(p['shopify_pid']),'')}): סטטוס={p['source_status']}")
    md.append("")
    md.append("## הצעת שלד 'פרטי הדגם' (chips, מובייל)")
    md.append("")
    md.append("עיקרון: כל chip מציג רק שדה שלא UNKNOWN. אם השדה UNKNOWN — לא להציג chip.")
    md.append("מקסימום 6 chips. לא טבלה. פרימיום מינימליסטי.")
    md.append("")
    md.append("שדות מותרים כעת (לפי מה שאומת בפועל):")
    md.append("- 📏 **גודל** — מתוך SKU של Shopify (49cm/50cm/60cm) או מ-Ali (אם חופפים)")
    md.append("- 👤 **מתאים ל** — Girls / יוניסקס (מ-Ali ממדים=מגדר)")
    md.append("- 🧸 **שם דגם** — Levi / Maddie / Pascale / Felicia / LouLou (מ-Shopify handle)")
    md.append("")
    md.append("שדות שאסור להציג עכשיו (כולם UNKNOWN לכל המוצרים):")
    md.append("- משקל, גיל, רחיצה/אמבטיה, אביזרים, תעודות, חומר גוף מדויק")
    md.append("")
    md.append("---")
    md.append("**מקורות**: Shopify Admin API (קריאה בלבד) + Playwright Chromium על דפי AliExpress + screenshots מאוחסנים תחת `reborn-audit/screenshots/`.")
    md.append("")
    (ROOT / "reborn-diff-table.md").write_text("\n".join(md), encoding="utf-8")

    print("WROTE: reborn-tech-specs.json, reborn-reviews.json, reborn-diff-table.md")


if __name__ == "__main__":
    main()
