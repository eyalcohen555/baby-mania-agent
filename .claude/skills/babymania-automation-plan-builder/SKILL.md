---
name: babymania-automation-plan-builder
description: בונה Conductor plans נכונים לפי מערכת האוטומציה של BabyMania. הפעל בכל פעם שיש 2+ שלבים תלויים, audit → fix → retest flow, או כל צורך ב-plan YAML. טריגרים: "plan", "Conductor", "stages", "dry-run", "bridge", "automation", "workflow", "2+ שלבים", "multi-stage", "plan YAML", "תוכנית", "רב-שלבי", "AUDIT STAGE", "FIX STAGE", "LOGIC STAGE", "RETEST", "conductor.py", "Codex review", "bridge.py". פועל לפי docs/management/conductor-plan-format.md.
allowed-tools: Read, Grep, Glob
---

# babymania-automation-plan-builder — בניית Conductor Plans

## מתי להשתמש

- יש 2+ שלבים תלויים זה בזה (output שלב א → input שלב ב)
- זרימה מסוג: audit → fix → retest
- צריך routing מותנה (LOGIC stage — YES/NO decision)
- צריך dry-run לפני ביצוע
- המשתמש ביקש "תיצור plan"

## מתי לא להשתמש

- פעולה אחת פשוטה ללא תלות — השתמש ב-bridge ידני
- אין routing מותנה ואין 2+ שלבים — bridge ידני עדיף
- המשתמש ביקש state check בלבד (T0)

## מבנה Plan YAML — חוקים קריטיים

### שדות חובה ב-plan level

```yaml
plan_id: <slug>-<NNN>        # לדוגמה: shoes-rollout-003
plan_name: string
approval_tier: T0|T1|T2|T3  # הגבוה ביותר בין כל השלבים
telegram_notify:
  start: bool
  milestones: bool
  done: bool
  blocked: bool
  questions: bool
stages: [...]
```

### שדות חובה בכל stage

```yaml
id: STAGE-<N>               # חובה: STAGE-1, STAGE-2, ... (לא stage1, לא S1)
name: string
type: AUDIT|FIX|LOGIC|RETEST
goal: string                # משפט אחד — מה השלב משיג
action: string              # הוראה חד-משמעית — פעולה אחת בלבד
approval_tier: T0|T1|T2|T3 # חובה — חסר = conductor עוצר
expected_output: string
exit_conditions: [list]     # חייב להיות list — לא מחרוזת
fail_conditions: [list]     # חייב להיות list — לא מחרוזת
next_on_pass: STAGE-X|DONE
next_on_fail: STAGE-X|STOP|SKIP
```

### Stage Types — כללים קריטיים

| Type | תפקיד | כלל |
|------|--------|-----|
| AUDIT | קריאה / בדיקה | אין כתיבה — מחזיר STAGE_VERDICT: PASS/FAIL |
| FIX | תיקון / שינוי | next_on_fail: SKIP אסור — אם נכשל → STOP |
| LOGIC | החלטה בינארית | מחזיר `<KEY>: YES` או `<KEY>: NO` — לא PASS/FAIL |
| RETEST | בדיקה חוזרת | מגיע אחרי FIX — מאמת שהתיקון עבד |

### LOGIC Stage — routing decision

```yaml
- id: STAGE-2
  type: LOGIC
  goal: "להחליט אם נדרש תיקון"
  action: >
    אם condition X → החזר CLEANUP_REQUIRED: YES
    אם לא → החזר CLEANUP_REQUIRED: NO
  expected_output: "CLEANUP_REQUIRED: YES / NO"
  exit_conditions: ["החלטה ברורה YES או NO"]
  fail_conditions: ["לא ניתן להחליט"]
  next_on_pass: STAGE-3    # YES branch → תיקון
  next_on_fail: DONE       # NO branch → לא צריך תיקון (לא כישלון!)
```

**LOGIC_NO ≠ כישלון.** זהו routing decision בלבד.

### אסור ✗

```
FIX + next_on_fail: SKIP          ← אסור (כישלון בfix לא דלגים)
exit_conditions: "הכל תקין"       ← מחרוזת — צריך list
approval_tier: חסר                ← conductor עוצר
stage id: "stage1" / "S-1"       ← חייב STAGE-1
plan_id: ללא suffix NNN           ← חייב slug-NNN
```

## מתי נדרש Codex Review

הוסף `codex_review: true` לstage כשיש:
- שינוי קוד (FIX על קבצי Python / Liquid / YAML)
- routing decision קריטי (LOGIC stage)
- risk לקבצים מחוץ לscope
- ארכיטקטורה השתנתה
- לפני merge ל-main

## כלל Approval Tiers

| Tier | stage type | דוגמה |
|------|-----------|-------|
| T0 | AUDIT — קריאה בלבד | state check, file read |
| T1 | FIX — שינויים בטוחים | תיקון YAML, שינוי config |
| T2 | FIX — שינויים משמעותיים | שינוי agent logic, sections |
| T3 | FIX — Shopify live | כתיבה ל-Shopify, bulk update |

**plan.approval_tier חייב להיות >= הגבוה ביותר בין stages.**

## Preflight לפני ריצה

```
bridge.py רץ (instance אחד בלבד)
telegram_bot.py רץ
watchdog.py רץ
bridge/next-task.md ריק
bridge/status.md = idle
conductor-state: לא RUNNING / לא BLOCKED
```

## הרצה רשמית (נתיב Python מלא — חובה)

```powershell
# Dry-run (לפני כל ריצה אמיתית)
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml --dry-run

# Real run (רק אחרי dry-run PASS)
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml

# Resume (מנקודת עצירה)
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml --resume
```

**אסור:** `python conductor.py` — Windows stub! יוצר 2 instances.

## Organic Plan — STAGE-0 חובה

כל plan שמתחיל ב-`organic-` חייב לכלול STAGE-0:

```yaml
- id: STAGE-0
  name: ORGANIC STATE READ
  type: AUDIT
  goal: "לקרוא state doc ולוודא שהמשימה מתאימה לשכבה הנוכחית"
  action: >
    קרא docs/organic/מצב-הפרויקט-האורגני.md.
    זהה CURRENT_LAYER, NEXT_OPEN_ITEM.
    ודא שהמשימה תואמת לפריט הפתוח. אסור לדלג שכבה.
  approval_tier: T0
  files_allowed: [docs/organic/מצב-הפרויקט-האורגני.md]
  exit_conditions: ["state doc נקרא", "CURRENT_LAYER זוהה", "אין דילוג שכבה"]
  fail_conditions: ["state doc לא נמצא", "המשימה מדלגת שכבה"]
  next_on_pass: STAGE-1
  next_on_fail: STOP
```

## פורמט פלט חובה

```
PLAN_ID:              [slug-NNN]
PLAN_NAME:            [שם קריא]
STAGES_COUNT:         N
APPROVAL_TIER:        [T0/T1/T2/T3 — הגבוה]
STAGE_TYPES:          [AUDIT, FIX, LOGIC, RETEST — כל הstagaes]
T3_STAGES:            [IDs של T3 stages, אחרת NONE]
CODEX_REVIEW:         [IDs שדורשים, אחרת NONE]
TELEGRAM_NOTIFY:      configured
DRY_RUN_REQUIRED:     YES (תמיד)
AYAL_APPROVAL:        [אם יש T3 — YES]
ORGANIC_STAGE0:       [אם organic plan — PRESENT / MISSING]
VALIDATION_ERRORS:    [רשימה, אחרת NONE]
VERDICT:              PLAN_VALID / PLAN_INVALID — [סיבה]
```

## קבצי מקור שחובה לקרוא

- `docs/management/conductor-plan-format.md` — פורמט רשמי + כל החוקים
- `docs/management/chat-to-automation-operating-protocol.md` — מתי plan, מתי bridge ידני

## קבצים שמותר לקרוא

- `bridge/conductor-state.md` — לבדיקת מצב לפני ריצה
- `bridge/status.md` — bridge status לפני ריצה
- `plans/*.yaml` — plans קיימים (לדוגמה / reference)

## פעולות אסורות

- להריץ plan בלי dry-run קודם
- להריץ כשbridge לא idle
- להריץ plan עם T3 stage בלי אישור אייל
- להשתמש ב-`python` ישיר (Windows stub) — חובה נתיב Python מלא
- ליצור FIX stage עם next_on_fail: SKIP
- ליצור exit_conditions כמחרוזת (לא list)
- להשמיט approval_tier מstage
- ליצור plan_id ללא פורמט slug-NNN

## חוקי BabyMania

- Full automation: NO — ממתין לאישור נפרד מאייל.
- Controlled: YES (T1 plans עם dry-run לפני).
- Codex APPROVED ≠ אייל אישר — הם לא אותו דבר.
- conductor לא מחליף bridge.py — הוא שכבה מעל.

## טעויות נפוצות למניעה

- לשכוח approval_tier בstage — conductor לא מריץ, עוצר בparsing.
- exit_conditions כמחרוזת במקום list — parsing error בconductor.
- להשתמש ב-`python` ישיר — יוצר Windows stub chain, preflight כושל.
- LOGIC stage עם next_on_fail: SKIP — LOGIC חייב להחזיר YES/NO, SKIP לא חוקי.
- לא לכלול STAGE-0 בplan אורגני — מדלג שכבה בלי לבדוק state.
