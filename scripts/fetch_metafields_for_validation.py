#!/usr/bin/env python3
"""Fetch baby_mania metafields for 3 products and dump to JSON for analysis."""
import json, os, sys, requests
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(BASE / ".env")
_tok = Path.home() / "Desktop/shopify-token/.env"
if _tok.exists():
    load_dotenv(_tok, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP = os.getenv("SHOPIFY_SHOP_URL", "a2756c-c0.myshopify.com")
API = f"https://{SHOP}/admin/api/2024-10"
HDR = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# Products: 2 that passed pipeline + 1 rich-context product
PIDS = ["9687596728633", "9688932909369", "9657091293497"]

def fetch(pid):
    r = requests.get(f"{API}/products/{pid}/metafields.json?namespace=baby_mania&limit=250", headers=HDR, timeout=15)
    r.raise_for_status()
    mfs = {m["key"]: m["value"] for m in r.get("metafields", [])} if "metafields" in r.json() else {}
    # Also get product info
    p = requests.get(f"{API}/products/{pid}.json", headers=HDR, timeout=15)
    p.raise_for_status()
    prod = p.json().get("product", {})
    return {
        "product_id": pid,
        "title": prod.get("title", ""),
        "handle": prod.get("handle", ""),
        "template_suffix": prod.get("template_suffix", ""),
        "metafields": mfs,
        "metafield_count": len(mfs),
    }

results = {}
for pid in PIDS:
    try:
        results[pid] = fetch(pid)
        print(f"OK: {pid} — {results[pid]['metafield_count']} metafields")
    except Exception as e:
        results[pid] = {"error": str(e)}
        print(f"FAIL: {pid} — {e}")

out = BASE / "output" / "v2_validation_metafields.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out}")
