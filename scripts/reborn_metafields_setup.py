"""
reborn_metafields_setup.py
Terminal 6 — BabyMania Reborn only

Check and create metafield definitions per reborn-metafields-contract.md.
SAFE: reads only, then creates ONLY missing definitions.
NEVER: fills values, updates products, changes prices/titles/SEO/theme.
"""

import sys
import json
import requests
import os
from datetime import datetime
from pathlib import Path

# ── Load existing project infrastructure ──────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

# ── Constants ─────────────────────────────────────────────────────────────────
GRAPHQL_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}/graphql.json"
STATUS_FILE = Path(__file__).parent.parent / "reborn-audit" / "reborn-metafields-admin-status.md"

# ── Contract: definitions required per reborn-metafields-contract.md ──────────
# Format: (namespace, key, type_name, display_name, required)
REQUIRED_DEFINITIONS = [
    ("reborn_doll",  "hebrew_name",    "single_line_text_field", "שם עברי קצר",          True),
    ("reborn_doll",  "model_label",    "single_line_text_field", "תווית דגם לתצוגה",     True),
    ("reborn_specs", "size_cm",        "single_line_text_field", "גודל ס״מ",              True),
    ("reborn_specs", "source_note",    "single_line_text_field", "מקור נתון",             False),
    ("reborn_copy",  "hero_subtitle",  "multi_line_text_field",  "תת-כותרת Hero",         True),
    # baby_mania.faq — CHECK ONLY, never create/modify if exists
    ("baby_mania",   "faq",            "json",                   "שאלות נפוצות JSON",     False),
]

# Fields that must NEVER be created even if missing
BLOCKED_FIELDS = {
    ("baby_mania", "faq"),  # only check existence; never create or modify
}


def gql_headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }


def run_query(query: str, variables: dict = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = requests.post(GRAPHQL_URL, headers=gql_headers(), json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ── Step 1: Fetch all existing PRODUCT metafield definitions ──────────────────
FETCH_DEFS_QUERY = """
{
  metafieldDefinitions(first: 100, ownerType: PRODUCT) {
    edges {
      node {
        id
        namespace
        key
        name
        type { name }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def fetch_existing_definitions() -> dict:
    """Returns dict keyed by (namespace, key) → {id, name, type}"""
    print("  -> Querying existing metafield definitions...")
    result = run_query(FETCH_DEFS_QUERY)
    defs = {}
    edges = result.get("data", {}).get("metafieldDefinitions", {}).get("edges", [])
    for edge in edges:
        node = edge["node"]
        key = (node["namespace"], node["key"])
        defs[key] = {
            "id":   node["id"],
            "name": node["name"],
            "type": node["type"]["name"],
        }
    return defs


# ── Step 2: Compare contract vs existing ─────────────────────────────────────
def compare(existing: dict) -> tuple[list, list, list]:
    """Returns (ok, missing, mismatch)"""
    ok       = []
    missing  = []
    mismatch = []

    for ns, key, expected_type, display_name, required in REQUIRED_DEFINITIONS:
        lookup = (ns, key)
        if lookup in existing:
            actual_type = existing[lookup]["type"]
            if actual_type == expected_type:
                ok.append((ns, key, expected_type, display_name, required))
            else:
                mismatch.append((ns, key, expected_type, actual_type, display_name, required))
        else:
            missing.append((ns, key, expected_type, display_name, required))

    return ok, missing, mismatch


# ── Step 3: Create a single definition ───────────────────────────────────────
CREATE_DEF_MUTATION = """
mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition {
      id
      namespace
      key
      type { name }
    }
    userErrors {
      field
      message
    }
  }
}
"""


def create_definition(ns: str, key: str, type_name: str, display_name: str) -> dict:
    variables = {
        "definition": {
            "namespace":   ns,
            "key":         key,
            "name":        display_name,
            "type":        type_name,
            "ownerType":   "PRODUCT",
        }
    }
    result = run_query(CREATE_DEF_MUTATION, variables)
    data   = result.get("data", {}).get("metafieldDefinitionCreate", {})
    errors = data.get("userErrors", [])
    if errors:
        return {"ok": False, "errors": errors}
    created = data.get("createdDefinition", {})
    return {"ok": True, "id": created.get("id"), "type": created.get("type", {}).get("name")}


# ── Step 4: Safety DRY-RUN print ─────────────────────────────────────────────
def print_plan(missing, mismatch, existing):
    print("\n" + "="*60)
    print("PLAN — definitions to create:")
    print("="*60)
    to_create = [
        (ns, key, t, dn, req)
        for (ns, key, t, dn, req) in missing
        if (ns, key) not in BLOCKED_FIELDS
    ]
    if not to_create:
        print("  (nothing to create — all required definitions exist)")
    for ns, key, t, dn, req in to_create:
        flag = "[REQUIRED]" if req else "[optional]"
        print(f"  {flag}  {ns}.{key}  →  type: {t}  |  name: {dn}")

    blocked_missing = [(ns, key, t, dn, req) for (ns, key, t, dn, req) in missing if (ns, key) in BLOCKED_FIELDS]
    if blocked_missing:
        print("\nBLOCKED (check-only, will NOT create):")
        for ns, key, t, dn, req in blocked_missing:
            print(f"  {ns}.{key}  — does not exist in Shopify, but contract says check-only")

    if mismatch:
        print("\nMISMATCH (type differs — will NOT auto-fix, manual review needed):")
        for ns, key, exp, act, dn, req in mismatch:
            print(f"  {ns}.{key}  expected={exp}  actual={act}")
    print("="*60)


# ── Step 5: Update status file ────────────────────────────────────────────────
def update_status_file(ok, missing, mismatch, created, failed, existing):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# סטטוס Metafield Definitions — Shopify Admin",
        f"**טרמינל 6 | BabyMania | ריבורן בלבד**",
        f"**עדכון:** {now}",
        "",
        "---",
        "",
        "## 1. שדות קיימים (מה שנמצא בשופיפיי)",
        "",
        "| namespace | key | type | status |",
        "|---|---|---|---|",
    ]

    for ns, key, t, dn, req in ok:
        lines.append(f"| `{ns}` | `{key}` | `{t}` | ✅ existed |")

    for c in created:
        lines.append(f"| `{c['ns']}` | `{c['key']}` | `{c['type']}` | ✅ created |")

    for ns, key, t, dn, req in missing:
        if (ns, key) in BLOCKED_FIELDS:
            lines.append(f"| `{ns}` | `{key}` | `{t}` | ⚠️ missing — check-only (not created) |")

    for f in failed:
        lines.append(f"| `{f['ns']}` | `{f['key']}` | `{f['type']}` | ❌ creation failed: {f['error']} |")

    for ns, key, exp, act, dn, req in mismatch:
        lines.append(f"| `{ns}` | `{key}` | expected `{exp}` / actual `{act}` | ⚠️ mismatch — manual review |")

    # Full table with Hero/CTA/FAQ/specs columns
    lines += [
        "",
        "---",
        "",
        "## 2. טבלת שימוש לפי סקשן",
        "",
        "| namespace | key | Hero S1 | Final CTA S17 | FAQ S16 | פרטי דגם S13 |",
        "|---|---|---|---|---|---|",
        "| `reborn_doll` | `hebrew_name` | ✅ | ✅ | ✅ | ❌ |",
        "| `reborn_doll` | `model_label` | ✅ | ✅ | ✅ | ❌ |",
        "| `reborn_specs` | `size_cm` | ✅ | ❌ | ❌ | ✅ |",
        "| `reborn_specs` | `source_note` | ❌ | ❌ | ❌ | ✅ |",
        "| `reborn_copy` | `hero_subtitle` | ✅ | ❌ | ❌ | ❌ |",
        "| `baby_mania` | `faq` | ❌ | ❌ | ✅ | ❌ |",
        "",
        "---",
        "",
        "## 3. שדות שלא נוצרו ולמה",
        "",
        "| שדה | סיבה |",
        "|---|---|",
        "| שיער / עיניים / אביזרים / בגדים | UNKNOWN בכל המוצרים |",
        "| רחיץ / גיל / CE | לא מאומת |",
        "| baby_mania.faq | check-only — אסור ליצור/לשנות |",
    ]

    # Can we go to step 7?
    required_missing = [
        (ns, key) for (ns, key, t, dn, req) in missing
        if req and (ns, key) not in BLOCKED_FIELDS
    ]
    required_failed  = [f for f in failed if f.get("required")]
    required_mismatch = [(ns, key) for (ns, key, exp, act, dn, req) in mismatch if req]

    can_proceed = (not required_missing) and (not required_failed) and (not required_mismatch)

    lines += [
        "",
        "---",
        "",
        "## 4. האם אפשר לעבור לשלב 7?",
        "",
    ]
    if can_proceed:
        lines += [
            "✅ **כן** — כל definitions חובה קיימים.",
            "",
            "שלב 7: המרת S1 Hero ו-S17 Final CTA ל-Liquid.",
            "",
            "לפני שלב 7 נדרש גם:",
            "- [ ] כתיבת ערכי לוי לשופיפיי (לפי `levi-metafield-values-draft.md`)",
            "- [ ] אישור אייל על הערכים",
        ]
    else:
        lines += ["❌ **לא עדיין** — יש בעיות שדורשות טיפול:"]
        for ns, key in required_missing:
            lines.append(f"- חסר required: `{ns}.{key}`")
        for f in required_failed:
            lines.append(f"- כשלון יצירה: `{f['ns']}.{f['key']}` — {f['error']}")
        for ns, key in required_mismatch:
            lines.append(f"- mismatch type: `{ns}.{key}` — צריך תיקון ידני")

    STATUS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  -> Status file updated: {STATUS_FILE}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "="*60)
    print("reborn_metafields_setup.py — Terminal 6")
    print("Mode: CHECK + CREATE missing definitions only")
    print("="*60)

    # Verify token (show only first 4 + last 4 chars)
    token = _get_access_token()
    masked = token[:4] + "..." + token[-4:]
    print(f"  Auth token: {masked}")
    print(f"  Shop: {SHOPIFY_SHOP_URL}")
    print(f"  API: {SHOPIFY_API_VERSION}")

    # Step 1: fetch existing
    existing = fetch_existing_definitions()
    print(f"  Found {len(existing)} existing PRODUCT metafield definitions.")

    # Step 2: compare
    ok, missing, mismatch = compare(existing)

    # Step 3: dry-run print
    print_plan(missing, mismatch, existing)

    # Step 4: create missing (skip BLOCKED_FIELDS)
    created = []
    failed  = []

    to_create = [
        (ns, key, t, dn, req)
        for (ns, key, t, dn, req) in missing
        if (ns, key) not in BLOCKED_FIELDS
    ]

    if to_create:
        print(f"\nCreating {len(to_create)} missing definition(s)...")
        for ns, key, t, dn, req in to_create:
            print(f"  -> Creating {ns}.{key} ({t})...", end=" ")
            result = create_definition(ns, key, t, dn)
            if result["ok"]:
                print("✅ created")
                created.append({"ns": ns, "key": key, "type": t, "id": result["id"], "required": req})
            else:
                err_msg = "; ".join(e.get("message", "?") for e in result["errors"])
                print(f"❌ FAILED: {err_msg}")
                failed.append({"ns": ns, "key": key, "type": t, "error": err_msg, "required": req})
    else:
        print("\nNothing to create.")

    # Step 5: update status file
    update_status_file(ok, missing, mismatch, created, failed, existing)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  existed:  {len(ok)}")
    print(f"  created:  {len(created)}")
    print(f"  failed:   {len(failed)}")
    print(f"  mismatch: {len(mismatch)}")
    blocked = [(ns, key) for (ns, key, t, dn, req) in missing if (ns, key) in BLOCKED_FIELDS]
    print(f"  blocked (check-only): {len(blocked)}")
    if blocked:
        for ns, key in blocked:
            status = "exists ✅" if (ns, key) in existing else "missing ⚠️"
            print(f"    {ns}.{key} — {status}")
    print("="*60)


if __name__ == "__main__":
    main()
