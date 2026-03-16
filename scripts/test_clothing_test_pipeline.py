#!/usr/bin/env python3
"""
BabyMania — clothing-test Pipeline Test
========================================
Steps:
  1. Verify 10 selected clothing products + report current template
  2. Update template_suffix → clothing-test
  3. Run orchestrator push (writes metafields) for each product
     NOTE: push will reset suffix → "clothing"; we re-apply "clothing-test" after.
  4. Verify metafields written (baby_mania namespace, required keys)
  5. Verify section data mapping (logical render check)
  6. Print final report

Usage:
  python scripts/test_clothing_test_pipeline.py
"""
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

# ── Env ───────────────────────────────────────────────────────────────────────
load_dotenv(BASE_DIR / ".env")
tok_path = Path.home() / "Desktop/shopify-token/.env"
if tok_path.exists():
    load_dotenv(tok_path, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = os.getenv("SHOPIFY_SHOP_URL", "a2756c-c0.myshopify.com")
API   = f"https://{SHOP}/admin/api/2024-10"
HDR   = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

# ── Test Products (10 clothing products with STATUS:PASS pipeline outputs) ────
TEST_PIDS = [
    "10009173033273",
    "10029648970041",
    "10029649101113",
    "10029649133881",
    "9657091293497",
    "9673732292921",
    "9687596728633",
    "9688660312377",
    "9688932909369",
    "9688934940985",
]

# Required metafields (from config.yaml)
REQUIRED_METAFIELDS = [
    "hero_eyebrow", "hero_headline", "hero_subheadline",
    "fabric_title", "fabric_body", "fabric_highlight", "fabric_tags",
    "whats_special", "benefits", "emotional_reassurance",
    "care_instructions", "faq",
]

# Section → metafield mapping (for render verification)
SECTION_METAFIELD_MAP = {
    "bm-store-banner":   ["hero_eyebrow", "hero_headline", "hero_subheadline"],
    "bm-store-fabric":   ["fabric_title", "fabric_body", "fabric_highlight", "fabric_tags"],
    "bm-store-benefits": ["benefits", "whats_special", "emotional_reassurance"],
    "bm-store-sizes":    [],   # handled by product variants — no custom metafield required
    "bm-store-care":     ["care_instructions"],
    "bm-store-faq":      ["faq"],
    "bm-store-urgency":  [],   # stock_level / units_left (optional — may be absent)
    "bm-store-contact":  [],   # whatsapp_number / whatsapp_message (optional)
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def shopify_get(path: str) -> dict:
    r = requests.get(f"{API}/{path}", headers=HDR, timeout=15)
    r.raise_for_status()
    return r.json()


def shopify_put(path: str, payload: dict) -> dict:
    r = requests.put(f"{API}/{path}", headers=HDR, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def set_template_suffix(pid: str, suffix: str) -> bool:
    """Update template_suffix for a product. Returns True on success."""
    try:
        shopify_put(
            f"products/{pid}.json",
            {"product": {"id": int(pid), "template_suffix": suffix}},
        )
        return True
    except Exception as e:
        print(f"  ERROR set_template_suffix({pid}, {suffix}): {e}")
        return False


def run_orchestrator(cmd: str, pid: str) -> int:
    """Run orchestrator.py with a command and product ID. Returns exit code."""
    orch = BASE_DIR / "00-team-lead" / "orchestrator.py"
    result = subprocess.run(
        [sys.executable, str(orch), cmd, pid],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        for line in result.stdout.strip().splitlines():
            print(f"    | {line}")
    if result.returncode != 0 and result.stderr:
        for line in result.stderr.strip().splitlines()[-5:]:
            print(f"    ERR| {line}")
    return result.returncode


def get_metafields(pid: str) -> dict:
    """Fetch baby_mania metafields for a product. Returns {key: value}."""
    resp = shopify_get(f"products/{pid}/metafields.json?namespace=baby_mania&limit=250")
    return {mf["key"]: mf["value"] for mf in resp.get("metafields", [])}


def get_product(pid: str) -> dict:
    """Fetch product details from Shopify."""
    return shopify_get(f"products/{pid}.json")["product"]


# ── Section render verification ───────────────────────────────────────────────

def verify_section_data(section: str, metafields: dict) -> tuple[bool, list[str]]:
    """
    Check that required metafields for a section are present and non-empty.
    Returns (ok: bool, missing_keys: list).
    """
    required = SECTION_METAFIELD_MAP.get(section, [])
    if not required:
        return True, []  # no required metafields — section uses product data or optional mf
    missing = [k for k in required if not metafields.get(k)]
    return len(missing) == 0, missing


# ── Main pipeline test ────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
        sys.exit(1)

    sep = "=" * 70
    print(sep)
    print("BabyMania — clothing-test Pipeline Test")
    print(f"Products: {len(TEST_PIDS)}  |  Target suffix: clothing-test")
    print(sep)

    # ─── STEP 1: Fetch current product state ─────────────────────────────────
    print("\n" + "─" * 70)
    print("STEP 1 — Current product state")
    print("─" * 70)
    products_info = {}
    step1_rows = []
    for pid in TEST_PIDS:
        try:
            p = get_product(pid)
            products_info[pid] = {
                "title":            p.get("title", ""),
                "handle":           p.get("handle", ""),
                "template_suffix":  p.get("template_suffix") or "",
                "status":           p.get("status", ""),
            }
            step1_rows.append((pid, p.get("handle",""), p.get("title","")[:45],
                               p.get("template_suffix") or ""))
        except Exception as e:
            products_info[pid] = {"title": "ERROR", "handle": "", "template_suffix": "?", "status": "?"}
            step1_rows.append((pid, "?", "ERROR", str(e)))
        time.sleep(0.2)

    print(f"{'product_id':<20} {'handle':<40} {'title':<45} {'current_template'}")
    print("-" * 120)
    for pid, handle, title, suffix in step1_rows:
        print(f"{pid:<20} {handle:<40} {title:<45} {suffix}")

    # ─── STEP 2: Update template_suffix → clothing-test ─────────────────────
    print("\n" + "─" * 70)
    print("STEP 2 — Update template_suffix → clothing-test")
    print("─" * 70)
    print(f"{'PRODUCT ID':<20} {'OLD TEMPLATE':<20} {'NEW TEMPLATE':<20} {'STATUS'}")
    print("-" * 80)
    step2_results = {}
    for pid in TEST_PIDS:
        old_suffix = products_info[pid].get("template_suffix", "")
        ok = set_template_suffix(pid, "clothing-test")
        status = "OK" if ok else "FAIL"
        new_suffix = "clothing-test" if ok else old_suffix
        step2_results[pid] = {"old": old_suffix, "new": new_suffix, "ok": ok}
        print(f"{pid:<20} {old_suffix:<20} {new_suffix:<20} {status}")
        time.sleep(0.3)

    # ─── STEP 3: Run orchestrator push (writes metafields) ───────────────────
    print("\n" + "─" * 70)
    print("STEP 3 — Run pipeline push (metafields → Shopify)")
    print("─" * 70)
    print("NOTE: push resets suffix → 'clothing'; will re-apply 'clothing-test' after.")
    push_results = {}
    for pid in TEST_PIDS:
        title = products_info[pid].get("title", pid)[:50]
        print(f"\n  [{pid}] {title}")
        rc = run_orchestrator("push", pid)
        push_results[pid] = {"rc": rc, "ok": rc == 0}
        if rc == 0:
            # Re-apply clothing-test (push sets it back to "clothing")
            re_ok = set_template_suffix(pid, "clothing-test")
            push_results[pid]["reapply_suffix"] = re_ok
            suffix_status = "clothing-test ✓" if re_ok else "RE-APPLY FAILED"
            print(f"  → push OK  |  suffix re-applied: {suffix_status}")
        else:
            push_results[pid]["reapply_suffix"] = False
            print(f"  → push FAILED (exit code {rc})")
        time.sleep(0.5)

    # ─── STEP 4: Verify metafields in Shopify ────────────────────────────────
    print("\n" + "─" * 70)
    print("STEP 4 — Verify metafields written")
    print("─" * 70)
    mf_results  = {}
    print(f"{'PRODUCT ID':<20} {'METAFIELDS WRITTEN':<22} {'STATUS'}")
    print("-" * 60)
    for pid in TEST_PIDS:
        if not push_results.get(pid, {}).get("ok"):
            mf_results[pid] = {"mf": {}, "present": 0, "missing": REQUIRED_METAFIELDS.copy(), "ok": False}
            print(f"{pid:<20} {'SKIPPED (push failed)':<22} FAIL")
            continue
        try:
            mf = get_metafields(pid)
            present_keys = [k for k in REQUIRED_METAFIELDS if mf.get(k)]
            missing_keys = [k for k in REQUIRED_METAFIELDS if not mf.get(k)]
            ok = len(missing_keys) == 0
            status = "OK" if ok else f"MISSING {len(missing_keys)}"
            mf_results[pid] = {"mf": mf, "present": len(present_keys), "missing": missing_keys, "ok": ok}
            print(f"{pid:<20} {len(present_keys)}/{len(REQUIRED_METAFIELDS)}  {REQUIRED_METAFIELDS[0]}...{'':>5} {status}")
            if missing_keys:
                print(f"  ↳ Missing: {', '.join(missing_keys)}")
        except Exception as e:
            mf_results[pid] = {"mf": {}, "present": 0, "missing": REQUIRED_METAFIELDS.copy(), "ok": False, "error": str(e)}
            print(f"{pid:<20} {'ERROR':<22} FAIL  ({e})")
        time.sleep(0.2)

    # ─── STEP 5: Section render verification ─────────────────────────────────
    print("\n" + "─" * 70)
    print("STEP 5 — Section render verification")
    print("─" * 70)

    sections = list(SECTION_METAFIELD_MAP.keys())
    section_results = {}   # pid → {section: (ok, missing)}

    print(f"{'PRODUCT ID':<20} {'SECTION':<30} {'DATA FOUND':<15} {'STATUS'}")
    print("-" * 80)
    for pid in TEST_PIDS:
        mf = mf_results.get(pid, {}).get("mf", {})
        section_results[pid] = {}
        for section in sections:
            ok, missing = verify_section_data(section, mf)
            section_results[pid][section] = (ok, missing)
            data_found = "YES" if ok else f"MISSING {len(missing)}"
            status = "PASS" if ok else "WARN"
            print(f"{pid:<20} {section:<30} {data_found:<15} {status}")
            if missing:
                print(f"  {'':>20} ↳ {', '.join(missing)}")

    # ─── STEP 3b: Verify template_suffix is clothing-test ────────────────────
    print("\n" + "─" * 70)
    print("STEP 2b — Verify final template_suffix")
    print("─" * 70)
    suffix_verify = {}
    print(f"{'PRODUCT ID':<20} {'TEMPLATE':<25} {'STATUS'}")
    print("-" * 50)
    for pid in TEST_PIDS:
        try:
            p = get_product(pid)
            current = p.get("template_suffix") or ""
            ok = current == "clothing-test"
            suffix_verify[pid] = current
            print(f"{pid:<20} {current:<25} {'OK' if ok else 'WRONG'}")
        except Exception as e:
            suffix_verify[pid] = "ERROR"
            print(f"{pid:<20} {'ERROR':<25} FAIL ({e})")
        time.sleep(0.2)

    # ─── FINAL REPORT ────────────────────────────────────────────────────────
    print("\n" + sep)
    print("FINAL REPORT")
    print(sep)

    total = len(TEST_PIDS)
    push_ok     = sum(1 for pid in TEST_PIDS if push_results.get(pid, {}).get("ok"))
    mf_ok       = sum(1 for pid in TEST_PIDS if mf_results.get(pid, {}).get("ok"))
    suffix_ok   = sum(1 for pid in TEST_PIDS if suffix_verify.get(pid) == "clothing-test")
    failed_pids = [pid for pid in TEST_PIDS if not mf_results.get(pid, {}).get("ok")]

    # Section stats
    section_pass_total = 0
    section_total      = 0
    for pid in TEST_PIDS:
        for s, (ok, _) in section_results.get(pid, {}).items():
            section_total += 1
            if ok:
                section_pass_total += 1

    errors = []
    for pid in TEST_PIDS:
        if not push_results.get(pid, {}).get("ok"):
            errors.append(f"  push FAILED: {pid}")
        if not push_results.get(pid, {}).get("reapply_suffix"):
            errors.append(f"  suffix re-apply FAILED: {pid}")
        for k in mf_results.get(pid, {}).get("missing", []):
            errors.append(f"  missing metafield '{k}': {pid}")

    # Risk level
    if len(failed_pids) == 0 and suffix_ok == total:
        risk = "LOW — all products ready"
    elif len(failed_pids) <= 2:
        risk = "MEDIUM — minor failures"
    else:
        risk = "HIGH — multiple failures"

    print(f"\n  PRODUCTS TESTED:    {total}")
    print(f"  PUSH SUCCEEDED:     {push_ok}/{total}")
    print(f"  METAFIELDS WRITTEN: {mf_ok}/{total}")
    print(f"  SECTIONS RENDERED:  {section_pass_total}/{section_total}")
    print(f"  SUFFIX=clothing-test:{suffix_ok}/{total}")
    print(f"  FAILED PRODUCTS:    {len(failed_pids)}")
    if failed_pids:
        for p in failed_pids:
            print(f"    - {p}  {products_info.get(p,{}).get('title','')[:40]}")
    print(f"\n  ERRORS:             {len(errors)}")
    for e in errors[:20]:
        print(f"    {e}")
    print(f"\n  RISK LEVEL:         {risk}")
    print(sep)

    # Save JSON report
    report = {
        "products_tested":      total,
        "push_succeeded":       push_ok,
        "metafields_written":   mf_ok,
        "sections_rendered":    f"{section_pass_total}/{section_total}",
        "suffix_clothing_test": suffix_ok,
        "failed_products":      failed_pids,
        "errors":               errors,
        "risk_level":           risk,
        "step2_table":          step2_results,
        "mf_results":           {k: {kk: vv for kk, vv in v.items() if kk != "mf"} for k, v in mf_results.items()},
        "section_results":      {
            pid: {s: {"ok": ok, "missing": miss} for s, (ok, miss) in sr.items()}
            for pid, sr in section_results.items()
        },
    }
    report_path = BASE_DIR / "output" / "clothing_test_pipeline_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  Report saved → {report_path}")


if __name__ == "__main__":
    # Force UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    elif hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
