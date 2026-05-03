#!/usr/bin/env python3
# Layer 6 Phase 2 — Source Mapping Sample (30 products)
import json, os, re, yaml, sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = Path("C:/Projects/baby-mania-agent")
PHASE0 = BASE / "output/tags/phase0-raw-products.json"
YAML_DIR = BASE / "shared/product-context"
OUT_JSON = BASE / "output/tags/phase2-source-map-sample-30.json"
OUT_MD   = BASE / "output/tags/phase2-source-map-sample-30.md"

load_dotenv(Path.home() / "Desktop/shopify-token/.env")
TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
API   = f"https://{SHOP}/admin/api/2024-10"

# ── Taxonomy allowed values ────────────────────────────────────────────────────
TYPE_VALUES = [
    "type-romper","type-set","type-bodysuit","type-pajama","type-cardigan",
    "type-coat","type-dress","type-shorts","type-pants","type-shirt",
    "type-hat","type-socks","type-shoes","type-sandals","type-boots",
    "type-slippers","type-blanket","type-bag","type-toy","type-doll","type-other"
]
AGE_VALUES = [
    "age-0-3m","age-3-6m","age-6-12m","age-12-18m","age-18-24m",
    "age-2-3y","age-3-5y","age-5y-plus"
]
SEASON_VALUES = ["season-summer","season-winter","season-spring-fall","season-all-year"]
FABRIC_VALUES = ["fabric-cotton","fabric-velvet","fabric-fleece","fabric-linen",
                 "fabric-knit","fabric-denim","fabric-muslin","fabric-synthetic"]
OCC_VALUES    = ["occ-everyday","occ-gift","occ-special-event","occ-holiday","occ-beach","occ-sport"]
GENDER_VALUES = ["gender-girl","gender-boy","gender-unisex"]
STYLE_VALUES  = ["style-elegant","style-casual","style-cartoon","style-floral",
                 "style-striped","style-animal-print","style-minimal","style-boho"]

REQUIRED_CATS   = {"CAT-A","CAT-B","CAT-C","CAT-F"}
RECOMMENDED_CATS = {"CAT-D","CAT-E","CAT-G"}

# ── Load phase0 products ───────────────────────────────────────────────────────
with open(PHASE0, encoding="utf-8") as f:
    ph0 = json.load(f)
products_map = {str(p["id"]): p for p in ph0["products"]}

# ── Load YAMLs ─────────────────────────────────────────────────────────────────
yaml_ids = set()
yaml_data = {}
for yf in YAML_DIR.glob("*.yaml"):
    pid = yf.stem
    yaml_ids.add(pid)
    with open(yf, encoding="utf-8") as f:
        try:
            yaml_data[pid] = yaml.safe_load(f)
        except Exception:
            yaml_data[pid] = {}

# ── Categorize active products ─────────────────────────────────────────────────
def has_yaml(pid):
    return str(pid) in yaml_ids

SHOE_WORDS = ["shoes","shoe","boot","boots","sandal","sandals","slipper","slippers","sneaker","footwear"]
REBORN_WORDS = ["reborn","doll","silicone-baby","vinyl-baby","realistic-baby","newborn-doll"]
TOY_WORDS = ["toy","toys","stuffed","plush","teddy","musical"]

def classify_product(p):
    h = p["handle"].lower()
    t = p["title"].lower()
    pid = str(p["id"])
    combined = h + " " + t
    if any(w in combined for w in REBORN_WORDS):
        return "reborn"
    if any(w in combined for w in TOY_WORDS) and not any(w in combined for w in
            ["romper","bodysuit","pajama","suit","set","dress","pants","shirt","coat","cardigan"]):
        return "toy"
    if any(w in combined for w in SHOE_WORDS):
        return "shoes"
    return "clothing"

clothing_yaml, shoes_yaml, reborn_gap, toy_gap, gap_other = [], [], [], [], []

for p in ph0["products"]:
    pid = str(p["id"])
    cat = classify_product(p)
    has_y = has_yaml(pid)
    if cat == "reborn":
        reborn_gap.append(p)
    elif cat == "toy":
        toy_gap.append(p)
    elif cat == "shoes" and has_y:
        shoes_yaml.append(p)
    elif cat == "clothing" and has_y:
        clothing_yaml.append(p)
    elif not has_y:
        gap_other.append(p)

print(f"clothing+yaml: {len(clothing_yaml)}, shoes+yaml: {len(shoes_yaml)}, "
      f"reborn: {len(reborn_gap)}, toys: {len(toy_gap)}, gap: {len(gap_other)}")

# ── Sample selection ───────────────────────────────────────────────────────────
import random
random.seed(42)

sample_clothing = clothing_yaml[:10] if len(clothing_yaml) >= 10 else clothing_yaml
sample_shoes    = shoes_yaml[:10]    if len(shoes_yaml) >= 10    else shoes_yaml
sample_reborn   = (reborn_gap + toy_gap)[:5]
# YAML_GAP: 5 products with no YAML (mix of categories)
sample_gap      = gap_other[:5]

sample = []
for p in sample_clothing: sample.append((p, "clothing_yaml"))
for p in sample_shoes:    sample.append((p, "shoes_yaml"))
for p in sample_reborn:
    cat = classify_product(p)
    sample.append((p, "reborn_gap" if cat=="reborn" else "toy_gap"))
for p in sample_gap:      sample.append((p, "gap_clothing"))

print(f"Sample size: {len(sample)}")

# ── Fetch product details from Shopify ────────────────────────────────────────
def shopify_get(pid):
    url = f"{API}/products/{pid}.json"
    r = requests.get(url, headers={"X-Shopify-Access-Token": TOKEN})
    if r.status_code == 200:
        return r.json().get("product", {})
    return {}

details_cache = {}
for p, grp in sample:
    pid = str(p["id"])
    print(f"  Fetching {pid}...", end=" ", flush=True)
    d = shopify_get(pid)
    details_cache[pid] = d
    print(d.get("product_type","") or "no-type")

# ── Source mapping logic ───────────────────────────────────────────────────────

def norm(s):
    return s.lower().strip() if s else ""

def text_sources(pid, d):
    """Returns dict of text sources for inference."""
    title = norm(d.get("title",""))
    handle = norm(d.get("handle",""))
    body = norm(re.sub(r"<[^>]+>","", d.get("body_html","") or ""))[:600]
    tags_existing = [norm(t) for t in (d.get("tags","") or "").split(",") if t.strip()]
    yd = yaml_data.get(pid, {}) or {}
    yaml_desc = norm(yd.get("description_raw","") or "")[:600]
    yaml_fabric = norm(yd.get("fabric_type","") or "")
    yaml_use = norm(yd.get("main_use","") or "")
    return {
        "title": title,
        "handle": handle,
        "body": body,
        "tags_existing": tags_existing,
        "yaml_desc": yaml_desc,
        "yaml_fabric": yaml_fabric,
        "yaml_use": yaml_use,
    }

def find_type(pid, d, src):
    """CAT-A: Product Type"""
    title = src["title"]
    handle = src["handle"]
    body = src["body"]
    existing = src["tags_existing"]

    rules = [
        ("type-romper",   ["romper","jumpsuit","crawling suit","overall","אוברול"]),
        ("type-bodysuit", ["bodysuit","onesie","body suit"]),
        ("type-set",      ["set","suit set","baby set","outfit set","2-piece","3-piece","2 piece","3 piece"]),
        ("type-pajama",   ["pajama","pyjama","sleepwear","sleep suit","nightwear"]),
        ("type-dress",    ["dress","שמלה"]),
        ("type-coat",     ["coat","jacket","outwear","outercoat"]),
        ("type-cardigan", ["cardigan","sweatshirt","hoodie","sweater","knitwear"]),
        ("type-shorts",   ["shorts","short pant"]),
        ("type-pants",    ["pants","trousers","legging","leggings"]),
        ("type-shirt",    ["shirt","top","t-shirt","blouse","tee"]),
        ("type-hat",      ["hat","cap","beanie","bonnet","כובע"]),
        ("type-socks",    ["socks","sock","גרביים"]),
        ("type-shoes",    ["shoes","shoe","sneaker","נעליים","נעל"]),
        ("type-sandals",  ["sandal","sandals","סנדל"]),
        ("type-boots",    ["boot","boots","מגף"]),
        ("type-slippers", ["slipper","slippers","slip-on"]),
        ("type-blanket",  ["blanket","swaddle","sleeping bag"]),
        ("type-bag",      ["bag","backpack","תיק"]),
        ("type-doll",     ["doll","reborn","silicone baby","vinyl baby","בובה"]),
        ("type-toy",      ["toy","plush","stuffed","teddy","musical toy"]),
    ]
    combined = title + " " + handle + " " + body
    for tag, keywords in rules:
        for kw in keywords:
            if kw in combined:
                source_field = "title" if kw in title else ("handle" if kw in handle else "body")
                return tag, 0.9, source_field
    # fallback: check existing tags
    for et in existing:
        for tag, keywords in rules:
            for kw in keywords:
                if kw in et:
                    return tag, 0.7, "existing_tag"
    return "type-other", 0.5, "fallback"

def find_age(pid, d, src):
    """CAT-B: Age Group"""
    combined = src["title"] + " " + src["handle"] + " " + src["body"] + " " + src["yaml_desc"]
    age_patterns = [
        ("age-0-3m",   [r"\b0[-–]3\s*m", r"\b0\s*to\s*3\s*month", r"newborn.*3.*month", r"3\s*month"]),
        ("age-3-6m",   [r"\b3[-–]6\s*m", r"3\s*to\s*6\s*month"]),
        ("age-6-12m",  [r"\b6[-–]12\s*m", r"6\s*to\s*12\s*month"]),
        ("age-12-18m", [r"\b12[-–]18\s*m", r"12\s*to\s*18\s*month"]),
        ("age-18-24m", [r"\b18[-–]24\s*m", r"18\s*to\s*24\s*month"]),
        ("age-2-3y",   [r"\b2[-–]3\s*y", r"2\s*to\s*3\s*year", r"\b2\s*year"]),
        ("age-3-5y",   [r"\b3[-–]5\s*y", r"3\s*to\s*5\s*year"]),
        ("age-5y-plus",[r"\b5\+\s*y", r"5\s*year\s*(and\s*)?up"]),
    ]
    # Also check for Hebrew age indicators
    heb_age = [
        ("age-0-3m",   ["0-3 חודשים","0 עד 3 חודשים","3 חודשים","3M","3m"]),
        ("age-3-6m",   ["3-6 חודשים","3 עד 6 חודשים"]),
        ("age-6-12m",  ["6-12 חודשים","6 עד 12 חודשים"]),
        ("age-12-18m", ["12-18 חודשים","12 עד 18 חודשים"]),
        ("age-18-24m", ["18-24 חודשים","18 עד 24 חודשים"]),
        ("age-2-3y",   ["2-3 שנים","2 עד 3 שנים"]),
    ]

    found = []
    for tag, patterns in age_patterns:
        for pat in patterns:
            if re.search(pat, combined, re.IGNORECASE):
                found.append(tag)
                break

    # Hebrew check on yaml_desc
    yaml_desc = src["yaml_desc"]
    for tag, phrases in heb_age:
        for ph in phrases:
            if ph in yaml_desc:
                if tag not in found:
                    found.append(tag)

    # Deduplicate, pick primary (widest range or first found)
    if not found:
        # Check for general "newborn" = 0-3m
        if "newborn" in combined or "0-18" in combined:
            return [("age-0-3m",0.6,"title_heuristic")], True  # multi-age product
        return [], False
    if len(found) > 1:
        return [(t, 0.85, "title_regex") for t in found], True
    return [(found[0], 0.9, "title_regex")], False

def find_season(pid, d, src, type_tag=""):
    """CAT-C: Season"""
    combined = src["title"] + " " + src["handle"] + " " + src["body"] + " " + src["yaml_desc"]
    cl = combined.lower()

    # Swimwear → summer is allowed
    swim_words = ["swimwear","swimsuit","swim","bathing suit","bikini","beachwear"]
    if any(w in cl for w in swim_words):
        return "season-summer", 0.9, "type_inference_swimwear"

    season_rules = [
        ("season-summer", ["summer","warm weather","hot weather","light fabric","לקיץ","קיץ"]),
        ("season-winter", ["winter","warm","thick","fleece","velvet","woolen","fuzzy","חורף","לחורף","חם"]),
        ("season-spring-fall", ["spring","autumn","fall","transitional","spring-fall","אביב","סתיו"]),
        ("season-all-year",  ["all year","all-year","year round","year-round","all season","כל עונות"]),
    ]
    for tag, keywords in season_rules:
        for kw in keywords:
            if kw in cl:
                source_field = "title" if kw in src["title"].lower() else ("yaml_desc" if kw in src["yaml_desc"].lower() else "body")
                return tag, 0.85, source_field
    return None, 0, ""

def find_fabric(pid, d, src, has_y, yaml_gap):
    """CAT-D: Fabric — BLOCKED for yaml_gap without explicit title source"""
    # Check yaml_fabric first (most reliable)
    yaml_fab = src["yaml_fabric"]
    if yaml_fab and not yaml_gap:
        fab_map = {
            "cotton": "fabric-cotton", "כותנה": "fabric-cotton",
            "velvet": "fabric-velvet", "קטיפה": "fabric-velvet",
            "fleece": "fabric-fleece",
            "linen": "fabric-linen", "פשתן": "fabric-linen",
            "knit": "fabric-knit",
            "denim": "fabric-denim", "ג'ינס": "fabric-denim",
            "muslin": "fabric-muslin",
        }
        for kw, tag in fab_map.items():
            if kw in yaml_fab:
                return tag, 0.95, "yaml_fabric_field"

    # Check title for explicit fabric mention
    title = src["title"]
    fab_title_map = {
        "cotton": "fabric-cotton", "100% cotton": "fabric-cotton",
        "velvet": "fabric-velvet",
        "fleece": "fabric-fleece",
        "linen": "fabric-linen",
        "knit": "fabric-knit",
        "denim": "fabric-denim",
        "muslin": "fabric-muslin",
    }
    for kw, tag in fab_title_map.items():
        if kw in title.lower():
            return tag, 0.9, "title"

    if yaml_gap:
        return None, 0, "BLOCKED:yaml_gap_no_explicit_source"

    # Check yaml_desc / body for fabric
    combined = src["yaml_desc"] + " " + src["body"]
    fab_body_map = {
        "100% cotton": "fabric-cotton", "pure cotton": "fabric-cotton",
        "כותנה": "fabric-cotton",
        "velvet": "fabric-velvet", "קטיפה": "fabric-velvet",
        "fleece": "fabric-fleece",
        "linen": "fabric-linen",
        "knit": "fabric-knit",
        "denim": "fabric-denim",
        "muslin": "fabric-muslin",
    }
    for kw, tag in fab_body_map.items():
        if kw in combined.lower():
            source = "yaml_desc" if kw in src["yaml_desc"].lower() else "body"
            return tag, 0.8, source
    return None, 0, ""

def find_occasion(pid, d, src, type_tag=""):
    """CAT-E: Occasion"""
    combined = src["title"] + " " + src["handle"] + " " + src["body"] + " " + src["yaml_desc"]
    cl = combined.lower()

    occ_rules = [
        ("occ-gift",     ["gift","baby shower","מתנה","מתנת לידה","baby gift"]),
        ("occ-special-event", ["party","wedding","ceremony","special occasion","formal","אירוע","חג"]),
        ("occ-holiday",  ["holiday","christmas","purim","chanukah","eid","פורים","חנוכה"]),
        ("occ-beach",    ["beach","pool","swim","bathing","ים","בריכה"]),
        ("occ-sport",    ["sport","athletic","active","gym","outdoor"]),
        ("occ-everyday", ["everyday","daily","casual","day-to-day","יומיומי"]),
    ]
    found = []
    for tag, keywords in occ_rules:
        for kw in keywords:
            if kw in cl:
                found.append((tag, 0.8, "body" if kw in src["body"].lower() else "title"))
                break
    if not found:
        # Default to everyday for clothing
        if type_tag in ["type-romper","type-bodysuit","type-set","type-dress","type-shirt","type-pants","type-shorts"]:
            return [("occ-everyday", 0.6, "type_default")]
    return found[:2]  # max 2

def find_gender(pid, d, src):
    """CAT-F: Gender — NO color inference"""
    combined = src["title"] + " " + src["handle"]
    cl = combined.lower()
    existing = src["tags_existing"]

    # Explicit gender words only
    girl_words = ["girl","girls","baby girl","female","princess","little girl","בת","ילדה"]
    boy_words  = ["boy","boys","baby boy","male","little boy","בן","ילד"]
    unisex_words = ["unisex","neutral","gender neutral","יוניסקס","ניוטרלי"]

    # Check existing tags first
    for et in existing:
        if any(w in et for w in ["girls-clothing","girl","בנות"]):
            return "gender-girl", 0.9, "existing_tag"
        if any(w in et for w in ["boys-clothing","boy","בנים"]):
            return "gender-boy", 0.9, "existing_tag"
        if "neutral" in et or "unisex" in et:
            return "gender-unisex", 0.9, "existing_tag"

    has_girl = any(w in cl for w in girl_words)
    has_boy  = any(w in cl for w in boy_words)
    has_uni  = any(w in cl for w in unisex_words)

    if has_uni or (has_girl and has_boy):
        return "gender-unisex", 0.85, "title"
    if has_girl:
        return "gender-girl", 0.9, "title"
    if has_boy:
        return "gender-boy", 0.9, "title"

    # Existing tag check for neutral-baby-outfit
    for et in existing:
        if "neutral" in et:
            return "gender-unisex", 0.85, "existing_tag"
    return "gender-unisex", 0.6, "default_unisex"

def find_style(pid, d, src):
    """CAT-G: Style — explicit words only"""
    combined = src["title"] + " " + src["handle"] + " " + src["body"] + " " + src["yaml_desc"]
    cl = combined.lower()

    style_rules = [
        ("style-elegant",      ["elegant","formal","luxury","luxury","אלגנטי","מפואר"]),
        ("style-casual",       ["casual","everyday","basic","simple","יומיומי","פשוט"]),
        ("style-cartoon",      ["cartoon","character","batman","disney","mickey","winnie","דמות"]),
        ("style-floral",       ["floral","flower","rose","blossom","פרח","פרחים"]),
        ("style-striped",      ["strip","stripe","striped","פסים"]),
        ("style-animal-print", ["animal print","leopard","zebra","tiger","animal","bear print",
                                 "dinosaur","dino","rabbit","bunny","duck","fox"]),
        ("style-minimal",      ["minimal","minimalist","clean","solid color","plain","מינימליסטי"]),
        ("style-boho",         ["boho","bohemian","ethnic","folk","boho-chic"]),
    ]
    for tag, keywords in style_rules:
        for kw in keywords:
            if kw in cl:
                source = "title" if kw in src["title"].lower() else ("body" if kw in src["body"].lower() else "handle")
                return tag, 0.8, source
    return None, 0, ""

def quality_score(proposed_tags, missing_required):
    req_present = len(REQUIRED_CATS) - len(missing_required)
    rec_tags = [t for t in proposed_tags
                if any(t["tag"].startswith(p) for p in ["fabric-","occ-","style-"])]
    rec_present = min(len(rec_tags), 3)
    confidences = [t["confidence"] for t in proposed_tags] if proposed_tags else [0]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    score = (req_present / 4) * 60 + (rec_present / 3) * 20 + avg_conf * 20
    if score >= 75:
        status = "PASS"
    elif score >= 50:
        status = "NEEDS_REVIEW"
    else:
        status = "BLOCKED"
    return round(score, 1), status, req_present, rec_present, round(avg_conf, 3)

# ── Process each product ───────────────────────────────────────────────────────
results = []

for p, grp in sample:
    pid = str(p["id"])
    d   = details_cache.get(pid, {})
    has_y = has_yaml(pid)
    yaml_gap = not has_y
    yd  = yaml_data.get(pid, {}) or {}

    # Merge d with p (phase0 has cleaner tags list sometimes)
    if not d:
        d = p
    src = text_sources(pid, d)

    proposed = []
    blocked  = []

    # CAT-A: Type
    type_tag, type_conf, type_src = find_type(pid, d, src)
    proposed.append({"tag": type_tag, "category": "CAT-A", "confidence": type_conf,
                     "source": type_src, "rule": "title_keyword"})

    # CAT-B: Age
    age_result, multi_age = find_age(pid, d, src)
    if age_result:
        for (age_tag, age_conf, age_src) in age_result:
            proposed.append({"tag": age_tag, "category": "CAT-B", "confidence": age_conf,
                             "source": age_src, "rule": "regex_age_range"})
    # else: missing

    # CAT-C: Season
    season_tag, season_conf, season_src = find_season(pid, d, src, type_tag)
    if season_tag:
        proposed.append({"tag": season_tag, "category": "CAT-C", "confidence": season_conf,
                         "source": season_src, "rule": "keyword"})

    # CAT-D: Fabric
    fabric_tag, fabric_conf, fabric_src = find_fabric(pid, d, src, has_y, yaml_gap)
    if fabric_tag:
        proposed.append({"tag": fabric_tag, "category": "CAT-D", "confidence": fabric_conf,
                         "source": fabric_src, "rule": "explicit_source"})
    elif fabric_src.startswith("BLOCKED"):
        blocked.append({"tag": "fabric-*", "category": "CAT-D",
                        "reason": fabric_src, "rule": "yaml_gap_fabric_block"})

    # CAT-E: Occasion
    occ_results = find_occasion(pid, d, src, type_tag)
    for (occ_tag, occ_conf, occ_src) in occ_results:
        proposed.append({"tag": occ_tag, "category": "CAT-E", "confidence": occ_conf,
                         "source": occ_src, "rule": "keyword"})

    # CAT-F: Gender
    gender_tag, gender_conf, gender_src = find_gender(pid, d, src)
    proposed.append({"tag": gender_tag, "category": "CAT-F", "confidence": gender_conf,
                     "source": gender_src, "rule": "explicit_keyword_no_color"})

    # CAT-G: Style
    style_tag, style_conf, style_src = find_style(pid, d, src)
    if style_tag:
        proposed.append({"tag": style_tag, "category": "CAT-G", "confidence": style_conf,
                         "source": style_src, "rule": "keyword"})

    # Determine missing required
    covered_cats = {t["category"] for t in proposed}
    missing_req = [c for c in REQUIRED_CATS if c not in covered_cats]

    # Quality score
    score, status, req_pres, rec_pres, avg_conf_val = quality_score(proposed, missing_req)

    results.append({
        "product_id": pid,
        "title": d.get("title") or p["title"],
        "handle": d.get("handle") or p["handle"],
        "product_group": grp,
        "has_yaml": has_y,
        "yaml_gap": yaml_gap,
        "source_status": "limited" if yaml_gap else "full",
        "current_tags": [t.strip() for t in (d.get("tags","") or "").split(",") if t.strip()],
        "proposed_tags": proposed,
        "blocked_tags": blocked,
        "missing_required_categories": missing_req,
        "quality_precheck": {
            "required_categories_present": req_pres,
            "recommended_categories_present": rec_pres,
            "avg_confidence": avg_conf_val,
            "estimated_score": score,
            "status": status,
        }
    })

# ── Write JSON ─────────────────────────────────────────────────────────────────
output_json = {
    "meta": {
        "phase": "Phase 2 — Source Mapping Sample",
        "date": "2026-05-05",
        "sample_size": len(results),
        "groups": {
            "clothing_yaml": sum(1 for r in results if r["product_group"]=="clothing_yaml"),
            "shoes_yaml":    sum(1 for r in results if r["product_group"]=="shoes_yaml"),
            "reborn_gap":    sum(1 for r in results if r["product_group"]=="reborn_gap"),
            "toy_gap":       sum(1 for r in results if r["product_group"]=="toy_gap"),
            "gap_clothing":  sum(1 for r in results if r["product_group"]=="gap_clothing"),
        }
    },
    "products": results
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)
print(f"\nWrote {OUT_JSON}")

# ── Write MD ───────────────────────────────────────────────────────────────────
pass_count   = sum(1 for r in results if r["quality_precheck"]["status"]=="PASS")
review_count = sum(1 for r in results if r["quality_precheck"]["status"]=="NEEDS_REVIEW")
blocked_count = sum(1 for r in results if r["quality_precheck"]["status"]=="BLOCKED")

md_lines = [
    "# Layer 6 — Phase 2 Source Mapping Sample",
    f"## BabyMania Organic | Date: 2026-05-05 | Status: COMPLETE",
    "",
    "---",
    "",
    "## 1. Sample Summary",
    "",
    f"| מדד | ערך |",
    f"|-----|-----|",
    f"| סה\"כ מוצרים בsample | **{len(results)}** |",
    f"| clothing + YAML | **{output_json['meta']['groups']['clothing_yaml']}** |",
    f"| shoes + YAML | **{output_json['meta']['groups']['shoes_yaml']}** |",
    f"| reborn / toys (YAML_GAP) | **{output_json['meta']['groups']['reborn_gap'] + output_json['meta']['groups']['toy_gap']}** |",
    f"| YAML_GAP clothing | **{output_json['meta']['groups']['gap_clothing']}** |",
    f"| Quality PASS | **{pass_count}** |",
    f"| Quality NEEDS_REVIEW | **{review_count}** |",
    f"| Quality BLOCKED | **{blocked_count}** |",
    "",
    "---",
    "",
    "## 2. Source Mapping Per Product",
    "",
]

for r in results:
    grp_label = r["product_group"].upper()
    yaml_label = "HAS_YAML" if r["has_yaml"] else "YAML_GAP"
    score = r["quality_precheck"]["estimated_score"]
    status = r["quality_precheck"]["status"]
    status_icon = "✅" if status=="PASS" else ("⚠️" if status=="NEEDS_REVIEW" else "❌")

    md_lines.append(f"### [{grp_label}] {r['title'][:80]}")
    md_lines.append(f"**ID:** `{r['product_id']}` | **Handle:** `{r['handle'][:60]}`")
    md_lines.append(f"**Group:** {r['product_group']} | **YAML:** {yaml_label} | **Score:** {score} {status_icon} {status}")
    md_lines.append("")

    md_lines.append("**Current tags:**")
    if r["current_tags"]:
        md_lines.append(", ".join(f"`{t}`" for t in r["current_tags"][:10]))
    else:
        md_lines.append("_(none)_")
    md_lines.append("")

    md_lines.append("**Proposed tags:**")
    md_lines.append("| Tag | Category | Confidence | Source |")
    md_lines.append("|-----|---------|------------|--------|")
    for t in r["proposed_tags"]:
        conf_pct = f"{int(t['confidence']*100)}%"
        md_lines.append(f"| `{t['tag']}` | {t['category']} | {conf_pct} | `{t['source']}` |")

    if r["blocked_tags"]:
        md_lines.append("")
        md_lines.append("**Blocked tags:**")
        for bt in r["blocked_tags"]:
            md_lines.append(f"- `{bt['tag']}` — {bt['reason']}")

    if r["missing_required_categories"]:
        md_lines.append("")
        md_lines.append(f"**Missing required:** {', '.join(r['missing_required_categories'])}")

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

md_lines.append("## 3. Taxonomy Coverage Analysis")
md_lines.append("")
# Count coverage by category
cat_coverage = {}
for cat in ["CAT-A","CAT-B","CAT-C","CAT-D","CAT-E","CAT-F","CAT-G"]:
    count = sum(1 for r in results if any(t["category"]==cat for t in r["proposed_tags"]))
    cat_coverage[cat] = count

cat_names = {
    "CAT-A": "Product Type (type-)", "CAT-B": "Age Group (age-)",
    "CAT-C": "Season (season-)", "CAT-D": "Fabric (fabric-)",
    "CAT-E": "Occasion (occ-)", "CAT-F": "Gender (gender-)",
    "CAT-G": "Style (style-)"
}
md_lines.append("| קטגוריה | כיסוי | % | Required |")
md_lines.append("|---------|-------|---|----------|")
for cat, count in cat_coverage.items():
    pct = round(count/len(results)*100)
    req = "✅ Required" if cat in REQUIRED_CATS else "Recommended"
    md_lines.append(f"| {cat_names[cat]} | {count}/{len(results)} | {pct}% | {req} |")

md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append("## 4. Phase 2 Observations")
md_lines.append("")

# Key observations
obs = []
avg_score = round(sum(r["quality_precheck"]["estimated_score"] for r in results)/len(results),1)
obs.append(f"- ממוצע quality score: **{avg_score}** | PASS: {pass_count} | NEEDS_REVIEW: {review_count} | BLOCKED: {blocked_count}")
gap_blocked = sum(1 for r in results if r["yaml_gap"] and any(bt["category"]=="CAT-D" for bt in r["blocked_tags"]))
obs.append(f"- YAML_GAP fabric blocks: **{gap_blocked}** מוצרים — CAT-D חסום ללא מקור מפורש בכותרת")
multi_age_count = sum(1 for r in results if sum(1 for t in r["proposed_tags"] if t["category"]=="CAT-B") > 1)
obs.append(f"- מוצרים עם טווח גיל מרובה: **{multi_age_count}** — מוצרים 0-18M ו-0-24M מקבלים multiple age tags")
no_season = sum(1 for r in results if not any(t["category"]=="CAT-C" for t in r["proposed_tags"]))
obs.append(f"- ללא season tag: **{no_season}** מוצרים — עונה לא ניתנת להסקה מהכותרת/תיאור")
for o in obs:
    md_lines.append(o)

md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append(f"*Phase 2 Source Mapping Sample הורץ: 2026-05-05 | read-only source analysis | T0 | אין שינוי ב-Shopify*")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Wrote {OUT_MD}")

# Summary
print(f"\n=== PHASE 2 COMPLETE ===")
print(f"Sample: {len(results)} products")
print(f"PASS: {pass_count} | NEEDS_REVIEW: {review_count} | BLOCKED: {blocked_count}")
print(f"Avg score: {avg_score}")
for cat, count in cat_coverage.items():
    print(f"  {cat}: {count}/{len(results)}")
