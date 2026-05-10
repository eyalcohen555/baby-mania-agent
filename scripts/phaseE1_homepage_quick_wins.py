"""
Phase E1 — Homepage Quick Wins + Sticky Reality Audit
T1 APPROVED — settings only (no Liquid/CSS/JS changes)
Date: 2026-05-10

Changes (Part A — T1 only):
  E1-1a: featured_collection products_to_show 25→8
  E1-1b: featured_collection_FXYxk4 products_to_show 25→8
  E1-2:  Disable image_banner_WY4jhi (blank — all blocks disabled)
  E1-3:  Disable rich_text_bWQ9mf (empty heading)
  E1-4:  Rename rich_text_xKGEmA heading "הנמכרים ביותר" → "מוצר השבוע"
  E1-5:  Add bm-trust-badges section (if schema permits, T1 only)
  E1-6:  show_rating — read-only check, no change without review evidence

Part B: Sticky add-to-cart reality audit (READ-ONLY)

Usage:
  python scripts/phaseE1_homepage_quick_wins.py --mode=dry-run
  python scripts/phaseE1_homepage_quick_wins.py --mode=live
"""
import argparse, json, sys, time, os, re, copy
import requests

sys.stdout.reconfigure(encoding="utf-8")

# ─── Config ────────────────────────────────────────────────────────────────────
SHOP         = "a2756c-c0.myshopify.com"
API_VER      = "2024-10"
BASE         = f"https://{SHOP}/admin/api/{API_VER}"
TOKEN_URL    = f"https://{SHOP}/admin/oauth/access_token"
STOREFRONT   = "https://www.babymania-il.com"
THEME_ID     = 183668179257
TEMPLATE_KEY = "templates/index.json"

DESKTOP_ENV  = r"C:\Users\3024e\Desktop\shopify-token\.env"
PROJECT_ENV  = r"C:\Projects\baby-mania-agent\.env"

OUTPUT_DIR   = "output/tags"
DOCS_DIR     = "docs/organic"

# ─── Section IDs (from Phase D audit + phaseD_index.json) ─────────────────────
SEC_FEAT_COLL_1  = "featured_collection"          # בגדי-חורף  products_to_show=25
SEC_FEAT_COLL_2  = "featured_collection_FXYxk4"   # נעליים     products_to_show=25
SEC_IMG_BANNER   = "image_banner_WY4jhi"           # blank — all blocks disabled
SEC_RICH_EMPTY   = "rich_text_bWQ9mf"             # empty heading block
SEC_RICH_DUP     = "rich_text_xKGEmA"             # pos 6 — "הנמכרים ביותר" (duplicate)
RICH_DUP_BLOCK   = "heading_fwngai"               # block ID inside rich_text_xKGEmA
HERO_SECTION_ID  = "bm_video_hero_CRzC6Q"

TRUST_SECTION_TYPE = "bm-trust-badges"
TRUST_SECTION_KEY  = "sections/bm-trust-badges.liquid"
NEW_TRUST_SEC_ID   = "bm_trust_badges_E1_2026"

TRUST_BADGE_TEXTS = [
    "משלוח מהיר לכל הארץ",
    "תשלום מאובטח",
    "החזרות עד 14 יום",
    "שירות לקוחות אישי",
]

DUP_HEADING_FROM = "הנמכרים ביותר"
DUP_HEADING_TO   = "מוצר השבוע"

PRODUCT_TEMPLATES = [
    "templates/product.json",
    "templates/product.clothing.json",
    "templates/product.shoes.json",
    "templates/product.accessories.json",
    "templates/product.reborn.json",
    "templates/product.easy-sleep.json",
    "templates/product.tempio.json",
    "templates/product.test-template.json",
    "templates/product.test.json",
]


# ─── Auth ──────────────────────────────────────────────────────────────────────
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


def get_token():
    for path in [DESKTOP_ENV, PROJECT_ENV]:
        env = load_env(path)
        cid  = env.get("SHOPIFY_CLIENT_ID") or env.get("CLIENT_ID")
        csec = env.get("SHOPIFY_CLIENT_SECRET") or env.get("CLIENT_SECRET")
        if cid and csec:
            r = requests.post(
                TOKEN_URL,
                data={"grant_type": "client_credentials", "client_id": cid, "client_secret": csec},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15,
            )
            r.raise_for_status()
            return r.json()["access_token"]
    raise RuntimeError("No credentials found in DESKTOP_ENV or PROJECT_ENV")


def make_session(token):
    s = requests.Session()
    s.headers.update({"X-Shopify-Access-Token": token, "Content-Type": "application/json"})
    return s


# ─── Theme API helpers ─────────────────────────────────────────────────────────
def get_asset(session, key):
    r = session.get(
        f"{BASE}/themes/{THEME_ID}/assets.json",
        params={"asset[key]": key},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()["asset"]["value"]


def put_asset(session, key, value):
    r = session.put(
        f"{BASE}/themes/{THEME_ID}/assets.json",
        json={"asset": {"key": key, "value": value}},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


# ─── Trust badge schema parser ─────────────────────────────────────────────────
def extract_schema(liquid_source):
    """Extract JSON schema from {% schema %}...{% endschema %} block."""
    m = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}', liquid_source, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def find_trust_block_type(schema):
    """Return block type name that has a text/title/label setting, or None."""
    for block in schema.get("blocks", []):
        for setting in block.get("settings", []):
            if setting.get("type") in ("text", "textarea", "richtext", "inline_richtext") \
               and setting.get("id") in ("text", "title", "label", "heading", "body"):
                return block.get("type"), setting.get("id")
    return None, None


def build_trust_section(block_type, text_field):
    """Build the section entry for templates/index.json."""
    blocks = {}
    block_order = []
    for i, badge_text in enumerate(TRUST_BADGE_TEXTS):
        bid = f"trust_badge_{i}"
        blocks[bid] = {
            "type": block_type,
            "settings": {text_field: badge_text}
        }
        block_order.append(bid)
    return {
        "type": TRUST_SECTION_TYPE,
        "blocks": blocks,
        "block_order": block_order,
        "settings": {}
    }


# ─── Template mutation ─────────────────────────────────────────────────────────
def compute_changes(template, trust_section_entry=None):
    """
    Compute all T1 changes.
    Returns: (modified_template, changes_list) — does NOT write anything.
    """
    modified = copy.deepcopy(template)
    sections = modified["sections"]
    order    = modified["order"]
    changes  = []

    # E1-1a: products_to_show featured_collection
    sec = sections.get(SEC_FEAT_COLL_1, {})
    old = sec.get("settings", {}).get("products_to_show")
    if old == 25:
        sections[SEC_FEAT_COLL_1]["settings"]["products_to_show"] = 8
        changes.append({"id": "E1-1a", "section": SEC_FEAT_COLL_1,
                         "field": "settings.products_to_show", "from": 25, "to": 8, "status": "APPLIED"})
    else:
        changes.append({"id": "E1-1a", "section": SEC_FEAT_COLL_1,
                         "field": "settings.products_to_show", "current": old,
                         "status": "SKIPPED" if old != 25 else "NOT_FOUND"})

    # E1-1b: products_to_show featured_collection_FXYxk4
    sec = sections.get(SEC_FEAT_COLL_2, {})
    old = sec.get("settings", {}).get("products_to_show")
    if old == 25:
        sections[SEC_FEAT_COLL_2]["settings"]["products_to_show"] = 8
        changes.append({"id": "E1-1b", "section": SEC_FEAT_COLL_2,
                         "field": "settings.products_to_show", "from": 25, "to": 8, "status": "APPLIED"})
    else:
        changes.append({"id": "E1-1b", "section": SEC_FEAT_COLL_2,
                         "field": "settings.products_to_show", "current": old,
                         "status": "SKIPPED" if old is not None else "NOT_FOUND"})

    # E1-2: Disable image_banner_WY4jhi
    if SEC_IMG_BANNER in sections:
        old_d = sections[SEC_IMG_BANNER].get("disabled", False)
        sections[SEC_IMG_BANNER]["disabled"] = True
        status = "ALREADY_DISABLED" if old_d is True else "APPLIED"
        changes.append({"id": "E1-2", "section": SEC_IMG_BANNER,
                         "field": "disabled", "from": old_d, "to": True, "status": status})
    else:
        changes.append({"id": "E1-2", "section": SEC_IMG_BANNER, "status": "NOT_FOUND"})

    # E1-3: Disable rich_text_bWQ9mf
    if SEC_RICH_EMPTY in sections:
        old_d = sections[SEC_RICH_EMPTY].get("disabled", False)
        sections[SEC_RICH_EMPTY]["disabled"] = True
        status = "ALREADY_DISABLED" if old_d is True else "APPLIED"
        changes.append({"id": "E1-3", "section": SEC_RICH_EMPTY,
                         "field": "disabled", "from": old_d, "to": True, "status": status})
    else:
        changes.append({"id": "E1-3", "section": SEC_RICH_EMPTY, "status": "NOT_FOUND"})

    # E1-4: Rename duplicate heading
    if SEC_RICH_DUP in sections and RICH_DUP_BLOCK in sections[SEC_RICH_DUP].get("blocks", {}):
        old_h = sections[SEC_RICH_DUP]["blocks"][RICH_DUP_BLOCK]["settings"].get("heading", "")
        if old_h == DUP_HEADING_FROM:
            sections[SEC_RICH_DUP]["blocks"][RICH_DUP_BLOCK]["settings"]["heading"] = DUP_HEADING_TO
            changes.append({"id": "E1-4", "section": SEC_RICH_DUP,
                             "block": RICH_DUP_BLOCK, "field": "blocks.heading_fwngai.settings.heading",
                             "from": old_h, "to": DUP_HEADING_TO, "status": "APPLIED"})
        else:
            changes.append({"id": "E1-4", "section": SEC_RICH_DUP,
                             "field": "blocks.heading_fwngai.settings.heading",
                             "current": old_h, "expected": DUP_HEADING_FROM,
                             "status": "SKIPPED_UNEXPECTED_VALUE"})
    else:
        changes.append({"id": "E1-4", "section": SEC_RICH_DUP, "status": "NOT_FOUND"})

    # E1-5: Trust badges
    if trust_section_entry is not None:
        if NEW_TRUST_SEC_ID in sections:
            changes.append({"id": "E1-5", "section": NEW_TRUST_SEC_ID,
                             "status": "ALREADY_EXISTS", "note": "Trust section already in template"})
        else:
            sections[NEW_TRUST_SEC_ID] = trust_section_entry
            # Insert into order after hero
            hero_pos = order.index(HERO_SECTION_ID) if HERO_SECTION_ID in order else -1
            if hero_pos >= 0:
                order.insert(hero_pos + 1, NEW_TRUST_SEC_ID)
            else:
                order.insert(1, NEW_TRUST_SEC_ID)
            changes.append({"id": "E1-5", "section": NEW_TRUST_SEC_ID,
                             "status": "APPLIED", "badges": TRUST_BADGE_TEXTS,
                             "inserted_after": HERO_SECTION_ID})
    else:
        changes.append({"id": "E1-5", "status": "BLOCKED",
                         "reason": "bm-trust-badges.liquid not found or schema incompatible"})

    # E1-6: show_rating (read-only check, no change)
    for sid in [SEC_FEAT_COLL_1, SEC_FEAT_COLL_2]:
        sr = sections.get(sid, {}).get("settings", {}).get("show_rating")
        changes.append({"id": "E1-6", "section": sid, "show_rating_current": sr,
                         "status": "NO_CHANGE",
                         "reason": "Cannot verify product review count without app API — leaving disabled"})

    return modified, changes


# ─── Verify ───────────────────────────────────────────────────────────────────
def verify_template(session, expected_changes):
    """Fetch live template and verify each change."""
    raw = get_asset(session, TEMPLATE_KEY)
    live = json.loads(raw)
    sections = live["sections"]
    results = []

    for c in expected_changes:
        cid    = c["id"]
        sec_id = c.get("section", "")
        status = c.get("status", "")

        if status in ("SKIPPED", "BLOCKED", "NOT_FOUND", "NO_CHANGE",
                      "SKIPPED_UNEXPECTED_VALUE", "ALREADY_DISABLED", "ALREADY_EXISTS"):
            results.append({"id": cid, "section": sec_id, "verdict": "SKIP_OK",
                             "note": status})
            continue

        if cid in ("E1-1a", "E1-1b"):
            actual = sections.get(sec_id, {}).get("settings", {}).get("products_to_show")
            results.append({"id": cid, "section": sec_id,
                             "expected": 8, "actual": actual,
                             "verdict": "PASS" if actual == 8 else "FAIL"})

        elif cid in ("E1-2", "E1-3"):
            actual_d = sections.get(sec_id, {}).get("disabled")
            results.append({"id": cid, "section": sec_id,
                             "expected_disabled": True, "actual_disabled": actual_d,
                             "verdict": "PASS" if actual_d is True else "FAIL"})

        elif cid == "E1-4":
            actual_h = (sections.get(sec_id, {})
                        .get("blocks", {})
                        .get(RICH_DUP_BLOCK, {})
                        .get("settings", {})
                        .get("heading", ""))
            results.append({"id": cid, "section": sec_id,
                             "expected": DUP_HEADING_TO, "actual": actual_h,
                             "verdict": "PASS" if actual_h == DUP_HEADING_TO else "FAIL"})

        elif cid == "E1-5":
            present = NEW_TRUST_SEC_ID in sections
            in_order = NEW_TRUST_SEC_ID in live.get("order", [])
            results.append({"id": cid, "section": sec_id,
                             "in_sections": present, "in_order": in_order,
                             "verdict": "PASS" if (present and in_order) else "FAIL"})

    all_verdicts = [r["verdict"] for r in results if r["verdict"] not in ("SKIP_OK",)]
    overall = "PASS" if all(v == "PASS" for v in all_verdicts) else "FAIL"
    return {"overall": overall, "items": results}


# ─── Part B: Sticky reality audit ─────────────────────────────────────────────
def sticky_audit(session):
    """Full read-only audit of sticky add-to-cart across all product templates."""
    results = []

    for tkey in PRODUCT_TEMPLATES:
        entry = {"template": tkey}
        try:
            raw = get_asset(session, tkey)
            tmpl = json.loads(raw)
        except Exception as e:
            entry.update({"status": "FETCH_ERROR", "error": str(e)})
            results.append(entry)
            continue

        secs = tmpl.get("sections", {})

        # Check sticky bar presence
        has_sticky = any(
            s.get("type") == "bm-sticky-bar"
            for s in secs.values()
        )

        # Find main-product section
        main_product_sec = None
        main_product_enabled = None
        for sid, sobj in secs.items():
            if sobj.get("type") == "main-product":
                main_product_sec = sid
                main_product_enabled = not sobj.get("disabled", False)
                break

        # Check product-form__buttons reachability
        # If main-product is disabled → .product-form__buttons won't be in DOM
        form_buttons_in_dom = main_product_enabled if main_product_sec else None

        if not has_sticky:
            sticky_verdict = "BROKEN_NO_SECTION"
        elif main_product_sec is None:
            sticky_verdict = "UNKNOWN_NO_MAIN_PRODUCT"
        elif not main_product_enabled:
            sticky_verdict = "BROKEN_MAIN_PRODUCT_DISABLED"
        else:
            sticky_verdict = "LIKELY_WORKING"

        entry.update({
            "has_sticky_bar": has_sticky,
            "main_product_section": main_product_sec,
            "main_product_enabled": main_product_enabled,
            "form_buttons_expected_in_dom": form_buttons_in_dom,
            "sticky_verdict": sticky_verdict,
        })
        results.append(entry)
        time.sleep(0.3)

    return results


def storefront_clothing_check(session):
    """
    Fetch a live clothing product (template_suffix=clothing) and check
    whether .product-form__buttons and bm-sticky-bar exist in storefront HTML.
    """
    # Get a clothing product handle
    r = session.get(
        f"{BASE}/products.json",
        params={"limit": 10, "template_suffix": "clothing"},
        timeout=15,
    )
    products = r.json().get("products", []) if r.status_code == 200 else []

    if not products:
        # Fallback: get any product from בגדי-בנות collection
        r2 = session.get(
            f"{BASE}/collections/products.json",
            params={"limit": 5},
            timeout=15,
        )
        # Try direct products list
        r3 = session.get(
            f"{BASE}/products.json",
            params={"limit": 5, "collection_id": "בגדי-בנות"},
            timeout=15,
        )
        products = r3.json().get("products", []) if r3.status_code == 200 else []

    if not products:
        return {"status": "NO_PRODUCT_FOUND", "reason": "Could not find a clothing product via API"}

    product = products[0]
    handle   = product.get("handle", "")
    pid      = product.get("id")
    title    = product.get("title", "")
    tsuffix  = product.get("template_suffix", "")

    # Fetch storefront HTML
    url = f"{STOREFRONT}/products/{handle}"
    try:
        resp = requests.get(url, timeout=20,
                            headers={"User-Agent": "BabyMania-E1-Audit/1.0"})
        html = resp.text
    except Exception as e:
        return {"status": "FETCH_ERROR", "url": url, "error": str(e)}

    has_sticky_in_html   = "bm-sticky-bar" in html
    has_form_buttons     = "product-form__buttons" in html
    has_product_form     = "product-form" in html
    has_sticky_observer  = "IntersectionObserver" in html
    # Check if sticky is hidden via aria-hidden (initial state)
    sticky_aria_hidden   = 'aria-hidden="true"' in html and "bm-sticky-bar" in html

    return {
        "status": "OK",
        "product_id": pid,
        "product_title": title,
        "product_handle": handle,
        "template_suffix": tsuffix,
        "url": url,
        "http_status": resp.status_code,
        "has_sticky_bar_in_html": has_sticky_in_html,
        "has_product_form__buttons": has_form_buttons,
        "has_product_form": has_product_form,
        "has_intersection_observer": has_sticky_observer,
        "sticky_starts_hidden": sticky_aria_hidden,
        "analysis": {
            "sticky_section_rendered": has_sticky_in_html,
            "form_buttons_in_dom": has_form_buttons,
            "observer_attached": has_sticky_observer and has_form_buttons,
            "issue": None if has_form_buttons else ".product-form__buttons NOT FOUND IN HTML"
        }
    }


def check_product_reviews(session):
    """Check if any products have review metafields (proxy for show_rating)."""
    r = session.get(
        f"{BASE}/products.json",
        params={"limit": 5},
        timeout=15,
    )
    if r.status_code != 200:
        return {"status": "API_ERROR", "code": r.status_code}

    products = r.json().get("products", [])
    if not products:
        return {"status": "NO_PRODUCTS"}

    pid = products[0]["id"]
    r2  = session.get(
        f"{BASE}/products/{pid}/metafields.json",
        params={"limit": 25},
        timeout=15,
    )
    if r2.status_code != 200:
        return {"status": "METAFIELDS_ERROR", "code": r2.status_code}

    mf = r2.json().get("metafields", [])
    review_fields = [m for m in mf if "review" in m.get("namespace", "").lower()
                     or "review" in m.get("key", "").lower()]

    return {
        "status": "OK",
        "product_sample_id": pid,
        "metafields_count": len(mf),
        "review_metafields": review_fields,
        "has_reviews": len(review_fields) > 0
    }


# ─── Output writers ────────────────────────────────────────────────────────────
def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote: {path}")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  Wrote: {path}")


def format_dry_run_md(changes, backup_note, trust_schema_note):
    lines = [
        "# Phase E1 — Dry Run Report",
        f"**Date:** 2026-05-10 | **Mode:** DRY-RUN | **Writes:** NONE",
        "",
        backup_note,
        "",
        "## Planned Changes",
        "",
        "| ID | Section | Field | From | To | Status |",
        "|----|---------|-------|------|----|--------|",
    ]
    for c in changes:
        cid    = c.get("id", "")
        sec    = c.get("section", "")
        field  = c.get("field", "")
        frm    = c.get("from", c.get("current", "—"))
        to     = c.get("to", "—")
        status = c.get("status", "")
        lines.append(f"| {cid} | `{sec}` | `{field}` | {frm} | {to} | {status} |")

    lines += ["", f"**Trust badge schema:** {trust_schema_note}", "",
              "**No writes performed in dry-run mode.**"]
    return "\n".join(lines)


def format_verify_md(verify_result):
    lines = [
        "# Phase E1 — Verify Report",
        f"**Date:** 2026-05-10 | **Mode:** LIVE",
        f"**Overall:** {verify_result['overall']}",
        "",
        "| ID | Section | Expected | Actual | Verdict |",
        "|----|---------|----------|--------|---------|",
    ]
    for r in verify_result["items"]:
        cid     = r.get("id", "")
        sec     = r.get("section", "")
        exp     = r.get("expected", r.get("expected_disabled", r.get("in_sections", "—")))
        act     = r.get("actual", r.get("actual_disabled", r.get("in_sections", "—")))
        verdict = r.get("verdict", "")
        lines.append(f"| {cid} | `{sec}` | {exp} | {act} | **{verdict}** |")
    return "\n".join(lines)


def format_sticky_md(template_results, storefront_check, scope, root_cause, confidence):
    lines = [
        "# Phase E1 — Sticky Add-to-Cart Reality Audit",
        f"**Date:** 2026-05-10 | **Mode:** READ-ONLY",
        f"**STICKY_SCOPE:** {scope}",
        f"**ROOT_CAUSE_CONFIDENCE:** {confidence}",
        "",
        "## Template Audit",
        "",
        "| Template | Has Sticky | Main-Product | Enabled | form__buttons in DOM | Verdict |",
        "|----------|-----------|-------------|---------|---------------------|---------|",
    ]
    for t in template_results:
        tpl   = t.get("template", "").replace("templates/", "")
        hs    = "✅" if t.get("has_sticky_bar") else "❌"
        mp    = t.get("main_product_section") or "—"
        en    = "✅" if t.get("main_product_enabled") else ("❌" if t.get("main_product_enabled") is False else "—")
        fbd   = "✅" if t.get("form_buttons_expected_in_dom") else ("❌" if t.get("form_buttons_expected_in_dom") is False else "—")
        verd  = t.get("sticky_verdict", t.get("status", "—"))
        lines.append(f"| {tpl} | {hs} | `{mp}` | {en} | {fbd} | {verd} |")

    lines += [""]

    # Storefront check
    lines += [
        "## Storefront HTML Check",
        "",
        f"**Product:** {storefront_check.get('product_title', '—')} (`{storefront_check.get('product_handle', '—')}`)",
        f"**Template suffix:** {storefront_check.get('template_suffix', '—')}",
        f"**URL:** {storefront_check.get('url', '—')}",
        f"**HTTP status:** {storefront_check.get('http_status', '—')}",
        "",
        f"- `bm-sticky-bar` in HTML: {'✅' if storefront_check.get('has_sticky_bar_in_html') else '❌'}",
        f"- `.product-form__buttons` in HTML: {'✅' if storefront_check.get('has_product_form__buttons') else '❌'}",
        f"- `product-form` in HTML: {'✅' if storefront_check.get('has_product_form') else '❌'}",
        f"- `IntersectionObserver` in HTML: {'✅' if storefront_check.get('has_intersection_observer') else '❌'}",
        f"- Sticky starts hidden (aria-hidden=true): {'✅' if storefront_check.get('sticky_starts_hidden') else '⚠️ NO'}",
        "",
        "### Analysis",
        f"**Issue:** {storefront_check.get('analysis', {}).get('issue', 'None found')}",
        "",
    ]

    lines += [
        "## Root Cause Summary",
        "",
        f"**LIKELY_ROOT_CAUSE:** {root_cause}",
        "",
        "## Recommended Fix Options",
        "",
        "| Tier | Fix | Scope |",
        "|------|-----|-------|",
        "| T2 | Edit bm-sticky-bar.liquid: add fallback selector (.product-form, form[action*='/cart/add']) | Liquid code — needs T2 approval |",
        "| T3 | Enable main-product section on product.easy-sleep.json + product.tempio.json | Template structure — needs T3 approval |",
        "",
        "**Note:** If .product-form__buttons missing on clothing pages → root cause is selector mismatch not template disable. Requires deeper Dawn section inspection (T2).",
    ]
    return "\n".join(lines)


def format_rollback_md(backup_note):
    return f"""# Phase E1 — Rollback Plan
**Date:** 2026-05-10 | **Mode:** LIVE

## Rollback Scope
All changes are to `templates/index.json` only (homepage template settings).
No Liquid/CSS/JS files were modified.

## How to Rollback

### Option A — Restore via API (preferred)
1. Read `output/tags/phaseE1-homepage-quick-wins-backup.json`
2. Extract the `template_value` field
3. PUT to theme {THEME_ID} asset `templates/index.json`

### Option B — Manual restore via Shopify Customize
Reverse each change individually:
- E1-1a/b: Restore products_to_show = 25 on both featured-collection sections
- E1-2: Re-enable image_banner_WY4jhi section
- E1-3: Re-enable rich_text_bWQ9mf section
- E1-4: Restore heading in rich_text_xKGEmA from "מוצר השבוע" → "הנמכרים ביותר"
- E1-5: Remove bm_trust_badges_E1_2026 section

## Backup
{backup_note}
"""


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run", "live"], required=True)
    args = parser.parse_args()

    print(f"\n=== Phase E1 | mode={args.mode} | {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    # Auth
    print("Auth...")
    token   = get_token()
    session = make_session(token)
    print("  Token OK\n")

    # Fetch current template
    print("Fetching templates/index.json...")
    raw_template = get_asset(session, TEMPLATE_KEY)
    template     = json.loads(raw_template)
    print(f"  Sections: {len(template['sections'])} | Order: {len(template['order'])}\n")

    # Fetch trust badge schema
    print("Fetching bm-trust-badges.liquid...")
    trust_section_entry = None
    trust_schema_note   = ""
    try:
        trust_liquid = get_asset(session, TRUST_SECTION_KEY)
        schema       = extract_schema(trust_liquid)
        if schema:
            block_type, text_field = find_trust_block_type(schema)
            if block_type and text_field:
                trust_section_entry = build_trust_section(block_type, text_field)
                trust_schema_note = f"FOUND — block_type='{block_type}' text_field='{text_field}'"
                print(f"  Trust schema: {trust_schema_note}")
            else:
                trust_schema_note = "FOUND but no compatible text block type"
                print(f"  Trust schema: {trust_schema_note}")
        else:
            trust_schema_note = "Schema parse failed"
            print(f"  Trust schema: {trust_schema_note}")
    except Exception as e:
        trust_schema_note = f"FETCH_ERROR: {e}"
        print(f"  Trust schema: {trust_schema_note}")

    # Check reviews
    print("Checking product reviews (show_rating)...")
    review_check = check_product_reviews(session)
    print(f"  Reviews: has_reviews={review_check.get('has_reviews', 'unknown')}\n")

    # Compute changes
    modified_template, changes = compute_changes(template, trust_section_entry)

    # Backup
    backup_data = {
        "date": "2026-05-10",
        "mode": args.mode,
        "theme_id": THEME_ID,
        "template_key": TEMPLATE_KEY,
        "template_value": raw_template,
        "review_check": review_check,
    }
    write_json(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-backup.json", backup_data)
    backup_note = f"Backup saved: output/tags/phaseE1-homepage-quick-wins-backup.json"

    # Dry-run outputs
    dry_run_data = {
        "date": "2026-05-10",
        "mode": args.mode,
        "changes": changes,
        "trust_schema": trust_schema_note,
        "review_check_summary": review_check,
    }
    write_json(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-dry-run.json", dry_run_data)
    write_text(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-dry-run.md",
               format_dry_run_md(changes, backup_note, trust_schema_note))
    write_text(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-rollback-plan.md",
               format_rollback_md(backup_note))

    print("\n=== Planned changes ===")
    for c in changes:
        print(f"  {c['id']} {c['section']:35s} → {c['status']}")

    if args.mode == "dry-run":
        print("\nDRY-RUN complete. No writes to Shopify.")

        # Part B: Sticky audit (run in both modes)
        print("\n=== Part B: Sticky Audit ===")
        tmpl_results = sticky_audit(session)
        sf_check     = storefront_clothing_check(session)

        # Determine scope and root cause
        broken = [t for t in tmpl_results if "BROKEN" in t.get("sticky_verdict", "")]
        working = [t for t in tmpl_results if t.get("sticky_verdict") == "LIKELY_WORKING"]
        scope   = "all_products" if len(broken) > len(working) else "special_templates_only"

        if not sf_check.get("has_product_form__buttons"):
            root_cause = ".product-form__buttons MISSING from clothing storefront HTML — selector mismatch or Dawn version issue"
            confidence = "HIGH"
            scope = "all_products"
        elif broken:
            root_cause = f"main-product disabled on: {[t['template'] for t in broken if 'DISABLED' in t.get('sticky_verdict', '')]}"
            confidence = "HIGH"
        else:
            root_cause = "Unknown — sticky section present and form buttons in DOM, timing or JS issue"
            confidence = "LOW"

        write_json(f"{OUTPUT_DIR}/phaseE1-sticky-reality-audit.json", {
            "date": "2026-05-10",
            "mode": "READ-ONLY",
            "sticky_scope": scope,
            "root_cause_confidence": confidence,
            "likely_root_cause": root_cause,
            "template_results": tmpl_results,
            "storefront_check": sf_check,
            "review_check": review_check,
        })
        write_text(f"{OUTPUT_DIR}/phaseE1-sticky-reality-audit.md",
                   format_sticky_md(tmpl_results, sf_check, scope, root_cause, confidence))

        return

    # ── LIVE MODE ────────────────────────────────────────────────────────────────
    print("\nLIVE MODE — Writing template to Shopify...")
    applied_changes = [c for c in changes if c["status"] in ("APPLIED",)]
    print(f"  Applying {len(applied_changes)} changes...")

    new_template_str = json.dumps(modified_template, ensure_ascii=False)
    put_asset(session, TEMPLATE_KEY, new_template_str)
    print("  PUT templates/index.json — OK\n")

    # Verify
    print("Verifying...")
    time.sleep(2)
    verify_result = verify_template(session, changes)
    print(f"  Verify overall: {verify_result['overall']}")
    for item in verify_result["items"]:
        print(f"    {item['id']} {item.get('section', ''):35s} → {item['verdict']}")

    write_json(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-verify.json", verify_result)
    write_text(f"{OUTPUT_DIR}/phaseE1-homepage-quick-wins-verify.md",
               format_verify_md(verify_result))

    # Part B: Sticky audit
    print("\n=== Part B: Sticky Audit ===")
    tmpl_results = sticky_audit(session)
    sf_check     = storefront_clothing_check(session)

    broken  = [t for t in tmpl_results if "BROKEN" in t.get("sticky_verdict", "")]
    working = [t for t in tmpl_results if t.get("sticky_verdict") == "LIKELY_WORKING"]
    scope   = "all_products" if len(broken) > len(working) else "special_templates_only"

    if not sf_check.get("has_product_form__buttons"):
        root_cause = ".product-form__buttons MISSING from clothing storefront HTML — selector mismatch or Dawn version issue"
        confidence = "HIGH"
        scope = "all_products"
    elif broken:
        root_cause = f"main-product disabled on: {[t['template'] for t in broken if 'DISABLED' in t.get('sticky_verdict', '')]}"
        confidence = "HIGH"
    else:
        root_cause = "Unknown — sticky section present and form buttons in DOM, timing or JS issue"
        confidence = "LOW"

    write_json(f"{OUTPUT_DIR}/phaseE1-sticky-reality-audit.json", {
        "date": "2026-05-10",
        "mode": "READ-ONLY",
        "sticky_scope": scope,
        "root_cause_confidence": confidence,
        "likely_root_cause": root_cause,
        "template_results": tmpl_results,
        "storefront_check": sf_check,
        "review_check": review_check,
    })
    write_text(f"{OUTPUT_DIR}/phaseE1-sticky-reality-audit.md",
               format_sticky_md(tmpl_results, sf_check, scope, root_cause, confidence))

    # Write main report
    all_applied = [c["id"] for c in changes if c["status"] == "APPLIED"]
    all_skip    = [c["id"] for c in changes if c["status"] not in ("APPLIED",)]
    overall_verdict = "PHASEE1_HOMEPAGE_QUICK_WINS_PASS" if verify_result["overall"] == "PASS" \
                      else "PHASEE1_HOMEPAGE_QUICK_WINS_PARTIAL"

    report_md = f"""# Phase E1 — Homepage Quick Wins Report
**Date:** 2026-05-10 | **Mode:** LIVE | **Tier:** T1
**Verdict:** {overall_verdict}

## Changes Applied
Applied: {all_applied}
Skipped/Blocked: {all_skip}

## Verify: {verify_result['overall']}
{format_verify_md(verify_result)}

## Sticky Audit
Scope: {scope}
Root cause confidence: {confidence}
Likely root cause: {root_cause}

## show_rating
Review metafields found: {review_check.get('has_reviews', 'unknown')}
Action: NO CHANGE — leaving show_rating disabled until reviews confirmed.

## Trust Badges
Schema note: {trust_schema_note}
"""
    write_text(f"{DOCS_DIR}/phaseE1-homepage-quick-wins-report.md", report_md)

    print(f"\n=== {overall_verdict} ===")


if __name__ == "__main__":
    main()
