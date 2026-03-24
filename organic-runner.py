#!/usr/bin/env python3
"""
organic-runner.py — BabyMania Organic Pipeline Queue Controller

Semi-manual queue controller. This script does NOT run agents autonomously.
It manages task order, state, and dependencies. Claude runs each agent manually
based on what this runner displays.

Usage:
    python organic-runner.py                        -- show next pending task
    python organic-runner.py --done                 -- mark current running task as done
    python organic-runner.py --failed "reason"      -- mark current running task as failed
    python organic-runner.py --status               -- print full queue status
    python organic-runner.py --queue path/to/file   -- use a different queue file

Queue file default: teams/organic/organic-task-queue.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DEFAULT_QUEUE = BASE_DIR / "teams" / "organic" / "organic-task-queue.json"


def resolve_path(path_str: str) -> Path:
    """Resolve a path string against BASE_DIR if relative, leave absolute paths unchanged."""
    p = Path(path_str)
    return p if p.is_absolute() else BASE_DIR / p

ALLOWED_STATUSES = {"pending", "running", "done", "failed", "blocked"}
REQUIRED_FIELDS  = {"id", "agent", "description", "status", "depends_on", "output_file"}


# ── Schema Validation ──────────────────────────────────────────────────────────

def validate_queue(tasks: list[dict]) -> list[str]:
    """
    Validate queue schema. Returns list of error strings (empty = valid).
    Rules:
      1. unique ids
      2. depends_on must reference existing ids
      3. no circular dependencies
      4. allowed status values only
      5. required fields per task
    """
    errors = []
    ids_seen: set[str] = set()
    all_ids: set[str] = {t.get("id", "") for t in tasks}

    for task in tasks:
        tid = task.get("id", "<missing>")

        # Rule 5 — required fields
        missing = REQUIRED_FIELDS - set(task.keys())
        if missing:
            errors.append(f"INVALID: missing field(s) {missing} in task '{tid}'")

        # Rule 1 — unique ids
        if tid in ids_seen:
            errors.append(f"INVALID: duplicate id '{tid}'")
        ids_seen.add(tid)

        # Rule 4 — status whitelist
        status = task.get("status", "")
        if status not in ALLOWED_STATUSES:
            errors.append(f"INVALID: unknown status '{status}' in task '{tid}'")

        # Rule 2 — depends_on refs
        for dep in task.get("depends_on", []):
            if dep not in all_ids:
                errors.append(f"INVALID: depends_on '{dep}' not found (task '{tid}')")

    # Rule 3 — no circular dependencies
    errors.extend(_check_circular(tasks))

    return errors


def _check_circular(tasks: list[dict]) -> list[str]:
    """Detect circular dependencies using DFS."""
    graph: dict[str, list[str]] = {t["id"]: t.get("depends_on", []) for t in tasks if "id" in t}
    visited:  set[str] = set()
    rec_stack: set[str] = set()

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return [f"INVALID: circular dependency detected involving '{node}'"]
    return []


# ── Queue I/O ─────────────────────────────────────────────────────────────────

def load_queue(path: Path) -> dict:
    if not path.exists():
        print(f"[ERROR] Queue file not found: {path}")
        sys.exit(1)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] Queue file is not valid JSON: {e}")
        sys.exit(1)

    errors = validate_queue(data.get("tasks", []))
    if errors:
        print("[ERROR] Queue validation failed:")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)

    return data


def save_queue(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Task Logic ────────────────────────────────────────────────────────────────

def find_running(tasks: list[dict]) -> dict | None:
    return next((t for t in tasks if t["status"] == "running"), None)


def find_next_pending(tasks: list[dict]) -> dict | None:
    """Return first pending task whose all depends_on are done."""
    done_ids = {t["id"] for t in tasks if t["status"] == "done"}
    for task in tasks:
        if task["status"] == "pending":
            if all(dep in done_ids for dep in task.get("depends_on", [])):
                return task
    return None


def block_dependents(tasks: list[dict], failed_id: str) -> None:
    """Recursively mark all tasks that depend (directly or indirectly) on failed_id as blocked."""
    changed = True
    blocked: set[str] = {failed_id}
    while changed:
        changed = False
        for task in tasks:
            if task["status"] == "pending" and any(d in blocked for d in task.get("depends_on", [])):
                task["status"] = "blocked"
                blocked.add(task["id"])
                changed = True


# ── Display ───────────────────────────────────────────────────────────────────

STATUS_ICON = {
    "pending": "⏳",
    "running": "🔄",
    "done":    "✅",
    "failed":  "❌",
    "blocked": "🚫",
}


def print_status(data: dict) -> None:
    tasks = data["tasks"]
    total = len(tasks)
    done_count  = sum(1 for t in tasks if t["status"] == "done")
    print(f"\n{'─'*60}")
    print(f"QUEUE: {data.get('queue_id', '?')}  |  HUB: {data.get('hub', '?')}")
    print(f"Progress: {done_count}/{total} done")
    print(f"{'─'*60}")
    for task in tasks:
        icon = STATUS_ICON.get(task["status"], "?")
        err = f"  ← {task['error']}" if task.get("error") else ""
        print(f"  {icon} [{task['id']}] {task['agent']} — {task['description']}{err}")
    print(f"{'─'*60}\n")


def print_task_prompt(task: dict) -> None:
    idx    = task["id"]
    agent  = task["agent"]
    desc   = task["description"]
    inputs = task.get("input_files") or []
    output = task.get("output_file", "")

    print(f"\n{'═'*60}")
    print(f"NEXT TASK [{idx}]: {agent}")
    print(f"Description: {desc}")
    if inputs:
        print(f"Input files:")
        for f in inputs:
            exists = "✓" if resolve_path(f).exists() else "✗ NOT FOUND"
            print(f"  {exists}  {f}")
    print(f"Output file: {output}")
    print(f"{'─'*60}")
    print(f"Run agent '{agent}' now. When done, confirm:")
    print(f"  python organic-runner.py --done")
    print(f"  python organic-runner.py --failed \"reason\"")
    print(f"{'═'*60}\n")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_next(data: dict, queue_path: Path) -> None:
    tasks = data["tasks"]

    running = find_running(tasks)
    if running:
        print(f"[INFO] Task '{running['id']}' is already running: {running['description']}")
        print("       Use --done or --failed to close it before starting the next task.")
        return

    task = find_next_pending(tasks)
    if not task:
        all_done = all(t["status"] in ("done", "blocked") for t in tasks)
        if all_done:
            print_status(data)
            print("[DONE] All tasks completed.")
        else:
            print("[BLOCKED] No eligible pending tasks. Check for failures or blocked tasks.")
            print_status(data)
        return

    task["status"]     = "running"
    task["started_at"] = now_iso()
    save_queue(queue_path, data)
    print_task_prompt(task)


def cmd_done(data: dict, queue_path: Path) -> None:
    tasks   = data["tasks"]
    running = find_running(tasks)
    if not running:
        print("[ERROR] No task is currently running.")
        sys.exit(1)

    output_file = running.get("output_file", "")
    if output_file and not resolve_path(output_file).exists():
        print(f"[WARNING] output_file not found on disk: {output_file}")
        print("          Marking done anyway — verify manually that output was saved.")

    running["status"]       = "done"
    running["completed_at"] = now_iso()
    running["error"]        = None
    save_queue(queue_path, data)
    print(f"[DONE] Task '{running['id']}' marked as done: {running['description']}")

    if data.get("stop_after_each", True):
        print("\n[PAUSED] stop_after_each is enabled.")
        print("         Run `python organic-runner.py` to continue to the next task.")
    else:
        print("\n[AUTO] Continuing to next task...")
        cmd_next(data, queue_path)


def cmd_failed(data: dict, queue_path: Path, reason: str) -> None:
    tasks   = data["tasks"]
    running = find_running(tasks)
    if not running:
        print("[ERROR] No task is currently running.")
        sys.exit(1)

    running["status"]       = "failed"
    running["completed_at"] = now_iso()
    running["error"]        = reason

    if data.get("stop_on_failure", True):
        block_dependents(tasks, running["id"])
        save_queue(queue_path, data)
        print(f"[FAILED] Task '{running['id']}': {reason}")
        print("[BLOCKED] Dependent tasks have been blocked.")
        print_status(data)
        print("[STOPPED] stop_on_failure is enabled. Fix the issue, then reset the task manually.")
    else:
        save_queue(queue_path, data)
        print(f"[FAILED] Task '{running['id']}': {reason}")
        print("[INFO] stop_on_failure is disabled. Continuing to next eligible task.")
        cmd_next(data, queue_path)


# ── Entry Point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="BabyMania Organic Queue Controller")
    parser.add_argument("--queue",  default=str(DEFAULT_QUEUE), help="Path to queue JSON file")
    parser.add_argument("--done",   action="store_true",        help="Mark running task as done")
    parser.add_argument("--failed", metavar="REASON",           help="Mark running task as failed")
    parser.add_argument("--status", action="store_true",        help="Print full queue status")
    args = parser.parse_args()

    queue_path = Path(args.queue)
    data       = load_queue(queue_path)

    if args.status:
        print_status(data)
    elif args.done:
        cmd_done(data, queue_path)
    elif args.failed:
        cmd_failed(data, queue_path, args.failed)
    else:
        cmd_next(data, queue_path)


if __name__ == "__main__":
    # Windows: force UTF-8 output to avoid cp1255 encoding errors
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
