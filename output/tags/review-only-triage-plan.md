# REVIEW_ONLY Triage Plan — BabyMania

**תאריך:** 2026-05-10  
**מצב:** READ-ONLY PLANNING  
**pool:** ~133 מוצרים REVIEW_ONLY (מPhase 7C Long-Run Plan, 2026-05-06)  
**מוצרים ידועים:** 2 מ-Batch 10 (PIDs: 9096636825913, 9605887689017)

---

## 1. קטגוריות Triage

### קטגוריה 1: approve_for_tagging

**תיאור:** מוצר ברור, ניתן לתייג ישירות ללא ראיית תמונה.  
**קריטריונים:**
- כותרת ברורה + עברית מפורשת (למשל: "שמלת ילדה חגיגית")
- אין מילות false-positive ידועות
- סוג מוצר ביגוד ברור: שמלה, סרבל, סט, כובע, מעיל

**דוגמאות:**
- "שמלת פרחים לתינוקת" → type-dress + gender-girl
- "מעיל חורף לתינוק בנים" → type-coat + gender-boy
- "סט לידה לבנות" → type-set + gender-girl + occ-gift

**פעולה:** כלול בbatch planning ישירות. אין צורך בimage review.

**תגים אפשריים:** type-*, gender-*, occ-*

---

### קטגוריה 2: image_review_needed

**תיאור:** מוצר שנראה כביגוד אך כותרת לא ברורה מספיק — תמונה תפתור.  
**קריטריונים:**
- כותרת באנגלית גנרית ("Baby Girls Clothing Set", "Newborn Romper")
- יש מילות ביגוד אך גם אמביוולנטיות (למשל: "set" בלי פירוט)
- כותרת מעורבת — עברית וביגוד אך לא ברור gender/type

**דוגמאות:**
- "Baby Girls Cute Romper 2024" — ייתכן type-romper, gender-girl, אבל צריך אישור תמונה
- "Newborn Set Summer" — type-set? צריך תמונה

**פעולה:** שלח לimage review agent (vision). המתן לconfidence HIGH/MEDIUM לפני batch.

---

### קטגוריה 3: manual_review_needed

**תיאור:** מוצר מיוחד שדורש שיפוט אנושי — אוטומציה לא תספיק.  
**קריטריונים:**
- כותרת סותרת (נעל + ביגוד, בובה + ביגוד)
- מוצר ייחודי שלא נכנס לאף קטגוריה taxonomy קיימת
- מוצר שנראה שייך לקטגוריה עתידית (bath, feeding) אך לא ברור

**דוגמאות:**
- "Baby Reborn Doll Clothes Set" — האם ביגוד לבובה? לא לתייג עם type-set
- "Newborn Gift Basket with Romper and Toy" — מארז מעורב

**פעולה:** Human review — אייל מחליט. אסור לתייג אוטומטית.

---

### קטגוריה 4: reject_not_relevant

**תיאור:** מוצר שלא שייך לביגוד/נעליים — false positive ידוע.  
**קריטריונים:**
- מוצר שחמק מfalsep positive blocking: אמבטיה, צעצוע, מזון, ציוד
- מוצר ARCHIVED/DRAFT שחמק מהסינון
- מוצר עם template_suffix="shoes" אך הוא לא נעל ולא ביגוד

**דוגמאות:**
- אמבטיה לתינוק עם מד טמפרטורה → reject (cat-bath future)
- אוניברסיטה לתינוק (צעצוע) → reject
- BabySleep Pro (מוצר שינה) → reject

**פעולה:** הוסף לfalsep positive block list. אין תיוג. עדכן באוטומציה.

---

### קטגוריה 5: future_category_candidate

**תיאור:** מוצר ביגוד/מוצר תינוק ממשי אבל שייך לקטגוריה שלא קיימת בtaxonomy הנוכחי.  
**קריטריונים:**
- מוצר תקין אך סוגו לא נכלל בtype-* הקיימים
- שייך לקטגוריה עתידית: שמיכה (textile), אמבטיה (bath), כלי האכלה (feeding)
- אין תג ביגוד מתאים עדיין

**דוגמאות:**
- שמיכת תינוק (טקסטיל) → future: cat-textile
- בקבוק תינוק → future: cat-feeding
- כרית/מצעים → future: cat-textile

**פעולה:** תעד ב-future-smart-collections-proposal.md. אין תיוג עכשיו. הוסף ל-backlog.

---

## 2. Batch Workflow — 20 מוצרים לbatch

```
STEP 1: שלוף 20 מוצרים מpool REVIEW_ONLY
STEP 2: Triage אוטומטי לפי keywords → קטגוריות 1–5
STEP 3: approve_for_tagging → dry run → T3 approval → live write → verify
STEP 4: image_review_needed → image review agent → confidence check → dry run → T3 approval → live write → verify
STEP 5: manual_review_needed → Human queue (Ayal)
STEP 6: reject_not_relevant → update false positive list
STEP 7: future_category_candidate → document, no action
STEP 8: עדכן organic-journal.md + מצב-הפרויקט-האורגני.md
STEP 9: הבא batch
```

**גודל batch:** 20 → audit → image review → dry run → approval → live write → verify

---

## 3. כללי הכנסה לbatch

| בדיקה | כלל |
|---|---|
| אין age-* tags | חסימה |
| אין type collision | חסימה |
| אין gender collision | חסימה |
| אין EU shoe size | חסימה |
| אין keywords ידועים של false positive | חסימה |
| confidence HIGH מimage review | דרישה לimage_review_needed |
| אין overlap עם batches קודמים | חסימה |

---

## 4. false positive keywords לעדכון (מ-Batch 10)

רשימה זו לעדכון בscanner לפני הרצת triage:

```python
FALSE_POSITIVE_ADDITIONAL = [
    "swimsuit", "swim", "ביגוד ים",
    "brush", "מברשות",
    "potty", "toilet", "סיר",
    "formula", "powder", "storage", "container",
    "postpartum", "belly-band", "corset",
    "שמיכות",  # plural — שמיכה alone might be OK in context
    "spinner", "toy", "toys",
    "טטרה",     # muslin bib
    "שמיכ",    # prefix match for שמיכה/שמיכות
    "ספינר",
]
```

---

## 5. מוצרים ידועים מ-Batch 10

| PID | כותרת חלקית | הערה |
|---|---|---|
| 9096636825913 | לא ידוע (REVIEW_ONLY מBatch 10) | human review נדרש |
| 9605887689017 | לא ידוע (REVIEW_ONLY מBatch 10) | human review נדרש |

שני מוצרים אלה עברו לREVIEW_ONLY אחרי שנמצאו כ-manual_review_needed ב-Batch 10 business audit.

---

*מסמך זה הוא תוכנית בלבד. אין כתיבות Shopify ללא T3 approval.*
