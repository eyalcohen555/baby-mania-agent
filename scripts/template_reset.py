"""
BabyMania — Product Template System Reset
==========================================
Current state (discovered 2026-03-11):
  - No per-product .json templates exist anymore (already deleted)
  - product-general.json is MISSING (but 62+ products reference it → BROKEN)
  - product-test.json is MISSING
  - Some products have suffix=blank → product.blank.liquid (needs cleanup)
  - tempio / easy-sleep → protected, leave alone

Steps:
  3. Create templates/product.general.json  (duplicate of product.json)
  4. Ensure all non-clothing products have template_suffix="general"
     and all clothing products have template_suffix="" (default)
     (blank suffix → reassign based on collection membership)
  5. Create templates/product.test.json     (duplicate of product.json)
  6. Duplicate 2 clothing products as DRAFT + assign template_suffix = "test"

DO NOT touch:
  - product.tempio.json / products with suffix=tempio
  - product.easy-sleep.json / products with suffix=easy-sleep
  - sections, liquid code, metafields, product content
"""

import json
import sys
import time
import os
import requests

TOKEN = "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"
SHOP  = "a2756c-c0.myshopify.com"
API_VER = "2024-10"
BASE = f"https://{SHOP}/admin/api/{API_VER}"
THEME_ID = "183668179257"

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

PROTECTED_SUFFIXES = {"tempio", "easy-sleep", "test", "blank"}

CLOTHING_COLLECTION_TITLES = {
    "בגדי חורף",
    "קיץ 2025",
    "בגדי בנים",
    "בגדי בנות",
    "בגדי תינוקות",
}

# -- Helpers ------------------------------------------------------------------─
def api_get(path, params=None):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def api_put(path, payload):
    r = requests.put(f"{BASE}{path}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

def api_post(path, payload):
    r = requests.post(f"{BASE}{path}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

def get_all_products():
    products = []
    params = {"limit": 250, "fields": "id,title,handle,template_suffix,status"}
    while True:
        data = api_get("/products.json", params)
        batch = data.get("products", [])
        products.extend(batch)
        if len(batch) < 250:
            break
        params["since_id"] = batch[-1]["id"]
    return products

def get_all_theme_assets():
    data = api_get(f"/themes/{THEME_ID}/assets.json")
    return [a["key"] for a in data.get("assets", [])]

def get_asset(key):
    data = api_get(f"/themes/{THEME_ID}/assets.json", {"asset[key]": key})
    return data.get("asset", {})

def create_or_update_asset(key, value):
    payload = {"asset": {"key": key, "value": value}}
    r = requests.put(f"{BASE}/themes/{THEME_ID}/assets.json", headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

def get_clothing_product_ids():
    """Return set of product IDs that belong to at least one clothing collection."""
    clothing_ids = set()
    custom = api_get("/custom_collections.json", {"limit": 250}).get("custom_collections", [])
    smart  = api_get("/smart_collections.json",  {"limit": 250}).get("smart_collections",  [])
    all_collections = custom + smart
    clothing_cols = [c for c in all_collections if c["title"] in CLOTHING_COLLECTION_TITLES]

    found_titles = {c["title"] for c in clothing_cols}
    missing = CLOTHING_COLLECTION_TITLES - found_titles
    if missing:
        print(f"  WARNING: Collections NOT found: {missing}")

    print(f"  Found clothing collections:")
    for c in clothing_cols:
        page_params = {"limit": 250, "collection_id": c["id"], "fields": "id"}
        col_products = api_get("/products.json", page_params).get("products", [])
        ids = {p["id"] for p in col_products}
        clothing_ids |= ids
        print(f"    - {c['title']}: {len(ids)} products")

    return clothing_ids


# -- STEP 3 — Create product-general.json --------------------------------------
def step3_create_general():
    print("\n-- STEP 3: Create templates/product.general.json --")
    base = get_asset("templates/product.json")
    value = base.get("value") or base.get("content", "")
    if not value:
        print("  ERROR: Could not read templates/product.json")
        sys.exit(1)
    result = create_or_update_asset("templates/product.general.json", value)
    print(f"  OK Created templates/product.general.json  updated_at={result['asset']['updated_at']}")
    return value


# -- STEP 4 — Fix all product template assignments ----------------------------─
def step4_fix_assignments(all_products, clothing_ids):
    print("\n-- STEP 4: Fix template assignments for all products --")
    print("  Clothing collection membership loaded.")

    clothing_fixed = []
    general_fixed  = []
    already_ok     = []
    skipped        = []
    changes_table  = []  # (handle, title, old_suffix, new_suffix)

    for p in all_products:
        suffix = p.get("template_suffix") or ""
        pid    = p["id"]
        handle = p.get("handle", "")
        title  = p.get("title", "")

        if suffix in PROTECTED_SUFFIXES:
            skipped.append(title)
            changes_table.append((handle, title, suffix, "PROTECTED - skipped"))
            continue

        if pid in clothing_ids:
            if suffix == "":
                already_ok.append(title)
                changes_table.append((handle, title, "", "(no change)"))
            else:
                api_put(f"/products/{pid}.json", {"product": {"id": pid, "template_suffix": ""}})
                clothing_fixed.append(title)
                changes_table.append((handle, title, suffix, ""))
                time.sleep(0.4)
        else:
            if suffix == "general":
                already_ok.append(title)
                changes_table.append((handle, title, "general", "(no change)"))
            else:
                api_put(f"/products/{pid}.json", {"product": {"id": pid, "template_suffix": "general"}})
                general_fixed.append(title)
                changes_table.append((handle, title, suffix, "general"))
                time.sleep(0.4)

    print(f"\n  OK Already correct:         {len(already_ok)}")
    print(f"  OK Reset to clothing:       {len(clothing_fixed)}")
    print(f"  OK Moved to general:        {len(general_fixed)}")
    print(f"  OK Skipped (protected):     {len(skipped)}")

    # Print change table (only rows that actually changed)
    changed_rows = [r for r in changes_table if r[3] not in ("(no change)", "PROTECTED - skipped")]
    if changed_rows:
        print(f"\n{'handle':<55} {'title':<45} {'old_suffix':<25} {'new_suffix'}")
        print("-" * 140)
        for handle, title, old, new in changed_rows:
            print(f"{handle[:55]:<55} {title[:45]:<45} {old:<25} {new}")

    return clothing_fixed, general_fixed


# -- STEP 5 — Create product-test.json ----------------------------------------─
def step5_create_test(base_value):
    print("\n-- STEP 5: Create templates/product.test.json --")
    result = create_or_update_asset("templates/product.test.json", base_value)
    print(f"  OK Created templates/product.test.json  updated_at={result['asset']['updated_at']}")


# -- STEP 6 — Create 2 test products ------------------------------------------
def step6_create_test_products(all_products, clothing_ids):
    print("\n-- STEP 6: Duplicate 2 clothing products as DRAFT for testing --")
    # Filter: active clothing products that are not test copies already
    candidates = [
        p for p in all_products
        if p["id"] in clothing_ids
        and "[TEST COPY]" not in p.get("title", "")
        and (p.get("template_suffix") or "") not in PROTECTED_SUFFIXES
    ][:2]

    if len(candidates) < 2:
        print(f"  WARNING  Only {len(candidates)} candidates found")

    created = []
    for p in candidates:
        full = api_get(f"/products/{p['id']}.json").get("product", {})
        new_product = {
            "title": f"[TEST COPY] {full['title']}",
            "body_html": full.get("body_html", ""),
            "vendor": full.get("vendor", ""),
            "product_type": full.get("product_type", ""),
            "status": "draft",
            "template_suffix": "test",
            "tags": full.get("tags", ""),
        }
        resp = api_post("/products.json", {"product": new_product})
        new_id = resp["product"]["id"]
        print(f"  OK Created: {new_product['title'][:60]}  (id={new_id})")
        created.append({"title": new_product["title"], "id": new_id, "source": p["title"]})
        time.sleep(0.5)

    return created


# -- MAIN ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print("BabyMania — Template System Reset")
    print("=" * 60)

    print("\nFetching all products...")
    all_products = get_all_products()
    print(f"Total products: {len(all_products)}")

    print("\nFetching clothing collection membership...")
    clothing_ids = get_clothing_product_ids()
    print(f"Total clothing products: {len(clothing_ids)}")

    # Step 3
    base_value = step3_create_general()

    # Step 4
    clothing_fixed, general_fixed = step4_fix_assignments(all_products, clothing_ids)

    # Step 5
    step5_create_test(base_value)

    # Step 6
    test_products = step6_create_test_products(all_products, clothing_ids)

    # -- FINAL REPORT ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    print(f"\n>> Templates created:")
    print(f"   - templates/product.general.json  OK")
    print(f"   - templates/product.test.json     OK")

    if clothing_fixed:
        print(f"\n>> Products reset to clothing template ({len(clothing_fixed)}):")
        for t in clothing_fixed:
            print(f"   - {t!r}")

    if general_fixed:
        print(f"\n>> Products fixed → product-general ({len(general_fixed)}):")
        for t in general_fixed:
            print(f"   - {t!r}")

    print(f"\n>> Test products created (DRAFT):")
    for tp in test_products:
        print(f"   - {tp['title']!r}  id={tp['id']}")

    print("\n>> Final template structure:")
    assets = get_all_theme_assets()
    for a in sorted(a for a in assets if a.startswith("templates/product")):
        print(f"   {a}")

    print("\nOK Done!")


if __name__ == "__main__":
    main()
