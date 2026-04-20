# VISUAL QA CHECKLIST

**גרסה:** v1
**תאריך:** 2026-04-19
**שייך ל:** P1-S5 / AUTOMATION-HARDENING-PLAN v1

---

## STATUS

טיוטה פעילה — מסמך חובה לפני push

---

## PURPOSE

בדיקה חזותית מחייבת לפני push נועדה לזהות כשלים שעוברים טכנית אך נכשלים ברמת התוכן החי — במיוחד fingerprints, type mismatch, template artifacts, וחריגות bundle.

הבדיקה האוטומטית (Gates 1–4) אינה מספיקה לבדה. עין אנושית חייבת לאמת לפני כל push.

---

## WHEN THIS CHECKLIST IS REQUIRED

Visual QA חובה בכל אחד מהמצבים הבאים:

- לפני **כל** live push — ללא יוצא מן הכלל
- אחרי recovery ממוקד (תיקון מוצרים פגועים)
- אחרי שינוי ב-generator, validator, או bundler רלוונטי
- לפני closure declaration של שכבה
- אחרי כל batch שבו נמצא anomaly חדש

---

## REQUIRED SAMPLE

לכל Visual QA, חובה לבדוק את המדגם הבא:

| קבוצה | כמות | הגדרה |
|---|---|---|
| clothing sample | 12 | מוצרי ביגוד מגוונים מה-batch — כולל לפחות 2 מוצרים מקטגוריות שונות |
| shoes sample | 4 | מוצרי נעלים מה-batch — אם אין 4 בריצה, בודקים את כולם |
| anomaly controls | 2 | מוצרים שמופיעים ב-Known Anomalies Registry — לאמת שאינם ב-bundle |
| comparison cases | 2 | מוצרים עם `geo_comparison=true` — לאמת שה-comparison field תקין |

**כשאין comparison cases בריצה:**
רשום בשדה ה-verdict: `comparison_cases: N/A — לא רלוונטי לריצה זו`

**כשאין shoes בריצה:**
רשום: `shoes_sample: N/A — אין נעלים ב-batch`

---

## VISUAL CHECKS

---

### CHECK A — אין Technical Fingerprint גלוי

**מה בודקים:**
קריאה של 3 שורות ראשונות בטקסט כל מוצר ב-sample — האם מופיעים מזהים טכניים.

**FAIL אם:**
- מופיעים ספרות בסוגריים: `(1113)`, `(XXXX)`, `(221)`
- מופיעות מחרוזות אנגלית-טכנית: `pid:`, `sku:`, `handle:`, `id:`
- מופיעות מחרוזות שנראות כ-code במקום טקסט טבעי

**PASS אם:**
הטקסט קריא כשפה טבעית ללא אף מזהה טכני

**מחייב עצירה:**
כן — כל fingerprint אחד = עצירת push מיידית

---

### CHECK B — סוג המוצר תואם לטקסט

**מה בודקים:**
קריאת ה-hero headline + שורת הפתיחה — האם הטקסט מתאר את המוצר שה-title מגדיר?

**FAIL אם:**
- מוצר חליפה מתואר עם מינוח של נעל/כובע/אביזר
- הנושא הראשי בטקסט הוא product type שונה מהמוצר עצמו
- ה-title מציין `חליפה` אך הטקסט כותב `"הסוליה"` / `"הכובע"` כנושא

**PASS אם:**
ה-headline ושורת הפתיחה עקביים עם שם ו-type של המוצר

**מחייב עצירה:**
כן — type mismatch = עצירת push

---

### CHECK C — אין Template Repetition בולט

**מה בודקים:**
השוואה ויזואלית מהירה בין 5 מוצרים שונים ב-sample — האם הפתיחות/סיומות זהות?

**FAIL אם:**
- 3+ מוצרים פותחים באותה שורה או משפט
- 3+ מוצרים מסיימים באותה שורה
- הטקסט נראה "מוחתם" — אותו שלד עם שינויי ערכים בלבד

**PASS אם:**
כל מוצר מרגיש ייחודי בפתיחתו ובסיומו

**מחייב עצירה:**
כן — אם pattern בולט ב-3+ מוצרים

---

### CHECK D — אין Description Bleed

**מה בודקים:**
קריאת הטקסט ובדיקה האם מופיע ניסוח שנראה מועתק מתיאור מוצר אחר או מ-description_raw.

**FAIL אם:**
- הטקסט כולל שם מוצר ספציפי שלא תואם את ה-title הנוכחי
- ניכר ניסוח מכני זהה לניסוח שיווקי ישן שאינו מותאם למוצר
- מופיעות פרטים ספציפיים (שמות דמויות, מותגים) שלא שייכים למוצר הנוכחי

**PASS אם:**
הטקסט עקבי עם המוצר הספציפי ואינו כולל ניסוח שנראה "גנוב"

**מחייב עצירה:**
כן — bleed ברור = עצירת push

---

### CHECK E — אין Fabricated Claim נראה לעין

**מה בודקים:**
קריאה של benefits + emotional_reassurance — האם יש טענות שנראות לא מבוססות?

**FAIL אם:**
- מופיעות כוכביות / דירוגים ללא הקשר של reviews אמיתיים
- מופיעים ציטוטים מהורים שנראים מומצאים
- מופיעות תעודות / אישורים ללא מקור ברור
- מופיע "90% מההורים" או דומה ללא מקור

**PASS אם:**
הטענות כלליות ועקביות עם מה שנפוץ לתיאורי מוצרים — ללא מספרים ספציפיים או ציטוטים

**מחייב עצירה:**
כן — fabricated claim בולט = עצירת push

---

### CHECK F — geo_comparison מופיע רק כשצריך

**מה בודקים:**
לכל מוצר ב-comparison sample: האם ה-geo_comparison metafield קיים? לכל מוצר שאינו comparison-eligible: האם ה-field נעדר?

**FAIL אם:**
- מוצר שאינו comparison-eligible מכיל geo_comparison
- מוצר comparison-eligible חסר את ה-field

**PASS אם:**
התאמה מלאה בין comparison_eligible flag לבין קיום ה-field

**מחייב עצירה:**
כן — geo_comparison leak = עצירת push

---

### CHECK G — Anomaly PID מוחרג באמת

**מה בודקים:**
בדיקה שכל PID ב-Known Anomalies Registry **אינו** מופיע ב-bundle הנוכחי.

**FAIL אם:**
- PID `9881362759993` (או כל anomaly רשום אחר) מופיע ברשימת המוצרים שעומדים ל-push

**PASS אם:**
כל ה-PIDs ב-registry נעדרים מה-bundle

**מחייב עצירה:**
כן — anomaly leakage = עצירת push מיידית

---

### CHECK H — הטקסט נראה טבעי ואנושי

**מה בודקים:**
קריאה רצופה של טקסט מוצר אחד שלם — האם הוא נשמע כמו תוכן שנכתב לאדם?

**FAIL אם:**
- המשפטים נשמעים מכניים / robotics / חוזרניים ברמה בולטת
- הטקסט כולל מעברים פתאומיים שאינם הגיוניים
- חלקים שנראים כמו תבנית שלא מולאה: `[שם מוצר]`, `___`, `XXX`
- שפה גנרית חסרת ייחוד לאורך כל הטקסט

**PASS אם:**
הטקסט קריא, טבעי, ומרגיש מותאם למוצר הספציפי

**מחייב עצירה:**
שיקול דעת — אם 3+ מוצרים ב-sample נכשלים ב-Check H → עצירת push

---

## APPROVAL FORMAT

לאחר ביצוע ה-Visual QA, חובה למלא ולשמור אישור בפורמט הבא:

```
VISUAL QA APPROVAL
==================
DATE:         YYYY-MM-DD
REVIEWER:     [שם הבודק]
BATCH:        [תיאור ה-batch / שם הריצה]

SAMPLE REVIEWED:
  clothing:   [מספר שנבדקו] / 12
  shoes:      [מספר שנבדקו] / 4  (או N/A)
  anomaly:    [מספר שנבדקו] / 2
  comparison: [מספר שנבדקו] / 2  (או N/A)

CHECK RESULTS:
  A - Technical Fingerprint:  PASS / FAIL
  B - Type Consistency:       PASS / FAIL
  C - Template Repetition:    PASS / FAIL
  D - Description Bleed:      PASS / FAIL
  E - Fabricated Claim:       PASS / FAIL
  F - Geo Comparison:         PASS / FAIL / N/A
  G - Anomaly Exclusion:      PASS / FAIL
  H - Human Feel:             PASS / FAIL

BLOCKERS:     [תיאור חוסמים אם קיימים, או "אין"]

VERDICT:      PASS / FAIL
PUSH ALLOWED: YES / NO

SIGNATURE:    [שם + תאריך]
```

---

## STOP RULE

**אם Visual QA מזהה אחד מהבאים — אין push:**

| ממצא | פעולה |
|---|---|
| Technical fingerprint (Check A) | עצירה מיידית — חזרה ל-generator |
| Type mismatch (Check B) | עצירה — בדיקת context + regeneration |
| Template repetition בולט (Check C) | עצירה — בדיקת generator logic |
| Description bleed (Check D) | עצירה — זיהוי מקור ה-bleed |
| Fabricated claim (Check E) | עצירה — הסרת הטענה + regeneration |
| Anomaly PID ב-bundle (Check G) | עצירה מיידית — הסרה ידנית מה-bundle |
| 3+ מוצרים נכשלים ב-Check H | עצירה — בדיקת איכות כללית לפני המשך |

**כלל על-כולם:** PUSH ALLOWED: YES מופיע **רק** אם כל 8 ה-checks הם PASS (או N/A כשרלוונטי). כל FAIL אחד = PUSH ALLOWED: NO.

---

*VISUAL QA CHECKLIST v1 — BabyMania Layer 4 — P1-S5 / AUTOMATION-HARDENING-PLAN v1*
*מסמך חובה לפני push — אין לדלג עליו בשום תנאי*
