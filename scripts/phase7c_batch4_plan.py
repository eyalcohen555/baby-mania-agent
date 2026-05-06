"""
Phase 7C Batch 4 — READ-ONLY Planning.
Classifies remaining SAFE candidates (dress/set/romper/bodysuit only),
selects up to 20, writes plan. NO Shopify writes. GET only.
Explicitly excludes all product IDs already written in Batch 1/2/3.
"""
import sys, os, re, json, datetime, time, argparse, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

ENV_PATH = r"C:\Users\3024e\Desktop\shopify-token\.env"
SHOP     = "a2756c-c0.myshopify.com"
BASE     = f"https://{SHOP}/admin/api/2024-10"

OUT_MD   = "output/tags/phase7c-batch4-plan.md"
OUT_JSON = "output/tags/phase7c-batch4-plan.json"

# Product IDs already written in Phase 7C Batch 1/2/3 (plus 7A/7B for extra safety)
ALREADY_WRITTEN_PIDS = {
    # Batch 1/2/3 verify PASS IDs
    "10005779743033","10005779808569","10005779841337","10024854847801",
    "10026520445241","10190522876217","10190523269433","10190523334969",
    "9096599994681","9096606908729","9096607138105","9096607301945",
    "9179134132537","9179136426297","9179137048889","9179138457913",
    "9179138687289","9179140915513","9179141308729","9179147829561",
    "9179151794489","9179152482617","9179155693881","9179156742457",
    "9179161231673","9179168964921","9179172733241","9179176141113",
    "9606690111801","9606694142265","9606864666937","9673730359609",
    "9673732292921","9678573240633","9687596663097","9688885952825",
    "9688934940985","9688965087545","9688976228665","9717957525817",
    "9719189635385","9724813443385","9731768713529","9855017550137",
    "9858268430649","9864947827001","9892620927289",
}

# ── Classification rules ───────────────────────────────────────────────────────

TYPE_RULES = {
    "type-dress": {
        "keywords": ["dress", "שמלה", "שמלת"],
        "min_conf": 0.90,
    },
    "type-bodysuit": {
        "keywords": ["bodysuit", "בגד גוף", "בגד-גוף"],
        "min_conf": 0.90,
    },
    "type-set": {
        "keywords": ["set", "סט", "חליפה", "חליפת", "2pcs", "2-pcs", "pcs", "suit", "outfit"],
        "min_conf": 0.88,
    },
    "type-romper": {
        "keywords": ["romper", "אוברול", "סרבל", "jumpsuit"],
        "min_conf": 0.88,
    },
}

GENDER_RULES = {
    "gender-girl": {
        "title_kw": ["girl", "girls", "בנות", "לבנות", "ילדה", "נסיכה"],
        "handle_kw": ["girl", "girls"],
    },
    "gender-boy": {
        "title_kw": ["boy", "boys", "בנים", "לבנים", "ילד"],
        "handle_kw": ["boy", "boys"],
    },
    "gender-neutral": {
        "title_kw": ["unisex", "יוניסקס", "neutral"],
        "handle_kw": ["unisex", "neutral"],
    },
}

OCC_RULES = {
    "occ-gift":      ["gift", "מתנה", "shower", "baby shower"],
    "occ-everyday":  ["everyday", "daily", "יומיומי", "casual"],
    "occ-seasonal":  ["winter", "summer", "seasonal", "חורף", "קיץ", "אביב"],
}

LAYER67_TYPE_TAGS = {f"type-{t}" for t in [
    "set", "romper", "dress", "bodysuit", "hat", "swimwear", "coat",
    "pants", "top", "shoes", "sandals", "sneakers", "accessory", "reborn-doll"
]}

SHOE_TITLE_KW = ["סנדל", "נעל", "מגפ", "כפכף", "sandal", "shoe", "sneaker", "boot", "croc"]

NOT_DRESS_TITLE_KW   = ["מגבת", "תיק", "משפך", "שמיכה", "ספוג", "towel", "bag", "blanket", "sponge"]
NOT_SET_TITLE_KW     = ["מגבת", "towel", "אמבטיה", "bath", "בגד ים", "swimsuit", "swimwear"]
NOT_ROMPER_TITLE_KW  = ["מגבת", "תיק", "towel", "bag"]
NOT_BODYSUIT_TITLE_KW = ["מגבת", "תיק", "towel", "bag"]

NOT_TYPE_KW = {
    "type-dress":    NOT_DRESS_TITLE_KW,
    "type-set":      NOT_SET_TITLE_KW,
    "type-romper":   NOT_ROMPER_TITLE_KW,
    "type-bodysuit": NOT_BODYSUIT_TITLE_KW,
}

PREFERRED_TYPES = ["type-dress", "type-set", "type-romper", "type-bodysuit"]

ALLOWED_VALUES = {
    "type-dress", "type-set", "type-romper", "type-bodysuit", "type-hat",
    "type-coat", "type-pants", "type-top", "type-swimwear", "type-shoes",
    "type-sandals", "type-sneakers", "type-accessory",
    "gender-girl", "gender-boy", "gender-neutral",
    "occ-gift", "occ-everyday", "occ-seasonal", "occ-school", "occ-special",
    "age-newborn", "age-0-3m", "age-3-6m", "age-6-12m", "age-12-24m",
    "age-2-3y", "age-2-4y", "age-3-4y", "age-4-5y",
}

FORBIDDEN_RE = re.compile(
    r"^age-|season-unknown|size-unknown|gender-unknown|"
    r"\d+[A-Za-z]+\d+[A-Za-z]|[A-Za-z]\d+$|\s",
    re.UNICODE
)


def log(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()


def load_env(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                d[k.strip()] = v.strip()
    return d


def shopify_get_all_active(token):
    products = []
    url = f"{BASE}/products.json?limit=250&status=active&fields=id,title,handle,tags,status"
    headers = {"X-Shopify-Access-Token": token}
    while url:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
        batch = data.get("products", [])
        products.extend(batch)
        link = r.headers.get("Link", "")
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                m = re.search(r'<([^>]+)>', part)
                if m:
                    url = m.group(1)
        if url:
            time.sleep(0.3)
    return products


def is_shoe_title(title):
    t = title.lower()
    return any(kw.lower() in t for kw in SHOE_TITLE_KW)


def is_false_positive(typ, title):
    t = title.lower()
    return any(kw.lower() in t for kw in NOT_TYPE_KW.get(typ, []))


def _kw_match(kw_low, text_low):
    if len(kw_low) <= 2:
        return bool(re.search(r'(?<!\S)' + re.escape(kw_low) + r'(?!\S)', text_low))
    return kw_low in text_low


def score_type(title, handle):
    t_low = title.lower()
    h_low = handle.lower()
    for typ, rule in TYPE_RULES.items():
        for kw in rule["keywords"]:
            kw_low = kw.lower()
            in_title  = _kw_match(kw_low, t_low)
            in_handle = kw_low in h_low
            if not in_title and not in_handle:
                continue
            src = "title" if in_title else "handle"
            if typ == "type-set" and kw_low == "suit" and "אוברול" in t_low:
                continue
            return typ, rule["min_conf"], src, kw
    return None, 0.0, None, None


def score_gender(title, handle):
    t_low = title.lower()
    h_low = handle.lower()
    for gender, rule in GENDER_RULES.items():
        for kw in rule["title_kw"]:
            if kw.lower() in t_low:
                return gender, 0.90, "title", kw
        for kw in rule["handle_kw"]:
            if kw.lower() in h_low:
                return gender, 0.90, "handle", kw
    return None, 0.0, None, None


def score_occ(title):
    t_low = title.lower()
    found = []
    seen = set()
    for occ, kws in OCC_RULES.items():
        for kw in kws:
            if kw.lower() in t_low and occ not in seen:
                found.append((occ, kw))
                seen.add(occ)
                break
    return found


def classify_product(p):
    pid    = str(p["id"])
    title  = p.get("title", "")
    handle = p.get("handle", "")
    raw_tags = sorted([t.strip() for t in p.get("tags", "").split(",") if t.strip()])
    tags_set = set(raw_tags)

    if pid in ALREADY_WRITTEN_PIDS:
        return {"status": "already_written_batch123", "product_id": pid, "title": title}

    if LAYER67_TYPE_TAGS & tags_set:
        return {"status": "already_tagged", "product_id": pid, "title": title}

    if is_shoe_title(title):
        return {"status": "shoe_blocked", "product_id": pid, "title": title}

    typ, type_conf, type_src, type_kw = score_type(title, handle)

    if not typ or typ not in PREFERRED_TYPES:
        return {"status": "not_preferred_type", "product_id": pid, "title": title}

    if type_conf < TYPE_RULES[typ]["min_conf"]:
        return {"status": "low_confidence", "product_id": pid, "title": title}

    if is_false_positive(typ, title):
        return {"status": "false_positive_blocked", "product_id": pid, "title": title,
                "reason": f"matched {typ} keyword but title suggests non-clothing item"}

    gender, gender_conf, gender_src, gender_kw = score_gender(title, handle)
    occs = score_occ(title)

    proposed = [typ]
    if gender:
        proposed.append(gender)
    for occ, _ in occs:
        proposed.append(occ)

    not_allowed   = [t for t in proposed if t not in ALLOWED_VALUES]
    forbidden_tags = [t for t in proposed if FORBIDDEN_RE.search(t)]
    age_tags      = [t for t in proposed if t.startswith("age-")]
    type_tags_proposed   = [t for t in proposed if t.startswith("type-")]
    gender_tags_proposed = [t for t in proposed if t.startswith("gender-")]

    source_trace = f"type matched '{type_kw}' in {type_src} (conf={type_conf:.2f})"
    if gender:
        source_trace += f"; gender matched '{gender_kw}' in {gender_src} (conf={gender_conf:.2f})"
    if occs:
        source_trace += f"; occ: {', '.join(o for o, _ in occs)}"

    flags = []
    if not_allowed:           flags.append(f"not_in_allowed_values: {not_allowed}")
    if forbidden_tags:        flags.append(f"forbidden_tags: {forbidden_tags}")
    if age_tags:              flags.append(f"age_tags: {age_tags}")
    if len(type_tags_proposed) > 1:   flags.append(f"type_collision: {type_tags_proposed}")
    if len(gender_tags_proposed) > 1: flags.append(f"gender_collision: {gender_tags_proposed}")

    if flags:
        return {"status": "BLOCKED", "product_id": pid, "title": title,
                "reason": "; ".join(flags)}

    existing_non_type = [t for t in raw_tags if t not in ALLOWED_VALUES or not any(
        t.startswith(pfx) for pfx in ("type-", "gender-", "occ-", "age-")
    )]
    final_tags = sorted(set(existing_non_type) | set(proposed))

    reason_selected = (
        f"type-source={type_src}, conf={type_conf:.2f}, kw='{type_kw}'"
    )
    if gender:
        reason_selected += f", gender-source={gender_src}, kw='{gender_kw}'"
    reason_selected += ", no false-positive flags, no shoe title, active product, not in batch1/2/3"

    return {
        "status": "SAFE",
        "product_id": pid,
        "title": title,
        "handle": handle,
        "current_tags": raw_tags,
        "current_tags_count": len(raw_tags),
        "proposed_type": typ,
        "type_conf": type_conf,
        "type_source": type_src,
        "type_keyword": type_kw,
        "proposed_gender": gender,
        "gender_conf": gender_conf,
        "gender_source": gender_src,
        "gender_keyword": gender_kw,
        "proposed_occs": [o for o, _ in occs],
        "proposed_new_tags": proposed,
        "final_tags_after_merge": final_tags,
        "source_trace": source_trace,
        "risk_level": "LOW",
        "confidence": type_conf,
        "reason_selected": reason_selected,
        "safety_flags": [],
    }


def run_safety_checks(candidates):
    flags = []
    for c in candidates:
        pid = c["product_id"]
        proposed = c["proposed_new_tags"]
        age_tags   = [t for t in proposed if t.startswith("age-")]
        type_tags  = [t for t in proposed if t.startswith("type-")]
        gender_tags = [t for t in proposed if t.startswith("gender-")]
        not_allowed = [t for t in proposed if t not in ALLOWED_VALUES]
        forbidden   = [t for t in proposed if FORBIDDEN_RE.search(t)]

        if age_tags:            flags.append(f"{pid}: age_tags={age_tags}")
        if len(type_tags) > 1:  flags.append(f"{pid}: type_collision={type_tags}")
        if len(gender_tags) > 1: flags.append(f"{pid}: gender_collision={gender_tags}")
        if not_allowed:         flags.append(f"{pid}: not_in_allowed={not_allowed}")
        if forbidden:           flags.append(f"{pid}: forbidden={forbidden}")
        if is_shoe_title(c["title"]): flags.append(f"{pid}: shoe_title_leaked")
        if c["product_id"] in ALREADY_WRITTEN_PIDS:
            flags.append(f"{pid}: ALREADY_WRITTEN_batch123")

    return len(flags) == 0, flags


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="read-only")
    parser.add_argument("--max-products", type=int, default=20)
    parser.add_argument("--types", default="type-dress,type-set,type-romper,type-bodysuit")
    args = parser.parse_args()

    allowed_types = [t.strip() for t in args.types.split(",")]
    max_n = args.max_products

    log("=" * 62)
    log("Phase 7C Batch 4 — READ-ONLY Planning")
    log("=" * 62)
    log(f"[config] mode={args.mode} | max_products={max_n} | types={allowed_types}")
    log(f"[config] shopify_writes=NONE — GET only")
    log(f"[config] already_written_pids excluded: {len(ALREADY_WRITTEN_PIDS)}")

    env = load_env(ENV_PATH)
    token = env.get("SHOPIFY_ACCESS_TOKEN", "")
    if not token:
        log("[FAIL] no SHOPIFY_ACCESS_TOKEN in env"); return 1
    log(f"[token] suffix={token[-4:]}")

    log("\n[1] Fetching all active products from Shopify (GET only)...")
    try:
        products = shopify_get_all_active(token)
    except Exception as e:
        log(f"[FAIL] fetch error: {e}"); return 1
    log(f"  fetched={len(products)} active products")

    log("\n[2] Classifying products...")
    already_written = []
    already_tagged  = []
    shoe_blocked    = []
    fp_blocked      = []
    low_conf        = []
    not_preferred   = []
    blocked         = []
    safe            = []

    for p in products:
        r = classify_product(p)
        s = r["status"]
        if s == "already_written_batch123":
            already_written.append(r)
        elif s == "already_tagged":
            already_tagged.append(r)
        elif s == "shoe_blocked":
            shoe_blocked.append(r)
        elif s == "false_positive_blocked":
            fp_blocked.append(r)
        elif s == "low_confidence":
            low_conf.append(r)
        elif s == "not_preferred_type":
            not_preferred.append(r)
        elif s == "BLOCKED":
            blocked.append(r)
        elif s == "SAFE":
            if r["proposed_type"] in allowed_types:
                safe.append(r)

    log(f"  already_written_batch123: {len(already_written)}")
    log(f"  already_tagged (type-*):  {len(already_tagged)}")
    log(f"  shoe_blocked:             {len(shoe_blocked)}")
    log(f"  false_positive_blkd:      {len(fp_blocked)}")
    log(f"  low_confidence:           {len(low_conf)}")
    log(f"  not_preferred_type:       {len(not_preferred)}")
    log(f"  blocked:                  {len(blocked)}")
    log(f"  SAFE (preferred, new):    {len(safe)}")

    log("\n[3] Selecting up to {} candidates by confidence...".format(max_n))

    target_per_type = max(1, max_n // len(allowed_types))
    type_pools = {}
    for t in allowed_types:
        type_pools[t] = sorted(
            [c for c in safe if c["proposed_type"] == t],
            key=lambda c: -c["type_conf"]
        )

    type_counts = {t: 0 for t in allowed_types}
    candidates  = []

    for t in allowed_types:
        take = min(target_per_type, len(type_pools[t]))
        for _ in range(take):
            candidates.append(type_pools[t].pop(0))
            type_counts[t] += 1

    while len(candidates) < max_n:
        added = False
        for t in sorted(type_pools, key=lambda t: -len(type_pools[t])):
            if type_pools[t] and len(candidates) < max_n:
                candidates.append(type_pools[t].pop(0))
                type_counts[t] += 1
                added = True
                break
        if not added:
            break

    log(f"  selected={len(candidates)} candidates")
    for t, cnt in sorted(type_counts.items()):
        log(f"    {t}: {cnt}")

    log("\n[4] Running safety checks on selected candidates...")
    all_pass, safety_flags = run_safety_checks(candidates)

    if all_pass:
        log("  ✅ All safety checks PASS — 0 flags")
    else:
        log(f"  ❌ {len(safety_flags)} safety flags:")
        for f in safety_flags:
            log(f"    {f}")

    log("\n[5] Per-candidate evidence:")
    for i, c in enumerate(candidates, 1):
        log(f"  [{i:02d}] {c['product_id']} | {c['proposed_type']} | conf={c['confidence']:.2f} | {c['title'][:50]}")
        log(f"       source_trace: {c['source_trace']}")
        log(f"       proposed: {c['proposed_new_tags']}")
        log(f"       current_tags_count={c['current_tags_count']}")

    ts = datetime.datetime.utcnow().isoformat() + "+00:00"
    verdict = "READY_FOR_PHASE7C_BATCH4_T3_APPROVAL" if (
        all_pass and len(candidates) > 0
    ) else "HOLD_PHASE7C_BATCH4_NEEDS_FIX"

    log(f"\n[VERDICT] {verdict}")
    log(f"[summary] selected={len(candidates)} | safety_pass={'YES' if all_pass else 'NO'}")

    os.makedirs("output/tags", exist_ok=True)
    _write_json(ts, candidates, type_counts, all_pass, safety_flags, verdict, len(products),
                len(already_written))
    _write_md(ts, candidates, type_counts, all_pass, safety_flags, verdict, len(products),
              len(already_written))

    log(f"\n[saved] {OUT_MD}")
    log(f"[saved] {OUT_JSON}")
    return 0 if verdict == "READY_FOR_PHASE7C_BATCH4_T3_APPROVAL" else 1


def _write_json(ts, candidates, type_counts, all_pass, safety_flags, verdict, total_active,
                already_written_count):
    data = {
        "phase": "7C",
        "batch": 4,
        "task": "batch4_read_only_plan",
        "mode": "READ_ONLY_PLANNING",
        "timestamp": ts,
        "shopify_writes": "NONE",
        "total_active_products_fetched": total_active,
        "already_written_batch123": already_written_count,
        "selected_candidates": len(candidates),
        "type_breakdown": type_counts,
        "safety_pass": all_pass,
        "safety_flags": safety_flags,
        "allowed_types": ["type-dress", "type-set", "type-romper", "type-bodysuit"],
        "excluded": [
            "already written in Batch 1/2/3 (explicit PID list)",
            "already tagged (type-* exists in Shopify tags)",
            "shoes/sandals/sneakers (title keyword blocker)",
            "false-positive items (towel/bag/blanket/sponge/swimwear)",
            "low confidence (<min_conf threshold)",
            "non-preferred types (hat/coat/pants/top/swimwear)",
        ],
        "products": [
            {
                "product_id": c["product_id"],
                "title": c["title"],
                "handle": c["handle"],
                "current_tags": c["current_tags"],
                "current_tags_count": c["current_tags_count"],
                "proposed_new_tags": c["proposed_new_tags"],
                "final_tags_after_merge": c["final_tags_after_merge"],
                "proposed_type": c["proposed_type"],
                "type_conf": c["type_conf"],
                "type_source": c["type_source"],
                "type_keyword": c["type_keyword"],
                "proposed_gender": c["proposed_gender"],
                "gender_conf": c["gender_conf"],
                "gender_source": c["gender_source"],
                "gender_keyword": c["gender_keyword"],
                "proposed_occs": c["proposed_occs"],
                "source_trace": c["source_trace"],
                "risk_level": c["risk_level"],
                "confidence": c["confidence"],
                "reason_selected": c["reason_selected"],
                "safety_flags": c["safety_flags"],
            }
            for c in candidates
        ],
        "verdict": verdict,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_md(ts, candidates, type_counts, all_pass, safety_flags, verdict, total_active,
              already_written_count):
    lines = [
        "# Phase 7C Batch 4 — Read-Only Tagging Plan",
        "",
        "## MODE",
        "READ-ONLY PLANNING. No Shopify writes.",
        "",
        f"**Timestamp:** {ts}  ",
        f"**Shopify writes:** NONE — GET only  ",
        "",
        "---",
        "",
        "## 1. Selection Summary",
        "",
        "| Item | Count |",
        "|------|-------|",
        f"| Active products fetched | {total_active} |",
        f"| Already written Batch 1/2/3 (excluded) | {already_written_count} |",
        f"| Selected SAFE candidates | **{len(candidates)}** |",
        f"| Safety flags | {'0 ✅' if all_pass else str(len(safety_flags)) + ' ❌'} |",
        "",
        "### Type Breakdown",
        "",
        "| Type | Count |",
        "|------|-------|",
    ]
    for t, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{t}` | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## 2. Excluded / Blocked",
        "",
        "- Already written in Batch 1/2/3 (explicit PID exclusion): excluded",
        "- Already tagged with `type-*` in Shopify: excluded",
        "- Shoe/sandal/sneaker title keyword: excluded",
        "- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear): excluded",
        "- Low confidence (< type min_conf): excluded",
        "- Non-preferred types (hat/coat/pants/top/swimwear): excluded",
        "- REVIEW_ONLY: excluded (not in SAFE pool)",
        "",
        "---",
        "",
        "## 3. Per-Product Evidence",
        "",
    ]

    for i, c in enumerate(candidates, 1):
        lines += [
            f"### [{i:02d}] `{c['product_id']}` — {c['title'][:60]}",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| product_id | `{c['product_id']}` |",
            f"| title | {c['title']} |",
            f"| status | active |",
            f"| current_tags_count | {c['current_tags_count']} |",
            f"| current_tags | `{'`, `'.join(c['current_tags'][:6])}{'...' if len(c['current_tags']) > 6 else ''}` |",
            f"| proposed_new_tags | `{'`, `'.join(c['proposed_new_tags'])}` |",
            f"| final_tags_after_merge | `{'`, `'.join(c['final_tags_after_merge'][:8])}{'...' if len(c['final_tags_after_merge']) > 8 else ''}` |",
            f"| proposed_type | `{c['proposed_type']}` |",
            f"| type_source | {c['type_source']} |",
            f"| type_keyword | `{c['type_keyword']}` |",
            f"| type_conf | {c['type_conf']:.2f} |",
            f"| proposed_gender | `{c['proposed_gender'] or '—'}` |",
            f"| gender_source | {c['gender_source'] or '—'} |",
            f"| gender_keyword | `{c['gender_keyword'] or '—'}` |",
            f"| gender_conf | {c['gender_conf']:.2f} |",
            f"| proposed_occs | `{'`, `'.join(c['proposed_occs']) or '—'}` |",
            f"| source_trace | {c['source_trace']} |",
            f"| risk_level | {c['risk_level']} |",
            f"| confidence | {c['confidence']:.2f} |",
            f"| reason_selected | {c['reason_selected']} |",
            f"| safety_flags | {'NONE ✅' if not c['safety_flags'] else str(c['safety_flags'])} |",
            "",
            "**Checks:**",
            f"- allowed_values_check: {'✅ PASS' if not any(t not in ALLOWED_VALUES for t in c['proposed_new_tags']) else '❌ FAIL'}",
            f"- forbidden_tags_check: {'✅ PASS' if not any(FORBIDDEN_RE.search(t) for t in c['proposed_new_tags']) else '❌ FAIL'}",
            f"- age_tags_check: {'✅ PASS' if not any(t.startswith('age-') for t in c['proposed_new_tags']) else '❌ FAIL'}",
            f"- type_collision_check: {'✅ PASS' if len([t for t in c['proposed_new_tags'] if t.startswith('type-')]) == 1 else '❌ FAIL'}",
            f"- gender_collision_check: {'✅ PASS' if len([t for t in c['proposed_new_tags'] if t.startswith('gender-')]) <= 1 else '❌ FAIL'}",
            f"- shoe_title_check: {'✅ PASS' if not is_shoe_title(c['title']) else '❌ FAIL'}",
            f"- false_positive_check: {'✅ PASS' if not is_false_positive(c['proposed_type'], c['title']) else '❌ FAIL'}",
            f"- not_in_batch123_check: ✅ PASS",
            "",
            "---",
            "",
        ]

    lines += [
        "## 4. Batch-Level Safety Summary",
        "",
        "| Check | Result |",
        "|-------|--------|",
        f"| No age-* tags | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| No type collision | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| No gender collision | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| No forbidden tags | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| No shoe title leak | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| No Shopify writes | ✅ PASS — GET only |",
        f"| Not in Batch 1/2/3 | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        f"| All tags in ALLOWED_VALUES | {'✅ PASS' if all_pass else '❌ FAIL'} |",
        "",
    ]

    if safety_flags:
        lines += ["**Safety flags:**", ""]
        for f in safety_flags:
            lines.append(f"- ❌ {f}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 5. Required Gates for Live Batch",
        "",
        "Before any live write, each product must pass:",
        "1. backup before write",
        "2. dry run verification",
        "3. forbidden tag check",
        "4. age-* check",
        "5. RANGE_TOO_BROAD check",
        "6. type collision check",
        "7. gender collision check",
        "8. false-positive keyword check",
        "9. Shopify PUT only after T3 approval",
        "10. Shopify GET verify",
        "11. post-verify independent check",
        "12. rollback plan on file",
        "13. report",
        "14. explicit git add only (no git add -A)",
        "",
        "---",
        "",
        "## 6. Verdict",
        "",
        f"**{verdict}**",
        "",
    ]

    if verdict == "READY_FOR_PHASE7C_BATCH4_T3_APPROVAL":
        lines += [
            f"✅ {len(candidates)} SAFE candidates selected.",
            "All safety checks PASS. No age-* tags. No type collision. No forbidden tags.",
            "No overlap with Batch 1/2/3 written products.",
            "Next step: request T3 approval from Ayal → Phase 7C Batch 4 live.",
        ]
    else:
        lines += [
            "⚠️ Fix safety flags before requesting T3 approval.",
            "See Section 4 for details.",
        ]

    lines += ["", "---", "", "*Generated by scripts/phase7c_batch4_plan.py*"]

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
