"""
Phase E1c Post-Verify — T0 READ-ONLY
Checks live storefront HTML on clothing + shoes + accessories/reborn products.
No writes to Shopify. No theme changes.
"""
import json, sys, time, os, requests

sys.stdout.reconfigure(encoding="utf-8")

SHOP        = "a2756c-c0.myshopify.com"
API_VER     = "2024-10"
BASE        = f"https://{SHOP}/admin/api/{API_VER}"
TOKEN_URL   = f"https://{SHOP}/admin/oauth/access_token"
STOREFRONT  = "https://www.babymania-il.com"
DESKTOP_ENV = r"C:\Users\3024e\Desktop\shopify-token\.env"
PROJECT_ENV = r"C:\Projects\baby-mania-agent\.env"
OUTPUT_DIR  = "output/tags"
DOCS_DIR    = "docs/organic"

TEMPLATE_SUFFIXES = {
    "shoes":        "shoes",
    "accessories":  "accessories",
    "reborn":       "reborn",
}

CHECKS = [
    ("http_200",              lambda h, s: s == 200),
    ("has_sticky_bar",        lambda h, s: "bm-sticky-bar" in h),
    ("has_form_buttons",      lambda h, s: "product-form__buttons" in h),
    ("has_init_observer",     lambda h, s: "initStickyObserver" in h),
    ("has_domcontent",        lambda h, s: "DOMContentLoaded" in h),
    ("has_threshold_01",      lambda h, s: "threshold: 0.1" in h),
    ("no_old_threshold_0",    lambda h, s: "{ threshold: 0 }" not in h),
    ("aria_hidden_true_init", lambda h, s: 'aria-hidden="true"' in h),
]


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


_product_cache = []

def load_products(session):
    """Fetch all active products (up to 250) into cache."""
    global _product_cache
    if _product_cache:
        return
    r = session.get(
        f"{BASE}/products.json",
        params={"status": "active", "limit": 250},
        timeout=20,
    )
    r.raise_for_status()
    _product_cache = r.json().get("products", [])


def find_live_product(session, template_suffix, max_try=5):
    """Return first active product with given template_suffix that returns HTTP 200 on storefront."""
    load_products(session)
    candidates = [
        p for p in _product_cache
        if p.get("status") == "active"
        and p.get("template_suffix") == template_suffix
        and p.get("handle")
    ]
    for p in candidates[:max_try]:
        handle = p["handle"]
        try:
            r = requests.get(
                f"{STOREFRONT}/products/{handle}",
                timeout=10,
                headers={"User-Agent": "BabyMania-E1c-PostVerify/1.0"},
                allow_redirects=True,
            )
            if r.status_code == 200:
                return handle, p.get("title", "")
        except Exception:
            pass
        time.sleep(0.2)
    return None, f"No live accessible product with template_suffix={template_suffix}"


def verify_product(handle, label):
    url = f"{STOREFRONT}/products/{handle}"
    try:
        resp = requests.get(url, timeout=20,
                            headers={"User-Agent": "BabyMania-E1c-PostVerify/1.0"})
        html = resp.text
        status = resp.status_code
        result = {"handle": handle, "label": label, "url": url, "http_status": status}
        passed = []
        for name, fn in CHECKS:
            val = fn(html, status)
            result[name] = val
            passed.append(val)
        result["verdict"] = "PASS" if all(passed) else "FAIL"
        result["fail_checks"] = [n for n, fn in CHECKS if not fn(html, status)]
    except Exception as e:
        result = {"handle": handle, "label": label, "url": url,
                  "error": str(e), "verdict": "ERROR"}
    return result


def main():
    print("\n=== Phase E1c Post-Verify | T0 READ-ONLY ===\n")

    token   = get_token()
    session = make_session(token)
    print("  Auth OK\n")

    targets = [
        {"handle": "חליפת-תחרה-פרחונית-מורן", "label": "clothing (confirmed)"},
    ]

    # Find live products from shoes + accessories + reborn
    for label, suffix in TEMPLATE_SUFFIXES.items():
        print(f"Finding product with template_suffix='{suffix}'...")
        handle, title = find_live_product(session, suffix)
        if handle:
            print(f"  Found: {handle} ({title[:40]})")
            targets.append({"handle": handle, "label": label})
        else:
            print(f"  Not found: {title}")
        time.sleep(0.3)

    print(f"\nVerifying {len(targets)} products on live storefront...\n")
    results = []
    for t in targets:
        print(f"  Checking: {t['handle'][:60]}...")
        r = verify_product(t["handle"], t["label"])
        results.append(r)
        v = r.get("verdict", "ERROR")
        print(f"    → {v}" + (f"  FAIL: {r.get('fail_checks')}" if v != "PASS" else ""))
        time.sleep(0.4)

    pass_count = sum(1 for r in results if r.get("verdict") == "PASS")
    fail_count = len(results) - pass_count
    overall = "PASS" if fail_count == 0 else "FAIL"
    verdict = ("PHASEE1C_STICKY_STANDARD_VERIFY_PASS"
               if fail_count == 0
               else "PHASEE1C_STICKY_STANDARD_VERIFY_FAIL")

    print(f"\nOverall: {overall} ({pass_count}/{len(results)} PASS)")
    print(f"Verdict: {verdict}\n")

    # Write JSON
    json_data = {
        "date": "2026-05-10",
        "mode": "READ-ONLY POST-VERIFY",
        "tier": "T0",
        "overall": overall,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "verdict": verdict,
        "items": results,
        "easysleep_tempio": "NOT TESTED — main-product disabled, T3 fix required separately",
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_json = f"{OUTPUT_DIR}/phaseE1c-sticky-post-verify.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote: {out_json}")

    # Write MD
    md_lines = [
        "# Phase E1c — Sticky Post-Verify",
        f"**Date:** 2026-05-10 | **Mode:** READ-ONLY | **Tier:** T0",
        f"**Overall:** {overall} ({pass_count}/{len(results)}) | **Verdict:** `{verdict}`",
        "",
        "| Product | Label | HTTP | sticky_bar | form_buttons | initObserver | DOMContent | threshold_0.1 | no_old_t0 | aria_init | Verdict |",
        "|---------|-------|------|-----------|-------------|-------------|------------|--------------|-----------|-----------|---------|",
    ]
    for r in results:
        def c(k): return "✅" if r.get(k) else "❌"
        md_lines.append(
            f"| `{r.get('handle','')[:38]}` | {r.get('label','')} "
            f"| {r.get('http_status','')} "
            f"| {c('has_sticky_bar')} | {c('has_form_buttons')} "
            f"| {c('has_init_observer')} | {c('has_domcontent')} "
            f"| {c('has_threshold_01')} | {c('no_old_threshold_0')} "
            f"| {c('aria_hidden_true_init')} | **{r.get('verdict','?')}** |"
        )
    md_lines += [
        "",
        "## EasySleep / Tempio",
        "Not tested — `main-product` section disabled on those templates.",
        "Sticky will not appear. Requires separate T3 fix.",
        "",
        f"## Files",
        f"- `output/tags/phaseE1c-sticky-post-verify.json`",
        f"- `output/tags/phaseE1c-sticky-post-verify.md`",
    ]
    out_md = f"{OUTPUT_DIR}/phaseE1c-sticky-post-verify.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"  Wrote: {out_md}")

    # Print summary for journal update
    print("\n--- SUMMARY FOR JOURNAL ---")
    for r in results:
        print(f"  {r.get('label','')}: {r.get('handle','')[:50]} → {r.get('verdict','?')}")
    print(f"  EasySleep/Tempio: NOT TESTED (T3)")
    print(f"\nVERDICT: {verdict}")


if __name__ == "__main__":
    main()
