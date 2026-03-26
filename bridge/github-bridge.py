import subprocess
import os
import sys
import time
from datetime import datetime

# Force UTF-8 output on Windows to avoid cp1255 emoji errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = r"C:\Projects\baby-mania-agent"
TASK_FILE = r"C:\Projects\baby-mania-agent\bridge\next-task.md"
RESULT_FILE = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
STATUS_FILE = r"C:\Projects\baby-mania-agent\bridge\status.md"
RESPONSE_FILE = r"C:\Projects\baby-mania-agent\bridge\telegram-response.md"
TASK_LOG_FILE = r"C:\Projects\baby-mania-agent\bridge\task-log.md"
CLAUDE = r"C:\Users\3024e\AppData\Roaming\npm\claude.cmd"

RESPONSE_TIMEOUT = 300   # 5 minutes max wait for Telegram response
RESPONSE_POLL    = 5     # poll every 5 seconds
MAX_ROUNDS       = 5     # safety cap — max Claude re-runs per task
CLAUDE_TIMEOUT   = 600   # 10 minutes max for a single Claude run

def generate_task_id() -> str:
    """Generate a unique task_id based on timestamp."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def parse_approval_tier(task_text: str) -> str:
    """Extract APPROVAL_TIER from task text. Returns T0/T1/T2/T3 or 'UNKNOWN'."""
    for line in task_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("APPROVAL_TIER:"):
            value = stripped.split(":", 1)[1].strip().upper()
            if value in ("T0", "T1", "T2", "T3"):
                return value
    return "UNKNOWN"

# Current task_id — set when a task starts, empty otherwise
current_task_id = ""
current_tier = ""

def write_status(state: str, detail: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(f"status: {state}\ntime: {ts}\n")
        if current_task_id:
            f.write(f"task_id: {current_task_id}\n")
        if current_tier:
            f.write(f"approval_tier: {current_tier}\n")
        f.write(f"detail: {detail}\n")

def needs_response(output: str):
    """
    Detect if Claude output requires a Telegram response before continuing.
    Mirrors the same detection logic used by telegram_bot.py.
    Returns 'APPROVAL_NEEDED' | 'QUESTION' | None
    """
    lower = output.lower()
    approval_kws = [
        "approval needed", "requires approval", "waiting for approval",
        "נדרש אישור", "אישור אייל", "אישור נדרש",
    ]
    if any(kw in lower for kw in approval_kws):
        return "APPROVAL_NEEDED"
    question_kws = ["question for user", "question:", "שאלה:", "האם "]
    if any(kw in lower for kw in question_kws):
        return "QUESTION"
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.endswith("?") and len(stripped) > 5:
            return "QUESTION"
    return None

def read_response() -> str:
    """Read current content of telegram-response.md, empty string if missing."""
    try:
        return open(RESPONSE_FILE, encoding="utf-8").read().strip()
    except FileNotFoundError:
        return ""

def clear_response():
    """Clear telegram-response.md after it has been consumed."""
    try:
        open(RESPONSE_FILE, "w", encoding="utf-8").close()
    except Exception:
        pass


def log_task(task_text, action):
    """Append entry to bridge/task-log.md (shared with telegram_bot.py)."""
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

def parse_response_field(content: str, field: str) -> str:
    """Extract a field from telegram-response.md content."""
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith(f"{field.lower()}:"):
            return line.split(":", 1)[1].strip()
    return ""


def wait_for_telegram_response(event_type: str) -> str:
    """
    Wait up to RESPONSE_TIMEOUT seconds for telegram-response.md to be populated.
    Validates task_id — stale responses (wrong task_id) are discarded, not consumed.
    Returns the response content, or empty string on timeout.
    """
    write_status("waiting_response", f"Waiting for Telegram {event_type}")
    print(f"\n⏳ ממתין לתשובת טלגרם ({event_type}) — מקסימום {RESPONSE_TIMEOUT}s...")
    deadline = time.time() + RESPONSE_TIMEOUT
    while time.time() < deadline:
        content = read_response()
        if content:
            resp_task_id = parse_response_field(content, "task_id")
            # Validate task_id — discard stale responses
            if resp_task_id and resp_task_id != current_task_id:
                print(f"⚠️ תגובה ישנה/שגויה — task_id={resp_task_id!r} (מצפה: {current_task_id!r}) — מנקה")
                clear_response()
                time.sleep(RESPONSE_POLL)
                continue
            print(f"✅ תשובה תקינה מטלגרם (task_id={resp_task_id!r}):\n{content}")
            return content
        time.sleep(RESPONSE_POLL)
    print("⏰ תם הזמן — לא התקבלה תשובה מטלגרם")
    return ""

print("GitHub Bridge — one-shot mode")
print("=" * 50)

write_status("starting")

# 1. git pull
print("מושך שינויים מ-GitHub...")
pull = subprocess.run(
    ["git", "pull", "origin", "main"],
    cwd=REPO,
    capture_output=True,
    text=True
)
if pull.returncode != 0:
    write_status("error", f"git pull failed: {pull.stderr.strip()}")
    print(f"שגיאה ב-git pull: {pull.stderr.strip()}")
    exit(1)

# 2. קרא משימה
if not os.path.exists(TASK_FILE):
    write_status("idle", "next-task.md not found")
    print("לא נמצא קובץ משימה.")
    exit(0)

with open(TASK_FILE, "r", encoding="utf-8") as f:
    task = f.read().strip()

if not task:
    write_status("idle", "next-task.md is empty")
    print("next-task.md ריק — אין משימה להריץ.")
    exit(0)

current_task_id = generate_task_id()
current_tier = parse_approval_tier(task)
print(f"\nמשימה נמצאה — task_id: {current_task_id} | tier: {current_tier}")

# 2b. T3 enforcement — עצירה מלאה עד אישור אייל
if current_tier == "T3":
    print("🛑 APPROVAL_TIER: T3 — נדרש אישור אייל. לא מבצע.")
    log_task(task, f"BLOCKED_T3 [{current_task_id}]")
    awaiting_msg = (
        f"task_id: {current_task_id}\n"
        f"approval_tier: T3\n"
        f"---\n"
        f"STATUS: AWAITING_APPROVAL\n"
        f"REASON: APPROVAL_TIER T3 — נדרש אישור אייל לפני ביצוע\n"
        f"TASK_PREVIEW: {task[:200]}\n"
    )
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(awaiting_msg)
    write_status("awaiting_approval", "T3 — waiting for Eyal approval")
    # Do NOT remove task file — task stays for retry after approval
    subprocess.run(["git", "add", "bridge/"], cwd=REPO)
    subprocess.run(["git", "commit", "-m", f"bridge: T3 awaiting approval [{current_task_id}]"], cwd=REPO)
    subprocess.run(["git", "push"], cwd=REPO)
    print("משימה ממתינה לאישור — task file נשמר.")
    exit(0)

# 2c. UNKNOWN tier — treat as T3 (safe default)
if current_tier == "UNKNOWN":
    print("⚠️ APPROVAL_TIER חסר — מתייחס כ-T3 (ברירת מחדל בטוחה)")
    log_task(task, f"BLOCKED_UNKNOWN_TIER [{current_task_id}]")
    awaiting_msg = (
        f"task_id: {current_task_id}\n"
        f"approval_tier: UNKNOWN (defaulted to T3)\n"
        f"---\n"
        f"STATUS: AWAITING_APPROVAL\n"
        f"REASON: APPROVAL_TIER חסר — ברירת מחדל T3\n"
        f"TASK_PREVIEW: {task[:200]}\n"
    )
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(awaiting_msg)
    write_status("awaiting_approval", "UNKNOWN tier — defaulted to T3")
    if not _args.no_push:
        subprocess.run(["git", "add", "bridge/"], cwd=REPO)
        subprocess.run(["git", "commit", "-m", f"bridge: missing tier, blocked [{current_task_id}]"], cwd=REPO)
        subprocess.run(["git", "push"], cwd=REPO)
    print("משימה ממתינה — הוסף APPROVAL_TIER למשימה.")
    exit(0)

print("מריץ Team Lead...")
log_task(task, f"STARTED [{current_task_id}] [TIER:{current_tier}]")
write_status("running", task[:80])

TL_TIMEOUT = CLAUDE_TIMEOUT + 120  # buffer for Team Lead decision overhead

try:
    # 3. הרץ Team Lead במקום קריאה ישירה ל-Claude
    # team_lead.py כותב ל-RESULT_FILE ול-runtime-state.md בעצמו
    # stdout מכיל summary מובנה: STATUS / VERDICT / SUMMARY
    try:
        tl = subprocess.run(
            [sys.executable,
             os.path.join(REPO, "teams", "team-lead", "team_lead.py"),
             "--task", TASK_FILE],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=TL_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        print(f"❌ Team Lead timeout after {TL_TIMEOUT}s")
        write_status("error", f"Team Lead timeout after {TL_TIMEOUT}s")
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            f.write(f"task_id: {current_task_id}\n---\nERROR: Team Lead timed out after {TL_TIMEOUT}s\n")
        log_task(task, f"TIMEOUT [{current_task_id}]")
        try:
            os.remove(TASK_FILE)
        except OSError:
            pass
        exit(1)

    # stdout = structured summary from team_lead (STATUS / VERDICT / SUMMARY)
    tl_stdout = (tl.stdout or tl.stderr or "").strip()

    if not tl_stdout:
        print(f"❌ Team Lead returned empty output — exit code: {tl.returncode}")
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            f.write(
                f"task_id: {current_task_id}\n"
                f"approval_tier: {current_tier}\n"
                f"---\n"
                f"STATUS: FAILED\n"
                f"REASON: Team Lead returned empty stdout and stderr\n"
                f"EXIT_CODE: {tl.returncode}\n"
            )
        log_task(task, f"FAILED_EMPTY [{current_task_id}]")
        try:
            os.remove(TASK_FILE)
        except OSError:
            pass
        subprocess.run(["git", "add", "bridge/"], cwd=REPO)
        subprocess.run(["git", "commit", "-m", f"bridge: FAILED empty output [{current_task_id}]"], cwd=REPO)
        subprocess.run(["git", "push"], cwd=REPO)
        write_status("failed", f"empty output [{current_task_id}]")
        exit(1)

    print(f"Team Lead stdout:\n{tl_stdout}")

    # team_lead.py כתב כבר ל-RESULT_FILE — קרא אותו לצורך בדיקת Telegram
    try:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            result_content = f.read()
    except OSError:
        result_content = tl_stdout

    # בדוק אם נדרשת תשובת טלגרם (future: team_lead יטפל בזה בעצמו)
    event = needs_response(result_content)
    if event:
        response = wait_for_telegram_response(event)
        if not response:
            write_status("error", f"Telegram response timeout after {event}")
            print(f"❌ timeout — אין תשובה מטלגרם. עוצר.")
            try:
                os.remove(TASK_FILE)
            except OSError:
                pass
            exit(1)
        # תשובה התקבלה — הוסף ל-RESULT_FILE
        with open(RESULT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n---\nTELEGRAM_RESPONSE: {response}\n")
        clear_response()

    print(f"✅ Team Lead סיים")

    # 4. נקה response file לאחר השלמת המשימה
    clear_response()

    # 5. נקה משימה רק אחרי שהתוצאה נכתבה
    try:
        os.remove(TASK_FILE)
    except OSError:
        pass

    log_task(task, f"DONE [{current_task_id}] [TIER:{current_tier}]")
    write_status("done", "result written, task removed")

    # 6. Push תוצאה + status ל-GitHub
    subprocess.run(["git", "add", "bridge/"], cwd=REPO)
    commit = subprocess.run(
        ["git", "commit", "-m", f"bridge: task result [{current_task_id}]"],
        cwd=REPO, capture_output=True, text=True
    )
    if commit.returncode != 0:
        print(f"⚠️ git commit: {commit.stderr.strip()}")

    push = subprocess.run(["git", "push"], cwd=REPO, capture_output=True, text=True)
    if push.returncode != 0:
        write_status("error", f"push failed: {push.stderr.strip()[:80]}")
        print(f"❌ git push failed: {push.stderr.strip()}")
    else:
        print("✅ תוצאה הועלתה ל-GitHub")

finally:
    # ALWAYS transition out of "running" — prevents stuck status
    # Only write idle here if we didn't already write a terminal status above
    finished_id = current_task_id
    current_task_id = ""
    current_tier = ""
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            current_status = f.read()
        if "status: running" in current_status or "status: starting" in current_status:
            write_status("idle", f"task {finished_id} finished (fallback cleanup)")
    except Exception:
        write_status("idle", f"task {finished_id} finished (fallback cleanup)")

print("סיים!")
print("=" * 50)
