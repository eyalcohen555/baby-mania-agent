# Bridge Runtime Status Guide
**תפקיד:** הסבר איך לקרוא את מצב ה-bridge הלייב.
**מצב live אמיתי:** תמיד `bridge/status.md`

---

## איך לבדוק שה-bridge חי

```bash
# בדיקה מהירה
cat C:/Projects/baby-mania-agent/bridge/status.md
cat C:/Projects/baby-mania-agent/bridge/bridge.lock
```

**תוצאה תקינה:**
```
status: idle
time: 2026-03-25 12:56:01
detail: PID 9568
```
+ קובץ `bridge.lock` מכיל את אותו PID.

---

## ערכי status.md

| status | משמעות | פעולה |
|--------|---------|--------|
| `idle` | Bridge חי, ממתין למשימה | ✅ מוכן לקבל משימה |
| `running` | מבצע משימה כרגע | ⏳ המתן |
| `done` | סיים משימה, כותב idle | ✅ קרא last-result.md |
| `failed` | שגיאה בלולאה | ⚠️ בדוק logs/bridge.log |
| `locked` | נסיון instance שני נחסם | ℹ️ instance קיים רץ |

---

## Task Scheduler

**שם Task:** `BabyMania Bridge AutoStart`
**Trigger:** At logon — user 3024e
**Action:** `cmd.exe /c "C:\Projects\baby-mania-agent\start-bridge.bat"`
**Log:** `C:\Projects\baby-mania-agent\logs\bridge.log`

```powershell
# בדיקה
Get-ScheduledTaskInfo -TaskName "BabyMania Bridge AutoStart"
```

---

## כיצד לשלוח משימה

1. כתוב לקובץ `bridge/next-task.md` בפורמט הרשמי (ראה `bridge/task-format.md`)
2. Bridge מזהה שינוי תוך 4 שניות
3. מריץ Claude Code עם `--dangerously-skip-permissions`
4. תוצאה נכתבת ל-`bridge/last-result.md`
5. `bridge/next-task.md` מנוקה
6. status חוזר ל-`idle`

---

## נתיבים רשמיים

```
bridge/next-task.md     ← כתיבת משימה
bridge/last-result.md   ← קריאת תוצאה
bridge/status.md        ← מצב live
bridge/bridge.lock      ← PID פעיל
logs/bridge.log         ← log ריצה מלא
```

---

## אם ה-bridge לא רץ

```bash
# בדוק אם יש lock ישן
cat C:/Projects/baby-mania-agent/bridge/bridge.lock
# אם קיים — בדוק אם ה-PID חי. אם מת — bridge.py ינקה אוטומטית בהפעלה הבאה.

# הפעל דרך Task Scheduler
Start-ScheduledTask -TaskName "BabyMania Bridge AutoStart"

# הפעל ישירות — חובה נתיב Python מלא (לא stub!)
cd C:\Projects\baby-mania-agent
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe bridge.py
```

---

## ⚠️ כלל Python path — ריצה ידנית / conductor

**בעיה ידועה:** הרצת `python bridge.py` דרך Windows stub יוצרת שרשרת:
`WindowsApps\python.exe bridge.py` → `pythoncore-3.14-64\python.exe bridge.py`

שני הprocesses מכילים `bridge.py` ב-commandline — conductor סופר אותם כ-2 instances ונכשל בpreflight עם:
`PREFLIGHT FAILED: Multiple bridge.py instances running (2)`

**פתרון — השתמש בנתיב Python המלא:**
```powershell
# bridge (הפעלה ידנית)
cd C:\Projects\baby-mania-agent
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe bridge.py

# conductor
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml
```

**אבחון לפני kill — בדוק command line מלא:**
```powershell
Get-WmiObject Win32_Process -Filter "name='python.exe'" |
  Where-Object { $_.CommandLine -like '*bridge.py*' -and $_.CommandLine -notlike '*github-bridge*' } |
  Select-Object ProcessId,CommandLine | Format-List
```
אם רואים stub (WindowsApps) + real (pythoncore) — זה **לא** duplicate, זו שרשרת launcher.
פתרון: הפעל עם נתיב מלא → תקבל process אחד בלבד.

---

## ביטול / עצירה

```powershell
# עצור את ה-task (לא מוחק)
Stop-ScheduledTask -TaskName "BabyMania Bridge AutoStart"

# השבת לצמיתות
Disable-ScheduledTask -TaskName "BabyMania Bridge AutoStart"

# הפעל מחדש אחרי השבתה
Enable-ScheduledTask  -TaskName "BabyMania Bridge AutoStart"

# מחק לגמרי
Unregister-ScheduledTask -TaskName "BabyMania Bridge AutoStart" -Confirm:$false
```

---

## הפעלה ידנית ואימות

**⚠️ הפעלה ידנית נקייה — תמיד עם נתיב Python מלא:**
```powershell
cd C:\Projects\baby-mania-agent
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe bridge.py
```

**דרך Task Scheduler:**
```powershell
# הפעל עכשיו
Start-ScheduledTask -TaskName "BabyMania Bridge AutoStart"

# בדוק תוצאה אחרי 4 שניות
Start-Sleep 4
Get-ScheduledTaskInfo -TaskName "BabyMania Bridge AutoStart"
# LastTaskResult: 0x41301 = RUNNING ✅
# LastTaskResult: 0x0     = SUCCESS (יצא נקי)
# LastTaskResult: 0xC000013A = נסגר בCtrl+C / kill (נורמלי בטסטים)

# אמת שה-bridge חי
cat C:/Projects/baby-mania-agent/bridge/status.md
```
