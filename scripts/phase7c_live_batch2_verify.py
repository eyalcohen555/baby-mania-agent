"""
Phase 7C Live Batch 2 — Post-run verify.
Re-GETs each written product and confirms tags stable.
READ-ONLY. No writes.
"""
import json, sys, time, urllib.request, datetime

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
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

BACKUP_FILE = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-backup.json"
VERIFY_JSON = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-verify.json"

def log(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()

def shopify_get(pid):
    url = f"{BASE}/products/{pid}.json?fields=id,title,tags,status"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"]

def main():
    log("=" * 60)
    log("Phase 7C Live Batch 2 — Post-run Verify (READ-ONLY)")
    log("=" * 60)

    with open(BACKUP_FILE, encoding="utf-8") as f:
        backup = json.load(f)
    with open(VERIFY_JSON, encoding="utf-8") as f:
        live_verify = json.load(f)

    log(f"\n[info] backup={len(backup['products'])} | live_verdict={live_verify['verdict']} | written={live_verify['total_written']}")

    pid_to_result = {str(r["product_id"]): r for r in live_verify["products"]}
    post_rows = []
    all_pass = True

    log("\n[re-verify] GET + check each written product")

    for bp in backup["products"]:
        pid = str(bp["product_id"])
        live_r = pid_to_result.get(pid)
        if not live_r or live_r["final_verdict"] != "PASS":
            continue

        try:
            p = shopify_get(pid)
        except Exception as e:
            log(f"  [FAIL] {pid} GET error: {e}")
            all_pass = False
            post_rows.append({"product_id": pid, "verdict": "FAIL", "reason": f"GET_ERROR: {e}"})
            continue

        time.sleep(0.3)
        cur_tags = sorted([t.strip() for t in p.get("tags","").split(",") if t.strip()])
        proposed = bp["proposed_new_tags"]
        before   = bp["before_tags"]

        missing_proposed = [t for t in proposed if t not in cur_tags]
        missing_before   = [t for t in before   if t not in cur_tags]
        age_tags = [t for t in cur_tags if t.startswith("age-")]

        ok = (not missing_proposed and not missing_before and
              p.get("title","") == bp["title_from_shopify"] and
              p.get("status","") == "active" and not age_tags)

        row = {
            "product_id": pid,
            "title_from_shopify": p.get("title",""),
            "status": p.get("status",""),
            "after_tags_count": len(cur_tags),
            "after_tags": cur_tags,
            "missing_proposed_tags": missing_proposed,
            "missing_before_tags": missing_before,
            "age_tags": age_tags,
            "verdict": "PASS" if ok else "FAIL",
        }
        post_rows.append(row)

        if ok:
            log(f"  ✅ {pid} — {p.get('title','')[:40]} | {len(cur_tags)} tags")
        else:
            all_pass = False
            reasons = []
            if missing_proposed: reasons.append(f"missing_proposed={missing_proposed}")
            if missing_before:   reasons.append(f"missing_before={missing_before}")
            if age_tags:         reasons.append(f"age_tags={age_tags}")
            log(f"  ❌ {pid} FAIL: {'; '.join(reasons)}")

    pass_n = sum(1 for r in post_rows if r["verdict"] == "PASS")
    fail_n = sum(1 for r in post_rows if r["verdict"] == "FAIL")
    verdict = "POST_VERIFY_PASS" if all_pass and fail_n == 0 else "POST_VERIFY_FAIL"

    log(f"\n[POST-VERIFY SUMMARY] checked={len(post_rows)} | PASS={pass_n} | FAIL={fail_n}")
    log(f"[VERDICT] {verdict}")

    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    live_verify["post_verify"] = {
        "phase": "7C-batch2",
        "type": "live_batch2_post_verify",
        "timestamp": ts,
        "shopify_writes": "NONE — GET only",
        "checked": len(post_rows),
        "pass_count": pass_n,
        "fail_count": fail_n,
        "products": post_rows,
        "verdict": verdict,
    }
    with open(VERIFY_JSON, "w", encoding="utf-8") as f:
        json.dump(live_verify, f, ensure_ascii=False, indent=2)
    log(f"[saved] {VERIFY_JSON}")

    sys.exit(0 if verdict == "POST_VERIFY_PASS" else 1)

if __name__ == "__main__":
    main()
