"""
Phase 7C Live Batch 8 — Post-run verify.
Reads backup JSON, re-GETs each product from Shopify, re-verifies tags.
Also verifies Hebrew month normalization was applied.
READ-ONLY. No writes.
"""
import argparse, json, sys, time, urllib.request, datetime

ENV_PATH = r"C:\Users\3024e\Desktop\shopify-token\.env"

def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

env = load_env(ENV_PATH)
TOKEN = env["SHOPIFY_ACCESS_TOKEN"]
SHOP  = env["SHOPIFY_SHOP_URL"]
BASE  = f"https://{SHOP}/admin/api/2024-10"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

BACKUP_JSON = "output/tags/phase7c-live-batch8-backup.json"
VERIFY_JSON = "output/tags/phase7c-live-batch8-verify.json"

HEBREW_MONTH_NORM = {
    "0-3 חודש":   "0-3 חודשים",
    "3-6 חודש":   "3-6 חודשים",
    "6-12 חודש":  "6-12 חודשים",
    "12-18 חודש": "12-18 חודשים",
    "18-24 חודש": "18-24 חודשים",
}


def log(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()


def shopify_get(pid):
    url = f"{BASE}/products/{pid}.json?fields=id,title,tags,status"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default="output/tags/phase7c-batch8-plan.json")
    parser.add_argument("--normalize-hebrew-months", default="true")
    parser.add_argument("--exclude-product-id", default="", help="Informational — matches live script flag")
    parser.add_argument("--max-products", type=int, default=20)
    args = parser.parse_args()

    do_normalize = args.normalize_hebrew_months.lower() == "true"

    log("=" * 62)
    log("Phase 7C Live Batch 8 — Post-run Verify (READ-ONLY)")
    log("=" * 62)

    try:
        with open(BACKUP_JSON, encoding="utf-8") as f:
            backup = json.load(f)
    except FileNotFoundError:
        log(f"[FAIL] backup file not found: {BACKUP_JSON}")
        sys.exit(1)

    try:
        with open(VERIFY_JSON, encoding="utf-8") as f:
            live_verify = json.load(f)
    except FileNotFoundError:
        log(f"[FAIL] verify JSON not found: {VERIFY_JSON}")
        sys.exit(1)

    log(f"\n[info] backup has {len(backup['products'])} products")
    log(f"[info] live_verify verdict={live_verify['verdict']}")
    log(f"[info] live_verify written={live_verify.get('total_written', 0)} pass={live_verify.get('pass_count', 0)}")

    if live_verify["verdict"] != "PHASE7C_LIVE_BATCH8_PASS":
        log(f"[WARN] live_verify verdict not PASS — post-run verify will re-check all written products")

    pid_to_result = {str(r["product_id"]): r for r in live_verify["products"]}

    post_rows = []
    all_pass  = True

    log(f"\n[re-verify] GET + check each product from Shopify")

    for bp in backup["products"]:
        pid             = str(bp["product_id"])
        title_expected  = bp["title_from_shopify"]
        before_tags     = bp["before_tags"]
        proposed        = bp["proposed_new_tags"]
        month_ch        = bp.get("month_changes", [])
        final_expected  = bp["final_tags_before_write"]

        live_r = pid_to_result.get(pid)
        if not live_r:
            log(f"  [SKIP] {pid} — not in live verify results")
            continue

        if live_r["final_verdict"] != "PASS":
            log(f"  [SKIP] {pid} — live_verdict=FAIL (not written successfully)")
            continue

        try:
            p = shopify_get(pid)
        except Exception as e:
            log(f"  [FAIL] {pid} GET error: {e}")
            all_pass = False
            post_rows.append({"product_id": pid, "verdict": "FAIL",
                              "reason": f"GET_ERROR: {e}"})
            continue

        time.sleep(0.3)

        cur_tags   = sorted([t.strip() for t in p.get("tags", "").split(",") if t.strip()])
        cur_title  = p.get("title", "")
        cur_status = p.get("status", "")

        missing_proposed   = [t for t in proposed if t not in cur_tags]
        lingering_singular = [t for t in cur_tags  if t in HEBREW_MONTH_NORM] if do_normalize else []
        missing_normalized = []
        if do_normalize and month_ch:
            missing_normalized = [c["to"] for c in month_ch if c["to"] not in cur_tags]
        title_ok  = (cur_title  == title_expected)
        status_ok = (cur_status == "active")
        age_tags  = [t for t in cur_tags if t.startswith("age-")]

        ok = (
            not missing_proposed   and
            not lingering_singular and
            not missing_normalized and
            title_ok               and
            status_ok              and
            not age_tags
        )

        row = {
            "product_id":               pid,
            "title_from_shopify":       cur_title,
            "status":                   cur_status,
            "after_tags_count":         len(cur_tags),
            "after_tags":               cur_tags,
            "missing_proposed_tags":    missing_proposed,
            "lingering_singular_month": lingering_singular,
            "missing_normalized_month": missing_normalized,
            "title_ok":                 title_ok,
            "status_ok":                status_ok,
            "age_tags":                 age_tags,
            "verdict":                  "PASS" if ok else "FAIL",
        }
        post_rows.append(row)

        if ok:
            month_note = f" | {len(month_ch)} month(s) normalized" if month_ch else ""
            log(f"  ✅ {pid} — {cur_title[:45]} | {len(cur_tags)} tags{month_note}")
        else:
            all_pass = False
            reasons = []
            if missing_proposed:   reasons.append(f"missing_proposed={missing_proposed}")
            if lingering_singular: reasons.append(f"lingering_singular={lingering_singular}")
            if missing_normalized: reasons.append(f"missing_normalized={missing_normalized}")
            if not title_ok:       reasons.append("title_changed")
            if not status_ok:      reasons.append(f"status={cur_status}")
            if age_tags:           reasons.append(f"age_tags={age_tags}")
            log(f"  ❌ {pid} FAIL: {'; '.join(reasons)}")

    pass_n  = sum(1 for r in post_rows if r["verdict"] == "PASS")
    fail_n  = sum(1 for r in post_rows if r["verdict"] == "FAIL")
    verdict = "POST_VERIFY_PASS" if all_pass and fail_n == 0 else "POST_VERIFY_FAIL"

    log(f"\n[POST-VERIFY SUMMARY]")
    log(f"  checked={len(post_rows)} | PASS={pass_n} | FAIL={fail_n}")
    log(f"[VERDICT] {verdict}")

    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase":            "7C",
        "type":             "live_batch8_post_verify",
        "timestamp":        ts,
        "shopify_writes":   "NONE — GET only",
        "normalize_hebrew_months": do_normalize,
        "checked":          len(post_rows),
        "pass_count":       pass_n,
        "fail_count":       fail_n,
        "products":         post_rows,
        "verdict":          verdict,
    }

    live_verify["post_verify"] = result
    with open(VERIFY_JSON, "w", encoding="utf-8") as f:
        json.dump(live_verify, f, ensure_ascii=False, indent=2)
    log(f"[saved] {VERIFY_JSON} (post_verify appended)")

    sys.exit(0 if verdict == "POST_VERIFY_PASS" else 1)


if __name__ == "__main__":
    main()
