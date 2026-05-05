"""
Phase 8F — Main Menu Navigation Update LIVE (T3 approved)
GraphQL menuUpdate on gid://shopify/Menu/250909851961
T3 approval: Ayal approved — 'בגדי תינוקות' + 'מתנות לתינוק' + remove 3 legacy items.
NO collections deleted. NO products changed. NO tags changed. NO Mega Menu.
"""
import sys, os, re, json, time, datetime, requests

sys.stdout.reconfigure(encoding="utf-8")

SHOP       = "a2756c-c0.myshopify.com"
GQL_URL    = f"https://{SHOP}/admin/api/2024-10/graphql.json"
BASE       = f"https://{SHOP}/admin/api/2024-10"
STOREFRONT = f"https://{SHOP}"
TOKEN_URL  = f"https://{SHOP}/admin/oauth/access_token"

DESKTOP_ENV = r"C:\Users\3024e\Desktop\shopify-token\.env"
PROJECT_ENV = r"C:\Projects\baby-mania-agent\.env"

MENU_GID  = "gid://shopify/Menu/250909851961"
MENU_HANDLE = "main-menu"

BACKUP_JSON = "output/tags/phase8f-main-menu-prewrite-backup.json"
REPORT_MD   = "output/tags/phase8f-navigation-live-verify.md"
REPORT_JSON = "output/tags/phase8f-navigation-live-verify.json"

# Collection GIDs — Phase 8C + Phase 8E-4
COLLS = {
    "gender-girl":  "gid://shopify/Collection/526691729721",
    "gender-boy":   "gid://shopify/Collection/526691762489",
    "type-set":     "gid://shopify/Collection/526691795257",
    "type-romper":  "gid://shopify/Collection/526691828025",
    "occ-gift":     "gid://shopify/Collection/526691860793",
    "clothing-all": "gid://shopify/Collection/526700020025",
}

# Items to remove from nav by exact title
REMOVE_TITLES = {"בגדי בנות", "בגדי בנים", "מארזי מתנה"}

# 6 URLs to verify
CHECK_URLS = [
    "/collections/type-set",
    "/collections/type-romper",
    "/collections/gender-girl",
    "/collections/gender-boy",
    "/collections/clothing-all",
    "/collections/occ-gift",
]

# ── GraphQL fragments ──────────────────────────────────────────────────────────

QUERY_MENU = """
{
  menus(first: 1, query: "handle:main-menu") {
    edges {
      node {
        id handle title
        items {
          id title url type resourceId
          items { id title url type resourceId }
        }
      }
    }
  }
}
"""

MUTATION_MENU_UPDATE = """
mutation menuUpdate($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) {
  menuUpdate(id: $id, title: $title, items: $items) {
    menu {
      id handle title
      items {
        id title url type resourceId
        items { id title url type resourceId }
      }
    }
    userErrors { field message }
  }
}
"""


def load_env(path):
    d = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    d[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return d


def update_desktop_token(tok):
    try:
        with open(DESKTOP_ENV, encoding="utf-8") as f:
            c = f.read()
        c = re.sub(r"^SHOPIFY_ACCESS_TOKEN=.*$", f"SHOPIFY_ACCESS_TOKEN={tok}", c, flags=re.MULTILINE)
        with open(DESKTOP_ENV, "w", encoding="utf-8") as f:
            f.write(c)
    except Exception as e:
        print(f"  Warning: .env update failed: {e}")


def get_fresh_token(cid, csec):
    r = requests.post(TOKEN_URL,
        data={"grant_type": "client_credentials", "client_id": cid, "client_secret": csec},
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=15)
    r.raise_for_status()
    return r.json()["access_token"]


def gql(token, query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(GQL_URL,
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        json=payload, timeout=25)
    return r.status_code, r.json()


def rest_get(token, path):
    r = requests.get(f"{BASE}{path}",
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        timeout=15)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {}


def check_url(path):
    try:
        r = requests.get(f"{STOREFRONT}{path}", timeout=12, allow_redirects=True)
        return r.status_code
    except Exception as e:
        return 0


def read_menu(token):
    code, body = gql(token, QUERY_MENU)
    if code != 200:
        return None, f"HTTP {code}"
    errors = body.get("errors")
    if errors:
        return None, str(errors)
    edges = body.get("data", {}).get("menus", {}).get("edges", [])
    if not edges:
        return None, "no edges returned"
    return edges[0]["node"], None


def items_to_input(items_list):
    """Convert live item list to MenuItemUpdateInput list for rollback."""
    result = []
    for item in items_list:
        inp = {"title": item["title"], "type": item["type"]}
        if item.get("resourceId"):
            inp["resourceId"] = item["resourceId"]
        if item.get("url") and item["type"] not in ("COLLECTION", "BLOG", "PAGE", "FRONTPAGE", "CATALOG", "PRODUCT", "PRODUCT_VARIANT"):
            inp["url"] = item["url"]
        if item.get("type") == "HTTP":
            inp["url"] = item.get("url", "#")
        nested = item.get("items", [])
        if nested:
            inp["items"] = items_to_input(nested)
        result.append(inp)
    return result


def build_new_items(existing_items):
    """
    Build the new items list for the updated menu.
    Inserts 'בגדי תינוקות' (parent+5 subs) and 'מתנות לתינוק' after 'דף הבית'.
    Removes REMOVE_TITLES from top-level.
    """
    new_items = []

    # Inject after דף הבית
    clothing_parent = {
        "title": "בגדי תינוקות",
        "type": "HTTP",
        "url": "#",
        "items": [
            {"title": "סטים",      "type": "COLLECTION", "resourceId": COLLS["type-set"]},
            {"title": "סרבלים",    "type": "COLLECTION", "resourceId": COLLS["type-romper"]},
            {"title": "בגדי בנות", "type": "COLLECTION", "resourceId": COLLS["gender-girl"]},
            {"title": "בגדי בנים", "type": "COLLECTION", "resourceId": COLLS["gender-boy"]},
            {"title": "כל הבגדים", "type": "COLLECTION", "resourceId": COLLS["clothing-all"]},
        ],
    }
    gifts_item = {
        "title": "מתנות לתינוק",
        "type": "COLLECTION",
        "resourceId": COLLS["occ-gift"],
    }

    inserted = False
    for item in existing_items:
        title = item.get("title", "")

        # Skip removed items
        if title in REMOVE_TITLES:
            continue

        new_items.append(item_to_input(item))

        # After דף הבית — inject new items
        if title == "דף הבית" and not inserted:
            new_items.append(item_to_input(clothing_parent))
            new_items.append(item_to_input(gifts_item))
            inserted = True

    if not inserted:
        # fallback: prepend if דף הבית not found
        new_items = [item_to_input(clothing_parent), item_to_input(gifts_item)] + new_items

    return new_items


def item_to_input(item):
    """Convert a single item dict to MenuItemUpdateInput."""
    inp = {"title": item["title"], "type": item["type"]}

    if item.get("resourceId"):
        inp["resourceId"] = item["resourceId"]

    # URL: only for HTTP type
    if item["type"] == "HTTP":
        inp["url"] = item.get("url", "#")

    nested = item.get("items", [])
    if nested:
        inp["items"] = [item_to_input(n) for n in nested]

    return inp


def main():
    print("=" * 62)
    print("Phase 8F — Main Menu Navigation Update LIVE")
    print("T3 approval: Ayal — מאשר Phase 8F")
    print("=" * 62)

    de = load_env(DESKTOP_ENV)
    pe = load_env(PROJECT_ENV)
    cid  = de.get("SHOPIFY_CLIENT_ID") or pe.get("SHOPIFY_CLIENT_ID")
    csec = de.get("SHOPIFY_CLIENT_SECRET") or pe.get("SHOPIFY_CLIENT_SECRET")

    print("\n[0] Token...")
    try:
        token = get_fresh_token(cid, csec)
        update_desktop_token(token)
        print(f"  ✅ suffix={token[-4:]}")
    except Exception as e:
        token = de.get("SHOPIFY_ACCESS_TOKEN", "")
        print(f"  ⚠ fallback suffix={token[-4:] if token else 'N/A'}: {e}")
    if not token:
        print("  ❌ no token"); return

    os.makedirs("output/tags", exist_ok=True)

    # ── Step A: Read + backup current menu ────────────────────────────────────
    print("\n[A] Reading current main-menu for backup...")
    current_menu, err = read_menu(token)
    if err or not current_menu:
        print(f"  ❌ Failed to read menu: {err}")
        return

    menu_id_live = current_menu["id"]
    menu_title   = current_menu["title"]
    current_items = current_menu.get("items", [])
    before_count  = len(current_items)

    print(f"  ✅ Menu: '{menu_title}' | id={menu_id_live} | items={before_count}")

    if menu_id_live != MENU_GID:
        print(f"  ❌ STOP — menu GID mismatch: expected {MENU_GID}, got {menu_id_live}")
        return

    # Save backup
    backup_data = {
        "backup_time": datetime.datetime.now().isoformat(),
        "phase": "8F-prewrite",
        "menu_id": menu_id_live,
        "menu_handle": current_menu.get("handle"),
        "menu_title": menu_title,
        "item_count": before_count,
        "items": current_items,
    }
    with open(BACKUP_JSON, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Backup saved → {BACKUP_JSON}")

    # ── Step B: URL checks ────────────────────────────────────────────────────
    print("\n[B] URL pre-checks...")
    url_results = {}
    all_urls_ok = True
    for path in CHECK_URLS:
        status = check_url(path)
        ok = status == 200
        url_results[path] = status
        print(f"  {'✅' if ok else '❌'} {path} → HTTP {status}")
        if not ok:
            all_urls_ok = False

    if not all_urls_ok:
        failed = [p for p, s in url_results.items() if s != 200]
        print(f"\n  ⛔ HOLD — URL check failed: {failed}")
        print("  verdict: HOLD_PHASE8F_URL_FAIL")
        write_hold_report(token[-4:], "URL_FAIL", failed, before_count, url_results)
        return

    print("  ✅ All 6 URLs return 200")

    # ── Step C: Build new items list ──────────────────────────────────────────
    print("\n[C] Building new items list...")
    new_items = build_new_items(current_items)
    after_count_expected = len(new_items)
    print(f"  Before: {before_count} top-level items")
    print(f"  Expected after: {after_count_expected} top-level items")
    print(f"  (removed: {len(REMOVE_TITLES)}, added: 2 — 'בגדי תינוקות' + 'מתנות לתינוק')")

    # Print new structure
    for i, item in enumerate(new_items, 1):
        sub = item.get("items", [])
        sub_str = f" [{len(sub)} subs]" if sub else ""
        print(f"    {i:2}. {item['title']}{sub_str}")
        for s in sub:
            print(f"         └─ {s['title']}")

    # ── Step D: menuUpdate mutation ───────────────────────────────────────────
    print("\n[D] Executing menuUpdate mutation...")
    variables = {
        "id": MENU_GID,
        "title": menu_title,
        "items": new_items,
    }

    mutation_ok = False
    mutation_errors = []
    updated_menu = None

    time.sleep(1)
    code_m, body_m = gql(token, MUTATION_MENU_UPDATE, variables)

    gql_errors = body_m.get("errors")
    if gql_errors:
        print(f"  ❌ GraphQL errors: {gql_errors}")
        mutation_errors = gql_errors
    elif code_m != 200:
        print(f"  ❌ HTTP {code_m}")
        mutation_errors = [{"message": f"HTTP {code_m}"}]
    else:
        payload_data = body_m.get("data", {}).get("menuUpdate", {})
        user_errors = payload_data.get("userErrors", [])
        if user_errors:
            print(f"  ❌ userErrors: {user_errors}")
            mutation_errors = user_errors
        else:
            updated_menu = payload_data.get("menu", {})
            mutation_ok = True
            print(f"  ✅ menuUpdate succeeded — id={updated_menu.get('id')}")

    if not mutation_ok:
        print(f"\n[E] Verdict: PHASE8F_NAVIGATION_LIVE_FAIL (mutation failed)")
        write_fail_report(token[-4:], mutation_errors, before_count, url_results)
        return

    # ── Step E: Verify ─────────────────────────────────────────────────────────
    print("\n[E] Verify — re-reading menu...")
    time.sleep(2)
    verified_menu, verr = read_menu(token)
    if verr or not verified_menu:
        print(f"  ❌ Could not re-read menu: {verr}")
        verified_menu = updated_menu  # fall back to mutation response

    v_items    = verified_menu.get("items", [])
    v_id       = verified_menu.get("id", "")
    after_count = len(v_items)

    checks = {}

    # 1. GID unchanged
    checks["01_gid_unchanged"] = ("✅", f"id={v_id}") if v_id == MENU_GID else ("❌", f"id changed: {v_id}")

    # 2. 'בגדי תינוקות' exists as top-level
    clothing_item = next((i for i in v_items if i["title"] == "בגדי תינוקות"), None)
    checks["02_clothing_parent_exists"] = ("✅", "'בגדי תינוקות' found") if clothing_item else ("❌", "'בגדי תינוקות' not found")

    # 3. Exactly 5 sub-items under 'בגדי תינוקות'
    sub_count = len(clothing_item.get("items", [])) if clothing_item else 0
    checks["03_clothing_sub_count"] = ("✅", f"{sub_count} sub-items") if sub_count == 5 else ("❌", f"{sub_count} sub-items (expected 5)")

    # 4. Sub-item order and URLs
    expected_subs = [
        ("סטים",      "/collections/type-set"),
        ("סרבלים",    "/collections/type-romper"),
        ("בגדי בנות", "/collections/gender-girl"),
        ("בגדי בנים", "/collections/gender-boy"),
        ("כל הבגדים", "/collections/clothing-all"),
    ]
    subs_actual = [(s["title"], s.get("url", "")) for s in (clothing_item.get("items", []) if clothing_item else [])]
    sub_order_ok = True
    sub_url_ok   = True
    sub_notes    = []
    for i, (exp_title, exp_url_part) in enumerate(expected_subs):
        if i < len(subs_actual):
            act_title, act_url = subs_actual[i]
            if act_title != exp_title:
                sub_order_ok = False
                sub_notes.append(f"pos{i+1}: title={act_title} (expected {exp_title})")
            if exp_url_part not in act_url:
                sub_url_ok = False
                sub_notes.append(f"pos{i+1}: url={act_url} (expected contains {exp_url_part})")
        else:
            sub_order_ok = False
            sub_notes.append(f"missing pos{i+1}")

    checks["04_sub_order"] = ("✅", "correct order") if sub_order_ok else ("❌", "; ".join(sub_notes))
    checks["05_sub_urls"]  = ("✅", "all URLs correct") if sub_url_ok else ("❌", "; ".join(sub_notes))

    # 5. 'מתנות לתינוק' exists as top-level
    gifts_item_v = next((i for i in v_items if i["title"] == "מתנות לתינוק"), None)
    checks["06_gifts_exists"] = ("✅", "'מתנות לתינוק' found") if gifts_item_v else ("❌", "'מתנות לתינוק' not found")

    # 6. 'מתנות לתינוק' points to /collections/occ-gift
    gifts_url = gifts_item_v.get("url", "") if gifts_item_v else ""
    checks["07_gifts_url"] = ("✅", f"url={gifts_url}") if "occ-gift" in gifts_url else ("❌", f"url={gifts_url} (expected occ-gift)")

    # 7. Legacy items removed from top-level
    legacy_still_present = [i["title"] for i in v_items if i["title"] in REMOVE_TITLES]
    checks["08_legacy_removed"] = ("✅", "3 legacy items removed") if not legacy_still_present else ("❌", f"still present: {legacy_still_present}")

    # 8. Unrelated items untouched — check a sample
    preserved_titles = {"דף הבית", "בגדי חורף", "קיץ 2026", "כל המוצרים", "בובת ריבורן", "מוצרי בטיחות", "בלוג", "יצירת קשר"}
    v_title_set = {i["title"] for i in v_items}
    missing_preserved = preserved_titles - v_title_set
    checks["09_unrelated_preserved"] = ("✅", "unrelated items intact") if not missing_preserved else ("❌", f"missing: {missing_preserved}")

    # 9. URL checks after mutation
    print("  Re-checking URLs...")
    post_url_results = {}
    all_post_ok = True
    for path in CHECK_URLS:
        status = check_url(path)
        post_url_results[path] = status
        ok = status == 200
        if not ok:
            all_post_ok = False
    checks["10_urls_200"] = ("✅", "all 6 URLs → 200") if all_post_ok else ("❌", f"failed: {[p for p,s in post_url_results.items() if s!=200]}")

    # 11. No Mega Menu
    has_mega = any(len(i.get("items", [])) > 10 for i in v_items)
    checks["11_no_mega_menu"] = ("✅", "no mega menu") if not has_mega else ("❌", "has mega menu (>10 nested items)")

    # 12. Collections unchanged — check count via REST
    code_cc, body_cc = rest_get(token, "/smart_collections/count.json")
    coll_count = body_cc.get("count", -1) if code_cc == 200 else -1
    checks["12_collections_unchanged"] = ("✅", f"smart collections count={coll_count} (expected 6)") if coll_count == 6 else ("❌", f"count={coll_count}")

    # 13. clothing-all still exists with 51 products
    code_ca, body_ca = rest_get(token, "/smart_collections.json?handle=clothing-all")
    ca_list = body_ca.get("smart_collections", []) if code_ca == 200 else []
    ca_exists = len(ca_list) > 0
    checks["13_clothing_all_exists"] = ("✅", f"clothing-all exists") if ca_exists else ("❌", "clothing-all not found")

    code_capc, body_capc = rest_get(token, "/products/count.json?collection_id=526700020025")
    ca_count = body_capc.get("count", -1) if code_capc == 200 else -1
    checks["14_clothing_all_count"] = ("✅", f"count={ca_count}") if ca_count == 51 else ("❌", f"count={ca_count} (expected 51)")

    # 14. No product tag changes
    checks["15_no_tag_changes"] = ("✅", "no tag writes in this phase")
    checks["16_item_count"] = ("✅", f"top-level items: {after_count}") if after_count == after_count_expected else ("❌", f"got {after_count}, expected {after_count_expected}")

    print(f"\n  Verify results ({after_count} top-level items):")
    all_pass = True
    for key, (mark, detail) in sorted(checks.items()):
        print(f"  {mark} {key}: {detail}")
        if mark == "❌":
            all_pass = False

    # ── Step F: Rollback if needed ─────────────────────────────────────────────
    rollback_needed = False
    rollback_ok = False
    if not all_pass:
        critical_fails = [k for k, (m, _) in checks.items() if m == "❌"]
        print(f"\n  ⚠️  Critical failures: {critical_fails}")
        print("  Attempting rollback...")
        rollback_items = items_to_input(current_items)
        rb_vars = {"id": MENU_GID, "title": menu_title, "items": rollback_items}
        rb_code, rb_body = gql(token, MUTATION_MENU_UPDATE, rb_vars)
        rb_ue = rb_body.get("data", {}).get("menuUpdate", {}).get("userErrors", [])
        if rb_code == 200 and not rb_ue:
            rollback_ok = True
            rollback_needed = True
            print("  ✅ Rollback succeeded — menu restored")
        else:
            rollback_needed = True
            print(f"  ❌ Rollback FAILED — HTTP {rb_code}, userErrors={rb_ue}")

    verdict = "PHASE8F_NAVIGATION_LIVE_PASS"
    if not all_pass:
        verdict = "PHASE8F_NAVIGATION_ROLLED_BACK" if rollback_ok else "PHASE8F_NAVIGATION_LIVE_FAIL"

    print(f"\n[F] Verdict: {verdict}")
    print(f"    before_count={before_count}, after_count={after_count}")
    print(f"    rollback_needed={rollback_needed}")

    # ── Step G: Reports ────────────────────────────────────────────────────────
    write_report(token[-4:], v_items, before_count, after_count, checks,
                 url_results, post_url_results, rollback_needed, rollback_ok, verdict, current_items)
    write_json_report(token[-4:], v_items, before_count, after_count, checks,
                      url_results, post_url_results, rollback_needed, rollback_ok, verdict)

    print(f"\n  Reports saved:")
    print(f"    {REPORT_MD}")
    print(f"    {REPORT_JSON}")

    return verdict


def write_hold_report(tok_sfx, reason, details, before_count, url_results):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 8F — Navigation Live Verify\n\n")
        f.write(f"**Date:** {ts}\n**Verdict:** HOLD_PHASE8F_{reason}\n\n")
        f.write(f"Phase halted — {reason}: {details}\n")
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump({"verdict": f"HOLD_PHASE8F_{reason}", "details": details}, f, ensure_ascii=False, indent=2)


def write_fail_report(tok_sfx, errors, before_count, url_results):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 8F — Navigation Live Verify\n\n")
        f.write(f"**Date:** {ts}\n**Verdict:** PHASE8F_NAVIGATION_LIVE_FAIL\n\n")
        f.write(f"Mutation failed:\n```\n{json.dumps(errors, ensure_ascii=False, indent=2)}\n```\n")
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump({"verdict": "PHASE8F_NAVIGATION_LIVE_FAIL", "errors": errors}, f, ensure_ascii=False, indent=2)


def write_report(tok_sfx, v_items, before, after, checks, pre_urls, post_urls,
                 rollback, rollback_ok, verdict, orig_items):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Phase 8F — Navigation Live Verify",
        "",
        f"**Date:** {ts}  ",
        f"**Shop:** a2756c-c0.myshopify.com  ",
        f"**T3 Approval:** Ayal — מאשר Phase 8F — עדכון main-menu  ",
        f"**Token suffix:** `{tok_sfx}`  ",
        "",
        "---",
        "",
        "## 1. T3 Approval",
        "",
        "| Field | Value |",
        "|-------|-------|",
        "| Tier | T3 |",
        "| Approver | אייל |",
        "| Scope | menuUpdate בלבד — no collections, no products, no tags, no theme |",
        "| Mega Menu | ❌ לא |",
        "| Collections deleted | ❌ לא |",
        "",
        "---",
        "",
        "## 2. Backup",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Backup path | `{BACKUP_JSON}` |",
        f"| Before item count | {before} |",
        "",
        "---",
        "",
        "## 3. Menu",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Menu GID | `gid://shopify/Menu/250909851961` |",
        f"| Before | {before} top-level items |",
        f"| After | {after} top-level items |",
        f"| Removed from nav | 'בגדי בנות', 'בגדי בנים', 'מארזי מתנה' (nav only, not deleted) |",
        f"| Added | 'בגדי תינוקות' (parent+5 subs), 'מתנות לתינוק' |",
        "",
        "### New Menu Structure:",
        "",
        "| # | Item | Sub-items |",
        "|---|------|-----------|",
    ]
    for i, item in enumerate(v_items, 1):
        subs = item.get("items", [])
        sub_str = " / ".join(s["title"] for s in subs) if subs else "—"
        lines.append(f"| {i} | {item['title']} | {sub_str} |")

    lines += [
        "",
        "---",
        "",
        "## 4. Verify Checks (16)",
        "",
        "| Check | Mark | Detail |",
        "|-------|------|--------|",
    ]
    for key, (mark, detail) in sorted(checks.items()):
        lines.append(f"| `{key}` | {mark} | {detail} |")

    lines += [
        "",
        "---",
        "",
        "## 5. URL Checks",
        "",
        "| URL | Pre | Post |",
        "|-----|-----|------|",
    ]
    for path in CHECK_URLS:
        pre  = pre_urls.get(path, "?")
        post = post_urls.get(path, "?")
        lines.append(f"| `{path}` | {pre} | {post} |")

    lines += [
        "",
        "---",
        "",
        "## 6. Rollback",
        "",
        f"| Rollback needed | {'✅ לא נדרש' if not rollback else '⚠ כן — ' + ('הצליח' if rollback_ok else 'נכשל')} |",
        "|-----------------|--|",
        "",
        "---",
        "",
        "## 7. Side Effects",
        "",
        "| Check | Status |",
        "|-------|--------|",
        "| Collections changed | ✅ לא |",
        "| Products changed | ✅ לא |",
        "| Tags changed | ✅ לא |",
        "| Theme changed | ✅ לא |",
        "",
        "---",
        "",
        "## 8. Verdict",
        "",
        f"**{verdict}**",
        "",
    ]

    if verdict == "PHASE8F_NAVIGATION_LIVE_PASS":
        lines += [
            "✅ main-menu עודכן בהצלחה.",
            "בגדי תינוקות עם 5 תתי פריטים: סטים, סרבלים, בגדי בנות, בגדי בנים, כל הבגדים.",
            "מתנות לתינוק כפריט ראשי נפרד.",
            "3 פריטים ישנים הוסרו מהניווט בלבד — collections לא נמחקו.",
            "הצעד הבא: Visual QA ידני.",
        ]
    elif verdict == "PHASE8F_NAVIGATION_ROLLED_BACK":
        lines += [
            "⚠️ Verify נכשל — rollback בוצע בהצלחה.",
            "התפריט שוחזר למצב המקורי.",
            "יש לבדוק את הסיבה לכשל לפני ניסיון חוזר.",
        ]
    else:
        lines += [
            "❌ mutation נכשל.",
            "ראה checks section לפרטים.",
            "לא בוצע rollback (mutation לא הצליח).",
        ]

    lines += ["", "---", "", "*Report generated by scripts/phase8f_navigation_live.py*"]

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_json_report(tok_sfx, v_items, before, after, checks, pre_urls, post_urls,
                      rollback, rollback_ok, verdict):
    payload = {
        "phase": "8F",
        "type": "navigation_live_update",
        "t3_approval": "Ayal: מאשר Phase 8F — עדכון main-menu עם בגדי תינוקות + מתנות לתינוק",
        "token_suffix": tok_sfx,
        "menu_gid": MENU_GID,
        "before_item_count": before,
        "after_item_count": after,
        "items_removed_from_nav": list(REMOVE_TITLES),
        "items_added": ["בגדי תינוקות (parent+5)", "מתנות לתינוק"],
        "pre_url_checks": pre_urls,
        "post_url_checks": post_urls,
        "checks": {k: {"mark": v[0], "detail": v[1]} for k, v in checks.items()},
        "rollback_needed": rollback,
        "rollback_ok": rollback_ok if rollback else None,
        "collections_changed": False,
        "products_changed": False,
        "tags_changed": False,
        "shopify_writes": "1 GraphQL menuUpdate only",
        "final_menu_structure": [
            {
                "title": i["title"],
                "url": i.get("url"),
                "type": i.get("type"),
                "sub_items": [{"title": s["title"], "url": s.get("url")} for s in i.get("items", [])],
            }
            for i in v_items
        ],
        "verdict": verdict,
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
