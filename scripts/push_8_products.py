#!/usr/bin/env python3
"""Push 8 failed products (post V2 migration) and re-apply clothing-test suffix."""
import io, os, sys, subprocess, time, json, requests
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")
tok_path = Path.home() / "Desktop/shopify-token/.env"
if tok_path.exists():
    load_dotenv(tok_path, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
HDR   = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
ORCH  = BASE_DIR / "00-team-lead" / "orchestrator.py"

REQUIRED_MF = [
    "hero_eyebrow", "hero_headline", "hero_subheadline",
    "fabric_title", "fabric_body", "fabric_highlight", "fabric_tags",
    "whats_special", "benefits", "emotional_reassurance",
    "care_instructions", "faq",
]

PIDS = [
    "10009173033273", "10029648970041", "10029649101113", "10029649133881",
    "9657091293497",  "9673732292921",  "9688660312377",  "9688934940985",
]

def push(pid):
    r = subprocess.run(
        [sys.executable, str(ORCH), "push", pid],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    lines = (r.stdout or "").strip().splitlines()
    for l in lines[-5:]:
        print(f"    {l}")
    return r.returncode

def set_suffix(pid, suffix):
    resp = requests.put(
        f"https://{SHOP}/admin/api/2024-10/products/{pid}.json",
        headers=HDR,
        json={"product": {"id": int(pid), "template_suffix": suffix}},
        timeout=10,
    )
    return resp.status_code == 200

def get_metafields(pid):
    resp = requests.get(
        f"https://{SHOP}/admin/api/2024-10/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania", "limit": 250},
        timeout=10,
    )
    return {mf["key"]: mf["value"] for mf in resp.json().get("metafields", [])}

print("=" * 60)
print("BabyMania — Push 8 Products (V2 publisher.json)")
print("=" * 60)

push_results = {}
for pid in PIDS:
    print(f"\n[{pid}]")
    rc = push(pid)
    push_results[pid] = {"rc": rc}
    if rc == 0:
        ok = set_suffix(pid, "clothing-test")
        push_results[pid]["suffix"] = ok
        print(f"    clothing-test: {'OK' if ok else 'FAIL'}")
    else:
        push_results[pid]["suffix"] = False
    time.sleep(0.5)

# --- Verify ---
print("\n" + "=" * 60)
print("VERIFICATION — Metafields in Shopify")
print("=" * 60)
print(f"\n{'PRODUCT ID':<20} {'MF WRITTEN':<15} {'STATUS'}")
print("-" * 50)

total_ok = 0
for pid in PIDS:
    if not push_results[pid]["rc"] == 0:
        print(f"{pid:<20} {'SKIPPED':<15} FAIL")
        continue
    mf = get_metafields(pid)
    present = [k for k in REQUIRED_MF if mf.get(k)]
    missing = [k for k in REQUIRED_MF if not mf.get(k)]
    ok = len(missing) == 0
    if ok:
        total_ok += 1
    status = "OK" if ok else f"MISSING {len(missing)}"
    print(f"{pid:<20} {len(present)}/{len(REQUIRED_MF)}{'':>7} {status}")
    if missing:
        print(f"  {'':>20}missing: {', '.join(missing)}")
    time.sleep(0.2)

print(f"\n{'='*60}")
print(f"RESULT: {total_ok}/{len(PIDS)} products with all metafields written")
print(f"{'='*60}")
