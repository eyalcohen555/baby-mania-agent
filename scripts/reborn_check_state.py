"""
reborn_check_state.py — Terminal 6
Checks:
1. Product handle for PID 9689589383481 (to build correct storefront URL)
2. Assets in test theme 182057763129 (verifies product.reborn.liquid is there)
Read-only. No changes to anything.
"""
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

BASE_URL  = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"
THEME_ID  = 182057763129
PRODUCT_ID = 9689589383481

def headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }

def check_product():
    url  = f"{BASE_URL}/products/{PRODUCT_ID}.json"
    resp = requests.get(url, params={"fields": "id,title,handle,template_suffix"}, headers=headers(), timeout=15)
    resp.raise_for_status()
    p = resp.json().get("product", {})
    print(f"\n[Product]")
    print(f"  id:              {p.get('id')}")
    print(f"  title:           {p.get('title')}")
    print(f"  handle:          {p.get('handle')}")
    print(f"  template_suffix: {p.get('template_suffix')}")
    print(f"\n  Correct preview URL:")
    handle = p.get('handle', str(PRODUCT_ID))
    print(f"  https://{SHOPIFY_SHOP_URL}/products/{handle}?preview_theme_id={THEME_ID}")
    return p

def check_assets():
    print(f"\n[Theme {THEME_ID} — key assets]")
    keys = [
        "templates/product.reborn.liquid",
        "templates/product.reborn.json",
        "sections/bm-reborn-product-page.liquid",
    ]
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    for key in keys:
        resp = requests.get(url, params={"asset[key]": key}, headers=headers(), timeout=15)
        if resp.status_code == 200:
            asset = resp.json().get("asset", {})
            if asset:
                print(f"  ✅ {key} ({asset.get('size', '?')} bytes)")
            else:
                print(f"  ❌ {key} — not found")
        else:
            print(f"  ❌ {key} — HTTP {resp.status_code}")

if __name__ == "__main__":
    check_product()
    check_assets()
