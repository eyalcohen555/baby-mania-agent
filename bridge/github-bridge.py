import subprocess
import os
from datetime import datetime

REPO = r"C:\Projects\baby-mania-agent"
TASK_FILE = r"C:\Projects\baby-mania-agent\bridge\next-task.md"
RESULT_FILE = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
STATUS_FILE = r"C:\Projects\baby-mania-agent\bridge\status.md"
CLAUDE = r"C:\Users\3024e\AppData\Roaming\npm\claude.cmd"

def write_status(state: str, detail: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(f"status: {state}\ntime: {ts}\ndetail: {detail}\n")

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

print(f"\nמשימה נמצאה — מריץ Claude Code...")
write_status("running", task[:80])

# 3. הרץ Claude Code
result = subprocess.run(
    [CLAUDE, "--print", "--dangerously-skip-permissions", task],
    cwd=REPO,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

output = result.stdout if result.stdout else result.stderr

# 4. כתוב תוצאה לפני ניקוי המשימה
with open(RESULT_FILE, "w", encoding="utf-8") as f:
    f.write(output)

# 5. נקה משימה רק אחרי שהתוצאה נכתבה
os.remove(TASK_FILE)

write_status("done", "result written, task removed")

# 6. Push תוצאה + status ל-GitHub
subprocess.run(["git", "add", "bridge/"], cwd=REPO)
subprocess.run(["git", "commit", "-m", "bridge: task result"], cwd=REPO)
push = subprocess.run(["git", "push"], cwd=REPO)

if push.returncode != 0:
    write_status("error", "push failed after task completion")
else:
    write_status("pushed")

print("סיים! תוצאה הועלתה ל-GitHub")
print("=" * 50)
