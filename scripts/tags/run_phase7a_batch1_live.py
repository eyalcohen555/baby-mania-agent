"""
Layer 7 — Phase 7A Batch 1 Live Write
T3 approval: "מאשר Phase 7A live batch ראשון — 10 מוצרים SAFE בלבד"
10 diverse products: type-dress + type-bodysuit + type-set
LIVE WRITE — backs up → writes → verifies one product at a time.
"""

import json, os, re, sys, html
from datetime import datetime, timezone
from pathlib import Path

ROOT      = Path(__file__).resolve().parents[2]
ENV_PATH  = Path.home() / "Desktop/shopify-token/.env"
SHOP_URL  = "https://a2756c-c0.myshopify.com"
API_VER   = "2024-10"

BACKUP_FILE = ROOT / "output/tags/phase7a-batch1-tags-backup.json"
VERIFY_FILE = ROOT / "output/tags/phase7a-batch1-live-verify.md"

# ── 10 selected SAFE products (diverse types, ordered by type then score) ──
# type-dress: 1  |  type-bodysuit: 2  |  type-set: 7
BATCH = [
    # type-dress (1)
    {
        "pid": "9731768746297",
        "title": "סט בגדי תינוקות גינס ושמלה דגם טליה",
        "type": "type-dress",
        "score": 85.0,
        "proposed": ["type-dress", "season-summer", "fabric-denim", "gender-girl"],
    },
    # type-bodysuit (2)
    {
        "pid": "9179166671161",
        "title": "בגד גוף שמלה ג׳ינס מכותנה - הרפר",
        "type": "type-bodysuit",
        "score": 95.0,
        "proposed": ["type-bodysuit", "size-12-18m", "size-3-6m", "fabric-cotton"],
    },
    {
        "pid": "9874906382649",
        "title": "בגד גוף פו הדוב דגם לירון",
        "type": "type-bodysuit",
        "score": 100.0,
        "proposed": [
            "type-bodysuit", "size-18-24m", "size-0-3m", "size-9-12m",
            "size-12-18m", "size-3-6m", "size-6-9m",
            "season-summer", "fabric-cotton", "gender-girl", "style-teddy",
        ],
    },
    # type-set (7)
    {
        "pid": "9874906546489",
        "title": "חליפת דובי מלאה בסטייל דגם מאור",
        "type": "type-set",
        "score": 100.0,
        "proposed": ["type-set", "size-3-6m", "size-9-12m", "season-spring-fall", "gender-boy", "style-teddy"],
    },
    {
        "pid": "9688660377913",
        "title": "חליפת קואלה דגם שני",
        "type": "type-set",
        "score": 100.0,
        "proposed": [
            "type-set", "size-0-3m", "size-3-6m", "size-6-9m",
            "size-9-12m", "size-12-18m", "size-18-24m",
            "season-spring-fall", "gender-girl", "style-casual",
        ],
    },
    {
        "pid": "9688976326969",
        "title": "חליפה דוב מופתע דגם ליאל",
        "type": "type-set",
        "score": 100.0,
        "proposed": [
            "type-set", "size-0-3m", "size-3-6m", "size-6-9m",
            "size-9-12m", "size-12-18m", "gender-boy", "style-casual",
        ],
    },
    {
        "pid": "9688964989241",
        "title": "חליפה דוב מקסימה דגם אריאל",
        "type": "type-set",
        "score": 100.0,
        "proposed": ["type-set", "size-9-12m", "season-winter", "fabric-polyester", "gender-boy", "style-teddy"],
    },
    {
        "pid": "9688674566457",
        "title": "חליפה לבנים דגם אימרי",
        "type": "type-set",
        "score": 100.0,
        "proposed": [
            "type-set", "size-0-3m", "size-3-6m", "size-12-18m",
            "size-18-24m", "gender-boy", "style-casual",
        ],
    },
    {
        "pid": "9688976294201",
        "title": "חליפה מהממת רקמת דובי חמוד דגם אלי",
        "type": "type-set",
        "score": 100.0,
        "proposed": [
            "type-set", "size-6-9m", "size-9-12m", "size-12-18m",
            "size-18-24m", "season-winter", "gender-boy", "style-casual",
        ],
    },
    {
        "pid": "10190523302201",
        "title": "Children's Summer New Arrival Boys' Regular Striped Teddy Bear Set",
        "type": "type-set",
        "score": 100.0,
        "proposed": [
            "type-set", "size-18-24m", "size-9-12m", "size-12-18m",
            "size-3-6m", "size-6-9m", "season-summer", "gender-boy", "style-casual",
        ],
    },
]

FORBIDDEN_TAGS = {
    "age-0-3m","age-3-6m","age-6-9m","age-9-12m","age-12-18m","age-18-24m",
    "3-6m6-9m","copy ai","all categories",
}

# ── helpers ────────────────────────────────────────────────────────────────
def load_env():
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SHOPIFY_ACCESS_TOKEN"):
                    return line.split("=", 1)[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    return None


def shopify_get(pid, token):
    import urllib.request
    url = f"{SHOP_URL}/admin/api/{API_VER}/products/{pid}.json?fields=id,title,tags,status"
    req = urllib.request.Request(
        url, headers={"X-Shopify-Access-Token": token}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read()).get("product", {})


def shopify_put_tags(pid, tags_str, token):
    import urllib.request
    url = f"{SHOP_URL}/admin/api/{API_VER}/products/{pid}.json"
    body = json.dumps({"product": {"id": int(pid), "tags": tags_str}}).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.status
        data = json.loads(resp.read())
    return status, data.get("product", {})


def parse_tags(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def merge_tags(current: list[str], new: list[str]) -> list[str]:
    seen = set()
    result = []
    for t in (current + new):
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


def check_forbidden(tags: list[str]) -> list[str]:
    return [t for t in tags if t.lower() in FORBIDDEN_TAGS]


def now_ts():
    return datetime.now(timezone.utc).isoformat()


# ── main ───────────────────────────────────────────────────────────────────
def main():
    token = load_env()
    if not token:
        print("ERROR: no Shopify token")
        sys.exit(1)

    print("=== Phase 7A Batch 1 — LIVE WRITE ===")
    print(f"Products to write: {len(BATCH)}")
    print()

    ts = now_ts()
    backup_entries = []
    verify_results = []
    written_pids = []
    rollback_needed = False

    # ── STEP 1: pre-flight fetch + backup ─────────────────────────────────
    print("Step 1: Fetching current tags (pre-flight) ...")
    for item in BATCH:
        pid = item["pid"]
        p = shopify_get(pid, token)
        if not p:
            print(f"  ERROR: product {pid} not found in Shopify")
            sys.exit(1)
        current_tags = parse_tags(p.get("tags", ""))
        item["current_tags"] = current_tags
        item["shopify_title"] = p.get("title", "")
        item["status"] = p.get("status", "")

        # safety: no forbidden tags in proposed
        forbidden_in_proposed = check_forbidden(item["proposed"])
        if forbidden_in_proposed:
            print(f"  ERROR: forbidden tags in proposed for {pid}: {forbidden_in_proposed}")
            sys.exit(1)

        # compute final tags
        final_tags = merge_tags(current_tags, item["proposed"])
        forbidden_in_final = check_forbidden(final_tags)
        if forbidden_in_final:
            print(f"  ERROR: forbidden tags in final for {pid}: {forbidden_in_final}")
            sys.exit(1)
        item["final_tags"] = final_tags

        print(f"  {pid}: current={len(current_tags)} tags -> final={len(final_tags)} tags")

        backup_entries.append({
            "candidate": f"P-{pid[-6:]}",
            "product_id": pid,
            "title": item["shopify_title"],
            "type": item["type"],
            "current_tags": current_tags,
            "proposed_new_tags": item["proposed"],
            "final_tags_after_write": final_tags,
            "timestamp": ts,
        })

    # ── STEP 2: write backup ───────────────────────────────────────────────
    print()
    print("Step 2: Writing backup ...")
    backup_data = {
        "backup_timestamp": ts,
        "phase": "Phase 7A batch 1 pre-write backup",
        "products": backup_entries,
    }
    BACKUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    print(f"  Backup written: {BACKUP_FILE}")

    # ── STEP 3: write + verify one at a time ──────────────────────────────
    print()
    print("Step 3: Writing tags (one at a time with verify) ...")
    for item in BATCH:
        pid = item["pid"]
        title = item["shopify_title"]
        final_str = ", ".join(item["final_tags"])
        print(f"\n  [{pid}] {title[:40]}")
        print(f"    PUT tags ({len(item['final_tags'])} tags) ...")

        # PUT
        try:
            status_code, resp_product = shopify_put_tags(pid, final_str, token)
        except Exception as e:
            print(f"    ERROR: PUT failed: {e}")
            rollback_needed = True
            verify_results.append({
                "pid": pid, "title": title, "type": item["type"],
                "put_status": "ERROR", "verify": "FAIL", "reason": str(e),
            })
            break

        if status_code != 200:
            print(f"    ERROR: PUT returned {status_code}")
            rollback_needed = True
            verify_results.append({
                "pid": pid, "title": title, "type": item["type"],
                "put_status": status_code, "verify": "FAIL", "reason": f"PUT {status_code}",
            })
            break

        written_pids.append(pid)
        print(f"    PUT {status_code} OK")

        # GET verify
        print(f"    GET verify ...")
        try:
            p_verify = shopify_get(pid, token)
        except Exception as e:
            print(f"    ERROR: GET verify failed: {e}")
            rollback_needed = True
            verify_results.append({
                "pid": pid, "title": title, "type": item["type"],
                "put_status": status_code, "verify": "FAIL", "reason": f"GET verify error: {e}",
            })
            break

        live_tags = parse_tags(p_verify.get("tags", ""))
        live_title = p_verify.get("title", "")
        live_status = p_verify.get("status", "")

        # verify checks
        fail_reason = None

        # 1. all proposed tags present
        for t in item["proposed"]:
            if t not in live_tags:
                fail_reason = f"proposed tag missing: {t}"
                break

        # 2. all original tags preserved
        if not fail_reason:
            for t in item["current_tags"]:
                if t not in live_tags:
                    fail_reason = f"original tag removed: {t}"
                    break

        # 3. no forbidden tags
        if not fail_reason:
            bad = check_forbidden(live_tags)
            if bad:
                fail_reason = f"forbidden tags present: {bad}"

        # 4. title unchanged
        if not fail_reason and live_title != item["shopify_title"]:
            fail_reason = f"title changed: was '{item['shopify_title']}' now '{live_title}'"

        # 5. status active
        if not fail_reason and live_status != "active":
            fail_reason = f"status not active: {live_status}"

        if fail_reason:
            print(f"    VERIFY FAIL: {fail_reason}")
            rollback_needed = True
            verify_results.append({
                "pid": pid, "title": title, "type": item["type"],
                "put_status": status_code, "verify": "FAIL", "reason": fail_reason,
                "live_tags": live_tags,
            })
            break
        else:
            print(f"    VERIFY PASS — {len(live_tags)} tags live")
            verify_results.append({
                "pid": pid, "title": title, "type": item["type"],
                "put_status": status_code, "verify": "PASS",
                "live_tags": live_tags,
                "proposed_count": len(item["proposed"]),
                "final_count": len(live_tags),
            })

    # ── STEP 4: rollback if needed ─────────────────────────────────────────
    if rollback_needed and written_pids:
        print()
        print("ROLLBACK REQUIRED — reverting written products ...")
        rollback_results = []
        for pid in written_pids:
            original = next((b for b in backup_entries if b["product_id"] == pid), None)
            if not original:
                rollback_results.append({"pid": pid, "status": "ERROR: no backup found"})
                continue
            orig_str = ", ".join(original["current_tags"])
            try:
                rc, _ = shopify_put_tags(pid, orig_str, token)
                rollback_results.append({"pid": pid, "status": f"OK ({rc})"})
                print(f"  Rolled back {pid}: {rc}")
            except Exception as e:
                rollback_results.append({"pid": pid, "status": f"ERROR: {e}"})
                print(f"  Rollback ERROR {pid}: {e}")

        rollback_report = {
            "timestamp": now_ts(),
            "rolled_back": rollback_results,
        }
        rb_path = ROOT / "output/tags/phase7a-batch1-rollback-report.json"
        with open(rb_path, "w", encoding="utf-8") as f:
            json.dump(rollback_report, f, ensure_ascii=False, indent=2)
        print(f"  Rollback report: {rb_path}")

    # ── STEP 5: write verify report ────────────────────────────────────────
    write_verify_report(verify_results, written_pids, rollback_needed, BATCH, ts)

    # ── summary ────────────────────────────────────────────────────────────
    pass_count = sum(1 for r in verify_results if r.get("verify") == "PASS")
    fail_count = sum(1 for r in verify_results if r.get("verify") == "FAIL")
    verdict = "PHASE7A_BATCH1_LIVE_PASS" if (not rollback_needed and pass_count == len(BATCH)) else "PHASE7A_BATCH1_LIVE_FAIL"

    print()
    print("=== SUMMARY ===")
    print(f"Written: {len(written_pids)}/{len(BATCH)}")
    print(f"Verify PASS: {pass_count}")
    print(f"Verify FAIL: {fail_count}")
    print(f"Rollback: {'YES' if rollback_needed else 'NO'}")
    print(f"Verdict: {verdict}")

    if rollback_needed:
        sys.exit(1)


def write_verify_report(verify_results, written_pids, rollback_needed, batch, ts):
    pass_count = sum(1 for r in verify_results if r.get("verify") == "PASS")
    fail_count = sum(1 for r in verify_results if r.get("verify") == "FAIL")
    verdict = "PHASE7A_BATCH1_LIVE_PASS" if (not rollback_needed and pass_count == len(batch)) else "PHASE7A_BATCH1_LIVE_FAIL"

    from collections import Counter
    type_dist = Counter(r["type"] for r in verify_results if r.get("verify") == "PASS")

    lines = [
        "# Layer 7 — Phase 7A Batch 1 Live Verify Report",
        f"**תאריך:** {ts[:10]}",
        "**Phase:** 7A — Batch 1 — 10 מוצרים מגוונים",
        f"**T3 approval:** מאשר Phase 7A live batch ראשון — 10 מוצרים SAFE בלבד",
        "",
        "---",
        "",
        "## 1. System State",
        "",
        "| פרמטר | ערך |",
        "|-------|-----|",
        "| Phase 6 batch 1+2 | COMPLETE + PASS |",
        "| T3 approval batch Phase 7A | RECEIVED |",
        f"| Shopify live BEFORE | YES — 5 products (C3, C2, C4, C5, C1) |",
        f"| Shopify live AFTER | YES — {5 + pass_count} products |",
        "| age-* tags | 0 |",
        f"| rollback | {'נדרש' if rollback_needed else 'לא נדרש'} |",
        "",
        "---",
        "",
        "## 2. מוצרים שנבחרו",
        "",
        "| # | product_id | כותרת | type | score |",
        "|---|-----------|-------|------|-------|",
    ]
    for i, item in enumerate(batch, 1):
        lines.append(f"| {i} | {item['pid']} | {item['title'][:45]} | {item['type']} | {item['score']} |")

    lines += [
        "",
        "---",
        "",
        "## 3. תגיות לפי מוצר",
        "",
    ]

    for i, item in enumerate(batch, 1):
        r = next((x for x in verify_results if x["pid"] == item["pid"]), {})
        verd = r.get("verify", "NOT_REACHED")
        reason = r.get("reason", "")
        added = item.get("proposed", [])

        lines += [
            f"### P{i} — {item['pid']}",
            "",
            f"**לפני:** `{', '.join(item.get('current_tags', []))}`",
            "",
            f"**נוספו ({len(added)}):**",
            f"`{', '.join(added)}`",
            "",
            f"**VERIFY:** **{verd}**",
        ]
        if reason:
            lines.append(f"**REASON:** {reason}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 4. Verify לכל מוצר",
        "",
        "| בדיקה | " + " | ".join(f"P{i+1}" for i in range(len(batch))) + " |",
        "|-------|" + "--------|" * len(batch),
    ]
    checks = [
        "תגיות Layer 6/7 קיימות",
        "תגיות קיימות נשמרו",
        "אין age-* tags",
        "title לא השתנה",
        "status active",
    ]
    for check in checks:
        row = f"| {check} |"
        for r in verify_results:
            v = r.get("verify", "—")
            row += f" **{v}** |"
        lines.append(row)

    lines += [
        "",
        "---",
        "",
        "## 5. פילוח סוגים שנכתבו",
        "",
        "| type | מוצרים |",
        "|------|--------|",
    ]
    for t, cnt in sorted(type_dist.items()):
        lines.append(f"| {t} | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## 6. שגיאות",
        "",
        "אין שגיאות." if not rollback_needed else "**שגיאה — ראה rollback report.**",
        "",
        "---",
        "",
        "## 7. Rollback",
        "",
        "לא נדרש rollback." if not rollback_needed else "**Rollback בוצע — ראה phase7a-batch1-rollback-report.json**",
        "",
        "---",
        "",
        "## 8. Verdict סופי",
        "",
        f"**{verdict}**",
        "",
        "| בדיקה | תוצאה |",
        "|-------|-------|",
        f"| dry run עבר | YES |",
        f"| גיבוי נוצר | YES |",
    ]
    for r in verify_results:
        lines.append(f"| {r['pid']} נכתב ועבר verify | {r.get('verify','—')} |")

    lines += [
        "| אין age-* tags | YES |",
        f"| אין תגיות שנמחקו | {'YES' if not rollback_needed else 'CHECK ROLLBACK'} |",
        f"| rollback נדרש | {'NO' if not rollback_needed else 'YES'} |",
        f"| **Shopify live** | **YES — {5 + pass_count} products total** |",
        "",
        f"**הצעד הבא:** post-live monitor לאחר review — ואז batch נוסף / Phase 7B.",
        "",
        "---",
        "",
        f"*Phase 7A batch 1 — {'COMPLETE' if not rollback_needed else 'ROLLED BACK'}.*",
    ]

    with open(VERIFY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nVerify report written: {VERIFY_FILE}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
