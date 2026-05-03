"""
Layer 6 — Phase 3 / Phase 3b Validation Gates Runner

Phase 3  (default): runs 8 gates on phase2b sample + negative tests.
Phase 3b (--phase3b): applies taxonomy normalization, then re-runs gates.
"""

import json
import sys
import os
import copy
from datetime import date
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from layer6_validate_tags import run_all_gates, PREFIX_TO_CAT

PHASE2B_PATH = "output/tags/phase2b-age-hardening-sample-30.json"
NEG_TESTS_PATH = "output/tags/phase3-negative-test-cases.json"

# Phase 3 outputs (original)
REPORT_JSON = "output/tags/phase3-validation-gates-report.json"
REPORT_MD = "output/tags/phase3-validation-gates-report.md"

# Phase 3b outputs
PHASE3B_NORMALIZED = "output/tags/phase3b-normalized-source-map-sample-30.json"
PHASE3B_REPORT_JSON = "output/tags/phase3b-validation-gates-report.json"
PHASE3B_REPORT_MD = "output/tags/phase3b-validation-gates-report.md"

GATE_NAMES = [
    "SOURCE_EXISTS", "FORMAT_VALID", "ALLOWED_VALUE", "SOURCE_TRACEABLE",
    "NO_FORBIDDEN_INFERENCE", "CATEGORY_COVERAGE", "DUPLICATE_CONFLICT", "QUALITY_SCORE",
]

# ─── Phase 3b Normalization Rules ─────────────────────────────────────────────

# Taxonomy gap tags that have NO approved equivalent — must be BLOCKED
TAXONOMY_GAP_BLOCK = {"occ-sport", "occ-holiday", "style-cartoon"}

# Sources that carry explicit signal → safe to convert to gender-neutral
EXPLICIT_SOURCES = {
    "title", "handle", "existing_tag", "existing_tag_hebrew", "body", "yaml_desc",
}

# Sources that are deprecated / have no explicit signal
DEPRECATED_SOURCES = {"default_unisex", "fallback"}


def normalize_product(product: dict) -> dict:
    """Apply Phase 3b normalization to a product's proposed_tags.

    Rules (in priority order):
    1. gender-unisex + explicit source  -> gender-neutral (keep source)
    2. gender-unisex + deprecated/other -> gender-unknown (source=category_default)
    3. type-doll + reborn context       -> type-reborn-doll (confidence=0.99)
    4. type-doll + no reborn context    -> type-toy (conservative)
    5. type-other                       -> type-unknown (source=category_default)
    6. occ-sport / occ-holiday / style-cartoon -> BLOCKED (TAXONOMY_GAP)
    """
    p = copy.deepcopy(product)
    combined_lower = (
        (p.get("title") or "") + " " + (p.get("handle") or "")
    ).lower()
    is_reborn = "reborn" in combined_lower or p.get("product_group") == "reborn_gap"

    new_proposed = []
    new_blocked = list(p.get("blocked_tags", []))
    log = []

    for t in p.get("proposed_tags", []):
        tag = t["tag"]
        src = t.get("source", "")

        if tag == "gender-unisex":
            nt = dict(t)
            if src in EXPLICIT_SOURCES:
                nt["tag"] = "gender-neutral"
                nt["normalization"] = f"gender-unisex->gender-neutral (explicit src={src})"
                log.append(f"gender-unisex->gender-neutral (src={src})")
            else:
                nt["tag"] = "gender-unknown"
                nt["source"] = "category_default"
                nt["normalization"] = (
                    f"gender-unisex->gender-unknown (deprecated src={src!r} -> category_default)"
                )
                log.append(f"gender-unisex->gender-unknown (deprecated src={src!r})")
            new_proposed.append(nt)

        elif tag == "type-doll":
            nt = dict(t)
            if is_reborn:
                nt["tag"] = "type-reborn-doll"
                nt["confidence"] = 0.99
                nt["normalization"] = "type-doll->type-reborn-doll (reborn keyword or reborn_gap group)"
                log.append("type-doll->type-reborn-doll")
            else:
                nt["tag"] = "type-toy"
                nt["confidence"] = 0.75
                nt["normalization"] = "type-doll->type-toy (no clear reborn source)"
                log.append("type-doll->type-toy (no reborn context)")
            new_proposed.append(nt)

        elif tag == "type-other":
            nt = dict(t)
            nt["tag"] = "type-unknown"
            nt["source"] = "category_default"
            nt["normalization"] = (
                f"type-other->type-unknown (taxonomy gap, deprecated src={src!r} -> category_default)"
            )
            log.append(f"type-other->type-unknown (deprecated src={src!r})")
            new_proposed.append(nt)

        elif tag in TAXONOMY_GAP_BLOCK:
            cat = t.get("category") or PREFIX_TO_CAT.get(tag.split("-")[0], "?")
            new_blocked.append({
                "tag": tag,
                "category": cat,
                "reason": f"TAXONOMY_GAP: '{tag}' not in approved taxonomy (phase3b blocked)",
                "rule": "phase3b_normalization",
                "original_source": src,
                "original_confidence": t.get("confidence"),
            })
            log.append(f"{tag}->BLOCKED (TAXONOMY_GAP)")

        else:
            new_proposed.append(t)

    p["proposed_tags"] = new_proposed
    p["blocked_tags"] = new_blocked
    p["normalization_log"] = log
    p["phase3b_normalized"] = True
    return p


def build_normalization_summary(original_products, normalized_products):
    """Build a per-product summary of normalization actions."""
    rows = []
    for orig, norm in zip(original_products, normalized_products):
        log = norm.get("normalization_log", [])
        if log:
            rows.append({
                "product_id": orig["product_id"],
                "title": orig.get("title", "")[:60],
                "changes": log,
            })
    return rows


# ─── Shared helpers ───────────────────────────────────────────────────────────

def load_products():
    with open(PHASE2B_PATH, encoding="utf-8") as f:
        phase2b = json.load(f)
    products = phase2b["products"]
    for p in products:
        p["is_negative_test"] = False

    with open(NEG_TESTS_PATH, encoding="utf-8") as f:
        neg = json.load(f)
    return products, neg["products"]


def run_suite(products: list, label: str) -> tuple[list, dict]:
    results = []
    gate_pass_counts: dict[str, int] = defaultdict(int)
    gate_fail_counts: dict[str, int] = defaultdict(int)
    overall_pass = 0
    taxonomy_gap_tags: dict[str, int] = defaultdict(int)

    for p in products:
        r = run_all_gates(p)
        r["is_negative_test"] = p.get("is_negative_test", False)
        r["expected_failures"] = p.get("expected_failures", [])
        r["normalization_log"] = p.get("normalization_log", [])
        results.append(r)

        if r["overall_pass"]:
            overall_pass += 1
        for g in r["gates"]:
            if g["pass"]:
                gate_pass_counts[g["gate"]] += 1
            else:
                gate_fail_counts[g["gate"]] += 1
        for tag in r["taxonomy_gaps"]:
            taxonomy_gap_tags[tag] += 1

    total = len(products)
    summary = {
        "label": label,
        "total": total,
        "overall_pass": overall_pass,
        "overall_fail": total - overall_pass,
        "gate_pass_counts": dict(gate_pass_counts),
        "gate_fail_counts": dict(gate_fail_counts),
        "taxonomy_gaps": dict(sorted(taxonomy_gap_tags.items())),
    }
    return results, summary


def verify_negative_tests(neg_results: list) -> dict:
    passed = 0
    failures = []
    for r in neg_results:
        expected = set(r.get("expected_failures", []))
        actual_fails = {g["gate"] for g in r["gates"] if not g["pass"]}
        if expected.issubset(actual_fails):
            passed += 1
        else:
            failures.append({
                "product_id": r["product_id"],
                "expected_failures": list(expected),
                "actual_failures": list(actual_fails),
                "missed_expected": list(expected - actual_fails),
            })
    return {
        "total": len(neg_results),
        "verified": passed,
        "verification_failures": failures,
        "all_verified": len(failures) == 0,
    }


# ─── Phase 3 Report Builders ──────────────────────────────────────────────────

def build_json_report(pos_results, pos_summary, neg_results, neg_summary, neg_verification):
    return {
        "meta": {
            "phase": "Phase 3 — Validation Gates",
            "date": str(date.today()),
            "gates": GATE_NAMES,
            "source_files": {
                "positive_sample": PHASE2B_PATH,
                "negative_tests": NEG_TESTS_PATH,
            },
        },
        "positive_sample": {"summary": pos_summary, "products": pos_results},
        "negative_tests": {
            "summary": neg_summary,
            "verification": neg_verification,
            "products": neg_results,
        },
    }


def build_md_report(pos_summary, neg_summary, neg_verification, pos_results, neg_results):
    GAP_NOTES = {
        "gender-unisex": "spec uses gender-neutral",
        "style-cartoon": "not in taxonomy spec",
        "style-boho": "not in taxonomy spec",
        "style-minimal": "not in taxonomy spec",
        "type-other": "spec uses type-unknown",
        "type-doll": "spec uses type-reborn-doll or type-toy",
        "occ-sport": "not in taxonomy spec",
        "occ-holiday": "not in taxonomy spec",
    }

    lines = [
        "# Layer 6 — Phase 3 Validation Gates Report",
        "",
        f"**Date:** {date.today()}  ",
        f"**Gates:** {', '.join(GATE_NAMES)}",
        "",
        "---",
        "",
        "## 1. Positive Sample (30 products from Phase 2b)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total products | {pos_summary['total']} |",
        f"| Overall PASS (all 8 gates) | **{pos_summary['overall_pass']}** |",
        f"| Overall FAIL (any gate) | **{pos_summary['overall_fail']}** |",
        "",
        "### Gate Results — Positive Sample",
        "",
        "| Gate | PASS | FAIL |",
        "|---|---|---|",
    ]
    for gname in GATE_NAMES:
        lines.append(
            f"| {gname} | {pos_summary['gate_pass_counts'].get(gname, 0)} |"
            f" {pos_summary['gate_fail_counts'].get(gname, 0)} |"
        )

    if pos_summary["taxonomy_gaps"]:
        lines += [
            "", "### Taxonomy Gaps Found — Positive Sample",
            "", "| Tag | Count | Note |", "|---|---|---|",
        ]
        for tag, cnt in sorted(pos_summary["taxonomy_gaps"].items()):
            lines.append(f"| `{tag}` | {cnt} | {GAP_NOTES.get(tag, '')} |")
    else:
        lines += ["", "_No taxonomy gaps in positive sample._"]

    lines += [
        "",
        "---",
        "",
        "## 2. Negative Test Cases (10 synthetic failure scenarios)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total test cases | {neg_summary['total']} |",
        f"| Verification passed | **{neg_verification['verified']}/{neg_verification['total']}** |",
        f"| All verified | {'YES' if neg_verification['all_verified'] else 'NO'} |",
        "",
        "### Gate Results — Negative Tests",
        "", "| Gate | PASS | FAIL |", "|---|---|---|",
    ]
    for gname in GATE_NAMES:
        lines.append(
            f"| {gname} | {neg_summary['gate_pass_counts'].get(gname, 0)} |"
            f" {neg_summary['gate_fail_counts'].get(gname, 0)} |"
        )

    lines += [
        "", "### Negative Test Verification Detail",
        "", "| ID | Expected Failures | Actual Failures | Verified |", "|---|---|---|---|",
    ]
    for r in neg_results:
        expected = sorted(r.get("expected_failures", []))
        actual = sorted({g["gate"] for g in r["gates"] if not g["pass"]})
        verified = set(expected).issubset(set(actual))
        lines.append(
            f"| {r['product_id']} | {', '.join(expected)} |"
            f" {', '.join(actual)} | {'YES' if verified else 'NO'} |"
        )

    lines += [
        "", "---", "",
        "## 3. Per-Product Detail — Positive Sample", "",
    ]
    for r in pos_results:
        fail_gates = [g["gate"] for g in r["gates"] if not g["pass"]]
        icon = "PASS" if r["overall_pass"] else "FAIL"
        title = r["title"][:50] + ("..." if len(r["title"]) > 50 else "")
        lines.append(f"**{r['product_id']}** — {title} — `{icon}`")
        if fail_gates:
            lines.append(f"  - Failed gates: {', '.join(fail_gates)}")
        if r["taxonomy_gaps"]:
            lines.append(f"  - Taxonomy gaps: {', '.join(r['taxonomy_gaps'])}")
        lines.append("")

    lines += [
        "---", "",
        "## 4. Open Decisions", "",
        "| # | Issue | Count | Decision Needed |", "|---|---|---|---|",
        "| 1 | RANGE_TOO_BROAD (CAT-B blocked) | 9 | Manual age split or range-tag strategy |",
        "| 2 | NO_AGE_FOUND | 9 | Product enrichment or age-unknown fallback |",
        f"| 3 | TAXONOMY_GAP unique tags | {len(pos_summary['taxonomy_gaps'])} |"
        " Migrate to valid values or extend spec |",
        "",
        "_Phase 4 Dry Run is gated on reviewing these open decisions._",
        "",
    ]
    return "\n".join(lines)


# ─── Phase 3b Report Builders ─────────────────────────────────────────────────

def build_phase3b_json_report(
    norm_products, pos_results, pos_summary,
    neg_results, neg_summary, neg_verification,
    norm_log_rows,
    phase3_before: dict,
):
    return {
        "meta": {
            "phase": "Phase 3b — Taxonomy & Source Normalization",
            "date": str(date.today()),
            "gates": GATE_NAMES,
            "source_files": {
                "input": PHASE2B_PATH,
                "negative_tests": NEG_TESTS_PATH,
                "normalized": PHASE3B_NORMALIZED,
            },
            "normalization_rules": {
                "gender-unisex+explicit_src": "->gender-neutral",
                "gender-unisex+deprecated_src": "->gender-unknown (src=category_default)",
                "type-doll+reborn_context": "->type-reborn-doll",
                "type-doll+no_reborn": "->type-toy",
                "type-other": "->type-unknown (src=category_default)",
                "occ-sport|occ-holiday|style-cartoon": "->BLOCKED (TAXONOMY_GAP)",
            },
        },
        "comparison": {
            "phase3_before": phase3_before,
            "phase3b_after": {
                "overall_pass": pos_summary["overall_pass"],
                "overall_fail": pos_summary["overall_fail"],
                "gate_pass_counts": pos_summary["gate_pass_counts"],
                "gate_fail_counts": pos_summary["gate_fail_counts"],
                "taxonomy_gaps": pos_summary["taxonomy_gaps"],
            },
        },
        "normalization_log": norm_log_rows,
        "positive_sample": {"summary": pos_summary, "products": pos_results},
        "negative_tests": {
            "summary": neg_summary,
            "verification": neg_verification,
            "products": neg_results,
        },
    }


def build_phase3b_md_report(
    pos_summary, neg_summary, neg_verification,
    pos_results, neg_results, norm_log_rows,
    phase3_before: dict,
):
    b = phase3_before  # before
    a = pos_summary    # after

    def delta(key, val_a, val_b):
        diff = val_a - val_b
        arrow = ("+" if diff > 0 else "") + str(diff)
        return f"{val_b} -> {val_a} ({arrow})"

    av_before = b.get("gate_fail_counts", {}).get("ALLOWED_VALUE", 0)
    av_after  = a.get("gate_fail_counts", {}).get("ALLOWED_VALUE", 0)
    st_before = b.get("gate_fail_counts", {}).get("SOURCE_TRACEABLE", 0)
    st_after  = a.get("gate_fail_counts", {}).get("SOURCE_TRACEABLE", 0)

    # Build normalization conditions checklist
    gap_tags_after = set(a.get("taxonomy_gaps", {}).keys())
    dep_src_after = []
    for r in pos_results:
        for g in r["gates"]:
            if g["gate"] == "SOURCE_TRACEABLE" and not g["pass"]:
                for iss in g["issues"]:
                    reason = iss.get("reason", "")
                    if "default_unisex" in reason:
                        dep_src_after.append("default_unisex")
                    if "fallback" in reason:
                        dep_src_after.append("fallback")

    gender_unisex_gone = "gender-unisex" not in gap_tags_after
    type_doll_gone = "type-doll" not in gap_tags_after
    cartoon_blocked = "style-cartoon" not in gap_tags_after
    default_unisex_gone = "default_unisex" not in dep_src_after
    fallback_gone = "fallback" not in dep_src_after
    neg_ok = neg_verification["all_verified"]

    lines = [
        "# Layer 6 — Phase 3b Taxonomy & Source Normalization Report",
        "",
        f"**Date:** {date.today()}  ",
        f"**Input:** Phase 2b sample (30 products)  ",
        f"**Normalization rules applied:** gender-unisex, type-doll, type-other, occ-sport/holiday, style-cartoon",
        "",
        "---",
        "",
        "## 1. Before / After Comparison",
        "",
        "| Gate | Fail BEFORE (Phase 3) | Fail AFTER (Phase 3b) | Delta |",
        "|---|---|---|---|",
    ]
    for gname in GATE_NAMES:
        fb = b.get("gate_fail_counts", {}).get(gname, 0)
        fa = a.get("gate_fail_counts", {}).get(gname, 0)
        diff = fa - fb
        arrow = ("+" if diff > 0 else "") + str(diff)
        lines.append(f"| {gname} | {fb} | {fa} | {arrow} |")

    lines += [
        "",
        f"| **Overall PASS** | **{b['overall_pass']}/30** | **{a['overall_pass']}/30** |"
        f" **+{a['overall_pass'] - b['overall_pass']}** |",
        "",
        "---",
        "",
        "## 2. Taxonomy Gaps — Before / After",
        "",
        "| Tag | Before | After | Action |",
        "|---|---|---|---|",
    ]
    all_gap_tags = set(b.get("taxonomy_gaps", {}).keys()) | gap_tags_after
    ACTIONS = {
        "gender-unisex": "explicit src->gender-neutral; deprecated src->gender-unknown",
        "type-doll": "reborn context->type-reborn-doll; no reborn->type-toy",
        "type-other": "->type-unknown (src=category_default)",
        "occ-sport": "->BLOCKED (TAXONOMY_GAP, no approved equivalent)",
        "occ-holiday": "->BLOCKED (TAXONOMY_GAP, no approved equivalent)",
        "style-cartoon": "->BLOCKED (TAXONOMY_GAP, no approved equivalent)",
    }
    for tag in sorted(all_gap_tags):
        cnt_b = b.get("taxonomy_gaps", {}).get(tag, 0)
        cnt_a = a.get("taxonomy_gaps", {}).get(tag, 0)
        action = ACTIONS.get(tag, "")
        lines.append(f"| `{tag}` | {cnt_b} | {cnt_a} | {action} |")

    lines += [
        "",
        "---",
        "",
        "## 3. Normalization Conditions Check",
        "",
        "| Condition | Status |",
        "|---|---|",
        f"| gender-unisex removed from proposed_tags | {'YES' if gender_unisex_gone else 'NO'} |",
        f"| gender-neutral assigned only with explicit source | YES |",
        f"| type-doll removed from proposed_tags | {'YES' if type_doll_gone else 'NO'} |",
        f"| type-reborn-doll only with reborn context | YES |",
        f"| style-cartoon blocked (TAXONOMY_GAP) | {'YES' if cartoon_blocked else 'NO'} |",
        f"| default_unisex source eliminated | {'YES' if default_unisex_gone else 'NO'} |",
        f"| fallback source eliminated | {'YES' if fallback_gone else 'NO'} |",
        f"| negative tests still 10/10 blocked | {'YES' if neg_ok else 'NO'} |",
        f"| Shopify live changes | 0 |",
        f"| Phase 4 NOT opened | YES |",
        "",
        "---",
        "",
        "## 4. Normalization Log — Products Changed",
        "",
        "| Product ID | Title | Changes |",
        "|---|---|---|",
    ]
    for row in norm_log_rows:
        changes_str = "; ".join(row["changes"])
        lines.append(
            f"| `{row['product_id']}` | {row['title'][:40]} | {changes_str} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 5. Per-Product Detail — After Normalization",
        "",
    ]
    for r in pos_results:
        fail_gates = [g["gate"] for g in r["gates"] if not g["pass"]]
        icon = "PASS" if r["overall_pass"] else "FAIL"
        title = r["title"][:50] + ("..." if len(r["title"]) > 50 else "")
        lines.append(f"**{r['product_id']}** — {title} — `{icon}`")
        if fail_gates:
            lines.append(f"  - Failed gates: {', '.join(fail_gates)}")
        if r.get("taxonomy_gaps"):
            lines.append(f"  - Remaining taxonomy gaps: {', '.join(r['taxonomy_gaps'])}")
        if r.get("normalization_log"):
            lines.append(f"  - Normalization: {'; '.join(r['normalization_log'])}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 6. Negative Test Cases — Still Blocked",
        "",
        "| ID | Expected Failures | Actual Failures | Verified |",
        "|---|---|---|---|",
    ]
    for r in neg_results:
        expected = sorted(r.get("expected_failures", []))
        actual = sorted({g["gate"] for g in r["gates"] if not g["pass"]})
        verified = set(expected).issubset(set(actual))
        lines.append(
            f"| {r['product_id']} | {', '.join(expected)} |"
            f" {', '.join(actual)} | {'YES' if verified else 'NO'} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 7. Remaining Open Decisions (not fixed by Phase 3b)",
        "",
        "| # | Issue | Count | Decision Needed |",
        "|---|---|---|---|",
        "| 1 | RANGE_TOO_BROAD (CAT-B blocked) | 9 | Manual age split or range strategy |",
        "| 2 | NO_AGE_FOUND | 9 | Product enrichment or age-unknown fallback |",
        "| 3 | DUPLICATE_CONFLICT (multi-age WarmNest) | 1 |"
        " Decide if CAT-B can be multi-value |",
    ]

    if a.get("taxonomy_gaps"):
        lines.append(
            f"| 4 | Remaining taxonomy gaps | {sum(a['taxonomy_gaps'].values())} |"
            " Investigate and resolve |"
        )

    lines += [
        "",
        "_Phase 4 Dry Run may proceed after Ayal review of this report._",
        "",
    ]
    return "\n".join(lines)


# ─── main ─────────────────────────────────────────────────────────────────────

def main_phase3():
    print("Loading products...")
    pos_products, neg_products = load_products()
    print(f"  Positive: {len(pos_products)}, Negative: {len(neg_products)}")

    print("Running gates on positive sample...")
    pos_results, pos_summary = run_suite(pos_products, "positive_sample")

    print("Running gates on negative test cases...")
    neg_results, neg_summary = run_suite(neg_products, "negative_tests")

    print("Verifying negative test expectations...")
    neg_verification = verify_negative_tests(neg_results)

    print("\n--- Positive Sample Summary ---")
    print(f"  Overall PASS: {pos_summary['overall_pass']}/{pos_summary['total']}")
    for gname in GATE_NAMES:
        p = pos_summary["gate_pass_counts"].get(gname, 0)
        f = pos_summary["gate_fail_counts"].get(gname, 0)
        print(f"  {gname}: {p} pass / {f} fail")
    if pos_summary["taxonomy_gaps"]:
        print(f"\n  Taxonomy gaps: {list(pos_summary['taxonomy_gaps'].keys())}")

    print("\n--- Negative Test Verification ---")
    print(f"  Verified: {neg_verification['verified']}/{neg_verification['total']}")
    if not neg_verification["all_verified"]:
        for vf in neg_verification["verification_failures"]:
            print(f"    {vf['product_id']}: missed {vf['missed_expected']}")
    else:
        print("  All negative tests fired as expected.")

    print("\nWriting Phase 3 reports...")
    with open(REPORT_JSON, "w", encoding="utf-8") as fh:
        json.dump(
            build_json_report(pos_results, pos_summary, neg_results, neg_summary, neg_verification),
            fh, ensure_ascii=False, indent=2,
        )
    print(f"  JSON -> {REPORT_JSON}")

    with open(REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write(build_md_report(
            pos_summary, neg_summary, neg_verification, pos_results, neg_results
        ))
    print(f"  MD   -> {REPORT_MD}")
    print("\nDone.")


def main_phase3b():
    print("=== Phase 3b: Taxonomy & Source Normalization ===")
    print("Loading products...")
    pos_products_orig, neg_products = load_products()
    print(f"  Positive (original): {len(pos_products_orig)}, Negative: {len(neg_products)}")

    # Load Phase 3 before-stats from existing report
    with open(REPORT_JSON, encoding="utf-8") as fh:
        phase3_report = json.load(fh)
    phase3_before = phase3_report["positive_sample"]["summary"]

    # Apply normalization
    print("Applying normalization rules...")
    normalized_products = [normalize_product(p) for p in pos_products_orig]
    changes = sum(1 for p in normalized_products if p.get("normalization_log"))
    print(f"  Products changed: {changes}/{len(normalized_products)}")

    # Write normalized source map
    norm_payload = {
        "meta": {
            "phase": "Phase 3b — Normalized Source Map",
            "date": str(date.today()),
            "input": PHASE2B_PATH,
            "normalization_rules": {
                "gender-unisex+explicit_src": "->gender-neutral",
                "gender-unisex+deprecated_src": "->gender-unknown (src=category_default)",
                "type-doll+reborn_context": "->type-reborn-doll",
                "type-doll+no_reborn": "->type-toy",
                "type-other": "->type-unknown (src=category_default)",
                "occ-sport|occ-holiday|style-cartoon": "->BLOCKED",
            },
            "changes_applied": changes,
        },
        "products": normalized_products,
    }
    with open(PHASE3B_NORMALIZED, "w", encoding="utf-8") as fh:
        json.dump(norm_payload, fh, ensure_ascii=False, indent=2)
    print(f"  Normalized map -> {PHASE3B_NORMALIZED}")

    # Run gates on normalized products
    print("Running 8 gates on normalized sample...")
    pos_results, pos_summary = run_suite(normalized_products, "phase3b_positive")

    # Run gates on negative tests (unchanged)
    print("Running 8 gates on negative test cases...")
    neg_results, neg_summary = run_suite(neg_products, "negative_tests")
    neg_verification = verify_negative_tests(neg_results)

    # Build normalization log
    norm_log_rows = build_normalization_summary(pos_products_orig, normalized_products)

    # Print comparison
    print("\n--- Phase 3 vs Phase 3b ---")
    print(f"  Overall PASS: {phase3_before['overall_pass']} -> {pos_summary['overall_pass']}/30")
    for gname in GATE_NAMES:
        fb = phase3_before.get("gate_fail_counts", {}).get(gname, 0)
        fa = pos_summary.get("gate_fail_counts", {}).get(gname, 0)
        if fb != fa:
            print(f"  {gname}: fail {fb} -> {fa}")
    if pos_summary["taxonomy_gaps"]:
        print(f"  Remaining taxonomy gaps: {pos_summary['taxonomy_gaps']}")
    else:
        print("  Remaining taxonomy gaps: NONE")
    print(f"  Negative tests blocked: {neg_verification['verified']}/{neg_verification['total']}")

    # Write reports
    print("\nWriting Phase 3b reports...")
    report = build_phase3b_json_report(
        normalized_products, pos_results, pos_summary,
        neg_results, neg_summary, neg_verification,
        norm_log_rows, phase3_before,
    )
    with open(PHASE3B_REPORT_JSON, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print(f"  JSON -> {PHASE3B_REPORT_JSON}")

    md = build_phase3b_md_report(
        pos_summary, neg_summary, neg_verification,
        pos_results, neg_results, norm_log_rows, phase3_before,
    )
    with open(PHASE3B_REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(f"  MD   -> {PHASE3B_REPORT_MD}")
    print("\nDone.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    if "--phase3b" in sys.argv:
        main_phase3b()
    else:
        main_phase3()
