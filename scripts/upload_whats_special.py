#!/usr/bin/env python3
"""
upload_whats_special.py
-----------------------
1. Upload sections/bm-store-whats-special.liquid
2. Upload templates/product.clothing.json (with bm_whats_special wired in)
3. Pull-back verify both assets
"""
import io, os, sys, json, requests, time
from pathlib import Path
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(r"C:\Users\3024e\Desktop\shopify-token\.env", override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
API   = "2024-10"
HDR   = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
BASE  = f"https://{SHOP}/admin/api/{API}"

SECTION_LOCAL   = Path(r"C:\Users\3024e\Downloads\קלוד קוד\sections\bm-store-whats-special.liquid")
TEMPLATE_LOCAL  = BASE_DIR / "product.clothing.json"

SECTION_KEY     = "sections/bm-store-whats-special.liquid"
TEMPLATE_KEY    = "templates/product.clothing.json"

THEME_ID = 183668179257


def push(key, value):
    r = requests.put(
        f"{BASE}/themes/{THEME_ID}/assets.json",
        headers=HDR,
        json={"asset": {"key": key, "value": value}},
        timeout=20,
    )
    return r.status_code, r.json()


def pull(key):
    r = requests.get(
        f"{BASE}/themes/{THEME_ID}/assets.json",
        headers=HDR,
        params={"asset[key]": key},
        timeout=15,
    )
    return r.status_code, r.json().get("asset", {}).get("value", "")


if not TOKEN:
    print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
    sys.exit(1)

print("=" * 65)
print("BabyMania — Upload What's Special Section + Template")
print("=" * 65)

# ── 1. Read local files ───────────────────────────────────────────────────────
print(f"\n[1] Reading local files...")
section_value  = SECTION_LOCAL.read_text(encoding="utf-8")
template_value = TEMPLATE_LOCAL.read_text(encoding="utf-8")
print(f"    section  : {len(section_value):,} bytes — {SECTION_LOCAL}")
print(f"    template : {len(template_value):,} bytes — {TEMPLATE_LOCAL}")

# ── 2. Validate template JSON ─────────────────────────────────────────────────
print(f"\n[2] Validating template JSON...")
try:
    tpl = json.loads(template_value)
    sections = set(tpl["sections"].keys())
    order    = tpl["order"]
    assert sections == set(order), f"key/order mismatch: {sections.symmetric_difference(set(order))}"
    assert len(order) == len(set(order)), "duplicate in order"
    ws_in_sections = "bm_whats_special" in sections
    ws_in_order    = "bm_whats_special" in order
    ws_pos         = order.index("bm_whats_special") if ws_in_order else -1
    fabric_pos     = order.index("bm_fabric") if "bm_fabric" in order else -1
    sizes_pos      = order.index("bm_sizes") if "bm_sizes" in order else -1
    print(f"    sections count : {len(sections)}")
    print(f"    order count    : {len(order)}")
    print(f"    bm_whats_special in sections: {ws_in_sections}")
    print(f"    bm_whats_special in order   : {ws_in_order}  (pos={ws_pos})")
    print(f"    position check: fabric={fabric_pos} < whats_special={ws_pos} < sizes={sizes_pos} — {'OK' if fabric_pos < ws_pos < sizes_pos else 'FAIL'}")
except Exception as e:
    print(f"    ERROR: {e}")
    sys.exit(1)

# ── 3. Check section mentions schema at top level ─────────────────────────────
print(f"\n[3] Checking Liquid structure...")
if "{% schema %}" not in section_value:
    print("    ERROR: no {%% schema %%} found in section file")
    sys.exit(1)
# Ensure schema is NOT inside an if block (basic check)
schema_pos = section_value.find("{% schema %}")
if_count_before   = section_value[:schema_pos].count("{% if")
endif_count_before = section_value[:schema_pos].count("{% endif %}")
nested = if_count_before > endif_count_before
print(f"    schema tag found at char pos: {schema_pos}")
print(f"    if-blocks before schema: {if_count_before}  endifs before: {endif_count_before}")
print(f"    schema nested inside if: {nested}  — {'FAIL — abort' if nested else 'OK'}")
if nested:
    sys.exit(1)

# ── 4. Upload section first ───────────────────────────────────────────────────
print(f"\n[4] Uploading {SECTION_KEY}...")
status, resp = push(SECTION_KEY, section_value)
print(f"    HTTP {status}  →  {'OK' if status in (200,201) else 'FAIL'}")
if status not in (200, 201):
    print(f"    Response: {json.dumps(resp, ensure_ascii=False, indent=2)}")
    sys.exit(1)
time.sleep(1)

# ── 5. Upload template ────────────────────────────────────────────────────────
print(f"\n[5] Uploading {TEMPLATE_KEY}...")
status_t, resp_t = push(TEMPLATE_KEY, template_value)
print(f"    HTTP {status_t}  →  {'OK' if status_t in (200,201) else 'FAIL'}")
if status_t not in (200, 201):
    print(f"    Response: {json.dumps(resp_t, ensure_ascii=False, indent=2)}")
    sys.exit(1)
time.sleep(1)

# ── 6. Pull-back verify ───────────────────────────────────────────────────────
print(f"\n[6] Pull-back verification...")

pb_status_s, pb_section = pull(SECTION_KEY)
section_match = pb_section.strip() == section_value.strip()
print(f"    section  HTTP {pb_status_s}  match={section_match}")

pb_status_t, pb_template = pull(TEMPLATE_KEY)
template_match = pb_template.strip() == template_value.strip()
print(f"    template HTTP {pb_status_t}  match={template_match}")

# Check bm_whats_special visible in live template order
try:
    live_tpl = json.loads(pb_template)
    live_order = live_tpl["order"]
    print(f"\n    Live template order:")
    for i, k in enumerate(live_order, 1):
        marker = " ← NEW" if k == "bm_whats_special" else ""
        print(f"      {i:2}. {k}{marker}")
except Exception as e:
    print(f"    ERROR parsing live template: {e}")

# ── 7. Summary ────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("RESULT")
print("=" * 65)
ok = section_match and template_match and status in (200,201) and status_t in (200,201)
print(f"  section  upload : HTTP {status}  pull-back match: {section_match}")
print(f"  template upload : HTTP {status_t}  pull-back match: {template_match}")
print(f"  OVERALL         : {'SUCCESS' if ok else 'PARTIAL / FAIL'}")
if ok:
    print("\n  NEXT STEP: Open a live clothing product page in browser")
    print("  and verify .bm-ws-section renders with product-specific text.")
    print("  Products with whats_special set: check section appears.")
    print("  Products without whats_special: confirm section is hidden (blank guard).")
