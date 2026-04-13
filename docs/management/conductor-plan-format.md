# Conductor Plan Format — Official Spec
**גרסה:** 1.0 | **תאריך:** 2026-03-27
**תפקיד:** פורמט רשמי לתוכניות execution רב-שלביות עבור conductor.py
**סטטוס:** ACTIVE SPEC

---

## 1. PURPOSE

תוכנית execution (`plan`) היא רצף מוגדר של שלבים (stages) שconductor.py קורא ומבצע אחד-אחד דרך ה-bridge הקיים.

**מה conductor צריך לקרוא מהקובץ:**
- מה המשימה הכוללת (`plan_name`, `plan_id`)
- אילו שלבים לבצע ובאיזה סדר (`stages`)
- מה ה-approval tier של כל שלב (`approval_tier`)
- מה נחשב הצלחה / כישלון לכל שלב (`exit_conditions`, `fail_conditions`)
- לאן לעבור אחרי כל שלב (`next_on_pass`, `next_on_fail`)
- מתי לשלוח Telegram (`telegram_notify`, `is_milestone`)

**מה הפורמט לא מגדיר:**
- לוגיקת bridge פנימית
- פורמט task ל-Claude (conductor ממיר בעצמו)
- כלים, scripts, או קוד ספציפי

---

## 2. FILE FORMAT

**פורמט:** YAML בלבד.

**מיקום:** `plans/<plan-name>.yaml`

**דוגמאות נתיב:**
```
plans/bridge-stabilization.yaml
plans/telegram-fix-001.yaml
plans/shoes-rollout.yaml
```

**כלל שמות קבצים:**
- lowercase, מקפים בין מילים
- ללא רווחים
- סיומת `.yaml` בלבד (לא `.yml`)

---

## 3. TOP-LEVEL REQUIRED FIELDS

```yaml
plan_id: string          # מזהה ייחודי. פורמט: <slug>-<NNN> לדוגמה: bridge-stabilization-001
plan_name: string        # שם קריא בעברית או אנגלית
approval_tier: T0|T1|T2|T3  # ה-tier הכולל של התוכנית (הגבוה ביותר שמופיע בשלבים)
telegram_notify:         # מדיניות Telegram לתוכנית כולה
  start: bool            # שלח הודעה כשהתוכנית מתחילה
  milestones: bool       # שלח הודעה על שלבי milestone
  done: bool             # שלח הודעה כשהתוכנית מסתיימת
  blocked: bool          # שלח הודעה כשהתוכנית נחסמת
  questions: bool        # שלח הודעה כשנדרשת שאלה (מעבר לmechanism הקיים בbridge)
stages: list[Stage]      # רשימה סדורה של שלבים — הסדר קובע סדר ביצוע
```

**כלל approval_tier ברמת plan:**
```
plan.approval_tier חייב להיות >= ל-approval_tier הגבוה ביותר בין כל שלביו.
אם stage כלשהו הוא T3, אז plan.approval_tier = T3.
```

---

## 4. STAGE REQUIRED FIELDS

כל פריט ברשימת `stages` מגדיר שלב אחד:

```yaml
id: string               # מזהה ייחודי בתוך התוכנית. פורמט: STAGE-<N> לדוגמה: STAGE-1
name: string             # שם קריא לשלב
type: AUDIT|FIX|LOGIC|RETEST  # סיווג השלב (ראה סעיף 6)
goal: string             # מה השלב אמור להשיג — משפט אחד
action: string           # הוראה חד-משמעית לביצוע — מה לבדוק / לתקן / לבצע
approval_tier: T0|T1|T2|T3   # tier לשלב הספציפי הזה
expected_output: string  # מה נצפה לראות ב-last-result לאחר הביצוע
exit_conditions: list[string]  # תנאים שחייבים להתקיים כדי שהשלב ייחשב PASS
fail_conditions: list[string]  # תנאים שמעידים על FAIL — conductor עוצר או מסלים
next_on_pass: STAGE-X|DONE     # לאן עוברים אם השלב עבר
next_on_fail: STAGE-X|STOP|SKIP  # לאן עוברים אם השלב נכשל
```

---

## 5. OPTIONAL FIELDS

שדות אופציונליים לכל stage:

```yaml
files_allowed: list[string]   # קבצים מותרים לbridge task. ברירת מחדל: ריק (ללא הגבלה)
files_forbidden: list[string] # קבצים אסורים לbridge task. ברירת מחדל: ריק
is_milestone: bool            # האם לשלוח Telegram notification בסיום מוצלח. ברירת מחדל: false
requires_approval: bool       # האם לעצור ולבקש אישור מאייל לפני הביצוע (T3 behavior). ברירת מחדל: false
```

**כלל requires_approval:**
```
אם requires_approval: true — conductor עוצר לפני ביצוע השלב,
שולח Telegram עם כפתורי אשר/דחה, וממתין לתגובה.
זה רלוונטי גם ל-T2 שלבים רגישים, לא רק T3.
```

---

## 6. FIELD RULES

### id
- חייב להיות ייחודי בתוך התוכנית
- פורמט: `STAGE-<N>` כאשר N מספר עולה מ-1
- ✅ `STAGE-1`, `STAGE-2`, `STAGE-14`
- ❌ `stage1`, `S1`, `STAGE_1`

### type
חייב להיות בדיוק אחד מ:

| ערך | משמעות |
|-----|--------|
| `AUDIT` | קריאה ובדיקה בלבד, ללא כתיבה |
| `FIX` | תיקון / שינוי קבצים |
| `LOGIC` | החלטה מחושבת — ניתוח תוצאות ובחירת מסלול |
| `RETEST` | בדיקה חוזרת אחרי fix |

#### LOGIC Stage Routing — כלל מיוחד

שלב מסוג `LOGIC` **אינו** stage של PASS/FAIL רגיל.
הוא מייצג **החלטה בינארית** שמנתבת את התוכנית לאחד משני מסלולים.

```
LOGIC stage:
  next_on_pass = YES branch  — תנאי מתקיים, מסלול A
  next_on_fail = NO branch   — תנאי לא מתקיים, מסלול B

זה ≠ כישלון. זהו routing decision בלבד.
```

**כלל חובה לconductor:**
```
אם stage.type == "LOGIC":
  חפש בoutput שורה בפורמט: <FIELD>: YES או <FIELD>: NO
  YES → next_on_pass (מסלול A)
  NO  → next_on_fail (מסלול B)
  לא נמצא YES/NO → UNKNOWN → עצור (אל תנחש)

אם stage.type != "LOGIC":
  חפש: STAGE_VERDICT: PASS | FAIL | AWAITING_APPROVAL
  PASS → next_on_pass
  FAIL → next_on_fail
```

**פורמט חובה לoutput של LOGIC stage:**
```
<KEY>: YES   ← שורה אחת ברורה
או
<KEY>: NO
```
דוגמאות תקינות:
```
CLEANUP_REQUIRED: YES
MESSAGE_FIX_REQUIRED: NO
RESUME_POSSIBLE: YES
```

**next_on_fail של LOGIC stage אינו מוגבל:**
```
✅ LOGIC + next_on_fail: STAGE-X  (alternate path)
✅ LOGIC + next_on_fail: STOP     (אם גם NO הוא כישלון)
✅ LOGIC + next_on_fail: DONE     (אם NO = המשימה הושלמה)
❌ LOGIC + next_on_fail: SKIP     (אסור — LOGIC חייב להחזיר verdict ברור)
```

### next_on_pass / next_on_fail
ערכים חוקיים:

| ערך | משמעות |
|-----|--------|
| `STAGE-X` | עבור לשלב X |
| `DONE` | התוכנית הושלמה בהצלחה |
| `STOP` | עצור, התוכנית נכשלה — שלח Telegram |
| `SKIP` | דלג לשלב הבא ברשימה |

- `SKIP` אסור ב-`next_on_fail` של שלב `type: FIX` — כישלון בfix לא ניתן לדילוג
- `STOP` מסיים את התוכנית מיד ומדווח PLAN_FAILED

### approval_tier
- חייב להיות בדיוק: `T0`, `T1`, `T2`, או `T3`
- חסר approval_tier = שגיאת parsing — conductor עוצר לפני ביצוע

### action
- חייב לתאר פעולה אחת בלבד
- חייב לכלול מה לבדוק / מה לכתוב / מה לתקן
- ❌ `"בדוק הכל"` — לא מספיק ספציפי
- ✅ `"בדוק כמה instances של bridge.py רצים, זהה duplicates לפי cmdline"`

### exit_conditions / fail_conditions
- חייבים להיות `list` — גם אם פריט אחד
- כל פריט: מחרוזת תנאי ברורה וניתנת לבדיקה
- ❌ `exit_conditions: "הכל תקין"` — מחרוזת ולא רשימה
- ✅ `exit_conditions: ["process list ברור", "אין ambiguity ב-runtime"]`

---

## 7. VALID EXAMPLE

```yaml
plan_id: bridge-runtime-audit-001
plan_name: "Bridge Runtime Audit"
approval_tier: T1
telegram_notify:
  start: true
  milestones: false
  done: true
  blocked: true
  questions: true

stages:
  - id: STAGE-1
    name: RUNTIME AUDIT
    type: AUDIT
    goal: "לזהות כמה instances של bridge.py רצים ואם יש duplicates"
    action: >
      בדוק את רשימת תהליכי Python הרצים.
      זהה instances של bridge.py, telegram_bot.py, watchdog.py.
      ציין PID, command line, וסטטוס כל תהליך.
    approval_tier: T0
    files_allowed:
      - bridge/**
      - logs/**
    files_forbidden: []
    expected_output: "רשימת processes ברורה עם זיהוי duplicates"
    exit_conditions:
      - "כל processes זוהו עם PID ו-cmdline"
      - "ברור כמה instances פעילים מכל סוג"
    fail_conditions:
      - "לא ניתן לקרוא process list"
      - "ambiguity — לא ברור איזה instance הוא הרשמי"
    next_on_pass: STAGE-2
    next_on_fail: STOP

  - id: STAGE-2
    name: CLEANUP DECISION
    type: LOGIC
    goal: "להחליט אם נדרש ניקוי על בסיס תוצאות STAGE-1"
    action: >
      אם נמצאו duplicate processes או stale lock files → next_on_pass = STAGE-3.
      אם הכל נקי → next_on_pass = DONE.
      החלטה חייבת להיות מבוססת רק על ממצאי STAGE-1.
    approval_tier: T1
    expected_output: "CLEANUP_REQUIRED: YES / NO עם נימוק"
    exit_conditions:
      - "החלטה ברורה: CLEANUP YES או CLEANUP NO"
    fail_conditions:
      - "לא ניתן להחליט מהמידע שנאסף"
    next_on_pass: STAGE-3
    next_on_fail: STOP

  - id: STAGE-3
    name: CLEANUP
    type: FIX
    goal: "להרוג processes כפולים ולנקות lock files עודפים"
    action: >
      עצור את ה-processes הכפולים שזוהו ב-STAGE-1.
      נקה lock/pid files שמצביעים על PIDs מתים.
      אל תגע בקוד. אל תשנה לוגיקה.
    approval_tier: T1
    files_allowed:
      - bridge/bridge.lock
      - bridge/watchdog.pid
    files_forbidden:
      - bridge.py
      - teams/**
    is_milestone: true
    expected_output: "runtime נקי — instance אחד בלבד מכל סוג"
    exit_conditions:
      - "רק instance אחד של bridge.py פעיל"
      - "רק instance אחד של watchdog.py פעיל"
      - "bridge.lock מצביע על PID חי"
    fail_conditions:
      - "לא ניתן לעצור process"
      - "cleanup עלול לסכן stability"
    next_on_pass: DONE
    next_on_fail: STOP
```

---

## 8. INVALID EXAMPLES

### ❌ דוגמה שגויה 1 — חסר approval_tier בשלב

```yaml
stages:
  - id: STAGE-1
    name: AUDIT
    type: AUDIT
    goal: "בדיקה"
    action: "בדוק משהו"
    expected_output: "תוצאה"
    exit_conditions: ["תוצאה תקינה"]
    fail_conditions: ["תוצאה שגויה"]
    next_on_pass: DONE
    next_on_fail: STOP
    # ❌ חסר: approval_tier
```
**למה שגוי:** `approval_tier` הוא שדה חובה בכל stage. conductor לא יכול לקבוע את ה-tier בעצמו — זו אחריות מחבר התוכנית.

---

### ❌ דוגמה שגויה 2 — exit_conditions כמחרוזת, לא רשימה

```yaml
  - id: STAGE-2
    name: DECISION
    type: LOGIC
    goal: "החלטה"
    action: "בדוק ותחליט"
    approval_tier: T1
    expected_output: "החלטה"
    exit_conditions: "הכל תקין"    # ❌ מחרוזת במקום list
    fail_conditions: "משהו נכשל"   # ❌ מחרוזת במקום list
    next_on_pass: DONE
    next_on_fail: STOP
```
**למה שגוי:** `exit_conditions` ו-`fail_conditions` חייבים להיות `list`. מחרוזת לא ניתנת לאיטרציה וconductor ייכשל ב-parsing.

---

### ❌ דוגמה שגויה 3 — next_on_fail: SKIP על שלב מסוג FIX

```yaml
  - id: STAGE-4
    name: FIX LOCK FILE
    type: FIX               # שלב fix
    goal: "תיקון lock file"
    action: "מחק bridge.lock ישן"
    approval_tier: T1
    expected_output: "lock file תוקן"
    exit_conditions: ["lock file מצביע על PID חי"]
    fail_conditions: ["לא ניתן למחוק"]
    next_on_pass: STAGE-5
    next_on_fail: SKIP      # ❌ SKIP על FIX אסור
```
**למה שגוי:** כישלון בשלב `FIX` לא ניתן לדילוג — המערכת עלולה להישאר במצב תקוע. חובה להשתמש ב-`STOP` ולחקור.

---

## 9. PARSING NOTES

**סדר ביצוע:**
```
conductor מבצע stages לפי סדר הופעתן ברשימה.
next_on_pass / next_on_fail קובעים לאן ממשיכים —
לא בהכרח לפי הסדר הפיזי ברשימה.
conductor מחפש את ה-stage לפי id.
```

**זיהוי stop condition:**
```
אם next_on_pass = DONE   → התוכנית הצליחה, conductor כותב PLAN_VERDICT: PASS
אם next_on_fail = STOP   → התוכנית נכשלה, conductor כותב PLAN_VERDICT: FAILED
אם stage verdict = UNKNOWN → conductor מתייחס כאל FAIL
```

**זיהוי milestone:**
```
אם stage.is_milestone = true וה-stage עבר (PASS) →
conductor שולח Telegram (אם telegram_notify.milestones = true)
```

**זיהוי flow ב-LOGIC stages:**
```
שלב מסוג LOGIC לא אמור לשנות קבצים.
ה-action שלו מנחה את Claude לבצע ניתוח ולהחזיר החלטה בינארית.

conductor מחפש בoutput:
  1. שורה בפורמט "<KEY>: YES" → LOGIC_YES → next_on_pass
  2. שורה בפורמט "<KEY>: NO"  → LOGIC_NO  → next_on_fail
  3. לא נמצא → UNKNOWN → עצור (conductor לא מנחש)

LOGIC_YES ו-LOGIC_NO אינם PASS/FAIL — הם routing decisions בלבד.
conductor לא ירשום LOGIC_NO כ-failed_stage.
```

**overall flow:**
```
1. conductor טוען plan YAML
2. מתחיל מ-stages[0]
3. ממיר stage → bridge task → כותב לbridge/next-task.md
4. ממתין לbridge לסיים (status = idle + task_id תואם)
5. קורא last-result.md → מחפש PASS / FAIL / AWAITING_APPROVAL
6. עדכן conductor-state.md
7. עבור ל-next_on_pass / next_on_fail
8. חזור לשלב 3 עד DONE / STOP
```

---

## 10. תוספת — Organic Plan Template

**כל plan שנוגע לאורגני חייב לכלול STAGE-0 מסוג AUDIT לפני כל שלב אחר:**

```yaml
  - id: STAGE-0
    name: ORGANIC STATE READ
    type: AUDIT
    goal: "לקרוא את state doc האורגני ולזהות שהמשימה מתאימה לשכבה הנוכחית"
    action: >
      קרא את docs/organic/מצב-הפרויקט-האורגני.md.
      זהה: CURRENT_LAYER, NEXT_OPEN_ITEM.
      ודא שהמשימה הנוכחית מתאימה לפריט הפתוח הראשון.
      אסור לדלג שכבה. אסור לפתוח item חדש אם יש item פתוח קודם.
    approval_tier: T0
    files_allowed:
      - docs/organic/מצב-הפרויקט-האורגני.md
    files_forbidden: []
    expected_output: >
      STATE FILE READ: YES
      CURRENT LAYER: [X]
      NEXT OPEN ITEM: [item]
      WHY THIS TASK NOW: [reason]
      WHAT IS BLOCKED AFTER THIS: [blockers]
    exit_conditions:
      - "state doc נקרא"
      - "CURRENT_LAYER זוהה"
      - "המשימה תואמת לפריט הפתוח — אין דילוג שכבה"
    fail_conditions:
      - "state doc לא נמצא"
      - "לא ניתן לזהות CURRENT_LAYER"
      - "המשימה מדלגת שכבה פתוחה"
    next_on_pass: STAGE-1
    next_on_fail: STOP
```

**כלל:** אם plan_id מתחיל ב-`organic-` → STAGE-0 מסוג ORGANIC STATE READ הוא חובה.
conductor אינו מאמת זאת בקוד — זו אחריות כותב ה-plan.

---

## 10. DESIGN BOUNDARY

```
Plan file (*.yaml)
  ↓ מגדיר מה לעשות
conductor.py
  ↓ מנהל תוכנית, מחליט stage הבא, שולח Telegram
  ↓ כותב task אחד בכל פעם
bridge/next-task.md
  ↓ קובץ תקשורת יחיד
bridge.py / github-bridge.py
  ↓ single-task executor — לא יודע על conductor
  ↓ מריץ task, מחזיר תוצאה
team_lead.py
  ↓ task-level manager — מנתח output per task, נותן verdict
  ↓ לא יודע על תוכנית רב-שלבית
watchdog.py
  ↓ מוניטור stuck per task — לא משתנה
telegram_bot.py
  ↓ ערוץ תקשורת — מקבל events מconductor דרך conductor-notify.md
```

**כלל ברזל:**
```
conductor לא מחליף bridge.py, team_lead.py, או watchdog.py.
conductor הוא שכבה מעל — orchestrator של stages.
bridge נשאר single-task executor בלבד.
team_lead נשאר task-level verdict provider בלבד.
```

---

## נספח — מיפוי שדות: Plan Stage → Bridge Task

| שדה ב-stage | שדה בbridge task | הערה |
|-------------|-----------------|------|
| `id` | `CONDUCTOR_STAGE` | מזהה לmatch בלast-result |
| `goal` + `action` | `GOAL` + `ACTION` | ממוזגים לhook אחד |
| `approval_tier` | `APPROVAL_TIER` | מועבר ישיר |
| `files_allowed` | `FILES_ALLOWED` | מועבר ישיר |
| `files_forbidden` | `FILES_FORBIDDEN` | מועבר ישיר |
| `expected_output` | `EXPECTED` | מועבר ישיר |
| `plan_id` + `id` + timestamp | `TASK_ID` | `conductor-<plan_id>-<stage_id>-<ts>` |
