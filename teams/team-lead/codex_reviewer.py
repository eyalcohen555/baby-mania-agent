"""
codex_reviewer.py — Codex Decision Loop
Location: teams/team-lead/codex_reviewer.py

Invoked by conductor.py after each stage completion.
Reads stage output + plan context, calls Claude as Codex reviewer,
returns a structured decision that conductor uses for routing.

Decisions:
  CONTINUE   — output meets exit conditions, proceed as planned
  RETRY      — output incomplete/incorrect, retry same stage (once)
  FIX        — specific fixable problem; conductor runs a synthetic fix task
  STOP       — critical issue or data risk; halt plan immediately
  ASK_AYAL   — ambiguous/high-stakes; escalate to human
  NEXT_STAGE — skip normal routing, jump to a specific stage
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

# Same claude.exe path as bridge.py uses
CLAUDE = (
    r"C:\Users\3024e\AppData\Roaming\npm"
    r"\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
)

CODEX_DECISION_FILE = Path(r"C:\Projects\baby-mania-agent\bridge\codex-decision.md")

VALID_DECISIONS = {"CONTINUE", "RETRY", "FIX", "STOP", "ASK_AYAL", "NEXT_STAGE"}

CODEX_TIMEOUT = 120  # seconds


# ── Prompt Builder ────────────────────────────────────────────────────────────

def _build_prompt(plan: dict, stage: dict, output: str) -> str:
    exit_conds = "\n".join(
        f"  - {c}" for c in (stage.get("exit_conditions") or [])
    )
    fail_conds = "\n".join(
        f"  - {c}" for c in (stage.get("fail_conditions") or [])
    )
    return (
        f"CODEX REVIEW REQUEST\n"
        f"Plan:  {plan['plan_id']} — {plan.get('plan_name', '')}\n"
        f"Stage: {stage['id']} — {stage.get('name', '')}\n"
        f"Type:  {stage.get('type', '')}\n"
        f"Tier:  {stage.get('approval_tier', '')}\n"
        f"\n"
        f"Goal:\n{stage.get('goal', '').strip()}\n"
        f"\n"
        f"Exit conditions (all must be met for PASS):\n{exit_conds}\n"
        f"\n"
        f"Fail conditions (any one = FAIL):\n{fail_conds}\n"
        f"\n"
        f"--- CLAUDE CODE OUTPUT ---\n"
        f"{output.strip()}\n"
        f"--- END OUTPUT ---\n"
        f"\n"
        f"You are Codex, the safety and quality reviewer for BabyMania automation.\n"
        f"Review whether the Claude Code output satisfies the stage requirements above.\n"
        f"\n"
        f"Decision rules:\n"
        f"  CONTINUE   — output meets all exit conditions → proceed to next stage\n"
        f"  RETRY      — output is incomplete or slightly wrong → retry same stage once\n"
        f"  FIX        — specific fixable problem → provide exact fix in CODEX_ACTION\n"
        f"  STOP       — critical issue, data risk, or irreversible mistake → halt plan\n"
        f"  ASK_AYAL   — ambiguous or high-stakes decision → escalate to human\n"
        f"  NEXT_STAGE — output is fine but normal routing should be overridden;\n"
        f"               set CODEX_ACTION to: Jump to STAGE-N\n"
        f"\n"
        f"Respond with EXACTLY these four lines (no preamble):\n"
        f"CODEX_DECISION: CONTINUE | RETRY | FIX | STOP | ASK_AYAL | NEXT_STAGE\n"
        f"CODEX_REASON: <one sentence — why this decision>\n"
        f"CODEX_ACTION: <what to do next — specific and actionable>\n"
        f"CODEX_RISK: LOW | MEDIUM | HIGH\n"
    )


# ── Output Parser ─────────────────────────────────────────────────────────────

def _parse_output(text: str) -> dict:
    result: dict = {}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("CODEX_DECISION:"):
            result["decision"] = line.split(":", 1)[1].strip().upper()
        elif line.startswith("CODEX_REASON:"):
            result["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("CODEX_ACTION:"):
            result["action"] = line.split(":", 1)[1].strip()
        elif line.startswith("CODEX_RISK:"):
            result["risk"] = line.split(":", 1)[1].strip().upper()

    if result.get("decision") not in VALID_DECISIONS:
        result["decision"] = "STOP"
        result.setdefault("reason", "Codex returned invalid or missing decision")

    result.setdefault("reason", "No reason provided")
    result.setdefault("action", "Manual review required")
    result.setdefault("risk", "HIGH")
    return result


# ── Public Interface ──────────────────────────────────────────────────────────

def run(plan: dict, stage: dict, output: str) -> dict:
    """
    Invoke Codex review for a completed stage.
    Returns dict with keys: decision, reason, action, risk.
    On any failure, returns STOP with HIGH risk.
    """
    prompt = _build_prompt(plan, stage, output)
    try:
        proc = subprocess.run(
            [CLAUDE, "--print", "--dangerously-skip-permissions"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=CODEX_TIMEOUT,
        )
        raw = proc.stdout.decode("utf-8", errors="replace")
        return _parse_output(raw)
    except subprocess.TimeoutExpired:
        return {
            "decision": "STOP",
            "reason":   "Codex review timed out",
            "action":   "Manual review required — Codex did not respond in time",
            "risk":     "HIGH",
        }
    except Exception as exc:
        return {
            "decision": "STOP",
            "reason":   f"Codex reviewer error: {exc}",
            "action":   "Manual review required",
            "risk":     "HIGH",
        }


def write_decision(result: dict, plan_id: str, stage_id: str) -> None:
    """Write last Codex decision to bridge/codex-decision.md for visibility."""
    content = (
        f"EVENT: CODEX_REVIEW\n"
        f"plan_id: {plan_id}\n"
        f"stage_id: {stage_id}\n"
        f"decision: {result['decision']}\n"
        f"reason: {result['reason']}\n"
        f"action: {result['action']}\n"
        f"risk: {result['risk']}\n"
        f"time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    try:
        CODEX_DECISION_FILE.write_text(content, encoding="utf-8")
    except Exception:
        pass


def parse_next_stage(action: str) -> str | None:
    """Extract STAGE-N from a NEXT_STAGE action string. Returns None if not found."""
    m = re.search(r"STAGE-\d+", action, re.IGNORECASE)
    return m.group(0).upper() if m else None
