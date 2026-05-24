"""
reborn_upload_fixed_template.py — Terminal 6
Uploads the updated product.reborn.liquid to test theme 182057763129.
Read-only on Shopify product data. No live theme changes.
"""
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

THEME_ID  = 182057763129
TEMPLATE_KEY = "templates/product.reborn.liquid"
LOCAL_FILE = Path(r"C:\Projects\baby-mania-agent\output\pages\reborn-landing\levi-reborn-product-liquid-draft.liquid")

BASE_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"

def headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }

def main():
    content = LOCAL_FILE.read_text(encoding="utf-8")
    print(f"File: {len(content.splitlines())} lines, {len(content.encode('utf-8'))} bytes")

    # Quick checks before upload
    assert "{% layout none %}" not in content, "ABORT: layout none still present"
    assert "<main dir=\"rtl\">" in content, "ABORT: main dir=rtl missing"
    assert "<!DOCTYPE" not in content, "ABORT: DOCTYPE still present"
    assert "</body>" not in content, "ABORT: </body> still present"
    assert "sec-lbl\">S" not in content, "ABORT: sec-lbl labels still present"
    print("Pre-checks: ok")

    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    payload = {"asset": {"key": TEMPLATE_KEY, "value": content}}
    resp = requests.put(url, headers=headers(), json=payload, timeout=60)

    if resp.status_code in (200, 201):
        asset = resp.json().get("asset", {})
        print(f"Uploaded: {asset.get('key')} ({asset.get('size')} bytes)")
    else:
        print(f"FAILED: HTTP {resp.status_code}")
        print(resp.text[:300])
        return

    # Verify
    resp2 = requests.get(url, params={"asset[key]": TEMPLATE_KEY}, headers=headers(), timeout=15)
    if resp2.status_code == 200:
        a = resp2.json().get("asset", {})
        print(f"Verified: {a.get('size')} bytes — exists: {bool(a)}")

    print(f"\nPreview URL:")
    print(f"  https://{SHOPIFY_SHOP_URL}/products/{{handle}}?preview_theme_id={THEME_ID}")
    print("  (replace {handle} with the product handle)")

if __name__ == "__main__":
    main()
