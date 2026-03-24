#!/usr/bin/env python3
"""Bulk push+verify with retry logic. ASCII output only."""
import subprocess
import time
import json

PIDS = [
    "9179173617977","9688976326969","9688965022009","9678573240633","9688660377913",
    "9096606810425","9179167949113","9096607301945","9874906546489","9179154612537",
    "9179155693881","9717957525817","9858268528953","10009173721401","9606691914041",
    "9688885952825","10029649002809","9688976294201","10005779841337","9606694043961",
    "9096606974265","9179158217017","9719189635385","9096607498553","9688670110009",
    "9179172733241","9858268463417","9096599994681","9606691356985","9179172077881",
    "9179133870393","9873511022905","9096606908729","9179167129913","9179170799929",
    "9688964989241","9688885985593","9687596663097","9858268430649","9864947827001",
    "9606694273337","9096607138105","9895864435001","9687653122361","10011383103801",
    "9606694404409","9605887754553","9096607400249","9874906513721","9874906480953",
    "9858268496185","9688934973753","9096606056761","9678573273401","9179138687289",
    "9606693880121","9606691750201","9179167654201","9657036374329","10005779808569",
    "9855017582905","9688955912505","9687579033913","9179173191993","9688964956473",
    "9179152482617","9688674533689","9874906382649","9606694437177","9874906349881",
    "9605887787321","9096607072569","9688935006521","10005779710265","9673732194617",
    "9724813443385","9179159888185","9688965087545","9096605827385"
]

ORCH = "C:/Projects/baby-mania-agent/00-team-lead/orchestrator.py"
CWD = "C:/Projects/baby-mania-agent"

results = {"push_success": [], "push_failed": [], "verify_failed": []}

def run_cmd(cmd, pid, step):
    attempts = 0
    while attempts < 6:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", cwd=CWD
        )
        out = r.stdout + r.stderr
        if "429" in out or "Too Many Requests" in out:
            attempts += 1
            wait = 15 * attempts
            print(f"  [{step}] {pid} - 429, wait {wait}s (attempt {attempts})")
            time.sleep(wait)
        elif r.returncode != 0 or "ERROR" in out:
            return False, out[-300:]
        else:
            return True, out
    return False, "max retries exceeded"

total = len(PIDS)
for i, pid in enumerate(PIDS):
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

push_fail = len(results["push_failed"])
ver_fail = len(results["verify_failed"])
success = len(results["push_success"])
print(f"\n=== DONE: {success} success, {push_fail} push-failed, {ver_fail} verify-failed ===")
if results["push_failed"]:
    print("PUSH FAILED:", results["push_failed"])
if results["verify_failed"]:
    print("VERIFY FAILED:", results["verify_failed"])

with open("C:/Projects/baby-mania-agent/output/bulk_push_verify_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
