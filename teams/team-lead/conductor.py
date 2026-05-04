#!/usr/bin/env python3
"""
conductor.py — Multi-Stage Plan Executor
Location: teams/team-lead/conductor.py

Reads plans/*.yaml and executes stages one-by-one via bridge.
Sits ABOVE bridge.py + team_lead.py — does NOT modify them.
Communicates via bridge state files only.

Usage:
  python conductor.py plans/bridge-stabilization.yaml
  python conductor.py plans/bridge-stabilization.yaml --dry-run
  python conductor.py plans/bridge-stabilization.yaml --resume
"""

import sys
import os
import time
import json
import yaml
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO             = Path(r"C:\Projects\baby-mania-agent")
BRIDGE_DIR       = REPO / "bridge"
NEXT_TASK_FILE   = BRIDGE_DIR / "next-task.md"
LAST_RESULT_FILE = BRIDGE_DIR / "last-result.md"
STATUS_FILE      = BRIDGE_DIR / "status.md"
CONDUCTOR_STATE  = BRIDGE_DIR / "conductor-state.md"
CONDUCTOR_LOG    = BRIDGE_DIR / "conductor-log.md"
DECISION_RUNS    = BRIDGE_DIR / "decision-engine-runs.yaml"

# ── Timeouts (seconds) ────────────────────────────────────────────────────────
POLL_INTERVAL        = 5    # between status polls
BRIDGE_PICKUP_WAIT   = 60   # max wait for bridge to pick up task
TASK_COMPLETION_WAIT = 720  # max wait for a single task (12 min)
IDLE_WAIT            = 120  # max wait for bridge to become idle before writing

# ── Helpers ───────────────────────────────────────────────────────────────────

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str):
    print(f"[CONDUCTOR] {msg}")


# ── Plan Loading ──────────────────────────────────────────────────────────────

def load_plan(plan_file: str) -> dict:
    """Load and validate a plan YAML file."""
    with open(plan_file, encoding="utf-8") as f:
        plan = yaml.safe_load(f)

    for key in ("plan_id", "plan_name", "approval_tier", "stages"):
        if key not in plan:
            raise ValueError(f"Plan missing required top-level field: {key!r}")

    if not plan["stages"]:
        raise ValueError("Plan has no stages")

    stage_ids = [s.get("id") for s in plan["stages"]]
    if len(stage_ids) != len(set(stage_ids)):
        raise ValueError("Plan has duplicate stage IDs")

    required_stage_fields = [
        "id", "name", "type", "goal", "action", "approval_tier",
        "expected_output", "exit_conditions", "fail_conditions",
        "next_on_pass", "next_on_fail",
    ]
    for stage in plan["stages"]:
        missing = [k for k in required_stage_fields if k not in stage]
        if missing:
            raise ValueError(f"Stage {stage.get('id', '?')} missing fields: {missing}")
        if stage["type"] not in ("AUDIT", "FIX", "LOGIC", "RETEST"):
            raise ValueError(f"Stage {stage['id']}: invalid type {stage['type']!r}")

    return plan


# ── Bridge Status ─────────────────────────────────────────────────────────────

def read_bridge_status() -> str:
    """Return the current status value from bridge/status.md."""
    try:
        for line in STATUS_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("status:"):
                return line.split(":", 1)[1].strip()
    except FileNotFoundError:
        pass
    return "unknown"


def wait_for_bridge_idle(timeout: int = IDLE_WAIT) -> bool:
    """Wait until bridge/status.md shows 'idle'. Returns False on timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if read_bridge_status() == "idle":
            return True
        time.sleep(POLL_INTERVAL)
    return False


def wait_for_bridge_completion(written_at: float,
                               timeout: int = TASK_COMPLETION_WAIT) -> str:
    """
    Wait for bridge to pick up and complete the task written to next-task.md.

    written_at: time.time() captured just before writing next-task.md.
    Returns: 'done' | 'timeout' | 'error'

    Detection logic:
      Phase 1 — pickup: wait for status to leave 'idle' (→ running/starting)
      Phase 2 — running: wait for status to reach 'done' or 'idle'
                         AND last-result.md mtime > written_at
                         AND next-task.md no longer exists
    """
    deadline = time.time() + timeout
    saw_running = False

    while time.time() < deadline:
        status = read_bridge_status()

        if not saw_running:
            if status in ("running", "starting", "waiting_response"):
                saw_running = True
                log(f"  Bridge picked up task (status={status})")
            elif time.time() - written_at > BRIDGE_PICKUP_WAIT:
                log("  Bridge did not pick up task within pickup window")
                return "timeout"

        else:
            if status in ("done", "idle", "token_safe_stop"):
                # Verify result was updated after we wrote the task
                try:
                    result_mtime = os.path.getmtime(LAST_RESULT_FILE)
                except FileNotFoundError:
                    result_mtime = 0.0

                task_gone = (
                    not NEXT_TASK_FILE.exists()
                    or not NEXT_TASK_FILE.read_text(encoding="utf-8").strip()
                )

                if result_mtime > written_at and task_gone:
                    # Content guard: ensure file is non-empty before signalling done.
                    # Prevents race where mtime advances on an intermediate/empty write.
                    try:
                        content = LAST_RESULT_FILE.read_text(encoding="utf-8").strip()
                    except Exception:
                        content = ""
                    if content:
                        if status == "token_safe_stop":
                            return "token_safe_stop"
                        return "done"
                # result not ready yet — keep waiting
            elif status in ("failed", "error", "blocked"):
                # Grace check: bridge may have written result before entering error state
                try:
                    _r_mtime = os.path.getmtime(LAST_RESULT_FILE)
                    _t_gone = (
                        not NEXT_TASK_FILE.exists()
                        or not NEXT_TASK_FILE.read_text(encoding="utf-8").strip()
                    )
                    if _r_mtime > written_at and _t_gone:
                        _content = LAST_RESULT_FILE.read_text(encoding="utf-8").strip()
                        if _content:
                            return "done"
                except Exception:
                    pass
                return "error"
            elif status in ("awaiting_approval", "waiting_response"):
                # Bridge waiting for approval or Telegram response — keep polling
                pass

        time.sleep(POLL_INTERVAL)

    return "timeout"


# ── Reading Result ────────────────────────────────────────────────────────────

def read_last_result() -> str:
    try:
        return LAST_RESULT_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ── Verdict Analysis ──────────────────────────────────────────────────────────

def _clean(line: str) -> str:
    """Strip whitespace + markdown wrappers (*_`#) from a line before keyword matching."""
    return line.strip().strip("*_`#").strip()


def analyze_verdict(output: str, stage: dict) -> str:
    """
    Determine the stage verdict from bridge/last-result.md content.

    Returns one of:
      PASS            — stage completed successfully
      FAIL            — stage failed
      LOGIC_YES       — LOGIC stage: condition met    → next_on_pass
      LOGIC_NO        — LOGIC stage: condition absent → next_on_fail
      BLOCKED         — T3 / approval / manual needed
      UNKNOWN         — cannot determine (treated as FAIL by caller)
    """
    # ── LOGIC: look for <KEY>: YES / NO ──────────────────────────────────────
    if stage["type"] == "LOGIC":
        for line in output.splitlines():
            cleaned = _clean(line).upper()
            if cleaned.endswith(": YES"):
                return "LOGIC_YES"
            if cleaned.endswith(": NO"):
                return "LOGIC_NO"
        return "UNKNOWN"

    # ── Explicit STAGE_VERDICT marker (preferred) ─────────────────────────────
    # NOTE: do NOT do a full-text scan for "awaiting_approval" — audit outputs
    # often mention the keyword in descriptions, causing false BLOCKED verdicts.
    # Only match on structured verdict lines (STAGE_VERDICT: / STATUS:).
    def _match_kw(val: str, kw: str) -> bool:
        """True if val equals kw or starts with kw followed by non-alphanumeric char."""
        return val == kw or (val.startswith(kw) and not val[len(kw):len(kw)+1].isalnum())

    for line in output.splitlines():
        cleaned = _clean(line).upper()
        if cleaned.startswith("STAGE_VERDICT:"):
            val = cleaned.split(":", 1)[1].strip().strip("*_`# ")
            if _match_kw(val, "PASS"):
                return "PASS"
            if _match_kw(val, "FAIL"):
                return "FAIL"
            if _match_kw(val, "AWAITING_APPROVAL"):
                return "BLOCKED"

    # ── Fallback: STATUS field ────────────────────────────────────────────────
    for line in output.splitlines():
        cleaned = _clean(line).upper()
        if cleaned.startswith("STATUS:"):
            val = cleaned.split(":", 1)[1].strip().strip("*_`# ")
            if _match_kw(val, "PASS"):
                return "PASS"
            if _match_kw(val, "FAIL"):
                return "FAIL"
            if _match_kw(val, "AWAITING_APPROVAL"):
                return "BLOCKED"

    return "UNKNOWN"


# ── Task Writing ──────────────────────────────────────────────────────────────

def build_task_text(stage: dict, plan: dict) -> tuple:
    """
    Build the bridge task text for a stage.
    Returns (task_text: str, conductor_task_id: str)
    """
    plan_id  = plan["plan_id"]
    stage_id = stage["id"]
    task_id  = (
        f"conductor-{plan_id}-{stage_id}"
        f"-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )

    # Merge global + stage-level file lists
    g_allowed   = plan.get("global_files_allowed", [])
    g_forbidden = plan.get("global_files_forbidden", [])
    s_allowed   = stage.get("files_allowed", [])
    s_forbidden = stage.get("files_forbidden", [])

    allowed   = s_allowed   if s_allowed   else g_allowed
    forbidden = s_forbidden if s_forbidden else g_forbidden

    def fmt_list(items):
        return "\n".join(f"- {i}" for i in items) if items else "- (not restricted)"

    text = (
        f"TASK_ID: {task_id}\n"
        f"APPROVAL_TIER: {stage['approval_tier']}\n"
        f"CONDUCTOR_PLAN: {plan_id}\n"
        f"CONDUCTOR_STAGE: {stage_id}\n"
        f"\n"
        f"GOAL:\n{stage['goal'].strip()}\n"
        f"\n"
        f"ACTION:\n{stage['action'].strip()}\n"
        f"\n"
        f"FILES_ALLOWED:\n{fmt_list(allowed)}\n"
        f"\n"
        f"FILES_FORBIDDEN:\n{fmt_list(forbidden)}\n"
        f"\n"
        f"EXPECTED:\n{stage['expected_output'].strip()}\n"
        f"\n"
        f"OUTPUT_REQUIRED:\n"
        f"Include in your response:\n"
        f"STAGE_VERDICT: PASS | FAIL | AWAITING_APPROVAL\n"
        f"EVIDENCE: [proof or failure reason]\n"
        f"SYSTEM STATE: [current state after this stage]\n"
    )
    return text, task_id


def write_stage_task(stage: dict, plan: dict) -> tuple:
    """
    Write bridge task to next-task.md.
    Returns (conductor_task_id: str, written_at: float)
    """
    task_text, task_id = build_task_text(stage, plan)
    written_at = time.time()
    NEXT_TASK_FILE.write_text(task_text, encoding="utf-8")
    log(f"  Wrote task: {task_id}")
    return task_id, written_at


# ── Conductor State ───────────────────────────────────────────────────────────

def write_conductor_state(state: dict):
    """Write bridge/conductor-state.md as YAML."""
    state["updated_at"] = now()
    with open(CONDUCTOR_STATE, "w", encoding="utf-8") as f:
        yaml.dump(state, f, allow_unicode=True, default_flow_style=False,
                  sort_keys=False)


def load_conductor_state() -> dict:
    """Load bridge/conductor-state.md. Returns {} if missing."""
    try:
        with open(CONDUCTOR_STATE, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def append_conductor_log(entry: str):
    """Append a timestamped entry to bridge/conductor-log.md."""
    if not CONDUCTOR_LOG.exists():
        CONDUCTOR_LOG.write_text(
            "| time | entry |\n|------|-------|\n",
            encoding="utf-8"
        )
    with open(CONDUCTOR_LOG, "a", encoding="utf-8") as f:
        f.write(f"| {now()} | {entry} |\n")


# ── Decision Engine ──────────────────────────────────────────────────────────

def _load_decision_engine(plan: dict) -> dict | None:
    """Load decision engine YAML referenced by plan.decision_engine. Returns None if absent."""
    ref = plan.get("decision_engine")
    if not ref:
        return None
    path = REPO / ref
    if not path.exists():
        log(f"  WARNING: decision_engine file not found: {path}")
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _compute_batch_metrics(state: dict) -> dict:
    """Derive success_rate, failure_patterns, critical_failure from conductor state."""
    completed = state.get("completed_stages", [])
    failed    = state.get("failed_stages", [])
    total     = len(completed) + len(failed)

    success_rate     = 100 if total == 0 else int(len(completed) / total * 100)
    failure_patterns = len(set(failed))          # distinct stage IDs that failed
    critical_failure = (
        state.get("overall_verdict") in ("BLOCKED", "FAILED")
        and len(failed) > 0
    )
    return {
        "success_rate":     success_rate,
        "failure_patterns": failure_patterns,
        "critical_failure": critical_failure,
        "completed_count":  len(completed),
        "failed_count":     len(failed),
    }


def _update_clean_runs(plan_id: str, run_passed: bool) -> int:
    """Increment (on pass) or reset (on fail) clean_runs for plan_id. Returns new value."""
    try:
        with open(DECISION_RUNS, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        data = {}

    entry = data.get(plan_id, {"clean_runs": 0})
    entry["clean_runs"] = (entry.get("clean_runs", 0) + 1) if run_passed else 0
    entry["last_updated"] = now()
    data[plan_id] = entry

    with open(DECISION_RUNS, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return entry["clean_runs"]


def _evaluate_decision_state(engine: dict, metrics: dict) -> str:
    """
    Match metrics against DECISION_ENGINE thresholds.
    Evaluation order (most critical first):
      STOP > FIX_AND_RETEST > READY_FOR_FULL > READY_FOR_SCALE > READY_FOR_ROLLOUT
    """
    cfg         = engine.get("DECISION_ENGINE", {})
    sr          = metrics["success_rate"]
    fp          = metrics["failure_patterns"]
    cr          = metrics["clean_runs"]
    cf          = metrics["critical_failure"]
    stop_on     = cfg.get("stop_on_patterns", 2)
    scale_after = cfg.get("scale_after_runs", 2)
    full_after  = cfg.get("full_after_runs", 3)

    if fp >= stop_on or cf:
        return "STOP"
    if sr < 100:
        return "FIX_AND_RETEST"
    if sr == 100 and fp == 0 and cr >= full_after:
        return "READY_FOR_FULL"
    if sr == 100 and fp == 0 and cr >= scale_after:
        return "READY_FOR_SCALE"
    return "READY_FOR_ROLLOUT"


MAX_CHAIN_DEPTH = 5


def run_post_batch_decision(plan: dict, state: dict, dry_run: bool = False,
                            no_telegram: bool = False, _chain_depth: int = 0):
    """
    Evaluate POST_BATCH_DECISION if defined in plan. Called at end of run_plan().
    No-op (backward-compatible) if plan lacks POST_BATCH_DECISION or decision_engine.

    Writes decision result into conductor-state.md and conductor-log.md.
    For STOP / FIX_AND_RETEST: marks state as FAILED so next run is blocked.
    For READY_FOR_SCALE / READY_FOR_FULL / FIX_AND_RETEST: auto-chains next plan
      if plan defines next_plan_on.<decision>. Requires no error state.
    Loop protection: aborts chain if _chain_depth >= MAX_CHAIN_DEPTH.
    """
    if not plan.get("POST_BATCH_DECISION"):
        return

    engine = _load_decision_engine(plan)
    if not engine:
        log("  POST_BATCH_DECISION: decision_engine not loadable — skipping evaluation")
        return

    plan_id    = plan["plan_id"]
    metrics    = _compute_batch_metrics(state)
    run_passed = state.get("overall_verdict") == "PASS"
    clean_runs = _update_clean_runs(plan_id, run_passed)
    metrics["clean_runs"] = clean_runs

    decision = _evaluate_decision_state(engine, metrics)
    action   = plan["POST_BATCH_DECISION"].get("actions", {}).get(decision, "(no action defined)")

    log("\n── POST_BATCH_DECISION ──────────────────────────────────────────")
    log(f"  success_rate:     {metrics['success_rate']}%")
    log(f"  failure_patterns: {metrics['failure_patterns']}")
    log(f"  clean_runs:       {metrics['clean_runs']}")
    log(f"  critical_failure: {metrics['critical_failure']}")
    log(f"  → MATCHED STATE:  {decision}")
    log(f"  → ACTION:         {action}")
    log(f"  chain_depth:      {_chain_depth}/{MAX_CHAIN_DEPTH}")
    log("────────────────────────────────────────────────────────────────")

    state["post_batch_decision"] = {
        "evaluated_at":    now(),
        "metrics":         metrics,
        "matched_state":   decision,
        "action":          action,
        "chain_depth":     _chain_depth,
    }
    write_conductor_state(state)

    append_conductor_log(
        f"POST_BATCH_DECISION: {decision} | "
        f"sr={metrics['success_rate']}% fp={metrics['failure_patterns']} "
        f"runs={metrics['clean_runs']} cf={metrics['critical_failure']} | "
        f"action={action}"
    )

    # ── STOP: hard halt ───────────────────────────────────────────────────────
    if decision == "STOP":
        log("  HALTING — failure_patterns threshold reached or critical failure")
        state["status"]         = "FAILED"
        state["blocked_reason"] = f"POST_BATCH_DECISION STOP: {action}"
        write_conductor_state(state)
        return

    # ── FIX_AND_RETEST: mark failed, then try to chain fix plan ──────────────
    if decision == "FIX_AND_RETEST":
        log("  STOPPING ROLLOUT — fix stage required before next run")
        state["status"]         = "FAILED"
        state["blocked_reason"] = "POST_BATCH_DECISION FIX_AND_RETEST: fix required"
        write_conductor_state(state)
        _try_chain_next_plan(plan, decision, dry_run, no_telegram, _chain_depth)
        return

    # ── READY_FOR_SCALE / READY_FOR_FULL: chain next plan if defined ──────────
    if decision in ("READY_FOR_SCALE", "READY_FOR_FULL"):
        log(f"  READY — attempting to chain next plan for: {decision}")
        _try_chain_next_plan(plan, decision, dry_run, no_telegram, _chain_depth)
        return

    # ── READY_FOR_ROLLOUT: no chaining (initial state) ────────────────────────
    log(f"  READY_FOR_ROLLOUT — no auto-chain at this state")


def _try_chain_next_plan(plan: dict, decision: str, dry_run: bool,
                         no_telegram: bool, chain_depth: int):
    """
    Check plan.next_plan_on.<decision> and run the referenced plan if safe to do so.
    Enforces loop protection and skips if plan defines requires_approval: true.
    """
    # ── Loop protection ───────────────────────────────────────────────────────
    if chain_depth >= MAX_CHAIN_DEPTH:
        log(f"  CHAIN LIMIT REACHED ({chain_depth}/{MAX_CHAIN_DEPTH}) — stopping auto-chain")
        append_conductor_log(
            f"CHAIN_LIMIT: depth={chain_depth} reached on decision={decision} — halted"
        )
        return

    # ── Check if plan defines next_plan_on for this decision ─────────────────
    next_plan_on = plan.get("next_plan_on", {})
    if not next_plan_on:
        log(f"  next_plan_on not defined in plan — log only, no auto-chain")
        return

    next_plan_file = next_plan_on.get(decision)
    if not next_plan_file:
        log(f"  next_plan_on.{decision} not defined — log only, no auto-chain")
        return

    next_plan_path = REPO / next_plan_file
    if not next_plan_path.exists():
        log(f"  WARNING: next plan file not found: {next_plan_path}")
        append_conductor_log(
            f"CHAIN_MISSING_FILE: {next_plan_file} for decision={decision}"
        )
        return

    # ── Load next plan to check approval requirement ──────────────────────────
    try:
        next_plan = load_plan(str(next_plan_path))
    except Exception as e:
        log(f"  ERROR loading next plan {next_plan_file}: {e}")
        append_conductor_log(f"CHAIN_LOAD_ERROR: {next_plan_file} — {e}")
        return

    # ── Safety gate: skip auto-run if plan requires approval ─────────────────
    if next_plan.get("requires_approval"):
        log(f"  next plan requires_approval=true — sending Telegram instead of auto-run")
        append_conductor_log(
            f"CHAIN_APPROVAL_REQUIRED: {next_plan_file} — manual trigger needed"
        )
        _notify_chain_requires_approval(next_plan_file, decision)
        return

    # ── Safe to auto-run ──────────────────────────────────────────────────────
    log(f"\n── AUTO-CHAIN: {decision} → {next_plan_file} (depth={chain_depth + 1}) ──")
    append_conductor_log(
        f"CHAIN_START: depth={chain_depth + 1} decision={decision} plan={next_plan_file}"
    )
    run_plan(str(next_plan_path), dry_run=dry_run, no_telegram=no_telegram,
             _chain_depth=chain_depth + 1)


def _notify_chain_requires_approval(next_plan_file: str, decision: str):
    """
    Write a Telegram notification request when next plan needs manual approval.
    Uses the same conductor-notify.md mechanism the rest of the system uses.
    """
    notify_file = BRIDGE_DIR / "conductor-notify.md"
    msg = (
        f"CHAIN_APPROVAL_NEEDED\n"
        f"decision: {decision}\n"
        f"next_plan: {next_plan_file}\n"
        f"action: manual trigger required — run conductor.py with this plan\n"
        f"time: {now()}\n"
    )
    try:
        notify_file.write_text(msg, encoding="utf-8")
        log(f"  Telegram notification written to conductor-notify.md")
    except Exception as e:
        log(f"  WARNING: could not write conductor-notify.md: {e}")


# ── Preflight Check ───────────────────────────────────────────────────────────

def _get_python_procs() -> list:
    """Return list of (pid, cmdline) for all running Python processes."""
    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                "Get-WmiObject Win32_Process | "
                "Where-Object { $_.Name -like 'python*' } | "
                "Select-Object ProcessId,CommandLine | "
                "ConvertTo-Json -Compress"
            ],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0 or not result.stdout.strip():
            return []
        data = json.loads(result.stdout.strip())
        if isinstance(data, dict):
            data = [data]
        return [(str(p.get("ProcessId", "")), p.get("CommandLine") or "") for p in data]
    except Exception:
        return []


def preflight_check(no_telegram: bool = False, resume: bool = False) -> tuple:
    """
    Check system readiness before starting a plan run.
    Returns (ok: bool, reason: str).

    Blocks if:
      - github-bridge.py not running
      - telegram_bot.py not running (skipped when no_telegram=True)
      - watchdog.py not running
      - more than 1 bridge instance running
      - more than 1 conductor instance running
      - next-task.md exists and is non-empty
      - bridge status not idle
      - conductor-state.md shows active RUNNING/BLOCKED state
    """
    procs = _get_python_procs()

    def count_script(name: str) -> int:
        return sum(1 for _, cmd in procs if name in cmd)

    # 1. bridge running? (exclude github-bridge.py — substring collision)
    bridge_count = sum(
        1 for _, cmd in procs
        if "bridge.py" in cmd and "github-bridge.py" not in cmd
    )
    if bridge_count == 0:
        return False, "bridge.py is not running"

    # 2. telegram_bot.py running? (skipped in --no-telegram mode)
    if not no_telegram and count_script("telegram_bot.py") == 0:
        return False, "telegram_bot.py is not running"

    # 3. watchdog.py running?
    if count_script("watchdog.py") == 0:
        return False, "watchdog.py is not running"

    # 4. More than 1 bridge instance? (re-uses bridge_count from above)
    if bridge_count > 1:
        return False, f"Multiple bridge.py instances running ({bridge_count}) — kill duplicates first"

    # 5. More than 1 conductor instance?
    conductor_count = count_script("conductor.py")
    if conductor_count > 1:
        return False, f"Multiple conductor instances running ({conductor_count})"

    # 6. next-task.md not empty?
    if NEXT_TASK_FILE.exists() and NEXT_TASK_FILE.read_text(encoding="utf-8").strip():
        return False, "next-task.md exists and is non-empty — bridge may be busy"

    # 7. Bridge status not idle?
    bridge_status = read_bridge_status()
    if bridge_status not in ("idle", "unknown"):
        return False, f"Bridge status is '{bridge_status}', expected idle"

    # 8. Stale active conductor-state? (skipped when resuming — user acknowledges existing state)
    if not resume and CONDUCTOR_STATE.exists():
        prev = load_conductor_state()
        if prev.get("status") in ("RUNNING", "BLOCKED"):
            return False, (
                f"conductor-state.md has status={prev.get('status')!r} "
                f"(plan={prev.get('plan_id')!r}) — use --resume or clear state first"
            )

    return True, ""


# ── Main Execution Loop ───────────────────────────────────────────────────────

def run_plan(plan_file: str, dry_run: bool = False, resume: bool = False,
             no_telegram: bool = False, _chain_depth: int = 0):
    log(f"Loading plan: {plan_file}")
    if no_telegram:
        log("  --no-telegram: telegram_bot.py check skipped. T3 requires manual approval via bridge/telegram-response.md")
    plan = load_plan(plan_file)
    plan_id    = plan["plan_id"]
    stages_map = {s["id"]: s for s in plan["stages"]}
    first_id   = plan["stages"][0]["id"]

    # ── Preflight check (skip in dry-run) ────────────────────────────────────
    if not dry_run:
        log("Running preflight checks...")
        ok, reason = preflight_check(no_telegram=no_telegram, resume=resume)
        if not ok:
            log(f"PREFLIGHT FAILED: {reason}")
            log("Conductor aborted — fix the above before running.")
            sys.exit(1)
        log("  Preflight OK")

    # ── Init or resume state ──────────────────────────────────────────────────
    if resume and CONDUCTOR_STATE.exists():
        state = load_conductor_state()
        current_stage_id = state.get("current_stage", first_id)
        log(f"Resuming from stage: {current_stage_id}")
    else:
        state = {
            "plan_id":          plan_id,
            "plan_file":        plan_file,
            "status":           "RUNNING",
            "current_stage":    first_id,
            "current_task_id":  "",
            "completed_stages": [],
            "failed_stages":    [],
            "skipped_stages":   [],
            "blocked_reason":   "",
            "waiting_for":      "",
            "next_stage":       "",
            "overall_verdict":  "IN_PROGRESS",
            "started_at":       now(),
        }
        current_stage_id = first_id

    write_conductor_state(state)
    mode_label = "RESUMED" if (resume and CONDUCTOR_STATE.exists()) else "STARTED"
    append_conductor_log(f"{mode_label}: {plan_id}")
    log(f"Plan: {plan['plan_name']} ({len(plan['stages'])} stages)")

    if dry_run:
        log("DRY RUN mode — will not write to bridge")

    # ── Stage loop ────────────────────────────────────────────────────────────
    while current_stage_id not in ("DONE", "STOP", None):

        stage = stages_map.get(current_stage_id)
        if not stage:
            log(f"ERROR: Stage not found in plan: {current_stage_id!r}")
            state.update({
                "status":         "BLOCKED",
                "blocked_reason": f"Stage ID not found: {current_stage_id}",
            })
            write_conductor_state(state)
            append_conductor_log(f"BLOCKED: unknown stage {current_stage_id}")
            break

        log(f"\n── {stage['id']}: {stage['name']}"
            f"  (type={stage['type']}, tier={stage['approval_tier']}) ──")

        # ── Dry run: walk without executing ──────────────────────────────────
        if dry_run:
            log(f"  [DRY RUN] Would execute: {stage['goal'][:80]}")
            state["completed_stages"].append(stage["id"])
            current_stage_id = stage["next_on_pass"]
            state["current_stage"] = current_stage_id
            write_conductor_state(state)
            continue

        # ── Wait for bridge to be free ────────────────────────────────────────
        log("  Waiting for bridge idle...")
        if not wait_for_bridge_idle():
            log("  Bridge not idle — cannot proceed")
            state.update({
                "status":         "BLOCKED",
                "blocked_reason": "Bridge not idle after timeout",
                "waiting_for":    "BRIDGE_IDLE",
            })
            write_conductor_state(state)
            append_conductor_log(f"BLOCKED {stage['id']}: bridge not idle")
            break

        # ── Write task to bridge ──────────────────────────────────────────────
        state.update({"status": "RUNNING", "current_stage": stage["id"]})
        write_conductor_state(state)

        task_id, written_at = write_stage_task(stage, plan)
        state["current_task_id"] = task_id
        write_conductor_state(state)
        append_conductor_log(f"STARTED {stage['id']} [{task_id}]")

        # ── Wait for completion ───────────────────────────────────────────────
        log("  Waiting for bridge to complete...")
        completion = wait_for_bridge_completion(written_at)
        output = read_last_result()

        if completion == "timeout":
            log(f"  TIMEOUT on {stage['id']}")
            verdict = "UNKNOWN"
            append_conductor_log(f"TIMEOUT {stage['id']}")
        elif completion == "error":
            log(f"  BRIDGE ERROR on {stage['id']}")
            verdict = analyze_verdict(output, stage)  # might still have useful output
            # Preserve BLOCKED (e.g. T3 AWAITING_APPROVAL) — do not downgrade to FAIL
            if verdict not in ("PASS", "LOGIC_YES", "LOGIC_NO", "BLOCKED"):
                verdict = "FAIL"
            append_conductor_log(f"ERROR {stage['id']}")
        else:
            verdict = analyze_verdict(output, stage)
            log(f"  Verdict: {verdict}")

        append_conductor_log(f"  {stage['id']} | {verdict}")

        # ── Route based on verdict ────────────────────────────────────────────
        if verdict in ("PASS", "LOGIC_YES"):
            state["completed_stages"].append(stage["id"])
            current_stage_id = stage["next_on_pass"]
            state["status"] = "RUNNING"

        elif verdict == "LOGIC_NO":
            # Alternate path — NOT a failure
            state["completed_stages"].append(stage["id"])
            current_stage_id = stage["next_on_fail"]
            state["status"] = "RUNNING"

        elif verdict in ("FAIL", "UNKNOWN"):
            state["failed_stages"].append(stage["id"])
            next_id = stage["next_on_fail"]

            if next_id == "STOP":
                log(f"  STOP — {stage['id']} failed, plan stopping")
                current_stage_id = "STOP"
            elif next_id == "SKIP":
                state["skipped_stages"].append(stage["id"])
                ids = [s["id"] for s in plan["stages"]]
                idx = ids.index(stage["id"])
                current_stage_id = ids[idx + 1] if idx + 1 < len(ids) else "DONE"
            else:
                current_stage_id = next_id

            state["status"] = "RUNNING"

        elif verdict == "BLOCKED":
            log(f"  BLOCKED — {stage['id']} needs manual intervention")
            state.update({
                "status":         "BLOCKED",
                "blocked_reason": f"Stage blocked: {stage['id']}",
                "waiting_for":    "MANUAL_INTERVENTION",
            })
            write_conductor_state(state)
            append_conductor_log(
                f"BLOCKED {stage['id']}: approval or manual intervention needed"
            )
            current_stage_id = "STOP"

        state["next_stage"] = current_stage_id
        write_conductor_state(state)

    # ── Final verdict ─────────────────────────────────────────────────────────
    if current_stage_id == "DONE":
        state.update({"overall_verdict": "PASS", "status": "DONE"})
        append_conductor_log(f"PLAN DONE: {plan_id} — PASS")
        log(f"\n✓ PLAN DONE: {plan['plan_name']}")

    elif current_stage_id == "STOP":
        is_blocked = (state.get("status") == "BLOCKED")
        state.update({
            "overall_verdict": "BLOCKED" if is_blocked else "FAILED",
            "status":          "FAILED",
        })
        append_conductor_log(
            f"PLAN STOPPED: {plan_id} at {state.get('current_stage')}"
        )
        log(f"\n✗ PLAN STOPPED at {state.get('current_stage')}")

    write_conductor_state(state)

    # ── POST_BATCH_DECISION (no-op if plan doesn't define it) ─────────────────
    run_post_batch_decision(plan, state, dry_run=dry_run,
                            no_telegram=no_telegram, _chain_depth=_chain_depth)


# ── Bridge Room Mode ──────────────────────────────────────────────────────────

BRIDGE_ROOM_BASE     = REPO / "docs" / "management" / "bridge-room-prototype"
BRIDGE_ROOM_INBOX    = BRIDGE_ROOM_BASE / "inbox"
BRIDGE_ROOM_VERDICTS = BRIDGE_ROOM_BASE / "verdicts"
BRIDGE_ROOM_OUTBOX   = BRIDGE_ROOM_BASE / "outbox"
BRIDGE_ROOM_JOURNAL  = BRIDGE_ROOM_BASE / "journal"
BRIDGE_ROOM_STATE    = BRIDGE_ROOM_BASE / "room-state.json"
SESSION_REGISTRY     = REPO / "docs" / "management" / "bridge-room-session-registry.json"
PACK_REGISTRY        = REPO / "docs" / "management" / "bridge-room-pack-registry.json"

VERDICT_POLL_TIMEOUT  = 300   # 5 min max for Codex to write verdict
VERDICT_POLL_INTERVAL = 10


def load_execution_pack(pack_file: str) -> dict:
    """Load and validate an Execution Pack YAML."""
    with open(pack_file, encoding="utf-8") as f:
        pack = yaml.safe_load(f)
    for field in ("pack_id", "room_id", "stages"):
        if field not in pack:
            raise ValueError(f"Execution Pack missing required field: {field!r}")
    if not pack["stages"]:
        raise ValueError("Execution Pack has no stages")
    return pack


def build_brm_task_text(stage: dict, pack: dict, session_id: str) -> tuple:
    """Build bridge task text for a Bridge Room stage. Returns (task_text, task_id)."""
    ts       = datetime.now().strftime("%Y%m%d-%H%M")
    pack_id  = pack["pack_id"]
    stage_id = stage["id"]
    room_id  = pack["room_id"]
    task_id  = f"brm-{pack_id}-{stage_id}-{ts}"

    lines = [
        f"TASK_ID: {task_id}",
        f"APPROVAL_TIER: T2",
        f"ROOM_ID: {room_id}",
        f"PACK_ID: {pack_id}",
        f"STAGE_ID: {stage_id}",
        f"SESSION_ID: {session_id}",
        f"STAGE_TYPE: {stage.get('type', 'UNKNOWN')}",
        f"GOAL: {stage.get('goal', '')}",
    ]
    if stage.get("targets"):
        t = stage["targets"]
        lines.append(f"TARGETS: {', '.join(t) if isinstance(t, list) else t}")
    if stage.get("files_allowed"):
        fa = stage["files_allowed"]
        lines.append(f"FILES_ALLOWED: {', '.join(fa) if isinstance(fa, list) else fa}")
    lines.append("OUTPUT_REQUIRED: Emit BRIDGE_ROOM_OUTPUT_START ... BRIDGE_ROOM_OUTPUT_END block with structured JSON")
    if stage.get("context"):
        lines.append(f"CONTEXT: {stage['context']}")
    return "\n".join(lines), task_id


def brm_journal(pack_id: str, event_type: str, data: dict):
    """Append a journal event to the pack journal JSONL file."""
    ts    = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    event = {"ts": ts, "event": event_type, "pack_id": pack_id, **data}
    jfile = BRIDGE_ROOM_JOURNAL / f"{pack_id}-log.jsonl"
    with open(jfile, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def brm_update_state(updates: dict):
    """Atomically update room-state.json."""
    state = {}
    if BRIDGE_ROOM_STATE.exists():
        state = json.loads(BRIDGE_ROOM_STATE.read_text(encoding="utf-8"))
    state.update(updates)
    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tmp = Path(str(BRIDGE_ROOM_STATE) + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(BRIDGE_ROOM_STATE)


def brm_wait_for_verdict(pack_id: str, stage_id: str) -> dict:
    """Poll verdicts/ for verdict file. Returns dict or None on timeout."""
    vfile    = BRIDGE_ROOM_VERDICTS / f"{pack_id}-{stage_id}-verdict.json"
    deadline = time.time() + VERDICT_POLL_TIMEOUT
    while time.time() < deadline:
        if vfile.exists():
            return json.loads(vfile.read_text(encoding="utf-8"))
        time.sleep(VERDICT_POLL_INTERVAL)
    return None


def brm_extract_output(raw: str) -> dict:
    """Extract JSON from BRIDGE_ROOM_OUTPUT_START...END block. Returns dict or None."""
    START, END = "BRIDGE_ROOM_OUTPUT_START", "BRIDGE_ROOM_OUTPUT_END"
    if START not in raw or END not in raw:
        return None
    block = raw[raw.index(START) + len(START):raw.index(END)].strip()
    try:
        return json.loads(block)
    except json.JSONDecodeError:
        return {"raw_block": block}


def brm_detect_tss(raw: str) -> dict:
    """Detect TOKEN_SAFE_STOP_START...END block. Returns dict or None."""
    START, END = "TOKEN_SAFE_STOP_START", "TOKEN_SAFE_STOP_END"
    if START not in raw or END not in raw:
        return None
    block = raw[raw.index(START) + len(START):raw.index(END)].strip()
    try:
        return json.loads(block)
    except json.JSONDecodeError:
        return {"raw_block": block}


def run_bridge_room(pack_file: str, dry_run: bool = False):
    """Execute an Execution Pack via the Bridge Room loop."""
    pack       = load_execution_pack(pack_file)
    pack_id    = pack["pack_id"]
    room_id    = pack["room_id"]
    stages     = pack["stages"]
    session_id = f"SES-{pack_id}-{datetime.now().strftime('%Y%m%d-%H%M')}"

    log(f"Bridge Room: pack_id={pack_id} room_id={room_id} stages={len(stages)} session={session_id}")

    if dry_run:
        log("DRY RUN — validating pack schema, no bridge dispatch")
        for i, s in enumerate(stages, 1):
            log(f"  STAGE {i}: id={s.get('id')} type={s.get('type')} goal={str(s.get('goal',''))[:60]}")
        log("Pack validation: PASS")
        return

    brm_update_state({"pack_id": pack_id, "room_id": room_id,
                      "pack_status": "RUNNING", "session_id": session_id,
                      "current_stage": None})
    brm_journal(pack_id, "EVT_PACK_START",
                {"room_id": room_id, "session_id": session_id, "stage_count": len(stages)})

    pack_result = "UNKNOWN"

    for stage in stages:
        stage_id   = stage["id"]
        stage_type = stage.get("type", "UNKNOWN")
        log(f"\nDispatching {stage_id} ({stage_type})")
        brm_update_state({"current_stage": stage_id, "stage_status": "RUNNING"})
        brm_journal(pack_id, "EVT_STAGE_START",
                    {"stage_id": stage_id, "stage_type": stage_type})

        if not wait_for_bridge_idle():
            log(f"Bridge not idle before {stage_id} — aborting")
            brm_journal(pack_id, "EVT_STAGE_ERROR",
                        {"stage_id": stage_id, "reason": "bridge_not_idle"})
            pack_result = "PACK_FAILED"
            break

        task_text, task_id = build_brm_task_text(stage, pack, session_id)
        written_at = time.time()
        NEXT_TASK_FILE.write_text(task_text, encoding="utf-8")
        log(f"Task written: {task_id}")

        outcome = wait_for_bridge_completion(written_at)
        if outcome == "token_safe_stop":
            log(f"TOKEN_SAFE_STOP status from bridge on {stage_id}")
            raw = read_last_result()
            tss = brm_detect_tss(raw)
            brm_journal(pack_id, "EVT_TOKEN_SAFE_STOP",
                        {"stage_id": stage_id, "tss_present": tss is not None})
            brm_update_state({"pack_status": "TOKEN_SAFE_STOP"})
            pack_result = "TOKEN_SAFE_STOP"
            break
        if outcome == "timeout":
            log(f"Bridge timeout on {stage_id}")
            brm_journal(pack_id, "EVT_STAGE_ERROR",
                        {"stage_id": stage_id, "reason": "bridge_timeout"})
            brm_update_state({"pack_status": "TOKEN_SAFE_STOP"})
            pack_result = "TOKEN_SAFE_STOP"
            break
        if outcome == "error":
            log(f"Bridge error on {stage_id}")
            brm_journal(pack_id, "EVT_STAGE_ERROR",
                        {"stage_id": stage_id, "reason": "bridge_error"})
            pack_result = "PACK_FAILED"
            break

        raw = read_last_result()
        if not raw:
            log(f"No result content after {stage_id}")
            pack_result = "PACK_FAILED"
            break

        tss = brm_detect_tss(raw)
        if tss:
            log(f"TOKEN_SAFE_STOP block in output for {stage_id}")
            brm_journal(pack_id, "EVT_TOKEN_SAFE_STOP",
                        {"stage_id": stage_id, "tss": tss})
            brm_update_state({"pack_status": "TOKEN_SAFE_STOP"})
            pack_result = "TOKEN_SAFE_STOP"
            break

        brm_out = brm_extract_output(raw)
        if not brm_out:
            log(f"WARNING: no BRIDGE_ROOM_OUTPUT block in {stage_id} — treating as ERROR")
            brm_journal(pack_id, "EVT_STAGE_ERROR",
                        {"stage_id": stage_id, "reason": "no_brm_output_block"})
            pack_result = "PACK_FAILED"
            break

        out_file = BRIDGE_ROOM_INBOX / f"{pack_id}-{stage_id}-output.json"
        out_file.write_text(json.dumps(brm_out, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        brm_journal(pack_id, "EVT_OUTPUT_WRITTEN",
                    {"stage_id": stage_id, "output_file": str(out_file)})

        log(f"Waiting for Codex verdict on {stage_id}...")
        verdict = brm_wait_for_verdict(pack_id, stage_id)
        if verdict is None:
            log(f"Verdict timeout on {stage_id}")
            brm_journal(pack_id, "EVT_VERDICT_TIMEOUT", {"stage_id": stage_id})
            brm_update_state({"pack_status": "TOKEN_SAFE_STOP"})
            pack_result = "TOKEN_SAFE_STOP"
            break

        v = verdict.get("verdict", "UNKNOWN")
        log(f"Verdict: {v}")
        brm_journal(pack_id, "EVT_VERDICT_RECEIVED",
                    {"stage_id": stage_id, "verdict": v})

        if v == "PASS":
            brm_update_state({"stage_status": "PASS"})
            if stage is stages[-1]:
                pack_result = "PACK_COMPLETE"
        elif v == "FAIL":
            brm_update_state({"stage_status": "FAIL"})
            pack_result = "PACK_FAILED"
            break
        elif v == "BLOCKED":
            esc_id   = f"ESC-{pack_id}-{stage_id}"
            esc_file = BRIDGE_ROOM_OUTBOX / f"{esc_id}-escalation.json"
            esc_file.write_text(
                json.dumps({"escalation_id": esc_id, "pack_id": pack_id,
                            "stage_id": stage_id, "verdict": verdict},
                           ensure_ascii=False, indent=2),
                encoding="utf-8")
            brm_update_state({"pack_status": "BLOCKED", "stage_status": "BLOCKED",
                               "pending_decision": {"escalation_id": esc_id,
                                                    "stage_id": stage_id,
                                                    "consumed": False}})
            brm_journal(pack_id, "EVT_BLOCKED",
                        {"stage_id": stage_id, "escalation_id": esc_id})
            pack_result = "BLOCKED"
            break
        else:
            brm_update_state({"stage_status": "ERROR"})
            pack_result = "PACK_FAILED"
            break

    brm_update_state({"pack_status": pack_result, "current_stage": None})
    brm_journal(pack_id, "EVT_PACK_END", {"result": pack_result})
    log(f"\nBridge Room complete: {pack_result}")


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="conductor.py — Multi-Stage Plan Executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python conductor.py plans/bridge-stabilization.yaml\n"
            "  python conductor.py plans/bridge-stabilization.yaml --dry-run\n"
            "  python conductor.py --mode bridge-room --pack plans/execution-packs/exec-dry-run-001.yaml\n"
        ),
    )
    parser.add_argument(
        "plan_file", nargs="?",
        help="Path to conductor plan YAML (conductor mode only)"
    )
    parser.add_argument(
        "--mode", default="conductor", choices=["conductor", "bridge-room"],
        help="Execution mode: conductor (default) or bridge-room"
    )
    parser.add_argument(
        "--pack",
        help="Path to Execution Pack YAML (bridge-room mode only)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Walk through stages without writing to bridge"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Resume from last conductor-state.md checkpoint (conductor mode only)"
    )
    parser.add_argument(
        "--no-telegram", action="store_true",
        help="Skip telegram_bot.py preflight check"
    )
    args = parser.parse_args()

    if args.mode == "bridge-room":
        if not args.pack:
            print("ERROR: --pack <yaml> required in bridge-room mode")
            sys.exit(1)
        if not os.path.exists(args.pack):
            print(f"ERROR: Pack file not found: {args.pack}")
            sys.exit(1)
        run_bridge_room(args.pack, dry_run=args.dry_run)
        return

    # Conductor mode
    if not args.plan_file:
        print("ERROR: plan_file required in conductor mode")
        sys.exit(1)
    if not os.path.exists(args.plan_file):
        print(f"ERROR: Plan file not found: {args.plan_file}")
        sys.exit(1)
    run_plan(args.plan_file, dry_run=args.dry_run, resume=args.resume,
             no_telegram=args.no_telegram)


if __name__ == "__main__":
    main()
