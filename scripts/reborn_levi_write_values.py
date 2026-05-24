"""
reborn_levi_write_values.py
Terminal 6 — BabyMania Reborn only

Write metafield VALUES for Levi (PID 9689589383481) only.
Values sourced from: reborn-audit/levi-metafield-values-draft.md

SAFE:
- Writes ONLY to PID 9689589383481
- Skips baby_mania.faq (FAQ stage deferred)
- Does NOT touch title/price/compare-at/SEO/handle/template/theme

NEVER:
- Write to any other product
- Write baby_mania.faq
- Change prices, descriptions, images, variants
"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

PRODUCT_ID = 9689589383481
BASE_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"
STATUS_FILE = Path(__file__).parent.parent / "reborn-audit" / "levi-metafields-write-status.md"

# Values per levi-metafield-values-draft.md
# baby_mania.faq is listed here only to report it as DEFERRED — never written
VALUES_TO_WRITE = [
    {
        "namespace": "reborn_doll",
        "key":       "hebrew_name",
        "value":     "לוי",
        "type":      "single_line_text_field",
    },
    {
        "namespace": "reborn_doll",
        "key":       "model_label",
        "value":     "בובת ריבורן לוי",
        "type":      "single_line_text_field",
    },
    {
        "namespace": "reborn_specs",
        "key":       "size_cm",
        "value":     "46 ס״מ",
        "type":      "single_line_text_field",
    },
    {
        "namespace": "reborn_specs",
        "key":       "source_note",
        "value":     "לפי נתוני ספק",
        "type":      "single_line_text_field",
    },
    {
        "namespace": "reborn_copy",
        "key":       "hero_subtitle",
        "value":     "בובת ריבורן לוי נראית ומרגישה כמו תינוק אמיתי: 46 ס״מ, מגע רך, הבעה עדינה, בקבוק ומוצץ מגנטי באריזה.",
        "type":      "multi_line_text_field",
    },
]

DEFERRED = [("baby_mania", "faq", "json")]


def rest_headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }


def write_metafield(namespace: str, key: str, value: str, field_type: str) -> dict:
    url = f"{BASE_URL}/products/{PRODUCT_ID}/metafields.json"
    payload = {
        "metafield": {
            "namespace": namespace,
            "key":       key,
            "value":     value,
            "type":      field_type,
        }
    }
    resp = requests.post(url, headers=rest_headers(), json=payload, timeout=15)
    if resp.status_code == 422:
        # Already exists — update instead
        existing_id = get_existing_metafield_id(namespace, key)
        if existing_id:
            return update_metafield(existing_id, value)
        return {"ok": False, "error": f"422 and could not find existing id"}
    resp.raise_for_status()
    data = resp.json().get("metafield", {})
    return {"ok": True, "id": data.get("id"), "value": data.get("value")}


def get_existing_metafield_id(namespace: str, key: str) -> int | None:
    url = f"{BASE_URL}/products/{PRODUCT_ID}/metafields.json"
    resp = requests.get(url, headers=rest_headers(), timeout=15)
    resp.raise_for_status()
    for mf in resp.json().get("metafields", []):
        if mf["namespace"] == namespace and mf["key"] == key:
            return mf["id"]
    return None


def update_metafield(metafield_id: int, value: str) -> dict:
    url = f"{BASE_URL}/metafields/{metafield_id}.json"
    payload = {"metafield": {"id": metafield_id, "value": value}}
    resp = requests.put(url, headers=rest_headers(), json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json().get("metafield", {})
    return {"ok": True, "id": data.get("id"), "value": data.get("value")}


def verify_values() -> dict:
    """Re-read all metafields for the product and return dict keyed by (ns, key)."""
    url = f"{BASE_URL}/products/{PRODUCT_ID}/metafields.json"
    resp = requests.get(url, headers=rest_headers(), timeout=15)
    resp.raise_for_status()
    result = {}
    for mf in resp.json().get("metafields", []):
        result[(mf["namespace"], mf["key"])] = mf.get("value", "")
    return result


def write_status_file(results: list, verified: dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# סטטוס כתיבת Metafield Values — לוי",
        f"**PID:** {PRODUCT_ID}",
        f"**עדכון:** {now}",
        "",
        "---",
        "",
        "## 1. תוצאות כתיבה",
        "",
        "| namespace | key | ערך שנכתב | סטטוס |",
        "|---|---|---|---|",
    ]

    all_ok = True
    for r in results:
        ns, key, value, status, error = r
        short_val = value[:40] + "..." if len(value) > 40 else value
        if status == "ok":
            lines.append(f"| `{ns}` | `{key}` | `{short_val}` | ok |")
        else:
            lines.append(f"| `{ns}` | `{key}` | `{short_val}` | FAILED: {error} |")
            all_ok = False

    for ns, key, field_type in DEFERRED:
        lines.append(f"| `{ns}` | `{key}` | — | DEFERRED (FAQ stage) |")

    lines += [
        "",
        "---",
        "",
        "## 2. אימות (re-read מ-Shopify)",
        "",
        "| namespace | key | ערך בשופיפיי |",
        "|---|---|---|",
    ]

    for r in results:
        ns, key, _, status, _ = r
        if status == "ok":
            live_val = verified.get((ns, key), "NOT FOUND")
            short_live = live_val[:40] + "..." if len(live_val) > 40 else live_val
            match = "ok" if live_val != "NOT FOUND" else "MISSING"
            lines.append(f"| `{ns}` | `{key}` | `{short_live}` |")

    lines += [
        "",
        "---",
        "",
        "## 3. האם אפשר לעבור לשלב 7?",
        "",
    ]

    required_keys = {(r[0], r[1]) for r in results if r[2] is not None}
    failed_required = [r for r in results if r[3] != "ok"]

    if all_ok:
        lines += [
            "ok **כן** — כל 5 ערכי החובה נכתבו בהצלחה.",
            "",
            "שלב 7: המרת S1 Hero ו-S17 Final CTA ל-Liquid.",
        ]
    else:
        lines += ["FAIL **לא עדיין** — יש כשלונות:"]
        for r in failed_required:
            lines.append(f"- `{r[0]}.{r[1]}`: {r[4]}")

    STATUS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  -> Status file: {STATUS_FILE}")


def main():
    print("\n" + "=" * 60)
    print("reborn_levi_write_values.py — Terminal 6")
    print(f"Target PID: {PRODUCT_ID}")
    print("=" * 60)

    token = _get_access_token()
    masked = token[:4] + "..." + token[-4:]
    print(f"  Auth: {masked}")
    print(f"  Shop: {SHOPIFY_SHOP_URL}")

    print(f"\nDeferred (will NOT write):")
    for ns, key, t in DEFERRED:
        print(f"  {ns}.{key} [{t}] -> DEFERRED (FAQ stage)")

    print(f"\nWriting {len(VALUES_TO_WRITE)} metafield(s)...")

    results = []
    for field in VALUES_TO_WRITE:
        ns   = field["namespace"]
        key  = field["key"]
        val  = field["value"]
        ftype = field["type"]
        print(f"  -> {ns}.{key} ...", end=" ")
        try:
            r = write_metafield(ns, key, val, ftype)
            if r["ok"]:
                print("ok")
                results.append((ns, key, val, "ok", ""))
            else:
                print(f"FAILED: {r.get('error', '?')}")
                results.append((ns, key, val, "failed", r.get("error", "?")))
        except Exception as e:
            print(f"EXCEPTION: {e}")
            results.append((ns, key, val, "failed", str(e)))

    print("\nVerifying (re-reading from Shopify)...")
    try:
        verified = verify_values()
        for field in VALUES_TO_WRITE:
            ns, key = field["namespace"], field["key"]
            live = verified.get((ns, key))
            if live:
                short = live[:50] + "..." if len(live) > 50 else live
                print(f"  {ns}.{key} = {short}")
            else:
                print(f"  {ns}.{key} = NOT FOUND")
    except Exception as e:
        print(f"  Verify failed: {e}")
        verified = {}

    write_status_file(results, verified)

    ok_count = sum(1 for r in results if r[3] == "ok")
    fail_count = sum(1 for r in results if r[3] != "ok")
    print("\n" + "=" * 60)
    print(f"  written:  {ok_count}")
    print(f"  failed:   {fail_count}")
    print(f"  deferred: {len(DEFERRED)} (baby_mania.faq)")
    print("=" * 60)


if __name__ == "__main__":
    main()
