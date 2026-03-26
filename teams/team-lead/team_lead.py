"""
BabyMania — Team Lead MVP
Decision loop: task packet in → worker run → analyze output → verdict

Usage:
    python teams/team-lead/team_lead.py --task bridge/next-task.md
    python teams/team-lead/team_lead.py --task bridge/next-task.md --dry-run
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

REPO          = r"C:\Projects\baby-mania-agent"
CLAUDE        = r"C:\Users\3024e\AppData\Roaming\npm\claude.cmd"
STATE_FILE    = r"C:\Projects\baby-mania-agent\bridge\runtime-state.md"
RESULT_FILE   = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
CLAUDE_TIMEOUT = 600   # 10 min max per worker run
MAX_RETRIES    = 2

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Verdict constants ──────────────────────────────────────────────────────────

PASS            = "PASS"
RETRY           = "RETRY"
BLOCKED         = "BLOCKED"
FAILED_EMPTY    = "FAILED_EMPTY"
FAILED_RATE_LIMIT = "FAILED_RATE_LIMIT"
FALSE_SUCCESS   = "FALSE_SUCCESS"
PARTIAL         = "PARTIAL"


# ── Runtime state ──────────────────────────────────────────────────────────────

class RuntimeState:
    def __init__(self, task_id: str, task_preview: str):
        self.task_id       = task_id
        self.task_preview  = task_preview
        self.stage         = "STARTING"
        self.current_worker = ""
        self.round         = 0
        self.completed_steps: list[str] = []
        self.failed_steps:    list[str] = []
        self.blocked_reason = ""
        self.waiting_for    = ""
        self.next_action    = ""
        self.final_verdict  = ""

    def write(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"task_id:        {self.task_id}",
            f"time:           {ts}",
            f"stage:          {self.stage}",
            f"current_worker: {self.current_worker}",
            f"round:          {self.round} / {MAX_RETRIES}",
            f"completed:      {', '.join(self.completed_steps) or '—'}",
            f"failed:         {', '.join(self.failed_steps) or '—'}",
            f"blocked_reason: {self.blocked_reason or '—'}",
            f"waiting_for:    {self.waiting_for or '—'}",
            f"next_action:    {self.next_action or '—'}",
            f"final_verdict:  {self.final_verdict or '—'}",
            f"task_preview:   {self.task_preview[:120]}",
        ]
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def log(self, msg: str):
        print(f"[TL {self.task_id}] {msg}")


# ── Output analysis ────────────────────────────────────────────────────────────

def analyze_output(output: str, task_text: str, round_num: int) -> str:
    """
    Analyze Claude worker output and return a verdict constant.
    Order matters: check failure modes first, then success.
    """

    # 1. Empty output
    if not output.strip():
        return FAILED_EMPTY

    # 2. Rate limit hit
    rate_limit_signals = [
        "you've hit your limit",
        "hit your limit",
        "rate limit",
        "resets at",
        "resets 5pm",
    ]
    lower = output.lower()
    if any(sig in lower for sig in rate_limit_signals):
        return FAILED_RATE_LIMIT

    # 3. Explicit failure
    if "status: fail" in lower or "status: failed" in lower:
        if round_num >= MAX_RETRIES:
            return BLOCKED
        return RETRY

    # 4. False success — claims PASS but no meaningful content
    has_evidence = any(kw in lower for kw in (
        "files_updated", "changes_made", "updated:", "created:", "fixed", "wrote"
    ))
    false_success_signals = [
        "status: pass" in lower and len(output.strip()) < 120 and not has_evidence,
        output.strip().lower() in ("done", "ok", "pass") and len(output.strip()) < 10,
        output.strip().endswith("?"),           # ended with a question
    ]
    if any(false_success_signals):
        return FALSE_SUCCESS

    # 5. Partial completion
    partial_signals = [
        "status: partial" in lower,
        "partially complete" in lower,
        "not all steps" in lower,
        "remaining:" in lower,
    ]
    if any(partial_signals):
        if round_num >= MAX_RETRIES:
            return BLOCKED
        return PARTIAL

    # 6. Repeated failure
    if round_num >= MAX_RETRIES and (
        "fail" in lower or "error" in lower or "blocked" in lower
    ):
        return BLOCKED

    # 7. Explicit pass
    if "status: pass" in lower:
        return PASS

    # 8. Implicit pass — has substantial output, no failure signals
    if len(output.strip()) > 200:
        return PASS

    # 9. Unclear — treat as partial, retry if rounds remain
    if round_num < MAX_RETRIES:
        return PARTIAL
    return BLOCKED


# ── Worker execution ───────────────────────────────────────────────────────────

def run_worker(task_text: str, state: RuntimeState, dry_run: bool = False) -> str:
    """Run Claude Code worker with the given task. Returns raw output string."""
    state.current_worker = "claude-code"
    state.stage = "RUNNING"
    state.write()
    state.log(f"Running worker (round {state.round})...")

    if dry_run:
        state.log("[DRY RUN] skipping actual Claude call")
        return f"STATUS: PASS\nDRY RUN — task would have been sent to Claude Code.\nTask preview: {task_text[:200]}"

    try:
        result = subprocess.run(
            [CLAUDE, "--print", "--dangerously-skip-permissions", task_text],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=CLAUDE_TIMEOUT,
        )
        return (result.stdout or result.stderr or "").strip()

    except subprocess.TimeoutExpired:
        state.log(f"Worker timeout after {CLAUDE_TIMEOUT}s")
        return f"TIMEOUT: Claude Code did not respond within {CLAUDE_TIMEOUT}s"

    except FileNotFoundError:
        state.log(f"Claude executable not found: {CLAUDE}")
        return f"ERROR: Claude executable not found at {CLAUDE}"


# ── Decision loop ──────────────────────────────────────────────────────────────

def run(task_text: str, dry_run: bool = False) -> str:
    """
    Main Team Lead decision loop.
    Returns final verdict string.
    """
    task_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    task_preview = task_text.strip().splitlines()[0][:120]
    state = RuntimeState(task_id, task_preview)
    state.log(f"Starting — task_id={task_id}")
    state.write()

    last_output = ""

    for round_num in range(1, MAX_RETRIES + 1):
        state.round = round_num

        # Run worker
        output = run_worker(task_text, state, dry_run=dry_run)
        last_output = output

        # Write result immediately
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            f.write(f"task_id: {task_id}\nround: {round_num}\n---\n{output}\n")

        # Analyze
        state.stage = "ANALYZING"
        state.write()
        verdict = analyze_output(output, task_text, round_num)
        state.log(f"Round {round_num} verdict: {verdict}")

        # ── Terminal verdicts ──────────────────────────────────────────────
        if verdict == PASS:
            state.completed_steps.append(f"round-{round_num}")
            state.final_verdict = PASS
            state.stage = "DONE"
            state.next_action = "done"
            state.write()
            state.log("DONE ✅")
            return PASS

        if verdict == FAILED_EMPTY:
            state.failed_steps.append(f"round-{round_num}:empty")
            state.final_verdict = FAILED_EMPTY
            state.stage = "FAILED"
            state.blocked_reason = "Worker returned empty output"
            state.next_action = "escalate"
            state.write()
            state.log("FAILED — empty output ❌")
            return FAILED_EMPTY

        if verdict == FAILED_RATE_LIMIT:
            state.failed_steps.append(f"round-{round_num}:rate_limit")
            state.final_verdict = FAILED_RATE_LIMIT
            state.stage = "BLOCKED"
            state.blocked_reason = "Claude rate limit hit — wait and retry manually"
            state.next_action = "wait"
            state.write()
            state.log("BLOCKED — rate limit ⏳")
            return FAILED_RATE_LIMIT

        if verdict == BLOCKED:
            state.failed_steps.append(f"round-{round_num}:blocked")
            state.final_verdict = BLOCKED
            state.stage = "BLOCKED"
            state.blocked_reason = f"Worker failed after {round_num} rounds"
            state.next_action = "escalate_telegram"
            state.write()
            state.log("BLOCKED — escalate to Telegram 🔴")
            return BLOCKED

        if verdict == FALSE_SUCCESS:
            state.failed_steps.append(f"round-{round_num}:false_success")
            state.log(f"FALSE_SUCCESS detected — retrying with explicit instruction")
            # Augment task for next round
            task_text = (
                task_text
                + "\n\n[TEAM LEAD NOTE] Previous output was too short or ambiguous to confirm success. "
                "Please provide explicit STATUS: PASS with FILES_UPDATED and CHANGES_MADE sections."
            )

        if verdict in (RETRY, PARTIAL):
            state.failed_steps.append(f"round-{round_num}:{verdict.lower()}")
            state.log(f"{verdict} — {'retrying' if round_num < MAX_RETRIES else 'max rounds reached'}")
            if round_num >= MAX_RETRIES:
                state.final_verdict = BLOCKED
                state.stage = "BLOCKED"
                state.blocked_reason = f"Max retries reached with verdict {verdict}"
                state.next_action = "escalate_telegram"
                state.write()
                return BLOCKED

    # Should not reach here
    state.final_verdict = BLOCKED
    state.stage = "BLOCKED"
    state.write()
    return BLOCKED


# ── CLI entry point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BabyMania Team Lead MVP")
    parser.add_argument("--task", required=True, help="Path to task file (e.g. bridge/next-task.md)")
    parser.add_argument("--dry-run", action="store_true", help="Skip actual Claude call")
    args = parser.parse_args()

    task_path = Path(args.task)
    if not task_path.is_absolute():
        task_path = Path(REPO) / task_path

    if not task_path.exists():
        print(f"ERROR: task file not found: {task_path}")
        sys.exit(1)

    task_text = task_path.read_text(encoding="utf-8").strip()
    if not task_text:
        print("ERROR: task file is empty")
        sys.exit(1)

    print(f"Team Lead MVP — task: {task_path.name}")
    print("=" * 50)

    verdict = run(task_text, dry_run=args.dry_run)

    # Structured stdout summary — consumed by github-bridge.py
    print("=" * 50)
    print(f"STATUS: {'PASS' if verdict == PASS else 'FAILED'}")
    print(f"VERDICT: {verdict}")
    try:
        state_lines = Path(STATE_FILE).read_text(encoding="utf-8").splitlines()
        tid   = next((l for l in state_lines if l.startswith("task_id:")), "")
        stage = next((l for l in state_lines if l.startswith("stage:")),   "")
        print(f"SUMMARY: {tid} | {stage}")
    except Exception:
        print(f"SUMMARY: verdict={verdict}")

    sys.exit(0 if verdict == PASS else 1)


if __name__ == "__main__":
    main()
