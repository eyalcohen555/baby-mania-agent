import time
import os
import subprocess
import atexit
import ctypes
from datetime import datetime

TASK_FILE   = r"C:\Projects\baby-mania-agent\bridge\next-task.md"
RESULT_FILE = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
STATUS_FILE = r"C:\Projects\baby-mania-agent\bridge\status.md"
LOCK_FILE     = r"C:\Projects\baby-mania-agent\bridge\bridge.lock"
RESPONSE_FILE = r"C:\Projects\baby-mania-agent\bridge\telegram-response.md"
TASK_LOG_FILE = r"C:\Projects\baby-mania-agent\bridge\task-log.md"
CLAUDE        = r"C:\Users\3024e\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
CLAUDE_TIMEOUT = 600   # 10 minutes max for a single Claude run


def generate_task_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def parse_approval_tier(task_text: str) -> str:
    for line in task_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("APPROVAL_TIER:"):
            value = stripped.split(":", 1)[1].strip().upper()
            if value in ("T0", "T1", "T2", "T3"):
                return value
    return "UNKNOWN"


def needs_response(output: str):
    """
    Determine if Claude output requires Telegram interaction before finishing.
    Returns 'APPROVAL_NEEDED' | 'QUESTION' | None.
    STAGE_VERDICT: PASS short-circuits to None immediately.
    Keyword scan fires ONLY when no STAGE_VERDICT line is found.
    """
    has_verdict_line  = False
    awaiting_approval = False
    verdict_question  = False
    response_needed   = False
    response_type     = ""

    for line in output.splitlines():
        cl = line.strip().strip("*_`#").strip().upper()

        if cl.startswith("STAGE_VERDICT:"):
            has_verdict_line = True
            val = cl.split(":", 1)[1].strip()
            if val.startswith("PASS"):
                return None
            if val.startswith("AWAITING_APPROVAL"):
                awaiting_approval = True
            if val.startswith("QUESTION"):
                verdict_question = True

        elif cl.startswith("STATUS:"):
            val = cl.split(":", 1)[1].strip()
            if val.startswith("PASS"):
                return None
            if val.startswith("AWAITING_APPROVAL"):
                awaiting_approval = True

        elif cl.startswith("RESPONSE_NEEDED:") and "YES" in cl:
            response_needed = True

        elif cl.startswith("RESPONSE_TYPE:"):
            response_type = cl.split(":", 1)[1].strip()

    if awaiting_approval:
        return "APPROVAL_NEEDED"
    if verdict_question:
        return "QUESTION"

    if response_needed:
        if "APPROVAL" in response_type:
            return "APPROVAL_NEEDED"
        if "QUESTION" in response_type:
            return "QUESTION"
        return "APPROVAL_NEEDED"

    if not has_verdict_line:
        lower = output.lower()
        approval_kws = [
            "approval needed", "requires approval", "waiting for approval",
            "נדרש אישור", "אישור אייל", "אישור נדרש",
        ]
        if any(kw in lower for kw in approval_kws):
            return "APPROVAL_NEEDED"
        question_kws = ["question for user", "שאלה לאייל:", "שאלה:"]
        if any(kw in lower for kw in question_kws):
            return "QUESTION"

    return None


# ── Status ─────────────────────────────────────────────────────────────────────

# Current task context — set per-task, cleared when done
_current_task_id = ""
_current_tier = ""


def write_status(state: str, detail: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(f"status: {state}\ntime: {ts}\n")
        if _current_task_id:
            f.write(f"task_id: {_current_task_id}\n")
        if _current_tier:
            f.write(f"approval_tier: {_current_tier}\n")
        f.write(f"detail: {detail}\n")


def log_task(task_text, action):
    """Append entry to bridge/task-log.md."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview = task_text.strip().splitlines()[0][:100] if task_text.strip() else "(empty)"
    entry = f"| {ts} | {action} | {preview} |\n"
    try:
        if not os.path.exists(TASK_LOG_FILE):
            with open(TASK_LOG_FILE, "w", encoding="utf-8") as f:
                f.write("| time | action | task |\n|------|--------|------|\n" + entry)
        else:
            with open(TASK_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
    except Exception as e:
        print(f"[task-log] write error: {e}")


def _parse_response_file():
    """
    Read and parse bridge/telegram-response.md WITHOUT clearing it.
    Returns dict or None (same logic as consume_telegram_response).
    """
    if not os.path.exists(RESPONSE_FILE):
        return None
    try:
        with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
    except OSError:
        return None

    if not raw:
        return None

    parsed = {"time": "", "type": "", "action": "", "content": ""}
    for line in raw.splitlines():
        for key in parsed:
            if line.startswith(f"{key}:"):
                parsed[key] = line[len(key) + 1:].strip()
                break

    if not parsed["action"]:   # mandatory — if missing, file is corrupt/partial
        return None

    return parsed


def consume_telegram_response():
    """
    Read bridge/telegram-response.md, parse its fields, clear the file,
    and return a dict: {time, type, action, content}.
    Returns None if the file is missing, empty, or missing 'action' field.

    Written by telegram_bot.py in the format:
      time:    YYYY-MM-DD HH:MM:SS
      type:    APPROVAL | QUESTION | BLOCKED
      action:  approve | reject | answer | skip | retry | stop
      content: free text (only for action=answer)

    NOTE: Only call this when NOT waiting for a Claude re-run.
          Use _parse_response_file() to peek without clearing.
    """
    parsed = _parse_response_file()
    if parsed is None:
        return None

    # Clear the file after successful parse
    try:
        with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
            f.write("")
    except OSError as e:
        print(f"[BRIDGE] אזהרה: לא ניתן לנקות את קובץ התגובה: {e}")

    return parsed


# ── Singleton lock ──────────────────────────────────────────────────────────────

def is_pid_alive(pid: int) -> bool:
    """Check if a Windows process is alive by PID (no external deps)."""
    PROCESS_QUERY_INFORMATION = 0x0400
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
    if handle == 0:
        return False
    ctypes.windll.kernel32.CloseHandle(handle)
    return True


def is_bridge_process(pid: int) -> bool:
    """Check if a PID is actually running bridge.py (not just any python)."""
    try:
        result = subprocess.run(
            ["wmic", "process", "where", f"ProcessId={pid}",
             "get", "CommandLine", "/FORMAT:CSV"],
            capture_output=True, text=True, timeout=5
        )
        return "bridge.py" in result.stdout
    except Exception:
        return True  # assume it's bridge if we can't check


def acquire_lock() -> bool:
    """Try to acquire singleton lock.
    Returns True if acquired.
    Returns False if another live bridge.py instance holds the lock.
    Clears stale lock if previous instance crashed or is not bridge.py.
    """
    my_pid = os.getpid()

    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                existing_pid = int(f.read().strip())
        except (ValueError, OSError):
            existing_pid = None

        if existing_pid and is_pid_alive(existing_pid) and is_bridge_process(existing_pid):
            write_status("locked", f"instance already running — PID {existing_pid}")
            print(f"[BRIDGE] already running (PID {existing_pid}). exiting.")
            return False

        # Stale lock or PID reused by non-bridge process
        print(f"[BRIDGE] stale lock (PID {existing_pid}) — cleaning up.")
        write_status("failed", f"cleared stale lock from PID {existing_pid}")
        os.remove(LOCK_FILE)

    with open(LOCK_FILE, "w") as f:
        f.write(str(my_pid))
    return True


def release_lock():
    """Release lock file. Safe to call multiple times."""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except OSError:
        pass


# Register cleanup on any normal exit (Ctrl+C, sys.exit, etc.)
atexit.register(release_lock)


def kill_old_bridge_processes():
    """Kill any old bridge.py python processes (except self).
    Prevents zombie accumulation across restarts.
    """
    my_pid = os.getpid()
    try:
        result = subprocess.run(
            ["wmic", "process", "where",
             "Name='python.exe' AND CommandLine LIKE '%bridge.py%'",
             "get", "ProcessId", "/FORMAT:CSV"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().splitlines():
            parts = line.strip().split(",")
            if len(parts) >= 2:
                try:
                    pid = int(parts[-1])
                except ValueError:
                    continue
                if pid != my_pid and pid != os.getppid():
                    print(f"[BRIDGE] killing old bridge process PID {pid}")
                    try:
                        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                       capture_output=True, timeout=5)
                    except Exception:
                        pass
    except Exception as e:
        print(f"[BRIDGE] zombie cleanup skipped: {e}")


# ── Entry point ────────────────────────────────────────────────────────────────

kill_old_bridge_processes()

if not acquire_lock():
    exit(1)

print(f"[BRIDGE] active (PID {os.getpid()}) — polling bridge/next-task.md")
print("=" * 50)
write_status("idle", f"PID {os.getpid()}")

last_content = ""
_waiting_for_response = False   # True when Claude output a QUESTION/APPROVAL

try:
    while True:
        try:
            # ── Task execution (skip if waiting for Telegram response) ───────
            if os.path.exists(TASK_FILE) and not _waiting_for_response:
                with open(TASK_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if content and content != last_content:
                    last_content = content

                    # Set task context
                    _current_task_id = generate_task_id()
                    _current_tier = parse_approval_tier(content)
                    print(f"\n[BRIDGE] new task! id={_current_task_id} tier={_current_tier}")
                    log_task(content, f"STARTED [{_current_task_id}] [TIER:{_current_tier}]")

                    # T3 enforcement — block unless pre-approved via Telegram
                    if _current_tier == "T3":
                        _t3_resp = _parse_response_file()
                        _t3_approved = (
                            _t3_resp is not None
                            and _t3_resp.get("type") == "APPROVAL"
                            and _t3_resp.get("action") == "approved"
                        )
                        if _t3_approved:
                            consume_telegram_response()
                            print("[BRIDGE] T3 — pre-approval found. proceeding with execution.")
                            log_task(content, f"T3_APPROVED [{_current_task_id}]")
                            # Inject approval into task so Claude knows not to block
                            content += "\n\nAPPROVAL_GRANTED: YES — T3 approved via telegram-response.md. Execute immediately without stopping for approval."
                            # Fall through to normal execution below
                        else:
                            print("[BRIDGE] T3 — requires Eyal approval. blocking.")
                            log_task(content, f"BLOCKED_T3 [{_current_task_id}]")
                            with open(RESULT_FILE, "w", encoding="utf-8") as f:
                                f.write(
                                    f"task_id: {_current_task_id}\n"
                                    f"approval_tier: T3\n---\n"
                                    f"STAGE_VERDICT: AWAITING_APPROVAL\n"
                                    f"STATUS: AWAITING_APPROVAL\n"
                                    f"REASON: T3 — requires Eyal approval\n"
                                    f"TASK_PREVIEW: {content[:200]}\n"
                                )
                            write_status("awaiting_approval", "T3 — waiting for Eyal")
                            _waiting_for_response = True  # prevents else-branch from consuming approval file
                            _current_task_id = ""
                            _current_tier = ""
                            continue

                    write_status("running", content[:80])

                    try:
                        result = subprocess.run(
                            [CLAUDE, "--print", "--dangerously-skip-permissions", content],
                            cwd=r"C:\Projects\baby-mania-agent",
                            capture_output=True,
                            timeout=CLAUDE_TIMEOUT
                        )
                        # Binary mode: text=True+encoding crashes on Windows cp1255 with Hebrew.
                        raw = result.stdout or result.stderr or b""
                        output = raw.decode("utf-8", errors="replace").strip()
                    except subprocess.TimeoutExpired:
                        output = f"ERROR: Claude Code timed out after {CLAUDE_TIMEOUT}s"
                        print(f"[BRIDGE] TIMEOUT after {CLAUDE_TIMEOUT}s")
                        log_task(content, f"TIMEOUT [{_current_task_id}]")

                    # Empty output — treat as FAILED, not silent success
                    if not output:
                        print(f"[BRIDGE] empty output — exit code: {result.returncode}")
                        with open(RESULT_FILE, "w", encoding="utf-8") as f:
                            f.write(
                                f"task_id: {_current_task_id}\n"
                                f"approval_tier: {_current_tier}\n"
                                f"---\n"
                                f"STATUS: FAILED\n"
                                f"REASON: Claude returned empty stdout and empty stderr\n"
                                f"EXIT_CODE: {result.returncode}\n"
                            )
                        log_task(content, f"FAILED_EMPTY [{_current_task_id}]")
                        with open(TASK_FILE, "w", encoding="utf-8") as f:
                            f.write("")
                        last_content = ""
                        write_status("failed", f"empty output [{_current_task_id}]")
                        _current_task_id = ""
                        _current_tier = ""
                        write_status("idle", f"PID {os.getpid()}")
                        print("=" * 50)
                        continue

                    # Write result with task_id header
                    with open(RESULT_FILE, "w", encoding="utf-8") as f:
                        f.write(f"task_id: {_current_task_id}\n---\n{output}")

                    # Bridge Room TOKEN_SAFE_STOP detection (brm- tasks only)
                    _is_brm = "ROOM_ID:" in content
                    if _is_brm and "TOKEN_SAFE_STOP_START" in output:
                        print(f"[BRIDGE] TOKEN_SAFE_STOP detected [{_current_task_id}]")
                        log_task(content, f"TOKEN_SAFE_STOP [{_current_task_id}]")
                        with open(TASK_FILE, "w", encoding="utf-8") as f:
                            f.write("")
                        last_content = ""
                        write_status("token_safe_stop", f"TOKEN_SAFE_STOP [{_current_task_id}]")
                        print("=" * 50)
                        _current_task_id = ""
                        _current_tier = ""
                        write_status("idle", f"PID {os.getpid()}")
                        continue

                    # Check if Claude needs a Telegram response before finishing
                    event = needs_response(output)
                    if event:
                        # Do NOT clear the task — keep it for re-run after response
                        _waiting_for_response = True
                        write_status("waiting_response",
                                     f"Waiting for Telegram {event} — task kept for re-run")
                        print(f"[BRIDGE] Claude asked ({event}) — waiting for Telegram...")
                    else:
                        with open(TASK_FILE, "w", encoding="utf-8") as f:
                            f.write("")
                        last_content = ""
                        consume_telegram_response()
                        log_task(content, f"DONE [{_current_task_id}] [TIER:{_current_tier}]")
                        write_status("done", "result written")
                        print("[BRIDGE] done! result in bridge/last-result.md")

                        # Git commit/push — ensure local results are tracked
                        try:
                            _repo = r"C:\Projects\baby-mania-agent"
                            subprocess.run(["git", "add", "bridge/"], cwd=_repo,
                                           capture_output=True, timeout=15)
                            _commit = subprocess.run(
                                ["git", "commit", "-m",
                                 f"bridge: task result [{_current_task_id}]"],
                                cwd=_repo, capture_output=True, text=True, timeout=15)
                            if _commit.returncode == 0:
                                _push = subprocess.run(
                                    ["git", "push"], cwd=_repo,
                                    capture_output=True, text=True, timeout=30)
                                if _push.returncode == 0:
                                    print("[BRIDGE] git push OK")
                                else:
                                    print(f"[BRIDGE] git push failed: {_push.stderr.strip()[:80]}")
                            else:
                                print("[BRIDGE] nothing to commit (already committed)")
                        except Exception as e:
                            print(f"[BRIDGE] git error (non-fatal): {e}")

                        print("=" * 50)
                        # Clear task context before idle
                        _current_task_id = ""
                        _current_tier = ""
                        write_status("idle", f"PID {os.getpid()}")

            # ── Telegram response handling ───────────────────────────────────
            if _waiting_for_response:
                # Peek without clearing — Claude must read the file itself
                response = _parse_response_file()
                if response:
                    action   = response.get("action", "")
                    rtype    = response.get("type", "")
                    print(f"[BRIDGE] תגובת טלגרם זוהתה — type={rtype!r} action={action!r}")
                    # Unblock — force re-run on next cycle
                    # telegram-response.md is kept so Claude can read it
                    _waiting_for_response = False
                    last_content = ""
                    write_status("running", f"re-run after {rtype} {action}")
                    print("[BRIDGE] מריץ שוב את המשימה — קלוד יקרא את התשובה בעצמו...")
            else:
                # Normal consumption — clear after reading
                response = consume_telegram_response()
                if response:
                    action   = response.get("action", "")
                    rtype    = response.get("type", "")
                    rcontent = response.get("content", "")
                    print(f"[BRIDGE] תגובת טלגרם נצרכה — type={rtype!r} action={action!r}" +
                          (f" content={rcontent[:60]!r}" if rcontent else ""))
                    write_status("idle", f"PID {os.getpid()} — response consumed: {action}")

        except Exception as e:
            write_status("failed", str(e))
            print(f"[BRIDGE] error: {e}")
            # Clear task context so status doesn't show stale task_id
            _current_task_id = ""
            _current_tier = ""
            time.sleep(4)
            write_status("idle", f"PID {os.getpid()} — recovered from error")

        time.sleep(4)

finally:
    _current_task_id = ""
    _current_tier = ""
    release_lock()
    write_status("idle", "bridge stopped")
    print("[BRIDGE] stopped — lock released.")
