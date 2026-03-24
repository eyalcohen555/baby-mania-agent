#!/usr/bin/env python3
"""Bulk push+verify for 133 remaining clothing PIDs. ASCII output only."""
import subprocess
import time
import json

PIDS = [
    "10005779743033","10011383071033","10011383103801","10011383136569",
    "10011383234873","10025300853049","10026520445241","10029649068345",
    "9096599994681","9096606220601","9096606515513","9096606679353",
    "9096606810425","9096606974265","9096607138105","9096607301945",
    "9096607596857","9096607695161","9096622473529","9096622604601",
    "9096636694841","9179133870393","9179134132537","9179136131385",
    "9179136426297","9179137933625","9179138457913","9179138687289",
    "9179142750521","9179145568569","9179146256697","9179148190009",
    "9179149173049","9179150516537","9179151008057","9179151335737",
    "9179152154937","9179152482617","9179152875833","9179155693881",
    "9179156742457","9179157266745","9179157725497","9179158217017",
    "9179158479161","9179158839609","9179161231673","9179162083641",
    "9179162444089","9179162804537","9179164344633","9179164705081",
    "9179165753657","9179166376249","9179166671161","9179168473401",
    "9179168964921","9179169128761","9179169620281","9179170144569",
    "9179170799929","9179172274489","9179172733241","9179173454137",
    "9179173617977","9179174895929","9179176141113","9605503516985",
    "9605662212409","9605887492409","9605887590713","9605887721785",
    "9605887754553","9605887787321","9606670909753","9606691291449",
    "9606691324217","9606691520825","9606691619129","9606693945657",
    "9606694011193","9606694043961","9606694240569","9606694306105",
    "9606694338873","9606694371641","9672569749817","9673730359609",
    "9673732194617","9673732227385","9673732260153","9678573207865",
    "9678573240633","9678598734137","9687563305273","9687563338041",
    "9687563370809","9687563403577","9687596564793","9687596663097",
    "9687653024057","9687653056825","9687653089593","9688660377913",
    "9688670110009","9688670142777","9688674500921","9688674533689",
    "9688674566457","9688674599225","9688885920057","9688955945273",
    "9688955978041","9688956043577","9688964989241","9688965087545",
    "9688976228665","9688976326969","9717957525817","9719189635385",
    "9724813443385","9724813476153","9731768746297","9858268430649",
    "9858268496185","9864947794233","9873511022905","9874906349881",
    "9874906382649","9874906513721","9892620894521","9895864402233",
    "9895864435001"
]

ORCH = "C:/Projects/baby-mania-agent/00-team-lead/orchestrator.py"
CWD  = "C:/Projects/baby-mania-agent"

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
ver_fail  = len(results["verify_failed"])
success   = len(results["push_success"])
print(f"\n=== DONE: {success} success, {push_fail} push-failed, {ver_fail} verify-failed ===")
if results["push_failed"]:
    print("PUSH FAILED:", results["push_failed"])
if results["verify_failed"]:
    print("VERIFY FAILED:", results["verify_failed"])

with open("C:/Projects/baby-mania-agent/output/bulk_push_133_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
