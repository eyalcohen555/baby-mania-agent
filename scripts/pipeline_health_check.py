#!/usr/bin/env python3
"""
BabyMania — Pipeline Health Check
Checks: V2 format, metafield count, template suffix, missing fields, section coverage.
"""
import io, json, os, sys, time
from pathlib import Path
from dotenv import load_dotenv
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

load_dotenv(BASE_DIR / ".env")
tok = Path.home() / "Desktop/shopify-token/.env"
if tok.exists():
    load_dotenv(tok, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
HDR   = {"X-Shopify-Access-Token": TOKEN}
API   = f"https://{SHOP}/admin/api/2024-10"

REQUIRED_MF = [
    "hero_eyebrow", "hero_headline", "hero_subheadline",
    "fabric_title", "fabric_body", "fabric_highlight", "fabric_tags",
    "whats_special", "benefits", "emotional_reassurance",
    "care_instructions", "faq",
]

SECTION_MAP = {
    "bm-store-banner":   ["hero_eyebrow", "hero_headline", "hero_subheadline"],
    "bm-store-fabric":   ["fabric_title", "fabric_body", "fabric_highlight", "fabric_tags"],
    "bm-store-benefits": ["benefits", "whats_special", "emotional_reassurance"],
    "bm-store-sizes":    [],
    "bm-store-care":     ["care_instructions"],
    "bm-store-faq":      ["faq"],
    "bm-store-urgency":  [],
    "bm-store-contact":  [],
}

VALID_SUFFIXES = {"clothing", "clothing-test", "general", "tempio", "easy-sleep", ""}


def shopify_get(path):
    r = requests.get(f"{API}/{path}", headers=HDR, timeout=15)
    r.raise_for_status()
    return r.json()


def get_metafields(pid):
    resp = shopify_get(f"products/{pid}/metafields.json?namespace=baby_mania&limit=250")
    return {mf["key"]: mf["value"] for mf in resp.get("metafields", [])}


def get_product(pid):
    return shopify_get(f"products/{pid}.json")["product"]


def check_publisher_format(pid):
    path = STAGE_OUT_DIR / f"{pid}_publisher.json"
    if not path.exists():
        return "NO_FILE", None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return "PARSE_ERROR", None
    if "metafields" in data and data["metafields"]:
        return "V2", data
    if "fabric" in data or "care" in data:
        return "V1", data
    return "EMPTY", data


# ── Collect all PIDs that have a publisher.json ────────────────────────────────
all_pids = sorted(
    f.stem.replace("_publisher", "")
    for f in STAGE_OUT_DIR.glob("*_publisher.json")
)

print(f"Products with publisher.json: {len(all_pids)}")
print("Fetching Shopify data...\n")

rows = []
for pid in all_pids:
    fmt, pub_data = check_publisher_format(pid)

    # Shopify live data
    try:
        product   = get_product(pid)
        suffix    = product.get("template_suffix") or ""
        title     = product.get("title", "")[:40]
        live_mf   = get_metafields(pid)
    except Exception as e:
        rows.append({
            "pid": pid, "title": "FETCH ERROR", "fmt": fmt,
            "suffix": "?", "suffix_ok": False,
            "mf_count": 0, "missing": REQUIRED_MF[:], "sections": {},
            "error": str(e),
        })
        time.sleep(0.3)
        continue

    present  = [k for k in REQUIRED_MF if live_mf.get(k)]
    missing  = [k for k in REQUIRED_MF if not live_mf.get(k)]
    suffix_ok = suffix in VALID_SUFFIXES

    # Section coverage
    sections = {}
    for sec, keys in SECTION_MAP.items():
        if not keys:
            sections[sec] = True
        else:
            sections[sec] = all(live_mf.get(k) for k in keys)

    rows.append({
        "pid": pid, "title": title, "fmt": fmt,
        "suffix": suffix, "suffix_ok": suffix_ok,
        "mf_count": len(present), "missing": missing,
        "sections": sections, "error": None,
    })
    time.sleep(0.25)

# ── Print results ──────────────────────────────────────────────────────────────
SEP = "=" * 90

print(SEP)
print(f"{'PRODUCT ID':<20} {'TITLE':<42} {'FMT':<4} {'SUFFIX':<15} {'MF':>5}  {'MISSING':<30} STATUS")
print("-" * 90)

stats = {"ok": 0, "warn": 0, "fail": 0, "v1": 0, "v2": 0}

for r in rows:
    if r["error"]:
        print(f"{r['pid']:<20} {'ERROR':<42} {'?':<4} {'?':<15} {'?':>5}  {r['error'][:30]:<30} FAIL")
        stats["fail"] += 1
        continue

    fmt_flag = r["fmt"]
    if fmt_flag == "V2":
        stats["v2"] += 1
    else:
        stats["v1"] += 1

    missing_short = ", ".join(r["missing"][:3]) + ("..." if len(r["missing"]) > 3 else "")
    sections_pass = sum(1 for v in r["sections"].values() if v)
    sections_total = len(r["sections"])

    if r["mf_count"] == len(REQUIRED_MF) and fmt_flag == "V2" and r["suffix_ok"]:
        status = "OK"
        stats["ok"] += 1
    elif r["mf_count"] >= 8 and fmt_flag == "V2":
        status = f"WARN ({sections_pass}/{sections_total} sec)"
        stats["warn"] += 1
    else:
        status = "FAIL"
        stats["fail"] += 1

    suffix_disp = r["suffix"] if r["suffix"] else "(blank)"
    print(f"{r['pid']:<20} {r['title']:<42} {fmt_flag:<4} {suffix_disp:<15} {r['mf_count']:>2}/{len(REQUIRED_MF):<3}  {missing_short:<30} {status}")

# ── Section coverage summary ───────────────────────────────────────────────────
print(f"\n{SEP}")
print("SECTION COVERAGE SUMMARY")
print(f"{SEP}")
section_stats = {s: 0 for s in SECTION_MAP}
covered_products = [r for r in rows if not r["error"] and r["sections"]]
for r in covered_products:
    for s, ok in r["sections"].items():
        if ok:
            section_stats[s] += 1

print(f"{'SECTION':<30} {'PRODUCTS WITH DATA':>20} {'COVERAGE %':>12}")
print("-" * 65)
n = len(covered_products)
for sec, count in section_stats.items():
    pct = f"{100*count//n}%" if n else "0%"
    bar = "#" * (count * 20 // n) if n else ""
    print(f"{sec:<30} {count:>8}/{n:<12} {pct:>10}  {bar}")

# ── Final summary ──────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("FINAL SUMMARY")
print(f"{SEP}")
print(f"  Total products checked:  {len(all_pids)}")
print(f"  Format V2:               {stats['v2']}")
print(f"  Format V1 (needs fix):   {stats['v1']}")
print(f"  Status OK:               {stats['ok']}")
print(f"  Status WARN:             {stats['warn']}")
print(f"  Status FAIL:             {stats['fail']}")

fail_products = [r for r in rows if not r["error"] and (r["fmt"] != "V2" or r["mf_count"] < len(REQUIRED_MF))]
if fail_products:
    print(f"\n  Products needing attention:")
    for r in fail_products:
        print(f"    {r['pid']}  fmt={r['fmt']}  mf={r['mf_count']}/{len(REQUIRED_MF)}  missing={r['missing'][:4]}")
print(SEP)

# Save JSON report
report_path = BASE_DIR / "output" / "health_check_report.json"
report = [
    {k: v for k, v in r.items() if k != "sections"}
    | {"sections_ok": sum(1 for v in r.get("sections", {}).values() if v),
       "sections_total": len(r.get("sections", {}))}
    for r in rows
]
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {report_path}")
