# מדריך Workflow יומי — מערכת האוטומציה של BabyMania
**גרסה:** 1.0 | **תאריך:** 2026-05-07
**סטטוס:** ACTIVE
**מטרה:** הסבר פשוט לשימוש יומי במערכת — מי עושה מה, מתי, ואיך

---

## 1. מה המערכת עושה

המערכת מחליפה לולאות copy-paste ידניות בין GPT לבין Claude Code.

**לפני:** GPT כותב משימה → אייל מעתיק ל-Claude → Claude מחזיר → אייל מעתיק חזרה לGPT.
**אחרי:** GPT כותב plan YAML → Conductor מריץ אוטומטית → Codex בודק כל שלב → Conductor ממשיך.

**מי עושה מה:**

| שחקן | תפקיד |
|------|--------|
| GPT | מנהל פרויקט — מתכנן, כותב plans, מנחה |
| Claude Code | מבצע — קורא קבצים, עורך, מריץ דרך bridge |
| Conductor | מנהל שלבים — קורא YAML, מריץ, מנתב |
| Codex | מבקר — בודק output של Claude ומחזיר decision |
| אייל | מאשר — נכנס רק ל-T3, blockers, ו-RISK HIGH |

---

## 2. מתי להשתמש באוטומציה במקום משימה ידנית

**השתמש ב-Conductor plan כאשר:**
- המשימה כוללת 2+ שלבים תלויים זה בזה
- יש קריטריוני PASS / FAIL ברורים לכל שלב
- הכישלון בשלב אחד צריך לעצור את הבא
- רוצים שCodex יבדוק output לפני שממשיכים

**המשך עם bridge ידני (next-task.md) כאשר:**
- המשימה חד-שלבית ופשוטה
- אין routing מותנה
- אין צורך בביקורת Codex

**לעולם לא:**
- copy-paste ידני של output בין Claude לבין GPT אם plan יכול לטפל בזה
- הרצה ידנית של סקריפטים כשיש plan מוכן
- דילוג על Codex review כשscopecritical

---

## 3. איך משימה הופכת ל-plan

```
1. GPT מגדיר מטרה עסקית ברורה
2. GPT בודק מצב נוכחי (קבצים, branch, conductort-state)
3. GPT כותב plan YAML עם stages
4. כל stage מגדיר:
   - goal: מה הוא אמור לבצע
   - type: AUDIT / FIX / LOGIC / RETEST
   - approval_tier: T0 / T1 / T2 / T3
   - codex_review: true/false
   - files_allowed + files_forbidden
   - exit_conditions
   - next_on_pass / next_on_fail
5. GPT מבקש מ-Claude Code להריץ:
   python conductor.py plans/<plan>.yaml
```

פורמט מלא: `docs/management/conductor-plan-format.md`

---

## 4. איך Claude Code מבצע שלב

```
Conductor קורא stage מה-YAML
    ↓
כותב task לתוך bridge/next-task.md
    ↓
bridge.py מזהה task (polling כל 4 שניות)
    ↓
בודק APPROVAL_TIER:
  T3 → עוצר: AWAITING_APPROVAL (מחכה לאייל)
  T0–T2 → מריץ: claude --print --dangerously-skip-permissions
    ↓
Claude Code קורא את המשימה, מבצע, כותב ל-last-result.md
    ↓
Conductor קורא output, מנתח verdict (PASS / FAIL / UNKNOWN)
    ↓
אם codex_review: true → Codex בודק (ראה סעיף 5)
אחרת → routing לפי next_on_pass / next_on_fail
```

---

## 5. איך Codex בודק output

**Codex מופעל אוטומטית לאחר כל stage שמסומן `codex_review: true`.**

```
Conductor קורא output של Claude
    ↓
שולח ל-codex_reviewer.py: plan context + stage goal + output
    ↓
Codex (Claude נפרד) קורא, מנתח, מחזיר decision מובנה
    ↓
Conductor כותב decision ל-bridge/codex-decision.md
    ↓
Conductor ממשיך לפי decision (ראה סעיף 6)
```

**מה Codex בודק:**
- האם exit_conditions התקיימו?
- האם fail_conditions התרחשו?
- האם הפעולה הייתה בתוך scope המוגדר?
- האם יש risk בהמשך?

**Codex לא מחליף אייל.** הוא רק ממליץ. אייל הוא הגורם המאשר.

---

## 6. decisions שCodex יכול להחזיר

| Decision | משמעות | מה Conductor עושה |
|----------|---------|-------------------|
| `CONTINUE` | הכל תקין, המשך | routing לפי next_on_pass |
| `RETRY` | output לא מספיק, נסה שוב | routing לפי next_on_fail (FAIL) |
| `FIX` | תקן בעיה ספציפית | Conductor יוצר stage סינתטי לתיקון, מריץ, ואז ממשיך |
| `STOP` | עצור — סיכון גבוה | Conductor עוצר ב-BLOCKED ללא קשר ל-next_on_fail |
| `ASK_AYAL` | נדרשת החלטה של הבעלים | Conductor עוצר ב-BLOCKED, מחכה לאייל |
| `NEXT_STAGE` | דלג לשלב ספציפי | Conductor קופץ ל-STAGE-N שCodon ציין |

**כלל:** Codex STOP / ASK_AYAL = עצור לחלוטין. אין override אוטומטי.

---

## 7. מתי אייל חייב להיכנס

**חובה — אין אוטומציה:**
- כל stage מסוג T3 (Shopify live / bulk / ארכיטקטורה)
- Codex החזיר `ASK_AYAL` או `STOP`
- RISK LEVEL: HIGH מ-Codex
- merge ל-main (לעולם לא אוטומטי)
- full automation ראשון מסוגו (precedent)
- כל פעולה בלתי הפיכה שלא הוגדרה מראש

**לא נדרש — אוטומטי:**
- T0 stages (read-only, audit)
- T1 stages (שינויים בטוחים)
- T2 stages (שינויים משמעותיים — Claude מנתח, Codex בודק)
- Codex החזיר `CONTINUE` — ללא התערבות

---

## 8. מה אסור — הגבלות מוחלטות

```
❌ full automation ללא אישור מפורש מאייל
❌ Shopify live write ללא T3 + אישור אייל
❌ קבצים מחוץ ל-scope המוגדר ב-files_allowed / files_forbidden
❌ copy-paste ידני אם plan יכול לטפל בזה
❌ דילוג על Codex review ב-stages קריטיים
❌ merge ל-main ללא G-A Codex gate + אישור אייל מפורש
❌ הרצת plan ב-automation-conductor-telegram-clean לפני בדיקה ב-branch נפרד
```

---

## 9. איך chat עתידי צריך לעבוד

**סדר חובה לפני כל ביצוע:**

```
שלב א: הבן מטרה עסקית
  → מה אנחנו רוצים להשיג? מה הבעיה שפותרים?

שלב ב: בדוק מצב נוכחי
  → קרא: BABYMANIA-MASTER-PROMPT.md (snapshot)
  → קרא: journal רלוונטי (management / organic / product)
  → בדוק: branch נוכחי, conductor-state, bridge status

שלב ג: בחר נתיב
  → משימה חד-שלבית → bridge ידני (next-task.md)
  → משימה רב-שלבית → Conductor plan (YAML)
  → ספק, scope לא ברור → שאל אייל לפני ביצוע

שלב ד: כתוב את ה-command
  → רק אחרי שלבים א–ג
  → עם approval_tier מוגדר
  → עם files_allowed + files_forbidden ברורים
  → עם exit_conditions מדידים
```

**כלל זהב:**
> אם לא ברור מה המטרה → אל תריץ. בקש הבהרה.
> אם ברור המטרה אבל לא ברור הscope → כתוב plan YAML ובדוק עם Codex לפני הרצה.

---

## נספח: נתיבי Python רשמיים

```powershell
# conductor
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml

# dry-run
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/<plan>.yaml --dry-run

# bridge (ידני)
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe bridge.py
```

⚠️ לעולם לא: `python conductor.py` — Windows stub יוצר duplicate process ומכשיל preflight.

---

## מצב נוכחי — Full Automation

```
Full automation: NO
PR #2 מוזג; full automation עדיין NO ודורש אישור נפרד מאייל.
Codex Decision Loop: OPERATIONAL (smoke test PASS, 2026-05-07)
bridge-telegram-stabilization-001: DONE / PASS על main (2026-05-08 08:45:24)
G-A Codex Gate: APPROVED / RISK LOW
Controlled main real test: PASS (2026-05-08) — 7/7 stages

הפעלת full automation מחייבת:
1. החלטה ניהולית מפורשת מאייל על full automation
```

---

*source of truth לworkflow יומי. שאלות על workflow → מסמך זה. שאלות על תפקיד Codex → `docs/management/codex-automation-role.md`.*
