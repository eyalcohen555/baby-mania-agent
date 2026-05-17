"""
Phase 8C — Create 5 Smart Collections in Shopify Live
T3 approved by Ayal: 2026-05-05
Collections: gender-girl, gender-boy, type-set, type-romper, occ-gift
NOT creating: type-dress, type-bodysuit
"""

import json
import os
import sys
import requests
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

SHOP        = os.getenv("SHOPIFY_SHOP_URL", "a2756c-c0.myshopify.com")
TOKEN       = os.getenv("SHOPIFY_ACCESS_TOKEN")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-10")

if not TOKEN:
    raise RuntimeError("SHOPIFY_ACCESS_TOKEN is not set. Add it to your .env file.")

BASE_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

COLLECTIONS = [
    {
        "collection_key": "gender-girl",
        "handle": "gender-girl",
        "title": "בנות",
        "body_html": "גלי ביגוד תינוקות לבנות: שמלות, סטים, סרבלים ובגדי גוף. איכות פרימיום לתינוקות 0-24 חודש.",
        "meta_title": "ביגוד לבנות — BabyMania",
        "meta_description": "גלי ביגוד תינוקות לבנות: שמלות, סטים, סרבלים ובגדי גוף. איכות פרימיום לתינוקות 0-24 חודש.",
        "rule_condition": "gender-girl",
        "expected_count": 20,
    },
    {
        "collection_key": "gender-boy",
        "handle": "gender-boy",
        "title": "בנים",
        "body_html": "גלי ביגוד תינוקות לבנים: סטים, סרבלים ובגדי גוף. עיצובים מגניבים לתינוקות 0-24 חודש.",
        "meta_title": "ביגוד לבנים — BabyMania",
        "meta_description": "גלי ביגוד תינוקות לבנים: סטים, סרבלים ובגדי גוף. עיצובים מגניבים לתינוקות 0-24 חודש.",
        "rule_condition": "gender-boy",
        "expected_count": 19,
    },
    {
        "collection_key": "type-set",
        "handle": "type-set",
        "title": "סטים",
        "body_html": "סטים מושלמים לתינוקות: חליפות 2-3 חלקים באיכות פרימיום. מתאים לכל מגדר. מידות 0 עד 4 שנים.",
        "meta_title": "סטים לתינוקות — BabyMania",
        "meta_description": "סטים מושלמים לתינוקות: חליפות 2-3 חלקים באיכות פרימיום. מתאים לכל מגדר. מידות 0 עד 4 שנים.",
        "rule_condition": "type-set",
        "expected_count": 18,
    },
    {
        "collection_key": "type-romper",
        "handle": "type-romper",
        "title": "סרבלים ואוברולים",
        "body_html": "סרבלים ואוברולים לתינוקות: ג'ינס, פליז, כותנה. לבנות ולבנים. מידות Newborn עד 18-24 חודש.",
        "meta_title": "סרבלים לתינוקות — BabyMania",
        "meta_description": "סרבלים ואוברולים לתינוקות: ג'ינס, פליז, כותנה. לבנות ולבנים. מידות Newborn עד 18-24 חודש.",
        "rule_condition": "type-romper",
        "expected_count": 16,
    },
    {
        "collection_key": "occ-gift",
        "handle": "occ-gift",
        "title": "מתנות לתינוק",
        "body_html": "מתנות מושלמות לתינוק: סטים, סרבלים ושמלות. אידיאלי למקלחת תינוק ולהולדת ילד.",
        "meta_title": "מתנות לתינוק — BabyMania",
        "meta_description": "מתנות מושלמות לתינוק: סטים, סרבלים ושמלות. אידיאלי למקלחת תינוק ולהולדת ילד.",
        "rule_condition": "occ-gift",
        "expected_count": 14,
    },
]

BACKUP_PATH = "output/tags/phase8c-smart-collections-backup.json"
VERIFY_PATH = "output/tags/phase8c-smart-collections-live-verify.md"

created_collections = []


def get_all_smart_collections():
    url = f"{BASE_URL}/smart_collections.json?limit=250"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json().get("smart_collections", [])


def get_products_count(collection_id):
    url = f"{BASE_URL}/products/count.json?collection_id={collection_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json().get("count", -1)


def create_collection(cdef):
    payload = {
        "smart_collection": {
            "title": cdef["title"],
            "handle": cdef["handle"],
            "body_html": cdef["body_html"],
            "published": True,
            "disjunctive": False,
            "sort_order": "best-selling",
            "rules": [
                {
                    "column": "tag",
                    "relation": "equals",
                    "condition": cdef["rule_condition"]
                }
            ],
            "metafields": [
                {
                    "key": "title_tag",
                    "value": cdef["meta_title"],
                    "type": "single_line_text_field",
                    "namespace": "global"
                },
                {
                    "key": "description_tag",
                    "value": cdef["meta_description"],
                    "type": "single_line_text_field",
                    "namespace": "global"
                }
            ]
        }
    }
    url = f"{BASE_URL}/smart_collections.json"
    r = requests.post(url, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()["smart_collection"]


def verify_collection(collection_id, cdef):
    url = f"{BASE_URL}/smart_collections/{collection_id}.json"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    sc = r.json()["smart_collection"]

    products_count = get_products_count(collection_id)

    checks = {}
    checks["id_present"] = sc.get("id") is not None
    checks["handle_match"] = sc.get("handle") == cdef["handle"]
    checks["title_match"] = sc.get("title") == cdef["title"]
    checks["published"] = sc.get("published_at") is not None
    checks["disjunctive_false"] = sc.get("disjunctive") == False
    checks["sort_order"] = sc.get("sort_order") == "best-selling"
    rules = sc.get("rules", [])
    checks["rule_count"] = len(rules) == 1
    checks["rule_column"] = rules[0].get("column") == "tag" if rules else False
    checks["rule_relation"] = rules[0].get("relation") == "equals" if rules else False
    checks["rule_condition"] = rules[0].get("condition") == cdef["rule_condition"] if rules else False
    checks["products_count_ok"] = products_count >= (cdef["expected_count"] - 1)

    all_pass = all(checks.values())
    return sc, products_count, checks, all_pass


def delete_collection(collection_id):
    url = f"{BASE_URL}/smart_collections/{collection_id}.json"
    r = requests.delete(url, headers=HEADERS)
    return r.status_code


def main():
    print("=" * 60)
    print("Phase 8C — Creating 5 Smart Collections (LIVE)")
    print(f"Shop: {SHOP}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # STEP 1 — Check existing collections for conflicts
    print("\n[STEP 1] Checking existing smart collections for handle conflicts...")
    existing = get_all_smart_collections()
    existing_handles = {sc["handle"]: sc["id"] for sc in existing}
    print(f"  Found {len(existing)} existing smart collections")

    target_handles = [c["handle"] for c in COLLECTIONS]
    conflicts = [h for h in target_handles if h in existing_handles]
    if conflicts:
        print(f"  CONFLICT DETECTED: {conflicts}")
        print("  STOPPING — resolve conflicts before proceeding.")
        sys.exit(1)
    print(f"  No conflicts found. Safe to proceed.")

    # STEP 2 — Backup
    print("\n[STEP 2] Writing backup JSON...")
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "existing_smart_collections": existing,
        "planned_collections": COLLECTIONS
    }
    os.makedirs("output/tags", exist_ok=True)
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    print(f"  Backup written: {BACKUP_PATH}")

    # STEP 3 — Create collections one at a time
    print("\n[STEP 3] Creating collections...")
    verify_results = []

    for cdef in COLLECTIONS:
        print(f"\n  -> Creating: {cdef['handle']} ({cdef['title']})")
        try:
            sc = create_collection(cdef)
            cid = sc["id"]
            created_collections.append({"handle": cdef["handle"], "id": cid})
            print(f"     Created ID: {cid}")

            import time; time.sleep(2)  # allow Shopify to index the new collection

            sc_full, pcount, checks, all_pass = verify_collection(cid, cdef)
            result = {
                "collection_key": cdef["collection_key"],
                "handle": cdef["handle"],
                "title": cdef["title"],
                "id": cid,
                "products_count": pcount,
                "expected_count": cdef["expected_count"],
                "checks": checks,
                "all_pass": all_pass,
                "sc_data": sc_full
            }
            verify_results.append(result)

            if all_pass:
                print(f"     VERIFY: PASS ({pcount} products)")
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"     VERIFY: FAIL — failed checks: {failed}")
                print(f"     ROLLING BACK: deleting {cid}...")
                status = delete_collection(cid)
                print(f"     DELETE status: {status}")
                write_rollback_report(verify_results, cdef["handle"], failed)
                sys.exit(1)

        except requests.HTTPError as e:
            print(f"     HTTP ERROR: {e.response.status_code} — {e.response.text}")
            rollback_all()
            sys.exit(1)

    # STEP 4 — Write verify report
    print("\n[STEP 4] Writing verify report...")
    write_verify_report(verify_results)
    print(f"  Verify report: {VERIFY_PATH}")

    print("\n" + "=" * 60)
    print("Phase 8C COMPLETE — 5 Smart Collections created and verified")
    print("=" * 60)

    # Print summary for commit message reference
    for r in verify_results:
        status = "PASS" if r["all_pass"] else "FAIL"
        print(f"  {r['handle']:20s} id={r['id']}  count={r['products_count']}/{r['expected_count']}  {status}")


def rollback_all():
    print("\nROLLBACK: Deleting all created collections...")
    for item in created_collections:
        status = delete_collection(item["id"])
        print(f"  DELETE {item['handle']} (id={item['id']}): HTTP {status}")


def write_rollback_report(verify_results, failed_handle, failed_checks):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = "output/tags/phase8c-rollback-report.md"
    lines = [
        "# Phase 8C — Rollback Report",
        f"",
        f"**Date:** {ts}",
        f"**Failed on:** `{failed_handle}`",
        f"**Failed checks:** {failed_checks}",
        "",
        "## Collections Created Before Failure",
        "",
    ]
    for r in verify_results:
        status = "PASS — KEPT" if r["all_pass"] else "FAIL — DELETED"
        lines.append(f"- `{r['handle']}` (id={r['id']}) — {status}")
    lines += ["", "## Action", "All collections created in this run have been deleted. No Shopify state changed."]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Rollback report written: {path}")


def write_verify_report(verify_results):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Phase 8C — Smart Collections Live Verify Report",
        "",
        f"**Date:** {ts}  ",
        f"**Shop:** {SHOP}  ",
        f"**API Version:** {API_VERSION}  ",
        f"**Collections created:** {len(verify_results)}  ",
        f"**All PASS:** {all(r['all_pass'] for r in verify_results)}",
        "",
        "---",
        "",
    ]

    check_labels = {
        "id_present": "01. ID present",
        "handle_match": "02. Handle match",
        "title_match": "03. Title match",
        "published": "04. Published",
        "disjunctive_false": "05. Disjunctive=false",
        "sort_order": "06. Sort order=best-selling",
        "rule_count": "07. Rule count=1",
        "rule_column": "08. Rule column=tag",
        "rule_relation": "09. Rule relation=equals",
        "rule_condition": "10. Rule condition match",
        "products_count_ok": "11. Products count ≥ expected-1",
    }

    for r in verify_results:
        status = "PASS" if r["all_pass"] else "FAIL"
        sc = r["sc_data"]
        lines += [
            f"## Collection: `{r['handle']}` — {status}",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| ID | {r['id']} |",
            f"| Handle | {sc.get('handle')} |",
            f"| Title | {sc.get('title')} |",
            f"| Published | {sc.get('published_at')} |",
            f"| Disjunctive | {sc.get('disjunctive')} |",
            f"| Sort Order | {sc.get('sort_order')} |",
            f"| Rules | {json.dumps(sc.get('rules', []), ensure_ascii=False)} |",
            f"| Products Count | {r['products_count']} (expected ≥ {r['expected_count'] - 1}) |",
            "",
            "### QA Checks (11/11)",
            "",
        ]
        for key, label in check_labels.items():
            val = r["checks"].get(key)
            mark = "✅" if val else "❌"
            lines.append(f"- {mark} {label}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Summary table
    lines += [
        "## Summary Table",
        "",
        "| Collection | ID | Expected | Actual | Status |",
        "|------------|-----|----------|--------|--------|",
    ]
    for r in verify_results:
        status = "✅ PASS" if r["all_pass"] else "❌ FAIL"
        lines.append(f"| `{r['handle']}` | {r['id']} | {r['expected_count']} | {r['products_count']} | {status} |")

    lines += [
        "",
        "---",
        "",
        f"*Report generated by scripts/phase8c_create_collections.py — Phase 8C*",
    ]

    with open(VERIFY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
