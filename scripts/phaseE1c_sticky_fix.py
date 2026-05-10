"""
Phase E1c — Sticky Add-to-Cart Fix (DOM Timing Bug)
T2 approved by Ayal — 2026-05-10

File changed: sections/bm-sticky-bar.liquid (JS only — no HTML/CSS/schema)
Root cause:   Inline <script> runs before main-product section renders.
              querySelector('.product-form__buttons') = null → early return.
Fix:          Wrap observer setup in initStickyObserver() + readyState check.

Usage:
  python scripts/phaseE1c_sticky_fix.py --mode=dry-run
  python scripts/phaseE1c_sticky_fix.py --mode=live
"""
import argparse, json, sys, time, os, difflib
import requests

sys.stdout.reconfigure(encoding="utf-8")

SHOP         = "a2756c-c0.myshopify.com"
API_VER      = "2024-10"
BASE         = f"https://{SHOP}/admin/api/{API_VER}"
TOKEN_URL    = f"https://{SHOP}/admin/oauth/access_token"
STOREFRONT   = "https://www.babymania-il.com"
THEME_ID     = 183668179257
ASSET_KEY    = "sections/bm-sticky-bar.liquid"

DESKTOP_ENV  = r"C:\Users\3024e\Desktop\shopify-token\.env"
PROJECT_ENV  = r"C:\Projects\baby-mania-agent\.env"
OUTPUT_DIR   = "output/tags"
DOCS_DIR     = "docs/organic"

# ─── Verify targets ─────────────────────────────────────────────────────────────
VERIFY_PRODUCTS = [
    {"handle": "חליפת-תחרה-פרחונית-מורן",     "template": "clothing"},
    {"handle": "newborn-baby-winter-jacket-warm-hooded-infant-romper-thicken", "template": "clothing"},
]

# ─── The exact block to replace (must match live file character-for-character) ──
OLD_JS = """  // Watch the product form buttons container
  var target = document.querySelector('.product-form__buttons');
  if (!target) return;

  new IntersectionObserver(
    function (entries) {
      bar.setAttribute('aria-hidden', entries[0].isIntersecting ? 'true' : 'false');
    },
    { threshold: 0 }
  ).observe(target);"""

NEW_JS = """  // Fix: section renders before main-product in template order.
  // DOMContentLoaded ensures .product-form__buttons exists when observer attaches.
  function initStickyObserver() {
    var target = document.querySelector('.product-form__buttons')
              || document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)');
    if (!target) return;

    new IntersectionObserver(
      function (entries) {
        var vis = entries[0].isIntersecting;
        bar.setAttribute('aria-hidden', vis ? 'true' : 'false');
      },
      { threshold: 0.1 }
    ).observe(target);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyObserver);
  } else {
    initStickyObserver();
  }"""


# ─── Auth ───────────────────────────────────────────────────────────────────────
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
                data={"grant_type": "client_credentials",
                      "client_id": cid, "client_secret": csec},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15,
            )
            r.raise_for_status()
            return r.json()["access_token"]
    raise RuntimeError("No credentials found")


def make_session(token):
    s = requests.Session()
    s.headers.update({"X-Shopify-Access-Token": token,
                      "Content-Type": "application/json"})
    return s


# ─── Theme API ──────────────────────────────────────────────────────────────────
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


# ─── Patch logic ────────────────────────────────────────────────────────────────
def apply_patch(source):
    """Return patched source + metadata."""
    if OLD_JS not in source:
        return None, "OLD_JS_NOT_FOUND — source may have changed since E1b audit"

    if NEW_JS in source:
        return None, "ALREADY_PATCHED — NEW_JS already present in source"

    patched = source.replace(OLD_JS, NEW_JS, 1)

    # Sanity checks
    checks = {
        "initStickyObserver_present":        "function initStickyObserver()" in patched,
        "domcontent_listener_present":       "DOMContentLoaded" in patched,
        "readystate_check_present":          "readyState" in patched,
        "threshold_0.1_present":             "threshold: 0.1" in patched,
        "old_threshold_0_absent":            "{ threshold: 0 }" not in patched,
        "old_early_return_absent":           "if (!target) return;\n\n  new IntersectionObserver" not in patched,
        "html_unchanged":                    patched.count("<div id=\"bm-sticky-bar\"") == source.count("<div id=\"bm-sticky-bar\""),
        "schema_unchanged":                  patched.count("{% schema %}") == source.count("{% schema %}"),
        "style_unchanged":                   patched.count(".bm-sticky-bar {") == source.count(".bm-sticky-bar {"),
    }

    all_pass = all(checks.values())
    return patched, checks, all_pass


def diff_preview(old, new, n=5):
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = list(difflib.unified_diff(old_lines, new_lines,
                                     fromfile="bm-sticky-bar.liquid (before)",
                                     tofile="bm-sticky-bar.liquid (after)",
                                     n=n))
    return "".join(diff)


# ─── Verify ─────────────────────────────────────────────────────────────────────
def verify_storefront(products):
    results = []
    for p in products:
        handle = p["handle"]
        url = f"{STOREFRONT}/products/{handle}"
        try:
            resp = requests.get(url, timeout=20,
                                headers={"User-Agent": "BabyMania-E1c-Verify/1.0"})
            html = resp.text
            entry = {
                "handle": handle,
                "template": p["template"],
                "http_status": resp.status_code,
                "has_sticky_bar":            "bm-sticky-bar" in html,
                "has_form_buttons":          "product-form__buttons" in html,
                "has_init_sticky_observer":  "initStickyObserver" in html,
                "has_domcontent_listener":   "DOMContentLoaded" in html,
                "has_readystate_check":      "readyState" in html,
                "has_threshold_0.1":         "threshold: 0.1" in html,
                "old_threshold_0_gone":      "{ threshold: 0 }" not in html,
                "sticky_starts_hidden":      'aria-hidden="true"' in html and "bm-sticky-bar" in html,
            }
            entry["verdict"] = "PASS" if all([
                entry["has_sticky_bar"],
                entry["has_form_buttons"],
                entry["has_init_sticky_observer"],
                entry["has_domcontent_listener"],
                entry["has_readystate_check"],
                entry["http_status"] == 200,
                entry["old_threshold_0_gone"],
            ]) else "FAIL"
        except Exception as e:
            entry = {"handle": handle, "error": str(e), "verdict": "ERROR"}
        results.append(entry)
        time.sleep(0.5)
    return results


# ─── Output writers ─────────────────────────────────────────────────────────────
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


# ─── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run", "live"], required=True)
    args = parser.parse_args()

    print(f"\n=== Phase E1c Sticky Fix | mode={args.mode} | {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    token   = get_token()
    session = make_session(token)
    print("  Auth OK\n")

    # Fetch live file
    print(f"Fetching {ASSET_KEY}...")
    live_source = get_asset(session, ASSET_KEY)
    print(f"  Length: {len(live_source)} chars\n")

    # Backup
    backup_data = {
        "date": "2026-05-10",
        "theme_id": THEME_ID,
        "asset_key": ASSET_KEY,
        "source_length": len(live_source),
        "source": live_source,
    }
    write_json(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-backup.json", backup_data)

    # Apply patch (in memory)
    result = apply_patch(live_source)
    if len(result) == 2:
        patched, error_msg = result
        print(f"\nPATCH CANNOT BE APPLIED: {error_msg}")
        write_json(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-dry-run.json",
                   {"status": "BLOCKED", "reason": error_msg})
        write_text(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-dry-run.md",
                   f"# Phase E1c Dry Run\n**Status:** BLOCKED\n**Reason:** {error_msg}\n")
        return
    else:
        patched, checks, all_pass = result

    # Diff
    diff_text = diff_preview(live_source, patched)
    lines_changed = sum(1 for l in diff_text.splitlines()
                        if l.startswith("+") or l.startswith("-"))

    print("=== Diff preview ===")
    print(diff_text[:3000])
    print(f"  Lines changed (+ and -): {lines_changed}")
    print(f"  Sanity checks: {checks}")
    print(f"  All checks pass: {all_pass}\n")

    # Write dry-run files
    dry_run_data = {
        "date": "2026-05-10",
        "mode": args.mode,
        "asset_key": ASSET_KEY,
        "patch_applied": True,
        "lines_changed": lines_changed,
        "sanity_checks": checks,
        "all_pass": all_pass,
    }
    write_json(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-dry-run.json", dry_run_data)
    write_text(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-dry-run.md",
               f"# Phase E1c — Dry Run\n**Mode:** {args.mode}\n**Status:** {'PASS' if all_pass else 'FAIL'}\n\n"
               f"## Diff\n```diff\n{diff_text}\n```\n\n"
               f"## Sanity Checks\n" + "\n".join(f"- {k}: {'✅' if v else '❌'}" for k,v in checks.items()))

    # Rollback plan
    write_text(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-rollback-plan.md",
               f"""# Phase E1c — Rollback Plan
**Date:** 2026-05-10

## How to Rollback

Restore original `sections/bm-sticky-bar.liquid` from backup:
1. Read `output/tags/phaseE1c-sticky-fix-backup.json`
2. Extract `.source` field
3. PUT to theme {THEME_ID} asset `{ASSET_KEY}`

The change is JS-only. Rolling back restores the original inline script behavior.
Backup saved: `output/tags/phaseE1c-sticky-fix-backup.json`
""")

    if args.mode == "dry-run":
        print("DRY-RUN complete. No writes to Shopify.")
        if not all_pass:
            print("WARNING: Not all sanity checks passed. Review before running --mode=live.")
        return

    if not all_pass:
        print("BLOCKED: sanity checks failed — not writing to Shopify.")
        return

    # ── LIVE MODE ─────────────────────────────────────────────────────────────────
    print("LIVE MODE — Writing patched asset to Shopify...")
    put_asset(session, ASSET_KEY, patched)
    print("  PUT OK\n")

    # Verify storefront
    print("Verifying storefront HTML...")
    time.sleep(3)
    verify_results = verify_storefront(VERIFY_PRODUCTS)

    overall = "PASS" if all(r.get("verdict") == "PASS" for r in verify_results) else "FAIL"
    print(f"  Overall verify: {overall}")
    for r in verify_results:
        print(f"  {r['handle'][:50]:50s} → {r.get('verdict', 'ERROR')}")
        if r.get("verdict") != "PASS":
            for k, v in r.items():
                if k not in ("handle", "template", "verdict", "http_status"):
                    if not v:
                        print(f"    FAIL: {k}")

    write_json(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-verify.json", {
        "date": "2026-05-10",
        "overall": overall,
        "items": verify_results,
        "easysleep_tempio_note": "Not verified here — main-product disabled, T3 fix required separately",
    })

    verify_md_lines = [
        "# Phase E1c — Verify Report",
        f"**Date:** 2026-05-10 | **Overall:** {overall}",
        "",
        "| Product | Template | HTTP | Sticky | form__buttons | initObserver | DOMContent | readyState | threshold 0.1 | old gone | Verdict |",
        "|---------|----------|------|--------|---------------|-------------|------------|------------|--------------|----------|---------|",
    ]
    for r in verify_results:
        verify_md_lines.append(
            f"| {r.get('handle','')[:35]} | {r.get('template','')} "
            f"| {r.get('http_status','')} "
            f"| {'✅' if r.get('has_sticky_bar') else '❌'} "
            f"| {'✅' if r.get('has_form_buttons') else '❌'} "
            f"| {'✅' if r.get('has_init_sticky_observer') else '❌'} "
            f"| {'✅' if r.get('has_domcontent_listener') else '❌'} "
            f"| {'✅' if r.get('has_readystate_check') else '❌'} "
            f"| {'✅' if r.get('has_threshold_0.1') else '❌'} "
            f"| {'✅' if r.get('old_threshold_0_gone') else '❌'} "
            f"| **{r.get('verdict','?')}** |"
        )
    verify_md_lines += [
        "",
        "## EasySleep / Tempio",
        "Not tested here — `main-product` section is disabled on these templates.",
        "Sticky will still not appear. Requires separate T3 fix (enable main-product).",
    ]
    write_text(f"{OUTPUT_DIR}/phaseE1c-sticky-fix-verify.md", "\n".join(verify_md_lines))

    # Main report
    verdict = "PHASEE1C_STICKY_FIX_PASS" if overall == "PASS" else "PHASEE1C_STICKY_FIX_PARTIAL"
    report_md = f"""# Phase E1c — Sticky Add-to-Cart Fix Report
**Date:** 2026-05-10 | **Mode:** LIVE | **Tier:** T2
**Verdict:** {verdict}

## Change Applied

**File:** `sections/bm-sticky-bar.liquid`
**Type:** JavaScript only — no HTML, no CSS, no schema changes
**Lines changed:** {lines_changed}

### Root Cause Fixed
Inline `<script>` (no defer) runs before `main-product` section renders.
`querySelector('.product-form__buttons')` returns null → early return → observer never created.

### Patch Applied (Option A)
Wrapped observer setup in `initStickyObserver()` with `readyState` check:
- If `readyState === 'loading'`: wait for `DOMContentLoaded` → run observer setup
- Otherwise: run immediately
- Added `.product-form__submit` fallback selector
- Changed `threshold: 0` → `threshold: 0.1` (shows sticky when 90% of button gone)

## Sanity Checks
{chr(10).join(f'- {k}: {"✅" if v else "❌"}' for k,v in checks.items())}

## Verify: {overall}
See `output/tags/phaseE1c-sticky-fix-verify.md` for per-product results.

## EasySleep / Tempio
Still broken — different root cause (`main-product` disabled).
Requires separate T3 approval and fix.

## Files
- Backup: `output/tags/phaseE1c-sticky-fix-backup.json`
- Rollback: `output/tags/phaseE1c-sticky-fix-rollback-plan.md`
"""
    write_text(f"{DOCS_DIR}/phaseE1c-sticky-fix-report.md", report_md)

    print(f"\n=== {verdict} ===")


if __name__ == "__main__":
    main()
