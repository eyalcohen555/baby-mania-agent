#!/usr/bin/env python3
"""
upload_clothing_template.py
---------------------------
Safe upload of product.clothing.json (merged) + bm-store-fabric.liquid
to the active Shopify theme.

Steps:
  1. Resolve active theme ID
  2. Backup current templates/product.clothing.json from Shopify
  3. Compare local bm-store-fabric.liquid vs live (upload only if different)
  4. Upload templates/product.clothing.json
  5. Upload sections/bm-store-fabric.liquid (if changed)
  6. Pull-back both assets and verify content matches
  7. Find products with template_suffix="clothing" and spot-check metafields

Does NOT:
  - Transfer any products to new template
  - Touch generator / pipeline / other metafields
"""
import io, os, sys, json, hashlib, requests, time
from pathlib import Path
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")
tok_path = Path.home() / "Desktop/shopify-token/.env"
if tok_path.exists():
    load_dotenv(tok_path, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
API   = "2024-10"
HDR   = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
BASE  = f"https://{SHOP}/admin/api/{API}"

LOCAL_TEMPLATE  = BASE_DIR / "fetch_tmp/templates__product.clothing.json"
LOCAL_FABRIC    = BASE_DIR / "theme_assets/sections/bm-store-fabric.liquid"
BACKUP_DIR      = BASE_DIR / "fetch_tmp/backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATE_KEY = "templates/product.clothing.json"
FABRIC_KEY   = "sections/bm-store-fabric.liquid"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def get_active_theme_id():
    resp = requests.get(f"{BASE}/themes.json", headers=HDR, timeout=10)
    resp.raise_for_status()
    for t in resp.json()["themes"]:
        if t.get("role") == "main":
            return t["id"], t["name"]
    t = resp.json()["themes"][0]
    return t["id"], t["name"]


def pull_asset(theme_id, key):
    resp = requests.get(
        f"{BASE}/themes/{theme_id}/assets.json",
        headers=HDR,
        params={"asset[key]": key},
        timeout=15,
    )
    return resp.status_code, resp.json().get("asset", {}).get("value", "")


def push_asset(theme_id, key, value):
    resp = requests.put(
        f"{BASE}/themes/{theme_id}/assets.json",
        headers=HDR,
        json={"asset": {"key": key, "value": value}},
        timeout=20,
    )
    return resp.status_code, resp.json()


def find_clothing_products():
    """Return products with template_suffix='clothing' (max 250)."""
    resp = requests.get(
        f"{BASE}/products.json",
        headers=HDR,
        params={"limit": 250, "fields": "id,title,handle,template_suffix", "template_suffix": "clothing"},
        timeout=15,
    )
    if resp.status_code != 200:
        return []
    return resp.json().get("products", [])


def check_product_metafields(pid):
    """Return dict of key→present for bm sections."""
    resp = requests.get(
        f"{BASE}/products/{pid}/metafields.json",
        headers=HDR,
        params={"namespace": "baby_mania"},
        timeout=10,
    )
    if resp.status_code != 200:
        return {}
    mfs = {m["key"]: m["value"] for m in resp.json().get("metafields", [])}
    return mfs


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if not TOKEN:
    print("ERROR: SHOPIFY_ACCESS_TOKEN not set")
    sys.exit(1)

print("=" * 65)
print("BabyMania — Safe Template Upload")
print("=" * 65)

# ── Step 1: Active theme ──────────────────────────────────────────────────────
print("\n[1] Resolving active theme...")
theme_id, theme_name = get_active_theme_id()
print(f"    Theme: {theme_name}  (id={theme_id})")

# ── Step 2: Backup current template ──────────────────────────────────────────
print(f"\n[2] Backing up {TEMPLATE_KEY} from Shopify...")
status, live_template = pull_asset(theme_id, TEMPLATE_KEY)
if status == 200:
    backup_path = BACKUP_DIR / "BACKUP_templates__product.clothing.json"
    backup_path.write_text(live_template, encoding="utf-8")
    print(f"    HTTP {status}  →  saved: {backup_path}")
    print(f"    live sha: {sha(live_template)}")
else:
    print(f"    WARNING: Could not pull backup (HTTP {status}) — proceeding")

# ── Step 3: Compare bm-store-fabric.liquid ────────────────────────────────────
print(f"\n[3] Comparing {FABRIC_KEY}...")
status_f, live_fabric = pull_asset(theme_id, FABRIC_KEY)
local_fabric = LOCAL_FABRIC.read_text(encoding="utf-8")
fabric_changed = live_fabric.strip() != local_fabric.strip()
print(f"    live sha  : {sha(live_fabric)}")
print(f"    local sha : {sha(local_fabric)}")
print(f"    changed   : {fabric_changed}")
if fabric_changed:
    # Backup live version
    bk = BACKUP_DIR / "BACKUP_bm-store-fabric.liquid"
    bk.write_text(live_fabric, encoding="utf-8")
    print(f"    backup    : {bk}")

# ── Step 4: Upload template ───────────────────────────────────────────────────
print(f"\n[4] Uploading {TEMPLATE_KEY}...")
new_template_value = LOCAL_TEMPLATE.read_text(encoding="utf-8")
# Validate JSON before upload
try:
    parsed = json.loads(new_template_value)
    section_keys = set(parsed["sections"].keys())
    order_items  = parsed["order"]
    assert section_keys == set(order_items), "key/order mismatch"
    assert len(order_items) == len(set(order_items)), "duplicate in order"
    print(f"    JSON valid: {len(section_keys)} sections, {len(order_items)} in order — OK")
except Exception as e:
    print(f"    ERROR pre-upload validation failed: {e}")
    sys.exit(1)

status_t, resp_t = push_asset(theme_id, TEMPLATE_KEY, new_template_value)
print(f"    HTTP {status_t}  →  {'OK' if status_t in (200,201) else 'FAIL'}")
if status_t not in (200, 201):
    print(f"    Response: {resp_t}")
    sys.exit(1)
time.sleep(0.5)

# ── Step 5: Upload fabric (if changed) ───────────────────────────────────────
fabric_uploaded = False
if fabric_changed:
    print(f"\n[5] Uploading {FABRIC_KEY} (changes detected)...")
    status_f2, resp_f2 = push_asset(theme_id, FABRIC_KEY, local_fabric)
    print(f"    HTTP {status_f2}  →  {'OK' if status_f2 in (200,201) else 'FAIL'}")
    if status_f2 not in (200, 201):
        print(f"    Response: {resp_f2}")
    else:
        fabric_uploaded = True
    time.sleep(0.5)
else:
    print(f"\n[5] {FABRIC_KEY} — no change, skip upload")

# ── Step 6: Pull-back and verify ─────────────────────────────────────────────
print("\n[6] Pull-back verification...")

status_pb1, pulled_template = pull_asset(theme_id, TEMPLATE_KEY)
local_sha  = sha(new_template_value)
pulled_sha = sha(pulled_template)
template_match = local_sha == pulled_sha
print(f"    {TEMPLATE_KEY}")
print(f"      local sha   : {local_sha}")
print(f"      pulled sha  : {pulled_sha}")
print(f"      match       : {template_match}")

fabric_match = True
if fabric_changed or fabric_uploaded:
    status_pb2, pulled_fabric = pull_asset(theme_id, FABRIC_KEY)
    local_f_sha  = sha(local_fabric)
    pulled_f_sha = sha(pulled_fabric)
    fabric_match = local_f_sha == pulled_f_sha
    print(f"    {FABRIC_KEY}")
    print(f"      local sha   : {local_f_sha}")
    print(f"      pulled sha  : {pulled_f_sha}")
    print(f"      match       : {fabric_match}")

# Verify section count from pulled template
try:
    pulled_parsed = json.loads(pulled_template)
    pulled_sections = list(pulled_parsed["sections"].keys())
    pulled_order    = pulled_parsed["order"]
    print(f"\n    sections in live template : {len(pulled_sections)}")
    print(f"    order items in live       : {len(pulled_order)}")
    for i, k in enumerate(pulled_order, 1):
        status_mark = "OK" if k in pulled_sections else "MISSING"
        print(f"      {i:2}. {k:<25} [{status_mark}]")
    # Check no כותנה in live fabric
    has_cotton = "כותנה" in pulled_fabric if fabric_changed else ("כותנה" not in live_fabric)
except Exception as e:
    print(f"    ERROR parsing pulled template: {e}")

# ── Step 7: Spot-check clothing products ─────────────────────────────────────
print("\n[7] Spot-checking products with template_suffix='clothing'...")
clothing_products = find_clothing_products()
print(f"    Found {len(clothing_products)} products with suffix='clothing'")

if not clothing_products:
    print("    NOTE: No products assigned to 'clothing' template yet.")
    print("    This is expected — no product migration was requested.")
else:
    checked = clothing_products[:3]  # check up to 3
    for p in checked:
        pid   = str(p["id"])
        title = p.get("title", "")[:50]
        mfs   = check_product_metafields(pid)
        faq_ok  = "faq"  in mfs and len(mfs["faq"]) > 10
        care_ok = "care_instructions" in mfs or "care" in mfs
        fabric_present = "fabric_title" in mfs or "fabric_body" in mfs
        print(f"\n    [{pid}] {title}")
        print(f"      faq present       : {'yes' if faq_ok else 'NO'}")
        print(f"      care present      : {'yes' if care_ok else 'NO'}")
        print(f"      fabric present    : {'yes' if fabric_present else 'NO'}")
        print(f"      all mf keys       : {list(mfs.keys())}")
        time.sleep(0.3)

# ─── Final Report ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("UPLOAD REPORT")
print("=" * 65)
print(f"  SYSTEM STATE:   theme={theme_name}  id={theme_id}")
print(f"  backup created: {'yes' if status == 200 else 'no (pull failed)'}")
print(f"  template upload HTTP: {status_t}  match: {template_match}")
print(f"  fabric  upload HTTP: {'skipped (no change)' if not fabric_changed else str(status_f2)}"
      f"  match: {fabric_match}")
print(f"  sections in live template: {len(pulled_sections)}")
print(f"  all 13 sections: {'yes' if len(pulled_sections) == 13 and len(pulled_order) == 13 else 'NO'}")
print(f"  clothing products found:  {len(clothing_products)}")

failed = []
if not template_match: failed.append("template pull-back mismatch")
if not fabric_match:   failed.append("fabric pull-back mismatch")
if len(pulled_sections) != 13: failed.append(f"section count={len(pulled_sections)} (expected 13)")
print(f"\n  ISSUES FOUND: {failed if failed else 'none'}")
risk = "LOW" if not failed else "HIGH"
print(f"  RISK LEVEL:   {risk}")
print(f"  NEXT STEP:    {'Assign clothing products to template' if not failed else 'Investigate failures'}")
