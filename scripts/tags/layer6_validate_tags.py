"""
Layer 6 — Phase 3 Validation Gates
8 gates for validating proposed tags before pushing to Shopify.
"""

import re
from typing import Any

# ─── Taxonomy Spec (CAT-A through CAT-G) ──────────────────────────────────────
ALLOWED_VALUES: dict[str, set[str]] = {
    "CAT-A": {
        "type-romper", "type-bodysuit", "type-dress", "type-set",
        "type-pants", "type-top", "type-hat", "type-swimwear",
        "type-shoes", "type-sandals", "type-sneakers", "type-boots",
        "type-coat", "type-reborn-doll", "type-toy", "type-plush-toy",
        "type-sleep-soother", "type-accessory", "type-bath-accessory",
        "type-swimming-ring", "type-unknown",
    },
    "CAT-B": {
        "age-0-3m", "age-3-6m", "age-6-12m", "age-12-18m",
        "age-18-24m", "age-2-3y", "age-3-5y", "age-0-6m",
        "age-newborn", "age-unknown",
    },
    "CAT-C": {
        "season-summer", "season-winter", "season-spring-fall",
        "season-all", "season-unknown",
    },
    "CAT-D": {
        "fabric-cotton", "fabric-linen", "fabric-muslin", "fabric-knit",
        "fabric-fleece", "fabric-denim", "fabric-polyester", "fabric-faux-fur",
        "fabric-corduroy", "fabric-velvet", "fabric-waffle-knit",
        "fabric-silicone", "fabric-body", "fabric-unknown",
    },
    "CAT-E": {
        "occ-everyday", "occ-gift", "occ-baby-shower", "occ-beach",
        "occ-sleep", "occ-special-event", "occ-photoshoot", "occ-first-step",
        "occ-water-play", "occ-calming", "occ-unknown",
    },
    "CAT-F": {
        "gender-girl", "gender-boy", "gender-neutral", "gender-unknown",
    },
    "CAT-G": {
        "style-elegant", "style-casual", "style-vintage", "style-sporty",
        "style-floral", "style-animal-print", "style-teddy", "style-european",
        "style-unicorn", "style-striped", "style-modern", "style-unknown",
    },
}

# Phase 5b rule: CAT-B (age) required only for clothing and shoes.
# Toys, plush toys, reborn dolls, bath accessories, accessories → age not required.
CLOTHING_SHOES_TYPES: set[str] = {
    "type-romper", "type-bodysuit", "type-dress", "type-set",
    "type-pants", "type-top", "type-coat", "type-swimwear", "type-hat",
    "type-shoes", "type-sandals", "type-sneakers", "type-boots",
}
NON_AGE_TYPES: set[str] = {
    "type-toy", "type-plush-toy", "type-reborn-doll", "type-sleep-soother",
    "type-swimming-ring", "type-bath-accessory", "type-accessory", "type-unknown",
}

ALL_ALLOWED: set[str] = set().union(*ALLOWED_VALUES.values())

PREFIX_TO_CAT: dict[str, str] = {
    "type": "CAT-A", "age": "CAT-B", "season": "CAT-C",
    "fabric": "CAT-D", "occ": "CAT-E", "gender": "CAT-F", "style": "CAT-G",
}

REQUIRED_CATS = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}

VALID_SOURCES = {
    "handle", "title", "body", "yaml_desc", "existing_tag",
    "existing_tag_hebrew", "type_default", "category_default",
    "age_hardening_v2", "manual",
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

TAG_FORMAT_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)+$")


def _get_all_tags(product: dict) -> list[dict]:
    """Proposed tags + age_after tags, merged and deduped by tag value."""
    seen: set[str] = set()
    tags: list[dict] = []
    for t in product.get("proposed_tags", []) + product.get("age_after", []):
        if t["tag"] not in seen:
            seen.add(t["tag"])
            tags.append(t)
    return tags


def _cat_of(t: dict) -> str | None:
    cat = t.get("category")
    if cat:
        return cat
    return PREFIX_TO_CAT.get(t["tag"].split("-")[0])


def _catb_exempt(product: dict) -> tuple[bool, str]:
    age_status = product.get("age_status", "")
    is_reborn = product.get("product_group", "") == "reborn"
    if age_status in ("RANGE_TOO_BROAD", "DOLL_NO_AGE_APPLICABLE") or is_reborn:
        return True, age_status or "reborn"
    if product.get("yaml_gap") and age_status == "NO_AGE_FOUND":
        return True, "YAML_GAP+NO_AGE_FOUND"
    # Phase 5b: non-clothing/shoes types are exempt from CAT-B requirement.
    proposed_type = next(
        (t["tag"] for t in product.get("proposed_tags", []) if t["tag"].startswith("type-")),
        None,
    )
    if proposed_type and proposed_type in NON_AGE_TYPES:
        return True, f"NON_CLOTHING_SHOES:{proposed_type}"
    return False, ""


# ─── Gate 1: SOURCE_EXISTS ────────────────────────────────────────────────────
def gate_source_exists(product: dict) -> dict:
    """Every proposed tag must have a non-empty source field."""
    issues = []
    for t in _get_all_tags(product):
        if not t.get("source"):
            issues.append({
                "tag": t["tag"],
                "category": _cat_of(t) or "?",
                "reason": "source field missing or empty",
            })
    return {"gate": "SOURCE_EXISTS", "pass": not issues, "issues": issues}


# ─── Gate 2: FORMAT_VALID ─────────────────────────────────────────────────────
def gate_format_valid(product: dict) -> dict:
    """Every tag must match ^[a-z][a-z0-9]*(-[a-z0-9]+)+$ (ASCII lowercase slug)."""
    issues = []
    for t in _get_all_tags(product):
        if not TAG_FORMAT_RE.match(t["tag"]):
            issues.append({
                "tag": t["tag"],
                "category": _cat_of(t) or "?",
                "reason": "invalid format (must be lowercase ASCII slug)",
            })
    return {"gate": "FORMAT_VALID", "pass": not issues, "issues": issues}


# ─── Gate 3: ALLOWED_VALUE ────────────────────────────────────────────────────
def gate_allowed_value(product: dict) -> dict:
    """Every tag must exist in the taxonomy spec's allowed values list."""
    issues = []
    for t in _get_all_tags(product):
        if t["tag"] not in ALL_ALLOWED:
            issues.append({
                "tag": t["tag"],
                "category": _cat_of(t) or "UNKNOWN_PREFIX",
                "reason": "TAXONOMY_GAP: value not in allowed list",
            })
    return {"gate": "ALLOWED_VALUE", "pass": not issues, "issues": issues}


# ─── Gate 4: SOURCE_TRACEABLE ─────────────────────────────────────────────────
def gate_source_traceable(product: dict) -> dict:
    """Tags must not use deprecated or unrecognized source values."""
    DEPRECATED = {"title_heuristic", "heuristic", "unknown", "guess"}
    issues = []
    for t in _get_all_tags(product):
        src = t.get("source", "")
        if src in DEPRECATED:
            issues.append({
                "tag": t["tag"],
                "category": _cat_of(t) or "?",
                "reason": f"deprecated source: '{src}'",
            })
        elif src not in VALID_SOURCES:
            issues.append({
                "tag": t["tag"],
                "category": _cat_of(t) or "?",
                "reason": f"unrecognized source: '{src}'",
            })
    return {"gate": "SOURCE_TRACEABLE", "pass": not issues, "issues": issues}


# ─── Gate 5: NO_FORBIDDEN_INFERENCE ──────────────────────────────────────────
def gate_no_forbidden_inference(product: dict) -> dict:
    """No age tag from non-authoritative source when handle/title has a wide age range."""
    combined = (
        (product.get("title") or "") + " " + (product.get("handle") or "")
    ).lower()
    wide_match = next(
        (desc for pat, desc in WIDE_RANGE_PATS if re.search(pat, combined, re.IGNORECASE)),
        None,
    )
    issues = []
    if wide_match:
        for t in _get_all_tags(product):
            if (_cat_of(t) == "CAT-B" or t["tag"].startswith("age-")) and \
               t.get("source") != "existing_tag_hebrew":
                issues.append({
                    "tag": t["tag"],
                    "category": "CAT-B",
                    "reason": f"age inferred despite wide-range pattern in product ({wide_match})",
                })
    return {"gate": "NO_FORBIDDEN_INFERENCE", "pass": not issues, "issues": issues}


# ─── Gate 6: CATEGORY_COVERAGE ───────────────────────────────────────────────
def gate_category_coverage(product: dict) -> dict:
    """Required categories (A, B, C, F) must be present; CAT-B exempt under valid conditions."""
    covered = {_cat_of(t) for t in _get_all_tags(product)} - {None}
    catb_exempt, exempt_reason = _catb_exempt(product)

    effective_required = set(REQUIRED_CATS)
    if catb_exempt:
        effective_required.discard("CAT-B")

    missing = effective_required - covered
    issues = [
        {"category": cat, "reason": "required category not covered"}
        for cat in sorted(missing)
    ]
    note = f"CAT-B exempt: {exempt_reason}" if catb_exempt else ""
    return {"gate": "CATEGORY_COVERAGE", "pass": not issues, "issues": issues, "note": note}


# ─── Gate 7: DUPLICATE_CONFLICT ──────────────────────────────────────────────
def gate_duplicate_conflict(product: dict) -> dict:
    """No two different values for the same single-tag category (A, B, C, F).
    Multi-tag categories D, E, G are allowed to repeat.
    """
    SINGLE_TAG_CATS = {"CAT-A", "CAT-B", "CAT-C", "CAT-F"}
    cat_tags: dict[str, list[str]] = {}
    for t in _get_all_tags(product):
        cat = _cat_of(t)
        if cat in SINGLE_TAG_CATS:
            cat_tags.setdefault(cat, []).append(t["tag"])

    issues = []
    for cat, tags in cat_tags.items():
        unique = list(dict.fromkeys(tags))
        if len(unique) > 1:
            issues.append({
                "category": cat,
                "tags": unique,
                "reason": f"conflict: multiple values in single-tag category",
            })
    return {"gate": "DUPLICATE_CONFLICT", "pass": not issues, "issues": issues}


# ─── Gate 8: QUALITY_SCORE ────────────────────────────────────────────────────
def gate_quality_score(product: dict) -> dict:
    """Quality score >= 75 for PASS.
    score = (req_present/4)*60 + min(rec_present,3)/3*20 + avg_conf*20
    req_present: count of {A,B,C,F} covered (CAT-B exempt counts as present)
    rec_present: count of individual CAT-D/E/G tags (up to 3)
    avg_conf: mean confidence of all proposed tags
    """
    tags = _get_all_tags(product)
    if not tags:
        return {
            "gate": "QUALITY_SCORE", "pass": False,
            "issues": [{"reason": "no tags at all", "score": 0}], "score": 0,
        }

    covered = {_cat_of(t) for t in tags} - {None}
    catb_exempt, exempt_reason = _catb_exempt(product)

    req_present = sum(
        1 for c in REQUIRED_CATS
        if c in covered or (c == "CAT-B" and catb_exempt)
    )
    rec_tags = [t for t in tags if _cat_of(t) in ("CAT-D", "CAT-E", "CAT-G")]
    rec_present = min(len(rec_tags), 3)
    confs = [t.get("confidence", 0) for t in tags]
    avg_conf = sum(confs) / len(confs)

    score = round((req_present / 4) * 60 + (rec_present / 3) * 20 + avg_conf * 20, 1)
    passed = score >= 75

    issues = [] if passed else [{"reason": f"score {score} < 75 threshold", "score": score}]
    note = f"CAT-B exempt ({exempt_reason}): counted as present" if catb_exempt else ""
    return {
        "gate": "QUALITY_SCORE", "pass": passed,
        "issues": issues, "score": score, "note": note,
    }


# ─── Run all gates ────────────────────────────────────────────────────────────
GATES = [
    gate_source_exists,
    gate_format_valid,
    gate_allowed_value,
    gate_source_traceable,
    gate_no_forbidden_inference,
    gate_category_coverage,
    gate_duplicate_conflict,
    gate_quality_score,
]


def run_all_gates(product: dict) -> dict:
    results = [g(product) for g in GATES]
    all_pass = all(r["pass"] for r in results)
    taxonomy_gaps = [i["tag"] for r in results if r["gate"] == "ALLOWED_VALUE" for i in r["issues"]]
    return {
        "product_id": product.get("product_id", ""),
        "title": product.get("title", ""),
        "overall_pass": all_pass,
        "gates": results,
        "taxonomy_gaps": taxonomy_gaps,
    }
