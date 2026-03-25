#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Intelligence Builder -- BabyMania
=========================================
Combines outputs from:
  01  product-analyzer    → {pid}_analyzer.yaml
  01b visual-analyzer     → {pid}_visual.json

Produces:
  {pid}_intelligence.json

Run after both analyzers, before writing agents (02-05).

Usage:
  python scripts/product_intelligence_builder.py {product_id}
"""

import io
import json
import re
import sys
from pathlib import Path

# Force UTF-8 on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"

try:
    import yaml
except ImportError:
    print("Missing: pip install pyyaml")
    sys.exit(1)

# ── Lookup tables ──────────────────────────────────────────────────────────────

CLOTHING_TYPE_MAP = {
    "romper":    ["romper", "אוברול", "bodysuit", "onesie", "sleepsuit"],
    "dress":     ["dress", "שמלה"],
    "set":       ["set", "suit", "חליפה", "3-piece", "2-piece"],
    "jacket":    ["jacket", "מעיל", "ג׳קט", "coat", "fleece"],
    "pants":     ["pants", "מכנסיים", "leggings", "leggins"],
    "top":       ["top", "חולצה", "shirt", "blouse", "sweater", "סוודר"],
    "hat":       ["hat", "כובע", "beanie"],
    "bodysuit":  ["bodysuit", "בגד-גוף", "body"],
    "swimsuit":  ["swim", "בגד-ים"],
}

PRINT_MAP = {
    "lion":      ["lion", "אריה", "cub"],
    "bear":      ["bear", "דוב", "teddy"],
    "elephant":  ["elephant", "פיל"],
    "giraffe":   ["giraffe", "ג׳ירפה"],
    "bunny":     ["bunny", "rabbit", "ארנב"],
    "fox":       ["fox", "שועל"],
    "deer":      ["deer", "צבי"],
    "star":      ["star", "כוכב"],
    "stripe":    ["stripe", "פס", "stripes"],
    "floral":    ["flower", "פרח", "floral", "flora"],
    "check":     ["check", "משבצת", "plaid", "gingham"],
    "denim":     ["denim", "ג׳ינס", "jeans"],
    "plain":     ["plain", "solid", "basic"],
    "cactus":    ["cactus", "קקטוס"],
    "moon":      ["moon", "ירח", "star-moon"],
    "cloud":     ["cloud", "ענן"],
    "dinosaur":  ["dinosaur", "דינוזאור", "dino"],
    "penguin":   ["penguin", "פינגווין"],
    "rainbow":   ["rainbow", "קשת"],
}

SET_ITEMS_MAP = {
    "hat":      ["hat", "כובע", "beanie", "cap"],
    "mittens":  ["mitten", "כפפות", "glove"],
    "booties":  ["bootie", "boot", "sock", "גרב"],
    "bib":      ["bib", "סינר"],
    "pants":    ["pants", "מכנסיים", "trousers"],
    "shorts":   ["short"],
    "jacket":   ["jacket", "מעיל"],
    "headband": ["headband", "סרט ראש"],
    "vest":     ["vest", "אפוד"],
    "scarf":    ["scarf", "צעיף"],
}

COLOR_MAP = {
    "white":  ["white", "לבן", "ivory", "cream"],
    "beige":  ["beige", "בז׳", "sand", "nude"],
    "gray":   ["gray", "grey", "אפור"],
    "pink":   ["pink", "ורוד"],
    "blue":   ["blue", "כחול", "navy"],
    "green":  ["green", "ירוק"],
    "yellow": ["yellow", "צהוב"],
    "red":    ["red", "אדום"],
    "purple": ["purple", "סגול"],
    "brown":  ["brown", "חום"],
    "black":  ["black", "שחור"],
    "denim":  ["denim", "ג׳ינס"],
}


# ── Pattern matching helpers ───────────────────────────────────────────────────

def _match_map(text: str, lookup: dict) -> str:
    """Return first key whose keywords appear in text (case-insensitive)."""
    text_lower = text.lower()
    for key, keywords in lookup.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return key
    return ""


def _match_map_multi(text: str, lookup: dict) -> list[str]:
    """Return all matching keys."""
    text_lower = text.lower()
    found = []
    for key, keywords in lookup.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(key)
                break
    return found


# ── Stage 01 (analyzer.yaml) parsing ─────────────────────────────────────────

def parse_analyzer(pid: str) -> dict:
    path = STAGE_OUT_DIR / f"{pid}_analyzer.yaml"
    if not path.exists():
        print(f"  [PIB] analyzer not found: {path}")
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    # Fallback: enrich from context YAML if description_raw or product_template_type missing
    ctx_path = CONTEXT_DIR / f"{pid}.yaml"
    if ctx_path.exists():
        ctx = yaml.safe_load(ctx_path.read_text(encoding="utf-8")) or {}
        if not data.get("description_raw"):
            data["description_raw"] = ctx.get("description_raw", "")
        if not data.get("product_template_type"):
            data["product_template_type"] = ctx.get("product_template_type", "")
    return data


# ── Stage 01b (visual.json) parsing ──────────────────────────────────────────

def parse_visual(pid: str) -> dict:
    path = STAGE_OUT_DIR / f"{pid}_visual.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


# ── Inference helpers ─────────────────────────────────────────────────────────

def infer_clothing_type(title: str, handle: str, analyzer: dict) -> str:
    """Detect main garment type from title/handle/product_type."""
    text = f"{title} {handle} {analyzer.get('product_type', '')}"
    return _match_map(text, CLOTHING_TYPE_MAP) or "romper"


def infer_sleeve(handle: str, visual: dict) -> str:
    """Detect sleeve length. Visual result takes priority."""
    # From visual
    v_sleeve = (
        visual.get("visual_structure", {})
        .get("sleeves", {})
        .get("length", "")
    )
    if v_sleeve:
        if "long" in v_sleeve.lower():
            return "long"
        if "short" in v_sleeve.lower() or "sleeveless" in v_sleeve.lower():
            return "short"

    # From handle
    handle_lower = handle.lower()
    if "long-sleeve" in handle_lower or "long_sleeve" in handle_lower:
        return "long"
    if "short-sleeve" in handle_lower or "sleeveless" in handle_lower:
        return "short"
    return ""


def infer_outfit_type(handle: str, description: str, special_feature: str) -> str:
    """Detect if product is a set or single item."""
    text = f"{handle} {description} {special_feature}".lower()
    set_signals = ["hat", "mitten", "כובע", "כפפות", "3-piece", "2-piece", "set", "סט"]
    if any(s in text for s in set_signals):
        return "set"
    return "single"


def infer_set_items(handle: str, description: str, special_feature: str) -> list[str]:
    """List accessories included in the set."""
    text = f"{handle} {description} {special_feature}"
    items = _match_map_multi(text, SET_ITEMS_MAP)
    # exclude main garment type items (hat used as main garment is different)
    return items


def infer_print(title: str, handle: str, visual: dict) -> str:
    """Detect print/pattern. Visual result takes priority."""
    # From visual
    v_motifs = visual.get("pattern_and_design", {}).get("motifs", [])
    if isinstance(v_motifs, list) and v_motifs:
        for motif in v_motifs:
            for key, keywords in PRINT_MAP.items():
                for kw in keywords:
                    if kw.lower() in str(motif).lower():
                        return key
    v_pattern = visual.get("pattern_and_design", {}).get("pattern_type", "")
    if v_pattern:
        mapped = _match_map(v_pattern, PRINT_MAP)
        if mapped:
            return mapped

    # From title + handle
    text = f"{title} {handle}"
    return _match_map(text, PRINT_MAP) or ""


def infer_color(handle: str, variants: list, visual: dict) -> str:
    """Detect primary color. Visual result takes priority."""
    # From visual
    v_color = visual.get("color_palette", {}).get("primary", "")
    if v_color:
        return _match_map(v_color, COLOR_MAP) or v_color.lower()

    # From handle
    handle_match = _match_map(handle, COLOR_MAP)
    if handle_match:
        return handle_match

    # From first variant option
    if variants:
        option_val = variants[0].get("option1", "") or variants[0].get("option2", "")
        if option_val:
            mapped = _match_map(option_val, COLOR_MAP)
            if mapped:
                return mapped
            return option_val.lower()
    return ""


def infer_baby_stage(target_age: str, handle: str) -> str:
    """Map age range to life stage."""
    text = f"{target_age} {handle}".lower()

    # Newborn signals
    if any(s in text for s in ["0-3", "newborn", "nb", "נייבורן"]):
        return "newborn"
    # Infant signals
    if any(s in text for s in ["infant", "0-12", "0-6", "3-6", "6-9", "6-12"]):
        return "infant"
    # Toddler signals
    if any(s in text for s in ["toddler", "1-2", "18", "24", "2y", "3y"]):
        return "toddler"
    # Default for 0-12M
    if target_age and re.search(r"0-\d{1,2}M", target_age):
        return "infant"
    return "infant"


def infer_movement_friendly(clothing_type: str, visual: dict) -> bool:
    """True if garment design supports active movement."""
    use_cases = visual.get("style_interpretation", {}).get("use_cases", [])
    if isinstance(use_cases, list):
        for uc in use_cases:
            if any(w in str(uc).lower() for w in ["play", "active", "crawl", "move", "daily"]):
                return True
    # Rompers and sets are generally movement-friendly
    return clothing_type in ("romper", "bodysuit", "set")


def infer_dressing_ease(handle: str, description: str, special_feature: str, visual: dict) -> str:
    """Estimate ease of dressing. high/medium/low."""
    text = f"{handle} {description} {special_feature}".lower()

    # Check visual closure type
    v_closure = visual.get("visual_structure", {}).get("closure", "")
    if v_closure:
        if any(w in v_closure.lower() for w in ["snap", "button", "zip"]):
            return "high"
        if "pullover" in v_closure.lower():
            return "medium"

    # From text signals
    if any(s in text for s in ["snap", "button", "פתח", "רוכסן", "quick", "easy", "zip"]):
        return "high"
    return "medium"


def infer_giftable(description: str, title: str, handle: str, outfit_type: str) -> bool:
    """True if product signals gift suitability."""
    text = f"{description} {title} {handle}".lower()
    gift_signals = ["gift", "מתנה", "present", "newborn gift", "baby shower"]
    if any(s in text for s in gift_signals):
        return True
    # Sets are inherently more giftable
    return outfit_type == "set"


def infer_parent_use_case(main_use: str, handle: str) -> str:
    """Map main_use to parent mental model."""
    text = f"{main_use} {handle}".lower()
    if any(s in text for s in ["sleep", "שינה", "night", "lullaby"]):
        return "sleep_outfit"
    if any(s in text for s in ["event", "party", "אירוע", "occasion"]):
        return "occasion_outfit"
    return "quick_outfit"


def infer_season(visual: dict, handle: str) -> str:
    """Detect season signals."""
    v_season = visual.get("texture_and_season_signals", {}).get("season", "")
    if v_season:
        s = v_season.lower()
        if "winter" in s or "חורף" in s:
            return "winter"
        if "summer" in s or "קיץ" in s:
            return "summer"
        if "all" in s or "year" in s:
            return "all_season"

    handle_lower = handle.lower()
    if "winter" in handle_lower or "fleece" in handle_lower or "warm" in handle_lower:
        return "winter"
    if "summer" in handle_lower or "light" in handle_lower:
        return "summer"
    return "all_season"


# ── Shoes inference helpers ────────────────────────────────────────────────────

def infer_closure_type(text: str) -> str:
    """Detect shoe closure type. Returns velcro|slip-on|laces|button|unknown."""
    t = text.lower()
    if any(kw in t for kw in ["velcro", "ולקרו", "סקוטש", "סקוצ'", "סקוצ"]):
        return "velcro"
    if any(kw in t for kw in ["slip-on", "slip on", "ללא שרוכים"]):
        return "slip-on"
    if any(kw in t for kw in ["laces", "שרוכים", "lace-up", "lace up"]):
        return "laces"
    if any(kw in t for kw in ["buckle strap", "buckle", "כפתור", "אבזם"]):
        return "buckle"
    if any(kw in t for kw in ["hook and loop", "hook-and-loop", "hook & loop"]):
        return "velcro"
    if any(kw in t for kw in ["button"]):
        return "button"
    return "unknown"


def infer_sole_type(text: str) -> str:
    """Detect shoe sole type. Returns flexible|anti-slip|firm|unknown."""
    t = text.lower()
    if any(kw in t for kw in ["anti slip", "anti-slip", "non slip", "non-slip",
                                "מונעת החלקה", "מונע החלקה", "אנטי סליפ"]):
        return "anti-slip"
    if any(kw in t for kw in ["flexible", "גמישה", "גמיש", "soft sole",
                                "סוליה רכה", "סוליה גמישה"]):
        return "flexible"
    if any(kw in t for kw in ["firm", "hard sole", "rigid", "קשיחה", "סוליה קשיחה"]):
        return "firm"
    return "unknown"


_SHOE_FEATURE_MAP = {
    "anti_slip":     ["anti slip", "anti-slip", "non slip", "non-slip",
                      "מונעת החלקה", "מונע החלקה", "אנטי סליפ"],
    "velcro":        ["velcro", "ולקרו", "סקוטש", "סקוצ'", "סקוצ"],
    "soft_sole":     ["soft sole", "סוליה רכה", "soft bottom"],
    "mesh":          ["mesh", "רשת נושמת", "breathable mesh"],
    "breathable":    ["breathable", "נושמת", "נושם"],
    "padded":        ["padded", "ריפוד", "מרופד", "cushion"],
    "flexible_sole": ["flexible sole", "סוליה גמישה", "flexible", "גמישה"],
    "lightweight":   ["lightweight", "light weight", "קל", "קלה"],
    "first_steps":   ["first step", "first-step", "צעד ראשון", "צעדים ראשונים"],
    "closed_toe":    ["closed toe", "closed-toe", "אצבעות סגורות"],
}


def infer_detected_features(text: str) -> list:
    """Return list of shoe features found in text. Keyword-only — no inference."""
    t = text.lower()
    return [feat for feat, kws in _SHOE_FEATURE_MAP.items() if any(kw in t for kw in kws)]


# ── Main builder ───────────────────────────────────────────────────────────────

def build_intelligence(pid: str) -> dict:
    analyzer = parse_analyzer(pid)
    visual   = parse_visual(pid)

    if not analyzer:
        print(f"  [PIB] ERROR: analyzer.yaml missing for {pid}")
        return {}

    # Raw product data
    title           = analyzer.get("product_title", "")
    handle          = analyzer.get("product_handle", "")
    description     = analyzer.get("description_raw", "")
    special_feature = analyzer.get("special_feature", "")
    target_age      = analyzer.get("target_age", "")
    main_use        = analyzer.get("main_use", "יומיומי")
    fabric_type     = analyzer.get("fabric_type", "")
    fallback_flags  = analyzer.get("fallback_flags", {})

    # From visual: audience_signals
    gender_signal = (
        visual.get("audience_signals", {}).get("gender_styling_signal", "")
    )

    # Infer each dimension
    clothing_type = infer_clothing_type(title, handle, analyzer)
    sleeve        = infer_sleeve(handle, visual)
    outfit_type   = infer_outfit_type(handle, description, special_feature)
    set_items     = infer_set_items(handle, description, special_feature) if outfit_type == "set" else []
    print_val     = infer_print(title, handle, visual)
    color         = infer_color(handle, [], visual)
    baby_stage    = infer_baby_stage(target_age, handle)
    mvmt_friendly = infer_movement_friendly(clothing_type, visual)
    dress_ease    = infer_dressing_ease(handle, description, special_feature, visual)
    giftable      = infer_giftable(description, title, handle, outfit_type)
    parent_use    = infer_parent_use_case(main_use, handle)
    season        = infer_season(visual, handle)

    # ── Shoes-specific fields (shoes path only) ──────────────────────────────
    product_template_type = analyzer.get("product_template_type", "")
    if product_template_type == "shoes":
        shoe_text         = f"{title} {description}"
        detected_features = infer_detected_features(shoe_text)
        closure_type      = infer_closure_type(shoe_text)
        sole_type         = infer_sole_type(shoe_text)
    else:
        detected_features = []
        closure_type      = "unknown"
        sole_type         = "unknown"

    # Visual content_guidance — safe angles for writers
    safe_benefit_directions = (
        visual.get("content_guidance", {}).get("useful_benefit_directions", [])
    )
    hero_directions = (
        visual.get("content_guidance", {}).get("hero_directions", [])
    )
    unsafe_claims = (
        visual.get("content_guidance", {}).get("unsafe_claims_to_avoid", [])
    )

    intelligence = {
        "product_id":    pid,
        "generated_at":  __import__("datetime").datetime.now().isoformat(),
        "source": {
            "analyzer_used": True,
            "visual_used":   bool(visual),
        },
        "product_intelligence": {
            "clothing_type":    clothing_type,
            "print":            print_val,
            "color":            color,
            "sleeve":           sleeve,
            "outfit_type":      outfit_type,
            "set_items":        set_items,
            "baby_stage":       baby_stage,
            "season":           season,
            "movement_friendly": mvmt_friendly,
            "dressing_ease":    dress_ease,
            "giftable":         giftable,
            "parent_use_case":  parent_use,
            "fabric_known":     bool(fabric_type),
            "fabric_type":      fabric_type,
            "gender_signal":    gender_signal,
        },
        "writing_guidance": {
            "visual_benefit_directions": safe_benefit_directions,
            "hero_directions":           hero_directions,
            "unsafe_claims":             unsafe_claims,
        },
        "fallback_flags": fallback_flags,
    }

    # Merge shoes-specific fields into product_intelligence (shoes path only)
    if product_template_type == "shoes":
        intelligence["product_intelligence"].update({
            "clothing_type":     None,   # not applicable for shoes
            "detected_features": detected_features,
            "closure_type":      closure_type,
            "sole_type":         sole_type,
        })

    # Save
    out_path = STAGE_OUT_DIR / f"{pid}_intelligence.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(intelligence, f, ensure_ascii=False, indent=2)

    print(f"  [PIB] intelligence saved -> {out_path}")
    return intelligence


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python product_intelligence_builder.py {product_id}")
        sys.exit(1)

    pid = sys.argv[1]
    print(f"Building product intelligence for: {pid}")
    intel = build_intelligence(pid)

    if intel:
        pi = intel.get("product_intelligence", {})
        print()
        print("── Product Intelligence ─────────────────────")
        for k, v in pi.items():
            if v not in (None, "", [], False):
                print(f"  {k:20s} : {v}")
        print("─────────────────────────────────────────────")
        print(f"  visual_used: {intel['source']['visual_used']}")
        print()
        print("OK — ready for writing agents 02-05")
