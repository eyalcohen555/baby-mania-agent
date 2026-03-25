import subprocess
import os

REPO = r"C:\Projects\baby-mania-agent"
TASK_FILE = r"C:\Projects\baby-mania-agent\bridge\next-task.md"
RESULT_FILE = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
CLAUDE = r"C:\Users\3024e\AppData\Roaming\npm\claude.cmd"

print("GitHub Bridge — one-shot mode")
print("=" * 50)

# 1. git pull
print("מושך שינויים מ-GitHub...")
subprocess.run(["git", "pull", "origin", "main"], cwd=REPO)

# 2. קרא משימה מ-next-task.md
if not os.path.exists(TASK_FILE):
    print(f"לא נמצא קובץ משימה: {TASK_FILE}")
    exit(0)

with open(TASK_FILE, "r", encoding="utf-8") as f:
    task = f.read().strip()

if not task:
    print("next-task.md ריק — אין משימה להריץ.")
    exit(0)

print(f"\nמשימה נמצאה — מריץ Claude Code...")

# 3. הרץ פעם אחת
result = subprocess.run(
    [CLAUDE, "--print", task],
    cwd=REPO,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

output = result.stdout if result.stdout else result.stderr

# שמור תוצאה
with open(RESULT_FILE, "w", encoding="utf-8") as f:
    f.write(output)

# נקה משימה
os.remove(TASK_FILE)

# Push תוצאה ל-GitHub
subprocess.run(["git", "add", "bridge/"], cwd=REPO)
subprocess.run(["git", "commit", "-m", "bridge: task result"], cwd=REPO)
subprocess.run(["git", "push"], cwd=REPO)

print("סיים! תוצאה הועלתה ל-GitHub")
print("=" * 50)
