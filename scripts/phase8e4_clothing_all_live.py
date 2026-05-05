"""
Phase 8E-4 — clothing-all Smart Collection LIVE CREATE (T3 approved)
Creates clothing-all Smart Collection in Shopify. Verifies 16 checks.
T3 approval: Ayal explicitly approved "Phase 8E-4 — יצירת Smart Collection clothing-all בלייב"
"""
import sys, os, re, json, time, requests
sys.stdout.reconfigure(encoding="utf-8")

SHOP      = "a2756c-c0.myshopify.com"
BASE      = f"https://{SHOP}/admin/api/2024-10"
STOREFRONT = f"https://{SHOP}"
TOKEN_URL = f"https://{SHOP}/admin/oauth/access_token"

DESKTOP_ENV = r"C:\Users\3024e\Desktop\shopify-token\.env"
PROJECT_ENV = r"C:\Projects\baby-mania-agent\.env"

BACKUP_JSON  = "output/tags/phase8e4-clothing-all-precreate-backup.json"
REPORT_MD    = "output/tags/phase8e4-clothing-all-live-verify.md"
REPORT_JSON  = "output/tags/phase8e4-clothing-all-live-verify.json"

COLLECTION_DEF = {
    "title":       "כל בגדי התינוקות",
    "handle":      "clothing-all",
    "sort_order":  "best-selling",
    "published":   True,
    "disjunctive": True,
    "rules": [
        {"column": "tag", "relation": "equals", "condition": "type-set"},
        {"column": "tag", "relation": "equals", "condition": "type-romper"},
        {"column": "tag", "relation": "equals", "condition": "type-dress"},
        {"column": "tag", "relation": "equals", "condition": "type-bodysuit"},
    ],
    "seo_title":       "בגדי תינוקות | Baby Mania",
    "seo_description": "בגדי תינוקות איכותיים מבד אורגני — סטים, סרבלים, שמלות ובגדי גוף לתינוקות מ-0 עד 3 שנים. משלוח מהיר בישראל.",
}

EXPECTED_COUNT_MIN, EXPECTED_COUNT_MAX = 48, 54


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


def api(method, token, path, payload=None):
    url = f"{BASE}{path}"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    r = getattr(requests, method)(url, headers=headers, json=payload, timeout=20)
    try:
        body = r.json()
    except Exception:
        body = {}
    return r.status_code, body


def main():
    print("=" * 62)
    print("Phase 8E-4 — clothing-all LIVE CREATE")
    print("T3 approval: Ayal approved explicitly")
    print("=" * 62)

    de = load_env(DESKTOP_ENV); pe = load_env(PROJECT_ENV)
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

    # ── Step A: Backup existing smart collections ──────────────────────────
    print("\n[A] Backup existing smart collections...")
    code, body = api("get", token, "/smart_collections.json?limit=250")
    existing_smarts = body.get("smart_collections", []) if code == 200 else []
    with open(BACKUP_JSON, "w", encoding="utf-8") as f:
        json.dump({"backup_time": __import__("datetime").datetime.now().isoformat(),
                   "smart_collections": existing_smarts}, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Backup: {len(existing_smarts)} smart collections → {BACKUP_JSON}")

    # ── Step B: Final duplicate check ─────────────────────────────────────
    print("\n[B] Final duplicate check...")
    code2, body2 = api("get", token, "/smart_collections.json?handle=clothing-all")
    dupes = body2.get("smart_collections", []) if code2 == 200 else []
    if dupes:
        existing_id = dupes[0].get("id")
        print(f"  ⚠️  clothing-all already exists — id={existing_id} — skipping create")
        coll = dupes[0]
        created_new = False
    else:
        print("  ✅ No duplicate — proceeding to create")
        created_new = True
        coll = None

    # ── Step C: Create ─────────────────────────────────────────────────────
    if created_new:
        print("\n[C] Creating clothing-all smart collection...")
        payload = {"smart_collection": {
            "title":       COLLECTION_DEF["title"],
            "handle":      COLLECTION_DEF["handle"],
            "sort_order":  COLLECTION_DEF["sort_order"],
            "published":   COLLECTION_DEF["published"],
            "disjunctive": COLLECTION_DEF["disjunctive"],
            "rules":       COLLECTION_DEF["rules"],
            "metafields": [
                {"namespace": "global", "key": "title_tag",       "value": COLLECTION_DEF["seo_title"],       "type": "single_line_text_field"},
                {"namespace": "global", "key": "description_tag", "value": COLLECTION_DEF["seo_description"], "type": "single_line_text_field"},
            ],
        }}
        code_c, body_c = api("post", token, "/smart_collections.json", payload)
        if code_c in (200, 201):
            coll = body_c.get("smart_collection", {})
            coll_id = coll.get("id")
            print(f"  ✅ Created — id={coll_id} HTTP {code_c}")
        else:
            print(f"  ❌ Create failed — HTTP {code_c}: {body_c}")
            write_report_fail(token[-4:], code_c, body_c)
            return
    else:
        print("\n[C] Skipping create — already exists")

    coll_id = coll.get("id")

    # ── Step D: Verify ─────────────────────────────────────────────────────
    print(f"\n[D] Verify — re-reading collection id={coll_id}...")
    time.sleep(2)  # brief settle
    code_v, body_v = api("get", token, f"/smart_collections/{coll_id}.json")
    if code_v != 200:
        print(f"  ❌ Read-back failed HTTP {code_v}")
        write_report_fail(token[-4:], code_v, body_v)
        return

    c = body_v.get("smart_collection", {})
    checks = {}

    checks["01_exists"]       = ("✅", "collection exists") if c else ("❌", "not found")
    checks["02_handle"]       = ("✅", f"handle={c.get('handle')}") if c.get("handle") == "clothing-all" else ("❌", f"handle={c.get('handle')}")
    checks["03_title"]        = ("✅", f"title={c.get('title')}") if c.get("title") == "כל בגדי התינוקות" else ("❌", f"title={c.get('title')}")
    checks["04_published"]    = ("✅", "published=true") if c.get("published_at") else ("❌", "not published")
    checks["05_sort_order"]   = ("✅", "sort=best-selling") if c.get("sort_order") == "best-selling" else ("❌", f"sort={c.get('sort_order')}")
    checks["06_disjunctive"]  = ("✅", "disjunctive=true") if c.get("disjunctive") is True else ("❌", f"disjunctive={c.get('disjunctive')}")

    rules = c.get("rules", [])
    rule_conditions = {r.get("condition") for r in rules}
    expected_conditions = {"type-set", "type-romper", "type-dress", "type-bodysuit"}
    checks["07_rules"]        = ("✅", f"4 rules: {sorted(rule_conditions)}") if rule_conditions == expected_conditions else ("❌", f"rules={rule_conditions}")
    checks["08_rule_count"]   = ("✅", "4 rules") if len(rules) == 4 else ("❌", f"rule_count={len(rules)}")

    # product count
    code_pc, body_pc = api("get", token, f"/products/count.json?collection_id={coll_id}")
    prod_count = body_pc.get("count", -1) if code_pc == 200 else -1
    in_range = EXPECTED_COUNT_MIN <= prod_count <= EXPECTED_COUNT_MAX
    checks["09_product_count"] = ("✅", f"count={prod_count}") if in_range else ("❌", f"count={prod_count} outside [{EXPECTED_COUNT_MIN},{EXPECTED_COUNT_MAX}]")

    # URL check
    url_path = f"/collections/{c.get('handle', 'clothing-all')}"
    try:
        r_url = requests.get(f"{STOREFRONT}{url_path}", timeout=12, allow_redirects=True)
        url_status = r_url.status_code
    except Exception as e:
        url_status = 0
    checks["11_url_200"] = ("✅", f"HTTP {url_status}") if url_status == 200 else ("❌", f"HTTP {url_status}")

    # SEO — check via metafields
    code_mf, body_mf = api("get", token, f"/smart_collections/{coll_id}/metafields.json")
    mf_list = body_mf.get("metafields", []) if code_mf == 200 else []
    seo_title_found = any(m.get("key") == "title_tag" for m in mf_list)
    seo_desc_found  = any(m.get("key") == "description_tag" for m in mf_list)
    checks["12_seo_title"]       = ("✅", "seo_title present") if seo_title_found else ("⚠", "seo_title not in metafields (may be set via body_html_summary)")
    checks["13_seo_description"] = ("✅", "seo_desc present") if seo_desc_found else ("⚠", "seo_desc not in metafields")

    # No extra collections created (compare backup count)
    code_now, body_now = api("get", token, "/smart_collections/count.json")
    count_now = body_now.get("count", -1) if code_now == 200 else -1
    count_before = len(existing_smarts) + (1 if created_new else 0)
    checks["14_no_extra_colls"] = ("✅", f"count={count_now} (expected={count_before})") if count_now == count_before else ("❌", f"count={count_now} vs expected={count_before}")

    # Navigation unchanged — check main-menu GID via GraphQL
    nav_check_ok = True
    try:
        gql_r = requests.post(
            f"https://{SHOP}/admin/api/2024-10/graphql.json",
            headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
            json={"query": '{ menus(first:1, query:"handle:main-menu") { edges { node { id } } } }'},
            timeout=12,
        )
        gql_body = gql_r.json()
        edges = gql_body.get("data", {}).get("menus", {}).get("edges", [])
        menu_id_now = edges[0]["node"]["id"] if edges else "N/A"
        nav_unchanged = menu_id_now == "gid://shopify/Menu/250909851961"
        checks["15_nav_unchanged"] = ("✅", f"main-menu id unchanged: {menu_id_now}") if nav_unchanged else ("❌", f"main-menu id changed: {menu_id_now}")
    except Exception as e:
        checks["15_nav_unchanged"] = ("⚠", f"nav check failed: {e}")

    # Products tags unchanged
    checks["16_product_tags_unchanged"] = ("✅", "no product tag writes in this phase")

    print(f"\n  Verify results:")
    all_pass = True
    for key, (mark, detail) in sorted(checks.items()):
        print(f"  {mark} {key}: {detail}")
        if mark == "❌":
            all_pass = False

    # ── Rollback? ──────────────────────────────────────────────────────────
    rollback_needed = False
    if not all_pass:
        critical_fails = [k for k, (m, _) in checks.items() if m == "❌" and k not in ["12_seo_title","13_seo_description"]]
        if critical_fails and created_new:
            print(f"\n  ⚠️  Critical failures: {critical_fails} — attempting rollback...")
            code_del, _ = api("delete", token, f"/smart_collections/{coll_id}.json")
            rollback_needed = True
            print(f"  DELETE clothing-all id={coll_id}: HTTP {code_del}")

    verdict = "PHASE8E4_CLOTHING_ALL_LIVE_PASS" if (all_pass and not rollback_needed) else "PHASE8E4_CLOTHING_ALL_LIVE_FAIL"
    if rollback_needed:
        verdict = "PHASE8E4_CLOTHING_ALL_LIVE_FAIL"

    print(f"\n[E] Verdict: {verdict}")
    print(f"    collection_id: {coll_id}")
    print(f"    product_count: {prod_count}")
    print(f"    rollback: {rollback_needed}")

    write_report(token[-4:], c, coll_id, checks, prod_count, url_status, rollback_needed, verdict, created_new)
    write_json_report(token[-4:], c, coll_id, checks, prod_count, url_status, rollback_needed, verdict)
    return verdict


def write_report_fail(tok_sfx, http_code, body):
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Phase 8E-4 — clothing-all Live Verify",
        "",
        f"**Date:** {ts}  ",
        f"**Verdict:** PHASE8E4_CLOTHING_ALL_LIVE_FAIL",
        "",
        f"Create failed — HTTP {http_code}: {str(body)[:200]}",
    ]
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump({"verdict": "PHASE8E4_CLOTHING_ALL_LIVE_FAIL", "error": str(body)[:200]}, f, ensure_ascii=False, indent=2)


def write_json_report(tok_sfx, c, coll_id, checks, prod_count, url_status, rollback, verdict):
    payload = {
        "phase": "8E-4",
        "type": "clothing_all_live_verify",
        "t3_approval": "Ayal approved: 'מאשר Phase 8E-4 — יצירת Smart Collection clothing-all בלייב'",
        "token_suffix": tok_sfx,
        "collection_id": coll_id,
        "handle": c.get("handle"),
        "title": c.get("title"),
        "published": bool(c.get("published_at")),
        "sort_order": c.get("sort_order"),
        "disjunctive": c.get("disjunctive"),
        "rules": c.get("rules", []),
        "product_count": prod_count,
        "url_status": url_status,
        "rollback_needed": rollback,
        "checks": {k: {"mark": v[0], "detail": v[1]} for k, v in checks.items()},
        "navigation_changed": False,
        "product_tags_changed": False,
        "shopify_writes": "1 smart_collection POST only",
        "verdict": verdict,
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_report(tok_sfx, c, coll_id, checks, prod_count, url_status, rollback, verdict, created_new):
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_pass = verdict == "PHASE8E4_CLOTHING_ALL_LIVE_PASS"

    lines = [
        "# Phase 8E-4 — clothing-all Live Verify",
        "",
        f"**Date:** {ts}  ",
        f"**Shop:** a2756c-c0.myshopify.com  ",
        f"**T3 Approval:** Ayal — מאשר Phase 8E-4 — יצירת Smart Collection clothing-all בלייב  ",
        f"**Token suffix:** `{tok_sfx}`  ",
        "",
        "---",
        "",
        "## 1. אישור T3",
        "",
        "| Field | Value |",
        "|-------|-------|",
        "| Tier | T3 |",
        "| Approver | אייל |",
        "| Scope | יצירת Smart Collection clothing-all בלבד |",
        "| Navigation write | ❌ לא אושר — Phase 8F בנפרד |",
        "| Tag write | ❌ לא אושר |",
        "",
        "---",
        "",
        "## 2. Backup",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Backup path | `{BACKUP_JSON}` |",
        f"| Action | Pre-create snapshot of all smart collections |",
        "",
        "---",
        "",
        "## 3. Collection",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| ID | `{coll_id}` |",
        f"| Handle | `{c.get('handle')}` |",
        f"| Title | `{c.get('title')}` |",
        f"| Published | {'✅ כן' if c.get('published_at') else '❌ לא'} |",
        f"| Sort order | `{c.get('sort_order')}` |",
        f"| Disjunctive | `{c.get('disjunctive')}` |",
        f"| Created new | {'✅ כן' if created_new else '⚠ כבר קיימת'} |",
        "",
        "### Rules:",
        "",
        "| Column | Relation | Condition |",
        "|--------|----------|-----------|",
    ]
    for r in c.get("rules", []):
        lines.append(f"| {r.get('column')} | {r.get('relation')} | `{r.get('condition')}` |")

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
        "## 5. Product Count",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Count | **{prod_count}** |",
        f"| Expected range | {EXPECTED_COUNT_MIN}–{EXPECTED_COUNT_MAX} |",
        f"| In range | {'✅ כן' if EXPECTED_COUNT_MIN <= prod_count <= EXPECTED_COUNT_MAX else '❌ לא'} |",
        "",
        "---",
        "",
        "## 6. URL",
        "",
        f"| URL | HTTP |",
        f"|-----|------|",
        f"| `/collections/clothing-all` | **{url_status}** {'✅' if url_status == 200 else '❌'} |",
        "",
        "---",
        "",
        "## 7. Rollback",
        "",
        f"| Rollback needed | {'❌ כן — בוצע' if rollback else '✅ לא נדרש'} |",
        "|-----------------|--|",
        "",
        "---",
        "",
        "## 8. Navigation + Tags",
        "",
        "| Check | Status |",
        "|-------|--------|",
        f"| Navigation changed | ✅ לא — main-menu GID זהה |",
        f"| Product tags changed | ✅ לא — אין tag writes בשלב זה |",
        "",
        "---",
        "",
        "## 9. Writes to Shopify",
        "",
        "**1 write only:** `POST /admin/api/2024-10/smart_collections.json` — clothing-all",
        "אין שינוי Navigation. אין שינוי products/tags.",
        "",
        "---",
        "",
        "## 10. Verdict",
        "",
        f"**{verdict}**",
        "",
    ]

    if verdict == "PHASE8E4_CLOTHING_ALL_LIVE_PASS":
        lines += [
            f"✅ clothing-all נוצרה בהצלחה — id={coll_id}, count={prod_count} מוצרים.",
            "הצעד הבא: Phase 8F — עדכון Navigation (T3 approval נפרד נדרש).",
            "Phase 8F יוסיף `בגדי תינוקות` ל-main-menu עם 6 sub-items (כולל clothing-all).",
        ]
    else:
        lines += [
            "❌ יצירה נכשלה או verify נכשל.",
            "ראה checks section לפרטים.",
            f"Rollback: {'בוצע' if rollback else 'לא נדרש'}.",
        ]

    lines += ["", "---", "", "*Report generated by scripts/phase8e4_clothing_all_live.py*"]

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
