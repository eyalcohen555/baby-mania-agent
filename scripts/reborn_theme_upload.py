"""
reborn_theme_upload.py
Terminal 6 — BabyMania Reborn only

Steps:
1. List all themes → find an inactive (non-main) theme
2. Upload sections/bm-reborn-product-page.liquid to test theme
3. Upload templates/product.reborn-test.json to test theme
4. Verify files exist on theme after upload
5. Check template_suffix of product 9689589383481 (read only — no change)
6. Write reborn-audit/theme-test-upload-status.md

NEVER: touches live/main theme, changes product template_suffix,
       modifies prices/titles/SEO/description/metafields.
"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

BASE_URL   = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"
STATUS_FILE = Path(__file__).parent.parent / "reborn-audit" / "theme-test-upload-status.md"

FILES_TO_UPLOAD = [
    {
        "local": Path(__file__).parent.parent / "output" / "theme-test" / "sections" / "bm-reborn-product-page.liquid",
        "key":   "sections/bm-reborn-product-page.liquid",
    },
    {
        "local": Path(__file__).parent.parent / "output" / "theme-test" / "templates" / "product.reborn-test.json",
        "key":   "templates/product.reborn-test.json",
    },
]

PRODUCT_ID = 9689589383481


def rest_headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }


# ── Step 1: List themes ───────────────────────────────────────────────────────
def list_themes() -> list:
    resp = requests.get(f"{BASE_URL}/themes.json", headers=rest_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json().get("themes", [])


def pick_test_theme(themes: list) -> dict | None:
    """Pick the best inactive theme for testing. Prefer non-main themes."""
    inactive = [t for t in themes if t.get("role") != "main"]
    if not inactive:
        return None
    # Prefer a theme named test/draft/staging/dev, else first inactive
    for t in inactive:
        name = t.get("name", "").lower()
        if any(kw in name for kw in ["test", "draft", "staging", "dev", "reborn", "backup"]):
            return t
    return inactive[0]


# ── Step 2: Upload asset ──────────────────────────────────────────────────────
def upload_asset(theme_id: int, key: str, content: str) -> dict:
    url = f"{BASE_URL}/themes/{theme_id}/assets.json"
    payload = {"asset": {"key": key, "value": content}}
    resp = requests.put(url, headers=rest_headers(), json=payload, timeout=30)
    if resp.status_code in (200, 201):
        asset = resp.json().get("asset", {})
        return {"ok": True, "key": asset.get("key"), "updated": asset.get("updated_at")}
    return {"ok": False, "status": resp.status_code, "body": resp.text[:200]}


# ── Step 3: Verify asset exists ───────────────────────────────────────────────
def verify_asset(theme_id: int, key: str) -> dict:
    url = f"{BASE_URL}/themes/{theme_id}/assets.json"
    resp = requests.get(url, params={"asset[key]": key}, headers=rest_headers(), timeout=15)
    if resp.status_code == 200:
        asset = resp.json().get("asset", {})
        return {"exists": bool(asset), "size": asset.get("size", 0), "updated": asset.get("updated_at")}
    return {"exists": False, "status": resp.status_code}


# ── Step 4: Get product template_suffix ──────────────────────────────────────
def get_product_template(product_id: int) -> dict:
    url = f"{BASE_URL}/products/{product_id}.json"
    resp = requests.get(url, params={"fields": "id,title,template_suffix"}, headers=rest_headers(), timeout=15)
    resp.raise_for_status()
    p = resp.json().get("product", {})
    return {
        "id":              p.get("id"),
        "title":           p.get("title"),
        "template_suffix": p.get("template_suffix") or "(none — uses product.json)",
    }


# ── Step 5: Write status file ─────────────────────────────────────────────────
def write_status(themes, test_theme, uploaded, verified, product_info, shop):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# סטטוס Theme Test Upload — שלב 9",
        f"**טרמינל 6 | BabyMania | ריבורן בלבד**",
        f"**עדכון:** {now}",
        f"**חנות:** {shop}",
        "",
        "---",
        "",
        "## 1. Themes בחנות",
        "",
        "| שם | role | theme_id |",
        "|---|---|---|",
    ]
    for t in themes:
        role = t.get("role", "?")
        marker = " ← **LIVE**" if role == "main" else (" ← **TEST**" if t.get("id") == test_theme.get("id") else "")
        lines.append(f"| {t.get('name')} | {role} | {t.get('id')}{marker} |")

    if not test_theme:
        lines += ["", "❌ לא נמצא theme לא-פעיל — נדרשת הכרעה ידנית."]
        write_file(lines)
        return

    lines += [
        "",
        "---",
        "",
        f"## 2. Theme שנבחר לבדיקה",
        "",
        f"| | |",
        "|---|---|",
        f"| **שם** | {test_theme.get('name')} |",
        f"| **theme_id** | {test_theme.get('id')} |",
        f"| **role** | {test_theme.get('role')} |",
        f"| **פעיל (live)?** | {'❌ לא' if test_theme.get('role') != 'main' else '⚠️ כן — שגיאה!'} |",
        "",
        "---",
        "",
        "## 3. קבצים שהועלו",
        "",
        "| key | סטטוס | גודל |",
        "|---|---|---|",
    ]
    for key, result in uploaded.items():
        vr = verified.get(key, {})
        status = "✅ הועלה" if result.get("ok") else f"❌ שגיאה: {result.get('status')} {result.get('body', '')[:60]}"
        size   = f"{vr.get('size', '?')} bytes" if vr.get("exists") else "לא אומת"
        lines.append(f"| `{key}` | {status} | {size} |")

    lines += [
        "",
        "---",
        "",
        "## 4. אימות קבצים בתוך theme",
        "",
        "| key | קיים? | גודל |",
        "|---|---|---|",
    ]
    for key, vr in verified.items():
        exists = "✅ קיים" if vr.get("exists") else "❌ לא נמצא"
        size   = f"{vr.get('size', '?')} bytes" if vr.get("exists") else "—"
        lines.append(f"| `{key}` | {exists} | {size} |")

    # template_suffix info
    cur_suffix = product_info.get("template_suffix", "")
    needs_change = cur_suffix not in ("reborn-test",)
    lines += [
        "",
        "---",
        "",
        "## 5. Template Suffix של לוי",
        "",
        f"| | |",
        "|---|---|",
        f"| **PID** | {product_info.get('id')} |",
        f"| **title** | {product_info.get('title')} |",
        f"| **template_suffix נוכחי** | `{cur_suffix}` |",
        f"| **template_suffix נדרש** | `reborn-test` |",
        f"| **צריך שינוי?** | {'✅ כן — ממתין לאישור אייל' if needs_change else '✅ כבר מוגדר'} |",
        "",
        "> ⚠️ **שינוי template_suffix = שינוי דף המוצר בלייב.**",
        "> לפני שינוי — אישור מפורש מאייל נדרש.",
        "",
        "---",
        "",
        "## 6. קישור Preview",
        "",
    ]

    tid = test_theme.get("id")
    preview_url = f"https://{shop}/products/{PRODUCT_ID}?preview_theme_id={tid}"
    if needs_change:
        lines += [
            f"Preview URL (ללא שינוי template_suffix — יציג template ברירת מחדל של לוי):",
            f"",
            f"`{preview_url}`",
            "",
            "⚠️ כדי לראות את `product.reborn-test.json` — צריך לשנות template_suffix של לוי ל-`reborn-test`.",
            "לא בוצע — ממתין לאישור אייל.",
        ]
    else:
        lines += [
            f"`{preview_url}`",
            "",
            "✅ Preview אמור להציג את הדף החדש.",
        ]

    lines += [
        "",
        "---",
        "",
        "## 7. מה נשאר לפני בדיקה",
        "",
        "- [ ] אישור אייל לשינוי `template_suffix` של לוי ל-`reborn-test`",
        "- [ ] לאחר אישור: `PUT /products/9689589383481.json` עם `template_suffix: reborn-test`",
        "- [ ] פתיחת preview URL לבדיקה ויזואלית",
        "- [ ] Buy Now JS — עדיין TODO",
        "- [ ] Tailwind CDN → assets pipeline — לפני production",
    ]

    STATUS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  -> Status: {STATUS_FILE}")


def main():
    print("\n" + "=" * 60)
    print("reborn_theme_upload.py — Terminal 6")
    print("=" * 60)

    token = _get_access_token()
    masked = token[:4] + "..." + token[-4:]
    print(f"  Auth: {masked}  |  Shop: {SHOPIFY_SHOP_URL}")

    # Step 1: List themes
    print("\n[1] Listing themes...")
    themes = list_themes()
    for t in themes:
        marker = " ← LIVE" if t.get("role") == "main" else ""
        print(f"  {t.get('id')} | {t.get('role'):10} | {t.get('name')}{marker}")

    test_theme = pick_test_theme(themes)
    if not test_theme:
        print("\n  ERROR: No inactive theme found. Cannot upload.")
        write_status(themes, {}, {}, {}, {}, SHOPIFY_SHOP_URL)
        return
    print(f"\n  Selected test theme: [{test_theme.get('id')}] {test_theme.get('name')} (role={test_theme.get('role')})")

    # Step 2+3: Upload + verify
    print("\n[2] Uploading files...")
    uploaded = {}
    verified = {}

    for f in FILES_TO_UPLOAD:
        key = f["key"]
        local = f["local"]
        if not local.exists():
            print(f"  ERROR: Local file not found: {local}")
            uploaded[key] = {"ok": False, "error": "local file not found"}
            continue
        content = local.read_text(encoding="utf-8")
        print(f"  -> Uploading {key} ({len(content)} chars)...", end=" ")
        result = upload_asset(test_theme["id"], key, content)
        uploaded[key] = result
        if result["ok"]:
            print("ok")
        else:
            print(f"FAILED {result.get('status')} {result.get('body','')[:80]}")

    print("\n[3] Verifying uploads...")
    for f in FILES_TO_UPLOAD:
        key = f["key"]
        vr  = verify_asset(test_theme["id"], key)
        verified[key] = vr
        status = "exists" if vr.get("exists") else "MISSING"
        print(f"  {key}: {status} ({vr.get('size', '?')} bytes)")

    # Step 4: Product template_suffix
    print(f"\n[4] Reading product {PRODUCT_ID} template_suffix...")
    product_info = get_product_template(PRODUCT_ID)
    print(f"  title:           {product_info['title']}")
    print(f"  template_suffix: {product_info['template_suffix']}")
    print(f"  -> NOT changing template_suffix. Requires Eyal approval.")

    # Step 5: Write status
    write_status(themes, test_theme, uploaded, verified, product_info, SHOPIFY_SHOP_URL)

    # Summary
    ok_uploads = sum(1 for r in uploaded.values() if r.get("ok"))
    ok_verified = sum(1 for v in verified.values() if v.get("exists"))
    print("\n" + "=" * 60)
    print(f"  uploaded:  {ok_uploads}/{len(FILES_TO_UPLOAD)}")
    print(f"  verified:  {ok_verified}/{len(FILES_TO_UPLOAD)}")
    print(f"  theme:     [{test_theme.get('id')}] {test_theme.get('name')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
