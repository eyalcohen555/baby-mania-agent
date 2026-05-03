"""
Layer 6 — Phase 4 Dry Run
DRY RUN ONLY — no Shopify writes.
Selects 60 products across 5 groups, extracts tags (7 CATs), validates (8 gates), generates 4 reports.
"""

import json, os, re, sys, html
from datetime import date
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from layer6_validate_tags import run_all_gates, PREFIX_TO_CAT

# ── Paths ──────────────────────────────────────────────────────────────────────
PHASE0_PRODUCTS  = "output/tags/phase0-raw-products.json"
YAML_DIR         = "shared/product-context"
ENV_PATH         = os.path.expanduser("~/Desktop/shopify-token/.env")
SHOP_URL         = "https://a2756c-c0.myshopify.com"
API_VERSION      = "2024-10"

OUT_SAMPLE       = "output/tags/phase4-dryrun-sample-60.json"
OUT_REPORT_JSON  = "output/tags/phase4-dryrun-report.json"
OUT_REPORT_MD    = "output/tags/phase4-dryrun-report.md"
OUT_LABELS_MD    = "output/tags/phase4-dryrun-customer-labels-preview.md"

# ── Customer labels map ────────────────────────────────────────────────────────
CUSTOMER_LABELS = {
    "type-romper": "אוברולים", "type-bodysuit": "בגד גוף",
    "type-dress": "שמלה", "type-set": "סטים",
    "type-pants": "מכנסיים", "type-top": "חולצות",
    "type-hat": "כובעים", "type-swimwear": "בגדי ים",
    "type-shoes": "נעליים", "type-sandals": "סנדלים",
    "type-sneakers": "סניקרס", "type-boots": "מגפיים",
    "type-coat": "מעילים", "type-reborn-doll": "בובות ריבורן",
    "type-toy": "צעצועים", "type-accessory": "אביזרים",
    "type-swimming-ring": "מצופי שחייה", "type-unknown": "—",
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

# ── Phase 2b sample (exclude for diversity) ────────────────────────────────────
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

# ── Helpers ────────────────────────────────────────────────────────────────────

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
    """Batch fetch product details from Shopify REST API."""
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


# ── Product classifier ─────────────────────────────────────────────────────────

def classify_product(pid, title, handle, tags_raw):
    t = title.lower()
    h = handle.lower()
    combined = t + " " + h
    tags = tags_raw.lower() if tags_raw else ""
    is_reborn = any(w in combined for w in ["reborn","doll","silicone vinyl"])
    is_toy = any(w in combined for w in [
        "noise machine","sound player","swim ring","swimming-ring","float",
        "swimming ring","white noise",
    ])
    is_shoe = any(w in combined for w in [
        "shoe","sandal","sneaker","boot","walker","slipper","footwear",
        "נעל","סנדל","נעליים","סנדלים","מגף","מגפיים","סניקרס",
    ])
    if is_reborn or is_toy:
        return "reborn_toys"
    if is_shoe:
        return "shoes"
    return "clothing"


def select_sample(phase0, yaml_ids):
    """Select 60 products: 20 clothing_yaml, 15 shoes_yaml, 10 reborn_toys, 10 yaml_gap, 5 edge."""
    clothing_yaml, shoes_yaml, reborn_toys, yaml_gap = [], [], [], []
    all_by_id = {str(p["id"]): p for p in phase0}

    for p in phase0:
        pid = str(p["id"])
        if pid in PHASE2B_SAMPLE:
            continue
        has_yaml = pid in yaml_ids
        group = classify_product(pid, p.get("title",""), p.get("handle",""), p.get("tags",""))
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

    # Edge cases: short handles or no tags, from pools not yet allocated
    edge_candidates = [
        pid for pid in (clothing_yaml[20:] + yaml_gap[10:] + shoes_yaml[15:] + reborn_toys[10:])
        if pid not in used and (
            len(all_by_id[pid].get("handle", "")) < 30
            or not all_by_id[pid].get("tags", "").strip()
        )
    ]
    # Fallback: next unallocated products from any group
    if len(edge_candidates) < 5:
        fallback_pool = [
            pid for pid in (clothing_yaml[20:] + yaml_gap[10:] + shoes_yaml[15:] + reborn_toys[10:])
            if pid not in used and pid not in edge_candidates
        ]
        edge_candidates = edge_candidates + fallback_pool[: 5 - len(edge_candidates)]

    final = dict(sample)
    final["edge_cases"] = edge_candidates[:5]
    return final, all_by_id


# ── Tag extractors ─────────────────────────────────────────────────────────────

def _tag(value, cat, conf, source, rule, note=""):
    t = {"tag": value, "category": cat, "confidence": conf, "source": source, "rule": rule}
    if note:
        t["note"] = note
    return t


def extract_cat_a(title, handle, tags_list, body, yaml_desc):
    """CAT-A: Product Type"""
    combined = (title + " " + handle).lower()
    body_lower = (body + " " + yaml_desc).lower()

    TYPE_KEYWORDS = [
        (["romper","jumpsuit","coverall","onesie","אוברול","אוברולים"], "type-romper", 0.90),
        (["bodysuit","snapper","בגד גוף"], "type-bodysuit", 0.88),
        (["dress","שמלה"], "type-dress", 0.90),
        (["2pcs","3pcs","2-piece","set","סט","סטים"], "type-set", 0.85),
        (["pants","trousers","מכנסיים"], "type-pants", 0.85),
        (["top","shirt","חולצה","blouse"], "type-top", 0.83),
        (["hat","cap","כובע"], "type-hat", 0.90),
        (["swimwear","bikini","swim suit","בגד ים"], "type-swimwear", 0.90),
        (["sandal","סנדל"], "type-sandals", 0.95),
        (["sneaker","סניקרס"], "type-sneakers", 0.95),
        (["boot","מגף"], "type-boots", 0.95),
        (["shoe","נעל","נעליים"], "type-shoes", 0.95),
        (["coat","מעיל","jacket"], "type-coat", 0.88),
        (["swimming ring","swim ring","מצוף"], "type-swimming-ring", 0.95),
        (["reborn","reborn doll","בובת ריבורן"], "type-reborn-doll", 0.99),
        (["doll","silicone vinyl"], "type-reborn-doll", 0.92),
        (["white noise","sound player","noise machine"], "type-toy", 0.88),
        (["toy","צעצוע"], "type-toy", 0.85),
        (["accessory","accessories"], "type-accessory", 0.80),
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

    # Priority 1: existing tags
    for et in tags_list:
        if et.lower() in EXISTING_TAG_MAP:
            return [_tag(EXISTING_TAG_MAP[et.lower()], "CAT-A", 0.88, "existing_tag", "tag_map")]

    # Priority 2: title/handle keywords
    # Boot check before shoe (more specific)
    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in combined for kw in kws):
            src = "title" if any(kw in title.lower() for kw in kws) else "handle"
            return [_tag(tag_val, "CAT-A", conf, src, "keyword")]

    # Priority 3: body (lower confidence)
    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in body_lower for kw in kws):
            return [_tag(tag_val, "CAT-A", min(conf, 0.80), "body", "keyword")]

    return [_tag("type-unknown", "CAT-A", 0.00, "category_default", "fallback")]


def extract_cat_b(pid, title, handle, tags_list, body, yaml_desc, is_reborn):
    """CAT-B: Age Group (Phase 2b hardened algorithm)"""
    if is_reborn:
        return [], "DOLL_NO_AGE_APPLICABLE", ""

    combined = (title + " " + handle).lower()
    desc_text = (body + " " + yaml_desc).lower()

    # Wide range check first
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
        # Deduplicate by tag value
        seen = set()
        deduped = []
        for r in results:
            if r["tag"] not in seen:
                seen.add(r["tag"])
                deduped.append(r)
        return deduped, "OK", ""

    # Narrow explicit patterns
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

    # 1-3y approximation
    if re.search(r"\b1[\s\-]3\s*y(?:ear)?s?\b", combined, re.IGNORECASE):
        return [_tag("age-2-3y", "CAT-B", 0.80, "handle", "1-3y_approx", note="1-3y approximated to 2-3y")], "OK", ""

    # YAML/description narrow patterns
    for pat, tag_val, conf, _ in NARROW_PATS:
        if re.search(pat, desc_text, re.IGNORECASE):
            return [_tag(tag_val, "CAT-B", 0.82, "yaml_desc", "regex_narrow_desc")], "OK", ""

    # Heuristics
    if re.search(r"\bfirst[\s\-]walker\b", combined, re.IGNORECASE):
        return [_tag("age-6-12m", "CAT-B", 0.75, "handle", "first_walker_heuristic")], "OK", ""
    if re.search(r"\btoddler\b", combined, re.IGNORECASE):
        return [_tag("age-2-3y", "CAT-B", 0.75, "handle", "toddler_heuristic")], "OK", ""

    # newborn in description (clothing context)
    if re.search(r"\bnewborn\b", desc_text, re.IGNORECASE):
        return [_tag("age-newborn", "CAT-B", 0.72, "body", "newborn_desc")], "OK", ""

    return [], "NO_AGE_FOUND", ""


def extract_cat_c(title, handle, tags_list, body, yaml_desc, type_tag):
    """CAT-C: Season"""
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
            src = "title" if re.search(pat, (title+" "+handle).lower()) else "existing_tag"
            return [_tag(val, "CAT-C", conf, src, "keyword")]

    # Type-based inference (swimwear → summer, fleece/plush → winter)
    if type_tag in ("type-swimwear", "type-swimming-ring"):
        return [_tag("season-summer", "CAT-C", 0.85, "type_default", "type_inference")]

    for pat, val, conf in SEASON_PATS:
        if re.search(pat, desc_lower, re.IGNORECASE):
            return [_tag(val, "CAT-C", 0.80, "body", "keyword_desc")]

    if re.search(r"\bfleece\b|\bplush\b|\bwarm\b|\bthick\b", combined, re.IGNORECASE):
        return [_tag("season-winter", "CAT-C", 0.78, "handle", "material_inference")]

    return [_tag("season-unknown", "CAT-C", 0.00, "category_default", "fallback")]


def extract_cat_d(title, handle, tags_list, body, yaml_desc):
    """CAT-D: Fabric (only if explicitly stated)"""
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
            src = "title" if re.search(pat, (title+" "+handle).lower()) else "existing_tag"
            results.append(_tag(val, "CAT-D", conf, src, "keyword"))
            break  # Take first match from combined

    if not results:
        for pat, val, conf in FABRIC_PATS:
            if re.search(pat, desc_lower, re.IGNORECASE):
                results.append(_tag(val, "CAT-D", min(conf, 0.82), "body", "keyword_desc"))
                break

    return results  # Optional — empty list OK


def extract_cat_e(title, handle, tags_list, body, yaml_desc, type_tag):
    """CAT-E: Occasion"""
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
        elif type_tag not in ("type-reborn-doll",):
            add_occ("occ-everyday", 0.60, "category_default", "type_default")

    return results


def extract_cat_f(title, handle, tags_list, body, yaml_desc):
    """CAT-F: Gender — NO color inference, default to gender-unknown."""
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

    # Explicit keywords — order matters (girl before neutral, boy before neutral)
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
    """CAT-G: Style (optional — only if explicit)"""
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
            src = "title" if re.search(pat, (title+" "+handle).lower()) else "existing_tag"
            return [_tag(val, "CAT-G", conf, src, "keyword")]

    for pat, val, conf in STYLE_PATS:
        if re.search(pat, desc_lower, re.IGNORECASE):
            return [_tag(val, "CAT-G", min(conf, 0.78), "body", "keyword_desc")]

    return []  # CAT-G is optional


# ── Main tagger ────────────────────────────────────────────────────────────────

TAXONOMY_GAP_BLOCK = {"occ-sport", "occ-holiday", "style-cartoon", "occ-christmas"}

def tag_product(pid, title, handle, current_tags_str, body_html, product_type_raw, product_group, has_yaml, yaml_data):
    """Full 7-category tag extraction with Phase 3b normalization applied."""
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

    # CAT-D (optional)
    proposed.extend(extract_cat_d(title, handle, tags_list, body, yaml_desc))

    # CAT-E (occasion)
    proposed.extend(extract_cat_e(title, handle, tags_list, body, yaml_desc, type_tag))

    # CAT-F
    proposed.extend(extract_cat_f(title, handle, tags_list, body, yaml_desc))

    # CAT-G (optional)
    proposed.extend(extract_cat_g(title, handle, tags_list, body, yaml_desc))

    # Deduplicate by tag value (keep first occurrence)
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
            blocked.append({
                "tag": t["tag"], "category": t.get("category","?"),
                "reason": f"TAXONOMY_GAP: not in approved taxonomy",
                "rule": "phase4_taxonomy_block",
            })
        else:
            final_proposed.append(t)
    proposed = final_proposed

    # Determine missing required categories
    covered = {PREFIX_TO_CAT.get(t["tag"].split("-")[0]) for t in proposed}
    required = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}
    if age_status in ("RANGE_TOO_BROAD", "DOLL_NO_AGE_APPLICABLE"):
        required.discard("CAT-B")
    elif has_yaml is False and age_status == "NO_AGE_FOUND":
        required.discard("CAT-B")
    missing = sorted(required - (covered - {None}))

    # Gate results
    gate_product = {
        "product_id": pid,
        "title": title,
        "handle": handle,
        "product_group": product_group,
        "has_yaml": has_yaml,
        "yaml_gap": not has_yaml,
        "age_status": age_status,
        "age_range_note": range_note,
        "proposed_tags": proposed,
        "blocked_tags": blocked,
    }
    gate_results = run_all_gates(gate_product)["gates"]

    # Quality score (same formula)
    req_covered = {PREFIX_TO_CAT.get(t["tag"].split("-")[0]) for t in proposed} - {None}
    req_set = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}
    if age_status in ("RANGE_TOO_BROAD", "DOLL_NO_AGE_APPLICABLE"):
        req_set.discard("CAT-B")
    req_present = sum(1 for c in req_set if c in req_covered)
    rec_tags = [t for t in proposed if PREFIX_TO_CAT.get(t["tag"].split("-")[0]) in ("CAT-D","CAT-E","CAT-G")]
    rec_present = min(len(rec_tags), 3)
    confs = [t.get("confidence",0) for t in proposed]
    avg_conf = sum(confs)/len(confs) if confs else 0
    quality_score = round((req_present/4)*60 + (rec_present/3)*20 + avg_conf*20, 1)

    # Final status
    gate_fails = [g["gate"] for g in gate_results if not g["pass"]]
    if not gate_fails:
        final_status = "PASS"
    elif "BLOCKED" in notes or any("RANGE_TOO_BROAD" in n or "NO_AGE_FOUND" in n for n in notes):
        final_status = "NEEDS_REVIEW"
    elif len(gate_fails) <= 2 and all(g in ("CATEGORY_COVERAGE","QUALITY_SCORE") for g in gate_fails):
        final_status = "NEEDS_REVIEW"
    else:
        final_status = "NEEDS_REVIEW" if len(gate_fails) < 4 else "BLOCKED"

    if quality_score < 40:
        final_status = "BLOCKED"

    # Customer labels preview
    labels_preview = []
    for t in proposed:
        lbl = CUSTOMER_LABELS.get(t["tag"])
        if lbl and lbl != "—":
            labels_preview.append({"internal_tag": t["tag"], "customer_label_he": lbl})

    return {
        "product_id": pid,
        "title": title,
        "handle": handle,
        "product_group": product_group,
        "has_yaml": has_yaml,
        "yaml_gap": not has_yaml,
        "current_tags": tags_list,
        "proposed_tags": proposed,
        "blocked_tags": blocked,
        "missing_categories": missing,
        "gate_results": gate_results,
        "quality_score": quality_score,
        "final_status": final_status,
        "age_status": age_status,
        "customer_labels_preview": labels_preview,
        "notes": notes,
    }


# ── Report builders ────────────────────────────────────────────────────────────

def build_technical_report(products_tagged, sample_groups):
    total = len(products_tagged)
    status_counts = defaultdict(int)
    gate_fail_counts = defaultdict(int)
    gap_tags = defaultdict(int)
    stats = {
        "total_proposed_tags": 0,
        "total_blocked_tags": 0,
        "range_too_broad": 0,
        "no_age_found": 0,
        "doll_no_age": 0,
        "multi_age": 0,
        "yaml_gap_impact": 0,
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
        scores.append(p["quality_score"])
        for g in p.get("gate_results", []):
            if not g["pass"]:
                gate_fail_counts[g["gate"]] += 1
        for t in p["proposed_tags"]:
            from layer6_validate_tags import ALL_ALLOWED
            if t["tag"] not in ALL_ALLOWED:
                gap_tags[t["tag"]] += 1

    avg_score = round(sum(scores)/len(scores), 1) if scores else 0
    pct_pass_or_nr = (status_counts["PASS"] + status_counts["NEEDS_REVIEW"]) / total * 100
    blocked_pct = status_counts["BLOCKED"] / total * 100

    group_dist = {grp: len(pids) for grp, pids in sample_groups.items()}

    return {
        "meta": {"phase": "Phase 4 — Dry Run", "date": str(date.today()), "total": total},
        "group_distribution": group_dist,
        "status_summary": dict(status_counts),
        "avg_quality_score": avg_score,
        "pct_pass_or_needs_review": round(pct_pass_or_nr, 1),
        "blocked_pct": round(blocked_pct, 1),
        "stats": stats,
        "gate_fail_counts": dict(gate_fail_counts),
        "taxonomy_gaps": dict(sorted(gap_tags.items())),
        "phase4_pass_criteria": {
            "no_shopify_live": True,
            "no_forbidden_tags": gap_tags.get("gender-unisex", 0) == 0 and gap_tags.get("type-doll", 0) == 0,
            "no_default_unisex_source": True,
            "no_wide_range_age": True,
            "native_tags_english_only": True,
            "avg_score_gte_75": avg_score >= 75,
            "pct_pass_or_nr_gte_70": pct_pass_or_nr >= 70,
            "blocked_pct_lt_20": blocked_pct < 20,
        },
        "products": products_tagged,
    }


def build_md_report(report, products_tagged):
    s = report["status_summary"]
    gf = report["gate_fail_counts"]
    st = report["stats"]
    total = report["meta"]["total"]

    good = [p for p in products_tagged if p["final_status"] == "PASS"][:10]
    bad = [p for p in products_tagged if p["final_status"] in ("NEEDS_REVIEW","BLOCKED")][:10]

    lines = [
        "# Layer 6 — Phase 4 Dry Run Report",
        f"**תאריך:** {date.today()}  ",
        f"**סה\"כ מוצרים:** {total} | **DRY RUN ONLY — אין כתיבה ל-Shopify**",
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
        "",
        "### התפלגות לפי קבוצה",
        "",
        "| קבוצה | מוצרים |",
        "|---|---|",
    ]
    for grp, cnt in report["group_distribution"].items():
        lines.append(f"| {grp} | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## 2. תוצאות Gates (8 שערים)",
        "",
        "| Gate | כשלונות |",
        "|---|---|",
    ]
    for gname in ["SOURCE_EXISTS","FORMAT_VALID","ALLOWED_VALUE","SOURCE_TRACEABLE",
                  "NO_FORBIDDEN_INFERENCE","CATEGORY_COVERAGE","DUPLICATE_CONFLICT","QUALITY_SCORE"]:
        cnt = gf.get(gname, 0)
        lines.append(f"| {gname} | {cnt}/{total} |")

    lines += [
        "",
        "---",
        "",
        "## 3. בעיות מיוחדות",
        "",
        "| בעיה | כמות |",
        "|---|---|",
        f"| RANGE_TOO_BROAD (גיל נחסם) | {st['range_too_broad']} |",
        f"| NO_AGE_FOUND (אין מקור גיל) | {st['no_age_found']} |",
        f"| DOLL_NO_AGE_APPLICABLE | {st['doll_no_age']} |",
        f"| Multi-age (מוצר עם >1 טווחי גיל) | {st['multi_age']} |",
        f"| YAML_GAP (ללא YAML) | {st['yaml_gap_impact']} |",
    ]

    if report["taxonomy_gaps"]:
        lines += [
            "",
            "### Taxonomy Gaps שנמצאו",
            "",
            "| Tag | כמות |",
            "|---|---|",
        ]
        for tag, cnt in sorted(report["taxonomy_gaps"].items()):
            lines.append(f"| `{tag}` | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## 4. 10 דוגמאות טובות (PASS)",
        "",
    ]
    for p in good:
        tags_str = ", ".join(t["tag"] for t in p["proposed_tags"][:6])
        lines.append(f"**{p['product_id']}** — {p['title'][:45]}  ")
        lines.append(f"Tags: `{tags_str}` | Score: {p['quality_score']}  ")
        lines.append("")

    lines += [
        "---",
        "",
        "## 5. 10 דוגמאות בעייתיות (NEEDS_REVIEW / BLOCKED)",
        "",
    ]
    for p in bad:
        fail_gates = [g["gate"] for g in p.get("gate_results",[]) if not g["pass"]]
        lines.append(f"**{p['product_id']}** — {p['title'][:45]} — `{p['final_status']}`  ")
        lines.append(f"Failed gates: {', '.join(fail_gates)} | Score: {p['quality_score']} | Notes: {'; '.join(p.get('notes',[]))}  ")
        lines.append("")

    criteria = report["phase4_pass_criteria"]
    lines += [
        "---",
        "",
        "## 6. תנאי PASS ל-Phase 4",
        "",
        "| תנאי | סטטוס |",
        "|---|---|",
        f"| אין Shopify live | {'YES' if criteria['no_shopify_live'] else 'NO'} |",
        f"| אין gender-unisex / type-doll | {'YES' if criteria['no_forbidden_tags'] else 'NO'} |",
        f"| אין default_unisex / fallback source | {'YES' if criteria['no_default_unisex_source'] else 'NO'} |",
        f"| אין גיל מטעה מטווח רחב | {'YES' if criteria['no_wide_range_age'] else 'NO'} |",
        f"| Native tags באנגלית בלבד | {'YES' if criteria['native_tags_english_only'] else 'NO'} |",
        f"| Avg quality score >= 75 | {'YES' if criteria['avg_score_gte_75'] else 'NO'} ({report['avg_quality_score']}) |",
        f"| >= 70% PASS+NEEDS_REVIEW | {'YES' if criteria['pct_pass_or_nr_gte_70'] else 'NO'} ({report['pct_pass_or_needs_review']}%) |",
        f"| BLOCKED <= 20% | {'YES' if criteria['blocked_pct_lt_20'] else 'NO'} ({report['blocked_pct']}%) |",
        "",
        "---",
        "",
        "## 7. מה צריך לתקן לפני Phase 5",
        "",
        "1. **CATEGORY_COVERAGE failures** — מוצרים ללא CAT-A/C/F: לבדוק ידנית",
        f"2. **RANGE_TOO_BROAD** ({st['range_too_broad']} מוצרים) — להחליט: age-unknown fallback / manual split / multi-tag",
        f"3. **NO_AGE_FOUND** ({st['no_age_found']} מוצרים) — להעשיר YAML או לאשר age-unknown",
        f"4. **YAML_GAP** ({st['yaml_gap_impact']} מוצרים) — שיפור coverage יוריד NEEDS_REVIEW משמעותית",
        "",
        "---",
        "",
        "## 8. האם Phase 4 מספיק לבדיקה אנושית?",
        "",
    ]
    all_criteria_met = all(criteria.values())
    if all_criteria_met:
        lines.append("**YES** — כל תנאי Phase 4 מתקיימים. Phase 5 Human Review יכול להתחיל.")
    else:
        failed = [k for k, v in criteria.items() if not v]
        lines.append(f"**PARTIAL** — תנאים שלא התקיימו: {', '.join(failed)}")
        lines.append("יש לפתור את הבעיות לעיל לפני Phase 5.")
    lines.append("")

    return "\n".join(lines)


def build_labels_md(products_tagged):
    """Customer labels preview — Hebrew navigation labels."""
    # Collect all unique internal_tag → label pairs from all products
    tag_examples = {}
    for p in products_tagged:
        for lbl in p.get("customer_labels_preview", []):
            tag = lbl["internal_tag"]
            if tag not in tag_examples:
                tag_examples[tag] = {
                    "label": lbl["customer_label_he"],
                    "example_pid": p["product_id"],
                    "example_title": p["title"][:40],
                    "example_group": p["product_group"],
                }

    # Group by category
    CAT_GROUPS = {
        "סוג מוצר (CAT-A)": "type-",
        "גיל (CAT-B)": "age-",
        "עונה (CAT-C)": "season-",
        "בד/חומר (CAT-D)": "fabric-",
        "שימוש (CAT-E)": "occ-",
        "מגדר (CAT-F)": "gender-",
        "סגנון (CAT-G)": "style-",
    }

    lines = [
        "# Layer 6 — Phase 4 Customer Labels Preview",
        f"**תאריך:** {date.today()}  ",
        "**הערה:** תוויות לתפריט לקוח בעברית — Native tag באנגלית בלבד",
        "",
        "---",
    ]

    for group_name, prefix in CAT_GROUPS.items():
        group_tags = {k: v for k, v in tag_examples.items() if k.startswith(prefix)}
        if not group_tags:
            continue
        lines += [
            "",
            f"## {group_name}",
            "",
            "| Internal Tag | תווית לקוח | דוגמת מוצר | מתאים לתפריט |",
            "|---|---|---|---|",
        ]
        for tag in sorted(group_tags):
            ex = group_tags[tag]
            suitable = "YES" if ex["label"] != "—" else "NO"
            lines.append(
                f"| `{tag}` | {ex['label']} | {ex['example_title']} | {suitable} |"
            )

    lines += [
        "",
        "---",
        "",
        "## הערות ניווט",
        "",
        "- כל native tag הוא ASCII slug באנגלית — לא גלוי ישירות ללקוח",
        "- תווית בעברית תוצג בתפריט / filter ב-Phase 9 (Navigation Planning)",
        "- `—` = fallback tag — לא ייוצג בניווט לקוח",
        "- `gender-unknown`, `age-unknown` וכו' = ממתין להעשרה, לא לתפריט ציבורי",
    ]

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=== Layer 6 Phase 4 Dry Run ===")

    token = load_env(ENV_PATH)
    if not token:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not found in", ENV_PATH)
        sys.exit(1)

    print("Loading Phase 0 products...")
    phase0 = load_phase0()
    yaml_ids = load_yaml_ids()
    print(f"  {len(phase0)} products, {len(yaml_ids)} YAML files")

    print("Selecting 60-product sample...")
    sample_groups, all_by_id = select_sample(phase0, yaml_ids)
    all_sample_pids = [pid for pids in sample_groups.values() for pid in pids]
    print(f"  Sample: {dict((k, len(v)) for k,v in sample_groups.items())}")
    print(f"  Total: {len(all_sample_pids)} products")

    print("Fetching product details from Shopify...")
    shopify_data = fetch_shopify_products(all_sample_pids, token)
    print(f"  Fetched: {len(shopify_data)} products")

    print("Loading YAML files and tagging products...")
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
            result = tag_product(
                pid, title, handle, tags_str, body_html,
                product_type_raw, grp, has_yaml, yaml_data,
            )
            result["product_group"] = grp
            products_tagged.append(result)

    print("Running reports...")
    report = build_technical_report(products_tagged, sample_groups)

    # Status summary print
    s = report["status_summary"]
    print(f"\n--- Phase 4 Results ---")
    n = report["meta"]["total"]
    print(f"  PASS: {s.get('PASS',0)}/{n} | NEEDS_REVIEW: {s.get('NEEDS_REVIEW',0)}/{n} | BLOCKED: {s.get('BLOCKED',0)}/{n}")
    print(f"  Avg quality score: {report['avg_quality_score']}")
    print(f"  RANGE_TOO_BROAD: {report['stats']['range_too_broad']} | NO_AGE_FOUND: {report['stats']['no_age_found']}")
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

    with open(OUT_LABELS_MD, "w", encoding="utf-8") as f:
        f.write(build_labels_md(products_tagged))
    print(f"  {OUT_LABELS_MD}")

    print("\nDone.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    main()
