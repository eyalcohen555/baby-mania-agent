# REBORN-MASTER-PROMPT
## מסמך שליטה — קטגוריית ריבורן | BabyMania
### גרסה: 1.0 | נוצר: 2026-04-24 | סטטוס: PLANNING

---

## ⚠️ כפיפות מערכת

**מסמך זה כפוף ל: `BABYMANIA-MASTER-PROMPT.md`**

כל חוקי המערכת הכלליים של BabyMania — Bridge, Approval Tiers, שכבות, כללי PASS/FAIL — חלים במלואם על פרויקט ריבורן.
אין ארכיטקטורה נפרדת. אין מערכת עצמאית. ריבורן = קטגוריה נוספת בתוך BabyMania.

```
REBORN-MASTER-PROMPT.md  ←  כפוף ל  ←  BABYMANIA-MASTER-PROMPT.md
```

---

## 🎯 סקופ — מה כולל פרויקט ריבורן

**כולל:**
- דף נחיתה (Landing Page) לקטגוריית ריבורן
- דפי מוצר אישיים ל-6 בובות ריבורן הקיימות

**לא כולל — אסור לגעת:**
- אורגני (HUBs, blog, articles) — נוהל נפרד לחלוטין
- נעליים (Shoes pipeline) — בייצור פעיל
- ביגוד (Clothing pipeline) — בייצור פעיל
- תיקוני live/bug — מחוץ לסקופ
- שינויים ב-Bridge, Team Lead, Watchdog
- כל Shopify live ללא T3 + אישור אייל

---

## 📐 כללי מערכת — חובה

### סדר שכבות

```
DATA → LOGIC → OUTPUT
```

אין output לפני verified product truth.
אין הבטחות ללא עדות מוצר/ספק.
אין ערבוב בין זוויות: טיפול/מבוגרים/דמנציה ← **אסור** בדף הראשי (ילדים/מתנות).

### כללי PASS / FAIL

```
אין "בערך טוב" | אין "כנראה עובד" | אין דילוג שכבות
```

| כלל | הפרה = |
|-----|--------|
| אמת מוצרית לפני קופי | FAIL |
| ספציפי, לא גנרי | FAIL |
| הבטחה = רק אם יש ראיה | FAIL |
| DATA לפני OUTPUT | FAIL |

### מתי לעצור ולשאול אייל

- כל החלטה ארכיטקטונית על הדף
- כל נגיעה ב-Shopify live
- הוספת זווית שיווקית חדשה שלא אושרה
- פיצול או איחוד קטגוריות ריבורן
- כישלון חוזר 3 פעמים

---

## 📁 קבצי הפרויקט

| קובץ | תפקיד |
|------|--------|
| `docs/product/reborn/REBORN-MASTER-PROMPT.md` | מסמך זה — שליטה + חוקים |
| `docs/product/reborn/reborn-product-page-state.md` | מצב תפעולי + כיוון מאושר |
| `docs/product/reborn/reborn-task-checklist.md` | צ'ק ליסט שלבים + פריטים |
| `docs/product/reborn/reborn-first-summary-report.md` | דוח מחקר שוק ראשון — reference input בלבד |
| `docs/product/reborn/reborn-product-truth-collection.md` | אמת מוצרית מהספקית — מקור יחיד לקופי |
| `docs/product/reborn/reborn-marketing-inputs.md` | קלטי שיווק גולמיים — ממתינים לעיבוד PHASE 6 |

---

## 🤖 סוכני ריבורן — תכנון עתידי בלבד

**אין לבנות סוכנים לפני שיש:**
1. היררכיית דף מאושרת
2. אמת מוצרית מאומתת
3. מבנה נתונים ברור

**סוכנים מתוכננים (עתידי):**
- Reborn Intelligence — זיהוי חומר, גודל, שיער, עיניים, אביזרים
- Reborn Positioning — בחירת זווית לפי סוג הבובה
- Reborn Benefits — כתיבת יתרונות לפי אווטאר
- Reborn Sections — יצירת סקשנים לדפי מוצר
- Reborn FAQ — שאלות לפי התנגדויות
- Reborn Validator — בדיקת הבטחות שקריות
- Reborn Publisher — פרסום (עתידי, אם ישולב במערכת)

---

## 🔄 חוק עדכון הקובץ הזה

עדכן אחרי: milestone נסגר | החלטה ארכיטקטונית | agent חדש | לפני handoff.
שינויים שוטפים → `reborn-product-page-state.md`.

---

*כפוף ל-BABYMANIA-MASTER-PROMPT.md בכל עת.*
