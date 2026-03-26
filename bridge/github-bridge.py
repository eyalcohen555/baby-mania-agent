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

def generate_task_id() -> str:
    """Generate a unique task_id based on timestamp."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")

# Current task_id — set when a task starts, empty otherwise
current_task_id = ""

def write_status(state: str, detail: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(f"status: {state}\ntime: {ts}\n")
        if current_task_id:
            f.write(f"task_id: {current_task_id}\n")
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

def wait_for_telegram_response(event_type: str) -> str:
    """
    Wait up to RESPONSE_TIMEOUT seconds for telegram-response.md to be populated.
    Returns the response content, or empty string on timeout.
    """
    write_status("waiting_response", f"Waiting for Telegram {event_type}")
    print(f"\n⏳ ממתין לתשובת טלגרם ({event_type}) — מקסימום {RESPONSE_TIMEOUT}s...")
    deadline = time.time() + RESPONSE_TIMEOUT
    while time.time() < deadline:
        content = read_response()
        if content:
            print(f"✅ תשובה התקבלה מטלגרם:\n{content}")
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
print(f"\nמשימה נמצאה — task_id: {current_task_id}")
print("מריץ Claude Code...")
log_task(task, f"STARTED [{current_task_id}]")
write_status("running", task[:80])

# 3. הרץ Claude Code — עם wait-loop לתשובת טלגרם
output = ""
for round_num in range(1, MAX_ROUNDS + 1):
    print(f"\n--- Round {round_num}/{MAX_ROUNDS} ---")
    result = subprocess.run(
        [CLAUDE, "--print", "--dangerously-skip-permissions", task],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    output = result.stdout if result.stdout else result.stderr

    # שמור תוצאה ביניים — עם task_id בראש הקובץ
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(f"task_id: {current_task_id}\n---\n{output}")

    # בדוק אם קלוד ממתין לתשובה מטלגרם
    event = needs_response(output)
    if not event:
        print(f"✅ Claude סיים ללא המתנה (round {round_num})")
        break

    # ממתין לתשובת טלגרם
    response = wait_for_telegram_response(event)
    if not response:
        write_status("error", f"Telegram response timeout after {event}")
        print(f"❌ timeout — אין תשובה מטלגרם. עוצר.")
        os.remove(TASK_FILE)
        exit(1)

    # תשובה התקבלה — נקה את הקובץ ורוץ שוב (קלוד יקרא telegram-response.md)
    # הקובץ נשמר ב-RESPONSE_FILE כדי שקלוד יוכל לקרוא אותו בסיבוב הבא
    print(f"🔄 מריץ שוב עם תשובת טלגרם (round {round_num + 1})...")
    write_status("running", f"re-run after {event} response (round {round_num + 1})")
else:
    print(f"⚠️ הגענו למקסימום {MAX_ROUNDS} סיבובים — עוצר")
    write_status("error", f"max rounds ({MAX_ROUNDS}) reached")
    os.remove(TASK_FILE)
    exit(1)

# 4. נקה response file לאחר השלמת המשימה
clear_response()

# 5. נקה משימה רק אחרי שהתוצאה נכתבה
os.remove(TASK_FILE)

log_task(task, f"DONE [{current_task_id}]")
write_status("done", "result written, task removed")

# 6. Push תוצאה + status ל-GitHub
subprocess.run(["git", "add", "bridge/"], cwd=REPO)
subprocess.run(["git", "commit", "-m", f"bridge: task result [{current_task_id}]"], cwd=REPO)
push = subprocess.run(["git", "push"], cwd=REPO)

if push.returncode != 0:
    write_status("error", "push failed after task completion")
else:
    write_status("pushed")

print("סיים! תוצאה הועלתה ל-GitHub")
print("=" * 50)
