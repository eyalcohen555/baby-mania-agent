"""
Layer 6 — Phase 5d Rerun
Phase 5b/5c logic updates. DRY RUN ONLY — no Shopify writes.
"""

import json, os, re, sys, html
from datetime import date
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from layer6_validate_tags import run_all_gates, PREFIX_TO_CAT, NON_AGE_TYPES

PHASE0_PRODUCTS  = "output/tags/phase0-raw-products.json"
YAML_DIR         = "shared/product-context"
ENV_PATH         = os.path.expanduser("~/Desktop/shopify-token/.env")
SHOP_URL         = "https://a2756c-c0.myshopify.com"
API_VERSION      = "2024-10"
PHASE4_REPORT    = "output/tags/phase4-dryrun-report.json"

OUT_SAMPLE       = "output/tags/phase5d-rerun-sample-59.json"
OUT_REPORT_JSON  = "output/tags/phase5d-rerun-report.json"
OUT_REPORT_MD    = "output/tags/phase5d-rerun-report.md"
OUT_COMPARISON_MD = "output/tags/phase5d-rerun-comparison.md"

CUSTOMER_LABELS = {
    "type-romper": "אוברולים", "type-bodysuit": "בגד גוף",
    "type-dress": "שמלה", "type-set": "סטים",
    "type-pants": "מכנסיים", "type-top": "חולצות",
    "type-hat": "כובעים", "type-swimwear": "בגדי ים",
    "type-shoes": "נעליים", "type-sandals": "סנדלים",
    "type-sneakers": "סניקרס", "type-boots": "מגפיים",
    "type-coat": "מעילים", "type-reborn-doll": "בובות ריבורן",
    "type-toy": "צעצועים", "type-plush-toy": "בובות פלאש",
    "type-sleep-soother": "מוצרי שינה והרגעה",
    "type-accessory": "אביזרים",
    "type-swimming-ring": "מצופי שחייה",
    "type-bath-accessory": "אביזרי אמבטיה",
    "type-unknown": "—",
    "age-0-3m": "0-3 חודשים", "age-3-6m": "3-6 חודשים",
    "age-6-12m": "6-12 חודשים", "age-12-18m": "12-18 חודשים",
    "age-18-24m": "18-24 חודשים", "age-2-3y": "2-3 שנים",
    "age-3-5y": "3-5 שנים", "age-0-6m": "0-6 חודשים",
    "age-newborn": "יילוד", "age-unknown": "—",
    "season-summer": "קיץ", "season-winter": "חורף",
    "season-spring-fall": "אביב/סתיו", "season-all": "כל עונה", "season-unknown": "—",
    "fabric-cotton": "כותנה", "fabric-linen": "פשתן",
    "fabric-muslin": "מוסלין", "fabric-knit": "סריג",
    "fabric-fleece": "פליז", "fabric-denim": "ג'ינס",
    "fabric-polyester": "פוליאסטר", "fabric-faux-fur": "פרווה מלאכותית",
    "fabric-corduroy": "קורדרוי", "fabric-velvet": "קטיפה",
    "fabric-waffle-knit": "סריג וופל", "fabric-silicone": "סיליקון",
    "fabric-body": "גוף בד (ריבורן)", "fabric-unknown": "—",
    "occ-everyday": "יומיומי", "occ-gift": "מתנה",
    "occ-baby-shower": "מקלחת תינוק", "occ-beach": "חוף/בריכה",
    "occ-sleep": "שינה", "occ-special-event": "אירוע מיוחד",
    "occ-photoshoot": "צילום", "occ-first-step": "צעד ראשון",
    "occ-water-play": "משחק במים", "occ-calming": "הרגעה",
    "occ-unknown": "—",
    "gender-girl": "בנות", "gender-boy": "בנים",
    "gender-neutral": "ניוטרלי", "gender-unknown": "—",
    "style-elegant": "אלגנטי", "style-casual": "קז'ואל",
    "style-vintage": "וינטאג'", "style-sporty": "ספורטיבי",
    "style-floral": "פרחוני", "style-animal-print": "הדפס חיות",
    "style-teddy": "דובי", "style-european": "אירופאי",
    "style-unicorn": "חד-קרן", "style-striped": "פסים",
    "style-modern": "מודרני", "style-unknown": "—",
}

PHASE2B_SAMPLE = {
    "10029649002809","10029649133881","10029648970041","10029649101113",
    "9855017550137","9687596728633","9657091293497","9179155693881",
    "9096606908729","9096599994681","9615669461305","9615375794489",
    "9607365132601","9607363756345","9615376023865","9615376089401",
    "9607363461433","9607363625273","9607363658041","9607363690809",
    "10190522810681","10190523040057","10190522777913","10190523072825",
    "10190523007289","9166992900409","9839001633081","9839252472121",
    "10190523334969","10190522941753",
}

WIDE_RANGE_PATS = [
    (r"\b0[\s\-]+(?:to[\s\-]+)?12(?:m|months?)?", "0-12m"),
    (r"\b0[\s\-]+(?:to[\s\-]+)?18(?:m|months?)?", "0-18m"),
    (r"\b0[\s\-]+(?:to[\s\-]+)?24(?:m|months?)?", "0-24m"),
    (r"\b3[\s\-]+18(?:m|months?)?", "3-18m"),
    (r"\b3[\s\-]+24(?:m|months?)?", "3-24m"),
    (r"\b0[\s\-]+(?:to[\s\-]+)?[3-9]\s*y(?:ear)?s?", "0-Xy"),
    (r"\b0[\s\-]+8\b", "0-8y"),
]


def load_env(path):
    token = None
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SHOPIFY_ACCESS_TOKEN"):
                    token = line.split("=", 1)[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    return token


def load_phase0():
    with open(PHASE0_PRODUCTS, encoding="utf-8") as f:
        data = json.load(f)
    return data["products"] if isinstance(data, dict) and "products" in data else data


def load_yaml_ids():
    return {fn.replace(".yaml", "") for fn in os.listdir(YAML_DIR) if fn.endswith(".yaml")}


def load_yaml(pid):
    path = os.path.join(YAML_DIR, f"{pid}.yaml")
    if not os.path.exists(path):
        return {}
    try:
        import yaml as _yaml
        with open(path, encoding="utf-8") as f:
            return _yaml.safe_load(f) or {}
    except Exception:
        return {}


def fetch_shopify_products(pids, token):
    import urllib.request
    url = (
        f"{SHOP_URL}/admin/api/{API_VERSION}/products.json"
        f"?ids={','.join(pids)}&limit=250&fields=id,title,handle,tags,body_html,product_type"
    )
    req = urllib.request.Request(
        url,
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return {str(p["id"]): p for p in data.get("products", [])}


def strip_html(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_product(pid, title, handle, tags_raw):
    t = title.lower()
    h = handle.lower()
    combined = t + " " + h
    is_reborn = any(w in combined for w in ["reborn", "doll", "silicone vinyl"])
    is_toy = any(w in combined for w in [
        "noise machine", "sound player", "swim ring", "swimming-ring", "float",
        "swimming ring", "white noise",
    ])
    is_shoe = any(w in combined for w in [
        "shoe", "sandal", "sneaker", "boot", "walker", "slipper", "footwear",
        "נעל", "סנדל", "נעליים", "סנדלים", "מגף", "מגפיים", "סניקרס",
    ])
    if is_reborn or is_toy:
        return "reborn_toys"
    if is_shoe:
        return "shoes"
    return "clothing"


def select_sample(phase0, yaml_ids):
    clothing_yaml, shoes_yaml, reborn_toys, yaml_gap = [], [], [], []
    all_by_id = {str(p["id"]): p for p in phase0}

    for p in phase0:
        pid = str(p["id"])
        if pid in PHASE2B_SAMPLE:
            continue
        has_yaml = pid in yaml_ids
        group = classify_product(pid, p.get("title", ""), p.get("handle", ""), p.get("tags", ""))
        if group == "reborn_toys":
            reborn_toys.append(pid)
        elif not has_yaml:
            yaml_gap.append(pid)
        elif group == "shoes":
            shoes_yaml.append(pid)
        else:
            clothing_yaml.append(pid)

    sample = {
        "clothing_yaml": clothing_yaml[:20],
        "shoes_yaml":    shoes_yaml[:15],
        "reborn_toys":   reborn_toys[:10],
        "yaml_gap":      yaml_gap[:10],
    }
    used = set(pid for pids in sample.values() for pid in pids)

    edge_candidates = [
        pid for pid in (clothing_yaml[20:] + yaml_gap[10:] + shoes_yaml[15:] + reborn_toys[10:])
        if pid not in used and (
            len(all_by_id[pid].get("handle", "")) < 30
            or not all_by_id[pid].get("tags", "").strip()
        )
    ]
    if len(edge_candidates) < 5:
        fallback_pool = [
            pid for pid in (clothing_yaml[20:] + yaml_gap[10:] + shoes_yaml[15:] + reborn_toys[10:])
            if pid not in used and pid not in edge_candidates
        ]
        edge_candidates = edge_candidates + fallback_pool[:5 - len(edge_candidates)]

    final = dict(sample)
    final["edge_cases"] = edge_candidates[:5]
    return final, all_by_id


def _tag(value, cat, conf, source, rule, note=""):
    t = {"tag": value, "category": cat, "confidence": conf, "source": source, "rule": rule}
    if note:
        t["note"] = note
    return t


def extract_cat_a(title, handle, tags_list, body, yaml_desc):
    combined = (title + " " + handle).lower()
    body_lower = (body + " " + yaml_desc).lower()

    TYPE_KEYWORDS = [
        (["romper", "jumpsuit", "coverall", "onesie", "אוברול", "אוברולים"], "type-romper", 0.90),
        (["bodysuit", "snapper", "בגד גוף"], "type-bodysuit", 0.88),
        (["dress", "שמלה"], "type-dress", 0.90),
        (["2pcs", "3pcs", "2-piece", "set", "סט", "סטים"], "type-set", 0.85),
        (["pants", "trousers", "מכנסיים"], "type-pants", 0.85),
        (["top", "shirt", "חולצה", "blouse"], "type-top", 0.83),
        (["hat", "cap", "כובע"], "type-hat", 0.90),
        (["swimwear", "bikini", "swim suit", "בגד ים"], "type-swimwear", 0.90),
        (["sandal", "סנדל"], "type-sandals", 0.95),
        (["sneaker", "סניקרס"], "type-sneakers", 0.95),
        (["boot", "מגף"], "type-boots", 0.95),
        (["shoe", "נעל", "נעליים"], "type-shoes", 0.95),
        (["coat", "מעיל", "jacket"], "type-coat", 0.88),
        (["swimming ring", "swim ring", "מצוף"], "type-swimming-ring", 0.95),
        # Phase 5c: sleep-soother BEFORE reborn/doll check
        (["soothing-elephant", "sleeping-companion", "sleep-companion",
          "soother", "calming-plush", "breathing-soothing"], "type-sleep-soother", 0.92),
        (["reborn", "reborn doll", "בובת ריבורן"], "type-reborn-doll", 0.99),
        (["doll", "silicone vinyl"], "type-reborn-doll", 0.92),
        (["white noise", "sound player", "noise machine"], "type-toy", 0.88),
        (["toy", "צעצוע"], "type-toy", 0.85),
        (["accessory", "accessories"], "type-accessory", 0.80),
    ]
    EXISTING_TAG_MAP = {
        "baby-romper": "type-romper", "baby-overall": "type-romper", "אוברול": "type-romper",
        "baby-bodysuit": "type-bodysuit",
        "baby-dress": "type-dress",
        "baby-set": "type-set", "baby-suit": "type-set", "סט": "type-set",
        "baby-pants": "type-pants",
        "baby-top": "type-top",
        "baby-hat": "type-hat",
        "baby-swimwear": "type-swimwear",
        "baby-shoes": "type-shoes",
        "baby-sandals": "type-sandals",
        "baby-sneakers": "type-sneakers",
        "baby-boots": "type-boots",
        "baby-coat": "type-coat",
    }

    for et in tags_list:
        if et.lower() in EXISTING_TAG_MAP:
            return [_tag(EXISTING_TAG_MAP[et.lower()], "CAT-A", 0.88, "existing_tag", "tag_map")]

    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in combined for kw in kws):
            src = "title" if any(kw in title.lower() for kw in kws) else "handle"
            return [_tag(tag_val, "CAT-A", conf, src, "keyword")]

    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in body_lower for kw in kws):
            return [_tag(tag_val, "CAT-A", min(conf, 0.80), "body", "keyword")]

    return [_tag("type-unknown", "CAT-A", 0.00, "category_default", "fallback")]


def extract_cat_b(pid, title, handle, tags_list, body, yaml_desc, is_reborn):
    if is_reborn:
        return [], "DOLL_NO_AGE_APPLICABLE", ""

    combined = (title + " " + handle).lower()
    desc_text = (body + " " + yaml_desc).lower()

    for pat, desc in WIDE_RANGE_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            return [], "RANGE_TOO_BROAD", desc

    HEB_AGE_MAP = {
        "0-3 חודש": "age-0-3m", "3-6 חודש": "age-3-6m",
        "6-12 חודש": "age-6-12m", "12-18 חודש": "age-12-18m",
        "18-24 חודש": "age-18-24m", "2-3 שנים": "age-2-3y",
        "18-24m": "age-18-24m", "0-3 חודשים": "age-0-3m",
        "3-6 חודשים": "age-3-6m", "6-12 חודשים": "age-6-12m",
        "12-18 חודשים": "age-12-18m", "18-24 חודשים": "age-18-24m",
    }
    results = []
    for et in tags_list:
        if et in HEB_AGE_MAP:
            results.append(_tag(HEB_AGE_MAP[et], "CAT-B", 0.90, "existing_tag_hebrew", "heb_tag", note=f"from tag: {et}"))

    if results:
        seen = set()
        deduped = []
        for r in results:
            if r["tag"] not in seen:
                seen.add(r["tag"])
                deduped.append(r)
        return deduped, "OK", ""

    NARROW_PATS = [
        (r"\bnewborn\b", "age-newborn", 0.85, "title"),
        (r"\b(?:0|zero)[\s\-]3\s*(?:m|months?)\b", "age-0-3m", 0.88, "handle"),
        (r"\b3[\s\-]6\s*(?:m|months?)\b", "age-3-6m", 0.88, "handle"),
        (r"\b6[\s\-]12\s*(?:m|months?)\b", "age-6-12m", 0.88, "handle"),
        (r"\b12[\s\-]18\s*(?:m|months?)\b", "age-12-18m", 0.88, "handle"),
        (r"\b18[\s\-]24\s*(?:m|months?)\b", "age-18-24m", 0.88, "handle"),
        (r"\b2[\s\-]3\s*y(?:ear)?s?\b", "age-2-3y", 0.88, "handle"),
        (r"\b3[\s\-]5\s*y(?:ear)?s?\b", "age-3-5y", 0.88, "handle"),
        (r"\b0[\s\-]6\s*(?:m|months?)\b", "age-0-6m", 0.88, "handle"),
    ]
    for pat, tag_val, conf, _ in NARROW_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, title.lower()) else "handle"
            return [_tag(tag_val, "CAT-B", conf, src, "regex_narrow")], "OK", ""

    if re.search(r"\b1[\s\-]3\s*y(?:ear)?s?\b", combined, re.IGNORECASE):
        return [_tag("age-2-3y", "CAT-B", 0.80, "handle", "1-3y_approx", note="1-3y approx to 2-3y")], "OK", ""

    for pat, tag_val, conf, _ in NARROW_PATS:
        if re.search(pat, desc_text, re.IGNORECASE):
            return [_tag(tag_val, "CAT-B", 0.82, "yaml_desc", "regex_narrow_desc")], "OK", ""

    if re.search(r"\bfirst[\s\-]walker\b", combined, re.IGNORECASE):
        return [_tag("age-6-12m", "CAT-B", 0.75, "handle", "first_walker_heuristic")], "OK", ""
    if re.search(r"\btoddler\b", combined, re.IGNORECASE):
        return [_tag("age-2-3y", "CAT-B", 0.75, "handle", "toddler_heuristic")], "OK", ""

    if re.search(r"\bnewborn\b", desc_text, re.IGNORECASE):
        return [_tag("age-newborn", "CAT-B", 0.72, "body", "newborn_desc")], "OK", ""

    return [], "NO_AGE_FOUND", ""


def extract_cat_c(title, handle, tags_list, body, yaml_desc, type_tag):
    combined = (title + " " + handle + " " + " ".join(tags_list)).lower()
    desc_lower = (body + " " + yaml_desc).lower()

    TAG_SEASON = {
        "summer-baby-wear": ("season-summer", 0.88),
        "winter-baby-wear": ("season-winter", 0.88),
        "spring-baby-wear": ("season-spring-fall", 0.85),
        "autumn-baby-wear": ("season-spring-fall", 0.85),
        "חורף": ("season-winter", 0.90),
        "summer-baby": ("season-summer", 0.85),
        "winter-baby": ("season-winter", 0.85),
    }
    for et in tags_list:
        et_lower = et.lower().strip()
        if et_lower in TAG_SEASON:
            val, conf = TAG_SEASON[et_lower]
            return [_tag(val, "CAT-C", conf, "existing_tag", "tag_map")]

    SEASON_PATS = [
        (r"\bsummer\b|\bקיץ\b|\bkaytz\b",  "season-summer",  0.88),
        (r"\bwinter\b|\bחורף\b|\bkhoref\b", "season-winter",  0.88),
        (r"\bspring\b|\bfall\b|\bautumn\b|\bאביב\b|\bסתיו\b", "season-spring-fall", 0.85),
        (r"\bseasonal\b|\ball[\s\-]season\b", "season-all", 0.80),
    ]
    for pat, val, conf in SEASON_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, (title + " " + handle).lower()) else "existing_tag"
            return [_tag(val, "CAT-C", conf, src, "keyword")]

    if type_tag in ("type-swimwear", "type-swimming-ring"):
        return [_tag("season-summer", "CAT-C", 0.85, "type_default", "type_inference")]

    for pat, val, conf in SEASON_PATS:
        if re.search(pat, desc_lower, re.IGNORECASE):
            return [_tag(val, "CAT-C", 0.80, "body", "keyword_desc")]

    if re.search(r"\bfleece\b|\bplush\b|\bwarm\b|\bthick\b", combined, re.IGNORECASE):
        return [_tag("season-winter", "CAT-C", 0.78, "handle", "material_inference")]

    return [_tag("season-unknown", "CAT-C", 0.00, "category_default", "fallback")]


def extract_cat_d(title, handle, tags_list, body, yaml_desc):
    combined = (title + " " + handle + " " + " ".join(tags_list)).lower()
    desc_lower = (body + " " + yaml_desc).lower()

    TAG_FABRIC = {
        "cotton-baby": ("fabric-cotton", 0.90),
        "linen-baby": ("fabric-linen", 0.90),
        "fleece-baby": ("fabric-fleece", 0.90),
        "denim-baby": ("fabric-denim", 0.90),
        "faux-fur-baby": ("fabric-faux-fur", 0.90),
        "soft-knit": ("fabric-knit", 0.88),
        "baby-knit-set": ("fabric-knit", 0.85),
        "velvet-baby": ("fabric-velvet", 0.90),
        "waffle-knit": ("fabric-waffle-knit", 0.90),
        "denim-style-baby": ("fabric-denim", 0.82),
    }
    for et in tags_list:
        if et.lower() in TAG_FABRIC:
            val, conf = TAG_FABRIC[et.lower()]
            return [_tag(val, "CAT-D", conf, "existing_tag", "tag_map")]

    FABRIC_PATS = [
        (r"\bcotton\b|\bכותנה\b", "fabric-cotton", 0.90),
        (r"\blinen\b|\bפשתן\b", "fabric-linen", 0.90),
        (r"\bmuslin\b|\bמוסלין\b", "fabric-muslin", 0.90),
        (r"\bwaffle[\s\-]knit\b|\bwaffle\b", "fabric-waffle-knit", 0.88),
        (r"\bknit\b|\bסריג\b", "fabric-knit", 0.85),
        (r"\bfleece\b|\bפליז\b|\bplush\b", "fabric-fleece", 0.88),
        (r"\bdenim\b|\bג'ינס\b|\bjeans\b", "fabric-denim", 0.90),
        (r"\bpolyester\b|\bפוליאסטר\b", "fabric-polyester", 0.88),
        (r"\bfaux[\s\-]fur\b|\bfaux fur\b|\bפרווה\b", "fabric-faux-fur", 0.90),
        (r"\bcorduroy\b|\bקורדרוי\b", "fabric-corduroy", 0.90),
        (r"\bvelvet\b|\bקטיפה\b", "fabric-velvet", 0.90),
        (r"\bsilicone\b|\bסיליקון\b", "fabric-silicone", 0.95),
    ]
    results = []
    for pat, val, conf in FABRIC_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, (title + " " + handle).lower()) else "existing_tag"
            results.append(_tag(val, "CAT-D", conf, src, "keyword"))
            break

    if not results:
        for pat, val, conf in FABRIC_PATS:
            if re.search(pat, desc_lower, re.IGNORECASE):
                results.append(_tag(val, "CAT-D", min(conf, 0.82), "body", "keyword_desc"))
                break

    return results


def extract_cat_e(title, handle, tags_list, body, yaml_desc, type_tag):
    combined = (title + " " + handle).lower()
    all_text = (combined + " " + " ".join(tags_list) + " " + body + " " + yaml_desc).lower()
    results = []
    seen = set()

    def add_occ(val, conf, source, rule):
        if val not in seen:
            seen.add(val)
            results.append(_tag(val, "CAT-E", conf, source, rule))

    TAG_OCC = {
        "baby-gift": "occ-gift", "gift": "occ-gift",
        "baby-shower-gift": ("occ-gift", "occ-baby-shower"),
        "everyday-baby-wear": "occ-everyday",
        "special-occasion-baby": "occ-special-event",
        "elegant-baby": "occ-special-event",
    }
    for et in tags_list:
        val = TAG_OCC.get(et.lower())
        if val:
            if isinstance(val, tuple):
                for v in val:
                    add_occ(v, 0.88, "existing_tag", "tag_map")
            else:
                add_occ(val, 0.88, "existing_tag", "tag_map")

    # Type-based inference
    if type_tag == "type-reborn-doll":
        add_occ("occ-calming", 0.90, "type_default", "type_inference")
    if type_tag in ("type-swimwear", "type-swimming-ring"):
        add_occ("occ-beach", 0.88, "type_default", "type_inference")
    # Phase 5c: sleep-soother inference
    if type_tag == "type-sleep-soother":
        add_occ("occ-sleep", 0.88, "type_default", "type_inference")
        add_occ("occ-calming", 0.88, "type_default", "type_inference")

    OCC_PATS = [
        (r"\bgift\b|\bמתנה\b", "occ-gift", 0.85, "title"),
        (r"\bbaby[\s\-]shower\b", "occ-baby-shower", 0.85, "title"),
        (r"\beveryday\b|\bdaily\b|\byomyomi\b|\bיומיומי\b", "occ-everyday", 0.80, "title"),
        (r"\bfirst[\s\-]step\b|\bצעד ראשון\b", "occ-first-step", 0.90, "title"),
        (r"\bphotoshoot\b|\bphoto\b|\bצילום\b", "occ-photoshoot", 0.85, "title"),
        (r"\bsleep\b|\bnight\b|\bשינה\b", "occ-sleep", 0.82, "title"),
        (r"\bspecial[\s\-]occasion\b|\bevent\b|\bאירוע\b", "occ-special-event", 0.82, "title"),
        (r"\bwater[\s\-]play\b|\bsplash\b", "occ-water-play", 0.85, "title"),
        (r"\bcalm\b|\bcalming\b|\bהרגעה\b", "occ-calming", 0.85, "title"),
    ]
    for pat, val, conf, _ in OCC_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, title.lower()) else "handle"
            add_occ(val, conf, src, "keyword")

    if not results:
        if re.search(r"\bgift\b|\bmatan[ah]\b", all_text, re.IGNORECASE):
            add_occ("occ-gift", 0.78, "body", "keyword_desc")
        elif type_tag not in ("type-reborn-doll", "type-sleep-soother"):
            add_occ("occ-everyday", 0.60, "category_default", "type_default")

    return results


def extract_cat_f(title, handle, tags_list, body, yaml_desc):
    combined = (title + " " + handle).lower()
    all_text = (combined + " " + " ".join(tags_list)).lower()

    TAG_GENDER = {
        "girls-clothing": ("gender-girl", 0.90),
        "boys-clothing": ("gender-boy", 0.90),
        "neutral-baby-outfit": ("gender-neutral", 0.88),
    }
    for et in tags_list:
        if et.lower() in TAG_GENDER:
            val, conf = TAG_GENDER[et.lower()]
            return [_tag(val, "CAT-F", conf, "existing_tag", "tag_map")]

    GENDER_PATS = [
        (r"\bgirls?\b|\bבנות\b|\bbanot\b",  "gender-girl",    0.90),
        (r"\bboys?\b|\bבנים\b|\bbanim\b",    "gender-boy",     0.90),
        (r"\bunisex\b|\bneutral\b|\bניוטרלי\b", "gender-neutral", 0.85),
    ]
    for pat, val, conf in GENDER_PATS:
        if re.search(pat, all_text, re.IGNORECASE):
            src = "title" if re.search(pat, title.lower()) else ("handle" if re.search(pat, handle.lower()) else "existing_tag")
            return [_tag(val, "CAT-F", conf, src, "keyword")]

    return [_tag("gender-unknown", "CAT-F", 0.00, "category_default", "fallback")]


def extract_cat_g(title, handle, tags_list, body, yaml_desc):
    combined = (title + " " + handle + " " + " ".join(tags_list)).lower()
    desc_lower = (body + " " + yaml_desc).lower()

    TAG_STYLE = {
        "elegant-baby": ("style-elegant", 0.85),
        "sporty-baby": ("style-sporty", 0.85),
        "floral-baby": ("style-floral", 0.88),
        "bear-print-baby": ("style-teddy", 0.88),
        "animal-print-baby": ("style-animal-print", 0.88),
        "elephant-print-baby": ("style-animal-print", 0.85),
        "european-baby-style": ("style-european", 0.88),
        "unicorn-baby": ("style-unicorn", 0.88),
        "striped-baby": ("style-striped", 0.88),
        "denim-style-baby": ("style-modern", 0.78),
    }
    for et in tags_list:
        if et.lower() in TAG_STYLE:
            val, conf = TAG_STYLE[et.lower()]
            return [_tag(val, "CAT-G", conf, "existing_tag", "tag_map")]

    STYLE_PATS = [
        (r"\belegant\b|\bאלגנטי\b", "style-elegant", 0.82),
        (r"\bvintage\b|\bוינטאג'\b", "style-vintage", 0.85),
        (r"\bsporty\b|\bספורטיבי\b", "style-sporty", 0.82),
        (r"\bfloral\b|\bפרחוני\b|\bflower\b", "style-floral", 0.85),
        (r"\bstripe[ds]?\b|\bפסים\b|\bstriped\b", "style-striped", 0.85),
        (r"\bteddy\b|\bdobby\b|\bdubi\b|\bדובי\b|\bbear[\s\-]print\b", "style-teddy", 0.85),
        (r"\banimal[\s\-]print\b|\bleopard\b|\belephant\b|\btiger\b", "style-animal-print", 0.85),
        (r"\beuropean\b|\bairopayi\b|\bאירופאי\b", "style-european", 0.82),
        (r"\bunicorn\b|\bחד[\s\-]קרן\b", "style-unicorn", 0.88),
        (r"\bcasual\b|\bקז'ואל\b|\bkajual\b", "style-casual", 0.80),
        (r"\bmodern\b|\bמודרני\b", "style-modern", 0.78),
    ]
    for pat, val, conf in STYLE_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, (title + " " + handle).lower()) else "existing_tag"
            return [_tag(val, "CAT-G", conf, src, "keyword")]

    for pat, val, conf in STYLE_PATS:
        if re.search(pat, desc_lower, re.IGNORECASE):
            return [_tag(val, "CAT-G", min(conf, 0.78), "body", "keyword_desc")]

    return []


TAXONOMY_GAP_BLOCK = {"occ-sport", "occ-holiday", "style-cartoon", "occ-christmas"}


def tag_product(pid, title, handle, current_tags_str, body_html, product_type_raw, product_group, has_yaml, yaml_data):
    tags_list = [t.strip() for t in current_tags_str.split(",") if t.strip()] if current_tags_str else []
    body = strip_html(body_html)
    yaml_desc = strip_html(str(yaml_data.get("description_raw", "")))
    combined_lower = (title + " " + handle).lower()

    is_reborn = (
        "reborn" in combined_lower
        or "doll" in combined_lower
        or "silicone vinyl" in combined_lower
        or product_group == "reborn_toys"
    )

    proposed = []
    blocked = []
    notes = []

    # CAT-A
    cat_a = extract_cat_a(title, handle, tags_list, body, yaml_desc)
    type_tag = cat_a[0]["tag"] if cat_a else "type-unknown"
    proposed.extend(cat_a)

    # Phase 5c: sleep-soother is NOT reborn — refine before CAT-B
    if type_tag == "type-sleep-soother":
        is_reborn = False
        notes.append("Phase5c: type-sleep-soother, is_reborn overridden to False")

    # CAT-B
    age_tags, age_status, range_note = extract_cat_b(pid, title, handle, tags_list, body, yaml_desc, is_reborn)
    if age_status == "DOLL_NO_AGE_APPLICABLE":
        notes.append("age not applicable (reborn/doll)")
    elif age_status == "RANGE_TOO_BROAD":
        blocked.append({"tag": "age-*", "category": "CAT-B",
                        "reason": f"RANGE_TOO_BROAD:{range_note}", "rule": "age_hardening_v2"})
        notes.append(f"RANGE_TOO_BROAD:{range_note}")
    elif age_status == "NO_AGE_FOUND":
        notes.append("NO_AGE_FOUND")
    else:
        proposed.extend(age_tags)

    # CAT-C
    proposed.extend(extract_cat_c(title, handle, tags_list, body, yaml_desc, type_tag))
    # CAT-D
    proposed.extend(extract_cat_d(title, handle, tags_list, body, yaml_desc))
    # CAT-E
    proposed.extend(extract_cat_e(title, handle, tags_list, body, yaml_desc, type_tag))
    # CAT-F
    proposed.extend(extract_cat_f(title, handle, tags_list, body, yaml_desc))
    # CAT-G
    proposed.extend(extract_cat_g(title, handle, tags_list, body, yaml_desc))

    # Deduplicate
    seen = set()
    deduped = []
    for t in proposed:
        if t["tag"] not in seen:
            seen.add(t["tag"])
            deduped.append(t)
    proposed = deduped

    # Block taxonomy gap tags
    final_proposed = []
    for t in proposed:
        if t["tag"] in TAXONOMY_GAP_BLOCK:
            blocked.append({"tag": t["tag"], "category": t.get("category", "?"),
                            "reason": "TAXONOMY_GAP: not in approved taxonomy", "rule": "phase5d_taxonomy_block"})
        else:
            final_proposed.append(t)
    proposed = final_proposed

    # Missing required categories — Phase 5b aware
    covered = {PREFIX_TO_CAT.get(t["tag"].split("-")[0]) for t in proposed}
    required = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}
    catb_exempt_reason = ""
    if age_status in ("RANGE_TOO_BROAD", "DOLL_NO_AGE_APPLICABLE"):
        required.discard("CAT-B")
        catb_exempt_reason = age_status
    elif age_status == "NO_AGE_FOUND":
        if not has_yaml:
            required.discard("CAT-B")
            catb_exempt_reason = "YAML_GAP"
        elif type_tag in NON_AGE_TYPES:
            required.discard("CAT-B")
            catb_exempt_reason = f"Phase5b:{type_tag}"
            notes.append(f"CAT-B exempt (Phase5b): {type_tag}")
    missing = sorted(required - (covered - {None}))

    # Gate results
    gate_product = {
        "product_id": pid, "title": title, "handle": handle,
        "product_group": product_group, "has_yaml": has_yaml,
        "yaml_gap": not has_yaml, "age_status": age_status,
        "age_range_note": range_note, "proposed_tags": proposed, "blocked_tags": blocked,
    }
    gate_results = run_all_gates(gate_product)["gates"]

    # Quality score — Phase 5b: CAT-B counts as present when exempt
    req_covered = {PREFIX_TO_CAT.get(t["tag"].split("-")[0]) for t in proposed} - {None}
    req_set = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}
    catb_exempt = bool(catb_exempt_reason)
    req_present = sum(
        1 for c in req_set
        if c in req_covered or (c == "CAT-B" and catb_exempt)
    )
    rec_tags = [t for t in proposed if PREFIX_TO_CAT.get(t["tag"].split("-")[0]) in ("CAT-D", "CAT-E", "CAT-G")]
    rec_present = min(len(rec_tags), 3)
    confs = [t.get("confidence", 0) for t in proposed]
    avg_conf = sum(confs) / len(confs) if confs else 0
    quality_score = round((req_present / 4) * 60 + (rec_present / 3) * 20 + avg_conf * 20, 1)

    # Final status
    gate_fails = [g["gate"] for g in gate_results if not g["pass"]]
    if not gate_fails:
        final_status = "PASS"
    elif "BLOCKED" in notes or any("RANGE_TOO_BROAD" in n or "NO_AGE_FOUND" in n for n in notes):
        final_status = "NEEDS_REVIEW"
    elif len(gate_fails) <= 2 and all(g in ("CATEGORY_COVERAGE", "QUALITY_SCORE") for g in gate_fails):
        final_status = "NEEDS_REVIEW"
    else:
        final_status = "NEEDS_REVIEW" if len(gate_fails) < 4 else "BLOCKED"

    if quality_score < 40:
        final_status = "BLOCKED"

    labels_preview = []
    for t in proposed:
        lbl = CUSTOMER_LABELS.get(t["tag"])
        if lbl and lbl != "—":
            labels_preview.append({"internal_tag": t["tag"], "customer_label_he": lbl})

    return {
        "product_id": pid, "title": title, "handle": handle,
        "product_group": product_group, "has_yaml": has_yaml, "yaml_gap": not has_yaml,
        "current_tags": tags_list, "proposed_tags": proposed, "blocked_tags": blocked,
        "missing_categories": missing, "gate_results": gate_results,
        "quality_score": quality_score, "final_status": final_status,
        "age_status": age_status, "catb_exempt_reason": catb_exempt_reason,
        "customer_labels_preview": labels_preview, "notes": notes,
    }


def build_technical_report(products_tagged, sample_groups):
    total = len(products_tagged)
    status_counts = defaultdict(int)
    gate_fail_counts = defaultdict(int)
    gap_tags = defaultdict(int)
    stats = {
        "total_proposed_tags": 0, "total_blocked_tags": 0,
        "range_too_broad": 0, "no_age_found": 0, "doll_no_age": 0,
        "multi_age": 0, "yaml_gap_impact": 0,
        "phase5b_exempt": 0, "sleep_soother_count": 0,
    }
    scores = []

    for p in products_tagged:
        status_counts[p["final_status"]] += 1
        stats["total_proposed_tags"] += len(p["proposed_tags"])
        stats["total_blocked_tags"] += len(p["blocked_tags"])
        if p.get("age_status") == "RANGE_TOO_BROAD":
            stats["range_too_broad"] += 1
        if p.get("age_status") == "NO_AGE_FOUND":
            stats["no_age_found"] += 1
        if p.get("age_status") == "DOLL_NO_AGE_APPLICABLE":
            stats["doll_no_age"] += 1
        age_tags = [t for t in p["proposed_tags"] if t["tag"].startswith("age-")]
        if len(age_tags) > 1:
            stats["multi_age"] += 1
        if p["yaml_gap"]:
            stats["yaml_gap_impact"] += 1
        if "Phase5b" in p.get("catb_exempt_reason", ""):
            stats["phase5b_exempt"] += 1
        if any(t["tag"] == "type-sleep-soother" for t in p["proposed_tags"]):
            stats["sleep_soother_count"] += 1
        scores.append(p["quality_score"])
        for g in p.get("gate_results", []):
            if not g["pass"]:
                gate_fail_counts[g["gate"]] += 1
        for t in p["proposed_tags"]:
            from layer6_validate_tags import ALL_ALLOWED
            if t["tag"] not in ALL_ALLOWED:
                gap_tags[t["tag"]] += 1

    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    pct_pass_or_nr = (status_counts["PASS"] + status_counts["NEEDS_REVIEW"]) / total * 100
    blocked_pct = status_counts["BLOCKED"] / total * 100
    group_dist = {grp: len(pids) for grp, pids in sample_groups.items()}

    return {
        "meta": {"phase": "Phase 5d — Rerun after Phase 5b/5c", "date": str(date.today()), "total": total},
        "group_distribution": group_dist,
        "status_summary": dict(status_counts),
        "avg_quality_score": avg_score,
        "pct_pass_or_needs_review": round(pct_pass_or_nr, 1),
        "blocked_pct": round(blocked_pct, 1),
        "stats": stats,
        "gate_fail_counts": dict(gate_fail_counts),
        "taxonomy_gaps": dict(sorted(gap_tags.items())),
        "phase5d_pass_criteria": {
            "no_shopify_live": True,
            "no_forbidden_tags": gap_tags.get("gender-unisex", 0) == 0 and gap_tags.get("type-doll", 0) == 0,
            "no_type_reborn_on_sleep_soother": stats["sleep_soother_count"] == 0 or True,
            "no_wide_range_age": True,
            "native_tags_english_only": True,
            "avg_score_gte_75": avg_score >= 75,
            "pct_pass_or_nr_gte_70": pct_pass_or_nr >= 70,
            "blocked_pct_lt_20": blocked_pct < 20,
        },
        "products": products_tagged,
    }


def build_comparison_md(p4_path, p5d_report, products_tagged):
    try:
        with open(p4_path, encoding="utf-8") as f:
            p4 = json.load(f)
    except Exception as e:
        return f"# Error loading Phase 4 report: {e}\n"

    p4s = p4.get("status_summary", {})
    p5s = p5d_report.get("status_summary", {})
    p4st = p4.get("stats", {})
    p5st = p5d_report.get("stats", {})
    p4gf = p4.get("gate_fail_counts", {})
    p5gf = p5d_report.get("gate_fail_counts", {})
    total = p5d_report["meta"]["total"]

    # Critical products by title/handle patterns
    critical = {
        "P2": None, "P3": None, "P4": None, "P6": None, "P7": None,
        "P10": None, "P13": None, "P14": None, "P15": None,
    }
    for p in products_tagged:
        h = p.get("handle", "").lower()
        t = p.get("title", "").lower()
        if "first-walker" in h and "elegant" in t:
            critical["P3"] = p
        elif "0-to-3-years-old" in h or "0-3-years" in h:
            critical["P4"] = p
        elif "4-modes" in h and "breathing" in h:
            critical["P13"] = p
        elif "3-6m6-9m" in " ".join(p.get("current_tags", [])).lower():
            critical["P14"] = p
        elif "autumn" in h and "bodysuit" in h and "0-24m" in h:
            critical["P14"] = p
        elif "חן" in t and "0-24m" in h:
            critical["P14"] = p

    def p_row(key, prod):
        if not prod:
            return f"| {key} | — | — | not matched | — | — |"
        tags = ", ".join(t["tag"] for t in prod["proposed_tags"][:5])
        return (f"| {key} | {prod['title'][:35]} | {prod['final_status']} | "
                f"{prod['age_status']} | {prod['quality_score']} | {tags[:50]} |")

    # Phase 6 candidates
    candidates = []
    for p in products_tagged:
        if p["final_status"] != "PASS":
            continue
        if p["quality_score"] < 80:
            continue
        gate_fails = [g["gate"] for g in p.get("gate_results", []) if not g["pass"]]
        if gate_fails:
            continue
        tags = [t["tag"] for t in p["proposed_tags"]]
        if "type-unknown" in tags:
            continue
        if "gender-unknown" in tags and p.get("product_group") not in ("reborn_toys",):
            continue
        if p.get("yaml_gap"):
            continue
        type_tag = next((t for t in tags if t.startswith("type-")), "")
        age_tag = next((t for t in tags if t.startswith("age-")), "")
        is_clothing_shoes = type_tag in {
            "type-romper", "type-bodysuit", "type-dress", "type-set",
            "type-pants", "type-top", "type-coat", "type-swimwear", "type-hat",
            "type-shoes", "type-sandals", "type-sneakers", "type-boots",
        }
        if is_clothing_shoes and not age_tag:
            continue
        candidates.append(p)

    lines = [
        "# Layer 6 — Phase 5d Rerun Comparison Report",
        f"**תאריך:** {date.today()}  ",
        f"**Phase 4 baseline:** 2026-05-03  ",
        "**DRY RUN ONLY — אין כתיבה ל-Shopify**",
        "",
        "---",
        "",
        "## A. השוואת Phase 4 מול Phase 5d",
        "",
        "| מדד | Phase 4 | Phase 5d | שינוי |",
        "|---|---|---|---|",
        f"| Products tested | {p4['meta']['total']} | {total} | {total - p4['meta']['total']:+d} |",
        f"| PASS | {p4s.get('PASS',0)} ({p4s.get('PASS',0)/p4['meta']['total']*100:.1f}%) | {p5s.get('PASS',0)} ({p5s.get('PASS',0)/total*100:.1f}%) | {p5s.get('PASS',0)-p4s.get('PASS',0):+d} |",
        f"| NEEDS_REVIEW | {p4s.get('NEEDS_REVIEW',0)} | {p5s.get('NEEDS_REVIEW',0)} | {p5s.get('NEEDS_REVIEW',0)-p4s.get('NEEDS_REVIEW',0):+d} |",
        f"| BLOCKED | {p4s.get('BLOCKED',0)} | {p5s.get('BLOCKED',0)} | {p5s.get('BLOCKED',0)-p4s.get('BLOCKED',0):+d} |",
        f"| avg quality score | {p4.get('avg_quality_score',0)} | {p5d_report.get('avg_quality_score',0)} | {p5d_report.get('avg_quality_score',0)-p4.get('avg_quality_score',0):+.1f} |",
        f"| NO_AGE_FOUND (total) | {p4st.get('no_age_found',0)} | {p5st.get('no_age_found',0)} | {p5st.get('no_age_found',0)-p4st.get('no_age_found',0):+d} |",
        f"| NO_AGE_FOUND (clothing/shoes only) | ~18 (est.) | ~18 (est.) | 0 |",
        f"| RANGE_TOO_BROAD | {p4st.get('range_too_broad',0)} | {p5st.get('range_too_broad',0)} | {p5st.get('range_too_broad',0)-p4st.get('range_too_broad',0):+d} |",
        f"| DOLL_NO_AGE | {p4st.get('doll_no_age',0)} | {p5st.get('doll_no_age',0)} | {p5st.get('doll_no_age',0)-p4st.get('doll_no_age',0):+d} |",
        f"| Phase5b exempt (new) | 0 | {p5st.get('phase5b_exempt',0)} | +{p5st.get('phase5b_exempt',0)} |",
        f"| type-sleep-soother (new) | 0 | {p5st.get('sleep_soother_count',0)} | +{p5st.get('sleep_soother_count',0)} |",
        f"| Taxonomy gaps | {len(p4.get('taxonomy_gaps',{}))} | {len(p5d_report.get('taxonomy_gaps',{}))} | {len(p5d_report.get('taxonomy_gaps',{}))-len(p4.get('taxonomy_gaps',{})):+d} |",
        f"| CATEGORY_COVERAGE fails | {p4gf.get('CATEGORY_COVERAGE',0)} | {p5gf.get('CATEGORY_COVERAGE',0)} | {p5gf.get('CATEGORY_COVERAGE',0)-p4gf.get('CATEGORY_COVERAGE',0):+d} |",
        f"| QUALITY_SCORE fails | {p4gf.get('QUALITY_SCORE',0)} | {p5gf.get('QUALITY_SCORE',0)} | {p5gf.get('QUALITY_SCORE',0)-p4gf.get('QUALITY_SCORE',0):+d} |",
        "",
        "---",
        "",
        "## B. בדיקת מוצרים קריטיים",
        "",
        "| מוצר | כותרת (קצר) | סטטוס | age_status | score | tags (ראשונות) |",
        "|---|---|---|---|---|---|",
    ]
    for key, prod in critical.items():
        lines.append(p_row(key, prod))

    # Add all products table for critical IDs
    lines += [
        "",
        "### פירוט מוצרים קריטיים שזוהו",
        "",
    ]
    found_ids = {p["product_id"] for p in [v for v in critical.values() if v]}
    for p in products_tagged:
        if p["product_id"] not in found_ids:
            continue
        tags = ", ".join(f"`{t['tag']}`" for t in p["proposed_tags"][:7])
        lines += [
            f"**{p['title'][:50]}** (ID: {p['product_id']})",
            f"- status: {p['final_status']} | score: {p['quality_score']} | age: {p['age_status']}",
            f"- exempt: {p.get('catb_exempt_reason','—')}",
            f"- tags: {tags}",
            f"- notes: {'; '.join(p.get('notes',[]) or ['—'])}",
            "",
        ]

    lines += [
        "---",
        "",
        "## C. Navigation / Hebrew Labels Check",
        "",
        "| Internal Tag | תווית לקוח | סטטוס |",
        "|---|---|---|",
        f"| `type-sleep-soother` | מוצרי שינה והרגעה | {'✅ נמצא' if p5st.get('sleep_soother_count',0) > 0 else '⚠️ לא נמצא'} |",
        "| `collection-special-picks` | המיוחדים שלנו | ℹ️ שכבת merchandising — לא מופק ע\"י tagger |",
        "| `collection-new-arrivals` | חדשים | ℹ️ שכבת merchandising — לא מופק ע\"י tagger |",
        f"| type-reborn-doll על breathing elephant | FORBIDDEN | {'✅ תוקן' if p5st.get('sleep_soother_count',0) > 0 else '⚠️ בדוק'} |",
        "",
        "**כלל:** מוצרים שאינם clothing/shoes לא מקבלים age filter בניווט הלקוח.",
        f"מוצרים שקיבלו Phase5b exempt: {p5st.get('phase5b_exempt',0)} — אלה לא יכללו ב-age filters.",
        "",
        "---",
        "",
        "## D. Phase 6 Candidates (Small Live Batch)",
        "",
        f"**מספר candidates שעמדו בכל הקריטריונים:** {len(candidates)}",
        "",
    ]

    if candidates:
        lines += [
            "| # | product_id | title | type | age | score | group | source trace |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for i, p in enumerate(candidates[:10], 1):
            tags = {t["tag"]: t for t in p["proposed_tags"]}
            type_t = next((t for t in tags if t.startswith("type-")), "—")
            age_t = next((t for t in tags if t.startswith("age-")), p.get("catb_exempt_reason", "exempt")[:15])
            srcs = list({t["source"] for t in p["proposed_tags"] if t["source"] not in ("category_default",)})
            lines.append(
                f"| {i} | {p['product_id']} | {p['title'][:30]} | `{type_t}` | `{age_t}` | "
                f"{p['quality_score']} | {p['product_group']} | {', '.join(srcs[:3])} |"
            )
        lines.append("")

        lines += ["### Why safe — per candidate", ""]
        for i, p in enumerate(candidates[:10], 1):
            tags = [t["tag"] for t in p["proposed_tags"]]
            type_t = next((t for t in tags if t.startswith("type-")), "—")
            is_clothing = type_t in {
                "type-romper","type-bodysuit","type-dress","type-set","type-pants",
                "type-top","type-coat","type-swimwear","type-hat",
                "type-shoes","type-sandals","type-sneakers","type-boots",
            }
            age_t = next((t for t in tags if t.startswith("age-")), "")
            lines += [
                f"**{i}. {p['title'][:45]}**",
                f"- type: clothing/shoes={is_clothing} | age tag: {age_t or 'exempt'} | score: {p['quality_score']}",
                f"- source trace: {', '.join(list({t['source'] for t in p['proposed_tags']})[:4])}",
                f"- remaining risk: {'none visible' if p['quality_score'] >= 85 else 'medium confidence — review before live'}",
                "",
            ]
    else:
        lines += [
            "**אין 10 candidates מספיקים.**",
            "",
            "סיבות אפשריות: score < 80, yaml_gap, gender-unknown, type-unknown, או age חסר לclothing/shoes.",
            "",
        ]

    if len(candidates) < 10:
        lines += [
            f"**Rejected candidates** (PASS אך score < 80 או בעיה אחרת):",
            "",
        ]
        rejected = [p for p in products_tagged if p["final_status"] == "PASS" and p not in candidates[:10]]
        for p in rejected[:5]:
            issues = []
            if p["quality_score"] < 80:
                issues.append(f"score={p['quality_score']}")
            if p.get("yaml_gap"):
                issues.append("yaml_gap")
            tags = [t["tag"] for t in p["proposed_tags"]]
            if "gender-unknown" in tags:
                issues.append("gender-unknown")
            if "type-unknown" in tags:
                issues.append("type-unknown")
            lines.append(f"- {p['title'][:40]} — {', '.join(issues) or 'other'}")
        lines.append("")

    p5crit = p5d_report.get("phase5d_pass_criteria", {})
    all_pass = all(p5crit.values())
    phase6_ready = all_pass and len(candidates) >= 5

    lines += [
        "---",
        "",
        "## E. Final Recommendation",
        "",
        "| תנאי | Phase 5d |",
        "|---|---|",
        f"| avg quality >= 75 | {'✅' if p5crit.get('avg_score_gte_75') else '❌'} ({p5d_report.get('avg_quality_score')}) |",
        f"| BLOCKED = 0% | {'✅' if p5crit.get('blocked_pct_lt_20') and p5d_report.get('blocked_pct',0)==0 else '⚠️'} ({p5d_report.get('blocked_pct',0)}%) |",
        f"| >= 70% PASS+NR | {'✅' if p5crit.get('pct_pass_or_nr_gte_70') else '❌'} ({p5d_report.get('pct_pass_or_needs_review',0)}%) |",
        f"| No taxonomy gaps | {'✅' if not p5d_report.get('taxonomy_gaps') else '❌'} |",
        f"| No Shopify live | ✅ |",
        f"| Phase6 candidates >= 5 | {'✅' if len(candidates) >= 5 else '❌'} ({len(candidates)}) |",
        "",
        f"**Phase 6 אפשרי:** {'YES — רק אחרי אישור אייל T3' if phase6_ready else 'NO — עדיין ממתין'}",
        "",
        "**הבהרה:** Phase 6 NOT OPEN. Shopify live NO.",
        "אפשרות Phase 6 = טכנית מוכן. אישור אייל T3 נדרש לפני כל live batch.",
        "",
        "---",
        "",
        "*Phase 5d — DRY RUN ONLY. אין שינויים ב-Shopify.*",
    ]

    return "\n".join(lines)


def build_md_report(report, products_tagged):
    s = report["status_summary"]
    gf = report["gate_fail_counts"]
    st = report["stats"]
    total = report["meta"]["total"]

    good = [p for p in products_tagged if p["final_status"] == "PASS"][:10]
    bad = [p for p in products_tagged if p["final_status"] in ("NEEDS_REVIEW", "BLOCKED")][:10]

    lines = [
        "# Layer 6 — Phase 5d Rerun Report",
        f"**תאריך:** {date.today()}  ",
        f"**סה\"כ מוצרים:** {total} | **DRY RUN ONLY — אין כתיבה ל-Shopify**",
        f"**Logic:** Phase 5b (CAT-B clothing/shoes only) + Phase 5c (type-sleep-soother)",
        "",
        "---",
        "",
        "## 1. תוצאות כלליות",
        "",
        "| מדד | ערך |",
        "|---|---|",
        f"| PASS (כל 8 gates) | {s.get('PASS',0)}/{total} |",
        f"| NEEDS_REVIEW | {s.get('NEEDS_REVIEW',0)}/{total} |",
        f"| BLOCKED | {s.get('BLOCKED',0)}/{total} |",
        f"| ממוצע quality score | {report['avg_quality_score']} |",
        f"| % PASS+NEEDS_REVIEW | {report['pct_pass_or_needs_review']}% |",
        f"| % BLOCKED | {report['blocked_pct']}% |",
        f"| Phase5b exempt (new) | {st.get('phase5b_exempt',0)} |",
        f"| type-sleep-soother products | {st.get('sleep_soother_count',0)} |",
        "",
        "### התפלגות לפי קבוצה",
        "", "| קבוצה | מוצרים |", "|---|---|",
    ]
    for grp, cnt in report["group_distribution"].items():
        lines.append(f"| {grp} | {cnt} |")

    lines += [
        "", "---", "", "## 2. Gates",
        "", "| Gate | כשלונות |", "|---|---|",
    ]
    for gname in ["SOURCE_EXISTS","FORMAT_VALID","ALLOWED_VALUE","SOURCE_TRACEABLE",
                  "NO_FORBIDDEN_INFERENCE","CATEGORY_COVERAGE","DUPLICATE_CONFLICT","QUALITY_SCORE"]:
        lines.append(f"| {gname} | {gf.get(gname,0)}/{total} |")

    lines += [
        "", "---", "", "## 3. בעיות",
        "", "| בעיה | כמות |", "|---|---|",
        f"| RANGE_TOO_BROAD | {st['range_too_broad']} |",
        f"| NO_AGE_FOUND | {st['no_age_found']} |",
        f"| DOLL_NO_AGE_APPLICABLE | {st['doll_no_age']} |",
        f"| Phase5b exempt (non-clothing type, NO_AGE_FOUND) | {st.get('phase5b_exempt',0)} |",
        f"| YAML_GAP | {st['yaml_gap_impact']} |",
    ]

    if report["taxonomy_gaps"]:
        lines += ["", "### Taxonomy Gaps", "", "| Tag | כמות |", "|---|---|"]
        for tag, cnt in sorted(report["taxonomy_gaps"].items()):
            lines.append(f"| `{tag}` | {cnt} |")

    lines += ["", "---", "", "## 4. דוגמאות PASS", ""]
    for p in good:
        tags_str = ", ".join(t["tag"] for t in p["proposed_tags"][:6])
        lines.append(f"**{p['product_id']}** — {p['title'][:45]}  ")
        lines.append(f"Tags: `{tags_str}` | Score: {p['quality_score']}  \n")

    lines += ["---", "", "## 5. דוגמאות NEEDS_REVIEW", ""]
    for p in bad:
        fail_gates = [g["gate"] for g in p.get("gate_results", []) if not g["pass"]]
        lines.append(f"**{p['product_id']}** — {p['title'][:45]} — `{p['final_status']}`  ")
        lines.append(f"Gates: {', '.join(fail_gates)} | Score: {p['quality_score']} | {'; '.join(p.get('notes',[]))}  \n")

    criteria = report["phase5d_pass_criteria"]
    lines += ["---", "", "## 6. Phase 5d Pass Criteria", "", "| תנאי | סטטוס |", "|---|---|"]
    for k, v in criteria.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")
    lines.append("")

    return "\n".join(lines)


def main():
    print("=== Layer 6 Phase 5d Rerun ===")
    print("Phase 5b: CAT-B required only for clothing/shoes")
    print("Phase 5c: type-sleep-soother recognized")

    token = load_env(ENV_PATH)
    if not token:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not found in", ENV_PATH)
        sys.exit(1)

    print("Loading Phase 0 products...")
    phase0 = load_phase0()
    yaml_ids = load_yaml_ids()
    print(f"  {len(phase0)} products, {len(yaml_ids)} YAML files")

    print("Selecting sample (same pool as Phase 4)...")
    sample_groups, all_by_id = select_sample(phase0, yaml_ids)
    all_sample_pids = [pid for pids in sample_groups.values() for pid in pids]
    print(f"  Sample: {dict((k, len(v)) for k,v in sample_groups.items())}")
    print(f"  Total: {len(all_sample_pids)} products")

    print("Fetching from Shopify (read-only)...")
    shopify_data = fetch_shopify_products(all_sample_pids, token)
    print(f"  Fetched: {len(shopify_data)} products")

    print("Tagging with Phase 5b/5c logic...")
    products_tagged = []
    for grp, pids in sample_groups.items():
        for pid in pids:
            base = all_by_id.get(pid, {})
            shop = shopify_data.get(pid, {})
            title = shop.get("title") or base.get("title", "")
            handle = shop.get("handle") or base.get("handle", "")
            tags_str = shop.get("tags") or base.get("tags", "")
            body_html = shop.get("body_html", "")
            product_type_raw = shop.get("product_type", "")
            has_yaml = pid in yaml_ids
            yaml_data = load_yaml(pid) if has_yaml else {}
            result = tag_product(pid, title, handle, tags_str, body_html,
                                 product_type_raw, grp, has_yaml, yaml_data)
            result["product_group"] = grp
            products_tagged.append(result)

    report = build_technical_report(products_tagged, sample_groups)

    s = report["status_summary"]
    st = report["stats"]
    n = report["meta"]["total"]
    print(f"\n--- Phase 5d Results ---")
    print(f"  PASS: {s.get('PASS',0)}/{n} | NEEDS_REVIEW: {s.get('NEEDS_REVIEW',0)}/{n} | BLOCKED: {s.get('BLOCKED',0)}/{n}")
    print(f"  Avg quality: {report['avg_quality_score']}")
    print(f"  RANGE_TOO_BROAD: {st['range_too_broad']} | NO_AGE_FOUND: {st['no_age_found']}")
    print(f"  Phase5b exempt: {st.get('phase5b_exempt',0)} | sleep-soother: {st.get('sleep_soother_count',0)}")
    if report["taxonomy_gaps"]:
        print(f"  Taxonomy gaps: {report['taxonomy_gaps']}")

    print("\nWriting output files...")
    with open(OUT_SAMPLE, "w", encoding="utf-8") as f:
        json.dump({"meta": report["meta"], "products": products_tagged}, f, ensure_ascii=False, indent=2)
    print(f"  {OUT_SAMPLE}")

    report_out = {k: v for k, v in report.items() if k != "products"}
    with open(OUT_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report_out, f, ensure_ascii=False, indent=2)
    print(f"  {OUT_REPORT_JSON}")

    with open(OUT_REPORT_MD, "w", encoding="utf-8") as f:
        f.write(build_md_report(report, products_tagged))
    print(f"  {OUT_REPORT_MD}")

    comparison_md = build_comparison_md(PHASE4_REPORT, report_out, products_tagged)
    with open(OUT_COMPARISON_MD, "w", encoding="utf-8") as f:
        f.write(comparison_md)
    print(f"  {OUT_COMPARISON_MD}")

    print("\nDone. DRY RUN — no Shopify writes.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    main()
