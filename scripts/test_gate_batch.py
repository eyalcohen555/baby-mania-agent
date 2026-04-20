#!/usr/bin/env python3
"""
Test Gate Batch — P1-S6 Verification
AUTOMATION-HARDENING-PLAN v1

Runs Gate 1 + Gate 2 on a controlled test batch of 8 cases:
  4 real products (should PASS)
  1 fingerprint injection (should FAIL check_a)
  1 type mismatch injection (should FAIL check_b)
  1 anomaly PID control (should FAIL gate1 anomaly_exclusion)
  1 fabricated claim injection (should FAIL check_c)

Usage: python test_gate_batch.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import yaml

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"

# ── Load gate modules ─────────────────────────────────────────────────────────

def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

g1 = _load_module("gate1", BASE_DIR / "scripts" / "gate1_hardening.py")
g2 = _load_module("gate2", BASE_DIR / "scripts" / "gate2_semantic.py")

# ── Real product PIDs (must have publisher.json + context.yaml) ───────────────

REAL_PIDS = [
    "10005779710265",
    "10005779743033",
    "10005779808569",
    "10005779841337",
]

ANOMALY_PID = "9881362759993"


# ── Synthetic Test Cases ───────────────────────────────────────────────────────

def _load_real_pub(pid: str) -> dict | None:
    p = STAGE_OUT_DIR / f"{pid}_publisher.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _load_real_ctx(pid: str) -> dict | None:
    p = CONTEXT_DIR / f"{pid}.yaml"
    if not p.exists():
        return None
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def make_fingerprint_case(base_pub: dict) -> dict:
    """Inject a technical fingerprint into hero_headline."""
    pub = copy.deepcopy(base_pub)
    pub["product_id"] = "TEST_FINGERPRINT"
    pub["metafields"]["hero_headline"] = "חליפת חורף איכותית (1113) לתינוקות"
    return pub


def make_type_mismatch_case(base_pub: dict) -> dict:
    """Inject a shoe term into a clothing product's headline."""
    pub = copy.deepcopy(base_pub)
    pub["product_id"] = "TEST_TYPE_MISMATCH"
    pub["product_template_type"] = "clothing"
    pub["metafields"]["hero_headline"] = "הסוליה הגמישה עוטפת את רגלי התינוק"
    return pub


def make_fabricated_claim_case(base_pub: dict) -> dict:
    """Inject a star rating into product with has_reviews=false."""
    pub = copy.deepcopy(base_pub)
    pub["product_id"] = "TEST_FABRICATED_CLAIM"
    pub["metafields"]["emotional_reassurance"] = "4.9 כוכבים — הורים ממליצים בחום על החליפה הזו"
    return pub


def make_anomaly_pub(base_pub: dict) -> dict:
    """Create a publisher record with the known anomaly PID."""
    pub = copy.deepcopy(base_pub)
    pub["product_id"] = ANOMALY_PID
    return pub


# ── Test Runner ───────────────────────────────────────────────────────────────

def run_test(label: str, pid: str, pub_data: dict, ctx: dict,
             expect_gate1: str = "PASS", expect_gate2: str = "PASS") -> bool:
    """Run both gates and compare to expected result. Returns True if test passes."""
    g1_result = g1.run_gate1_extended(pid, pub_data, save_result=False)
    g2_result = g2.run_gate2(pid, pub_data, ctx, save_result=False)

    g1_ok = g1_result["status"] == expect_gate1
    g2_ok = g2_result["status"] == expect_gate2

    overall = "✓ PASS" if (g1_ok and g2_ok) else "✗ FAIL"
    print(f"\n  [{overall}] {label}")
    print(f"    Gate1: {g1_result['status']} (expected {expect_gate1}) {'✓' if g1_ok else '✗'}")
    if g1_result.get("fail_reasons"):
        for fr in g1_result["fail_reasons"]:
            print(f"      - [{fr['check']}] {fr['detail']}")
    print(f"    Gate2: {g2_result['status']} (expected {expect_gate2}) {'✓' if g2_ok else '✗'}")
    if g2_result.get("fail_reasons"):
        for fr in g2_result["fail_reasons"]:
            print(f"      - [{fr['check']}] {fr['detail']}")
    print(f"    check_e: {g2_result.get('check_e_status')} (should be DISABLED)")

    return g1_ok and g2_ok


def main() -> int:
    print("=" * 60)
    print("TEST GATE BATCH — P1-S6 Verification")
    print("AUTOMATION-HARDENING-PLAN v1")
    print("=" * 60)

    results: list[bool] = []
    base_pub = _load_real_pub(REAL_PIDS[0])
    base_ctx = _load_real_ctx(REAL_PIDS[0])

    if not base_pub or not base_ctx:
        print(f"ERROR: Cannot load real product {REAL_PIDS[0]} — aborting test")
        return 1

    # ── Real products: should PASS ────────────────────────────────────────────
    print("\n── Real Products (expected: PASS) ──")
    for pid in REAL_PIDS:
        pub = _load_real_pub(pid)
        ctx = _load_real_ctx(pid)
        if not pub or not ctx:
            print(f"  [SKIP] {pid} — missing files")
            continue
        ok = run_test(f"Real product {pid}", pid, pub, ctx,
                      expect_gate1="PASS", expect_gate2="PASS")
        results.append(ok)

    # ── Anomaly PID: Gate1 should FAIL (anomaly_exclusion) ───────────────────
    print("\n── Anomaly Control (expected: Gate1 FAIL) ──")
    anomaly_pub = make_anomaly_pub(base_pub)
    ok = run_test("Anomaly PID 9881362759993", ANOMALY_PID, anomaly_pub, base_ctx,
                  expect_gate1="FAIL", expect_gate2="PASS")
    results.append(ok)

    # ── Synthetic: Fingerprint — Gate2 should FAIL ────────────────────────────
    print("\n── Synthetic: Technical Fingerprint (expected: Gate2 FAIL) ──")
    fp_pub = make_fingerprint_case(base_pub)
    ok = run_test("Fingerprint injection", "TEST_FINGERPRINT", fp_pub, base_ctx,
                  expect_gate1="PASS", expect_gate2="FAIL")
    results.append(ok)

    # ── Synthetic: Type Mismatch — Gate2 should FAIL ─────────────────────────
    print("\n── Synthetic: Type Mismatch (expected: Gate2 FAIL) ──")
    tm_pub = make_type_mismatch_case(base_pub)
    ok = run_test("Type mismatch injection", "TEST_TYPE_MISMATCH", tm_pub, base_ctx,
                  expect_gate1="PASS", expect_gate2="FAIL")
    results.append(ok)

    # ── Synthetic: Fabricated Claim — Gate2 should FAIL ─────────────────────
    print("\n── Synthetic: Fabricated Claim (expected: Gate2 FAIL) ──")
    fc_pub  = make_fabricated_claim_case(base_pub)
    fc_ctx  = copy.deepcopy(base_ctx)
    fc_ctx.setdefault("fallback_flags", {})["has_reviews"] = False
    ok = run_test("Fabricated claim injection", "TEST_FABRICATED_CLAIM", fc_pub, fc_ctx,
                  expect_gate1="PASS", expect_gate2="FAIL")
    results.append(ok)

    # ── Check E confirmation: must be DISABLED ────────────────────────────────
    print("\n── Check E Status ──")
    g2_test = g2.run_gate2("CHECK_E_TEST", base_pub, base_ctx, save_result=False)
    check_e_disabled = g2_test.get("check_e_status") == "DISABLED"
    print(f"  check_e_status = '{g2_test.get('check_e_status')}' — {'✓ DISABLED as required' if check_e_disabled else '✗ SHOULD BE DISABLED'}")
    results.append(check_e_disabled)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    passed = sum(results)
    total  = len(results)
    print(f"TEST BATCH RESULT: {passed}/{total} passed")
    if passed == total:
        print("✓ ALL TESTS PASSED — Gate 1 + Gate 2 operating correctly")
        print("  Check E: DISABLED (awaiting Ayel threshold approval)")
    else:
        print(f"✗ {total - passed} TESTS FAILED — review output above")
    print("=" * 60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
