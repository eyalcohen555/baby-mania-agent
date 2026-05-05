"""
Phase 7C Live Batch 2 — hat + coat candidates only.
T3 approval received from Ayal. Max 20 products.
Re-classifies all active products (batch1 products are auto-excluded as already-tagged).
Modes: --mode=dry-run | --mode=live. --types=type-hat,type-coat
"""
import argparse, json, sys, time, datetime, re, urllib.request, urllib.error

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
BACKUP_FILE = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-backup.json"
DRYRUN_JSON = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-dry-run.json"
DRYRUN_MD   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-dry-run.md"
ROLLBACK_MD = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-rollback-plan.md"
VERIFY_JSON = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-verify.json"
VERIFY_MD   = r"C:\Projects\baby-mania-agent\output\tags\phase7c-live-batch2-verify.md"

# ── taxonomy ──────────────────────────────────────────────────────────────────
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

LAYER67_TYPE_TAGS = {f"type-{t}" for t in [
    "set","romper","dress","bodysuit","hat","swimwear","coat","pants","top",
    "shoes","sandals","sneakers","accessory","reborn-doll","boots","toy","swimming-ring",
]}

SHOE_TITLE_KW = ["סנדל", "נעל", "מגפ", "כפכף", "sandal", "shoe", "sneaker", "boot", "croc"]

# Titles that contain a hat/coat keyword but are NOT hats/coats (false-positive blocker)
NOT_HAT_TITLE_KW  = ["מגבת", "תיק", "משפך", "שמיכה", "ספוג", "towel", "bag", "blanket", "sponge"]
NOT_COAT_TITLE_KW = ["שמיכה", "מגבת", "blanket", "towel"]

# ── classification rules (same as planning script) ────────────────────────────
TYPE_RULES = {
    "type-set": {"keywords": ["set", "סט", "חליפה", "חליפת", "2pcs", "2-pcs", "pcs", "suit", "outfit"], "min_conf": 0.88},
    "type-romper": {"keywords": ["romper", "אוברול", "סרבל", "bodysuit one-piece", "jumpsuit"], "min_conf": 0.88},
    "type-dress": {"keywords": ["dress", "שמלה", "שמלת"], "min_conf": 0.90},
    "type-bodysuit": {"keywords": ["bodysuit", "בגד גוף", "בגד-גוף"], "min_conf": 0.90},
    "type-hat": {"keywords": ["כובע", "hat", "cap", "beanie"], "min_conf": 0.92},
    "type-swimwear": {"keywords": ["בגד ים", "swimsuit", "swimwear", "bikini"], "min_conf": 0.92},
    "type-coat": {"keywords": ["מעיל", "coat", "jacket", "ז'קט", "ז'קט"], "min_conf": 0.90},
    "type-pants": {"keywords": ["מכנסי", "מכנס", "pants", "trousers", "legging"], "min_conf": 0.90},
    "type-top": {"keywords": ["חולצת", "חולצה", "top", "shirt", "blouse", "tee"], "min_conf": 0.90},
}

GENDER_RULES = {
    "gender-girl": {"title_kw": ["girl", "girls", "בנות", "לבנות", "ילדה", "נסיכה"], "handle_kw": ["girl", "girls"], "tag_kw": ["girl", "girls"]},
    "gender-boy":  {"title_kw": ["boy", "boys", "בנים", "לבנים", "ילד"], "handle_kw": ["boy", "boys"], "tag_kw": ["boy", "boys"]},
    "gender-neutral": {"title_kw": ["unisex", "יוניסקס", "neutral", "boys & girls"], "handle_kw": ["unisex", "neutral"], "tag_kw": ["unisex", "neutral"]},
}

OCC_RULES = {
    "occ-gift":     ["gift", "מתנה", "shower", "baby shower"],
    "occ-everyday": ["everyday", "daily", "יומיומי", "casual", "leisure"],
    "occ-seasonal": ["winter", "summer", "seasonal", "חורף", "קיץ", "אביב"],
}

FORBIDDEN_RE = re.compile(
    r"^age-|season-unknown|size-unknown|gender-unknown|\d+[A-Za-z]+\d+[A-Za-z]|[A-Za-z]\d+$|\s",
    re.UNICODE
)

# ── helpers ───────────────────────────────────────────────────────────────────
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
        if " " in t:
            violations.append(f"SPACE_IN_TAG: {t}")
    return violations

def score_type(title, handle, tags):
    t_low = title.lower()
    h_low = handle.lower()
    for typ, rule in TYPE_RULES.items():
        for kw in rule["keywords"]:
            if kw.lower() in t_low or kw.lower() in h_low:
                src = "title" if kw.lower() in t_low else "handle"
                return typ, rule["min_conf"], src
    return None, 0.0, None

def score_gender(title, handle, tags):
    t_low  = title.lower()
    h_low  = handle.lower()
    ta_set = {tg.lower() for tg in tags}
    for gender, rule in GENDER_RULES.items():
        for kw in rule["title_kw"]:
            if kw.lower() in t_low:
                return gender, 0.90, "title"
        for kw in rule["handle_kw"]:
            if kw.lower() in h_low:
                return gender, 0.90, "handle"
        for kw in rule["tag_kw"]:
            for tg in ta_set:
                if kw.lower() in tg:
                    return gender, 0.88, "existing_tag"
    return None, 0.0, None

def score_occ(title, tags):
    t_low  = title.lower()
    ta_set = {tg.lower() for tg in tags}
    found  = {}
    for occ, kws in OCC_RULES.items():
        for kw in kws:
            if kw.lower() in t_low:
                found[occ] = "title"
                break
            for tg in ta_set:
                if kw.lower() in tg:
                    found[occ] = "existing_tag"
                    break
    return list(found.items())

def classify_product(p, allowed_types):
    pid    = str(p["id"])
    title  = p.get("title", "")
    handle = p.get("handle", "")
    raw_tags = [t.strip() for t in p.get("tags", "").split(",") if t.strip()]
    tags_set = set(raw_tags)

    if p.get("status") != "active":
        return None

    # already has a type tag → skip
    if LAYER67_TYPE_TAGS & tags_set:
        return None

    # shoe title blocker
    if is_shoe_title(title):
        return None

    typ, type_conf, type_src = score_type(title, handle, raw_tags)

    # must be in allowed_types and meet confidence
    if not typ or type_conf < 0.88:
        return None
    if typ not in allowed_types:
        return None

    # EU shoe blocker (redundant but explicit)
    if typ in ("type-shoes", "type-sandals", "type-sneakers"):
        return None

    # False-positive blocker: hat/coat keyword matched but product is NOT a hat/coat
    t_low = title.lower()
    if typ == "type-hat" and any(kw.lower() in t_low for kw in NOT_HAT_TITLE_KW):
        return None
    if typ == "type-coat" and any(kw.lower() in t_low for kw in NOT_COAT_TITLE_KW):
        return None

    gender, gender_conf, gender_src = score_gender(title, handle, raw_tags)
    occs = score_occ(title, raw_tags)

    proposed = [typ]
    if gender:
        proposed.append(gender)
    for occ, _ in occs:
        proposed.append(occ)

    # forbidden check
    viols = check_forbidden(proposed)
    if viols:
        return None

    # allowed_values check
    if any(t not in ALLOWED_VALUES for t in proposed):
        return None

    return {
        "product_id": pid,
        "title": title,
        "handle": handle,
        "proposed_type": typ,
        "type_conf": type_conf,
        "type_source": type_src,
        "proposed_gender": gender,
        "gender_conf": gender_conf,
        "gender_source": gender_src,
        "proposed_occs": [o for o, _ in occs],
        "all_proposed_tags": proposed,
        "current_tags": raw_tags,
        "current_tags_count": len(raw_tags),
        "risk_level": "LOW",
        "confidence": type_conf,
    }

def fetch_all_active_products():
    products = []
    url = f"{BASE}/products.json?limit=250&status=active&fields=id,title,handle,tags,status,variants"
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            batch = data.get("products", [])
            products.extend(batch)
            # pagination
            link = r.headers.get("Link", "")
            url = None
            for part in link.split(","):
                if 'rel="next"' in part:
                    m = re.search(r'<([^>]+)>', part)
                    if m:
                        url = m.group(1)
    return products

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

# ── DRY RUN ───────────────────────────────────────────────────────────────────
def run_dry_run(candidates, max_n):
    log("=" * 60)
    log("Phase 7C Live Batch 2 — DRY RUN (hat + coat only)")
    log("=" * 60)

    selected = candidates[:max_n]
    log(f"\n[select] {len(candidates)} SAFE hat/coat candidates → {len(selected)} selected (max={max_n})")

    type_counts = {}
    for p in selected:
        type_counts[p["proposed_type"]] = type_counts.get(p["proposed_type"], 0) + 1
    for t, n in sorted(type_counts.items()):
        log(f"  {t}: {n}")

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
        status_live = live.get("status", "unknown")

        viols = check_forbidden(proposed)
        forbidden_ok = "PASS" if not viols else f"FAIL: {viols}"

        not_allowed = [t for t in proposed if t not in ALLOWED_VALUES]
        allowed_ok = "PASS" if not not_allowed else f"FAIL: {not_allowed}"

        existing_type = [t for t in cur_tags if t.startswith("type-")]
        type_ok = "PASS" if not existing_type else f"WARN: existing type {existing_type}"

        age_ok = "PASS" if not [t for t in proposed if t.startswith("age-")] else "FAIL"

        ok = (forbidden_ok == "PASS" and allowed_ok == "PASS" and
              age_ok == "PASS" and status_live == "active")

        row = {
            "product_id": pid,
            "title_from_shopify": live["title"],
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
            failures.append(f"{pid}: FAIL forbidden={forbidden_ok} allowed={allowed_ok} age={age_ok}")

        log(f"    title: {live['title']}")
        log(f"    status: {status_live} | before={len(cur_tags)} proposed={len(proposed)} final={len(final_tags)}")
        log(f"    new_tags: {new_tags}")
        log(f"    forbidden={forbidden_ok} | allowed={allowed_ok} | age={age_ok}")
        log(f"    verdict: {'✅ PASS' if ok else '❌ FAIL'}")

    pass_n = sum(1 for r in dry_rows if r["dry_run_verdict"] == "PASS")
    fail_n = sum(1 for r in dry_rows if r["dry_run_verdict"] == "FAIL")

    log(f"\n[DRY RUN SUMMARY]  selected={len(selected)} | PASS={pass_n} | FAIL={fail_n}")
    overall = "DRY_RUN_PASS" if not failures else "DRY_RUN_FAIL"
    if failures:
        log("[DRY RUN FAIL] blocking issues:")
        for ff in failures:
            log(f"  {ff}")
    log(f"[VERDICT] {overall}")

    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C-batch2",
        "type": "live_batch2_dry_run",
        "timestamp": ts,
        "t3_approval": "Ayal approved Phase 7C Live Batch 2 — hat + coat only",
        "shopify_writes": "NONE — dry run only",
        "types_filter": ["type-hat", "type-coat"],
        "safe_candidates_found": len(candidates),
        "selected": len(selected),
        "dry_run_pass": pass_n,
        "dry_run_fail": fail_n,
        "products": dry_rows,
        "verdict": overall,
    }
    with open(DRYRUN_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"[saved] {DRYRUN_JSON}")

    with open(DRYRUN_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 7C Live Batch 2 — Dry Run (hat + coat)\n\n")
        f.write(f"**Date:** {ts[:10]}  \n")
        f.write(f"**Shopify writes:** NONE  \n")
        f.write(f"**SAFE hat/coat candidates:** {len(candidates)} → selected {len(selected)}  \n\n")
        f.write("---\n\n## Dry Run Results\n\n")
        f.write("| # | product_id | title | type | conf | src | gender | proposed_tags | before | final | verdict |\n")
        f.write("|---|-----------|-------|------|------|-----|--------|--------------|--------|-------|--------|\n")
        for i, r in enumerate(dry_rows, 1):
            t = r["title_from_shopify"][:35]
            g = r["proposed_gender"] or "—"
            tags_str = ", ".join(r["all_proposed_tags"])
            v = "✅ PASS" if r["dry_run_verdict"] == "PASS" else "❌ FAIL"
            f.write(f"| {i} | `{r['product_id']}` | {t} | `{r['proposed_type']}` | {r['type_conf']} | {r['type_source']} | {g} | {tags_str} | {r['before_count']} | {r['final_count']} | {v} |\n")
        f.write(f"\n---\n\n## Verdict\n\n**{overall}**\n")
    log(f"[saved] {DRYRUN_MD}")

    with open(ROLLBACK_MD, "w", encoding="utf-8") as f:
        f.write(f"# Phase 7C Live Batch 2 — Rollback Plan\n\n")
        f.write(f"**Backup file:** `output/tags/phase7c-live-batch2-backup.json`  \n")
        f.write(f"**Trigger:** any product verify FAIL during live write  \n\n")
        f.write("## Protocol\n\n1. Stop immediately on first FAIL\n")
        f.write("2. Read backup — get `before_tags` for each written product\n")
        f.write("3. PUT back `before_tags` for each written product\n")
        f.write("4. GET verify rollback\n")
        f.write("5. Commit: `rollback(layer7): phase7c live batch2`\n\n")
        f.write(f"## Products ({len(selected)})\n\n")
        f.write("| product_id | title | proposed_tags |\n|-----------|-------|---------------|\n")
        for r in dry_rows:
            f.write(f"| `{r['product_id']}` | {r['title_from_shopify'][:40]} | {', '.join(r['all_proposed_tags'])} |\n")
    log(f"[saved] {ROLLBACK_MD}")

    return overall == "DRY_RUN_PASS", dry_rows, selected

# ── LIVE ──────────────────────────────────────────────────────────────────────
def run_live(candidates, max_n):
    log("=" * 60)
    log("Phase 7C Live Batch 2 — LIVE WRITE (hat + coat only)")
    log("=" * 60)

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

    selected = candidates[:max_n]
    log(f"[select] {len(selected)} products for live write")
    log(f"[token] suffix={TOKEN[-4:]}")

    # STEP B: backup
    log("\n[STEP B] Creating backup")
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
        sources = [{"tag": p["proposed_type"], "source": p["type_source"], "conf": p["type_conf"]}]
        if p["proposed_gender"]:
            sources.append({"tag": p["proposed_gender"], "source": p["gender_source"], "conf": p["gender_conf"]})
        for occ in p["proposed_occs"]:
            sources.append({"tag": occ, "source": "title_or_existing_tag", "conf": 0.85})
        backup_products.append({
            "product_id": pid,
            "title_from_shopify": live["title"],
            "status_before": live.get("status","unknown"),
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
        "phase": "Phase 7C live batch 2 pre-write backup",
        "t3_approval": "Ayal approved Phase 7C Live Batch 2 — hat + coat only",
        "shopify_writes_at_backup": "NONE",
        "products": backup_products,
    }
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    log(f"[BACKUP SAVED] {BACKUP_FILE}")

    # STEP C+D: write + verify
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

        for t in cur:
            if t not in final:
                msg = f"SAFETY_FAIL: tag '{t}' would be removed"
                log(f"    [FAIL] {msg}")
                failed_pid = pid
                verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
                break
        if failed_pid:
            break

        viols = check_forbidden(proposed)
        if viols:
            msg = f"FORBIDDEN: {viols}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
            break

        not_allowed = [t for t in proposed if t not in ALLOWED_VALUES]
        if not_allowed:
            msg = f"NOT_IN_ALLOWED_VALUES: {not_allowed}"
            log(f"    [FAIL] {msg}")
            failed_pid = pid
            verify_results.append(_fail_record(entry, msg, "NOT_WRITTEN"))
            break

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

        after_tags   = sorted([t.strip() for t in after_product.get("tags","").split(",") if t.strip()])
        after_title  = after_product.get("title","")
        after_status = after_product.get("status","")

        missing_new = [t for t in proposed if t not in after_tags]
        removed_old = [t for t in cur      if t not in after_tags]
        unexpected  = [t for t in after_tags if t not in final and t not in cur]
        title_changed = "NO" if after_title == title else "YES"
        age_tags = [t for t in after_tags if t.startswith("age-")]

        passed = (not missing_new and not removed_old and not unexpected and
                  title_changed == "NO" and after_status == "active" and not age_tags)
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
            "allowed_values_check": "PASS",
            "forbidden_tags_check": "PASS",
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
            if missing_new:  reasons.append(f"missing_new={missing_new}")
            if removed_old:  reasons.append(f"removed_old={removed_old}")
            if unexpected:   reasons.append(f"unexpected={unexpected}")
            if title_changed == "YES": reasons.append("title_changed")
            if after_status != "active": reasons.append(f"status={after_status}")
            if age_tags:     reasons.append(f"age_tags={age_tags}")
            log(f"    verify ❌ FAIL: {'; '.join(reasons)}")
            failed_pid = pid
            r["rollback_needed"] = "YES"
            break

    # rollback if failure
    if failed_pid and written:
        log(f"\n[ROLLBACK] failure at {failed_pid} — rolling back {len(written)} written products")
        for w in reversed(written):
            try:
                shopify_put(w["pid"], w["before_tags"])
                time.sleep(0.3)
                log(f"  rollback {w['pid']}: done")
            except Exception as e:
                log(f"  rollback {w['pid']}: ERROR {e}")

    pass_n = sum(1 for r in verify_results if r["final_verdict"] == "PASS")
    fail_n = sum(1 for r in verify_results if r["final_verdict"] == "FAIL")
    overall = "PHASE7C_LIVE_BATCH2_PASS" if not failed_pid else "HOLD_PHASE7C_LIVE_BATCH2"

    log(f"\n[RESULT] written={len(written)} | PASS={pass_n} | FAIL={fail_n}")
    log(f"[VERDICT] {overall}")

    ts2 = datetime.datetime.utcnow().isoformat() + "+00:00"
    result = {
        "phase": "7C-batch2",
        "type": "live_batch2_verify",
        "timestamp": ts2,
        "t3_approval": "Ayal approved Phase 7C Live Batch 2 — hat + coat only",
        "shopify_writes": f"{len(written)} products PUT",
        "types_filter": ["type-hat", "type-coat"],
        "total_selected": len(selected),
        "total_written": len(written),
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
    return overall == "PHASE7C_LIVE_BATCH2_PASS"

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
        "after_tags": [], "after_tags_count": 0,
        "missing_new_tags": entry["proposed_new_tags"],
        "removed_old_tags": [], "unexpected_tags": [],
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
        f.write(f"# Phase 7C Live Batch 2 — Verify Report (hat + coat)\n\n")
        f.write(f"**Date:** {ts}  \n**T3 approval:** {result['t3_approval']}  \n")
        f.write(f"**Shopify writes:** {result['shopify_writes']}  \n")
        f.write(f"**Written:** {result['total_written']} / {result['total_selected']}  \n")
        f.write(f"**Rollback triggered:** {'YES' if result['rollback_triggered'] else 'NO'}  \n\n---\n\n")
        f.write("## QA Table\n\n")
        f.write("| # | product_id | title | type | before | +new | after | forbidden | miss_new | removed | age | title_chg | status | verdict |\n")
        f.write("|---|-----------|-------|------|--------|------|-------|-----------|---------|---------|-----|-----------|--------|--------|\n")
        for i, r in enumerate(rows, 1):
            title = r["title_from_shopify"][:28]
            new_n = len(r["proposed_new_tags"])
            typ   = next((t for t in r["proposed_new_tags"] if t.startswith("type-")), "?")
            fbd   = "✅" if r["forbidden_tags_check"] == "PASS" else "❌"
            mn    = "✅" if not r["missing_new_tags"] else f"❌{r['missing_new_tags']}"
            rm    = "✅" if not r["removed_old_tags"] else f"❌{r['removed_old_tags']}"
            age   = "✅" if r["age_tags_check"] == "PASS" else "❌"
            v     = "✅ PASS" if r["final_verdict"] == "PASS" else "❌ FAIL"
            f.write(f"| {i} | `{r['product_id']}` | {title} | `{typ}` | {r['before_tags_count']} | +{new_n} | {r['after_tags_count']} | {fbd} | {mn} | {rm} | {age} | {r['title_changed']} | {r['status_after']} | {v} |\n")
        f.write(f"\n---\n\n## Per-Product Detail\n\n")
        for r in rows:
            f.write(f"### {r['product_id']} — {r['title_from_shopify']}\n\n")
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
        f.write(f"---\n\n## Verdict\n\n**{overall}**\n\npass={result['pass_count']} | fail={result['fail_count']} | written={result['total_written']}\n")
    log(f"[saved] {VERIFY_MD}")

# ── entry ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run", "live"], required=True)
    parser.add_argument("--max-products", type=int, default=20)
    parser.add_argument("--types", default="type-hat,type-coat")
    args = parser.parse_args()

    allowed_types = set(args.types.split(","))
    log(f"[mode] {args.mode} | max={args.max_products} | types={sorted(allowed_types)}")
    log(f"[token] suffix={TOKEN[-4:]}")

    log("\n[classify] Fetching all active products from Shopify...")
    products = fetch_all_active_products()
    log(f"  fetched {len(products)} active products")

    candidates = []
    already_count = 0
    review_count  = 0
    for p in products:
        tags_set = {t.strip() for t in p.get("tags","").split(",") if t.strip()}
        if LAYER67_TYPE_TAGS & tags_set:
            already_count += 1
            continue
        c = classify_product(p, allowed_types)
        if c:
            candidates.append(c)
        else:
            review_count += 1

    candidates.sort(key=lambda x: (-x["type_conf"], x["title"]))

    log(f"\n[pool] already_tagged={already_count} | SAFE hat/coat={len(candidates)} | other={review_count}")

    if not candidates:
        log("[STOP] No SAFE hat/coat candidates found.")
        sys.exit(1)

    if args.mode == "dry-run":
        ok, _, _ = run_dry_run(candidates, args.max_products)
        sys.exit(0 if ok else 1)
    else:
        ok = run_live(candidates, args.max_products)
        sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
