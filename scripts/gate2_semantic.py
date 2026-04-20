#!/usr/bin/env python3
"""
Gate 2 — Semantic Gate
AUTOMATION-HARDENING-PLAN v1 | P1-S6
Checks: A (Technical Fingerprint), B (Type Consistency),
        C (Fabricated Claim), D (Description Bleed),
        E (Template Repetition — DISABLED pending Ayel threshold approval)

Usage:
  python gate2_semantic.py <pid>
  python gate2_semantic.py <pid> --batch-titles "title1|title2|title3"
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"

# ── Check E: DISABLED — awaiting Ayel threshold approval ─────────────────────
# Set to True only after Ayel approves Jaccard thresholds (0.6 / 0.8)
CHECK_E_ENABLED: bool = False


# ── Text Extraction ───────────────────────────────────────────────────────────

def extract_all_text(pub_data: dict) -> dict[str, str]:
    """Extract text content from all metafield sections."""
    meta = pub_data.get("metafields", {})
    sections: dict[str, str] = {}

    # Simple string fields
    for field in [
        "hero_eyebrow", "hero_headline", "hero_subheadline",
        "fabric_title", "fabric_body", "fabric_body_2", "fabric_highlight",
        "whats_special", "emotional_reassurance",
    ]:
        val = meta.get(field, "")
        if val:
            sections[field] = str(val)

    # Benefits: title + description
    benefits = meta.get("benefits", [])
    if isinstance(benefits, list):
        parts = []
        for b in benefits:
            if isinstance(b, dict):
                parts.append(b.get("title", "") + " " + b.get("description", ""))
        if parts:
            sections["benefits"] = " ".join(parts)

    # FAQ: question + answer
    faq = meta.get("faq", [])
    if isinstance(faq, list):
        parts = []
        for q in faq:
            if isinstance(q, dict):
                parts.append(q.get("question", "") + " " + q.get("answer", ""))
        if parts:
            sections["faq"] = " ".join(parts)

    # Care instructions: title + text
    care = meta.get("care_instructions", [])
    if isinstance(care, list):
        parts = []
        for c in care:
            if isinstance(c, dict):
                parts.append(c.get("card_title", "") + " " + c.get("card_text", ""))
        if parts:
            sections["care"] = " ".join(parts)

    return sections


# ── Check A — Technical Fingerprint ──────────────────────────────────────────

# Closed patterns — each is a compiled regex
_FINGERPRINT_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("digits_in_parens",   re.compile(r"\(\d{3,}\)")),
    ("pid_prefix",         re.compile(r"\b(?:pid|id|sku|handle):", re.IGNORECASE)),
    ("bm_prefix",          re.compile(r"\bBM-", re.IGNORECASE)),
    ("handle_parts",       re.compile(r"-(?:SUIT|SET|SHOES)-", re.IGNORECASE)),
    ("file_suffixes",      re.compile(r"_(?:edited|publisher|validator)\b", re.IGNORECASE)),
    ("long_english_kebab", re.compile(r"\b[A-Za-z]{3,}(?:-[A-Za-z]{2,}){3,}\b")),
]

def check_a_technical_fingerprint(pid: str, sections: dict[str, str]) -> dict:
    """Fail if any known technical artifact pattern is found in visible text."""
    all_text = " ".join(sections.values())

    for pattern_name, pattern in _FINGERPRINT_PATTERNS:
        match = pattern.search(all_text)
        if match:
            # Find which section
            found_in = next(
                (sec for sec, text in sections.items() if pattern.search(text)),
                "unknown"
            )
            return {
                "check": "check_a",
                "status": "FAIL",
                "fail_reason": (
                    f"Technical fingerprint detected: pattern='{pattern_name}' "
                    f"match='{match.group()}' section='{found_in}'"
                ),
            }

    return {"check": "check_a", "status": "PASS"}


# ── Check B — Product Type Consistency ───────────────────────────────────────

# Terms that must NOT appear in hero_headline when product_template_type is as listed
_TYPE_MISMATCH_RULES: dict[str, list[str]] = {
    "clothing": ["נעל", "סנדל", "מגף", "כפכף", "סוליה", "שרוכים", "צייזל"],
    "shoes":    [],  # shoes can mention clothing accessories — no rule currently
}

# Terms forbidden in hero_headline when product_template_type=clothing (shoe-only anatomy)
_SHOE_ANATOMY_TERMS = ["סוליה", "שרוכים", "צייזל", "מדרס", "קרסול"]

def check_b_type_consistency(pid: str, pub_data: dict, sections: dict[str, str]) -> dict:
    """Fail if hero_headline or geo_who_for contains terms from a different product type."""
    product_type = pub_data.get("product_template_type", "")
    headline     = sections.get("hero_headline", "")
    subheadline  = sections.get("hero_subheadline", "")

    # Rule 1: shoe/accessory anatomy terms in clothing headline
    if product_type == "clothing":
        for term in _SHOE_ANATOMY_TERMS:
            if term in headline:
                return {
                    "check": "check_b",
                    "status": "FAIL",
                    "fail_reason": (
                        f"Type mismatch: term='{term}' (shoe anatomy) in hero_headline "
                        f"for product_type='{product_type}'"
                    ),
                }

    # Rule 2: forbidden type terms per product type
    forbidden_terms = _TYPE_MISMATCH_RULES.get(product_type, [])
    for term in forbidden_terms:
        if term in headline or term in subheadline:
            return {
                "check": "check_b",
                "status": "FAIL",
                "fail_reason": (
                    f"Type mismatch: term='{term}' forbidden for "
                    f"product_type='{product_type}' (found in headline/subheadline)"
                ),
            }

    return {"check": "check_b", "status": "PASS"}


# ── Check C — Fabricated Claim ────────────────────────────────────────────────

_STAR_PATTERNS       = re.compile(r"[★☆⭐]|\d+[\./]\d+\s*(?:כוכב|כוכבים|stars?)", re.IGNORECASE)
_PARENT_QUOTE_HINTS  = re.compile(r"(?:אמרה לנו|אמר לנו|לפי הורים|הורים רבים|אמר הורה)", re.IGNORECASE)
_CERT_PATTERNS       = re.compile(r"(?:תקן\s+[A-Z]+|ISO\s*\d+|מאושר\s+(?:על ידי|ע\"י|ע\"י))", re.IGNORECASE)
_NUMERIC_CLAIM       = re.compile(r"\d+%\s*(?:מה|מן|מ)", re.IGNORECASE)

def check_c_fabricated_claim(pid: str, all_text: str, ctx: dict) -> dict:
    """Fail if text contains claims that have no source in context."""
    fallback_flags = ctx.get("fallback_flags", {}) or {}
    has_reviews    = fallback_flags.get("has_reviews", False)

    if not has_reviews:
        if _STAR_PATTERNS.search(all_text):
            return {
                "check": "check_c",
                "status": "FAIL",
                "fail_reason": "Star/rating text found but has_reviews=false in context",
            }
        if _PARENT_QUOTE_HINTS.search(all_text):
            return {
                "check": "check_c",
                "status": "FAIL",
                "fail_reason": "Parent quote/testimonial pattern found but has_reviews=false in context",
            }

    if _CERT_PATTERNS.search(all_text):
        return {
            "check": "check_c",
            "status": "FAIL",
            "fail_reason": "Certification claim detected — not present in product context",
        }

    if _NUMERIC_CLAIM.search(all_text):
        return {
            "check": "check_c",
            "status": "FAIL",
            "fail_reason": "Numeric percentage claim found without source in context",
        }

    return {"check": "check_c", "status": "PASS"}


# ── Check D — Description Bleed ───────────────────────────────────────────────

def _word_ngrams(text: str, n: int = 8) -> list[tuple]:
    """Return all n-grams of words from text."""
    words = text.split()
    return [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]


def check_d_description_bleed(
    pid: str,
    all_text: str,
    ctx: dict,
    batch_product_titles: list[str] | None = None,
) -> dict:
    """
    Fail if:
    - 8+ consecutive words from description_raw appear unchanged in new text
    - A title/handle from another product in the batch appears in this text
    """
    # Condition 1: raw description bleed
    description_raw = ctx.get("description_raw", "") or ""
    if description_raw and len(description_raw.split()) >= 8:
        raw_ngrams  = set(_word_ngrams(description_raw, 8))
        text_ngrams = set(_word_ngrams(all_text, 8))
        overlap     = raw_ngrams & text_ngrams
        if overlap:
            sample = " ".join(list(overlap)[0])
            return {
                "check": "check_d",
                "status": "FAIL",
                "fail_reason": (
                    f"Description bleed: 8-word sequence from description_raw "
                    f"found in new text. Sample: '{sample[:80]}...'"
                ),
            }

    # Condition 2: cross-product title bleed
    if batch_product_titles:
        product_title = ctx.get("product_title", "")
        for other_title in batch_product_titles:
            if not other_title or other_title == product_title:
                continue
            # Check if significant part of another product's title appears
            other_words = other_title.split()
            if len(other_words) >= 4:
                other_seq = " ".join(other_words[:4])
                if other_seq in all_text:
                    return {
                        "check": "check_d",
                        "status": "FAIL",
                        "fail_reason": (
                            f"Cross-product bleed: title fragment from another product "
                            f"('{other_seq}') found in this product's text"
                        ),
                    }

    return {"check": "check_d", "status": "PASS"}


# ── Check E — Template Repetition (DISABLED) ─────────────────────────────────

def check_e_template_repetition_batch(batch_pub_data: list[dict]) -> dict:
    """
    Batch-level check: 4-gram Jaccard similarity on hero_headline.
    DISABLED BY DEFAULT — awaiting Ayel threshold approval.
    Thresholds: PAIR_WARN ≥ 0.6, BATCH_FAIL ≥ 0.8 in 2+ pairs (proposed).
    """
    if not CHECK_E_ENABLED:
        return {
            "check": "check_e",
            "status": "DISABLED",
            "note": "Check E disabled — awaiting Ayel approval for Jaccard thresholds (0.6/0.8)",
        }

    def _fourgrams(text: str) -> set[tuple]:
        words = text.split()
        return {tuple(words[i:i + 4]) for i in range(len(words) - 3)}

    headlines = [
        (p.get("product_id", "?"), p.get("metafields", {}).get("hero_headline", ""))
        for p in batch_pub_data
    ]

    pair_warns = []
    batch_fails = []

    for i in range(len(headlines)):
        for j in range(i + 1, len(headlines)):
            pid_a, h_a = headlines[i]
            pid_b, h_b = headlines[j]
            g_a, g_b = _fourgrams(h_a), _fourgrams(h_b)
            if not g_a or not g_b:
                continue
            similarity = len(g_a & g_b) / len(g_a | g_b)
            if similarity >= 0.8:
                batch_fails.append((pid_a, pid_b, round(similarity, 3)))
            elif similarity >= 0.6:
                pair_warns.append((pid_a, pid_b, round(similarity, 3)))

    if len(batch_fails) >= 2:
        return {
            "check": "check_e",
            "status": "BATCH_FAIL",
            "fail_reason": f"Template repetition: {len(batch_fails)} pairs with Jaccard ≥ 0.8: {batch_fails}",
        }
    if len(pair_warns) >= 3:
        return {
            "check": "check_e",
            "status": "BATCH_WARN",
            "fail_reason": f"Template repetition warning: {len(pair_warns)} pairs with Jaccard ≥ 0.6: {pair_warns}",
        }

    return {"check": "check_e", "status": "PASS"}


# ── Main Gate Runner ──────────────────────────────────────────────────────────

def run_gate2(
    pid: str,
    pub_data: dict,
    ctx: dict,
    batch_product_titles: list[str] | None = None,
    save_result: bool = True,
) -> dict:
    """
    Run Gate 2 semantic checks A–D on a single product.
    Check E must be run separately at batch level via check_e_template_repetition_batch().
    Returns gate2_result dict.
    """
    sections = extract_all_text(pub_data)
    all_text = " ".join(sections.values())

    checks: list[dict] = [
        check_a_technical_fingerprint(pid, sections),
        check_b_type_consistency(pid, pub_data, sections),
        check_c_fabricated_claim(pid, all_text, ctx),
        check_d_description_bleed(pid, all_text, ctx, batch_product_titles),
    ]

    failed = [c for c in checks if c["status"] == "FAIL"]

    # semantic_signature: true only if ALL checks pass AND batch has no BATCH_WARN/FAIL
    # Note: Check E batch status must be evaluated separately and merged before issuing signature
    all_pass = len(failed) == 0

    result = {
        "product_id": pid,
        "gate": "gate2_semantic",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "FAIL" if failed else "PASS",
        "semantic_signature": all_pass,  # May be overridden if batch has BATCH_WARN
        "check_e_status": "DISABLED" if not CHECK_E_ENABLED else "PENDING_BATCH",
        "check_results": {c["check"]: c["status"] for c in checks},
        "fail_reasons": [
            {"check": c["check"], "detail": c["fail_reason"]}
            for c in failed
        ],
    }

    if save_result:
        out_path = STAGE_OUT_DIR / f"{pid}_gate2_result.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gate 2 — Semantic Gate")
    parser.add_argument("pid", help="Product ID")
    parser.add_argument(
        "--batch-titles",
        help="Pipe-separated titles of other products in batch (for bleed check)",
        default="",
    )
    args = parser.parse_args()

    pub_path = STAGE_OUT_DIR / f"{args.pid}_publisher.json"
    ctx_path = CONTEXT_DIR   / f"{args.pid}.yaml"

    if not pub_path.exists():
        print(f"[GATE2] ERROR: publisher.json not found for {args.pid}")
        sys.exit(1)
    if not ctx_path.exists():
        print(f"[GATE2] ERROR: context.yaml not found for {args.pid}")
        sys.exit(1)

    pub_data = json.loads(pub_path.read_text(encoding="utf-8"))
    ctx      = yaml.safe_load(ctx_path.read_text(encoding="utf-8")) or {}
    batch_titles = [t.strip() for t in args.batch_titles.split("|") if t.strip()] or None

    result = run_gate2(args.pid, pub_data, ctx, batch_titles)

    symbol = "✓" if result["status"] == "PASS" else "✗"
    print(f"[GATE2] {symbol} {args.pid} — {result['status']}")
    for fr in result.get("fail_reasons", []):
        print(f"  FAIL [{fr['check']}]: {fr['detail']}")
    print(f"  check_e: {result['check_e_status']}")

    sys.exit(0 if result["status"] == "PASS" else 1)
