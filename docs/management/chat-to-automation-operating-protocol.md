# Chat to Automation Operating Protocol
**גרסה:** 1.0 | **תאריך:** 2026-05-08
**סטטוס:** ACTIVE
**מטרה:** לכל צ'אט GPT עתידי — איך להפוך משימה ל-plan אוטומטי רב-שלבי

---

## 1. מטרת המסמך

כל צ'אט GPT חייב להבין את המטרה העסקית לפני שהוא שולח פקודה כלשהי ל-Claude Code.

**המטרה אינה:** לשלוח הרבה פקודות Claude ידניות.
**המטרה היא:** להמיר עבודת פרויקט אמיתית לאוטומציה רב-שלבית בטוחה.

**למה זה חשוב:**
- אייל לא צריך להיות תקוע בלולאות copy-paste בין GPT לבין Claude Code.
- כל משימה שיכולה להיות plan — חייבת להיות plan.
- כל plan שיש בו risk — חייב Codex review.
- כל החלטה קריטית — חייבת אישור אייל.

**הכלל הראשון:**
> לפני כל פקודה — הבן את המטרה. לפני כל הרצה — ודא dry-run.

---

## 2. חוק ראשון לכל צ'אט

לפני כל פקודה Claude, הצ'אט חייב לענות על:

```
1. מה המטרה העסקית?
   → מה אנחנו רוצים להשיג? מה הבעיה שפותרים?

2. איזה צוות / תחום?
   → product page / organic / automation / other

3. מה המצב הנוכחי?
   → קרא: BABYMANIA-MASTER-PROMPT.md
   → קרא: journal רלוונטי
   → בדוק: branch, conductor-state, bridge status

4. האם זו משימה אחת פשוטה או workflow רב-שלבי?
   → משימה אחת → bridge ידני
   → 2+ שלבים תלויים → Conductor plan

5. האם ניתן לטפל בזה דרך אוטומציה?
   → אם כן — צור plan YAML

6. מה יכול להשתבש?
   → הגדר fail_conditions לכל שלב

7. היכן חייב אייל לאשר?
   → T3 / merge / full automation / high risk
```

**לא לדלג על שאלות אלו.** צ'אט שדולג על שלב 1–3 לפני ביצוע — עוצר.

---

## 3. החלטה: משימה ידנית או plan אוטומטי

| מצב | גישה מומלצת |
|-----|-------------|
| פעולה אחת קטנה ללא תלות | bridge ידני (next-task.md) |
| אין routing מותנה | bridge ידני |
| אין צורך ב-Codex review | bridge ידני |
| אין risk בקבצים לא-רלוונטיים | bridge ידני |
| 2+ שלבים תלויים | Conductor plan |
| audit → fix → retest flow | Conductor plan |
| output של שלב אחד קובע את הבא | Conductor plan |
| risk של קבצים מחוץ לscope | Conductor plan + Codex review |
| Codex צריך לבדוק output | Conductor plan עם `codex_review: true` |
| אייל רוצה להפחית copy-paste | Conductor plan |

**כלל ברור:**
> אם יש ספק — plan. אם יש risk — Codex. אם יש T3 — עצור ושאל אייל.

---

## 4. Flow אוטומציה רשמי

```
GPT מגדיר מטרה עסקית
        ↓
Claude Code מבצע STATE AUDIT (בדיקת מצב נוכחי)
        ↓
Claude Code יוצר plan YAML
        ↓
Dry-run — ניסוי ללא ביצוע (conductor.py --dry-run)
        ↓
Plan מאושר ורץ פעם אחת (conductor.py)
        ↓
Claude Code מבצע שלב אחרי שלב דרך bridge
        ↓
Codex בודק output בכל שלב שמסומן codex_review: true
        ↓
Conductor מנתב לשלב הבא לפי verdict + Codex decision
        ↓
אייל נכנס רק ל-T3 / blockers / RISK HIGH / full automation
```

**אסור לדלג על dry-run.** אסור להריץ plan בלי לבדוק YAML קודם.

---

## 5. מבנה plan נדרש

כל plan חייב לכלול:

```yaml
plan_id: <slug>-NNN             # לדוגמה: shoes-rollout-003
plan_name: string
approval_tier: T0|T1|T2|T3     # הגבוה ביותר בין כל השלבים
telegram_notify:
  start: true|false
  milestones: true|false
  done: true|false
  blocked: true|false
  questions: true|false
stages:
  - id: STAGE-1
    name: string
    type: AUDIT|FIX|LOGIC|RETEST
    goal: string                # משפט אחד — מה השלב אמור להשיג
    action: string              # הוראה חד-משמעית
    approval_tier: T0|T1|T2|T3
    codex_review: true|false
    files_allowed: [list]
    files_forbidden: [list]
    expected_output: string
    exit_conditions: [list]
    fail_conditions: [list]
    next_on_pass: STAGE-X|DONE
    next_on_fail: STAGE-X|STOP|SKIP
```

**spec מלא:** `docs/management/conductor-plan-format.md`

---

## 6. כללי עיצוב stage

כל stage חייב להיות קטן, ממוקד ומדיד.

```
✅ כל stage:
  - מטרה אחת ברורה
  - קבצים מורשים מפורשים (files_allowed)
  - קבצים אסורים מפורשים (files_forbidden)
  - תנאי PASS מדידים (exit_conditions)
  - תנאי FAIL ברורים (fail_conditions)
  - routing ברור (next_on_pass / next_on_fail)

❌ אסור:
  - מטרה מעורפלת ("שפר משהו")
  - גישה רחבה לקבצים ללא הצדקה
  - exit_conditions: [] (ריק — Conductor לא יכול לאמת)
  - שני דברים שונים באותו stage
```

**שלב ל-AUDIT, שלב ל-FIX, שלב ל-RETEST — לעולם לא ביחד.**

---

## 7. כללי שימוש ב-Codex

**Codex חובה כאשר:**
- תוצאת stage קובעת את העבודה הבאה
- קוד השתנה (FIX stage)
- ארכיטקטורה השתנתה
- נדרשת merge readiness (G-A gate)
- scope קבצים מסוכן
- לוגיקה T2 / T3 מעורבת
- איכות output חשובה לפרויקט

**Decisions של Codex:**

| Decision | משמעות | תגובת Conductor |
|----------|---------|----------------|
| `CONTINUE` | הכל תקין | routing לפי next_on_pass |
| `RETRY` | output לא מספיק | routing לפי next_on_fail (FAIL) |
| `FIX` | תקן בעיה ספציפית | stage סינתטי לתיקון → ממשיך |
| `STOP` | עצור — סיכון גבוה | BLOCKED ללא override |
| `ASK_AYAL` | נדרשת החלטה של הבעלים | BLOCKED, מחכה לאייל |
| `NEXT_STAGE` | דלג לשלב ספציפי | קופץ ל-STAGE-N שCodon ציין |

**כלל:** `STOP` ו-`ASK_AYAL` — אין override אוטומטי. אייל בלבד.

---

## 8. כללי אישור

| פעולה | מי מאשר |
|-------|---------|
| T0 stages (read-only, audit) | אוטומטי |
| T1 stages (שינויים בטוחים) | אוטומטי |
| T2 stages (שינויים משמעותיים) | Claude מנתח, Codex בודק, אוטומטי |
| T3 stages (Shopify live / bulk / ארכיטקטורה) | **אייל חובה** |
| Shopify live write | **אייל חובה** |
| merge ל-main | **אייל חובה** |
| full automation | **אייל חובה — החלטה ניהולית נפרדת** |
| Codex STOP / ASK_AYAL | **אייל חובה** |
| שינוי ארכיטקטורה עם risk גבוה | **אייל חובה** |
| כל פעולה בלתי הפיכה שלא הוגדרה מראש | **אייל חובה** |

---

## 9. פקודות Claude Code סטנדרטיות לצ'אטים עתידיים

### A. STATE AUDIT COMMAND
**מטרה:** לפני תכנון, הבן את המצב הנוכחי.

```
TASK: STATE AUDIT — <PROJECT_NAME>
APPROVAL_TIER: T0
LAYER: 1

MISSION MODE: Read-only audit. Do not modify files. Do not commit. Do not push.

GOAL:
Audit current state for <PROJECT_NAME> before planning <BUSINESS_GOAL>.

ACTION:
1. Read BABYMANIA-MASTER-PROMPT.md — confirm current snapshot.
2. Read relevant journal: <JOURNAL_PATH>
3. Check git branch: git branch --show-current
4. Check conductor-state: bridge/conductor-state.md
5. Check bridge status: bridge/status.md
6. List relevant files: <FILES_TO_CHECK>

EXPECTED OUTPUT:
SYSTEM STATE
BRANCH
CONDUCTOR STATE
BRIDGE STATUS
RELEVANT FILES EXIST: YES / NO
ISSUES FOUND
READY TO PLAN: YES / NO
```

---

### B. CREATE PLAN COMMAND
**מטרה:** לבקש מ-Claude Code ליצור plan YAML מלא.

```
TASK: CREATE PLAN — <PLAN_NAME>
APPROVAL_TIER: T1
LAYER: 1

MISSION MODE: Create YAML plan only. Do not execute. Do not commit.

GOAL:
Create a complete Conductor plan YAML for <BUSINESS_GOAL>.

PLAN REQUIREMENTS:
- plan_id: <PLAN_NAME>
- Plan must include: <STAGE_COUNT> stages
- Stage types required: AUDIT / FIX / LOGIC / RETEST (as needed)
- Files allowed: <FILES_ALLOWED>
- Files forbidden: <FILES_FORBIDDEN>
- Codex review: required on stages that change files or decide routing
- Expected final result: <EXPECTED_RESULT>
- Full automation: NO (Ayal must approve separately)

OUTPUT FILE:
plans/<PLAN_NAME>.yaml

EXPECTED OUTPUT:
FILE CREATED: YES / NO
STAGES COUNT
YAML VALID: YES / NO
```

---

### C. DRY-RUN COMMAND
**מטרה:** לאמת מבנה plan ללא ביצוע.

```
TASK: DRY-RUN — <PLAN_NAME>
APPROVAL_TIER: T1
LAYER: 1

MISSION MODE: Dry-run only. Do not execute stages. Do not write to bridge. Do not commit.

ACTION:
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<PLAN_NAME>.yaml --dry-run

EXPECTED OUTPUT:
BRANCH
DRY RUN RESULT: PASS / FAIL
STAGES PARSED
ROUTING VALID: YES / NO
FILES CHANGED: NO
ISSUES FOUND
READY FOR REAL RUN: YES / NO
```

---

### D. RUN CONTROLLED PLAN COMMAND
**מטרה:** הרצה מבוקרת של plan אחד.

```
TASK: RUN CONTROLLED PLAN — <PLAN_NAME>
APPROVAL_TIER: T1
LAYER: 1

MISSION MODE:
Run one plan once. Do not run full automation. Do not touch Shopify. Do not commit runtime files.

PRECHECK (must all pass before running):
- Branch: main
- bridge.py running (single instance, real Python path)
- telegram_bot.py running
- watchdog.py running
- bridge/status.md = idle
- bridge/next-task.md = empty
- conductor-state: not RUNNING, not BLOCKED

ACTION (only if precheck passes):
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<PLAN_NAME>.yaml

EXPECTED OUTPUT:
PRECHECK RESULT: PASS / FAIL
REAL PLAN RESULT: PASS / FAIL / BLOCKED / NOT RUN
STAGES COMPLETED
FILES CHANGED
ISSUES FOUND
READY FOR FULL AUTOMATION: NO
```

---

### E. POST-RUN REPORT COMMAND
**מטרה:** לסכם תוצאה ולתעד milestone אם נדרש.

```
TASK: POST-RUN REPORT — <PLAN_NAME>
APPROVAL_TIER: T1
LAYER: 1

MISSION MODE: Report and document only. Do not run plans. Do not touch code.

ACTION:
1. Read bridge/conductor-state.md — confirm final status.
2. Read bridge/conductor-log.md — confirm stages and timestamps.
3. If result = PASS and milestone worthy:
   - Add entry to docs/management/management-journal.md
   - Update BABYMANIA-MASTER-PROMPT.md snapshot if needed
4. Report full result.

FILES_ALLOWED: docs/management/management-journal.md, BABYMANIA-MASTER-PROMPT.md
FILES_FORBIDDEN: bridge/**, plans/**, scripts/**, teams/**, Shopify

EXPECTED OUTPUT:
PLAN: <PLAN_NAME>
RESULT: PASS / FAIL / BLOCKED
STAGES COMPLETED
MILESTONE DOCUMENTED: YES / NO
MASTER PROMPT UPDATED: YES / NO
FULL AUTOMATION STILL NO: YES
```

---

## 10. טעויות למניעה

```
❌ לא לפקוד ל-Claude לפני שמבינים את המטרה העסקית.
❌ לא ליצור לולאת copy-paste ידנית אם plan יכול לטפל בזה.
❌ לא ליצור plan ענקי עם stages לא ברורים.
❌ לא לדלג על dry-run לפני הרצה אמיתית.
❌ לא לדלג על Codex review בstages קריטיים.
❌ לא לגעת ב-Shopify ללא T3 ואישור אייל.
❌ לא לערבב scopes: product / organic / automation בplan אחד.
❌ לא לתקן output כשהבעיה היא ב-logic.
❌ לא להפעיל full automation ללא אישור מפורש מאייל.
❌ לא לפרש "Codex APPROVED" כ"אייל אישר" — הם לא אותו דבר.
```

---

## 11. חוק סופי לכל צ'אט

כל צ'אט חייב לסיים תכנון עם:

```
1. מה הצעד הבא המדויק?
   → פעולה אחת, ברורה, עם scope מוגדר

2. למה הצעד הזה?
   → מה הוא מקדם בפרויקט?

3. מה מוכיח הצלחה?
   → exit_conditions ספציפיים — לא "כנראה עובד"

4. מה אסור לקרות?
   → fail_conditions ברורים

5. האם זה ידני או אוטומציה?
   → אם אוטומציה — plan מוכן? dry-run עבר?
```

**אין "בערך טוב". אין "כנראה עובד". יש PASS או FAIL.**

---

## מצב נוכחי

```
Full automation: NO — ממתין לאישור נפרד מאייל להפעלה מלאה.
Controlled daily use: YES (T1 plans עם dry-run לפני)
bridge-telegram-stabilization-001: DONE / PASS על main (2026-05-08)
```

---

*source of truth לפרוטוקול אוטומציה. שאלות על תפקיד Codex → `docs/management/codex-automation-role.md`. שאלות על workflow יומי → `docs/management/automation-daily-workflow.md`.*
