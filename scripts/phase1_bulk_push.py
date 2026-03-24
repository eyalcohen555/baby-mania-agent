#!/usr/bin/env python3
"""
Phase 1 — Bulk push all clothing products with complete publisher.json.
Excludes: 9606693749049 (permanent fail), 9605662212409 (non-clothing bib).
Skips products with missing fabric_highlight (19 products — pipeline issue).
Date: 2026-03-18
"""
import subprocess
import time
import json
from pathlib import Path

BASE_DIR = Path("C:/Projects/baby-mania-agent")
STAGE_DIR = BASE_DIR / "output" / "stage-outputs"
ORCH = str(BASE_DIR / "00-team-lead" / "orchestrator.py")
OUTPUT_FILE = BASE_DIR / "output" / "phase1_push_results.json"

EXCLUDED_PIDS = {
    "9606693749049",  # permanent failure — verification loop
    "9605662212409",  # non-clothing (bib/burp cloth set)
}

REQUIRED_MF = [
    "hero_eyebrow", "hero_headline", "hero_subheadline",
    "fabric_title", "fabric_body", "fabric_highlight", "fabric_tags",
    "whats_special", "benefits", "emotional_reassurance",
    "care_instructions", "faq",
]

ALREADY_OK = {
    # bulk_push_verify push_success
    "9688965022009","9179167949113","9874906546489","9179154612537",
    "9858268528953","10009173721401","9606691914041","9688885952825",
    "10029649002809","9688976294201","10005779841337","9096607498553",
    "9858268463417","9606691356985","9179172077881","9096606908729",
    "9179167129913","9688885985593","9864947827001","9606694273337",
    "9687653122361","9606694404409","9096607400249","9874906480953",
    "9688934973753","9096606056761","9678573273401","9606693880121",
    "9606691750201","9179167654201","9657036374329","10005779808569",
    "9855017582905","9688955912505","9687579033913","9179173191993",
    "9688964956473","9606694437177","9096607072569","9688935006521",
    "10005779710265","9179159888185","9096605827385",
    # retry_push success
    "9688935039289","9606693847353","9731768713529","10011383202105",
    "9864947990841","9606691848505","9606694076729","9794582774073",
    "9873511055673","9724813410617","9864947958073","9606670942521",
    "9687579066681","9606671008057","9864947859769","9605887820089",
    "9864947728697",
    # health_check confirmed OK
    "10009173033273","10026705748281","10029648970041","10029649101113",
    "10029649133881","9657091293497","9673732292921","9687596728633",
    "9688660312377","9688932909369","9688934940985","9855017550137",
    "9874906415417","9892196417849","9895864205625",
}


def get_complete_pids():
    """Return PIDs with publisher.json and all 12 required metafields."""
    pub_files = list(STAGE_DIR.glob("*_publisher.json"))
    complete = []
    skipped_incomplete = []

    for f in pub_files:
        pid = f.name.replace("_publisher.json", "")

        if pid in EXCLUDED_PIDS:
            continue
        if pid in ALREADY_OK:
            continue

        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)

        mf = data.get("metafields", {})
        missing = [k for k in REQUIRED_MF if k not in mf or not mf[k]]
        if missing:
            skipped_incomplete.append((pid, missing))
        else:
            complete.append(pid)

    return complete, skipped_incomplete


def run_cmd(cmd, pid, step):
    attempts = 0
    while attempts < 6:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            cwd=str(BASE_DIR)
        )
        out = r.stdout + r.stderr
        if "429" in out or "Too Many Requests" in out:
            attempts += 1
            wait = 15 * attempts
            print(f"  [{step}] {pid} — 429, wait {wait}s (attempt {attempts})")
            time.sleep(wait)
        elif r.returncode != 0 or "ERROR" in out:
            return False, out[-300:]
        else:
            return True, out
    return False, "max retries exceeded"


def main():
    complete_pids, skipped = get_complete_pids()

    print(f"=== PHASE 1 BULK PUSH ===")
    print(f"Already confirmed OK (skipping): {len(ALREADY_OK)}")
    print(f"Excluded PIDs: {len(EXCLUDED_PIDS)}")
    print(f"Skipped (incomplete metafields): {len(skipped)}")
    print(f"Target for push: {len(complete_pids)}")
    print()

    if skipped:
        print("SKIPPED (incomplete):")
        for pid, miss in skipped:
            print(f"  {pid}: missing {miss}")
        print()

    results = {
        "push_success": [],
        "push_failed": [],
        "verify_failed": [],
        "skipped_incomplete": [pid for pid, _ in skipped],
        "excluded": list(EXCLUDED_PIDS),
        "already_ok_count": len(ALREADY_OK),
    }

    total = len(complete_pids)
    for i, pid in enumerate(complete_pids):
        print(f"[{i+1}/{total}] {pid}")

        ok, out = run_cmd(["python3", ORCH, "push", pid], pid, "push")
        if not ok:
            print(f"  PUSH FAILED: {out[-100:]}")
            results["push_failed"].append(pid)
            time.sleep(2)
            continue

        ok2, out2 = run_cmd(["python3", ORCH, "verify", pid], pid, "verify")
        if not ok2:
            print(f"  VERIFY FAILED: {out2[-100:]}")
            results["verify_failed"].append(pid)
        else:
            print(f"  OK")
            results["push_success"].append(pid)

        time.sleep(1.5)

    push_ok = len(results["push_success"])
    push_fail = len(results["push_failed"])
    ver_fail = len(results["verify_failed"])
    print(f"\n=== PHASE 1 DONE ===")
    print(f"Push + verify OK: {push_ok}")
    print(f"Push failed:      {push_fail}")
    print(f"Verify failed:    {ver_fail}")
    print(f"Skipped (incomplete mf): {len(skipped)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
