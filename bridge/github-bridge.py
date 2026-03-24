import time
import subprocess
import os

REPO = r"C:\Projects\baby-mania-agent"
TASK_FILE = r"C:\Projects\baby-mania-agent\bridge\next-task.md"
RESULT_FILE = r"C:\Projects\baby-mania-agent\bridge\last-result.md"
CLAUDE = r"C:\Users\3024e\AppData\Roaming\npm\claude.cmd"

print("GitHub Bridge פעיל — מאזין לשינויים ב-GitHub...")
print("=" * 50)

last_task = ""

while True:
    try:
        # משוך שינויים מ-GitHub
        subprocess.run(
            ["git", "pull", "--quiet"],
            cwd=REPO,
            capture_output=True
        )

        # קרא את קובץ המשימה
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                task = f.read().strip()

            if task and task != last_task:
                last_task = task
                print(f"\nמשימה חדשה מ-GPT!")

                # הרץ Claude Code
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
                with open(TASK_FILE, "w", encoding="utf-8") as f:
                    f.write("")

                # Push תוצאה ל-GitHub
                subprocess.run(["git", "add", "bridge/"], cwd=REPO)
                subprocess.run(
                    ["git", "commit", "-m", "bridge: task result"],
                    cwd=REPO
                )
                subprocess.run(["git", "push"], cwd=REPO)

                print("סיים! תוצאה הועלתה ל-GitHub")
                print("=" * 50)
                last_task = ""

    except Exception as e:
        print(f"שגיאה: {e}")

    time.sleep(10)
