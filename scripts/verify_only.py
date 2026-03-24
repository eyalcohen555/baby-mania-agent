#!/usr/bin/env python3
"""Verify-only for 28 products that were pushed but verify timed out (429)."""
import subprocess
import time
import json

PIDS = [
    "9179173617977", "9688976326969", "9678573240633", "9688660377913",
    "9096606810425", "9096607301945", "9179155693881", "9606694043961",
    "9096606974265", "9179158217017", "9688670110009", "9179172733241",
    "9096599994681", "9179133870393", "9873511022905", "9179170799929",
    "9688964989241", "9895864435001", "10011383103801", "9605887754553",
    "9874906513721", "9858268496185", "9179138687289", "9179152482617",
    "9688674533689", "9874906382649", "9605887787321", "9673732194617",
]

orch = "C:/Projects/baby-mania-agent/00-team-lead/orchestrator.py"
results = {"success": [], "failed": []}

for i, pid in enumerate(PIDS):
    attempts = 0
    ok = False
    while attempts < 8:
        r = subprocess.run(
            ["python3", orch, "verify", pid],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd="C:/Projects/baby-mania-agent"
        )
        out = r.stdout + r.stderr
        if "429" in out or "Too Many Requests" in out:
            attempts += 1
            wait = 15 * attempts
            print("[{}/{}] {} - 429, wait {}s (attempt {})".format(i+1, len(PIDS), pid, wait, attempts))
            time.sleep(wait)
        elif "FAIL" in out or r.returncode != 0:
            print("[{}/{}] {} - VERIFY FAIL: {}".format(i+1, len(PIDS), pid, out[-200:].strip()))
            results["failed"].append(pid)
            ok = True
            break
        else:
            print("[{}/{}] {} - OK".format(i+1, len(PIDS), pid))
            results["success"].append(pid)
            ok = True
            break
    if not ok:
        print("[{}/{}] {} - VERIFY FAILED: max retries".format(i+1, len(PIDS), pid))
        results["failed"].append(pid)
    time.sleep(1)

print("\n=== DONE: {} success, {} failed ===".format(len(results["success"]), len(results["failed"])))
if results["failed"]:
    print("FAILED:", results["failed"])

with open("C:/Projects/baby-mania-agent/output/verify_only_results.json", "w") as f:
    json.dump(results, f, indent=2)
