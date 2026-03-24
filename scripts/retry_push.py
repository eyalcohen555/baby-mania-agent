#!/usr/bin/env python3
"""Retry push for failed products from bd2x9ftp6."""
import subprocess, time, json

FAILED = [
    "9688935039289","9606693847353","9731768713529","10011383202105","9864947990841",
    "9606691848505","9606694076729","9794582774073","9873511055673","9724813410617",
    "9864947958073","9606670942521","9687579066681","9606693749049","9606671008057",
    "9864947859769","9605887820089","9864947728697"
]

results = {"success": [], "failed": []}
orch = "C:/Projects/baby-mania-agent/00-team-lead/orchestrator.py"

for i, pid in enumerate(FAILED):
    attempts = 0
    success = False
    while attempts < 5:
        result = subprocess.run(
            ["python3", orch, "push", pid],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd="C:/Projects/baby-mania-agent"
        )
        output = result.stdout + result.stderr
        if "429" in output or "Too Many Requests" in output:
            attempts += 1
            wait = 15 * attempts
            print(f"[{i+1}/{len(FAILED)}] {pid} - 429, waiting {wait}s (attempt {attempts})")
            time.sleep(wait)
        elif "ERROR" in output or result.returncode != 0:
            print(f"[{i+1}/{len(FAILED)}] {pid} - FAILED: {output[-300:]}")
            results["failed"].append(pid)
            break
        else:
            print(f"[{i+1}/{len(FAILED)}] {pid} - SUCCESS")
            results["success"].append(pid)
            success = True
            break
    if not success and pid not in results["failed"]:
        results["failed"].append(pid)
    time.sleep(2)

print(f"\n=== DONE: {len(results['success'])} success, {len(results['failed'])} failed ===")
if results["failed"]:
    print("STILL FAILED:", results["failed"])

with open("C:/Projects/baby-mania-agent/output/retry_push_results.json", "w") as f:
    json.dump(results, f, indent=2)
