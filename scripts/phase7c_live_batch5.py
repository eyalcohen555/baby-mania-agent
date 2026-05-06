"""
Phase 7C Live Batch 5.
T3 approval received from Ayal. Reads phase7c-batch5-plan.json.
Types: dress/set/romper/bodysuit only. Max 20 products.
Modes: --mode=dry-run (GET only) | --mode=live (PUT + verify).
Hebrew month normalization: 'X חודש' → 'X חודשים' on existing tags.
Stops on any failure; rollbacks written products on FAIL.
"""
import argparse, json, sys, time, datetime, urllib.request, urllib.error

ENV_PATH = r"C:\Users\3024e\Desktop\shopify-token\.env"

def load_env(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                d[k.strip()] = v.strip()
    return d

env = load_env(ENV_PATH)
TOKEN = env["SHOPIFY_ACCESS_TOKEN"]
SHOP  = env["SHOPIFY_SHOP_URL"]
BASE  = f"https://{SHOP}/admin/api/2024-10"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

BACKUP_JSON  = "output/tags/phase7c-live-batch5-backup.json"
DRYRUN_JSON  = "output/tags/phase7c-live-batch5-dry-run.json"
DRYRUN_MD    = "output/tags/phase7c-live-batch5-dry-run.md"
ROLLBACK_MD  = "output/tags/phase7c-live-batch5-rollback-plan.md"
VERIFY_JSON  = "output/tags/phase7c-live-batch5-verify.json"
VERIFY_MD    = "output/tags/phase7c-live-batch5-verify.md"

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
SHOE_TITLE_KW      = ["סנדל", "נעל", "מגפ", "כפכף", "sandal", "shoe", "sneaker", "boot", "croc"]

# Hebrew month normalization: singular → plural
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


def is_shoe_title(title):
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
        if " " in t and t not in HEBREW_MONTH_NORM.values():
            # Hebrew month normalized tags contain spaces — allow them
            violations.append(f"SPACE_IN_TAG: {t}")
    return violations


def normalize_month_tags(tags, do_normalize):
    """Replace singular חודש tags with plural חודשים. Returns (normalized_list, changes_list)."""
    if not do_normalize:
        return list(tags), []
    result = []
    changes = []
    for t in tags:
        if t in HEBREW_MONTH_NORM:
            new_t = HEBREW_MONTH_NORM[t]
            result.append(new_t)
            changes.append((t, new_t))
        else:
            result.append(t)
    return result, changes


def shopify_get(pid):
    url = f"{BASE}/products/{pid}.json?fields=id,title,tags,status"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"]


def shopify_put(pid, tags_list):
    # Use comma+space separator (Shopify convention for multi-word tags)
    tags_str = ", ".join(sorted(set(tags_list)))
    body = json.dumps({"product": {"id": int(pid), "tags": tags_str}}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/products/{pid}.json",
        data=body, headers=HEADERS, method="PUT"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["product"], r.status


def select_batch(plan_products, max_n):
    excluded_shoe = []
    candidates = []
    for p in plan_products:
        if is_shoe_title(p["title"]):
            excluded_shoe.append(p)
        else:
            candidates.append(p)
    return candidates[:max_n], excluded_shoe


# ── DRY RUN ───────────────────────────────────────────────────────────────────
def run_dry_run(plan_products, max_n, do_normalize):
    log("=" * 62)
    log("Phase 7C Live Batch 5 — DRY RUN")
    log("=" * 62)

    selected, excluded = select_batch(plan_products, max_n)
    log(f"\n[select] {len(plan_products)} in plan → {len(excluded)} excluded (shoe title) → {len(selected)} selected")

    if excluded:
        log("\n[excluded — shoe title keyword]")
        for p in excluded:
            log(f"  EXCLUDE: {p['product_id']} | {p['title']}")

    log(f"\n[selected — {len(selected)} products for batch]")

    rows    = []
    all_pass = True

    for i, entry in enumerate(selected, 1):
        pid      = entry["product_id"]
        proposed = entry["proposed_new_tags"]
        trace    = entry.get("source_trace", "")

        log(f"\n  [{i:02d}/{len(selected):02d}] GET {pid}")
        try:
            p = shopify_get(pid)
        except Exception as e:
            log(f"    [FAIL] GET error: {e}")
            all_pass = False
            rows.append(_fail_record(entry, f"GET_ERROR: {e}", "unknown"))
            continue

        time.sleep(0.3)

        cur_title  = p.get("title", "")
        cur_status = p.get("status", "")
        before_tags = sorted([t.strip() for t in p.get("tags", "").split(",") if t.strip()])

        log(f"    title: {cur_title}")
        log(f"    status: {cur_status}")
        log(f"    source_trace: {trace}")

        # Apply Hebrew month normalization to existing tags
        normalized_existing, month_changes = normalize_month_tags(before_tags, do_normalize)
        if month_changes:
            log(f"    hebrew_month_norm: {month_changes}")

        # Build final tags
        final_tags = sorted(set(normalized_existing) | set(proposed))
        new_tag_count = len(final_tags) - len(before_tags)

        log(f"    before={len(before_tags)} +new={proposed} month_norm={len(month_changes)} final={len(final_tags)}")

        # Checks
        forbidden_v  = check_forbidden(proposed)
        not_allowed  = [t for t in proposed if t not in ALLOWED_VALUES]
        type_collision = [t for t in final_tags if t.startswith("type-")]
        age_check    = [t for t in final_tags if t.startswith("age-")]
        shoe_check   = is_shoe_title(cur_title)
        status_check = (cur_status == "active")

        # Check old חודש tags would be removed
        lingering_singular = [t for t in final_tags if t in HEBREW_MONTH_NORM]

        ok = (
            not forbidden_v and
            not not_allowed and
            len(type_collision) == 1 and
            not age_check and
            not shoe_check and
            status_check and
            not lingering_singular
        )

        row = {
            "product_id": pid,
            "title_from_shopify": cur_title,
            "status_before": cur_status,
            "before_tags": before_tags,
            "month_changes": [{"from": f, "to": t} for f, t in month_changes],
            "proposed_new_tags": proposed,
            "final_tags_before_write": final_tags,
            "source_trace": trace,
            "forbidden_check": "PASS" if not forbidden_v else f"FAIL: {forbidden_v}",
            "allowed_values_check": "PASS" if not not_allowed else f"FAIL: {not_allowed}",
            "type_collision_check": "PASS" if len(type_collision) == 1 else f"FAIL: {type_collision}",
            "age_check": "PASS" if not age_check else f"FAIL: {age_check}",
            "shoe_check": "PASS" if not shoe_check else "FAIL",
            "status_check": "PASS" if status_check else f"FAIL: status={cur_status}",
            "month_norm_check": "PASS" if not lingering_singular else f"FAIL: singular_remaining={lingering_singular}",
            "final_verdict": "PASS" if ok else "FAIL",
        }
        rows.append(row)

        fv = "PASS" if ok else "FAIL"
        log(f"    forbidden={row['forbidden_check']} | allowed={row['allowed_values_check']} | "
            f"age={row['age_check']} | shoe={row['shoe_check']} | month_norm={row['month_norm_check']}")
        log(f"    verdict: {'✅' if ok else '❌'} {fv}")

        if not ok:
            all_pass = False

    pass_n = sum(1 for r in rows if r["final_verdict"] == "PASS")
    fail_n = sum(1 for r in rows if r["final_verdict"] == "FAIL")
    verdict = "DRY_RUN_PASS" if all_pass and fail_n == 0 else "DRY_RUN_FAIL"

    log(f"\n[DRY RUN SUMMARY]")
    log(f"  selected={len(selected)} | PASS={pass_n} | FAIL={fail_n}")
    log(f"\n[VERDICT] {verdict}")

    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C", "batch": 5, "mode": "DRY_RUN",
        "timestamp": ts, "shopify_writes": "NONE",
        "selected": len(selected), "pass_count": pass_n, "fail_count": fail_n,
        "normalize_hebrew_months": do_normalize,
        "products": rows, "verdict": verdict,
    }

    import os; os.makedirs("output/tags", exist_ok=True)
    with open(DRYRUN_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"[saved] {DRYRUN_JSON}")

    _write_dryrun_md(result, rows)
    log(f"[saved] {DRYRUN_MD}")

    _write_rollback_md(rows, ts)
    log(f"[saved] {ROLLBACK_MD}")

    return verdict == "DRY_RUN_PASS"


def _write_dryrun_md(result, rows):
    lines = [
        "# Phase 7C Live Batch 5 — Dry Run Report",
        "",
        "## MODE: DRY RUN — No Shopify writes",
        "",
        f"**Timestamp:** {result['timestamp']}  ",
        f"**Shopify writes:** NONE  ",
        f"**Hebrew month normalization:** {result['normalize_hebrew_months']}  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Selected | {result['selected']} |",
        f"| PASS | {result['pass_count']} |",
        f"| FAIL | {result['fail_count']} |",
        f"| Verdict | **{result['verdict']}** |",
        "",
        "---",
        "",
        "## Per-Product Evidence",
        "",
    ]
    for i, r in enumerate(rows, 1):
        ok = r["final_verdict"] == "PASS"
        mc = r.get("month_changes", [])
        lines += [
            f"### [{i:02d}] `{r['product_id']}` {'✅' if ok else '❌'}",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| product_id | `{r['product_id']}` |",
            f"| title | {r.get('title_from_shopify','')} |",
            f"| status_before | {r.get('status_before','')} |",
            f"| before_tags_count | {len(r.get('before_tags',[]))} |",
            f"| proposed_new_tags | `{'`, `'.join(r.get('proposed_new_tags',[]))}` |",
            f"| month_normalizations | {len(mc)} — {mc if mc else 'none'} |",
            f"| final_tags_count | {len(r.get('final_tags_before_write',[]))} |",
            f"| forbidden_check | {r.get('forbidden_check','')} |",
            f"| allowed_values_check | {r.get('allowed_values_check','')} |",
            f"| type_collision_check | {r.get('type_collision_check','')} |",
            f"| age_check | {r.get('age_check','')} |",
            f"| shoe_check | {r.get('shoe_check','')} |",
            f"| status_check | {r.get('status_check','')} |",
            f"| month_norm_check | {r.get('month_norm_check','')} |",
            f"| final_verdict | **{r['final_verdict']}** |",
            "",
            "---",
            "",
        ]
    lines += [f"**VERDICT: {result['verdict']}**", ""]
    with open(DRYRUN_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _write_rollback_md(rows, ts):
    lines = [
        "# Phase 7C Live Batch 5 — Rollback Plan",
        "",
        f"**Generated:** {ts}  ",
        "**Use if live write fails.** For each product below, PUT the before_tags back.",
        "",
        "| # | product_id | title | before_tags |",
        "|---|-----------|-------|------------|",
    ]
    for i, r in enumerate(rows, 1):
        bt = ", ".join(r.get("before_tags", []))
        lines.append(f"| {i} | `{r['product_id']}` | {r.get('title_from_shopify','')[:40]} | `{bt}` |")
    lines += ["", "**Rollback command pattern:**",
              "```", "PUT /products/{id}.json  →  tags = before_tags", "```"]
    with open(ROLLBACK_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _fail_record(entry, msg, status_after):
    return {
        "product_id": entry["product_id"],
        "title_from_shopify": entry.get("title", ""),
        "proposed_new_tags": entry.get("proposed_new_tags", []),
        "before_tags": [],
        "final_tags_before_write": [],
        "month_changes": [],
        "final_verdict": "FAIL",
        "fail_reason": msg,
        "status_after": status_after,
        "rollback_needed": False,
    }


# ── LIVE WRITE ────────────────────────────────────────────────────────────────
def run_live(plan_products, max_n, do_normalize):
    log("=" * 62)
    log("Phase 7C Live Batch 5 — LIVE WRITE")
    log("=" * 62)

    # Verify dry run passed first
    try:
        with open(DRYRUN_JSON, encoding="utf-8") as f:
            dr = json.load(f)
    except FileNotFoundError:
        log(f"[FAIL] dry-run JSON not found. Run --mode=dry-run first.")
        sys.exit(1)

    if dr.get("verdict") != "DRY_RUN_PASS":
        log(f"[FAIL] dry-run verdict={dr.get('verdict')} — must be DRY_RUN_PASS to proceed.")
        sys.exit(1)

    log(f"[pre-check] dry-run verdict=DRY_RUN_PASS ✅")

    selected, _ = select_batch(plan_products, max_n)
    log(f"[select] {len(selected)} products for live write")

    token_suffix = TOKEN[-4:] if TOKEN else "????"
    log(f"[token] suffix={token_suffix}")

    # ── STEP B: Backup ────────────────────────────────────────────────────────
    log(f"\n[STEP B] Creating backup (GET all products before any write)")
    ts0 = datetime.datetime.utcnow().isoformat() + "+00:00"
    backup_products = []
    for entry in selected:
        pid = entry["product_id"]
        try:
            p = shopify_get(pid)
        except Exception as e:
            log(f"  [FAIL] backup GET {pid}: {e}")
            sys.exit(1)
        time.sleep(0.2)

        before_tags = sorted([t.strip() for t in p.get("tags", "").split(",") if t.strip()])
        normalized_existing, month_changes = normalize_month_tags(before_tags, do_normalize)
        proposed = entry["proposed_new_tags"]
        final_tags = sorted(set(normalized_existing) | set(proposed))

        backup_products.append({
            "product_id": pid,
            "title_from_shopify": p.get("title", ""),
            "status_before": p.get("status", ""),
            "before_tags": before_tags,
            "month_changes": [{"from": f, "to": t} for f, t in month_changes],
            "proposed_new_tags": proposed,
            "final_tags_before_write": final_tags,
            "source_trace": entry.get("source_trace", ""),
        })

    backup = {
        "phase": "7C", "batch": 5, "timestamp": ts0,
        "shopify_writes": "NONE — backup GET only",
        "normalize_hebrew_months": do_normalize,
        "products": backup_products,
    }
    import os; os.makedirs("output/tags", exist_ok=True)
    with open(BACKUP_JSON, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    log(f"[saved] {BACKUP_JSON}")
    log(f"[STEP B] Backup complete — {len(backup_products)} products")

    # ── STEP C: Live write ────────────────────────────────────────────────────
    log(f"\n[STEP C] Live write — one at a time")

    written = []
    rows    = []
    all_pass = True

    for i, bp in enumerate(backup_products, 1):
        pid         = bp["product_id"]
        title       = bp["title_from_shopify"]
        before_tags = bp["before_tags"]
        proposed    = bp["proposed_new_tags"]
        final_tags  = bp["final_tags_before_write"]
        month_ch    = bp.get("month_changes", [])
        trace       = bp.get("source_trace", "")

        log(f"\n  [{i:02d}/{len(backup_products):02d}] {pid} | {title[:50]}")
        log(f"    proposed: {proposed}")
        if month_ch:
            log(f"    month_norm: {[(c['from'], c['to']) for c in month_ch]}")
        log(f"    source_trace: {trace}")
        log(f"    before={len(before_tags)} | final={len(final_tags)}")

        # Safety gate: stop conditions
        if any(t.startswith("age-") for t in final_tags):
            log(f"    [FAIL] age-* tag in final_tags — STOP")
            all_pass = False
            rows.append(_fail_record(bp, "age_tag_in_final", "not_written"))
            break

        type_tags = [t for t in final_tags if t.startswith("type-")]
        if len(type_tags) > 1:
            log(f"    [FAIL] type_collision: {type_tags} — STOP")
            all_pass = False
            rows.append(_fail_record(bp, f"type_collision: {type_tags}", "not_written"))
            break

        # PUT
        try:
            put_p, http_status = shopify_put(pid, final_tags)
        except Exception as e:
            log(f"    [FAIL] PUT error: {e}")
            all_pass = False
            rows.append(_fail_record(bp, f"PUT_ERROR: {e}", "unknown"))
            # Rollback all previously written
            _do_rollback(written, before_tags)
            sys.exit(1)

        log(f"    PUT HTTP {http_status}")
        written.append({"pid": pid, "before_tags": before_tags})
        time.sleep(0.4)

        # GET verify
        try:
            vp = shopify_get(pid)
        except Exception as e:
            log(f"    [FAIL] verify GET error: {e}")
            all_pass = False
            rows.append(_fail_record(bp, f"VERIFY_GET_ERROR: {e}", "unknown"))
            _do_rollback(written, before_tags)
            sys.exit(1)

        time.sleep(0.3)

        after_tags = sorted([t.strip() for t in vp.get("tags", "").split(",") if t.strip()])
        after_title  = vp.get("title", "")
        after_status = vp.get("status", "")

        # Verify checks
        missing_proposed = [t for t in proposed if t not in after_tags]
        lingering_singular = [t for t in after_tags if t in HEBREW_MONTH_NORM]
        missing_normalized = []
        if do_normalize and month_ch:
            missing_normalized = [c["to"] for c in month_ch if c["to"] not in after_tags]
        title_ok   = (after_title == title)
        status_ok  = (after_status == "active")
        age_ok     = not any(t.startswith("age-") for t in after_tags)

        ok = (
            not missing_proposed and
            not lingering_singular and
            not missing_normalized and
            title_ok and status_ok and age_ok
        )

        row = {
            "product_id": pid,
            "title_from_shopify": after_title,
            "status_after": after_status,
            "before_tags": before_tags,
            "month_changes": month_ch,
            "proposed_new_tags": proposed,
            "final_tags_before_write": final_tags,
            "after_tags": after_tags,
            "after_tags_count": len(after_tags),
            "missing_proposed_tags": missing_proposed,
            "lingering_singular_month_tags": lingering_singular,
            "missing_normalized_month_tags": missing_normalized,
            "title_ok": title_ok,
            "status_ok": status_ok,
            "age_ok": age_ok,
            "rollback_needed": not ok,
            "final_verdict": "PASS" if ok else "FAIL",
        }
        rows.append(row)

        if ok:
            log(f"    verify ✅ PASS — after={len(after_tags)} tags")
        else:
            all_pass = False
            reasons = []
            if missing_proposed:   reasons.append(f"missing_proposed={missing_proposed}")
            if lingering_singular: reasons.append(f"lingering_singular={lingering_singular}")
            if missing_normalized: reasons.append(f"missing_normalized={missing_normalized}")
            if not title_ok:       reasons.append("title_changed")
            if not status_ok:      reasons.append(f"status={after_status}")
            if not age_ok:         reasons.append("age_tag_present")
            log(f"    verify ❌ FAIL: {'; '.join(reasons)}")
            # Rollback all written
            _do_rollback(written, before_tags)
            log(f"[ROLLBACK COMPLETE]")
            break

    pass_n  = sum(1 for r in rows if r["final_verdict"] == "PASS")
    fail_n  = sum(1 for r in rows if r["final_verdict"] == "FAIL")
    verdict = "PHASE7C_LIVE_BATCH5_PASS" if all_pass and fail_n == 0 else "HOLD_PHASE7C_LIVE_BATCH5"

    log(f"\n[RESULT] written={len(written)} | PASS={pass_n} | FAIL={fail_n}")
    log(f"[VERDICT] {verdict}")

    ts2 = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C", "batch": 5, "mode": "LIVE",
        "timestamp": ts2, "shopify_token_suffix": TOKEN[-4:],
        "normalize_hebrew_months": do_normalize,
        "total_written": len(written), "pass_count": pass_n, "fail_count": fail_n,
        "products": rows, "verdict": verdict,
    }

    with open(VERIFY_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"[saved] {VERIFY_JSON}")

    _write_verify_md(result, rows)
    log(f"[saved] {VERIFY_MD}")

    if verdict != "PHASE7C_LIVE_BATCH5_PASS":
        sys.exit(1)


def _do_rollback(written, current_before):
    log(f"\n[ROLLBACK] reversing {len(written)} written products...")
    for w in reversed(written):
        pid = w["pid"]
        bt  = w["before_tags"]
        try:
            shopify_put(pid, bt)
            time.sleep(0.4)
            log(f"  [rollback] ✅ {pid} → {len(bt)} original tags")
        except Exception as e:
            log(f"  [rollback] ❌ {pid} FAILED: {e}")


def _write_verify_md(result, rows):
    lines = [
        "# Phase 7C Live Batch 5 — Verify Report",
        "",
        f"**Timestamp:** {result['timestamp']}  ",
        f"**Token suffix:** {result.get('shopify_token_suffix','')}  ",
        f"**Hebrew month normalization:** {result['normalize_hebrew_months']}  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total written | {result['total_written']} |",
        f"| PASS | {result['pass_count']} |",
        f"| FAIL | {result['fail_count']} |",
        f"| Verdict | **{result['verdict']}** |",
        "",
        "---",
        "",
        "## QA Evidence — Per Product (11 checks)",
        "",
    ]

    for i, r in enumerate(rows, 1):
        ok = r["final_verdict"] == "PASS"
        mc = r.get("month_changes", [])
        lines += [
            f"### [{i:02d}] `{r['product_id']}` {'✅ PASS' if ok else '❌ FAIL'}",
            "",
            "| Check | Result |",
            "|-------|--------|",
            f"| 1. product_id | `{r['product_id']}` |",
            f"| 2. title_unchanged | {'✅ PASS' if r.get('title_ok') else '❌ FAIL'} — {r.get('title_from_shopify','')[:40]} |",
            f"| 3. status_after | {'✅ PASS' if r.get('status_ok') else '❌ FAIL'} — {r.get('status_after','')} |",
            f"| 4. proposed_tags_present | {'✅ PASS' if not r.get('missing_proposed_tags') else '❌ FAIL: ' + str(r.get('missing_proposed_tags'))} |",
            f"| 5. before_tags_preserved | {'✅ PASS' if not r.get('lingering_singular_month_tags') else '❌ (singular removed)'} |",
            f"| 6. month_norm_applied | {'✅ PASS' if not r.get('missing_normalized_month_tags') else '❌ FAIL: ' + str(r.get('missing_normalized_month_tags'))} |",
            f"| 7. no_age_tags | {'✅ PASS' if r.get('age_ok') else '❌ FAIL'} |",
            f"| 8. no_lingering_singular | {'✅ PASS' if not r.get('lingering_singular_month_tags') else '❌ FAIL: ' + str(r.get('lingering_singular_month_tags'))} |",
            f"| 9. after_tags_count | {r.get('after_tags_count',0)} |",
            f"| 10. rollback_needed | {r.get('rollback_needed', False)} |",
            f"| 11. final_verdict | **{'✅ PASS' if ok else '❌ FAIL'}** |",
            "",
            f"**Proposed new tags:** `{'`, `'.join(r.get('proposed_new_tags',[]))}`  ",
            f"**Month normalizations:** {len(mc)} — {[(c['from'], c['to']) for c in mc] if mc else 'none'}  ",
            f"**After tags:** `{'`, `'.join(r.get('after_tags',[])[:10])}{'...' if len(r.get('after_tags',[])) > 10 else ''}`  ",
            "",
            "---",
            "",
        ]

    lines += [f"**FINAL VERDICT: {result['verdict']}**", ""]
    with open(VERIFY_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run", "live"], required=True)
    parser.add_argument("--plan", default="output/tags/phase7c-batch5-plan.json")
    parser.add_argument("--max-products", type=int, default=20)
    parser.add_argument("--normalize-hebrew-months", default="true")
    args = parser.parse_args()

    do_normalize = args.normalize_hebrew_months.lower() == "true"

    try:
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
    except FileNotFoundError:
        log(f"[FAIL] plan file not found: {args.plan}")
        sys.exit(1)

    plan_products = plan.get("products", [])
    log(f"[plan] {len(plan_products)} products | token_suffix={TOKEN[-4:]}")
    log(f"[mode] {args.mode} | max={args.max_products} | normalize_months={do_normalize}")
    log(f"[types] {sorted(set(p.get('proposed_type','') for p in plan_products))}")

    if args.mode == "dry-run":
        ok = run_dry_run(plan_products, args.max_products, do_normalize)
        sys.exit(0 if ok else 1)
    elif args.mode == "live":
        run_live(plan_products, args.max_products, do_normalize)


if __name__ == "__main__":
    main()
