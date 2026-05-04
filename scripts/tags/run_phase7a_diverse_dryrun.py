"""
Layer 6/7 — Phase 7A Diverse Rollout Dry Run
Selects 20 diverse candidates (dress/bodysuit/hat/pants/set) from Shopify inventory.
DRY RUN ONLY — no Shopify writes. No collections. No Mega Menu.
"""

import json, os, re, sys, html
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parents[2]
PHASE0     = ROOT / "output/tags/phase0-raw-products.json"
YAML_DIR   = ROOT / "shared/product-context"
ENV_PATH   = Path.home() / "Desktop/shopify-token/.env"
SHOP_URL   = "https://a2756c-c0.myshopify.com"
API_VER    = "2024-10"

OUT_JSON   = ROOT / "output/tags/phase7a-diverse-rollout-candidates.json"
OUT_MD     = ROOT / "output/tags/phase7a-diverse-rollout-candidates.md"

# Already live — never re-tag
LIVE_C1_C5 = {
    "9688660312377","9874906349881","9895864205625",
    "9687579033913","9688932909369",
}
# Already in existing sample — skip to avoid overlap
EXISTING_SAMPLE_IDS: set[str] = set()

# ── 20 diverse candidates (pre-selected by type) ───────────────────────────
# priority: dress > bodysuit > hat > pants > set
CANDIDATE_PIDS = [
    # dress (4)
    "9179166671161",
    "9606694437177",
    "9731768746297",
    "9607363559737",
    # bodysuit (5)
    "9179165753657",
    "9179168964921",
    "9179152154937",
    "9179167129913",
    "9874906382649",
    # hat (4)
    "9688885985593",
    "9688934973753",
    "9874906546489",
    "9688660377913",
    # pants (4)
    "9688976326969",
    "9688964989241",
    "9688674566457",
    "9688976294201",
    # set (3)  — 3 only since sets already represented in existing sample
    "10190523302201",
    "10190523203897",
    "10190523138361",
]

# ── helpers ────────────────────────────────────────────────────────────────
def load_env(path):
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SHOPIFY_ACCESS_TOKEN"):
                    return line.split("=", 1)[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    return None


def strip_html(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_yaml(pid):
    path = YAML_DIR / f"{pid}.yaml"
    if not path.exists():
        return {}
    try:
        import yaml as _yaml
        with open(path, encoding="utf-8") as f:
            return _yaml.safe_load(f) or {}
    except Exception:
        return {}


def fetch_shopify(pids, token):
    import urllib.request
    url = (
        f"{SHOP_URL}/admin/api/{API_VER}/products.json"
        f"?ids={','.join(pids)}&limit=250"
        f"&fields=id,title,handle,tags,body_html,product_type,variants,status"
    )
    req = urllib.request.Request(
        url, headers={"X-Shopify-Access-Token": token}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return {str(p["id"]): p for p in json.loads(resp.read()).get("products", [])}


# ── tag extraction (mirrors Phase 5k logic) ────────────────────────────────
def _tag(value, cat, conf, source, rule, note=""):
    t = {"tag": value, "category": cat, "confidence": conf, "source": source, "rule": rule}
    if note:
        t["note"] = note
    return t


def extract_cat_a(title, handle, tags_list, body, yaml_desc):
    combined = (title + " " + handle).lower()
    body_lower = (body + " " + yaml_desc).lower()

    EXISTING_TAG_MAP = {
        "baby-romper": "type-romper", "baby-overall": "type-romper", "אוברול": "type-romper",
        "baby-bodysuit": "type-bodysuit", "בגד גוף": "type-bodysuit",
        "baby-dress": "type-dress", "שמלה": "type-dress",
        "baby-set": "type-set", "baby-suit": "type-set", "סט": "type-set",
        "baby-pants": "type-pants", "מכנסיים": "type-pants",
        "baby-top": "type-top", "חולצה": "type-top",
        "baby-hat": "type-hat", "כובע": "type-hat",
        "baby-swimwear": "type-swimwear",
        "baby-shoes": "type-shoes", "baby-sandals": "type-sandals",
        "baby-sneakers": "type-sneakers", "baby-boots": "type-boots",
        "baby-coat": "type-coat",
    }
    TYPE_KEYWORDS = [
        (["romper", "jumpsuit", "coverall", "onesie", "אוברול", "אוברולים"], "type-romper", 0.90),
        (["bodysuit", "snapper", "בגד גוף"], "type-bodysuit", 0.88),
        (["dress", "שמלה"], "type-dress", 0.90),
        (["2pcs", "3pcs", "2-piece", "set", "סט", "סטים"], "type-set", 0.85),
        (["pants", "trousers", "leggings", "מכנסיים"], "type-pants", 0.85),
        (["top", "shirt", "חולצה", "blouse"], "type-top", 0.83),
        (["hat", "cap", "כובע", "beanie", "bucket-hat"], "type-hat", 0.90),
        (["swimwear", "bikini", "swim suit", "בגד ים"], "type-swimwear", 0.90),
        (["sandal", "סנדל"], "type-sandals", 0.95),
        (["sneaker", "סניקרס"], "type-sneakers", 0.95),
        (["boot", "מגף"], "type-boots", 0.95),
        (["shoe", "נעל", "נעליים"], "type-shoes", 0.95),
        (["coat", "מעיל", "jacket"], "type-coat", 0.88),
        (["swimming ring", "swim ring", "מצוף"], "type-swimming-ring", 0.95),
    ]
    GENERIC_SHOE_OVERRIDES = {
        "baby-shoes": [
            (["sneaker", "סניקרס"], "type-sneakers", 0.92),
            (["sandal", "סנדל"],    "type-sandals",  0.92),
            (["boot", "מגף"],       "type-boots",    0.92),
        ]
    }
    for et in tags_list:
        et_lower = et.lower()
        if et_lower in EXISTING_TAG_MAP:
            base_type = EXISTING_TAG_MAP[et_lower]
            if et_lower in GENERIC_SHOE_OVERRIDES:
                for kws, specific_type, specific_conf in GENERIC_SHOE_OVERRIDES[et_lower]:
                    if any(kw in combined for kw in kws):
                        src = "title" if any(kw in title.lower() for kw in kws) else "handle"
                        return [_tag(specific_type, "CAT-A", specific_conf, src, "keyword_override")]
            return [_tag(base_type, "CAT-A", 0.88, "existing_tag", "tag_map")]

    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in combined for kw in kws):
            src = "title" if any(kw in title.lower() for kw in kws) else "handle"
            return [_tag(tag_val, "CAT-A", conf, src, "keyword")]

    for kws, tag_val, conf in TYPE_KEYWORDS:
        if any(kw in body_lower for kw in kws):
            return [_tag(tag_val, "CAT-A", min(conf, 0.80), "body", "keyword")]

    return [_tag("type-unknown", "CAT-A", 0.00, "category_default", "fallback")]


VARIANT_SIZE_MAP = {
    "nb": "size-newborn", "newborn": "size-newborn", "ניו בורן": "size-newborn",
    "0-3m": "size-0-3m", "0-3": "size-0-3m",
    "3-6m": "size-3-6m", "3-6": "size-3-6m",
    "6-9m": "size-6-9m", "6-9": "size-6-9m",
    "9-12m": "size-9-12m", "9-12": "size-9-12m",
    "12-18m": "size-12-18m", "12-18": "size-12-18m",
    "18-24m": "size-18-24m", "18-24": "size-18-24m",
    "2y": "size-2y", "2t": "size-2y",
    "3y": "size-3y", "3t": "size-3y",
    "4y": "size-4y", "4t": "size-4y",
    "s": None, "m": None, "l": None, "xl": None,  # EU/numeric → skip
}

WIDE_RANGE_PATS = [
    (r"\b0[\s\-]+(?:to[\s\-]+)?12(?:m|months?)?", "0-12m"),
    (r"\b0[\s\-]+(?:to[\s\-]+)?18(?:m|months?)?", "0-18m"),
    (r"\b0[\s\-]+(?:to[\s\-]+)?24(?:m|months?)?", "0-24m"),
    (r"\b3[\s\-]+18(?:m|months?)?", "3-18m"),
    (r"\b3[\s\-]+24(?:m|months?)?", "3-24m"),
]


def extract_cat_b(title, handle, tags_list, variants):
    combined = (title + " " + handle).lower()
    for pat, desc in WIDE_RANGE_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            return [], "RANGE_TOO_BROAD", desc

    # variant option source (highest priority — Phase 5k normalization)
    if variants:
        seen: set[str] = set()
        results = []
        for v in variants:
            opts = [
                v.get("option1") or "", v.get("option2") or "", v.get("option3") or "",
                (v.get("title") or "").split(" / ")[0],
            ]
            for opt in opts:
                key = re.sub(r'\s+', '', opt.strip().lower())
                if key in VARIANT_SIZE_MAP:
                    tag_val = VARIANT_SIZE_MAP[key]
                    if tag_val and tag_val not in seen:
                        seen.add(tag_val)
                        results.append(_tag(tag_val, "CAT-B", 0.95, "variant", "variant_option"))
        if results:
            return results, "OK", ""

    # Hebrew/clean existing tags
    HEB_SIZE_MAP = {
        "0-3 חודש": "size-0-3m", "3-6 חודש": "size-3-6m",
        "6-9 חודש": "size-6-9m", "9-12 חודש": "size-9-12m",
        "12-18 חודש": "size-12-18m", "18-24 חודש": "size-18-24m",
        "0-3 חודשים": "size-0-3m", "3-6 חודשים": "size-3-6m",
        "6-9 חודשים": "size-6-9m", "9-12 חודשים": "size-9-12m",
        "12-18 חודשים": "size-12-18m", "18-24 חודשים": "size-18-24m",
        "newborn": "size-newborn", "יילוד": "size-newborn",
    }
    results = []
    for et in tags_list:
        mapped = HEB_SIZE_MAP.get(et) or HEB_SIZE_MAP.get(et.lower())
        if mapped and mapped not in {r["tag"] for r in results}:
            results.append(_tag(mapped, "CAT-B", 0.90, "existing_tag_hebrew", "heb_tag", note=f"from tag: {et}"))
    if results:
        return results, "OK", ""

    # title/handle narrow regex
    NARROW_SIZE_PATS = [
        (r"\bnewborn\b|\bיילוד\b", "size-newborn", 0.88),
        (r"\b0[\s\-]3\s*(?:m|months?)\b", "size-0-3m", 0.88),
        (r"\b3[\s\-]6\s*(?:m|months?)\b", "size-3-6m", 0.88),
        (r"\b6[\s\-]9\s*(?:m|months?)\b", "size-6-9m", 0.88),
        (r"\b9[\s\-]12\s*(?:m|months?)\b", "size-9-12m", 0.88),
        (r"\b12[\s\-]18\s*(?:m|months?)\b", "size-12-18m", 0.88),
        (r"\b18[\s\-]24\s*(?:m|months?)\b", "size-18-24m", 0.88),
        (r"\b2\s*[yY](?:ear)?s?\b|\b2T\b", "size-2y", 0.88),
        (r"\b3\s*[yY](?:ear)?s?\b|\b3T\b", "size-3y", 0.88),
        (r"\b4\s*[yY](?:ear)?s?\b|\b4T\b", "size-4y", 0.88),
    ]
    for pat, tag_val, conf in NARROW_SIZE_PATS:
        if re.search(pat, combined, re.IGNORECASE):
            src = "title" if re.search(pat, title, re.IGNORECASE) else "handle"
            return [_tag(tag_val, "CAT-B", conf, src, "regex_narrow")], "OK", ""

    return [], "NO_SIZE_FOUND", ""


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

    KW_SEASON = [
        (["קיץ", "summer"], "season-summer", 0.88),
        (["חורף", "winter", "fleece", "פליז"], "season-winter", 0.85),
        (["אביב", "spring", "סתיו", "autumn", "fall"], "season-spring-fall", 0.82),
    ]
    for kws, val, conf in KW_SEASON:
        if any(kw in combined for kw in kws):
            return [_tag(val, "CAT-C", conf, "title_handle", "keyword")]

    # type context
    if type_tag == "type-swimwear":
        return [_tag("season-summer", "CAT-C", 0.88, "type_context", "type_infer")]

    return [_tag("season-unknown", "CAT-C", 0.00, "none", "fallback")]


def extract_cat_f(title, handle, tags_list, yaml_desc):
    combined = (title + " " + handle + " " + " ".join(tags_list)).lower()

    GENDER_TAGS = {
        "girls-clothing": "gender-girl", "girls": "gender-girl",
        "boys-clothing": "gender-boy", "boys": "gender-boy",
        "neutral-baby-outfit": "gender-neutral",
        "unisex-baby": "gender-neutral",
    }
    for et in tags_list:
        et_lower = et.lower()
        if et_lower in GENDER_TAGS:
            return [_tag(GENDER_TAGS[et_lower], "CAT-F", 0.90, "existing_tag", "tag_map")]

    # title/handle keywords
    GENDER_KW = [
        (["בנות", "girl", "girls", "feminine"], "gender-girl", 0.90),
        (["בנים", "boy", "boys", "masculine"], "gender-boy", 0.90),
        (["ניוטרלי", "unisex", "neutral"], "gender-neutral", 0.88),
    ]
    for kws, val, conf in GENDER_KW:
        if any(kw in combined for kw in kws):
            src = "title" if any(kw in (title + " " + " ".join(tags_list)).lower() for kw in kws) else "handle"
            return [_tag(val, "CAT-F", conf, src, "keyword")]

    # YAML
    yaml_gender = yaml_desc.lower()
    if "בנות" in yaml_gender or "girl" in yaml_gender:
        return [_tag("gender-girl", "CAT-F", 0.90, "yaml", "yaml_field")]
    if "בנים" in yaml_gender or "boy" in yaml_gender:
        return [_tag("gender-boy", "CAT-F", 0.90, "yaml", "yaml_field")]
    if "ניוטרלי" in yaml_gender or "unisex" in yaml_gender or "neutral" in yaml_gender:
        return [_tag("gender-neutral", "CAT-F", 0.85, "yaml", "yaml_field")]

    return [_tag("gender-unknown", "CAT-F", 0.00, "none", "fallback")]


def extract_cat_d(title, handle, tags_list, yaml_data):
    combined = (title + " " + handle).lower()
    fabric_yaml = str(yaml_data.get("fabric_type", "")).lower()
    full_text = combined + " " + fabric_yaml + " " + " ".join(t.lower() for t in tags_list)

    FABRIC_MAP = {
        "כותנה": "fabric-cotton", "cotton": "fabric-cotton", "cotton-baby": "fabric-cotton",
        "פשתן": "fabric-linen", "linen": "fabric-linen", "linen-baby": "fabric-linen",
        "מוסלין": "fabric-muslin", "muslin": "fabric-muslin",
        "פליז": "fabric-fleece", "fleece": "fabric-fleece", "fleece-baby": "fabric-fleece",
        "ג'ינס": "fabric-denim", "denim": "fabric-denim", "denim-baby": "fabric-denim",
        "פוליאסטר": "fabric-polyester", "polyester": "fabric-polyester",
        "פרווה": "fabric-faux-fur", "faux-fur": "fabric-faux-fur", "faux-fur-baby": "fabric-faux-fur",
        "קורדרוי": "fabric-corduroy", "corduroy": "fabric-corduroy",
        "קטיפה": "fabric-velvet", "velvet": "fabric-velvet",
        "סריג": "fabric-knit", "knit": "fabric-knit", "knitted": "fabric-knit",
    }
    for kw, tag_val in FABRIC_MAP.items():
        if kw in full_text:
            src = "yaml" if kw in fabric_yaml else ("existing_tag" if kw in " ".join(tags_list).lower() else "title")
            conf = 0.92 if src == "yaml" else 0.90
            return [_tag(tag_val, "CAT-D", conf, src, "keyword")]

    return []


def extract_cat_g(title, handle, tags_list, yaml_data):
    combined = (title + " " + handle).lower()
    style_yaml = str(yaml_data.get("style", "")).lower()
    full_text = combined + " " + style_yaml + " " + " ".join(t.lower() for t in tags_list)

    STYLE_MAP = {
        "elegant-baby": "style-elegant", "אלגנטי": "style-elegant", "elegant": "style-elegant",
        "casual": "style-casual", "קז'ואל": "style-casual",
        "vintage-baby": "style-vintage", "וינטאג'": "style-vintage", "vintage": "style-vintage",
        "floral-baby": "style-floral", "פרחוני": "style-floral", "floral": "style-floral",
        "animal-print-baby": "style-animal-print", "leopard": "style-animal-print",
        "bear-print-baby": "style-teddy", "teddy": "style-teddy",
        "european-baby-style": "style-european",
        "unicorn-baby": "style-unicorn", "חד-קרן": "style-unicorn",
        "striped-baby": "style-striped", "פסים": "style-striped", "striped": "style-striped",
    }
    for kw, tag_val in STYLE_MAP.items():
        if kw in full_text:
            src = "yaml" if kw in style_yaml else ("existing_tag" if kw in " ".join(tags_list).lower() else "title")
            conf = 0.85 if src == "yaml" else 0.82
            return [_tag(tag_val, "CAT-G", conf, src, "keyword")]

    return []


# ── scoring ────────────────────────────────────────────────────────────────
def compute_score(proposed_tags, size_status, type_tag, has_yaml):
    # Base 60
    score = 60.0

    # CAT-A present and not unknown (+15)
    type_tags = [t for t in proposed_tags if t["category"] == "CAT-A"]
    if type_tags and not type_tags[0]["tag"].endswith("unknown"):
        score += 15

    # CAT-B present (if applicable, i.e. clothing/shoes) (+15)
    NON_SIZE_TYPES = {"type-reborn-doll", "type-toy", "type-sleep-soother", "type-swimming-ring", "type-accessory"}
    if type_tag not in NON_SIZE_TYPES:
        size_tags = [t for t in proposed_tags if t["category"] == "CAT-B"]
        if size_tags:
            score += 15

    # CAT-F present and not unknown (+5)
    gender_tags = [t for t in proposed_tags if t["category"] == "CAT-F"]
    if gender_tags and not gender_tags[0]["tag"].endswith("unknown"):
        score += 5

    # CAT-C present and not unknown (+5)
    season_tags = [t for t in proposed_tags if t["category"] == "CAT-C"]
    if season_tags and not season_tags[0]["tag"].endswith("unknown"):
        score += 5

    # has YAML (+5)
    if has_yaml:
        score += 5

    # high confidence source trace: all required tags ≥0.85 (+5)
    required_cats = {"CAT-A", "CAT-B", "CAT-F"}
    req_tags = [t for t in proposed_tags if t["category"] in required_cats]
    if req_tags and all(t["confidence"] >= 0.85 for t in req_tags):
        score += 5

    # penalty: no size for clothing (-10)
    if type_tag not in NON_SIZE_TYPES and size_status != "OK":
        score -= 10

    return min(round(score, 1), 100.0)


def assign_verdict(score, proposed_tags, size_status, type_tag):
    type_tags = [t for t in proposed_tags if t["category"] == "CAT-A"]
    if not type_tags or type_tags[0]["tag"] == "type-unknown":
        return "REJECT", "type-unknown — no clear product type"

    # check for forbidden tags
    forbidden = {"age-0-3m", "age-3-6m", "age-6-9m", "age-9-12m", "age-12-18m", "age-18-24m"}
    for t in proposed_tags:
        if t["tag"] in forbidden:
            return "REJECT", f"forbidden age-* tag: {t['tag']}"

    NON_SIZE_TYPES = {"type-reborn-doll", "type-toy", "type-sleep-soother", "type-swimming-ring"}
    if type_tag not in NON_SIZE_TYPES and size_status == "RANGE_TOO_BROAD":
        return "REVIEW_ONLY", "size range too broad"

    if score >= 85:
        return "SAFE_FOR_PHASE7A", ""
    elif score >= 70:
        return "REVIEW_ONLY", f"score {score} < 85 minimum"
    else:
        return "REJECT", f"score {score} too low"


# ── main ───────────────────────────────────────────────────────────────────
def main():
    token = load_env(ENV_PATH)
    if not token:
        print("ERROR: no Shopify token found")
        sys.exit(1)

    print(f"Fetching {len(CANDIDATE_PIDS)} products from Shopify...")
    shopify_data = fetch_shopify(CANDIDATE_PIDS, token)
    print(f"  Received: {len(shopify_data)} products")

    yaml_ids = {fn.replace(".yaml", "") for fn in os.listdir(YAML_DIR) if fn.endswith(".yaml")}

    results = []
    type_distribution: dict[str, int] = defaultdict(int)

    for pid in CANDIDATE_PIDS:
        if pid not in shopify_data:
            results.append({
                "product_id": pid,
                "status": "NOT_FOUND",
                "verdict": "REJECT",
                "reason": "product not found in Shopify",
            })
            continue

        p = shopify_data[pid]
        if p.get("status") != "active":
            results.append({
                "product_id": pid,
                "title": p.get("title", ""),
                "status": "INACTIVE",
                "verdict": "REJECT",
                "reason": f"product status: {p.get('status')}",
            })
            continue

        title    = p.get("title", "")
        handle   = p.get("handle", "")
        tags_str = p.get("tags", "")
        tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]
        body     = strip_html(p.get("body_html", ""))
        variants = p.get("variants", [])
        has_yaml = pid in yaml_ids
        yaml_data = load_yaml(pid) if has_yaml else {}
        yaml_desc = str(yaml_data.get("description", "")) + " " + str(yaml_data.get("fabric_type", ""))

        # --- tag extraction ---
        cat_a = extract_cat_a(title, handle, tags_list, body, yaml_desc)
        type_tag = cat_a[0]["tag"] if cat_a else "type-unknown"

        is_hat = type_tag == "type-hat"
        NON_SIZE_TYPES = {"type-reborn-doll","type-toy","type-sleep-soother","type-swimming-ring","type-accessory","type-hat"}

        if type_tag in NON_SIZE_TYPES:
            cat_b, size_status, size_note = [], "NOT_APPLICABLE", ""
        else:
            cat_b, size_status, size_note = extract_cat_b(title, handle, tags_list, variants)

        cat_c = extract_cat_c(title, handle, tags_list, body, yaml_desc, type_tag)
        cat_d = extract_cat_d(title, handle, tags_list, yaml_data)
        cat_f = extract_cat_f(title, handle, tags_list, yaml_desc)
        cat_g = extract_cat_g(title, handle, tags_list, yaml_data)

        # Filter: skip unknown fallbacks for live
        all_proposed = cat_a + cat_b + cat_c + cat_d + cat_f + cat_g
        live_tags = [t for t in all_proposed if not t["tag"].endswith("unknown") and t["confidence"] >= 0.80]

        score = compute_score(all_proposed, size_status, type_tag, has_yaml)
        verdict, reason = assign_verdict(score, all_proposed, size_status, type_tag)

        type_distribution[type_tag] += 1

        results.append({
            "product_id": pid,
            "title": title,
            "type": type_tag,
            "current_tags": tags_list,
            "proposed_all": all_proposed,
            "proposed_live_tags": [t["tag"] for t in live_tags],
            "source_trace": {t["tag"]: {"source": t["source"], "rule": t["rule"], "conf": t["confidence"]} for t in all_proposed},
            "size_status": size_status,
            "size_note": size_note,
            "score": score,
            "has_yaml": has_yaml,
            "verdict": verdict,
            "reason": reason,
        })

    # --- summary ---
    safe   = [r for r in results if r.get("verdict") == "SAFE_FOR_PHASE7A"]
    review = [r for r in results if r.get("verdict") == "REVIEW_ONLY"]
    reject = [r for r in results if r.get("verdict") == "REJECT"]

    output = {
        "meta": {
            "phase": "Phase 7A — Diverse Rollout Dry Run",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "total_candidates": len(CANDIDATE_PIDS),
            "safe": len(safe),
            "review_only": len(review),
            "reject": len(reject),
        },
        "type_distribution": dict(type_distribution),
        "products": results,
    }

    # Write JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"JSON written: {OUT_JSON}")

    # Write Markdown report
    write_md_report(output, safe, review, reject)
    print(f"MD written: {OUT_MD}")

    # Summary
    print()
    print("=== PHASE 7A DRY RUN SUMMARY ===")
    print(f"SAFE_FOR_PHASE7A: {len(safe)}")
    print(f"REVIEW_ONLY:      {len(review)}")
    print(f"REJECT:           {len(reject)}")
    print(f"Type distribution: {dict(type_distribution)}")
    print()
    if len(safe) >= 10:
        print("VERDICT: READY_FOR_PHASE7A_T3_APPROVAL")
    else:
        print("VERDICT: NEED_MORE_CANDIDATE_REVIEW")


def write_md_report(output, safe, review, reject):
    meta = output["meta"]
    products = output["products"]
    type_dist = output["type_distribution"]

    LIVE_5 = [
        ("C3","9688660312377","אוברול ג׳ינס דגם אתי","type-romper"),
        ("C2","9874906349881","אוברול ג'ינס מתוק דגם זוהר","type-romper"),
        ("C4","9895864205625","אוברול ג'ינס יוניסקס דגם שלו","type-romper"),
        ("C5","9687579033913","אוברול לבבות דגם הילה","type-romper"),
        ("C1","9688932909369","אוברול אריה חמוד דגם שמר","type-romper"),
    ]

    lines = [
        "# Layer 7 — Phase 7A Diverse Rollout Candidates",
        f"**תאריך:** {meta['date']}",
        "**Phase:** 7A — Dry Run — DRY RUN ONLY — אין כתיבה ל-Shopify",
        "",
        "---",
        "",
        "## 1. מצב מערכת",
        "",
        "| פרמטר | ערך |",
        "|-------|-----|",
        "| Phase 6 batch 1+2 | COMPLETE — PASS |",
        "| Shopify live | YES — **5 products** (C3, C2, C4, C5, C1) |",
        "| כל 5 מוצרים חיים | type-romper בלבד |",
        "| Phase 7A | DRY RUN |",
        "| collections | NOT OPEN |",
        "| Mega Menu | NO |",
        "| כתיבה ל-Shopify | NO |",
        "",
        "---",
        "",
        "## 2. למה לא collections עדיין",
        "",
        "| סיבה | פרטים |",
        "|------|-------|",
        "| 5 מוצרים חיים בלבד (1.3% מהinventory) | Phase 7 (50+) נדרש לפני Phase 8 |",
        "| כל 5 מוצרים = type-romper | אין גיוון — collection = לא ערך ללקוח |",
        "| spec דורש Phase 7 לפני Phase 8 | Collections = downstream phase |",
        "| navigation עם item אחד | UX confusion |",
        "",
        "**target לפני collections:** 50+ מוצרים מ-4+ סוגים שונים.",
        "",
        "---",
        "",
        "## 3. מועמדים — 20 מוצרים",
        "",
        "| # | product_id | כותרת | type | verdict | score |",
        "|---|-----------|-------|------|---------|-------|",
    ]

    for i, r in enumerate(products, 1):
        title = r.get("title", "")[:45]
        typ   = r.get("type", "—")
        verd  = r.get("verdict", "—")
        score = r.get("score", 0)
        pid   = r.get("product_id", "")
        lines.append(f"| {i} | {pid} | {title} | {typ} | {verd} | {score} |")

    lines += [
        "",
        "---",
        "",
        "## 4. פילוח לפי סוג מוצר",
        "",
        "| type | מוצרים בbatch זה | מוצרים חיים |",
        "|------|----------------|------------|",
    ]
    all_types = ["type-romper","type-dress","type-set","type-bodysuit","type-pants","type-hat","type-shoes","type-sneakers","type-sandals","type-coat"]
    for t in all_types:
        batch_cnt = type_dist.get(t, 0)
        live_cnt = sum(1 for _, _, _, lt in LIVE_5 if lt == t)
        if batch_cnt > 0 or live_cnt > 0:
            lines.append(f"| {t} | {batch_cnt} | {live_cnt} |")

    lines += [
        "",
        "---",
        "",
        "## 5. פרטים לכל מוצר",
        "",
    ]

    for r in products:
        pid    = r.get("product_id", "")
        title  = r.get("title", "")
        typ    = r.get("type", "—")
        verd   = r.get("verdict", "—")
        score  = r.get("score", 0)
        reason = r.get("reason", "")
        has_yaml = r.get("has_yaml", False)
        size_status = r.get("size_status", "—")
        live_tags = r.get("proposed_live_tags", [])
        trace = r.get("source_trace", {})

        lines += [
            f"### {pid} — {title}",
            f"**type:** {typ} | **score:** {score} | **verdict:** `{verd}` | **has_yaml:** {has_yaml}",
        ]
        if reason:
            lines.append(f"**reason:** {reason}")
        lines.append(f"**size_status:** {size_status}")
        if live_tags:
            lines.append(f"**proposed tags ({len(live_tags)}):** `{', '.join(live_tags)}`")

        if trace:
            lines.append("")
            lines.append("**source trace:**")
            lines.append("| tag | source | rule | conf |")
            lines.append("|-----|--------|------|------|")
            for tag, info in trace.items():
                if not tag.endswith("unknown"):
                    lines.append(f"| {tag} | {info['source']} | {info['rule']} | {info['conf']} |")

        lines.append("")

    # Section 6 — SAFE list
    lines += [
        "---",
        "",
        "## 6. רשימת SAFE_FOR_PHASE7A",
        "",
        "| product_id | כותרת | type | score |",
        "|-----------|-------|------|-------|",
    ]
    for r in safe:
        lines.append(f"| {r['product_id']} | {r.get('title','')[:50]} | {r.get('type','—')} | {r.get('score',0)} |")

    # Section 7 — diversity check
    safe_types = set(r.get("type","") for r in safe)
    safe_type_count = len([t for t in safe_types if t and not t.endswith("unknown")])
    diverse_ok = safe_type_count >= 3 and len(safe) >= 10
    lines += [
        "",
        "---",
        "",
        "## 7. בדיקת גיוון",
        "",
        f"| בדיקה | תוצאה |",
        f"|-------|-------|",
        f"| מספר SAFE_FOR_PHASE7A | {len(safe)} |",
        f"| סוגי מוצר ב-SAFE | {safe_type_count} ({', '.join(t for t in safe_types if t and not t.endswith('unknown'))}) |",
        f"| לפחות 10 SAFE מגוונים | {'כן ✅' if diverse_ok else 'לא ❌'} |",
    ]

    # Section 8 — batch recommendation
    lines += [
        "",
        "---",
        "",
        "## 8. המלצת batch חי ראשון של Phase 7A",
        "",
        "**כלל:** לא 20 מוצרים live בבת אחת — batch של 10 בלבד.",
        "",
        "| המלצה | פרטים |",
        "|-------|-------|",
        "| גודל batch | 10 מוצרים (לא 20) |",
        "| עדיפות | SAFE_FOR_PHASE7A בלבד |",
        "| גיוון | לפחות 3 סוגים שונים בbatch |",
        "| כלל | 1 מוצר בכל פעם עם verify |",
        "",
        "**batch מומלץ (10 הראשונים):**",
        "",
        "| # | product_id | כותרת | type | score |",
        "|---|-----------|-------|------|-------|",
    ]
    top10 = sorted(safe, key=lambda r: -r.get("score", 0))[:10]
    for i, r in enumerate(top10, 1):
        lines.append(f"| {i} | {r['product_id']} | {r.get('title','')[:45]} | {r.get('type','—')} | {r.get('score',0)} |")

    # Section 9 — backup/verify/rollback plan
    lines += [
        "",
        "---",
        "",
        "## 9. Backup / Verify / Rollback Plan",
        "",
        "| שלב | תיאור |",
        "|-----|-------|",
        "| גיבוי | GET tags לכל מוצר → שמור JSON לפני כל כתיבה |",
        "| כתיבה | PUT tags אחד בכל פעם (merge: current + new) |",
        "| verify | GET אחרי כל PUT — בדוק כל tag קיים, אין age-*, title לא השתנה |",
        "| rollback | אם verify נכשל → PUT tags מקוריות מהגיבוי |",
        "| מוצר פגוע | עצור batch, rollback מיידי |",
        "",
    ]

    # Section 10 — verdict
    final_verdict = "READY_FOR_PHASE7A_T3_APPROVAL" if diverse_ok else "NEED_MORE_CANDIDATE_REVIEW"
    lines += [
        "---",
        "",
        "## 10. Verdict סופי",
        "",
        f"**{final_verdict}**",
        "",
        "| בדיקה | תוצאה |",
        "|-------|-------|",
        f"| SAFE_FOR_PHASE7A | {len(safe)} |",
        f"| REVIEW_ONLY | {len(review)} |",
        f"| REJECT | {len(reject)} |",
        f"| גיוון סוגים ב-SAFE | {safe_type_count} סוגים |",
        f"| לפחות 10 SAFE | {'כן ✅' if len(safe) >= 10 else 'לא ❌'} |",
        f"| כתיבה ל-Shopify | **NO** |",
        f"| collections נוצרו | **NO** |",
        f"| Mega Menu נוצר | **NO** |",
        "",
        "---",
        "",
        "*Phase 7A dry run only — אין שינויים ב-Shopify. כל ביצוע מותנה ב-T3 approval.*",
    ]

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
