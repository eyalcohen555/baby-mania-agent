# Bridge Operations Journal
**תחום:** כל מה שקשור ל-bridge — runtime, permissions, singleton, task flow, startup
**עדכון:** אחרי כל שינוי bridge או גילוי תפעולי חדש

---

## JOURNAL TEMPLATE

```
## DATE: YYYY-MM-DD
## TASK: שם המשימה
## SCOPE: bridge component
## WHAT CHANGED:
## FILES TOUCHED:
## SYSTEM IMPACT:
## OPEN ISSUES:
## NEXT STEP:
```

---

## DATE: 2026-03-25
## TASK: Bridge Initial Audit
## SCOPE: כל תשתית ה-bridge
## WHAT CHANGED: audit בלבד, ללא שינויים
## FILES TOUCHED: none

## SYSTEM IMPACT — מצב שנמצא:
- `bridge.py` קיים אך לא רץ אוטומטית
- `bridge/github-bridge.py` קיים (one-shot + git sync)
- **בעיה קריטית:** `claude.cmd --print` ללא `--dangerously-skip-permissions` → Claude עוצר ומבקש אישור
- כפילות: `next-task.md` + `last-result.md` קיימים גם ב-root וגם ב-`bridge/`
- אין singleton guard — שני instances יכולים לרוץ יחד

## OPEN ISSUES: ראה next entries

## NEXT STEP: תיקון --dangerously-skip-permissions, נרמול path

---

## DATE: 2026-03-25
## TASK: Bridge Fix — dangerously-skip-permissions
## SCOPE: bridge.py, github-bridge.py
## WHAT CHANGED:
- `bridge.py`: הוסף `--dangerously-skip-permissions` לקריאת claude.cmd
- `bridge/github-bridge.py`: הוסף `--dangerously-skip-permissions`
- נוצר `start-bridge.bat`

## FILES TOUCHED:
- `bridge.py` (שורה 24)
- `bridge/github-bridge.py` (שורה 52)
- `start-bridge.bat` (חדש)

## SYSTEM IMPACT:
- Claude Code מבצע tool calls ללא עצירה לאישור
- TEST: `BRIDGE_OK` נכתב ל-`last-result.md` ✅

## OPEN ISSUES: none
## NEXT STEP: נרמול path

---

## DATE: 2026-03-25
## TASK: Bridge Path Normalization
## SCOPE: bridge.py — path unification
## WHAT CHANGED:
- `bridge.py` עודכן: TASK_FILE + RESULT_FILE + STATUS_FILE → `bridge/` במקום root
- `bridge/` הוגדר כ-official path הרשמי
- root `next-task.md` + `last-result.md` → DEPRECATED
- נוצר `bridge/task-format.md` עם schema רשמי למשימה ותוצאה
- **תיקון חשוב בפורמט:** task לא מבקש מClause לכתוב ל-last-result.md — bridge.py לוכד stdout ושומר

## FILES TOUCHED:
- `bridge.py` (paths, write_status)
- `bridge/task-format.md` (חדש)
- `next-task.md` (DEPRECATED)
- `last-result.md` (DEPRECATED)

## SYSTEM IMPACT:
- שני הסקריפטים (bridge.py + github-bridge.py) מצביעים לאותם קבצים
- source of truth אחד: `bridge/next-task.md`, `bridge/last-result.md`, `bridge/status.md`

## OPEN ISSUES: none
## NEXT STEP: singleton guard

---

## DATE: 2026-03-25
## TASK: Bridge Singleton Lock (Hardening)
## SCOPE: bridge.py — runtime safety
## WHAT CHANGED:
- `bridge/bridge.lock` — קובץ lock חדש עם PID
- `acquire_lock()` — בדיקת PID חי ב-Windows ע"י `ctypes.windll.kernel32.OpenProcess`
- Stale lock recovery — אם PID מת: מנקה lock ועולה
- `atexit.register(release_lock)` — שחרור lock בכל סיום נורמלי
- `try/finally` — שחרור lock גם ב-exception
- Lifecycle statuses: `idle / running / done / failed / locked`

## FILES TOUCHED:
- `bridge.py` (singleton-hardened, full rewrite)

## SYSTEM IMPACT:
- שני instances לא יכולים לרוץ יחד
- crash recovery אוטומטי (stale lock detection)
- status.md מדויק בכל מצב

## TEST RESULTS:
- Instance 1 עולה + lock נוצר ✅
- Instance 2 נחסם + status=locked ✅
- stale lock (PID מת) → cleaned → instance חדש ✅
- atexit → lock released ✅

## OPEN ISSUES: none
## NEXT STEP: Task Scheduler auto-start

---

## DATE: 2026-03-25
## TASK: Task Scheduler Auto-Start
## SCOPE: Windows Task Scheduler, start-bridge.bat
## WHAT CHANGED:
- `start-bridge.bat` עודכן: הסרת `start /B`, הוספת `python -u` (unbuffered log), `>>` לappend
- `scripts/setup_bridge_scheduler.ps1` נוצר — רושם task ב-Task Scheduler
- Task `BabyMania Bridge AutoStart` נרשם: logon trigger, user 3024e, RestartCount 3, ExecTimeLimit ∞

## FILES TOUCHED:
- `start-bridge.bat`
- `scripts/setup_bridge_scheduler.ps1` (חדש)

## SYSTEM IMPACT:
- Bridge עולה אוטומטית בכל login
- אין צורך בהפעלה ידנית
- Logs נכתבים ל-`logs/bridge.log`

## TEST:
- Task רשום ✅
- Enabled: True ✅
- LastTaskResult: 0x41301 (RUNNING) ✅
- bridge/status.md: idle PID 9568 ✅

## OPEN ISSUES: none

## NEXT STEP: bridge מוכן לשימוש יומיומי. כתוב משימות ל-bridge/next-task.md.

---

## DATE: 2026-03-25
## TASK: Operations Lane — Official Closure
## SCOPE: operations lane — סגירה רשמית
## WHAT CHANGED: תיעוד רשמי בלבד — אין שינוי קוד

## OPERATIONS LANE STATUS: ✅ CLOSED — OPERATIONAL

### מה נסגר ומאומת:
| רכיב | מצב |
|------|-----|
| `bridge/` — official path | ✅ source of truth יחיד |
| `bridge/next-task.md` | ✅ כניסת משימות |
| `bridge/last-result.md` | ✅ יציאת תוצאות (stdout) |
| `bridge/status.md` | ✅ מצב live אוטומטי |
| `bridge.py` — polling loop | ✅ singleton-safe (PID lock + stale recovery) |
| `bridge/bridge.lock` | ✅ מגן מ-dual instance |
| `--dangerously-skip-permissions` | ✅ Claude Code מבצע ללא עצירה |
| `start-bridge.bat` — entrypoint | ✅ `python -u bridge.py >> logs\bridge.log` |
| Task Scheduler: `BabyMania Bridge AutoStart` | ✅ Enabled, logon trigger, user 3024e |
| `scripts/setup_bridge_scheduler.ps1` | ✅ קיים להקמה מחדש |
| `docs/operations/bridge-runtime-status.md` | ✅ quick-reference מלא |

### אין open issues בoperations.

## FILES TOUCHED: none (תיעוד בלבד)
## SYSTEM IMPACT: operations lane רשמית סגורה ותפעולית
## OPEN ISSUES: none
## NEXT STEP: priority חוזר ל-shoes lane — ריצת test ראשונה על מוצר נעל אמיתי

---

## DATE: 2026-03-25
## TASK: GitHub Mode — Official Source of Truth
## SCOPE: bridge architecture — GitHub כ-source of truth

## WHAT CHANGED:
- `.github/workflows/claude-bridge.yml` תוקן: הוסף `--dangerously-skip-permissions`
- `.gitignore` עודכן: הוסר `bridge/last-result.md` (חייב להיות tracked עבור CI), הוסף `bridge/bridge.lock` (runtime)
- BABYMANIA-MASTER-PROMPT.md עודכן: GitHub flow מתועד כמסלול רשמי

## ARCHITECTURE — שני מסלולים:

**GitHub mode (רשמי):**
```
GPT push → bridge/next-task.md → GitHub Actions trigger
→ claude --print --dangerously-skip-permissions
→ bridge/last-result.md committed back → GPT קורא מGitHub
```

**Local fallback:**
```
bridge.py (singleton-safe) ← Task Scheduler (BabyMania Bridge AutoStart)
← bridge/next-task.md (מקומי) → bridge/last-result.md
```

## חוקי GitHub mode:
- GitHub repo = source of truth — לא המחשב המקומי
- local runner = executor בלבד
- GPT כותב task ל-GitHub, קורא result מ-GitHub
- CI מריץ: `ANTHROPIC_API_KEY` חייב להיות ב-GitHub Secrets

## FILES TOUCHED:
- `.github/workflows/claude-bridge.yml` (תוקן)
- `.gitignore` (עודכן)
- `BABYMANIA-MASTER-PROMPT.md` (עודכן)

## OPEN ISSUES:
- [ ] לוודא ש-`ANTHROPIC_API_KEY` מוגדר ב-GitHub Secrets של הrepo

## NEXT STEP: shoes pipeline test-run

---

## DATE: 2026-03-30
## TASK: Document Real Python Start Rule
## SCOPE: master prompt + runtime docs — תיעוד בלבד
## WHAT CHANGED:
- `BABYMANIA-MASTER-PROMPT.md`: שכתוב סקציית startup — הפרדה ברורה בין אוטומטי (bat) לידני (Python מלא), הוספת דוגמאות conductor (plan/dry-run/resume), סימון "אסור" מפורש ל-`python bridge.py`
- `docs/operations/bridge-runtime-status.md`: עדכון "אם bridge לא רץ" — נתיב Python מלא במקום start-bridge.bat

## FILES TOUCHED:
- `BABYMANIA-MASTER-PROMPT.md`
- `docs/operations/bridge-runtime-status.md`

## SYSTEM IMPACT: תיעוד בלבד — אין שינוי קוד
## OPEN ISSUES: none
## NEXT STEP: —
