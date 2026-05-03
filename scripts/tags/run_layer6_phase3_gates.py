"""
Layer 6 — Phase 3 Validation Gates Runner
Reads phase2b sample (30 products) + negative test cases (10),
runs all 8 gates, writes JSON and MD reports.
"""

import json
import sys
import os
from datetime import date
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from layer6_validate_tags import run_all_gates

PHASE2B_PATH = "output/tags/phase2b-age-hardening-sample-30.json"
NEG_TESTS_PATH = "output/tags/phase3-negative-test-cases.json"
REPORT_JSON = "output/tags/phase3-validation-gates-report.json"
REPORT_MD = "output/tags/phase3-validation-gates-report.md"

GATE_NAMES = [
    "SOURCE_EXISTS", "FORMAT_VALID", "ALLOWED_VALUE", "SOURCE_TRACEABLE",
    "NO_FORBIDDEN_INFERENCE", "CATEGORY_COVERAGE", "DUPLICATE_CONFLICT", "QUALITY_SCORE",
]


def load_products():
    with open(PHASE2B_PATH, encoding="utf-8") as f:
        phase2b = json.load(f)
    products = phase2b["products"]
    for p in products:
        p["is_negative_test"] = False

    with open(NEG_TESTS_PATH, encoding="utf-8") as f:
        neg = json.load(f)
    neg_products = neg["products"]

    return products, neg_products


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
        results.append(r)

        if r["overall_pass"]:
            overall_pass += 1
        for gate_result in r["gates"]:
            gname = gate_result["gate"]
            if gate_result["pass"]:
                gate_pass_counts[gname] += 1
            else:
                gate_fail_counts[gname] += 1
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
    """Check that each negative test failed at least its expected gates."""
    passed_verification = 0
    failures = []
    for r in neg_results:
        expected = set(r.get("expected_failures", []))
        actual_fails = {g["gate"] for g in r["gates"] if not g["pass"]}
        if expected.issubset(actual_fails):
            passed_verification += 1
        else:
            missed = expected - actual_fails
            failures.append({
                "product_id": r["product_id"],
                "expected_failures": list(expected),
                "actual_failures": list(actual_fails),
                "missed_expected": list(missed),
            })
    return {
        "total": len(neg_results),
        "verified": passed_verification,
        "verification_failures": failures,
        "all_verified": len(failures) == 0,
    }


def build_json_report(
    pos_results, pos_summary, neg_results, neg_summary, neg_verification
):
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
        "positive_sample": {
            "summary": pos_summary,
            "products": pos_results,
        },
        "negative_tests": {
            "summary": neg_summary,
            "verification": neg_verification,
            "products": neg_results,
        },
    }


def build_md_report(pos_summary, neg_summary, neg_verification, pos_results, neg_results):
    total_tax_gaps = sum(pos_summary["taxonomy_gaps"].values()) + sum(neg_summary["taxonomy_gaps"].values())
    all_tax_gaps = {}
    for tag, cnt in {**pos_summary["taxonomy_gaps"], **neg_summary["taxonomy_gaps"]}.items():
        all_tax_gaps[tag] = all_tax_gaps.get(tag, 0) + cnt

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
        f"| Metric | Value |",
        f"|---|---|",
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
        p = pos_summary["gate_pass_counts"].get(gname, 0)
        f = pos_summary["gate_fail_counts"].get(gname, 0)
        lines.append(f"| {gname} | {p} | {f} |")

    if pos_summary["taxonomy_gaps"]:
        lines += [
            "",
            "### Taxonomy Gaps Found — Positive Sample",
            "",
            "| Tag | Count | Note |",
            "|---|---|---|",
        ]
        GAP_NOTES = {
            "gender-unisex": "spec uses gender-neutral",
            "style-cartoon": "not in taxonomy spec",
            "style-boho": "not in taxonomy spec",
            "style-minimal": "not in taxonomy spec",
            "type-other": "spec uses type-unknown",
            "type-bag": "not in taxonomy spec",
            "type-socks": "not in taxonomy spec",
            "type-slippers": "not in taxonomy spec",
            "type-blanket": "not in taxonomy spec",
            "type-pajama": "not in taxonomy spec",
            "type-cardigan": "not in taxonomy spec",
            "type-shirt": "not in taxonomy spec",
            "occ-sport": "not in taxonomy spec",
            "occ-holiday": "not in taxonomy spec",
        }
        for tag, cnt in sorted(pos_summary["taxonomy_gaps"].items()):
            note = GAP_NOTES.get(tag, "")
            lines.append(f"| `{tag}` | {cnt} | {note} |")
    else:
        lines += ["", "_No taxonomy gaps in positive sample._"]

    lines += [
        "",
        "---",
        "",
        "## 2. Negative Test Cases (10 synthetic failure scenarios)",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total test cases | {neg_summary['total']} |",
        f"| Verification passed (all expected gates fired) | **{neg_verification['verified']}/{neg_verification['total']}** |",
        f"| All verified | {'YES' if neg_verification['all_verified'] else 'NO'} |",
        "",
        "### Gate Results — Negative Tests",
        "",
        "| Gate | PASS | FAIL |",
        "|---|---|---|",
    ]
    for gname in GATE_NAMES:
        p = neg_summary["gate_pass_counts"].get(gname, 0)
        f = neg_summary["gate_fail_counts"].get(gname, 0)
        lines.append(f"| {gname} | {p} | {f} |")

    lines += [
        "",
        "### Negative Test Verification Detail",
        "",
        "| ID | Expected Failures | Actual Failures | Verified |",
        "|---|---|---|---|",
    ]
    for r in neg_results:
        expected = set(r.get("expected_failures", []))
        actual = {g["gate"] for g in r["gates"] if not g["pass"]}
        verified = expected.issubset(actual)
        lines.append(
            f"| {r['product_id']} | {', '.join(sorted(expected))} | "
            f"{', '.join(sorted(actual))} | {'YES' if verified else 'NO'} |"
        )

    if neg_verification["verification_failures"]:
        lines += ["", "**Verification failures:**", ""]
        for vf in neg_verification["verification_failures"]:
            lines.append(f"- `{vf['product_id']}`: missed gates {vf['missed_expected']}")

    lines += [
        "",
        "---",
        "",
        "## 3. Per-Product Detail — Positive Sample",
        "",
    ]
    for r in pos_results:
        fail_gates = [g["gate"] for g in r["gates"] if not g["pass"]]
        status_icon = "PASS" if r["overall_pass"] else "FAIL"
        pid = r["product_id"]
        title = r["title"][:50] + ("..." if len(r["title"]) > 50 else "")
        lines.append(f"**{pid}** — {title} — `{status_icon}`")
        if fail_gates:
            lines.append(f"  - Failed gates: {', '.join(fail_gates)}")
        if r["taxonomy_gaps"]:
            lines.append(f"  - Taxonomy gaps: {', '.join(r['taxonomy_gaps'])}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 4. Open Decisions",
        "",
        "| # | Issue | Count | Decision Needed |",
        "|---|---|---|---|",
        "| 1 | RANGE_TOO_BROAD products (CAT-B blocked) | 9 | Manual age split or range-tag strategy |",
        "| 2 | NO_AGE_FOUND products | 9 | Product enrichment or age-unknown fallback |",
        f"| 3 | TAXONOMY_GAP tags (positive sample) | {len(pos_summary['taxonomy_gaps'])} unique | Migrate to valid values or extend spec |",
        "",
        "_Phase 4 Dry Run is gated on reviewing these open decisions._",
        "",
    ]
    return "\n".join(lines)


def main():
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
        print("  FAILURES:")
        for vf in neg_verification["verification_failures"]:
            print(f"    {vf['product_id']}: missed {vf['missed_expected']}")
    else:
        print("  All negative tests fired as expected.")

    print("\nWriting reports...")
    report = build_json_report(
        pos_results, pos_summary, neg_results, neg_summary, neg_verification
    )
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  JSON -> {REPORT_JSON}")

    md = build_md_report(pos_summary, neg_summary, neg_verification, pos_results, neg_results)
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  MD   -> {REPORT_MD}")
    print("\nDone.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    main()
