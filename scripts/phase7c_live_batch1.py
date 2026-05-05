"""
Phase 7C Live Batch 1.
T3 approval received from Ayal. Max 20 products from phase7c plan.
Excludes shoe/sandal/sneaker products by title keyword check.
Modes: --mode=dry-run (GET only) | --mode=live (PUT + verify).
Stops on any failure; rollback written products on FAIL.
"""
import argparse, json, sys, time, datetime, urllib.request, urllib.error

# ── credentials ───────────────────────────────────────────────────────────────
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

# ── paths ─────────────────────────────────────────────────────────────────────
PLAN_FILE     = r"C:\Projects\baby-mania-agent\output\tags\phase7c-tagging-expansion-plan.json"
BACKUP_FILE   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-backup.json"
DRYRUN_JSON   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-dry-run.json"
DRYRUN_MD     = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-dry-run.md"
ROLLBACK_MD   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-rollback-plan.md"
VERIFY_JSON   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-verify.json"
VERIFY_MD     = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch1-verify.md"

# ── allowed values (taxonomy spec v1 §14) ─────────────────────────────────────
ALLOWED_VALUES = {
    "type-romper","type-bodysuit","type-dress","type-set","type-pants","type-top",
    "type-hat","type-swimwear","type-shoes","type-sandals","type-sneakers","type-boots",
    "type-coat","type-reborn-doll","type-toy","type-accessory","type-swimming-ring",
    "size-newborn","size-0-3m","size-3-6m","size-6-9m","size-9-12m","size-12-18m",
    "size-18-24m","size-2y","size-3y","size-4y",
    "season-summer","season-winter","season-spring-fall","season-all",
    "fabric-cotton","fabric-linen","fabric-muslin","fabric-knit","fabric-fleece",
    "fabric-denim","fabric-polyester","fabric-faux-fur","fabric-corduroy","fabric-velvet",
    "fabric-waffle-knit","fabric-silicone","fabric-body",
    "occ-everyday","occ-gift","occ-baby-shower","occ-beach","occ-sleep",
    "occ-special-event","occ-photoshoot","occ-first-step","occ-water-play","occ-calming",
    "occ-seasonal",
    "gender-girl","gender-boy","gender-neutral",
    "style-elegant","style-casual","style-vintage","style-sporty","style-floral",
    "style-animal-print","style-teddy","style-european","style-unicorn",
    "style-striped","style-modern",
}

FORBIDDEN_PREFIXES = ["age-"]
FORBIDDEN_EXACT    = {"season-unknown", "size-unknown", "gender-unknown", "3-6M6-9M"}

# T3 exclusion: no shoes/sandals/sneakers by title keyword
SHOE_TITLE_KW = ["סנדל", "נעל", "מגפ", "כפכף", "sandal", "shoe", "sneaker", "boot", "croc"]

# ── helpers ───────────────────────────────────────────────────────────────────
def log(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()

def is_shoe_title(title: str) -> bool:
    t = title.lower()
    return any(kw.lower() in t for kw in SHOE_TITLE_KW)

def check_forbidden(tags):
    violations = []
    for t in tags:
        for p in FORBIDDEN_PREFIXES:
            if t.startswith(p):
                violations.append(f"FORBIDDEN_PREFIX: {t}")
        if t in FORBIDDEN_EXACT:
            violations.append(f"FORBIDDEN_EXACT: {t}")
        if " " in t:
            violations.append(f"SPACE_IN_TAG: {t}")
    return violations

def shopify_get(pid):
    url = f"{BASE}/products/{pid}.json?fields=id,title,tags,status"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"]

def shopify_put(pid, tags_list):
    tags_str = ", ".join(sorted(set(tags_list)))
    body = json.dumps({"product": {"id": int(pid), "tags": tags_str}}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/products/{pid}.json",
        data=body, headers=HEADERS, method="PUT"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"], r.status

def shopify_put_restore(pid, original_tags_list):
    return shopify_put(pid, original_tags_list)

# ── select batch ─────────────────────────────────────────────────────────────
def select_batch(plan, max_n):
    excluded_shoe = []
    candidates = []
    for p in plan["recommended_batch"]:
        if is_shoe_title(p["title"]):
            excluded_shoe.append(p)
        else:
            candidates.append(p)
    selected = candidates[:max_n]
    return selected, excluded_shoe

# ── DRY RUN ───────────────────────────────────────────────────────────────────
def run_dry_run(plan, max_n):
    log("=" * 60)
    log("Phase 7C Live Batch 1 — DRY RUN")
    log("=" * 60)

    selected, excluded = select_batch(plan, max_n)
    log(f"\n[select] {len(plan['recommended_batch'])} in plan → {len(excluded)} excluded (shoe title) → {len(selected)} selected")

    if excluded:
        log("\n[excluded — shoe title keyword]")
        for p in excluded:
            log(f"  EXCLUDE: {p['product_id']} | {p['title']}")

    log(f"\n[selected — {len(selected)} products for batch]")

    dry_rows = []
    failures = []

    for idx, p in enumerate(selected, 1):
        pid = p["product_id"]
        proposed = p["all_proposed_tags"]
        log(f"\n  [{idx:02}/{len(selected)}] GET {pid}")

        try:
            live = shopify_get(pid)
        except Exception as e:
            log(f"    GET_ERROR: {e}")
            failures.append(f"{pid}: GET_ERROR: {e}")
            continue

        cur_tags = sorted([t.strip() for t in live["tags"].split(",") if t.strip()])
        final_tags = sorted(set(cur_tags) | set(proposed))
        new_tags = [t for t in proposed if t not in cur_tags]
        title_live = live["title"]
        status_live = live.get("status", "unknown")

        # forbidden check on proposed
        viols = check_forbidden(proposed)
        forbidden_ok = "PASS" if not viols else f"FAIL: {viols}"

        # allowed_values check
        not_allowed = [t for t in proposed if t not in ALLOWED_VALUES]
        allowed_ok = "PASS" if not not_allowed else f"FAIL: {not_allowed}"

        # no existing type-* collision
        existing_type = [t for t in cur_tags if t.startswith("type-")]
        p_type = p["proposed_type"]
        type_collision = [t for t in existing_type if t != p_type]
        type_ok = "PASS" if not type_collision else f"WARN: existing type {type_collision}"

        # age-* in proposed
        age_proposed = [t for t in proposed if t.startswith("age-")]
        age_ok = "PASS" if not age_proposed else f"FAIL: {age_proposed}"

        ok = (forbidden_ok == "PASS" and allowed_ok == "PASS" and
              age_ok == "PASS" and status_live == "active")

        row = {
            "product_id": pid,
            "title_from_shopify": title_live,
            "status": status_live,
            "before_count": len(cur_tags),
            "before_tags": cur_tags,
            "proposed_type": p["proposed_type"],
            "type_conf": p["type_conf"],
            "type_source": p["type_source"],
            "proposed_gender": p["proposed_gender"],
            "gender_conf": p["gender_conf"],
            "gender_source": p["gender_source"],
            "proposed_occs": p["proposed_occs"],
            "all_proposed_tags": proposed,
            "new_tags_to_add": new_tags,
            "final_tags": final_tags,
            "final_count": len(final_tags),
            "forbidden_check": forbidden_ok,
            "allowed_values_check": allowed_ok,
            "type_collision_check": type_ok,
            "age_check": age_ok,
            "dry_run_verdict": "PASS" if ok else "FAIL",
        }
        dry_rows.append(row)

        if not ok:
            failures.append(f"{pid}: dry_run_verdict=FAIL forbidden={forbidden_ok} allowed={allowed_ok} age={age_ok}")

        log(f"    title: {title_live}")
        log(f"    status: {status_live}")
        log(f"    before={len(cur_tags)} proposed={len(proposed)} final={len(final_tags)}")
        log(f"    new_tags: {new_tags}")
        log(f"    forbidden={forbidden_ok} | allowed={allowed_ok} | age={age_ok}")
        log(f"    verdict: {'✅ PASS' if ok else '❌ FAIL'}")

    # summary
    pass_n = sum(1 for r in dry_rows if r["dry_run_verdict"] == "PASS")
    fail_n = sum(1 for r in dry_rows if r["dry_run_verdict"] == "FAIL")

    log(f"\n[DRY RUN SUMMARY]")
    log(f"  selected: {len(selected)} | PASS: {pass_n} | FAIL: {fail_n}")

    if failures:
        log("[DRY RUN FAIL] Blocking issues found:")
        for f in failures:
            log(f"  {f}")

    overall = "DRY_RUN_PASS" if not failures else "DRY_RUN_FAIL"
    log(f"\n[VERDICT] {overall}")

    # write JSON
    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C",
        "type": "live_batch1_dry_run",
        "timestamp": ts,
        "t3_approval": "Ayal approved Phase 7C Live Batch 1",
        "shopify_writes": "NONE — dry run only",
        "total_in_plan": len(plan["recommended_batch"]),
        "excluded_shoe": len(excluded),
        "selected": len(selected),
        "dry_run_pass": pass_n,
        "dry_run_fail": fail_n,
        "products": dry_rows,
        "verdict": overall,
    }

    with open(DRYRUN_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"[saved] {DRYRUN_JSON}")

    # write MD
    with open(DRYRUN_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 7C Live Batch 1 — Dry Run\n\n")
        f.write(f"**Date:** {ts[:10]}  \n")
        f.write(f"**Shopify writes:** NONE  \n")
        f.write(f"**Selected:** {len(selected)} / {len(plan['recommended_batch'])} ({len(excluded)} excluded — shoe title)  \n\n")
        f.write(f"---\n\n## Excluded (shoe title keyword)\n\n")
        for p in excluded:
            f.write(f"- `{p['product_id']}` — {p['title']}\n")
        f.write(f"\n---\n\n## Dry Run Results\n\n")
        f.write("| # | product_id | title | type | conf | src | gender | proposed_tags | before | final | verdict |\n")
        f.write("|---|-----------|-------|------|------|-----|--------|--------------|--------|-------|--------|\n")
        for i, r in enumerate(dry_rows, 1):
            t = r["title_from_shopify"][:35]
            g = r["proposed_gender"] or "—"
            tags_str = ", ".join(r["all_proposed_tags"])
            v = "✅ PASS" if r["dry_run_verdict"] == "PASS" else "❌ FAIL"
            f.write(f"| {i} | `{r['product_id']}` | {t} | `{r['proposed_type']}` | {r['type_conf']} | {r['type_source']} | {g} | {tags_str} | {r['before_count']} | {r['final_count']} | {v} |\n")
        f.write(f"\n---\n\n## Verdict\n\n**{overall}**\n")
        if failures:
            f.write("\n### Failures\n\n")
            for ff in failures:
                f.write(f"- {ff}\n")
    log(f"[saved] {DRYRUN_MD}")

    # write rollback plan
    with open(ROLLBACK_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 7C Live Batch 1 — Rollback Plan\n\n")
        f.write(f"**Backup file:** `output/tags/phase7c-live-batch1-backup.json`  \n")
        f.write(f"**Trigger:** any product verify FAIL during live write  \n\n")
        f.write(f"## Protocol\n\n")
        f.write("1. Stop immediately on first FAIL\n")
        f.write("2. Read backup JSON — get `before_tags` for each written product\n")
        f.write("3. For each written product: PUT back `before_tags` only\n")
        f.write("4. GET verify rollback completed\n")
        f.write("5. Commit with message: `rollback(layer7): phase7c live batch1`\n\n")
        f.write(f"## Products in this batch ({len(selected)})\n\n")
        f.write("| product_id | title | proposed_tags |\n")
        f.write("|-----------|-------|---------------|\n")
        for r in dry_rows:
            tags_str = ", ".join(r["all_proposed_tags"])
            f.write(f"| `{r['product_id']}` | {r['title_from_shopify'][:40]} | {tags_str} |\n")
    log(f"[saved] {ROLLBACK_MD}")

    return overall == "DRY_RUN_PASS", dry_rows, selected

# ── LIVE ──────────────────────────────────────────────────────────────────────
def run_live(plan, max_n):
    log("=" * 60)
    log("Phase 7C Live Batch 1 — LIVE WRITE")
    log("=" * 60)

    # require dry run to have passed
    try:
        with open(DRYRUN_JSON, encoding="utf-8") as f:
            dry = json.load(f)
    except FileNotFoundError:
        log("[FAIL] dry-run JSON not found — run --mode=dry-run first")
        return False
    if dry["verdict"] != "DRY_RUN_PASS":
        log(f"[FAIL] dry-run verdict={dry['verdict']} — must be DRY_RUN_PASS before live")
        return False
    log(f"[pre-check] dry-run verdict=DRY_RUN_PASS ✅")

    selected, excluded = select_batch(plan, max_n)
    log(f"[select] {len(selected)} products for live write")

    # ── STEP A: token check ───────────────────────────────────────────────────
    log(f"\n[token] suffix={TOKEN[-4:]}")

    # ── STEP B: backup ────────────────────────────────────────────────────────
    log("\n[STEP B] Creating backup from Shopify (GET all products before any write)")
    backup_products = []
    ts = datetime.datetime.utcnow().isoformat() + "+00:00"

    for p in selected:
        pid = p["product_id"]
        try:
            live = shopify_get(pid)
        except Exception as e:
            log(f"[FAIL] backup GET {pid}: {e}")
            return False
        cur_tags = sorted([t.strip() for t in live["tags"].split(",") if t.strip()])
        final_tags = sorted(set(cur_tags) | set(p["all_proposed_tags"]))
        sources = [
            {"tag": p["proposed_type"], "source": p["type_source"], "conf": p["type_conf"]},
        ]
        if p["proposed_gender"]:
            sources.append({"tag": p["proposed_gender"], "source": p["gender_source"], "conf": p["gender_conf"]})
        for occ in p["proposed_occs"]:
            sources.append({"tag": occ, "source": "title_or_existing_tag", "conf": 0.85})
        backup_products.append({
            "product_id": pid,
            "title_from_shopify": live["title"],
            "status_before": live.get("status", "unknown"),
            "before_tags": cur_tags,
            "before_tags_count": len(cur_tags),
            "proposed_new_tags": p["all_proposed_tags"],
            "proposed_new_tags_with_source": sources,
            "confidence_per_tag": {t: p["type_conf"] for t in p["all_proposed_tags"]},
            "source_per_tag": {t: p["type_source"] for t in p["all_proposed_tags"]},
            "final_tags_before_write": final_tags,
            "backup_timestamp": ts,
        })
        log(f"  backed up {pid} — before={len(cur_tags)} final={len(final_tags)}")

    backup = {
        "backup_timestamp": ts,
        "phase": "Phase 7C live batch 1 pre-write backup",
        "t3_approval": "Ayal approved Phase 7C Live Batch 1",
        "shopify_writes_at_backup": "NONE",
        "products": backup_products,
    }
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    log(f"[BACKUP SAVED] {BACKUP_FILE}")

    # ── STEP C+D: write + verify one at a time ────────────────────────────────
    log(f"\n[STEP C+D] Writing + verifying {len(selected)} products")
    written = []
    verify_results = []
    failed_pid = None

    for idx, entry in enumerate(backup_products, 1):
        pid     = entry["product_id"]
        title   = entry["title_from_shopify"]
        cur     = entry["before_tags"]
        proposed = entry["proposed_new_tags"]
        sources  = entry["proposed_new_tags_with_source"]
        final   = entry["final_tags_before_write"]

        log(f"\n  [{idx:02}/{len(backup_products)}] pid={pid} — {title[:50]}")
        log(f"    before={len(cur)} proposed={len(proposed)} final={len(final)}")

        # safety: no deletions
        for t in cur:
            if t not in final:
                msg = f"SAFETY_FAIL: current tag '{t}' would be removed"
                log(f"    [FAIL] {msg}")
                failed_pid = pid
                verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
                break
        if failed_pid:
            break

        # forbidden check
        viols = check_forbidden(proposed)
        if viols:
            msg = f"FORBIDDEN: {viols}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
            break

        # not-in-allowed check
        not_allowed = [t for t in proposed if t not in ALLOWED_VALUES]
        if not_allowed:
            msg = f"NOT_IN_ALLOWED_VALUES: {not_allowed}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
            break

        # PUT
        try:
            put_product, http_status = shopify_put(pid, final)
            log(f"    PUT HTTP {http_status}")
        except Exception as e:
            msg = f"PUT_ERROR: {e}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            r = _fail_record(entry, msg, "PUT_ERROR")
            r["rollback_needed"] = "YES"
            verify_results.append(r)
            break

        written.append({"pid": pid, "title": title, "before_tags": cur, "final_tags": final})

        # GET verify
        time.sleep(0.4)
        try:
            after_product = shopify_get(pid)
        except Exception as e:
            msg = f"GET_VERIFY_ERROR: {e}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            r = _fail_record(entry, msg, "GET_ERROR")
            r["rollback_needed"] = "YES"
            verify_results.append(r)
            break

        after_tags = sorted([t.strip() for t in after_product.get("tags","").split(",") if t.strip()])
        after_title  = after_product.get("title","")
        after_status = after_product.get("status","")

        missing_new = [t for t in proposed if t not in after_tags]
        removed_old = [t for t in cur      if t not in after_tags]
        unexpected  = [t for t in after_tags if t not in final and t not in cur]
        title_changed = "NO" if after_title == title else "YES"
        age_tags = [t for t in after_tags if t.startswith("age-")]
        not_allowed_after = [t for t in proposed if t not in ALLOWED_VALUES]

        allowed_check  = "PASS" if not not_allowed else f"FAIL: {not_allowed}"
        forbidden_check = "PASS" if not viols else f"FAIL: {viols}"

        passed = (
            not missing_new and
            not removed_old and
            not unexpected and
            title_changed == "NO" and
            after_status == "active" and
            not age_tags and
            not not_allowed
        )
        verdict = "PASS" if passed else "FAIL"

        r = {
            "product_id": pid,
            "title_from_shopify": title,
            "status_before": entry["status_before"],
            "status_after": after_status,
            "before_tags": cur,
            "before_tags_count": len(cur),
            "proposed_new_tags": proposed,
            "proposed_new_tags_with_source": sources,
            "confidence_per_tag": entry["confidence_per_tag"],
            "source_per_tag": entry["source_per_tag"],
            "allowed_values_check": allowed_check,
            "forbidden_tags_check": forbidden_check,
            "final_tags_before_write": final,
            "after_tags": after_tags,
            "after_tags_count": len(after_tags),
            "missing_new_tags": missing_new,
            "removed_old_tags": removed_old,
            "unexpected_tags": unexpected,
            "title_changed": title_changed,
            "rollback_needed": "NO",
            "age_tags_check": "PASS" if not age_tags else f"FAIL: {age_tags}",
            "final_verdict": verdict,
        }
        verify_results.append(r)

        if verdict == "PASS":
            log(f"    verify ✅ PASS — after={len(after_tags)} tags")
        else:
            reasons = []
            if missing_new:    reasons.append(f"missing_new={missing_new}")
            if removed_old:    reasons.append(f"removed_old={removed_old}")
            if unexpected:     reasons.append(f"unexpected={unexpected}")
            if title_changed == "YES": reasons.append("title_changed")
            if after_status != "active": reasons.append(f"status={after_status}")
            if age_tags:       reasons.append(f"age_tags={age_tags}")
            log(f"    verify ❌ FAIL: {'; '.join(reasons)}")
            failed_pid = pid
            r["rollback_needed"] = "YES"
            break

    # ── rollback on failure ───────────────────────────────────────────────────
    if failed_pid and written:
        log(f"\n[ROLLBACK] Failure at {failed_pid} — rolling back {len(written)} written products")
        for w in reversed(written):
            try:
                shopify_put_restore(w["pid"], w["before_tags"])
                time.sleep(0.3)
                after_restore = shopify_get(w["pid"])
                r_after = sorted([t.strip() for t in after_restore.get("tags","").split(",") if t.strip()])
                ok = all(t in r_after for t in w["before_tags"])
                log(f"  rollback {w['pid']}: {'OK' if ok else 'WARN — verify manually'}")
            except Exception as e:
                log(f"  rollback {w['pid']}: ERROR {e}")

    # ── write results ─────────────────────────────────────────────────────────
    pass_n = sum(1 for r in verify_results if r["final_verdict"] == "PASS")
    fail_n = sum(1 for r in verify_results if r["final_verdict"] == "FAIL")
    total_written = len(written)

    if not failed_pid:
        overall = "PHASE7C_LIVE_BATCH1_PASS"
    else:
        overall = "HOLD_PHASE7C_LIVE_BATCH1"

    log(f"\n[RESULT] written={total_written} | PASS={pass_n} | FAIL={fail_n}")
    log(f"[VERDICT] {overall}")

    ts2 = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C",
        "type": "live_batch1_verify",
        "timestamp": ts2,
        "t3_approval": "Ayal approved Phase 7C Live Batch 1",
        "shopify_writes": f"{total_written} products PUT",
        "total_selected": len(selected),
        "total_written": total_written,
        "pass_count": pass_n,
        "fail_count": fail_n,
        "rollback_triggered": bool(failed_pid),
        "failed_pid": failed_pid,
        "products": verify_results,
        "verdict": overall,
    }
    with open(VERIFY_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"[saved] {VERIFY_JSON}")

    _write_verify_md(result, verify_results)

    return overall == "PHASE7C_LIVE_BATCH1_PASS"

def _fail_record(entry, msg, status_after):
    return {
        "product_id": entry["product_id"],
        "title_from_shopify": entry["title_from_shopify"],
        "status_before": entry["status_before"],
        "status_after": status_after,
        "before_tags": entry["before_tags"],
        "before_tags_count": len(entry["before_tags"]),
        "proposed_new_tags": entry["proposed_new_tags"],
        "proposed_new_tags_with_source": entry["proposed_new_tags_with_source"],
        "confidence_per_tag": entry.get("confidence_per_tag", {}),
        "source_per_tag": entry.get("source_per_tag", {}),
        "allowed_values_check": "NOT_CHECKED",
        "forbidden_tags_check": "NOT_CHECKED",
        "final_tags_before_write": entry["final_tags_before_write"],
        "after_tags": [],
        "after_tags_count": 0,
        "missing_new_tags": entry["proposed_new_tags"],
        "removed_old_tags": [],
        "unexpected_tags": [],
        "title_changed": "NOT_CHECKED",
        "rollback_needed": "NO",
        "age_tags_check": "NOT_CHECKED",
        "final_verdict": "FAIL",
        "fail_reason": msg,
    }

def _write_verify_md(result, rows):
    ts = result["timestamp"][:10]
    overall = result["verdict"]

    with open(VERIFY_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 7C Live Batch 1 — Verify Report\n\n")
        f.write(f"**Date:** {ts}  \n")
        f.write(f"**T3 approval:** {result['t3_approval']}  \n")
        f.write(f"**Shopify writes:** {result['shopify_writes']}  \n")
        f.write(f"**Total selected:** {result['total_selected']}  \n")
        f.write(f"**Written:** {result['total_written']}  \n")
        f.write(f"**Rollback triggered:** {'YES' if result['rollback_triggered'] else 'NO'}  \n\n")
        f.write(f"---\n\n")

        f.write("## QA Table — All Products\n\n")
        f.write("| # | product_id | title | before | +new | after | forbidden | miss_new | removed | age_check | title_chg | status | verdict |\n")
        f.write("|---|-----------|-------|--------|------|-------|-----------|---------|---------|-----------|-----------|--------|--------|\n")

        for i, r in enumerate(rows, 1):
            title = r["title_from_shopify"][:30]
            new_n = len(r["proposed_new_tags"])
            fbd   = "✅" if r["forbidden_tags_check"] == "PASS" else "❌"
            mn    = "✅" if not r["missing_new_tags"] else f"❌{r['missing_new_tags']}"
            rm    = "✅" if not r["removed_old_tags"] else f"❌{r['removed_old_tags']}"
            age   = "✅" if r["age_tags_check"] == "PASS" else "❌"
            tc    = r["title_changed"]
            st    = r["status_after"]
            v     = "✅ PASS" if r["final_verdict"] == "PASS" else "❌ FAIL"
            f.write(f"| {i} | `{r['product_id']}` | {title} | {r['before_tags_count']} | +{new_n} | {r['after_tags_count']} | {fbd} | {mn} | {rm} | {age} | {tc} | {st} | {v} |\n")

        f.write(f"\n---\n\n## Per-Product Detail\n\n")
        for r in rows:
            pid = r["product_id"]
            f.write(f"### {pid} — {r['title_from_shopify']}\n\n")
            f.write(f"**status_before:** `{r['status_before']}`  \n")
            f.write(f"**before_tags ({r['before_tags_count']}):** `{', '.join(r['before_tags'])}`  \n")
            f.write(f"**proposed_new_tags:** `{', '.join(r['proposed_new_tags'])}`  \n")
            f.write(f"**final_tags_before_write ({len(r['final_tags_before_write'])}):** `{', '.join(r['final_tags_before_write'])}`  \n")
            f.write(f"**after_tags ({r['after_tags_count']}):** `{', '.join(r['after_tags'])}`  \n")
            f.write(f"**missing_new_tags:** `{r['missing_new_tags'] or 'none'}`  \n")
            f.write(f"**removed_old_tags:** `{r['removed_old_tags'] or 'none'}`  \n")
            f.write(f"**unexpected_tags:** `{r['unexpected_tags'] or 'none'}`  \n")
            f.write(f"**allowed_values_check:** `{r['allowed_values_check']}`  \n")
            f.write(f"**forbidden_tags_check:** `{r['forbidden_tags_check']}`  \n")
            f.write(f"**age_tags_check:** `{r['age_tags_check']}`  \n")
            f.write(f"**title_changed:** `{r['title_changed']}`  \n")
            f.write(f"**status_after:** `{r['status_after']}`  \n")
            f.write(f"**rollback_needed:** `{r['rollback_needed']}`  \n")
            f.write(f"**final_verdict:** `{r['final_verdict']}`  \n\n")

        f.write(f"---\n\n## Verdict\n\n**{overall}**\n\n")
        f.write(f"pass={result['pass_count']} | fail={result['fail_count']} | written={result['total_written']}\n")

    log(f"[saved] {VERIFY_MD}")

# ── entry ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run","live"], required=True)
    parser.add_argument("--max-products", type=int, default=20)
    args = parser.parse_args()

    with open(PLAN_FILE, encoding="utf-8") as f:
        plan = json.load(f)

    log(f"[plan] {plan['recommended_batch_size']} in batch | token_suffix={plan['token_suffix']}")
    log(f"[mode] {args.mode} | max={args.max_products}")

    if args.mode == "dry-run":
        ok, _, _ = run_dry_run(plan, args.max_products)
        sys.exit(0 if ok else 1)
    else:
        ok = run_live(plan, args.max_products)
        sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
